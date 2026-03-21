# 腾讯会议 Skill 配置指南

## 环境变量
需要配置以下环境变量：

- `TENCENT_MEETING_TOKEN`: 腾讯会议Skill的专属Token（从腾讯会议Skill配置页面获取）

## 集成步骤
1. 获取Token：
   - 访问 https://meeting.tencent.com/ai-skill.html
   - 登录腾讯会议账号
   - 复制安装指令和Token

2. 配置到OpenClaw：
   - 将Token设置为环境变量 `TENCENT_MEETING_TOKEN`
   - 或在skill配置中直接引用

3. 重启OpenClaw以加载新skill

## API端点
腾讯会议Skill可能需要调用以下API端点：
- 会议管理API
- 用户日程API  
- 参会统计API
- 录制文件API

具体API详情请参考腾讯会议官方文档。

## 权限要求
- 会议创建/修改/删除权限
- 日程读取权限
- 参会人信息读取权限
- 录制文件访问权限