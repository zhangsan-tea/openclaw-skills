#!/bin/bash

# Token Optimizer - L2 Interactive Version
# This script provides interactive tools to help users manage their OpenClaw token consumption.

echo "=== 🦐 OpenClaw Token 优化助手 (L2 交互版) ==="
echo ""

# Function to generate task context summary
generate_task_summary() {
    echo "正在为您生成当前任务的上下文摘要..."
    # Placeholder for actual AI call to generate summary
    echo "【模拟摘要】这是一个由 AI 生成的任务摘要，包含了关键结论和下一步计划。" > TASK_CONTEXT_临时.md
    echo "✅ 摘要已保存为 'TASK_CONTEXT_临时.md'。您现在可以安全地使用 /new 命令了。"
}

# Function to scan and suggest cleanup
scan_workspace() {
    echo "正在扫描所有助手的工作区..."
    WORKSPACES="/Users/lee/.openclaw/workspace-*"
    FOUND_ISSUES=0

    for ws in $WORKSPACES; do
        if [ -d "$ws" ]; then
            AGENT_NAME=$(basename "$ws" | cut -d'-' -f2-)
            echo ""
            echo "--- 助手: $AGENT_NAME ---"
            
            # Check for non-core .md files in root
            NON_CORE_FILES=$(find "$ws" -maxdepth 1 -name "*.md" -not -name "SOUL.md" -not -name "IDENTITY.md" -not -name "USER.md" -not -name "MEMORY.md" -not -name "AGENTS.md" -not -name "TOOLS.md" -not -name "HEARTBEAT.md" -not -name "BOOTSTRAP.md")
            if [ -n "$NON_CORE_FILES" ]; then
                echo "⚠️  发现非核心文件，可能增加启动消耗:"
                echo "$NON_CORE_FILES" | sed 's/^/    /'
                FOUND_ISSUES=$((FOUND_ISSUES+1))
            else
                echo "✅ 根目录干净。"
            fi
        fi
    done

    if [ $FOUND_ISSUES -eq 0 ]; then
        echo ""
        echo "🎉 所有助手的工作区都很干净！"
    else
        echo ""
        echo "💡 建议：将上述非核心文件移入该助手目录下的 'archive/' 文件夹中。"
    fi
}

# Main menu
while true; do
    echo ""
    echo "请选择您要执行的操作:"
    echo "1) 生成当前任务摘要 (用于 /new 前)"
    echo "2) 扫描工作区并提供建议"
    echo "3) 退出"
    read -p "请输入选项 (1-3): " choice

    case $choice in
        1)
            generate_task_summary
            ;;
        2)
            scan_workspace
            ;;
        3)
            echo "再见！"
            exit 0
            ;;
        *)
            echo "无效选项，请重试。"
            ;;
    esac
done
