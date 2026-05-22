---
document_type: api_reference
audience: llm_agent
topic: jycm_fetch_data_config_chain
base_url: https://jycm.lydaas.com
auth: session_cookie
---

# 取数配置链 API（Agent 版）

> **本技能范围限定：仅使用 `channelName=天猫淘宝` + `dataPlatform=生意参谋`（`type=shop`）的取数路径。本文档中出现的京东 / 抖音 / 拼多多 / 小红书 / 观星台等示例仅为 API 原响应的参考，不属于本技能的可用取数路径；其中品牌（`type=brand`）线（步骤 S₂）在本技能内不会被调用。**
> **多店取数：本技能支持在一次 `createAndDownload` 请求中传入多个淘系店铺 id（`shopIds: List<String>`，例如 `["436", "437", "502"]`），不需拆成多次请求；所有 id 必须来自同一次 `getAllShopList` 在淘系（`channelName=天猫淘宝`）下的匹配结果。**

> 人类阅读：本文件为 **OpenClaw / 自动化 Agent** 优化的接口说明；**禁止跳过步骤顺序**；③④ 的选项来自 **响应 JSON 的 object key**，不是 value；**步骤 B 的 `type` 决定 G 用 `shopIds` 还是 `brandId`**（见 §5、§9.5～§9.6；本技能仅走 `type=shop`）；**`indicators` 默认取步骤 F 的全部 key**。

---

## 1. Agent 执行协议（必读）

### 1.1 目标

按顺序调用接口，完成「选配置 → 选指标 → **按平台类型解析主体 id（店铺或品牌）** → 新建报表并拿到下载链接」。核心链为 **A～F + S + G**（见 §2）：**S** 分两支——若步骤 **B** 选中项的 **`type === "shop"`**，用 **`getAllShopList`** 解析 **`shopIds`**；若 **`type === "brand"`**，用 **`getBrandListByDataPlatform`** 解析 **`brandId`**（见 §9.5、§9.6）。**禁止**把用户口头编号直接当成 id。

### 1.2 必须维护的状态变量（每步更新）

在调用过程中，请在上下文中维护以下键（名称固定，便于拼接请求）：

| 变量名 | 类型 | 由哪一步写入 | 用途 |
|--------|------|----------------|------|
| `channelName` | string | 步骤 A | ②③④⑤⑥ |
| `dataPlatform` | string | 步骤 B（取 `data[].platform`） | ③④⑤⑥ |
| `dataType` | string | 步骤 C（取 `data` 的 **key**） | ④⑤⑥ |
| `dataDimension` | string | 步骤 D（取 `data` 的 **key**） | ⑤⑥ |
| `dateType` | string | 步骤 E 或 `getDateTypeList` | ⑤⑥ |
| `indicatorKeys` | string[] | 步骤 F：`Object.keys(data)` **全量**（默认不遗漏；仅当用户明确要求部分指标时才取子集） | G 的 `indicators` |
| `platformType` | `"shop"` \| `"brand"` | **步骤 B**：当前选用的 `data[].type` | 决定走 **S 店铺** 还是 **S 品牌** |
| `shopIds` | **string[]**（`List<String>`） | **步骤 S（仅 `type=shop`）**：`getAllShopList` 的 `data[]` 按 **`shopName`** 匹配 → 取 **`id`** 后 **`String(id)`** 写入 G | G（与 `brandId` 互斥）；**禁止**在 JSON 里用数字数组代替 |
| `brandId` | string | **步骤 S（仅 `type=brand`）**：`getBrandListByDataPlatform` 的 `data` 按 **品牌名/value** 匹配 → **key**（品牌 id） | G（与 `shopIds` 互斥） |
| `itemIds` | string[] | 可选；商品维度取数时由业务提供 | G |
| `datasource` | string | **默认固定为 `电商后台`**（与业务侧约定一致；未指定时 Agent 应使用此值） | ⑥ `createAndDownload` / `createReport` |

### 1.3 关键规则（违反会导致错误选项）

1. **顺序**：`A → B → C → D → (E 可选) → F → S → G`，不可颠倒（**F 与 S 可互换**，但须在 **G 之前**都完成）。  
2. **步骤 B 的 `type`（与 `createAndDownload` 主体字段）**：  
   - 选中平台项的 **`type === "shop"`** → **G** 必须带非空 **`shopIds`**（来自 **`getAllShopList`**），**不要**带 `brandId`（服务端会按业务清空其一）。  
   - **`type === "brand"`**（如观星台）→ **G** 必须带非空 **`brandId`**（来自 **`getBrandListByDataPlatform`**），**不要**依赖 `shopIds`（服务端会清空店铺侧字段）。  
   - **`itemIds`**：可选；商品粒度取数时传入 `List<String>`，与店铺/品牌维度按业务互斥或并存以实际报表为准。  
3. **③④ 的 `data` 是对象**：用户可选值 = **该对象的所有 key**；value 常为 `"{}"` 字符串，**不要**从 value 解析选项。  
4. **⑤ 的 `data` 是对象**：指标 API 名 = **key**（如 `pay_ord_amt_1d_001`）；`columnNameZh` 是中文展示名。  
5. **`indicators`（步骤 G）**：默认 = **步骤 F 返回 `data` 的全部 key**（`Object.keys(data)`），**不得遗漏**；仅当用户明确说「只要某几个指标」时才缩小范围。  
6. **`shopIds`（`type=shop`）**：必须由 **`GET /fetchData/getAllShopList.json`** 解析：按 **`shopName`** 匹配用户描述，取 **`id`**。**禁止**把口语数字直接当 id。  
7. **`POST /fetchData/createAndDownload.json` 的 `shopIds`**：请求体中必须为 **`List<String>`**（JSON 数组元素为 **字符串**，如 `["436","437"]` 或长数字 id 亦用引号包裹）。**禁止**传成 **`List<Long>`** 或未加引号的数字数组（如 `[436,437]`），其它 Agent/序列化易错；从 `getAllShopList` 取到 `id` 后统一 **`String(id)`** 再入参。  
8. **`brandId`（`type=brand`）**：必须由 **`GET /fetchData/getBrandListByDataPlatform.json?dataPlatform={步骤B的platform}`** 解析：`data` 为 **品牌 id → 品牌名称** 的映射，按用户说的品牌名找到对应 **key** 作为 `brandId`（字符串）。  
9. **GET 查询参数**：`channelName`、`dataPlatform`、`dataType` 等含中文时必须 **URL 编码**。  
10. **G**：仅新建；`indicators` 非空；**店铺线**与**品牌线**校验与 `FetchReportController` / `DATA_PLATFORM_FOR_BRAND` 一致（观星台必须品牌，非观星台必须店铺）。  
11. **`datasource`（步骤 G）**：**默认 `电商后台`**。  
12. **日期时区（`startDate` / `endDate`）**：**必须使用北京时区偏移 `+08:00`，且时间部分统一为 `T00:00:00+08:00`**（即结束日当天的零点，如 `2026-04-26T00:00:00+08:00`）。示例：要取上周 4/20-4/26 7 天 → `startDate=2026-04-20T00:00:00+08:00`、`endDate=2026-04-26T00:00:00+08:00`。
    - **禁用 `T23:59:59.999+08:00`**：后端实测会多返回次日数据（如 4/20-4/26 会拿到 4/27），导致区间多出一天。
    - **禁用 `Z`（UTC 零时区）**：使用 `Z` 会让后端把「北京当天 00:00」当作「UTC 00:00」解析，等价于北京 08:00，同样导致区间多一天。
13. **成功码**：响应中 `code == 0` 且 `success == true`（若环境不同以实际为准）。

---

## 2. 端点索引（机器可读）

| step | id | method | path | role |
|------|-----|--------|------|------|
| A | `getChannelList` | GET | `/fetchData/getChannelList.json` | 取渠道列表 |
| B | `getDataPlatformMap` | GET | `/fetchData/getDataPlatformMap.json` | 取数据平台列表 |
| C | `getDataTypeMapList` | GET | `/fetchData/getDataTypeMapList.json` | 取数据类型 key |
| D | `getDataDimensionMapList` | GET | `/fetchData/getDataDimensionMapList.json` | 取维度 key |
| E | `getDateTypeList` | GET | `/fetchData/getDateTypeList.json` | 可选：取 `dateType` |
| F | `getIndicatorListByDims` | POST | `/fetchData/getIndicatorListByDims.json` | 取指标元数据（key 列表 → `indicators`） |
| S₁ | `getAllShopList` | GET | `/fetchData/getAllShopList.json` | **`B.type=shop`**：按 `shopName` → `shopIds` |
| S₂ | `getBrandListByDataPlatform` | GET | `/fetchData/getBrandListByDataPlatform.json` | **`B.type=brand`**：按品牌名 → `brandId` |
| G | `createAndDownload` | POST | `/fetchData/createAndDownload.json` | 新建报表；`shopIds` 或 `brandId` 或 `itemIds` 见 §10 |

**前缀**：`BASE = https://jycm.lydaas.com`

---

## 3. 响应包装（所有接口）

解析时优先读：

```json
{
  "code": 0,
  "message": "success",
  "data": {},
  "success": true,
  "ok": true,
  "traceId": "..."
}
```

| 字段 | 含义 |
|------|------|
| `code` | 业务码，`0` 成功 |
| `data` | 载荷，类型见各步 |
| `success` / `ok` | 布尔成功标志 |

---

## 4. 步骤 A：`getChannelList`

| 属性 | 值 |
|------|-----|
| **HTTP** | `GET /fetchData/getChannelList.json` |
| **Query** | 无 |

**从响应提取**

- `data` 为 `string[]`  
- 设置：`channelName = data[i]`（用户或策略选一个）

**示例 `data`**

```json
["天猫淘宝", "京东", "拼多多", "抖音", "小红书", "唯品会"]
```

---

## 5. 步骤 B：`getDataPlatformMap`

| 属性 | 值 |
|------|-----|
| **HTTP** | `GET /fetchData/getDataPlatformMap.json` |
| **Query** | `channelName={channelName}`（URL 编码） |

**从响应提取**

- `data` 为 `{ type: string, platform: string }[]`  
- **`type`**：`"shop"` 表示该平台走 **店铺** 维度（后续用 **`getAllShopList`** → `shopIds`）；**`"brand"`** 表示 **品牌/观星台** 等（后续用 **`getBrandListByDataPlatform`** → `brandId`）。  
- 设置：`dataPlatform = 选中项.platform`，并记录 **`platformType = 选中项.type`** 供步骤 S、G 使用。

**示例 `data`**

```json
[
  { "type": "shop", "platform": "生意参谋" },
  { "type": "brand", "platform": "观星台" }
]
```

---

## 6. 步骤 C：`getDataTypeMapList`

| 属性 | 值 |
|------|-----|
| **HTTP** | `GET /fetchData/getDataTypeMapList.json` |
| **Query** | `channelName`, `dataPlatform` |

**从响应提取**

- `data` 为 `Record<string, string>`（键为数据类型中文名）  
- 设置：`dataType = 选中的 key`（如 `"店铺"`）

**示例 `data`**

```json
{
  "店铺": "{}",
  "商品": "{}",
  "品类": "{}",
  "内容": "{}",
  "客户": "{}",
  "推荐分析": "{}"
}
```

---

## 7. 步骤 D：`getDataDimensionMapList`

| 属性 | 值 |
|------|-----|
| **HTTP** | `GET /fetchData/getDataDimensionMapList.json` |
| **Query** | `channelName`, `dataPlatform`, `dataType` |

**从响应提取**

- `data` 为 `Record<string, string>`  
- 设置：`dataDimension = 选中的 key`（如 `"整体"`）

**示例 `data`**

```json
{
  "整体": "{\"image\":\"\",\"text\":\"\"}",
  "分小时": "{}",
  "关键词": "{\"image\":\"\",\"text\":\"\"}"
}
```

---

## 8. 步骤 E（可选）：`getDateTypeList`

当不确定 `dateType` 时调用（参数与维度相关，见 **[fetch-report-api-doc.md](./fetch-report-api-doc.md)**）。

- 设置：`dateType` = 返回列表中某项的 `dateType` 字段（如 `day`）。

---

## 9. 步骤 F：`getIndicatorListByDims`

| 属性 | 值 |
|------|-----|
| **HTTP** | `POST /fetchData/getIndicatorListByDims.json` |
| **Header** | `Content-Type: application/json` |
| **Body JSON** | 见下表 |

| 字段 | 必填 | 说明 |
|------|------|------|
| `channelName` | 是 | 同状态变量 |
| `dataPlatform` | 是 | 同状态变量 |
| `dataType` | 是 | 同状态变量 |
| `dataDimension` | 是 | 同状态变量 |
| `dateType` | 否 | 如 `day` |
| `dims` | 否 | `Record<string, string[]>` |

**从响应提取**

- `data` 为 `Record<string, object>`，**key = 指标字段名**  
- 设置：`indicatorKeys = Object.keys(data)`（**默认全量，不遗漏**；仅用户明确要求部分指标时取子集）  
- 每个 value 含：`columnName`, `columnNameZh`, `columnDesc`, `dataType`, `tableName`, `bizType` 等

**请求示例**

```json
{
  "channelName": "天猫淘宝",
  "dataPlatform": "生意参谋",
  "dataType": "店铺",
  "dataDimension": "整体",
  "dateType": "day"
}
```

---

## 9.5 步骤 S₁：`getAllShopList`（**仅当步骤 B 选中项 `type=shop`**）

用户描述的「某店铺」一般指 **店铺名称 `shopName`**，不是数字 id。若当前平台 **`type === "shop"`**，必须先调本接口再填 `createAndDownload` 的 **`shopIds`**。

| 属性 | 值 |
|------|-----|
| **HTTP** | `GET /fetchData/getAllShopList.json` |
| **Query** | 无 |
| **Header** | 需登录 Session（`Cookie`） |

**从响应提取**

- `data` 为 **数组**，元素类型类似：`{ "id": "436" 或 436, "shopName": "店铺18", "channelName": "...", ... }`（字段以实际为准，见 `EnterpriseShopDO`）。  
- **匹配算法（Agent）**：  
  1. 令 `targets = 用户给出的店铺名称列表`（单店就是单元素列表）。  
  2. 对每个 `target`，在 `data` 中找 **`shopName === target`**；若无，再尝试 **`shopName.includes(target)`** 或大小写不敏感匹配；只保留 `channelName === "天猫淘宝"` 的候选项。  
  3. 每个 `target` 取匹配项的 **`id`**，汇总后在步骤 **G** 请求体中填入 **`shopIds = [String(id), …]`**（**`List<String>`**，勿用 number 数组；多店场景即一个数组内多个字符串 id）。  
  4. 若任一 `target` 的匹配结果为 **0 条或多条**，应 **中止**并提示用户澄清（列出候选 `shopName` / `id`）；**禁止**在多店请求中静默跳过或用错店铺。

**示例（节选）**

```json
{
  "code": 0,
  "data": [
    { "id": "436", "shopName": "店铺18", "channelName": "天猫淘宝" }
  ]
}
```

---

## 9.6 步骤 S₂：`getBrandListByDataPlatform`（**仅当步骤 B 选中项 `type=brand`**）

> ⚠️ **本技能不使用此步骤**：淘系生意参谋为 `type=shop`，始终走 §9.5 店铺线。本小节仅作为 API 参考保留，帮助理解整体路由。

若 **`type === "brand"`**（如 **观星台**），**不要**用 `getAllShopList` 填 `shopIds`；应调用本接口，用返回映射解析 **`brandId`**。

| 属性 | 值 |
|------|-----|
| **HTTP** | `GET /fetchData/getBrandListByDataPlatform.json` |
| **Query** | `dataPlatform={dataPlatform}`（**与步骤 B 选中项的 `platform` 一致**，须 URL 编码） |
| **Header** | 需登录 Session（`Cookie`） |

**从响应提取**

- `data` 为 **`Record<string, string>`**：**key = 品牌 id**，**value = 品牌显示名**（线上形态可能与旧文档「数组」示例不同，**以实际响应为准**）。  
- **匹配算法（Agent）**：按用户给出的品牌名与 **value** 做精确或模糊匹配，取对应 **key** 作为 **`brandId`**（字符串）。  
- 多匹配 / 无匹配时提示用户从列表中选择。

**请求示例**

```bash
curl 'https://jycm.lydaas.com/fetchData/getBrandListByDataPlatform.json?dataPlatform=%E8%A7%82%E6%98%9F%E5%8F%B0'
```

**响应示例**

```json
{
  "traceId": "dd740e13cf9f9f8229fe6844d9db676c",
  "code": 0,
  "message": "success",
  "data": {
    "20085": "Olay/玉兰油",
    "20090": "潘婷",
    "3322567": "SK-II"
  },
  "success": true,
  "ok": true
}
```

---

## 10. 步骤 G：`createAndDownload`

**源码**：`com.alibaba.lingyang.sycm.datafetch.FetchReportController#createAndDownload`

| 属性 | 值 |
|------|-----|
| **HTTP** | `POST /fetchData/createAndDownload.json` |
| **Header** | `Content-Type: application/json` |
| **Body** | `ReportSettingRequest`（仅新建） |

**服务端行为（固定）**

1. 校验 `indicators` 非空；观星台/店铺规则见下  
2. 拉新版企业 → `403`「拉新版暂无权限」  
3. `creatReport` → `submitDownloadTask` → 轮询 `queryDownloadUrl`，**2s × 15 次**（约 30s）  
4. 成功：`data` 含 **`url` 或 `downloadUrl`**（OSS 签名链接）；失败：`500`；轮询结束未完成：`message` 含「等待下载超时」

### 10.1 Body 字段表（Agent 填表）

| 字段 | 必填 | 来源 |
|------|------|------|
| `id` | 否 | 固定 `0` |
| `reportName` | 是 | 用户指定 |
| `datasource` | 是 | **默认：`电商后台`**（数据来源标识；与门户/取数业务约定一致） |
| `channelName` | 是 | 步骤 A |
| `dataPlatform` | 是 | 步骤 B |
| `dataType` | 是 | 步骤 C |
| `dataDimension` | 是 | 步骤 D |
| `dateType` | 否 | 步骤 E |
| `startDate` | 是 | ISO8601，**必须显式用北京时区偏移 `+08:00`、时间部分固定为 `T00:00:00+08:00`**（如 `2026-04-01T00:00:00+08:00`）。**禁用 `Z`、禁用 `T23:59:59.999` 后缀**（详见 §1.3.12） |
| `endDate` | 是 | ISO8601，**必须显式用 `+08:00`、时间部分固定为 `T00:00:00+08:00`**（即结束日当天的零点，如 `2026-04-26T00:00:00+08:00`）。**禁用 `T23:59:59.999+08:00`**：后端实测会多返回次日数据，导致区间多一天（已知缺陷；详见 §1.3.12） |
| `indicators` | 是 | **步骤 F** 的 **`Object.keys(data)` 全量**（默认），非空 |
| `shopIds` | 条件 | **`B.type=shop` 时必填**：非空 **`List<String>`**（JSON 中为字符串 id 数组），来自 **§9.5**，每个元素为 **`String(店铺id)`**；**禁止** `List<Long>` / 未加引号数字数组；**`B.type=brand` 时不要传或会被服务端清空** |
| `brandId` | 条件 | **`B.type=brand` 时必填**：非空字符串，来自 **§9.6** 的 `data` **key**；**`type=shop` 时不要传或会被清空** |
| `itemIds` | 否 | 可选，`List<String>`；商品维度取数时使用（与店铺/品牌组合规则以后端为准） |
| `dims` / `customFilters` | 否 | 可选 |
| `isAutoUpdate` | 否 | **Agent 默认：`"0"`**（字符串，关闭自动更新）；需自动更新时再改 |
| `autoUpdateCycle` | 否 | 与 `isAutoUpdate` 配合；默认不传 |
| `isDataFormat` | 否 | **Agent 默认：`"Y"`**（字符串，格式化导出）；用户明确要求时再改 |

**成功响应 `data`（线上常见两种形态，以实际为准）**

```json
{
  "url": "https://....aliyuncs.com/....xlsx?Expires=...&Signature=...",
  "status": "1"
}
```

部分环境也可能返回 `downloadUrl` + 文本类 `status`（如 `FINISHED`）。**Agent 解析**：优先取 `data.url` 或 `data.downloadUrl` 作为 Excel 下载地址；`status` 以实际枚举为准。

---

## 11. 决策表（步骤 B 的 `type` / 平台与 G  body）

| 步骤 B 选中项 `type` | 步骤 S | `createAndDownload` 主体 |
|---------------------|--------|---------------------------|
| **`shop`** | **§9.5** `getAllShopList` | **`shopIds`** 非空；`brandId` 不传或空 |
| **`brand`**（如观星台） | **§9.6** `getBrandListByDataPlatform`（`dataPlatform` = 当前 `platform`） | **`brandId`** 非空；`shopIds` 不传或空 |

**与后端一致**：`FetchReportController#createAndDownload` 对观星台/品牌平台会 **清空 `shopIds`**，非品牌平台会 **清空 `brandId`**。**`itemIds`** 在需要商品粒度时可选传入。

---

## 12. 一键复制：完整工作流（伪代码）

```text
GET  /fetchData/getChannelList.json
  → channelName

GET  /fetchData/getDataPlatformMap.json?channelName=...
  → dataPlatform = data[0].platform   // 或用户选择

GET  /fetchData/getDataTypeMapList.json?channelName=...&dataPlatform=...
  → dataType = key from data

GET  /fetchData/getDataDimensionMapList.json?channelName=...&dataPlatform=...&dataType=...
  → dataDimension = key from data

[可选] GET /fetchData/getDateTypeList.json?... 
  → dateType

POST /fetchData/getIndicatorListByDims.json
  body: { channelName, dataPlatform, dataType, dataDimension, dateType? }
  → indicatorKeys = Object.keys(data)   // 默认全量，不遗漏

IF 步骤 B 选中 platform 项的 type == "shop":
  GET /fetchData/getAllShopList.json
    → shopIds = 按 shopName 从 data[] 解析 id 后 **List<String>**（每项 String(id)，勿用 Long 数组）
ELSE IF type == "brand":
  GET /fetchData/getBrandListByDataPlatform.json?dataPlatform={当前 platform}
    → brandId = 在 data{ id -> 名称 } 中按品牌名匹配到的 key
  // itemIds 可选：按业务传入商品 id 列表

POST /fetchData/createAndDownload.json
  body: { datasource: "电商后台", channelName, dataPlatform, dataType, dataDimension, dateType?,
          startDate, endDate, indicators: indicatorKeys,
          shopIds? 或 brandId?,  itemIds?,
          ... }
  → 下载地址 from data.url 或 data.downloadUrl
```

---

## 13. curl 参考（人类调试）

```bash
# B
curl "${BASE}/fetchData/getDataPlatformMap.json?channelName=%E4%BA%AC%E4%B8%9C"

# F（响应 data 的全部 key 作为 indicators 全量）
curl "${BASE}/fetchData/getIndicatorListByDims.json" \
  -H "Content-Type: application/json" \
  -d '{"channelName":"天猫淘宝","dataPlatform":"生意参谋","dataType":"店铺","dataDimension":"整体","dateType":"day"}'

# S₁ 店铺线（type=shop）
curl "${BASE}/fetchData/getAllShopList.json"

# S₂ 品牌线（type=brand，dataPlatform 与 B 中选中 platform 一致）
curl "${BASE}/fetchData/getBrandListByDataPlatform.json?dataPlatform=%E8%A7%82%E6%98%9F%E5%8F%B0"

# G 店铺线示例
curl "${BASE}/fetchData/createAndDownload.json" \
  -H "Content-Type: application/json" \
  -d '{"id":0,"reportName":"x","datasource":"电商后台","channelName":"天猫淘宝","dataPlatform":"生意参谋","dataType":"店铺","dataDimension":"整体","dateType":"day","startDate":"2026-03-01T00:00:00+08:00","endDate":"2026-03-15T00:00:00+08:00","shopIds":["436"],"indicators":["<F的全部key>"]}'

# G 品牌线示例（无 shopIds，有 brandId；可另传 itemIds）
curl "${BASE}/fetchData/createAndDownload.json" \
  -H "Content-Type: application/json" \
  -d '{"id":0,"reportName":"x","datasource":"电商后台","channelName":"天猫淘宝","dataPlatform":"观星台","dataType":"...","dataDimension":"...","dateType":"day","startDate":"...","endDate":"...","brandId":"3322567","indicators":["..."]}'
```

---

## 14. 相关文档

- **Agent 可识别性自检**（静态校验脚本 + 干跑清单）：**[fetch-data-config-chain-agent-checklist.md](./fetch-data-config-chain-agent-checklist.md)**
- 其它取数接口（店铺列表、报表 CRUD、下载轮询详情）：**[fetch-report-api-doc.md](./fetch-report-api-doc.md)**
