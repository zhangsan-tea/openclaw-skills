---
name: obsidian-recent-updates-refresh
description: Refresh an Obsidian vault's machine-generated recent-updates
  summary note by running the dedicated Python script with the vault path,
  output file name, title, and label provided by the user or automation. Use
  when the task is specifically to refresh the auto summary without manually
  editing other Obsidian content, and report the exact stdout path, file mtime,
  success/failure step, and any unexpected concurrent file changes observed
  during verification.
description_zh: Obsidian自动摘要刷新
description_en: Obsidian summary refresh
agent_created: true
---

# obsidian-recent-updates-refresh

## When to use
- 用户明确要求刷新 Obsidian 某个知识库的“最近更新摘要”“自动摘要”“近 72 小时增量”等机器生成文件。
- 已知要运行的脚本是 `obsidian_recent_updates_auto_refresh.py`，或任务本质上等价于“运行既有脚本重写自动摘要文件”。
- 任务约束是：只刷新目标摘要文件，不手工改动其他 Obsidian 正文文件；若失败，要指出失败步骤和原因。
- 自动化任务或跨终端续接流程里，需要定时重刷 `00_最近更新摘要_自动刷新版_近72小时文件增量.md` 一类文件时。

## Steps
1. 先读自动化/项目上下文要求的记忆文件；如果是自动化执行，优先读对应 `.workbuddy/automations/<automation-id>/memory.md`。
2. 运行受管 Python：
   `"/Users/lee/.workbuddy/binaries/python/versions/3.13.12/bin/python3" "/Users/lee/WorkBuddy/Claw/.workbuddy/scripts/obsidian_recent_updates_auto_refresh.py" --vault "<vault_path>" --output-name "<output_name>" --title "<title>" --label "<label>"`
3. 保留完整命令结果：stdout、stderr、exit code。正常情况下 stdout 只会返回目标文件绝对路径。
4. 验证目标文件：
   - 确认文件存在；
   - 读取前几十行，确认标题和“最近生成”时间已经刷新；
   - 记录 mtime、size、path。
5. 如果用户要求“不要改动其他 Obsidian 文件”，额外做一次只读核验：列出本轮时间窗内同 vault 下被更新的文件。如果发现目标文件之外还有变更，必须如实报告“观察到还有哪些文件在同时间窗变化”，但不要擅自回滚。
   - 做 shell + 内嵌 Python 复核时，先显式 `export` 需要传给 Python 的环境变量；不要在 Python 里直接读取一个未导出的 shell 变量。
   - 若脚本已成功但“以启动时间为阈值”的复核子步骤本身失败，可退回到“以目标文件 mtime 为中心的小时间窗”做只读复核，并在结果里说明这是补充校验，不影响刷新动作本身是否成功。
6. 将高层摘要写回自动化记忆和工作区日记；只记结果，不记整段正文。
7. 最终回复必须包含：是否成功、stdout 返回路径、目标文件 mtime、失败时的失败步骤和原因、是否观察到同时间窗其他文件变化。
8. 若目标摘要文件本身是用户需要查看的交付物，最后要把该 Markdown 文件作为结果交付出去。

## Pitfalls
- 不要把“脚本运行成功”偷换成“严格只有一个文件发生变化”；后者需要额外核验。
- 不要手工改写 Obsidian 正文文件来“修正摘要内容”；这个流程只负责运行脚本并验证产物。
- 若 stderr 为空但 exit code 非 0，仍然按失败处理，明确指出失败步骤。
- 若同时间窗内有 `.obsidian/workspace.json`、`.workbuddy/...` 或其他 topic/source 文件变化，不要武断归因给本脚本；只报告观察事实。

## Verification
- 命令 exit code = 0。
- stdout 返回目标文件绝对路径。
- 目标文件存在，且 `最近生成` 时间、文件 mtime 与本轮执行时间匹配。
- 如做了时间窗核验，结果中明确区分“目标文件成功刷新”和“观察到的其他并发变更”。
