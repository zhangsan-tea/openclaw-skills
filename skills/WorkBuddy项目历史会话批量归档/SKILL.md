---
name: workbuddy-project-session-batch-archiver
title: WorkBuddy项目历史会话批量归档
description: 批量归档 WorkBuddy 项目侧边栏中的重复历史会话或自动化执行记录。适用于同名任务大量堆积、逐条归档费时、移动本地 JSONL
  后界面仍有数据库索引残留的场景；先只读预检，再备份 workbuddy.db、排除活动会话、移动会话载荷、更新 sessions 索引并核验。
description_zh: WorkBuddy项目历史会话批量归档
description_en: WorkBuddy project session batch archive
agent_created: true
---

# WorkBuddy项目历史会话批量归档

## 触发场景

在以下情况调用：

- 用户要求批量归档项目侧边栏里大量同名历史会话。
- 自动化任务已删除，但每次执行形成的历史记录仍堆在项目中。
- 手动移动 `~/.workbuddy/projects/` 下的 `.jsonl` 后，侧边栏仍显示旧记录。
- 用户明确表示逐条点击归档太费劲，希望一次处理一批。

不要用于删除当前正在运行的会话，不要用于普通 Obsidian 笔记归档，也不要用于清理项目资产文件。

## 安全原则

1. 先预检，后执行。默认只运行 dry-run。
2. 先确认用户要归档的标题范围，再执行写操作。
3. 永远排除 `working / planning / pending / running / active` 状态。
4. 不直接删除会话文件；移动到 `~/.workbuddy/session-archives/`，保留可恢复副本。
5. 修改数据库前，用 SQLite backup API 生成完整备份并执行 `PRAGMA integrity_check`。
6. 只根据 `sessions.title / custom_title` 识别目标，再按 session ID 定位文件；不要全文扫描会话正文作为主要识别方法。
7. 当前对话标题与目标标题相同时，显式传入 `--exclude-session-id`，或先改名再执行。
8. 任何数据库表结构与本 Skill 假设不一致时停止，不猜字段、不直接改库。

## 执行流程

### 1. 明确匹配范围

确认以下信息：

- 标题关键词或精确标题。
- 是否限定某个或多个 `cwd`。
- 允许归档的状态，默认 `completed,Completed,error`。
- 当前会话 ID；存在误匹配可能时加入排除列表。

### 2. 运行只读预检

执行：

```bash
python3 "<skill-dir>/scripts/archive_project_sessions.py" \
  --title-pattern "数字幕僚自动刷新最近更新摘要" \
  --archive-label "数字幕僚自动刷新最近更新摘要"
```

需要限定项目时追加：

```bash
--cwd "/Users/lee/Obsidian/数字幕僚"
```

需要保留当前会话时追加：

```bash
--exclude-session-id "<current-session-id>"
```

读取 JSON 输出，重点核对：

- `session_count`
- `eligible_statuses`
- `cwd_filter`
- `sessions[].id / status / cwd / title / custom_title`
- `payload_count`

### 3. 展示影响并取得确认

向用户说明将归档的会话数量、涉及项目、归档目录和会生成数据库备份。等待用户明确确认后再执行。

不要把 dry-run 当成执行授权；用户只说“看看有多少条”时不得执行。

### 4. 执行归档

获得确认后执行：

```bash
python3 "<skill-dir>/scripts/archive_project_sessions.py" \
  --title-pattern "数字幕僚自动刷新最近更新摘要" \
  --archive-label "数字幕僚自动刷新最近更新摘要" \
  --exclude-session-id "<current-session-id>" \
  --execute \
  --confirm ARCHIVE_MATCHED_SESSIONS
```

脚本按顺序完成：

1. 查询 `workbuddy.db` 的 `sessions` 表。
2. 过滤活动状态和排除的 session ID。
3. 为每个 session ID 在 `~/.workbuddy/projects/*/` 下定位 `.jsonl`、`.meta.json` 和配套目录。
4. 备份数据库到 `~/.workbuddy/session-archives/db-backups/`。
5. 移动会话载荷到时间戳归档目录。
6. 在单个数据库事务中把目标记录更新为 `archived`。
7. 校验所有目标 ID 已是 `archived`。
8. 写出 `manifest.json`。

### 5. 处理已归档但文件仍残留的记录

仅在确认数据库记录已是 `archived`、但活跃项目目录仍有载荷时，单独预检：

```bash
python3 "<skill-dir>/scripts/archive_project_sessions.py" \
  --title-pattern "<标题关键词>" \
  --statuses archived
```

确认后再追加执行参数。不要把 `archived` 与普通状态混在第一次执行中，避免掩盖既有状态差异。

### 6. 核验界面

执行后完成三层核验：

1. 数据库：目标会话状态均为 `archived`。
2. 文件：对应 session ID 的载荷已离开活跃项目目录。
3. 界面：完全退出并重启 WorkBuddy，确认侧边栏不再显示旧记录。

若数据库和文件均已归档但界面仍显示，优先判断为内存缓存；不要反复改数据库。

## 常见问题

- **只移动 JSONL，侧边栏仍显示**：侧边栏主要读取 `workbuddy.db` 的 `sessions` 索引，需同步更新状态。
- **数据库里条目数多于文件数**：同一次执行可能产生多个索引记录，或部分记录没有本地载荷；按 session ID 分别处理，不要求一一等量。
- **同一标题跨多个 cwd**：先 dry-run 看清分布；用户只指定当前项目时传 `--cwd`。
- **当前会话也匹配标题**：传 `--exclude-session-id`，不要依赖修改时间判断。
- **归档途中失败**：脚本尝试回滚已移动载荷；保留数据库备份和错误输出，停止后人工核对，不盲目重跑。
- **用户要求彻底删除**：本 Skill 只归档；永久删除属于另一项高风险操作，必须单独确认并另行处理。

## 验收标准

- dry-run 结果与用户看到的目标记录范围一致。
- 活动会话数量归档前后不变。
- 执行结果包含 `archive_dir`、`database_backup`、`manifest`。
- 数据库备份完整性检查为 `ok`。
- 目标历史记录全部为 `archived`。
- WorkBuddy 重启后侧边栏不再出现该批历史记录。
