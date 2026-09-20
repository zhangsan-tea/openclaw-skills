---
name: km-article-ingest-review
description: Read a Tencent KM article via the KM connector, extract the
  article's core ideas, compare them with the user's existing knowledge lines,
  and produce a practical ingest recommendation for Obsidian or other local
  knowledge systems. Use when the user shares a km.woa.com article and asks to
  "读一下", "学习一下", "看怎么入库", or wants source/memo/topic naming and挂载建议.
description_zh: KM文章学习入库
description_en: KM article ingest review
agent_created: true
---

# km-article-ingest-review

## When to use
- 用户给出 `km.woa.com` 文章链接，希望你读取、学习、总结。
- 用户不仅要摘要，还要你判断“怎么入库”“挂到哪条知识线”“要不要新建 topic”。
- 材料是 KM 内部文章，适合先用 KM 连接器读取，而不是网页抓取。
- 你需要把“文章在说什么”和“这篇文章对当前知识体系有什么意义”分开处理。

## Steps
1. **先读文章，不要先猜**
   - 优先用 KM 连接器读取文章详情。
   - 若用户明确要“学习”，尽量同时拿 AI 摘要和正文。

2. **抓三层信息**
   - 文章在讲什么（主题、结构、核心结论）
   - 哪些点对用户当前知识线有印证 / 补充 / 修正
   - 这篇材料更像：新闻、案例、方法论、外部参照，还是正式工作资料

3. **对照现有知识线**
   - 搜索 Obsidian / 本地知识库里与该主题最接近的 topic、source、memo。
   - 判断应主挂哪条线，哪些只做弱关联。
   - 如果现有 topic 还装得下，不要急着新建 topic。

4. **优先给“最小入库方案”**
   - 默认先给：
     - source 标题建议
     - memo 标题建议
     - 主挂 topic
     - 是否需要新建独立 topic
   - 只有在你确信后续同类材料会持续增加时，才建议新建 topic。

5. **写成可执行的备忘**
   - 输出不要停在抽象判断。
   - 至少写清：
     - 这篇文章值不值得入库
     - 为什么
     - 挂哪条线最合适
     - 不建议挂哪条线
     - 如果正式入库，文件名怎么起

6. **如果用户当场要求“直接入库”**
   - 再切换到正式落库动作：写 source / memo / topic 文件，并补最小必要关联链接。

## Pitfalls
- 不要把 KM 文章只当成普通摘要任务，用户常常真正要的是“这篇东西在我的知识体系里算什么”。
- 不要看到技术文章就马上新建 topic；很多时候它只是某条主线的外部参照。
- 不要忽略“这篇文章不该挂哪里”的判断，这和“该挂哪里”一样重要。
- 如果文章内容与用户现有工作主线弱相关，要明确说是弱关联，不要硬塞进主线。

## Verification
- 已拿到文章正文或足够完整的摘要。
- 已明确这篇材料的性质：案例 / 方法论 / 外部参照 / 正式工作资料。
- 已给出 source / memo / topic 的具体入库建议，而不是泛泛说“可以入库”。
- 若建议不新建 topic，已说明原因；若建议新建，也已说明触发条件。
