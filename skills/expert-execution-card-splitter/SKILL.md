---
name: expert-execution-card-splitter
description: Split 1-2 high-value work materials into expert-ready execution
  cards when the user is building or feeding a WorkBuddy work expert. Use for
  meeting summaries, stage memos, operating notes, or strategy materials that
  contain reusable judgments but should not be fed whole. The skill turns source
  materials into stable cards with titles, scenarios, core judgments, key
  points, response constraints, and source anchors, while stripping meeting tone
  and personal context.
description_zh: 工作专家执行卡拆解
description_en: Expert execution card splitter
agent_created: true
---

# expert-execution-card-splitter

## When to use
- 用户正在搭建或喂养一个工作型 WorkBuddy 专家，已经明确“不要整篇材料原样挂进去”，而要先拆成卡
- 手头有 1-2 份会议纪要、阶段备忘、推进总结、专题材料，里面有可复用判断，但原文现场感太强
- 用户已经收口了专家的主知识边界，下一步是把“阶段材料 → 可挂载执行卡”
- 用户已经做完上一轮时间线、候选清单、首批执行卡或挂载顺序，希望继续从这些中间产物里抽“第二批方法层 / 治理层 / 角色层卡”
- 需要先出一版卡片草案，再决定是否落 Obsidian / 母本 / 专家知识库

## Steps
1. 先确认这轮是“从原始材料拆卡”还是“从上一轮中间产物继续抽卡”。无论哪种，都不要扩扫全库；优先挑“当前最值钱、最接近专家主任务”的 1-2 份材料或 1 份中间产物。
2. 读取材料时只抓会影响专家回答的部分：阶段判断、执行约束、边界条件、动作链路、可迁移方法。不要被开场寒暄、参会人、对话口气带偏。
3. 如果输入的是时间线、候选清单、挂载顺序这类中间产物，就继续往下压“第二批方法层 / 治理层 / 角色层母结论”，不要退回去重复写摘要。
4. 先做“可挂载判断”筛选：把原文或中间产物拆成 4-8 个候选判断，要求每个判断都能回答一个真实问题，而不是一句笼统总结。
5. 卡片标题优先写成“对象 + 动作/边界/阶段 + 卡”，避免泛标题。例：`测试环境与免测争取卡`、`材料/台账双轨卡`。
6. 每张卡默认包含这些段落：
   - 定位
   - 适用场景
   - 核心判断
   - 关键内容
   - 对专家的回答约束
   - 一句话版（可选）
   - 来源锚点
7. 如果用户明确要“正式挂载版”或继续往下落，不要停在草案层；把卡统一补成可挂载格式，至少加上 frontmatter 字段：`title / card_type / status / priority / tags / related / source_anchor`，并补“边界与例外 / 关联卡”两段。
8. 如果用户继续要求可直接落地，就把正式挂载版再拆成独立 md 文件；文件名建议加顺序和优先级（如 `01_P1_...卡.md`），并补一份索引清单，写清推荐挂载顺序和下一步继续拆的材料。
9. 改写时默认去掉：会议口气、对话现场感、对具体人的依赖、只对当时参会者成立的背景句。保留：结论、边界、动作、依赖关系、阶段信号。
10. 如果某条判断仍明显依赖单次会议或个人上下文，不要硬做成卡；要么降成“候选卡”，要么继续留在改写层。
11. 输出时先写到 `outputs/` 的 markdown 草案，不直接落正式知识库，除非用户明确要求你同步写回。
12. 最后给出两类收口：
   - 本轮已拆出的卡片清单
   - 下一步最该继续拆的 1-2 份材料或 2-3 张卡
13. 如果已经连续做了 3-4 批正式挂载卡，不要机械地一直补散卡；优先判断是否该转去产出一张“总入口索引 / 卡片地图”，把法规层、状态层、执行层、方法层、治理与人才层串起来。
14. 完成后更新工作记忆：记录拆了哪几份材料、出了哪些卡、下一步接什么。

## Pitfalls
- 不要把整篇纪要改个标题就当成卡；卡必须能单独回答问题。
- 不要把“对 Lee 的说明口气”原样保留在卡里。
- 不要一次拆太多文件；1-2 份最稳，超过这个容易开始泛化和偷懒。
- 不要把组织判断、人事评价、推进拿捏直接塞进卡里，除非已抽成机制表达。
- 不要为了凑数量拆出过细小卡；宁可 5 张扎实卡，也不要 12 张空卡。
- 不要只给标题列表；至少写出核心判断和回答约束，否则后面还得重做。
- 如果用户已经明确要“可挂载版”或“独立卡文件”，不要还停在单一汇总稿里；应继续补 frontmatter、优先级、关联卡，并拆成独立 md。

## Verification
- 每张卡都能回答一个真实用户问题，而不只是记录一段材料。
- 卡片正文已去掉会议现场感，外行读也能看懂。
- 4-8 张卡之间边界基本清楚，没有明显重复。
- 每张卡都能指出来源材料，后续可追溯。
- 如果本轮目标是“正式挂载版”，则每张卡都应有统一 frontmatter，且包含 `边界与例外`、`关联卡`。
- 如果本轮目标是“独立文件版”，则应额外产出索引清单，并能直接按优先级逐张挂载。
- 输出文件能直接作为专家母本或 Obsidian 卡片前置草案继续加工。
