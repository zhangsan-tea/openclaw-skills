#!/bin/bash

# Token Optimizer Installation Script
# This script installs and configures the Token Optimizer skill

echo "=== 🦐 OpenClaw Token Optimizer 安装脚本 ==="
echo ""

# Check if OpenClaw is installed
if ! command -v openclaw &> /dev/null; then
    echo "❌ OpenClaw 未安装或不在 PATH 中。"
    exit 1
fi

# Get the script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Create logs directory if it doesn't exist
LOGS_DIR="$SCRIPT_DIR/logs"
mkdir -p "$LOGS_DIR"

echo "✅ 日志目录已创建: $LOGS_DIR"

# Make scripts executable
chmod +x "$SCRIPT_DIR/scripts"/*.sh
chmod +x "$SCRIPT_DIR/scripts"/*.py

echo "✅ 脚本权限已设置"

# Ask user if they want to install the automated cron job
read -p "是否安装自动化清理定时任务？(每天凌晨 2:00 执行) [Y/n]: " install_cron
if [[ ! $install_cron =~ ^[Nn]$ ]]; then
    # Install the cron job
    cron add --job "$SCRIPT_DIR/token-optimizer-cron.json"
    
    if [ $? -eq 0 ]; then
        echo "✅ 自动化清理任务已安装！"
    else
        echo "⚠️  自动化清理任务安装失败，请手动运行："
        echo "   cron add --job $SCRIPT_DIR/token-optimizer-cron.json"
    fi
else
    echo "ℹ️  跳过自动化任务安装。您可以稍后手动安装。"
fi

echo ""
echo "=== 安装完成！ ==="
echo ""
echo "使用方法："
echo "1. L2 交互式工具: $SCRIPT_DIR/scripts/improved_interactive_token_optimizer.sh"
echo "2. L3 自动化工具: 已配置为每天凌晨 2:00 自动运行"
echo "3. 手动运行 L3: python3 $SCRIPT_DIR/scripts/automated_token_optimizer.py"
echo ""
echo "文档: $SCRIPT_DIR/SKILL.md"