# 第九期参考实现（已脱敏：原文引文替换为〔原文略〕，嘉宾称谓替换）。只作结构参考，不能直接运行于新一期。
# V0.6 修订稿：原逐字稿为底；所有剪掉的话=修订删除，作者按“谁剪的”（剪辑V0.2 / 嘉宾 / 赵文彬 / 剪辑V0.3 / 剪辑V0.4 / 剪辑V0.6）
import json,sys
from docx import Document
from docx.shared import Pt,RGBColor
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
exec(open('align_cut.py').read().split("asr=json.load")[0])
OUT=sys.argv[1]; DATE=sys.argv[2]
L=json.load(open('lines_v02.json')); ch=json.load(open('chapters_v02.json')); T=json.load(open('align.json'))['T']
S=json.load(open('state_v06.json')); keep=S['keep']; author=S['author']; hl=S['hl']
_R=''.join(c for x in json.load(open('lines_v02.json')) for t,_ in x['segs'] for c in norm(t))
GOLD=[('〔原文略〕','金句备选'),
      ('〔原文略〕','金句备选'),
      ('〔原文略〕','金句'),
      ('〔原文略〕','金句'),
      ('〔原文略〕','金句'),
      ('〔原文略〕','金句')]
GOLD_NOTES={}
for g,lab in GOLD:
    gg=''.join(norm(g)); assert _R.count(gg)==1,g[:10]; i=_R.find(gg)
    for j in range(i,i+len(gg)): hl[j]=True
    GOLD_NOTES[i]=f'Lee 标注：{lab}（已收入开场金句方案 V4）'
runs=json.load(open('keep_runs_v06.json')); M=json.load(open('map_v06.json')); pos=M['pos']; mus=set(M['music_before'])
SPK={'嘉宾':'嘉宾','walker':'Walker','文彬':'文彬'}
def ts(s): h,m,x=map(int,s.split(':')); return h*3600+m*60+x
def mmss(t): t=int(t); return f'{t//3600:d}:{t%3600//60:02d}:{t%60:02d}' if t>=3600 else f'{t//60:02d}:{t%60:02d}'
j2run={}
for k,(s,e,a,b) in enumerate(runs):
    for j in range(a,b+1): j2run[j]=k
def newt(j): k=j2run[j]; return pos[k]+max(T[j][0]-runs[k][0],0)
R=[]
for li,x in enumerate(L):
    for txt,st in x['segs']:
        for c in norm(txt): R.append(li)
chap_at={}
for c in ch:
    li=[i for i,x in enumerate(L) if x['t']>=ts(c['orig']) and any(keep[j] for j in range(len(R)) if R[j]==i)][0]; chap_at[li]=c
# 批注：V0.3 我的改动 + 文彬原批注 + 转场音乐
EDIT_NOTES={e[3]:(f'剪辑V0.6｜{e[0]}｜{e[2][5:]}' if e[2].startswith('V0.6') else f'剪辑V0.4｜{e[0]}｜{e[2]}') for e in S['edits']}
for i,t in GOLD_NOTES.items(): EDIT_NOTES[i]=(EDIT_NOTES[i]+'；'+t) if i in EDIT_NOTES else t
music_j={runs[k][2]:k for k in mus}
doc=Document()
st=doc.styles['Normal']; st.font.size=Pt(11); st.font.name='PingFang SC'; st.element.rPr.rFonts.set(qn('w:eastAsia'),'PingFang SC')
st.paragraph_format.space_after=Pt(6); st.paragraph_format.line_spacing=1.35
for hn in ['Heading 1','Heading 2']:
    h=doc.styles[hn]; h.font.name='PingFang SC'; h.element.rPr.rFonts.set(qn('w:eastAsia'),'PingFang SC'); h.font.color.rgb=RGBColor(0x1F,0x3A,0x5F)
rid=[1000]
def nid(): rid[0]+=1; return str(rid[0])
def del_wrap(r,au):
    d=OxmlElement('w:del'); d.set(qn('w:id'),nid()); d.set(qn('w:author'),au); d.set(qn('w:date'),DATE)
    r._r.addprevious(d); d.append(r._r)
    for t in r._r.findall(qn('w:t')): t.tag=qn('w:delText')
def del_para_mark(p,au):
    pPr=p._p.get_or_add_pPr(); rPr=pPr.find(qn('w:rPr'))
    if rPr is None: rPr=OxmlElement('w:rPr'); pPr.append(rPr)
    d=OxmlElement('w:del'); d.set(qn('w:id'),nid()); d.set(qn('w:author'),au); d.set(qn('w:date'),DATE); rPr.append(d)
def yellow(r):
    rPr=r._r.get_or_add_rPr(); s=OxmlElement('w:shd'); s.set(qn('w:val'),'clear'); s.set(qn('w:color'),'auto'); s.set(qn('w:fill'),'FFFF00'); rPr.append(s)
def gray(r,sz=8): r.font.size=Pt(sz); r.font.color.rgb=RGBColor(0x99,0x99,0x99)
total=pos[-1]+runs[-1][1]-runs[-1][0]
doc.add_heading('WOW时刻第九期｜V0.6 剪辑稿（修订模式）',level=1)
for s in [f'〔原文略〕',
          '〔原文略〕',
          '〔原文略〕',
          '〔原文略〕',
          '〔原文略〕',
          '〔原文略〕',
          '〔原文略〕']:
    p=doc.add_paragraph(s)
    for r in p.runs: r.font.size=Pt(9.5); r.font.color.rgb=RGBColor(0x55,0x55,0x55)
doc.add_heading('正文',level=1)
j=0; nc=0; pend=[]
for li,x in enumerate(L):
    if li in chap_at:
        c=chap_at[li]; doc.add_heading(c['title'].replace('推荐嘉宾与结束','结束：社会支持系统'),level=2); hp=doc.paragraphs[-1]
    pieces=[]; cur=None; buf=''; first=None
    def flush():
        global buf
        if buf: pieces.append((cur,buf)); buf=''
    for chx in ''.join(t for t,_ in x['segs']):
        if norm(chx):
            if j in EDIT_NOTES: flush(); pieces.append(('N',EDIT_NOTES[j]))
            if j in music_j: flush(); pieces.append(('N',f'剪辑V0.6｜转场音乐：此处前插约 5 秒钢琴（成片 {mmss(pos[music_j[j]]-M["mdur"])}）'))
            key=(keep[j], author[j], hl[j])
            if keep[j] and first is None: first=j
            if cur is not None and key!=cur: flush()
            cur=key; buf+=chx; j+=1
        else: buf+=chx
    flush()
    allcut=first is None
    if li in chap_at and not allcut:
        r=hp.add_run(f'　成片 {mmss(newt(first))}｜原 {chap_at[li]["orig"]}'); gray(r,9)
    p=doc.add_paragraph()
    if not allcut: gray(p.add_run(mmss(newt(first))+'　'))
    spk=p.add_run(SPK.get(x['spk'],x['spk'])+'：'); spk.bold=True
    para_au=None
    if allcut:
        para_au=next(v[0][1] for v in pieces if v[0]!='N' and v[0][1])
        del_wrap(spk,para_au)
    for stt,v in pieces:
        if stt=='N': pend.append(v); continue
        r=p.add_run(v)
        k,au,h=stt
        if h: yellow(r)
        if k:
            for t in pend: doc.add_comment(r,text=t,author='剪辑V0.6',initials='AI'); nc+=1
            pend=[]
        else: del_wrap(r,au)
    if allcut: del_para_mark(p,para_au)
# 文彬原批注：挂在“那次你唱的是什么？”
for p in doc.paragraphs:
    if '那次你唱的是什么' in p.text:
        rr=[r for r in p.runs if '那次你唱的是什么' in r.text][0]
        doc.add_comment(rr,text='〔原文略〕',author='赵文彬',initials='赵'); nc+=1; break
s=doc.settings.element; tr=OxmlElement('w:trackRevisions'); s.find(qn('w:defaultTabStop')).addprevious(tr)
doc.save(OUT); print('comments',nc,'revisions',rid[0]-1000,'成片',mmss(total))
