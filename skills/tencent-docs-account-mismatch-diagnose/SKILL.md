---
name: tencent-docs-account-mismatch-diagnose
description: Diagnose why a Tencent Docs link opens for one account but fails
  for another, especially when a file was uploaded under a personal
  WeChat/QQ-authorized Tencent Docs account but the user tries to open it with
  an Enterprise WeCom Tencent Docs identity. Use this skill to verify
  owner/account, inspect privilege policy, judge whether the issue is
  cross-account membership vs. file visibility, and choose between public-read,
  re-upload, or enterprise-account reauthorization.
description_zh: 腾讯文档跨账号排查
description_en: Tencent Docs Cross-Account Diagnosis
agent_created: true
---

# tencent-docs-account-mismatch-diagnose

## When to use
- 用户说“腾讯文档链接打不开”，但文件本身已上传成功
- 用户怀疑“是不是传到微信账号/QQ账号了，不是企微账号”
- 同一个 `docs.qq.com` 链接在一个身份下可见，在另一个身份下不可见
- 需要判断该文件是否只是权限不对，还是根本上传到了另一账号名下

## Steps
1. 先用 `manage.query_file_info` 查询 `owner_name`、`creator_name`、`is_owner`、`policy`、`file_parent_id`，确认文件归属与当前连接器身份看到的结果。
2. 再用 `manage.get_privilege` 单独确认权限策略：
   - `0=PRIVATE`
   - `1=MEMBERS`
   - `2=PUBLIC_READ`
   - `3=PUBLIC_WRITE`
   - `6/7=INTERNAL_*`
3. 如果 `policy=1` 且用户是用另一个账号（如企微身份）打开，优先判断为“跨账号成员不可见”，不要误判成链接坏了。
4. 读取腾讯文档授权说明：当前这套 MCP 常见授权链路通常要求 QQ/微信侧授权；若用户要真正切到企微账号名下，说明需要改用企微身份重新登录/授权后再上传，而不是只复用当前个人账号下的文件链接。
5. 若用户只想“能打开”，给出两种方案并说明差异：
   - 方案 A：改权限为公开只读（有外泄风险，必须先征得用户确认）
   - 方案 B：在企微登录环境中重新上传/复制到企微账号空间（更符合“转到企微账号”本意）
6. 执行公开只读时，不要只看 `set_privilege` 返回成功；必须再用 `get_privilege` / `query_file_info` 回读 `policy`，必要时再用浏览器或直链验证是否真的脱离登录页。
7. 如果 `set_privilege` 返回成功但 `policy` 仍停留在 `1`，或浏览器打开仍跳登录页，把它判断为“当前文件类型/链路下公开权限未真正生效”。这时不要继续空转重试，直接给兜底方案：
   - 用 `manage.apply_download` + `manage.query_task` 生成临时直链，先解决用户当下下载需求
   - 同时说明：要长期稳定访问，仍需在企微身份下重传，或等可用登录态时再从 UI 侧改权限
8. 若当前 API/连接器没有企微身份或企业空间，就直接说明限制，不要假装能“转 ownership”。这时可改用浏览器方式在企微登录态下重传，或让用户先完成企微授权。

## Pitfalls
- 不要把“链接打不开”直接归因为文件损坏；先看 owner 和 policy。
- 不要未经确认就把权限改成公开只读，尤其是内部材料。
- `docs.qq.com` 与“企微登录腾讯文档”可能对应不同身份；能登录同一站点，不等于能访问同一文件。
- `copy_file` 只能在当前已授权账号/空间里复制，不能等价成“跨账号转移所有权”。
- 如果浏览器里出现登录页，说明当前浏览器态并未自动继承企业身份，不要假定已经登录。
- 对上传到文件空间的通用文件，`set_privilege` 可能出现“接口返回成功，但回读 policy 仍是 1”的情况；不做回读验证就向用户宣布“已公开”会误导。
- `apply_download` 生成的直链是临时签名链接，不是长期公开链接；要向用户明确时效性。

## Verification
- `query_file_info` 明确返回 owner/creator，且能解释为何用户当前身份打不开
- 给用户清楚说明：当前文件属于哪个身份、权限是什么、下一步该走公开权限还是企微重传
- 如果已经完成重传，返回新的企微侧文件链接；若未完成，明确卡点是“需企微登录/授权”而不是文件本身失败
