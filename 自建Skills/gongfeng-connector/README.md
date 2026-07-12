---
tags:
  - 自建skill
  - 平台集成
  - 工蜂
  - 代码管理
  - git
created: 2025-07-12
updated: 2025-07-12
status: 有效
maintainer: WorkBuddy
source: skills/gongfeng-connector/
---

# gongfeng-connector

> 工蜂代码平台集成 — clone/push 代码，创建和管理 Pull Request（git.woa.com）

## 基本信息

| 属性 | 值 |
|------|-----|
| 版本 | 2.3.0 |
| 作者 | CodeBuddy AI |
| 创建日期 | 2026-02-01 |
| 最后更新 | 2026-02-05 |
| 触发关键词 | 工蜂、git.woa.com、merge request |

## 核心能力

- clone/push 代码到工蜂（git.woa.com）
- 查看 PR（Merge Request）列表和详情
- 创建 PR
- 添加 PR 评论
- 合并 PR

## 基础信息

- **Git URL**: `https://git.woa.com`
- **API URL**: `https://git.woa.com/api/v3`
- **认证**: `Authorization: Bearer <token>`

## 认证方式

OAuth Token 通过 `get_token.sh` 获取，使用环境变量 `GONGFENG_TOKEN`：

```bash
source <skill-directory>/scripts/get_token.sh gongfeng && git clone https://oauth2:${GONGFENG_TOKEN}@git.woa.com/{group}/{project}.git
```

## 常用操作

### 克隆仓库

```bash
# 标准克隆
source <skill-directory>/scripts/get_token.sh gongfeng && git clone https://oauth2:${GONGFENG_TOKEN}@git.woa.com/{group}/{project}.git

# 浅克隆
source <skill-directory>/scripts/get_token.sh gongfeng && git clone --depth 1 https://oauth2:${GONGFENG_TOKEN}@git.woa.com/{group}/{project}.git
```

### PR（Merge Request）操作

```bash
# 获取 PR 列表
curl -H "Authorization: Bearer $GONGFENG_TOKEN" \
  "https://git.woa.com/api/v3/projects/{project_id}/merge_requests?state=opened"

# 获取 PR 详情
curl -H "Authorization: Bearer $GONGFENG_TOKEN" \
  "https://git.woa.com/api/v3/projects/{project_id}/merge_requests/{mr_iid}"

# 创建 PR
curl -X POST -H "Authorization: Bearer $GONGFENG_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"source_branch":"feature","target_branch":"main","title":"PR标题"}' \
  "https://git.woa.com/api/v3/projects/{project_id}/merge_requests"

# 添加 PR 评论
curl -X POST -H "Authorization: Bearer $GONGFENG_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"body":"评论内容"}' \
  "https://git.woa.com/api/v3/projects/{project_id}/merge_requests/{mr_iid}/notes"

# 合并 PR
curl -X PUT -H "Authorization: Bearer $GONGFENG_TOKEN" \
  -d '{"should_remove_source_branch":true}' \
  "https://git.woa.com/api/v3/projects/{project_id}/merge_requests/{mr_iid}/merge"
```

## 常用 API

| 操作 | API |
|------|-----|
| PR 列表 | `GET /projects/{id}/merge_requests` |
| PR 详情 | `GET /projects/{id}/merge_requests/{iid}` |
| 创建 PR | `POST /projects/{id}/merge_requests` |
| PR 评论 | `POST /projects/{id}/merge_requests/{iid}/notes` |
| 合并 PR | `PUT /projects/{id}/merge_requests/{iid}/merge` |
| PR 变更 | `GET /projects/{id}/merge_requests/{iid}/changes` |
| 创建分支 | `POST /projects/{id}/repository/branches` |

## 完整工作流

```bash
# 1. 克隆并创建分支
source <skill-directory>/scripts/get_token.sh gongfeng && git clone https://oauth2:${GONGFENG_TOKEN}@git.woa.com/{group}/{project}.git
cd {project}
git checkout -b feature-branch

# 2. 开发并推送
git add . && git commit -m "Add feature"
git push -u origin feature-branch

# 3. 创建 PR
curl -X POST -H "Authorization: Bearer $GONGFENG_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"source_branch":"feature-branch","target_branch":"main","title":"Add feature"}' \
  "https://git.woa.com/api/v3/projects/{project_id}/merge_requests"
```

## 安全规则

- 禁止输出 Token
- 所有命令使用 `$GONGFENG_TOKEN` 环境变量引用
- Token 过期提示用户重新授权

## 源码文件

```
gongfeng-connector/
├── SKILL.md              # Skill 定义
└── scripts/
    ├── get_token.sh      # Token 获取
    └── gongfeng_api.sh   # API 调用脚本
```
