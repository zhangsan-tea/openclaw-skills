# 药品管理系统

> 💊 家庭药品智能管理 - 自动检查过期药品，用药安全无忧

**版本**: v1.0  
**最后更新**: 2026-03-22

---

## 🎯 功能特点

- ✅ **每周自动检查** - 周日上午 9 点自动检查过期药品
- ✅ **Telegram 提醒** - 通过 Telegram 发送检查报告
- ✅ **一键确认** - 点击按钮即可确认处理情况
- ✅ **多模型备份** - 主模型失败自动切换备用模型
- ✅ **数据备份** - 自动备份药品数据到 Google Drive
- ✅ **简单易用** - 小白用户 5 分钟上手

---

## 🚀 快速开始

### 安装

```bash
cd /Users/lee/.openclaw/skills/medication-management
bash scripts/install.sh
```

### 使用

在 Telegram 中：

```
添加药品 - 布洛芬，保质期 2028-06-30
```

### 检查

等待每周日 09:00 自动检查报告。

---

## 📁 目录结构

```
medication-management/
├── SKILL.md                      # 技能文档（完整说明）
├── README.md                     # 本文件（快速开始）
├── docs/
│   ├── INSTALL_GUIDE.md          # 安装指南（小白版）
│   ├── USER_MANUAL.md            # 用户手册（简化版）
│   └── FAQ.md                    # 常见问题
├── scripts/
│   ├── install.sh                # 安装脚本
│   ├── check_status.sh           # 状态检查
│   └── backup.sh                 # 备份脚本
└── references/
    └── config_examples.json      # 配置文件示例
```

---

## 💡 常用操作

### 添加药品

```
添加药品 - 布洛芬，保质期 2028-06-30
```

### 查看清单

```
查看药品清单
```

### 查询药品

```
感冒药有哪些？
```

### 删除药品

```
删除 med_001
```

---

## 🔧 维护命令

### 检查状态

```bash
bash scripts/check_status.sh
```

### 手动检查

```bash
cron run --job-id <JOB_ID>
```

### 备份数据

```bash
bash scripts/backup.sh
```

---

## 📖 文档

| 文档 | 用途 | 适合人群 |
|-----|------|---------|
| [README.md](README.md) | 快速开始 | 所有用户 |
| [docs/INSTALL_GUIDE.md](docs/INSTALL_GUIDE.md) | 详细安装步骤 | 新用户 |
| [docs/USER_MANUAL.md](docs/USER_MANUAL.md) | 日常使用指南 | 所有用户 |
| [docs/FAQ.md](docs/FAQ.md) | 问题解决 | 遇到问题时 |
| [SKILL.md](SKILL.md) | 完整技术文档 | 开发者/高级用户 |

---

## ❓ 常见问题

### Q: 没有收到每周提醒？

**A**: 运行 `bash scripts/check_status.sh` 检查系统状态。

### Q: 药品信息错了？

**A**: 发送 `更新 med_001 的保质期为 2028-01-01`。

### Q: 误删了药品？

**A**: 从备份恢复 `cp medications/backups/medications_backup_*.csv medications/medications.csv`。

更多问题查看 [FAQ.md](docs/FAQ.md)。

---

## 🛡️ 鲁棒性设计

### 多模型切换

```
主模型：coding-plan/glm-5
  ↓ 失败
备用 1: ollama/qwen3:8b（本地）
  ↓ 失败
备用 2: coding-plan/qwen3-max
  ↓ 失败
请求用户帮助
```

### 自动备份

- 每天自动备份 CSV 文件
- 备份到 Google Drive
- 保留最近 30 天备份

### 错误处理

- 超时自动重试（3 次）
- 模型失败自动切换
- 关键操作需要确认

---

## 📊 系统要求

| 项目 | 要求 |
|-----|------|
| OpenClaw | 已安装 |
| Google 账号 | 必需 |
| Telegram | 必需 |
| 存储空间 | 至少 100MB |

---

## 🔐 隐私与安全

- 数据存储在个人 Google Drive
- 仅授权代理人访问
- 定期备份重要数据
- 不分享给第三方

---

## ⚠️ 医疗免责

> 本系统提供的药品管理功能仅供参考，不能替代专业医疗建议。用药请遵医嘱，如有健康问题，请咨询医生或药师。

---

## 📞 获取帮助

1. **自助排查**: `bash scripts/check_status.sh`
2. **查看文档**: [docs/](docs/) 目录
3. **查看日志**: `cat memory/medication_log.md`
4. **提交问题**: GitHub Issues

---

## 🎉 开始使用

```bash
# 1. 安装
bash scripts/install.sh

# 2. 录入药品
添加药品 - 布洛芬，保质期 2028-06-30

# 3. 等待每周检查
# 每周日 09:00 自动发送报告
```

**祝你用药安全，身体健康！** 💪

---

**许可**: MIT  
**作者**: Health Advisor Team  
**联系**: GitHub Issues
