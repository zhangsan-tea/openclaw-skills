# 「热点事件库」Skill — 维护与备份约定

> 本文件是整个 skill 的「宪法」。任何使用、修改、分发本 skill 的人或 AI，都必须先读这一份。

## 核心模型：本地为主，GitHub 为备份

**你原则上不更换 AI 工具，主战场就是 WorkBuddy。** 因此：

- **主工作区（日常修改在这里）**：本地 `~/.codebuddy/skills/热点事件库/`
- **唯一备份源（改了必须同步到这里）**：GitHub `zhangsan-tea/openclaw-skills` → `热点事件库/`

## 硬性规则：改完必须备份（最重要）

> ⚠️ **任何对「热点事件库」skill 内容的修改，完成后必须立即 commit 并 push 到 GitHub。**

具体来说，当你（或 AI）修改了 SKILL.md 或 references/ 下的任何文件后，必须执行：

```bash
cd /path/to/openclaw-skills   # GitHub 仓库的本地 clone
cp -r ~/.codebuddy/skills/热点事件库/. 热点事件库/
git add 热点事件库/
git commit -m "update: 热点事件库 skill 更新说明"
git push origin main
```

**这一条是强制性的，不可跳过。** 改完不 push 等于没备份。

## 修改流程（按此顺序）

1. **直接改本地** `~/.codebuddy/skills/热点事件库/`（这是主工作区，改了立刻在当前环境生效）。
2. 改完**立即备份到 GitHub**（见上一条命令）。
3. 不需要在其他任何地方（工蜂、tdrive、workspace）维护副本——那些位置如有需要，随时从 GitHub 拉取即可。

## 为什么这样设计

- **日常零负担**：改本地文件，下个对话窗口 AI 自动读到新版，无需任何「同步」动作。
- **GitHub 是保险**：万一沙箱环境重置，`~/.codebuddy/skills/` 被清空，可从 GitHub 一键恢复。
- **不依赖人记忆**：把「改完必须 push」写成硬性规则，由 AI 执行，你不用记。

## 如何在环境重置后恢复

如果沙箱被重置，`~/.codebuddy/skills/` 空了，执行：

```bash
git clone https://github.com/zhangsan-tea/openclaw-skills.git
cp -r openclaw-skills/热点事件库 ~/.codebuddy/skills/
```

即可恢复主工作区。

## 其他位置（工蜂 / tdrive / workspace）

这些位置**不维护副本**。它们的作用仅是「历史存档」，如确实需要更新，从 GitHub 拉取覆盖即可，不纳入日常同步。

## 一句话原则

**本地改，GitHub 备。改完必 push，其余全靠拉。**

---
*本文件由「数字智库」项目维护，最后更新：2026-08-15*
