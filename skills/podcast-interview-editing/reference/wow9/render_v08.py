# 第九期参考实现（已脱敏：原文引文替换为〔原文略〕，嘉宾称谓替换）。只作结构参考，不能直接运行于新一期。
# V0.5 渲染：语音单独做母带（高通/低通/轻降噪/削峰/慢压/静态增益到 -16 LUFS），音乐处理后再放进占位，最后安全限幅
import json,subprocess,numpy as np,sys,re
FF='/opt/homebrew/bin/ffmpeg'; SR=44100
OUT=sys.argv[1]; MONO=len(sys.argv)>2 and sys.argv[2]=='mono'; BR=sys.argv[3] if len(sys.argv)>3 else '192k'
runs=json.load(open('keep_runs_v06.json')); M=json.load(open('map_v06.json')); mus=set(M['music_before']); EX=M.get('extra',{}); MS=M['msrc']
a=np.frombuffer(subprocess.run([FF,'-v','error','-i','src.mp3','-ac','1','-ar',str(SR),'-f','f32le','-'],capture_output=True).stdout,np.float32)*0.70710678  # 原片双声道相同，取单声道真实电平
F=int(0.02*SR); ramp=np.linspace(0,1,F,dtype=np.float32)
MLEN=int(5.1*SR); PAD=int(0.25*SR)
parts=[]; slots=[]; cur=0
for k,(s,e,_,_) in enumerate(runs):
    if k>0:
        if k in mus:
            slots.append((cur+PAD,k)); n=PAD+MLEN+PAD
        else: n=int(EX.get(str(runs[k][2]),0.12)*SR)
        parts.append(np.zeros(n,np.float32)); cur+=n
    x=a[int(s*SR):int(e*SR)].copy()
    if len(x)>2*F: x[:F]*=ramp; x[-F:]*=ramp[::-1]
    parts.append(x); cur+=len(x)
y=np.concatenate(parts)
def ff(af,x):
    return np.frombuffer(subprocess.run([FF,'-v','error','-f','f32le','-ac','1','-ar',str(SR),'-i','-','-af',af,'-f','f32le','-'],input=x.tobytes(),capture_output=True).stdout,np.float32)
def lufs_mono(x):
    o=subprocess.run([FF,'-hide_banner','-f','f32le','-ac','1','-ar',str(SR),'-i','-','-af','ebur128','-f','null','-'],input=x.tobytes(),capture_output=True).stderr.decode()
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS',o)[-1])
CHAIN=('highpass=f=70,volume=8dB,'   # V0.8 轻处理：无降噪、无低通，只削尖峰＋很轻的慢压，保留原声音色
       'acompressor=detection=peak:threshold=-16dB:ratio=4:attack=1:release=80:knee=6,'
       'acompressor=detection=rms:threshold=-26dB:ratio=1.6:attack=30:release=600:knee=8')
z=ff(CHAIN,y).copy(); assert abs(len(z)-len(y))<SR, (len(z),len(y))
z=z[:len(y)] if len(z)>=len(y) else np.pad(z,(0,len(y)-len(z)))
I=lufs_mono(z); TGT=-19.0   # 单声道 -19 = 双声道成片 -16 LUFS
z*=10**((TGT-I)/20)
# 音乐：每处取不同乐句，渐入 0.25s / 渐出 1.8s，音量比语音有声部分低 6dB
def act_rms(x):
    f=x[:len(x)//4410*4410].reshape(-1,4410); r=np.sqrt((f**2).mean(1)); r=r[r>np.percentile(r,40)]; return np.sqrt((r**2).mean())
sp=act_rms(z[int(600*SR):int(1800*SR)])
env=np.ones(MLEN,np.float32); fi=int(0.25*SR); fo=int(1.8*SR); env[:fi]=np.linspace(0,1,fi); env[-fo:]=np.cos(np.linspace(0,np.pi/2,fo))**2
for st,k in slots:
    m=np.frombuffer(subprocess.run([FF,'-v','error','-ss',str(MS[str(k)]),'-t','5.1','-i','music/satie_gymnopedie1_musopen_PD.ogg','-ac','1','-ar',str(SR),'-f','f32le','-'],capture_output=True).stdout,np.float32)[:MLEN].copy()
    m=np.pad(m,(0,MLEN-len(m)))*env; m*=(sp/act_rms(m))*10**(-6/20)
    z[st:st+MLEN]+=m
# V0.8：前面接开场金句（A跳切V2），与正片间留 0.3s
CO=np.load('coldopen/coldopen_A跳切V2_v08.npy'); z=np.concatenate([CO,np.zeros(int(0.3*SR),np.float32),z]); print('开场 %.1fs + 0.3s 后接正片'%(len(CO)/SR))
pk_before=np.abs(z).max()
st2=(z[:,None] if MONO else np.repeat(z[:,None],2,axis=1)).astype(np.float32); NC='1' if MONO else '2'
subprocess.run([FF,'-y','-v','error','-f','f32le','-ac',NC,'-ar',str(SR),'-i','-',
                '-af','alimiter=limit=0.80:attack=3:release=80:level=false:latency=1',
                '-c:a','libmp3lame','-b:a',BR,OUT],input=st2.tobytes(),check=True)
print('时长 %.1fs | 母带前 I(单) %.1f → 目标 %.1f | 限幅前峰值 %.2f（>0.84 的样本 %d）'%(len(z)/SR,I,TGT,pk_before,(np.abs(z)>0.84).sum()))
