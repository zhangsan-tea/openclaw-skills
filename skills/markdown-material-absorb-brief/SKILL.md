---
name: markdown-material-absorb-brief
description: Absorb a markdown source such as a page-by-page PPT interpretation,
  meeting note, or training handout into a concise working brief. Use when the
  user wants you to continue reading the next material, digest it quickly,
  retain only the durable structure, and relate it to existing project knowledge
  instead of rewriting the whole source.
description_zh: 吸收 Markdown 材料
description_en: Absorb Markdown Brief
agent_created: true
---

# markdown-material-absorb-brief

## When to use
- 用户给出一个 `.md` 文件，让你“吸收”“继续看下一个”“吃透这份材料”“先消化一下”。
- 材料本身已经是逐页解读、会议纪要、培训讲义或长文笔记，用户需要的是提炼，不是全文重写。
- 需要把新材料和已有项目判断、长期记忆或既有知识线做印证、补充、冲突识别。
- 输出应短、直接、结构化，方便后续继续吸收下一份材料。

## Steps
1. 先读用户给出的 Markdown 正文，确认它是原文、逐页解读、还是二次整理稿；如果是二次稿，要在输出里说明这一层来源。
2. 抓三类信息：
   - 材料在讲什么组织/主题/机制；
   - 最值得保留的结构件（职责、链路、分工、方法论、案例、指标）；
   - 哪些只是例子，哪些是可迁移的方法。
3. 结合当前项目记忆或已知上下文，输出三种关系：
   - 印证了什么旧判断；
   - 新补了什么结构；
   - 哪些地方仍缺图、缺数据、缺原文支撑。
4. 默认按以下顺序汇报：
   - 一句话总判断；
   - 最值得记住的 4-6 个点；
   - 对当前主线的印证 / 补充；
   - 留白或待继续看的点。
5. 如果用户显然在连续吸收多份材料，避免长篇摘要；只保留下一轮还会用到的骨架信息。
6. 完成后把本次吸收内容写入今日日志；只有当它属于长期稳定判断或项目约束时，才追加到项目 MEMORY。

## Pitfalls
- 不要把整份 Markdown 再复述一遍，尤其是已经带“解读注释”的二次材料。
- 不要把图片缺失页硬补成确定事实，应明确哪些页只是图示、文字无法完整提取。
- 不要只摘案例，要把案例背后的工作链路、组织关系、升级机制抽出来。
- 不要输出成口播稿或大段散文，应优先给可继续累积的备忘提纲。

## Verification
- 明确说明材料来源形态（原文 / 二次整理 / 逐页解读）。
- 输出中至少包含：总判断、关键结构件、印证/补充、留白。
- 用户看完后能直接决定是否继续发下一份材料，而不需要再问“这份到底重要在哪”。
