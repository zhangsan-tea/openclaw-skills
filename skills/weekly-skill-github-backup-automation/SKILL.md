---
name: weekly-skill-github-backup-automation
description: Set up or maintain a recurring automation that backs up
  user-created or iteratively updated WorkBuddy skills to a GitHub repository,
  with clear commit history and rollback rules.
description_zh: 每周备份 Skill 到 GitHub
description_en: Weekly Skill Backup to GitHub
agent_created: true
---

# weekly-skill-github-backup-automation

## When to use
- 用户要把自创 Skill 或近期迭代过的 Skill 定期备份到 GitHub。
- 用户提到“每周备份 skill”“定时同步 skill 仓库”“保留 skill 版本并可回退”。
- 已经明确了本地 skill 源目录与 GitHub 仓库目录，希望创建 recurring automation。

## Steps
1. 先确认是否已有同类自动化，避免重复创建。
2. 确认 Skill 来源目录通常为 `~/.workbuddy/skills/`，并优先以 `agent-created-skills.json` 作为“自创 Skill 清单”。
3. 确认 GitHub 仓库副本目录、远程和分支，例如 `/Users/lee/WorkBuddy/openclaw-skills`、`origin`、`main`。
4. 创建每周备份 automation：
   - 读取 `agent-created-skills.json`
   - 先确认仓库 `main`/`origin` 状态正常，且没有与本次备份无关的脏改动
   - 将每个自创 Skill 目录与仓库里的 `skills/<skillDir>` 对比
   - 对新增或变更的 Skill，同步整个目录，而不只复制 `SKILL.md`
   - 只暂存本次涉及的 `skills/<skillDir>` 路径，不要 `git add .`
   - 只有在 `git status` 有变化时才提交和推送
   - 若发现源目录中某个 Skill 消失，不要自动删仓库副本，先报告为待确认删除
5. 如果用户关心“版本锚点”和更稳的回退，再补第二个 automation：
   - 每周一运行，但仅在“当月第一个周一”时创建月度 annotated tag
   - 先确认工作区干净，再打 tag，避免把脏状态当基线
   - tag 命名固定为 `skills-backup-YYYY-MM`
   - tag 只打在 `main` 当前 HEAD 上
   - 若同名 tag 已存在则跳过，不重复创建
   - tag message 尽量附上自上个基线以来有变更的 Skill 摘要，便于后续回看
6. 在 automation prompt 里写死版本策略：
   - 每次运行最多创建一个新 commit
   - 不要 amend，不要 squash
   - commit 标题带日期，并尽量带 Skill 名称
   - push 失败时保留本地变更，不要强推
   - 标签 push 失败时保留本地 tag，不强推、不删远端已有内容
7. 同时写清回退原则：
   - 默认按单个 Skill 目录回退，不覆盖整个仓库
   - 先看 `git log -- skills/<skillDir>`
   - 再用 `git checkout <commit> -- skills/<skillDir>` 或 `git revert <commit>`
   - 若要回到月度基线，可先看 tag：`git show skills-backup-YYYY-MM`

8. 失败自动通知（两个自动化通用）：
   - 任何阻断性步骤失败时（仓库状态异常、push 失败、工作区脏改动、tag 异常等），立即通过飞书给用户发消息
   - 消息必须包含：①哪个自动化失败 ②失败步骤 ③失败原因 ④当前状态
   - 使用 lark-im skill 发送飞书消息，发给用户本人
   - 若飞书通知也失败，在自动化运行结果中醒目标注"备份失败+飞书通知也失败"
   - 通知是兜底手段，不替代 prompt 里的"保留本地变更、不强推"等安全策略

## Pitfalls
- 不要把“所有 skill”都备份；优先限定在用户自创或明确要纳入版本管理的 skill。
- 不要只复制 `SKILL.md`，否则 scripts/、references/、assets/ 的变更会丢失。
- 不要在无变更时硬提交空 commit。
- 不要用 force push 处理失败，避免覆盖历史。
- 不要把“回退”理解成重置整个仓库；多数情况只需回退某个 skill 目录。
- 月度 tag 不是替代每周 commit 的；它只是月度锚点，真正细粒度回退仍要靠提交历史。
- 不要把 monthly RRULE 硬写成系统不支持的“第一个周一”表达；更稳的做法是每周一触发一次，再在执行逻辑里判断是否为当月第一个周一。
- 不要把仓库里其他临时改动一起打包进备份 commit；skill 备份只应覆盖本次识别出的 `skills/<skillDir>` 变更。
- 对“删除 skill”要更保守：自动新增、自动备份通常没问题，自动删除仓库副本则更容易误伤。
- 飞书失败通知不要默认只走 user 身份；若 `lark-im` 发送时报缺少 `im:message.send_as_user` scope，可改用 bot 身份重试，只要 bot 对目标用户可发私信即可。

## Verification
- 每周备份自动化已创建且为 ACTIVE。
- 如用户要求月度锚点，月度 tag 自动化也已创建且为 ACTIVE。
- 自动化 prompt 明确包含：扫描自创 skill、仅变更时提交、保留 commit 历史、失败不强推、按目录回退。
- 若启用 tag 自动化，其 prompt 明确包含：仅在当月第一个周一打 tag、tag 命名规则、tag 已存在则跳过、push 失败不强推。
- GitHub 仓库已确认 remote 和目标分支。
- 自动化 prompt 明确包含失败通知机制：飞书消息通知用户，飞书也失败则醒目标注。
