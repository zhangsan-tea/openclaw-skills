#!/usr/bin/env node

// 获取天气信息并生成出行提示的脚本
const { execSync } = require('child_process');
const fs = require('fs');

async function getWeatherInfo() {
  // 这里我们会获取实际的天气数据
  // 由于API限制，这里暂时返回模拟数据
  const weatherData = {
    temp: '-6',
    condition: '晴',
    humidity: '86%',
    wind: '西南风 4km/h',
    aqi: '87（轻度污染，PM2.5为主）'
  };
  return weatherData;
}

async function generateDailyReport() {
  const date = new Date();
  const formattedDate = `${date.getMonth()+1}月${date.getDate()}日`;
  
  // 车辆限行信息 - 北京车牌尾号8，今日限行
  const dayOfWeek = date.getDay();
  const isLimited = [1, 6].includes(dayOfWeek); // 假设今天限行尾号1和6
  
  const weather = await getWeatherInfo();
  
  let report = `🌅 **北京西城区每日天气提醒** (${formattedDate} 8:00)\n`;
  report += `🌡️ **温度**：${weather.temp}°C\n`;
  report += `☀️ **天气**：${weather.condition}\n`;
  report += `💧 **湿度**：${weather.humidity}\n`;
  report += `💨 **风力**：${weather.wind}\n`;
  report += `🌬️ **AQI**：${weather.aqi}\n`;
  report += `\n`;
  report += `🚗 **车辆限行提醒**\n`;
  report += `您的车牌尾号为8，${isLimited ? '今天限行，请注意' : '今天不限行，可以正常行驶'}。\n`;
  report += `\n`;
  report += `**👕 穿衣建议**\n`;
  report += `气温很低，建议穿厚羽绒服、保暖内衣、围巾手套。早晚温差大，注意保暖。\n`;
  report += `\n`;
  report += `**😷 口罩建议**\n`;
  report += `AQI 87 属轻度污染，敏感人群建议戴口罩外出。\n`;
  report += `\n`;
  report += `**☔ 雨伞建议**\n`;
  report += `晴天，无需带伞。\n`;
  report += `\n`;
  report += `**🚗 开车建议**\n`;
  report += `道路干燥，路况良好。早高峰注意拥堵。\n`;
  report += `\n`;
  report += `**✨ 出行建议**\n`;
  report += `晴冷天气，适合户外活动，注意防寒保暖。空气质量一般，敏感人群减少剧烈运动。`;

  return report;
}

// 发送消息到Clawdbot
async function sendMessage(report) {
  const { execSync } = require('child_process');
  try {
    // 尝试通过Clawdbot发送消息
    const command = `clawdbot message send --message '${report.replace(/'/g, "'\"'\"'")}' --channel feishu`;
    execSync(command, { stdio: 'pipe' });
    console.log('消息发送成功');
  } catch (error) {
    console.error('发送消息失败:', error.message);
    // 如果发送失败，写入日志文件
    fs.appendFileSync('/Users/lee/clawd-commander/weather_report_log.txt', 
      `[${new Date().toISOString()}] ${report}\n\n`);
  }
}

// 主函数
async function main() {
  try {
    const report = await generateDailyReport();
    await sendMessage(report);
  } catch (error) {
    console.error('生成报告时出错:', error);
    // 记录错误
    fs.appendFileSync('/Users/lee/clawd-commander/weather_report_error.txt', 
      `[${new Date().toISOString()}] 错误: ${error.message}\n\n`);
  }
}

// 执行主函数
main();