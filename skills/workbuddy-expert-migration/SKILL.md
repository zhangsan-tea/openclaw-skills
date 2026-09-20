---
name: workbuddy-expert-migration
description: Package a WorkBuddy expert for cross-device migration and restore
  it quickly on another terminal. Use when the user wants to move one expert or
  an entire my-experts set to a new machine, reinstall WorkBuddy without
  rebuilding experts from scratch, or produce a reusable migration bundle with
  zip, instructions, and optional motherbook files.
description_zh: WorkBuddy 专家迁移
description_en: WorkBuddy expert migration
agent_created: true
---

# workbuddy-expert-migration

## When to use
- 用户想把一个 WorkBuddy 专家迁到另一台电脑
- 用户刚换设备、重装系统或重装 WorkBuddy，想快速恢复“我的专家”
- 用户想给自己留一个可重复使用的专家发布包，而不是下次再从头创建
- 用户想区分“专家本体”和“母本/知识库”哪些该一起迁，哪些不必跟着走

## Steps
1. 先判断迁移范围：是迁单个专家，还是迁整个 `~/.workbuddy/plugins/marketplaces/my-experts/`。
2. 确认最小可移植单元：单专家时以专家目录为准，至少包含 `.codebuddy-plugin/plugin.json`、`agents/*.md`、`avatars/`，以及该专家目录内已有的 `skills/`、`bin/`、`references/`。
3. 源端先打包：优先使用 expert-manager 的 `package_expert.py` 生成 zip；如果用户要整包迁移全部个人专家，再考虑整体复制 `my-experts/` 目录。
4. 如果该专家依赖外部母本而不是把知识全塞在专家正文里，要同时整理可迁移的母本文件，并单独放入迁移包，不要误以为专家 zip 已包含全部知识。
5. 如果用户有可跨终端同步的 Obsidian 或其他知识库，同步整理一套“迁移资料包”进去：至少包含一页索引、一页迁移说明、一段可直接发给 WorkBuddy 的引导语、专家 zip，以及母本文件；需要更快恢复时再附一个恢复脚本。
6. 新终端上把单专家解压到 `~/.workbuddy/plugins/marketplaces/my-experts/plugins/<expert-name>/`；如果迁的是整包，则恢复 `my-experts/` 根目录结构。
7. 新终端重新运行 `validate_expert.py` 校验专家目录，再运行 `register_expert.py` 让 WorkBuddy 重写 `.codebuddy-plugin/marketplace.json`。
8. 如果用户更想少动手，优先给一段“直接对 WorkBuddy 说的话”：先让 WorkBuddy 读取同步好的资料包，能直接恢复 zip 就恢复；只有 zip 不可用时才按母本重建。
9. 打开 WorkBuddy 的“我的专家”确认是否出现；如未即时刷新，重开专家页或重启 WorkBuddy 再检查。
10. 如需长期维护，额外输出一页迁移说明，写清源端路径、目标路径、恢复命令、母本位置和后续修订顺序，后续直接复用。

## Pitfalls
- 不要只带 `marketplace.json`；它只是索引，不是专家本体。
- 不要把 `.created-by-session` 当成必需文件；它不决定专家是否可用。
- 不要把聊天记录误当成专家迁移内容；迁的是专家包，不是运行时上下文。
- 如果专家目录外还有依赖文件，必须明确标注并单独带走；否则新终端会“看得到壳，用不好内容”。
- 如果只是为了恢复可调用状态，不要在新终端重写专家内容；优先复制原专家目录并重新注册。
- 如果用户追求最快恢复多位专家，整包迁移 `my-experts/` 通常比逐个重建更快；但关键专家仍建议逐个重新注册一次。
- 不要只存 zip 不存母本；这样能恢复可调用状态，但后面一改就容易失去上位依据。
- 如果用户已经有跨终端同步的 Obsidian，不要把迁移说明仍然只留在本地 outputs；应同时放进同步目录，避免换机时找不到说明和引导语。
- 给 WorkBuddy 的引导语要明确“优先恢复、不随意重写 name/agentName/目录名、zip 不可用时再按母本重建”，否则容易把恢复任务做成重建任务。

## Verification
- 打包后的 zip 能解压出完整专家目录结构。
- `validate_expert.py` 通过。
- `register_expert.py` 成功，且 `my-experts/.codebuddy-plugin/marketplace.json` 出现或更新对应条目。
- WorkBuddy “我的专家”中能看到目标专家并正常召唤。
- 如果额外迁了母本，迁移说明里能清楚指出母本文件路径和后续修订顺序。
- 如果用户有同步型 Obsidian，知识库里已经存在完整迁移资料包：索引、说明、给 WorkBuddy 的引导语、专家 zip、母本文件，以及可选恢复脚本。