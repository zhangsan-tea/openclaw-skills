---
name: health-automation
description: 健康数据自动化管理。当用户需要设置 Apple Health 数据自动导出、Google Drive 同步、每周健康分析报告、睡前运动提醒、药品检查等健康管理功能时使用。
---

# 健康数据自动化管理 Skill

## 功能概述

本 skill 提供完整的个人健康数据自动化管理方案，包括：

1. **Apple Health 数据自动导出** - 通过 Health Auto Export App + Google Drive
2. **每周健康分析报告** - 自动抓取、分析、生成报告
3. **睡前运动提醒** - 每晚 22:00 提醒 + 打卡互动
4. **药品定期检查** - 每周日检查过期药品
5. **综合健康追踪** - 整合多源数据（Apple Health、运动打卡、手动输入）

---

## 前置条件

### 硬件/软件要求

| 项目 | 要求 | 说明 |
|-----|------|------|
| iPhone | iOS 14+ | 安装 Health Auto Export App |
| Apple Watch | 可选 | 提供更完整的健康数据 |
| Google 账号 | 必需 | 用于数据存储 |
| OpenClaw | 已安装 | 运行自动化脚本 |
| gog 工具 | 已配置 | 访问 Google Drive |

### 需要安装的 App

**Health Auto Export**（iOS App）
- App Store 下载
- 用于从 Apple Health 导出数据
- 支持自动导出到 Google Drive

---

## 配置流程

### 第 1 步：配置 Health Auto Export

1. 打开 Health Auto Export App
2. 授权访问 Apple Health 数据
3. 选择导出格式：JSON
4. 选择健康指标：全选

### 第 2 步：配置 Google Drive 导出

1. 在 App 中选择"自动化流程"
2. 添加 Google Drive 为目标
3. 授权访问 Google Drive
4. 设置保存文件夹：`apple health weekly`
5. 设置导出频率：每周日

### 第 3 步：配置 OpenClaw 定时任务

创建以下 cron job：

```json
{
  "name": "健康顾问 - 每周健康数据抓取",
  "schedule": {
    "kind": "cron",
    "expr": "0 21 * * 0",
    "tz": "Asia/Shanghai"
  },
  "payload": {
    "kind": "agentTurn",
    "message": "你是健康顾问。请执行以下任务：\n\n1. 从 Google Drive 的 `apple health weekly` 文件夹读取最新的健康数据文件\n2. 分析数据（睡眠、心率、HRV、步数、运动等）\n3. 生成周度健康分析报告\n4. 整合本周运动打卡记录\n5. 发送完整报告给用户",
    "model": "coding-plan/glm-5"
  },
  "sessionTarget": "isolated",
  "delivery": {
    "mode": "announce",
    "channel": "telegram",
    "to": "USER_ID"
  }
}
```

### 第 4 步：配置 gog 访问 Google Drive

```bash
gog auth add USER_EMAIL@gmail.com
```

授权范围包括：
- Google Drive（读写）
- 其他 Google 服务（可选）

---

## 核心功能

### 1. 每周健康分析报告

**触发时间**：每周日 21:00

**分析内容**：
- 睡眠分析（时长、深睡、REM、入睡时间）
- 心血管健康（心率、HRV、血氧）
- 运动与活动（步数、锻炼时长、爬楼）
- 其他指标（呼吸频率、体温等）

**输出格式**：

```markdown
# 本周健康分析报告

**周期**: 2026-03-15 至 2026-03-22

## 📊 核心指标概览

| 指标 | 本周平均 | 参考范围 | 评价 |
|-----|---------|---------|-----|
| 睡眠时长 | 5.7 小时 | 7-9 小时 | ⚠️ 偏少 |
| 静息心率 | 73 bpm | 60-100 bpm | ✅ 正常 |
| HRV | 31 ms | 20-100 ms | ⚠️ 偏低 |
| 日均步数 | 9,381 步 | 8,000-10,000 步 | ✅ 良好 |

## 💡 本周建议

1. 睡眠优先 — 从 5.7h → 6.5-7h
2. 提前入睡 — 从 00:44 → 00:00
3. 继续正念 — 对提升 HRV 有帮助
```

### 2. 睡前运动提醒

**触发时间**：每晚 22:00

**提醒内容**：
```
🌙 睡前运动时间到！

【放松拉伸】
1️⃣ 婴儿式放松 — 60-90 秒

【核心激活】
2️⃣ 臀桥 — 10-15 次
3️⃣ 鸟狗式 — 每边 5-8 次
4️⃣ 死虫式 — 8-10 次

【助眠抗阻】
5️⃣ 提踵 — 20-30 次
6️⃣ 深蹲 — 10-15 次
7️⃣ 高抬腿 — 各 10 次

⏱️ 总时长约 10 分钟
```

**互动按钮**：
- ✅ 已完成
- ⏭️ 今天跳过
- ❓ 查看动作

### 3. 药品定期检查

**触发时间**：每周日 9:00

**检查内容**：
- 已过期的药品
- 未来 7 天内到期的药品

**输出格式**：
```
💊 每周药品检查报告

【已过期的药品】
❌ 美愈伪麻口服溶液 — 过期约 1 年

【未来 7 天内到期】
✅ 无

👇 请确认过期药品处理情况

[✅ 已全部处理] [⏳ 部分处理] [❌ 还未处理]
```

---

## 数据源整合

| 数据源 | 内容 | 频率 |
|-------|------|------|
| Apple Health | 睡眠、心率、HRV、步数 | 每周 |
| 睡前运动打卡 | 完成情况 | 每天 |
| 手动输入 | 身体不适、用药、感受 | 随时 |
| 药品管理 | 过期检查、用药记录 | 每周 |

---

## 文件结构

```
workspace-health-advisor/
├── memory/
│   ├── reminder_config.md          # 定时提醒配置
│   ├── exercise_tracker.md         # 运动打卡记录
│   ├── bedtime_exercise.md         # 睡前运动指南
│   ├── medications_log.md          # 用药记录
│   ├── weekly_health/              # 周度健康报告
│   │   └── 2026-W12.md
│   └── daily_health/               # 每日健康记录
│       └── 2026-03-22.md
├── medications/
│   └── medications.csv             # 药品清单
└── USER.md                         # 用户健康档案
```

---

## 使用说明

### 用户日常操作

**每天**：
- 22:00 收到睡前运动提醒
- 点击按钮打卡

**每周**：
- 周日 20:00 提醒导出 Apple Health 数据（如未配置自动导出）
- 周日 21:00 收到健康分析报告
- 周日 9:00 收到药品检查报告

**随时**：
- 可以手动输入身体不适、用药情况
- 可以查询健康数据趋势

### 管理员配置

**初始化配置**：
```bash
# 1. 配置 Google Drive 访问
gog auth add USER_EMAIL@gmail.com

# 2. 创建定时任务
cron add --job health-weekly-report.json

# 3. 测试 Google Drive 访问
gog drive search "apple health weekly"
```

**定期检查**：
- 检查 cron job 运行状态
- 检查 Google Drive 文件是否正常上传
- 检查健康报告生成是否正常

---

## 故障排查

### 问题：Google Drive 无法访问

**原因**：API 未启用或授权过期

**解决**：
1. 访问 https://console.developers.google.com/apis/api/drive.googleapis.com
2. 启用 Google Drive API
3. 重新授权：`gog auth add USER_EMAIL@gmail.com`

### 问题：健康数据文件未更新

**原因**：Health Auto Export 未自动导出

**解决**：
1. 检查 App 是否运行正常
2. 检查网络连接
3. 手动触发一次导出测试

### 问题：定时任务未执行

**原因**：cron job 配置错误或 Gateway 未运行

**解决**：
1. 检查 cron job 状态：`cron list`
2. 检查 Gateway 运行状态
3. 重新创建 cron job

---

## 扩展功能

### 可添加的功能

1. **每日数据追踪** - 每天导出并分析
2. **健康目标设定** - 设定并追踪健康目标
3. **异常预警** - 检测到异常数据时提醒
4. **趋势分析** - 月度、季度趋势对比
5. **医生建议整合** - 整合体检报告建议

### 与其他工具集成

- **Obsidian** - 同步健康日记到知识库
- **Notion** - 创建健康仪表板
- **Telegram Bot** - 通过 bot 命令查询健康数据

---

## 注意事项

### 隐私保护

- 健康数据存储在个人 Google Drive
- 仅授权代理人访问
- 定期备份重要数据

### 数据准确性

- Apple Health 数据依赖设备佩戴
- 睡眠数据可能有不完整的情况
- 手动输入可补充自动数据不足

### 医疗免责声明

本工具提供的健康分析仅供参考，不能替代专业医疗建议。如有健康问题，请咨询医生或专业医疗机构。

---

## 相关文件

- `memory/reminder_config.md` - 定时提醒配置
- `memory/exercise_tracker.md` - 运动打卡记录
- `medications/medications.csv` - 药品清单
- `USER.md` - 用户健康档案

---

## 版本历史

- **v1.0** (2026-03-22) - 初始版本
  - Apple Health 每周自动导出
  - Google Drive 同步
  - 每周健康分析报告
  - 睡前运动提醒
  - 药品定期检查
