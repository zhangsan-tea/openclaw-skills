# 第九期参考实现（已脱敏：原文引文替换为〔原文略〕，嘉宾称谓替换）。只作结构参考，不能直接运行于新一期。
# 开场金句 Cold open 渲染：原片切段 → 压长停顿 → 母带链 → 萨蒂钢琴垫底 → 接 V0.6 开头 8 秒
import json,subprocess,numpy as np,sys,re
FF='/opt/homebrew/bin/ffmpeg'; SR=44100
PLANS={
 'A':[('嘉宾','老僧入定',1569.96,1582.05,[],'tight'),
      ('文彬/嘉宾','心跳·泉眼',3784.00,3795.75,[]),
      ('嘉宾','冻土',2057.90,2071.15,[]),
      ('Walker','A口B口C口',4016.25,4024.93,[]),
      ('嘉宾','不往下传',4437.15,4443.98,[]),
      ('文彬','先看见',2255.78,2264.24,[]),
      ('嘉宾','改变也是控制',4820.75,4825.35,[])],
 'B':[('嘉宾','过程',1213.58,1218.55,[]),
      ('嘉宾','片段C',4104.50,4123.35,[]),
      ('Walker','妈妈',2703.38,2714.45,[]),
      ('嘉宾','东西不会被掩盖',3975.35,3985.10,[(3976.70,3979.78)]),
      ('文彬','长教养',3847.81,3851.72,[]),
      ('嘉宾','不往下传',4433.55,4443.98,[])]}
LS=('嘉宾','老僧入定',1569.96,1582.05,[],'tight')
XT=('文彬','心跳·泉眼',3784.00,3795.75,[(3786.25,3787.90)])
DT=('嘉宾','冻土',2057.90,2071.15,[])
SS=('嘉宾','片段C',4104.50,4123.35,[])
AK=('Walker','A口B口C口',4016.25,4024.93,[])
WX=('嘉宾','不往下传',4433.55,4443.98,[])
ZQ=('嘉宾','改变也是控制',4820.75,4825.35,[])
PLANS['A跳切']=[ZQ,XT,SS,LS,AK,DT,WX]
PLANS['A按人']=[LS,DT,SS,ZQ,WX,XT,AK]
WX2=('嘉宾','不往下传',4437.15,4443.98,[])
PLANS['A跳切V2']=[ZQ,XT,LS,AK,DT,WX2]   # 10-30 Lee：删片段C；往下传去掉“当时那个波密老师就说了一个意思”
GAPS={'A跳切V2':1.6}
P=sys.argv[1]; OUT=sys.argv[2]
src=np.frombuffer(subprocess.run([FF,'-v','error','-i','src.mp3','-ac','1','-ar',str(SR),'-f','f32le','-'],capture_output=True).stdout,np.float32)*0.70710678
db=20*np.log10(np.load('rms10ms.npy')+1e-6)
def snap(t,lo,hi):
    a,b=int(round((t+lo)*100)),int(round((t+hi)*100)); w=db[a:b+1]; return (a+int(np.argmin(w)))/100
def compress(x):  # 句内静音 >0.45s 压到 0.35s
    f=int(0.01*SR); n=len(x)//f; e=20*np.log10(np.sqrt((x[:n*f].reshape(n,f)**2).mean(1))+1e-6)
    keep=np.ones(n,bool); i=0
    while i<n:
        if e[i]<-55:
            j=i
            while j<n and e[j]<-55: j+=1
            if j-i>45: keep[i+17:j-18]=False
            i=j
        else: i+=1
    m=np.repeat(keep,f); m=np.r_[m,np.ones(len(x)-len(m),bool)]; return x[m]
F=int(0.015*SR); ramp=np.linspace(0,1,F,dtype=np.float32)
def fade(x):
    x=x.copy()
    if len(x)>2*F: x[:F]*=ramp; x[-F:]*=ramp[::-1]
    return x
LEAD=3.0; GAP=GAPS.get(P,0.6); TAIL=4.0
parts=[np.zeros(int(LEAD*SR),np.float32)]; marks=[]; cur=LEAD
for i,(spk,name,s,e,cuts,*opt) in enumerate(PLANS[P]):
    s2=s if opt else snap(s,-0.10,0.02); e2=snap(e,-0.02,0.10)
    pieces=[]; a=s2
    for c0,c1 in cuts: pieces.append(fade(src[int(a*SR):int(c0*SR)])); a=c1
    pieces.append(fade(src[int(a*SR):int(e2*SR)]))
    seg=compress(np.concatenate(pieces)) if len(pieces)==1 else np.concatenate([compress(p) for p in pieces])
    if i: parts.append(np.zeros(int(GAP*SR),np.float32)); cur+=GAP
    marks.append((spk,name,cur,cur+len(seg)/SR,s2,e2)); parts.append(seg); cur+=len(seg)/SR
parts.append(np.zeros(int(TAIL*SR),np.float32)); speech_end=cur; cur+=TAIL
y=np.concatenate(parts)
def ff(af,x): return np.frombuffer(subprocess.run([FF,'-v','error','-f','f32le','-ac','1','-ar',str(SR),'-i','-','-af',af,'-f','f32le','-'],input=x.tobytes(),capture_output=True).stdout,np.float32).copy()
def lufs(x):
    o=subprocess.run([FF,'-hide_banner','-f','f32le','-ac','1','-ar',str(SR),'-i','-','-af','ebur128','-f','null','-'],input=x.tobytes(),capture_output=True).stderr.decode()
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS',o)[-1])
CHAIN=('highpass=f=70,volume=8dB,'   # V0.8 轻处理：无降噪、无低通，只削尖峰＋很轻的慢压，保留原声音色
       'acompressor=detection=peak:threshold=-16dB:ratio=4:attack=1:release=80:knee=6,'
       'acompressor=detection=rms:threshold=-26dB:ratio=1.6:attack=30:release=600:knee=8')
z=ff(CHAIN,y)[:len(y)]; z=np.pad(z,(0,len(y)-len(z)))
z*=10**((-19.0-lufs(z[int(LEAD*SR):int(speech_end*SR)]))/20)
# 钢琴垫底：开头/结尾 -6dB（同正文转场），人声段 -20dB
N=len(z); m=np.frombuffer(subprocess.run([FF,'-v','error','-ss','1.9','-t','%.2f'%(N/SR+0.5),'-i','music/satie_gymnopedie1_musopen_PD.ogg','-ac','1','-ar',str(SR),'-f','f32le','-'],capture_output=True).stdout,np.float32)[:N].copy()
m=np.pad(m,(0,N-len(m)))
def act(x):
    f=x[:len(x)//4410*4410].reshape(-1,4410); r=np.sqrt((f**2).mean(1)); r=r[r>np.percentile(r,40)]; return np.sqrt((r**2).mean())
sp=act(z[int(LEAD*SR):int(speech_end*SR)]); m*=sp/act(m)
t=np.arange(N)/SR; g=np.full(N,-20.0)
g[t<LEAD-0.6]=-6; sel=(t>=LEAD-0.6)&(t<LEAD+0.2); g[sel]=-6+(-14)*(t[sel]-(LEAD-0.6))/0.8
sel=(t>=speech_end)&(t<speech_end+0.8); g[sel]=-20+14*(t[sel]-speech_end)/0.8; g[t>=speech_end+0.8]=-6
if P in GAPS:   # 句间空档：音乐从 -20 抬到 -12 dB（0.35s 上升 / 0.35s 回落），让每句之间有“断开”感
    for (_,_,_,e0,_,_),(_,_,s1,_,_,_) in zip(marks[:-1],marks[1:]):
        sel=(t>=e0)&(t<s1); tt=t[sel]; up=np.clip((tt-e0)/0.35,0,1); dn=np.clip((s1-tt)/0.35,0,1)
        mr=np.sqrt((m[sel]**2).mean())+1e-9; top=20*np.log10(sp*10**(-12/20)/mr)   # 每个空档音乐都调到比人声低 12dB，钢琴弱奏处也听得见
        top=float(np.clip(top,-20,-4)); g[sel]=-20+(top+20)*np.minimum(up,dn)
env=10**(g/20); fi=int(0.3*SR); env[:fi]*=np.linspace(0,1,fi); fo=int(2.5*SR); env[-fo:]*=np.cos(np.linspace(0,np.pi/2,fo))**2
z=z+m*env
np.save(f'coldopen/coldopen_{P}_v08.npy',z.astype(np.float32))   # 供正片拼接（未限幅、单声道真实电平）
# 接 V0.6 正片开头 8 秒（“大家好，欢迎来到 WOW 时刻”），听交接
v=np.frombuffer(subprocess.run([FF,'-v','error','-t','8','-i','../WOW时刻第九期_V0.6粗剪.mp3','-ac','1','-ar',str(SR),'-f','f32le','-'],capture_output=True).stdout,np.float32)*0.70710678
full=np.concatenate([z,np.zeros(int(0.3*SR),np.float32),v]).astype(np.float32)
subprocess.run([FF,'-y','-v','error','-f','f32le','-ac','1','-ar',str(SR),'-i','-','-af','alimiter=limit=0.80:attack=3:release=80:level=false:latency=1','-c:a','libmp3lame','-b:a','192k',OUT],input=full.tobytes(),check=True)
json.dump(dict(plan=P,coldopen_len=round(N/SR,1),marks=[dict(spk=a,name=b,start=round(c,1),end=round(d,1),src=[e,f]) for a,b,c,d,e,f in marks]),open(f'coldopen/coldopen_{P}.json','w'),ensure_ascii=False)
print(P,'开场 %.1fs（不含接正片 8s）'%(N/SR))
for a,b,c,d,e,f in marks: print('  %4.1f–%4.1f  %-8s %s'%(c,d,a,b))
