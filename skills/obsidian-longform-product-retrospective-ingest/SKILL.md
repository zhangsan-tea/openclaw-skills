---
name: obsidian-longform-product-retrospective-ingest
description: Analyze a long-form product retrospective, internal postmortem, or
  development/operations field report; separate first-hand observations from
  literary expression; compare against existing Obsidian source/concept/memo
  notes; and decide whether to ingest it as a standalone source, extract
  reusable concepts, and/or create a comparison memo without polluting the
  knowledge base with raw prose.
description_zh: 长文产品复盘入库
description_en: Longform Retrospective Ingest
agent_created: true
---

# obsidian-longform-product-retrospective-ingest

## When to use
- 用户发来一篇很长的 PDF / Markdown / 网页长文，说“你学习一下，看有什么发现，如何入库”。
- 材料不是课程，而是产品开发手记、内部复盘、运维观察、组织观察、创始人回忆录式复盘。
- 文本很长、信息密度高、带明显作者风格，不能直接整篇搬进 wiki，需要先抽取结构性判断。
- 需要判断它到底应该落成：独立 source、案例型 source + 多个 concept、还是比较 memo。

## Steps
1. 先提取全文并快速确认文本性质：是第一手现场记录、二手综述，还是作者文学化改写的混合文本。
2. 识别三层内容，不要混在一起：
   - **事实层**：产品、团队、用户、开发、运维、指标、竞争、组织机制。
   - **判断层**：作者对成败、张力、节奏、权力、用户价值的解释。
   - **修辞层**：比喻、文学表达、情绪抒发、人物刻画。
3. 优先保留事实层和判断层；修辞层只保留能稳定复用的原句或极强的判断，不要把散文性表述整段塞进 wiki。
4. 在 Obsidian 里检索同主题条目，至少对照：
   - AI组织进化 / 超级个体 / AI作为生产系统
   - AI4SE / 驾驭工程 / 结构化需求 / 技术债
   - 产品方法 / 用户研究 / 敏捷 / 组织协同
5. 判断它属于哪类输入：
   - **独立新信源**：有一手现场经验，且提供了现有知识库里没有的完整案例。
   - **同主题补充**：事实不够新，但可以回写既有 source / concept。
   - **比较 memo**：新增价值主要在比较框架，不在原始事实。
6. 如果是长文复盘，优先采用“1 个 source + 2~4 个 concept + 1 篇 memo（可选）”的拆法：
   - source：保留案例全貌与时间线
   - concept：沉淀可复用的结构件
   - memo：连接到已有主线，提炼共识/差异/对 Lee 的启发
7. 给 source / memo 起标题时，不要只写泛主题词。标题内部要适度突出**重点和信息量**，让人一眼看出：
   - 这是什么对象/案例
   - 重点落在哪个主轴
   - 它为什么值得单独存
   优先采用“对象或案例 + 重点问题/方法/结构 + 场景”这类写法，避免空泛标题。
8. 抽 concept 时优先找这些类型的抓手：
   - 用户最诚实的反馈不在嘴上，而在成本里
   - 默认值即制度 / 平台产品不能只靠主厨审美
   - 敏捷作为组织记账法
   - 外部保密，内部保共识
   - 看见事 vs 做完事 / AI 工作入口的断层
   - 技术债不只是代码债，而是反馈闭环、权限、责任、上下文的系统债
9. 输出时必须明确告诉用户：
   - 这篇长文最值钱的发现是什么
   - 它属于独立新信源 / 补充 / memo 哪一类
   - 建议新建或回写哪些 source / concept / memo
   - 哪些内容值得保留，哪些只适合作为阅读材料、不适合入库

## Pitfalls
- 不要把作者文笔好误判成知识密度高；散文性强不等于结构价值强。
- 不要把整篇长文机械当 source 原样搬入；长文复盘的价值往往在 concept 层。
- 不要只摘“金句”；必须回到作者到底提供了什么一手事实和结构判断。
- 不要忽略它作为案例的完整性；如果它是一手现场复盘，通常值得保留独立 source。
- 不要只看产品结论；长文里常常还藏着组织机制、汇报节奏、权限结构、评价体系等更硬的东西。
- 不要为了显得系统，把一个案例硬拆成过多 concept；优先保留最硬、最可复用的 2~4 个抓手。

## Verification
- 已区分事实层、判断层、修辞层。
- 已明确判断这篇长文是独立 source、补充还是 memo。
- 已指出至少 2 个值得沉淀的 concept，或说明为什么不该新建 concept。
- 已给出具体入库路径建议，而不是只说“很有价值”。