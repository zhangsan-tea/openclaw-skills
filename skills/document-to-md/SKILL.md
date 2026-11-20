---
name: document-to-md
description: |
  Convert office documents into AI-readable Markdown. Supports PPTX, DOCX, PDF,
  and image OCR. Self-contained with no external skill dependencies. Use when
  user needs 转成MD, 转换格式, 提取文字, PPT转文字, OCR, 文档转写, 材料入库.
agent_created: true
---

# Document to Markdown Converter

Convert office documents into structured, AI-readable Markdown files. All conversion
logic is self-contained — no dependency on external skills.

## Supported Formats

| Format | Method | Dependency |
|--------|--------|------------|
| .pptx / .ppt | python-pptx text extraction | `pip install python-pptx` |
| .docx / .doc | python-docx paragraph + table extraction | `pip install python-docx` |
| .pdf (text) | pdfplumber page-by-page extraction | `pip install pdfplumber` |
| .xlsx / .xls | openpyxl sheet-by-sheet + per-sheet CSV output | `pip install openpyxl` |
| .png/.jpg/.bmp/.tiff | pytesseract OCR (chi_sim+eng) | `pip install pytesseract Pillow` + system tesseract |

PyTorch / transformers are NOT used — all converters are lightweight and fast.

## Workflow

### Phase 1: Check Dependencies

Before conversion, verify required Python packages:

```bash
python3 scripts/extract.py --check-deps
```

Install missing packages into the active venv:

```bash
pip install python-pptx python-docx pdfplumber pytesseract Pillow openpyxl
```

For OCR (image/PDF), tesseract must be installed at the system level:

```bash
# macOS
brew install tesseract tesseract-lang
# Ubuntu
sudo apt install tesseract-ocr tesseract-ocr-chi-sim
```

### Phase 2: Batch Extraction (Raw Text — 模式三)

Run the extraction script against all target files. Use bulk mode for efficiency:

```bash
# Single file
python3 scripts/extract.py "file.pptx" -o ./AI语料/

# Batch (use shell glob or find + xargs)
python3 scripts/extract.py ./原始文件/*.pptx -o ./AI语料/ --verbose
python3 scripts/extract.py ./原始文件/*.docx -o ./AI语料/ --verbose
python3 scripts/extract.py ./原始文件/*.pdf -o ./AI语料/ --verbose
python3 scripts/extract.py ./原始文件/*.xlsx -o ./AI语料/ --verbose
python3 scripts/extract.py ./原始文件/*.png ./原始文件/*.jpg -o ./AI语料/ --verbose
```

The script:
- Auto-detects format by extension
- Skips empty/scanned content (PDF with all blank pages, images that yield under 20 chars)
- Outputs `BASENAME_AI可读.md` with YAML comment header tracking source and date (BASENAME = original filename without extension)
- **For XLSX/XLS**: also writes one CSV per sheet (`BASENAME_<sheetname>.csv`, UTF-8 with BOM for Excel compatibility). Empty sheets are skipped. The MD overview is truncated to first 200 rows per sheet; full data lives in the CSV files.
- Preserves slide structure (PPTX), heading levels (DOCX), page markers (PDF)
- Reports success/skip/fail counts per batch

Handle skips:
- **Scanned PDFs**: Report them separately; OCR of full scanned PDFs requires a different approach (page-by-page image extraction + OCR).
- **Empty DOCX**: These are template/stub files; skip without error.
- **Empty Excel sheets**: Logged in the MD overview but no CSV is written.
- **OCR failures**: Check tesseract language packs (`chi_sim` for Chinese).

### Phase 3: Quality Sampling

After batch extraction, sample 2-3 files per format:

1. Open the output `_AI可读.md` file
2. Check the first 30 lines: is the text coherent? Are there garbled characters?
3. For OCR outputs: read a paragraph and assess noise level
4. If ≥2/3 samples are acceptable, proceed. If not, investigate and re-extract.

### Phase 4: PPT Multi-Mode Generation (LLM-driven)

For PPTX files, the raw extraction (模式三) is the base. Additionally provide three
LLM-generated modes that the assistant produces by reading the raw text:

**Mode 1 — 逐页详细解读 (`_逐页解读.md`)**:
For each slide: quote the key content, then add a "解读注释" paragraph explaining
context, implications, what's missing, and connections to other knowledge.

**Mode 2 — 整体拉通阐述 (`_整体叙述.md`)**:
Synthesize a flowing narrative covering: 一句话结论 → 背景与问题 →
核心打法/解决方案 → 成效与数据 → 后续方向/待决策项.

**Mode 3 — 原始文本提取 (`_AI可读.md`)**:
Already produced by the script. Raw structural text. No LLM interpretation.

**Mode 4 — 决策摘要 (`_决策摘要.md`)**:
Executive summary format: 背景 (2-3 sentences) → 核心结论 (3-5 bullet points) →
待决策事项 (numbered list) → 主要风险 (prioritized) → 建议行动.

To generate modes 1/2/4, read the `_AI可读.md` file into context, then produce each
mode. The 4-mode naming convention matches the source file:

```
original_AI可读.md        # Mode 3
original_逐页解读.md      # Mode 1
original_整体叙述.md      # Mode 2
original_决策摘要.md      # Mode 4
```

### Phase 5: Organize Output

Mirror the original file directory structure:

```
原始文件/                      AI语料/
├── 关基检查/                   ├── 关基检查/
│   ├── 报告.pdf      →        │   ├── 报告_AI可读.md
│   └── 方案.docx     →        │   └── 方案_AI可读.md
└── 培训/                      └── 培训/
    └── 培训.pptx     →            ├── 培训_AI可读.md
                                   ├── 培训_逐页解读.md
                                   ├── 培训_整体叙述.md
                                   └── 培训_决策摘要.md
```

After conversion, produce a brief summary document naming the original and output
directories, with success/skip/fail counts per format.

### Phase 6: Cross-reference Index

When building a knowledge base, create a bidirectional index linking MD files back
to their original source files. Each output file already has a source file comment in its YAML header.
header. Optionally create a master index (`_索引_原文映射.md`) with all mappings.

## Important Notes

- Never install packages globally. Always use a venv:
```bash
python3 -m venv /path/to/venv
/path/to/venv/bin/pip install python-pptx python-docx pdfplumber pytesseract Pillow openpyxl
```
- For large batches (over 100 files), process in sub-batches by format to catch errors early.
- OCR quality depends heavily on image resolution. Screenshots of text-heavy slides
  work well; photos of documents with poor lighting will produce noisy output.
- This skill does NOT handle video, audio, or scanned PDF OCR (page-level image extraction).
  Those require separate specialized tools.
