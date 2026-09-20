---
name: work-expert-motherbook-builder
description: Build or refactor a WorkBuddy work-oriented expert together with
  its external motherbook. Use when the user wants to concentrate work knowledge
  into an expert but keep the expert as an entry shell rather than a total
  knowledge warehouse. Covers role-shell design, plugin/agent drafting,
  motherbook structure, registration, and iteration rules.
description_zh: 工作专家与母本搭建
description_en: Work expert and motherbook builder
agent_created: true
---

# work-expert-motherbook-builder

## When to use
- 用户想新建、重构或收敛一个与工作强相关的 WorkBuddy 专家
- 用户已经有大量工作对话、知识库、模板或经验，想集中到一个可调用的专家上
- 用户明确提到“专家是不是合适载体”“想让不同场景或其他工具也能调用”
- 用户需要同时处理专家壳和外部知识母本的边界，不想把专家做成总知识仓

## Steps
1. 先判断载体边界：把“专家壳”“长期记忆”“知识库母本”“工具/连接层”分开，先确认专家只做入口层、人格壳、方法论和输出规范。
2. 如果用户已经在 OpenClaw、WorkBuddy 本地对话或其他旧专家里积累了记忆，先补一轮“记忆来源盘点”：区分旧记忆、当前窗口高价值判断、既有知识库母本，准备做去重、冲突标记和稳定表述合并。
3. 判断 expertType：默认先做 Agent 型；只有明确存在多角色分工和协作流程时才升为 Team 型。
4. 设计专家卡字段：确定 name、displayName、profession、categoryId、displayDescription、tags、quickPrompts，并保持 quickPrompts 第一条等于 defaultInitPrompt。若专家需要承担知识治理职责，quickPrompts 里至少留一条“知识挂载/回写判断”类提示。
5. 起草或修改 agent.md：写清角色定义、核心能力、工作流程、输出规范、知识接入约定和边界条件。工作型专家默认少人名、重角色，只有职责界面、任务分配或责任归属时才保留真实姓名。
6. 如果用户有明确主知识库，必须把知识库对象范围写清楚：是整个 Obsidian vault、某个 topic 集合，还是某个子目录；不要默认缩成单一材料库。涉及 Obsidian 时，优先补充全局结构识别顺序（如 index / rules / log / wiki / raw / skills）。
7. 如果用户要落地到 WorkBuddy：用 expert-manager 标准流程 init → 写入 plugin.json / agent.md → 生成头像 → validate → register。
8. 同步建立三份母本：角色总纲、判断与方法、场景与模板索引。母本放在工作区输出或知识库目标位置，供后续迁入 Obsidian 或其他工具。
9. 如果能力缺口集中在“记忆整理”或“知识治理”，优先在母本里补“记忆合并法”“知识库识别法”“回写动作单”这类稳定方法，不要只改几句 prompt。
10. 补一套 V3 压测机制：至少生成“压测清单”和“修订回路”两份文档，明确真实工作题型、观察维度、常见偏差，以及偏差应优先修改哪份母本。
11. 写一份使用说明：说明三份母本各管什么、专家和知识库如何分层、后续如何通过真实任务压测再修订。
12. 完成后更新项目记忆：记录专家的承载原则、脱敏规则、母本三件套和“先修母本，再修专家壳”的迭代顺序。

## Pitfalls
- 不要把专家当总知识仓，原始材料、案例正文和高时效进展仍应放外部知识库。
- 不要一上来就做 Team 型，容易过重且难维护。
- 不要把启发题自动写成可行性评估。
- 不要默认保留真实人名；工作知识蒸馏时优先用角色、团队和链路位置表达。
- 不要先改专家壳再改母本；遇到系统性跑偏时优先修母本。
- 不要一题一改；至少归并出 2-3 类高频偏差后，再回写母本，否则规则会被单次波动带偏。
- 不要把“主知识库”偷换成某个高频材料目录；如果用户说的是整个 vault，就必须按整库结构写清识别顺序。
- 不要把 OpenClaw 旧记忆、当前窗口对话和既有知识库内容原样堆在一起；必须先做去重、冲突标记和稳定表述合并。
- 不要只补 prompt 不补方法；如果问题在记忆整理和知识治理，至少要同步改“判断与方法”或“场景与模板索引”。

## Verification
- plugin.json 无 TODO，占位字段完整，quickPrompts 数量为 3 且第一条与 defaultInitPrompt 一致。
- agent.md 的角色、能力、流程、边界完整，且与用户目标一致。
- 如果用户强调了历史记忆和整库知识治理，agent.md 中已明确写出记忆合并逻辑、主知识库范围和默认结构识别顺序。
- 专家已通过 validate 并注册成功，能在“我的专家”中看到。
- 三份母本齐全：角色总纲、判断与方法、场景与模板索引。
- 母本中已能定位“记忆合并法”“知识库识别法”或同等方法章节，而不是只剩抽象原则。
- V3 文档齐全：至少有压测清单和修订回路，且能把常见偏差映射到具体母本文件。
- 最终结果能清楚回答：专家负责什么，母本负责什么，后续怎么迭代。
