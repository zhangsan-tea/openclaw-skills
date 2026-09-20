---
name: coach-certification-guide-ingest
description: Ingest an updated coaching certification, ACC/PCC exam, or
  training-guide document into the personal-growth knowledge base. Use when the
  user uploads a new guide PDF/markdown and wants a direct decision on whether
  to update an existing note, create a versioned source, or produce an
  action-oriented checklist without repeated confirmation.
description_zh: 教练考牌指引入库
description_en: Coach Guide Ingest
agent_created: true
---

# coach-certification-guide-ingest

## When to use
- 用户上传教练考牌、ACC/PCC 认证、课程结业、报名流程、训练营规则等指引材料，并说“怎么入库”“帮我整理到向内看”“看看该怎么放”。
- 已有同主题旧笔记，需要判断新材料是小修小补、正式更新版，还是应拆成行动清单。
- 输入常见是 PDF、截图合集、Markdown 摘要、机构正式通知。

## Steps
1. 先读取新材料正文；若是 PDF，优先用隔离 Python 环境提取文本，不要先停下来问用户是否运行。
2. 在 `/Users/lee/Obsidian/向内看/` 下搜索同主题旧笔记，重点看是否已有同机构、同认证路径、同年份的摘要或旧版本。
3. 判断新材料性质：
   - 小修补：直接更新旧笔记；
   - 正式更新版：保留旧摘要，新增一个带日期的版本化 source；
   - 面向执行：在 source 之外，再拆一篇“我的行动清单”。
4. 输出时优先说明：为什么这样入库、和旧材料是什么关系、最值得保留的更新点是什么。
5. 如果正文包含硬时限、费用、资格门槛、评估标准，务必提炼成单独小节，避免散在全文里。
6. 写入 Obsidian 时，标题要带日期、对象、主轴和“为什么值得单列”。
7. 完成后更新当日日志；若用户再次强调“低风险步骤直接执行”，同步强化 `~/.workbuddy/MEMORY.md`。

## Pitfalls
- 不要把新版正式指引直接覆盖旧摘要，除非差异极小且旧笔记本就是活文档。
- 不要只复述全文，要明确新版相对旧版的增量。
- 不要把“服务有效期”“建议窗口”“系统硬时限”混成一个概念，必须分别写清。
- 不要因为 PDF 提取、依赖安装或工具切换的小故障停下来向用户追问“是否运行”。

## Verification
- 至少读到一份新材料和一份旧笔记。
- 明确给出入库策略：更新旧笔记 / 新增版本化 source / 再拆行动清单。
- 输出中至少包含 3 类关键信息：资格门槛、流程节点、更新差异。
- 产出的笔记路径落在 `/Users/lee/Obsidian/向内看/` 对应主题目录下。
