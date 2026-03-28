#!/bin/bash
# OpenClaw 配置自动备份脚本
# 每天 3:00 执行，小白用户也能看懂的变更说明

cd /Users/lee/.openclaw

DATE=$(date '+%Y-%m-%d %H:%M')
LOG_FILE="/Users/lee/.openclaw/logs/backup.log"
BOT_TOKEN="8536197347:AAEgILrmXFbPe7YCc-aNjxbzhsxWbcWpx_w"
CHAT_ID="8051279955"

# 检查是否有更改
CHANGES=$(git status --porcelain)

if [ -z "$CHANGES" ]; then
    MSG="ℹ️ 今天没有配置变更，系统运行正常"
    curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
        -d chat_id="$CHAT_ID" \
        -d text="$MSG" > /dev/null 2>&1
    exit 0
fi

# 分析变更内容
CHANGE_NOTES=""

# 1. 检查新增的 skill - 读取它的功能描述
NEW_SKILLS=$(echo "$CHANGES" | grep "^?? skills/" | awk '{print $2}' | sed 's|skills/||' | sed 's|/.*||')
if [ -n "$NEW_SKILLS" ]; then
    for skill in $NEW_SKILLS; do
        SKILL_FILE="/Users/lee/.openclaw/skills/$skill/SKILL.md"
        if [ -f "$SKILL_FILE" ]; then
            DESC=$(grep "^description:" "$SKILL_FILE" 2>/dev/null | head -1 | sed 's/description: //' | cut -c1-50)
            if [ -z "$DESC" ]; then
                DESC="新增技能模块"
            fi
            CHANGE_NOTES="${CHANGE_NOTES}📦 新增功能【$skill】\n   $DESC\n\n"
        fi
    done
fi

# 2. 检查新增的 agent - 读取它的角色说明
NEW_AGENTS=$(echo "$CHANGES" | grep "^?? workspace-" | awk '{print $2}' | sed 's|workspace-||' | sed 's|/.*||')
if [ -n "$NEW_AGENTS" ]; then
    for agent in $NEW_AGENTS; do
        SOUL_FILE="/Users/lee/.openclaw/workspace-$agent/SOUL.md"
        if [ -f "$SOUL_FILE" ]; then
            # 提取角色说明（通常是 "你是 xxx" 或第一段）
            ROLE=$(grep -E "^你是|^你叫|角色|职责" "$SOUL_FILE" 2>/dev/null | head -1 | sed 's/^# //' | cut -c1-40)
            if [ -z "$ROLE" ]; then
                ROLE="新的智能助手"
            fi
            CHANGE_NOTES="${CHANGE_NOTES}🤖 新增助手【$agent】\n   $ROLE\n\n"
        fi
    done
fi

# 3. 检查主配置变更 - 解析具体改了什么
if echo "$CHANGES" | grep -q " M openclaw.json\|^M  openclaw.json"; then
    CONFIG_NOTES=""
    
    # 检查新增 Bot 账户 - 提取名称
    NEW_BOTS=$(git diff openclaw.json 2>/dev/null | grep -A2 '^\+.*"accounts"' | grep '"name"' | sed 's/.*"name": "//' | sed 's/".*//' | head -3)
    if [ -n "$NEW_BOTS" ]; then
        for bot in $NEW_BOTS; do
            CONFIG_NOTES="${CONFIG_NOTES}• 新增 Telegram 机器人【$bot】\n"
        done
    fi
    
    # 检查新增定时任务 - 提取任务名
    NEW_CRONS=$(git diff openclaw.json 2>/dev/null | grep '^\+.*"name"' | grep -v "accounts\|agents" | sed 's/.*"name": "//' | sed 's/".*//' | head -3)
    if [ -n "$NEW_CRONS" ]; then
        for cron in $NEW_CRONS; do
            CONFIG_NOTES="${CONFIG_NOTES}• 新增定时任务【$cron】\n"
        done
    fi
    
    # 检查模型变更
    if git diff openclaw.json 2>/dev/null | grep -qE '^\+.*"primary"'; then
        NEW_MODEL=$(git diff openclaw.json 2>/dev/null | grep '^\+.*"primary"' | head -1 | sed 's/.*"primary": "//' | sed 's/".*//')
        if [ -n "$NEW_MODEL" ]; then
            # 简化模型名
            SIMPLE_NAME=$(echo "$NEW_MODEL" | sed 's|.*/||' | sed 's/anthropic/Claude/' | sed 's/openai/GPT/')
            CONFIG_NOTES="${CONFIG_NOTES}• 默认模型改为【$SIMPLE_NAME】\n"
        fi
    fi
    
    # 检查路由绑定 - 新增助手绑定
    if git diff openclaw.json 2>/dev/null | grep -qE '^\+.*"agentId"'; then
        NEW_BINDINGS=$(git diff openclaw.json 2>/dev/null | grep '^\+.*"agentId"' | sed 's/.*"agentId": "//' | sed 's/".*//' | head -3)
        for b in $NEW_BINDINGS; do
            CONFIG_NOTES="${CONFIG_NOTES}• 新助手【$b】已接入 Telegram\n"
        done
    fi
    
    if [ -n "$CONFIG_NOTES" ]; then
        CHANGE_NOTES="${CHANGE_NOTES}⚙️ 系统配置更新\n$CONFIG_NOTES\n"
    fi
fi

# 4. 检查 skill 更新
MODIFIED_SKILLS=$(echo "$CHANGES" | grep " M skills/.*SKILL.md\|^M  skills/.*SKILL.md" | awk '{print $2}' | sed 's|skills/||' | sed 's|/SKILL.md||')
if [ -n "$MODIFIED_SKILLS" ]; then
    for skill in $MODIFIED_SKILLS; do
        CHANGE_NOTES="${CHANGE_NOTES}📝 更新功能【$skill】\n"
    done
    CHANGE_NOTES="${CHANGE_NOTES}\n"
fi

# 5. 检查 Agent 配置更新
MODIFIED_SOULS=$(echo "$CHANGES" | grep "workspace-.*/SOUL.md" | awk '{print $2}' | sed 's|workspace-||' | sed 's|/SOUL.md||')
if [ -n "$MODIFIED_SOULS" ]; then
    for agent in $MODIFIED_SOULS; do
        CHANGE_NOTES="${CHANGE_NOTES}🔧 调整助手【$agent】的角色设定\n"
    done
    CHANGE_NOTES="${CHANGE_NOTES}\n"
fi

# 6. 检查脚本变更
SCRIPT_CHANGES=$(echo "$CHANGES" | grep "scripts/" | awk '{print $2}' | sed 's|scripts/||')
if [ -n "$SCRIPT_CHANGES" ]; then
    for script in $SCRIPT_CHANGES; do
        if [[ "$script" == *"backup"* ]]; then
            CHANGE_NOTES="${CHANGE_NOTES}📜 更新自动备份脚本\n"
        else
            CHANGE_NOTES="${CHANGE_NOTES}📜 更新脚本【$script】\n"
        fi
    done
    CHANGE_NOTES="${CHANGE_NOTES}\n"
fi

# 如果没有识别出具体变更，用简单的话说明
if [ -z "$CHANGE_NOTES" ]; then
    CHANGE_NOTES="📂 系统文件有更新（配置或日志）\n"
fi

# 提交并推送
git add .
git commit -m "auto backup: $DATE" --quiet
git push --quiet

# 生成消息
MSG="✅ OpenClaw 配置已自动备份

📅 $DATE

$(echo -e "$CHANGE_NOTES")
🔗 点击查看详情：
https://github.com/zhangsan-tea/openclaw-bak"

# 发送消息
curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
    -d chat_id="$CHAT_ID" \
    -d text="$MSG" > /dev/null 2>&1

# 记录日志
echo "$DATE: 已备份" >> "$LOG_FILE"