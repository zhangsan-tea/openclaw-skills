---
name: monthly-report-formatter
description: 月报排版生成器。将月报内容按"迎检支持小组阅览版"标准格式排版，生成 Word(.docx) 为主、可选 HTML 版；内置内容比对校验环节，确保排版后文字与源内容逐字一致。触发词：月报排版、月报生成、生成月报Word、月报模板、迎检月报、报告排版、内容比对校验。
agent_created: true
---

# 月报排版生成器 (monthly-report-formatter)

把月报的原始内容，按标准化的专业格式排版，输出 **Word(.docx) 为主**、可选 **HTML** 版本，并在生成前后做**内容比对校验**，确保文字逐字准确、不失真。

格式标准参照"迎检支持小组六月月报阅览版"——蓝底一级章节条、蓝竖线小标题、专业表格（表头深蓝、斑马纹、彩色状态标签）、"值得关注"浅蓝提示框、配图（自动嵌入）、落款等。

## 何时使用

- 用户要把一份月报/工作小结**排版成规范的 Word 文档**；
- 用户提供了"标准模板/样版"，希望**照着这个格式**生成新月报；
- 用户强调要**核对文字内容准确性**（内容比对 / 逐字校验）；
- 触发词：月报排版、生成月报、月报模板、迎检月报、报告排版、内容比对。

## 核心理念

**数据与排版分离**：先把月报内容整理成结构化 JSON（数据契约），再由脚本渲染成 Word/HTML。
好处：① 同一份内容可同时产出 Word 和 HTML；② 内容比对只需校验 JSON，与排版解耦；③ 换月份只改 JSON。

## 工作流程（务必按序执行）

### 第 0 步（可选但有图片时必做）：从企微文档提取图片

如果源文档是企微文档（wecom-cli 获取），且内部含有图片，先从原始输出中提取：

```bash
python scripts/extract_images.py <wecom_raw_output.txt> <output_dir/>
```

这会从 `wecom-cli doc get_doc_content` 返回的原始 JSON 输出中，自动识别 `data:image/...;base64,...` 格式的图片，解码保存为 `img_00.png`、`img_01.png` 等，同时输出 `results.json` 记录每张图片的路径和大小。

> 注意：`wecom-cli` 的原始输出文件路径可通过查看上次调用时的 tool-results 目录找到。本脚本只认 CSV/JSON 中的 base64 图片数据，不依赖 wecom-cli。

### 第 1 步：整理内容为结构化 JSON

参照 `references/sample_report_2026-06.json` 的结构，把用户的月报内容整理成 JSON。
节点 `type` 支持：

| type | 用途 | 关键字段 |
|---|---|---|
| `h1` | 一级章节（蓝底白字条，如"一、上半年迎检支持情况"） | text, children |
| `h2` | 二级标题（蓝竖线，如"（一）整体工作支持情况"） | text, children |
| `h3` | 三级标题（加粗蓝字，如"1、[公安]…"） | text, children |
| `para` | 正文段落（首行缩进） | text |
| `callout` | "值得关注"浅蓝提示框 | text |
| `note` | 右对齐灰色注释（如联系人说明） | text |
| `list` | 项目符号列表 | items[] |
| `table` | 表格（表头深蓝+斑马纹+状态标签） | caption, headers[], rows[][] |
| `figure` | 配图（如有 `image` 字段则嵌入真实图片，否则显示占位框） | caption, note, image |

- `text` 内用 `**xxx**` 标记加粗（渲染时 callout 内加粗自动变深蓝）。
- 表格单元格中若出现「已结束/进行中/一级/二级/三级/顺利通过」等词，HTML 版会自动渲染成彩色标签。
- 顶层字段：`meta`(title/period/footer)、`intro`(导语)、`sections`[]。

### 第 2 步：内容比对校验（关键，不可跳过）

在生成文档**之前**，先用基准源文本校验 JSON 文字是否准确：

```bash
python scripts/verify_content.py <report.json> --source <基准源.txt>
```

- 基准源 = 用户提供的原文（或从原文档 OCR / 提取的纯文本）。把它存成一个 .txt。
- 脚本会归一化（去空白、统一标点）后逐条比对，输出"✅全部通过"或"⚠️未匹配清单"。
- 若有未匹配项，逐条人工核对，修正 JSON 后重跑，直到通过。
- 也可先 `--dump` 抽取 JSON 全部文字，人工快速通读一遍。

```bash
python scripts/verify_content.py <report.json> --dump   # 仅抽取文字+字数
```

### 第 3 步：生成 Word（主产出）

```bash
python scripts/build_report_docx.py <report.json> <输出.docx>
```

### 第 4 步（可选）：生成 HTML（精致视觉版）

```bash
python scripts/build_report_html.py <report.json> <输出.html>
```

HTML 版能呈现 Word 做不到的渐变卡片、圆角、彩色标签，适合贴回企微文档或转 PDF。

## 运行环境

优先使用已装好 python-docx 的隔离环境：
```
/Users/sanzhang/.workbuddy/binaries/python/envs/default/bin/python
```
若缺 python-docx：`/Users/sanzhang/.workbuddy/binaries/python/envs/default/bin/pip install python-docx`

## 格式规范速查（阅览版标准）

- 主标题：居中、20pt、加粗、深蓝 `#1F4E8C`；下方汇报周期灰色小字。
- 一级章节 `h1`：蓝底白字横条（渐变，HTML 版）。
- 二级 `h2`：左侧蓝竖线 + 蓝字。
- 三级 `h3`：加粗深蓝。
- "值得关注" `callout`：浅蓝底 `#EAF1FB` + 左蓝条。
- 表格：表头底色 `#1F4E8C` 白字，数据行斑马纹 `#F5F8FC`。
- 落款：居中灰字（如"迎检支持小组 · 2026年6月"）。

## Pitfalls

- **只排版用户要求的范围**：如用户说"只要6月部分"，则忽略历史月报、收件人名单等其它材料，不要塞进去。
- **配图自动嵌入**：如果源文档（企微）内有图片，先用 `extract_images.py` 提取，然后在 JSON 的 figure 节点设 `image` 字段指向图片路径。Word 和 HTML 脚本会自动将真实图片嵌入文档。如果 figure 节点没设 `image` 字段，则显示占位框作为降级。
- **中文字体**：docx 里东亚字体必须单独设 `w:eastAsia`，脚本已用 `set_cn_font` 处理，勿改动。
- **内容比对不能省**：这是本 skill 的核心价值之一。哪怕内容看起来没问题，也要跑一遍 verify_content，把"✅通过"作为交付前置条件。
- **状态标签颜色**：涨跌/通过类默认绿色系、风险/一级默认红色系，符合中文语境（红=重点/风险，绿=通过/完成）。
