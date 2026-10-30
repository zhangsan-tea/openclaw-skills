# 第九期参考实现（已脱敏：原文引文替换为〔原文略〕，嘉宾称谓替换）。只作结构参考，不能直接运行于新一期。
import json,subprocess,mlx_whisper,numpy as np,difflib
exec(open('align_cut.py').read().split("asr=json.load")[0])
MODEL='/Users/sanzhang/.cache/wow9-whisper-turbo'
L=json.load(open('lines_v02.json')); runs=json.load(open('keep_runs_v06.json')); M=json.load(open('map_v06.json')); pos=M['pos']; mus=set(M['music_before'])
R=[]
for li,x in enumerate(L):
    for txt,st in x['segs']:
        for c in norm(txt): R.append(c)
y=np.frombuffer(subprocess.run(['/opt/homebrew/bin/ffmpeg','-v','error','-i','/Users/sanzhang/Downloads/WOW时刻第九期_剪辑工作/WOW时刻第九期_V0.6粗剪.mp3','-ac','1','-ar','16000','-f','f32le','-'],capture_output=True).stdout,np.float32)
def tr(a,b):
    return mlx_whisper.transcribe(y[int(a*16000):int(b*16000)],path_or_hf_repo=MODEL,language='zh',initial_prompt='以下是简体中文。')['text'].strip()
def lm(e,g): return difflib.SequenceMatcher(None,e,g).find_longest_match(0,len(e),0,len(g)).size
rows=[]
for k in range(1,len(runs)):
    el=''.join(R[max(runs[k-1][3]-7,0):runs[k-1][3]+1]); er=''.join(R[runs[k][2]:runs[k][2]+7])
    j=pos[k]
    if k in mus:
        gl=''.join(norm(tr(pos[k]-M['mdur']-3.5,pos[k]-M['mdur']))); gr=''.join(norm(tr(j,j+3.5)))
    else:
        g=''.join(norm(tr(j-3.5,j+3.5))); gl=gr=g
    ok=lm(el,gl)>=3 and lm(er,gr)>=3
    rows.append(dict(k=k,new=hms(j),cut=round(runs[k][0]-runs[k-1][1],1),exp=el+'‖'+er,got=gl if gl==gr else gl+' / '+gr,ok=ok,music=k in mus))
    print(k,'OK' if ok else '待查',hms(j),el,'‖',er,'|',(gl if gl==gr else gl+' / '+gr)[:50],flush=True)
json.dump(rows,open('junction_qa_v06.json','w'),ensure_ascii=False)
print('通过',sum(r['ok'] for r in rows),'/',len(rows))
