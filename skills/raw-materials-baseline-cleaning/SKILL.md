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

## Pitfalls

- Do not merge boundary-broken links with true missing nodes in one batch.
- Do not treat all duplicate files as safe-to-delete; keep canonical and review context.
- Do not scan binary files as plain text and assume sensitive-clean.
- Do not execute destructive dedup without explicit user confirmation and backup.

## Verification

1. Confirm output directory exists and includes all required artifacts.
2. Confirm `summary.json` metrics are internally consistent (`total >= unique`, queue sizes non-negative).
3. Confirm source repository remains unchanged (non-destructive baseline pass).
4. Confirm canonical manifest includes only raw non-derived files intended for download.