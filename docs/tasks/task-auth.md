# M01 认证管理 — 子任务清单

> 负责 JYCM OpenAPI Cookie 的生命周期管理：获取、缓存、刷新、验证。
> 关联文件：`auth.md`、`scripts/`（相关逻辑）、`auth/jycm.json`

---

## 已完成

- [x] A-01: 设计凭证文件格式（`auth/jycm.json` 三字段结构）
- [x] A-02: 实现首次初始化流程（Token Key → AK/SK/Cookie）
- [x] A-03: 实现缓存 Cookie 读取与校验（GET product.json）
- [x] A-04: 实现 Digest 自动刷新（POST authToken.json + Digest）
- [x] A-05: 实现刷新后回写（只更新 jycmOpenApiCookie，保留 AK/SK）
- [x] A-06: 编写 `auth.md` 完整认证流程文档（含 curl 参考）

---

## 待完成

### P1 — 高优先级
- [ ] A-07: **凭证文件权限强制 `chmod 600`**
  - 测试点：文件创建后权限为 `-rw-------`
  - 验收：Linux/Mac 下 `ls -l auth/jycm.json` 显示 `600`

- [ ] A-08: **增加结构化日志持久化**
  - 测试点：认证操作（初始化/刷新/失败）记录到日志文件
  - 验收：`logs/auth.log` 存在且包含时间戳、操作类型、结果

### P2 — 功能增强
- [ ] A-09: 增加凭证加密存储（可选，base64 或简单加密）
  - 测试点：明文 AK/SK 不在文件系统直接可读
  - 验收：文件内容非明文 JSON，解密后结构正确

- [ ] A-10: 增加凭证备份机制（刷新前备份旧 Cookie）
  - 测试点：刷新失败时可回滚到上一个有效 Cookie
  - 验收：`auth/jycm.json.bak` 存在且可恢复

---

## 依赖关系

```
A-01 → A-02 → A-03 → A-04 → A-05
                  ↓
                A-07（依赖 A-03 的文件写入）
                A-08（依赖 A-04 的刷新逻辑）
```

---

*模块状态：🔄 维护中 | 完成：6/10*
