---
name: openclaw-to-workbuddy-migration-router
description: Router skill for OpenClaw to WorkBuddy migration and follow-up
  troubleshooting. Use when the user mentions migration, backup-first transfer,
  turning agents into experts, post-migration channel issues, or oversized
  WorkBuddy sessions, and you need to decide which specialized migration skill
  to invoke first.
description_zh: OpenClaw迁移路由
description_en: OpenClaw Migration Router
agent_created: true
---

# openclaw-to-workbuddy-migration-router

## When to use
- 用户提到 OpenClaw → WorkBuddy 迁移，但还没明确是“先盘点”“转专家”“修渠道”还是“修会话故障”。
- 用户强调“先备份、不覆盖、别把现有 WorkBuddy 数据冲掉”，需要先做动作分流。
- 同一轮请求里同时混着迁移、渠道接入、无响应排查、会话 400 等后续问题，需要先拆路由。

## Steps
1. 先识别用户当前阶段：
   - **只读盘点/迁移前摸底** → 调 `openclaw-migration-readonly-inventory`
   - **把单个 OpenClaw 助理做成 WorkBuddy 专家** → 调 `openclaw-agent-to-workbuddy-expert`
   - **新接的企微机器人不回消息** → 调 `workbuddy-wecom-writer-noresponse-fix`
   - **WorkBuddy 某条会话过大、UI 卡死、企微报 400 invalid parameter value** → 调 `workbuddy-session-slim-archive`
   - **需要把 OpenClaw 网关切到本机免鉴权直连** → 调 `openclaw-local-noauth-switch`
2. 无论走哪条支线，先确认总原则：
   - 先备份，再改动
   - 不删除 OpenClaw 原数据
   - 对已经在 WorkBuddy/Obsidian 演化过的内容默认只补缺失，不覆盖回滚
3. 若用户一句话里混了多类任务，按顺序拆开：
   - 迁移前先盘点
   - 迁移中再转专家/搬配置
   - 迁移后再修渠道/会话故障
4. 进入对应子技能后，严格执行其自己的验证步骤，不要在路由层直接跳过。

## Pitfalls
- 不要看到“迁移”两个字就直接写目标配置；先判断用户现在要的是盘点、转换还是排障。
- 不要把“数字幕僚”这类已在 WorkBuddy 深度演化的助理当普通全量迁移对象；这类角色默认只做补缺失，不能覆盖现有知识。
- 不要把渠道故障误判成角色迁移失败；很多时候专家已建好，问题只是新 bot 没注册或会话已膨胀。
- 不要在路由层重复执行子技能的细节步骤；路由只负责分流，不替代专门技能。

## Verification
- 已明确当前请求属于哪一条支线，并说明为什么走这条。
- 已遵守“先备份、不覆盖”的总原则。
- 已切到对应子技能继续执行，而不是停留在抽象建议层。
