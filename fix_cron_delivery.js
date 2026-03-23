const fs = require('fs');
const path = require('path');

const cronJobsPath = path.join(process.env.HOME, '.openclaw', 'cron', 'jobs.json');
const data = JSON.parse(fs.readFileSync(cronJobsPath, 'utf8'));

// 获取当前微信用户的ID
const currentWeChatId = '044cf7e98993-im-bot@im.wechat';

// 修复需要推送的任务
const tasksToFix = [
  'c83da580-1e10-4a70-807c-52e097fbf945', // 每日 Token 使用报告
  '132d6bb9-b729-4e06-9f24-2adef059d018', // 弗洛一德 - 每周总结
  '955f2ab4-a8bc-420b-b013-b4840233b14e', // 数字幕僚 - 每周总结
  'a176fd9b-829e-4b1e-a958-cd5c55adf8d9', // 写作助手 - 每周总结
  'a068c821-a138-4873-9542-c6194b338ac9', // 觉醒教练 - 每周总结
  '9eb01c2c-55a0-46cd-9aef-888cb0fa7cd8'  // 健康顾问 - 每周总结
];

data.jobs.forEach(job => {
  if (tasksToFix.includes(job.id)) {
    // 设置正确的微信通道和目标
    if (!job.delivery) {
      job.delivery = {};
    }
    job.delivery.channel = 'openclaw-weixin';
    job.delivery.to = currentWeChatId;
    job.delivery.mode = 'announce';
    
    console.log(`已修复任务: ${job.name}`);
  }
});

// 备份原文件
const backupPath = cronJobsPath + '.backup.' + Date.now();
fs.copyFileSync(cronJobsPath, backupPath);
console.log(`已备份原文件到: ${backupPath}`);

// 写入修复后的文件
fs.writeFileSync(cronJobsPath, JSON.stringify(data, null, 2));
console.log('定时任务配置已修复！');