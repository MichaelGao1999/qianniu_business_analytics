# 淘系店铺经营数据分析技能（本地Excel驱动版）

> **适用范围**：仅覆盖淘系（天猫 / 淘宝 → 生意参谋）单渠道数据分析，**支持单店或多家淘系店铺合并分析（多店横向对比 + 排行）**；暂不支持京东 / 抖音 / 全渠道跨平台合并。若需万相台 / 直通车 / 店铺推广等广告投放分析，请使用 `qianniu_ad_analytics`。
>
> **v5.0.0 更新**：已改为**本地Excel驱动模式**，无需订购平台服务或API权限，直接分析生意参谋导出的Excel。

---

## 快速开始

### 1. 安装依赖

```bash
pip install pandas openpyxl
```

### 2. 准备数据

1. 登录生意参谋后台
2. 进入「店铺」或「商品」模块
3. 选择时间范围，点击「下载数据」
4. 将导出的 `.xlsx` 文件放入本项目 `data/` 目录

### 3. 生成报告

**方式一：Agent 对话触发（推荐）**

直接在对话中说出需求：

- "帮我分析上周店铺经营数据"
- "对比 XX 旗舰店和 YY 官方店上周的销售情况"
- "看看这个Excel里的数据"

Agent 会自动读取 `data/` 下的 Excel，生成四段式分析报告。

**方式二：命令行一键跑**

```bash
# 扫描 data/ 目录所有 Excel 并生成报告
python3 scripts/jycm_auto_report.py

# 指定店铺名称 + 飞书推送
python3 scripts/jycm_auto_report.py --shop "XX旗舰店" --feishu

# 指定具体文件
python3 scripts/jycm_auto_report.py data/店铺A.xlsx data/店铺B.xlsx --shop "多店合并" --feishu

# 自定义输出路径
python3 scripts/jycm_auto_report.py --output reports/自定义报告.md
```

**方式三：单独调用分析脚本**

```bash
# 单店分析
python3 scripts/analyze_excel_report.py data/XX店铺_20260401_20260407.xlsx

# 多店合并
python3 scripts/analyze_excel_report.py data/店铺A.xlsx data/店铺B.xlsx --shop "多店汇总"
```

---

## 飞书推送配置（可选）

```bash
export FEISHU_WEBHOOK='https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxxxxxxxxxx'
```

然后在运行脚本时加上 `--feishu` 参数即可自动推送。

---

## 目录结构

```
qianniu_business_analytics/
├── SKILL.md              # 技能主入口（Agent指令）
├── auth.md               # ~~旧版认证流程（已停用）~~
├── fetch-data.md         # Excel上传规则
├── fetch-data-api.md     # ~~旧版API参考（已归档）~~
├── report-analyze.md     # 报告分析与飞书推送规范
├── scripts/              # 脚本目录
│   ├── analyze_excel_report.py   # Excel分析 → Markdown报告（核心）
│   ├── jycm_auto_report.py       # 自动化全流程
│   ├── feishu_send_markdown.py   # 飞书推送
│   └── feishu_send_markdown.py   # 飞书推送
├── data/                 # 用户上传的生意参谋Excel
└── reports/              # 生成的分析报告目录
```

---

## 报告格式

所有报告统一采用**四段式结构**：

1. **整体指标**：周期汇总核心指标（访客数、支付金额、转化率等）
2. **日度趋势**：按日展示关键指标走势
3. **TOP 排行**：商品/店铺维度 TOP 10
4. **分析总结**：3~6 条基于数据的量化洞察
5. **原始数据**：列出分析所用的 Excel 文件路径

详见 `report-analyze.md`。

---

## 常见问题

### Q: 报告中的指标显示为「-」？
A: 说明脚本未能自动识别该列。请检查 Excel 列名是否为生意参谋标准导出格式，或参考 `fetch-data.md` 中的指标映射表。

### Q: 如何启用飞书推送？
A: 设置环境变量 `export FEISHU_WEBHOOK='https://open.feishu.cn/open-apis/bot/v2/hook/...'`，运行脚本时加 `--feishu`。

### Q: 本技能支持京东 / 抖音 / 全渠道吗？
A: **不支持**。本技能仅处理淘系（天猫 / 淘宝 → 生意参谋）Excel 数据。若遇到非淘系或跨平台诉求，Agent 会明确告知不在范围内。

### Q: 本技能支持同时分析多家淘系店铺吗？
A: **支持**。将多家店铺的 Excel 同时放入 `data/` 目录，或使用 `analyze_excel_report.py` 传入多个文件路径。

### Q: 为什么移除了API取数功能？
A: v5.0.0 起改为本地Excel驱动，无需平台服务订购和API权限，降低了使用门槛。旧版API取数脚本已归档后删除。

---

## 参考文档

- 技能说明：`SKILL.md`
- Excel规则：`fetch-data.md`
- 报告规范：`report-analyze.md`
- 旧版API：`fetch-data-api.md`（参考归档）
