#!/bin/bash

# Weekly Cross-Domain Analysis Script
# 弗洛一德总指挥 - 每周跨域分析自动化脚本

DATE=$(date +%Y-%m-%d)
WEEK_START=$(date -v-monday +%Y-%m-%d)
WEEK_END=$(date -v-sunday +%Y-%m-%d)

echo "Starting weekly cross-domain analysis for week $WEEK_START to $WEEK_END"

# 创建分析报告目录
mkdir -p /Users/lee/.openclaw/workspace-commander/memory/weekly-analysis

# 收集各领域数据
echo "Collecting data from all assistants..."

# 数字幕僚 - 工作数据
DIGITAL_DATA=""
if [ -f "/Users/lee/.openclaw/workspace-digital-secretary/memory/todo_list_$(date +%Y%m%d).md" ]; then
    DIGITAL_DATA=$(cat "/Users/lee/.openclaw/workspace-digital-secretary/memory/todo_list_$(date +%Y%m%d).md")
fi

# 健康顾问 - 健康数据  
HEALTH_DATA=""
for file in /Users/lee/.openclaw/workspace-health-advisor/memory/2026-03-*.md; do
    if [[ -f "$file" ]]; then
        HEALTH_DATA="$HEALTH_DATA$(cat "$file")"
    fi
done

# 觉醒教练 - 心理数据
COACH_DATA=""
for file in /Users/lee/.openclaw/workspace-awakening-coach/memory/2026-03-*.md; do
    if [[ -f "$file" ]]; then
        COACH_DATA="$COACH_DATA$(cat "$file")"
    fi
done

# 弗洛一德 - 系统数据
COMMANDER_DATA=""
for file in /Users/lee/.openclaw/workspace-commander/memory/2026-03-*.md; do
    if [[ -f "$file" ]]; then
        COMMANDER_DATA="$COMMANDER_DATA$(cat "$file")"
    fi
done

# 生成综合分析报告
cat > "/Users/lee/.openclaw/workspace-commander/memory/weekly-analysis/weekly-analysis-$DATE.md" << EOF
# 周度跨域分析报告 - $DATE

> 弗洛一德总指挥综合分析

## 分析周期
- **开始日期**: $WEEK_START
- **结束日期**: $WEEK_END

## 数据来源
- **工作维度**: 数字幕僚记忆文件
- **健康维度**: 健康顾问记忆文件  
- **心理维度**: 觉醒教练记忆文件
- **系统维度**: 弗洛一德记忆文件

## 跨域关联分析

### 1. 工作-健康关联
\`\`\`
$DIGITAL_DATA
$HEALTH_DATA
\`\`\`

### 2. 心理-行为模式
\`\`\`
$COACH_DATA
$COMMANDER_DATA
\`\`\`

### 3. 系统-个人协同
\`\`\`
$COMMANDER_DATA
\`\`\`

## 关键洞察与建议

### 🔴 风险预警
- [待填充]

### 🟡 机会识别  
- [待填充]

### 🟢 优化建议
- [待填充]

## 下周重点关注
- [待填充]

---
*本报告由弗洛一德自动化系统生成，基于多 Agent 记忆数据综合分析*
EOF

echo "Weekly analysis report generated: weekly-analysis-$DATE.md"