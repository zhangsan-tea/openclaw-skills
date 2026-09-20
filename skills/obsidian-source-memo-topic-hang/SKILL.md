---
name: obsidian-source-memo-topic-hang
description: Ingest a newly provided work material into an existing Obsidian
  knowledge axis by creating a structured source note, writing an analysis memo,
  and hanging both back onto the most relevant existing topic pages without
  starting a new framework.
description_zh: Obsidian材料挂轴入库
description_en: Obsidian source-memo-topic hang
agent_created: true
---

# obsidian-source-memo-topic-hang

## When to use

Use this skill when all of the following are true:
1. The user provides a new document, article, meeting note, or exported markdown to be learned or ingested.
2. There is already an existing Obsidian topic line for the subject.
3. The goal is not to create a brand-new theme, but to hang the new material back onto the existing source / memo / topic axis.
4. The work should preserve Lee's usual style: no flat duplication, no framework inflation, emphasize what is new, what is same-source refresh, and what is truly additive.

Typical triggers:
- “按前面的方式入库”
- “挂到既有 topic/source/memo 轴里”
- “学习一下，放回已有 Obsidian 里”
- “不要另起新框架，接回原来的线”

## Steps

1. **Read the material first**
   - If the user gives a `doc.weixin.qq.com` link, load `wecom-doc-link-reader` first and get the real markdown content.
   - If the material is already local, read the exported markdown / source file directly.
   - Do not start writing before you know the material's actual structure and main claims.
   - If the material is a meeting summary, speech transcript, or other ASR-derived secondary draft, first capture any user-confirmed noun corrections (person names, product names, platform names, project names). Write the corrected form into the source and memo, and explicitly note that it was an ASR correction when relevant.

2. **Find the existing axis**
   - Search the relevant vault for existing topics, sources, memos, and concepts around the same subject.
   - Prefer the current main topic page over older scattered notes.
   - Decide whether the material belongs under one topic or should be cross-tagged to two nearby topics.

3. **Classify the material before writing**
   - Decide whether it is:
     - a **new source**,
     - a **same-source refresh** of an existing note,
     - a **memo-only signal** that does not deserve a new source,
     - or a **topic-level update** only.
   - If it is mostly a new example of an existing pattern, do not pretend it is a new theory.

4. **Create or update the source note**
   - For a new source, create a note under `wiki/sources/` with an informative filename and title.
   - Keep the source structured rather than verbatim-dumping everything.
   - Preserve the most decision-useful content: background, key structure, scenarios, mechanisms, constraints, engineering lessons, and why it matters.
   - Add frontmatter with at least: `type`, `title`, `created`, `event_date` when known, `tags`, `related_topic`, `sensitivity` when relevant.

5. **Write the analysis memo**
   - Create a memo under `wiki/memos/` when the material has cross-source value.
   - The memo should answer:
     - what this material confirms,
     - what is actually new,
     - what it corrects or narrows,
     - and what it changes in the knowledge-line structure.
   - Do not repeat the source. Compare it to existing notes.

6. **Hang it back to the topic pages**
   - Update the most relevant topic's `sources` list and one short descriptive bullet in the appropriate subsection.
   - If the material is clearly cross-topic, also update the second topic page.
   - Only bump the version note when the material changes the topic in a meaningful way.

7. **Keep Lee's bias checks active**
   - No new framework unless the material truly introduces one.
   - Prefer “frontline sample / concrete increment / engineering lesson” over inflated abstraction.
   - If the material is just another example of the same judgment, label it as confirmation, not a breakthrough.

8. **Finish with memory**
   - Append a concise note to the project's dated memory file stating what was ingested, where it was hung, and what the real increment was.

## Pitfalls

- Do not create a new topic page when an existing one already fits.
- Do not dump the entire source verbatim into Obsidian if a structured source note is enough.
- Do not confuse a new example with a new concept.
- Do not skip the memo when the material has cross-source interpretive value.
- Do not update only the source note and forget to hang it back to topic pages.
- When the material is same-source refresh, prefer updating the existing source instead of making duplicates.

## Verification

A good run should satisfy all of these:
1. The new material is stored as either a new source or a justified refresh of an existing source.
2. A memo exists when the material adds interpretive value beyond raw content.
3. At least one relevant topic page now links to the source and reflects the new increment.
4. The final summary states clearly whether the material was a new framework, a same-source refresh, or a frontline sample.
5. The project memory note records the ingestion result and why it mattered.