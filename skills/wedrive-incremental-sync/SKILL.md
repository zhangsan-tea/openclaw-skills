---
name: wedrive-incremental-sync
description: Compare a WeDrive archive directory with the canonical Obsidian archive, detect genuinely new or modified materials despite divergent folder names, exclude WeDrive placeholder markers, produce a non-destructive triage ledger, and route confirmed materials into redaction and incremental knowledge-base ingestion.
description_zh: WeDrive 增量比对与入库
description_en: WeDrive incremental sync
disable: false
agent_created: true
---

# wedrive-incremental-sync

## When to use

Use this skill whenever `迎检材料归档` must be periodically synchronized from the WeDrive source of truth into the local canonical archive, especially when the two sides use different folder names or when the source contains `.WeDrive` placeholder markers.

This workflow is non-destructive: it never modifies or deletes source originals during comparison or triage.

## Steps

1. Declare the scope before scanning:
   - `SOURCE_ROOT`: the WeDrive `01 迎检材料归档` directory.
   - `TARGET_ROOT`: the local `迎检材料归档` canonical original layer.
   - Exclude `AI语料/` and governance output directories beginning with `_` from the local canonical inventory.
   - Keep source originals untouched.
2. Build inventories on both sides with file size and relative path. Exclude `.DS_Store`; do not rely on mtime because WeDrive synchronization can touch the whole tree.
3. Compare using `(basename, size)` rather than full paths. Classify rows as:
   - `matched`: same basename and size;
   - `modified`: same basename but different size;
   - `new`: basename absent from the local inventory.
   This avoids false positives caused by divergent folder taxonomies.
4. Verify suspected no-extension rows before any ingestion. Treat files named `.WeDrive` and `WeDrive` as synchronization placeholders/markers. Recount real new materials after excluding them.
5. Generate a non-destructive triage CSV with at least: source size, relative path, basename, extension, source existence, stage, and decision. Recommended stages:
   - `placeholder`: exclude;
   - `tool_metadata`: exclude temporary tool metadata such as `.playwright-cli`;
   - `material_candidate`: office/PDF/text/archive formats needing content review;
   - `image_review`: image or scan needing human/OCR review;
   - `manual_review`: unknown type or ambiguous item.
6. Review material candidates at content level and assign `new`, `revision`, or `irrelevant`. Do not equate “new to local” with “must enter the AI corpus”; historical or duplicate-context materials require judgment.
7. For approved AI-corpus items only, create redacted copies and `_AI可读.md` companions. Never alter originals. Apply the repository’s redaction rules and keep source/original download paths separate from AI corpus paths.
8. Decide graph operation based on structure, not file count:
   - new evidence under existing inspection modules → incremental ingestion/update;
   - new inspection or changed check-item definition → review whether a graph module update or retraining is required.
9. Persist a run ledger under a gitignored governance output directory, including the raw inventory comparison, verified new list, triage CSV, summary JSON, and a dated report. Use the latest ledger as the baseline for the next run.

## Pitfalls

- Do not compare full paths: WeDrive and Obsidian folder taxonomies diverge.
- Do not use mtime as a freshness signal.
- Do not ingest `.WeDrive` or `WeDrive` markers; they are not business materials.
- Do not print sensitive filenames or directory names into chat when content interception blocks them. Keep detailed lists in the gitignored governance output and report aggregate counts.
- Do not treat all new files as knowledge-base candidates. Separate source-of-truth originals, AI corpus derivatives, and iWiki publishable material.
- Do not redact in place or delete originals. Redaction and quarantine require isolated copies and explicit approval for any destructive action.
- Image-only PDFs and scans require OCR/manual review; an empty text extraction is not proof of being clean.
- Do not trigger a full graph retrain merely because new files arrived; first check for new modules or changed inspection semantics.

## Verification

After each run, verify:

1. The source inventory count, target inventory count, and matched/modified/new totals reconcile.
2. Every excluded placeholder is identified by its marker name and no real material is classified as a placeholder.
3. Every real candidate path exists in `SOURCE_ROOT`.
4. The triage stage counts sum to the total comparison rows.
5. The target repository remains unchanged during comparison/triage.
6. Governance outputs are under the ignored archive layer and are not published to iWiki until a separate desensitization review passes.
