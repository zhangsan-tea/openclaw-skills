#!/bin/bash

# 药品管理系统 - 状态检查脚本
# 快速诊断系统问题

set -e

echo "🔍 药品管理系统状态检查"
echo "========================"
echo ""

WORKSPACE_DIR="/Users/lee/.openclaw/workspace-health-advisor"
CSV_FILE="$WORKSPACE_DIR/medications/medications.csv"
CONFIG_FILE="$WORKSPACE_DIR/medication_config.json"

# 检查项计数
TOTAL=0
PASSED=0

check_item() {
    TOTAL=$((TOTAL + 1))
    if [ $1 -eq 0 ]; then
        echo -e "✅ $2"
        PASSED=$((PASSED + 1))
    else
        echo -e "❌ $2"
    fi
}

# 1. 检查药品清单
echo "📋 检查药品清单..."
if [ -f "$CSV_FILE" ]; then
    MED_COUNT=$(tail -n +2 "$CSV_FILE" | wc -l | tr -d ' ')
    check_item 0 "药品清单文件存在 ($MED_COUNT 种药品)"
else
    check_item 1 "药品清单文件不存在"
fi

# 2. 检查配置文件
echo ""
echo "⚙️  检查配置文件..."
if [ -f "$CONFIG_FILE" ]; then
    check_item 0 "配置文件存在"
    
    # 检查 JSON 格式
    if python3 -c "import json; json.load(open('$CONFIG_FILE'))" 2>/dev/null; then
        check_item 0 "配置文件格式正确"
    else
        check_item 1 "配置文件格式错误"
    fi
else
    check_item 1 "配置文件不存在"
fi

# 3. 检查定时任务
echo ""
echo "⏰ 检查定时任务..."
JOB_COUNT=$(cron list 2>/dev/null | grep -c "药品检查" || echo "0")
if [ "$JOB_COUNT" -gt 0 ]; then
    check_item 0 "药品检查任务已配置 ($JOB_COUNT 个)"
    
    # 获取任务状态
    JOB_STATUS=$(cron list 2>/dev/null | grep "药品检查" | grep -o "enabled: true" || echo "")
    if [ -n "$JOB_STATUS" ]; then
        check_item 0 "任务已启用"
    else
        check_item 1 "任务未启用"
    fi
else
    check_item 1 "药品检查任务未配置"
fi

# 4. 检查 Google Drive 连接
echo ""
echo "🔗 检查 Google Drive 连接..."
if gog drive search "test" &>/dev/null; then
    check_item 0 "Google Drive 已连接"
    
    # 检查备份文件夹
    if gog drive search "medications_backup" &>/dev/null; then
        check_item 0 "备份文件夹存在"
    else
        check_item 1 "备份文件夹不存在"
    fi
else
    check_item 1 "Google Drive 未连接"
    echo "   解决：gog auth add YOUR_EMAIL@gmail.com"
fi

# 5. 检查 OpenClaw 状态
echo ""
echo "🦐 检查 OpenClaw 状态..."
if openclaw gateway status &>/dev/null; then
    check_item 0 "Gateway 运行正常"
else
    check_item 1 "Gateway 未运行"
    echo "   解决：openclaw gateway start"
fi

# 6. 检查照片目录
echo ""
echo "📸 检查照片目录..."
PHOTOS_DIR="$WORKSPACE_DIR/medications/photos"
if [ -d "$PHOTOS_DIR" ]; then
    PHOTO_COUNT=$(ls -1 "$PHOTOS_DIR" 2>/dev/null | wc -l | tr -d ' ')
    check_item 0 "照片目录存在 ($PHOTO_COUNT 张照片)"
else
    check_item 1 "照片目录不存在"
fi

# 7. 检查备份目录
echo ""
echo "💾 检查备份目录..."
BACKUP_DIR="$WORKSPACE_DIR/medications/backups"
if [ -d "$BACKUP_DIR" ]; then
    BACKUP_COUNT=$(ls -1 "$BACKUP_DIR" 2>/dev/null | wc -l | tr -d ' ')
    check_item 0 "备份目录存在 ($BACKUP_COUNT 个备份)"
else
    check_item 1 "备份目录不存在"
fi

# 8. 检查模型访问
echo ""
echo "🤖 检查模型访问..."
if command -v ollama &> /dev/null; then
    if ollama list &>/dev/null | grep -q "qwen3"; then
        check_item 0 "本地模型可用 (ollama/qwen3)"
    else
        check_item 1 "本地模型未安装"
    fi
else
    check_item 1 "Ollama 未安装"
fi

# 总结
echo ""
echo "========================"
echo "📊 检查结果：$PASSED/$TOTAL 通过"
echo "========================"

if [ "$PASSED" -eq "$TOTAL" ]; then
    echo -e "${GREEN}✅ 系统运行正常${NC}"
    exit 0
else
    echo -e "${YELLOW}⚠️  发现 $((TOTAL - PASSED)) 个问题${NC}"
    echo ""
    echo "💡 建议："
    
    if [ ! -f "$CSV_FILE" ]; then
        echo "  • 运行安装脚本：bash scripts/install.sh"
    fi
    
    if [ "$JOB_COUNT" -eq 0 ]; then
        echo "  • 创建定时任务：bash scripts/install.sh"
    fi
    
    if ! gog drive search "test" &>/dev/null; then
        echo "  • 授权 Google Drive：gog auth add YOUR_EMAIL@gmail.com"
    fi
    
    if ! openclaw gateway status &>/dev/null; then
        echo "  • 启动 Gateway：openclaw gateway start"
    fi
fi

echo ""
