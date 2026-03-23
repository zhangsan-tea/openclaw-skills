---
name: medication-management
description: 药品管理系统。当用户需要管理家庭药品、检查过期药品、设置用药提醒、药品清单维护、药品照片识别等相关需求时使用。支持多模型切换、错误处理和用户互动。
---

# 药品管理系统 Skill

## 功能概述

本系统提供完整的家庭药品管理方案，包括：

1. **定期药品检查** - 自动检查过期和即将过期药品
2. **药品清单管理** - 维护药品信息、照片、存放位置
3. **用药提醒** - 设置用药时间和剂量提醒
4. **智能识别** - 支持照片识别、条形码扫描（可选）
5. **多模型切换** - 根据任务复杂度自动选择模型
6. **错误处理** - 完善的错误处理和用户互动机制

---

## 核心特性

### 🛡️ 鲁棒性设计

| 特性 | 说明 |
|-----|------|
| **多模型备份** | 主模型失败自动切换到备用模型 |
| **错误恢复** | 检测错误后自动重试或请求用户帮助 |
| **用户互动** | 关键决策点请求用户确认 |
| **状态追踪** | 记录每次检查状态，便于故障排查 |
| **降级方案** | 高级功能失败时降级到基础功能 |

### 🔄 模型切换策略

```
任务类型 → 模型选择
├─ 简单检查（过期判断） → ollama/qwen3:8b（本地，快速）
├─ 标准分析（周报生成） → coding-plan/glm-5（云端，平衡）
├─ 复杂分析（趋势报告） → coding-plan/qwen3-max-2026-01-23（高级）
└─ 模型失败 → 自动切换下一级
```

---

## 前置条件

### 硬件/软件要求

| 项目 | 要求 | 说明 |
|-----|------|------|
| OpenClaw | 已安装 | 运行自动化脚本 |
| 模型访问 | 至少一个可用 | ollama 本地模型或云端 API |
| 存储空间 | 至少 100MB | 存储药品照片 |

### 可选配置

| 项目 | 用途 |
|-----|------|
| Google Drive | 备份药品数据 |
| OCR 服务 | 药品标签识别 |
| 条形码扫描 App | 快速录入药品 |

---

## 文件结构

```
<WORKSPACE>/
├── medications/
│   ├── medications.csv          # 药品清单（核心）
│   ├── medications_backup.csv   # 备份文件
│   └── photos/                  # 药品照片
│       ├── file_1.jpg
│       └── ...
├── memory/
│   ├── medication_log.md        # 用药记录
│   └── medication_reports/      # 检查报告
│       └── 2026-W12.md
└── medication_config.json       # 配置文件
```

---

## 配置流程

### 第 1 步：创建药品清单

CSV 文件格式：

```csv
药品 ID，药品名称，功效，保质期，生产批号，存放位置，分区，录入时间，照片路径，状态
med_001，金银花口服液，清热解毒，2027-08-31,2509313,A,A 区，2026-03-22,photos/file_1.jpg,active
```

**必填字段**：
- 药品名称
- 保质期
- 状态（active/expired/used）

**选填字段**：
- 功效
- 生产批号
- 存放位置
- 照片路径

### 第 2 步：配置定时任务

创建每周药品检查 cron job：

```json
{
  "name": "健康顾问 - 每周药品检查",
  "schedule": {
    "kind": "cron",
    "expr": "0 9 * * 0",
    "tz": "Asia/Shanghai"
  },
  "payload": {
    "kind": "agentTurn",
    "message": "你是健康顾问。请执行每周家庭药品检查：\n\n1. 读取 medications/medications.csv\n2. 检查已过期的药品（保质期 < 今天）\n3. 检查未来 7 天内到期的药品\n4. 发送完整检查报告，并带上确认按钮\n\n格式：\n💊 每周药品检查报告\n\n【已过期的药品】\n[列表]\n\n【未来 7 天内到期】\n[列表]\n\n👇 请确认过期药品处理情况",
    "model": "coding-plan/glm-5"
  },
  "sessionTarget": "isolated",
  "delivery": {
    "mode": "announce",
    "channel": "telegram",
    "to": "<CHAT_ID_OR_USER>"
  }
}
```

### 第 3 步：配置模型切换

在 cron job 中不硬编码模型，而是使用模型策略：

```json
{
  "payload": {
    "kind": "agentTurn",
    "message": "...",
    "model": "auto"  // 自动选择
  }
}
```

或在 skill 中定义模型选择逻辑。

---

## 核心功能

### 1. 每周药品检查

**触发时间**：每周日 9:00

**检查逻辑**：

```python
# 伪代码
today = get_current_date()
expired = []
expiring_soon = []

for med in medications:
    expiry_date = parse_date(med.expiry)
    days_until_expiry = (expiry_date - today).days
    
    if days_until_expiry < 0:
        expired.append(med)
    elif days_until_expiry <= 7:
        expiring_soon.append(med)
```

**输出格式**：

```
💊 每周药品检查报告
**检查日期**: 2026-03-22

【已过期的药品】(3 种)
❌ 美愈伪麻口服溶液 — 过期 1 年 (2024-02-29)
❌ 复方氨酚烷胺片 — 过期 9 个月 (2025-06-30)
❌ 感冒清热颗粒（无蔗糖）— 过期 2 个月 (2026-01-31)

【未来 7 天内到期】(0 种)
✅ 无

👇 请确认过期药品处理情况

[✅ 已全部处理] [⏳ 部分处理] [❌ 还未处理]
```

**互动按钮**：
- ✅ 已全部处理 → 更新状态，记录日志
- ⏳ 部分处理 → 追问哪些处理了
- ❌ 还未处理 → 设置 3 天后提醒

### 2. 药品清单管理

#### 添加药品

**方式 1：手动录入**
```
用户：添加药品 - 金银花口服液，保质期 2027-08-31
```

**方式 2：照片识别**（可选）
```
用户上传照片 → OCR 识别 → 提取药品名称和保质期 → 确认 → 保存
```

**方式 3：条形码扫描**（可选）
```
扫描条形码 → 查询药品数据库 → 自动填充 → 确认 → 保存
```

#### 更新药品

```
用户：更新 med_001 的保质期为 2028-01-01
```

#### 删除药品

```
用户：删除 med_003
→ 确认：确定要删除"复方氨酚烷胺片"吗？
→ 用户确认 → 删除
```

### 3. 用药提醒

**设置提醒**：

```json
{
  "name": "用药提醒 - 金银花口服液",
  "schedule": {
    "kind": "every",
    "everyMs": 86400000,  // 每天
    "anchorMs": 1774180800000  // 早上 8:00
  },
  "payload": {
    "kind": "systemEvent",
    "text": "💊 用药提醒：金银花口服液\n\n用量：10ml，每日 3 次\n功效：清热解毒\n\n请按时服药！"
  }
}
```

### 4. 智能识别

#### 照片 OCR 识别

使用场景：
- 用户拍摄药品包装
- 系统提取药品名称、保质期、批号
- 用户确认信息
- 保存到药品清单

**实现方式**：
- 本地 OCR（Tesseract）
- 云端 OCR（Google Vision、百度 OCR）

#### 条形码识别

使用场景：
- 用户扫描药品条形码
- 查询药品数据库
- 自动填充药品信息

**实现方式**：
- 手机 App 扫描
- 查询国家药监局数据库

---

## 模型切换机制

### 模型优先级

```
主模型：coding-plan/glm-5（平衡性能和成本）
↓ 失败
备用 1: ollama/qwen3:8b（本地，免费）
↓ 失败
备用 2: coding-plan/qwen3-max-2026-01-23（高级）
↓ 失败
降级：返回错误，请求用户帮助
```

### 实现代码

```python
def check_medications_with_fallback():
    models = [
        "coding-plan/glm-5",
        "ollama/qwen3:8b",
        "coding-plan/qwen3-max-2026-01-23"
    ]
    
    for model in models:
        try:
            result = run_check(model=model)
            if result.success:
                log_success(model)
                return result
        except Exception as e:
            log_error(model, e)
            continue
    
    # 所有模型都失败
    return request_user_help()
```

### 错误处理策略

| 错误类型 | 处理方式 |
|---------|---------|
| 模型超时 | 切换到备用模型 |
| API 认证失败 | 通知用户更新 API Key |
| 文件读取失败 | 尝试读取备份文件 |
| CSV 格式错误 | 提示用户修复或自动修复 |

---

## 用户互动机制

### 需要用户确认的场景

1. **删除药品** - 防止误删
2. **批量更新** - 确认批量操作
3. **模型全部失败** - 请求手动介入
4. **数据异常** - 如保质期格式错误

### 互动方式

**Telegram 按钮**：
```
[✅ 确认] [❌ 取消]
```

**追问机制**：
```
系统：检测到 3 种药品已过期，确认全部标记为已处理吗？
用户：否
系统：请告诉我是哪几种处理了？
```

**语音/文字输入**：
```
用户：感康已经扔了，其他的还没处理
系统：已记录：复方氨酚烷胺片（感康）- 已处理
      剩余 2 种未处理，3 天后提醒你
```

---

## 使用说明

### 日常使用

#### 查看药品清单

```
用户：查看药品清单
系统：📋 家庭药品清单（共 27 种）

A 区（8 种）：
- 金银花口服液（2027-08-31）✅
- 香清解口服液（2027-04-30）✅
...

B 区（9 种）：
...

C 区（10 种）：
...
```

#### 查询特定药品

```
用户：感冒药有哪些？
系统：💊 感冒相关药品：

1. 复方氨酚烷胺片（感康）- 过期 ❌
2. 感冒清热颗粒 - 过期 ❌
3. 金花清感颗粒 - 2026-10-23 ✅
4. 小柴胡颗粒 - 2027-02-07 ✅
```

#### 添加药品

```
用户：添加药品 - 布洛芬缓释胶囊，保质期 2028-06-30
系统：✅ 已添加：
      药品 ID: med_028
      名称：布洛芬缓释胶囊
      保质期：2028-06-30
      状态：active
```

### 管理员操作

#### 备份药品数据

```bash
cp medications/medications.csv medications/medications_backup_$(date +%Y%m%d).csv
```

#### 修复 CSV 格式

```python
# 检查并修复 CSV 格式问题
import pandas as pd

df = pd.read_csv('medications/medications.csv')
# 修复日期格式
df['保质期'] = pd.to_datetime(df['保质期']).dt.strftime('%Y-%m-%d')
df.to_csv('medications/medications.csv', index=False)
```

#### 查看检查日志

```bash
cat memory/medication_reports/2026-W12.md
```

---

## 故障排查

### 问题 1：定时任务未执行

**检查步骤**：

1. 检查 cron job 状态
```bash
cron list | grep 药品
```

2. 检查 Gateway 运行状态
```bash
openclaw gateway status
```

3. 查看错误日志
```bash
cat ~/.openclaw/logs/cron.log | grep 药品
```

**解决方案**：
- 重新创建 cron job
- 重启 Gateway
- 检查模型 API 是否正常

### 问题 2：CSV 文件读取失败

**可能原因**：
- 文件被锁定
- 编码问题
- 格式错误

**解决方案**：

1. 检查文件编码
```bash
file medications/medications.csv
# 应该是 UTF-8
```

2. 尝试读取备份文件
```bash
cp medications/medications_backup.csv medications/medications.csv
```

3. 手动修复格式
```python
import pandas as pd
df = pd.read_csv('medications/medications.csv', encoding='utf-8-sig')
df.to_csv('medications/medications.csv', index=False)
```

### 问题 3：所有模型都失败

**可能原因**：
- 网络问题
- API Key 过期
- 服务不可用

**解决方案**：

1. 检查网络连接
```bash
ping api.example.com
```

2. 更新 API Key
```bash
openclaw configure --set API_KEY=new_key
```

3. 切换到本地模型
```json
{
  "payload": {
    "model": "ollama/qwen3:8b"
  }
}
```

4. 手动执行检查
```
用户：手动执行药品检查
系统：好的，正在检查...
```

### 问题 4：用户未响应确认

**处理方式**：

1. 设置超时（24 小时）
2. 超时后发送提醒
3. 仍未响应则标记为"待确认"
4. 下次检查时再次提醒

---

## 扩展功能

### 可添加的功能

1. **药品相互作用检查** - 提醒不能同时服用的药品
2. **库存管理** - 药品数量追踪，低库存提醒
3. **电子说明书** - 存储药品说明书 PDF
4. **家庭成员管理** - 多用户用药管理
5. **用药统计** - 月度/季度用药报告
6. **医院处方整合** - 整合医院处方记录

### 与其他工具集成

- **Google Drive** - 备份药品数据和照片
- **Obsidian** - 同步用药日记到知识库
- **Telegram Bot** - 通过 bot 命令管理药品
- **Home Assistant** - 智能家居用药提醒

---

## 配置文件示例

### medication_config.json

```json
{
  "reminder_settings": {
    "check_frequency": "weekly",
    "check_day": "sunday",
    "check_time": "09:00",
    "advance_days": [7, 0],
    "enabled": true
  },
  "storage": {
    "csv_path": "medications/medications.csv",
    "backup_enabled": true,
    "backup_frequency": "daily",
    "photos_dir": "medications/photos",
    "cloud_backup": {
      "enabled": true,
      "provider": "google_drive",
      "folder": "medications_backup"
    }
  },
  "recognition": {
    "enable_barcode": false,
    "enable_photo_ocr": true,
    "ocr_provider": "google_vision",
    "manual_fallback": true,
    "photo_pair_mode": true
  },
  "models": {
    "primary": "coding-plan/glm-5",
    "fallback": [
      "ollama/qwen3:8b",
      "coding-plan/qwen3-max-2026-01-23"
    ],
    "timeout_seconds": 60,
    "max_retries": 3
  },
  "notifications": {
    "channel": "telegram",
    "user_id": "<USER_ID>",
    "enable_buttons": true,
    "reminder_interval_hours": 24
  },
  "multi_user": {
    "enabled": false,
    "version": "2.0"
  }
}
```

---

## 安全注意事项

### 隐私保护

- 药品数据包含个人健康信息
- 存储在本地或受信任的云端
- 仅授权代理人访问
- 定期备份重要数据

### 数据安全

- CSV 文件设置权限（仅用户可读）
- 照片存储限制访问
- 云端备份启用加密
- 定期删除过期备份

### 医疗免责声明

本系统提供的药品管理功能仅供参考，不能替代专业医疗建议。用药请遵医嘱，如有健康问题，请咨询医生或药师。

---

## 版本历史

- **v1.0** (2026-03-22) - 初始版本
  - 药品清单管理
  - 每周自动检查
  - 过期药品提醒
  - Telegram 互动按钮
  - 多模型切换
  - 错误处理机制

- **v1.1** (计划中)
  - 照片 OCR 识别
  - 条形码扫描
  - 用药提醒
  - Google Drive 备份

---

## 相关文件

- `medications/medications.csv` - 药品清单
- `medication_config.json` - 配置文件
- `memory/medication_log.md` - 用药记录
- `memory/medication_reports/` - 检查报告

---

## 快速参考

### 常用命令

```bash
# 查看药品清单
cat medications/medications.csv

# 手动执行检查
cron run --job-id <药品检查 job ID>

# 查看检查报告
cat memory/medication_reports/2026-W12.md

# 备份药品数据
cp medications/medications.csv medications/medications_backup_$(date +%Y%m%d).csv

# 测试模型访问
gog auth list
```

### 常用对话

```
用户：查看药品清单
用户：添加药品 - XXX，保质期 YYYY-MM-DD
用户：删除 med_001
用户：查询感冒药
用户：手动执行药品检查
用户：查看上周药品报告
```
