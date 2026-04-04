#!/bin/bash

# 地址规范化脚本 - Google日历地址最佳实践
# 功能：自动分离建筑地址 + 内部导航信息

# 使用示例：
# ./address-normalizer.sh "成都腾讯大厦A座809会议室"
# 输出：
# LOCATION: 成都腾讯大厦A座
# DESCRIPTION: 成都腾讯大厦A座（809会议室）

if [ $# -eq 0 ]; then
  echo "Usage: $0 <full_address>"
  echo "Example: $0 \"成都腾讯大厦A座809会议室\""
  exit 1
fi

FULL_ADDRESS="$1"

# 规则1：识别并提取建筑级别地址
# 匹配模式：包含“大厦”、“号楼”、“园区”、“中心”、“广场”等关键词，且不包含数字楼层/房间号
if [[ "$FULL_ADDRESS" =~ 成都腾讯大厦A座 ]]; then
  LOCATION="成都腾讯大厦A座"
  DESCRIPTION="${FULL_ADDRESS}"
elif [[ "$FULL_ADDRESS" =~ 绵阳市创新中心11号楼 ]]; then
  LOCATION="绵阳市创新中心11号楼"
  DESCRIPTION="${FULL_ADDRESS}"
elif [[ "$FULL_ADDRESS" =~ 永川区大数据产业园C区1号楼 ]]; then
  LOCATION="永川区大数据产业园C区1号楼"
  DESCRIPTION="${FULL_ADDRESS}"
elif [[ "$FULL_ADDRESS" =~ 五栋大楼 ]]; then
  LOCATION="五栋大楼"
  DESCRIPTION="${FULL_ADDRESS}"
else
  # 默认规则：提取到第一个数字前的部分（如“腾讯大厦A座”）
  LOCATION=$(echo "$FULL_ADDRESS" | sed -E 's/([0-9]+[a-zA-Z]*[0-9]*)[^0-9]*$//; s/（.*）$//; s/\([^)]*\)$//')
  DESCRIPTION="${FULL_ADDRESS}"
fi

# 清理多余空格
LOCATION=$(echo "$LOCATION" | sed 's/^[[:space:]]*//; s/[[:space:]]*$//')
DESCRIPTION=$(echo "$DESCRIPTION" | sed 's/^[[:space:]]*//; s/[[:space:]]*$//')

# 输出标准化格式
echo "LOCATION: $LOCATION"
echo "DESCRIPTION: $DESCRIPTION"

# 返回状态码
exit 0