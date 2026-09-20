---
name: pdf-epub-paragraph-reflow-fix
description: Fix EPUB paragraph segmentation when PDF visual line wraps were
  mistakenly converted into paragraph breaks. Use this when many paragraphs end
  without terminal punctuation, numbered list items are split apart, or readers
  show fragments like "一个攻 / 击" across separate paragraphs. Rebuild the EPUB
  from PDF with punctuation-aware reflow, preserve true headings, and generate a
  full-book self-check report.
description_zh: PDF转EPUB分段修复
description_en: PDF EPUB Paragraph Reflow Fix
agent_created: true
---

# pdf-epub-paragraph-reflow-fix

## When to use
- 用户反馈的问题不是“标题样式不对”，而是**段落本身被切碎**。
- 典型症状：大量换段前没有句号/问号/叹号；编号条目被拆成两三段；阅读器里出现“一个攻 / 击”这类明显断裂。
- 用户已经给出硬规则：**除标题外，几乎所有无结束标点的换段都应视为误切**。
- 需要从 PDF 重新生成 EPUB，并在交付前做全书自检，而不是只 patch 现有 EPUB。

## Steps
1. 先读用户截图，确认错法属于“视觉折行被误当成段落边界”，不要急着调 CSS。
2. 读取原 PDF 抽取结果，观察原始 `split('\n')` 行流，找出典型误切模式：
   - 编号条目开头的下一行仍是正文续接
   - 段尾无结束标点却被单独成段
   - 同一段跨页继续
3. 在 PDF→EPUB 脚本中重写段落合并规则：
   - 章节标题单独保留
   - 真正的小标题只在“上一段已正常结束 + 当前行够短 + 下一行像正文”时保留
   - 编号条目是段落开始，不是 heading
   - 当前段如果**没有结束标点**，默认继续拼接下一行
   - 只有遇到真正标题、下一个编号条目、或当前段已正常结束时才断开
   - `join_text()` 要显式处理中文→英文、英文→中文、数字→中文边界，避免 `在BlackBerry` 这类粘连
4. 若书里存在压平表格/对比块，先做“同页同行短文本合并”或窗口级重建，再做 paragraph-level merge，避免把表格碎片当残句。
5. 章节内再做一轮 paragraph-level merge，清掉首轮遗漏的误切。
6. 生成 EPUB 时保留较优版样式：小标题加粗留白、列表项不首行缩进、lead-in 单独处理。
7. 追加自检报告 `*_selfcheck.md`：
   - 每章段落数
   - 残留疑似误分段数
   - 疑似原书少句号例外
   - 关键片段回查
   - 页级探针命中情况
7. 抽查用户截图对应片段，确认关键错误已修复，再交付 EPUB + 报告 + 脚本。

## Pitfalls
- 不要把编号条目当标题；否则“条目首行”和“续行”会被拆开。
- 不要只靠“短句=标题”判断；要结合上下文，否则断裂正文会被误判成小标题。
- 若当前问题是分段逻辑错，继续 patch 现有 EPUB 样式只会把坏结构涂得更好看。
- 对真正缺句号的原书例外，不要强行补字；应在报告里单列为“疑似原书少句号例外”。
- 页级探针命中失败时，不一定是丢字，也可能是标题规范化（如 `1.` 前缀）导致；要做偏移 probe 回查。
- 不要把压平表格直接并入前后段落；否则自检里会出现一串假阳性“残留可疑段落”。

## Verification
- 报告中的“残留疑似分段问题”应为 0 或极低。
- 用户截图里的断裂片段要恢复为完整段落，例如：
  - `一个攻 / 击` → `一个攻击`
  - `一个僵化 / 而干瘪的能量球` → 单段
- 全书抽查至少覆盖：开头、中部、末尾、截图对应页。
- 若还剩异常，必须能明确归类为“标题”或“疑似原书少句号例外”，不能留下大量未解释的无标点断段。

## Related Skills
- 问题尚未分型、需要总控整书流程：`pdf-to-epub-book-workflow`
- 问题其实只是标题/列表样式：`epub-heading-restyle-fix`
