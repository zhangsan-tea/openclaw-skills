#!/usr/bin/env python3
"""
静心茶海报 · 背景照片判重工具

用途：在生成新批次金句卡前，确认所选背景照片既没跟历史批次撞车，也没在批内重复。
     以及从未使用过的照片池里列出可用候选。

铁律：判重按图像内容（dhash），不按文件名 —— photos/ 里存在 IMG 与 UUID 两套命名的
     同一批照片副本，按文件名筛选必然选出"以前用过的图"。

用法：
    # 1. 检查某批次 HTML 的照片是否撞历史
    python photo_dupe_check.py check "静心茶金句卡-9月版.html"

    # 2. 列出可用候选（未被历史引用、且彼此不重复），并生成拼图
    python photo_dupe_check.py candidates --top 60

    # 3. 校验一份指定的照片清单（每行一个文件名或 HTML 路径）
    python photo_dupe_check.py verify list.txt

依赖：Pillow
"""
import os, re, sys, glob, json, argparse, itertools

try:
    from PIL import Image, ImageDraw
except ImportError:
    sys.exit("需要 Pillow：/Users/sanzhang/.workbuddy/binaries/python/envs/default/bin/pip install Pillow")

PHOTO_DIR = "photos"
SUBDIR_USED = "已用"          # photos/已用/ 归档目录
QRCODE = "qrcode.jpg"
HAM_THRESHOLD = 10            # 256-bit dhash，>10 视为不同图


# ---------- 基础 ----------
def dhash(path, size=16):
    """256-bit 感知哈希"""
    im = Image.open(path).convert("L").resize((size + 1, size), Image.LANCZOS)
    px = list(im.getdata())
    bits = 0
    for r in range(size):
        row = r * (size + 1)
        for c in range(size):
            bits = (bits << 1) | (1 if px[row + c] < px[row + c + 1] else 0)
    return bits


def hamming(a, b):
    return bin(a ^ b).count("1")


def find_photo(name, base=PHOTO_DIR):
    """在 photos/ 与 photos/已用/ 中定位文件"""
    for sub in ("", SUBDIR_USED):
        p = os.path.join(base, sub, name) if sub else os.path.join(base, name)
        if os.path.isfile(p):
            return p
    return None


def safe_hash(name, base=PHOTO_DIR):
    p = find_photo(name, base)
    if not p:
        return None
    try:
        return dhash(p)
    except Exception:
        return None          # 损坏文件


def photos_in_html(path):
    """按出现顺序返回 HTML 引用的照片（去重、去二维码）"""
    txt = open(path, encoding="utf-8", errors="ignore").read()
    out = []
    for f in re.findall(r'photos/([^"\']+\.(?:jpeg|jpg))', txt):
        if f != QRCODE and f not in out:
            out.append(f)
    return out


def build_used_set(base=PHOTO_DIR, exclude_html=None):
    """已用内容真值集：全部历史 HTML 的引用 + photos/已用/ 归档"""
    used = set()
    for h in sorted(glob.glob("*.html")):
        if exclude_html and os.path.basename(h) == os.path.basename(exclude_html):
            continue
        used.update(f for f in photos_in_html(h) if find_photo(f, base))
    used_dir = os.path.join(base, SUBDIR_USED)
    if os.path.isdir(used_dir):
        used.update(f for f in os.listdir(used_dir)
                    if f.lower().endswith((".jpeg", ".jpg")) and find_photo(f, base))
    return used


def grid(names, out_png, title_fn=None, highlight=None, cols=5, cell=(310, 340), base=PHOTO_DIR):
    """生成带编号的网格拼图，供人工看图复核"""
    highlight = highlight or set()
    canvas = Image.new("RGB", (cols * cell[0], ((len(names) + cols - 1) // cols) * cell[1]), (248, 248, 248))
    d = ImageDraw.Draw(canvas)
    for i, f in enumerate(names):
        x, y = (i % cols) * cell[0], (i // cols) * cell[1]
        p = find_photo(f, base)
        try:
            im = Image.open(p).convert("RGB")
            im.thumbnail((cell[0] - 16, cell[1] - 70))
            canvas.paste(im, (x + 8, y + 56))
        except Exception:
            d.text((x + 10, y + 70), "读取失败", fill=(200, 0, 0))
        col = (200, 30, 30) if (i + 1) in highlight else (60, 120, 60)
        d.rectangle([x + 2, y + 2, x + cell[0] - 2, y + cell[1] - 2], outline=col,
                    width=2 if (i + 1) in highlight else 1)
        d.text((x + 10, y + 8), f"#{i+1}",
               fill=col)
        if title_fn:
            d.text((x + 10, y + 28), title_fn(i)[:26], fill=(80, 80, 80))
    canvas.save(out_png)
    return out_png


# ---------- 子命令 ----------
def cmd_check(args):
    base = args.photo_dir
    target = args.html
    names = photos_in_html(target)
    used = build_used_set(base, exclude_html=target)
    used_h = {f: safe_hash(f, base) for f in used}
    used_h = {f: h for f, h in used_h.items() if h is not None}
    print(f"目标: {target}")
    print(f"本批 {len(names)} 张 / 历史已用 {len(used_h)} 张 (可哈希)\n")
    print(f"=== 与历史批次判重 (dhash 汉明距离, 阈值 >{HAM_THRESHOLD}) ===")
    bad = []
    for i, f in enumerate(names, 1):
        h = safe_hash(f, base)
        if h is None:
            print(f"  {i:2d}. ⚠️  无法读取或缺失  {f}")
            bad.append(i)
            continue
        best = sorted(((hamming(h, hh), g) for g, hh in used_h.items()), key=lambda t: t[0])
        d0, g0 = best[0]
        if d0 <= HAM_THRESHOLD:
            bad.append(i)
            print(f"  {i:2d}. ❌ 撞历史 d={d0:3d}  {f}")
            print(f"           历史: {g0}")
        else:
            print(f"  {i:2d}. ✅ 距历史最近 d={d0:3d}  {f}")
    print(f"\n需替换: {len(bad)} 张 -> {bad}")
    return 0 if not bad else 1


def cmd_verify(args):
    src = args.source
    if src.endswith(".html"):
        names = photos_in_html(src)
        base_excl = src
    else:
        names = [l.strip() for l in open(src, encoding="utf-8") if l.strip() and not l.startswith("#")]
        base_excl = None
    base = args.photo_dir
    used = build_used_set(base, exclude_html=base_excl)
    used_h = {f: safe_hash(f, base) for f in used}
    used_h = {f: h for f, h in used_h.items() if h is not None}
    own = {f: safe_hash(f, base) for f in names}
    ok = True
    print("=== 与历史判重 ===")
    for i, f in enumerate(names, 1):
        if own.get(f) is None:
            print(f"  {i:2d} ⚠️ {f}"); ok = False; continue
        d0 = min((hamming(own[f], x) for x in used_h.values()), default=999)
        if d0 <= HAM_THRESHOLD:
            print(f"  {i:2d} ❌ 撞历史 d={d0}  {f}"); ok = False
        else:
            print(f"  {i:2d} ✅ d={d0:3d}  {f}")
    print("\n=== 批内彼此最近距离（越小越可疑）===")
    pairs = sorted((hamming(own[a], own[b]), i, j)
                   for (i, a), (j, b) in itertools.combinations(enumerate(names, 1), 2)
                   if own.get(a) is not None and own.get(b) is not None)
    for d, i, j in pairs[:8]:
        flag = "  ⚠️ 偏近，需人工看图" if d <= 30 else ""
        print(f"  d={d:3d}  #{i} <-> #{j}{flag}")
    print("\n结论:", "全部通过" if ok else "存在问题")
    return 0 if ok else 1


def cmd_candidates(args):
    base = args.photo_dir
    used = build_used_set(base)
    used_h = [h for h in (safe_hash(f, base) for f in used) if h is not None]
    cands = []
    for f in sorted(os.listdir(base)):
        if not f.lower().endswith((".jpeg", ".jpg")) or f == QRCODE:
            continue
        if not os.path.isfile(os.path.join(base, f)):
            continue
        if f in used:
            continue
        h = safe_hash(f, base)
        if h is None:
            continue
        cands.append((f, h, min((hamming(h, x) for x in used_h), default=999)))
    # 候选之间去重
    sel = []
    for f, h, mind in sorted(cands, key=lambda t: -t[2]):
        if mind <= HAM_THRESHOLD:
            continue
        if all(hamming(h, sh) > HAM_THRESHOLD for _, sh, _ in sel):
            sel.append((f, h, mind))
    print(f"未使用候选 {len(cands)} 张 -> 视觉唯一 {len(sel)} 张")
    for i, (f, _, mind) in enumerate(sel[:args.top], 1):
        print(f"  [{i:3d}] 距历史={mind:3d}  {f}")
    if args.grid:
        grid([f for f, _, _ in sel[:args.top]], args.grid)
        print(f"\n拼图已生成: {args.grid}（务必人工过一遍）")
    return 0


def main():
    ap = argparse.ArgumentParser(description="静心茶海报 · 背景照片判重")
    ap.add_argument("--photo-dir", default=PHOTO_DIR)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p1 = sub.add_parser("check", help="检查某批次 HTML 是否撞历史")
    p1.add_argument("html")
    p1.set_defaults(func=cmd_check)

    p2 = sub.add_parser("candidates", help="列出未使用且视觉唯一的候选")
    p2.add_argument("--top", type=int, default=60)
    p2.add_argument("--grid", help="输出拼图 PNG 路径")
    p2.set_defaults(func=cmd_candidates)

    p3 = sub.add_parser("verify", help="校验指定清单/HTML")
    p3.add_argument("source")
    p3.set_defaults(func=cmd_verify)

    args = ap.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
