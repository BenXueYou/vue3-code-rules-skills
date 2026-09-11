# Vue 3 前端编码规范规则清单

> 此文件由 `rules.yaml` 自动生成，仅供阅读与评审。请勿直接编辑。

- 版本：`0.0.1`
- 范围：Vue 3 项目的 Vue SFC、TypeScript、JavaScript、CSS、Less 与 SCSS
- 真源：`rules.yaml`

ACTIVE 规则会在后续 Skill 实现中执行；PENDING 规则保留原始证据，等待适用条件或含义确认后才可执行。

## ACTIVE（16 条）

### FCS-007 — 不允许连续出现两行及以上的空白行。

- 强度：`MUST`
- 适用：Vue SFC、TypeScript、JavaScript、CSS、Less、SCSS
- 判定：触及代码中任意连续空白行数量不得大于一行。
- 例外：生成文件、第三方代码和项目工具不可避免写入的内容不在本规则范围内。
- 来源：Markdown: `前端开发编码规范.md` — #### 2、缩进换行<br>PDF: `前端开发编码规范.pdf` — 第 6, 7 页

### FCS-011 — 标签属性超过三个时必须换行。

- 强度：`MUST`
- 适用：Vue SFC template
- 判定：一个标签含四个或更多属性时，属性应逐行排列。
- 例外：代码生成器输出、单个不可拆分表达式和项目格式化工具的限制需在实际任务中说明。
- 来源：Markdown: `前端开发编码规范.md` — #### 3、标签<br>PDF: `前端开发编码规范.pdf` — 第 8, 9 页

### FCS-013 — 标签内联样式不允许超过两项，超过时改用 class。

- 强度：`MUST`
- 适用：Vue SFC template
- 判定：style 属性中的样式声明数不得超过两项；超过两项时应提取为 class。
- 例外：CSS 变量、动态单项样式和第三方组件 API 的计数方式尚未说明。
- 来源：Markdown: `前端开发编码规范.md` — #### 4、样式<br>PDF: `前端开发编码规范.pdf` — 第 10, 11 页

### FCS-014 — class 名称采用小写字母，并以中划线或下划线连接。

- 强度：`GUIDANCE`
- 适用：Vue SFC、CSS、Less、SCSS
- 判定：新增 class 名称使用小写字符和 - 或 _ 作为词间连接符。
- 例外：CSS Modules、第三方覆盖选择器和框架生成类名不在本规则范围内。
- 来源：Markdown: `前端开发编码规范.md` — #### 4、样式<br>PDF: `前端开发编码规范.pdf` — 第 10, 11 页

### FCS-019 — 变量声明和导入中的 object 属性超过三个时必须换行显示。

- 强度：`MUST`
- 适用：TypeScript、JavaScript、Vue SFC script
- 判定：对象字面量或导入解构含四个或更多属性时，属性应逐行显示。
- 例外：类型参数、不可拆分的短字面量和项目格式化工具冲突需在实际任务中说明。
- 来源：Markdown: `前端开发编码规范.md` — #### 5、变量声明<br>PDF: `前端开发编码规范.pdf` — 第 11, 12 页

### FCS-021 — 箭头函数符号前后必须有空格。

- 强度：`MUST`
- 适用：TypeScript、JavaScript、Vue SFC script
- 判定：=> 两侧各保留一个空格。
- 例外：字符串、注释和第三方生成文件不在本规则范围内。
- 来源：Markdown: `前端开发编码规范.md` — #### 6、函数表达式格式<br>PDF: `前端开发编码规范.pdf` — 第 12, 13 页

### FCS-022 — 赋值和相等比较运算符前后必须有空格。

- 强度：`MUST`
- 适用：TypeScript、JavaScript、Vue SFC script
- 判定：=、== 和 === 两侧各保留一个空格。
- 例外：默认参数、类型语法及其他不属于赋值或比较的等号语法不在本规则范围内。
- 来源：Markdown: `前端开发编码规范.md` — #### 6、函数表达式格式<br>PDF: `前端开发编码规范.pdf` — 第 12, 13 页

### FCS-023 — 三目运算符周围必须有空格。

- 强度：`MUST`
- 适用：TypeScript、JavaScript、Vue SFC script
- 判定：条件、?、: 和两个结果表达式之间保留空格。
- 例外：嵌套三目表达式的换行方式未规定。
- 来源：Markdown: `前端开发编码规范.md` — #### 6、函数表达式格式<br>PDF: `前端开发编码规范.pdf` — 第 12 页

### FCS-024 — if 和 for 与左括号之间必须有空格。

- 强度：`MUST`
- 适用：TypeScript、JavaScript、Vue SFC script
- 判定：条件或循环语句使用 if (...) 和 for (...) 形式。
- 例外：while、switch、catch 等其他控制语句未在原文中规定。
- 来源：Markdown: `前端开发编码规范.md` — #### 6、函数表达式格式<br>PDF: `前端开发编码规范.pdf` — 第 12, 13 页

### FCS-025 — 表达式中的逗号、比较符和三目符号后必须有空格。

- 强度：`MUST`
- 适用：TypeScript、JavaScript、Vue SFC script
- 判定：,、>、<、?、: 后跟一个空格。
- 例外：泛型、对象字面量、标签语法和字符串中的同类字符不在本规则范围内。
- 来源：Markdown: `前端开发编码规范.md` — #### 6、函数表达式格式<br>PDF: `前端开发编码规范.pdf` — 第 12 页

### FCS-026 — if 成立后的 return 单独成行，且不带大括号。

- 强度：`MUST`
- 适用：TypeScript、JavaScript、Vue SFC script
- 判定：简单守卫返回写成 if (condition) return value，并独占一行。
- 例外：return 前后需要多条语句、声明作用域或项目规则要求大括号时需说明。
- 来源：Markdown: `前端开发编码规范.md` — #### 6、函数表达式格式<br>PDF: `前端开发编码规范.pdf` — 第 13 页

### FCS-027 — 迭代器回调箭头后的返回值单独成行，且不带大括号。

- 强度：`MUST`
- 适用：TypeScript、JavaScript、Vue SFC script
- 判定：简单迭代器回调的返回表达式独占一行且不使用函数体大括号。
- 例外：回调包含多条语句、返回对象字面量或 async 逻辑时的格式尚未说明。
- 来源：Markdown: `前端开发编码规范.md` — #### 6、函数表达式格式<br>PDF: `前端开发编码规范.pdf` — 第 13 页

### FCS-028 — 统一 vue、vue-router 等插件版本。

- 强度：`GUIDANCE`
- 适用：package.json、依赖管理
- 判定：同一项目中相关 Vue 生态依赖使用已确认的统一版本策略。
- 例外：monorepo、peerDependencies 和安全修复需要按项目依赖策略处理。
- 来源：Markdown: `前端开发编码规范.md` — #### 7、SDK版本管理<br>PDF: `前端开发编码规范.pdf` — 第 13 页

### FCS-029 — 不允许保留冗余的插件包。

- 强度：`MUST`
- 适用：package.json、依赖管理
- 判定：本次新增或修改的依赖声明不得包含明确未使用的冗余包。
- 例外：间接运行时加载、构建插件和后续任务范围外的既有依赖仅报告不删除。
- 来源：Markdown: `前端开发编码规范.md` — #### 7、SDK版本管理<br>PDF: `前端开发编码规范.pdf` — 第 13 页

### FCS-030 — 不引入未使用的实例、函数、方法、组件或变量。

- 强度：`MUST`
- 适用：Vue SFC、TypeScript、JavaScript
- 判定：触及代码中新增的 import 和声明必须被实际使用。
- 例外：类型导入、框架约定暴露和模板中使用的 script 绑定应按语言工具实际识别。
- 来源：Markdown: `前端开发编码规范.md` — #### 7、SDK版本管理<br>PDF: `前端开发编码规范.pdf` — 第 13 页

### FCS-032 — 推荐使用 Pinia 状态管理，避免直接操作全局对象。

- 强度：`GUIDANCE`
- 适用：Vue 状态管理
- 判定：新增全局状态优先建模为 Pinia store，而不是直接变更全局对象。
- 例外：现有状态库、微前端共享状态和小型局部状态可按项目约定处理。
- 来源：Markdown: `前端开发编码规范.md` — #### 8、Hooks方法规范<br>PDF: `前端开发编码规范.pdf` — 第 13 页

## PENDING（19 条）

### FCS-001 — 文件夹使用小写字母和中划线连接。

- 强度：`GUIDANCE`
- 适用：目录
- 判定：新建目录名应为 lower-kebab-case。
- 例外：原文未说明第三方目录、框架约定目录和既有目录的处理方式。
- 来源：Markdown: `前端开发编码规范.md` — #### 1、文件夹命名<br>PDF: `前端开发编码规范.pdf` — 第 3, 4 页

### FCS-002 — Vue 组件文件使用双驼峰命名。

- 强度：`GUIDANCE`
- 适用：Vue SFC 文件
- 判定：新建的非路由 Vue 组件文件名应为 UpperCamelCase.vue。
- 例外：index.vue、路由页面和框架约定文件的优先级尚未说明。
- 来源：Markdown: `前端开发编码规范.md` — #### 2、文件命名<br>PDF: `前端开发编码规范.pdf` — 第 4 页

### FCS-003 — 非 Vue 代码和样式文件使用驼峰命名。

- 强度：`GUIDANCE`
- 适用：TypeScript、JavaScript、CSS、Less、SCSS 文件
- 判定：新建的 .ts、.js、.css、.less、.scss 文件应为 camelCase 文件名。
- 例外：原文示例同时出现 index.css 等入口文件，入口文件与工具链约定尚未澄清。
- 来源：Markdown: `前端开发编码规范.md` — #### 2、文件命名<br>PDF: `前端开发编码规范.pdf` — 第 4, 5 页

### FCS-004 — 页面路由组件和其他 JavaScript 使用小驼峰命名。

- 强度：`GUIDANCE`
- 适用：路由页面 Vue SFC、JavaScript 文件
- 判定：适用对象的文件名应为 lowerCamelCase。
- 例外：页面路由组件与 FCS-002 的边界、以及“其他 js”的范围尚未说明。
- 来源：Markdown: `前端开发编码规范.md` — #### 2、文件命名<br>PDF: `前端开发编码规范.pdf` — 第 4, 5 页

### FCS-005 — 单文件组件从上至下排列 template、script、style 标签。

- 强度：`GUIDANCE`
- 适用：Vue SFC
- 判定：同时包含这些块的 SFC 应按 template、script、style 的顺序出现。
- 例外：缺少任一块时的顺序和多个 style 块的处理方式尚未说明。
- 来源：Markdown: `前端开发编码规范.md` — #### 1、单文件组件格式<br>PDF: `前端开发编码规范.pdf` — 第 5, 6 页

### FCS-006 — 换行使用两个空格缩进。

- 强度：`GUIDANCE`
- 适用：Vue SFC、TypeScript、JavaScript、CSS、Less、SCSS
- 判定：新增的嵌套代码或样式块每层缩进为两个空格。
- 例外：YAML、Markdown、第三方配置和工具自动格式化的优先级尚未说明。
- 来源：Markdown: `前端开发编码规范.md` — #### 2、缩进换行<br>PDF: `前端开发编码规范.pdf` — 第 6 页

### FCS-008 — 短注释使用单行注释，超过两行的注释使用多行注释，且多行注释后不留空白行。

- 强度：`GUIDANCE`
- 适用：TypeScript、JavaScript、Vue SFC script
- 判定：注释内容超过两行时应改用块注释，块注释结束后紧接后续代码。
- 例外：“超过两行”的计数口径和 JSDoc、版权声明的处理方式尚未说明。
- 来源：Markdown: `前端开发编码规范.md` — #### 2、缩进换行<br>PDF: `前端开发编码规范.pdf` — 第 6, 8 页

### FCS-009 — 自定义组件标签使用双驼峰命名。

- 强度：`GUIDANCE`
- 适用：Vue SFC template
- 判定：本地业务组件标签应为 UpperCamelCase。
- 例外：自动导入组件、Web Components 和跨团队共享组件的识别方式尚未说明。
- 来源：Markdown: `前端开发编码规范.md` — #### 3、标签<br>PDF: `前端开发编码规范.pdf` — 第 8, 9 页

### FCS-010 — 第三方组件标签使用小写中划线命名，并使用双闭合标签。

- 强度：`GUIDANCE`
- 适用：Vue SFC template
- 判定：被识别为第三方库的组件以 kebab-case 写出开始和结束标签。
- 例外：Vue 原生标签、自闭合语法和第三方组件识别依据尚未说明。
- 来源：Markdown: `前端开发编码规范.md` — #### 3、标签<br>PDF: `前端开发编码规范.pdf` — 第 8, 9 页

### FCS-012 — 标签属性依次排列为条件指令、标识属性、原生 style/class、动态 props、事件属性。

- 强度：`GUIDANCE`
- 适用：Vue SFC template
- 判定：同一标签的属性按 v-if/v-show、id 标识、style/class、动态 props、事件属性的分组顺序排序。
- 例外：v-for、v-model、ref、slot 和未列属性的分组归属尚未说明。
- 来源：Markdown: `前端开发编码规范.md` — #### 3、标签<br>PDF: `前端开发编码规范.pdf` — 第 8, 10 页

### FCS-015 — 样式属性依次排列为盒模型尺寸、定位布局、颜色字体背景。

- 强度：`GUIDANCE`
- 适用：CSS、Less、SCSS、Vue SFC style
- 判定：可归类的属性按 position/width/height/display/flex、top/right/bottom/left/margin/padding、color/font-size/background 三组排序。
- 例外：CSS 变量、浏览器前缀、未列属性及组内排序尚未说明。
- 来源：Markdown: `前端开发编码规范.md` — #### 4、样式<br>PDF: `前端开发编码规范.pdf` — 第 10, 11 页

### FCS-016 — import 的实例、方法、函数和变量采用驼峰命名。

- 强度：`GUIDANCE`
- 适用：TypeScript、JavaScript、Vue SFC script
- 判定：适用的导入标识符使用 lowerCamelCase。
- 例外：命名导出别名、库导出名和 TypeScript 类型导入的适用方式尚未说明。
- 来源：Markdown: `前端开发编码规范.md` — #### 5、变量声明<br>PDF: `前端开发编码规范.pdf` — 第 11, 12 页

### FCS-017 — import 的 class 类名和组件名采用双驼峰命名。

- 强度：`GUIDANCE`
- 适用：TypeScript、JavaScript、Vue SFC script
- 判定：class 和组件的导入本地标识符使用 UpperCamelCase。
- 例外：默认导出、命名空间导入与第三方导出名的处理方式尚未说明。
- 来源：Markdown: `前端开发编码规范.md` — #### 5、变量声明<br>PDF: `前端开发编码规范.pdf` — 第 11, 12 页

### FCS-018 — 变量声明中 class 类名和组件名使用双驼峰，其他名称使用驼峰。

- 强度：`GUIDANCE`
- 适用：TypeScript、JavaScript、Vue SFC script
- 判定：新增变量按其是否为 class 或组件采用 UpperCamelCase 或 lowerCamelCase。
- 例外：枚举、类型、泛型、私有字段和框架约定变量的命名规则尚未说明。
- 来源：Markdown: `前端开发编码规范.md` — #### 5、变量声明<br>PDF: `前端开发编码规范.pdf` — 第 11, 12 页

### FCS-020 — 常量声明使用大写字母，可使用下划线连接。

- 强度：`GUIDANCE`
- 适用：TypeScript、JavaScript、Vue SFC script
- 判定：适用的常量以 UPPER_SNAKE_CASE 命名。
- 例外：原文未定义“常量”的范围，且与项目既有 const 惯例可能冲突。
- 来源：Markdown: `前端开发编码规范.md` — #### 5、变量声明<br>PDF: `前端开发编码规范.pdf` — 第 12 页

### FCS-031 — Hooks 不直接操作外部对象，使用 key 变量映射全局对象的拷贝。

- 强度：`GUIDANCE`
- 适用：Vue Hooks、TypeScript、JavaScript
- 判定：新增 hooks 通过局部 key 或拷贝映射访问需要的全局对象状态。
- 例外：外部对象、key 映射和允许的只读访问均未定义。
- 来源：Markdown: `前端开发编码规范.md` — #### 8、Hooks方法规范<br>PDF: `前端开发编码规范.pdf` — 第 13 页

### FCS-033 — 文件下载不使用全局 axios 实例，而通过 fetch 请求走工具类方法。

- 强度：`GUIDANCE`
- 适用：文件下载、TypeScript、JavaScript
- 判定：新增文件下载调用使用项目的 fetch 工具封装而非全局 axios 实例。
- 例外：项目没有 fetch 工具类、鉴权需求和“全局 axios 实例”的识别方式尚未说明。
- 来源：Markdown: `前端开发编码规范.md` — #### 9.文件下载规范<br>PDF: `前端开发编码规范.pdf` — 第 13 页

### FCS-034 — 全局弹窗可采用声明式设计方式。

- 强度：`GUIDANCE`
- 适用：Vue 弹窗组件
- 判定：当选择声明式弹窗时，组件状态和模板以声明方式表达。
- 例外：原文同时展示命令式弹窗，未规定两种方式的选择条件或优先级。
- 来源：Markdown: `前端开发编码规范.md` — #### 10.全局弹窗组件的设计方式<br>PDF: `前端开发编码规范.pdf` — 第 13, 14 页

### FCS-035 — 全局弹窗可采用命令式设计方式。

- 强度：`GUIDANCE`
- 适用：Vue 弹窗组件
- 判定：当选择命令式弹窗时，调用入口和生命周期应由命令式 API 清晰表达。
- 例外：原文同时展示声明式弹窗，未规定两种方式的选择条件或优先级。
- 来源：Markdown: `前端开发编码规范.md` — #### 10.全局弹窗组件的设计方式<br>PDF: `前端开发编码规范.pdf` — 第 14, 15 页
