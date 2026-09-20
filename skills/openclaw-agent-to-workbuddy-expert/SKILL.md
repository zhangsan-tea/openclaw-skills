---
name: openclaw-agent-to-workbuddy-expert
description: Convert a single OpenClaw agent into a registered WorkBuddy expert
  by extracting persona and workflow files from the agent workspace, mapping
  them into WorkBuddy expert fields, generating the expert package, validating
  it, and registering it locally.
description_zh: OpenClaw助理转专家
description_en: OpenClaw Agent to Expert
agent_created: true
---

# openclaw-agent-to-workbuddy-expert

## When to use
- 用户要把 OpenClaw 里的某个单体助理迁成 WorkBuddy 专家。
- 已知来源主要在 `~/.openclaw/workspace-<agent-id>/`、`~/.openclaw/openclaw.json`、相关 skill/记忆文件。
- 目标是生成一个可在 WorkBuddy 专家中心出现的本地专家，而不是只做迁移方案。

## Steps
1. 先读取 `~/.openclaw/openclaw.json`，确认目标 agent 的 `id`、显示名、workspace 路径和是否为单角色。
2. 先核验 workspace 路径是否真实存在；若 `openclaw.json` 里有条目但对应 workspace 已缺失（如已废弃/未落盘的 agent），不要凭配置猜测生成专家，而是标记为 `source_missing` 并在结果中说明。
3. 读取该 agent workspace 下的 `IDENTITY.md`、`MEMORY.md`、`SOUL.md`、`USER.md`；如果该 agent 明确依赖某个 WorkBuddy skill，也一起读取。
4. 做字段映射：
   - `expertType`：单角色固定为 `agent`
   - `categoryId`：按主要输出物选择，不凭直觉乱填
   - `displayName`：沿用用户熟悉的助理名
   - `profession`：默认写成明确职业定位；但如果用户明确说“名字就叫 X”，要同步把 `profession.zh` 也改成 `X`，避免在“我的专家”里因卡片标题不是用户预期而找不到
5. 在 `~/.workbuddy/plugins/marketplaces/my-experts/plugins` 下创建专家目录；若不存在，先 `mkdir -p`，再用 `expert-manager/scripts/init_expert.py` 初始化。
6. 填写 `.codebuddy-plugin/plugin.json`、`agents/<agent-name>.md`、`README.md`。正文要保留：核心能力、工作流程、输出规范、注意事项。
7. 如果 OpenClaw 侧已经沉淀出同主题、可直接复用的 WorkBuddy skill（如 `awakening-coach`、`weekly-report-editing`，以及日程场景下的 `gog`），优先在 Agent MD frontmatter 里通过 `skills: [...]` 预加载，而不是把全部规则硬塞进专家正文。
8. 如果图像生成工具不可用，先放一个本地 PNG 占位头像，并在 `references/` 里留下推荐 prompt；不要因为头像卡住整个专家创建。
9. 运行 `validate_expert.py` 校验；通过后用 `register_expert.py <expert-dir> --session-id <当前session-id>` 注册。
10. 注册后额外核验三件事：
   - `~/.workbuddy/plugins/marketplaces/my-experts/.codebuddy-plugin/marketplace.json` 里已有该专家条目
   - 专家中心卡片标题是否符合用户预期（必要时同时调整 `displayName` 和 `profession`）
   - `.created-by-session` 是否真的落到专家目录；若脚本回显成功但文件缺失，手动补写当前 session id
11. 如需备份或分享，再运行 `package_expert.py` 打 zip 包。

## Pitfalls
- `plugin.json` 的 `name`、目录名、`agentName`、`agents/*.md` 文件名是一组唯一标识，后续不要随意改。
- `tags` 和 `quickPrompts` 必须各 3 个，第一条 `quickPrompt` 必须等于 `defaultInitPrompt`。
- `displayDescription` 中文需要控制在 40-50 字，别写成一句空泛口号。
- `~/.workbuddy/plugins/marketplaces/my-experts/plugins` 可能默认不存在，先建目录再初始化。
- OpenClaw 的渠道凭据、bot token、app secret 不该写进专家正文；只迁角色设定、流程和输出要求。
- `register_expert.py` 可能已成功更新 `marketplace.json`，但偶发不写 `.created-by-session`；不要只看脚本回显，必须落盘核验，缺失就手动补写。
- 某些教练/写作类 agent 已有对应 WorkBuddy skill，若不预加载，专家可用但会变“空心”，后续对话质量明显下降。
- 对已经在 WorkBuddy / Obsidian 深度演化过的高价值角色（如数字幕僚），默认只做补缺失，不做覆盖式回迁；必要时先人工比对，再决定是否单独迁。
- `openclaw.json` 里的 `main` 往往是后台进程或系统位，不一定适合当用户可见专家；批量迁移时默认只迁明确面向用户的助理，除非用户特别点名。
- 如果某个 agent 仅在 `openclaw.json` 里留名、workspace 实体已不存在（如 `presenter`），不要硬造一个“空专家”；应明确标记来源缺失并在结果里说明未迁移原因。

## Verification
- `validate_expert.py` 输出 `Expert package is valid!`
- `register_expert.py` 输出 `is now registered and visible in WorkBuddy`
- 专家目录内至少有：`.codebuddy-plugin/plugin.json`、`agents/*.md`、`avatars/`、`README.md`
- 打开 WorkBuddy 专家中心后，能看到该专家的显示名、职业、描述、标签和推荐问法

## Related Skills
- 迁移前先做资产摸底：`openclaw-migration-readonly-inventory`
- 同一类迁移请求但还没分清支线：`openclaw-to-workbuddy-migration-router`
- 专家建好但企微新 bot 不回消息：`workbuddy-wecom-writer-noresponse-fix`