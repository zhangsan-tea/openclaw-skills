# 「热点事件库」Skill — 唯一权威源说明

> 本文件是整个 skill 的「宪法」。任何使用、修改、分发本 skill 的人或 AI，都必须先读这一份。

## 唯一权威源（Single Source of Truth）

**本 skill 的唯一权威源是：**

```
GitHub 仓库：zhangsan-tea/openclaw-skills
路径：热点事件库/
```

**规则：所有对 skill 内容的修改，只在这里进行。**

其他任何位置出现的本 skill 副本，都是「派生副本」，一律以 GitHub 这份为准。

## 副本清单与定位

| 位置 | 定位 | 同步方式 |
|------|------|----------|
| **GitHub `zhangsan-tea/openclaw-skills`** | 🏆 **唯一权威源** | 修改只在这里 |
| 本地 `~/.codebuddy/skills/热点事件库/`（或 `~/.openclaw/skills/`） | 派生副本（供当前 AI 环境调用） | 从 GitHub 拉取 |
| 本地工作区 `/workspace/skills/热点事件库/` | 派生副本（供分享） | 从 GitHub 拉取 |
| 工蜂 `lyndonzhang/obsidian-private` → `舆情热点/_工作流/热点事件库/` | 派生副本（私域知识库备份） | 从 GitHub 拉取 |
| tdrive 项目资产 `skills/热点事件库/` | 派生副本（项目资产归档） | 从 GitHub 拉取 |

## 修改流程（必须遵守）

1. **只改 GitHub 仓库里的内容**（直接 clone 后修改，或在线编辑后 push）。
2. 修改后 `git commit` + `git push origin main`。
3. 需要同步到某处时，执行「拉取」动作（见下），而不是在目标处直接改。

## 如何在任意环境恢复/同步

在任何新环境（换电脑、换 AI 工具、新沙箱）里，执行：

```bash
# 1. 拉取唯一权威源
git clone https://github.com/zhangsan-tea/openclaw-skills.git

# 2. 复制到本地 skill 注册目录（供当前环境调用）
cp -r openclaw-skills/热点事件库 ~/.codebuddy/skills/

# （若环境用的是 ~/.openclaw/skills/，则改成对应路径）
```

## 同步到其他副本（按需执行）

```bash
# 同步到工作区
cp -r openclaw-skills/热点事件库 /workspace/skills/

# 同步到工蜂（需工蜂 OAuth token）
cd /path/to/obsidian-private
cp -r /path/to/openclaw-skills/热点事件库 "舆情热点/_工作流/"
git add . && git commit -m "sync: 从 GitHub 同步热点事件库 skill" && git push
```

## 重要提醒

- ⚠️ **禁止**在派生副本上直接修改内容（改了也不会回传，只会造成分叉）。
- ⚠️ 发现某处副本与 GitHub 不一致时，**以 GitHub 为准**，用「拉取」覆盖副本。
- ✅ 跨 AI 工具使用时，直接打开 GitHub 上的 `SKILL.md` 正文（去掉 frontmatter）即可，方法论本身是工具无关的。

---
*本文件由「数字智库」项目维护，最后更新：2026-08-15*
