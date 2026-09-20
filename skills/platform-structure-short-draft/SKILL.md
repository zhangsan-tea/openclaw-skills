---
name: platform-structure-short-draft
description: Turn a bloated platform or system feature list into a short
  decision-oriented structure draft. Use this when the user already has a heavy
  platform/product doc full of modules and feature tables, but actually needs a
  short version that clarifies positioning, internal-vs-external boundaries,
  shared底座, first-phase scope, and which heavy items to postpone.
description_zh: 平台短版结构稿
description_en: Platform short draft
agent_created: true
---

# platform-structure-short-draft

## When to use

Use this skill when all of the following are true:
1. The user has an existing platform / system / IA / feature document.
2. The current draft is too heavy, too detailed, or too much like a backlog.
3. The real ask is to restart it as a **short structure draft** for review, alignment, or boss discussion.
4. The key need is not more functions, but clearer answers to:
   - 为什么要分层 / 分版本
   - 谁用
   - 看什么
   - 能写什么
   - 哪些能力先做
   - 哪些重能力后置

Typical triggers:
- “直接重启一版短版结构稿”
- “别写成功能清单，先给我一个短结构”
- “这个平台稿子太重了，重起一版老板能看的”
- “先把对内对外边界写清楚”

## Steps

1. **Read the current heavy draft and the nearest boundary notes**
   - Read the current platform / system doc.
   - Read any earlier notes that already defined the intended split, such as “对外是服务台，对内是作战台”.
   - Do not start from a blank opinion if prior boundary decisions already exist.

2. **Identify the true decision axis**
   - Usually the heavy draft is not wrong because it has many functions.
   - It is wrong because the order is reversed: feature list first, positioning later.
   - Extract the real axis first, for example:
     - one shared底座 vs two independent systems
     - internal workbench vs external service desk
     - operating layer vs presentation layer
     - heavy management features vs light first-phase features

3. **Cut the draft into four mandatory layers**
   - Why split / why not just do permission gating
   - Overall structure (one底座 + two interfaces, or equivalent)
   - Internal version positioning and modules
   - External version positioning and modules

4. **Force boundary clarity before feature detail**
   - For each side, say clearly:
     - who uses it
     - what problem it solves
     - what it should contain
     - what it explicitly should not contain
   - If a module belongs to both sides, move it down to the shared底座 instead of duplicating it in both interfaces.

5. **Compress to a decision-friendly short draft**
   - Prefer a structure like:
     1. Why this split exists
     2. Overall architecture
     3. External version
     4. Internal version
     5. Boundary rules
     6. Phase 1 scope
     7. Postponed items
     8. One-line close
   - Keep the tone direct. This is not a PRD and not a backlog dump.

6. **Name heavy items and postpone them explicitly**
   - Typical heavy items include:
     - formal evaluation systems
     - full workflow engines
     - heavy analytics dashboards
     - mirrored double-end features
     - AI search with unclear internal/external order
   - Put them into a “暂缓项 / 先不写重” section.

7. **Output the short draft as a standalone Markdown**
   - The result should be usable directly in review or copied into a doc.
   - If useful, also state the core line in one sentence, e.g. “对外是服务台，对内是作战台，共用一套底座”.

## Pitfalls

- Do not keep the original module explosion and only shorten the wording.
- Do not start with six modules and forty features before explaining why the split exists.
- Do not make the external version look like a half-backend.
- Do not duplicate the same capability both as a core module and again as a dashboard/workbench subsection.
- Do not leave heavy items ambiguous; postpone them explicitly.
- Do not confuse “two interfaces” with “two independent systems”.

## Verification

A good result should satisfy all checks:
1. A reviewer can understand the split in the first screen without reading a giant feature table.
2. Internal and external versions have clearly different roles.
3. Shared capabilities are recognized as a common底座, not duplicated everywhere.
4. The short draft says what Phase 1 should do and what should wait.
5. The output reads like a structure draft for alignment, not a product backlog.
