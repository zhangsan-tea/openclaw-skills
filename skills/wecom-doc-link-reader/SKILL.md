---
name: wecom-doc-link-reader
description: Read a WeCom document link (doc.weixin.qq.com) through the user's
  installed wecom-cli suite when browser fetch, WebFetch, or Tencent Docs MCP
  only returns the login shell. Use this for WeCom
  doc/sheet/smartsheet/smartpage URLs to get actual content with the authorized
  enterprise account, then follow the correct async polling workflow and return
  the markdown content for downstream analysis or editing.
description_zh: 读取企微文档链接
description_en: Read WeCom doc link
agent_created: true
---

# wecom-doc-link-reader

## When to use

Use this skill when all of the following are true:
1. The user gives a `doc.weixin.qq.com` link.
2. Normal fetch methods only return login shells such as `企业身份登录`, or generic Tencent Docs tooling cannot read the page correctly.
3. The workspace already has the WeCom CLI suite installed, or it is reasonable to check for it.
4. You need the real document content for reading, analysis, summarization, or migration.

Typical triggers:
- “读一下这个企微文档”
- “这个企微文档之前能读，现在读不了了”
- “用企业微信套件把这个链接读出来”

## Steps

1. **Check CLI availability and auth first**
   ```bash
   wecom-cli --version && wecom-cli auth show --status
   ```
   - If auth shows `authorized`, continue.
   - If `unauthorized`, run:
   ```bash
   wecom-cli auth init --noninteractive
   ```
   and wait for user扫码授权。
   - **Important edge case:** `auth show --status` may still return `authorized` while the robot's **文档使用权限** has expired. If document reading returns `errcode: 851014` with `authorization expired` plus `help_instruction` / `help_message`, stop retrying and show the user the returned `help_message` **verbatim**. General web fetch will normally remain blocked by `企业身份登录` until the robot document permission is reauthorized.

2. **Route by URL type**
   - `/doc/` → use `wecom-cli doc get`
   - `/sheet/` / `/smartsheet/` → inspect `wecom-cli doc --help` and use the currently available dedicated subcommand; do not assume legacy `get_doc_content` exists
   - `/smartpage/` → inspect current CLI schema first; do not assume legacy async export commands exist

3. **For a normal `/doc/` link, read directly**
   ```bash
   wecom-cli doc get --docid "<URL>" --content-type markdown
   ```
   - In `wecom-cli 1.2.1`, this returns a synchronous JSON payload; the Markdown is directly in `content` when `errcode` is `0`.
   - Treat the returned export as a formatted Markdown representation, not necessarily a byte-for-byte document transcript.

4. **Only fall back to browser automation if WeCom CLI is unavailable or unauthorized**
   - Browser fetch and generic web fetch should not be the main path once `wecom-cli` is available.
   - If forced to use browser automation, explicitly explain that the content is blocked by login state and ask the user to provide access via Chrome profile or exported file.

7. **After reading content, continue the real task**
   - Do not stop at “I can read it now”.
   - Immediately do the downstream job: summarize, compare, extract signals, write memo, or update knowledge files.

## Pitfalls

- Do **not** assume Tencent Docs MCP can read `doc.weixin.qq.com` correctly. It may fail on share-link parsing or auth.
- CLI command surfaces have changed: in `wecom-cli 1.2.1`, normal documents use `wecom-cli doc get --docid "<URL>" --content-type markdown`, not the legacy `doc get_doc_content` command.
- Do not assume document retrieval is asynchronous. On `wecom-cli 1.2.1`, normal `/doc/` retrieval is synchronous and the final Markdown is in the JSON `content` field.
- Do **not** assume old Smartpage or sheet export commands still exist. Inspect `wecom-cli doc --help` or the current schema before calling them.
- If the document is a WeCom doc and the CLI is authorized, prefer `wecom-cli` over agent-browser or WebFetch.
- `wecom-cli auth show --status` being `authorized` does **not** guarantee doc export still works. If reading returns `errcode: 851014` / `authorization expired`, the blocker is usually the robot's document permission expiring, not the share link itself.
- When `help_instruction` says to display `help_message` verbatim, do exactly that. Do not paraphrase, translate, shorten, or prettify it.
- The returned content may already be a summarized or formatted markdown export, not a verbatim transcript. Preserve that distinction in downstream notes.

## Verification

A successful run should satisfy all checks:
1. `wecom-cli auth show --status` returns `authorized`.
2. The response JSON from `wecom-cli doc get` has `errcode: 0`.
3. The payload contains non-empty `content`, not `企业身份登录` or an empty shell.
4. You use the extracted content to finish the user's actual task instead of stopping at retrieval.
