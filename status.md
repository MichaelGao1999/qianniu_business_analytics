# 瓴羊·One 淘系店铺经营数据分析 — 项目状态看板

> 这是项目的活文档，每次会话结束后更新。新会话启动时**先读此文件**了解当前进度和待办。
> **已完成的历史追溯见 `session-log.md`**，本文件只回答"现在在哪"。

---

## 当前阶段

**阶段五（执行开发/维护迭代）约 85% 完成 | 下一步：补全 SOP 文档体系 → 持续维护与功能迭代**

---

## 进度总览

`P1 认证管理 ✅ | P1 淘系取数 ✅ | P1 报告分析 ✅ | P1 钉钉推送 ✅ | P2 自动化编排 ✅ | P2 多店合并分析 ✅ | P3 SOP 文档体系 🔄 | P3 跨平台扩展 ⚠️（明确不做）`

> 图例：✅ 已完成 | 🔄 进行中 | ⚠️ 阻塞/待修复

---

## 待办 📋

### 优先级 1 — 阻塞项
- [ ] 无当前阻塞项

### 优先级 1 — 当前进行
- [ ] **输出《代码评估报告》**（2026-05-21 执行）：评估现有 4 个 Python 脚本的架构现状、已完成模块、缺失模块、技术债务 → 决定后续是继续开发还是回溯补文档

### 优先级 2 — 功能迭代
- [ ] 支持更多 dataType / dataDimension 组合（商品/品类/内容/客户/推荐分析）
- [ ] 增加报告模板多样性（简洁版/高管版/运营版）
- [ ] Excel 分析容错增强（列名变化/空值处理）

### 优先级 3 — 优化与文档
- [x] 引入 Vibe Coding SOP 文档体系
- [ ] 补全 `docs/design.md` 架构设计文档
- [ ] 补全 `docs/brief.md` 决策摘要
- [ ] 补全 `docs/tasks/*.md` 子任务拆分
- [ ] 完善单元测试覆盖
- [ ] 代码注释与类型提示补齐

---

## 环境备忘

- **语言/框架版本**：Python 3.8+
- **依赖包**：requests，openpyxl
- **测试命令**：暂无自动化测试（待补充 pytest）
- **已知限制**：
  - Windows Git Bash 下文本文件可能触发 `LF will be replaced by CRLF` 警告
  - `requests` 未在 requirements.txt 中声明
  - 部分脚本中 `sys.path.insert` 引用了外部技能包路径，需确认是否仍然有效

---

## 关键代码入口

> 新会话接手时，若需要改代码，从这里定位文件。

```
qianniu_business_analytics/
├── scripts/
│   ├── qianniu_analytics_orchestrator.py  # 编排脚本（CLI 入口）
│   ├── jycm_auto_report.py               # 自动化全流程（定时任务入口）
│   ├── dingtalk_send_markdown.py         # 钉钉推送
│   └── jycm_fetch_sycm_shop.py           # 淘系生意参谋取数（A→G 接口链）
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

1. 先补完 SOP 文档体系中缺失的 `docs/design.md`、`docs/brief.md`、`docs/tasks/*.md`
2. 完善 Python 脚本的错误处理与日志输出
3. 补充 pytest 单元测试（认证模块、日期计算、钉钉推送模拟）

---

## 更新记录

| 日期 | 更新内容 |
|------|---------|
| 2026-05-20 | 引入 Vibe Coding SOP 文档体系；创建 AGENTS.md、status.md、session-log.md、decisions.md、troubleshooting.md、lessons-learned.md、vibe-coding-sop.md |

---

## 存档提示

**用户说「存档」时**，AI 应回顾本轮会话内容，更新本文件的以下章节：
- **当前阶段**：如有进展，更新百分比和下一步
- **进度总览**：更新各模块状态图标
- **待办**：勾选已完成项，新增下轮待办
- **更新记录**：追加本轮更新摘要
