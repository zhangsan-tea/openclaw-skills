---
tags:
  - 自建skill
  - 平台集成
  - cnb
  - 代码管理
  - git
created: 2025-07-12
updated: 2025-07-12
status: 已废弃
maintainer: WorkBuddy
source: skills/cnb-connector/
---

# cnb-connector

> ⚠️ **已废弃** — 仅用于连接器名称为 `cnb` 时。如果连接器名称为 `enterprise_cnb-apikey`，请使用新版 cnb-cli-connector。

## 基本信息

| 属性 | 值 |
|------|-----|
| 版本 | 2.0.0 |
| 作者 | CodeBuddy AI |
| 创建日期 | 2026-02-01 |
| 最后更新 | 2026-02-05 |
| 状态 | 已废弃 |

## 核心能力

- clone/push 代码到 cnb.woa.com
- 管理 Pull Request（查询/创建/评论）
- 管理 Issues（查询/更新）
- 通过 `cnb.js` 脚本调用 CNB API

## 认证方式

OAuth Token 通过 `get_token.sh` 获取，使用环境变量 `CNB_TOKEN`：

```bash
source <skill-directory>/scripts/get_token.sh cnb && git clone https://oauth2:${CNB_TOKEN}@cnb.woa.com/{owner}/{repo}.git
```

## cnb.js 命令速查

| 命令 | 说明 |
|------|------|
| `issues --repo x --state open` | 查询 open issues |
| `issues --repo x --number N` | 查询指定 issue |
| `prs --repo x --state all` | 查询所有 PR |
| `prs --repo x --number N` | 查询指定 PR |
| `create-pr --repo x --title T --head H --base B` | 创建 PR |
| `comment-pr --repo x --number N --body B` | 评论 PR |
| `update-issue --repo x --number N --state S` | 更新 issue |

## 源码文件

```
cnb-connector/
├── SKILL.md              # Skill 定义
├── swagger.json          # API 规范
└── scripts/
    ├── clone.sh          # 克隆脚本
    ├── cnb.js            # CNB API 封装
    ├── get_token.sh      # Token 获取
    └── package.json      # npm 依赖
```

## 安全规则

- 禁止输出 Token（不执行 `echo $CNB_TOKEN`）
- 所有命令使用 `$CNB_TOKEN` 环境变量引用，禁止明文
- Token 过期提示用户重新授权
