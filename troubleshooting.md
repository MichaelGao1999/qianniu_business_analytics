# 淘系店铺经营数据分析 — 急救手册

> 按错误关键词索引，只给"现象 → 原因 → 解决"，不给背景。
>
> 遇到问题时先搜此文件，再搜 `lessons-learned.md`（背景知识），最后问搜索引擎。

---

## 认证相关

### Cookie 过期 / 401 认证失败

| | 内容 |
|---|---|
| **状态** | 已修复（有自动刷新机制） |
| **现象** | 接口返回 401 或 302 重定向到登录页；`product.json` 返回 `success !== true` |
| **原因** | `jycmOpenApiCookie` 过期，需要刷新 |
| **解决** | 1. 读取 `auth/jycm.json` 中的 AK/SK<br>2. POST `openapi/employee/authToken.json` + Digest 认证获取新 requestCode<br>3. 回写 `auth/jycm.json`（只更新 `jycmOpenApiCookie`，保留 AK/SK）<br>4. 用新 Cookie 重试原请求。详见 `auth.md` 步骤 3 |

### Digest 刷新失败

| | 内容 |
|---|---|
| **状态** | 已知处理方案 |
| **现象** | POST authToken.json 返回非 200 或网络超时 |
| **原因** | 网络问题 / 服务端限流 / AK/SK 被服务端拒绝 |
| **解决** | 1. 自动重试 1 次<br>2. 仍失败 → 明确报 `FAILURE：Digest 刷新失败` + 真实原因<br>3. 若 AK/SK 被服务端拒绝 → 报 `AK/SK 不可用，需删除凭证文件后重新提供 Token Key` |

### auth/jycm.json 缺失字段

| | 内容 |
|---|---|
| **状态** | 已修复（有写入验证） |
| **现象** | 初始化后 Digest 刷新永远失败 |
| **原因** | 首次写入时只写了 `jycmOpenApiCookie`，漏写 `accessKey` / `secretKey` |
| **解决** | 1. 删除 `auth/jycm.json`<br>2. 重新引导用户提供 Token Key<br>3. 初始化时必须写入全部三字段，写入后立即读取验证非空 |

---

## 取数相关

### 日期区间多返回一天

| | 内容 |
|---|---|
| **状态** | 已修复（有强制约束） |
| **现象** | 请求 4/20-4/26，结果包含 4/27 的数据 |
| **原因** | `endDate` 使用了 `T23:59:59.999+08:00` 或 `Z`（UTC）后缀 |
| **解决** | 强制使用 `T00:00:00+08:00` 格式。详见 `SKILL.md` → 强约束 → 日期区间 |

### getAllShopList 返回空数组

| | 内容 |
|---|---|
| **状态** | 已知未修复（业务侧问题） |
| **现象** | 绑店检查显示「尚未绑任何店铺」 |
| **原因** | 用户未完成店铺绑定流程 |
| **解决** | 引导用户按 [绑店操作指南](https://alidocs.dingtalk.com/i/nodes/qnYMoO1rWxrkmoj2IznlmLDmJ47Z3je9) 完成绑定 |

### createAndDownload 返回失败

| | 内容 |
|---|---|
| **状态** | 已知未修复（需具体 case 分析） |
| **现象** | 步骤 G 返回 `code !== 0` 或 `success !== true` |
| **原因** | 参数错误 / 店铺无数据 / 指标不存在 / 日期范围超限 |
| **解决** | 1. 检查 `shopIds` 是否为 `List<String>`（非数字数组）<br>2. 检查 `channelName` / `dataPlatform` / `dataType` / `dataDimension` 是否匹配<br>3. 检查日期范围是否超限（如超过 90 天）<br>4. 检查 `indicators` 是否为步骤 F 返回的有效 key |

---

## 报告相关

### openpyxl 未安装

| | 内容 |
|---|---|
| **状态** | 临时绕过 |
| **现象** | 分析 Excel 时报 `ModuleNotFoundError: No module named 'openpyxl'` |
| **原因** | 依赖未声明或环境未安装 |
| **解决** | `pip install openpyxl`。建议后续补充 `requirements.txt` |

### 钉钉推送失败

| | 内容 |
|---|---|
| **状态** | 已知未修复（需用户侧配置） |
| **现象** | `dingtalk_send_markdown.py` 返回 HTTP 400/403 |
| **原因** | Webhook token 错误 / 机器人被禁 / 内容含敏感词 |
| **解决** | 1. 检查 `DINGTALK_WEBHOOK` 环境变量是否正确<br>2. 检查钉钉机器人是否被禁言<br>3. 检查 Markdown 内容是否含敏感关键词<br>4. 超长内容（>18000 字符）会自动截断，检查截断后是否格式破坏 |

---

## 环境相关

### Windows Git Bash LF/CRLF 警告

| | 内容 |
|---|---|
| **状态** | 已知未修复（不影响功能） |
| **现象** | `git add` 时提示 `LF will be replaced by CRLF` |
| **原因** | Windows 默认 `core.autocrlf=true` |
| **解决** | 不影响功能；跨平台协作前建议统一配置 `git config --global core.autocrlf true` |

---

*新增条目时复制上方模板，按"错误关键词"作为标题，便于快速搜索。*

---

## 存档提示

**用户说「存储」时**，AI 应回顾本轮会话内容，评估是否有新的具体报错需要记入本文件。有则按模板追加；没有则跳过。
