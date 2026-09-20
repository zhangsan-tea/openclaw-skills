---
name: ingested-material-refresh-review
description: Reconstruct prior context for a document or topic that has already
  been ingested into the user's knowledge base, compare older baseline materials
  with newly read content or newer notes and concepts, and output a concise
  refresh review. Use when the user asks to "回忆一下", "此前入过库", "看下原材料还能补什么", or
  wants a verdict like "哪些是印证/纠正/新增，以及怎么用库" based on existing Obsidian/wiki
  knowledge rather than starting from scratch.
description_zh: 入库材料回溯补强
description_en: Ingested Material Refresh Review
agent_created: true
---

# ingested-material-refresh-review

## When to use
- 用户说某份材料、文档、讲稿、会议纪要“此前入过库”，要你先回忆已有知识再给更新建议。
- 已经直接读到了当前正文，但用户要的不是摘要，而是“对照既有知识线，看哪些是印证、哪些是纠正、哪些是新增、怎么用库”。
- 链接当前打不开、只能拿到空壳，但本地 Obsidian / wiki / memory 里已经有相关 source、memo、concept、baseline。
- 目标不是重做摘要，而是做“回溯 + 对照 + 修订建议 / 用库建议”。

## Steps
1. 先找历史锚点：查 conversation_search、项目 memory、Obsidian wiki/sources、wiki/memos、wiki/concepts、baseline。
2. 优先读三类材料：
   - 最早的基础底稿 / baseline
   - 中间的 source / 会议纪要 / 课程记录
   - 最新的 analysis memo / concept 升级
3. 把信息分成三层：
   - 仍成立的底层判断 / 印证项
   - 后来被修正的旧表述 / 纠正项
   - 后来新增、值得补进原材料的新结构件 / 新增项
4. 根据用户问法选择输出框架：
   - 若用户要“回贴原材料修订建议” → 用三栏：建议修正 / 建议补充 / 结构重排建议
   - 若用户要“吸收判断” → 用四栏：印证 / 纠正 / 新增 / 用库建议
5. 如果拿到了当前正文，要明确哪些结论来自当前材料，哪些来自历史锚点；不要把两者混成一层。
6. 如果拿不到当前链接正文，要明确说明“以下按已入库知识线给出”，不要假装直接读到了链接内容。
7. 如果企业微信文档返回授权过期或异步导出失败，先把工具要求原样展示给用户，再退回已入库知识线给出 best-effort 建议。
8. 尽量引用具体文件路径和行号，方便用户回看原始依据。

## Pitfalls
- 不要只复述原材料，要明确哪些是旧判断、哪些是新增增量。
- 不要把“案例更新”误当成“结构更新”；很多时候更该补的是组织逻辑、工作流、机制条件。
- 不要忽略最新 memo / concept 里的“修正项”，尤其是对旧叙事的反驳。
- 若当前正文已经拿到，不要只做摘要；要明确指出与既有知识相比，到底印证了什么、纠正了什么、补了什么。
- 当前链接打不开时，不要硬编文档正文。
- 企微文档常见是授权过期，不要把认证报错误判成“文档不存在”或“没有内容”。

## Verification
- 至少覆盖 1 份 baseline、1 份 source、1 份最新 memo/concept。
- 输出里明确区分“修正”和“补充”，不是混成一堆建议。
- 用户看完能直接把建议贴回原材料做修订。