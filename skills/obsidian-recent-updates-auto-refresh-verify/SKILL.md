---
name: obsidian-recent-updates-auto-refresh-verify
description: Refresh an Obsidian vault's machine-generated recent-updates
  summary file with the given script command, then verify the target file
  timestamp, header generation time, and whether any non-target vault files
  changed in the same window. Use for scheduled or manual refresh tasks where
  the user requires a strict "only this summary file should change" check.
description_zh: Obsidian 自动摘要刷新校验
description_en: Obsidian auto summary refresh verify
agent_created: true
---

# obsidian-recent-updates-auto-refresh-verify

## When to use
- 用户要求刷新某个 Obsidian vault 的“最近更新摘要”“自动摘要”“近72小时文件增量”等机器生成摘要。
- 用户已经给出明确脚本命令，且要求确认目标文件已生成或更新。
- 用户强调“不要改动其他 Obsidian 文件”或要求报告失败步骤与原因。
- 适合自动化任务，也适合手工执行同类刷新动作。

## Steps
1. 先读取对应自动化/工作流的历史记忆，确认此前是否有已知异常或特殊校验口径。
2. 运行用户提供的脚本命令，不要擅自改动 vault、output-name、title、label 等参数。
3. 记录脚本 exit code 和 stdout；若脚本失败，原样保留错误信息。
4. 只读检查目标摘要文件是否存在，并读取文件头部，确认“最近生成”与 mtime 是否已刷新。
5. 优先把“刷新执行”和“只读校验”拆成两个清晰步骤；如果一定要在一条 shell 命令里把时间戳传给 Python，记得显式 `export` 变量，避免出现“刷新成功但校验脚本因取不到环境变量而报错”的假失败。
6. 以脚本启动时间或目标文件 mtime 为阈值扫描 vault，列出同时间窗内被改动的文件；重点区分：
   - 目标自动摘要文件
   - `.workbuddy/` 等辅助记忆文件
   - 其他业务 Markdown / 附件文件
7. 对用户汇报时直接给结论：成功/失败、目标文件路径、最近生成时间、mtime，以及是否发现非目标文件被改动。
8. 若当前工作区要求写记忆，再把高层结果回写到自动化记忆与当天工作日志，但不要把完整正文塞进记忆文件。

## Pitfalls
- 不要把校验包装命令写得过度复杂，避免因为 shell 引号或变量导出问题导致“刷新成功但校验脚本报错”。
- 若扫描到 `.workbuddy/` 辅助文件变动，要单独说明，不要误报成业务笔记被刷新脚本改写。
- 不要为“证明没改别的文件”去修改 vault 内任何文件；校验必须只读。
- 如果用户已明确授权执行，直接跑；不要再次请示“要不要开始运行”。

## Verification
- 脚本 exit code 为 0。
- stdout 返回目标摘要文件路径，或至少无报错且目标文件 mtime 已更新。
- 目标摘要文件头部的“最近生成”时间与本轮刷新时间一致或接近。
- 同时间窗内未发现目标摘要之外的业务 Obsidian 文件被改动；若发现 `.workbuddy/` 辅助文件更新时间戳变化，单独注明。
