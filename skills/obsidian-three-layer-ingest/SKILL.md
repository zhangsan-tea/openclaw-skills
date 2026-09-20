---
name: obsidian-three-layer-ingest
description: Ingest a work-related source into an Obsidian vault using a stable three-layer pattern: raw/source note for traceability, topic note for ongoing aggregation, and memo note for transferable judgment. Use when the user wants material formally stored in Obsidian rather than only analyzed in chat.
description_zh: Obsidian三层入库
description_en: Obsidian three-layer ingest
agent_created: true
---

# obsidian-three-layer-ingest

## When to use
Use this skill when the user wants a work material, interview transcript, meeting note, competitor signal, or research fragment formally written into an Obsidian vault, and the right structure is:

1. raw/source note for the original material or structured extract,
2. topic note for ongoing aggregation and comparison,
3. memo note for portable judgment.

Typical triggers:
- “按这个理解入库”
- “写进 Obsidian / 知识库”
- “给我按 raw / topic / memo 落一下”
- Competitive intelligence, inspection/迎检, strategy, organizational analysis, or other work notes that should become reusable knowledge instead of isolated chat output.

Do not use it for:
- purely personal journaling,
- one-off casual notes with no lasting value,
- tasks where the user only wants analysis but explicitly does not want files created.

## Steps
1. Confirm the active vault from `~/Library/Application Support/obsidian/obsidian.json` or other explicit user instruction. Do not guess the vault.
2. Locate existing relevant topic notes before writing. Search for the core topic name and related notes to avoid duplicating an established topic.
3. Decide the three-layer shape:
   - raw/source: preserve provenance, scope, caveats, and structured facts;
   - topic: integrate into the ongoing axis with sections like new facts, confirmations, conflicts, and open questions;
   - memo: distill the portable judgment only when there is enough signal.
4. Choose concrete paths that match the vault’s existing organization. For work vaults, common destinations are:
   - `课程摘要/...` or `组织分析/...` for source and memo,
   - `wiki/topics/...` for topic pages.
5. If needed, create missing subdirectories under existing parent directories. Avoid touching `.obsidian/`.
6. Write the notes directly as Markdown files. Keep titles information-dense: include object/case, main axis, and why the note is worth saving.
7. In the topic note, add stable observation fields instead of freeform dumping. For inspection-facing material, prefer fields such as question asked, first answer, follow-up, restatement, expert explanation, proof, exposed weakness, and underlying structural issue.
8. Re-read the created notes briefly to catch broken internal links, obviously wrong paths, or structural drift.
9. Record the ingest result in project memory or daily log so the next session can continue from the written notes.

## Pitfalls
- Do not mix multiple companies or themes into one raw note if one company is clearly the main sample and others are only comparison signals.
- Do not let the topic note become a chat transcript dump. It should hold stable columns and evolving judgment.
- Do not create a memo for every source. Memo is for portable judgment, not repetition.
- Do not over-index on material lists when the real value lies in questioning, restatement, explanation, and proof structure.
- Do not guess vault paths or note locations when the vault config or existing structure can be read directly.
- Do not dismiss official blank templates, zip attachment packs, or mostly-unfilled xlsx sheets as “empty” before inspecting sheet structure, sample rows, dropdown dictionaries, and hidden data sources. In inspection/compliance work, those files often reveal the regulator’s object model and minimum preparation units even when business values are missing.

## Verification
- The vault path is confirmed, not guessed.
- The raw/source note preserves provenance and caveats.
- The topic note clearly updates an ongoing axis instead of duplicating a standalone summary.
- The memo note contains judgment, not just summary.
- Paths and wikilinks match real files in the vault.
- Project memory reflects what was written and where.
