---
name: image-strip-to-office
description: Convert a narrow image-based strip or flight-strip style screenshot
  into editable Office outputs with layout restoration. Use when a user wants
  the visible content reconstructed into Word, PowerPoint, or spreadsheet files
  while keeping proportions close to the original strip.
description_zh: 图片条转Office
description_en: Image Strip to Office
agent_created: true
---

# image-strip-to-office

## When to use
- 用户给的是一张横向长条图片、航班条、票据条、设备条、截图表格条。
- 用户要的不是单纯 OCR 文本，而是 Word / PPT / Excel 这类 Office 文件。
- 需要尽量还原原图比例、边框分区、合并单元格、重点字号，而不是只给纯文本。

## Steps
1. 先读取图片，确认是否只有一张，避免在用户还要继续发图时提前开工。
2. 提取可见字段，先做一版结构化结果，明确哪些数字或符号是“按可见内容最佳识别”。
3. 用 Pillow 估算有效内容区域的宽高比：不要直接拿整张手机截图比例，要尽量定位真正的条状主体区域。
4. 生成 Excel：优先做两层输出——一层版式还原，一层结构化提取，便于后续复核。
5. 生成 Word：用横向页面、表格合并单元格、固定列宽和行高来还原版式；必要时加一页原图参考。
6. 生成 PPT：用表格或文本框重建布局，按条状主体宽高比控制整体尺寸；必要时单独加一页原图参考。
7. 在交付说明里明确哪些地方是模糊识别，避免用户误以为全部是高置信结果。
8. 完成后把文件放进工作区 outputs/，并更新项目记忆。

## Pitfalls
- 不要把整张手机截图比例当成主体比例，顶部状态栏和大面积黑边会误导尺寸。
- 图片模糊时不要装作识别很准，要在文件里或说明里保留“不确定”标记。
- 只做图片嵌入不算真正转换；如果用户要 Office 文件，优先给可编辑结构。
- Word 和 PPT 的表格边框、合并单元格行为不同，不能指望一份逻辑直接复制过去不调。

## Verification
- 检查输出文件能正常打开。
- 检查主标题、关键数字、右侧标签是否落在正确分区。
- 检查整体宽高是否接近原条状主体，而不是被拉成普通表格。
- 检查最终回复是否点明了模糊识别处和输出文件路径。
