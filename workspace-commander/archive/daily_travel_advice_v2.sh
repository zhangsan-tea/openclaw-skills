#!/bin/bash

# 每日出行提示脚本 - 完善版
# 作者: 弗洛一德
# 尾号: 8
# 地区: 上海 (天气) + 北京 (限行)

DATE=$(date +"%Y-%m-%d")
DAY_OF_WEEK=$(date +"%u") # 1=Monday, 7=Sunday
TODAY_NAME=$(date +"%A")

# 获取上海天气
WEATHER_DATA=$(curl -s "https://wttr.in/Shanghai?format=j1")
if [ $? -eq 0 ] && [ -n "$WEATHER_DATA" ]; then
    TEMP_C=$(echo "$WEATHER_DATA" | jq -r '.weather[0].hourly[] | select(.time=="900") | .tempC' 2>/dev/null)
    WEATHER_DESC=$(echo "$WEATHER_DATA" | jq -r '.weather[0].hourly[] | select(.time=="900") | .weatherDesc[0].value' 2>/dev/null)
    HUMIDITY=$(echo "$WEATHER_DATA" | jq -r '.current_condition[0].humidity' 2>/dev/null)
    
    if [ "$TEMP_C" = "null" ] || [ -z "$TEMP_C" ]; then
        TEMP_C="N/A"
        WEATHER_DESC="无法获取天气数据"
        HUMIDITY="N/A"
    fi
else
    TEMP_C="N/A"
    WEATHER_DESC="无法获取天气数据"
    HUMIDITY="N/A"
fi

# 穿衣建议
CLOTHING="请查看天气预报后决定"
if [ "$TEMP_C" != "N/A" ]; then
    TEMP_NUM=$(echo "$TEMP_C" | tr -d '"')
    if [ "$TEMP_NUM" -ge 25 ]; then
        CLOTHING="夏季服装：短袖、短裤、轻薄透气"
    elif [ "$TEMP_NUM" -ge 20 ]; then
        CLOTHING="春末夏初：长袖衬衫、薄外套、长裤"
    elif [ "$TEMP_NUM" -ge 15 ]; then
        CLOTHING="春季服装：长袖T恤、薄外套、长裤"
    elif [ "$TEMP_NUM" -ge 10 ]; then
        CLOTHING="初春服装：厚长袖、夹克、长裤"
    elif [ "$TEMP_NUM" -ge 5 ]; then
        CLOTHING="冬季服装：毛衣、厚外套、保暖裤"
    else
        CLOTHING="严寒服装：羽绒服、保暖内衣、帽子手套"
    fi
fi

# 北京限行判断 (工作日限行，周末不限行)
LIMITED_TODAY="不限行"
LIMIT_INFO=""
if [ "$DAY_OF_WEEK" -le 5 ]; then
    # 工作日，北京限行规则：周一1&6, 周二2&7, 周三3&8, 周四4&9, 周五5&0
    case $DAY_OF_WEEK in
        1)
            LIMIT_INFO="今日限行尾号：1, 6"
            ;;
        2)
            LIMIT_INFO="今日限行尾号：2, 7"
            ;;
        3)
            LIMIT_INFO="今日限行尾号：3, 8"
            LIMITED_TODAY="⚠️ 限行！尾号8今日限行"
            ;;
        4)
            LIMIT_INFO="今日限行尾号：4, 9"
            ;;
        5)
            LIMIT_INFO="今日限行尾号：5, 0"
            ;;
    esac
else
    LIMIT_INFO="周末不限行"
fi

# 生成出行提示
OUTPUT="
📅 $DATE ($TODAY_NAME) 出行提示

🌤️ 天气状况（上海）：
- 温度：${TEMP_C}°C
- 天气：$WEATHER_DESC
- 湿度：${HUMIDITY}%

👕 穿衣建议：
$CLOTHING

🚗 北京限行提醒（尾号8）：
$LIMITED_TODAY
$LIMIT_INFO

💡 出行建议：
- 如需前往北京，请注意限行规定
- 根据天气情况合理安排出行时间
- 雨天路滑，注意安全

---
由弗洛一德每日自动推送
"

# 输出到标准输出（供OpenClaw cron使用）
echo "$OUTPUT"