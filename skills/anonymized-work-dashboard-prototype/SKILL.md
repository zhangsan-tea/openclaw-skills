---
name: anonymized-work-dashboard-prototype
description: Build a first-pass work knowledge dashboard prototype for Lee using
  only work-related content. Use when the goal is to plan or produce an HTML
  overview page that shows summary-only cards, structures, relationships, and
  timelines while strictly excluding raw records, names, and letter-based
  shorthand.
description_zh: 匿名工作看板原型
description_en: Anonymized work dashboard
agent_created: true
---

# anonymized-work-dashboard-prototype

## When to use
- The user wants a visual web page for work knowledge, work priorities, inspection preparation, knowledge infrastructure, AI application governance, or long-line structural issues.
- The page must be summary-only and must not expose raw transcripts, raw notes, original meeting records, names, or letter-based shorthand.
- The task is to create a first-pass prototype, low-fidelity page, field schema, or static HTML layout before building a richer product.
- The content scope must stay inside work-related knowledge and exclude inward-looking, coaching, mindfulness, or humanities material.

## Steps
1. Confirm the content boundary first: work-only, summary-only, no raw records, no names, no letter abbreviations.
2. Decide the page role: it should be a dashboard or overview layer, not a raw archive.
3. Structure the page into three levels: global overview, topic sections, and summary cards.
4. Use the default section set unless the user asks otherwise: homepage overview, inspection-preparation line, knowledge infrastructure, key topics, relationship structure, and stage timeline.
5. For every item, compress content into stable fields such as conclusion, basis, blockage, action, priority, and topic link.
6. If the user wants to go from content to product in one pass, do it in B→A order: first build a structured data draft (prefer JSON), then upgrade the HTML to consume that data.
7. The first HTML can stay static, but the next pass should already support light interaction such as topic filtering, card expansion, view switching, and simple relation-driven filtering, while still staying summary-only.
8. Once the user asks for something closer to a finished product, add a report-friendly layer: a summary view with "most important", "main risks", and "next actions", plus top navigation and card-to-card linking.
9. Add a companion field list or iteration note in Markdown so the data layer and the display layer remain easy to extend.
10. Before presenting, run an explicit scan on the visible page text and on the structured data strings to ensure there are no raw quotes, no names, and no letter-based shorthand in user-facing content.
11. Preview the HTML for the user and deliver the main page plus the key supporting files as attachments.

## Pitfalls
- Do not paste meeting transcripts, chat logs, or quoted source text into the page.
- Do not accidentally include names inside examples, edge cases, or placeholder text.
- Do not let the page become a material dump. It should stay at the judgment and structure layer.
- Do not mix work knowledge with coaching, inward-looking, or humanities content.
- Do not over-design the first version. A stable structure matters more than visual flourish.
- When the user explicitly bans letter-based shorthand in titles and content, do not leave English abbreviations in visible page text just because the code layer still uses them.
- When you add relation nodes or report-view shortcuts, always let them jump back to the underlying summary cards. Otherwise the page looks polished but does not help navigation.

## Verification
- The page can be read top-down as: what matters now, what is blocked, what to do next.
- No title, paragraph, badge, or placeholder contains names or letter-based shorthand.
- Every card is summary-oriented and can stand alone without the raw source.
- The supporting Markdown file is sufficient for later extension of the data-driven dashboard.
- Report-view items and relation nodes can both navigate back to their underlying summary cards.
- The visible HTML text and structured data strings both pass an explicit check for banned raw quotes, names, and letter-based shorthand.