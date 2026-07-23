---
name: gongfeng-main-first-layer-isolation
description: Use this skill when a mixed Obsidian repo on Gongfeng must keep only the inspection knowledge base visible on main branch without rewriting Git history. It performs safe first-layer isolation by updating .gitignore to whitelist inspection paths, removing non-inspection files from Git tracking with --cached, committing, pushing to main, and verifying remote top-level visibility.
description_zh: 工蜂主线第一层隔离
description_en: Gongfeng Main Layer-1 Isolation
disable: false
agent_created: true
---

# gongfeng-main-first-layer-isolation

## When to use
- 用户要求“主线只保留迎检知识库可见层”，但暂不做历史改写。
- 仓库当前已混入其他知识库目录，需要在 `main` 上快速清理。
- 目标是“远端主线可见层清空非迎检内容”，并保留本地文件。

## Steps
1. 同步并对齐主线：`git -C <repo> fetch origin --prune`，确认在 `main`，必要时 `git -C <repo> reset --hard origin/main`。
2. 白名单化 `.gitignore`（根路径）：仅允许 `.gitattributes`、`.gitignore`、`AGENTS.md`、`index.md`、`log.md`、`迎检支持专家知识库/`。
3. 生成待移除追踪清单（NUL 安全）：基于 `git ls-files -z` 过滤非白名单路径。
4. 执行 `git rm -r --cached --pathspec-from-file=<nul-list> --pathspec-file-nul`，仅移除追踪，不删本地文件。
5. `git add -A` 后提交：`meta: 主线第一层隔离，仅保留迎检知识库可见层`。
6. 推送 `git -C <repo> push origin main`。
7. 验证远端：`git -C <repo> -c core.quotePath=false ls-tree --name-only origin/main` 仅含白名单项。

## Pitfalls
- 不要直接 `git rm -r`（会删本地文件）；必须使用 `--cached`。
- 过滤路径要支持中文和空格，优先使用 NUL 分隔清单。
- 若远端 main 有新提交，先对齐再清理，避免覆盖协作者工作。
- 这是“可见层清理”，不是“历史清洗”；旧提交仍在历史中。

## Verification
- `git status --short` 为空。
- `git rev-parse --short HEAD` 对应已推送提交。
- `ls-tree origin/main` 仅显示：`.gitattributes`、`.gitignore`、`AGENTS.md`、`index.md`、`log.md`、`迎检支持专家知识库/`。