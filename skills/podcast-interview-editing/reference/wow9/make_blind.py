# 第九期参考实现（已脱敏：原文引文替换为〔原文略〕，嘉宾称谓替换）。只作结构参考，不能直接运行于新一期。
# 盲听小样：同一段嘉宾+Walker对话（原片 1:06:55 起 30 秒），V0.4 / V0.7 / 轻处理版，响度对齐后随机命名 A/B/C
import json,subprocess,numpy as np,re,random
FF='/opt/homebrew/bin/ffmpeg'; SR=44100
WIN=(4015.0,30.0)
r4=json.load(open('keep_runs_v04.json')); p4=json.load(open('map_v04.json'))['pos']
r6=json.load(open('keep_runs_v06.json')); p6=json.load(open('map_v06.json'))['pos']
def o2n(t,R,P):
    for (s,e,a,b),p in zip(R,P):
        if s<=t<=e: return p+(t-s)
def dec(args): return np.frombuffer(subprocess.run([FF,'-v','error']+args+['-f','f32le','-'],capture_output=True).stdout,np.float32)
def ff(af,x): return dec(['-f','f32le','-ac','1','-ar',str(SR),'-i','-','-af',af]) if False else np.frombuffer(subprocess.run([FF,'-v','error','-f','f32le','-ac','1','-ar',str(SR),'-i','-','-af',af,'-f','f32le','-'],input=x.astype(np.float32).tobytes(),capture_output=True).stdout,np.float32).copy()
def lufs(x):
    o=subprocess.run([FF,'-hide_banner','-f','f32le','-ac','1','-ar',str(SR),'-i','-','-af','ebur128','-f','null','-'],input=x.astype(np.float32).tobytes(),capture_output=True).stderr.decode()
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS',o)[-1])
# ---- C：轻处理版，按全片计算增益（和正式出片同一做法）----
src=dec(['-i','src.mp3','-ac','1','-ar',str(SR)])*0.70710678
parts=[];pos=[];cur=0
for s,e,_,_ in r6:
    x=src[int(s*SR):int(e*SR)]; pos.append(cur); parts.append(x); parts.append(np.zeros(int(0.12*SR),np.float32)); cur+=len(x)+int(0.12*SR)
y=np.concatenate(parts)
LIGHT=('highpass=f=70,acompressor=detection=peak:threshold=-16dB:ratio=4:attack=1:release=80:knee=6,'
       'acompressor=detection=rms:threshold=-26dB:ratio=1.6:attack=30:release=600:knee=8')   # 轻处理 L3：无降噪、无低通，只削尖峰＋很轻的慢压
z=ff(LIGHT.replace('highpass=f=70,','highpass=f=70,volume=8dB,'),y)[:len(y)]
z*=10**((-19.0-lufs(z))/20)
LIM=0.80
over=np.abs(z)>LIM; print('〔原文略〕'%(over.sum(),over.mean()*100,20*np.log10(np.abs(z).max()/LIM)))
# 刺啦区（原片 4419–4445、4640–4670）限幅负担
def seg_of(t):
    for (s,e,_,_),p in zip(r6,pos):
        if s<=t<=e: return p+int((t-s)*SR)
for a,b in [(4425,4445),(4645,4665)]:
    i=seg_of(a); j=i+int((b-a)*SR); print('  刺啦区 %d–%d：需限幅样本 %d'%(a,b,over[i:j].sum()))
k=seg_of(WIN[0]); C=z[k:k+int(WIN[1]*SR)]
C=ff(f'alimiter=limit={LIM}:attack=3:release=80:level=false:latency=1',C)[:len(C)]
# ---- A/B：直接从成片里截同一段（取单声道真实电平）----
A0=dec(['-ss','%.3f'%o2n(WIN[0],r4,p4),'-t',str(WIN[1]),'-i','../WOW时刻第九期_V0.4粗剪.mp3','-ac','1','-ar',str(SR)])*0.70710678
B0=dec(['-ss','%.3f'%(o2n(WIN[0],r6,p6)+69.8+0.3),'-t',str(WIN[1]),'-i','../WOW时刻第九期_V0.7完整版.mp3','-ac','1','-ar',str(SR)])*0.70710678
SRCW=src[int(WIN[0]*SR):int((WIN[0]+WIN[1])*SR)]
# 对齐检查：三段和原片同一段的相关
def lag(x):
    c=np.correlate(x[SR:3*SR],SRCW[SR-2000:3*SR+2000],'valid'); return np.argmax(c)-2000
print('对齐偏移(样本) V0.4 %d / V0.7 %d / 轻处理 %d'%(lag(A0),lag(B0),lag(C)))
vers={'V0.4':A0,'V0.7':B0,'轻处理':C}
T=-24.0   # 单声道 -21 ≈ 双声道 -18 LUFS，留出余量不削波
out={}
for k,x in vers.items():
    g=T-lufs(x); x=x*10**(g/20); out[k]=x
    print('%-4s 响度调整 %+.1f dB，峰值 %.1f dBFS'%(k,g,20*np.log10(np.abs(x).max())))
labels=['A','B','C']; random.seed(20261030); order=list(vers); random.shuffle(order)
key={}
F=int(0.3*SR); fade=np.ones(len(SRCW),np.float32)
for lab,k in zip(labels,order):
    x=out[k][:len(SRCW)].copy(); x[:F]*=np.linspace(0,1,F); x[-F:]*=np.linspace(1,0,F)
    st=np.repeat(x[:,None],2,axis=1).astype(np.float32)
    subprocess.run([FF,'-y','-v','error','-f','f32le','-ac','2','-ar',str(SR),'-i','-','-c:a','libmp3lame','-b:a','192k',f'/tmp/wow9sp/WOW九期_盲听_{lab}.mp3'],input=st.tobytes(),check=True)
    key[lab]=k
json.dump(dict(window_orig=WIN,key=key,light_chain='volume+'+LIGHT+f'+alimiter {LIM}'),open('blind/答案_先别看.json','w'),ensure_ascii=False,indent=1)
print('已生成 A/B/C')
