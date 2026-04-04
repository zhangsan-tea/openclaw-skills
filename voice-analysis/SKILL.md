# SKILL: 语音深度分析与歌曲识别

**版本**：v2.0（2026-03-23）
**作者**：觉醒教练 × lee
**适用**：所有助手（通用技能）

---

## 用途

当用户发送语音消息时，自动执行多维分析：
- 文字转录
- 情感状态与语气
- 内心状态推断
- 旋律/哼唱识别
- **专业歌曲识别**（ACRCloud，准确率极高）

适用场景：教练对话、心理咨询、日常感悟记录、歌曲日记。

---

## 快速使用（推荐流程）

```python
import requests, base64, hashlib, hmac as hmac_lib, time, json
import urllib3; urllib3.disable_warnings()

audio_path = "<AUDIO_FILE_PATH>"

# ====== 第一步：ACRCloud 哼唱识曲 ======
# 从 OpenClaw workspace 的 memory 目录读取 API keys
import os
workspace_path = os.environ.get('OPENCLAW_WORKSPACE', os.path.expanduser('~/.openclaw/workspace-commander'))
api_keys_path = os.path.join(workspace_path, 'memory', 'api_keys.json')

with open(api_keys_path) as f:
    keys = json.load(f)['acrcloud']

access_key = keys['access_key']
access_secret = keys['access_secret']  # 注意：<O_OR_0_NOTE> 是两个大写字母O，非数字0
host = keys['host']

timestamp = str(int(time.time()))
string_to_sign = "\n".join(["POST", "/v1/identify", access_key, "audio", "1", timestamp])
signature = base64.b64encode(
    hmac_lib.new(access_secret.encode('ascii'), string_to_sign.encode('ascii'), digestmod=hashlib.sha1).digest()
).decode('ascii')

with open(audio_path, 'rb') as f:
    audio_data = f.read()

files = [('sample', ('audio.ogg', audio_data, 'audio/ogg'))]
data = {
    'access_key': access_key,
    'sample_bytes': str(len(audio_data)),
    'timestamp': timestamp,
    'signature': signature,
    'data_type': 'audio',
    'signature_version': '1'
}

resp = requests.post(f'https://{host}/v1/identify', files=files, data=data, timeout=15)
acr_result = resp.json()

# 提取识别结果
songs = []
for item in acr_result.get('metadata', {}).get('humming', []):
    songs.append({
        'title': item.get('title'),
        'artists': [a['name'] for a in item.get('artists', [])],
        'score': item.get('score'),
        'release_date': item.get('release_date', '')
    })

print("=== ACRCloud 哼唱识别 ===")
for s in songs:
    print(f"歌名: {s['title']} | 歌手: {s['artists']} | 置信度: {s['score']}")

# ====== 第二步：Gemini 情感分析 ======
with open(audio_path, 'rb') as f:
    audio_b64 = base64.b64encode(f.read()).decode('utf-8')

import os
ext = os.path.splitext(audio_path)[1].lstrip('.').lower()
fmt_map = {'ogg': 'ogg', 'mp3': 'mp3', 'wav': 'wav', 'm4a': 'mp4', 'opus': 'ogg'}
audio_format = fmt_map.get(ext, 'ogg')

api_key = "<API_KEY>"  # aiberm

payload = {
    "model": "google/gemini-2.5-flash",
    "messages": [{
        "role": "user",
        "content": [
            {"type": "input_audio", "input_audio": {"data": audio_b64, "format": audio_format}},
            {"type": "text", "text": "请分析这段语音，用中文简洁回答：1) 是说话还是哼唱；2) 若哼唱有歌词请转录；3) 情感状态和语气；4) 从声音质感推断当下内心状态。"}
        ]
    }]
}

headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
resp = requests.post("https://aiberm.com/v1/chat/completions",
                     headers=headers, json=payload, timeout=120, verify=False)
print("\n=== Gemini 情感分析 ===")
print(resp.json()['choices'][0]['message']['content'])
```

---

## API 配置

### ACRCloud（哼唱识曲）
- **配置文件**：`$OPENCLAW_WORKSPACE/memory/api_keys.json`（默认为 `~/.openclaw/workspace-commander/memory/api_keys.json`）
- **Host**：`<YOUR_ACRCLOUD_HOST>`
- **Access Key**：`<KEY_32_HEX>`
- **注册**：[console.acrcloud.com](https://console.acrcloud.com)（当前为免费试用，14天）
- **重要**：Secret 中 `<O_OR_0_NOTE>` 是两个大写字母 O，不是数字 0，否则报 signature error

### Gemini via aiberm（情感分析）
- **Base URL**：`https://aiberm.com/v1`
- **API Key**：存于 OpenClaw 配置文件中（providers.aiberm.apiKey）
- **模型**：`google/gemini-2.5-flash`（日常），`google/gemini-2.5-pro`（深度）
- **注意**：直连有时不稳定，超时设为 120s，verify=False

---

## 识别策略选择

| 场景 | 推荐方案 | 准确率 |
|------|---------|-------|
| 纯旋律哼唱（无歌词）| ACRCloud | ⭐⭐⭐⭐⭐ |
| 有歌词哼唱 | ACRCloud + Gemini 转录 | ⭐⭐⭐⭐⭐ |
| 情感状态分析 | Gemini 2.5 Flash | ⭐⭐⭐⭐⭐ |
| 说话内容转录 | Gemini（优先）/ Whisper（备用）| ⭐⭐⭐⭐ |
| Gemini 直接猜歌名 | ❌ 不推荐（容易猜错）| ⭐⭐ |

---

## 输出格式模板

```
🎙️ 语音深度分析

🎵 歌曲识别（ACRCloud）
歌名：《XXX》- 歌手（置信度 X.XX）

📝 歌词转录（如有）
[文字内容]

💭 情感状态
[Gemini 分析结果]

🌊 内心状态推断
[深层心理状态]

📖 记录到歌曲日记
路径：<OPENCLAW_WORKSPACE>/memory/songs/歌曲日记.md
```

---

## 验证记录

| 日期 | 音频 | 识别结果 | 置信度 | 是否正确 |
|------|------|---------|-------|--------|
| 2026-03-23 | 驿动的心哼唱 | 驿动的心（陈果版）| 0.96 | ✅ |
| 2026-03-23 | 皇后大道東哼唱 | 皇后大道東（羅大佑）| 0.6 | ✅ |
| 2026-03-23 | 水中花哼唱 | 水中花（郑阳/譚詠麟）| 0.8 | ✅ |
| 2026-03-23 | 唱脸谱哼唱 | 说唱脸谱/唱脸谱（杭天琪）| 0.96 | ✅ |

---

## 赋能其他助手

此 Skill 可赋能所有助手，使用时：
1. 复制上方「快速使用」代码块
2. 替换 `audio_path` 为实际音频文件路径
3. ACRCloud 配置文件路径固定，无需修改
4. 将识别结果追加到对应的歌曲日记或用户档案

**歌曲日记路径**：`$OPENCLAW_WORKSPACE/memory/songs/歌曲日记.md`
