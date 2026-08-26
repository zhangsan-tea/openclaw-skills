---
name: 静心茶转写校对
description: 对静心茶转写整理的 .md 文件进行五层交叉互检：音转文硬伤纠偏、中文反推英文标点、正念语义校准、修辞保留确认、输出标记。
read_when:
  - 用户要求校对静心茶转写记录
  - 用户提到静心茶录音转文字需要校对、交叉检查、互检
  - 用户要求纠正音转文错误、断句、标点
  - 静心茶转写记录需要质量审核
  - 与静心茶转写整理配合使用
---

# 静心茶转写校对 Skill

对静心茶转写整理 Skill 生成的 `.md` 文件进行交叉互检和语义校准，输出校对后的版本及修改清单。

---

## 前置依赖

- 必须先完成 `静心茶转写整理` Skill 的提取工作
- 输入：已生成的 `YYYYMMDD_静心茶练习.md` 文件
- 输出：校对后的 `.md` 文件 + `.changes.md` 修改清单

---

## 五层交叉互检模型

### Layer 1：音转文硬伤（英文 → 中文方向）

识别腾讯会议语音转文字产生的明显错误：

| 类型 | 示例 | 修正 |
|---|---|---|
| 语音听错词 | Dogs → Thoughts | **Thoughts** |
| 介词听错 | Two silence → **to** silence | **to** |
| 近音词混淆 | science → **silence** | **silence** |
| 近音词混淆 | common thing → **commenting** | **commenting** |
| 拼写/大小写 | if / i / who with | **If** / **I** / **with** |
| 重复词 | when that when that | when that |

**规则**：只改语音识别明显错误，不改原意修辞。

### Layer 2：中文反推英文（中文 → 英文方向）

通过中文语义反推英文的断句和标点问题：

- 英文句号位置是否导致语义断裂
- 英文是否遗漏了被语音转写"吃掉"的片段
- 英文断句是否错位（如 `Then even your speech. Will become...` → `Then even your speech will become...`）

**规则**：根据中文翻译的完整性，反推英文原文的断句是否合理。

### Layer 3：正念语义校准

从静心茶/正念的专业语境进行校准：

- **术语准确性**：stage vs state, mere 是否应为 meditative/inner/here
- **逻辑自洽性**：上下文是否连贯，概念是否完整
- **三要素完整性**：如"三件事"是否清晰列出（意图→放松→沉入空无）
- **前后呼应**：同一概念在不同段落中的表述是否一致

**规则**：不改动波密原意，只做使语义更准确的微调。

### Layer 4：修辞保留确认

波密常用的修辞手法，**不可改动**：

| 修辞类型 | 示例 | 处理方式 |
|---|---|---|
| 动词排比 | **watch, to observe** | 保留并列，不合并为单一词汇 |
| 不定式排比 | **Not to struggle, not to try** | 保留不定式结构 |
| 名词排比 | **the system of expression, the system of watching...** | 保留重复结构 |
| 排比问句 | **Is it silence, or is it impatience?** | 保留重复句式 |
| 短句重复 | **An expression of silence. An expression of listening...** | 保留短句节奏 |

**规则**：这些修辞是波密的表达风格，校对时只标注、不改动。

### Layer 5：输出标记

每处修改须标注类型：

| 标记 | 含义 | 使用场景 |
|---|---|---|
| `(音转文修正)` | 语音识别明显错误 | Dogs→Thoughts, Two→to |
| `(断句修正)` | 标点或断句调整 | 句号位置、合并被断开的句子 |
| `(语义校准)` | 使语义更准确 | stage→state, 补全遗漏概念 |
| `(修辞保留)` | 虽有疑问但保留原文 | watch/observe 排比, mere 存疑 |
| `(待确认)` | 语义存疑，需人工复核 | 无法判断的发音混淆 |

---

## 交叉互检流程

```
Step 1: 通读全文，标记明显的音转文硬伤（Layer 1）
Step 2: 逐段中文反推英文，检查断句和标点（Layer 2）
Step 3: 从正念语境检查术语和逻辑（Layer 3）
Step 4: 确认波密修辞未被改动（Layer 4）
Step 5: 输出校对后正文 + 修改清单（Layer 5）
```

---

## 常见音转文错误速查表

执行校对时优先检查以下高频错误模式：

| 语音转写 | 最可能的原文 | 语境线索 |
|---|---|---|
| Dogs | **Thoughts** | 前句"listen to the images"，后接念头 |
| Two | **to** | "from chattering Two silence" |
| science | **silence** | "expression of that science" 前后文都在讲宁静 |
| common thing | **commenting** | "drop the common thing around everything" → 放下评论 |
| stage | **state** | "the stage you're in now" → 语境指状态 |
| mere | **?** | 可能是 meditative/inner/here，需人工确认 |
| learn of | **learn from** | "learn of anything" 应为 learn from |
| if 句首小写 | **If** | 句首应大写 |
| i / we 小写 | **I / We** | Bommie 自述时首字母大写 |
| when that when that | **when that** | 重复词去重 |

---

## 输出格式

### 校对后正文

遵循静心茶转写整理的原格式规范：

```markdown
**Bommie**：
（校对后的英文原文）

**中脉空间**：
（校对后的中文翻译）
```

### 修改清单（同文件末尾或独立 .changes.md）

```markdown
## 修改记录

| 行号 | 原文 | 修改后 | 类型 |
|---|---|---|---|
| ~47 | Dogs. | Thoughts. | 音转文修正 |
| ~89 | Two silence | to silence | 音转文修正 |
| ~105 | science | silence | 音转文修正 |
| ~203 | common thing | commenting | 音转文修正 |
| ~156 | if these three | If these three | 断句修正 |
```

---

## 与静心茶转写整理的关系

| 环节 | Skill | 职责 | 输出 |
|---|---|---|---|
| 提取 | `静心茶转写整理` | 从腾讯会议拉取转写、格式化、入库 | `YYYYMMDD_静心茶练习.md` |
| 校对 | `静心茶转写校对` | 交叉互检、纠错、语义校准 | 校对后的 `.md` + 修改清单 |

**执行顺序**：必须先完成提取，再执行校对。两个环节可以分人执行。
