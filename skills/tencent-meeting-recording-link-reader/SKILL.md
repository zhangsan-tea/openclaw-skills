---
name: tencent-meeting-recording-link-reader
description: Read a Tencent Meeting recording or transcript page when the user
  provides a meeting.tencent.com/crm, /cw, /ctm, or /ct link, especially when
  meeting-code lookup, ended-meeting search, or record-list lookup cannot locate
  the transcript. Use the recording/transcript share page as the primary
  fallback to extract title, participants, smart summary, timestamps, and
  transcript text, then continue analysis or knowledge ingestion.
description_zh: 腾讯会议录制链接读取
description_en: Tencent Meeting Recording Link Reader
agent_created: true
---

# tencent-meeting-recording-link-reader

## When to use
- 用户提供 `https://meeting.tencent.com/crm/...`、`https://meeting.tencent.com/cw/...`、`https://meeting.tencent.com/ctm/...` 或 `https://meeting.tencent.com/ct/...` 的录制 / 转写链接。
- 仅有会议号时查不到会议、录制列表为空，后来用户补了录制或转写分享链接。
- 目标是读取录制页或转写页里的智能总结、逐字稿、发言人、会议主题、待办等内容，而不是修改会议。
- 后续要做会议内容分析、纪要提炼、知识入库时。
- 用户要求按同一会议号批量查找某段时间内的所有录制 / 转写记录。

## Steps
1. 如果拿到的是 `crm` 链接，先注意它通常会跳到对应的 `cw` 页面；如果拿到的是 `ctm` 链接，它通常会跳到对应的 `ct` 转写页面。
2. 先尝试用 WebFetch 直接读取录制页 / 转写页，提示词要明确要求提取：会议主题、时间、发言人、智能总结、逐字稿、待办事项。
3. 如果第一次结果偏概览，再用第二次更聚焦的提示词补抓：
   - 业务痛点与外部牵引
   - AI 落地方式与工作流
   - 团队协作与人才培养
   - 数据边界与合规限制
   - 后续分享/赋能计划
4. 若需要保留定位信息，可同时：
   - 用 Read 查看用户给的截图，核对会议主题、时间、会议号；
   - 用 curl 下载 HTML，确认 `crm` 到 `cw` 的跳转是否正常。
5. 如果 `ctm/ct` 页面只返回登录壳，可以尝试读取页面 `__NEXT_DATA__` 或公共接口线索：`ctm` 可能跳到 `ct`，短链可能解析出 `record_type=4` 的转写长链接；但若接口返回 `403 / 暂无访问权限 / 创建者设置了访问权限`，不要继续暴力重试。
6. 只有当录制页也拿不到内容时，才回退到腾讯会议 CLI / MCP 链路继续查 meeting_id、record list、smart minutes；若 CLI 能定位会议但 `record list` 为 0，而分享页返回 403，则应明确说明“会议可定位，但当前账号无该分享转写访问权限”。
7. 如果用户要查同一会议号在某个时间段内的所有录制，不要优先用 `tmeet record list --meeting-code`（可能返回 500）；更稳的是用 `tmeet record list --start <ISO> --end <ISO> --page-size 30 --format json` 拉取时间段录制列表，再在返回的 `record_meetings` 中按 `meeting_code` 过滤。
8. 对筛出的每条录制，用 `record_files[].record_file_id` 调 `tmeet record transcript-get --meeting-id <meeting_id> --record-file-id <record_file_id> --limit 5000 --format json`；同一场若多个 record_file 返回转写，通常选择段落数最多、时长最长的主录制，短录制/已删除录制只记录备注。
9. 如果同一批录制在一个登录身份下不完整，或 `crm/cw` 分享页公共接口返回 `403` / `recordings=[]`，不要立刻判断无内容；优先让用户确认是否还有微信登录、企业微信登录等其他腾讯会议账号。必要时按确认流程执行 `tmeet auth logout` 后重新 `tmeet auth login --no-browser`，切换账号再用时间段 `record list` 查询。实际经验：同一 `crm` 链接在公共接口或微信账号下可能不可读，切到企业微信登录腾讯会议账号后可通过 `record list` + `transcript-get` 正常读取。
10. 提取完内容后，再去做印证 / 纠正 / 补充分析，或写入指定输出文件。

## Pitfalls
- 不要在只有会议号查不到时就停住；录制分享页往往比会议号更容易直接拿到内容。
- `crm` 页面常只是跳转壳，不要把空壳 HTML 当作失败，优先改读 `cw` 页面；`ctm` 页面常会跳到 `ct` 转写页。
- 录制页 / 转写页能拿到的是“分享态内容”，不一定等同于腾讯会议 CLI 下的全部录制元数据。
- 腾讯会议账号身份会显著影响录制可见性；同一会议号同一时间段，微信登录、企业微信登录、普通腾讯会议账号看到的 `record list` 可能不同。
- 按时间段批量查录制时，`meeting list-ended` 可能查不到参会/他人主持的个人会议号记录；`record list --start/--end` 更容易返回可访问录制。
- `ctm/ct` 转写链接可能只暴露脱敏标题、创建者和权限状态；若公共接口返回 403 或“暂无访问权限”，说明需要创建者开放转写访问，不要伪造内容。
- 若用户要的是“修改会议/申请录制权限”，这不是本 skill 的目标，应回到腾讯会议正式工具链。

## Verification
- 至少确认拿到以下 4 类信息中的 3 类：会议主题、时间/发言人、智能总结、逐字稿正文。
- 输出时说明读取路径来自录制链接页，而不是只说“查到了”。
- 若最终仍失败，要明确区分：是录制页不可读，还是 CLI/MCP 查不到，不要混成一句话。
