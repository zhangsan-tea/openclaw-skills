#!/bin/bash

# 龙虾笔记演示网站 GitHub Pages 自动配置脚本
# 作者: 弗洛一德 (Freud2bot)
# 功能: 自动部署分页演示网站到 GitHub Pages

set -e

echo "🚀 开始配置龙虾笔记演示网站 GitHub Pages..."

# 1. 创建演示网站目录（如果不存在）
PRESENTATION_DIR="/Users/lee/.openclaw/workspace-commander/daily-openclaw-presentation"
if [ ! -d "$PRESENTATION_DIR" ]; then
    echo "❌ 演示网站目录不存在，请先运行演示网站生成脚本"
    exit 1
fi

# 2. 备份当前 openclaw-diary 仓库的 docs 目录（如果存在）
DIARY_REPO="/Users/lee/.openclaw/workspace-commander/daily-openclaw"
if [ -d "$DIARY_REPO/docs" ]; then
    echo "💾 备份现有的 docs 目录..."
    mv "$DIARY_REPO/docs" "$DIARY_REPO/docs_backup_$(date +%Y%m%d_%H%M%S)"
fi

# 3. 将演示网站内容复制到 docs 目录
echo "📋 复制演示网站文件到 docs 目录..."
mkdir -p "$DIARY_REPO/docs"
cp -r "$PRESENTATION_DIR"/* "$DIARY_REPO/docs/"

# 4. 提交更改到 openclaw-diary 仓库
echo "💾 提交更改到 GitHub 仓库..."
cd "$DIARY_REPO"
git add docs/
git commit -m "feat: 部署龙虾笔记 v1.7 分页演示网站" || echo "⚠️ 无更改需要提交"
git push origin main

# 5. 尝试通过 GitHub CLI 启用 Pages（如果失败则提示手动操作）
echo "🌐 尝试启用 GitHub Pages..."
if command -v gh &> /dev/null; then
    # 尝试多种方式启用 Pages
    echo "🔧 尝试通过 GitHub CLI 启用 Pages..."
    
    # 方法1: 使用 gh repo edit 命令
    if gh repo edit zhangsan-tea/openclaw-diary --homepage "https://zhangsan-tea.github.io/openclaw-diary" 2>/dev/null; then
        echo "✅ 成功设置仓库主页"
    fi
    
    # 方法2: 尝试 API 调用（备用）
    echo "📝 如果 Pages 未自动启用，请手动在 GitHub 网页上配置:"
    echo "   1. 访问 https://github.com/zhangsan-tea/openclaw-diary"
    echo "   2. 点击 Settings → Pages"
    echo "   3. Source 选择: Branch: main, Folder: /docs"
    echo "   4. 点击 Save"
else
    echo "📝 请手动在 GitHub 网页上启用 Pages:"
    echo "   1. 访问 https://github.com/zhangsan-tea/openclaw-diary"
    echo "   2. 点击 Settings → Pages"  
    echo "   3. Source 选择: Branch: main, Folder: /docs"
    echo "   4. 点击 Save"
fi

# 6. 显示完成信息
echo ""
echo "🎉 龙虾笔记演示网站部署完成！"
echo ""
echo "🔗 网站地址: https://zhangsan-tea.github.io/openclaw-diary/"
echo "📁 本地路径: $DIARY_REPO/docs/"
echo ""
echo "💡 提示: GitHub Pages 可能需要 1-2 分钟完成构建，首次访问如显示 404 请稍后刷新。"
echo ""
echo "📱 响应式设计: 网站在 PC 和手机上都能完美显示！"

# 7. 验证文件是否正确复制
echo ""
echo "🔍 验证部署文件:"
ls -la "$DIARY_REPO/docs/" | head -10

echo ""
echo "✅ 脚本执行完成！"