---
name: inspection-kb-signal-review
description: Read an inspection-related source package (WeCom doc, screenshot
  table, or notes), combine it with Obsidian knowledge base context, and extract
  what the new material verifies, corrects, and supplements from the perspective
  of the support team or strategy team.
description_zh: 检查材料知识库信号复盘
description_en: Inspection KB signal review
agent_created: true
---

# inspection-kb-signal-review

## When to use
Use this skill when Lee sends one or more discussion materials, screenshots, tables, or doc links about inspections, compliance reviews,专项、迎检、监管沟通 or similar topics, and wants a knowledge-backed answer focused on:
- what the new material **verifies** from existing knowledge;
- what it **corrects / rewrites**;
- what it **supplements**;
- what the support team should pay attention to from an organizational or tactical perspective.

Typical triggers:
- “老规矩，学习一下验证的、纠正的和补充的信息是什么”
- “结合知识库看看这份检查材料值得注意什么”
- “从迎检支持小组角度，有哪些值得关注的问题点”

## Steps
1. Read the user-provided material first. If there is a screenshot path, use the file read tool on the image rather than guessing from prose.
2. If a `doc.weixin.qq.com` link is provided, prefer the WeCom reading workflow. If the doc export is blocked by expired permission, show the `help_message` verbatim and continue with any readable screenshot/table material plus existing knowledge.
3. Search the Obsidian work vault for the closest topic/source/concept notes. Prioritize topic pages and the most recent source notes tied to the same inspection type.
4. Separate the answer into three buckets whenever possible:
   - **验证 / 印证**: existing judgments that the new material strengthens;
   - **纠正 / 改写**: old understandings that need to be narrowed, expanded, or rewritten;
   - **补充 / 新增**: genuinely new operational or structural signals.
5. If the user asks from a team perspective, rewrite the findings as “what the support group should watch”, not just “what happened in the project”.
6. Pull out cross-cutting issues such as:
   - interface instability / missing PA;
   - regulator-style differences;
   - repeated check + 回头看 + 复测 chains;
   -口径一致性;
   - whether the support team is slipping into arbitration rather than support.
7. End with a short “我会收成哪几条” summary that Lee can reuse upward.
8. Update project memory with the inspection topic, what materials were used, and the distilled judgment.

## Pitfalls
- Do not stop at summarizing the material; the task is to compare against the knowledge base.
- Do not merge “验证” and “补充” into one vague pile.
- Do not overfit to one project line; pull out the structural pattern across check types.
- Do not ignore screenshots/tables just because a doc link exists.
- If the doc export is blocked, do not hide the blocker; show the exact help text and then continue with what is available.

## Verification
- The answer explicitly distinguishes verification, correction, and supplementation when the material supports that structure.
- The answer is anchored in both the new material and at least 2-3 relevant Obsidian notes.
- The final output is written from the support team / strategy team perspective rather than as a flat meeting summary.
- If a WeCom permission blocker occurred, the exact help message was shown verbatim.
