# Codex Skill 化前端开发规范：可行性调研

## 结论

**可行，且适合做成仓库级（repo-scoped）Codex Skill。** 将《前端开发编码规范》的可操作条款整理进一个 `SKILL.md`，可让 Codex 在生成、修改和审查 Vue 前端代码时按同一套工作流执行，例如检查目录/文件命名、Vue SFC 标签顺序、模板属性顺序、样式顺序、命名和空格规则。

不过，Skill 的本质是向模型提供“指令、资源和可选脚本”，不是静态分析器或编译器。因此它能显著提高生成代码的一致性，但**不能仅靠 Skill 做到不可绕过的硬性拦截**。对必须零容忍的规则，应该在 Skill 中要求执行项目已有的 ESLint、Stylelint、Prettier、类型检查和测试；对现有工具无法覆盖的条款，再补充可执行检查脚本。

## 官方依据

| 结论 | 官方文档依据 |
| --- | --- |
| Skill 可以封装规范工作流 | 官方将 Skill 定义为用于扩展 ChatGPT 和 Codex 的“任务专用能力”，可打包 instructions、resources 和 optional scripts，使产品能可靠地遵循工作流。 |
| 最小结构简单 | 一个 Skill 是含 `SKILL.md` 的目录；`SKILL.md` 必须有 `name` 与 `description` 元数据，可再放 `scripts/` 与 `references/`。 |
| 可自动或显式触发 | Codex 可因任务匹配 `description` 隐式选择 Skill，也可在 CLI/IDE 中通过 `$技能名` 显式调用。`description` 应准确写明触发场景与边界。 |
| 可限制为显式调用 | `agents/openai.yaml` 中的 `policy.allow_implicit_invocation: false` 可关闭隐式触发；未配置时默认允许隐式触发。 |
| 可按仓库生效 | Codex 会从当前工作目录起、到仓库根目录之间各级 `.agents/skills` 扫描技能。因此放在仓库根的 `.agents/skills/` 下，可让该仓库的子目录工作都发现这条规范。 |
| 修改后的加载方式 | Codex 会自动检测 Skill 变更；若没有显示，官方建议重启 Codex。也可在 `~/.codex/config.toml` 用 `[[skills.config]]` 按路径禁用某个 Skill。 |

来源：OpenAI 官方文档 [Build skills](https://learn.chatgpt.com/docs/build-skills)（访问日期：2026-09-03）。

## 对当前规范的落地建议

建议的仓库结构如下（不改动原始规范文件）：

```text
.agents/
  skills/
    frontend-coding-standards/
      SKILL.md
      references/
        frontend-coding-spec.md
      scripts/                 # 仅放无法由既有 lint 覆盖的检查
```

1. `SKILL.md` 写精炼、可执行的行为：适用 Vue 组件、TS/JS、CSS/SCSS/LESS 文件；生成或修改后逐项自检；优先运行仓库已有校验命令；报告例外与无法自动验证的条款。
2. `references/frontend-coding-spec.md` 保存原规范的副本或经过结构化的摘录。将篇幅较大的规范放在 reference，可利用官方所述“progressive disclosure”：初始时只提供 Skill 名称和描述，选中 Skill 后才读取完整 `SKILL.md`；按需再读取引用材料。
3. 将规则分层：
   - **可由格式化/静态检查硬校验**：2 空格缩进、空行、运算符空格、未使用导入、样式属性排序等，交给 Prettier、ESLint、Stylelint 及相关插件。
   - **可由 Skill 审查并要求修正**：组件/目录命名、SFC 区块顺序、超过 3 个属性换行、属性排序、inline style 项数、下载方式、Pinia/全局对象约束、弹窗设计。
   - **需要业务上下文或原文不够明确**：仓库命名、页面路由命名、声明式/命令式弹窗的适用条件。应在 Skill 中明确判定准则或要求先询问，避免模型自行臆断。
4. 在团队日常使用中，用 `$frontend-coding-standards` 显式调用最确定；同时把描述写成“Vue 前端开发、代码生成、代码修改、代码审查、编码规范”等清晰触发词，允许 Codex 在匹配任务时隐式选择。

## 推荐的启用方式

若希望只作用于某一个前端仓库，在**该仓库根目录**创建：

```text
.agents/skills/frontend-coding-standards/SKILL.md
```

重新打开或重启 Codex 后，它应被发现。随后可在任何相关任务中显式写：

```text
$frontend-coding-standards 为这个 Vue 页面新增筛选表单，并遵循规范。
```

若要让个人机器上所有仓库默认可用，官方文档列出的用户级位置是：

```text
$HOME/.agents/skills/frontend-coding-standards/SKILL.md
```

团队分发则可将此 Skill 随仓库提交；要跨仓库/跨成员提供可安装分发，官方建议将其打包为 plugin。

## 注意事项

- 当前原规范中多处示例只以图片给出。将其转成 Skill 前，应把图片中隐含的判断规则补成文字化、可判定的“应当/不得”条款；否则模型和检查脚本都无法稳定执行。
- `description` 既是发现入口也是触发条件，过于宽泛会在不相关任务中加载，过于窄又会错过前端开发任务。
- Skill 的脚本能够把部分要求变为可验证步骤，但脚本是否运行、结果是否通过仍应由项目的 CI 作为最终硬门禁。官方文档描述 Skill 为可选脚本加指令的工作流载体，并未把它定义为强制的策略执行层；“无法单独硬拦截”是据此作出的实现边界判断。
