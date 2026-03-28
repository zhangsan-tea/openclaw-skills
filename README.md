# OpenClaw Skills 合集

> 可复用的 AI Agent 技能模块，按需安装，即插即用。

---

## 🚀 快速开始

```bash
# 一键安装健康管理系列（推荐新手）
curl -sSL https://raw.githubusercontent.com/zhangsan-tea/openclaw-skills/main/install-health.sh | bash

# 或手动安装
cd ~/.openclaw/skills
git clone --depth 1 https://github.com/zhangsan-tea/openclaw-skills.git temp
cp -r temp/medication-management .   # 药品管理
cp -r temp/calendar-reminder .       # 日程提醒
rm -rf temp
```

---

## 📦 模块列表

### 🏥 健康管理系列

> [详细介绍](./README-个人健康管理系统.md)

| 模块 | 功能 | 难度 |
|------|------|------|
| [健康顾问理念](./health-advisor-skill-extraction/) | 方法论与思维框架 | ⭐ |
| [药品管理](./medication-management/) | 药品清单、过期检查、用药提醒 | ⭐⭐ |
| [日程提醒](./calendar-reminder/) | 截图→日历提醒 | ⭐ |
| [健康数据自动化](./health-automation/) | Apple Health 导出、周报 | ⭐⭐⭐ |

### 🎙️ 音频处理系列

| 模块 | 功能 |
|------|------|
| [音频识别](./audio-understanding/) | 听歌识曲、情感分析、语音理解 |
| [语音分析](./voice-analysis/) | 语音特征提取、情绪推断 |

### 📄 文档处理系列

| 模块 | 功能 |
|------|------|
| [PPT转文本](./ppt-to-text/) | PPT 内容提取为文本 |

### 📊 工作汇报系列

| 模块 | 功能 |
|------|------|
| [双月会材料提炼](./2month-report/) | 从周报提炼跨团队共享材料 |

---

## 🎯 按需选择

### 我是新手，想快速体验
→ 安装 **日程提醒** + **健康顾问理念**

```bash
cd ~/.openclaw/skills
git clone --depth 1 https://github.com/zhangsan-tea/openclaw-skills.git temp
cp -r temp/calendar-reminder .
cp -r temp/health-advisor-skill-extraction .
rm -rf temp
```

### 我有家庭药箱需要管理
→ 安装 **药品管理**

### 我有 iPhone + Apple Watch
→ 安装 **健康数据自动化**（需要配置 Google Drive）

### 我想做双月会汇报
→ 安装 **双月会材料提炼**

---

## 📖 详细文档

- [个人健康管理系统介绍](./README-个人健康管理系统.md)
- 各模块目录下有 `SKILL.md` 说明文档

---

## ⚠️ 注意事项

- **不提交敏感信息**：API Key、Token 等存放在本地，不要提交到 Git
- **按需安装**：不需要全部安装，选择适合你的模块
- **医疗免责声明**：健康管理功能仅供参考，不能替代专业医疗建议

---

## 📮 反馈

- 问题或建议：欢迎提 Issue
- GitHub：https://github.com/zhangsan-tea/openclaw-skills

---

*简单、模块化、按需选择。*