"""根据 pilot.yaml 生成只读的试点验收与版本治理文档。"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml


def generate(source_path: Path, output_path: Path) -> None:
    """读取试点配置，并将验收场景及治理信息渲染为 Markdown。"""
    document: dict[str, Any] = yaml.safe_load(source_path.read_text(encoding="utf-8"))
    acceptance = document["acceptance"]
    governance = document["governance"]
    lines = [
        "# 前端编码规范试点验收与版本治理",
        "",
        "> 此文件由 `pilot.yaml` 自动生成，仅供执行验收与评审。请勿直接编辑。",
        "",
        f"- 规则版本：`{document['rule_version']}`",
        f"- 规则真源：`{document['rule_source']}`",
        f"- 规则阅读视图：`{document['reading_view']}`",
        f"- 项目例外样例：`{document['project_override_example']}`",
        "",
        "## 验收记录规则",
        "",
        f"- 可用状态：{', '.join(acceptance['allowed_statuses'])}",
        f"- 证据要求：{acceptance['evidence_policy']}",
        "",
        "## 验收场景",
        "",
    ]
    # 每个验收场景独立成节，便于评审时逐项核对状态、预期和证据。
    for scenario in acceptance["scenarios"]:
        lines.extend(
            [
                f"### {scenario['id']} — {scenario['capability']}",
                "",
                f"- 状态：`{scenario['status']}`",
                f"- 准备：{scenario['setup']}",
                f"- 操作：{scenario['action']}",
                "- 预期：",
                *[f"  - {item}" for item in scenario["expected"]],
                "- 证据：",
                *([f"  - {item}" for item in scenario["evidence"]] or ["  - 无"]),
                "",
            ]
        )

    # 按配置中的发布顺序输出版本路径，保留各阶段的职责与准入、退出条件。
    lines.extend(["## 版本路径", ""])
    for release in governance["releases"]:
        lines.extend(
            [
                f"### {release['version']} — {release['channel']}",
                "",
                f"- 规则变更审批：`{release['change_approver']}`",
                f"- 发布负责人：`{release['release_owner']}`",
                "- 进入条件：",
                *[f"  - {item}" for item in release["entry_criteria"]],
                "- 退出条件：",
                *[f"  - {item}" for item in release["exit_criteria"]],
                "",
            ]
        )
    maintenance = governance["maintenance"]
    lines.extend(
        [
            "## 维护权",
            "",
            f"- 试点规则维护：`{maintenance['pilot_rule_owner']}`",
            f"- 团队规则变更审批：`{maintenance['team_change_approver']}`",
            f"- 团队发布：`{maintenance['team_release_owner']}`",
            f"- 成员建议：{maintenance['contributor_policy']}",
            "",
        ]
    )
    output_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    """解析可选输入、输出路径，并执行文档生成。"""
    # 默认以 skill 根目录中的真源和阅读视图为输入、输出。
    root = Path(__file__).parents[1]
    source_path = Path(sys.argv[1]) if len(sys.argv) > 1 else root / "pilot.yaml"
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else root / "PILOT.md"
    generate(source_path, output_path)
    print(f"Generated {output_path} from {source_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
