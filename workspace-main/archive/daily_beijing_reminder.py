#!/usr/bin/env python3
"""
每日北京出行提示脚本
包含天气信息和车牌尾号限行提示
"""

import requests
import datetime
import json
import re

def get_beijing_weather():
    """获取北京天气信息"""
    # 使用免费的天气API获取北京天气
    try:
        # 尝试使用wttr.in天气服务
        url = "http://wttr.in/Beijing?format=j1"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            current = data['current_condition'][0]
            location = data['nearest_area'][0]
            
            weather_info = {
                'location': f"{location['areaName'][0]['value']}, {location['country'][0]['value']}",
                'temperature': current['temp_C'],
                'description': current['weatherDesc'][0]['value'],
                'humidity': current['humidity'],
                'feels_like': current['FeelsLikeC']
            }
            return weather_info
    except Exception as e:
        print(f"获取天气信息失败: {e}")
        
    # 如果上面的API不可用，返回默认信息
    return {
        'location': '北京',
        'temperature': 'N/A',
        'description': '请查看天气应用获取最新天气',
        'humidity': 'N/A',
        'feels_like': 'N/A'
    }

def get_beijing_limitation_info():
    """获取北京尾号限行信息"""
    today = datetime.date.today()
    weekday = today.weekday() + 1  # 周一为1，周日为7
    
    # 北京限行政策：工作日(周一至周五)限行
    # 根据年份和月份调整限行尾号规则
    # 通常周一至周五限行尾号分别为：[1, 6], [2, 7], [3, 8], [4, 9], [5, 0]
    # 对应周一到周五
    limitation_map = {
        1: [1, 6],  # 周一
        2: [2, 7],  # 周二
        3: [3, 8],  # 周三
        4: [4, 9],  # 周四
        5: [5, 0],  # 周五
        6: [],      # 周六 不限行
        7: []       # 周日 不限行
    }
    
    is_weekend = weekday >= 6
    if is_weekend:
        return {
            'weekday': weekday,
            'is_limited': False,
            'limited_numbers': [],
            'message': '今天是周末，不限行'
        }
    else:
        limited_numbers = limitation_map[weekday]
        return {
            'weekday': weekday,
            'is_limited': True,
            'limited_numbers': limited_numbers,
            'message': f'今天是工作日，限行尾号: {", ".join(map(str, limited_numbers))}'
        }

def generate_message():
    """生成出行提示消息"""
    now = datetime.datetime.now()
    
    # 获取天气信息
    weather = get_beijing_weather()
    
    # 获取限行信息
    limitation = get_beijing_limitation_info()
    
    # 构建消息
    message = f"🌅 早安！{now.strftime('%Y年%m月%d日')} ({now.strftime('%A')})\n\n"
    message += f"📍 天气信息:\n"
    message += f"   地点: {weather['location']}\n"
    message += f"   温度: {weather['temperature']}°C (体感 {weather['feels_like']}°C)\n"
    message += f"   状况: {weather['description']}\n"
    message += f"   湿度: {weather['humidity']}%\n\n"
    
    message += f"🚗 出行提示:\n"
    message += f"   今天是{['', '周一', '周二', '周三', '周四', '周五', '周六', '周日'][limitation['weekday']]}\n"
    message += f"   限行情况: {limitation['message']}\n"
    
    # 特别提醒车牌尾号为8的车辆
    if 8 in limitation['limited_numbers']:
        message += f"   ⚠️ 特别提醒: 您的车牌尾号为8，今天在工作日时段(7-20时)限行，请注意!\n"
    else:
        message += f"   提醒: 如需驾车出行，请注意交通状况\n"
    
    message += f"\n祝您今天愉快！"
    
    return message

def main():
    """主函数"""
    try:
        message = generate_message()
        print(message)
        
        # 这里可以添加发送消息的逻辑，如通过邮件、微信、或其他方式
        # 为了简单起见，这里只是打印出来
    except Exception as e:
        print(f"生成出行提示时发生错误: {e}")

if __name__ == "__main__":
    main()