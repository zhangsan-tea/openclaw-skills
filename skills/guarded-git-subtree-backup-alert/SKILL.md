---
name: guarded-git-subtree-backup-alert
description: Guard a recurring backup that mirrors selected subdirectories into
  a Git repository, stops when the repo has unrelated dirty changes, stages only
  approved paths, commits a new backup snapshot, pushes to origin/main, and
  sends a Feishu alert with failure step and retained-state details when the run
  is blocked or push fails.
description_zh: 受控子目录备份告警
description_en: Guarded subtree backup alert
agent_created: true
---

# guarded-git-subtree-backup-alert

## When to use
- 周期性把一组目录备份到 Git 仓库。
- 只允许同步白名单路径，禁止 `git add .`。
- 备份前必须检查仓库分支、remote、远端同步和工作区脏改动。
- 失败时需要把失败步骤、失败原因和本地状态通过飞书通知给指定用户。

## Steps
1. 读取待备份对象清单，确认每个对象的源目录与仓库目标目录。
2. 在目标仓库检查当前分支是否为 `main`、远程是否存在 `origin`，并执行 `git fetch origin main --tags`。
3. 读取 `git status --porcelain`；若存在与本次备份无关的脏改动，立即停止，不做同步、不做 commit，并记录保留现状。
4. 逐个对比源目录与仓库副本；对新增或更新对象，同步整个目录，至少包含 `SKILL.md` 以及已存在的 `scripts/`、`references/`、`assets/`、`templates/` 等附属文件。
5. 对源目录中已不存在但仓库仍保留的对象，只报告“疑似删除，待人工确认”，不要自动删仓库文件。
6. 若白名单路径下最终无变化，输出“本周无新增或更新”。
7. 若有变化，只暂存本次涉及的目标路径，创建新的 commit（不要 amend、不要 squash），commit 标题包含日期和对象摘要。
8. `git push origin main`；若 push 失败，保留本地变更并记录失败原因。
9. 任一步骤失败时，通过飞书 IM 向指定用户发送通知，消息必须包含：自动化名称、失败步骤、失败原因、当前状态（本地变更是否保留等）。

## Pitfalls
- 不要在仓库已有无关脏改动时继续执行，否则容易把杂项变更混入备份提交。
- 不要自动删除仓库中“源目录已消失”的对象，先做人审。
- 不要使用 `git add .`；必须显式列出允许暂存的路径。
- push 失败时不要强推，也不要清理本地改动。

## Verification
- 仓库干净且无变更时，输出“无新增或更新”。
- 仓库干净且有变更时，只出现白名单路径的 staged/committed 记录，并成功推送到 `origin/main`。
- 仓库状态异常或 push 失败时，飞书通知成功送达，且消息中包含失败步骤、原因和本地保留状态。
