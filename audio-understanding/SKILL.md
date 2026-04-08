# Audio Understanding Skill

## 功能描述
提供多维度的声音理解能力，包括：
- 音乐识别（听歌识曲）
- 声音情感分析  
- 音频内容理解
- 语音特征提取
- 环境声音识别

## 支持的模型
- **OpenAI GPT-4o**: 支持音频+文本多模态输入
- **Google Gemini 2.5+**: 支持音频理解
- **Claude Sonnet/Opus**: 支持音频输入（需验证）

## 使用方式
```javascript
// 音频文件路径 + 分析提示
const result = await audioAnalysis(audioPath, "分析这段音乐的情感和风格");
```

## 应用场景
- 音乐识别和推荐
- 语音情感分析  
- 健康声音监测（咳嗽、呼吸等）
- 会议录音分析
- 环境声音识别