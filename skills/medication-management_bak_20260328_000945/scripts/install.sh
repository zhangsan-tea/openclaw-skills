#!/bin/bash

# 药品管理系统 - 一键安装脚本
# 专为小白用户设计，自动化完成所有配置

set -e

echo "🚀 药品管理系统安装脚本"
echo "========================"
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查 OpenClaw 是否安装
echo "📋 检查前置条件..."
if ! command -v openclaw &> /dev/null; then
    echo -e "${RED}❌ OpenClaw 未安装${NC}"
    echo "请先安装 OpenClaw: https://docs.openclaw.ai"
    exit 1
fi
echo -e "${GREEN}✅ OpenClaw 已安装${NC}"

# 检查工作目录
WORKSPACE_DIR="/Users/lee/.openclaw/workspace-health-advisor"
if [ ! -d "$WORKSPACE_DIR" ]; then
    echo -e "${YELLOW}⚠️  创建工作目录${NC}"
    mkdir -p "$WORKSPACE_DIR/medications/photos"
    mkdir -p "$WORKSPACE_DIR/memory/medication_reports"
fi

# 创建药品清单 CSV
echo ""
echo "📝 创建药品清单..."
CSV_FILE="$WORKSPACE_DIR/medications/medications.csv"
if [ ! -f "$CSV_FILE" ]; then
    cat > "$CSV_FILE" << 'EOF'
药品 ID，药品名称，功效，保质期，生产批号，存放位置，分区，录入时间，照片路径，状态
EOF
    echo -e "${GREEN}✅ 药品清单已创建${NC}"
else
    echo -e "${YELLOW}⚠️  药品清单已存在${NC}"
fi

# 创建配置文件
echo ""
echo "⚙️  创建配置文件..."
CONFIG_FILE="$WORKSPACE_DIR/medication_config.json"
if [ ! -f "$CONFIG_FILE" ]; then
    cat > "$CONFIG_FILE" << 'EOF'
{
  "reminder_settings": {
    "check_frequency": "weekly",
    "check_day": "sunday",
    "check_time": "09:00",
    "advance_days": [7, 0],
    "enabled": true
  },
  "storage": {
    "csv_path": "medications/medications.csv",
    "backup_enabled": true,
    "backup_frequency": "daily",
    "photos_dir": "medications/photos"
  },
  "models": {
    "primary": "coding-plan/glm-5",
    "fallback": [
      "ollama/qwen3:8b",
      "coding-plan/qwen3-max-2026-01-23"
    ],
    "timeout_seconds": 60,
    "max_retries": 3
  },
  "notifications": {
    "channel": "telegram",
    "enable_buttons": true,
    "reminder_interval_hours": 24
  }
}
EOF
    echo -e "${GREEN}✅ 配置文件已创建${NC}"
else
    echo -e "${YELLOW}⚠️  配置文件已存在${NC}"
fi

# 创建定时任务
echo ""
echo "⏰ 创建定时任务..."

# 检查是否已存在药品检查任务
EXISTING_JOB=$(cron list 2>/dev/null | grep -c "药品检查" || true)

if [ "$EXISTING_JOB" -eq 0 ]; then
    # 获取用户 Telegram ID（从环境变量或配置）
    USER_ID="${TELEGRAM_USER_ID:-8051279955}"
    
    # 创建 cron job
    cat > /tmp/medication_cron.json << EOF
{
  "name": "健康顾问 - 每周药品检查",
  "schedule": {
    "kind": "cron",
    "expr": "0 9 * * 0",
    "tz": "Asia/Shanghai"
  },
  "payload": {
    "kind": "agentTurn",
    "message": "你是健康顾问。请执行每周家庭药品检查：\n\n1. 读取 medications/medications.csv\n2. 检查已过期的药品（保质期 < 今天）\n3. 检查未来 7 天内到期的药品\n4. 发送完整检查报告，并带上确认按钮\n\n格式：\n💊 每周药品检查报告\n\n【已过期的药品】\n[列表]\n\n【未来 7 天内到期】\n[列表]\n\n👇 请确认过期药品处理情况",
    "model": "coding-plan/glm-5"
  },
  "sessionTarget": "isolated",
  "delivery": {
    "mode": "announce",
    "channel": "telegram",
    "to": "$USER_ID"
  }
}
EOF
    
    # 添加 cron job
    if cron add --job /tmp/medication_cron.json 2>/dev/null; then
        echo -e "${GREEN}✅ 定时任务已创建${NC}"
    else
        echo -e "${YELLOW}⚠️  定时任务可能已存在${NC}"
    fi
    
    rm -f /tmp/medication_cron.json
else
    echo -e "${YELLOW}⚠️  定时任务已存在${NC}"
fi

# 测试 Google Drive 连接
echo ""
echo "🔗 测试 Google Drive 连接..."
if gog drive search "test" &>/dev/null; then
    echo -e "${GREEN}✅ Google Drive 已连接${NC}"
else
    echo -e "${YELLOW}⚠️  Google Drive 未连接${NC}"
    echo ""
    echo "请运行以下命令授权："
    echo "  gog auth add YOUR_EMAIL@gmail.com"
    echo ""
    echo "然后打开链接完成授权"
fi

# 创建备份脚本
echo ""
echo "💾 创建备份脚本..."
BACKUP_SCRIPT="$WORKSPACE_DIR/medications/scripts/backup.sh"
mkdir -p "$(dirname "$BACKUP_SCRIPT")"
cat > "$BACKUP_SCRIPT" << 'EOF'
#!/bin/bash
# 药品数据备份脚本
DATE=$(date +%Y%m%d)
CSV_FILE="/Users/lee/.openclaw/workspace-health-advisor/medications/medications.csv"
BACKUP_DIR="/Users/lee/.openclaw/workspace-health-advisor/medications/backups"

mkdir -p "$BACKUP_DIR"
cp "$CSV_FILE" "$BACKUP_DIR/medications_backup_$DATE.csv"
echo "✅ 备份完成：medications_backup_$DATE.csv"
EOF
chmod +x "$BACKUP_SCRIPT"
echo -e "${GREEN}✅ 备份脚本已创建${NC}"

# 显示完成信息
echo ""
echo "========================"
echo -e "${GREEN}🎉 安装完成！${NC}"
echo "========================"
echo ""
echo "📋 下一步："
echo "  1. 如果 Google Drive 未连接，请运行：gog auth add YOUR_EMAIL@gmail.com"
echo "  2. 录入药品：添加药品 - 药品名，保质期 YYYY-MM-DD"
echo "  3. 等待每周日 09:00 自动检查"
echo ""
echo "📁 重要文件位置："
echo "  药品清单：$WORKSPACE_DIR/medications/medications.csv"
echo "  配置文件：$WORKSPACE_DIR/medication_config.json"
echo "  使用指南：$WORKSPACE_DIR/../skills/medication-management/docs/INSTALL_GUIDE.md"
echo ""
echo "💡 常用命令："
echo "  查看药品清单：cat $WORKSPACE_DIR/medications/medications.csv"
echo "  手动执行检查：cron run --job-id <JOB_ID>"
echo "  查看系统状态：bash scripts/check_status.sh"
echo ""
