---
name: skill-portfolio-cleanup-audit
description: Audit an existing WorkBuddy skill portfolio and produce a cleanup
  plan. Use when the user asks to organize skills, identify duplicates, sort
  user-created vs marketplace skills, or decide what to keep, rename, archive,
  or delete before making destructive changes.
description_zh: 技能组合审计
description_en: Skill Portfolio Audit
agent_created: true
---

# skill-portfolio-cleanup-audit

## When to use
- 用户说“整理一下 skill”“清理技能目录”“哪些技能重复了”“这些 skill 该不该删”。
- 用户需要在真正删除、归档、重命名之前，先做一轮只读审计和清单输出。
- 技能目录里混有 marketplace 数字ID目录、agent_created 技能、重复安装 skill、嵌套子技能，需要先分层判断。

## Steps
1. 先全量盘点用户级技能目录 `~/.workbuddy/skills/`，至少记录：目录名、`SKILL.md` 的 `frontmatter.name`、`agent_created`、是否带 marketplace meta 文件、是否为嵌套子技能。
2. 把技能分成四类看：
   - agent_created 自建技能
   - 命名友好的普通用户技能
   - marketplace 数字ID目录技能
   - 嵌套子技能
3. 识别三类问题：
   - **真实重复**：`frontmatter.name` 相同，或正文/说明明显重复
   - **命名噪音**：目录名是数字ID，但触发名正常
   - **结构缺损**：如子技能缺 frontmatter、meta 不完整、命名与实际用途错位
4. 对“疑似重复”的技能，不要只看目录名；要进一步比较功能完整度：
   - `SKILL.md` 正文是否一致
   - `references/`、`scripts/`、额外说明文件是否一致
   - marketplace meta / 图标 / 安装信息是否只是包装差异，还是带来了真实可用能力差异
   - 若功能等价，优先保留命名清晰、触发稳定、后续维护更直观的一份
5. 输出清单时不要一锅端，要按动作拆开：
   - 保留不动
   - 建议改名/做命名版替身
   - 建议归档/删除（需用户确认）
   - 需要人工确认
6. 若用户要求进入“第三层整理”（实际删重复项），先做两步：
   - 在项目内创建备份副本，记录所有候选目录的备份位置
   - 输出一份删除前确认单，逐条列出拟保留项、拟删除项、风险与恢复路径
7. 若发现 marketplace skill 被本轮修补过，补写对应 `_skillhub_meta.json` 或 `_knot_meta.json` 的 `userModified: true`，防止后续更新静默覆盖。
8. 最终先给“分批处理建议”，不要默认执行全量删除；优先删明确重复，再处理高频命名噪音，低频技能最后再说。

## Pitfalls
- 不要因为目录名难看就直接删数字ID skill；很多只是 marketplace 安装目录名，不影响触发。
- 不要把 agent_created 技能和 marketplace 技能混在一起清；前者往往更贴用户自己的工作流，优先保留。
- 不要默认“命名版一定比数字ID版完整”或反过来；先比 `SKILL.md`、`references/`、`scripts/` 和附加配置，再下结论。
- 不要在未确认前删除任何重复 skill；先给保留项和归档候选，再让用户拍板。
- 对 `~/.workbuddy/skills/` 这类用户家目录下的技能目录，删除前必须先备份、列出精确路径，并让用户明确确认；不要把“开始整理”理解成“已授权直接删”。
- 遇到嵌套子技能时，不要只看目录层级判断异常；先确认是不是父 skill 的正常拆分结构。
- 修补 marketplace skill 文件后，别忘了同步 `userModified: true`，否则后续更新可能把本轮修补冲掉。

## Verification
- 已输出一份按“保留 / 建议改名 / 建议归档 / 需确认”分类的清单。
- 已明确指出哪些只是目录噪音，哪些才是真重复。
- 若本轮改过 marketplace skill，已把 `userModified: true` 写回对应 meta 文件。
- 没有在用户未确认前执行删除或归档。