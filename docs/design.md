# 淘系店铺经营数据分析 — 技术设计文档

> 架构总览、模块划分、接口契约、数据流。
> 本文档由阶段二产出，是阶段三~五的不可变更决策边界。

---

## 1. 架构总览

本项目为 **自包含技能包**，采用**分层流水线架构**：

```
┌─────────────────────────────────────────────────────────────┐
│                      入口层（Entry）                         │
│  ┌──────────────┐  ┌──────────────┐                        │
│  │ 对话触发     │  │ CLI 触发     │                        │
│  │ (SKILL.md)   │  │ (jycm_auto_  │                        │
│  │              │  │  report.py)  │                        │
│  └──────┬───────┘  └──────┬───────┘                        │
└─────────┼────────────────┼──────────────────────────────────┘
          │                │
          ▼                ▼
┌─────────────────────────────────────────────────────────────┐
│                   编排层（Orchestration）                     │
│         jycm_auto_report.py (Excel 驱动)                    │
│              │                                              │
│    ┌─────────┼─────────┐                                   │
│    ▼         ▼         ▼                                   │
│  扫描Excel → 分析报告 → 推送                                   │
└─────────────────────────────────────────────────────────────┘
          │
    ┌─────┴─────┬─────────────┐
    ──┴────┬─────┴─────────────┴──┐
    ▼           ▼               ▼
┌──────────┐ ┌──────────┐ ┌────────────┐
│ 数据准备 │ │ 报告分析 │ │ 消息推送   │
│ (用户手动 │ │ (M03)    │ │ (M04)      │
│  导出)   │ │          │ │            │
└──────────┘ └─────┬────┘ └─────┬──────┘
                   │             │
                   ▼             ▼
┌────────────────────────────────────────┐
│            基础设施层                   │
│  data/  │  reports/  │  Webhook HTTP  │
└────────────────────────────────────────┘
```

---

## 2. 模块划分

### M01 认证管理（Auth Management） — ~~已废弃~~

**职责**：~~管理 JYCM OpenAPI 的 Cookie 生命周期。~~
**2026-06-25 废弃**：Excel 驱动模式无需认证。`auth/` 目录已清空，`auth.md` 停用。

**核心文件**：
- `auth/jycm.json` — ~~凭证文件~~（已废弃）
- `auth.md` — ~~认证流程文档~~（已停用）

**对外接口**：

| 接口 | 输入 | 输出 | 说明 |
|------|------|------|------|
| `initialize_auth(token_key)` | 用户提供的 Token Key | `auth/jycm.json`（三字段完整） | 首次初始化 |
| `get_effective_cookie()` | `auth/jycm.json` | 有效 Cookie 字符串 / FAILURE | 读取缓存 → 校验 → Digest 刷新 |
| `refresh_cookie(ak, sk)` | AK, SK | 新 requestCode / FAILURE | POST authToken.json + Digest |

**数据契约**：
```json
{
    "accessKey": "string",
    "secretKey": "string",
    "jycmOpenApiCookie": "string"
}
```

---

### M02 淘系取数引擎（Fetch Engine） — ~~已废弃~~

**职责**：~~执行 JYCM OpenAPI A→G 接口链，获取生意参谋数据并下载 Excel。~~
**2026-06-25 废弃**：API 取数路线已确认放弃，脚本 `jycm_fetch_sycm_shop.py` 已删除。当前为 Excel 驱动模式（数据获取由用户手动从生意参谋导出）。

**核心文件**：
- ~~`scripts/jycm_fetch_sycm_shop.py` — 取数脚本（已删除）~~
- `fetch-data.md` — 取数规则文档
- `fetch-data-api.md` — API 完整参考（归档）

**对外接口**：

| 接口 | 输入 | 输出 | 说明 |
|------|------|------|------|
| `fetch_report(config, cookie)` | 取数配置 + Cookie | Excel 下载 URL / 错误码 | 执行完整 A→G 链 |
| `get_shop_list(cookie)` | Cookie | 店铺列表（含渠道过滤） | 支持按 `channelName=天猫淘宝` 过滤 |

**数据契约（取数配置）**：
```json
{
    "channelName": "天猫淘宝",
    "dataPlatform": "生意参谋",
    "dataType": "店铺",
    "dataDimension": "整体",
    "dateType": "day",
    "startDate": "2026-04-20T00:00:00+08:00",
    "endDate": "2026-04-26T00:00:00+08:00",
    "shopIds": ["12345", "67890"],
    "indicators": ["访客数", "支付金额"],
    "isAutoUpdate": "0",
    "isDataFormat": "Y"
}
```

**接口链（A→G）**：

| 步骤 | 接口 | 方法 | 用途 |
|------|------|------|------|
| A | `/fetchData/getChannelList.json` | GET | 验证渠道 |
| B | `/fetchData/getDataPlatformMap.json` | GET | 获取平台映射 |
| C | `/fetchData/getDataTypeMapList.json` | GET | 获取数据类型 |
| D | `/fetchData/getDataDimensionMapList.json` | GET | 获取数据维度 |
| E | `/fetchData/getDateTypeList.json` | GET | 获取日期类型（可选） |
| F | `/fetchData/getIndicatorListByDims.json` | POST | 获取指标列表 |
| S | `/fetchData/getAllShopList.json` | GET | 获取店铺列表 |
| G | `/fetchData/createAndDownload.json` | POST | 创建并下载报表 |

---

### M03 报告生成（Report Generation）

**职责**：读取 Excel 数据，生成 Markdown 四段式分析报告。

**核心文件**：
- `report-analyze.md` — 报告规范文档
- `data/` — 原始数据目录
- `reports/` — 分析报告目录

**对外接口**：

| 接口 | 输入 | 输出 | 说明 |
|------|------|------|------|
| `analyze_excel(xlsx_path, shops)` | Excel 文件路径 + 店铺列表 | Markdown 报告正文 | 四段式分析 |
| `save_report(markdown, filename)` | Markdown 正文 + 文件名 | `reports/` 下的 `.md` 文件 | 持久化报告 |

**报告结构（四段式，单店/多店通用）**：

```markdown
# XX店铺经营分析_20260401_20260407

## 一、整体指标
（表：指标｜数值）

## 二、日度趋势
（表：日期｜指标｜数值）

## 三、店铺排行 TOP N
（单店：商品/渠道 TOP；多店：店铺横向对比 TOP）

## 四、分析总结
（3~6 条量化要点；多店额外点出头部/尾部/Gap 最大店铺）

## 五、原始数据下载
（OSS 下载链接）
```

---

### M04 钉钉推送（DingTalk Push）

**职责**：将 Markdown 报告推送到钉钉机器人。

**核心文件**：
- `scripts/dingtalk_send_markdown.py`

**对外接口**：

| 接口 | 输入 | 输出 | 说明 |
|------|------|------|------|
| `send_dingtalk(title, markdown_text)` | 标题 + Markdown 正文 | 成功/失败 | 通过 Webhook 推送 |

**约束**：
- 标题必须含「经营」，否则自动补前缀 `经营·`
- 正文超过 18000 字符自动截断
- `DINGTALK_WEBHOOK` 环境变量未配置时跳过推送

---

### M05 自动化编排（Automation Orchestrator）

**职责**：CLI 入口，支持定时任务和命令行参数驱动。

**核心文件**：
- `scripts/jycm_auto_report.py` — 自动化全流程

**对外接口**：

| 接口 | 输入 | 输出 | 说明 |
|------|------|------|------|
| `main(args)` | CLI 参数（--days, --shops, --dingtalk） | 执行结果 + 报告文件 | 取数→分析→推送一条龙 |

---

### M06 对话编排（Dialog Orchestrator）

**职责**：Agent 对话流程控制，按 SKILL.md 规范响应用户自然语言请求。

**核心文件**：
- `SKILL.md` — 技能主入口
- `scripts/jycm_auto_report.py` — 自动化入口

**流程状态机**：

```
[用户输入] → [预检] → [取数] → [报告] → [推送]
              ↓         ↓         ↓         ↓
           授权/      Cookie/   Excel/   Webhook/
           订购/      接口链    分析     Markdown
           绑店
```

**分支规则**：
- 预检不通过 → 一次性列出所有缺失项 + 指引链接
- 取数失败 → 按错误类型分流（401→刷新Cookie / 参数错误→澄清 / 非淘系→明确拒绝）

---

## 3. 模块间调用关系矩阵

| 调用方 ↓ \ 被调用方 → | M01 认证 | M02 取数 | M03 报告 | M04 推送 | M05 自动化 | M06 对话 |
|----------------------|---------|---------|---------|---------|-----------|---------|
| M01 认证             | —       | 提供 Cookie | —       | —       | —         | 提供 Cookie |
| M02 取数             | 需要 Cookie | —       | 输出 Excel | —       | 被调用    | 被调用    |
| M03 报告             | —       | 输入 Excel | —       | 输出 Markdown | 被调用 | 被调用 |
| M04 推送             | —       | —       | 输入 Markdown | —       | 被调用    | 被调用    |
| M05 自动化           | 调用 M01 | 调用 M02 | 调用 M03 | 调用 M04 | —         | —       |
| M06 对话             | 调用 M01 | 调用 M02 | 调用 M03 | 调用 M04 | —         | —       |

---

## 4. 数据流

### 4.1 核心数据实体生命周期

```
Token Key（用户一次性提供）
    ↓
auth/jycm.json {accessKey, secretKey, jycmOpenApiCookie}
    ↓
Cookie（全链路携带）
    ↓
A→G 接口链 → Excel 文件（data/ 目录）
    ↓
openpyxl 读取 → DataFrame / dict
    ↓
Markdown 报告（reports/ 目录）
    ↓
钉钉推送（Webhook）
```

### 4.2 数据持久化方案

| 数据 | 存储位置 | 格式 | 生命周期 |
|------|---------|------|---------|
| 凭证（AK/SK/Cookie） | `auth/jycm.json` | JSON | 长期（直到用户删除） |
| 原始数据（Excel） | `data/` | .xlsx | 每次取数覆盖或新增 |
| 分析报告 | `reports/` | .md | 每次分析生成新文件 |
| 日志 | 标准输出 | 文本 | 进程结束即消失（待增强） |

---

## 5. 测试策略

| 测试层级 | 目标 | 方法 | 优先级 |
|---------|------|------|--------|
| 单元测试 | 认证模块、日期计算、钉钉截断逻辑 | pytest | P1 |
| 集成测试 | A→G 接口链端到端 | mock HTTP + 真实 Cookie | P2 |
| 契约测试 | API 请求/响应格式 | JSON Schema 校验 | P2 |
| 手动验证 | 报告排版、钉钉渲染效果 | 实际运行 + 人工检查 | P2 |

---

## 6. 接口签名速查

### Python 函数接口

```python
# M01 认证
def initialize_auth(token_key: str) -> bool
def get_effective_cookie() -> Optional[str]
def refresh_cookie(ak: str, sk: str) -> Result[str, str]

# M02 取数
def fetch_report(config: Dict[str, Any], cookie: str) -> Result[str, str]
def get_shop_list(cookie: str, channel_name: str = "天猫淘宝") -> List[Dict]

# M03 报告
def analyze_excel(xlsx_path: Path, shops: List[str]) -> str
def save_report(markdown: str, filename: str) -> Path

# M04 推送
def send_dingtalk(title: str, markdown_text: str) -> bool

# M05 自动化
def main() -> int  # CLI 入口
```

---

## 7. 已知限制与债务

1. **无 requirements.txt**：`requests`、`openpyxl` 等依赖未声明
2. **外部路径依赖**：`jycm_auto_report.py` 中 `sys.path.insert` 引用外部技能包
3. **无日志持久化**：仅标准输出，无结构化日志文件
4. **无单元测试**：当前 0 测试覆盖
5. **Cookie 存储权限**：`auth/jycm.json` 未强制 `chmod 600`
6. **日期计算分散**：多处重复计算"上周"逻辑，未统一工具函数

---

*文档版本：v1.0 | 最后更新：2026-05-20*
