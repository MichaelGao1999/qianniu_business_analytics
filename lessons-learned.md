# 淘系店铺经营数据分析 — 经验总结

> 模板化知识沉淀，供未来项目复用。结构分为「技术点」和「流程点」两类。
>
> **不是每个问题都值得记在这里**——详见下方「何时记录」。

---

## 何时记录

### 触发标准（满足任一即记录）

| 标准 | 说明 | 示例 |
|------|------|------|
| **跨项目可复用** | 换个项目做类似功能时，这条经验仍然有用 | "HTTP Digest 认证刷新 token 时，回写必须保留 AK/SK，否则后续刷新永久失败" |
| **花了 >30 分钟才解决** | 时间成本高，未来不值得再付一次 | "日期 `T23:59:59.999+08:00` 导致后端多返回一天数据" |
| **反直觉** | 表面看起来该 A，实际必须 B，违反第一直觉 | "结束日期用当天零点而非 23:59:59，才能精确限定区间" |
| **未来可能重复踩** | 架构/环境/工具链的固有陷阱，新成员大概率遇到 | "Python `sys.path.insert` 引用外部技能包路径，环境变化后失效" |

### 不记录的内容（排除标准）

- ❌ 已记入 `troubleshooting.md` 的具体错误修复步骤 → 那里是"急救手册"，这里是"模式总结"
- ❌ 一次性环境配置错误（如输错密码、网络临时中断）
- ❌ 过于基础的知识（如 "List 的 `add()` 是 O(1)")
- ❌ 仅适用于本项目特定业务逻辑的 hack

### 与 troubleshooting.md 的分界

| | `troubleshooting.md` | `lessons-learned.md` |
|---|---|---|
| **问法** | "这个报错怎么修？" | "这类问题为什么会发生 / 怎么预防？" |
| **粒度** | 具体错误关键词 + 具体解决步骤 | 抽象模式 + 根本原因 + 预防策略 |
| **时效** | 只要错误还在发生，就保持有效 | 即使工具版本升级，底层模式可能仍有效 |
| **示例** | "`openpyxl` 未安装 → `pip install openpyxl`" | "Python 技能包应始终附带 `requirements.txt`，否则跨环境部署时依赖缺失问题反复出现" |

### 记录时机

**用户说「存储」时**，与 `status.md`、`session-log.md` 同步评估更新。

评估方式：AI 回顾本轮会话内容，检查是否有符合「触发标准」的经验。有则提炼写入本文件；没有则跳过。

---

## 技术经验

| # | 经验 | 来源模块 |
|---|------|---------|
| 1 | **HTTP Digest 认证回写规则**：刷新 token 时只更新 `jycmOpenApiCookie`，必须保留 `accessKey` 和 `secretKey`。若覆盖整个文件丢失 AK/SK，后续 Digest 刷新将永久失败 | auth.md / auth/jycm.json |
| 2 | **日期区间陷阱**：后端按 "< endDate" 解析，`T23:59:59.999+08:00` 和 `Z`（UTC）后缀都会导致多返回一天数据。必须用 `T00:00:00+08:00` | SKILL.md / fetch-data.md |
| 3 | **shopIds 类型陷阱**：后端要求 `List<String>`（JSON 字符串数组），传入数字数组会导致参数校验失败 | jycm_fetch_sycm_shop.py |
| 4 | **Token Key 只问一次**：凭证文件存在但 Cookie 过期时，必须先走 Digest 自动刷新，绝不能直接问用户。这是用户体验的关键红线 | auth.md |
| 5 | **Markdown 一源多用**：对话交付和钉钉推送使用同一套 Markdown 正文，避免"对话一版、钉钉一版"的信息不一致 | report-analyze.md |
| 6 | **多店合并 vs 跨平台**：同为淘系的多家店铺可一次 `createAndDownload` 合并取数；但淘系与京东/抖音混用时必须明确拒绝，不得伪造数据 | SKILL.md | | TAG:build-env TAG:testing [来源:vibe-coding-project-sop @2026-05-22] | INFO | 纯 HTML+CSS+JS 项目无需 npm，双击 `index.html` 即可预览，但涉及 Web Worker（如 Stockfish）时必须启 HTTP 服务器 [来源:blindfold-chess @2026-05-21] | EngineModule |
| | TAG:dom TAG:api-design [来源:vibe-coding-project-sop @2026-05-22] | WARNING | 手写 IIFE 模块时，用 `window.ModuleName = Module` 暴露 API，内部私有变量用下划线前缀，避免全局泄漏 [来源:blindfold-chess @2026-05-21] | 所有 js/*.js |
| | TAG:data TAG:api-design [来源:vibe-coding-project-sop @2026-05-22] | INFO | PGN 解析器对空/无效输入返回 `[]`（空数组）而非 `null`，调用方需区分"无走法"和"解析失败" [来源:blindfold-chess @2026-05-21] | ReplayModule |
| | TAG:dom TAG:ux [来源:vibe-coding-project-sop @2026-05-22] | WARNING | 屏幕切换导航不能只隐藏上一个屏幕，必须遍历 `.screen` 全部隐藏后再显示目标，否则多层屏幕重叠 [来源:blindfold-chess @2026-05-21] | 全局导航 |
| | TAG:ai-workflow [来源:vibe-coding-project-sop @2026-05-22] | INFO | 项目文档结构会随时间进化，"存档"或"恢复"操作前应先 `ls`/`glob` 确认当前文件系统现状，避免按历史路径写入已不存在的文件 [来源:blindfold-chess @2026-05-21] | 文档维护 |
| | TAG:i18n [来源:vibe-coding-project-sop @2026-05-22] | CRITICAL | **i18n 分散架构必然导致翻译遗漏**：当项目同时存在"全局字典 + 模块私有字典 + 硬编码"三种翻译方式时，新增功能几乎必然漏掉其中一种或多种。唯一可持续的方案是"单一字典源" [来源:blindfold-chess @2026-05-21] | 全站 i18n |
| | TAG:i18n TAG:architecture [来源:vibe-coding-project-sop @2026-05-22] | WARNING | **模块内部字典若从不主动更新 DOM，则纯属冗余**：welcome.js 有 `_i18n` 和 `_t()`，但从不调用，完全依赖 common.js 的 `updateTexts()`。这种"假私有字典"不仅没用，还会给维护者造成"这里已经翻译了"的错觉 [来源:blindfold-chess @2026-05-21] | welcome.js |
| | TAG:i18n TAG:dom [来源:vibe-coding-project-sop @2026-05-22] | WARNING | **settings.js 的独立字典与 common.js 的全局扫描存在竞争**：settings panel 的元素带 `data-i18n`，settings.js 自己 `_updateAllTexts()` 会覆盖，但 common.js 的 `updateTexts()` 也会扫到，如果 common.js 缺键，用户会看到 key 名闪一下才被正确文本覆盖 [来源:blindfold-chess @2026-05-21] | settings.js / common.js |
| | TAG:testing TAG:architecture [来源:vibe-coding-project-sop @2026-05-22] | CRITICAL | **删除生产代码的 fallback 函数前，必须先评估测试环境是否提供了该依赖**：架构统一重构必须同时改代码+测试，只改一边会导致测试雪崩 [来源:blindfold-chess @2026-05-21] | 全站 i18n |
| | TAG:dom TAG:i18n [来源:vibe-coding-project-sop @2026-05-22] | WARNING | **全局 `updateTexts()` 与模块私有 `_updateXxx()` 可能存在 DOM 竞争**：两者操作同一 DOM 元素。测试必须验证最终渲染结果，而非中间状态 [来源:blindfold-chess @2026-05-21] | settings.js / common.js |
| | TAG:ux TAG:architecture [来源:vibe-coding-project-sop @2026-05-22] | WARNING | **UI 风格不一致的根因通常是「硬编码颜色」**：引入统一的「棋盘风格配置源」后，所有棋盘自动同步，消除不一致的根因 [来源:blindfold-chess @2026-05-21] | BoardRenderer / coordinate.js |
| | TAG:data TAG:architecture [来源:vibe-coding-project-sop @2026-05-22] | INFO | **数据层的双语字段与代码层的硬编码分支是两个问题**：区分"数据双语"和"代码分支"可避免过度重构 [来源:blindfold-chess @2026-05-21] | replay.js / data/games.js |
| | TAG:data TAG:build-env [来源:vibe-coding-project-sop @2026-05-22] | WARNING | **数据文件中的引号嵌套是极易被忽视的语法陷阱**：在真实浏览器中会抛出 `SyntaxError` 并阻断后续脚本执行 [来源:blindfold-chess @2026-05-21] | data/games.js |
| | TAG:testing TAG:debugging [来源:vibe-coding-project-sop @2026-05-22] | INFO | **playwright 是定位浏览器特有 bug 的有效手段**：通过 `page.add_init_script` 注入错误监听器 + `page.on('pageerror')`，可以精确定位到出错的文件、行号和列号 [来源:blindfold-chess @2026-05-21] | 调试工具 |
| | TAG:testing TAG:dom [来源:vibe-coding-project-sop @2026-05-22] | INFO | 浏览器集成测试阶段发现 welcome.js / replay.js / stats.js 的 DOM 事件绑定遗漏 [来源:blindfold-chess @2026-05-21] | |
| | TAG:cross-platform TAG:ai-workflow [来源:vibe-coding-project-sop @2026-05-22] | WARNING | **Shell here-document 在 Windows git bash 中不可靠**：含引号的多行复杂脚本会被截断或解析错误；应先 `WriteFile` 写脚本，再 `Shell` 执行 [来源:blindfold-chess @2026-05-21] | |
| | TAG:i18n TAG:ai-workflow [来源:vibe-coding-project-sop @2026-05-22] | WARNING | **翻译检查必须是独立任务，不能依赖"开发时顺手做"**：本次检查发现 25+ 处遗漏，分布在 HTML、JS 字典、硬编码三个层面 [来源:blindfold-chess @2026-05-21] | |
| | TAG:state-management [来源:vibe-coding-project-sop @2026-05-22] | CRITICAL | **绝对不要**在 `setState` 的 updater 函数内部调用 `dispatch()` 或其他 setState，会触发 React "渲染时更新" 警告 [来源:french-exit @2026-05-21] | `ResultsPage.tsx` |
| | TAG:cross-platform TAG:build-env [来源:vibe-coding-project-sop @2026-05-22] | CRITICAL | 中文路径 + MinGW = 链接器失败。解决方案：复制到纯 ASCII 路径（如 `/c/french-exit`）后编译 [来源:french-exit @2026-05-21] | |
| | TAG:testing TAG:cross-platform [来源:vibe-coding-project-sop @2026-05-22] | INFO | **`#[cfg(not(test))]` 隔离问题代码**是零副作用的修复手法：release 构建完全不受影响，测试逻辑移至独立模块继续跑 [来源:french-exit @2026-05-21] | |
| | TAG:data TAG:performance [来源:vibe-coding-project-sop @2026-05-22] | WARNING | 不要一次性加载所有完整 `TraceItem` 到前端（内存 + DOM 渲染压力大） [来源:french-exit @2026-05-21] | |
| | TAG:architecture TAG:data [来源:vibe-coding-project-sop @2026-05-22] | INFO | 正确做法：后端提供**轻量摘要接口**（只返回 id + category + suggested_action），前端用它批量生成 decisions [来源:french-exit @2026-05-21] | |
| | TAG:pagination TAG:architecture [来源:vibe-coding-project-sop @2026-05-22] | WARNING | 用户实际浏览仍按分页，但"全选全部"走轻量接口，两者解耦 [来源:french-exit @2026-05-21] | |
| | TAG:pagination TAG:state-management TAG:security [来源:vibe-coding-project-sop @2026-05-22] | CRITICAL | **事故经过**：ResultsPage 默认自动勾选所有扫描结果 → 用户点击"全选全部"（以为是全选当前页，实际是全选全部）→ 确认页看到"将删除 17,706 个文件"但未警觉 → 执行后大量文件丢失 [来源:french-exit @2026-05-21] | |
| | TAG:security TAG:ux [来源:vibe-coding-project-sop @2026-05-22] | CRITICAL | **教训**：涉及删除的安全工具，**默认安全 > 默认便利**。所有选择必须用户显式操作，任何"帮你选好"的设计都需反复审视 [来源:french-exit @2026-05-21] | |
| | 测试驱动开发能在手工测试无法触及的边界条件下发现 bug（如"恰好取消所有勾选"触发死循环）[来源:french-exit @2026-05-21] [来源:vibe-coding-project-sop @2026-05-22] |  |
| | `AGENTS.md` 定义触发词和行为约束，`status.md` 记录动态进度，两者分工明确，新会话读 2 份文件即可开工 [来源:french-exit @2026-05-21] [来源:vibe-coding-project-sop @2026-05-22] |  |
| | 涉及 7+ 文件读改测的架构重构，应新开会话执行，避免上下文压缩导致信息丢失 [来源:blindfold-chess @2026-05-21] [来源:vibe-coding-project-sop @2026-05-22] |  |
| | 中文路径 + MinGW = 链接器失败。解决方案：复制到纯 ASCII 路径后编译 [来源:french-exit @2026-05-21] [来源:vibe-coding-project-sop @2026-05-22] |  |
| | `cargo check --lib` 不需要链接，可以在中文路径直接跑；`cargo test --no-run` 同理 [来源:french-exit @2026-05-21] [来源:vibe-coding-project-sop @2026-05-22] |  |
| | Windows 路径在 git bash / Node.js / cmd 中转义规则不同，写跨平台脚本时优先用正斜杠或 `path.join` [来源:blindfold-chess @2026-05-21] [来源:vibe-coding-project-sop @2026-05-22] |  |
|

## 流程经验

### 问题发现机制
- 日期区间多一天的问题是通过**后端实测**发现的（请求 4/20-4/26 返回了 4/27），而非文档说明。API 对接时文档与实际行为可能有偏差，应以实测为准。
- Cookie 活性检测与订购检查**复用同一接口**（`product.json`），避免冗余调用。

### 文档维护
- 技能包的核心约束（如时区规则、渠道范围）应在 `SKILL.md` 和 `AGENTS.md` 中**双重声明**：`SKILL.md` 面向功能执行，`AGENTS.md` 面向开发维护，确保不同场景下都不会遗忘。
- `auth.md` 中必须包含完整的 curl 参考示例，方便 Agent 直接复制执行。

### 环境陷阱
- Windows Git Bash 下执行 `git init` 时，所有文本文件会触发 `LF will be replaced by CRLF` 警告。这不会阻断提交，但跨平台协作前建议统一配置 `core.autocrlf`（如 `git config --global core.autocrlf true`），否则 Linux/Mac 协作者可能遇到行尾符混乱。
- Python 脚本中通过 `sys.path.insert` 引用外部技能包路径（如 `jycm-fetch-report-nl`），在独立工作目录或环境变化后会失效。技能包应追求**自包含**（self-contained），避免跨包硬编码路径。

---

## 待验证假设（本轮未证实，下轮验证）

- [ ] `jycm_auto_report.py` 中 `sys.path.insert` 引用的外部路径 `jycm-fetch-report-nl` 在当前独立工作目录下是否已失效 — 计划通过实际运行验证
- [ ] `openpyxl` 是否已在所有运行环境中安装 — 计划补充 `requirements.txt` 并验证
- [ ] 多店合并取数时（`shopIds` 含多个 id），`createAndDownload` 返回的 Excel 列结构是否与单店一致 — 计划通过实测验证

---

*最后更新：2026-05-20*
