<!-- 母库: E:\work-space\vs-code\vibe-coding-project-sop -->
# 淘系店铺经营数据分析 — Agent 启动指令

> 本文件供 AI 开发助手读取。接手本项目时，**必须先读完下面列出的上下文文件**，再开始任何代码操作。
>
> 本项目为 **自包含技能包**，自包含认证、取数、分析、报告生成、钉钉推送全流程。
<!-- @sync:id=skeleton-protocol -->
## 0. 项目基础设施

### 基础设施层

| 文件 | 职责 |
|------|------|
| `AGENTS.md` | 项目硬规则 + 模块速查 |
| `docs/workflows/agent-coding-workflow.md` | 五阶段 workflow 参考 |
| `status.md` | 当前进度、待办清单 |
| `session-log.md` | 会话历史记录 |
| `ADR.md` | 关键决策记录 |
| `troubleshooting.md` | 问题索引 |
| `lessons-learned.md` | 跨项目经验沉淀 |
| `.gitattributes` | 统一换行符(LF) + 标记二进制文件 |
| `config/github-sync.json` | 跨项目知识同步配置 |

### 技能（Skills）

项目自带一组 AI 助手技能（路径：`.claude/skills/`），覆盖代码审查、调试、归档等场景。技能文件为 markdown 指令，由 AI 助手按需加载。

**激活方式**：运行分发脚本同步，或在 `.claude/skills/` 下为需要的技能创建符号链接：

```bash
ln -s {技能源路径} .claude/skills/{技能名}
```

**当前可用技能**（来源：`starter/.agents/skills/`，`init-skeleton.py` 或 `distribute.py` 自动安装）：

> ⚙️ 同步门禁：母库新增通用技能后，`awb health` 的「Starter 技能同步」检查和 `distribute.py` 的 sync-check 会报警提示补充到 `starter/.agents/skills/`。

| 技能 | 说明 |
|------|------|
| `checkpoint` | 轻量 git 快照：add → commit → push |
| `design-an-interface` | 设计新接口或 API 的流程、类型定义和边界 |
| `diagnose` | 结构化诊断硬 bug 和性能退化 |
| `edit-article` | 编辑和润色文章 |
| `git-guardrails-claude-code` | Git 安全操作护栏 |
| `grill-me` | 对设计方案持续追问直到达成共识 |
| `grill-with-docs` | 参考文档进行深入追问 |
| `handoff` | 任务交接，生成接力上下文 |
| `improve-codebase-architecture` | 代码架构改进建议 |
| `migrate-to-shoehorn` | 渐进式迁移到新架构模式 |
| `prototype` | 快速原型开发 |
| `python-code-quality` | Python 静态分析（ruff + mypy） |
| `qa` | 质量保证检查 |
| `request-refactor-plan` | 请求重构方案设计 |
| `review` | 审查变更（标准轴 + 规格轴） |
| `scaffold-exercises` | 脚手架练习生成 |
| `setup-pre-commit` | 配置 pre-commit 钩子 |
| `tdd` | 测试驱动开发流程 |
| `teach` | 教授用户新的技能或概念 |
| `to-issues` | 将内容转化为 Issue |
| `to-prd` | 将内容转化为 PRD |
| `triage` | 问题分类和优先级评估 |
| `ubiquitous-language` | DDD 通用语言术语表提取 |
| `write-a-skill` | 创建新的 AI skill |
| `writing-beats` | 写作节奏控制 |
| `writing-fragments` | 写作片段管理 |
| `writing-shape` | 写作结构设计 |
| `zoom-out` | 提供更广阔的上下文或高层视角 |

### 阶段产出层（按 SOP 五阶段逐步创建）

| 阶段 | 产出文件 |
|------|---------|
| 阶段一 | `docs/proposal.md` |
| 阶段二 | `docs/design.md`、`docs/brief.md`、`docs/database.md`（条件性，T-01②/③）、`docs/frontend.md`（条件性，T-05②） |
| 阶段三 | `docs/tasks/task-{module}.md` |
| 阶段四 | `prompt.md` |
| 阶段五 | `src/`、`tests/`、各模块源码 |

<!-- /@sync -->

---

<!-- @sync:id=archive -->
## 4.1 存档指令（「存档」）

> 完整流程见 `docs/workflows/archive.md`（7 步线性：快照→回顾→确认→选认知→更新文档→定稿→提交）。
> 待办写入规则见 `docs/workflows/todo-rules.md`。

<!-- /@sync -->---

<!-- @sync:id=core-constraints -->
## 3. 核心约束（硬规则，不可违反）

| 规则 ID | 规则内容 | 违反后果 |
|---------|---------|---------|
| **RULE-01** | **必须先建立基础设施层，再按阶段创建产出层** | 过程无记录、状态不可追踪 |
| **RULE-04** | **禁止向工作区以外的系统关键目录写入文件（如 C:\Windows、/System、/etc 等）；用户明确授权时可例外** | 系统文件被污染 |
| **ARCHIVE-01** | **存档时执行标准流程：先输出确认清单等待确认 → 确认后执行存档 → 删除已完成待办项，追加更新记录。历史完成记录由「更新记录」承担，待办清单只保留未完成项。** | 误触发导致非预期提交；文档与 Git 状态不一致；待办清单膨胀、重点模糊 |
| **RULE-05** | **跨项目知识同步时先备份母库文件，合并后标注来源（按规则去重）；`experience-index.md` 由脚本自动生成，禁止手动编辑索引文件。** | 母库内容来源不清、重复堆积；索引与源文件不同步 |
| **RULE-09** | **技术债务解决后，必须从 `status.md` 债务表删除，追加到「已解决债务」，并记录到 `lessons-learned.md`（标注 TAG:debt）** | 债务与经验脱节、重复犯错、无法追溯解决过程 |
| **RULE-11** | **阶段口令是启动器而非执行器：口令只负责检查前置条件、说明目标、确认启动，不通过则禁止启动该阶段。具体执行细节严格引用 `docs/workflows/agent-coding-workflow.md` 对应章节，禁止在口令逻辑中重写执行规范。** | 跳步导致产出无上下文；规则在两处维护导致版本分歧 |
| **RULE-12** | **写入 `troubleshooting.md` / `lessons-learned.md` / `ADR.md` 时，所有 IP 地址、本地文件路径、邮箱等敏感信息必须使用占位符替代；仅在问题重现必须精确信息时才保留，同时写入备注说明** | 经验文档聚合后泄露个人/基础设施信息 |
| **RULE-13** | **禁止在最终输出中出现占位符（`[...]`、`<...>`、`TBD`、`TODO`、`待补充`）；信息不足时使用通用表述替代，宁可放宽粒度不可留空洞** | 下游 agent 无法消费输出、内容不可用 |
| **RULE-14** | **所有文件 I/O 和 `subprocess.run()` 必须显式传入 `encoding` 参数** | Windows GBK 环境下不指定会导致 UnicodeDecodeError |
| **RULE-15** | **`git merge` 因文件系统不兼容失败时，禁止使用 `-s ours` / `-X ours`。必须改用 `git merge-tree --write-tree` 在对象空间完成合并，仅排除无法在当前文件系统创建的文件（`scripts/pre-merge-check.py` 预检 + `scripts/check-merge-integrity.py` 后检）** | 丢弃远端变更导致跨平台同步数据静默丢失 |
| **RULE-17** | **职责边界变动前必须输出 scope 声明表并等候用户确认。** 触发条件：新增/删除触发词、`RULE`、分发条目或改动 `CLAUDE.md` 入口结构。不触发：`@sync:id` 同步、workflow 内容更新、单文件修 bug。 | 单知多改、遗漏同步、下游无声不一致 |
| **RULE-18** | **方案分析、风险评估、决策确认时，必须运用 `adversarial-think` 方法论进行深度审查，输出固定格式报告。** 适用场景：方案定稿 / 技术选型 / 存档前变更审查 / 清理发现处置 / 新增模块前复用检查（搜索现有代码，禁止重复造轮子）。报告输出后禁止自行修复，必须等待用户审批。 | 分析泛化停留在表面；代码膨胀、重复造轮子；Agent 绕过用户直接修改代码 |

<!-- /@sync -->---
<!-- @sync:id=recovery -->
## 4.2 恢复指令（「恢复」）

> 完整流程见 `docs/workflows/resume.md`（6 步线性：分支确认 → 工作区检查 → Git 同步 → 读取状态 → 记忆同步 → 汇报）。

<!-- /@sync -->
---

## 4.2 恢复指令（「恢复」）

**触发词**：`恢复`（去除标点后精确等于这两个字）

**防误触**：
- 消息精确匹配「恢复」→ 执行恢复流程
- 消息包含「恢复」但还有其他内容 → 视为正常对话，不触发

**核心原则**：
> **恢复摘要以 `status.md` 为主，`session-log.md` 为辅。**
> **不要复述上轮历史。**

**标准动作序列**：
1. **Git 同步（三层安全闸）**：
   a. `git fetch origin`
   b. `python scripts/pre-merge-check.py origin/main` — 预检远端文件名兼容性
   c. 如通过（exit 0）→ `git pull`；如不通过（exit 1）→ 按 merge-tree 方案执行合并
   d. 检查 pull 是否有变化（对比 `git rev-parse HEAD@{1}` 与 HEAD）；无变化则跳过下一步
   e. `python scripts/check-merge-integrity.py` — 后检是否有意外丢失文件
   f. 如丢失 → 按脚本输出恢复；如通过 → 继续
2. 读取 `status.md`（主数据源）：阶段、进度、待办、阻塞项
3. 读取 `session-log.md` 最后一条（辅数据源）：只取「遗留问题/下轮开始点」
4. **分析 + 汇报**：用户有报错 → 搜索 troubleshooting；检查 status 字段有效性；综合判断后输出恢复摘要（当前状态 + 建议下一步）
5. 等待用户下一步指令

<!-- /@sync -->
---

---

<!-- @sync:id=project-review -->
## 4.6 项目审查（「项目审查」）

> 完整流程见 `docs/workflows/project-review.md`（六维度架构审查：目录树 / 模块清单 / 依赖图 / 循环依赖 / 重复实现 / 过度耦合）。
<!-- /@sync -->---

<!-- @sync:id=todo-rules -->
## 4.5 待办写入规则

> 完整规则见 `docs/workflows/todo-rules.md`（写入时机、格式、判断表）。
<!-- /@sync -->---

<!-- @sync:id=cleanup -->
## 4.4 清理指令（「清理」）

> 完整流程见 `docs/workflows/cleanup.md`（作用范围：知识文件 + AGENTS.md 结构）。
<!-- /@sync -->---

<!-- @sync:id=lightweight-dev -->
## 4.7 轻量立项指令（「立项」）

> 完整流程见 `docs/workflows/lightweight-dev.md`（讨论 → 方案 → 执行 → 归档，不固定会话边界）。
<!-- /@sync -->

---

## 5. 环境备忘索引

> 编译命令、PATH、已知限制见 `status.md` → 环境备忘

---

## 5.1 母库经验指令（「拉取母库」）

> 本指令用于从跨项目知识母库 `agent-coding-skeleton` 获取已沉淀的经验。

**触发词**：`拉取母库`、`拉取经验`、`更新经验`（去除标点后精确匹配任一）

**防误触**：
- 消息精确匹配上述任一触发词 → 执行母库经验同步流程
- 消息包含触发词但还有其他内容 → 视为正常对话，不触发

**前置条件**：
- 项目根目录存在 `scripts/pull.py`（或 `scripts/sync-knowledge.py`）
- 项目根目录存在 `config/github-sync.json` 且 `syncFrom` 已填写

**标准动作序列**：
1. 检查 `scripts/pull.py` 是否存在
   - 如存在 → 运行 `python scripts/pull.py`
   - 如不存在 → 从母库下载，然后运行
2. 读取脚本输出，汇报同步结果：
   - 母库仓库名
   - 拉取到的文件数
   - 新增条目数 / 全部已存在
3. 如有新增内容，提示用户查看 `ADR.md`、`lessons-learned.md`、`troubleshooting.md`

**Git 错误处理**：无 `.git` 目录 → 跳过 Git；无变更 → 跳过 commit；push 失败 → 报错暂停。

**反哺母库**：
如本项目在开发过程中产生了新的可复用经验，可手动提交到母库仓库，供所有项目共享。

> 实现细节见 `scripts/cognitive-extract.py`，AGENTS.md 不承载具体后端逻辑。

---
<!-- @sync:id=phase-commands -->
## 6. 阶段指令

> 启动机制和阶段定义详见 `docs/workflows/agent-coding-workflow.md` §阶段启动机制（通用启动流程、摘要模板、阶段定义速查）。口令是启动器而非执行器（RULE-11）。

### 6.1-6.5 阶段定义

| 触发词 | 阶段 | 前置条件 | 主要产出 | Spec |
|--------|------|---------|---------|------|
| `阶段一` | 需求讨论 | 无 | `docs/proposal.md` + T-01~T-05 | `docs/workflows/agent-coding-workflow.md §阶段一` |
| `阶段二` | 设计文档搭建 | proposal.md 存在 + 阶段一 ✅ | `docs/design.md`, `docs/brief.md` | `docs/workflows/agent-coding-workflow.md §阶段二` |
| `阶段三` | 划分任务 | design.md + brief.md + 阶段二 ✅ | `docs/tasks/task-{module}.md`, `task-progress.md` | `docs/workflows/agent-coding-workflow.md §阶段三` |
| `阶段四` | 生成 Prompt | task-progress.md 存在 | `prompt.md` | `docs/workflows/agent-coding-workflow.md §阶段四` |
| `阶段五` | 执行开发 | prompt.md 存在 | 源码 + 测试 + 集成 | `docs/workflows/agent-coding-workflow.md §阶段五` |

> 各阶段的完整目标、关键动作、完成标志见 `docs/workflows/agent-coding-workflow.md` 对应章节。

### 6.6 当前阶段（「当前阶段」）

> 完整执行流程见 `docs/workflows/current-phase.md`。

<!-- /@sync -->

---

<!-- @sync:id=checkpoint -->
