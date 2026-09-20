---
name: stillness-tea-transcript-organize
description: 从腾讯会议转写数据生成静心茶练习记录 Markdown 文件，中英文逐段交替格式（英文原文段后紧跟中文翻译段），保留发言人标记。使用已授权的 tmeet CLI 拉取录制与转写，不在 Skill 内保存 token。触发：拉取/整理静心茶练习记录、提到「静心茶转写/练习记录/补录记录」、批量生成或覆盖练习记录文件。
description_zh: 静心茶转写整理
description_en: Stillness Tea Transcript Organize
disable: false
agent_created: true
read_when:
  - 用户要拉取/整理静心茶练习记录
  - 用户提到「静心茶转写」「练习记录」「补录记录」
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

### 0. 检查授权（每次开工先做）

使用已授权的 `tmeet` CLI；不在 Skill 中硬编码 token、用户目录或旧脚本路径。

```bash
tmeet auth status
```

- 返回 `Not logged in` 时执行 `tmeet auth login --no-browser`，把打印出的 `authorize url` 交给 Lee 在浏览器确认，完成后再继续。
- 报错 `file lock timeout (5s): ~/.tmeet/token.lock` —— 说明上次登录进程残留，执行 `rm -f ~/.tmeet/token.lock` 后重跑。
- 凭证失效的典型迹象：`~/.tmeet/config.json` 缺失、`~/Library/Application Support/tmeet/` 下只剩 `.enc.lock` 没有 `.enc`。

#### 授权窗口只有约 5 分钟 —— 用续期循环，不要反复找 Lee 要链接（2026-09-20 立）

实测：`tmeet auth login` 打印的 `authorize url` **有效期约 5 分钟**，超时后进程自行退出，需重新发起。若只发一条链接给用户，用户稍一分神就必然超时，来回折腾。

正确做法：挂一个**自动续期循环**——一轮超时立刻开新一轮，任何时刻都有一条活链接可用。

```bash
cat > /tmp/tmeet_wait.sh <<'SH'
#!/bin/zsh
LOG=/tmp/tmeet_url.txt
: > "$LOG"
for i in {1..24}; do
  if tmeet auth status 2>/dev/null | grep -q "Logged in"; then
    echo "$(date '+%H:%M:%S') LOGIN_OK" >> "$LOG"; break
  fi
  ( tmeet auth login --no-browser > /tmp/tmeet_cycle.log 2>&1 ) &
  PID=$!
  for j in {1..25}; do sleep 1; grep -q "authorize url:" /tmp/tmeet_cycle.log 2>/dev/null && break; done
  echo "$(date '+%H:%M:%S') $(grep -m1 'authorize url:' /tmp/tmeet_cycle.log | sed 's/.*authorize url: //')" >> "$LOG"
  wait $PID
  tmeet auth status 2>/dev/null | grep -q "Logged in" && { echo "$(date '+%H:%M:%S') LOGIN_OK" >> "$LOG"; break; }
done
SH
chmod +x /tmp/tmeet_wait.sh
```

- **必须以后台任务方式启动**（`run_in_background: true`），否则会阻塞当前轮次。
- 启动后 `sleep 10` 再读 `/tmp/tmeet_url.txt`，取最后一条链接发给用户，并明确告知「有效期约 5 分钟，超时回我一个字，我立刻贴下一条」。
- 循环约可撑 2 小时（24 轮 × 5 分钟），足够用户随时点开。
- **若循环进程已死**（`ps aux | grep tmeet_wait.sh` 为空），先 `pkill -f "tmeet auth login"`，再重启循环。
- 授权成功后 `tmeet auth status` 会显示 `Logged in` + OpenId + UserName，AccessToken 有效期约 6 小时、RefreshToken 约 30 天。
- 排查线索：`~/.tmeet/logs/tmeet-YYYY-MM-DD.log` 会记录 `auth logout`、超时等事件——凭证被静默清空时先查这里。

### 1. 查询录制列表

```bash
tmeet record list --start "2026-09-01T00:00:00+08:00" --end "2026-09-30T23:59:59+08:00" --format json
```

**日期必须是 RFC3339 完整格式**（`2026-09-01T00:00:00+08:00`）。只给 `YYYY-MM-DD` 会报 `--start format error`。

返回路径 `data.record_meetings[].record_files[]`，记录目标录制的 `record_file_id` 与 `meeting_id`。

> 同一场会议常有多条 `record_files`（会前短片段 + 正片）。取**时长覆盖完整会议**的那条；会前短片段常已被删除，拉取时会报 `error_code 4051 录制文件已经被删除`，直接跳过即可。
>
> 排序建议：同一天按 `record_files[].record_start_time` 升序，**取最后一条（时长最长）为主录**。实测主录时长 45–130 分钟，会前短片段 0–6 分钟。

#### ⚠️ 录制「查不到」≠「不存在」——转码与可见有延迟，隔日必须复查（2026-09-20 实测立）

**实例**：9/16、9/18、9/19 三天在 9/18 早间按会议号全类型搜索 + 逐日复核时，均为 **0 场**，曾被判定为「无云端录制」；9/20 早间再查，**三天全部出现**，且 `state_int = 3（转码完成）`。

⇒ **铁律**：
1. **绝不下「这几天没有录制」的结论**。查不到只说明**此刻**不可见。
2. 补录任务里若有「今天/昨天」的场次缺失，先记为**待复查**，**次日再查一次**，不要写进「不要再试」的清单。
3. 查录制前先核 `state_int`：`3` = 转码完成可拉转写；未完成的场次等下一轮。
4. 一次把搜索窗口放宽到「目标日 ±7 天」，把已在库/未在库的所有静心茶场次一次列全，再按日期差集找缺口——比逐日单查更省调用，也不会漏掉延迟可见的场次。

### 2. 获取转写段落（**两步**，不可省）

**第一步：拿段落索引与总段数**

```bash
tmeet record transcript-paragraphs \
  --record-file-id "<record_file_id>" \
  --meeting-id "<meeting_id>" \
  --format json
```

返回 `data.pids[]`（每项含 `pid` / `start_time` / `end_time`）与 **`data.total`**（总段数）。**这一步拿不到任何正文文字**——只用来确定 `total`。

> ⚠️ 常见误判：直接拿这个接口的结果去数段落，会得到「0 段」的错觉（它没有 `minutes.paragraphs` 字段）。正文必须走第二步。

**第二步：按 `pid` 拉正文**

```bash
tmeet record transcript-get \
  --record-file-id "<record_file_id>" \
  --meeting-id "<meeting_id>" \
  --pid "0" \
  --limit "<total + 10>" \
  --format json
```

- `--limit` 给 `total + 10` 即可**一次拉全**（实测 516 段的场次一次到位）。
- 若取回的 `paragraphs` 数 < `total`，退化为**分批循环**：`--pid` 从 0 开始，每次 `--limit 50`，累加结果。

### 转写数据结构

返回 JSON 路径：`data.minutes.paragraphs[]`。

```text
paragraphs[].speaker.user_name
paragraphs[].sentences[].words[].text
```

- 每个 `paragraph` 包含说话人和多个 `sentence`；必须先按 `speaker.user_name` 保留说话人边界。
- Bommie 英文段后应紧跟对应的「中脉空间」中文段；不得因批处理而删除英文内容。
- 对于只有单语、缺少对应口译或说话人标记的录制，不强行补译；在处理清单中列为「待人工确认」。
- **说话人映射：编号不稳定，必须按语种判定，不可按编号机械映射**（2026-09-20 实测修正）：

  | 场次 | `中脉空间-发言人1` | `中脉空间-发言人2` |
  |---|---|---|
  | 20260914 | 全部**英文**（109 段） | 全部**中文**（109 段） |
  | 20260916 | 全部**英文**（82 段） | 全部**中文**（81 段） |
  | 20260917 | 以**中文**为主（82 中 + 2 中英混说） | 以**英文**为主（79 英 + 1 中「拜拜。」） |
  | 20260918 | 全部**英文**（78 段） | 全部**中文**（77 段） |
  | 20260919 | 英文 225 / 中文 235（**同一账号内混合**） | 同上（另含 5 位学员独立声纹） |

  ⇒ **发言人编号随「谁先开口」而变，两场之间可以完全相反。** 判定规则只有一条：
  - 段落 `speaker.user_name` **以 `中脉空间` 开头** → 按**段落语种**定标签：英文字符多于中文字符 → `**Bommie**`；否则 → `**中脉空间**`。
    实际有三种形态，都要覆盖：`中脉空间`（无后缀）、`中脉空间-发言人N`、`中脉空间 共享音频`（唱诵/播放段，归同一判定）。
    20260919 实测同一账号下英文 225 段、中文 235 段**交错**，`中脉空间-发言人1/2` 的区分与语种无稳定对应——**只能逐段看语种**。
  - `speaker.user_name` 是**学员名 + 声纹后缀**（如 `安然入税-发言人1`、`安然入税-发言人2`）→ **剥掉 `-发言人N`，取基础人名**做标签（同一人的两个编号是声纹切分，不是两个人）。
  - `speaker.user_name` 是**具体人名**（如「夜子」「利军」「谷雨」「路翠Lucy」「Elsa.艾莎」）→ 直接用该人名做标签，**不改写、不并入老师段**。
  - 判语种用 `len(re.findall(r"[A-Za-z]", t)) > len(re.findall(r"[\u4e00-\u9fff]", t))`；对中英混说段（如波密说「啊，所以所以。Halfway in the circle.」）以多数语种为准。
- 老师与学员共用账号时，学员**只有独立声纹**才会被识别出真实姓名；否则会被并进「发言人N」。逐场核一下非老师标签的数量，异常为 0 时在清单里记一句。
- 同一场若出现**连续同标签段**（ASR 把一句切成两帧），**保留原始 1:1 帧结构**，不做合并；库内既有成品同样存在该现象（如 20260912 有 105 处）。
- 文本拼接：`sentences[].words[].text` 顺序拼接后 `strip()`；空段落写 `（此处无清晰内容）`。
- 拉到 JSON 后用 `python3` 直接解析生成 md，**不要把原始 JSON 读进上下文**（单日约 120KB）。

### 2.5 会前片段、平台屏蔽词、库内版式对齐（2026-09-20 补）

**① 一场会议通常有 2 条 `record_files`**：会前短片段（几分钟、几 MB）+ 正片（45–50 分钟、几百 MB）。取**时长覆盖完整会议**的那条。会前短片段常已被删除，拉取时报 `error_code 4051 录制文件已经被删除`，跳过即可。

**② 转写里可能出现平台屏蔽词**：原始 JSON 中该词被替换成字面量 `**`（实测出现在会阴、乳头等身体词位置）。落到 Markdown 后 `**` 会破坏强调语法，**必须处理**：

- 优先按**同段中文口译** + 上下文还原该词，写成正常英文单词；
- 同时在 `校对记录/*.changes.md` 的「修改记录」标注为「屏蔽补出」、并在「待确认」里写清「原文为 `**`，还原属推断」；
- 不要留 `**` 在成品里（自检项：`残留 ** 掩码 = 0`）。

**③ 入库版式必须对齐库内主流形态**，开工前先跑一次统计再落笔，不要凭记忆：

```bash
cd ".../练习记录"
# frontmatter 形态
for f in *_静心茶练习.md; do sed -n '2p' "$f"; done | sort | uniq -c | sort -rn | head
# 标签形态（同行式 or 换行式）
```

2026-09-20 实测的库内主流（约 57 篇，且与紧邻的 9/15 一致）：

```markdown
---
date: YYYY-MM-DD
source: 腾讯会议转写
meeting: 21日静心茶营
type: 练习记录
auto_generated: true
---

# 21日静心茶营 · M月D日

来源：腾讯会议自动转写，AI 整理格式。

---

**Bommie**：
（英文段）

**中脉空间**：
（中文段）
```

- **双标签**（`**Bommie**：` + `**中脉空间**：`）、**换行式**（标签独占一行，正文在下一行）。
- ⚠️ 库里存在两种少数派变体，不要跟错：① `tags: [静心茶, 练习记录]` + `# 静心茶练习`（20260906–20260913 共 8 篇、及 0607/0614 等）；② 单标签「只留 `**Bommie**`、中文紧跟不带标签」（20260915、20260822–0825 等 11 篇）。发现新文件与主流不一致时，**先报告差异再产出**，不要静默跟随。

### 3. 关键参数与安全边界

| 项目 | 规则 |
|---|---|
| 认证 | 由 `tmeet auth status` 使用现有授权；Skill 内不保存 token |
| 日期范围 | 录制查询一次可放宽到「目标月 ±7 天」，再按日期差集找缺口；转写提取一次只处理一天 |
| 分页 | 先 `transcript-paragraphs` 取 `total`，再 `transcript-get --pid 0 --limit total+10` 一次拉全；不足时按 50 段一批循环 |
| 输出路径 | `/Users/lee/obsidian-private/向内看/静心茶/练习记录/` |

---

## Token 控制策略

腾讯会议转写数据量大，单次完整转写可能超过 50K token。必须采用管道方式处理：

1. **用 Bash 管道 + Python 提取**：调用 API 后直接用 Python 脚本解析 JSON、提取段落文本、生成 Markdown，避免将原始 JSON 全部加载到上下文
2. **分批处理**：每次只处理一天的录制
3. **直接写文件**：提取后直接写入 `.md` 文件，不要将完整内容回显到上下文

### 推荐处理脚本模式

```bash
# 1a. 先取段落索引拿到 total（此步无正文）
tmeet record transcript-paragraphs --record-file-id "<fid>" --meeting-id "<mid>" --format json \
  | python3 -c "import json,sys; d=json.load(sys.stdin)['data']; print(d['total'])"

# 1b. 再按 pid 拉正文到临时文件（不要回显到对话上下文）
tmeet record transcript-get --record-file-id "<fid>" --meeting-id "<mid>" \
  --pid "0" --limit "<total+10>" --format json > "/tmp/transcript_YYYYMMDD.json"

# 2. 用 Python 从 data.minutes.paragraphs 读取说话人和 words[].text，
#    直接写入目标 Markdown；写入前保留原文件备份，并生成独立修改清单。
```

> 若把两步合并成一次 `transcript-get --pid 0 --limit 250` 也能拿到前 250 段，但**长场次（如 128 分钟 / 516 段）会截断**——仍建议先取 `total` 再定 `--limit`。

---

## 与校对环节的衔接（固定流水线）

入库与校对是两件事，但常在同一次任务里连着做（用户说「入库和校对」）。顺序固定，不要跳步：

1. **生成入库稿** → `练习记录/YYYYMMDD_静心茶练习.md`（脚本机械映射，忠实于原始转写，不改字）
2. **立刻备份** → `练习记录/校对前备份/YYYYMM/YYYYMMDD_静心茶练习.md`，并 `md5` 双向校验一致
3. **通读 + 五层互检**（转 `stillness-tea-transcript-proofread` skill）→ 在**入库稿**上改
4. **落四节式清单** → `练习记录/校对记录/YYYYMM/YYYYMMDD_静心茶练习.changes.md`
   （四节：修改记录 / 标点与分段优化 / 待确认（未改）/ 自检）
5. **跑自检脚本**：保留率、frontmatter 一致、中文段 ≤150 字、游离句号/中文词间空格/多余空行/行尾空格/标点前空格/点号异常/小写 i 全部为 0

关键约束：
- 修正用**逐条替换 + 命中计数**的脚本做，不要手改长文件；未命中的条目必须回看原文（多半是引文抄错），不允许静默跳过。
- **英文长段不适用中文 150 字上限**。库内历史成品的英文单行最长可达 610 字符，属正常；只有**中文段** ≤150 字（容差 170，超出需在清单里说明）。
- 保留率合格区间 **90%–102%**（Get 笔记「空格代标点」形态可到 ≤103%）。

## 检查清单

处理完成后确认：

- [ ] 文件名格式正确：`YYYYMMDD_静心茶练习.md`
- [ ] YAML frontmatter **与库内主流形态一致**（先统计再落笔，不凭记忆）
- [ ] 正文标题格式：`# 21日静心茶营 · M月D日`
- [ ] 中英文逐段交替（英文段落 → 中文段落）
- [ ] 发言人标记：`**Bommie**：` 和 `**中脉空间**：`（**按语种判定，不按 `发言人N` 编号**）
- [ ] 学员独立声纹（如「夜子」）保留原姓名标签
- [ ] 没有遗漏英文内容；段落数与原始转写段落数一致
- [ ] **成品内无残留 `**` 屏蔽掩码**
- [ ] 入库稿已备份到 `校对前备份/YYYYMM/` 且 md5 一致
- [ ] 未在 Skill、脚本、日志或输出中写入认证 token
- [ ] 对缺失译文/说话人未知的段落标记「待人工确认」，未擅自补写
