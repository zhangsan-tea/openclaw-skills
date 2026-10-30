# 第九期参考实现（已脱敏：原文引文替换为〔原文略〕，嘉宾称谓替换）。只作结构参考，不能直接运行于新一期。
# 把原始逐字稿 452 行 + 台本(保留行/删除线/✂区间) 合成"逐行状态表"，叠加 V0.2 决策
import zipfile,re,json
def ts(s):
    h,m,x=map(int,s.split(':')); return h*3600+m*60+x
raw=[]
for l in open('raw.txt').read().splitlines():
    m=re.match(r'(.*?)\((\d\d:\d\d:\d\d)\):\s*(.*)',l)
    if m: raw.append(dict(spk=m.group(1),t=ts(m.group(2)),text=m.group(3)))
x=zipfile.ZipFile('script.docx').read('word/document.xml').decode()
script={}
for p in re.findall(r'<w:p[ >].*?</w:p>',x,flags=re.S):
    segs=[]
    for r in re.findall(r'<w:r[ >].*?</w:r>',p,flags=re.S):
        t=''.join(re.findall(r'<w:t[^>]*>(.*?)</w:t>',r,flags=re.S))
        st='<w:strike' in r and 'w:val="0"' not in r.split('<w:strike')[1][:20]
        segs.append([t,st])
    full=''.join(t for t,_ in segs)
    m=re.match(r'原 (\d\d:\d\d:\d\d)｜新 [\d:]+\u3000(\S+?)：',full)
    if m:
        # 去掉行首“原…｜新…　说话人：”前缀
        pre=len(m.group(0)); out=[];c=0
        for t,s in segs:
            if c+len(t)<=pre: c+=len(t); continue
            if c<pre: t=t[pre-c:]; c=pre
            c+=len(t); out.append([t,s])
        script.setdefault(ts(m.group(1)),[]).append(out)
cuts=[(ts(a),ts(b)) for a,b in re.findall(r'✂ 删除 (\d\d:\d\d:\d\d)–(\d\d:\d\d:\d\d)',open('script.txt').read())]
# ---- V0.2 ----
RESTORE_INLINE={ts('00:21:19'),ts('00:23:01'),ts('01:21:19'),ts('01:33:59')}
RESTORE_CUT={(ts('01:33:09'),ts('01:33:30'))}
DROP=(ts('02:01:20'),ts('02:03:41'))
cuts=[c for c in cuts if c not in RESTORE_CUT]
import difflib
assign={}
for t,groups in script.items():
    idx=[i for i,r in enumerate(raw) if r['t']==t]
    used=set()
    for g in groups:
        gt=''.join(x for x,_ in g)
        best=max((i for i in idx if i not in used),key=lambda i:difflib.SequenceMatcher(None,gt,raw[i]['text']).ratio())
        assign[best]=g; used.add(best)
lines=[];problems=[]
for i,r in enumerate(raw):
    t=r['t']
    if DROP[0]<=t<DROP[1]: st='drop'
    elif i in assign: st='keep'
    elif any(a<=t<b for a,b in cuts) or t<ts('00:00:39'): st='cut'
    elif any(a<=t<b for a,b in RESTORE_CUT): st='keep'
    else: st='?'; problems.append((i,t,r['text'][:30]))
    if st=='keep' and i in assign:
        segs=assign[i]
        if t in RESTORE_INLINE: segs=[[s,False] for s,_ in segs]
    elif st=='keep': segs=[[r['text'],False]]
    else: segs=[[r['text'],True]]
    lines.append(dict(i=i,spk=r['spk'],t=t,status=st,segs=segs))
# 01:29:15 剪掉“怎么收尾？”
for L in lines:
    if L['t']==ts('01:29:15'):
        s0=L['segs'][0][0]; assert s0.startswith('怎么收尾？'),s0[:10]
        L['segs']=[['怎么收尾？',True],[s0[len('怎么收尾？'):],False]]+L['segs'][1:]
dup=[t for t,v in script.items() if len(v)>1]
print('raw',len(raw),'script行',len(script),'同秒多行',dup)
print('未覆盖',problems)
from collections import Counter; print(Counter(l['status'] for l in lines))
json.dump(lines,open('lines_v02.json','w'),ensure_ascii=False,indent=0)
