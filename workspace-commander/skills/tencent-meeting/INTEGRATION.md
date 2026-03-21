# 腾讯会议 Skill 集成指南

## 方案一：为现有Agent添加Skill

如果你希望现有的writer agent能够使用腾讯会议功能，可以将此skill添加到writer的工作目录中：

```bash
cp -r /Users/lee/clawd-commander/skills/tencent-meeting /Users/lee/clawd-writer/skills/
```

## 方案二：创建专用的Evolver Agent

根据你的角色（系统进化官），建议创建专门的evolver agent来管理各种skills：

### 1. 更新 ~/.clawdbot/clawdbot.json

在agents.list中添加evolver agent：

```json
{
  "id": "evolver",
  "name": "Evolver (系统进化官)",
  "workspace": "/Users/lee/clawd-evolver",
  "model": {
    "primary": "moonshot/kimi-k2-0905-preview"
  }
}
```

### 2. 添加Telegram绑定

在bindings中添加：

```json
{
  "agentId": "evolver",
  "match": {
    "channel": "telegram",
    "accountId": "evolver"
  }
}
```

### 3. 添加Telegram账户配置

在channels.telegram.accounts中添加：

```json
"evolver": {
  "name": "Lee Evolver",
  "dmPolicy": "open",
  "botToken": "YOUR_BOT_TOKEN",
  "groupPolicy": "allowlist",
  "streamMode": "partial",
  "allowFrom": ["*"]
}
```

## 方案三：全局Skill目录

OpenClaw可能支持全局skill目录。将skill放在以下位置：

```
/Users/lee/.openclaw/skills/tencent-meeting/
```

这样所有agents都可以访问这个skill。

## Token配置

无论选择哪种方案，都需要配置腾讯会议Token：

### 环境变量方式
```bash
export TENCENT_MEETING_TOKEN="your_token_here"
```

### 配置文件方式
在skill目录下创建 `.env` 文件：
```
TENCENT_MEETING_TOKEN=your_token_here
```

## 测试集成

集成完成后，可以通过以下方式测试：

1. 重启OpenClaw服务
2. 在Telegram中向对应的bot发送消息："帮我预订一个腾讯会议"
3. 检查是否能正确调用腾讯会议API

## 故障排除

- **Token无效**: 重新获取Token并更新配置
- **权限错误**: 确认腾讯会议账号有相应的API权限
- **网络问题**: 检查网络连接和防火墙设置
- **Skill未加载**: 确认skill目录结构正确，包含SKILL.md文件