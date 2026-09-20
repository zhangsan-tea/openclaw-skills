---
name: handmade-skill-locator
description: 在聊天记录、个人笔记（如养虾笔记）和本地 skills / GitHub 备份仓库之间交叉定位用户手搓
  skill。适用于用户只记得用途、关键词或曾在哪提过，但忘了具体 skill 名称或路径的场景。
description_zh: 定位手搓 Skill
description_en: Locate handmade skill
agent_created: true
---

# handmade-skill-locator

## When to use
- 用户说“之前手搓过一个 skill，帮我找一下”
- 用户只记得用途、触发词、笔记提及位置或聊天里聊过，但不记得 skill 名称
- 需要同时从历史对话、个人笔记和本地/备份仓库交叉确认 skill 地址

## Steps
1. 先查历史对话，恢复可能的 skill 名称、用途、GitHub 地址或当时的描述。
2. 再查 `~/.workbuddy/skills/` 与相关备份仓库（如 `~/WorkBuddy/openclaw-skills/`），用用途关键词、文件名关键词和触发词三种角度搜索。
3. 如果用户提到个人笔记（如养虾笔记），优先搜最新版本笔记中的 skill 列表、GitHub 链接和用途摘要。
4. 对最可能候选读取 `SKILL.md`，确认名称、用途、输入格式、输出模式等核心信息。
5. 回答时优先给出：skill 名称、当前最可信路径、GitHub 地址、是否已安装到 `~/.workbuddy/skills/`；如有多个候选，再列备选项。
6. 若只在旧仓库或迁移目录找到，要明确说明“已定位到历史/备份位置，当前工作目录未见已安装副本”。

## Pitfalls
- 不要只按文件名搜；很多手搓 skill 名称和用户口头描述不完全一致。
- 不要把系统内置 skill 误认成用户手搓 skill；优先看 GitHub 备份仓库和带明确自定义用途的 `SKILL.md`。
- 个人笔记检索优先只读搜索，不做改动。
- 如果工作区路径不存在，要直接说明，不要把“没装”说成“没有这个 skill”。

## Verification
- 至少拿到以下三项中的两项：`SKILL.md` 实体文件、笔记中的 GitHub 链接、历史对话中的明确提及。
- 回答中应包含可直接打开的路径或链接，而不是只给模糊名称。
