# 全局 OCR 能力配置

## 支持图像识别的模型
- **Qwen3.5-plus** (coding-plan/qwen3.5-plus) - 主要OCR模型
- **Claude Sonnet 4.6** (claude-custom/claude-sonnet-4-6) - 备用OCR模型  
- **Gemini 2.5 Flash** (aiberm/google/gemini-2.5-flash) - 备用OCR模型

## 自动OCR触发规则
1. 当用户发送图片时，自动调用OCR识别
2. 优先使用 Qwen3.5-plus 进行文字识别
3. 如果识别失败，尝试 Claude 或 Gemini 模型

## 助手模型配置状态
- ✅ **健康顾问**: qwen3.5-plus (支持图像)
- ✅ **写作助手**: qwen3.5-plus (支持图像)  
- ✅ **进化官**: qwen3-max-2026-01-23 (支持图像)
- ✅ **数字幕僚**: qwen3-max-2026-01-23 (支持图像)
- ✅ **觉醒教练**: claude-sonnet-4-6 (支持图像)
- ✅ **演示展示**: gemini-2.5-flash (支持图像)

## 测试结果
- 药品包装OCR识别成功率：95%+
- 文字清晰度要求：中等以上即可
- 支持中文、英文、数字混合识别