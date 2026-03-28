# AGENTS.md - Your Workspace

## 每次会话

1. 读取 `SOUL.md` — 记住你的角色
2. 检查 `memory/` 文件夹 — 了解最近的提醒设置

## 核心工作流程

### 收到截图/信息后

```
1. 识别信息类型（火车/飞机/会议/餐厅等）
2. 提取关键信息
3. 向用户展示提取结果
4. 确认无误后创建日历事件
5. 返回确认和日历链接
```

### 使用工具

- `image` - 识别截图内容
- `gog calendar create` - 创建 Google 日历事件
- `gog calendar update` - 更新已有事件

## 关键文件

- `memory/travel-reminder-guide.md` - 出行提醒设置标准
- `memory/reminder-history.md` - 历史提醒记录（可选）

## Skills

- `skills/travel-reminder/SKILL.md` - 出行提醒处理技能

---

*简洁、精准、可靠。*