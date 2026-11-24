"""校验前端编码规范规则真源及项目例外配置的可移植结构。"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import yaml


# 单条规则必须具备的完整字段集合。
REQUIRED_RULE_FIELDS = {
    "id",
    "status",
    "strength",
    "applies_to",
    "rule",
    "decision_criteria",
    "exceptions",
    "sources",
}
VALID_STATUSES = {"ACTIVE", "PENDING"}
VALID_STRENGTHS = {"MUST", "VERIFY", "GUIDANCE"}
RULE_ID_PATTERN = re.compile(r"^FCS-\d{3}$")
VALID_OVERRIDE_OPERATIONS = {"add_exception", "downgrade_to_guidance"}
OVERRIDE_DOCUMENT_FIELDS = {"schema_version", "rule_version", "project", "overrides"}
OVERRIDE_FIELDS = {"rule_id", "operation", "reason", "owner", "exception"}


def validate(source_path: Path) -> list[str]:
    """校验一个规则真源文件，并返回便于人工阅读的全部错误。"""
    try:
        document = yaml.safe_load(source_path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as error:
        return [f"Unable to read rule source: {error}"]

    errors: list[str] = []
    if not isinstance(document, dict):
        return ["Rule source must be a mapping."]

    if not isinstance(document.get("version"), str) or not document["version"].strip():
        errors.append("Top-level version must be a non-empty string.")
    if not isinstance(document.get("metadata"), dict):
        errors.append("Top-level metadata must be a mapping.")

    rules = document.get("rules")
    if not isinstance(rules, list) or not rules:
        return errors + ["Top-level rules must be a non-empty list."]

    # 单次遍历同时检查字段完整性、规则 ID 唯一性和各字段的数据类型。
    seen_ids: set[str] = set()
    for index, rule in enumerate(rules, start=1):
        label = f"Rule #{index}"
        if not isinstance(rule, dict):
            errors.append(f"{label} must be a mapping.")
            continue

        missing = REQUIRED_RULE_FIELDS - rule.keys()
        if missing:
            errors.append(f"{label} is missing fields: {', '.join(sorted(missing))}.")

        rule_id = rule.get("id")
        if not isinstance(rule_id, str) or not RULE_ID_PATTERN.fullmatch(rule_id):
            errors.append(f"{label} id must match FCS-000.")
        elif rule_id in seen_ids:
            errors.append(f"Rule id {rule_id} is duplicated.")
        else:
            seen_ids.add(rule_id)

        if rule.get("status") not in VALID_STATUSES:
            errors.append(f"{label} has an invalid status.")
        if rule.get("strength") not in VALID_STRENGTHS:
            errors.append(f"{label} has an invalid strength.")
        if not isinstance(rule.get("applies_to"), list) or not rule["applies_to"]:
            errors.append(f"{label} applies_to must be a non-empty list.")

        for field in ("rule", "decision_criteria", "exceptions"):
            if not isinstance(rule.get(field), str) or not rule[field].strip():
                errors.append(f"{label} {field} must be a non-empty string.")

        sources = rule.get("sources")
        if not isinstance(sources, dict):
            errors.append(f"{label} sources must be a mapping.")
            continue
        markdown = sources.get("markdown")
        pdf = sources.get("pdf")
        references = sources.get("references")
        if not isinstance(markdown, dict) or not all(
            isinstance(markdown.get(key), str) and markdown[key].strip()
            for key in ("file", "section")
        ):
            errors.append(f"{label} must cite a Markdown file and section.")
        if "pdf" not in sources and "references" not in sources:
            errors.append(f"{label} must cite a PDF file or reference documents.")
        if "pdf" in sources:
            if not isinstance(pdf, dict) or not isinstance(pdf.get("file"), str) or not pdf["file"].strip():
                errors.append(f"{label} must cite a PDF file.")
            elif not isinstance(pdf.get("pages"), list) or not pdf["pages"] or not all(
                isinstance(page, int) and page > 0 for page in pdf["pages"]
            ):
                errors.append(f"{label} must cite one or more positive PDF page numbers.")
        if "references" in sources:
            if not isinstance(references, list) or not references:
                errors.append(f"{label} references must be a non-empty list.")
            else:
                for reference in references:
                    if not isinstance(reference, dict) or not all(
                        isinstance(reference.get(key), str) and reference[key].strip()
                        for key in ("title", "url")
                    ):
                        errors.append(f"{label} references must have a title and URL.")
                        continue
                    try:
                        url = urlparse(reference["url"])
                        valid_url = url.scheme == "https" and bool(url.hostname)
                    except ValueError:
                        valid_url = False
                    if not valid_url:
                        errors.append(f"{label} reference URL must be an absolute HTTPS URL.")

    return errors


def validate_overrides(override_path: Path, source_path: Path) -> list[str]:
    """校验项目级例外，并确保例外不会修改全局规则定义。"""
    try:
        override_document = yaml.safe_load(override_path.read_text(encoding="utf-8"))
        rule_document = yaml.safe_load(source_path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as error:
        return [f"Unable to read override material: {error}"]

    if not isinstance(override_document, dict):
        return ["Override source must be a mapping."]
    errors: list[str] = []
    # 使用字段白名单限制例外文件的能力边界，避免借此改写全局配置。
    unknown_document_fields = set(override_document) - OVERRIDE_DOCUMENT_FIELDS
    if unknown_document_fields:
        errors.append(
            "Override source contains forbidden top-level fields: "
            f"{', '.join(sorted(unknown_document_fields))}."
        )
    if not isinstance(rule_document, dict):
        return errors + ["Rule source must be a mapping."]
    if override_document.get("schema_version") != 1:
        errors.append("schema_version must be 1.")
    if override_document.get("rule_version") != rule_document.get("version"):
        errors.append("rule_version must match rules.yaml version.")
    if not isinstance(override_document.get("project"), str) or not override_document["project"].strip():
        errors.append("project must be a non-empty string.")

    rules = rule_document.get("rules", []) if isinstance(rule_document, dict) else []
    # 项目例外只能引用已启用规则，PENDING 规则仍需先完成全局决策。
    active_rule_ids = {
        rule.get("id")
        for rule in rules
        if isinstance(rule, dict) and rule.get("status") == "ACTIVE"
    }
    overrides = override_document.get("overrides")
    if not isinstance(overrides, list) or not overrides:
        return errors + ["overrides must be a non-empty list."]

    seen_ids: set[str] = set()
    for index, override in enumerate(overrides, start=1):
        label = f"Override #{index}"
        if not isinstance(override, dict):
            errors.append(f"{label} must be a mapping.")
            continue
        unknown_fields = set(override) - OVERRIDE_FIELDS
        if unknown_fields:
            errors.append(f"{label} contains forbidden fields: {', '.join(sorted(unknown_fields))}.")
        rule_id = override.get("rule_id")
        if rule_id not in active_rule_ids:
            errors.append(f"{label} rule_id must reference an ACTIVE global rule.")
        elif rule_id in seen_ids:
            errors.append(f"{label} duplicates rule_id {rule_id}.")
        else:
            seen_ids.add(rule_id)
        operation = override.get("operation")
        if operation not in VALID_OVERRIDE_OPERATIONS:
            errors.append(
                f"{label} operation must be add_exception or downgrade_to_guidance."
            )
        for field in ("reason", "owner"):
            if not isinstance(override.get(field), str) or not override[field].strip():
                errors.append(f"{label} {field} must be a non-empty string.")
        if operation == "add_exception":
            if not isinstance(override.get("exception"), str) or not override["exception"].strip():
                errors.append(f"{label} add_exception requires a non-empty exception.")
        elif "exception" in override:
            errors.append(f"{label} downgrade_to_guidance must not define exception.")

    return errors


def main() -> int:
    """校验指定规则文件，并通过退出码报告结果。"""
    source_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parents[1] / "rules.yaml"
    errors = validate(source_path)
    if errors:
        print("Rule source validation failed:")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    print(f"Rule source is valid: {source_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
