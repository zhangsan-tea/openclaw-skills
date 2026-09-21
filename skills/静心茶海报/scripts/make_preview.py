#!/usr/bin/env python3
"""生成自包含预览 HTML：把主 HTML 里所有 src 换成 base64 data URI。

⚠️ 关键坑（2026-09-21 修）：必须 ImageOps.exif_transpose() 先摆正再内嵌。
PIL 的 convert()/save() 会丢掉 EXIF orientation 标记，但像素本身没转 ——
于是带方向标记的图（exif=3/6/8）在预览里会倒着/躺着显示，
而主 HTML 用 Chrome 导出时是对的（Chrome 默认 image-orientation: from-image）。
曾因此误判「卡03/卡06 方向不对」而白换图。

用法:
  python make_preview.py <src.html> [-o <dst.html>]   # 默认 <src>-预览.html
"""
import argparse, base64, io, os, re, sys
from PIL import Image, ImageOps

NO_TRANS = 0


def embed(path, cache, base):
    full = path if os.path.isabs(path) else os.path.join(base, path)
    if full in cache:
        return cache[full]
    im = ImageOps.exif_transpose(Image.open(full)).convert('RGB')   # ① 摆正
    if 'qrcode' in os.path.basename(full):
        im.thumbnail((240, 240), Image.LANCZOS)
        q = 90
    else:
        im.thumbnail((760, 760), Image.LANCZOS)
        q = 82
    buf = io.BytesIO()
    im.save(buf, 'JPEG', quality=q, optimize=True)
    uri = 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()
    cache[full] = uri
    return uri


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('src')
    ap.add_argument('-o', '--out')
    a = ap.parse_args()
    src = os.path.abspath(a.src)
    base = os.path.dirname(src)
    dst = a.out or src.replace('.html', '-预览.html')
    html = open(src, encoding='utf-8').read()
    cache = {}
    out = html
    for s in sorted(set(re.findall(r'src="([^"]+)"', html))):
        if s.startswith('data:'):
            continue
        out = out.replace('src="%s"' % s, 'src="%s"' % embed(s, cache, base))
    left = re.findall(r'src="(?!data:)([^"]+)"', out)
    if left:
        print('⚠️ 仍有外部引用未内嵌:', left, file=sys.stderr)
    open(dst, 'w', encoding='utf-8').write(out)
    print('saved', dst, '%.2f MB' % (os.path.getsize(dst) / 1024 / 1024),
          '| 内嵌 %d 张，残留外部引用 %d' % (len(cache), len(left)))


if __name__ == '__main__':
    main()
