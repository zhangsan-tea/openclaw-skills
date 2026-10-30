# 第九期参考实现（已脱敏：原文引文替换为〔原文略〕，嘉宾称谓替换）。只作结构参考，不能直接运行于新一期。
import mlx_whisper, json, time
t = time.time()
r = mlx_whisper.transcribe(
    '/tmp/wow9/src.mp3',
    path_or_hf_repo='/tmp/wow9/model',
    language='zh', word_timestamps=True, condition_on_previous_text=False,
    initial_prompt='〔原文略〕',
    verbose=False)
json.dump(r, open('/tmp/wow9/asr.json', 'w'), ensure_ascii=False)
print('done', round(time.time() - t), len(r['segments']))
