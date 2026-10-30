#!/usr/bin/env python3
"""V0.8 母带链（播客人声，保留原声音色）。

用法（CLI）：
  python master_chain.py 输入音频 输出.mp3 [--target -16] [--mono] [--bitrate 192k]
用法（函数）：
  from master_chain import master, lufs, limiter_load
  y = master(x, sr)          # x: 单声道 float32，真实电平（双声道相同的源取单声道 ×1，不要用 -ac 1 下混，那样会 ×1.414）

链：highpass 70 → +8dB → 削尖峰(peak -16dB 4:1 1/80ms) → 轻慢压(rms -26dB 1.6:1 30/600ms)
    → 线性增益到单声道 target-3 LUFS（≈双声道 target）→ alimiter 0.80（出文件时）。
不降噪、不低通：降噪和重压缩会抬高房间回响、让声音发粗（第九期 V0.7 的教训）。
"""
import subprocess, re, sys, argparse
import numpy as np

FF = '/opt/homebrew/bin/ffmpeg'
CHAIN = ('highpass=f=70,volume=8dB,'
         'acompressor=detection=peak:threshold=-16dB:ratio=4:attack=1:release=80:knee=6,'
         'acompressor=detection=rms:threshold=-26dB:ratio=1.6:attack=30:release=600:knee=8')
LIMIT = 0.80
LIMITER = f'alimiter=limit={LIMIT}:attack=3:release=80:level=false:latency=1'


def _ff(af, x, sr):
    r = subprocess.run([FF, '-v', 'error', '-f', 'f32le', '-ac', '1', '-ar', str(sr), '-i', '-',
                        '-af', af, '-f', 'f32le', '-'], input=x.astype(np.float32).tobytes(), capture_output=True)
    y = np.frombuffer(r.stdout, np.float32).copy()
    if len(y) == 0:  # 参数越界时 ffmpeg 会静默输出空
        raise RuntimeError('ffmpeg 输出为空：' + r.stderr.decode()[:400])
    return y


def lufs(x, sr):
    o = subprocess.run([FF, '-hide_banner', '-f', 'f32le', '-ac', '1', '-ar', str(sr), '-i', '-',
                        '-af', 'ebur128', '-f', 'null', '-'], input=x.astype(np.float32).tobytes(),
                       capture_output=True).stderr.decode()
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS', o)[-1])


def master(x, sr, target_stereo=-16.0):
    """返回未限幅的单声道信号，已调到 target（双声道等效）。限幅在写文件时做。"""
    y = _ff(CHAIN, x, sr)
    y = y[:len(x)] if len(y) >= len(x) else np.pad(y, (0, len(x) - len(y)))
    return y * 10 ** ((target_stereo - 3.0 - lufs(y, sr)) / 20)


def limiter_load(y, sr, thr=0.75):
    """每 10 秒接近满幅的采样点数。合格：任意 10 秒 ≤ 1000。"""
    per = 10 * sr
    c = np.array([(np.abs(y[i:i + per]) > thr).sum() for i in range(0, max(len(y) - per, 1), per)])
    return dict(total=int((np.abs(y) > LIMIT).sum()), max10s=int(c.max()) if len(c) else 0,
                worst_at_s=int(np.argmax(c) * 10) if len(c) else 0, median10s=float(np.median(c)) if len(c) else 0)


def write(y, sr, out, mono=False, bitrate='192k'):
    st = (y[:, None] if mono else np.repeat(y[:, None], 2, axis=1)).astype(np.float32)
    subprocess.run([FF, '-y', '-v', 'error', '-f', 'f32le', '-ac', '1' if mono else '2', '-ar', str(sr), '-i', '-',
                    '-af', LIMITER, '-c:a', 'libmp3lame', '-b:a', bitrate, out], input=st.tobytes(), check=True)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('src'); ap.add_argument('out')
    ap.add_argument('--target', type=float, default=-16.0)
    ap.add_argument('--mono', action='store_true'); ap.add_argument('--bitrate', default='192k')
    ap.add_argument('--sr', type=int, default=44100)
    a = ap.parse_args()
    raw = subprocess.run([FF, '-v', 'error', '-i', a.src, '-f', 'f32le', '-ar', str(a.sr), '-'], capture_output=True).stdout
    ch = int(subprocess.run(['/opt/homebrew/bin/ffprobe', '-v', 'error', '-select_streams', 'a:0', '-show_entries',
                             'stream=channels', '-of', 'csv=p=0', a.src], capture_output=True, text=True).stdout.strip() or 1)
    x = np.frombuffer(raw, np.float32).reshape(-1, ch)[:, 0].copy()
    y = master(x, a.sr, a.target)
    print('限幅负担', limiter_load(y, a.sr))
    write(y, a.sr, a.out, a.mono, a.bitrate)
    print('已写出', a.out)
