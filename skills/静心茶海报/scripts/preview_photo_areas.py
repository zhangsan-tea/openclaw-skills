#!/usr/bin/env python3
"""按卡片实际渲染效果预览「图片区」——用于全批画面复核（方向/完整度/构图）。

图片区在卡片底部 37%（375×667 ⇒ 375×247），object-fit: cover。
本脚本复现 cover 裁切（含 object-position），拼成带编号的网格 PNG 供人工看图。

用法:
  python preview_photo_areas.py <html> [-o /tmp/areas.png] [--cols 4] [--cellw 340]
    [--sel '#bcard-{i}'] [--count 14]
  # 也可直接给一堆图片路径（不经过 HTML）：
  python preview_photo_areas.py --imgs photos/a.jpeg photos/b.jpeg -o /tmp/x.png
"""
import argparse, os, re, sys
from PIL import Image, ImageOps, ImageDraw, ImageFont

CARD_W, CARD_H = 375, 667
PHOTO_RATIO = 0.37          # 图片区高度占比
AREA_W = CARD_W
AREA_H = int(round(CARD_H * PHOTO_RATIO))   # 247


def parse_object_position(style: str):
    """解析 object-position: center 86% / 50% 50% / left top 等，返回 (x_pct, y_pct) 0~1"""
    if not style:
        return 0.5, 0.5
    m = re.search(r'object-position\s*:\s*([^;]+)', style)
    if not m:
        return 0.5, 0.5
    parts = m.group(1).strip().split()
    def one(tok):
        if tok.endswith('%'):
            return float(tok[:-1]) / 100.0
        if tok in ('left', 'top'):
            return 0.0
        if tok in ('right', 'bottom'):
            return 1.0
        if tok == 'center':
            return 0.5
        try:
            return float(tok)
        except ValueError:
            return 0.5
    if len(parts) == 1:
        return one(parts[0]), 0.5
    return one(parts[0]), one(parts[1])


def cover_crop(im: Image.Image, obj_pos=(0.5, 0.5)) -> Image.Image:
    """复现 CSS object-fit: cover —— 居中裁到 AREA_W×AREA_H 的比例后再等比缩放"""
    w, h = im.size
    target = AREA_W / AREA_H
    if w / h > target:          # 图更宽 → 裁左右
        nw = int(round(h * target))
        x = int(round((w - nw) * obj_pos[0]))
        im = im.crop((x, 0, x + nw, h))
    else:                        # 图更高 → 裁上下
        nh = int(round(w / target))
        y = int(round((h - nh) * obj_pos[1]))
        im = im.crop((0, y, w, y + nh))
    return im.resize((AREA_W, AREA_H), Image.LANCZOS)


def load_entries(html_path, sel_tpl, count):
    html = open(html_path, encoding='utf-8').read()
    base = os.path.dirname(os.path.abspath(html_path))
    entries = []
    if sel_tpl and '{i}' in sel_tpl:
        # 按 id="bcard-N" 分块；count<=0 时自动取 HTML 里最大的 N（避免手动漏传）
        if count <= 0:
            ns = [int(x) for x in re.findall(r'id="%s(\d+)"'
                  % re.escape(sel_tpl.format(i='').lstrip('#').lstrip('.')), html)]
            count = max(ns) if ns else 0
        for i in range(1, count + 1):
            sid = sel_tpl.format(i=i)
            key = sid.lstrip('#').lstrip('.')
            m = re.search(r'id="%s"' % re.escape(key), html)
            if not m:
                continue
            # 从该 id 位置往后找第一个 <img src="photos/...">
            seg = html[m.end(): m.end() + 4000]
            im = re.search(r'<img\s+src="([^"]+)"([^>]*)>', seg)
            if not im:
                continue
            entries.append((i, os.path.join(base, im.group(1)),
                            parse_object_position(im.group(2))))
    else:
        for i, m in enumerate(re.finditer(r'<img\s+src="(photos/[^"]+)"([^>]*)>', html), 1):
            entries.append((i, os.path.join(base, m.group(1)),
                            parse_object_position(m.group(2))))
    return entries


def make_grid(entries, out, cols=4, cellw=340):
    rows = (len(entries) + cols - 1) // cols
    cw = cellw
    ch = int(round(cellw * AREA_H / AREA_W)) + 22
    sheet = Image.new('RGB', (cols * cw, rows * ch), 'white')
    d = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype('/System/Library/Fonts/PingFang.ttc', 15)
    except Exception:
        font = ImageFont.load_default()
    for idx, (i, path, pos) in enumerate(entries):
        r, c = divmod(idx, cols)
        x, y = c * cw, r * ch
        try:
            im = ImageOps.exif_transpose(Image.open(path)).convert('RGB')
            area = cover_crop(im, pos)
            zoom = max(AREA_W / im.size[0], AREA_H / im.size[1])
            ori = Image.open(path).getexif().get(274)
        except Exception as e:
            area = Image.new('RGB', (AREA_W, AREA_H), '#cccccc')
            zoom, ori = -1, None
        area = area.resize((cw, ch - 22), Image.LANCZOS)
        sheet.paste(area, (x, y))
        name = os.path.basename(path)
        short = name if len(name) <= 34 else name[:31] + '...'
        flag = ''
        if zoom > 1.5:
            flag += ' LOW'
        if ori in (5, 6, 7, 8):
            flag += ' EXIF%d' % ori
        d.text((x + 4, y + ch - 19), '%02d %s%s' % (i, short, flag),
               fill=('#c0392b' if flag else '#333333'), font=font)
    sheet.save(out)
    print('saved', out, sheet.size, 'n=%d' % len(entries))
    for i, path, pos in entries:
        try:
            raw = Image.open(path)
            w, h = raw.size
            ori = raw.getexif().get(274)
            z = max(AREA_W / w, AREA_H / h)
            print('  %02d %-62s %5dx%-5d exif=%s zoom=%.2f pos=%s' %
                  (i, os.path.basename(path)[:60], w, h, ori, z, pos))
        except Exception as e:
            print('  %02d ERR %s %s' % (i, path, e))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('html', nargs='?')
    ap.add_argument('--imgs', nargs='*')
    ap.add_argument('-o', '--out', default='/tmp/photo_areas.png')
    ap.add_argument('--cols', type=int, default=4)
    ap.add_argument('--cellw', type=int, default=340)
    ap.add_argument('--sel', default='#bcard-{i}')
    ap.add_argument('--count', type=int, default=0,
                    help='卡片数；0（默认）= 自动取 HTML 中最大的 bcard-N')
    a = ap.parse_args()
    if a.imgs:
        entries = [(i + 1, p, (0.5, 0.5)) for i, p in enumerate(a.imgs)]
    else:
        entries = load_entries(a.html, a.sel, a.count)
    make_grid(entries, a.out, a.cols, a.cellw)


if __name__ == '__main__':
    main()
