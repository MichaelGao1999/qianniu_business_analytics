# M05 自动化编排 — 子任务清单

> 负责 CLI 入口、定时任务支持、全流程自动化编排。
> 关联文件：`scripts/jycm_auto_report.py`

---

## 已完成

- [x] O-01: 实现 `jycm_auto_report.py` CLI 参数解析（--days, --start, --end, --shops, --dingtalk）
- [x] O-02: 实现日期范围自动计算（默认上周自然周）
- [x] O-03: 实现全流程编排调用（取数→分析→推送）
- [x] O-04: ~~实现 `qianniu_analytics_orchestrator.py` 类编排接口~~（2026-06-25 该脚本已删除，此任务完成供历史参考）

---

## 待完成

### P1 — 高优先级
- [ ] O-05: **修复 `sys.path` 外部路径依赖**
  - 问题：`jycm_auto_report.py` 第 31 行 `sys.path.insert` 引用外部技能包 `jycm-fetch-report-nl`
  - 测试点：在独立工作目录下运行脚本不报错
  - 验收：删除或替换外部路径依赖，改为本技能包内部模块引用

- [ ] O-06: **补充 `requirements.txt`**
  - 测试点：新环境中 `pip install -r requirements.txt` 后所有脚本可运行
  - 验收：包含 `requests`、`openpyxl` 及版本号

### P2 — 功能增强
- [ ] O-07: **统一日期计算工具函数**
  - 问题：多处重复实现"上周"、"近 N 天"逻辑
  - 测试点：所有日期计算通过统一函数完成
  - 验收：新建 `scripts/utils/date_utils.py`，各脚本统一导入

- [ ] O-08: 增加 Cron 定时任务配置模板
  - 测试点：提供 crontab 示例，用户可直接复制使用
  - 验收：`README.md` 或 `docs/cron-setup.md` 中包含完整配置

- [ ] O-09: 增加配置文件驱动模式（YAML/JSON 配置替代命令行参数）
  - 测试点：`config.json` 中定义默认店铺、默认数据类型、Webhook
  - 验收：`--config` 参数支持读取配置文件

- [ ] O-10: 增加执行结果通知（推送失败时邮件/钉钉告警）
  - 测试点：流程失败时发送告警消息
  - 验收：异常捕获后发送带错误摘要的钉钉消息

---

## 依赖关系

```
O-01, O-02, O-03 → O-04
O-05（修复外部依赖）→ O-06（requirements.txt 依赖内部模块）
O-07（日期工具）→ O-01, O-02, O-03（替换分散的日期计算）
```

---

*模块状态：🔄 维护中 | 完成：4/8（1 个阻塞项：O-05）*
