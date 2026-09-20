---
name: workbuddy-session-slim-archive
description: Diagnose and fix WorkBuddy sessions whose history file has bloated,
  causing the assistant panel to stop responding or the model to return "400
  invalid parameter value". Use when a long-lived session (e.g. the fixed
  session a WeCom/企微 bot routes into) accumulates huge inline images (esp.
  unsupported image/heic) or file-history snapshot pointers until requests fail.
  Safely backs up, slims (removes inline base64 images + clears
  trackedFileBackups pointers), atomically replaces, and archives the large
  backup — without breaking the id/parentId chain and without ever touching the
  real file-history version store. Also supports rollback.
description_zh: 会话瘦身备份归档
description_en: Slim & archive session
agent_created: true
---

# workbuddy-session-slim-archive

## When to use
- 桌面「助理」界面发消息无反应，且/或企微等渠道回显 `抱歉，请求处理失败：400 invalid parameter value (<reqId>/<sessionId>)`。
- 某条长期会话（尤其企微 bot 路由进的固定 cli 会话）历史文件膨胀到几十~上百 MB。
- 日志出现 `ImageUtils.compressImage failed ... Unsupported MIME type: image/heic` 或 `[ModelProvider] Request failed with status code 400`。
- 用户想定期维护/归档某条超大会话，但要保留可回滚能力。

## 背景：文件布局（务必先认清）
- **真实会话历史** = `~/.workbuddy/projects/<Project-Slug>/<sessionId>.jsonl`（可达上百 MB）。
- `~/.workbuddy/sessions/*.json` 只是小索引，**不是**历史本体，别在这里找。
- **真正的文件版本库** = `~/.workbuddy/file-history/<sessionId>/`（`xxxx@v1 @v2 ...`）。这才是"改文件改错了回退某一版"依赖的东西，**绝不能动**。
- jsonl 里的 `file-history-snapshot.trackedFileBackups` 只是**指向版本库的指针/索引**，清空它不影响真实版本回滚。

## Steps
0. 用 managed python 运行脚本（推荐）：
   `PY=/Users/lee/.workbuddy/binaries/python/versions/3.13.12/bin/python3`
   `SCRIPT=/Users/lee/.workbuddy/skills/workbuddy-session-slim-archive/scripts/slim_session.py`
1. **定位 sessionId**：从报错括号里 `(<reqId>/<sessionId>)` 取后半段；或在 `~/.workbuddy/logs/<date>/` grep `400 invalid parameter value`。
2. **只读分析**（先看构成，不改任何东西）：
   `$PY $SCRIPT --analyze <sessionId 或 .jsonl绝对路径>`
   关注：总大小、`含内联图/heic 行`、各 type 字节占用。
3. **确认膨胀来源**：通常是 `data:image` 内联 base64（含 heic）+ `file-history-snapshot` 指针堆积。
4. **执行瘦身**（自动：备份→清内联图→清快照指针→校验→原子替换→大备份移归档）：
   `$PY $SCRIPT --slim <sessionId 或 .jsonl绝对路径>`
5. **若瘦身后仍偏大、UI 仍渲染不动**（气泡显示 `?`、加载不出），用深度压缩：裁掉早期历史只留最近 N 行 + 压缩工具结果。早期历史靠前面的备份兜底，可回滚。
   `$PY $SCRIPT --compact <sessionId> --keep-lines 2000`
   - 经验值（本机一条 17.5k 行会话）：留 2000 行≈4MB / 3000 行≈6MB / 4000 行≈8MB / 6000 行≈12MB。
   - 起点自动对齐到"最近 N 行内第一条 user 消息"，避免拆散工具调用；保留 ai-title/custom-title 让会话仍有名字；保留段首条父指针置空成为新起点。
6. **尾部失败往返清理（重要！文件已瘦身却仍 400 时必查）**：当文件已清干净（无图/无 heic/体积小）但仍持续 400，多半是会话**尾部堆了一串失败往返**——连续的"用户重发 + assistant 回 `400 invalid parameter value`(status=incomplete)"，且**最后一条是 incomplete assistant**。这种残缺尾部会让下一次请求拼出非法消息序列，后端继续 400，形成死循环。处理：备份后**截断到最后一条 status!=incomplete 的 assistant 消息**（含），丢弃其后所有失败往返与尾随快照。
   - 判别：日志里多次 400 的 `requestId` 长期不变（如同一个 reqId 重试几十分钟、跨越你的文件清理操作）→ 说明卡的是**进程内存里的僵尸请求/残缺尾部**，不是磁盘内容。
   - 清理后必须让用户**重启 WorkBuddy 或在该会话点停止/中断**，让内存里那个重试请求结束；否则磁盘改了它仍在用旧内存状态。
7. **告知用户验证**：开新会话（New Chat）在渠道发"你好"；老会话也应能重新加载。
8. **写记忆**：在项目 memory 里记录本次 sessionId、压缩前后大小、备份归档路径。

## 回滚
- 一键：`$PY $SCRIPT --rollback <sessionId 或 .jsonl绝对路径>`（自动找最近的 backup-/precompact- 备份，先把当前文件另存为 pre-rollback 再覆盖）。
- 手动：把 `~/.workbuddy/session-archives/<sessionId>.backup-*.jsonl`（或 `.precompact-*.jsonl`）复制回 projects 目录覆盖同名 jsonl。

## Pitfalls
- **磁盘改了仍 400 = 进程内存僵尸请求**：若同一 `requestId` 跨越你多次文件清理仍在重试，说明卡在运行中的进程内存，改磁盘文件无效，必须重启 WorkBuddy 或中断该会话当前请求。这是最容易误判的点。
- **别动 `~/.workbuddy/file-history/`**：它是文件级回滚命根子，体积小（几 MB）不影响速度，挪走会让回滚失效。
- 真实历史在 `projects/<slug>/`，不在 `sessions/`；找错地方会以为"没有大文件"。
- `mv`/命令行里**不要带 `#` 注释**，本环境会因无法识别命令根而拒绝执行；注释写进脚本即可。
- 瘦身**不删行、不改 id/parentId 链**，否则会话会断裂无法继续；脚本已保证只替换值。
- heic 不被支持：根因之一是用户发了 iPhone heic 截图。提醒用户发前转 png/jpg，或关掉 iOS「高效格式」。
- 瘦身后若仍偏大（function_call_result 未动）、且 UI 仍加载不出（气泡 `?`）：单纯截断长文本不够（实测仅能到 ~26MB），必须用 `--compact` 裁早期历史才能降到个位数 MB。
- `--compact` 会丢弃早期历史的"可见对话"（仍可从备份回滚）；执行前务必已有整段备份，并向用户确认保留行数。
- 大备份（>30MB）会被自动移到 `~/.workbuddy/session-archives/`，避免拖慢项目/会话扫描。

## Verification
- `--analyze` 复查：`含内联图(data:image)行` 应为 0，总大小明显下降。
- 瘦身后 jsonl 全部行可被 `json.loads` 解析（脚本内置校验，失败则放弃替换、保留原件）。
- 备份文件行数与原文件一致且末行可解析。
- 开新会话在渠道发消息能正常收到回复。

## Related Skills
- 迁移/接入问题总分流：`openclaw-to-workbuddy-migration-router`
- 企微新 bot 无响应但需先区分是不是会话膨胀：`workbuddy-wecom-writer-noresponse-fix`
- 迁移前只读盘点：`openclaw-migration-readonly-inventory`
