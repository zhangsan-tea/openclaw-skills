#!/usr/bin/env python3
"""成片音色验收：原片与成片里“同一段话”逐段对比。

用法：
  python audio_qa.py --src 原片.mp3 --out 成片.mp3 --seg 原片起点:成片起点:时长 [--seg ...] [--full]
  例：--seg 2057.9:1335.2:13  （秒）
每段至少 6 秒，三位说话人各取 1–2 段。--full 额外报告整片每 10 秒的限幅负担。
合格阈值（第九期 V0.8 定稿）：句尾回响偏差 ≤ +1.5dB；2–5k、5–10k 偏差 ≤ +2.0dB；70–200Hz ≤ +1.0dB；动态范围偏差 ≥ -4.0dB；任意 10 秒接近满幅 ≤ 1000。
"""
import argparse, subprocess
import numpy as np
FF = '/opt/homebrew/bin/ffmpeg'; SR = 44100
BANDS = [(70, 200), (200, 500), (500, 2000), (2000, 5000), (5000, 10000), (10000, 16000)]
TH = dict(tail=1.5, b25=2.0, b510=2.0, low=1.0, dyn=-4.0, max10s=1000)


def load(f, s=None, d=None):
    a = ['-v', 'error'] + (['-ss', '%.3f' % s, '-t', str(d)] if s is not None else []) + ['-i', f, '-f', 'f32le', '-ar', str(SR), '-']
    y = np.frombuffer(subprocess.run([FF] + a, capture_output=True).stdout, np.float32)
    ch = int(subprocess.run(['/opt/homebrew/bin/ffprobe', '-v', 'error', '-select_streams', 'a:0', '-show_entries', 'stream=channels',
                             '-of', 'csv=p=0', f], capture_output=True, text=True).stdout.strip() or 1)
    return y.reshape(-1, ch)[:, 0] if ch > 1 else y   # 取单个声道的真实电平（不下混）


def analyze(y):
    y = y - y.mean(); n = 2048; fr = np.fft.rfftfreq(n, 1 / SR); W = np.hanning(n)
    F = np.array([np.abs(np.fft.rfft(y[i:i + n] * W)) ** 2 for i in range(0, len(y) - n, n // 2)])
    lv = 10 * np.log10(F.sum(1) + 1e-12); P = F[lv > np.percentile(lv, 45)].mean(0)
    tot = P[(fr > 70) & (fr < 16000)].sum()
    b = [10 * np.log10(P[(fr >= a) & (fr < c)].sum() / tot) for a, c in BANDS]
    w = int(0.01 * SR); m = len(y) // w; e = 20 * np.log10(np.sqrt((y[:m * w].reshape(m, w) ** 2).mean(1)) + 1e-9)
    sp = e > np.percentile(e, 60); tails = [e[i + 4:i + 20].mean() - e[i - 10:i].mean()
                                           for i in range(10, m - 20) if sp[i] and not sp[i + 1] and sp[i - 10:i].all()]
    return dict(bands=b, tail=float(np.median(tails)) if tails else float('nan'),
                dyn=float(np.percentile(e, 95) - np.percentile(e, 15)))


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--src', required=True); ap.add_argument('--out', required=True)
    ap.add_argument('--seg', action='append', required=True); ap.add_argument('--full', action='store_true')
    a = ap.parse_args(); dev = []
    print('段 | 2-5k偏差 5-10k偏差 低频偏差 | 回响偏差 | 动态偏差')
    for s in a.seg:
        so, sn, d = map(float, s.split(':'))
        o = analyze(load(a.src, so, d)); n = analyze(load(a.out, sn, d))
        r = [n['bands'][3] - o['bands'][3], n['bands'][4] - o['bands'][4], n['bands'][0] - o['bands'][0], n['tail'] - o['tail'], n['dyn'] - o['dyn']]
        dev.append(r); print('%s | %+.1f %+.1f %+.1f | %+.1f | %+.1f' % (s, *r))
    m = np.nanmean(dev, 0)
    ok = dict(高频2_5k=m[0] <= TH['b25'], 高频5_10k=m[1] <= TH['b510'], 低频=m[2] <= TH['low'], 回响=m[3] <= TH['tail'], 动态=m[4] >= TH['dyn'])
    print('平均 | %+.1f %+.1f %+.1f | %+.1f | %+.1f' % tuple(m)); print('判定', {k: ('合格' if v else '不合格') for k, v in ok.items()})
    if a.full:
        y = load(a.out); per = 10 * SR
        c = np.array([(np.abs(y[i:i + per]) > 0.75).sum() for i in range(0, len(y) - per, per)])
        print('整片每 10 秒接近满幅：中位 %d，最多 %d（%d:%02d）→ %s' % (np.median(c), c.max(), np.argmax(c) * 10 // 60, np.argmax(c) * 10 % 60,
              '合格' if c.max() <= TH['max10s'] else '不合格'))
