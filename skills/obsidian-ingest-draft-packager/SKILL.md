---
name: obsidian-ingest-draft-packager
description: Package an analyzed work material into directly usable Obsidian
  ingest drafts and, when the user asks to "直接入库", write the final
  source/memo/topic notes into the user's Obsidian work vault. Use after you
  have already finished the analysis and know the target knowledge line, naming,
  and挂载方向.
description_zh: Obsidian入库打包
description_en: Obsidian ingest packager
agent_created: true
---

# obsidian-ingest-draft-packager

## When to use
- 用户已经让你完成了材料分析，现在要你“入库”“直接落库”“写进 Obsidian”。
- 你已经知道这份材料应落到哪条知识线，且需要输出 source / memo / topic 草稿或正式文件。
- 你需要把散落判断收束成一个最小可用入库包，而不是继续停留在聊天结论。
- 特别适用于“印证 / 纠正 / 新增 / 用库建议”之后的下一步落库动作。

## Steps
1. **先确认主挂方向**
   - 不要一上来就写文件。
   - 先明确：主挂哪个 topic，哪些是二级挂载，哪些只保留弱关联。
   - 如果用户已经明确“重点是 X”，优先围绕 X 建主线，而不是平均分散到多个 topic。

2. **检查 vault 现有结构**
   - 直接查看目标 vault 下的 `wiki/sources/`、`wiki/memos/`、`wiki/topics/`。
   - 优先参考已有命名风格，不要自创一套：
     - source 常用：`YYYYMMDD_对象_主题.md`
     - memo 常用：`分析备忘_YYYYMMDD_主题.md`
     - topic 常用：`主题名.md`

3. **读取你已经生成的草稿或分析文件**
   - 如果前一步已经在工作区生成 drafts / outputs，先读这些文件作为正式入库底稿。
   - 不要无必要重写内容；用户若说“内容不用改了”，就直接复用。

4. **判断是“新建”还是“更新”**
   - 用 Glob 检查目标 source / memo / topic 是否已存在。
   - 不存在：直接新建。
   - 已存在：先 Read，再用 Edit 做增量修改，避免覆盖历史。

5. **按最小完整包落库**
   - 至少落两层：
     - `source`：保存材料重组后的客观摘录与定位
     - `memo`：保存这次相对既有认知的判断、修正、补充
   - 如果该材料已经足以形成稳定主线，补一个 `topic`；否则只在既有 topic 中挂 source / related 即可。

6. **最小必要的关联补链**
   - 至少做一处“能从旧 topic 进入新内容”的链接修补。
   - 常见做法：给主挂 topic 增加 `related` 到新 topic，或把新 source 补进旧 topic 的 `sources`。
   - 只做最小必要动作，避免一次性大面积改库。

7. **写入后做轻验证**
   - 重新读取新建文件头部或关键片段，确认 frontmatter、links、文件名一致。
   - 检查是否把 draft 路径误留在正式文件里。

8. **补 memory**
   - 在项目 memory 里记录：落了哪些 source / memo / topic，主挂方向是什么，后续应沿哪条线继续吸收。

## Pitfalls
- 不要把“迎检弱相关”的材料硬挂成迎检主材料。
- 不要为了显得全面，把一份材料平均塞进太多 topic，导致主线模糊。
- 用户已明确“内容不用改”，就不要再做风格润色。
- 更新已有 topic 前一定先 Read，不能直接覆盖。
- topic 不是摘要仓库；只有当主线足够稳定时才新建 topic。

## Verification
- `wiki/sources/`、`wiki/memos/`、`wiki/topics/` 中出现目标文件。
- 新 source 与 memo 的 `related` 能指向主挂 topic。
- 至少有一处旧 topic 能回链到新入库内容或新 topic。
- 项目 memory 已记录这次入库动作与主挂方向。
