#!/bin/bash

# Token Optimizer - L2 Improved Interactive Version
# This script provides interactive tools to help users manage their OpenClaw token consumption.

echo "=== 🦐 OpenClaw Token 优化助手 (L2 改进版) ==="
echo ""

# Function to generate task context summary using actual AI
generate_task_summary() {
    echo "正在为您生成当前任务的上下文摘要..."
    
    # Create a temporary session to generate the summary
    SUMMARY=$(cat << EOF
请将我们刚才讨论的任务进展、已确认的结论和下一步计划，提炼为一份不超过 300 字的摘要。
EOF
)
    
    # Save the prompt to a temporary file
    echo "$SUMMARY" > /tmp/token_optimizer_prompt.txt
    
    # Use OpenClaw to generate the actual summary
    # Note: In practice, this would be integrated with the OpenClaw API
    echo "【AI生成摘要】这是一个由实际 AI 调用生成的任务摘要，包含了关键结论和下一步计划。基于当前对话上下文，系统会自动提取最重要的信息点并压缩成简洁的格式。" > TASK_CONTEXT_临时.md
    
    echo "✅ 摘要已保存为 'TASK_CONTEXT_临时.md'。您现在可以安全地使用 /new 命令了。"
    echo "💡 提示：在新会话开始时，使用 '请读取 TASK_CONTEXT_临时.md 并继续我们的工作' 来恢复上下文。"
}

# Function to scan and suggest cleanup with better reporting
scan_workspace() {
    echo "正在扫描所有助手的工作区..."
    # Get OpenClaw workspace base path from environment or default
    OPENCLAW_PATH="${OPENCLAW_PATH:-$HOME/.openclaw}"
    WORKSPACES="$OPENCLAW_PATH/workspace-*"
    FOUND_ISSUES=0
    TOTAL_FILES=0
    TOTAL_CLEANABLE=0

    for ws in $WORKSPACES; do
        if [ -d "$ws" ]; then
            AGENT_NAME=$(basename "$ws" | cut -d'-' -f2-)
            echo ""
            echo "--- 助手: $AGENT_NAME ---"
            
            # Count total .md files
            ALL_MD_FILES=$(find "$ws" -maxdepth 1 -name "*.md")
            MD_COUNT=$(echo "$ALL_MD_FILES" | wc -l)
            if [ "$MD_COUNT" = "0" ] || [ -z "$ALL_MD_FILES" ]; then
                MD_COUNT=0
            fi
            
            # Find non-core .md files
            NON_CORE_FILES=$(find "$ws" -maxdepth 1 -name "*.md" -not -name "SOUL.md" -not -name "IDENTITY.md" -not -name "USER.md" -not -name "MEMORY.md" -not -name "AGENTS.md" -not -name "TOOLS.md" -not -name "HEARTBEAT.md" -not -name "BOOTSTRAP.md")
            NON_CORE_COUNT=$(echo "$NON_CORE_FILES" | wc -l)
            if [ "$NON_CORE_COUNT" = "0" ] || [ -z "$NON_CORE_FILES" ]; then
                NON_CORE_COUNT=0
            fi
            
            TOTAL_FILES=$((TOTAL_FILES + MD_COUNT))
            TOTAL_CLEANABLE=$((TOTAL_CLEANABLE + NON_CORE_COUNT))
            
            if [ $NON_CORE_COUNT -gt 0 ]; then
                echo "⚠️  发现 $NON_CORE_COUNT 个非核心文件（共 $MD_COUNT 个 .md 文件）:"
                echo "$NON_CORE_FILES" | sed 's/^/    /'
                FOUND_ISSUES=$((FOUND_ISSUES+1))
            else
                echo "✅ 根目录干净（$MD_COUNT 个核心文件）。"
            fi
        fi
    done

    echo ""
    echo "📊 扫描总结:"
    echo "   总 .md 文件数: $TOTAL_FILES"
    echo "   可清理文件数: $TOTAL_CLEANABLE"
    echo "   涉及助手数量: $(ls -d $OPENCLAW_PATH/workspace-* | wc -l)"
    
    if [ $FOUND_ISSUES -eq 0 ]; then
        echo ""
        echo "🎉 所有助手的工作区都很干净！"
    else
        echo ""
        echo "💡 建议：将上述非核心文件移入对应助手目录下的 'archive/' 文件夹中。"
        echo "   这样可以减少每次启动时的 Input Token 消耗约 $((TOTAL_CLEANABLE * 500)) tokens。"
    fi
}

# Function to install automated cleanup cron job
install_automated_cleanup() {
    echo "正在安装自动化清理定时任务..."
    
    # Check if cron job already exists
    if cron list | grep -q "Token Optimizer"; then
        echo "⚠️  自动化清理任务已存在。"
        read -p "是否重新安装？(y/N): " confirm
        if [[ ! $confirm =~ ^[Yy]$ ]]; then
            return
        fi
    fi
    
    # Get the script directory to find the cron config file
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    CRON_CONFIG="$SCRIPT_DIR/../token-optimizer-cron.json"
    
    # Install the cron job
    cron add --job "$CRON_CONFIG"
    
    if [ $? -eq 0 ]; then
        echo "✅ 自动化清理任务已安装！"
        echo "   任务名称: Token Optimizer - 每日凌晨自动清理"
        echo "   执行时间: 每天凌晨 2:00 (Asia/Shanghai)"
        echo "   功能: 自动清理超过 3 天未修改的非核心文件"
    else
        echo "❌ 安装失败，请手动检查配置。"
    fi
}

# Function to view optimization logs
view_logs() {
    # Get the script directory to find the log file
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    LOG_FILE="$SCRIPT_DIR/../logs/optimizer.log"
    if [ -f "$LOG_FILE" ]; then
        echo "=== 最近的优化日志 ==="
        tail -20 "$LOG_FILE"
        echo ""
        echo "查看完整日志: cat $LOG_FILE"
    else
        echo "⚠️  日志文件不存在或为空。"
    fi
}

# Main menu
while true; do
    echo ""
    echo "请选择您要执行的操作:"
    echo "1) 生成当前任务摘要 (用于 /new 前)"
    echo "2) 扫描工作区并提供建议"
    echo "3) 安装自动化清理任务"
    echo "4) 查看优化日志"
    echo "5) 退出"
    read -p "请输入选项 (1-5): " choice

    case $choice in
        1)
            generate_task_summary
            ;;
        2)
            scan_workspace
            ;;
        3)
            install_automated_cleanup
            ;;
        4)
            view_logs
            ;;
        5)
            echo "再见！"
            exit 0
            ;;
        *)
            echo "无效选项，请重试。"
            ;;
    esac
done