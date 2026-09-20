---
name: obsidian-knowledge-distill-map
description: Distill a newly ingested work material in the Obsidian vault into a
  short key-points memo, build a cross-note knowledge map, optionally remove the
  original transient record, and update links so the concise notes become the
  main entry points.
description_zh: Obsidian 入库压缩与知识地图
description_en: Obsidian distill and map
agent_created: true
---

# obsidian-knowledge-distill-map

## When to use
Use this skill when Lee has already provided a work material and wants you to:
- extract only the most important points;
- replace or supersede a verbose original record with a cleaner markdown note;
- build a more complete knowledge map around the topic;
- keep the result inside the Obsidian work vault rather than as a one-off chat answer.

Typical triggers:
- “提炼最重要的要点，形成 md，再删原记录”
- “把这份材料压成能复用的短版”
- “基于这份材料补一个更完整的知识地图”

## Steps
1. Read the original material and the latest related source/memo notes already created from it.
2. Re-state the problem in one sentence: what is the real issue behind the user’s wording.
3. Distill the material into 5-8 non-overlapping key points. Prefer structural judgments over transcript details.
4. Create a concise memo note in the Obsidian work vault. The note should contain:
   - one-sentence conclusion;
   - key points;
   - 2-4 lines that Lee can directly reuse upward;
   - next questions worth tracking.
5. Build a separate “知识地图” markdown note. Organize it at minimum into:
   - problem itself;
   - structural breakpoints;
   - organization / interface issues;
   - usage scenarios;
   - risks if unresolved;
   - realistic推进路径.
6. Link the new notes back into the existing source/memo via `related` so the concise notes become easy entry points.
7. If the user asked to delete the original record, first determine which file is safe to remove:
   - transient import file / temp transcript: can delete directly once the distilled notes exist;
   - personal-vault note under Home: do not delete unless the request is explicit and unambiguous, and follow the safety policy for destructive actions.
8. Update project memory with: what was distilled, what map was created, and what was deleted.
9. Present the generated markdown files to the user.

## Pitfalls
- Do not confuse the raw import file with the curated source note in Obsidian.
- Do not keep repeating “缺数据”; force it into concrete layers such as feedback loop, bookkeeping, tag logic, query ability, and org interface.
- Do not build a map that is only a topic list; it must explain relationships and consequences.
- Do not delete notes in personal knowledge vaults casually; temp files and curated vault notes are different risk levels.

## Verification
- There is one concise memo note and one knowledge-map note.
- Both notes link to existing topic/source/memo context.
- The key-points note is materially shorter than the original record.
- If deletion was requested, the deleted target is explicitly identified and its status is confirmed.
- The user can open the final markdown files directly.
