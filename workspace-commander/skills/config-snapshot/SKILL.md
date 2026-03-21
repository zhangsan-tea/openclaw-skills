---
name: config-snapshot
description: OpenClaw 配置版本管理（时间机器）。通过 claw-snapshot 命令管理配置的版本备份、标签、回滚。
metadata:
  {
    "openclaw":
      {
        "emoji": "🕰️",
        "requires": { "bins": ["claw-snapshot"] },
      },
  }
---

# OpenClaw 配置时间机器

管理 `~/.openclaw/` 目录的配置版本。所有操作通过 `claw-snapshot` 命令完成，版本自动同步到 GitHub 私有仓库。

## 可用命令

通过 shell 执行以下命令：

### 保存快照

```bash
claw-snapshot save "描述信息"
```

保存当前配置状态，自动推送到 GitHub。

### 打版本标签（重要里程碑）

```bash
claw-snapshot tag v版本号 "备注说明"
```

例如：`claw-snapshot tag v1.2 '修好了群聊功能'`

版本号建议用 `v主版本.次版本` 格式，如 v1.1、v1.2、v2.0。

### 查看所有版本标签

```bash
claw-snapshot tag
```

列出所有打过的版本标签、时间和备注。

### 查看快照历史

```bash
claw-snapshot list
```

显示所有 commit 历史（含版本标签标记）。

### 查看当前改动

```bash
claw-snapshot diff
```

显示自上次快照以来改了哪些文件。

### 恢复到指定版本标签

```bash
claw-snapshot restore v版本号
```

例如：`claw-snapshot restore v1.1`

⚠️ **恢复后需要执行 `openclaw gateway restart` 让配置生效。**

这是一个交互式命令，需要用户确认。如果在非交互环境下，先告知用户将要恢复到哪个版本，让用户确认后再执行。

### 回滚到上一个快照

```bash
claw-snapshot rollback
# 或回滚 N 个快照
claw-snapshot rollback 3
```

这也是交互式命令，需要确认。

### 查看某个快照详情

```bash
claw-snapshot show
# 或查看 N 个快照前
claw-snapshot show 2
```

### 手动推送/拉取

```bash
claw-snapshot push    # 推到 GitHub
claw-snapshot pull    # 从 GitHub 拉取
```

## 用户意图映射

当用户说以下类似的话时，执行对应操作：

| 用户说的 | 执行 |
|---|---|
| "备份一下"、"存一下"、"保存配置" | `claw-snapshot save "用户的描述"` |
| "打个标签"、"标记版本 1.2"、"这个版本叫 v1.2" | `claw-snapshot tag v1.2 "备注"` |
| "看看有什么版本"、"查看版本号"、"版本列表" | `claw-snapshot tag` |
| "看看历史"、"快照列表" | `claw-snapshot list` |
| "改了什么"、"有什么变化" | `claw-snapshot diff` |
| "回到 v1.1"、"恢复 1.1 版本" | 先运行 `claw-snapshot tag` 确认版本存在，然后告知用户并执行 `claw-snapshot restore v1.1` |
| "回到上一个版本"、"撤销" | `claw-snapshot rollback` |

## 回复格式

- 执行命令后，将结果用简洁的中文回复用户
- 如果是版本列表，格式化展示版本号、时间和备注
- 如果恢复/回滚成功，提醒用户需要重启 Gateway

## 安全提示

- 恢复/回滚操作会改变配置文件，执行前务必告知用户将要执行什么操作
- 远程仓库是私有的，不用担心泄露
