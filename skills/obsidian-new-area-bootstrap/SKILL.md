---
name: obsidian-new-area-bootstrap
description: Bootstrap a new domain area under the user's Obsidian root when
  they want a fresh long-term knowledge region outside existing vault areas,
  with a minimal LLM+wiki structure for ongoing ingestion and later comparison.
description_zh: Obsidian新区域初始化
description_en: Obsidian new area bootstrap
agent_created: true
---

# obsidian-new-area-bootstrap

## When to use
Use this skill when the user wants to start a new long-term knowledge area under their Obsidian root, outside existing regions such as work, inner-life, or other established vaults, and wants a clean structure ready for LLM+wiki accumulation.

Typical triggers:
- “再建一个区域”
- “单独开一个 Obsidian 区域 / 库 / 主题区”
- “这个领域以后会持续丢信息进来，你先帮我搭好结构”
- education/school selection, family projects, new research tracks, or other ongoing domains that should not be mixed into existing work/personal vaults.

Do not use it for:
- adding one more note inside an existing topic,
- temporary scratchpads,
- cases where the user explicitly wants to keep the material inside an existing vault area.

## Steps
1. Read `~/Library/Application Support/obsidian/obsidian.json` and inspect the existing Obsidian root structure first. Do not guess where the new area should live.
2. Confirm whether the user wants a truly separate area outside the existing ones. If the instruction is clear and low-risk, proceed without re-asking.
3. Choose an information-dense, future-proof folder name under the Obsidian root. Prefer something slightly broader than the immediate subtask so the area can grow.
4. Create only the minimal directory skeleton needed for LLM+wiki use, usually:
   - `wiki/topics/`
   - a raw/source folder such as `课程摘要/<主题>/`
   - a memo folder such as `组织分析/<主题>/`
5. Create an `index.md` that states scope, current focus, directory roles, and a few usage rules.
6. Create a primary topic note under `wiki/topics/` with:
   - theme boundary,
   - three-layer ingest rule,
   - stable collection fields,
   - current open questions,
   - later comparison dimensions.
7. If the user has not yet provided enough samples for judgment, create only a light placeholder memo note rather than forcing a full analysis note.
8. Re-read the created notes briefly and ensure paths, wording, and note roles are coherent.
9. Record the created area and paths in project memory so later sessions know where to keep storing the new domain.

## Pitfalls
- Do not overbuild the area with too many empty notes or heavy templates; keep it light.
- Do not mix the new domain into existing work or inner-life vault areas if the user explicitly wants separation.
- Do not name the area too narrowly if the topic may expand beyond the first sub-problem.
- Do not jump to comparison judgments before enough samples exist.
- Do not touch `.obsidian/` settings unless the user explicitly asks to register or switch vaults.

## Verification
- The new area is created under the correct Obsidian root.
- The structure is minimal but sufficient for raw/topic/memo accumulation.
- `index.md` clearly explains what belongs there.
- The topic note contains reusable collection fields and open questions.
- The memo side is only a placeholder if evidence is still thin.
- Memory notes capture the area name and main paths for later continuation.
