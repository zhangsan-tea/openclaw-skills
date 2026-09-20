---
name: knowledge-grounded-report-draft
description: Draft or redraft a leadership-facing report, monthly summary, or
  memo by grounding it in existing local knowledge sources such as Obsidian
  notes, meeting records, and prior analyses. Use when the user wants a concise
  decision-oriented draft that reflects accumulated context rather than only the
  current source text.
description_zh: 基于知识库的汇报稿起草
description_en: Knowledge-grounded report draft
agent_created: true
---

# knowledge-grounded-report-draft

## When to use
Use this skill when all of the following are true:
1. The user wants a report, memo, month report, weekly report, or leadership-facing summary drafted or rewritten.
2. The current source text is not enough by itself, and the draft should be enriched with prior meeting records, notes, or local knowledge-base materials.
3. The output should be concise, structured, and decision-oriented rather than a long raw digest.
4. The user especially cares about questions such as: what support was actually provided, what issues were discovered, what should leadership pay attention to, and what next-stage priorities matter.

Typical triggers:
- “结合前期资料，直接给一个建议稿”
- “按老板/副总裁口径重写这份月报”
- “把知识库里已有判断融进这版汇报”

## Steps
1. Read the current source material first and extract the existing structure: progress, risks, capability building, next steps.
2. Search the local knowledge base for adjacent evidence using focused keywords such as the project name, inspection type, organization names, role gaps, risk terms, and known bottlenecks.
3. Pull only the few notes that add real decision value, especially:
   - what support actions were actually provided;
   - what structural problems or repeated blockers were exposed;
   - what broader trend or pressure judgment has already been formed;
   - what likely next-stage checks or milestones were previously predicted.
4. Distill the findings into four buckets before drafting:
   - current support provided;
   - discovered issues / risks;
   - leadership reminders;
   - next-stage priorities.
5. Rewrite for the target audience:
   - for senior leaders, compress background and process detail;
   - keep facts, key risks, and decisions or reminders;
   - avoid slogans, concept stacking, and overbuilt symmetry.
6. If the user asks for Markdown, output a clean Markdown version directly unless a file is explicitly requested.
7. When discussing future work, separate likely high-priority items from routine capability-building items so the hierarchy is visible.

## Pitfalls
- Do not dump raw knowledge-base findings into the report; only keep material that changes the judgment.
- Do not let “external project progress” crowd out “what our team actually did.”
- Do not write long policy background sections for leadership-facing drafts unless the background changes decision-making.
- Do not repeat the same issue in both “current findings” and “trend judgment”; merge them in one place when possible.
- Do not overclaim predicted checks; mark them as judgment, priority, or likely items when certainty is limited.

## Verification
A good output should satisfy all checks:
1. A leader can quickly answer: what happened, what support we gave, what problems surfaced, and what needs attention.
2. The draft is shorter and clearer than the raw material.
3. At least 2-4 grounded insights from prior notes materially improved the draft.
4. The final structure clearly separates current situation, judgment, and next actions.
