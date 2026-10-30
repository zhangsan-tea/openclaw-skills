# 第九期参考实现（已脱敏：原文引文替换为〔原文略〕，嘉宾称谓替换）。只作结构参考，不能直接运行于新一期。
import json,subprocess,mlx_whisper,numpy as np,difflib
exec(open('align_cut.py').read().split("asr=json.load")[0])
MODEL='/Users/sanzhang/.cache/wow9-whisper-turbo'
L=json.load(open('lines_v02.json')); R=''.join(c for x in L for t,_ in x['segs'] for c in norm(t))
S=json.load(open('state_v06.json')); keep=S['keep']
runs=json.load(open('keep_runs_v06.json')); M=json.load(open('map_v06.json'))
SR=16000
src=np.frombuffer(subprocess.run(['/opt/homebrew/bin/ffmpeg','-v','error','-i','src.mp3','-ac','1','-ar',str(SR),'-f','f32le','-'],capture_output=True).stdout,np.float32)
db=20*np.log10(np.load('rms10ms.npy')+1e-6)
def tr(a,b):
    y=src[int(a*SR):int(b*SR)].copy(); F=320
    y[:F]*=np.linspace(0,1,F); y[-F:]*=np.linspace(1,0,F)
    return ''.join(norm(mlx_whisper.transcribe(np.pad(y,(8000,8000)),path_or_hf_repo=MODEL,language='zh',initial_prompt='以下是简体中文。')['text']))
def mins(a,b):
    i0,i1=int(a*100),int(b*100); w=db[i0:i1]
    c=[ (i0+i)/100 for i in range(2,len(w)-2) if w[i]==w[i-2:i+3].min() and w[i]<-50]
    out=[]
    for x in c:
        if not out or x-out[-1]>=0.12: out.append(x)
    return out[:7]
for k in M['music_before']:
    e=runs[k-1][1]; s=runs[k][0]
    tail=R[runs[k-1][3]-5:runs[k-1][3]+1]; head=R[runs[k][2]:runs[k][2]+6]
    print(flush=True); print(f'〔原文略〕')
    for c in sorted(set([e]+mins(e-0.6,e+0.6))):
        t=tr(c-3.0,c); print('   止%.2f %s %4.0fdB  …%s'%(c,'←当前' if c==e else '     ',db[int(c*100)],t[-14:]))
    for c in sorted(set([s]+mins(s-0.8,s+0.5))):
        t=tr(c,c+3.0); print('   起%.2f %s %4.0fdB  %s…'%(c,'←当前' if c==s else '     ',db[int(c*100)],t[:14]))
