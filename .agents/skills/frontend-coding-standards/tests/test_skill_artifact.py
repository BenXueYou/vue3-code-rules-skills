"""Public-behaviour checks for the workspace-pilot Skill instructions."""

from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_PATH = ROOT / "SKILL.md"


class SkillArtifactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill = SKILL_PATH.read_text(encoding="utf-8")

    def test_skill_is_discoverable_for_explicit_and_vue3_code_tasks(self):
        self.assertIn("name: frontend-coding-standards", self.skill)
        self.assertIn("$frontend-coding-standards", self.skill)
        self.assertIn("Vue 3", self.skill)
        self.assertIn("自动匹配", self.skill)
        for file_type in (".vue", ".ts", ".js", ".css", ".less", ".scss"):
            self.assertIn(file_type, self.skill)

    def test_skill_applies_only_active_rules_to_touched_code(self):
        self.assertIn("rules.yaml", self.skill)
        self.assertIn("状态为 `ACTIVE`", self.skill)
        self.assertIn("`MUST`", self.skill)
        self.assertIn("`GUIDANCE`", self.skill)
        self.assertIn("`PENDING`", self.skill)
        self.assertIn("必须依赖某条 PENDING 规则", self.skill)
        self.assertIn("请求澄清", self.skill)
        self.assertIn("触及代码", self.skill)
        self.assertIn("存量规范债务", self.skill)
        self.assertIn("不自动", self.skill)

    def test_skill_preserves_project_configuration_without_explicit_authorization(self):
        self.assertIn("接入规范", self.skill)
        self.assertIn("覆盖工程格式", self.skill)
        self.assertIn("ESLint", self.skill)
        self.assertIn("Prettier", self.skill)
        self.assertIn("Stylelint", self.skill)
        self.assertIn("仅对触及代码", self.skill)
        self.assertIn("工具无法", self.skill)
        self.assertIn("限定文件范围", self.skill)
        self.assertIn("单独授权", self.skill)

    def test_skill_requires_scoped_existing_validation_and_delivery_feedback(self):
        self.assertIn("不临时安装依赖", self.skill)
        self.assertIn("rules.yaml` 的 `version`", self.skill)
        self.assertIn("触发方式", self.skill)
        self.assertIn("已运行校验", self.skill)
        self.assertIn("未执行校验", self.skill)

    def test_skill_records_a_reviewable_validation_and_delivery_record(self):
        self.assertIn("package.json", self.skill)
        self.assertIn("通过", self.skill)
        self.assertIn("失败", self.skill)
        self.assertIn("未执行", self.skill)
        self.assertIn("交付反馈模板", self.skill)
        self.assertIn("试点成熟度", self.skill)


if __name__ == "__main__":
    unittest.main()
