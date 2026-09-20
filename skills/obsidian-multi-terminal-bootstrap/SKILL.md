---
name: obsidian-multi-terminal-bootstrap
description: Bootstrap a multi-terminal Obsidian workflow for a shared vault by creating three coordination documents: a startup entry note, a recent-updates summary note, and a reusable trigger-phrases note. Use when the user wants to reduce manual context switching across home/work/mobile devices and needs a stable continuation/checking workflow.
description_zh: Obsidian 多终端续接初始化
description_en: Obsidian multi-terminal bootstrap
agent_created: true
---

# obsidian-multi-terminal-bootstrap

## When to use
- The user works on one Obsidian vault from multiple terminals or devices.
- The user says they are tired of remembering current state manually.
- The user wants a lightweight continuation workflow instead of full-vault scanning every time.
- The user wants concrete trigger phrases for “continue”, “check recent changes”, “lint”, or “write back”.

## Steps
1. Read the active vault config from `~/Library/Application Support/obsidian/obsidian.json` and confirm the target vault path.
2. Read `AGENTS.md`, `index.md`, and `log.md` to align with the vault’s structure and append-only conventions.
3. Check whether coordination notes already exist:
   - `00_开工入口_*.md`
   - `00_最近更新摘要_*.md`
   - `00_续接与检查口令_*.md`
4. If they do not exist, create them at the vault root with informative names:
   - startup entry note: current main lines, default startup actions, default shutdown actions, minimal refresh set
   - recent-updates summary: latest 24h/72h hotspots, first files to read, refresh rule
   - trigger-phrases note: short reusable prompts for continue / scan / lint / write-back
5. If the user wants the next stage, add two operational artifacts:
   - a machine-refreshable note such as `00_最近更新摘要_自动刷新版_*.md`
   - a live closing-status note such as `00_收工状态卡_*.md`
6. For the machine-refreshable note, prefer a small local script in the workspace (for example under `.workbuddy/scripts/`) that reads the active vault and rewrites the auto-summary note.
7. Update the top helper-links area in `index.md` so these coordination notes are easy to reopen.
8. Append a `meta` entry to `log.md` describing what was created and why.
9. In the user-facing response, group the recommended trigger phrases into a few simple categories instead of dumping a long list.
10. If the workflow used 15+ tool calls or revealed a reusable pattern, keep this skill updated with improved wording or steps.

## Pitfalls
- Do not default to full-vault scanning on every continuation; use it only for periodic recalibration.
- Do not bury the coordination notes deep inside a subfolder; they should be easy to reopen from any device.
- Do not turn the recent-updates summary into a long diary; keep it short and operational.
- Do not collapse machine-summary and human-summary into one file too early; it is often better to keep an auto-refreshable file and a human judgment file separate.
- Do not treat the closing-status note as a long-term knowledge page; it should stay lightweight and overwrite-friendly.
- Do not skip `log.md`; even helper-document setup is a vault-level change and should be logged.
- Do not create vague file names like `00_入口.md`; use informative titles that show object + purpose.

## Verification
- Confirm the three coordination notes exist.
- Confirm `index.md` top helper-links include the new notes.
- Confirm `log.md` has a new append-only `meta` record.
- Confirm the final reply gives the user 3-6 short phrases they can directly reuse on any device.
