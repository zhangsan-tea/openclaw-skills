# 药品管理系统 - 常见问题 FAQ

> 💡 快速解决常见问题，按场景分类

---

## 🚀 安装问题

### Q: 安装脚本运行失败

**症状**：运行 `bash scripts/install.sh` 时报错

**可能原因和解决**：

1. **权限问题**
```bash
chmod +x scripts/install.sh
bash scripts/install.sh
```

2. **OpenClaw 未安装**
```bash
# 检查是否安装
openclaw --version

# 未安装请先安装
# 参考：https://docs.openclaw.ai
```

3. **工作目录不存在**
```bash
mkdir -p /Users/lee/.openclaw/workspace-health-advisor/medications/photos
```

---

### Q: Google Drive 授权失败

**症状**：点击授权链接后显示错误

**解决步骤**：

1. **检查网络**
```bash
ping www.google.com
```

2. **确认账号正确**
- 确保使用正确的 Google 账号登录
- 如果是公司账号，可能需要管理员批准

3. **重新授权**
```bash
gog auth add YOUR_EMAIL@gmail.com
```

4. **启用 Drive API**
- 访问：https://console.developers.google.com/apis/api/drive.googleapis.com
- 点击"启用"按钮
- 等待几分钟后重试

---

### Q: 定时任务创建失败

**症状**：安装脚本提示定时任务创建失败

**解决**：

1. **检查 cron 服务**
```bash
cron status
```

2. **手动创建**
```bash
# 编辑 cron job 文件
cat > /tmp/med_cron.json << 'EOF'
{
  "name": "健康顾问 - 每周药品检查",
  "schedule": {
    "kind": "cron",
    "expr": "0 9 * * 0",
    "tz": "Asia/Shanghai"
  },
  "payload": {
    "kind": "agentTurn",
    "message": "你是健康顾问。请执行每周家庭药品检查",
    "model": "coding-plan/glm-5"
  },
  "sessionTarget": "isolated",
  "delivery": {
    "mode": "announce",
    "channel": "telegram",
    "to": "8051279955"
  }
}
EOF

# 添加任务
cron add --job /tmp/med_cron.json
```

---

## 📱 使用问题

### Q: 没有收到每周提醒

**症状**：周日上午没有收到药品检查报告

**排查步骤**：

1. **检查 Gateway 状态**
```bash
openclaw gateway status
```

2. **检查定时任务**
```bash
cron list | grep 药品
```

3. **查看任务状态**
```bash
# 应该显示 enabled: true
# 如果显示 false，需要启用
```

4. **手动触发测试**
```bash
# 获取 job ID
cron list | grep 药品

# 手动运行
cron run --job-id <JOB_ID>
```

5. **检查 Telegram**
- 确认 Telegram 正常运行
- 确认能收到其他消息

---

### Q: 药品清单为空

**症状**：查看药品清单时显示为空

**解决**：

1. **检查 CSV 文件**
```bash
cat /Users/lee/.openclaw/workspace-health-advisor/medications/medications.csv
```

2. **添加药品**
```
用户：添加药品 - 布洛芬，保质期 2028-06-30
```

3. **导入现有数据**
```bash
# 如果有备份
cp medications/backups/medications_backup_*.csv medications/medications.csv
```

---

### Q: 药品信息录入错误

**症状**：保质期或药品名称错了

**解决**：

**方式 1：更新信息**
```
用户：更新 med_001 的保质期为 2028-01-01
用户：更新 med_002 的名称为 布洛芬缓释胶囊
```

**方式 2：删除重新添加**
```
用户：删除 med_001
用户：添加药品 - 布洛芬，保质期 2028-06-30
```

**方式 3：直接编辑 CSV**
```bash
# 打开 CSV 文件
vi /Users/lee/.openclaw/workspace-health-advisor/medications/medications.csv

# 修改后保存
```

---

### Q: 误删了药品

**症状**：不小心删除了重要药品记录

**解决**：

1. **从备份恢复**
```bash
# 查看备份
ls -la medications/backups/

# 恢复最新备份
cp medications/backups/medications_backup_最新日期.csv medications/medications.csv
```

2. **重新添加**
```
用户：添加药品 - XXX，保质期 YYYY-MM-DD
```

---

## 🔧 技术问题

### Q: 模型全部失败

**症状**：提示所有模型都无法使用

**排查**：

1. **检查本地模型**
```bash
ollama list
# 应该看到 qwen3:8b
```

2. **检查云端 API**
```bash
# 测试 API 连接
curl -I https://api.example.com
```

3. **查看错误日志**
```bash
cat ~/.openclaw/logs/cron.log | grep 药品
```

**解决**：

1. **安装本地模型**
```bash
ollama pull qwen3:8b
```

2. **更新 API Key**
```bash
openclaw configure --set API_KEY=new_key
```

3. **降级到本地模型**
```json
{
  "payload": {
    "model": "ollama/qwen3:8b"
  }
}
```

---

### Q: CSV 文件读取失败

**症状**：提示无法读取药品清单

**可能原因**：

1. **文件编码问题**
```bash
# 检查编码
file medications/medications.csv
# 应该是 UTF-8

# 转换编码
iconv -f gbk -t utf-8 medications/medications.csv > temp.csv
mv temp.csv medications/medications.csv
```

2. **文件格式错误**
```python
# 修复 CSV 格式
python3 << 'EOF'
import pandas as pd
df = pd.read_csv('medications/medications.csv', encoding='utf-8-sig')
df.to_csv('medications/medications.csv', index=False)
print("✅ CSV 格式已修复")
EOF
```

3. **文件被锁定**
```bash
# 检查是否有进程占用
lsof medications/medications.csv

# 重启 Gateway
openclaw gateway restart
```

---

### Q: 照片无法上传

**症状**：上传药品照片失败

**解决**：

1. **检查照片大小**
- Telegram 限制：照片不超过 10MB
- 压缩照片后再上传

2. **检查目录权限**
```bash
ls -la medications/photos/
# 确保有写入权限
```

3. **手动保存照片**
```bash
# 保存照片到正确位置
mv ~/Downloads/photo.jpg medications/photos/file_1.jpg
```

---

## 💡 最佳实践

### 日常维护

**每周**：
- [ ] 查看药品检查报告
- [ ] 确认过期药品处理情况
- [ ] 清理已过期药品

**每月**：
- [ ] 检查备份是否正常
- [ ] 更新药品清单（新药/用完的药）
- [ ] 检查系统状态

**每季度**：
- [ ] 整理药箱（按分区整理）
- [ ] 拍摄新药照片
- [ ] 导出 CSV 备份

---

### 药品录入技巧

**快速录入**：
```
格式：添加药品 - 药品名，保质期 YYYY-MM-DD

示例：
添加药品 - 布洛芬，保质期 2028-06-30
添加药品 - 感冒清热颗粒，保质期 2026-01-31
```

**批量录入**：
```
# 准备 CSV 文件
药品 ID，药品名称，功效，保质期，生产批号，存放位置，分区，录入时间，照片路径，状态
med_001，布洛芬，止痛，2028-06-30,,,,2026-03-22,,active
med_002，感冒清热颗粒，感冒，2026-01-31,,,,2026-03-22,,active

# 导入
cat batch_import.csv >> medications/medications.csv
```

---

### 数据备份策略

**自动备份**：
- 系统每天自动备份
- 备份位置：`medications/backups/`

**手动备份**：
```bash
# 运行备份脚本
bash medications/scripts/backup.sh

# 或手动复制
cp medications/medications.csv medications/medications_backup_$(date +%Y%m%d).csv
```

**云端备份**：
```bash
# 上传到 Google Drive
gog drive upload medications/backups/medications_backup_*.csv
```

---

## 📞 获取帮助

### 自助排查

```bash
# 运行状态检查
bash scripts/check_status.sh

# 查看日志
cat memory/medication_log.md

# 测试连接
bash scripts/test_connection.sh
```

### 文档资源

- 安装指南：`docs/INSTALL_GUIDE.md`
- 用户手册：`docs/USER_MANUAL.md`
- 技能文档：`SKILL.md`

### 社区支持

- GitHub Issues: 提交问题
- 文档：https://docs.openclaw.ai
- 社区：https://discord.com/invite/clawd

---

## ⚠️ 重要提醒

### 医疗免责

> 本系统提供的药品管理功能仅供参考，不能替代专业医疗建议。用药请遵医嘱，如有健康问题，请咨询医生或药师。

### 隐私保护

> 药品数据包含个人健康信息，请妥善保管，不要分享给他人。

### 数据安全

> 定期备份药品数据，避免因系统故障导致数据丢失。

---

**最后更新**: 2026-03-22
**版本**: v1.0
