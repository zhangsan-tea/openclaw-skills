---
name: obsidian-topic-cross-tagger
description: Curate a new cross-cutting topic in an Obsidian vault, identify
  existing notes that belong to it, apply a shared tag to well-structured wiki
  notes, and produce a review memo that separates directly tagged notes from
  indirectly related or pending materials.
description_zh: Obsidian 跨主题打标整理
description_en: Obsidian cross-topic tagging
agent_created: true
---

# obsidian-topic-cross-tagger

## When to use
- 用户提出一个新的上位主题，例如“AI应用方法论”“工作系统设计”“个人AI工作流”，希望把分散在 Obsidian 里的材料重新收口。
- 用户要求“看看哪些材料也属于这条线”“给这些材料打同一个标签”“允许多标签，不想硬搬目录”。
- 目标是做**跨主题归拢**，不是重写全部笔记，也不是做一次性搜索列表。

## Steps
1. **先界定主题边界**
   - 用一句话说清这个新主题到底收什么、不收什么。
   - 把主题拆成 3-5 条子线，例如：个人工作法、产品/工作系统、工程化落地、组织转型、知识基建。

2. **盘点候选材料**
   - 优先搜索 Obsidian 的 `wiki/topics`、`wiki/sources`、`wiki/memos`，再看课程摘要、历史档案、输出区草稿。
   - 不要只按“AI”关键词硬搜；同时搜 `Agent`、`工作流`、`知识库`、`AI4SE`、`组织转型`、`产品设计` 等语义相关词。
   - 区分三类：
     1. 直接属于新主题、适合马上打标签；
     2. 相关但更像旁支，只适合挂关联；
     3. 目前只是外部草稿/旧档案，先纳入 topic，不急着改原文件结构。

3. **创建或更新总入口 topic**
   - 在 `wiki/topics/` 下新建或更新一个 topic 页。
   - topic 页至少包含：主题边界、子线拆分、多标签原则、当前主干材料、待补方向。
   - 如果已有下位 topic（如“安全知识数字化”）其实是专业分支，要在新 topic 中明确它和新主题的上下位关系。

4. **只对结构稳定的笔记直接打标签**
   - 优先修改有 YAML frontmatter 的 `wiki/topics`、`wiki/sources`、`wiki/memos`。
   - 在 `tags:` 下新增共享标签，例如 `AI应用方法论`。
   - 必要时补一个 `related:` 或 `related_topic:` 指回新 topic。
   - 如果文件里有 `updated:` 字段，顺手刷新日期。

5. **谨慎处理旧档和非 wiki 笔记**
   - 对没有 frontmatter 的历史档案、课程摘录、个人旧笔记，不要为了打标签就大改结构。
   - 更稳的做法是：先在新 topic 中挂进去，并在结果备忘里注明“已纳入，但暂不直接改旧档结构”。

6. **输出一份标签映射备忘**
   - 单独写一份 Markdown，列出：
     - 已直接打标的材料；
     - 已纳入 topic 但暂不改旧档结构的材料；
     - 推荐并行标签规则；
     - 一句话总判断。
   - 让用户能一眼看到这轮收口的逻辑，而不是只看到一堆文件被改了。

## Pitfalls
- 不要把所有带“AI”字样的笔记都打上同一个标签；要看它是不是在讲“怎么用”“怎么落地”“怎么形成工作系统”。
- 不要为了统一而强行搬目录；跨主题问题优先用标签和 topic 入口解决。
- 不要批量改老档历史笔记的结构，尤其是没有 frontmatter 的文件；先挂 topic，再决定要不要精修。
- 不要覆盖原有主题，只做上位收口和多标签补充。

## Verification
- 新 topic 页已创建或更新，并能说明主题边界和子线结构。
- 至少一组结构稳定的 `wiki/sources` / `wiki/memos` / `wiki/topics` 已成功新增共享标签。
- 输出备忘清楚区分了“已直接打标”和“只纳入 topic”的材料。
- 若 Obsidian 内搜索该新标签，结果应主要是同一条方法论线，而不是一堆泛 AI 杂项。
