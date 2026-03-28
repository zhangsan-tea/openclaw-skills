#!/bin/bash
# OpenClaw 配置自动备份脚本
# 每天 3:00 执行

cd /Users/lee/.openclaw

# 检查是否有更改
if [ -n "$(git status --porcelain)" ]; then
    git add .
    git commit -m "auto backup: $(date '+%Y-%m-%d %H:%M')"
    git push
    echo "$(date): 已备份到 GitHub"
else
    echo "$(date): 无更改，跳过备份"
fi