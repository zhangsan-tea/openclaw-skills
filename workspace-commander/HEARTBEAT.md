# HEARTBEAT.md - 定期检查任务

*每次 heartbeat 时检查以下任务，按优先级执行。*

---

## 每日检查（2-4次/天）

### 1. 系统健康
- [ ] 检查 OpenClaw 服务状态：`openclaw status`
- [ ] 如有异常，主动报告给 Lee

### 2. 记忆维护
- [ ] 检查 memory/YYYY-MM-DD.md 是否需要更新
- [ ] 重要经验写入 MEMORY.md

---

## 每周检查（1-2次/周）

### 1. Memory 整理
- [ ] 回顾本周 memory/*.md 文件
- [ ] 提取值得长期记住的经验到 MEMORY.md
- [ ] 清理过时信息

### 2. Skills 审视
- [ ] 是否有新 Skills 值得安装？
- [ ] 是否有 Skills 需要更新？

---

## 触发条件

- 收到 heartbeat poll 时执行

---

*保持简洁。做完就汇报，没做就说 HEARTBEAT_OK。*
