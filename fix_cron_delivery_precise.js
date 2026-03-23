const fs = require('fs');
const path = require('path');

const cronJobsPath = path.join(process.env.HOME, '.openclaw', 'cron', 'jobs.json');
const data = JSON.parse(fs.readFileSync(cronJobsPath, 'utf8'));

// 获取当前微信用户的ID
const currentWeChatId = '044cf7e98993-im-bot@im.wechat';

// 只保留每天早上8点的出行提醒在微信
const morningReminderTaskId = 'f83a599f-c7da-40e9-9e2d-00026f8af4ee'; // 每日早上8点出行提示（尾号8）

// 其他需要修复的定时任务（保持在Telegram）
const telegramTasksToFix = [
  'c83da580-1e10-4a70-807c-52e097fbf945', // 每日 Token 使用报告
  '132d6bb9-b729-4e06-9f24-2adef059d018', // 弗洛一德 - 每周总结
  '955f2ab4-a8bc-420b-b013-b4840233b14e', // 数字幕僚 - 每周总结
  'a176fd9b-829e-4b1e-a958-cd5c55adf8d9', // 写作助手 - 每周总结
  'a068c821-a138-4873-9542-c6194b338ac9', // 觉醒教练 - 每周总结
  '9eb01c2c-55a0-46cd-9aef-888cb0fa7cd8'  // 健康顾问 - 每周总结
];

data.jobs.forEach(job => {
  if (job.id === morningReminderTaskId) {
    // 早上8点出行提醒：保留在微信，但不需要delivery配置（因为是systemEvent类型）
    // systemEvent类型的任务会自动推送到当前会话，不需要显式delivery配置
    if (job.delivery) {
      delete job.delivery;
    }
    console.log(`✅ 保留任务在微信: ${job.name}`);
  } else if (telegramTasksToFix.includes(job.id)) {
    // 其他任务：配置为推送到Telegram
    if (!job.delivery) {
      job.delivery = {};
    }
    job.delivery.channel = 'telegram';
    job.delivery.to = '8051279955'; // 您的Telegram ID
    job.delivery.mode = 'announce';
    console.log(`✅ 配置任务到Telegram: ${job.name}`);
  }
});

// 备份原文件
const backupPath = cronJobsPath + '.backup.precise.' + Date.now();
fs.copyFileSync(cronJobsPath, backupPath);
console.log(`已备份原文件到: ${backupPath}`);

// 写入修复后的文件
fs.writeFileSync(cronJobsPath, JSON.stringify(data, null, 2));
console.log('定时任务配置已精确修复！');