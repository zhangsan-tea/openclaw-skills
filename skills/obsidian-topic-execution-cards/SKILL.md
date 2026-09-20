---
name: obsidian-topic-execution-cards
description: Turn a newly ingested Obsidian source/topic update into a small set
  of reusable execution cards under wiki/topics, then wire them back into the
  parent topic, index, and log. Use when the user wants practical cards such as
  coordination cards, judgment cards, response cards, or checklist-style
  subpages rather than another long memo.
description_zh: Obsidian主题执行卡
description_en: Obsidian Topic Execution Cards
agent_created: true
---

# obsidian-topic-execution-cards

## When to use
Use this skill when all of the following are true:
1. A work-related note has already been ingested into the Obsidian vault, or an existing topic has just gained a meaningful new increment.
2. The user now wants that material compressed into practical reusable cards, not more source summaries.
3. The cards should live as long-lived subpages under `wiki/topics/`, typically named `{主topic}_{子卡名}.md`.

Typical triggers:
- “把这份材料压成几张可执行卡”
- “做成协调卡 / 判断卡 / 口袋卡 / checklist”
- “A” after offering a next step like “把材料继续压成可问答卡 / 协调卡”
- After a routing / judgment card already exists, the user asks for a practical companion such as a minimal label schema, field table, or route-metadata card that makes the rule operational

## Steps
1. Read `AGENTS.md`, the parent topic, the latest related source/memo, and relevant `index.md` / `log.md` snippets.
2. Decide the minimum card set. Prefer 2-5 cards. Each card must solve a different action problem, e.g.:
   - coordination card
   - judgment / triage card
   - response / wording card
   - checklist / pocket card
   - companion schema card such as a minimal field table / label schema when the user wants the judgment rule to become a reusable tagging standard
3. Create each card under `wiki/topics/` with informative names like:
   - `2026关基检查跟踪_企业IT共性支持协调卡.md`
   - `2026关基检查跟踪_测试接入点协调卡.md`
4. In each card:
   - add YAML frontmatter with `type: topic`
   - link back to the parent topic and key source/memo
   - state what problem the card solves
   - separate “适合做 / 不适合做” or “建议说法 / 不建议说法” when relevant
   - end with a one-sentence conclusion
5. Update the parent topic, usually by:
   - bumping version if the topic meaningfully advances
   - adding a short section that introduces the new cards and when to use them
   - linking the new subpages in `related:` or the new section
6. Update `index.md` so the parent topic line reflects the new execution-card layer. Add indented bullets for the new subpages when helpful.
7. Append a `log.md` entry. This is an ingest-like knowledge-structure update, not just a note edit.
8. Present the newly created card files to the user, and summarize what each card is for.
9. Also append a brief workspace memory note capturing the new card set and what execution stage it represents.

## Pitfalls
- Do not create a new top-level topic if the material clearly belongs to an existing main axis.
- Do not write another source-like summary and call it a card. Cards must be directly usable.
- Do not mix multiple action problems into one bloated card if they have different owners or decision logic.
- Do not forget to update the parent topic and `index.md`; otherwise the cards become orphan pages.
- Do not present modified existing files as deliverables; present the newly created card files.
- If the user wants the card to be truly reusable for future intake, do not stop at the routing rule itself — consider whether a companion minimal-field table is needed so future materials can be tagged consistently instead of relying on prose memory.

## Verification
- The new cards exist under `wiki/topics/` and are linked back to the parent topic.
- The parent topic mentions the new cards and their purpose.
- `index.md` and `log.md` are updated.
- The user can understand, from your summary alone, which card to use for which situation.
