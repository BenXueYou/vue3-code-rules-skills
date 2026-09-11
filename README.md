# Vue 前端编码规范 Skill

本项目将现有《前端开发编码规范》整理为可由 Codex 使用的 Vue 3 前端编码规范
Skill。项目通过结构化规则真源、可读规则视图、验收场景和版本治理材料，使编码规则
能够被稳定执行、验证和追溯。

当前版本为工作区试点版 `0.0.1`。

## 适用范围

Skill 适用于 Vue 3 项目中的以下文件：

- Vue 单文件组件（`.vue`）
- TypeScript 和 JavaScript（`.ts`、`.js`）
- CSS、Less 和 SCSS（`.css`、`.less`、`.scss`）

试点版不适用于 Vue 2、React、Angular 或其他技术栈，也不会自动整改本次任务未触及
的存量代码。

## 核心能力

- 支持通过 `$frontend-coding-standards` 显式启用，也支持 Vue 3 代码任务自动匹配。
- 以 `rules.yaml` 作为唯一机器可读规则真源。
- 区分 `MUST`、`VERIFY`、`GUIDANCE` 和 `PENDING` 的执行语义。
- 只约束当前任务新增或直接修改的代码，避免扩大改动范围。
- 复用项目已有的格式化、lint、类型检查和测试能力。
- 要求工程格式覆盖和全库迁移分别获得明确授权。
- 提供可验证的试点验收矩阵及 `0.0.1 → 0.1.0 → 1.0.0` 版本治理路径。

## 目录结构

```text
.
├── .agents/skills/frontend-coding-standards/
│   ├── SKILL.md                  # Skill 入口与执行流程
│   ├── rules.yaml                # 编码规则唯一真源
│   ├── RULES.md                  # 由规则真源生成的阅读视图
│   ├── pilot.yaml                # 试点验收与版本治理真源
│   ├── PILOT.md                  # 由试点真源生成的评审视图
│   ├── overrides.example.yaml    # 项目级例外示例
│   ├── scripts/                  # 生成与结构验证脚本
│   ├── tests/                    # 公共行为测试
│   └── issues/                   # 分阶段实施记录
├── docs/specs/                   # 项目规格
├── CONTEXT.md                    # 项目术语表
├── 前端开发编码规范.md           # 原始 Markdown 规范
└── 前端开发编码规范.pdf          # 原始 PDF 规范
```

## 使用方式

在 Vue 3 代码生成或修改任务中显式调用 Skill：

```text
$frontend-coding-standards 按项目规范实现这个 Vue 3 组件
```

符合 Skill 描述的 Vue 3 前端任务也可以自动触发。Skill 启用后会读取
`rules.yaml`，只执行状态为 `ACTIVE` 的规则，并在交付反馈中说明规则版本、触发方式、
已应用规则、验证结果、冲突及未决项。

`PENDING` 规则不会被擅自执行。若实现必须依赖某条未决规则，Skill 会先请求澄清。

## 项目级例外

项目可参考 `overrides.example.yaml` 声明局部例外。例外只允许：

- 为现有 `ACTIVE` 规则新增项目例外；
- 将现有规则在当前项目中降级为 `GUIDANCE`。

每项例外必须记录项目原因和负责人，且不得修改、删除或替换全局 `rules.yaml` 中的
规则。

## 开发与验证

运行环境需要 Python 3 和 PyYAML。

在仓库根目录执行全部测试：

```bash
python -m unittest discover -s .agents/skills/frontend-coding-standards/tests -v
```

验证规则真源：

```bash
python .agents/skills/frontend-coding-standards/scripts/validate_rules.py
```

验证试点验收与版本治理材料：

```bash
python .agents/skills/frontend-coding-standards/scripts/validate_pilot.py
```

重新生成阅读视图：

```bash
python .agents/skills/frontend-coding-standards/scripts/generate_rules_view.py
python .agents/skills/frontend-coding-standards/scripts/generate_pilot_view.py
```

`RULES.md` 和 `PILOT.md` 均为自动生成文件，不应直接编辑。

## 版本治理

- `0.0.1`：工作区试点，由本地维护者维护和审批规则。
- `0.1.0`：完成首轮规则、Skill 和真实项目验证后，升级为本机默认规范。
- `1.0.0`：团队插件正式发布并承诺兼容性，由指定前端负责人审批规则变更和发布。

详细的验收场景、升级条件和维护权边界见
`.agents/skills/frontend-coding-standards/PILOT.md`。

## 贡献规则

修改规则时应同步更新 `rules.yaml`，重新生成 `RULES.md`，并运行全部验证。普通成员可
提交带证据的规则建议；进入团队插件阶段后，规则变更须由指定前端负责人审批。
