---
name: tri-layer-knowledge-sampler
description: Classify a representative sample of Obsidian or work-knowledge
  materials into three knowledge layers — public corpus, rewrite buffer, and
  personal judgment — then produce a concise action-oriented sample report that
  explains why each item belongs there and what to do next.
description_zh: 三层知识库样本分层
description_en: Tri-layer knowledge sampler
agent_created: true
---

# tri-layer-knowledge-sampler

## When to use

Use this skill when the user wants to:
- pick a first batch of representative materials instead of scanning a whole vault;
- test a three-layer knowledge architecture such as public corpus / rewrite buffer / personal judgment;
- decide what can feed a WorkBuddy expert versus what should stay private;
- produce a sample classification list before doing large-scale migration or refactoring.

Typical triggers:
- “先挑 20 份示范分层”
- “哪些适合公共语料，哪些只适合我自己留着”
- “先拿一批样本跑三层知识库”
- “给我一个首批分类清单”

## Steps

1. Confirm the scope first.
   - Prefer one active workline first, such as one Obsidian vault area or one topic cluster.
   - Do not expand to all worklines unless the user explicitly asks.

2. Build a representative sample instead of full inventory.
   - Mix `topics`, `sources`, `memos`, and if relevant `entities`.
   - Aim for 15-20 items unless the user specifies another size.
   - Prefer files that are already central to the current workline.

3. Read only enough to judge the file itself.
   - Read frontmatter, title, opening sections, and any explicit sensitivity or privacy markers.
   - Do not over-read the whole vault.
   - Use existing recent outputs and memory as context when available.

4. Classify each file by the file’s current body, not by its potential future derivative.
   - `Public corpus`: stable facts, workflows, templates, cards, low-side-effect method pages.
   - `Rewrite buffer`: useful but still carrying scene residue, internal anchoring, memo voice, or organization-specific context.
   - `Personal judgment`: high-context organizational analysis, people judgment, private strategic notes, emotional or life-state notes.

5. For every item, write one next action.
   - Public corpus: keep as shared source / topic / card.
   - Rewrite buffer: split into cards, FAQ, or cleaned topics before exposing to experts.
   - Personal judgment: keep the original private; if needed, create a new derivative card instead of reusing the raw file.

6. Produce a short report with three sections.
   - One summary section listing counts per layer.
   - One table per layer: file path, why it belongs there, next action.
   - One closing section naming the 3-5 best rewrite candidates to process next.

## Pitfalls

- Do not confuse “valuable” with “shareable”.
- Do not classify by topic alone; classify by side effect, scene residue, and reuse stability.
- Do not feed raw `memos` or internal `entity` pages to public experts by default.
- Do not rewrite the whole vault when the user only asked for a sample batch.
- Do not move or delete files in this step unless the user explicitly asks.

## Verification

A good result should satisfy all of these:
- the sample size is explicit;
- every item has a clear layer and reason;
- rewrite-layer items have a concrete next action;
- personal items are clearly marked as non-public originals;
- the final report gives the next small batch to continue with, rather than opening a new full-scan project.