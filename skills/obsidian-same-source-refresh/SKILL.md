---
name: obsidian-same-source-refresh
description: Refresh an existing Obsidian topic/source axis when the user
  provides another version of the same material or execution-side attachments.
  Use it to decide whether to update an existing source, add a topic increment,
  park an item as an execution attachment, or hold it as unreadable instead of
  creating duplicate notes.
description_zh: Obsidian同源刷新
description_en: Obsidian same-source refresh
agent_created: true
---

# obsidian-same-source-refresh

## When to use

Use this skill when all of the following are true:

1. The user is continuing an Obsidian-based knowledge workflow.
2. New material appears to be a refresh, variant, or attachment of an already ingested topic/source, not a brand-new theme.
3. The main task is to decide **refresh vs new note vs execution attachment vs hold**.
4. You need to keep the existing topic/source/memo axis clean and avoid duplicate branches.

Typical triggers:

- The user sends a refreshed smartpage, sheet, or Tencent Doc that obviously belongs to an existing source.
- The user sends a zip, tool package, manual, template, or screenshot bundle that should inform execution but not become a new strategic topic.
- The user asks to "continue", "update the existing note", "look at current Obsidian first", or "judge how this should be ingested".

Do **not** use this skill when the material is clearly a new topic, or when the user only wants analysis without touching files.

## Steps

1. Read the current topic/source/memo files around the existing axis first.
2. Read the newly provided material or its extracted text.
3. Classify the new material into one of four buckets:
   - **Same-source refresh**: update the existing source and note what changed.
   - **Topic increment**: add a new increment section to the existing topic.
   - **Execution attachment**: keep it under the current topic as execution-side material; do not create a new strategic topic.
   - **Hold / unreadable**: record that the item is not reliably readable yet and do not extend conclusions from it.
4. If it is a same-source refresh, edit the existing source instead of creating a duplicate source file.
5. If it changes the main line, add a concise increment section to the existing topic, focusing on what the refresh means for execution.
6. If it is an execution attachment, write the treatment rule explicitly in the topic or a dedicated execution card, such as tool trial, result return, repair, or review workflow.
7. If any old field in the existing source now conflicts with fresher evidence, mark that old field as a **historical field** instead of silently deleting it.
8. Update related links so the new execution card or refreshed source remains connected to the main topic.
9. After finishing, append a brief project memory note stating what was refreshed and what classification rule was applied.

## Pitfalls

- Do not create a new source just because the user sent another export of the same smartpage or sheet.
- Do not treat zip/tool/manual attachments as new strategy topics unless they truly introduce a new stable theme.
- Do not let stale timetable fields in old tables override fresher notices or meeting notes; mark them as historical.
- Do not extend conclusions from unreadable mind maps, login shells, or incomplete exports.
- Do not flatten everything into one note; keep topic vs source vs execution-card roles clear.

## Verification

- The existing source file was refreshed in place when appropriate.
- The main topic clearly records the treatment rule for the new material.
- Any new execution card is linked back to the main topic.
- Old conflicting fields are visibly marked as historical instead of silently left ambiguous.
- Project memory contains a short note about the refresh decision.
