---
name: obsidian-post-archive-continue-brief
description: Continue an Obsidian workspace after a sensitive archive,
  migration, or directory split by doing a read-only calibration first, then
  producing a short action brief with moved-file mapping, surviving references,
  and the smallest safe next step.
description_zh: Obsidian迁出后续接简报
description_en: Obsidian post-archive brief
agent_created: true
---

# obsidian-post-archive-continue-brief

## When to use
Use this skill when all of the following are true:

1. The user says “继续”, “接着做”, “先续上”, or asks to continue previous Obsidian work.
2. The recent work involved archive / migration / directory split / de-personalization / moving sensitive materials out of the main vault.
3. You need to avoid re-running destructive file moves and instead re-anchor the current state.
4. The right next step is unclear until you inspect current references, moved-file status, and recent vault hotspots.

Do not use it when:
- the user already named exact files to edit,
- the task is a brand-new ingest,
- the user wants a full-vault scan unrelated to archive follow-up,
- the request is to actually move/delete files again right now.

## Steps
1. Confirm the active vault from `~/Library/Application Support/obsidian/obsidian.json`. Do not guess.
2. Read-only first: check `index.md`, `log.md`, the latest continuation artifact in `outputs/`, and any recent project memory note that anchors the last completed step.
3. Identify what is already finished so you do not repeat it: moved files, backup paths, placeholder files, previous link checks, or prior de-personalization rounds.
4. Run a small read-only inventory of the vault:
   - total files / markdown files,
   - recent 24h / 72h / 7d updates,
   - top-level directory heat,
   - recent hotspots that matter to the archive follow-up.
5. Inspect surviving references that still point to moved materials. Separate these two meanings explicitly:
   - original source fact,
   - current archive location.
6. Produce a short continuation brief in the workspace outputs directory. The brief should contain:
   - current calibrated state,
   - what is already done and should not be repeated,
   - moved-file mapping summary,
   - remaining reference points,
   - smallest safe next step,
   - minimal refresh set for next time.
7. If a fresh continuation brief already exists and the user says “继续” again, do NOT repeat another broad vault scan by default. Instead, read the latest brief / candidate list, inspect only the shortlisted notes, and produce the next narrow artifact (for example a per-file pre-edit task sheet or batch plan).
8. If the most recent artifact already names the exact next 1-2 files and the edit rule is already clear and narrow, skip making another planning artifact. Go straight to: read the two files, back them up, edit them, verify the keyword cleanup, then produce a short post-edit result note.
9. If a batch of source notes was just cleaned and the next step is “check old reference points”, do not rescan everything manually. Run a targeted pattern scan for the just-cleaned note IDs / old slugs across the vault, exclude the just-edited source files and auto-generated recent-update notes, then classify the hits into:
   - link-only / source-list references that can stay for now because file paths were intentionally not renamed,
   - stale prose / section headings / summary descriptors that still carry old object shells and should be queued for patching,
   - private or non-shared notes that can be left for later.
10. If the latest artifact already identifies the exact outer-layer files to patch (for example `index.md`, a `topic`, `concept`, `entity`, or `memo` page), back up those files and patch only the stale prose / section headings / summary descriptors. Preserve source paths, filename links, and evidence-chain references unless the user explicitly wants filename changes.
11. If one shortlisted file is an `entity` page and the remaining names are mostly part of that entity page’s own subject (for example the page is explicitly about one person’s role, method, or trajectory), stop after removing the clearly non-essential outer shells. Treat any deeper de-personalization as a separate page-rewrite task, not as routine reference cleanup.
12. If the next step is clearly a page rewrite on one shortlisted `entity` / `topic` page, stop micro-patching. Back up the page, replace one bounded continuous section (for example the whole front half before the first dated delta block), refresh the `updated` field if the note uses it, then verify the old section headings / old personal shells no longer match.
13. If the user immediately gives a factual correction about the just-edited page (for example role, ownership, team relationship, whether someone is a leader vs expert), do not rescan. Back up the page, patch only the wrong role / fact statements, and produce a short correction note.
14. If one page was just rewritten in a bounded way (for example the front half of an `entity` page) and the user then says “继续看后半部分”, do not reopen calibration or produce another planning artifact. Back up the same page again, rewrite the remaining bounded section, then verify the old personal shells / shorthand for that section are gone while the corrected facts remain intact.
15. If that page is now basically closed and the user chooses “go to the next similar page”, do not reopen the same page. Shortlist sibling `entity` / `topic` pages that have the same smell (team page carrying dialogue shells or person-anchored mechanism text), rank 1-3 candidates, and explicitly exclude true person-entity pages whose subject is inherently a person.
16. If a candidate list was just produced, the rank-1 next page is already clear, and the user answers with a simple confirmation like “继续”, “好，继续”, or chooses the first option, do not rerun ranking. Back up that rank-1 page directly, rewrite the bounded mechanism-heavy sections, then verify the old dialogue shells / person anchors are gone.
17. Prefer “queue the next batch” over editing many source notes immediately. Only start a new edit/migration round if the user explicitly wants it or the next step is obviously safe and narrow.

## Pitfalls
- Do not re-run file moves just because the user said “继续”.
- Do not confuse historical provenance with current storage location.
- Do not treat placeholder-file mtime changes as new business knowledge.
- Do not default to a full-vault scan if a small calibration already reveals the next step.
- Do not batch-edit many source notes before first producing a clear continuation brief.
- If a continuation brief or candidate list was just produced in the previous step, do not rescan the whole vault again unless the state may have changed materially.
- If the previous result already fixed the exact next files and edit boundaries, do not waste a turn on another queueing artifact. Narrow the scope, back up first, edit directly, and verify with targeted keyword checks.
- During reference-cleanup follow-up, do not treat every hit as a problem. Separate file-path links and source lists from genuinely stale prose, otherwise you will create unnecessary churn because the filenames were intentionally preserved.
- When patching outer-layer references after a scan, do not rewrite evidence-chain links or `sources:` lists just because the visible summary text changed. Usually only the prose shell, section title, and shorthand need patching.
- If an `entity` page still contains many person names because the page itself is about that person’s role/history, do not keep sanding it down indefinitely. Once the obviously non-essential shells are gone, stop and classify the next step as a page rewrite or reframing task.
- Once the task is classified as a page rewrite, do not spend more turns on scattered one-line edits. Rewrite one bounded section cleanly, update metadata if needed, and verify by old-heading / old-shell patterns.
- If the user then gives a small factual correction to that rewritten page, do not reopen the broader rewrite flow. Treat it as a narrow fact patch on the same page.
- If the user then says "继续看后半部分" on that same page, do not rescan or re-queue. Treat it as the second bounded rewrite on the same file: back up again, replace the remaining section, and verify that the section-specific old shells are gone while the earlier fact corrections still stand.
- If that page is already closed and the user chooses the next similar page, do not keep polishing the finished page. Rank sibling team/topic pages, exclude person-entity pages, and recommend the smallest next rewrite target.
- If that candidate ranking is already done and the user simply confirms to continue, do not run the ranking again. Treat it as authorization to back up the rank-1 page and start the bounded rewrite directly.

## Verification
- Active vault was confirmed from config.
- The calibration pass was read-only.
- The brief clearly distinguishes completed work vs pending work.
- Moved-file mapping and surviving references are both listed.
- The output recommends one smallest safe next step instead of a vague backlog.
- The brief includes a minimal refresh set so the next continuation does not need another broad scan.
