---
name: 静心茶转写整理
description: 从腾讯会议转写数据生成静心茶练习记录 Markdown 文件。格式为中英文逐段交替（英文原文段后紧跟中文翻译段），保留发言人标记。
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
- 目标目录：`/Users/sanzhang/obsidian-private/向内看/静心茶/练习记录/`

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

```bash
cd /Users/sanzhang/.workbuddy/project-resources/p_caf3af7341e849959918adc085c08889/af8ef439-f1df-4d30-bb04-f5a9bfe93285/腾讯会议/scripts
TENCENT_MEETING_TOKEN="47Pe7xReFhj1PEdXdHseQVBu2uy1uVZvthqW6CSUDo513sJm" \
python3 tencent_meeting.py tools/call '{"name": "get_records_list", "arguments": {"start_time": "2026-08-01", "end_time": "2026-08-31"}}'
```

### 2. 获取转写详情

需要 `meeting_record_id` 和 `record_file_id`（从录制列表中获取）：

```bash
python3 tencent_meeting.py tools/call '{"name": "get_transcripts_details", "arguments": {"meeting_record_id": "<record_id>", "record_file_id": "<file_id>"}}'
```

### 3. 获取转写段落

```bash
python3 tencent_meeting.py tools/call '{"name": "get_transcripts_paragraphs", "arguments": {"meeting_record_id": "<record_id>", "record_file_id": "<file_id>"}}'
```

### 转写数据结构

返回 JSON 路径：`data.body`（字符串需二次 JSON 解析）

```
minutes.paragraphs[].sentences[].words[].text
```

- 每个 `paragraph` 包含多个 `sentence`
- 英文句和中文句交替出现在 `sentences` 数组中
- 需要将连续的英文句合并为一个英文段落，连续的中文句合并为对应的中文段落

### 4. 关键参数

| 参数 | 值 |
|---|---|
| 固定会议号（PMI） | `4551316924` |
| Token | `47Pe7xReFhj1PEdXdHseQVBu2uy1uVZvthqW6CSUDo513sJm` |
| 脚本路径 | `/Users/sanzhang/.workbuddy/project-resources/p_caf3af7341e849959918adc085c08889/af8ef439-f1df-4d30-bb04-f5a9bfe93285/腾讯会议/scripts/tencent_meeting.py` |

---

## Token 控制策略

腾讯会议转写数据量大，单次完整转写可能超过 50K token。必须采用管道方式处理：

1. **用 Bash 管道 + Python 提取**：调用 API 后直接用 Python 脚本解析 JSON、提取段落文本、生成 Markdown，避免将原始 JSON 全部加载到上下文
2. **分批处理**：每次只处理一天的录制
3. **直接写文件**：提取后直接写入 `.md` 文件，不要将完整内容回显到上下文

### 推荐处理脚本模式

```bash
# 1. 调用 API 获取转写 JSON，保存到临时文件
python3 tencent_meeting.py tools/call '{...}' > /tmp/transcript_YYYYMMDD.json

# 2. 用 Python 解析并生成 Markdown
python3 -c "
import json, sys
# 读取并解析
with open('/tmp/transcript_YYYYMMDD.json') as f:
    resp = json.load(f)
body = json.loads(resp['data']['body'])
# 提取段落到 Markdown 格式
...
" > /target/path/YYYYMMDD_静心茶练习.md
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
