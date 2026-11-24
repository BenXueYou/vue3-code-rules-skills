"""Public-artifact checks for the frontend coding-standards rule source."""

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


class RuleArtifactTests(unittest.TestCase):
    def validate_with_sources(self, sources):
        validator = load_module("validate_rule_sources", "scripts/validate_rules.py")
        document = yaml.safe_load((ROOT / "rules.yaml").read_text(encoding="utf-8"))
        document["rules"] = [dict(document["rules"][0], sources=sources)]
        with tempfile.TemporaryDirectory() as temp_dir:
            source_path = Path(temp_dir) / "rules.yaml"
            source_path.write_text(
                yaml.safe_dump(document, allow_unicode=True),
                encoding="utf-8",
            )
            return validator.validate(source_path)

    def test_rule_source_has_a_valid_traceable_structure(self):
        validator = load_module("validate_rules", "scripts/validate_rules.py")

        errors = validator.validate(ROOT / "rules.yaml")

        self.assertEqual([], errors)

    def test_checked_in_reading_view_is_generated_from_rule_source(self):
        generator = load_module("generate_rules_view", "scripts/generate_rules_view.py")

        with tempfile.TemporaryDirectory() as temp_dir:
            generated_path = Path(temp_dir) / "RULES.md"
            generator.generate(ROOT / "rules.yaml", generated_path)

            self.assertEqual(
                (ROOT / "RULES.md").read_text(encoding="utf-8"),
                generated_path.read_text(encoding="utf-8"),
            )

    def test_supplemental_rule_can_cite_markdown_and_reference_without_pdf(self):
        sources = {
            "markdown": {"file": "requirements.md", "section": "新增需求"},
            "references": [
                {"title": "W3C APG", "url": "https://www.w3.org/WAI/ARIA/apg/"}
            ],
        }

        self.assertEqual([], self.validate_with_sources(sources))

        generator = load_module("generate_reference_view", "scripts/generate_rules_view.py")
        rendered = generator.format_source(sources)
        self.assertIn("requirements.md", rendered)
        self.assertIn("[W3C APG](https://www.w3.org/WAI/ARIA/apg/)", rendered)
        self.assertNotIn("PDF:", rendered)

    def test_rule_without_pdf_or_reference_is_rejected(self):
        errors = self.validate_with_sources(
            {"markdown": {"file": "requirements.md", "section": "新增需求"}}
        )

        self.assertTrue(any("PDF file or reference" in error for error in errors))

    def test_malformed_references_are_rejected(self):
        for references in (
            [],
            [{}],
            [{"title": "W3C APG", "url": "relative/path"}],
            [{"title": "W3C APG", "url": "https://[invalid"}],
        ):
            with self.subTest(references=references):
                errors = self.validate_with_sources(
                    {
                        "markdown": {"file": "requirements.md", "section": "新增需求"},
                        "references": references,
                    }
                )

                self.assertTrue(errors)

    def test_reference_does_not_hide_invalid_pdf_evidence(self):
        errors = self.validate_with_sources(
            {
                "markdown": {"file": "requirements.md", "section": "新增需求"},
                "pdf": {"file": "evidence.pdf", "pages": []},
                "references": [
                    {"title": "W3C APG", "url": "https://www.w3.org/WAI/ARIA/apg/"}
                ],
            }
        )

        self.assertTrue(any("PDF page numbers" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
