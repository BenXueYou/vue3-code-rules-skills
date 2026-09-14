"""根据 rules.yaml 生成只读的规则 Markdown 阅读视图。"""

from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

import yaml


def format_source(source: dict[str, Any]) -> str:
    """将规则的 Markdown 与 PDF 来源整理为一段可读文本。"""
    markdown = source["markdown"]
    pdf = source["pdf"]
    pages = ", ".join(str(page) for page in pdf["pages"])
    return (
        f"Markdown: `{markdown['file']}` — {markdown['section']}<br>"
        f"PDF: `{pdf['file']}` — 第 {pages} 页"
    )


def generate(source_path: Path, output_path: Path) -> None:
    """读取规则真源，按状态分组后生成 Markdown 文档。"""
    document = yaml.safe_load(source_path.read_text(encoding="utf-8"))
    metadata = document["metadata"]
    rules_by_status: dict[str, list[dict[str, Any]]] = defaultdict(list)
    # 先按状态归类，确保阅读视图固定以 ACTIVE、PENDING 的顺序展示。
    for rule in document["rules"]:
        rules_by_status[rule["status"]].append(rule)

    lines = [
        "# Vue 3 前端编码规范规则清单",
        "",
        "> 此文件由 `rules.yaml` 自动生成，仅供阅读与评审。请勿直接编辑。",
        "",
        f"- 版本：`{document['version']}`",
        f"- 范围：{metadata['scope']}",
        f"- 真源：`{metadata['source_of_truth']}`",
        "",
        "ACTIVE 规则会在后续 Skill 实现中执行；PENDING 规则保留原始证据，等待适用条件或含义确认后才可执行。",
        "",
    ]

    for status in ("ACTIVE", "PENDING"):
        rules = rules_by_status.get(status, [])
        lines.extend([f"## {status}（{len(rules)} 条）", ""])
        for rule in rules:
            applies_to = "、".join(rule["applies_to"])
            lines.extend(
                [
                    f"### {rule['id']} — {rule['rule']}",
                    "",
                    f"- 强度：`{rule['strength']}`",
                    f"- 适用：{applies_to}",
                    f"- 判定：{rule['decision_criteria']}",
                    f"- 例外：{rule['exceptions']}",
                    f"- 来源：{format_source(rule['sources'])}",
                    "",
                ]
            )

    output_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    """解析可选输入、输出路径，并执行规则阅读视图生成。"""
    # 默认以 skill 根目录中的真源和阅读视图为输入、输出。
    root = Path(__file__).parents[1]
    source_path = Path(sys.argv[1]) if len(sys.argv) > 1 else root / "rules.yaml"
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else root / "RULES.md"
    generate(source_path, output_path)
    print(f"Generated {output_path} from {source_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
