---
name: pdf-epub-screenshot-driven-repair
description: Repair an EPUB converted from PDF by using user-supplied
  screenshots as ground truth. Use when the converted book still has broken line
  wraps, false bold/subheadings, flattened tables, or merged blocks that need
  deterministic fixes in the conversion script before regenerating and
  rechecking the EPUB.
description_zh: EPUB截图定点修复
description_en: EPUB Screenshot Repair
agent_created: true
---

# pdf-epub-screenshot-driven-repair

## When to use
- 用户已经给了 PDF 转 EPUB 的结果，但指出仍有排版问题。
- 用户会发 1 张或多张截图，要求按截图做定点修复。
- 问题类型主要是：错误换行、误加粗、误判小标题、表格被压平成段落、列表/标题/正文粘连。
- 需要在现有转换脚本上补“确定性修复规则”，而不是手工逐章改 XHTML。

## Steps
1. **先收齐材料再启动**
   - 如果用户明确说“还有几张截图没发完”，先等全部发完再处理。
   - 不要边收图边跑长流程。
2. **进入静默执行态，不做运行请示**
   - 一旦用户已经说了“继续推进/直接做/你来处理”，后续默认直接执行。
   - 不要再用“我现在运行/继续运行/要不要运行”这类请示式表述。
   - 能用 Read/Grep/Edit 等专用工具完成的，就不要额外起 Bash。
   - 必须执行命令时，尽量把连续步骤合并成少量批次，减少客户端出现额外的运行/授权感知。
3. **读取三类输入**
   - 用户截图。
   - 当前 EPUB 自检报告。
   - 现有转换脚本与解压后的 EPUB XHTML。
4. **定位截图对应位置**
   - 先在 extracted.txt 里搜截图中的独特句子。
   - 再在解压后的 `EPUB/*.xhtml` 里定位对应段落。
   - 归类问题：段落断裂、误判 sub-heading、表格压平、列表/段落粘连。
5. **优先改脚本，不优先手改成品**
   - 在 PDF→EPUB 脚本中补规则，例如：
     - 强化 `looks_like_subheading()` 的排除条件。
     - 在 `merge_items()` 后增加 `repair_known_blocks()` 这类定点修复函数。
     - 对已知标题/表格/列表模式做正则拆分与重组。
     - 对跨多行压平的表格/区块，优先用“窗口拼接 + 关键锚点命中”来识别，不要把规则写死成固定 `i+1/i+2/i+8` 偏移。
6. **重生成新版本**
   - 升级输出文件名（如 v3 → v4），避免覆盖旧版本。
   - 重新生成 EPUB、自检报告、提取文本。
7. **解压复检**
   - 解压新 EPUB。
   - 逐个核对截图命中的段落。
   - 再抽检新增修复点上下文，防止局部修复引入新粘连。
8. **交付时说明三件事**
   - 本轮具体修了哪些类型的问题。
   - 还有哪些残留风险。
   - 交付的是哪个最终文件与对应自检报告。
9. **如果用户要求云端下载，再单独验证交付链路**
   - 大文件 EPUB 上传到文件空间后，不要把“文档页能打开”当作可下载。
   - 优先给真实可下载的附件或导出直链。
   - 若某个平台的“公开权限”看似设置成功，但回读策略没变，按未公开处理。

## Pitfalls
- 用户还没发完截图就提前启动，会浪费时间，还容易改错方向。
- 用户已明确让你继续后，还反复用“运行/继续运行”做请示，会制造额外打断，也会放大客户端的授权感知。
- 只改 XHTML 不改脚本，下一次重生成还会复发。
- `looks_like_subheading()` 过宽时，中文短句很容易被误判成小标题。
- 表格压平后常表现为多行被合成一行，需要按固定字段顺序重建 table rows。
- 不要过度依赖固定偏移量匹配压平区块；PDF 重排后，同一个表可能在不同版本里多占或少占 1-3 行，应用关键短语做弹性窗口匹配。
- PDF 页眉页脚、日期、页码要持续过滤，不然会反复混入正文。
- 新版本必须改文件名和 book id，避免和上一版缓存混淆。
- 不要把腾讯文档文件页误当公开下载链接；上传成功、权限成功、真正可下载，是三件不同的事。

## Verification
- 新 EPUB 能正常打开。
- 用户截图对应的几个问题点，在新 XHTML 中已恢复正确结构。
- 自检报告的文本长度差值、可疑段落数、可疑小标题数没有明显恶化，最好下降。
- 最终交付同时附 EPUB 与自检报告。