# 第九期参考实现（已脱敏：原文引文替换为〔原文略〕，嘉宾称谓替换）。只作结构参考，不能直接运行于新一期。
import json,subprocess,numpy as np
FF='/opt/homebrew/bin/ffmpeg'; SR=44100
r4=json.load(open('keep_runs_v04.json')); p4=json.load(open('map_v04.json'))['pos']
r6=json.load(open('keep_runs_v06.json')); p6=json.load(open('map_v06.json'))['pos']
OFF7=69.8+0.3
def o2n(t,R,P):
    for (s,e,a,b),p in zip(R,P):
        if s<=t<=e: return p+(t-s)
def ld(f,s,d,k=1.0):
    y=np.frombuffer(subprocess.run([FF,'-v','error','-ss','%.3f'%s,'-t',str(d),'-i',f,'-f','f32le','-'],capture_output=True).stdout,np.float32).reshape(-1,2)[:,0]
    return y*k
V4='../WOW时刻第九期_V0.4粗剪.mp3'; V7='../WOW时刻第九期_V0.7完整版.mp3'
SEG={'嘉宾①':(1569.9,12),'嘉宾②':(2057.9,13),'嘉宾③':(4437.2,6.5),'Walker①':(4016.3,8.5),'Walker②':(2703.4,11),'文彬':(2255.8,8.4)}
def an(y):
    y=y-y.mean(); n=2048; h=n//2
    fr=np.fft.rfftfreq(n,1/SR); W=np.hanning(n)
    F=np.array([np.abs(np.fft.rfft(y[i:i+n]*W))**2 for i in range(0,len(y)-n,h)])
    lv=10*np.log10(F.sum(1)+1e-12); act=lv>np.percentile(lv,45)   # 有声帧
    P=F[act].mean(0)
    bands=[(70,200),(200,500),(500,2000),(2000,5000),(5000,10000),(10000,16000)]
    tot=P[(fr>70)&(fr<16000)].sum()
    b=[10*np.log10(P[(fr>=a)&(fr<c)].sum()/tot) for a,c in bands]
    cen=(P*fr).sum()/P.sum()
    w=int(0.01*SR); m=len(y)//w; e=20*np.log10(np.sqrt((y[:m*w].reshape(m,w)**2).mean(1))+1e-9)
    # 尾音/回响：每个语音段结束后 40–200ms 的平均电平，相对之前 100ms 的电平
    sp=e>np.percentile(e,60); tails=[]
    for i in range(10,m-20):
        if sp[i] and not sp[i+1] and sp[i-10:i].all():
            tails.append(e[i+4:i+20].mean()-e[i-10:i].mean())
    dyn=np.percentile(e,95)-np.percentile(e,15)
    crest=20*np.log10(np.abs(y).max()/np.sqrt((y**2).mean()))
    return b,cen,np.median(tails) if tails else np.nan,dyn,crest
rows=[]
print('列：低频70-200 / 200-500 / 500-2k / 2-5k / 5-10k / 10-16k（占全频段 dB）| 频谱重心 | 尾音衰减 | 动态范围 | 峰均比')
for nm,(s,d) in SEG.items():
    t4=o2n(s,r4,p4); t6=o2n(s,r6,p6)
    for tag,y in [('原片',ld('src.mp3',s,d)),('V0.4',ld(V4,t4,d)),('V0.7',ld(V7,t6+OFF7,d))]:
        b,c,tl,dy,cr=an(y)
        print('%-8s %-4s '%(nm,tag)+' '.join('%6.1f'%x for x in b)+' | %5.0fHz | %6.1f dB | %5.1f dB | %4.1f dB'%(c,tl,dy,cr))
    print()
