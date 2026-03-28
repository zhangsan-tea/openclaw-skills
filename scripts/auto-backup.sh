#!/bin/bash
# OpenClaw 配置自动备份脚本
# 每天 3:00 执行

cd /Users/lee/.openclaw

DATE=$(date '+%Y-%m-%d %H:%M')
LOG_FILE="/Users/lee/.openclaw/logs/backup.log"

# 检查是否有更改
if [ -n "$(git status --porcelain)" ]; then
    git add .
    git commit -m "auto backup: $DATE"
    git push
    
    MSG="✅ OpenClaw 配置备份完成 ($DATE)"
    echo "$DATE: 已备份到 GitHub" >> "$LOG_FILE"
else
    MSG="ℹ️ OpenClaw 配置无变更，跳过备份 ($DATE)"
    echo "$DATE: 无更改，跳过备份" >> "$LOG_FILE"
fi

# 发送消息到 Telegram
curl -s -X POST "https://api.telegram.org/bot8105171404:AAFef-9ixQJ6exQKlqj2P_INkFTW-JkVfO0/sendMessage" \
    -d chat_id="8051279955" \
    -d text="$MSG" \
    -d parse_mode="HTML" > /dev/null 2>&1