# 淘系店铺经营数据分析 — 技术设计文档

> 架构总览、模块划分、接口契约、数据流。
> 描述当前 **Excel 驱动模式**（v5.0.0+）的实际架构。历史 API 驱动架构已归档删除。

---

## 1. 架构总览

本项目为 **自包含技能包**，采用**平铺式流水线架构**：

```
┌──────────────────────────────────────────────────────────────┐
│                      入口层（Entry）                          │
│  ┌──────────────┐  ┌────────────────────┐                   │
│  │ 对话触发     │  │ CLI 触发           │                   │
│  │ (SKILL.md)   │  │ (jycm_auto_       │                   │
│  │              │  │  report.py)        │                   │
│  └──────┬───────┘  └────────┬───────────┘                   │
└─────────┼──────────────────┼────────────────────────────────┘
          │                  │
          ▼                  ▼
┌──────────────────────────────────────────────────────────────┐
│                    业务层（Business Logic）                   │
│                                                              │
│  ┌────────────────────┐  ┌────────────────────┐             │
│  │ M01 报告分析       │  │ M02 消息推送       │             │
│  │ analyze_excel_     │  │ dingtalk_send_     │             │
│  │ report.py          │  │ markdown.py        │             │
│  │ (pandas + openpyxl)│  │ feishu_send_       │             │
│  │                    │  │ markdown.py        │             │
│  └────────┬───────────┘  └────────┬───────────┘             │
│           │                       │                           │
└───────────┼───────────────────────┼──────────────────────────┘
            │                       │
            ▼                       ▼
┌──────────────────────────────────────────────────────────────┐
│                     基础设施层                                 │
│   data/  │  reports/  │  scripts/constants.py  │  Webhook   │
└──────────────────────────────────────────────────────────────┘
```

### 模块清单

| 模块 | 职责 | 入口/核心文件 |
|------|------|-------------|
| M01 报告分析 | 读取 Excel 数据 → 生成四段式 Markdown 报告 | `scripts/analyze_excel_report.py` |
| M02 消息推送 | 通过 Webhook 推送 Markdown 到钉钉/飞书 | `scripts/dingtalk_send_markdown.py`、`scripts/feishu_send_markdown.py` |
| M03 自动化编排 | CLI 入口，扫描 data/ 目录 → 调用 M01 → M02 | `scripts/jycm_auto_report.py` |
| M00 共享常量 | 时区、日期格式、指标关键词映射、推送长度限制 | `scripts/constants.py` |

### 设计原则

- **Excel 驱动**：用户从生意参谋导出 Excel → `data/` 目录 → 脚本读取分析，无需 API 权限
- **单店/多店透明**：同一套分析函数通过 `_shop_name` 内部标识列区分单店/多店模式
- **多渠道推送**：钉钉和飞书为独立实现的双渠道，互不依赖
- **技能包自包含**：所有逻辑在 `scripts/` 下，不依赖外部包（除 pandas、openpyxl、requests）

---

## 2. 模块划分

### 2.1 M01 报告分析（Report Analysis）

**职责**：读取生意参谋导出的 `.xlsx` 文件，通过列名模糊匹配识别核心指标，生成四段式 Markdown 报告。支持单店分析和多店合并分析。

**核心文件**：
- `scripts/analyze_excel_report.py`（599 行）— 核心分析逻辑
- `scripts/constants.py` — 指标关键词映射（`METRIC_KEYWORDS`）
- `data/` — 用户放置 Excel 的目录
- `reports/` — 生成的报告输出目录
- `report-analyze.md` — 报告规范文档

**对外接口**：

| 函数 | 输入 | 输出 | 说明 |
|------|------|------|------|
| `find_column(df, keywords)` | DataFrame + 关键词列表 | 匹配的列名 / None | 模糊列名匹配 |
| `find_columns(df)` | DataFrame | 所有指标列名的映射字典 | 遍历 `METRIC_KEYWORDS` 查找 |
| `detect_date_column(df)` | DataFrame | 日期列名 / None | 按关键词或 datetime 类型检测 |
| `analyze_excel(xlsx_path, shops)` | Excel 路径 + 店铺名列表 | Markdown 报告正文 | 核心流程，单店/多店通用 |
| `save_report(markdown, filename)` | 正文 + 文件名 | `reports/` 下的 `.md` 文件路径 | 持久化报告 |
| `main()` | CLI 参数 | 退出码 | 命令行入口 |

**指标识别**（通过 METRIC_KEYWORDS 映射）：

| 类目 | 指标 | 匹配关键词 |
|------|------|-----------|
| 流量 | 访客数、浏览量、搜索访客数 | "访客数"、"uv"、"pv" 等 |
| 交易 | 支付金额、支付买家数、支付转化率 | "gmv"、"成交金额"、"转化率" 等 |
| 转化 | 加购/收藏/分享人数、加购/收藏转化率 | "加购"、"收藏" 等 |
| 渠道 | 手淘搜索/首页/直播访客、淘内免费 | "手淘搜索"、"直播" 等 |
| 广告 | 直通车/钻展花费 | "直通车"、"钻展" |

**报告结构（四段式，单店/多店通用）**：

```markdown
# 店铺经营分析_20260401_20260407

## 一、整体指标
（表格：指标 | 数值）

## 二、日度趋势
（表格：日期 | 指标1 | 指标2 | ...）

## 三、TOP 排行
单店模式：商品/渠道 TOP 10
多店模式：店铺横向对比 + 排行（头部/尾部/Gap 最大店铺）

## 四、分析总结
（3~6 条数据洞察，含同比/环比变化）

## 五、原始数据
（列出分析所用的 Excel 文件路径）
```

---

### 2.2 M02 消息推送（Message Push）

**职责**：将 Markdown 报告通过 Webhook 推送到钉钉或飞书机器人。两个渠道为独立实现，用户可任选其一。

#### 钉钉推送

**核心文件**：`scripts/dingtalk_send_markdown.py`（102 行）

**入口函数**：

| 函数 | 输入 | 输出 |
|------|------|------|
| `send_dingtalk(title, markdown_text)` | 标题 + Markdown 正文 | `True` / `False` |

**约束**：
- 标题必须含「经营」，否则自动补前缀 `经营·`
- 正文超过 18000 字符自动截断
- 环境变量 `DINGTALK_WEBHOOK` 未配置时跳过推送
- 依赖：`urllib`（标准库，无需 requests）

#### 飞书推送

**核心文件**：`scripts/feishu_send_markdown.py`（99 行）

**入口函数**：

| 函数 | 输入 | 输出 |
|------|------|------|
| `send_feishu(title, markdown_text)` | 标题 + Markdown 正文 | `True` / `False` |

**约束**：
- 标题必须含「经营」，否则自动补前缀 `经营·`
- 正文超过 15000 字符自动截断
- 环境变量 `FEISHU_WEBHOOK` 未配置时跳过推送
- 依赖：`urllib`（标准库，无需 requests）

---

### 2.3 M03 自动化编排（Automation Orchestrator）

**职责**：提供 CLI 入口，扫描 `data/` 目录下的 Excel 文件，调用 M01 分析并生成报告，可选调用 M02 推送。

**核心文件**：`scripts/jycm_auto_report.py`（159 行）

**CLI 参数**：

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `--days` | int | 7 | 报告天数范围（用于报告标题） |
| `--start` | str | 自动计算 | 起始日期（YYYY-MM-DD） |
| `--end` | str | 自动计算 | 结束日期（YYYY-MM-DD） |
| `--shops` | str | — | 店铺名称，多个用逗号分隔 |
| `--dingtalk` | flag | — | 推送钉钉 |
| `--feishu` | flag | — | 推送飞书 |
| `--output` | str | 自动生成 | 自定义报告输出路径 |

**执行流程**：
1. 扫描 `data/` 目录获取 `.xlsx` 文件列表
2. 调用 `analyze_excel_report.generate_report()` 生成 Markdown
3. 保存报告到 `reports/`
4. 如指定 `--dingtalk`/`--feishu`，通过 `subprocess.run` 调用对应推送脚本

**默认日期**：上周自然周（上周一 → 上周日）

---

### 2.4 M00 共享常量（Shared Constants）

**核心文件**：`scripts/constants.py`（76 行）

| 常量 | 值 | 用途 |
|------|-----|------|
| `BJ_TZ` | `timezone(timedelta(hours=8))` | 北京时间时区 |
| `DATE_FMT` | `"%Y-%m-%d"` | 标准日期格式 |
| `DATE_FMT_COMPACT` | `"%Y%m%d"` | 紧凑日期格式 |
| `DATETIME_FMT` | `"%Y-%m-%d %H:%M"` | 日期时间格式 |
| `ISO8601_BJ_START` | `"T00:00:00+08:00"` | ISO8601 北京时间起始标记 |
| `MAX_TEXT_DINGTALK` | `18000` | 钉钉消息最大字符数 |
| `MAX_TEXT_FEISHU` | `15000` | 飞书消息最大字符数 |
| `METRIC_KEYWORDS` | `dict[str, list[str]]` | 27 个指标的关键词映射 |
| `REPORT_SECTIONS` | `list[str]` | 报告五段式标题 |

**时区规则（RULE-02��**：
- 日期时间统一使用北京时间（UTC+8）
- `ISO8601_BJ_START = "T00:00:00+08:00"` — 不可用 `T23:59:59.999+08:00`（后端会多返回一天数据）
- 不可用 `Z`（UTC）— `23:59:59Z` 会被解释为北京时间次日 07:59:59

---

## 3. 模块间调用关系

| 调用方 \ 被调用方 | M00 常量 | M01 报告分析 | M02 推送 |
|------------------|---------|-------------|---------|
| M01 报告分析 | 导入 METRIC_KEYWORDS、`fmt_*` | — | — |
| M02 推送 | 导入 MAX_TEXT_* | — | — |
| M03 自动化 | — | 调用 `analyze_excel()` + `save_report()` | 通过 `subprocess.run` 调用 |

> M02 钉钉和飞书为独立实现，互不调用。
> 对话触发（SKILL.md）直接在 Agent 层分析并推送，不经过 M03。

---

## 4. 数据流

### 4.1 核心数据实体生命周期

```
用户从生意参谋导出 Excel
    ↓
data/*.xlsx（手动放入）
    ↓
analyze_excel_report.py（pandas 读取）
    │  - 列名模糊匹配（METRIC_KEYWORDS）
    │  - 日期列自动检测
    │  - 数值格式化
    │  - 单店/多店分流
    ↓
Markdown 报告（四段式）
    ↓
reports/*.md（保存）
    ↓
dingtalk_send_markdown.py / feishu_send_markdown.py（可选推送）
```

### 4.2 数据持久化方案

| 数据 | 存储位置 | 格式 | 生命周期 |
|------|---------|------|---------|
| 原始数据（Excel） | `data/` | .xlsx | 手动管理，用户放入/删除 |
| 分析报告 | `reports/` | .md | 每次分析生成新文件，不覆盖 |
| 日志 | 标准输出 | 文本 | 进程结束即消失 |

---

## 5. 测试策略

| 测试层级 | 目标模块 | 方法 | 用例数 |
|---------|---------|------|--------|
| 单元测试 | M01 报告分析（指标查找、数值格式化） | pytest | 140 行 |
| 单元测试 | M02 推送（Webhook 消息构造） | pytest + mock | 55 行 |
| 单元测试 | M00 常量（格式验证） | pytest | 43 行 |
| 单元测试 | M03 自动化（文件扫描） | pytest | 35 行 |

**测试命令**：
```bash
python -m pytest tests/ -v    # 全部测试（33 条用例）
python -m pytest tests/ -v -k "test_format"  # 仅格式化测试
```

**测试文件结构**：
```
tests/
├── __init__.py
├── test_analyze_excel_report.py   # 核心分析逻辑测试
├── test_constants.py              # 常量验证
├── test_dingtalk_send_markdown.py # 推送测试（mock）
└── test_jycm_auto_report.py       # 入口文件扫描测试
```

---

## 6. 接口签名速查

```python
# M01 报告分析（scripts/analyze_excel_report.py）
def find_column(df: pd.DataFrame, keywords: list[str]) -> str | None
def find_columns(df: pd.DataFrame) -> dict[str, str | None]
def detect_date_column(df: pd.DataFrame) -> str | None
def parse_date_column(series: pd.Series) -> pd.Series

def fmt_number(val: Any) -> str
def fmt_currency(val: Any) -> str
def fmt_percent(val: Any) -> str

def analyze_excel(xlsx_path: Path, shops: list[str]) -> str
def save_report(markdown: str, filename: str) -> Path
def generate_report(xlsx_paths: list[Path], shop_names: list[str]) -> str

# M02 推送（scripts/dingtalk_send_markdown.py / feishu_send_markdown.py）
def send_dingtalk(title: str, markdown_text: str) -> bool
def send_feishu(title: str, markdown_text: str) -> bool

# M03 自动化（scripts/jycm_auto_report.py）
def main() -> int  # CLI 入口
```

---

## 7. 已知限制与债务

1. **无 `requirements.txt`**：依赖 `pandas`、`openpyxl`、`requests` 未锁定版本（任务 O-06）
2. **`scripts/` 非包结构**：无 `__init__.py`，测试和 `jycm_auto_report.py` 通过 `sys.path.insert` 导入
3. **`subprocess.run` 调推送**：`jycm_auto_report.py` 通过 `subprocess.run(["python3", ...])` 调用推送脚本，非函数级复用
4. **无日志持久化**：仅标准输出，无结构化日志文件
5. **日期计算分散**：多处重复计算"上周"和"近 N 天"逻辑，可统一为工具函数
6. **多店分析依赖文件名命名规则**：Excel 文件名的店铺名称提取基于启发式规则，不够健壮

---

## 附录 A：目录结构

```
qianniu_business_analytics/
├── SKILL.md                      # 技能主入口（Agent 指令）
├── auth.md                       # ~~旧版认证流程（已停用）~~
├── fetch-data.md                 # Excel 上传规则
├── fetch-data-api.md             # ~~旧版 API 参考（已归档）~~
├── report-analyze.md             # 报告分析规范
├── scripts/
│   ├── analyze_excel_report.py   # M01 核心分析逻辑（599 行）
│   ├── jycm_auto_report.py       # M03 CLI 入口（159 行）
│   ├── dingtalk_send_markdown.py # M02 钉钉推送（102 行）
│   ├── feishu_send_markdown.py   # M02 飞书推送（99 行）
│   └── constants.py              # M00 共享常量（76 行）
├── tests/
│   ├── test_analyze_excel_report.py  # M01 测试
│   ├── test_constants.py         # M00 测试
│   ├── test_dingtalk_send_markdown.py # M02 测试
│   └── test_jycm_auto_report.py  # M03 测试
├── data/                         # 用户放入的生意参谋 Excel
├── reports/                      # 生成的 Markdown 报告
├── AGENTS.md                     # 项目硬规则
├── README.md
├── status.md
├── session-log.md
├── ADR.md
├── lessons-learned.md
├── troubleshooting.md
├── experience-index.md
├── config/                       # 同步配置
└── docs/
    ├── design.md                 # 本文档
    ├── brief.md                  # 决策摘要
    └── tasks/                    # 任务分解
```

> 历史 API 取数脚本（`jycm_fetch_sycm_shop.py`、`qianniu_analytics_orchestrator.py`）已于 2026-06-25 删除。关键接口知识（shopIds 类型陷阱、日期时区处理）保留在 `lessons-learned.md` 中。

---

*文档版本：v2.0 | 最后更新：2026-06-25 | 对应架构：Excel 驱动流（v5.0.0+）*
