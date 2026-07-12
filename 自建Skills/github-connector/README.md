---
tags:
  - 自建skill
  - 平台集成
  - github
  - 代码管理
  - git
created: 2025-07-12
updated: 2025-07-12
status: 有效
maintainer: WorkBuddy
source: skills/github-connector/
---

# github-connector

> GitHub 平台集成 — clone/push 代码，查看、创建、评论 Pull Request

## 基本信息

| 属性 | 值 |
|------|-----|
| 版本 | 1.1.0 |
| 作者 | CodeBuddy AI |
| 创建日期 | 2026-02-01 |
| 最后更新 | 2026-02-05 |
| 触发关键词 | GitHub、github.com、PR、Pull Request |

## 核心能力

- clone/push 代码到 GitHub
- 查看 PR 列表和详情
- 创建 PR
- 添加 PR 评论

## 重要原则

**优先使用原生 `git` 命令，不要使用 `gh` CLI。**

## 认证方式

OAuth Token 通过 `get_token.sh` 获取，使用环境变量 `GITHUB_TOKEN`：

```bash
source <skill-directory>/scripts/get_token.sh github && git clone https://oauth2:${GITHUB_TOKEN}@github.com/{owner}/{repo}.git
```

## 常用操作

### 克隆仓库

```bash
# 标准克隆
source <skill-directory>/scripts/get_token.sh github && git clone https://oauth2:${GITHUB_TOKEN}@github.com/{owner}/{repo}.git

# 浅克隆（更快）
source <skill-directory>/scripts/get_token.sh github && git clone --depth 1 https://oauth2:${GITHUB_TOKEN}@github.com/{owner}/{repo}.git

# 克隆指定分支
source <skill-directory>/scripts/get_token.sh github && git clone --depth 1 --single-branch --branch {branch} https://oauth2:${GITHUB_TOKEN}@github.com/{owner}/{repo}.git
```

### 推送代码

```bash
git add .
git commit -m "commit message"
git push origin {branch}

# 如需重设远程 URL
git remote set-url origin https://oauth2:${GITHUB_TOKEN}@github.com/{owner}/{repo}.git
```

### PR 操作

```bash
# 查看 PR 列表
curl -s -H "Authorization: Bearer ${GITHUB_TOKEN}" \
  "https://api.github.com/repos/{owner}/{repo}/pulls?state=open"

# 查看 PR 详情
curl -s -H "Authorization: Bearer ${GITHUB_TOKEN}" \
  "https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"

# 创建 PR
curl -s -X POST -H "Authorization: Bearer ${GITHUB_TOKEN}" \
  -H "Content-Type: application/json" \
  "https://api.github.com/repos/{owner}/{repo}/pulls" \
  -d '{"title":"PR Title","head":"feature-branch","base":"main","body":"Description"}'

# 添加评论
curl -s -X POST -H "Authorization: Bearer ${GITHUB_TOKEN}" \
  -H "Content-Type: application/json" \
  "https://api.github.com/repos/{owner}/{repo}/issues/{pr_number}/comments" \
  -d '{"body":"Comment content"}'
```

## 完整工作流

```bash
# 1. 克隆并创建分支
source <skill-directory>/scripts/get_token.sh github && git clone https://oauth2:${GITHUB_TOKEN}@github.com/owner/repo.git
cd repo
git checkout -b feature/new-feature

# 2. 开发并推送
git add . && git commit -m "Add new feature"
git push -u origin feature/new-feature

# 3. 创建 PR
curl -s -X POST -H "Authorization: Bearer ${GITHUB_TOKEN}" \
  -H "Content-Type: application/json" \
  "https://api.github.com/repos/owner/repo/pulls" \
  -d '{"title":"Add new feature","head":"feature/new-feature","base":"main","body":"Description"}'
```

## 错误处理

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| 401 | Token 无效或过期 | 重新获取 Token |
| 403 | 权限不足或速率限制 | 检查权限或等待 |
| 404 | 仓库不存在 | 检查仓库路径 |

## 安全规则

- 禁止输出 Token
- 所有命令使用 `$GITHUB_TOKEN` 环境变量引用
- Token 过期提示用户重新授权

## 源码文件

```
github-connector/
├── README.md          # 说明文档
├── SKILL.md           # Skill 定义
└── scripts/
    └── get_token.sh   # Token 获取
```
