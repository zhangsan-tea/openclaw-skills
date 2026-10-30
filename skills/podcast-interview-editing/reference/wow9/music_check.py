# 第九期参考实现（已脱敏：原文引文替换为〔原文略〕，嘉宾称谓替换）。只作结构参考，不能直接运行于新一期。
import json,subprocess,mlx_whisper,numpy as np,sys
exec(open('align_cut.py').read().split("asr=json.load")[0])
MODEL='/Users/sanzhang/.cache/wow9-whisper-turbo'
TAG=sys.argv[1]; MP3=sys.argv[2]
L=json.load(open('lines_v02.json')); R=''.join(c for x in L for t,_ in x['segs'] for c in norm(t))
runs=json.load(open(f'keep_runs_{TAG}.json')); M=json.load(open(f'map_{TAG}.json')); pos=M['pos']
y=np.frombuffer(subprocess.run(['/opt/homebrew/bin/ffmpeg','-v','error','-i',MP3,'-ac','1','-ar','16000','-f','f32le','-'],capture_output=True).stdout,np.float32)
def tr(a,b): 
    r=mlx_whisper.transcribe(np.pad(y[int(a*16000):int(b*16000)],(8000,8000)),path_or_hf_repo=MODEL,language='zh',initial_prompt='以下是简体中文。',word_timestamps=True)
    return ' '.join(w['word'] for s in r['segments'] for w in s['words'])
for k in M['music_before']:
    pe=pos[k-1]+runs[k-1][1]-runs[k-1][0]; ps=pos[k]
    print(f'#{k} 音乐 {hms(pe)}–{hms(ps)} 原 {runs[k-1][1]:.2f}|{runs[k][0]:.2f}')
    print('  期望前:',R[runs[k-1][3]-12:runs[k-1][3]+1],' 实际前:',tr(pe-4,pe+0.3))
    print('  期望后:',R[runs[k][2]:runs[k][2]+12],' 实际后:',tr(ps-0.3,ps+4))
