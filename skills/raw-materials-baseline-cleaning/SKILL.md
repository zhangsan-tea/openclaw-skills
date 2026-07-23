---
name: raw-materials-baseline-cleaning
description: Build a clean baseline trunk for archival raw materials before knowledge ingestion. Use this skill when repeatedly running non-Wiki baseline governance on a material repository, including archive extraction, cross-batch dedup, sensitive-text candidate scan, binary redaction, generic filename queueing, provenance (year×inspection) extraction, and downloadable canonical manifest output.
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
2. Extract compressed archives before scanning, so everything inside them enters the pipeline.
3. Generate dedup/sensitive/unscanned queues without destructive operations — including cross-batch dedup against materials already processed in prior runs.
4. Preserve original files while producing an action queue for human review.
5. Prepare download policy for original reports and archival attachments.

## Steps

### Step 0 — Declare target library (mandatory, every run)

Every run MUST explicitly declare which knowledge base (library) it operates on. This determines:
- The trunk hash baseline for cross-batch dedup (see Step 3).
- The provenance manifest namespace.
- The output directory naming convention.

```
INPUT (declared at start of each run):
  TARGET_LIBRARY: <library name>           # e.g. 「迎检支持专家知识库」
  TARGET_ROOT:    <repository root path>    # e.g. /Users/sanzhang/obsidian/迎检支持专家知识库/迎检材料归档
  PRIOR_RUN_DIR:  <latest _治理输出_* or _P0_clean_*>   # for cross-batch dedup; NONE if first run
```

Convention: if operating on a different library than the previous run, the trunk hash baseline MUST be rebuilt — never reuse hashes across libraries.

### Step 1 — Extract archives BEFORE scan (pipeline gate)

Archives (.zip / .7z / .rar / .tar / .tgz / .gz) MUST be extracted before any scanning, dedup, or redaction. Files inside archives are invisible to hash-based dedup and text/redaction scanners until extracted.

Procedure:
1. Recursively scan TARGET_ROOT for archive files (`*.zip *.7z *.rar *.tar *.tgz *.tar.gz`).
2. Extract each to `<archive_filename>_解包/` subdirectory (preserving internal structure).
3. Recurse into `_解包/` directories for nested archives (extract again until no archives remain).
4. Record extraction manifest: `extract_manifest.csv` (archive path → extracted file count → extracted dir path → encrypted? flag).
5. Handle encoding edge cases:
   - GBK-encoded filenames in zip: use Python `zipfile` with `info.filename.encode('cp437').decode('gbk')` decode.
   - 7z archives: use `bsdtar` (libarchive backend) — `py7zr` may fail to install in sandboxed environments.
   - Encrypted archives → flag and skip (cannot extract without password); add to `encrypted_archive_queue.csv`.
6. AFTER extraction completes, the `_解包/` directories join the scanning scope alongside the original directory tree.

**Gate rule**: do not proceed to Step 2 until all extractable archives are resolved. Extracted files are equivalent to source files for all downstream purposes (dedup, redaction, provenance).

### Step 2 — Define scope and enforce non-destructive mode

Define scan scope now covering both original files AND extracted `_解包/` contents.

- Exclude from canonical set: `_治理输出_*`, `_P0_clean_*`, `_解包` (the extraction staging dirs are included in scan but excluded from the "original canonical" classification — they are copies).
- Exclude: temporary files (`~$*`), resource forks (`._*`), `__MACOSX`.
- Do not delete or move source files in baseline pass.

### Step 3 — Baseline scan + cross-batch dedup baseline construction

#### 3a — Build trunk hash sets

Two hash sets are needed:

1. **Within-batch hash set**: all file hashes in the current scan (original + extracted). For detecting duplicates within this batch.

2. **Prior-trunk hash set**: load canonical file hashes from PRIOR_RUN_DIR's `clean_trunk_manifest.csv` or `_P0_clean_*/_redaction_output/` redacted copies. This is the **cross-batch baseline**.
   - If PRIOR_RUN_DIR is NONE (first run), there is no prior-trunk set — cross-batch dedup is skipped.
   - Prior-trunk hashes should be built from REDACTED copies when available (since the knowledge base stores redacted versions, not originals).
   - Record `prior_trunk_source` path in summary for traceability.

#### 3b — Produce governance artifacts

Output under `_治理输出_<timestamp>/`:

- `clean_trunk_manifest.csv` — canonical non-derived files with `download_policy`, **plus a `cross_batch_status` column**:
  - `NEW` — hash not found in prior-trunk set (genuinely new material).
  - `PRIOR_OVERLAP` — hash matches an existing trunk file (duplicate of already-ingested material).
  - `FIRST_RUN` — no prior-trunk set exists.
- `duplicate_candidates_raw.csv` — within-batch raw duplicates (same as before).
- `duplicate_candidates_ai.csv` — within-batch derived duplicates.
- `cross_batch_overlap.csv` — files in current batch whose hash matches prior-trunk (column: current_path, prior_run_dir, prior_canonical_path, prior_inspection_name). → Human review queue.
- `sensitive_candidates_text_scan.csv` — phone/ID/email/key-like matches.
- `unscanned_binary_queue.csv` — pdf/docx/xlsx/pptx/images pending parser/OCR.
- `generic_filename_queue.csv` — files requiring rename normalization.
- `baseline_action_queue.csv` — P0/P1/P2 integrated queue; cross-batch overlaps are routed as P0-review.
- `summary.json` and `baseline_report.md`
- `provenance_manifest.csv` — per-file `inspection_year`/`inspection_name`/`inspection_level`/`material_class`.
- `inspection_rollup.csv` — grouped counts by year×inspection.
- `按年×专项溯源索引.md` — human-readable index + year-missing gap flags.

### Step 4 — Priority routing

- **P0**: 
  - Within-batch raw duplicate review.
  - Sensitive candidates on raw materials (text + binary).
  - **Cross-batch overlap review** (NEW — these files duplicate materials already in the library; decide: skip ingest / replace / version-append).
- **P1**: Generic filename normalization; extracted-file provenance assignment.
- **P2**: Derived-material duplicates; image PDF OCR queue.

### Step 5 — MD-learning and original-download split

- Mark raw canonical files as `download_policy=required`.
- Mark `PRIOR_OVERLAP` files as `download_policy=skip` (already in library).
- Keep derived/summary content outside mandatory download set.

### Step 6 — Provenance feeds downstream querying

- `provenance_manifest.csv` is the canonical source for the 入库 Agent to write frontmatter (`inspection_year`/`inspection_name`/`inspection_level`) when ingesting into iWiki.
- Future queries (`某年某次迎检全部资料`) are answered by filtering this manifest.
- Year-missing gap (folders without year in name) must be filled by content-based inference (入库 Agent reads dates/doc numbers), with human confirmation for ambiguous cases.

### Step 7 — Safe apply mode (isolation + rollback)

When the user approves applying P0 actions:
- Create `_P0_clean_<timestamp>/` with subfolders:
  - `_dedup_quarantine/<relative_path>` — MOVE within-batch duplicate files here.
  - `_redaction_output/<relative_path>` — WRITE redacted COPIES here; originals never modified.
  - `_cross_batch_quarantine/` — MOVE `PRIOR_OVERLAP` files here (after human confirms they duplicate existing library content).
- Emit `dedup_rollback_manifest.csv`, `cross_batch_rollback_manifest.csv`, `redaction_log.csv`, `redaction_log_binary.csv`, `rollback_manifest.csv`, `pre_run_snapshot.json`.

### Step 8 — Publish baseline results

Present `baseline_report.md` + queue CSV files. Request user confirmation before any destructive follow-up batch.

### Step 9 — Verification

1. Confirm output directory includes all required artifacts.
2. Confirm `summary.json` metrics are internally consistent.
3. Confirm source repository remains unchanged (non-destructive baseline pass).
4. Confirm extracted `_解包/` contents are included in scan results.
5. Confirm cross-batch overlap report distinguishes NEW vs PRIOR_OVERLAP correctly.
6. For binary redaction: verify via negative test (Step 10).

## Redaction patterns (conservative)

- **Phone**: `1[3-9]\d{9}` → `first 3 + **** + last 4` (e.g. `138****0001`).
- **Email**: mask local part (`u***@domain`).
- **ID card**: STRICT validator (GB 11643-1999: 2-digit province code + plausible date + checksum). Only validated IDs get masked. Do NOT blanket-mask all 18-digit numbers.
- **Key-like**: only `api_key/secret/token/password/sk-...` followed by a quoted secret ≥8 chars; mask the value.

## Provenance parsing rules

- Top-level folder name → `inspection_name` (strip year prefix, `一级：` prefix, `（新）` suffix).
- Year: 4-digit prefix (`2024`) or `NN年` prefix (`25年`→2025); otherwise leave empty and flag `⚠️ 缺失，需标注`.
- Level: `一级` if name starts with `一级：`; else `常规`.
- `通用材料库/迎检材料模板/原始文件/其他检查` → `material_class=通用/模板`, `inspection_name=(通用/模板/未归类)`.
- Exclude `AI语料/` (derived mirror) and `_治理输出_*` from canonical set.

## Step 10 — Binary redaction (docx / xlsx / pptx / pdf)

Running the binary redaction pass surfaced silent-failure bugs. All three let the script report `redacted` while the PII stayed in the copy:

1. **xlsx `read_only=True` → redactions never written.** Open in writable mode (`load_workbook(path)`, fall back to `data_only=True` on error).
2. **xlsx numeric cells skipped.** Phone/ID stored as `int` are invisible to `isinstance(cell.value, str)`. Convert via `str(cell.value)`, redact, write back only when changed.
3. **docx hyperlink text missed by `paragraph.runs`.** `paragraph.runs` excludes runs inside `w:hyperlink`. Iterate all `w:t` nodes: `list(paragraph._p.iter(qn('w:t')))`, join text, redact, write result into first `w:t`, blank the rest.

### Binary verification

- **Verify by negative test**, not by mask regex shape. Confirm the original's exact 11-digit phones / emails no longer appear as standalone PHONE_RE/EMAIL_RE matches in the copy. Do NOT assert on mask shape (`138****5678`) — text-formatted cells keep a leading `'` that breaks naive mask regex.
- **Image-only PDFs**: `pypdf` returns empty text for scanned/image PDFs → route to OCR / manual review. Never assume clean.
- Always emit `redaction_log_binary.csv` + `rollback_manifest_binary.csv`.

## Pitfalls

- Do not merge boundary-broken links with true missing nodes in one batch.
- Do not treat all duplicate files as safe-to-delete; keep canonical and review context.
- Do not scan binary files as plain text and assume sensitive-clean.
- Do not execute destructive dedup without explicit user confirmation and backup.
- Do not skip archive extraction — files inside archives are invisible to all downstream scanners.
- Do not reuse a prior-trunk hash set built for library A when running against library B.
- ID-card scanning: 18-digit sequences are mostly false positives; always validate before masking.
- When rewriting `provenance_manifest.csv`, avoid creating duplicate `year_missing` columns.

## Cross-batch dedup design notes

**Where does cross-batch dedup logic live?** This skill handles hash-level detection (`PRIOR_OVERLAP`). Higher-level decisions (replace vs version-append vs skip) belong to the **入库 Agent**, not this skill. Workflow:

1. This skill produces `cross_batch_overlap.csv` → human reviews.
2. For each overlap, the 入库 Agent decides:
   - **Skip** — material is byte-identical, already in library → do not re-ingest.
   - **Replace** — new material supersedes old (e.g. updated version) → replace library copy.
   - **Version-append** — keep both with version/date metadata → add as new revision.
3. The skill's role is detection and quarantine; the Agent's role is policy.

**Why hash-level, not content-similarity?** Near-duplicates (revised docs with small changes) are out of scope for baseline cleaning. Those are handled later by the 入库 Agent's content-aware dedup. This skill catches byte-identical overlaps only — fast and zero false positives.

## Pipeline order summary

```
Step 0: Declare target library + prior run dir
Step 1: Extract ALL archives (recursive) → _解包/
   ↓ GATE: no archives remaining
Step 2: Define scope (original + _解包/)
Step 3: Baseline scan (SHA256 all files)
   3a: Build within-batch hash set + prior-trunk hash set
   3b: Produce governance artifacts (incl. cross_batch_overlap.csv)
Step 4: Priority routing (P0/P1/P2)
Step 5: MD/original split + download policy
Step 6: Provenance enrichment
Step 7: Safe apply (isolation + rollback)
Step 8: Publish results for review
Step 9: Verification
Step 10: Binary redaction (docx/xlsx/pptx/pdf) + negative-test verify
```
