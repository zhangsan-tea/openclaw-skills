---
tags:
  - 自建skill
  - 自动化
  - 定时任务
  - cron
created: 2025-07-12
updated: 2025-07-12
status: 有效
maintainer: WorkBuddy
source: skills/automation-task-manager/
---

# automation-task-manager

> 自动化任务管理工具 — 帮助用户通过自然语言管理自动化定时任务

## 基本信息

| 属性 | 值 |
|------|-----|
| 版本 | 1.1.0 |
| 作者 | CodeBuddy AI |
| 创建日期 | 2026-04-01 |
| 最后更新 | 2026-07-06 |
| 触发关键词 | 自动化任务、定时任务、创建任务、编辑任务、删除任务、任务列表 |

## 触发条件

**何时触发**：
- 用户明确说"创建/新建定时任务"
- "帮我设置一个自动化任务"
- "某时间提醒我某件事"
- 用户要求"编辑/修改/暂停/恢复/删除某个任务"
- 用户要求"查看定时任务列表"或"查看某个任务详情"

**何时不触发**：
- 当 `CODEBUDDY_SESSION_TYPE` 为 `automation` 时（自动化调度执行中）
- 用户只是泛泛提到"任务"但并非调度管理

## 核心能力

1. **创建任务** — 支持 daily（每天）、interval（间隔）、once（单次）三种频率类型
2. **查询任务** — 列表查询（支持分页/状态/关键词过滤）、详情查询
3. **更新任务** — 修改名称、Cron、指令、状态（启用/停用）
4. **删除任务** — 删除指定任务

## 操作确认协议

对写操作（创建/编辑/删除），强制遵循 **先预览 → 后确认 → 再执行** 的三步协议：

```
用户提出需求 → 解析意图整理参数 → 展示操作预览 → 等用户确认 → 执行脚本
```

## 关键技术细节

### Cron 格式
- 6 位格式：`秒 分 时 日 月 周`
- 秒固定为 `0`，最小间隔 1 分钟
- 严禁秒级任务

### Frequency Type 识别

| 类型 | 值 | 识别特征 |
|------|-----|---------|
| 每天执行 | `daily` | 每天X点、每日、工作日、周末、每周X |
| 按间隔执行 | `interval` | 每X分钟、每X小时、每隔 |
| 单次执行 | `once` | 只执行一次、具体日期时间 |

### 默认值
- 时区：`Asia/Shanghai`
- 超时：300 秒（范围 10-1800）
- 重试：3 次（最大 10）

### Cron 速查

| 描述 | 表达式 |
|------|--------|
| 每天早上9点 | `0 0 9 * * *` |
| 每小时 | `0 0 * * * *` |
| 每30分钟 | `0 */30 * * * *` |
| 工作日每天9点 | `0 0 9 * * 1-5` |
| 每周一早上9点 | `0 0 9 * * 1` |
| 每月1号早上9点 | `0 0 9 1 * *` |

## 源码文件

```
automation-task-manager/
├── SKILL.md                       # Skill 定义
├── references/
│   └── cron_examples.md           # Cron 表达式参考
└── scripts/
    └── scheduler-api.sh           # API 调用脚本
```

## 使用示例

### 创建每天执行的任务
```bash
./scripts/scheduler-api.sh create \
  --name "每日日报提醒" \
  --cron "0 0 21 * * *" \
  --prompt "提醒用户写日报" \
  --frequency-type "daily"
```

### 创建按间隔执行的任务
```bash
./scripts/scheduler-api.sh create \
  --name "服务状态检查" \
  --cron "0 0 * * * *" \
  --prompt "检查各服务的运行状态" \
  --frequency-type "interval"
```

### 查询任务列表
```bash
./scripts/scheduler-api.sh list --status 1 --keyword "日报"
```

### 暂停/恢复任务
```bash
./scripts/scheduler-api.sh update --id 123 --status 0   # 暂停
./scripts/scheduler-api.sh update --id 123 --status 1   # 恢复
```

## 错误码

| 错误码 | 说明 |
|--------|------|
| INVALID_PARAM | 无效参数 |
| TASK_NOT_FOUND | 任务不存在 |
| TASK_LIMIT_EXCEEDED | 任务数量超限 (最多100个) |
| INVALID_CRON_EXPR | 无效的 Cron 表达式 |
