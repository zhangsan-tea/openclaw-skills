---
name: wiki-metadata-low-risk-fix
description: Use this skill to apply low-risk metadata normalization to wiki markdown pages without changing knowledge content. It limits edits to front-matter fields (type/title/created/updated/review), avoids link rewrites, excludes engine/source-code directories, and supports safe commit + push after review.
description_zh: Wiki元数据低风险修复
description_en: Wiki Metadata Low-Risk Fix
disable: false
agent_created: true
---

# wiki-metadata-low-risk-fix

## When to use
- 用户要求先做“低风险修复”，只修 front-matter 或时间字段。
- 当前语料不完整（如子集同步）导致断链很多，暂不适合做语义改写。
- 需要保护正在运行的引擎链路，不希望触碰源码目录。

## Steps
1. 明确边界：仅处理 `wiki/**/*.md`，不处理断链、不改正文语义、不改源码目录。
2. 扫描并分组：无 front-matter、缺 `title`、缺 `updated`、超90天缺 `review`。
3. 执行最小补丁：
   - 无 FM：补 `type/title/created/updated`
   - 缺 title：按 H1 或文件名补
   - 缺 updated：补当天日期
   - 超90天：补 `review: 待复核(超90天)`（不改 status）
4. 追加 `log.md` 修复记录（操作类型用 `fix`）。
5. 提交与推送：`git add` 指定范围、`git commit`、`git push origin main`。

## Pitfalls
- 不要把 `status` 扩展为未约定值（如 draft/archived）。
- 不要在语料不完整时批量修断链，容易误改。
- 不要修改 `迎检支持系统_源码/` 或运行中引擎文件。
- 路径含中文时避免通配误删，优先脚本+明确白名单。

## Verification
- `git diff --shortstat` 仅显示元数据增量（无大段正文改写）。
- 变更文件范围仅在 `wiki/**/*.md` + `log.md`。
- `git status --short` 推送后为空。
- 抽样检查 3 类文件：无FM修复样例、缺updated样例、超90天review样例。