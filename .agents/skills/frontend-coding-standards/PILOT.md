# 前端编码规范试点验收与版本治理

> 此文件由 `pilot.yaml` 自动生成，仅供执行验收与评审。请勿直接编辑。

- 规则版本：`0.0.1`
- 规则真源：`rules.yaml`
- 规则阅读视图：`RULES.md`
- 项目例外样例：`overrides.example.yaml`

## 验收记录规则

- 可用状态：NOT_RUN, PASS, FAIL, BLOCKED
- 证据要求：PASS 必须记录可复查的任务输入、改动或命令结果；未实际执行时保持 NOT_RUN。

## 验收场景

### FCS-ACC-001 — explicit_trigger

- 状态：`NOT_RUN`
- 准备：准备一个包含 Vue 3 SFC 的一次性试点项目。
- 操作：显式调用 $frontend-coding-standards 完成一处 Vue 3 代码修改。
- 预期：
  - 交付反馈将触发方式记录为显式。
  - 触及代码应用当前版本的 ACTIVE 规则。
- 证据：
  - 无

### FCS-ACC-002 — automatic_trigger

- 状态：`NOT_RUN`
- 准备：准备一个 Vue 3 代码修改任务，但不显式点名 Skill。
- 操作：请求修改 .vue、.ts、.js、.css、.less 或 .scss 文件。
- 预期：
  - Skill 由任务描述自动匹配。
  - 交付反馈将触发方式记录为自动。
- 证据：
  - 无

### FCS-ACC-003 — touched_code_only

- 状态：`NOT_RUN`
- 准备：在目标文件和未触及文件中预置存量规范债务。
- 操作：仅请求修改目标文件中的一个明确代码区域。
- 预期：
  - 规范修正限于新建或直接触及的代码。
  - 未触及债务只报告，不产生无关改动。
- 证据：
  - 无

### FCS-ACC-004 — pending_not_executed

- 状态：`NOT_RUN`
- 准备：选择会涉及至少一条 PENDING 规则的任务。
- 操作：在未提供额外规则解释的情况下执行任务。
- 预期：
  - PENDING 规则不被执行或提升强度。
  - 实现必须依赖该规则时请求澄清，否则在交付反馈中记录。
- 证据：
  - 无

### FCS-ACC-005 — rule_strength

- 状态：`NOT_RUN`
- 准备：选择同时涉及 ACTIVE MUST、GUIDANCE 和 VERIFY 的任务。
- 操作：完成代码修改并交付。
- 预期：
  - MUST 违规在触及代码中修正后再交付。
  - GUIDANCE 可因项目约定偏离，但记录原因。
  - VERIFY 通过项目既有命令执行，不被当作格式规则。
- 证据：
  - 无

### FCS-ACC-006 — conflict_priority

- 状态：`NOT_RUN`
- 准备：准备项目自动化配置与 ACTIVE 规则冲突的触及代码。
- 操作：执行普通代码修改，不授权工程格式覆盖。
- 预期：
  - ACTIVE 规则在触及代码中优先。
  - 项目配置和未触及文件保持不变，冲突被记录。
- 证据：
  - 无

### FCS-ACC-007 — format_override_authorization

- 状态：`NOT_RUN`
- 准备：准备需要调整 ESLint、Prettier 或 Stylelint 的项目。
- 操作：分别执行普通代码任务和明确要求接入规范或覆盖工程格式的任务。
- 预期：
  - 普通任务不修改工程格式配置。
  - 只有明确授权的任务才修改相关配置。
- 证据：
  - 无

### FCS-ACC-008 — full_repo_migration_authorization

- 状态：`NOT_RUN`
- 准备：准备配置变更会影响全库校验或工具无法限定文件范围的项目。
- 操作：仅授权工程格式覆盖，不授权全库迁移。
- 预期：
  - 在影响说明和单独授权前不执行全库格式化或迁移。
  - 配置接入与存量迁移作为两个独立决策记录。
- 证据：
  - 无

### FCS-ACC-009 — rule_source_and_reading_view

- 状态：`NOT_RUN`
- 准备：修改 rules.yaml 中一个可识别字段，并在临时位置生成阅读视图。
- 操作：运行规则结构验证和阅读视图生成检查。
- 预期：
  - rules.yaml 满足版本、唯一 ID、字段、枚举和来源约束。
  - RULES.md 与从 rules.yaml 生成的内容完全一致。
- 证据：
  - 无

### FCS-ACC-010 — project_override_structure

- 状态：`NOT_RUN`
- 准备：分别准备有效例外和尝试改写全局规则的 overrides.yaml。
- 操作：运行项目例外结构验证。
- 预期：
  - 仅允许新增例外或降级为 GUIDANCE，并要求原因与负责人。
  - 修改、删除或替换全局规则的操作验证失败。
- 证据：
  - 无

## 版本路径

### 0.0.1 — workspace-pilot

- 规则变更审批：`local-maintainer`
- 发布负责人：`local-maintainer`
- 进入条件：
  - 规则真源、Skill、阅读视图和结构验证可在当前工作区使用。
- 退出条件：
  - 在真实 Vue 3 任务中完成验收矩阵并保存证据。
  - 高影响 FAIL 或 BLOCKED 项已关闭或明确接受。

### 0.1.0 — local-default

- 规则变更审批：`local-maintainer`
- 发布负责人：`local-maintainer`
- 进入条件：
  - 首轮规则清单、Skill 和真实项目验证完成。
  - 规则、例外和自动触发行为在试点记录中趋于稳定。
- 退出条件：
  - 本机多个 Vue 3 项目验证通过，团队采用边界与负责人已确定。

### 1.0.0 — team-plugin

- 规则变更审批：`designated-frontend-lead`
- 发布负责人：`designated-frontend-lead`
- 进入条件：
  - 团队插件安装、升级和回退流程已验证。
  - 兼容性承诺、项目例外机制和发布审批生效。
- 退出条件：
  - 后续规则变更遵循团队发布与兼容性策略。

## 维护权

- 试点规则维护：`local-maintainer`
- 团队规则变更审批：`designated-frontend-lead`
- 团队发布：`designated-frontend-lead`
- 成员建议：普通成员提交带证据的建议，由当前阶段审批人合并；不得直接修改已发布真源。
