# 第九期参考实现（已脱敏：原文引文替换为〔原文略〕，嘉宾称谓替换）。只作结构参考，不能直接运行于新一期。
# V0.6 剪点：state_v06.json → keep_runs_v06.json + map_v06.json（含转场音乐位置）
import json,numpy as np
exec(open('align_cut.py').read().split("asr=json.load")[0])
S=json.load(open('state_v06.json')); keep=S['keep']; T=json.load(open('align.json'))['T']
L=json.load(open('lines_v02.json')); ch=json.load(open('chapters_v02.json'))
def ts(s): h,m,x=map(int,s.split(':')); return h*3600+m*60+x
R=[]
for li,x in enumerate(L):
    for txt,st in x['segs']:
        for c in norm(txt): R.append(li)
runs=[];cur=None
for j,k in enumerate(keep):
    if k:
        if cur is None: cur=[j,j]
        else: cur[1]=j
    elif cur: runs.append(cur); cur=None
if cur: runs.append(cur)
db=20*np.log10(np.load('rms10ms.npy')+1e-6)
def snap(t,lo,hi):
    a=max(int((t+lo)*100),0); b=min(int((t+hi)*100),len(db)-1)
    w=db[a:b+1]; cand=np.where(w<=w.min()+3)[0]; k=cand[np.argmin(abs((a+cand)/100-t))]; return (a+k)/100
out=[[snap(T[a][0],-0.35,0.04),snap(T[b][1],-0.04,0.35),a,b] for a,b in runs]
merged=[]
for x in out:
    if merged and x[0]-merged[-1][1]<0.35: merged[-1][1]=x[1]; merged[-1][3]=x[3]
    else: merged.append(x)
for r in merged:   # 结尾三人重叠（overrides.json）
    if abs(r[1]-7436.74)<0.3: r[1]=7436.62
    if abs(r[0]-7437.40)<0.3: r[0]=7437.63
for r in merged:   # #26 “雷打不动”起点对齐偏晚（ASR 1261.74 起），手工前移到字前静音
    if abs(r[0]-1262.11)<0.2: r[0]=1261.89
db2=db
def lowest(a,b): w=db2[int(a*100):int(b*100)]; return a+np.argmin(w)/100
for r in merged:   # #29 残留“角度”：下一段从“这是横向分类”开始
    if abs(r[0]-1390.01)<0.3: r[0]=lowest(1390.30,1390.64)
for r in merged:   # 家人句：保留到“跟我说”，从“你救的是你自己”接上
    if abs(r[1]-5665.83)<0.3: r[1]=5665.84   # “说”尾与“我”起之间的谷
    if abs(r[0]-5667.11)<0.3: r[0]=5667.47   # “你救的是你自己”起点
# ---- V0.4 手工剪点（Lee 批注）----
EXTRA={}   # 以“run 起始字索引”为键：该接口前的空白秒数
def split_run(j_end,t_end,j_start,t_start,gap=None):
    """〔原文略〕"""
    for k,(s,e,a,b) in enumerate(merged):
        if a<=j_end<b:
            merged[k]=[s,t_end,a,j_end]; merged.insert(k+1,[t_start,e,j_start,b])
            if gap: EXTRA[j_start]=gap
            return
    raise Exception('run not found')
# 批注2“切入”：后一段改从 211.28 起（“我去年…”前的静音谷），接口加 0.45s 空白
for r in merged:
    if r[2]==805:
        r[0]=211.28; EXTRA[805]=0.45
# 批注5“嘶”声：1165.3–1165.95 为吸气声，前段止于“挺有意思”后的静音（1164.90），后段自 1166.03 起
split_run(4953,1164.90,4954,1166.03,gap=0.40)
for r in merged:   # 批注3“去哪儿”：只留第一个“去哪儿”（ASR 364.00–364.70），止于 364.67；其后 364.7–366.1 是同音重复/拖音，Lee 只要三个字
    if r[2]==1392: r[1]=364.67
# 转场音乐：这三章开头之前
# 萨蒂《Gymnopédie No.1》不同乐句起点（秒）：原 3 处沿用 1.9s；V0.5 新增 4 处换乐句，避免重复
MUSIC_SRC={'〔原文略〕':9.0,'回家看啥都不顺眼：愤怒的表达 vs 表达愤怒':49.0,'文彬的身体扫描：心跳像泉眼':89.5,'从我们这代开始，不往下传':108.5,
           '两位主持人的收获':1.9,'三年后的 callback：山西民歌':1.9,'带货时间：ACC、某的下午茶、静心茶':1.9}
MUSIC_CH=list(MUSIC_SRC)
MDUR=5.6  # 音乐 5.1s + 前后各 0.25s 留白
music_before=set(); MSRC={}
for c in ch:
    if c['title'] in MUSIC_CH:
        li=[i for i,x in enumerate(L) if x['t']>=ts(c['orig']) and any(keep[j] for j in range(len(R)) if R[j]==i)][0]
        j0=[j for j in range(len(R)) if R[j]==li and keep[j]][0]
        k=[k for k,(s,e,a,b) in enumerate(merged) if a<=j0<=b][0]
        if merged[k][2]!=j0:  # 章节首字不在段首：从这里切开
            s,e,a,b=merged[k]; t=snap(T[j0][0],-0.35,0.04)
            merged[k]=[s,snap(T[j0-1][1],-0.04,0.35),a,j0-1]; merged.insert(k+1,[t,e,j0,b]); k+=1
        music_before.add(k); MSRC[k]=MUSIC_SRC[c['title']]
# ---- V0.6 音乐接口修正（Lee：转场处吞字）----
MFIX=[('end',1206.22,1206.22,None),      # #28 前段“左右不了的”保持
      ('start',1206.22,1206.45,'〔原文略〕'),
      ('end',4313.93,4311.90,'#65 前段语音止于 4311.66，去掉 2.3 秒空白'),
      ('start',4421.92,4423.20,'#65 后段语音起于 4423.45，去掉 1.5 秒空白'),
      ('start',5164.56,5164.92,'〔原文略〕'),
      ('end',5874.74,5873.35,'#83 前段语音止于 5873.05，去掉 1.4 秒空白'),
      ('start',5970.90,5971.10,'#83 后段起点后移 0.2 秒，去掉空白'),
      ('start',6327.15,6327.22,'〔原文略〕'),
      ('start',6360.81,6361.08,'〔原文略〕')]
MFIX_LOG=[]
for kind,old,new,why in MFIX:
    if why is None: continue
    hit=[r for r in merged if abs((r[1] if kind=='end' else r[0])-old)<0.05]
    assert len(hit)==1,(kind,old,len(hit))
    if kind=='end': hit[0][1]=new
    else: hit[0][0]=new
    MFIX_LOG.append(why)
pos=[];c=0
for k,(s,e,a,b) in enumerate(merged):
    if k>0: c+= MDUR if k in music_before else EXTRA.get(merged[k][2],0.12)
    pos.append(c); c+=e-s
json.dump(merged,open('keep_runs_v06.json','w'))
json.dump(dict(pos=pos,music_before=sorted(music_before),mdur=MDUR,extra={str(k):v for k,v in EXTRA.items()},msrc={str(k):v for k,v in MSRC.items()}),open('map_v06.json','w'))
print('保留段',len(merged),'音乐位置',[hms(pos[k]-MDUR) for k in sorted(music_before)],'总长',hms(c))
