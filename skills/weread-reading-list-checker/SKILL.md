---
name: weread-reading-list-checker
description: Check a reading list or article-derived book list against WeRead
  (微信读书), determine which titles exist in the catalog, compare them with the
  user's current shelf, and produce a clean result list of already in shelf /
  available but not in shelf / not found. Use this when the user provides a
  webpage, article, screenshot-derived list, or plain text list and wants a
  practical WeRead availability audit. This skill also handles the common
  limitation that the current WeRead agent gateway is read-only for shelf
  operations.
description_zh: 微信读书书单核查
description_en: WeRead list checker
agent_created: true
---

# weread-reading-list-checker

## When to use

Use this skill when one or more of the following are true:
1. The user gives a reading list, article link, or book recommendation post and wants to know which titles exist in 微信读书.
2. The user wants a final list of:
   - already in shelf
   - available in 微信读书 but not yet in shelf
   - not found
3. The user loosely says “把有的放书架里” and you need to first verify what the current WeRead API actually supports.
4. The source list may need preprocessing, such as extracting titles from a webpage or deduplicating an article’s recommendations.

Typical triggers:
- “帮我查这篇文章里的书，哪些微信读书有”
- “把这个书单在微信读书里对一下”
- “有的就放书架里，没有的列出来”

## Steps

1. **Load the WeRead skill first**
   - Use the existing `微信读书` skill as the authority for API format and field meanings.
   - Read `search.md` and `shelf.md` before calling the gateway.

2. **Extract the candidate book list**
   - If the source is a web article, use a fetch tool to extract explicit book titles and authors.
   - Deduplicate the list.
   - Preserve article order unless the user asks for sorting.
   - If the source includes sensitive items you cannot process, exclude them and note that one item was not processed.

3. **Check what the WeRead gateway can do right now**
   - Confirm `WEREAD_API_KEY` is set.
   - Call `/_list` to inspect available APIs before promising shelf mutations.
   - If only `/shelf/sync` is available for shelf operations, treat shelf handling as read-only.

4. **Get the current shelf**
   - Call `/shelf/sync` once at the beginning.
   - Build a set of current `bookId`s (and title map if useful) from `books[]`.

5. **Search each title**
   - For normal books, call `/store/search` with `scope=10`.
   - Prefer exact title + author matches.
   - If exact title is missing but a subtitle/edition clearly matches the requested work, mark it as a matched edition.
   - Keep the top few candidates for ambiguity handling.

6. **Classify each title**
   - `already_in_shelf`: matched title exists and matched `bookId` is already in the user shelf.
   - `available_not_in_shelf`: matched title exists in 微信读书 but `bookId` is not currently in shelf.
   - `not_found`: no credible match in the search results.
   - `needs_confirmation`: multiple plausible editions or author mismatch that you cannot resolve confidently.

7. **Handle “add to shelf” requests carefully**
   - Do not assume the WeRead gateway can write to the shelf.
   - If `/_list` shows no shelf mutation API, say clearly that current gateway access is read-only for shelf operations.
   - Only attempt browser automation if the user wants that extra step and a browser path is available.

8. **Produce a clean result memo**
   - Summarize counts first.
   - Then list titles under the four buckets above.
   - For matched-but-not-in-shelf items, include the matched edition title and author, not just the raw query text.

## Pitfalls

- Do not promise “已加入书架” before confirming the gateway actually exposes a shelf write API.
- Do not use title-only matching when the search result contains a different book with the same short title; use author to disambiguate whenever possible.
- Do not ignore subtitle editions; many legitimate WeRead matches differ only by subtitle like “xxx：副标题” or “全新升级版”.
- Do not repeatedly call `/shelf/sync` for every title; fetch shelf once and reuse it.
- Do not expose the API key or raw authorization headers in the output.

## Verification

A good run should satisfy all checks:
1. The source list is explicitly extracted and deduplicated.
2. The current shelf is fetched exactly once and used as the comparison baseline.
3. Each title ends up in one of four buckets: already in shelf / available not in shelf / not found / needs confirmation.
4. Any inability to add to shelf is explained as an API capability limit, not guessed or hidden.
5. The final output is a user-readable checklist, not raw JSON.
