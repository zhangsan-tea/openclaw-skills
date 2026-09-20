---
name: work-memo-version-polisher
description: Revise an existing work memo or draft into the next version when
  the user provides a current file or doc link plus delta feedback. Use this for
  “基于这个版本再推敲一下”“改成 v0.3”“把新增提醒补进去并压掉重复”类型任务， especially when the source is a
  WeCom/Tencent doc and the goal is to preserve the current structure while
  integrating new points, reducing overlap, and producing a cleaner next draft.
description_zh: 工作备忘迭代润色
description_en: Work memo version polisher
agent_created: true
---

# work-memo-version-polisher

## When to use
Use this skill when all of the following are true:
1. The user already has an existing memo,职责备忘,方案草稿, or structured draft.
2. The ask is to make a **next version** rather than write from zero.
3. The user gives delta instructions such as:
   - 增加某些提醒事项
   - 调整逻辑和结构
   - 压缩重复
   - 统一术语
   - 基于当前版本出 v0.x
4. The task needs you to keep the useful skeleton, not replace it with a brand new style.

Typical triggers:
- “基于这个版本再改一下”
- “出个 0.3 版本”
- “把这些新增点嵌进去，不要重复”
- “沿着当前结构略做推敲”

## Steps
1. **Read the current base version first**
   - If the user gives a local file, read it directly.
   - If the user gives a `doc.weixin.qq.com` link, use the existing `wecom-doc-link-reader` workflow first to get the real content.
   - If both local and remote versions exist, compare them and treat the newer one as the baseline.

2. **Extract the user’s delta list explicitly**
   - Separate the request into concrete edits, for example:
     - new reminders to add
     - overlap to remove
     - wording/terminology to unify
     - sections to keep stable
   - Do not start rewriting before this list is clear.

3. **Check nearby knowledge anchors only when they materially help**
   - Pull just enough related notes, sources, or prior drafts to support the new delta.
   - Use them to补具体动作、材料名称、流程节点、字段或边界，不要把 memo 重写成知识综述。

4. **Revise by “retain skeleton, adjust load-bearing points”**
   - Prefer keeping the current section order unless the user clearly wants a restructure.
   - Insert new points into the most natural existing section first.
   - If the user adds an operational reminder layer, consider adding one dedicated section instead of scattering the same reminder everywhere.
   - If there is too much repetition between positive duties and “what not to do”, move the prohibitions into one dedicated section and let earlier sections stay action-oriented.

5. **Write the next version cleanly**
   - Output a full next-version draft (e.g. v0.3), not a patch list unless the user asked for diff-only.
   - Keep tone aligned with the document’s real use case: memo, not制度；判断清楚，但别写成夸张官话。

6. **Give a short editorial summary**
   - Tell the user what changed in 2-4 bullets:
     - what was added
     - what overlap was reduced
     - what wording/structure changed

## Pitfalls
- Do not throw away the user’s current structure just because you can write a prettier one.
- Do not expand the draft into a long framework essay when the ask is “略做推敲”.
- Do not leave new operational reminders floating as a separate appendix if they clearly belong inside the memo’s main logic.
- Do not repeat the same prohibition in three places. If “不该干什么” exists, let it carry most of the explicit negatives.
- Do not turn a memo into a formal制度文件 unless the user explicitly asks.
- When revising from a WeCom doc, ignore sections the user told you to ignore (for example, separator lines and archived source material below them).

## Verification
A good result should satisfy all checks:
1. The next version still resembles the prior version structurally enough that the user can compare them.
2. Every user delta is either integrated or intentionally rejected with reason.
3. Repetition is lower than before, especially around negative boundaries.
4. The draft is immediately usable as the next version, not just a review note.
