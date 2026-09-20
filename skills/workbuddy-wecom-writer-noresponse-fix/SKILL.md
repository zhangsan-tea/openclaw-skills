---
name: workbuddy-wecom-writer-noresponse-fix
description: Diagnose and fix cases where a newly added WeCom bot (e.g. writer
  assistant) does not respond after migration from OpenClaw to WorkBuddy. Use
  this when one WeCom bot works but another bot in the same IM is silent. Focus
  on active connection registration, effective config path, and safe
  non-disruptive rollout.
description_zh: 企微新机器人无响应排查
description_en: WeCom Bot No-Response Fix
agent_created: true
---

# workbuddy-wecom-writer-noresponse-fix

## When to use
- 已有一个企微机器人可用（如数字幕僚），新加机器人（如 writer）无响应。
- 用户通过手改 settings.json 增加了账号字段，但机器人仍不回消息。
- 需要“不断当前入口”的增量排查和修复。

## Steps
1. 读取并比对两份配置：`~/.workbuddy/settings.json` 与 `~/Library/Application Support/CodeBuddy/User/settings.json`，确认实际生效入口与字段结构。
2. 在 `~/.workbuddy/logs/` 搜索新 botId，并额外搜 `WecomAiBotPlugin startAccount begin` / `status change`：若启动阶段只出现默认账号（如 `wecomaibot-aibAKSHL`）而没有新账号，说明当前真正上线的仍只有默认 bot。
3. 再看新 bot 是否有入站/出站轨迹；若日志持续只有旧 bot 的入站/出站，而新 bot 连启动记录都没有，优先判定为“未被注册/激活”，不是推理层故障。
4. 查官方 WeCom 接入文档，确认接入动作应在 WorkBuddy「设置-助理设置」中单独配置并注册，不依赖手改多账号字段。
5. 给出最小修复路径：
   - 保持现有默认 bot 不动；
   - 在 UI 里为新 bot 单独注册并确认连接状态；
   - 发“你好”做链路验证；
   - 再看日志是否出现新 botId。
6. 如用户允许短时切换测试，执行“临时切到 writer → 验证 → 切回默认 bot”的可回退测试。

## Pitfalls
- 误以为在 `wecomaibot.accounts.*` 增加账号就会自动建立第二路连接。
- 只看到 `channelId=wecomaibot` 已 connected，就误判所有 accounts 都在线；实际上日志里只启动了默认 account，也可能意味着新 bot 根本没被激活。
- 只改了配置但未在 UI 中执行“注册/连接”，导致新 bot 永远不在线。
- 企微当前常见是单入口/单槽位思路；新增 bot 很可能是“改绑当前入口”，不是天然并列多实例，排查时别默认支持多 bot 同挂。
- 忽略日志核验，无法区分“凭据错”与“根本未连上”。

## Verification
- 日志中能检索到新 botId 的入站/出站记录。
- 企微端给新 bot 发送测试消息，5-15 秒内有回复。
- 默认 bot 的原有会话不受影响（强隔离增量接入）。

## Related Skills
- 迁移前的整体分流：`openclaw-to-workbuddy-migration-router`
- 先做资产盘点：`openclaw-migration-readonly-inventory`
- 新 bot 实际可连但会话持续 400：`workbuddy-session-slim-archive`
