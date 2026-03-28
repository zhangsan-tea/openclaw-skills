#!/bin/bash
# OpenClaw 配置自动备份脚本
# 每天 3:00 执行，带人性化变更说明

cd /Users/lee/.openclaw

DATE=$(date '+%Y-%m-%d %H:%M')
LOG_FILE="/Users/lee/.openclaw/logs/backup.log"

# 检查是否有更改
CHANGES=$(git status --porcelain)

if [ -z "$CHANGES" ]; then
    MSG="ℹ️ OpenClaw 配置无变更 ($DATE)"
    curl -s -X POST "https://api.telegram.org/bot8105171404:AAFef-9ixQJ6exQKlqj2P_INkFTW-JkVfO0/sendMessage" \
        -d chat_id="8051279955" \
        -d text="$MSG" > /dev/null 2>&1
    exit 0
fi

# 分析变更内容
CHANGE_NOTES=""

# 1. 检查新增的 skill
NEW_SKILLS=$(echo "$CHANGES" | grep "^?? skills/" | awk '{print $2}' | sed 's|skills/||' | sed 's|/.*||')
if [ -n "$NEW_SKILLS" ]; then
    for skill in $NEW_SKILLS; do
        CHANGE_NOTES="${CHANGE_NOTES}🆕 新增 Skill: $skill\n"
    done
fi

# 2. 检查新增的 agent
NEW_AGENTS=$(echo "$CHANGES" | grep "^?? agents/" | awk '{print $2}' | sed 's|agents/||' | sed 's|/.*||')
if [ -n "$NEW_AGENTS" ]; then
    for agent in $NEW_AGENTS; do
        CHANGE_NOTES="${CHANGE_NOTES}🤖 新增 Agent: $agent\n"
    done
fi

# 3. 检查 openclaw.json 主配置变更
if echo "$CHANGES" | grep -q "openclaw.json"; then
    # 尝试提取具体变更
    CONFIG_CHANGES=""
    
    # 检查是否有新增 telegram 账户
    NEW_TG=$(git diff openclaw.json 2>/dev/null | grep -E '^\+.*"name".*行政|助理|顾问' | head -2)
    if [ -n "$NEW_TG" ]; then
        CONFIG_CHANGES="${CONFIG_CHANGES}• 新增 Bot 账户\n"
    fi
    
    # 检查是否有新增 cron 任务
    NEW_CRON=$(git diff openclaw.json 2>/dev/null | grep -E '^\+.*"name".*备份|提醒|检查' | head -2)
    if [ -n "$NEW_CRON" ]; then
        CONFIG_CHANGES="${CONFIG_CHANGES}• 新增定时任务\n"
    fi
    
    # 检查模型变更
    MODEL_CHANGE=$(git diff openclaw.json 2>/dev/null | grep -E '^\+.*"primary".*claude|gpt|gemini' | head -1)
    if [ -n "$MODEL_CHANGE" ]; then
        CONFIG_CHANGES="${CONFIG_CHANGES}• 调整模型配置\n"
    fi
    
    if [ -n "$CONFIG_CHANGES" ]; then
        CHANGE_NOTES="${CHANGE_NOTES}⚙️ 主配置变更:\n$CONFIG_CHANGES"
    else
        CHANGE_NOTES="${CHANGE_NOTES}⚙️ 主配置有调整\n"
    fi
fi

# 4. 检查 skill 文件变更
MODIFIED_SKILLS=$(echo "$CHANGES" | grep "skills/.*SKILL.md" | awk '{print $2}' | sed 's|skills/||' | sed 's|/SKILL.md||')
if [ -n "$MODIFIED_SKILLS" ]; then
    for skill in $MODIFIED_SKILLS; do
        CHANGE_NOTES="${CHANGE_NOTES}📝 更新 Skill: $skill\n"
    done
fi

# 5. 检查 agent 配置变更
MODIFIED_AGENTS=$(echo "$CHANGES" | grep -E "workspace-.*/(SOUL|AGENTS|USER).md" | awk '{print $2}' | sed 's|workspace-||' | sed 's|/.*||' | sort -u)
if [ -n "$MODIFIED_AGENTS" ]; then
    for agent in $MODIFIED_AGENTS; do
        CHANGE_NOTES="${CHANGE_NOTES}🔧 更新 Agent 配置: $agent\n"
    done
fi

# 6. 检查脚本变更
NEW_SCRIPTS=$(echo "$CHANGES" | grep "scripts/" | awk '{print $2}' | sed 's|scripts/||')
if [ -n "$NEW_SCRIPTS" ]; then
    CHANGE_NOTES="${CHANGE_NOTES}📜 脚本变更: $NEW_SCRIPTS\n"
fi

# 如果没有识别出具体变更，列出变更文件
if [ -z "$CHANGE_NOTES" ]; then
    FILES=$(echo "$CHANGES" | head -5 | awk '{print $2}' | sed 's|.*/||')
    CHANGE_NOTES="📂 文件变更:\n"
    for f in $FILES; do
        CHANGE_NOTES="${CHANGE_NOTES}  • $f\n"
    done
fi

# 提交并推送
git add .
git commit -m "auto backup: $DATE" --quiet
git push --quiet

# 生成消息
MSG="✅ OpenClaw 配置备份完成

📅 $DATE

$(echo -e "$CHANGE_NOTES")
🔗 https://github.com/zhangsan-tea/openclaw-bak"

# 发送消息
curl -s -X POST "https://api.telegram.org/bot8105171404:AAFef-9ixQJ6exQKlqj2P_INkFTW-JkVfO0/sendMessage" \
    -d chat_id="8051279955" \
    -d text="$MSG" > /dev/null 2>&1

# 记录日志
echo "$DATE: 已备份" >> "$LOG_FILE"