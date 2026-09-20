---
name: openclaw-migration-readonly-inventory
description: 对 OpenClaw 资产执行只读盘点，输出迁移前清单与映射风险，不做任何写入、删除、覆盖；适用于 OpenClaw ->
  WorkBuddy 迁移前的基线核查。
description_zh: OpenClaw只读盘点
description_en: OpenClaw Readonly Inventory
agent_created: true
---

# openclaw-migration-readonly-inventory

## When to use
- 用户准备从 OpenClaw 迁移到 WorkBuddy，要求先做“只读盘点”。
- 需要确认身份文件、memory、skills、MCP、渠道配置、cron 的现状与可迁移性。
- 用户要求“先备份、后迁移、源数据不删除”，并希望先拿到风险清单。

## Steps
1. 先确认用户授权只读盘点范围（是否包含渠道配置、cron）。
2. 只读检查源目录：`~/.openclaw`，列出关键资产路径是否存在。
3. 只读检查目标目录：`~/.workbuddy` 与 `~/Library/Application Support/CodeBuddy/User/settings.json`。
4. 读取以下关键文件（只读）：
   - `~/.openclaw/openclaw.json`
   - `~/.openclaw/cron/jobs*.json*`
   - `~/.openclaw/credentials/*.json`
   - `~/.workbuddy/mcp.json`
   - `~/Library/Application Support/CodeBuddy/User/settings.json`
5. 输出盘点报告：
   - 已发现资产（按类型分组）
   - 可直接映射项
   - 需要 manual review 的项
   - 明确“未执行任何写入/删除”。

## Pitfalls
- 不要把 `~/.openclaw/workspace` 作为固定路径硬编码；实际常见是 `workspace-*`。
- 不要在报告中回显敏感字段原文（token/appSecret/apiKey），只写“已检测到”。
- 不要把运行态缓存（runs/*.jsonl、sqlite-wal）当作迁移目标。
- 不要误把 OpenClaw 的整份配置直接覆盖 WorkBuddy 目标文件。
- 用户说“多渠道”时，先确认是“跨软件多渠道”还是“同一IM内多机器人按助理分流”；两者迁移策略不同。
- WorkBuddy 当前常见 `claw.channels` 结构是按 channelType 配置，若目标是同一IM内多机器人强隔离，需要先设计多实例或分层路由方案，不能直接假设1:1自动映射。

## Verification
- 报告里必须有六类资产：身份、memory、skills、MCP、channels、cron。
- 报告里必须明确“只读盘点完成，未做写入/删除”。
- 报告里必须包含下一步动作：备份打包与映射迁移。

## Related Skills
- 盘点后要把某个助理落成 WorkBuddy 专家：`openclaw-agent-to-workbuddy-expert`
- 迁移后企微新机器人不回消息：`workbuddy-wecom-writer-noresponse-fix`
- 迁移后会话历史过大、渠道报 400：`workbuddy-session-slim-archive`
- 用户只想处理 OpenClaw 本机免鉴权直连：`openclaw-local-noauth-switch`