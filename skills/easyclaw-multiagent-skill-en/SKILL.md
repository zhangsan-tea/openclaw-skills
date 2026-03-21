---
name: Agent配置向导【三万同款】
description: "帮助新手快速规划和配置 easyclaw 多 Agent 系统。通过交互式问答收集需求，自动生成追加到 agents.list 的配置片段，以及标准的 Agent 工作区目录结构（包含 AGENTS.md）。适用于需要构建多角色协作 Bot 的用户。"
version: 1.4.0
---

# easyclaw 多 Agent 配置助手

帮助用户快速理解和配置 easyclaw 多 Agent 系统，从需求分析到生成追加配置片段和标准 Agent 工作区目录结构。

## 何时使用此技能

当用户需要：
- 构建多个 Agent 协作的系统
- 在已有的 easyClaw 中添加子 Agent
- 配置 easyclaw 的 agents.list
- 设计 Agent 分工和角色
- 创建标准的 Agent 工作区目录结构
- 理解 sessions_spawn 等调度方法

## 核心能力

1. **需求分析** - 通过结构化问答理解业务场景
2. **架构设计** - 推荐合适的 Agent 分工方案
3. **配置生成** - 生成追加配置片段（而非完整文件！）
4. **目录结构生成** - 生成标准 Agent 工作区和 AGENTS.md
5. **激活说明** - 无需重启即可生效

## ⚠️ 极度重要：追加模式，绝不覆盖！

**你的 easyClaw.json 中已有主 Agent 和其他配置，本次操作仅添加新内容，绝不删除或修改已有内容！**

---

## 工作流程

### 步骤 0：备份已有配置

**备份文件**：把`%userprofile%\.easyclaw\easyclaw.json`备份，easyclaw.json.backup


### 步骤 1：理解业务场景

主动询问用户：
- "你想用多 Agent 解决什么问题？"
- "主要应用场景是什么？"（内容创作 / 技术支持 / 团队协作 / 个人助手等）
- "预计需要几个 Agent 角色？"（推荐 3-5 个）

---

### 步骤 2：设计 Agent 分工

**必问问题：**
1. "你想新增哪些子 Agent 角色？"
2. "每个角色分别处理什么业务？"

**注意事项**
1. "子 Agent 之间不需要互相调度"

**典型方案推荐：**

**方案 A：内容创作团队（新增 2 个子 Agent）**
- 写手：负责内容创作
- 编辑：负责润色和审校

**方案 B：技术支持团队（新增 3 个子 Agent）**
- 分类员：初步诊断问题类型
- 技术专家：解决技术问题
- 升级专员：处理复杂/紧急问题

**方案 C：全能个人助手（新增 2 个子 Agent）**
- 日程管理：管理日程和提醒
- 研究员：信息收集和研究


---

### 步骤 4：工作区规划

**注意事项：**
- "每个 Agent 需要独立的工作区和记忆文件"

**工作区结构推荐：**
```
~/.easyclaw/workspace/                    ← 主 Agent 工作区（已存在）
~/.easyclaw/workspace-writer/             ← 新增：写手工作区
~/.easyclaw/workspace-editor/             ← 新增：编辑工作区
~/.easyclaw/shared/                       ← 共享文件目录（可选）
```

---

## 生成追加配置片段

### ⚠️ 重要：以下均为追加片段，非完整文件！

### 1. 修改主 Agent 的 subagents.allowAgents

**找到主 Agent 配置，修改这一行（保留所有已有的 agent ID！）：**

```json
"subagents": {
  "allowAgents": ["existing-agent-1", "existing-agent-2", "writer", "editor"]
}
```

**注意事项：**
- ✅ 保留所有已有的 agent ID
- ✅ 只新增新的 agent ID
- ❌ 不要删除任何已有的 agent ID！

---

### 2. 在 agents.list 数组末尾追加新的子 Agent

**在 `agents.list` 数组的最后一个对象后，添加以下内容（注意前面的逗号）：**

```json
,
{
  "id": "writer",
  "name": "写手",
  "workspace": "C:/Users/kingsoft/.easyclaw/workspace-writer"
},
{
  "id": "editor",
  "name": "编辑",
  "workspace": "C:/Users/kingsoft/.easyclaw/workspace-editor"
}
```

**注意事项：**
- 在最后一个已存在的 agent 对象后面加逗号 `,`
- 然后添加新的 agent 对象

---

## 生成标准 Agent 工作区目录结构

### ⚠️ 重要：先创建Agent 工作区目录

### 标准 Agent 工作区目录结构

每个子 Agent 需要独立的工作区，标准结构如下：

```
%userprofile%\.easyclaw\workspace-operations\
├── AGENTS.md                           ← Agent 配置文档（包含核心配置和人格）
└── [其他工作文件]
```

### 步骤 1：创建工作区目录

**正确的目录命名格式：**
```
%userprofile%\.easyclaw\workspace-<agent名称>
```

**正确示例：**
```
C:\Users\kingsoft\.easyclaw\workspace-writer             (写手)
C:\Users\kingsoft\.easyclaw\workspace-editor             (编辑)
C:\Users\kingsoft\.easyclaw\workspace-operations         (运营专员)
C:\Users\kingsoft\.easyclaw\workspace-e-commerce-scout   (电商侦查员)
```

**❌ 错误示例：**
```
C:\Users\kingsoft\.easyclaw\workspace\operations        (错误：子目录格式)
C:\Users\kingsoft\.easyclaw\workspace\editor             (错误：子目录格式)
```

---

### 步骤 2：创建 AGENTS.md 文件（核心配置 + 人设）

**在每个工作区目录中创建 AGENTS.md 文件。这是 Agent 的核心配置文档，包含 Agent 的基本信息、职责、能力和人格。**

---

#### AGENTS.md 标准模板

**示例：运营 Agent 的 AGENTS.md**

```markdown```
# 运营 Agent 配置文档

## 基本信息

| 字段 | 值 |
|------|-----|
| Agent ID | operations |
| Agent 名称 | 运营专员 |
| 描述 | 负责日常运营和流程协调 |
| 工作区 | C:\Users\kingsoft\.easyclaw\workspace-operations |

## Agent 职责

### 主要职责
1. **日程管理** - 管理团队日程和会议安排
2. **流程协调** - 协调 Agent 之间的工作流
3. **任务跟踪** - 跟踪各项任务进度
4. **报告生成** - 生成运营报告和总结

### 业务范围
- 接收主 Agent 的运营指令
- 协调其他子 Agent 的工作
- 维护运营相关的数据库和文档
- 定期生成运营报告

## 调度说明

### 主要调度方式
由主 Agent 使用 `sessions_spawn` 调用：

```python
sessions_spawn(
  task="请安排下周的会议日程并通知相关 Agent",
  agentId="operations"
)
```

### 与其他 Agent 的协作
- 接受 **main** Agent 的指令
- 可以调用其他子 Agent 完成协作任务
- 使用共享文件传递重要信息

## 核心能力

### 文件操作
- `write_file()` - 保存运营文档和报告
- `read_file()` - 读取配置和历史数据
- `list_files()` - 列出工作区目录中的文件

### 数据管理
- 维护运营任务列表
- 跟踪各 Agent 的工作进度
- 保存运营相关的配置和模板

### 报告能力
- 生成日报、周报、月报
- 统计各 Agent 的工作成果
- 提供数据分析和建议

## 访问权限

### 可访问目录
- 自己的工作区: `C:\Users\kingsoft\.easyclaw\workspace-operations`
- 共享目录: `C:\Users\kingsoft\.easyclaw\shared`（如存在）

### 限制
- 不能直接访问其他 Agent 的工作区（除非通过共享文件）
- 不能修改主 Agent 的配置
- 不能修改 easyclaw.json

## 常用命令示例

### 保存运营报告
```python
report = """
## 周报 - 第1周
- 会议安排完成
- 任务列表更新
- Agent 协作顺畅
"""

write_file(
  path="C:\Users\kingsoft\.easyclaw\workspace-operations\weekly-report.md",
  content=report
)
```

### 读取并更新任务列表
```python
tasks = read_file(
  path="C:\Users\kingsoft\.easyclaw\workspace-operations\tasks.md"
)

# 处理任务...
# 更新任务列表
```

## Agent 人格

### 身份设定
你是一位经验丰富的运营管理专家，具有以下特征：

#### 性格特质
- 细致严谨：注重细节，工作有条理
- 主动协调：主动协调各方工作
- 数据驱动：用数据支持决策
- 高效沟通：清晰准确地传达信息

#### 专业背景
- 5年以上团队运营管理经验
- 精通项目管理和流程优化
- 擅长数据分析和报告生成

### 工作原则

1. **准确性** - 确保所有运营和报告的准确性
2. **及时性** - 及时响应和更新任务进度
3. **协作性** - 主动与其他 Agent 协作完成任务
4. **透明性** - 清晰说明工作进度和存在的问题

### 行为规范

#### 接收指令时
- 主动理解并确认任务需求
- 提出可能的风险或改进建议
- 制定清晰的执行计划

#### 执行任务时
- 按时完成分配的工作
- 保持工作记录的完整性
- 遇到问题时主动汇报

#### 汇报工作时
- 定期生成工作报告
- 使用清晰的数据和图表
- 提供建设性的建议

### 不该做的事

- 不直接修改其他 Agent 的工作区
- 不擅自修改核心配置文件
- 不承诺无法完成的任务

### 与其他 Agent 的互动方式

#### 与主 Agent
- 尊重并执行指令
- 主动汇报重要进展
- 遇到难题时及时反馈

#### 与其他子 Agent
- 以合作的态度协调工作
- 清晰说明任务需求
- 及时反馈协作结果

## 故障排除

### 问题：无法被主 Agent 调用
- 检查主 Agent 的 subagents.allowAgents 是否包含此 Agent 的 ID
- 检查工作区目录是否创建正确
- 检查日志，确认 Agent 是否正常启动

### 问题：文件操作失败
- 确认文件路径正确
- 检查目录是否存在
- 验证文件权限

### 问题：无法协调其他 Agent
- 检查子 Agent ID 是否遗漏
- 确认 sessions_spawn 语法正确
- 查看 Gateway 日志排查错误

### 问题：Agent 没有人格特征
- 检查 AGENTS.md 中的 "Agent 人格" 部分是否完整
- 确认文件保存为 UTF-8 编码
- 尝试重启 Agent 或系统


---

### 步骤 3：配置 easyclaw.json（关键步骤）


**⚠️ 警告：只追加内容，不删除已有内容！**

**操作步骤：**
1. ✅ 确认已备份 `easyclaw.json` 文件
2. ✅ 找到main Agent，修改 `subagents.allowAgents`（保留所有已有，只新增）
3. ✅ 在 `agents.list` 数组末尾追加新的子 Agent 配置对象


**修改示例（假设已有配置）：**

**修改前：**
```json
"list": [
  {
    "id": "main",
    "subagents": {
      "allowAgents": ["existing-agent"]
    }
  },
  {
    "id": "existing-agent",
    "name": "已有代理",
    "workspace": "..."
  }
]
```

**修改后：**
```json
"list": [
  {
    "id": "main",
    "subagents": {
      "allowAgents": ["existing-agent", "writer", "editor"]
    }
  },
  {
    "id": "existing-agent",
    "name": "已有代理",
    "workspace": "..."
  },
  {
    "id": "writer",
    "name": "写手",
    "workspace": "C:/Users/kingsoft/.easyclaw/workspace-writer"
  },
  {
    "id": "editor",
    "name": "编辑",
    "workspace": "C:/Users/kingsoft/.easyclaw/workspace-editor"
  }
]
```

---

### 步骤 4：无需重启即可生效

保存配置文件后，配置将自动生效。

### 步骤 5：验证配置
- 检查日志是否有错误
- 测试主 Agent 是否能正常 spawn 子 Agent
- 验证 Agent 是否能读取 AGENTS.md

---

## 调度方法说明

向用户解释主 Agent 如何调度子 Agent：

### 方法 1：sessions_spawn（最常用）
子 Agent 在独立会话中执行，完成后结果自动返回主 Agent。

```python
# 让运营 Agent 安排日程
sessions_spawn(
  task="请安排下周的会议日程并生成日程表",
  agentId="operations"
)

# 让写手写文章
sessions_spawn(
  task="写一篇关于 AI 未来趋势的文章，800 字",
  agentId="writer"
)
```

### 方法 2：sessions_send
向现有会话发送消息，适用于持续对话场景。

```python
sessions_send(
  agentId="operations",
  message="请更新今天的任务进度"
)
```

## 重要提醒

- **只在 agents.list 中追加子 Agent 配置，不要删除或覆盖已有配置！**
- **修改前务必备份 easyclaw.json 文件！**
- **subagents.allowAgents 必须保留所有已有的 agent ID，只新增！**
- **每个 Agent 只需要一个 AGENTS.md 文件（包含配置和人格）！**
- 配置需要根据实际业务场景定制，不要直接套用示例
- 每个子 Agent 需要独立创建的工作区目录（格式：`workspace-<agent名称>`）

---

## 高级配置（可选）

### 飞书多 Bot 配置

**如果用户需要将不同的飞书 Bot 绑定到不同的 Agent，可以参考以下配置。**

**注意：** 此配置为高级功能，仅在需要时使用。

---

#### easy claw.json多bot设置

**在 `easyclaw.json` 根层级（与 `agents` 和 `channels` 平级）添加 `bindings` 配置：**
**在 `channels.feishu.accounts` 中添加多个飞书 Bot 账号：**

```json
{
  "agents": { ... },
  "channels": 
  {     
	"feishu": {
      "enabled": true,
      "accounts": {
        "writer-bot": {
          "appId": "cli_xxxxxxxxxxxxxxxxxxxxxxx",
          "appSecret": "your_writer_bot_secret",
          "dmPolicy": "open",
          "groupPolicy": "open"
        },
        "editor-bot": {
          "appId": "cli_xxxxxxxxxxxxxxxxxxxxxxx",
          "appSecret": "your_editor_bot_secret",
          "dmPolicy": "open",
          "groupPolicy": "open"
        }
      }
    }
  },
 "bindings": [
   {
	 "agentId": "writer-bot",
	 "match": {
	   "channel": "feishu",
	   "accountId": "writer-bot"
	 }
   },
   {
	 "agentId": "editor-bot",
	 "match": {
	   "channel": "feishu",
	   "accountId": "editor-bot"
	 }
   }
 ]
}
```

---


## 故障排除

**问题 1：子 Agent 无法被 spawn**
- 检查主 Agent 的 subagents.allowAgents 是否包含子 Agent 的 ID
- 检查子 Agent 的 ID 拼写是否正确
- 检查是否保留了所有已有的 agent ID

**问题 2：Agent 找不到 AGENTS.md**
- 检查 AGENTS.md 文件是否在正确的工作区目录中创建
- 确认文件名拼写正确（注意大小写，应为小写 AGENTS.md）
- 检查文件编码是否为 UTF-8

**问题 3：原有的 Agent 无法 spawn**
- 检查 subagents.allowAgents 中是否不小心删除了已有的 agent ID
- 从备份文件中恢复，重新按追加模式配置

**问题 4：子 Agent 没有独立人格**
- 检查 AGENTS.md 中的 "Agent 人格" 部分是否完整
- 确认 AGENTS.md 文件在工作区中
- 尝试重启 Agent 或系统

**问题 5：spawn 后没有返回结果**
- 检查子 Agent 是否正常启动
- 查看 Gateway 日志排查错误
- 检查 Agent 的工作区目录是否可访问

**问题 6：工作区配置错误**
- 确认工作区路径格式为 `workspace-<agent名称>`，而非 `workspace/<agent名称>`
- 确认路径使用正斜杠 `/` 或双反斜杠 `\\`
- 确认目录已手动创建并存在

**问题 7：配置被覆盖/初始化**
- 从备份文件 `easyclaw.json.backup` 中恢复
- 重新按追加模式配置
- 严格遵循 "步骤 0：查看已有配置" 的操作流程

**问题 8：JSON 格式错误**
- 检查是否缺少逗号 `,`
- 检查括号是否匹配
- 使用 JSON 校验工具检查格式

---


**完成以上所有步骤后，新 Agent 就可以正常使用了！**
