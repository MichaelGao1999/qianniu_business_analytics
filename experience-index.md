# 经验索引

> 本文件由 `scripts/build-experience-index.py` 自动生成。
> 覆盖 troubleshooting / lessons-learned / ADR，统一搜索入口。

> 当前收录 **194** 条记录（问题 47 + 经验 106 + 决策 41）。

---

## 快速搜索表

| 领域 | 关键词 | 类型 | 分类 | 来源 | 状态 | 定位 |
|------|--------|------|------|------|------|------|
| general | AI 重复实现已有组件（棋盘/网格类 UI） | 问题 | 未分类 | blindfold-chess | pending | troubleshooting.md#L8 |
| general | Stockfish 加载超时 / 引擎不启动 | 问题 | 未分类 | blindfold-chess | known_limitation | troubleshooting.md#L19 |
| general | GitHub Pages 国内打不开 | 问题 | 未分类 | blindfold-chess | known_limitation | troubleshooting.md#L28 |
| general | Node.js 测试运行时 chess.js 未定义 | 问题 | 开发/测试 | blindfold-chess | resolved | troubleshooting.md#L41 |
| general | CLI subAgent 并行超时 | 问题 | 开发/测试 | blindfold-chess | resolved | troubleshooting.md#L50 |
| general | 设置面板一闪而过 | 问题 | 开发/测试 | blindfold-chess | resolved | troubleshooting.md#L59 |
| general | 旧代码与新模块冲突 | 问题 | 运行时 | blindfold-chess | wont_fix | troubleshooting.md#L72 |
| general | 引擎候选走法未集成 | 问题 | 运行时 | blindfold-chess | wont_fix | troubleshooting.md#L81 |
| general | JS 数据文件嵌套单引号导致 `Unexpected identifier` | 问题 | 运行时 | blindfold-chess | resolved | troubleshooting.md#L92 |
| general | 设置面板点击无反应（panel toggle 测试失败） | 问题 | 运行时 | blindfold-chess | resolved | troubleshooting.md#L102 |
| general | mock DOM 中 `querySelector` / `querySelectorAll` 缺失 | 问题 | 运行时 | blindfold-chess | resolved | troubleshooting.md#L112 |
| general | `cargo check --lib` 报错：`GetDiskFreeSpaceExW` 未定义 | 问题 | 运行时 | french-exit | — | troubleshooting.md#L124 |
| general | `cargo check --lib` 报错：`FILETIME` 未定义 | 问题 | 运行时 | french-exit | — | troubleshooting.md#L132 |
| general | `cargo test --lib` 报错 `0xc0000139`（UCRT DLL 缺失） | 问题 | 运行时错误 | french-exit | resolved | troubleshooting.md#L144 |
| general | 运行 `french-exit.exe` 报错：`Could not find the WebView2 Runtime... | 问题 | 运行时错误 | french-exit | — | troubleshooting.md#L156 |
| general | 运行 `french-exit.exe` 报错：`找不到 WebView2Loader.dll` | 问题 | 运行时错误 | french-exit | — | troubleshooting.md#L164 |
| general | `cargo tauri build` 失败：`另一个程序正在使用此文件` (os error 32) | 问题 | 运行时错误 | french-exit | — | troubleshooting.md#L172 |
| general | vitest 报错：`Failed to resolve import "@tauri-apps/api/fs"` | 问题 | 测试错误 | french-exit | — | troubleshooting.md#L182 |
| general | vitest 报错：`act is not a function` | 问题 | 测试错误 | french-exit | — | troubleshooting.md#L191 |
| general | vitest 报错：React 警告 `Cannot update a component while renderin... | 问题 | 测试错误 | french-exit | — | troubleshooting.md#L199 |
| general | checkbox 点击后状态不变化 | 问题 | 测试错误 | french-exit | — | troubleshooting.md#L208 |
| general | 中文路径下编译失败 | 问题 | 环境问题 | french-exit | — | troubleshooting.md#L221 |
| general | cargo tauri dev 在后台任务中崩溃 | 问题 | 环境问题 | french-exit | — | troubleshooting.md#L232 |
| general | PowerShell 执行中文脚本报 "UnexpectedToken" | 问题 | 存档提示 | vibe-coding-project-sop | — | troubleshooting.md#L253 |
| general | GitHub push 报错 `Permission denied (publickey)` | 问题 | 存档提示 | vibe-coding-project-sop | resolved | troubleshooting.md#L265 |
| general | `gh auth login` 超时：`read tcp ... operation timed out` | 问题 | 存档提示 | vibe-coding-project-sop | resolved | troubleshooting.md#L274 |
| general | HuggingFace 模型下载连接超时 `curl: (28) Could not connect to server... | 问题 | 存档提示 | vibe-coding-project-sop | resolved | troubleshooting.md#L283 |
| general | PowerShell 添加防火墙规则权限不足 `Access is denied` | 问题 | 存档提示 | vibe-coding-project-sop | known_limitation | troubleshooting.md#L292 |
| general | Node.js 报 SyntaxError: Unexpected identifier（i18n 中文字符串） | 问题 | 存档提示 | blindfold-chess | resolved | troubleshooting.md#L665 |
| general | sed 批量修改误改结构体定义 | 问题 | 存档提示 | french-exit | — | troubleshooting.md#L675 |
| general | French Exit 进程锁定 exe 导致复制失败 | 问题 | 存档提示 | french-exit | — | troubleshooting.md#L684 |
| python-data | Cookie 过期 / 401 认证失败 | 问题 | 存档提示 | qianniu_business_analytics | resolved | troubleshooting.md#L1029 |
| python-data | Digest 刷新失败 | 问题 | 存档提示 | qianniu_business_analytics | resolved | troubleshooting.md#L1038 |
| python-data | auth/jycm.json 缺失字段 | 问题 | 存档提示 | qianniu_business_analytics | resolved | troubleshooting.md#L1047 |
| python-data | 日期区间多返回一天 | 问题 | 取数相关 | qianniu_business_analytics | resolved | troubleshooting.md#L1060 |
| python-data | getAllShopList 返回空数组 | 问题 | 取数相关 | qianniu_business_analytics | wont_fix | troubleshooting.md#L1069 |
| python-data | createAndDownload 返回失败 | 问题 | 取数相关 | qianniu_business_analytics | wont_fix | troubleshooting.md#L1078 |
| python-data | openpyxl 未安装 | 问题 | 报告相关 | qianniu_business_analytics | wont_fix | troubleshooting.md#L1091 |
| python-data | 钉钉推送失败 | 问题 | 报告相关 | qianniu_business_analytics | wont_fix | troubleshooting.md#L1100 |
| python-data | Windows Git Bash LF/CRLF 警告 | 问题 | 环境相关 | qianniu_business_analytics | known_limitation | troubleshooting.md#L1113 |
| general | Hermes Agent Git 合并冲突导致 SyntaxError | 问题 | 存档提示 | vibe-coding-project-sop | resolved | troubleshooting.md#L1133 |
| general | Node.js 环境污染：Hermes Node.js 泄漏到用户 PATH | 问题 | 存档提示 | vibe-coding-project-sop | resolved | troubleshooting.md#L1145 |
| general | CodeBuddy 安装后 package.json 丢失导致命令不可用 | 问题 | 存档提示 | vibe-coding-project-sop | resolved | troubleshooting.md#L1163 |
| general | 条目状态流转 | 问题 | 存档提示 | agent-coding-skeleton | 含义 | troubleshooting.md#L1373 |
| general | 新增条目模板 | 问题 | 存档提示 | agent-coding-skeleton | — | troubleshooting.md#L1391 |
| general | [错误关键词] | 问题 | 存档提示 | agent-coding-skeleton | pending | troubleshooting.md#L1395 |
| general | distribute.py 子进程 GBK 编码错误 | 问题 | 存档提示 | agent-coding-skeleton | known_limitation | troubleshooting.md#L1408 |
| general | 纯 HTML+CSS+JS 项目无需 npm，双击 `index.html` 即可预览，但涉及 Web Worker（如... | 经验 | build-env / testing | blindfold-chess | INFO | lessons-learned.md#L14 |
| frontend | 手写 IIFE 模块时，用 `window.ModuleName = Module` 暴露 API，内部私有变量用下划线... | 经验 | dom / api-design | blindfold-chess | WARNING | lessons-learned.md#L15 |
| general | 浏览器集成测试用 TestRunner（自定义极简框架），保持与 Node 测试同一套断言 API，降低切换成本 | 经验 | testing | blindfold-chess | INFO | lessons-learned.md#L16 |
| general | Canvas 图表渲染在浏览器中测试，Node 环境用 Mock 2D context 跳过绘制验证，各测其责 | 经验 | testing | blindfold-chess | INFO | lessons-learned.md#L17 |
| general | PGN 解析器对空/无效输入返回 `[]`（空数组）而非 `null`，调用方需区分"无走法"和"解析失败" | 经验 | data / api-design | blindfold-chess | INFO | lessons-learned.md#L18 |
| frontend | `cloneNode(true)` 替换含 SVG 的按钮会导致 SVG 渲染异常（显示不完整）；移除事件监听器应优先用... | 经验 | dom | blindfold-chess | WARNING | lessons-learned.md#L19 |
| frontend | 匿名事件监听器无法被后续代码移除；需要动态解除绑定的监听器必须用命名函数（暴露到 `window` 或模块内部变量） | 经验 | dom | blindfold-chess | WARNING | lessons-learned.md#L20 |
| frontend | 屏幕切换导航不能只隐藏上一个屏幕，必须遍历 `.screen` 全部隐藏后再显示目标，否则多层屏幕重叠 | 经验 | dom / ux | blindfold-chess | WARNING | lessons-learned.md#L21 |
| frontend | SVG path 中密集参数（如 `a2 2 0 0 1-2.83 0`）在某些浏览器中可能解析异常，命令与参数间保留空... | 经验 | dom | blindfold-chess | INFO | lessons-learned.md#L22 |
| frontend | `document` 级事件监听器若引用了某个 DOM 元素，该元素被替换后监听器仍会按旧引用判断，导致逻辑错误（如点击... | 经验 | dom | blindfold-chess | WARNING | lessons-learned.md#L23 |
| general | 项目文档结构会随时间进化，"存档"或"恢复"操作前应先 `ls`/`glob` 确认当前文件系统现状，避免按历史路径写入... | 经验 | ai-workflow | blindfold-chess | INFO | lessons-learned.md#L24 |
| frontend | **UI 布局/样式不要猜测用户意图**：候选走法开关经历了 5 次位置/样式反复，每次修改后用户都不满意；应在设计阶段... | 经验 | ux | blindfold-chess | CRITICAL | lessons-learned.md#L25 |
| general | **引擎候选走法的调用时机决定产品逻辑正确性**：用户走完后立即 `goMultiPv` 分析的是对手局面；若要提示用户... | 经验 | api-design | blindfold-chess | CRITICAL | lessons-learned.md#L26 |
| general | **引擎返回 UCI（e2e4），用户界面必须用 SAN（e4）**：`goMultiPv` 回调中的 `move` 是... | 经验 | data / api-design | blindfold-chess | WARNING | lessons-learned.md#L27 |
| frontend | **静态 HTML 结构与动态渲染模块的 DOM 冲突**：`index.html` 中预置了完整棋盘结构，而 `Boa... | 经验 | dom | blindfold-chess | WARNING | lessons-learned.md#L28 |
| general | **删除功能必须同步删除对应测试**：移除 `showHints` / `multiPvSetting` 后，相关测试会... | 经验 | testing | blindfold-chess | WARNING | lessons-learned.md#L29 |
| frontend | **焦点管理是盲棋产品的核心体验**：进入对局自动 `input.focus()`、引擎走完后恢复焦点、全局 Enter... | 经验 | ux | blindfold-chess | WARNING | lessons-learned.md#L30 |
| frontend | **i18n 分散架构必然导致翻译遗漏**：当项目同时存在"全局字典 + 模块私有字典 + 硬编码"三种翻译方式时，新增... | 经验 | i18n | blindfold-chess | CRITICAL | lessons-learned.md#L31 |
| frontend | **JS 中的硬编码人类可读字符串是翻译遗漏的重灾区**：HTML 中的 `data-i18n` 至少能被肉眼扫描到，但... | 经验 | i18n | blindfold-chess | WARNING | lessons-learned.md#L32 |
| frontend | **复制粘贴是 i18n 错误的常见来源**：将中文值直接粘贴进英文字典，或反之，属于低级但高频的疏忽 | 经验 | i18n | blindfold-chess | WARNING | lessons-learned.md#L33 |
| frontend | **模块内部字典若从不主动更新 DOM，则纯属冗余**：welcome.js 有 `_i18n` 和 `_t()`，但从... | 经验 | i18n / architecture | blindfold-chess | WARNING | lessons-learned.md#L34 |
| frontend | **settings.js 的独立字典与 common.js 的全局扫描存在竞争**：settings panel 的元... | 经验 | i18n / dom | blindfold-chess | WARNING | lessons-learned.md#L35 |
| general | **已删除的 JS 文件若不从 index.html 移除引用，会导致 404**：功能清理和引用清理必须是同一任务 | 经验 | build-env | blindfold-chess | WARNING | lessons-learned.md#L36 |
| general | **Node 测试不对 UI 文本做断言，无法捕获翻译错误**：只测 API 形状和数值，不检查按钮文字、提示语等人类可... | 经验 | testing | blindfold-chess | WARNING | lessons-learned.md#L37 |
| general | **删除生产代码的 fallback 函数前，必须先评估测试环境是否提供了该依赖**：架构统一重构必须同时改代码+测试，... | 经验 | testing / architecture | blindfold-chess | CRITICAL | lessons-learned.md#L38 |
| general | **`localStorage` mock 必须支持 `setItem` 持久化**：测试中 `global.local... | 经验 | testing | blindfold-chess | WARNING | lessons-learned.md#L39 |
| frontend | **全局 `updateTexts()` 与模块私有 `_updateXxx()` 可能存在 DOM 竞争**：两者操作... | 经验 | dom / i18n | blindfold-chess | WARNING | lessons-learned.md#L40 |
| frontend | **配置类设置项用「弹窗选择」优于「循环切换」**：循环切换隐藏了全部选项，用户不知道有哪些风格；弹窗一次展示所有选项+... | 经验 | ux | blindfold-chess | INFO | lessons-learned.md#L41 |
| frontend | **`cloneNode(true)` 无法移除旧事件监听器，它只是复制了 DOM 结构**：真正安全的解绑是 `rem... | 经验 | dom | blindfold-chess | WARNING | lessons-learned.md#L42 |
| frontend | **UI 风格不一致的根因通常是「硬编码颜色」**：引入统一的「棋盘风格配置源」后，所有棋盘自动同步，消除不一致的根因。... | 经验 | ux / architecture | blindfold-chess | WARNING | lessons-learned.md#L43 |
| frontend | **功能入口迁移需要同步更新「正向路径」和「反向路径」**：不仅要添加新入口，还要移除旧入口，否则用户会在两个地方看到同... | 经验 | ux / architecture | blindfold-chess | WARNING | lessons-learned.md#L44 |
| general | **数据层的双语字段与代码层的硬编码分支是两个问题**：区分"数据双语"和"代码分支"可避免过度重构 | 经验 | data / architecture | blindfold-chess | INFO | lessons-learned.md#L45 |
| general | **测试中断言的具体文本值是重构的敏感点**：重构前应先审计测试中的文本断言，预估需要调整的范围 | 经验 | testing | blindfold-chess | WARNING | lessons-learned.md#L46 |
| general | **数据文件中的引号嵌套是极易被忽视的语法陷阱**：在真实浏览器中会抛出 `SyntaxError` 并阻断后续脚本执行 | 经验 | data / build-env | blindfold-chess | WARNING | lessons-learned.md#L47 |
| general | **Node 测试全过 ≠ 浏览器表现正常**：必须用 headless 浏览器（playwright）才能捕获浏览器特... | 经验 | testing | blindfold-chess | WARNING | lessons-learned.md#L48 |
| general | **playwright 是定位浏览器特有 bug 的有效手段**：通过 `page.add_init_script` ... | 经验 | testing / debugging | blindfold-chess | INFO | lessons-learned.md#L49 |
| general | **通用配置层设计能降低新增模式的边际成本**：新增对局模式时只需加一行 `else if` 分发逻辑，无需重复造 DO... | 经验 | architecture | blindfold-chess | INFO | lessons-learned.md#L50 |
| general | **向后兼容接口设计能减少重构的连锁反应**：旧接口继续工作，内部映射新参数，所有旧测试和外部调用点无需改动 | 经验 | api-design | blindfold-chess | INFO | lessons-learned.md#L51 |
| frontend | 浏览器集成测试阶段发现 welcome.js / replay.js / stats.js 的 DOM 事件绑定遗漏 | 经验 | testing / dom | blindfold-chess | INFO | lessons-learned.md#L52 |
| general | Node 测试覆盖逻辑，浏览器测试覆盖 DOM 集成，两者互补 | 经验 | testing | blindfold-chess | INFO | lessons-learned.md#L53 |
| general | `AGENTS.md` 定义触发词和行为约束，`status.md` 记录动态进度，分工明确，新会话读 2 份文件即可开... | 经验 | ai-workflow | french-exit | INFO | lessons-learned.md#L54 |
| general | 每批次开发完成后同步更新进度文档，避免新会话迷路 | 经验 | ai-workflow | blindfold-chess | INFO | lessons-learned.md#L55 |
| general | **手工构建100条结构化数据不现实**：经典棋局的 PGN 分散在各网站，无统一免费 API；手动录入工作量巨大且易出... | 经验 | data | blindfold-chess | INFO | lessons-learned.md#L56 |
| general | **WriteFile 不适合超大特殊字符内容**：含大量引号/换行的长文本会因 JSON 转义失败；应改用本地 Pyt... | 经验 | ai-workflow | blindfold-chess | WARNING | lessons-learned.md#L57 |
| general | **Shell here-document 在 Windows git bash 中不可靠**：含引号的多行复杂脚本会被... | 经验 | cross-platform / ai-workflow | blindfold-chess | WARNING | lessons-learned.md#L58 |
| frontend | **翻译检查必须是独立任务，不能依赖"开发时顺手做"**：本次检查发现 25+ 处遗漏，分布在 HTML、JS 字典、硬... | 经验 | i18n / ai-workflow | blindfold-chess | WARNING | lessons-learned.md#L59 |
| general | **涉及 7+ 文件读改测的架构重构，应新开会话执行**：继续塞进系统性重构容易触发窗口压缩，导致信息丢失 | 经验 | ai-workflow | blindfold-chess | INFO | lessons-learned.md#L60 |
| general | GitHub Pages 国内访问需代理；unpkg CDN 加载 Stockfish 可能超时，需考虑离线备选方案 | 经验 | build-env | blindfold-chess | INFO | lessons-learned.md#L61 |
| general | Windows 路径在 git bash / Node.js / cmd 中转义规则不同，写跨平台脚本时优先用正斜杠或 ... | 经验 | cross-platform | blindfold-chess | WARNING | lessons-learned.md#L62 |
| general | `GetDiskFreeSpaceExW` 传 `&HSTRING` 作为路径参数，`Option<&mut u64>`... | 经验 | api-design | french-exit | INFO | lessons-learned.md#L64 |
| general | CPU% 精确计算只需 `GetProcessTimes` + wall clock elapsed，不需要 `GetS... | 经验 | api-design | french-exit | INFO | lessons-learned.md#L65 |
| general | `FILETIME` 转 u64：`((high as u64) << 32) | 经验 | api-design | `resource/controller.rs` | INFO | lessons-learned.md#L66 |
| general | `Arc<dyn Fn(...) + Send + Sync>` 是 Rust 中给同步结构体注入回调的标准方式 | 经验 | api-design | french-exit | INFO | lessons-learned.md#L67 |
| general | Tauri 前端用 vitest + jsdom 测试时，必须在 `setup.ts` 中 `vi.mock()` 所有... | 经验 | testing | french-exit | INFO | lessons-learned.md#L68 |
| general | 若 `@tauri-apps/api/xxx` 模块不存在（如 v2 移除了 `fs`），用 **vite alias*... | 经验 | build-env | french-exit | INFO | lessons-learned.md#L69 |
| general | Controlled checkbox 的测试用 `@testing-library/user-event` 的 `us... | 经验 | testing | french-exit | INFO | lessons-learned.md#L70 |
| general | `tokio::sync::mpsc::Sender::try_send()` 适合非阻塞的进度回调，避免 Scanne... | 经验 | api-design | french-exit | INFO | lessons-learned.md#L71 |
| rust-tauri | **绝对不要**在 `setState` 的 updater 函数内部调用 `dispatch()` 或其他 setSt... | 经验 | state-management | french-exit | CRITICAL | lessons-learned.md#L72 |
| rust-tauri | `useEffect` 依赖 `state.xxx.size === 0` 作为触发条件时，容易形成死循环（用户操作 →... | 经验 | state-management | french-exit | CRITICAL | lessons-learned.md#L73 |
| rust-tauri | `useRef` 作为"只执行一次"的标志，比依赖数组更可靠，尤其涉及批量初始化逻辑时 | 经验 | state-management | french-exit | WARNING | lessons-learned.md#L74 |
| general | **测试驱动暴露 Bug**：ResultsPage 的默认勾选死循环是在写单元测试时发现的，手工测试几乎不可能复现（需... | 经验 | testing | french-exit | INFO | lessons-learned.md#L75 |
| general | **结论**：前端状态管理类的 bug，单元测试是最有效的发现手段，远超手工测试 | 经验 | testing | french-exit | INFO | lessons-learned.md#L76 |
| general | `prompt-next-session.md` 的问题：每次都要重写环境初始化、模块速查表等**不变内容** | 经验 | ai-workflow | french-exit | INFO | lessons-learned.md#L77 |
| general | **改进**：`status.md`（活文档，只记录变化）+ `AGENTS.md`（固定规则） | 经验 | ai-workflow | french-exit | INFO | lessons-learned.md#L78 |
| general | **收益**：新会话读 2 份文件即可开工，维护成本降低 80% | 经验 | ai-workflow | french-exit | INFO | lessons-learned.md#L79 |
| general | **横跨工具层和应用层的词汇必须确认语境**。用户问"一个项目多个终端能否实现同步处理进度"——"终端"可以指并行 ex... | 经验 | ai-workflow | french-exit | WARNING | lessons-learned.md#L80 |
| general | **工具硬性限制不要绕圈分析可行性**。Kimi CLI 多窗口无 IPC、无共享内存、无实时同步——回答应直接给结论 ... | 经验 | ai-workflow | french-exit | WARNING | lessons-learned.md#L81 |
| general | **从 SOP 模板采纳更新时，必须逐字核对关键字段，不要凭记忆改写**。触发词「存档」错误抄写为「存储」，原因是未逐字... | 经验 | ai-workflow | french-exit | WARNING | lessons-learned.md#L82 |
| rust-tauri | 中文路径 + MinGW = 链接器失败。解决方案：复制到纯 ASCII 路径（如 `/c/french-exit`）后... | 经验 | cross-platform / build-env | french-exit | CRITICAL | lessons-learned.md#L83 |
| rust-tauri | `cargo check --lib` 不需要链接，可以在中文路径直接跑；`cargo test --no-run` 同... | 经验 | cross-platform / build-env | french-exit | INFO | lessons-learned.md#L84 |
| general | **`0xc0000139` 不一定是 UCRT/MinGW 兼容性 issue**。先跑一个**最简单 lib 测试*... | 经验 | debugging | french-exit | INFO | lessons-learned.md#L85 |
| general | **`cargo test --bin` 能过、`cargo test --lib` 崩溃** → 问题出在**仅被 l... | 经验 | debugging | french-exit | WARNING | lessons-learned.md#L86 |
| general | **定位代码的最快方法**：清空 `lib.rs` 只保留一个空测试，逐步 `pub mod` 添加模块，直到崩溃复现。... | 经验 | debugging | french-exit | INFO | lessons-learned.md#L87 |
| rust-tauri | **`tauri::AppHandle` 出现在 `async fn` 签名中 + MinGW = `STATUS_EN... | 经验 | cross-platform / build-env | french-exit | CRITICAL | lessons-learned.md#L88 |
| rust-tauri | **`#[cfg(not(test))]` 隔离问题代码**是零副作用的修复手法：release 构建完全不受影响，测试... | 经验 | testing / cross-platform | french-exit | INFO | lessons-learned.md#L89 |
| frontend | `useRef` + `mousedown` 监听实现点击外部关闭 | 经验 | dom / ux | french-exit | INFO | lessons-learned.md#L90 |
| frontend | CSS `@keyframes dropdownIn` 实现淡入+位移动画 | 经验 | ux | french-exit | INFO | lessons-learned.md#L91 |
| frontend | 年月日联动限制（如今年只显示到当前月） | 经验 | ux | french-exit | INFO | lessons-learned.md#L92 |
| general | `cargo tauri dev` 必须在**交互式 Windows 桌面会话**中运行，无法通过远程/后台任务启动（W... | 经验 | build-env | french-exit | INFO | lessons-learned.md#L93 |
| general | **替代方案**：`npm run dev` 启动 Vite 服务器 → 浏览器访问 `http://localhost... | 经验 | build-env | french-exit | INFO | lessons-learned.md#L94 |
| general | **完整功能验证**：仍需本地运行 `cargo tauri dev` 或双击 release `.exe` | 经验 | build-env | french-exit | INFO | lessons-learned.md#L95 |
| general | 不要一次性加载所有完整 `TraceItem` 到前端（内存 + DOM 渲染压力大） | 经验 | data / performance | french-exit | WARNING | lessons-learned.md#L96 |
| general | 正确做法：后端提供**轻量摘要接口**（只返回 id + category + suggested_action），前端... | 经验 | architecture / data | french-exit | INFO | lessons-learned.md#L97 |
| rust-tauri | 用户实际浏览仍按分页，但"全选全部"走轻量接口，两者解耦 | 经验 | pagination / architecture | french-exit | WARNING | lessons-learned.md#L98 |
| rust-tauri | **事故经过**：ResultsPage 默认自动勾选所有扫描结果 → 用户点击"全选全部"（以为是全选当前页，实际是全... | 经验 | pagination / state-management / security | french-exit | CRITICAL | lessons-learned.md#L99 |
| rust-tauri | **根因链**：默认勾选 × deselectAll 只清当前页 × ConfirmPage 遍历 scanResult... | 经验 | pagination / state-management | french-exit | CRITICAL | lessons-learned.md#L100 |
| rust-tauri | **教训**：涉及删除的安全工具，**默认安全 > 默认便利**。所有选择必须用户显式操作，任何"帮你选好"的设计都需反... | 经验 | security / ux | french-exit | CRITICAL | lessons-learned.md#L101 |
| rust-tauri | **原实现**：`deselectAll` 只遍历 `searchedItems`（当前页数据），从 `selected... | 经验 | pagination / state-management | french-exit | WARNING | lessons-learned.md#L102 |
| rust-tauri | **修复**：`deselectAll` 清空 `selectedIds` 为 `new Set()`，同时 `disp... | 经验 | pagination / state-management | french-exit | INFO | lessons-learned.md#L103 |
| rust-tauri | **教训**：跨分页操作时，"取消"必须与"全选"的对称——全选影响多大范围，取消就必须影响多大范围 | 经验 | pagination / state-management | french-exit | WARNING | lessons-learned.md#L104 |
| rust-tauri | **原实现**：ConfirmPage 遍历 `state.scanResults`，过滤出选中的项 → 分页未加载的项... | 经验 | pagination / state-management | french-exit | WARNING | lessons-learned.md#L105 |
| rust-tauri | **修复**：遍历 `state.decisions`，每项在 `scanResults` 中查找详细信息，找不到时用 ... | 经验 | pagination / state-management | french-exit | INFO | lessons-learned.md#L106 |
| rust-tauri | **教训**：在分页/懒加载架构中，**用户操作集合（decisions）是主数据源，展示数据（scanResults）... | 经验 | pagination / architecture | french-exit | WARNING | lessons-learned.md#L107 |
| general | 在 Kimi Code CLI 上安装 Superpowers 需分 A/B 方案：A 方案替换 CLI 为 feat/... | 经验 | 未分类 | vibe-coding-project-sop | INFO | lessons-learned.md#L160 |
| general | 评估 skill 是否适合当前项目时，不应只看功能描述，而应对比项目形态（纯文档/工具型项目不需要 frontend-d... | 经验 | 未分类 | vibe-coding-project-sop | INFO | lessons-learned.md#L161 |
| general | PowerShell 5.1 默认以 Windows-1252 编码读取无 BOM 的 UTF-8 文件，中文字符被解码... | 经验 | 未分类 | vibe-coding-project-sop | INFO | lessons-learned.md#L162 |
| general | ModelScope 首页 HTTP 访问速度（~8KB/s）与实际 CDN 模型下载速度（~2.5MB/s）差异巨大，... | 经验 | 未分类 | vibe-coding-project-sop | INFO | lessons-learned.md#L163 |
| general | GitHub 下载完全不可达时，可尝试加速镜像 gh.llkk.cc，实测速度 300KB/s+，支持断点续传 | 经验 | 未分类 | vibe-coding-project-sop | INFO | lessons-learned.md#L164 |
| general | llama.cpp 的 server 模式兼容 OpenAI API 格式（/v1/chat/completions），... | 经验 | 未分类 | vibe-coding-project-sop | INFO | lessons-learned.md#L165 |
| general | macOS 无 Homebrew 时，GitHub CLI 可直接下载官方 zip 包，解压后放到 `~/bin/` 即... | 经验 | 未分类 | vibe-coding-project-sop | INFO | lessons-learned.md#L166 |
| general | `gh` 底层是 Go 程序，默认不走系统代理。访问 GitHub API 时必须显式设置 `HTTPS_PROXY` ... | 经验 | 未分类 | vibe-coding-project-sop | INFO | lessons-learned.md#L167 |
| general | 从 SSH 协议切换到 HTTPS + `gh auth setup-git` 后，`git push` 完全由 gh ... | 经验 | 未分类 | vibe-coding-project-sop | INFO | lessons-learned.md#L168 |
| general | Git for Windows 的 bash `/tmp` 与 PowerShell `$env:TEMP` 指向同一物... | 经验 | build-env | vibe-coding-project-sop | INFO | lessons-learned.md#L174 |
| general | 国内下载 HuggingFace 模型时，ModelScope 是比 hf-mirror 更可靠的 fallback（后... | 经验 | build-env | vibe-coding-project-sop | INFO | lessons-learned.md#L175 |
| general | Windows 非管理员运行 PowerShell 脚本时，`New-NetFirewallRule` 会失败，但 `l... | 经验 | build-env | vibe-coding-project-sop | WARNING | lessons-learned.md#L176 |
| general | `gh api --paginate --slurp` 返回嵌套数组 `[page1, page2, ...]`（每页一... | 经验 | api-design | 母库 | WARNING | lessons-learned.md#L208 |
| general | ADR-001：前端技术栈选型 | 决策 | 架构决策 | blindfold-chess | — | ADR.md#L8 |
| general | ADR-002：测试框架选型 | 决策 | 架构决策 | blindfold-chess | — | ADR.md#L22 |
| general | ADR-003：AI 开发方式与批次划分 | 决策 | 架构决策 | blindfold-chess | — | ADR.md#L36 |
| general | ADR-004：棋盘渲染与棋子方案 | 决策 | 架构决策 | blindfold-chess | — | ADR.md#L50 |
| general | ADR-005：数据持久化方案 | 决策 | 架构决策 | blindfold-chess | — | ADR.md#L64 |
| general | ADR-006：通用对局配置层设计 | 决策 | 架构决策 | blindfold-chess | — | ADR.md#L78 |
| general | ADR-007：难度选择从离散按钮改为连续滑块 | 决策 | 架构决策 | blindfold-chess | — | ADR.md#L92 |
| general | ADR-008：棋盘风格设置交互方案 | 决策 | 架构决策 | blindfold-chess | — | ADR.md#L106 |
| general | ADR-009：盲棋复盘入口位置 | 决策 | 架构决策 | blindfold-chess | — | ADR.md#L120 |
| general | ADR-017：GitHub 认证从 SSH 切换到 GitHub CLI + HTTPS | 决策 | 架构决策 | vibe-coding-project-sop | — | ADR.md#L132 |
| general | ADR-001：为什么用 Tauri（Rust + WebView2）而非 Electron？ | 决策 | 架构决策 | french-exit | — | ADR.md#L147 |
| general | ADR-002：为什么前端用 React（而非 Vue/Svelte）？ | 决策 | 架构决策 | french-exit | — | ADR.md#L160 |
| general | ADR-003：为什么 CPU% 用 `GetProcessTimes` 而非 `sysinfo` crate？ | 决策 | 架构决策 | french-exit | — | ADR.md#L174 |
| general | ADR-004：为什么 Scanner 进度用 `mpsc::channel` 而非 `tokio::sync::wat... | 决策 | 架构决策 | french-exit | — | ADR.md#L188 |
| general | ADR-005：为什么加密文件回调用同步 `Fn` 而非 `async`？ | 决策 | 架构决策 | french-exit | — | ADR.md#L202 |
| general | ADR-006：为什么用 `status.md` + `session-log.md` 替代 `prompt-next-... | 决策 | 架构决策 | french-exit | — | ADR.md#L216 |
| general | ADR-007：WebView2 分发策略——放弃 NSIS bootstrapper，改用携带 DLL | 决策 | 架构决策 | french-exit | — | ADR.md#L228 |
| general | ADR-008：默认深色主题而非跟随系统 | 决策 | 架构决策 | french-exit | — | ADR.md#L240 |
| general | ADR-009：全选全部功能的技术方案 | 决策 | 架构决策 | french-exit | — | ADR.md#L252 |
| general | ADR-010：路径交互设计 — 文本可点击 vs 独立按钮 | 决策 | 架构决策 | french-exit | — | ADR.md#L264 |
| general | ADR-011：删除策略从 DoD 安全擦除改为普通删除 | 决策 | 架构决策 | french-exit | — | ADR.md#L276 |
| general | ADR-012：扫描范围从 Desktop/Downloads 扩展为全盘扫描 | 决策 | 架构决策 | french-exit | — | ADR.md#L288 |
| general | ADR-013：移除 ResultsPage 默认自动勾选 | 决策 | 架构决策 | french-exit | — | ADR.md#L300 |
| general | ADR-014：同步脚本优先使用仓库 default_branch | 决策 | 架构决策 | vibe-coding-project-sop | — | ADR.md#L314 |
| general | ADR-015：syncFrom 配置实现聚合/分发双模式 | 决策 | 架构决策 | vibe-coding-project-sop | — | ADR.md#L326 |
| general | ADR-016：母库 AGENTS 与其他项目 AGENTS 物理分离 | 决策 | 架构决策 | vibe-coding-project-sop | — | ADR.md#L338 |
| general | ADR-009：Troubleshooting 索引采用独立文件 + 行号链接 | 决策 | 架构决策 |  | — | ADR.md#L392 |
| general | ADR-017：init-skeleton.py 保持 Python 3.9 兼容 | 决策 | 架构决策 |  | — | ADR.md#L416 |
| general | ADR-017：假删除模式通过环境变量 `FRENCH_EXIT_DRY_RUN` 控制 [来源:french-exit... | 决策 | 架构决策 | french-exit | — | ADR.md#L442 |
| general | ADR-017：扫描进度条采用后端全局加权进度计算 | 决策 | 架构决策 | french-exit | — | ADR.md#L458 |
| general | ADR-018：个人目录全量扫描 + 文件类型分类 | 决策 | 架构决策 | french-exit | — | ADR.md#L473 |
| general | ADR-018：WebView2 安装模式选择 downloadBootstrapper | 决策 | 架构决策 | french-exit | — | ADR.md#L491 |
| python-data | ADR-001：技术栈选型（Python 3 + requests） | 决策 | 架构决策 | qianniu_business_analytics | — | ADR.md#L510 |
| python-data | ADR-002：渠道范围限定（仅淘系生意参谋） | 决策 | 架构决策 | qianniu_business_analytics | — | ADR.md#L524 |
| python-data | ADR-003：Cookie 刷新策略（Digest 自动刷新，不问用户） | 决策 | 架构决策 | qianniu_business_analytics | — | ADR.md#L538 |
| python-data | ADR-004：日期时间格式（T00:00:00+08:00，禁用 23:59:59） | 决策 | 架构决策 | qianniu_business_analytics | — | ADR.md#L552 |
| python-data | ADR-005：报告形态（Markdown 四段式，单店/多店统一） | 决策 | 架构决策 | qianniu_business_analytics | — | ADR.md#L566 |
| python-data | ADR-017：聚焦 Excel 驱动流，API 驱动流暂不投入 [来源:qianniu_business_analyt... | 决策 | 架构决策 | qianniu_business_analytics | — | ADR.md#L584 |
| general | ADR-019：Node.js 环境隔离方案（nvm + 双 Node.js） [母库 @2026-05-30] | 决策 | 架构决策 | vibe-coding-project-sop | — | ADR.md#L598 |
| general | ADR-020：状态文档机制重构（待办清理 + 技术债务表格化） [母库 @2026-05-30] | 决策 | 架构决策 | vibe-coding-project-sop | — | ADR.md#L612 |
| python-data | ADR-022：保持 `qianniu_business_analytics` 与 `ecommerce-report-... | 决策 | 架构决策 | qianniu_business_analytics | — | ADR.md#L626 |

---

## 按技术栈分组

> 一个条目可能同时属于多个技术栈。

### Rust / Tauri

- [问题] `cargo check --lib` 报错：`GetDiskFreeSpaceExW` 未定义 — `运行时` → troubleshooting.md#L124
- [问题] `cargo check --lib` 报错：`FILETIME` 未定义 — `运行时` → troubleshooting.md#L132
- [问题] `cargo test --lib` 报错 `0xc0000139`（UCRT DLL 缺失） — `运行时错误` → troubleshooting.md#L144
- [问题] 运行 `french-exit.exe` 报错：`Could not find the WebVie — `运行时错误` → troubleshooting.md#L156
- [问题] 运行 `french-exit.exe` 报错：`找不到 WebView2Loader.dll` — `运行时错误` → troubleshooting.md#L164
- [问题] `cargo tauri build` 失败：`另一个程序正在使用此文件` (os error 32 — `运行时错误` → troubleshooting.md#L172
- [问题] vitest 报错：`Failed to resolve import "@tauri-apps/a — `测试错误` → troubleshooting.md#L182
- [问题] cargo tauri dev 在后台任务中崩溃 — `环境问题` → troubleshooting.md#L232
- [经验] `GetDiskFreeSpaceExW` 传 `&HSTRING` 作为路径参数，`Option< — `api-design` → lessons-learned.md#L64
- [经验] `FILETIME` 转 u64：`((high as u64) << 32) — `api-design` → lessons-learned.md#L66
- [经验] `Arc<dyn Fn(...) + Send + Sync>` 是 Rust 中给同步结构体注入回 — `api-design` → lessons-learned.md#L67
- [经验] Tauri 前端用 vitest + jsdom 测试时，必须在 `setup.ts` 中 `vi. — `testing` → lessons-learned.md#L68
- [经验] 若 `@tauri-apps/api/xxx` 模块不存在（如 v2 移除了 `fs`），用 **v — `build-env` → lessons-learned.md#L69
- [经验] 中文路径 + MinGW = 链接器失败。解决方案：复制到纯 ASCII 路径（如 `/c/fren — `cross-platform / build-env` → lessons-learned.md#L83
- [经验] `cargo check --lib` 不需要链接，可以在中文路径直接跑；`cargo test - — `cross-platform / build-env` → lessons-learned.md#L84
- [经验] **`0xc0000139` 不一定是 UCRT/MinGW 兼容性 issue**。先跑一个**最 — `debugging` → lessons-learned.md#L85
- [经验] **`cargo test --bin` 能过、`cargo test --lib` 崩溃** →  — `debugging` → lessons-learned.md#L86
- [经验] **`tauri::AppHandle` 出现在 `async fn` 签名中 + MinGW =  — `cross-platform / build-env` → lessons-learned.md#L88
- [经验] `cargo tauri dev` 必须在**交互式 Windows 桌面会话**中运行，无法通过远 — `build-env` → lessons-learned.md#L93
- [经验] **完整功能验证**：仍需本地运行 `cargo tauri dev` 或双击 release `. — `build-env` → lessons-learned.md#L95
- [决策] ADR-001：为什么用 Tauri（Rust + WebView2）而非 Electron？ — `架构决策` → ADR.md#L147
- [决策] ADR-003：为什么 CPU% 用 `GetProcessTimes` 而非 `sysinfo`  — `架构决策` → ADR.md#L174
- [决策] ADR-007：WebView2 分发策略——放弃 NSIS bootstrapper，改用携带 D — `架构决策` → ADR.md#L228
- [决策] ADR-018：WebView2 安装模式选择 downloadBootstrapper — `架构决策` → ADR.md#L491

### JavaScript / React / Vitest

- [问题] Node.js 测试运行时 chess.js 未定义 — `开发/测试` → troubleshooting.md#L41
- [问题] JS 数据文件嵌套单引号导致 `Unexpected identifier` — `运行时` → troubleshooting.md#L92
- [问题] mock DOM 中 `querySelector` / `querySelectorAll` 缺失 — `运行时` → troubleshooting.md#L112
- [问题] vitest 报错：`Failed to resolve import "@tauri-apps/a — `测试错误` → troubleshooting.md#L182
- [问题] vitest 报错：`act is not a function` — `测试错误` → troubleshooting.md#L191
- [问题] vitest 报错：React 警告 `Cannot update a component whil — `测试错误` → troubleshooting.md#L199
- [问题] Node.js 报 SyntaxError: Unexpected identifier（i18n  — `存档提示` → troubleshooting.md#L665
- [问题] Node.js 环境污染：Hermes Node.js 泄漏到用户 PATH — `存档提示` → troubleshooting.md#L1145
- [经验] 纯 HTML+CSS+JS 项目无需 npm，双击 `index.html` 即可预览，但涉及 We — `build-env / testing` → lessons-learned.md#L14
- [经验] 手写 IIFE 模块时，用 `window.ModuleName = Module` 暴露 API， — `dom / api-design` → lessons-learned.md#L15
- [经验] 浏览器集成测试用 TestRunner（自定义极简框架），保持与 Node 测试同一套断言 API， — `testing` → lessons-learned.md#L16
- [经验] Canvas 图表渲染在浏览器中测试，Node 环境用 Mock 2D context 跳过绘制验证 — `testing` → lessons-learned.md#L17
- [经验] `cloneNode(true)` 替换含 SVG 的按钮会导致 SVG 渲染异常（显示不完整）；移 — `dom` → lessons-learned.md#L19
- [经验] 匿名事件监听器无法被后续代码移除；需要动态解除绑定的监听器必须用命名函数（暴露到 `window`  — `dom` → lessons-learned.md#L20
- [经验] 屏幕切换导航不能只隐藏上一个屏幕，必须遍历 `.screen` 全部隐藏后再显示目标，否则多层屏幕重 — `dom / ux` → lessons-learned.md#L21
- [经验] SVG path 中密集参数（如 `a2 2 0 0 1-2.83 0`）在某些浏览器中可能解析异常 — `dom` → lessons-learned.md#L22
- [经验] `document` 级事件监听器若引用了某个 DOM 元素，该元素被替换后监听器仍会按旧引用判断， — `dom` → lessons-learned.md#L23
- [经验] **静态 HTML 结构与动态渲染模块的 DOM 冲突**：`index.html` 中预置了完整棋 — `dom` → lessons-learned.md#L28
- [经验] **模块内部字典若从不主动更新 DOM，则纯属冗余**：welcome.js 有 `_i18n` 和 — `i18n / architecture` → lessons-learned.md#L34
- [经验] **settings.js 的独立字典与 common.js 的全局扫描存在竞争**：setting — `i18n / dom` → lessons-learned.md#L35
- [经验] **Node 测试不对 UI 文本做断言，无法捕获翻译错误**：只测 API 形状和数值，不检查按钮 — `testing` → lessons-learned.md#L37
- [经验] **全局 `updateTexts()` 与模块私有 `_updateXxx()` 可能存在 DOM — `dom / i18n` → lessons-learned.md#L40
- [经验] **`cloneNode(true)` 无法移除旧事件监听器，它只是复制了 DOM 结构**：真正安 — `dom` → lessons-learned.md#L42
- [经验] **Node 测试全过 ≠ 浏览器表现正常**：必须用 headless 浏览器（playwrigh — `testing` → lessons-learned.md#L48
- [经验] **通用配置层设计能降低新增模式的边际成本**：新增对局模式时只需加一行 `else if` 分发逻 — `architecture` → lessons-learned.md#L50
- [经验] 浏览器集成测试阶段发现 welcome.js / replay.js / stats.js 的 DO — `testing / dom` → lessons-learned.md#L52
- [经验] Node 测试覆盖逻辑，浏览器测试覆盖 DOM 集成，两者互补 — `testing` → lessons-learned.md#L53
- [经验] **WriteFile 不适合超大特殊字符内容**：含大量引号/换行的长文本会因 JSON 转义失败 — `ai-workflow` → lessons-learned.md#L57
- [经验] Windows 路径在 git bash / Node.js / cmd 中转义规则不同，写跨平台脚 — `cross-platform` → lessons-learned.md#L62
- [经验] Tauri 前端用 vitest + jsdom 测试时，必须在 `setup.ts` 中 `vi. — `testing` → lessons-learned.md#L68
- [经验] 若 `@tauri-apps/api/xxx` 模块不存在（如 v2 移除了 `fs`），用 **v — `build-env` → lessons-learned.md#L69
- [经验] Controlled checkbox 的测试用 `@testing-library/user-ev — `testing` → lessons-learned.md#L70
- [经验] **绝对不要**在 `setState` 的 updater 函数内部调用 `dispatch()` — `state-management` → lessons-learned.md#L72
- [经验] `useRef` + `mousedown` 监听实现点击外部关闭 — `dom / ux` → lessons-learned.md#L90
- [经验] **替代方案**：`npm run dev` 启动 Vite 服务器 → 浏览器访问 `http:/ — `build-env` → lessons-learned.md#L94
- [经验] 不要一次性加载所有完整 `TraceItem` 到前端（内存 + DOM 渲染压力大） — `data / performance` → lessons-learned.md#L96
- [决策] ADR-002：为什么前端用 React（而非 Vue/Svelte）？ — `架构决策` → ADR.md#L160
- [决策] ADR-019：Node.js 环境隔离方案（nvm + 双 Node.js） [母库 @2026- — `架构决策` → ADR.md#L598

### Python

- [经验] **WriteFile 不适合超大特殊字符内容**：含大量引号/换行的长文本会因 JSON 转义失败 — `ai-workflow` → lessons-learned.md#L57
- [决策] ADR-017：init-skeleton.py 保持 Python 3.9 兼容 — `架构决策` → ADR.md#L416
- [决策] ADR-001：技术栈选型（Python 3 + requests） — `架构决策` → ADR.md#L510

### AI 工具链 / LLM

- [问题] HuggingFace 模型下载连接超时 `curl: (28) Could not connect — `存档提示` → troubleshooting.md#L283
- [经验] ModelScope 首页 HTTP 访问速度（~8KB/s）与实际 CDN 模型下载速度（~2.5 — `未分类` → lessons-learned.md#L163
- [经验] llama.cpp 的 server 模式兼容 OpenAI API 格式（/v1/chat/com — `未分类` → lessons-learned.md#L165
- [经验] 国内下载 HuggingFace 模型时，ModelScope 是比 hf-mirror 更可靠的  — `build-env` → lessons-learned.md#L175
- [经验] Windows 非管理员运行 PowerShell 脚本时，`New-NetFirewallRule — `build-env` → lessons-learned.md#L176

### Git / GitHub

- [问题] GitHub Pages 国内打不开 — `未分类` → troubleshooting.md#L28
- [问题] GitHub push 报错 `Permission denied (publickey)` — `存档提示` → troubleshooting.md#L265
- [问题] `gh auth login` 超时：`read tcp ... operation timed o — `存档提示` → troubleshooting.md#L274
- [问题] Windows Git Bash LF/CRLF 警告 — `环境相关` → troubleshooting.md#L1113
- [问题] Hermes Agent Git 合并冲突导致 SyntaxError — `存档提示` → troubleshooting.md#L1133
- [经验] **Shell here-document 在 Windows git bash 中不可靠**：含引 — `cross-platform / ai-workflow` → lessons-learned.md#L58
- [经验] GitHub Pages 国内访问需代理；unpkg CDN 加载 Stockfish 可能超时，需 — `build-env` → lessons-learned.md#L61
- [经验] Windows 路径在 git bash / Node.js / cmd 中转义规则不同，写跨平台脚 — `cross-platform` → lessons-learned.md#L62
- [经验] GitHub 下载完全不可达时，可尝试加速镜像 gh.llkk.cc，实测速度 300KB/s+，支 — `未分类` → lessons-learned.md#L164
- [经验] macOS 无 Homebrew 时，GitHub CLI 可直接下载官方 zip 包，解压后放到  — `未分类` → lessons-learned.md#L166
- [经验] `gh` 底层是 Go 程序，默认不走系统代理。访问 GitHub API 时必须显式设置 `HTT — `未分类` → lessons-learned.md#L167
- [经验] 从 SSH 协议切换到 HTTPS + `gh auth setup-git` 后，`git pus — `未分类` → lessons-learned.md#L168
- [经验] Git for Windows 的 bash `/tmp` 与 PowerShell `$env:T — `build-env` → lessons-learned.md#L174
- [决策] ADR-017：GitHub 认证从 SSH 切换到 GitHub CLI + HTTPS — `架构决策` → ADR.md#L132

### 网络 / 环境 / 权限

- [问题] GitHub Pages 国内打不开 — `未分类` → troubleshooting.md#L28
- [问题] 中文路径下编译失败 — `环境问题` → troubleshooting.md#L221
- [问题] HuggingFace 模型下载连接超时 `curl: (28) Could not connect — `存档提示` → troubleshooting.md#L283
- [问题] PowerShell 添加防火墙规则权限不足 `Access is denied` — `存档提示` → troubleshooting.md#L292
- [问题] Node.js 环境污染：Hermes Node.js 泄漏到用户 PATH — `存档提示` → troubleshooting.md#L1145
- [问题] distribute.py 子进程 GBK 编码错误 — `存档提示` → troubleshooting.md#L1408
- [经验] SVG path 中密集参数（如 `a2 2 0 0 1-2.83 0`）在某些浏览器中可能解析异常 — `dom` → lessons-learned.md#L22
- [经验] **UI 布局/样式不要猜测用户意图**：候选走法开关经历了 5 次位置/样式反复，每次修改后用户都 — `ux` → lessons-learned.md#L25
- [经验] **i18n 分散架构必然导致翻译遗漏**：当项目同时存在"全局字典 + 模块私有字典 + 硬编码" — `i18n` → lessons-learned.md#L31
- [经验] **JS 中的硬编码人类可读字符串是翻译遗漏的重灾区**：HTML 中的 `data-i18n` 至 — `i18n` → lessons-learned.md#L32
- [经验] **UI 风格不一致的根因通常是「硬编码颜色」**：引入统一的「棋盘风格配置源」后，所有棋盘自动同步 — `ux / architecture` → lessons-learned.md#L43
- [经验] **数据层的双语字段与代码层的硬编码分支是两个问题**：区分"数据双语"和"代码分支"可避免过度重构 — `data / architecture` → lessons-learned.md#L45
- [经验] **翻译检查必须是独立任务，不能依赖"开发时顺手做"**：本次检查发现 25+ 处遗漏，分布在 HT — `i18n / ai-workflow` → lessons-learned.md#L59
- [经验] GitHub Pages 国内访问需代理；unpkg CDN 加载 Stockfish 可能超时，需 — `build-env` → lessons-learned.md#L61
- [经验] Windows 路径在 git bash / Node.js / cmd 中转义规则不同，写跨平台脚 — `cross-platform` → lessons-learned.md#L62
- [经验] 中文路径 + MinGW = 链接器失败。解决方案：复制到纯 ASCII 路径（如 `/c/fren — `cross-platform / build-env` → lessons-learned.md#L83
- [经验] `cargo check --lib` 不需要链接，可以在中文路径直接跑；`cargo test - — `cross-platform / build-env` → lessons-learned.md#L84
- [经验] PowerShell 5.1 默认以 Windows-1252 编码读取无 BOM 的 UTF-8  — `未分类` → lessons-learned.md#L162
- [经验] ModelScope 首页 HTTP 访问速度（~8KB/s）与实际 CDN 模型下载速度（~2.5 — `未分类` → lessons-learned.md#L163
- [经验] `gh` 底层是 Go 程序，默认不走系统代理。访问 GitHub API 时必须显式设置 `HTT — `未分类` → lessons-learned.md#L167
- [经验] 国内下载 HuggingFace 模型时，ModelScope 是比 hf-mirror 更可靠的  — `build-env` → lessons-learned.md#L175
- [经验] Windows 非管理员运行 PowerShell 脚本时，`New-NetFirewallRule — `build-env` → lessons-learned.md#L176

### Windows / PowerShell

- [问题] `cargo test --lib` 报错 `0xc0000139`（UCRT DLL 缺失） — `运行时错误` → troubleshooting.md#L144
- [问题] 运行 `french-exit.exe` 报错：`Could not find the WebVie — `运行时错误` → troubleshooting.md#L156
- [问题] 运行 `french-exit.exe` 报错：`找不到 WebView2Loader.dll` — `运行时错误` → troubleshooting.md#L164
- [问题] PowerShell 执行中文脚本报 "UnexpectedToken" — `存档提示` → troubleshooting.md#L253
- [问题] PowerShell 添加防火墙规则权限不足 `Access is denied` — `存档提示` → troubleshooting.md#L292
- [问题] French Exit 进程锁定 exe 导致复制失败 — `存档提示` → troubleshooting.md#L684
- [问题] Windows Git Bash LF/CRLF 警告 — `环境相关` → troubleshooting.md#L1113
- [经验] **Shell here-document 在 Windows git bash 中不可靠**：含引 — `cross-platform / ai-workflow` → lessons-learned.md#L58
- [经验] Windows 路径在 git bash / Node.js / cmd 中转义规则不同，写跨平台脚 — `cross-platform` → lessons-learned.md#L62
- [经验] **横跨工具层和应用层的词汇必须确认语境**。用户问"一个项目多个终端能否实现同步处理进度"——"终 — `ai-workflow` → lessons-learned.md#L80
- [经验] 中文路径 + MinGW = 链接器失败。解决方案：复制到纯 ASCII 路径（如 `/c/fren — `cross-platform / build-env` → lessons-learned.md#L83
- [经验] **`0xc0000139` 不一定是 UCRT/MinGW 兼容性 issue**。先跑一个**最 — `debugging` → lessons-learned.md#L85
- [经验] **`tauri::AppHandle` 出现在 `async fn` 签名中 + MinGW =  — `cross-platform / build-env` → lessons-learned.md#L88
- [经验] `cargo tauri dev` 必须在**交互式 Windows 桌面会话**中运行，无法通过远 — `build-env` → lessons-learned.md#L93
- [经验] **完整功能验证**：仍需本地运行 `cargo tauri dev` 或双击 release `. — `build-env` → lessons-learned.md#L95
- [经验] PowerShell 5.1 默认以 Windows-1252 编码读取无 BOM 的 UTF-8  — `未分类` → lessons-learned.md#L162
- [经验] Git for Windows 的 bash `/tmp` 与 PowerShell `$env:T — `build-env` → lessons-learned.md#L174
- [经验] Windows 非管理员运行 PowerShell 脚本时，`New-NetFirewallRule — `build-env` → lessons-learned.md#L176
- [决策] ADR-007：WebView2 分发策略——放弃 NSIS bootstrapper，改用携带 D — `架构决策` → ADR.md#L228

### Chess / 引擎

- [问题] Stockfish 加载超时 / 引擎不启动 — `未分类` → troubleshooting.md#L19
- [问题] Node.js 测试运行时 chess.js 未定义 — `开发/测试` → troubleshooting.md#L41
- [经验] 纯 HTML+CSS+JS 项目无需 npm，双击 `index.html` 即可预览，但涉及 We — `build-env / testing` → lessons-learned.md#L14
- [经验] PGN 解析器对空/无效输入返回 `[]`（空数组）而非 `null`，调用方需区分"无走法"和"解 — `data / api-design` → lessons-learned.md#L18
- [经验] `cloneNode(true)` 替换含 SVG 的按钮会导致 SVG 渲染异常（显示不完整）；移 — `dom` → lessons-learned.md#L19
- [经验] **引擎候选走法的调用时机决定产品逻辑正确性**：用户走完后立即 `goMultiPv` 分析的是对 — `api-design` → lessons-learned.md#L26
- [经验] **引擎返回 UCI（e2e4），用户界面必须用 SAN（e4）**：`goMultiPv` 回调中 — `data / api-design` → lessons-learned.md#L27
- [经验] **`cloneNode(true)` 无法移除旧事件监听器，它只是复制了 DOM 结构**：真正安 — `dom` → lessons-learned.md#L42
- [经验] **手工构建100条结构化数据不现实**：经典棋局的 PGN 分散在各网站，无统一免费 API；手动 — `data` → lessons-learned.md#L56
- [经验] GitHub Pages 国内访问需代理；unpkg CDN 加载 Stockfish 可能超时，需 — `build-env` → lessons-learned.md#L61

### 其他

- [问题] AI 重复实现已有组件（棋盘/网格类 UI） — `未分类` → troubleshooting.md#L8
- [问题] CLI subAgent 并行超时 — `开发/测试` → troubleshooting.md#L50
- [问题] 设置面板一闪而过 — `开发/测试` → troubleshooting.md#L59
- [问题] 旧代码与新模块冲突 — `运行时` → troubleshooting.md#L72
- [问题] 引擎候选走法未集成 — `运行时` → troubleshooting.md#L81
- [问题] 设置面板点击无反应（panel toggle 测试失败） — `运行时` → troubleshooting.md#L102
- [问题] checkbox 点击后状态不变化 — `测试错误` → troubleshooting.md#L208
- [问题] sed 批量修改误改结构体定义 — `存档提示` → troubleshooting.md#L675
- [问题] Cookie 过期 / 401 认证失败 — `存档提示` → troubleshooting.md#L1029
- [问题] Digest 刷新失败 — `存档提示` → troubleshooting.md#L1038
- [问题] auth/jycm.json 缺失字段 — `存档提示` → troubleshooting.md#L1047
- [问题] 日期区间多返回一天 — `取数相关` → troubleshooting.md#L1060
- [问题] getAllShopList 返回空数组 — `取数相关` → troubleshooting.md#L1069
- [问题] createAndDownload 返回失败 — `取数相关` → troubleshooting.md#L1078
- [问题] openpyxl 未安装 — `报告相关` → troubleshooting.md#L1091
- [问题] 钉钉推送失败 — `报告相关` → troubleshooting.md#L1100
- [问题] CodeBuddy 安装后 package.json 丢失导致命令不可用 — `存档提示` → troubleshooting.md#L1163
- [问题] 条目状态流转 — `存档提示` → troubleshooting.md#L1373
- [问题] 新增条目模板 — `存档提示` → troubleshooting.md#L1391
- [问题] [错误关键词] — `存档提示` → troubleshooting.md#L1395
- [经验] 项目文档结构会随时间进化，"存档"或"恢复"操作前应先 `ls`/`glob` 确认当前文件系统现状 — `ai-workflow` → lessons-learned.md#L24
- [经验] **删除功能必须同步删除对应测试**：移除 `showHints` / `multiPvSettin — `testing` → lessons-learned.md#L29
- [经验] **焦点管理是盲棋产品的核心体验**：进入对局自动 `input.focus()`、引擎走完后恢复焦 — `ux` → lessons-learned.md#L30
- [经验] **复制粘贴是 i18n 错误的常见来源**：将中文值直接粘贴进英文字典，或反之，属于低级但高频的疏 — `i18n` → lessons-learned.md#L33
- [经验] **已删除的 JS 文件若不从 index.html 移除引用，会导致 404**：功能清理和引用清 — `build-env` → lessons-learned.md#L36
- [经验] **删除生产代码的 fallback 函数前，必须先评估测试环境是否提供了该依赖**：架构统一重构必 — `testing / architecture` → lessons-learned.md#L38
- [经验] **`localStorage` mock 必须支持 `setItem` 持久化**：测试中 `gl — `testing` → lessons-learned.md#L39
- [经验] **配置类设置项用「弹窗选择」优于「循环切换」**：循环切换隐藏了全部选项，用户不知道有哪些风格；弹 — `ux` → lessons-learned.md#L41
- [经验] **功能入口迁移需要同步更新「正向路径」和「反向路径」**：不仅要添加新入口，还要移除旧入口，否则用 — `ux / architecture` → lessons-learned.md#L44
- [经验] **测试中断言的具体文本值是重构的敏感点**：重构前应先审计测试中的文本断言，预估需要调整的范围 — `testing` → lessons-learned.md#L46
- [经验] **数据文件中的引号嵌套是极易被忽视的语法陷阱**：在真实浏览器中会抛出 `SyntaxError` — `data / build-env` → lessons-learned.md#L47
- [经验] **playwright 是定位浏览器特有 bug 的有效手段**：通过 `page.add_ini — `testing / debugging` → lessons-learned.md#L49
- [经验] **向后兼容接口设计能减少重构的连锁反应**：旧接口继续工作，内部映射新参数，所有旧测试和外部调用点 — `api-design` → lessons-learned.md#L51
- [经验] `AGENTS.md` 定义触发词和行为约束，`status.md` 记录动态进度，分工明确，新会话 — `ai-workflow` → lessons-learned.md#L54
- [经验] 每批次开发完成后同步更新进度文档，避免新会话迷路 — `ai-workflow` → lessons-learned.md#L55
- [经验] **涉及 7+ 文件读改测的架构重构，应新开会话执行**：继续塞进系统性重构容易触发窗口压缩，导致信 — `ai-workflow` → lessons-learned.md#L60
- [经验] CPU% 精确计算只需 `GetProcessTimes` + wall clock elapsed — `api-design` → lessons-learned.md#L65
- [经验] `tokio::sync::mpsc::Sender::try_send()` 适合非阻塞的进度回调 — `api-design` → lessons-learned.md#L71
- [经验] `useEffect` 依赖 `state.xxx.size === 0` 作为触发条件时，容易形成 — `state-management` → lessons-learned.md#L73
- [经验] `useRef` 作为"只执行一次"的标志，比依赖数组更可靠，尤其涉及批量初始化逻辑时 — `state-management` → lessons-learned.md#L74
- [经验] **测试驱动暴露 Bug**：ResultsPage 的默认勾选死循环是在写单元测试时发现的，手工测 — `testing` → lessons-learned.md#L75
- [经验] **结论**：前端状态管理类的 bug，单元测试是最有效的发现手段，远超手工测试 — `testing` → lessons-learned.md#L76
- [经验] `prompt-next-session.md` 的问题：每次都要重写环境初始化、模块速查表等**不 — `ai-workflow` → lessons-learned.md#L77
- [经验] **改进**：`status.md`（活文档，只记录变化）+ `AGENTS.md`（固定规则） — `ai-workflow` → lessons-learned.md#L78
- [经验] **收益**：新会话读 2 份文件即可开工，维护成本降低 80% — `ai-workflow` → lessons-learned.md#L79
- [经验] **工具硬性限制不要绕圈分析可行性**。Kimi CLI 多窗口无 IPC、无共享内存、无实时同步— — `ai-workflow` → lessons-learned.md#L81
- [经验] **从 SOP 模板采纳更新时，必须逐字核对关键字段，不要凭记忆改写**。触发词「存档」错误抄写为「 — `ai-workflow` → lessons-learned.md#L82
- [经验] **定位代码的最快方法**：清空 `lib.rs` 只保留一个空测试，逐步 `pub mod` 添加 — `debugging` → lessons-learned.md#L87
- [经验] **`#[cfg(not(test))]` 隔离问题代码**是零副作用的修复手法：release 构 — `testing / cross-platform` → lessons-learned.md#L89
- [经验] CSS `@keyframes dropdownIn` 实现淡入+位移动画 — `ux` → lessons-learned.md#L91
- [经验] 年月日联动限制（如今年只显示到当前月） — `ux` → lessons-learned.md#L92
- [经验] 正确做法：后端提供**轻量摘要接口**（只返回 id + category + suggested_ — `architecture / data` → lessons-learned.md#L97
- [经验] 用户实际浏览仍按分页，但"全选全部"走轻量接口，两者解耦 — `pagination / architecture` → lessons-learned.md#L98
- [经验] **事故经过**：ResultsPage 默认自动勾选所有扫描结果 → 用户点击"全选全部"（以为是 — `pagination / state-management / security` → lessons-learned.md#L99
- [经验] **根因链**：默认勾选 × deselectAll 只清当前页 × ConfirmPage 遍历  — `pagination / state-management` → lessons-learned.md#L100
- [经验] **教训**：涉及删除的安全工具，**默认安全 > 默认便利**。所有选择必须用户显式操作，任何"帮 — `security / ux` → lessons-learned.md#L101
- [经验] **原实现**：`deselectAll` 只遍历 `searchedItems`（当前页数据），从 — `pagination / state-management` → lessons-learned.md#L102
- [经验] **修复**：`deselectAll` 清空 `selectedIds` 为 `new Set() — `pagination / state-management` → lessons-learned.md#L103
- [经验] **教训**：跨分页操作时，"取消"必须与"全选"的对称——全选影响多大范围，取消就必须影响多大范围 — `pagination / state-management` → lessons-learned.md#L104
- [经验] **原实现**：ConfirmPage 遍历 `state.scanResults`，过滤出选中的项 — `pagination / state-management` → lessons-learned.md#L105
- [经验] **修复**：遍历 `state.decisions`，每项在 `scanResults` 中查找详 — `pagination / state-management` → lessons-learned.md#L106
- [经验] **教训**：在分页/懒加载架构中，**用户操作集合（decisions）是主数据源，展示数据（sc — `pagination / architecture` → lessons-learned.md#L107
- [经验] 在 Kimi Code CLI 上安装 Superpowers 需分 A/B 方案：A 方案替换 C — `未分类` → lessons-learned.md#L160
- [经验] 评估 skill 是否适合当前项目时，不应只看功能描述，而应对比项目形态（纯文档/工具型项目不需要  — `未分类` → lessons-learned.md#L161
- [经验] `gh api --paginate --slurp` 返回嵌套数组 `[page1, page2, — `api-design` → lessons-learned.md#L208
- [决策] ADR-001：前端技术栈选型 — `架构决策` → ADR.md#L8
- [决策] ADR-002：测试框架选型 — `架构决策` → ADR.md#L22
- [决策] ADR-003：AI 开发方式与批次划分 — `架构决策` → ADR.md#L36
- [决策] ADR-004：棋盘渲染与棋子方案 — `架构决策` → ADR.md#L50
- [决策] ADR-005：数据持久化方案 — `架构决策` → ADR.md#L64
- [决策] ADR-006：通用对局配置层设计 — `架构决策` → ADR.md#L78
- [决策] ADR-007：难度选择从离散按钮改为连续滑块 — `架构决策` → ADR.md#L92
- [决策] ADR-008：棋盘风格设置交互方案 — `架构决策` → ADR.md#L106
- [决策] ADR-009：盲棋复盘入口位置 — `架构决策` → ADR.md#L120
- [决策] ADR-004：为什么 Scanner 进度用 `mpsc::channel` 而非 `tokio: — `架构决策` → ADR.md#L188
- [决策] ADR-005：为什么加密文件回调用同步 `Fn` 而非 `async`？ — `架构决策` → ADR.md#L202
- [决策] ADR-006：为什么用 `status.md` + `session-log.md` 替代 `pr — `架构决策` → ADR.md#L216
- [决策] ADR-008：默认深色主题而非跟随系统 — `架构决策` → ADR.md#L240
- [决策] ADR-009：全选全部功能的技术方案 — `架构决策` → ADR.md#L252
- [决策] ADR-010：路径交互设计 — 文本可点击 vs 独立按钮 — `架构决策` → ADR.md#L264
- [决策] ADR-011：删除策略从 DoD 安全擦除改为普通删除 — `架构决策` → ADR.md#L276
- [决策] ADR-012：扫描范围从 Desktop/Downloads 扩展为全盘扫描 — `架构决策` → ADR.md#L288
- [决策] ADR-013：移除 ResultsPage 默认自动勾选 — `架构决策` → ADR.md#L300
- [决策] ADR-014：同步脚本优先使用仓库 default_branch — `架构决策` → ADR.md#L314
- [决策] ADR-015：syncFrom 配置实现聚合/分发双模式 — `架构决策` → ADR.md#L326
- [决策] ADR-016：母库 AGENTS 与其他项目 AGENTS 物理分离 — `架构决策` → ADR.md#L338
- [决策] ADR-009：Troubleshooting 索引采用独立文件 + 行号链接 — `架构决策` → ADR.md#L392
- [决策] ADR-017：假删除模式通过环境变量 `FRENCH_EXIT_DRY_RUN` 控制 [来源:f — `架构决策` → ADR.md#L442
- [决策] ADR-017：扫描进度条采用后端全局加权进度计算 — `架构决策` → ADR.md#L458
- [决策] ADR-018：个人目录全量扫描 + 文件类型分类 — `架构决策` → ADR.md#L473
- [决策] ADR-002：渠道范围限定（仅淘系生意参谋） — `架构决策` → ADR.md#L524
- [决策] ADR-003：Cookie 刷新策略（Digest 自动刷新，不问用户） — `架构决策` → ADR.md#L538
- [决策] ADR-004：日期时间格式（T00:00:00+08:00，禁用 23:59:59） — `架构决策` → ADR.md#L552
- [决策] ADR-005：报告形态（Markdown 四段式，单店/多店统一） — `架构决策` → ADR.md#L566
- [决策] ADR-017：聚焦 Excel 驱动流，API 驱动流暂不投入 [来源:qianniu_busin — `架构决策` → ADR.md#L584
- [决策] ADR-020：状态文档机制重构（待办清理 + 技术债务表格化） [母库 @2026-05-30] — `架构决策` → ADR.md#L612
- [决策] ADR-022：保持 `qianniu_business_analytics` 与 `ecommer — `架构决策` → ADR.md#L626


---

## 按状态分组（troubleshooting）

### pending（2 条）

- AI 重复实现已有组件（棋盘/网格类 UI） → troubleshooting.md#L8
- [错误关键词] → troubleshooting.md#L1395

### resolved（18 条）

- Node.js 测试运行时 chess.js 未定义 → troubleshooting.md#L41
- CLI subAgent 并行超时 → troubleshooting.md#L50
- 设置面板一闪而过 → troubleshooting.md#L59
- JS 数据文件嵌套单引号导致 `Unexpected identifier` → troubleshooting.md#L92
- 设置面板点击无反应（panel toggle 测试失败） → troubleshooting.md#L102
- mock DOM 中 `querySelector` / `querySelectorAll` 缺失 → troubleshooting.md#L112
- `cargo test --lib` 报错 `0xc0000139`（UCRT DLL 缺失） → troubleshooting.md#L144
- GitHub push 报错 `Permission denied (publickey)` → troubleshooting.md#L265
- `gh auth login` 超时：`read tcp ... operation timed out` → troubleshooting.md#L274
- HuggingFace 模型下载连接超时 `curl: (28) Could not connect to s... → troubleshooting.md#L283
- Node.js 报 SyntaxError: Unexpected identifier（i18n 中文字符串... → troubleshooting.md#L665
- Cookie 过期 / 401 认证失败 → troubleshooting.md#L1029
- Digest 刷新失败 → troubleshooting.md#L1038
- auth/jycm.json 缺失字段 → troubleshooting.md#L1047
- 日期区间多返回一天 → troubleshooting.md#L1060
- Hermes Agent Git 合并冲突导致 SyntaxError → troubleshooting.md#L1133
- Node.js 环境污染：Hermes Node.js 泄漏到用户 PATH → troubleshooting.md#L1145
- CodeBuddy 安装后 package.json 丢失导致命令不可用 → troubleshooting.md#L1163

### wont_fix（6 条）

- 旧代码与新模块冲突 → troubleshooting.md#L72
- 引擎候选走法未集成 → troubleshooting.md#L81
- getAllShopList 返回空数组 → troubleshooting.md#L1069
- createAndDownload 返回失败 → troubleshooting.md#L1078
- openpyxl 未安装 → troubleshooting.md#L1091
- 钉钉推送失败 → troubleshooting.md#L1100

### known_limitation（5 条）

- Stockfish 加载超时 / 引擎不启动 → troubleshooting.md#L19
- GitHub Pages 国内打不开 → troubleshooting.md#L28
- PowerShell 添加防火墙规则权限不足 `Access is denied` → troubleshooting.md#L292
- Windows Git Bash LF/CRLF 警告 → troubleshooting.md#L1113
- distribute.py 子进程 GBK 编码错误 → troubleshooting.md#L1408

### —（15 条）

- `cargo check --lib` 报错：`GetDiskFreeSpaceExW` 未定义 → troubleshooting.md#L124
- `cargo check --lib` 报错：`FILETIME` 未定义 → troubleshooting.md#L132
- 运行 `french-exit.exe` 报错：`Could not find the WebView2 Ru... → troubleshooting.md#L156
- 运行 `french-exit.exe` 报错：`找不到 WebView2Loader.dll` → troubleshooting.md#L164
- `cargo tauri build` 失败：`另一个程序正在使用此文件` (os error 32) → troubleshooting.md#L172
- vitest 报错：`Failed to resolve import "@tauri-apps/api/fs... → troubleshooting.md#L182
- vitest 报错：`act is not a function` → troubleshooting.md#L191
- vitest 报错：React 警告 `Cannot update a component while ren... → troubleshooting.md#L199
- checkbox 点击后状态不变化 → troubleshooting.md#L208
- 中文路径下编译失败 → troubleshooting.md#L221
- cargo tauri dev 在后台任务中崩溃 → troubleshooting.md#L232
- PowerShell 执行中文脚本报 "UnexpectedToken" → troubleshooting.md#L253
- sed 批量修改误改结构体定义 → troubleshooting.md#L675
- French Exit 进程锁定 exe 导致复制失败 → troubleshooting.md#L684
- 新增条目模板 → troubleshooting.md#L1391

---

## 按类型分组

### 问题（47 条）

- AI 重复实现已有组件（棋盘/网格类 UI） → troubleshooting.md#L8
- Stockfish 加载超时 / 引擎不启动 → troubleshooting.md#L19
- GitHub Pages 国内打不开 → troubleshooting.md#L28
- Node.js 测试运行时 chess.js 未定义 → troubleshooting.md#L41
- CLI subAgent 并行超时 → troubleshooting.md#L50
- 设置面板一闪而过 → troubleshooting.md#L59
- 旧代码与新模块冲突 → troubleshooting.md#L72
- 引擎候选走法未集成 → troubleshooting.md#L81
- JS 数据文件嵌套单引号导致 `Unexpected identifier` → troubleshooting.md#L92
- 设置面板点击无反应（panel toggle 测试失败） → troubleshooting.md#L102
- mock DOM 中 `querySelector` / `querySelectorAll` 缺失 → troubleshooting.md#L112
- `cargo check --lib` 报错：`GetDiskFreeSpaceExW` 未定义 → troubleshooting.md#L124
- `cargo check --lib` 报错：`FILETIME` 未定义 → troubleshooting.md#L132
- `cargo test --lib` 报错 `0xc0000139`（UCRT DLL 缺失） → troubleshooting.md#L144
- 运行 `french-exit.exe` 报错：`Could not find the WebView2 Ru... → troubleshooting.md#L156
- 运行 `french-exit.exe` 报错：`找不到 WebView2Loader.dll` → troubleshooting.md#L164
- `cargo tauri build` 失败：`另一个程序正在使用此文件` (os error 32) → troubleshooting.md#L172
- vitest 报错：`Failed to resolve import "@tauri-apps/api/fs... → troubleshooting.md#L182
- vitest 报错：`act is not a function` → troubleshooting.md#L191
- vitest 报错：React 警告 `Cannot update a component while ren... → troubleshooting.md#L199
- ... 还有 27 条

### 经验（106 条）

- 纯 HTML+CSS+JS 项目无需 npm，双击 `index.html` 即可预览，但涉及 Web Wor... → lessons-learned.md#L14
- 手写 IIFE 模块时，用 `window.ModuleName = Module` 暴露 API，内部私有变... → lessons-learned.md#L15
- 浏览器集成测试用 TestRunner（自定义极简框架），保持与 Node 测试同一套断言 API，降低切换成... → lessons-learned.md#L16
- Canvas 图表渲染在浏览器中测试，Node 环境用 Mock 2D context 跳过绘制验证，各测其责 → lessons-learned.md#L17
- PGN 解析器对空/无效输入返回 `[]`（空数组）而非 `null`，调用方需区分"无走法"和"解析失败" → lessons-learned.md#L18
- `cloneNode(true)` 替换含 SVG 的按钮会导致 SVG 渲染异常（显示不完整）；移除事件监听... → lessons-learned.md#L19
- 匿名事件监听器无法被后续代码移除；需要动态解除绑定的监听器必须用命名函数（暴露到 `window` 或模块内部... → lessons-learned.md#L20
- 屏幕切换导航不能只隐藏上一个屏幕，必须遍历 `.screen` 全部隐藏后再显示目标，否则多层屏幕重叠 → lessons-learned.md#L21
- SVG path 中密集参数（如 `a2 2 0 0 1-2.83 0`）在某些浏览器中可能解析异常，命令与参... → lessons-learned.md#L22
- `document` 级事件监听器若引用了某个 DOM 元素，该元素被替换后监听器仍会按旧引用判断，导致逻辑错... → lessons-learned.md#L23
- 项目文档结构会随时间进化，"存档"或"恢复"操作前应先 `ls`/`glob` 确认当前文件系统现状，避免按历... → lessons-learned.md#L24
- **UI 布局/样式不要猜测用户意图**：候选走法开关经历了 5 次位置/样式反复，每次修改后用户都不满意；应... → lessons-learned.md#L25
- **引擎候选走法的调用时机决定产品逻辑正确性**：用户走完后立即 `goMultiPv` 分析的是对手局面；若... → lessons-learned.md#L26
- **引擎返回 UCI（e2e4），用户界面必须用 SAN（e4）**：`goMultiPv` 回调中的 `mo... → lessons-learned.md#L27
- **静态 HTML 结构与动态渲染模块的 DOM 冲突**：`index.html` 中预置了完整棋盘结构，而... → lessons-learned.md#L28
- **删除功能必须同步删除对应测试**：移除 `showHints` / `multiPvSetting` 后，... → lessons-learned.md#L29
- **焦点管理是盲棋产品的核心体验**：进入对局自动 `input.focus()`、引擎走完后恢复焦点、全局 ... → lessons-learned.md#L30
- **i18n 分散架构必然导致翻译遗漏**：当项目同时存在"全局字典 + 模块私有字典 + 硬编码"三种翻译方... → lessons-learned.md#L31
- **JS 中的硬编码人类可读字符串是翻译遗漏的重灾区**：HTML 中的 `data-i18n` 至少能被肉眼... → lessons-learned.md#L32
- **复制粘贴是 i18n 错误的常见来源**：将中文值直接粘贴进英文字典，或反之，属于低级但高频的疏忽 → lessons-learned.md#L33
- ... 还有 86 条

### 决策（41 条）

- ADR-001：前端技术栈选型 → ADR.md#L8
- ADR-002：测试框架选型 → ADR.md#L22
- ADR-003：AI 开发方式与批次划分 → ADR.md#L36
- ADR-004：棋盘渲染与棋子方案 → ADR.md#L50
- ADR-005：数据持久化方案 → ADR.md#L64
- ADR-006：通用对局配置层设计 → ADR.md#L78
- ADR-007：难度选择从离散按钮改为连续滑块 → ADR.md#L92
- ADR-008：棋盘风格设置交互方案 → ADR.md#L106
- ADR-009：盲棋复盘入口位置 → ADR.md#L120
- ADR-017：GitHub 认证从 SSH 切换到 GitHub CLI + HTTPS → ADR.md#L132
- ADR-001：为什么用 Tauri（Rust + WebView2）而非 Electron？ → ADR.md#L147
- ADR-002：为什么前端用 React（而非 Vue/Svelte）？ → ADR.md#L160
- ADR-003：为什么 CPU% 用 `GetProcessTimes` 而非 `sysinfo` crate... → ADR.md#L174
- ADR-004：为什么 Scanner 进度用 `mpsc::channel` 而非 `tokio::sync... → ADR.md#L188
- ADR-005：为什么加密文件回调用同步 `Fn` 而非 `async`？ → ADR.md#L202
- ADR-006：为什么用 `status.md` + `session-log.md` 替代 `prompt-... → ADR.md#L216
- ADR-007：WebView2 分发策略——放弃 NSIS bootstrapper，改用携带 DLL → ADR.md#L228
- ADR-008：默认深色主题而非跟随系统 → ADR.md#L240
- ADR-009：全选全部功能的技术方案 → ADR.md#L252
- ADR-010：路径交互设计 — 文本可点击 vs 独立按钮 → ADR.md#L264
- ... 还有 21 条
