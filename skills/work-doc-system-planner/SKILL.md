---
name: work-doc-system-planner
description: Plan a workstream's document system when the user already has
  partial materials, scattered notes, or an existing scheme and now needs a
  structured set of documents, forms, data schemas, and internal/external
  information architecture. Use this skill to turn messy requirements into a
  layered content system, identify which items are upgrades vs new drafts, map
  documents to internal operations pages and external support pages, and produce
  a practical writing/build sequence.
description_zh: 文档体系规划
description_en: Doc system planner
agent_created: true
---

# work-doc-system-planner

## When to use

Use this skill when all or most of the following are true:
1. The user has an existing program, mechanism, team workflow, or knowledge base, and now wants to systematize the related documentation.
2. The request involves multiple document types at once, such as role descriptions, forms, templates, field dictionaries, operating manuals, or site/page structures.
3. The user is not just asking for one document, but for a **document family** or **documentation system**.
4. Or, the user is now asking to draft or revise **one anchor document** (for example a role memo, field dictionary, or IA skeleton) that is part of a larger document system you already identified.
5. Internal-use and external-use materials need to be separated, or mapped to different interfaces/sites.
6. The work may be partly sequential and partly parallel, and the user needs a recommended execution order rather than a simple linear checklist.

Typical triggers:
- “帮我把这批文档体系梳理出来”
- “哪些要新写，哪些在旧文档基础上改”
- “内部自用界面和对外支持站怎么对应”
- “先做哪些文档，后做哪些页面”

## Steps

1. **Read the latest anchor material first**
   - If the user provided a current master doc, read it before anything else.
   - If it is a `doc.weixin.qq.com` link and the workspace has `wecom-cli`, prefer the WeCom path over browser fetch.

2. **Inventory existing knowledge and artifacts**
   - Search the workspace or knowledge base for related role docs, prior memos, source notes, field lists, templates, and page prototypes.
   - Separate what already exists into three buckets:
     - reusable as-is
     - needs upgrade / rewrite
     - still missing
   - If the user is trying to return to "最基础的信息" or wants to know "手里到底有什么", add one more pass:
     - mature and can be directly挂接 / linked into the platform now
     - important but still in progress
     - not mature enough for phase one, do not design around it yet

3. **Identify the layers of the system**
   - Common layers to test for:
     - policy / role layer
     - data model / form layer
     - internal operations layer
     - external support / service layer
   - Adjust the layer names to fit the user’s actual workstream.

4. **Map every requested item to one layer**
   For each requested document/page, state:
   - purpose
   - audience
   - whether it is new or an upgrade
   - dependencies on other docs or data fields
   - where it should eventually live (doc, table, internal page, external page)

5. **Find the three earliest anchors**
   - Do not recommend writing everything in arbitrary order.
   - Identify the few items that constrain everything else, often including:
     - a role boundary document
     - a field dictionary / data schema
     - an information architecture or page skeleton

6. **Design the execution sequence**
   - Explicitly state which items can run in parallel and which must wait.
   - Prefer phased bundles such as:
     - rules bundle
     - data bundle
     - product / IA bundle
   - Explain why each bundle comes first.

7. **Produce a practical deliverable**
   - Write a concise planning memo or structured roadmap.
   - Include:
     - top-line conclusion
     - current-state diagnosis
     - proposed document family
     - internal vs external separation
     - writing/build order
     - next documents to draft immediately
   - When the user is not yet asking for a full solution but wants a reset from existing assets, prefer a memo shaped like:
     - what is already mature
     - what is still being built
     - what should be excluded from phase one
     - what internal pages need now
     - what external pages can already stand up now

8. **If the user is clearly ready, continue into drafting**
   - Do not stop at abstract planning if the user has already authorized execution.
   - Move directly into drafting the first 1–3 anchor documents.

## Pitfalls

- Do not treat “many documents” as a flat to-do list. The core task is to design the system, not just enumerate files.
- Do not mix internal operating records with external support materials. These should usually split into separate layers or views.
- Do not build page structures before clarifying the minimum field model; otherwise the UI will force rework later.
- Do not over-prescribe a fully serial sequence when the user already knows some items should progress in parallel.
- Do not create duplicate strategy docs if a solid existing anchor already exists; upgrade or extend it instead.
- Do not let not-yet-mature content (for example unfinished口径、half-filled lists, or aspirational features) hijack the whole IA. Phase one should be built around assets that already exist and can be linked or lightly整理 now.

## Verification

A good result should satisfy all checks:
1. Every requested item has been classified as new / upgrade / supporting asset.
2. The system is divided into clear layers rather than a flat list.
3. Internal-use and external-use materials are explicitly separated.
4. The response identifies the earliest anchor documents or schemas to draft first.
5. The user can immediately continue into execution without needing to reinterpret the plan.
