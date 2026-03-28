# 龙虾健康管理系统

> 基于 OpenClaw（龙虾）构建的个人健康管理方案

---

## 📋 系统概览

这是一个由 AI Agent 驱动的个人健康管理系统，核心能力包括：

| 功能 | 说明 |
|------|------|
| 📊 健康数据追踪 | Apple Health 自动导出 + 周度分析报告 |
| 💊 药品管理 | 过期检查、用药提醒、药品清单维护 |
| 🏃 运动提醒 | 睡前运动打卡、工作间歇活动提醒 |
| 🩺 健康顾问 | 个性化健康建议、康复指导、症状跟踪 |

---

## 🧠 设计理念

> 详见 [health-advisor-skill-extraction](./health-advisor-skill-extraction/)

### 核心原则

1. **我是教练，不是医生**
   - 不诊断、不开药方
   - 提供基于常识的健康建议和生活方式指导

2. **关注长期习惯，而非短期效果**
   - 鼓励进步，认可努力
   - 帮助用户看到坚持的价值

3. **系统性健康视角**
   - 从身体、心理、情绪、生活方式等多维度综合考虑
   - 识别风险因素的相互关联

4. **个性化适配**
   - 根据用户的具体情况调整建议
   - 在用户能力范围内提供最适合的方案

---

## 🔧 技术实现

> 详见 [health-automation](./health-automation/)

### 系统架构

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Apple Watch   │───▶│  Apple Health   │───▶│  Google Drive   │
│   iPhone        │    │  (Health Auto   │    │  (JSON 文件)    │
│                 │    │   Export App)   │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                      │
                                                      ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   定时提醒      │◀───│   OpenClaw      │◀───│   gog CLI       │
│   (Cron Jobs)   │    │   健康顾问      │    │   (Google API)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
        │
        ▼
┌─────────────────┐
│   Telegram      │
│   (消息推送)     │
└─────────────────┘
```

### 前置条件

| 项目 | 要求 | 说明 |
|------|------|------|
| iPhone | iOS 14+ | 安装 Health Auto Export App |
| Apple Watch | 可选 | 提供更完整的健康数据 |
| Google 账号 | 必需 | 用于数据存储 |
| OpenClaw | 已安装 | 运行自动化脚本 |
| Telegram | 可选 | 接收提醒和报告 |

---

## 📱 核心功能

### 1. 每周健康分析报告

**触发时间**：每周日 21:00

**分析内容**：
- 睡眠分析（时长、深睡、REM、入睡时间）
- 心血管健康（心率、HRV、血氧）
- 运动与活动（步数、锻炼时长、爬楼）
- 趋势对比（本周 vs 上周）

**示例报告**：

```markdown
# 本周健康分析报告

**周期**: 2026-03-22 至 2026-03-28

## 📊 核心指标概览

| 指标 | 本周平均 | 参考范围 | 评价 |
|-----|---------|---------|-----|
| 睡眠时长 | 6.2 小时 | 7-9 小时 | ⚠️ 偏少 |
| 静息心率 | 71 bpm | 60-100 bpm | ✅ 正常 |
| HRV | 35 ms | 20-100 ms | ✅ 正常 |
| 日均步数 | 8,542 步 | 8,000-10,000 步 | ✅ 良好 |

## 💡 本周建议

1. **睡眠优先** — 尝试提前 30 分钟入睡
2. **继续保持** — 运动习惯良好，继续保持
```

### 2. 睡前运动提醒

**触发时间**：每晚 22:00

**提醒内容**：
- 放松拉伸动作
- 核心激活练习
- 助眠抗阻训练
- 一键打卡功能

### 3. 药品定期检查

**触发时间**：每周日 9:00

**检查内容**：
- 已过期的药品清单
- 未来 7 天内到期的药品
- 用药记录维护

---

## 🚀 快速上手

### Step 1: 安装必要工具

```bash
# 安装 OpenClaw
brew install openclaw

# 安装 gog (Google CLI)
brew install steipete/tap/gogcli

# 配置 Google 授权
gog auth add YOUR_EMAIL@gmail.com
```

### Step 2: 配置 Health Auto Export

1. 在 iPhone 上下载 **Health Auto Export** App
2. 授权访问 Apple Health 数据
3. 配置自动导出到 Google Drive
4. 设置导出频率：每周日

### Step 3: 启用 Skills

将以下 Skills 放入 OpenClaw 的 skills 目录：

```bash
~/.openclaw/skills/
├── health-automation/        # 技术实现
├── health-advisor-skill-extraction/  # 方法论
├── medication-management/    # 药品管理
└── calendar-reminder/        # 日程提醒
```

### Step 4: 配置定时任务

```bash
# 每周健康报告
openclaw cron add --job health-weekly-report.json

# 睡前运动提醒
openclaw cron add --job bedtime-exercise.json

# 药品检查
openclaw cron add --job medication-check.json
```

---

## 📁 文件结构

```
~/.openclaw/workspace-health-advisor/
├── AGENTS.md                    # Agent 配置
├── SOUL.md                      # 角色定义
├── USER.md                      # 用户健康档案
├── memory/
│   ├── reminder_config.md       # 定时提醒配置
│   ├── exercise_tracker.md      # 运动打卡记录
│   ├── medications_log.md       # 用药记录
│   └── weekly_health/           # 周度健康报告
│       └── 2026-W12.md
└── medications/
    └── medications.csv          # 药品清单
```

---

## 💡 使用建议

### 日常操作

| 时间 | 操作 |
|------|------|
| 每天 22:00 | 收到睡前运动提醒，点击打卡 |
| 每周日 9:00 | 收到药品检查报告 |
| 每周日 21:00 | 收到健康分析报告 |

### 随时可做

- 询问健康问题：「我最近睡眠不好怎么办？」
- 记录身体状况：「今天腰有点疼」
- 查询健康趋势：「我最近心率怎么样？」
- 更新药品信息：「我买了新的维生素」

---

## ⚠️ 注意事项

### 医疗免责声明

本系统提供的健康分析和建议**仅供参考**，不能替代专业医疗建议。如有健康问题，请咨询医生或专业医疗机构。

### 数据隐私

- 健康数据存储在个人 Google Drive
- 仅授权用户本人访问
- 建议定期备份重要数据

---

## 📦 相关 Skills

| Skill | 说明 |
|-------|------|
| [health-automation](./health-automation/) | 技术实现文档 |
| [health-advisor-skill-extraction](./health-advisor-skill-extraction/) | 方法论与最佳实践 |
| [medication-management](./medication-management/) | 药品管理系统 |
| [calendar-reminder](./calendar-reminder/) | 日程提醒助手 |

---

## 🔄 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v1.0 | 2026-03-28 | 初始版本 |

---

## 📮 联系方式

如有问题或建议，欢迎联系：Lee

---

*让健康管理变得简单、持续、有效。*