#!/bin/bash

# 健康管理系列一键安装脚本
# 使用方法：curl -sSL https://raw.githubusercontent.com/zhangsan-tea/openclaw-skills/main/install-health.sh | bash

set -e

echo "════════════════════════════════════════════════════════"
echo "       个人健康管理系统 - 安装向导"
echo "════════════════════════════════════════════════════════"
echo ""

# 检查 OpenClaw 是否安装
if [ ! -d "$HOME/.openclaw" ]; then
    echo "❌ 未检测到 OpenClaw，请先安装 OpenClaw"
    echo "   安装方法：brew install openclaw"
    exit 1
fi

# 创建 skills 目录
SKILLS_DIR="$HOME/.openclaw/skills"
mkdir -p "$SKILLS_DIR"

echo "📁 Skills 目录：$SKILLS_DIR"
echo ""

# 显示模块选项
echo "请选择要安装的模块（可多选，用空格分隔）："
echo ""
echo "  1) 健康顾问理念    - 方法论与思维框架（推荐所有人）"
echo "  2) 药品管理        - 药品清单、过期检查（有家庭药箱）"
echo "  3) 日程提醒        - 截图→日历提醒（推荐所有人）"
echo "  4) 健康数据自动化  - Apple Health 导出（需 iPhone+Watch）"
echo "  a) 全部安装"
echo "  q) 取消"
echo ""

read -p "请输入选择 [1-4/a/q]: " choice

# 临时下载目录
TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

echo ""
echo "⬇️  正在下载..."

# 克隆仓库
git clone --depth 1 https://github.com/zhangsan-tea/openclaw-skills.git "$TEMP_DIR/repo" 2>/dev/null

install_skill() {
    local skill=$1
    if [ -d "$TEMP_DIR/repo/$skill" ]; then
        cp -r "$TEMP_DIR/repo/$skill" "$SKILLS_DIR/"
        echo "  ✅ $skill 已安装"
    else
        echo "  ⚠️  $skill 不存在"
    fi
}

case $choice in
    a|A)
        echo ""
        echo "📦 安装全部模块..."
        install_skill "health-advisor-skill-extraction"
        install_skill "medication-management"
        install_skill "calendar-reminder"
        install_skill "health-automation"
        ;;
    q|Q)
        echo "已取消"
        exit 0
        ;;
    *)
        echo ""
        echo "📦 安装选中的模块..."
        for i in $choice; do
            case $i in
                1) install_skill "health-advisor-skill-extraction" ;;
                2) install_skill "medication-management" ;;
                3) install_skill "calendar-reminder" ;;
                4) install_skill "health-automation" ;;
                *) echo "  ⚠️  无效选项: $i" ;;
            esac
        done
        ;;
esac

echo ""
echo "════════════════════════════════════════════════════════"
echo "✅ 安装完成！"
echo "════════════════════════════════════════════════════════"
echo ""
echo "📖 使用方法："
echo ""
echo "  • 日程提醒：发送截图或描述，自动创建日历提醒"
echo "  • 药品管理：说「检查过期药品」或「添加药品」"
echo "  • 健康咨询：问任何健康问题"
echo ""
echo "📚 详细文档："
echo "  https://github.com/zhangsan-tea/openclaw-skills"
echo ""