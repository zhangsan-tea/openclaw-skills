# WorkBuddy 自建 Skills 知识库

> 使用 Obsidian 管理的 WorkBuddy 自建 Skill 文档库。每个 Skill 独立目录，统一索引。

## 目录结构

```
obsidian-vault/
├── .obsidian/                    # Obsidian 配置
│   └── app.json
└── 自建Skills/                   # 自建 Skill 文档根目录
    ├── README.md                 # 总索引（Skill 总览表）
    ├── 同步规则.md                # 同步规则（记忆）
    ├── _assets/                  # 附件目录
    ├── automation-task-manager/  # 自动化任务管理
    ├── computer-use/             # 沙箱桌面交互
    ├── preview/                  # Web 项目预览
    ├── cnb-connector/            # CNB 平台集成（已废弃）
    ├── figma-connector/          # Figma 设计平台集成
    ├── github-connector/         # GitHub 平台集成
    └── gongfeng-connector/       # 工蜂平台集成
```

## 如何使用

1. 用 Obsidian 打开 `obsidian-vault/` 作为 Vault
2. 通过 `[[双向链接]]` 在 Skill 文档间跳转
3. 每次新增/更新自建 Skill 后，同步更新对应文档

## GitHub 同步

当前环境 GitHub 未登录。请在配置 GitHub 认证后执行：

```bash
cd /workspace/obsidian-vault
git remote add origin <your-repo-url>
git push -u origin main
```
