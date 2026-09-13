---
name: 静心茶转写整理
description: 从腾讯会议转写数据生成静心茶练习记录 Markdown 文件，中英文逐段交替格式（英文原文段后紧跟中文翻译段），保留发言人标记。使用已授权的 tmeet CLI 拉取录制与转写，不在 Skill 内保存 token。
read_when:
  - 用户要拉取/整理静心茶练习记录
  - 用户提到"静心茶转写"、"练习记录"、"补录记录"
  - 需要从腾讯会议抓取静心茶营转写并整理入库
  - 需要批量生成或覆盖静心茶练习记录文件
---

# 静心茶转写整理 Skill

从腾讯会议转写数据生成中英文逐段交替格式的静心茶练习记录。

---

## 格式规范（不可更改项）

### 文件命名

- 格式：`YYYYMMDD_静心茶练习.md`
- 示例：`20260810_静心茶练习.md`
- 目标目录：`/Users/lee/obsidian-private/向内看/静心茶/练习记录/`

### YAML Frontmatter

```yaml
---
date: YYYY-MM-DD
source: 腾讯会议转写
meeting: 21日静心茶营
type: 练习记录
auto_generated: true
---
```

### 正文结构

```markdown
# 21日静心茶营 · M月D日

来源：腾讯会议自动转写，AI 整理格式。

---

**Bommie**：
（英文原文段落）

**中脉空间**：
（中文翻译段落）

**Bommie**：
（英文原文段落）

**中脉空间**：
（中文翻译段落）
...
```

### 核心格式规则

1. **中英文逐段交替**：英文原文段落 → 中文翻译段落，交替出现，不可省略英文
2. **发言人标记**：
   - `**Bommie**：` — 英文原文段落（Bommie 说的英文）
   - `**中脉空间**：` — 中文翻译/口译段落（口译老师的中文转述）
3. **段落对应**：每个英文段落后面紧跟其对应的中文翻译段落
4. **不要**纯中文输出，**不要**纯英文输出
5. **不要**为了节省 token 而过滤掉英文内容

---

## 数据获取流程

### 1. 查询录制列表

使用已授权的 `tmeet` CLI；不在 Skill 中硬编码 token、用户目录或旧脚本路径。

```bash
tmeet record list --start "YYYY-MM-DD" --end "YYYY-MM-DD" --format json
```

从返回结果中记录目标录制的 `record_file_id` 与 `meeting_id`。

### 2. 获取转写段落

```bash
tmeet record transcript-get \
  --record-file-id "<record_file_id>" \
  --meeting-id "<meeting_id>" \
  --pid "0" \
  --limit "250" \
  --format json
```

### 转写数据结构

返回 JSON 路径：`data.minutes.paragraphs[]`。

```text
paragraphs[].speaker.user_name
paragraphs[].sentences[].words[].text
```

- 每个 `paragraph` 包含说话人和多个 `sentence`；必须先按 `speaker.user_name` 保留说话人边界。
- Bommie 英文段后应紧跟对应的「中脉空间」中文段；不得因批处理而删除英文内容。
- 对于只有单语、缺少对应口译或说话人标记的录制，不强行补译；在处理清单中列为「待人工确认」。

### 3. 关键参数与安全边界

| 项目 | 规则 |
|---|---|
| 认证 | 由 `tmeet auth status` 使用现有授权；Skill 内不保存 token |
| 日期范围 | 每次仅查询一个自然月，提取时一次只处理一天 |
| 分页 | 单次 `--limit 250`；段落更多时按服务端返回的分页标识续拉 |
| 输出路径 | `/Users/lee/obsidian-private/向内看/静心茶/练习记录/` |

---

## Token 控制策略

腾讯会议转写数据量大，单次完整转写可能超过 50K token。必须采用管道方式处理：

1. **用 Bash 管道 + Python 提取**：调用 API 后直接用 Python 脚本解析 JSON、提取段落文本、生成 Markdown，避免将原始 JSON 全部加载到上下文
2. **分批处理**：每次只处理一天的录制
3. **直接写文件**：提取后直接写入 `.md` 文件，不要将完整内容回显到上下文

### 推荐处理脚本模式

```bash
# 1. 拉取一天的转写 JSON 到临时文件（不要回显到对话上下文）
tmeet record transcript-get --record-file-id "<record_file_id>" --meeting-id "<meeting_id>" --pid "0" --limit "250" --format json > "/tmp/transcript_YYYYMMDD.json"

# 2. 用 Python 从 data.minutes.paragraphs 读取说话人和 words[].text，
#    直接写入目标 Markdown；写入前保留原文件备份，并生成独立修改清单。
```

---

## 检查清单

处理完成后确认：

- [ ] 文件名格式正确：`YYYYMMDD_静心茶练习.md`
- [ ] 包含 YAML frontmatter
- [ ] 正文标题格式：`# 21日静心茶营 · M月D日`
- [ ] 中英文逐段交替（英文段落 → 中文段落）
- [ ] 发言人标记：`**Bommie**：` 和 `**中脉空间**：`
- [ ] 没有遗漏英文内容
- [ ] 未在 Skill、脚本、日志或输出中写入认证 token
- [ ] 对缺失译文/说话人未知的段落标记「待人工确认」，未擅自补写
