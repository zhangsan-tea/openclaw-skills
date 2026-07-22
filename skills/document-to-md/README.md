# document-to-md

办公文档 → AI 可读 Markdown，一键转换，零外部 Skill 依赖。

## 支持的格式

| 格式 | 方法 | 额外产物 |
|------|------|---------|
| PPTX / PPT | python-pptx | — |
| DOCX / DOC | python-docx | — |
| PDF（文本型） | pdfplumber | — |
| XLSX / XLS | openpyxl | 每 sheet 一个 CSV |
| PNG / JPG / BMP | pytesseract OCR | — |

## 安装

```bash
pip install python-pptx python-docx pdfplumber openpyxl pytesseract Pillow
brew install tesseract tesseract-lang   # macOS OCR 可选
```

## 使用

```bash
python3 scripts/extract.py "材料.pptx" -o ./AI语料/      # 单文件
python3 scripts/extract.py ./原始文件/*.xlsx -o ./AI语料/  # 批量
python3 scripts/extract.py --check-deps                   # 检查环境
```

## 输出

- `原文件名_AI可读.md` 含 `<!-- source: -->` 头部标注
- Excel 额外输出 `原文件名_<sheet名>.csv`（UTF-8 BOM，Excel 双击直显中文）
