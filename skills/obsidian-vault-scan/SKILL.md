---
name: obsidian-vault-scan
description: Scan an Obsidian vault in read-only mode to establish current state
  before continuing work across devices or sessions. Use when the user wants a
  full-vault calibration, a recent-changes scan, or a minimal refresh set
  instead of guessing from stale context.
description_zh: Obsidian全库扫描
description_en: Obsidian vault scan
agent_created: true
---

# obsidian-vault-scan

## When to use
Use this skill when the user says things like:
- “先全盘扫描一次”
- “看看 Obsidian 现在最新是什么状态”
- “我在多个终端切换，先帮我校准一下”
- “不要停留在旧记忆，先按最新库状态继续”

Best fit:
1. multi-device / multi-session continuation,
2. Obsidian is the shared source of truth,
3. the user wants read-only calibration before analysis or editing,
4. you need to decide whether full scan or targeted refresh is appropriate.

Do not use it when:
- the user already named exact files to read,
- the task is to write new notes rather than inspect state,
- a personal directory cleanup / move / delete is being requested.

## Steps
1. Confirm the active vault from `~/Library/Application Support/obsidian/obsidian.json`. Do not guess the vault.
2. Treat the scan as read-only. Do not modify, move, rename, or delete anything in the vault during the scan pass.
3. Read `index.md` and `log.md` first if they exist. These are the fastest state anchors.
4. Run a filesystem-wide inventory of the target vault:
   - total file count,
   - markdown count,
   - major file types,
   - top-level directory counts,
   - recently modified files in the last 24h / 72h / 7d.
5. Summarize recent hotspots rather than dumping the whole tree. Focus on directories or file clusters that changed recently.
6. Identify the minimal refresh set for future continuation:
   - `index.md`,
   - `log.md`,
   - the current topic note(s),
   - recent `wiki/sources/*.md` and `wiki/memos/*.md` updates.
7. If useful, write a scan report into the workspace outputs directory, not into the vault. Keep the vault read-only during scanning.
8. In the final answer, distinguish clearly between:
   - what the vault currently contains,
   - what changed recently,
   - what should be read next time instead of scanning the whole vault again.

## Pitfalls
- Do not assume the currently relevant vault by memory alone; re-check `obsidian.json`.
- Do not default to full-vault scans every time. Full scan is for calibration; routine continuation should use targeted refresh.
- Do not treat file count heat as equal to business importance; explain when a hot directory is just generated output or code.
- Do not scan `.obsidian/`, `.git/`, or trash folders unless the user explicitly asks.
- Do not write the report back into the vault unless the user explicitly wants the scan result stored there.

## Verification
- The vault path was confirmed from config.
- The scan was read-only.
- `index.md` and `log.md` were checked first.
- Recent changes were summarized with timestamps or time windows.
- The result included a concrete minimal refresh set for next time.
- If a file report was created, it was written outside the vault and presented to the user.
