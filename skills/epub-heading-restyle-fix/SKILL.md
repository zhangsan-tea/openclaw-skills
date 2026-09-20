---
name: epub-heading-restyle-fix
description: Fix EPUB typography when heading bolding is wrong (missing bold on
  true subtitles and accidental bold on list items). Uses safe restyling on
  existing EPUB (zip-level patch) to adjust paragraph classes and CSS spacing
  without re-running heavy PDF extraction.
description_zh: EPUB标题样式修复
description_en: EPUB Heading Restyle Fix
agent_created: true
---

# epub-heading-restyle-fix

## When to use
- 用户反馈 EPUB 中“该加粗没加粗、不该加粗却加粗”。
- 已有可读 EPUB（如 v2），只需要改样式与标题识别，不想重跑 PDF→EPUB 全流程。
- 目标是：小标题加粗且上下留白，编号列表不加粗。

## When NOT to use
- 如果问题不是样式，而是**段落本身被切碎**（如“一个攻 / 击”被拆成两段、编号条目被拆断、几乎所有无句号换段都错），不要继续 patch 现有 EPUB。
- 这类情况应回到 PDF→EPUB 文本重组逻辑层修复，再重新生成 EPUB。

## Steps
1. 读取对照截图，提炼样式规则：
   - 短标题短语（如“伸展你的能量球”）→ `sub-heading`
   - 编号条目（如“一、每个人都是一个能量体。”）→ `list-item`
   - 列表引导句（如“更详细一点的阐述则是：”）→ `lead-in`
2. 在本地写一个纯 Python 脚本（仅 `zipfile/re/html`），对现有 EPUB 解包重写：
   - 遍历 `EPUB/chap_*.xhtml`，重算 `<p>` class
   - 更新 `EPUB/style/main.css` 的 `sub-heading/list-item/lead-in` 样式
3. 重新打包 EPUB，确保 `mimetype` 条目为首项且 `ZIP_STORED`。
4. 将新版本输出到 `*.epub`（建议按 v3→v4→v5 递增），必要时同步到用户常用打开路径（如 Desktop）。
5. 为避免反复沟通，追加一轮“全书自动质检”：统计 `sub-heading/list-item/lead-in` 总量，检查风险项（`sub-heading` 含句读或超长、`list-item` 非编号起始），输出 `*_qc_report.md`。

## Pitfalls
- 不要直接用“编号开头”判定为标题；编号条目通常是正文列表，不应加粗。
- 重打包 EPUB 时若 `mimetype` 不是首项且未存储模式，部分阅读器会兼容问题。
- 只改样式时优先 patch 已有 EPUB，避免重新抽 PDF 导致新断行噪声。
- 子标题阈值过宽会把正文短句误加粗；中文场景建议把 `is_subheading_text` 长度上限收紧到 18 左右，再配合“句读过滤”。
- `lead-in` 识别要结合“下一行是否编号条目”，否则会把普通冒号句误判成列表引导。
- 如果截图暴露的是“几乎所有无句号换段都错”，继续调 CSS 只会越补越乱；应立即切回 PDF 抽取脚本，把“无结束标点默认续接下一行”作为主规则。

## Verification
- 抽样检查关键片段：
  - `能量的演变` / `伸展你的能量球` 应为 `sub-heading`
  - `一、每个人都是一个能量体。` 应为 `list-item`
  - `更详细一点的阐述则是：` 应为 `lead-in`
- 在阅读器翻看截图对应页，确认：
  - 小标题加粗且上下空行
  - 列表条目不再误加粗
- 读取自动质检报告（`*_qc_report.md`），至少检查：
  - `sub-heading 风险项` 为 0 或极低
  - `list-item 风险项` 为 0
  - 抽样列表与用户截图预期一致

## Related Skills
- 问题未分型、需要先判断是结构还是样式：`pdf-to-epub-book-workflow`
- 如果实际上是整书分段逻辑错：`pdf-epub-paragraph-reflow-fix`
