# 第九期参考实现（已脱敏：原文引文替换为〔原文略〕，嘉宾称谓替换）。只作结构参考，不能直接运行于新一期。
# 字级对齐 → 剪点 → 吸附静音 → 拼接
import json,re,difflib,subprocess,numpy as np,zipfile,sys
FF='/opt/homebrew/bin/ffmpeg'
def norm(s): return [c.lower() for c in s if re.match(r'[\u4e00-\u9fffA-Za-z0-9]',c)]
def hms(t,ms=False):
    t=max(t,0); h=int(t//3600); m=int(t%3600//60); s=t%60
    return f"{h:02d}:{m:02d}:{s:06.3f}" if ms else f"{h:02d}:{m:02d}:{int(s):02d}"
asr=json.load(open('asr.json')); lines=json.load(open('lines_v02.json'))
# ASR 字流
A=[]
for sg in asr['segments']:
    for w in sg.get('words',[]):
        cs=norm(w['word']); n=len(cs)
        for k,c in enumerate(cs):
            d=(w['end']-w['start'])/n
            A.append((c,w['start']+k*d,w['start']+(k+1)*d))
# 参考字流
R=[]  # (char, line_idx, keep)
for li,L in enumerate(lines):
    for txt,struck in L['segs']:
        for c in norm(txt): R.append((c,li,L['status']=='keep' and not struck))
print('ASR字',len(A),'参考字',len(R),file=sys.stderr)
# 分块全局对齐：每块按逐字稿行时间截 ASR 窗口，保证单调
END=lines[-1]['t']+140
lt=[L['t'] for L in lines]
match=[None]*len(R)
CH=12  # 每块12行
ai=0
for b in range(0,len(lines),CH):
    e=min(b+CH,len(lines))
    r_idx=[j for j,(c,li,k) in enumerate(R) if b<=li<e]
    if not r_idx: continue
    t1=lt[e] if e<len(lines) else END
    a_idx=[j for j in range(ai,len(A)) if A[j][1]<t1+8]
    if not a_idx: continue
    ra=''.join(R[j][0] for j in r_idx); aa=''.join(A[j][0] for j in a_idx)
    sm=difflib.SequenceMatcher(None,ra,aa,autojunk=False)
    last=None
    for blk in sm.get_matching_blocks():
        if blk.size<2: continue
        for k in range(blk.size): match[r_idx[blk.a+k]]=a_idx[blk.b+k]; last=a_idx[blk.b+k]
    if last is not None: ai=last+1
# 时间：匹配字取 ASR 时间，未匹配插值
T=[None]*len(R)
for j,m in enumerate(match):
    if m is not None: T[j]=(A[m][1],A[m][2])
known=[j for j in range(len(R)) if T[j]]
for j in range(len(R)):
    if T[j] is None:
        import bisect
        p=bisect.bisect_left(known,j)
        lo=known[p-1] if p>0 else None; hi=known[p] if p<len(known) else None
        if lo is None: T[j]=(T[hi][0],T[hi][0])
        elif hi is None: T[j]=(T[lo][1],T[lo][1])
        else:
            f=(j-lo)/(hi-lo); x=T[lo][1]+f*(T[hi][0]-T[lo][1]); T[j]=(x,x)
cov=sum(m is not None for m in match)/len(R)
# 校验：每行首字对齐时间 vs 逐字稿行时间
off=[]
for li,L in enumerate(lines):
    js=[j for j in range(len(R)) if R[j][1]==li and match[j] is not None]
    if js: off.append(T[js[0]][0]-L['t'])
off=np.array(off)
print('对齐覆盖率 %.1f%%  行首偏差中位 %.2fs  |偏差|>5s 的行 %d'%(cov*100,np.median(off),(abs(off)>5).sum()),file=sys.stderr)
json.dump(dict(T=T,match=match),open('align.json','w'))
# 保留段
runs=[];cur=None
for j,(c,li,k) in enumerate(R):
    if k:
        if cur is None: cur=[j,j]
        else: cur[1]=j
    elif cur: runs.append(cur); cur=None
if cur: runs.append(cur)
segs=[[T[a][0],T[b][1],a,b] for a,b in runs]
# 吸附到能量最低点
rms=np.load('rms10ms.npy'); db=20*np.log10(rms+1e-6)
def snap(t,lo,hi):
    a=max(int((t+lo)*100),0); b=min(int((t+hi)*100),len(db)-1)
    if b<=a: return t
    w=db[a:b+1]; mn=w.min()
    cand=np.where(w<=mn+3)[0]  # 最低点附近 3dB 内取离 t 最近的
    k=cand[np.argmin(abs((a+cand)/100-t))]
    return (a+k)/100
out=[]
for s,e,a,b in segs:
    out.append([snap(s,-0.35,0.04),snap(e,-0.04,0.35),a,b])
# 合并：两段间被删的音频 <0.35s（多为插话/重叠），不剪
merged=[]
for x in out:
    if merged and x[0]-merged[-1][1]<0.35: merged[-1][1]=x[1]; merged[-1][3]=x[3]
    else: merged.append(x)
json.dump(merged,open('keep_runs.json','w'))
tot=sum(e-s for s,e,_,_ in merged)
print('保留段',len(merged),'粗剪时长',hms(tot),file=sys.stderr)
