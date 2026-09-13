#!/usr/bin/env python3
"""
静心茶海报 · 导出成品校验工具

用途：批量导出 JPG 后，确认「每张卡片用的确实是它该用的那张背景图」，防止串图 / 空白 / 渲染错图。

判定原理（相对判定，不用绝对阈值）：
  1. 从 HTML 里按出现顺序抽出所有非 qrcode 的图片 src（= 卡 1..N 应有背景）
  2. 从导出目录按文件名排序取出 N 张成品
  3. 对每张成品，裁出「图片区」并按 object-fit: cover 的算法在源图上裁出同一区域
  4. 求成品图区与每一张源图的 dhash 距离：
     - 自身那张必须距离最小
     - 次近距离与自身距离差值 >= 3（留足判定余量）

为什么不用绝对阈值：JPEG 压缩 + 只取局部 + equalize 会让同一张图的距离在 6~24 之间浮动，
绝对阈值（如 <=14）会误报。但「自身 vs 其他图」的差距是数量级的（自身 ~15，其他 ~110），相对判定很稳。

⚠️ 关键前置：必须知道图片区在卡片的「顶部」还是「底部」。
   本项目卡片是 flex-column，DOM 顺序为 text-area(63%) → photo-area(37%)，所以图片在【底部】。
   若把图片区当成顶部去裁，距离会全部飙到 100+，看起来像"整批图全错"，其实是裁错了位置。

用法：
  python3 verify_export.py --html 静心茶金句卡-9月版.html --dir 海报导出 --prefix 202609
  python3 verify_export.py --html X.html --dir out --prefix 202609 --photo bottom --ratio 0.37
"""
import os, re, sys, argparse
from PIL import Image, ImageOps

CARD_W, CARD_H = 750, 1334          # 375x667 @ deviceScaleFactor=2


def dhash(im):
    im = ImageOps.equalize(im.convert("L")).resize((17, 16))
    px = list(im.getdata())
    h = 0
    for r in range(16):
        for c in range(16):
            h = (h << 1) | (1 if px[r * 17 + c] > px[r * 17 + c + 1] else 0)
    return h


def ham(a, b):
    return bin(a ^ b).count("1")


def crop_like_cover(src, area_w, area_h, skip_ratio=0.42):
    """按 object-fit:cover; object-position:center 裁出与卡片图片区对应的区域，并跳过顶部渐隐带"""
    im = ImageOps.exif_transpose(Image.open(src))
    sw, sh = im.size
    sc = max(area_w / sw, area_h / sh)
    nw, nh = sw * sc, sh * sc
    ox, oy = (nw - area_w) / 2, (nh - area_h) / 2
    y0 = int(area_h * skip_ratio)
    box = (ox / sc, (oy + y0) / sc, (ox + area_w) / sc, (oy + area_h) / sc)
    return im.crop(box)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--html", required=True)
    ap.add_argument("--dir", required=True, help="导出目录")
    ap.add_argument("--prefix", default="", help="成品文件名前缀，如 202609")
    ap.add_argument("--photo", default="bottom", choices=["top", "bottom"], help="图片区在卡片的位置")
    ap.add_argument("--ratio", type=float, default=0.37, help="图片区高度占比")
    ap.add_argument("--min-gap", type=int, default=3, help="次近距离与自身距离的最小差值")
    a = ap.parse_args()

    html = open(a.html, encoding="utf-8").read()
    srcs = [x for x in re.findall(r'photos/[^"\')> ]+\.(?:jpg|jpeg|png|JPG|JPEG|PNG)', html)
            if "qrcode" not in x]
    if not srcs:
        print("HTML 里没找到图片引用，检查 --html 与相对路径前缀"); sys.exit(1)

    files = sorted(f for f in os.listdir(a.dir)
                   if f.lower().endswith((".jpg", ".jpeg", ".png")) and f.startswith(a.prefix))
    if len(files) != len(srcs):
        print(f"⚠️ 数量不匹配：HTML 引用 {len(srcs)} 张，目录命中 {len(files)} 张（prefix={a.prefix!r}）")
        print("   若目录里还有其他批次，请用 --prefix 精确限定")

    area_h = int(CARD_H * a.ratio)
    area_w = CARD_W
    y_card = 0 if a.photo == "top" else CARD_H - area_h
    skip = int(area_h * 0.42)

    refs = [dhash(crop_like_cover(s, area_w, area_h)) for s in srcs]

    bad = 0
    n = min(len(files), len(srcs))
    for i in range(n):
        f = files[i]
        p = os.path.join(a.dir, f)
        im = Image.open(p)
        if im.size != (CARD_W, CARD_H):
            print(f"BAD {f} 尺寸 {im.size[0]}x{im.size[1]} ≠ {CARD_W}x{CARD_H}")
            bad += 1
            continue
        cd = dhash(im.crop((0, y_card + skip, CARD_W, y_card + area_h)))
        ds = [ham(cd, r) for r in refs]
        best = min(range(len(ds)), key=lambda k: ds[k])
        second = sorted(ds)[1]
        ok = (best == i) and (second - ds[i] >= a.min_gap)
        if not ok:
            bad += 1
        print(f"{'OK ' if ok else 'BAD'} {f}  self={ds[i]:3d}  best={best+1}(d={ds[best]})  次近={second}")
    print(f"\n校验 {n} 张，异常 {bad} 张")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
