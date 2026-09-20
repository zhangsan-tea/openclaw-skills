---
name: workspace-memory-condense
description: Condense an oversized WorkBuddy workspace MEMORY.md into a shorter,
  durable project memory. Use when the injected workspace memory is truncated,
  when MEMORY.md has accumulated duplicate rules, or when the project memory
  needs reorganization without losing key collaboration norms, topic anchors,
  and storage conventions.
description_zh: 精简项目记忆
description_en: Condense Workspace Memory
agent_created: true
---

# workspace-memory-condense

## When to use
- The workspace memory injection says MEMORY.md was truncated or exceeded size limits.
- `/Users/lee/WorkBuddy/Claw/.workbuddy/memory/MEMORY.md` has become too long, repetitive, or hard to maintain.
- You need to preserve durable project conventions while removing stale or duplicate detail.
- The user task depends on having a clean project memory before proceeding.

## Steps
1. Read the full workspace memory file.
2. Extract only durable information:
   - collaboration rules and execution preferences
   - active project workstreams and durable judgments
   - stable person/term mappings that prevent confusion
   - knowledge-base storage rules, paths, and sync constraints
   - technical or migration constraints that are still active
3. Remove or compress:
   - repeated wording
   - temporary status notes that no longer guide future work
   - overly detailed examples when one summary rule is enough
   - items already covered by broader rules
4. Rewrite MEMORY.md in a compact structure with clear sections.
5. Confirm today’s daily memory log exists. If not, create it.
6. Append one brief maintenance note to the daily log describing that MEMORY.md was condensed and what kinds of information were preserved.
7. If the cleanup revealed a new long-term user preference that is cross-project rather than project-specific, also update `~/.workbuddy/MEMORY.md`.

## Pitfalls
- Do not overwrite the daily log; append only.
- Do not delete durable paths, naming rules, or sync constraints that future sessions rely on.
- Do not keep transient search results, temporary file paths, or tool errors.
- Keep the rewritten memory specific enough to be useful, but short enough to avoid future truncation.

## Verification
- Re-read the rewritten MEMORY.md if needed and confirm it now fits within a concise, maintainable structure.
- Ensure the daily log contains a short note about the cleanup.
- Proceed to the user’s actual task only after the memory file is cleaned up.