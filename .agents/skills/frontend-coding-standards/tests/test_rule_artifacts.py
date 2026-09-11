"""Public-artifact checks for the frontend coding-standards rule source."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, relative_path: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {relative_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class RuleArtifactTests(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
