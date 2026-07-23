---
name: raw-materials-baseline-cleaning
description: Build a clean baseline trunk for archival raw materials before knowledge ingestion. Use this skill when repeatedly running non-Wiki baseline governance on a material repository, including dedup candidate extraction, sensitive-text candidate scan, binary/OCR scan queue generation, generic filename queueing, provenance (year×inspection) extraction, and downloadable canonical manifest output.
description_zh: 原始材料基线清洗
description_en: Raw baseline cleaning
disable: false
agent_created: true
---

# raw-materials-baseline-cleaning

## When to use

Use this skill when a material repository (for example `迎检材料归档`) needs repeated baseline cleaning before AI ingestion, regardless of Wiki structure changes.

Trigger conditions:
1. Build a clean canonical trunk from raw files.
2. Generate dedup/sensitive/unscanned queues without destructive operations.
3. Preserve original files while producing an action queue for human review.
4. Prepare download policy for original reports and archival attachments.

## Steps

1. Define scope and enforce non-destructive mode.
   - Target one repository root (example: `/Users/sanzhang/obsidian/迎检支持专家知识库/迎检材料归档`).
   - Exclude output folders (`_治理输出_*`), temporary files (`~$*`), resource forks (`._*`), and `__MACOSX`.
   - Do not delete or move source files in baseline pass.

2. Run baseline scan and produce governance artifacts.
   - Collect all files and compute SHA256.
   - Build canonical mapping per hash (prefer non-derived files, then shorter path, then lexicographic order).
   - Output at least these files under `_治理输出_<timestamp>/`:
     - `clean_trunk_manifest.csv` (canonical non-derived files, `download_policy=required`)
     - `duplicate_candidates_raw.csv` (raw duplicate review queue)
     - `duplicate_candidates_ai.csv` (derived duplicate review queue)
     - `sensitive_candidates_text_scan.csv` (phone/ID/email/key-like matches in text files)
     - `unscanned_binary_queue.csv` (pdf/docx/xlsx/pptx/images, pending parser/OCR)
     - `generic_filename_queue.csv` (files requiring rename normalization)
    - `baseline_action_queue.csv` (P0/P1/P2 integrated execution queue)
    - `summary.json` and `baseline_report.md`
    - `provenance_manifest.csv` (per-file `inspection_year`/`inspection_name`/`inspection_level`/`material_class` — the source of truth for year×inspection attribution)
    - `inspection_rollup.csv` (grouped counts by year×inspection)
    - `按年×专项溯源索引.md` (human-readable index + year-missing gap flags)

   Provenance parsing rules:
   - Top-level folder name → `inspection_name` (strip year prefix, `一级：` prefix, `（新）` suffix).
   - Year: 4-digit prefix (`2024 ...`) or `NN年` prefix (`25年`→2025); otherwise leave empty and flag `⚠️ 缺失，需标注`.
   - Level: `一级` if name starts with `一级：`; else `常规`. `通用材料库/迎检材料模板/原始文件/其他检查` → `material_class=通用/模板`, `inspection_name=(通用/模板/未归类)`.
   - Exclude `AI语料/` (derived mirror; its provenance inherits the parallel 专项 folder) and `_治理输出_*` from canonical set.

3. Apply priority routing for action queue.
   - P0: raw duplicate review and sensitive candidates on raw materials.
   - P1: generic filename normalization and non-derived binary scan queue.
   - P2: derived-material duplicate cleanup and derived binary scan queue.

4. Keep MD-learning and original-download split explicit.
   - Mark raw canonical files as download-required.
   - Keep derived/summary content outside mandatory download set.

4.5 Provenance feeds downstream year×inspection querying.
   - `provenance_manifest.csv` is the canonical source for the 入库 Agent to write `inspection_year`/`inspection_name`/`inspection_level` frontmatter when ingesting into iWiki (so folder-based provenance survives the flattening into L1–L4 knowledge layers).
   - Future queries ("某年某次迎检全部资料" / "某资料是否属于某年某次迎检") are answered by filtering this manifest. The year-missing gap (folders without year in name) must be filled by content-based inference (入库 Agent reads dates/doc numbers), with human confirmation for ambiguous cases.

5. Publish baseline results for review.
   - Present `baseline_report.md` plus queue CSV files.
   - Request user confirmation before any destructive follow-up batch.

6. Safe apply mode (isolation + rollback) for approved P0 batches.
   When the user approves applying P0 actions (dedup move / redaction), run in an isolated, reversible folder tree. Never delete originals.
   - Create `_P0_clean_<timestamp>/` under the repository root with subfolders:
     - `_dedup_quarantine/<relative_path>` — MOVE duplicate files here (preserving relative path); canonical + non-duplicate files stay in place → clean trunk achieved without deletion.
     - `_redaction_output/<relative_path>` — WRITE redacted COPIES here; originals are never modified.
   - Emit `dedup_rollback_manifest.csv` (each moved file: src→quarantine, reverse `mv` command) and `redaction_log.csv` (per file: phone/email/idcard/key counts actually rewritten, dst path).
   - Emit `rollback_manifest.csv` (unified reverse instructions) and `pre_run_snapshot.json` (list of moved originals for integrity check).
   - Redaction patterns (conservative, avoid false positives):
     - Phone: `1[3-9]\d{9}` → keep first 3 + `****` + last 4.
     - Email: mask local part (`u***@domain`).
     - ID card: STRICT validator (GB 11643-1999: 2-digit province code in known set + plausible date + checksum). Raw 18-digit matches are ~99% false positives (hashes / case numbers); only validated IDs get masked. Do NOT blanket-mask all 18-digit numbers.
     - Key-like: only `api_key/secret/token/password/sk-...` followed by a quoted secret ≥8 chars; mask the secret value.
   - Year-missing flag: after extraction, add a single `year_missing` column to `provenance_manifest.csv` (value `YES` when `inspection_year` empty); regenerate the index with red-highlighted year-less groups. Guard against duplicate column headers when rewriting the CSV.

## Pitfalls

- Do not merge boundary-broken links with true missing nodes in one batch.
- Do not treat all duplicate files as safe-to-delete; keep canonical and review context.
- Do not scan binary files as plain text and assume sensitive-clean.
- Do not execute destructive dedup without explicit user confirmation and backup.
- ID-card scanning: 18-digit sequences are mostly false positives (file hashes, order numbers). Always validate with province code + checksum before masking; never mask blindly.
- When rewriting `provenance_manifest.csv`, avoid creating a duplicate `year_missing` column (read existing header first, then add at most one).

## Binary redaction pitfalls (docx / xlsx / pptx / pdf)

Running the binary redaction pass on real 迎检材料归档 surfaced three silent-failure bugs. All three let the script report `redacted` while the PII stayed in the copy:

1. **xlsx opened `read_only=True` → redactions never written.** `openpyxl.load_workbook(path, read_only=True)` makes cells immutable; assigning `cell.value = ...` raises `Cell is read only` and the file is logged as `ERROR` (not redacted). Open workbooks in writable mode (`load_workbook(path)`, fall back to `data_only=True` on load error) so redacted values persist.
2. **xlsx numeric cells skipped.** Phone/ID numbers stored as `int`/`float` cells are invisible to a `isinstance(cell.value, str)` guard, so they are never masked even though the scan (which stringifies `str(v)`) counted them. Convert non-string cell values with `str(cell.value)`, redact, and write the masked string back (`cell.value = s2` only when changed).
3. **docx hyperlink text missed by `paragraph.runs`.** `python-docx` `paragraph.runs` excludes runs inside `w:hyperlink`; `paragraph.text` includes them. A per-run redaction silently leaves hyperlinked emails/phones in place. Iterate all `w:t` nodes instead: `list(paragraph._p.iter(qn('w:t')))`, join their text, redact, write the result into the first `w:t` and blank the rest. (Tables are fine via `cell.text`, which already merges hyperlink text.)
4. **Verify by negative test, not by regex-shape of the mask.** After redacting, confirm the original's exact 11-digit phones / exact emails no longer appear as standalone matches (`PHONE_RE`/`EMAIL_RE`) in the copy. Do NOT assert on the mask shape (e.g. `138****5678`) — text-formatted phone cells keep a leading `'` (`'138****0001`), which breaks a naive mask regex.
5. **Image-only PDFs and archives can't be auto-redacted.** `pypdf` returns empty text for scanned/image PDFs (`pdf_image` skip) and `.7z/.zip/.doc/.png/.jpg` are not parsed. Route these to OCR / manual review; never assume them clean. Always keep originals untouched and emit a `redaction_log_binary.csv` + `rollback_manifest_binary.csv`.

## Verification

1. Confirm output directory exists and includes all required artifacts.
2. Confirm `summary.json` metrics are internally consistent (`total >= unique`, queue sizes non-negative).
3. Confirm source repository remains unchanged (non-destructive baseline pass).
4. Confirm canonical manifest includes only raw non-derived files intended for download.