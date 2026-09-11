"""Validate pilot acceptance coverage, governance, and linked artifacts."""

from __future__ import annotations

import importlib.util
import sys
import tempfile
from pathlib import Path
from typing import Any

import yaml


REQUIRED_CAPABILITIES = {
    "explicit_trigger",
    "automatic_trigger",
    "touched_code_only",
    "pending_not_executed",
    "rule_strength",
    "conflict_priority",
    "format_override_authorization",
    "full_repo_migration_authorization",
    "rule_source_and_reading_view",
    "project_override_structure",
}
RELEASE_PATH = ["0.0.1", "0.1.0", "1.0.0"]
RELEASE_CHANNELS = ["workspace-pilot", "local-default", "team-plugin"]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def non_empty_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_bundle(root: Path) -> list[str]:
    errors: list[str] = []
    pilot_path = root / "pilot.yaml"
    try:
        document = yaml.safe_load(pilot_path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as error:
        return [f"Unable to read pilot source: {error}"]
    if not isinstance(document, dict):
        return ["Pilot source must be a mapping."]
    if document.get("schema_version") != 1:
        errors.append("schema_version must be 1.")

    rule_source = root / str(document.get("rule_source", ""))
    reading_view = root / str(document.get("reading_view", ""))
    override_example = root / str(document.get("project_override_example", ""))
    try:
        rules_document = yaml.safe_load(rule_source.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as error:
        return errors + [f"Unable to read linked rule source: {error}"]
    if not isinstance(rules_document, dict):
        return errors + ["Linked rule source must be a mapping."]
    if document.get("rule_version") != rules_document.get("version"):
        errors.append("Pilot rule_version must match rules.yaml version.")

    acceptance = document.get("acceptance")
    if not isinstance(acceptance, dict):
        errors.append("acceptance must be a mapping.")
    else:
        allowed_statuses = acceptance.get("allowed_statuses")
        if allowed_statuses != ["NOT_RUN", "PASS", "FAIL", "BLOCKED"]:
            errors.append("acceptance allowed_statuses must define the four review states.")
        if not non_empty_text(acceptance.get("evidence_policy")):
            errors.append("acceptance evidence_policy must be non-empty.")
        scenarios = acceptance.get("scenarios")
        if not isinstance(scenarios, list):
            errors.append("acceptance scenarios must be a list.")
        else:
            ids: set[str] = set()
            capabilities: set[str] = set()
            for index, scenario in enumerate(scenarios, start=1):
                label = f"Scenario #{index}"
                if not isinstance(scenario, dict):
                    errors.append(f"{label} must be a mapping.")
                    continue
                scenario_id = scenario.get("id")
                if not non_empty_text(scenario_id) or scenario_id in ids:
                    errors.append(f"{label} id must be non-empty and unique.")
                else:
                    ids.add(scenario_id)
                capability = scenario.get("capability")
                if non_empty_text(capability):
                    capabilities.add(capability)
                if scenario.get("status") not in (allowed_statuses or []):
                    errors.append(f"{label} has an invalid status.")
                for field in ("setup", "action"):
                    if not non_empty_text(scenario.get(field)):
                        errors.append(f"{label} {field} must be non-empty.")
                if not isinstance(scenario.get("expected"), list) or not scenario["expected"]:
                    errors.append(f"{label} expected must be a non-empty list.")
                evidence = scenario.get("evidence")
                if not isinstance(evidence, list):
                    errors.append(f"{label} evidence must be a list.")
                elif scenario.get("status") == "PASS" and not evidence:
                    errors.append(f"{label} PASS requires evidence.")
            missing = REQUIRED_CAPABILITIES - capabilities
            if missing:
                errors.append(f"Acceptance coverage is missing: {', '.join(sorted(missing))}.")

    governance = document.get("governance")
    if not isinstance(governance, dict):
        errors.append("governance must be a mapping.")
    else:
        if governance.get("release_path") != RELEASE_PATH:
            errors.append("release_path must be 0.0.1 -> 0.1.0 -> 1.0.0.")
        releases = governance.get("releases")
        if not isinstance(releases, list) or [r.get("version") for r in releases if isinstance(r, dict)] != RELEASE_PATH:
            errors.append("governance releases must define every version in release_path order.")
        else:
            for release, channel in zip(releases, RELEASE_CHANNELS, strict=True):
                version = release["version"]
                if release.get("channel") != channel:
                    errors.append(f"Release {version} must use channel {channel}.")
                for field in ("change_approver", "release_owner"):
                    if not non_empty_text(release.get(field)):
                        errors.append(f"Release {version} {field} must be non-empty.")
                for field in ("entry_criteria", "exit_criteria"):
                    if not isinstance(release.get(field), list) or not release[field]:
                        errors.append(f"Release {version} {field} must be a non-empty list.")
            if releases[0].get("change_approver") != "local-maintainer":
                errors.append("0.0.1 changes must be approved by the local maintainer.")
            if releases[2].get("change_approver") != "designated-frontend-lead":
                errors.append("1.0.0 changes must be approved by the designated frontend lead.")
            if releases[2].get("release_owner") != "designated-frontend-lead":
                errors.append("1.0.0 releases must be owned by the designated frontend lead.")
        maintenance = governance.get("maintenance")
        if not isinstance(maintenance, dict):
            errors.append("governance maintenance must be a mapping.")
        else:
            required_roles = {
                "pilot_rule_owner": "local-maintainer",
                "team_change_approver": "designated-frontend-lead",
                "team_release_owner": "designated-frontend-lead",
            }
            for field, expected in required_roles.items():
                if maintenance.get(field) != expected:
                    errors.append(f"maintenance {field} must be {expected}.")
            if not non_empty_text(maintenance.get("contributor_policy")):
                errors.append("maintenance contributor_policy must be non-empty.")

    rule_validator = load_module("pilot_rule_validator", root / "scripts" / "validate_rules.py")
    errors.extend(f"rules.yaml: {error}" for error in rule_validator.validate(rule_source))
    errors.extend(
        f"overrides.example.yaml: {error}"
        for error in rule_validator.validate_overrides(override_example, rule_source)
    )
    rules_generator = load_module("pilot_rules_generator", root / "scripts" / "generate_rules_view.py")
    pilot_generator = load_module("pilot_view_generator", root / "scripts" / "generate_pilot_view.py")
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            generated_rules_path = Path(temp_dir) / "RULES.md"
            rules_generator.generate(rule_source, generated_rules_path)
            if reading_view.read_text(encoding="utf-8") != generated_rules_path.read_text(encoding="utf-8"):
                errors.append("RULES.md must match the view generated from rules.yaml.")
            generated_pilot_path = Path(temp_dir) / "PILOT.md"
            pilot_generator.generate(pilot_path, generated_pilot_path)
            if (root / "PILOT.md").read_text(encoding="utf-8") != generated_pilot_path.read_text(encoding="utf-8"):
                errors.append("PILOT.md must match the view generated from pilot.yaml.")
    except OSError as error:
        errors.append(f"Unable to compare generated views: {error}")
    return errors


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parents[1]
    errors = validate_bundle(root)
    if errors:
        print("Pilot material validation failed:")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    print(f"Pilot materials are valid: {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
