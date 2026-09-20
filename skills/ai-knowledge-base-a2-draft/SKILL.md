---
name: ai-knowledge-base-a2-draft
description: Turn an existing AI product or knowledge-base direction note into an A-2 implementation draft: compress the direction into concrete knowledge objects, minimum fields, storage shape, boundary rules, retrieval flow, and first-batch scope. Use when the user has already agreed on the high-level line (for example, knowledge reconstruction before QA assistant) and now needs a short, decision-friendly basic scheme rather than a full PRD.
description_zh: AI知识底座A2方案
description_en: AI knowledge base A2 draft
agent_created: true
---

# ai-knowledge-base-a2-draft

## When to use
Use this skill when all of the following are true:
1. The user already has a product direction, phase memo, or architecture note.
2. The next ask is not “what is the product” but “how does the knowledge layer actually land”.
3. The task is to convert a conceptual AI / knowledge-base idea into a short implementation draft.
4. The needed output should answer:
   - what knowledge objects exist
   - what the minimum fields are
   - where the data should live
   - who maintains which fields
   - how the QA layer should call it
   - what the first pilot scope should be

Typical triggers:
- “继续推进吧，先出基本方案”
- “从 A 开始推进”
- “把这个东西压成可实施字段表和存储方案”
- “先别写 PRD，先把知识底座怎么落讲清楚”

## Steps
1. Read the nearest phase memo and boundary notes first.
   - Reuse the existing agreed line instead of restarting from abstract opinion.
   - Confirm what is in scope and what is explicitly excluded.
2. Restate the true implementation target in one sentence.
   - Example: build an AI-ready knowledge card layer, not just a chat shell.
3. Freeze the knowledge object set.
   - Keep the list small.
   - Prefer 4-8 object types for the stable rule layer.
   - If the user also needs current system status, project archive, or statistics-style QA, split the model into two clusters instead of forcing everything into cards:
     - rule knowledge objects
     - state/archive structured objects
   - Do not let the draft explode into a backlog.
4. For each object type, define:
   - what question it answers
   - required fields
   - optional fields
   - likely source materials
   - whether it is better as a Markdown card or a structured table record
5. Add shared meta fields across all objects.
   - tags, scope, version, owner, review status, confidence.
6. Decide the storage shape.
   - Prefer a mixed model when the team already works in Markdown/Obsidian:
     - Markdown cards for human editing of stable rules
     - frontmatter for structure
     - structured tables for system status, project archive, or statistics-oriented records
     - exported JSON/JSONL index for machine use
7. Define boundary and visibility rules before retrieval design.
   - Separate direct-answer content, controlled-support content, and internal-only content.
   - Be explicit when some sensitive status content is allowed in an internal-only support layer rather than fully excluded.
8. Draft the retrieval / routing chain.
   - classify question
   - enrich context
   - route by object cluster (rules vs state/archive)
   - retrieve cards or structured records
   - assemble answer blocks
   - escalate or refuse when needed
9. Name a deliberately narrow pilot.
   - first batch sources
   - first batch card count
   - first batch answer scope
10. Output a short standalone Markdown.
   - Keep it decision-friendly.
   - End with 3-5 points the user should confirm next.
11. If the conversation is already past A-2/A-3 and the user says “continue” or “directly push forward”, stop repeating object theory.
   - Move into build-ready artifacts instead:
     - final table headers
     - CSV or online-table header files for core tables
     - 3-5 real sample cards
     - first refill checklist
     - 8-10 pseudo queries / analytics questions
     - page / interface mapping when the user is clearly entering semi-implementation stage
   - The goal is to cross the line from “field discussion” to “start filling and validating”.
12. If the conversation is already in A-7 style semi-implementation, the next useful step is usually A-8 style landing artifacts.
   - Prefer producing:
     - SQL build draft for core tables
     - one official rule-card template with frontmatter
     - one refill skeleton / rollout checklist
     - a short note that locks the order: build tables → create real card dirs → refill real data → run real query validation
   - Do not spend another round re-explaining the object model unless the user explicitly asks.
13. If the conversation is already in A-8 style landing stage and the user still says “continue”, move into A-9 style real starter files.
   - Prefer producing:
     - initialization CSV files for core tables
     - 3-5 real starter cards in formal subdirectories
     - one refill checklist for full coverage
     - one first-round validation question list
     - one note that tells exactly when the user should join testing
   - The goal is to stop shipping only design documents and start shipping files another person can immediately fill.

## Pitfalls
- Do not jump straight into model training or fine-tuning.
- Do not let every module become a knowledge object type.
- Do not force status data or project archives into Markdown cards if they are naturally table-shaped.
- Do not use vector search as a substitute for boundary design.
- Do not mix internal sensitive notes with external support content.
- Do not over-shrink valid internal-use status data just because it is sensitive; first decide whether it belongs in an internal-only layer.
- Do not mechanically sample project archives when the total volume is already small; full coverage may be better than a fake pilot subset.
- Do not pre-filter system-status records into “high frequency only” when the total system count is already small and the user may need discovery-style retrieval across the whole set.
- Do not make the first pilot too broad.
- Do not write a feature backlog disguised as a data model.

## Verification
A good result should satisfy all checks:
1. A reviewer can tell what the AI-ready knowledge layer is in the first screen.
2. Each object type clearly answers a kind of user question.
3. Required fields are concrete enough to start building cards immediately.
4. Storage, maintenance, and retrieval are all addressed, not just fields.
5. The pilot scope is intentionally narrow and realistic.
6. If the task is already in A-7 style execution, the output includes packaged artifacts that another person could immediately start filling or wiring, not just one more explanatory note.
