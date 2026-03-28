#!/bin/bash
# OpenClaw 配置自动备份脚本
# 每天 3:00 执行，带人性化变更说明

cd /Users/lee/.openclaw

DATE=$(date '+%Y-%m-%d %H:%M')
LOG_FILE="/Users/lee/.openclaw/logs/backup.log"
BOT_TOKEN="8536197347:AAEgILrmXFbPe7YCc-aNjxbzhsxWbcWpx_w"
CHAT_ID="8051279955"

# 检查是否有更改
CHANGES=$(git status --porcelain)

if [ -z "$CHANGES" ]; then
    MSG="ℹ️ OpenClaw 配置无变更 ($DATE)"
    curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
        -d chat_id="$CHAT_ID" \
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

# 2. 检查新增的 agent workspace
NEW_AGENTS=$(echo "$CHANGES" | grep "^?? workspace-" | awk '{print $2}' | sed 's|workspace-||' | sed 's|/.*||')
if [ -n "$NEW_AGENTS" ]; then
    for agent in $NEW_AGENTS; do
        CHANGE_NOTES="${CHANGE_NOTES}🤖 新增 Agent: $agent\n"
    done
fi

# 3. 检查 openclaw.json 主配置变更
if echo "$CHANGES" | grep -q "openclaw.json"; then
    CONFIG_CHANGES=""
    
    # 检查新增 telegram 账户
    if git diff openclaw.json 2>/dev/null | grep -qE '^\+.*"accounts".*\{'; then
        CONFIG_CHANGES="${CONFIG_CHANGES}• 新增 Bot 账户\n"
    fi
    
    # 检查新增 cron 任务
    if git diff openclaw.json 2>/dev/null | grep -qE '^\+.*"cron"'; then
        CONFIG_CHANGES="${CONFIG_CHANGES}• 新增定时任务\n"
    fi
    
    # 检查模型变更
    if git diff openclaw.json 2>/dev/null | grep -qE '^\+.*"primary".*claude|gpt|gemini'; then
        CONFIG_CHANGES="${CONFIG_CHANGES}• 调整模型配置\n"
    fi
    
    # 检查路由绑定变更
    if git diff openclaw.json 2>/dev/null | grep -qE '^\+.*"bindings"'; then
        CONFIG_CHANGES="${CONFIG_CHANGES}• 新增路由绑定\n"
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

# 5. 检查 agent 配置变更 (SOUL.md, AGENTS.md, USER.md)
MODIFIED_AGENTS=$(echo "$CHANGES" | grep -E "workspace-.*/(SOUL|AGENTS|USER).md" | awk '{print $2}' | sed 's|workspace-||' | sed 's|/.*||' | sort -u)
if [ -n "$MODIFIED_AGENTS" ]; then
    for agent in $MODIFIED_AGENTS; do
        CHANGE_NOTES="${CHANGE_NOTES}🔧 更新 Agent 配置: $agent\n"
    done
fi

# 6. 检查脚本变更
SCRIPT_CHANGES=$(echo "$CHANGES" | grep "scripts/" | awk '{print $2}' | sed 's|scripts/||')
if [ -n "$SCRIPT_CHANGES" ]; then
    CHANGE_NOTES="${CHANGE_NOTES}📜 脚本变更: $SCRIPT_CHANGES\n"
fi

# 7. 检查 memory 文件变更（健康档案等）
MEMORY_CHANGES=$(echo "$CHANGES" | grep "memory/.*\.md" | awk '{print $2}' | sed 's|.*/||' | head -3)
if [ -n "$MEMORY_CHANGES" ]; then
    CHANGE_NOTES="${CHANGE_NOTES}🧠 记忆文件更新\n"
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
curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
    -d chat_id="$CHAT_ID" \
    -d text="$MSG" > /dev/null 2>&1

# 记录日志
echo "$DATE: 已备份" >> "$LOG_FILE"