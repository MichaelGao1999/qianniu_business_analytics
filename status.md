# 淘系店铺经营数据分析 — 项目状态看板

> 这是项目的活文档，每次会话结束后更新。新会话启动时**先读此文件**了解当前进度和待办。
> **已完成的历史追溯见 `session-log.md`**，本文件只回答"现在在哪"。

---

## 当前阶段

**阶段五（执行开发/维护迭代）约 95% 完成 | 下一步：补全 docs/ 架构设计文档 → 持续维护与功能迭代**

---

## 进度总览

`P1 认证管理 ✅ | P1 淘系取数 ✅ | P1 报告分析 ✅ | P1 钉钉/飞书推送 ✅ | P2 自动化编排 ✅ | P2 多店合并分析 ✅ | P3 单元测试 ✅ | P3 SOP 文档体系 🔄 | P3 跨平台扩展 ⚠️（明确不做）`

> 图例：✅ 已完成 | 🔄 进行中 | ⚠️ 阻塞/待修复

---

## 待办 📋

### 优先级 1 — 阻塞项
- [ ] 无当前阻塞项

### 优先级 1 — 当前进行
- [x] **输出《代码评估报告》**（2026-05-22 完成）：评估 6 个 Python 脚本，确定聚焦 Excel 驱动流
- [x] **巩固 Excel 驱动流**（2026-05-22 完成）：常量抽取、subprocess→import、多店合并分析、单元测试、空壳脚本归档

### 优先级 2 — 功能迭代
- [ ] 支持更多 dataType / dataDimension 组合（商品/品类/内容/客户/推荐分析）
- [ ] 增加报告模板多样性（简洁版/高管版/运营版）
- [ ] Excel 分析容错增强（列名变化/空值处理）

### 优先级 3 — 优化与文档
- [x] 引入 Vibe Coding SOP 文档体系
- [x] 完善单元测试覆盖（33 条用例全部通过）
- [x] 补全 `docs/proposal.md` 需求提案
- [ ] 补全 `docs/design.md` 架构设计文档
- [ ] 补全 `docs/brief.md` 决策摘要
- [ ] 补全 `docs/tasks/*.md` 子任务拆分
- [ ] 生成 `prompt.md`（阶段四产出）← **用户提醒：后续需补**
- [ ] 代码注释与类型提示补齐

---

## 环境备忘

- **语言/框架版本**：Python 3.8+
- **依赖包**：pandas，openpyxl，requests，pytest
- **测试命令**：`python -m pytest tests/ -v`（33 条用例）
- **已知限制**：
  - Windows Git Bash 下文本文件可能触发 `LF will be replaced by CRLF` 警告
  - Windows Git Bash 下 emoji 输出可能触发 `UnicodeEncodeError`，需设置 `PYTHONIOENCODING=utf-8`

---

## 关键代码入口

> 新会话接手时，若需要改代码，从这里定位文件。

```
qianniu_business_analytics/
├── scripts/
│   ├── analyze_excel_report.py           # Excel 分析 → Markdown 报告（核心）
│   ├── jycm_auto_report.py               # 自动化全流程（扫描 → 分析 → 推送）
│   ├── dingtalk_send_markdown.py         # 钉钉推送
│   ├── feishu_send_markdown.py           # 飞书推送
│   ├── constants.py                      # 公共常量（时区/指标关键词/阈值）
│   ├── qianniu_analytics_orchestrator.py # 【已归档】API 驱动编排占位代码
│   └── jycm_fetch_sycm_shop.py           # 【已归档】旧版 API 取数（A→G 接口链）
├── auth/                                  # 凭证目录（auth/jycm.json）
├── data/                                  # 原始数据目录（Excel 下载）
└── reports/                               # 分析报告目录（Markdown）
```

---

## 核心规则（不可违反）

见 `AGENTS.md` 完整版。关键几条：
- **RULE-01**：禁止生成模拟数据，API 失败如实告知
- **RULE-02**：时间强制 `T00:00:00+08:00`，禁 `23:59:59`
- **RULE-04**：Token Key 只问一次，Cookie 过期走 Digest 刷新
- **RULE-05**：仅淘系生意参谋，非淘系明确拒绝

---

## 推荐策略

1. 补全 `docs/design.md` 架构设计文档（以代码评估报告为蓝本）
2. 补全 `docs/brief.md` 决策摘要
3. 补全 `docs/tasks/*.md` 子任务拆分
4. 完善 Python 脚本的错误处理与日志输出

---

## 更新记录

| 日期 | 更新内容 |
|------|---------|
| 2026-05-20 | 引入 Vibe Coding SOP 文档体系；创建 AGENTS.md、status.md、session-log.md、decisions.md、troubleshooting.md、lessons-learned.md、vibe-coding-sop.md |
| 2026-05-22 | 输出代码评估报告；巩固 Excel 驱动流：抽取 constants.py、修复 subprocess→import、完善多店合并分析、补充 33 条 pytest 用例、归档空壳脚本 |

---

## 存档提示

**用户说「存档」时**，AI 应回顾本轮会话内容，更新本文件的以下章节：
- **当前阶段**：如有进展，更新百分比和下一步
- **进度总览**：更新各模块状态图标
- **待办**：勾选已完成项，新增下轮待办
- **更新记录**：追加本轮更新摘要
