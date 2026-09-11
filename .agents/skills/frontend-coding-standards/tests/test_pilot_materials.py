"""Public-artifact checks for pilot acceptance and release governance."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, relative_path: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {relative_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PilotMaterialTests(unittest.TestCase):
    def test_pilot_materials_cover_required_behaviour_and_governance(self):
        validator = load_module("validate_pilot", "scripts/validate_pilot.py")

        errors = validator.validate_bundle(ROOT)

        self.assertEqual([], errors)

    def test_checked_in_pilot_view_is_generated_from_structured_material(self):
        generator = load_module("generate_pilot_view", "scripts/generate_pilot_view.py")

        with tempfile.TemporaryDirectory() as temp_dir:
            generated_path = Path(temp_dir) / "PILOT.md"
            generator.generate(ROOT / "pilot.yaml", generated_path)

            self.assertEqual(
                (ROOT / "PILOT.md").read_text(encoding="utf-8"),
                generated_path.read_text(encoding="utf-8"),
            )

    def test_project_override_rejects_global_rule_mutation(self):
        validator = load_module("validate_rules_for_override", "scripts/validate_rules.py")
        invalid_override = {
            "schema_version": 1,
            "rule_version": "0.0.1",
            "project": "example-vue3-app",
            "overrides": [
                {
                    "rule_id": "FCS-007",
                    "operation": "replace_rule",
                    "reason": "项目希望改写全局规则。",
                    "owner": "project-frontend-owner",
                }
            ],
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            override_path = Path(temp_dir) / "overrides.yaml"
            override_path.write_text(
                yaml.safe_dump(invalid_override, allow_unicode=True),
                encoding="utf-8",
            )

            errors = validator.validate_overrides(override_path, ROOT / "rules.yaml")

        self.assertTrue(any("operation" in error for error in errors))

    def test_project_override_rejects_embedded_global_rule_fields(self):
        validator = load_module("validate_rules_for_global_fields", "scripts/validate_rules.py")
        invalid_override = {
            "schema_version": 1,
            "rule_version": "0.0.1",
            "project": "example-vue3-app",
            "rules": [],
            "overrides": [
                {
                    "rule_id": "FCS-007",
                    "operation": "downgrade_to_guidance",
                    "reason": "项目工具暂时无法对齐。",
                    "owner": "project-frontend-owner",
                }
            ],
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            override_path = Path(temp_dir) / "overrides.yaml"
            override_path.write_text(
                yaml.safe_dump(invalid_override, allow_unicode=True),
                encoding="utf-8",
            )

            errors = validator.validate_overrides(override_path, ROOT / "rules.yaml")

        self.assertTrue(any("forbidden top-level" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
