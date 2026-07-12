---
tags:
  - 自建skill
  - 目录索引
  - workbuddy
created: 2025-07-12
updated: 2025-07-12
status: 有效
maintainer: WorkBuddy
---

# 自建 Skills 目录

> **说明**：本目录汇总了 WorkBuddy 自己手搓的所有 Skill。每个 Skill 有独立的子目录存放详细文档。
> **同步规则**：后续新增的自建 Skill 一律同步到本目录下，并推送至关联的 GitHub 仓库。

## Skills 总览

| # | Skill 名称 | 用途 | 核心能力 | 源码位置 |
|---|-----------|------|----------|----------|
| 1 | **automation-task-manager** | 自动化任务管理 | 创建/编辑/删除/查询定时任务，Cron 调度 | `skills/automation-task-manager/` |
| 2 | **computer-use** | 沙箱桌面交互 | 三层感知架构（CDP/AXTree/Screenshot），GUI 操作 | `skills/computer-use/` |
| 3 | **preview** | Web 项目预览 | 启动 Web 服务器，生成预览 URL | `skills/preview/` |
| 4 | **cnb-connector** | CNB 代码平台集成 | clone/push 代码，PR/Issue 管理（cnb.woa.com） | `skills/cnb-connector/` |
| 5 | **figma-connector** | Figma 设计平台集成 | 设计稿还原、代码生成、Design Token 提取 | `skills/figma-connector/` |
| 6 | **github-connector** | GitHub 平台集成 | clone/push 代码，PR 管理 | `skills/github-connector/` |
| 7 | **gongfeng-connector** | 工蜂代码平台集成 | clone/push 代码，PR 管理（git.woa.com） | `skills/gongfeng-connector/` |

## 分类

### 基础设施类
- [[computer-use]] — 桌面交互基础设施
- [[preview]] — Web 预览基础设施

### 平台集成类
- [[github-connector]] — GitHub
- [[cnb-connector]] — 腾讯 CNB
- [[gongfeng-connector]] — 腾讯工蜂
- [[figma-connector]] — Figma 设计

### 工具类
- [[automation-task-manager]] — 定时任务调度

## 维护规则

1. **新增自建 Skill** → 在此目录下创建同名子目录 + 文档，更新本 README
2. **更新 Skill** → 同步更新对应子目录文档，标注更新时间和变更内容
3. **废弃 Skill** → 标注 `status: 已废弃`，不移除文档（保留历史）
4. **GitHub 同步** → 每次变更后推送到关联仓库

---

*最后更新: 2025-07-12 | 维护人: WorkBuddy*
