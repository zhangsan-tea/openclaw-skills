# Skill 存放和管理规范

## 📁 存放位置

### 本地集中存放位置
- **路径**：`~/.openclaw/skills/`
- **用途**：集中存放所有自定义创建的skill
- **结构**：每个skill一个独立文件夹

### GitHub 仓库存放位置
- **仓库**：`https://github.com/zhangsan-tea/openclaw-skills`
- **用途**：集中管理和分享所有自定义skill
- **访问**：公开仓库，便于分享和协作

## 🔄 标准工作流程

### Skill 创建后的处理步骤

#### 1. 本地保存
```bash
# 创建skill文件夹
mkdir -p ~/.openclaw/skills/[skill-name]

# 复制skill文件到集中存放位置
cp -r [skill-files] ~/.openclaw/skills/[skill-name]/
```

#### 2. GitHub 推送
```bash
# 克隆skills仓库
cd /tmp && git clone https://github.com/zhangsan-tea/openclaw-skills.git

# 复制skill到仓库
cp -r ~/.openclaw/skills/[skill-name] /tmp/openclaw-skills/

# 提交并推送
cd /tmp/openclaw-skills
git add [skill-name]/
git commit -m "feat: add [skill-name] skill"
git push origin main
```

#### 3. 文档更新
- 更新本地的skill索引
- 更新GitHub仓库的README
- 记录skill的用途和特点

## 📋 Skill 文件结构标准

### 必需文件
1. **`SKILL_[skill-name].md`** - 主文档
   - 技能概述
   - 核心规则/方法
   - 使用指南
   - 示例说明

2. **`README.md`** - 使用说明
   - 快速开始指南
   - 文件结构说明
   - 使用方法
   - 效果指标

### 可选文件
3. **示例文件**
   - `示例_[name].md` - 示例文档
   - `示例_[name].docx` - 原始文档
   - 其他相关资源

## 🎯 命名规范

### Skill 文件夹命名
- 使用小写字母和连字符
- 描述性名称，便于理解
- 示例：`weekly-report-editing`、`health-automation`

### Skill 文档命名
- 主文档：`SKILL_[skill-name].md`
- 说明文档：`README.md`
- 示例文档：`示例_[description].[ext]`

## 📊 已创建的 Skills 列表

### 1. weekly-report-editing (周报编辑)
- **创建时间**：2026-03-27
- **用途**：政务类、工作汇报类稿件的精简优化
- **核心**：17条编辑规则
- **文件**：
  - `SKILL_weekly_report_editing.md`
  - `README.md`
  - `示例_团队周报_修订稿.md`
  - `示例_团队周报_原始稿.docx`

## 🔄 后续维护

### 版本更新
1. 更新本地skill文件
2. 更新GitHub仓库
3. 记录版本变化
4. 更新文档说明

### 反馈收集
1. 记录使用效果
2. 收集改进建议
3. 优化规则和方法
4. 迭代更新版本

## 📝 注意事项

1. **必须同步**：每次创建新skill都要同时保存到本地和GitHub
2. **文档完整**：确保包含主文档和README
3. **示例齐全**：提供实际使用示例
4. **命名规范**：遵循统一的命名规范
5. **版本管理**：使用Git进行版本控制

## 🚀 快速命令

### 创建新skill的完整命令
```bash
# 1. 创建本地文件夹
mkdir -p ~/.openclaw/skills/[skill-name]

# 2. 复制文件
cp [skill-files] ~/.openclaw/skills/[skill-name]/

# 3. 克隆GitHub仓库
cd /tmp && git clone https://github.com/zhangsan-tea/openclaw-skills.git

# 4. 复制到仓库
cp -r ~/.openclaw/skills/[skill-name] /tmp/openclaw-skills/

# 5. 提交推送
cd /tmp/openclaw-skills
git add [skill-name]/
git commit -m "feat: add [skill-name] skill"
git push origin main
```

---

**创建时间**：2026-03-29
**维护者**：OpenClaw Writer Assistant
**用途**：规范skill的存放和管理流程