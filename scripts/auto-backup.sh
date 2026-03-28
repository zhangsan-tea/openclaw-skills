#!/bin/bash
# OpenClaw 配置自动备份脚本
# 每天 3:00 执行，带变更说明

cd /Users/lee/.openclaw

DATE=$(date '+%Y-%m-%d %H:%M')
LOG_FILE="/Users/lee/.openclaw/logs/backup.log"

# 检查是否有更改
CHANGES=$(git status --porcelain)

if [ -z "$CHANGES" ]; then
    MSG="ℹ️ OpenClaw 配置无变更，跳过备份 ($DATE)"
    echo "$DATE: 无更改，跳过备份" >> "$LOG_FILE"
    curl -s -X POST "https://api.telegram.org/bot8105171404:AAFef-9ixQJ6exQKlqj2P_INkFTW-JkVfO0/sendMessage" \
        -d chat_id="8051279955" \
        -d text="$MSG" > /dev/null 2>&1
    exit 0
fi

# 统计变更
ADDED=$(echo "$CHANGES" | grep "^??" | wc -l | tr -d ' ')
MODIFIED=$(echo "$CHANGES" | grep "^ M\|^M " | wc -l | tr -d ' ')
DELETED=$(echo "$CHANGES" | grep "^ D\|^D " | wc -l | tr -d ' ')

# 获取主要变更文件（前5个）
MAIN_FILES=$(git status --short | head -5 | awk '{print $2}' | sed 's/.*\///')

# 生成变更说明
CHANGE_DESC=""
[ "$ADDED" -gt 0 ] && CHANGE_DESC="${CHANGE_DESC}+${ADDED}新增 "
[ "$MODIFIED" -gt 0 ] && CHANGE_DESC="${CHANGE_DESC}~${MODIFIED}修改 "
[ "$DELETED" -gt 0 ] && CHANGE_DESC="${CHANGE_DESC}-${DELETED}删除"

# 提交并推送
git add .
git commit -m "auto backup: $DATE | $CHANGE_DESC" --quiet
git push --quiet

# 生成消息
MSG="✅ OpenClaw 配置备份完成

📅 时间：$DATE
📊 变更：$CHANGE_DESC
📝 主要文件：
$(git status --short | head -5 | awk '{for(i=2;i<=NF;i++) printf "  • %s\n", $i}')

🔗 查看：https://github.com/zhangsan-tea/openclaw-bak"

# 发送消息
curl -s -X POST "https://api.telegram.org/bot8105171404:AAFef-9ixQJ6exQKlqj2P_INkFTW-JkVfO0/sendMessage" \
    -d chat_id="8051279955" \
    -d text="$MSG" \
    -d parse_mode="HTML" > /dev/null 2>&1

# 记录日志
echo "$DATE: 已备份 | $CHANGE_DESC" >> "$LOG_FILE"