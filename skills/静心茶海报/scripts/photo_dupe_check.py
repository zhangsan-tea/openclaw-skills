#!/usr/bin/env python3
"""
静心茶海报 · 背景照片判重 + 清晰度校验工具

用途：在生成新批次金句卡前，
  1) 确认所选背景照片既没跟历史批次撞车，也没在批内重复（dhash + 汉明距离）；
  2) 确认每张图清晰度足够（导出 750×1334 时图片区 750×494，不得放大）；
  3) 从未使用过的照片池里列出可用候选（已按清晰度过滤 + 视觉去重）。

铁律：
  - 判重按图像内容（dhash），不按文件名 —— photos/ 里存在 IMG 与 UUID 两套命名的
    同一批照片副本，按文件名筛选必然选出"以前用过的图"。
  - 清晰度按导出尺寸判定（宽 ≥750 且 高 ≥494），不是"长边 ≥1000"。
    `_4_5005_c` 后缀一律是缩略图，选图时直接排除。

用法：
    # 1. 检查某批次 HTML：判重 + 清晰度
    python photo_dupe_check.py check "静心茶金句卡-9月版.html"

    # 2. 只查清晰度（附同 UUID 高清版建议）
    python photo_dupe_check.py clarity "静心茶金句卡-9月版.html"

    # 3. 列出可用候选（高清 + 未用 + 视觉唯一），并生成拼图
    python photo_dupe_check.py candidates --top 60 --grid /tmp/cand.png

    # 4. 校验一份指定的照片清单（每行一个文件名，或以 .html 路径传入）
    python photo_dupe_check.py verify list.txt

依赖：Pillow
"""
import os, re, sys, glob, argparse, itertools

try:
    from PIL import Image, ImageDraw, ImageStat, ImageOps
except ImportError:
    sys.exit("需要 Pillow：/Users/sanzhang/.workbuddy/binaries/python/envs/default/bin/pip install Pillow")

PHOTO_DIR = "photos"
SUBDIR_USED = "已用"           # photos/已用/ 归档目录
QRCODE = "qrcode.jpg"
USED_JSON = "used-photos.json"  # 位于 PHOTO_DIR 的上一级（素材根目录）
# 索引/一览类 HTML 必须排除：它们把整池照片都列进 src（如「背景照片一览.html」嵌了 265 张），
# 若当成历史批次扫进去，全池照片都会被判成"已用"，候选永远是 0（2026-09-21 实测踩到）。
INDEX_HTML_PAT = ("一览", "索引", "gallery", "index", "-预览")

HAM_THRESHOLD = 10             # 256-bit dhash，>10 视为不同图
SAME_IMAGE = 12                # <=12 视为"同一张图的不同规格"
EXPORT_W, EXPORT_H = 750, 494  # 图片区导出尺寸（卡高 37% × deviceScaleFactor 2）
MAX_SCALE = 1.15               # 放大幅度容差，超过则必须换图


# ---------- 基础 ----------
def dhash(path, size=16):
    """256-bit 感知哈希。

    关键：先做直方图均衡再取梯度。
    夜景/烛光这类极暗图（均色 < rgb(30,30,30)）原始梯度几乎全为 0，
    哈希位由噪声主导，两张完全不同的暗图也会算出很小的距离（实测 d=27，
    而均衡后为 13、正常不同图为 128+）。均衡可恢复结构、让距离回到可比区间。
    正常光照图均衡前后距离不变（实测同图 0/0、不同图 136/136），无副作用。
    """
    im = Image.open(path)
    im = ImageOps.exif_transpose(im)   # 先按 EXIF 摆正：哈希必须反映"实际渲染的样子"，
                                       # 否则带 Orientation=6 的图算出的哈希与用户看到的画面
                                       # 差 90°，判重会失真
    im = im.convert("L")
    im = ImageOps.equalize(im)
    im = im.resize((size + 1, size), Image.LANCZOS)
    px = im.tobytes()          # 灰度图：每字节一个像素，行优先（避免 getdata 弃用告警）
    bits = 0
    for r in range(size):
        row = r * (size + 1)
        for c in range(size):
            bits = (bits << 1) | (1 if px[row + c] < px[row + c + 1] else 0)
    return bits


def hamming(a, b):
    return bin(a ^ b).count("1")


def photo_uuid(name):
    """归一化"同一张图"的标识：UUID 命名取前 36 字符；IMG_/DSC_ 取去掉 -r90 后缀的 stem"""
    stem = os.path.splitext(os.path.basename(name))[0]
    m = re.match(r"^([0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12})", stem)
    if m:
        return m.group(1)
    return re.sub(r"-(?:r90|rot(?:ated)?\d*)$", "", stem)


def find_photo(name, base=PHOTO_DIR):
    """在 photos/ 与 photos/已用/ 中定位文件"""
    for sub in ("", SUBDIR_USED):
        p = os.path.join(base, sub, name) if sub else os.path.join(base, name)
        if os.path.isfile(p):
            return p
    return None


def size_of(name, base=PHOTO_DIR):
    p = find_photo(name, base)
    if not p:
        return None
    try:
        return Image.open(p).size
    except Exception:
        return None


def scale_needed(size):
    """导出 750×494 所需的放大倍数，<=1 表示无需放大"""
    w, h = size
    return max(EXPORT_W / w, EXPORT_H / h)


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
    for f in re.findall(r'photos/([^"\']+\.(?:jpeg|jpg|JPG|JPEG))', txt):
        if f != QRCODE and f not in out:
            out.append(f)
    return out


def load_blacklist(base=PHOTO_DIR):
    """用户明确指定不再使用的「画面」黑名单 —— 从 used-photos.json 读取。

    注意：退役画面可能只存在于这里（已从 HTML 移除、也不在 photos/已用/ 目录），
    所以 build_used_set 覆盖不到，选候选时必须单独过滤，否则会被重新选中。
    返回 pattern 列表（按文件名前缀匹配，UUID 命名可封禁同图全部规格）。
    """
    p = os.path.join(os.path.dirname(os.path.abspath(base)) or ".", USED_JSON)
    if not os.path.exists(p):
        return []
    try:
        import json
        d = json.load(open(p, encoding="utf-8"))
    except Exception:
        return []
    bl = d.get("黑名单")
    if isinstance(bl, dict):
        bl = bl.get("items", [])
    if not isinstance(bl, list):
        return []
    out = []
    for it in bl:
        if isinstance(it, dict) and it.get("pattern"):
            out.append(it["pattern"])
        elif isinstance(it, str):
            out.append(it)
    return out


def build_used_set(base=PHOTO_DIR, exclude_html=None):
    """已用内容真值集：全部历史 HTML 的引用 + photos/已用/ 归档

    exclude_html 可传单个文件名或文件名列表 —— 同一批次的多个 HTML
    （如「9月版.html」与「9月版-双语.html」共用同一批图）必须一并排除，
    否则同批图会被自己的兄弟 HTML 判成「撞历史 d=0」（2026-09-21 实测踩到）。

    另外恒定跳过 INDEX_HTML_PAT（一览/索引/预览页）—— 它们不是卡片批次，
    却把整池照片写进了 src，扫进去会让全池误判为已用。
    """
    if not exclude_html:
        excl = set()
    elif isinstance(exclude_html, str):
        excl = {os.path.basename(exclude_html)}
    else:
        excl = {os.path.basename(x) for x in exclude_html}
    used = set()
    for h in sorted(glob.glob("*.html")):
        b = os.path.basename(h)
        if b in excl or any(p in b for p in INDEX_HTML_PAT):
            continue
        used.update(f for f in photos_in_html(h) if find_photo(f, base))
    used_dir = os.path.join(base, SUBDIR_USED)
    if os.path.isdir(used_dir):
        used.update(f for f in os.listdir(used_dir)
                    if f.lower().endswith((".jpeg", ".jpg")) and find_photo(f, base))
    return used


def all_photos(base=PHOTO_DIR, include_used_dir=False):
    out = [f for f in sorted(os.listdir(base))
           if f.lower().endswith((".jpeg", ".jpg")) and f != QRCODE
           and os.path.isfile(os.path.join(base, f))]
    if include_used_dir:
        ud = os.path.join(base, SUBDIR_USED)
        if os.path.isdir(ud):
            out += [f for f in sorted(os.listdir(ud))
                    if f.lower().endswith((".jpeg", ".jpg"))]
    return out


def best_by_uuid(base=PHOTO_DIR):
    """同 UUID 分组，返回 {uuid: (最高清文件名, 尺寸)}（用于把缩略图升级为同图高清版）"""
    best = {}
    for f in all_photos(base, include_used_dir=True):
        sz = size_of(f, base)
        if not sz:
            continue
        u = photo_uuid(f)
        if u not in best or max(sz) > max(best[u][1]):
            best[u] = (f, sz)
    return best


def top_color(name, base=PHOTO_DIR, frac=0.10):
    """取图顶部条带均色，用于复核卡片渐隐过渡色是否匹配"""
    p = find_photo(name, base)
    im = Image.open(p).convert("RGB")
    w, h = im.size
    band = im.crop((0, 0, w, max(1, int(h * frac))))
    r, g, b = (int(x) for x in ImageStat.Stat(band).mean)
    return "#%02x%02x%02x" % (r, g, b)


def grid(names, out_png, title_fn=None, highlight=None, cols=5, cell=(310, 340),
         base=PHOTO_DIR, crop_ratio=None):
    """生成带编号的网格拼图，供人工看图复核。
       crop_ratio=(w,h) 时按该比例做 cover 裁切（模拟卡片图片区实际入画效果）"""
    highlight = highlight or set()
    canvas = Image.new("RGB", (cols * cell[0], ((len(names) + cols - 1) // cols) * cell[1]), (248, 248, 248))
    d = ImageDraw.Draw(canvas)
    for i, f in enumerate(names):
        x, y = (i % cols) * cell[0], (i // cols) * cell[1]
        p = find_photo(f, base)
        try:
            im = Image.open(p).convert("RGB")
            if crop_ratio:
                rw, rh = crop_ratio
                w, h = im.size
                s = max(rw / w, rh / h)
                im = im.resize((max(1, int(w * s)), max(1, int(h * s))), Image.LANCZOS)
                nw, nh = im.size
                im = im.crop(((nw - rw) // 2, (nh - rh) // 2,
                              (nw - rw) // 2 + rw, (nh - rh) // 2 + rh))
            im.thumbnail((cell[0] - 16, cell[1] - 70))
            canvas.paste(im, (x + 8, y + 56))
        except Exception:
            d.text((x + 10, y + 70), "读取失败", fill=(200, 0, 0))
        col = (200, 30, 30) if (i + 1) in highlight else (60, 120, 60)
        d.rectangle([x + 2, y + 2, x + cell[0] - 2, y + cell[1] - 2], outline=col,
                    width=2 if (i + 1) in highlight else 1)
        d.text((x + 10, y + 8), f"#{i+1}", fill=col)
        if title_fn:
            d.text((x + 10, y + 28), title_fn(i)[:26], fill=(80, 80, 80))
    canvas.save(out_png)
    return out_png


# ---------- 子命令 ----------
def cmd_check(args):
    base, target = args.photo_dir, args.html
    names = photos_in_html(target)
    used = build_used_set(base, exclude_html=target)
    used_h = {f: safe_hash(f, base) for f in used}
    used_h = {f: h for f, h in used_h.items() if h is not None}
    print(f"目标: {target}")
    print(f"本批 {len(names)} 张 / 历史已用 {len(used_h)} 张 (可哈希)\n")

    print(f"=== 1) 清晰度 (导出图片区 {EXPORT_W}×{EXPORT_H}，须 w≥{EXPORT_W} 且 h≥{EXPORT_H}) ===")
    need_fix = []
    for i, f in enumerate(names, 1):
        sz = size_of(f, base)
        if not sz:
            print(f"  {i:2d}. ⚠️  无法读取或缺失  {f}")
            need_fix.append(i)
            continue
        s = scale_needed(sz)
        if s <= 1:
            print(f"  {i:2d}. ✅ {sz[0]}x{sz[1]:<5} 无需放大  {f}")
        else:
            flag = "⚠️ 轻微" if s <= MAX_SCALE else "❌ 必须换"
            if s > MAX_SCALE:
                need_fix.append(i)
            print(f"  {i:2d}. {flag} 需放大 {s:.2f}x  {sz[0]}x{sz[1]:<5} {f}")
            u = photo_uuid(f)
            hi = best_by_uuid(base).get(u)
            if hi and hi[0] != f and max(hi[1]) > max(sz):
                print(f"          同图高清版可用: {hi[0]}  {hi[1][0]}x{hi[1][1]}")

    print(f"\n=== 2) 与历史批次判重 (dhash 汉明距离, 阈值 >{HAM_THRESHOLD}) ===")
    bad = []
    for i, f in enumerate(names, 1):
        h = safe_hash(f, base)
        if h is None:
            print(f"  {i:2d}. ⚠️  无法读取或缺失  {f}")
            if i not in need_fix:
                need_fix.append(i)
            continue
        d0, g0 = sorted(((hamming(h, hh), g) for g, hh in used_h.items()), key=lambda t: t[0])[0]
        if d0 <= HAM_THRESHOLD:
            bad.append(i)
            print(f"  {i:2d}. ❌ 撞历史 d={d0:3d}  {f}\n           历史: {g0}")
        else:
            print(f"  {i:2d}. ✅ 距历史最近 d={d0:3d}  {f}")
    print(f"\n需替换: {len(bad)} 张 -> {bad}")
    print(f"需处理(清晰度/读取): {sorted(set(need_fix))}")
    return 0 if not bad and not need_fix else 1


def cmd_clarity(args):
    base, src = args.photo_dir, args.source
    names = photos_in_html(src) if src.endswith(".html") else \
        [l.strip() for l in open(src, encoding="utf-8") if l.strip() and not l.startswith("#")]
    best = best_by_uuid(base)
    print(f"=== 清晰度校验（导出图片区 {EXPORT_W}×{EXPORT_H}）===")
    bad = []
    for i, f in enumerate(names, 1):
        sz = size_of(f, base)
        if not sz:
            print(f"{i:2d}. ⚠️ 读取失败 {f}"); bad.append(i); continue
        s = scale_needed(sz)
        if s <= 1:
            print(f"{i:2d}. ✅ {sz[0]}x{sz[1]:<5} 无需放大  {f}")
        else:
            bad.append(i)
            hi = best.get(photo_uuid(f))
            tip = f" -> 可升级: {hi[0]} ({hi[1][0]}x{hi[1][1]})" if hi and hi[0] != f else " -> 无同图高清版，需换图"
            print(f"{i:2d}. {'⚠️' if s <= MAX_SCALE else '❌'} 需放大 {s:.2f}x  {sz[0]}x{sz[1]:<5} {f}{tip}")
    print(f"\n不达标: {bad if bad else '无'}")
    return 0 if not bad else 1


def cmd_verify(args):
    src = args.source
    if src.endswith(".html"):
        names, base_excl = photos_in_html(src), [src] + list(getattr(args, "exclude", []) or [])
    else:
        names = [l.strip() for l in open(src, encoding="utf-8") if l.strip() and not l.startswith("#")]
        base_excl = list(getattr(args, "exclude", []) or [])
    base = args.photo_dir
    used = build_used_set(base, exclude_html=base_excl)
    used_h = [h for h in (safe_hash(f, base) for f in used) if h is not None]
    own = {f: safe_hash(f, base) for f in names}
    ok = True
    print("=== 清晰度 ===")
    for i, f in enumerate(names, 1):
        sz = size_of(f, base)
        if not sz:
            print(f"  {i:2d} ⚠️ 读取失败 {f}"); ok = False; continue
        s = scale_needed(sz)
        flag = "✅" if s <= 1 else ("⚠️ 需放大%.2fx" % s)
        if s > MAX_SCALE:
            ok = False
        print(f"  {i:2d} {flag}  {sz[0]}x{sz[1]:<5} {f}")
    print("\n=== 与历史判重 ===")
    for i, f in enumerate(names, 1):
        if own.get(f) is None:
            print(f"  {i:2d} ⚠️ {f}"); ok = False; continue
        d0 = min((hamming(own[f], x) for x in used_h), default=999)
        if d0 <= HAM_THRESHOLD:
            print(f"  {i:2d} ❌ 撞历史 d={d0}  {f}"); ok = False
        else:
            print(f"  {i:2d} ✅ d={d0:3d}  {f}")
    print("\n=== 批内彼此最近距离（越小越可疑）===")
    pairs = sorted((hamming(own[a], own[b]), i, j)
                   for (i, a), (j, b) in itertools.combinations(enumerate(names, 1), 2)
                   if own.get(a) is not None and own.get(b) is not None)
    for d, i, j in pairs[:8]:
        print(f"  d={d:3d}  #{i} <-> #{j}" + ("  ⚠️ 偏近，需人工看图" if d <= 30 else ""))
    print("\n结论:", "全部通过" if ok else "存在问题")
    return 0 if ok else 1


def cmd_candidates(args):
    base = args.photo_dir
    used = build_used_set(base)
    used_h = [h for h in (safe_hash(f, base) for f in used) if h is not None]
    best = best_by_uuid(base)          # 同 UUID 只保留最高清的那个，避免缩略图混入
    skip_small = not args.allow_small
    bl = load_blacklist(base)          # 退役画面：只记录在 used-photos.json 里，build_used_set 覆盖不到

    # 批内已保留的图（换其中几张时用），用于同时输出「距批内」距离
    batch_h = []
    if getattr(args, "batch_html", None):
        for f in photos_in_html(args.batch_html):
            h = safe_hash(f, base)
            if h is not None:
                batch_h.append((f, h))

    cands = []
    dropped_small = dropped_used = dropped_bl = 0
    for f in all_photos(base):
        if any(f.startswith(p) for p in bl):     # 用户指定不再使用的画面
            dropped_bl += 1
            continue
        if f in used:
            dropped_used += 1
            continue
        if skip_small:
            sz = size_of(f, base)
            if not sz or scale_needed(sz) > 1:
                dropped_small += 1
                continue
        if best.get(photo_uuid(f), (f,))[0] != f:    # 该 UUID 已有更高清的版本
            continue
        h = safe_hash(f, base)
        if h is None:
            continue
        dh = min((hamming(h, x) for x in used_h), default=999)
        db = min((hamming(h, x) for _, x in batch_h), default=999) if batch_h else 999
        cands.append((f, h, dh, db))

    sel = []
    for f, h, dh, db in sorted(cands, key=lambda t: -min(t[2], t[3])):
        if dh <= HAM_THRESHOLD or (batch_h and db <= HAM_THRESHOLD):
            continue
        if all(hamming(h, sh) > HAM_THRESHOLD for _, sh, _, _ in sel):
            sel.append((f, h, dh, db))

    print(f"扫到 {len(all_photos(base))} 张，已用 {dropped_used} 张，"
          f"黑名单 {dropped_bl} 张，清晰度不足(低清缩略图) {dropped_small} 张")
    print(f"未使用且清晰 {len(cands)} 张 -> 视觉唯一 {len(sel)} 张"
          + (f"（批内参照 {len(batch_h)} 张）\n" if batch_h else "\n"))
    for i, (f, _, dh, db) in enumerate(sel[:args.top], 1):
        sz = size_of(f, base)
        ratio = sz[0] / sz[1]
        orient = "横" if ratio > 1.2 else ("竖" if ratio < 0.85 else "方")
        col = f"距历史={dh:3d} 距批内={db:3d}" if batch_h else f"距历史={dh:3d}"
        print(f"  [{i:3d}] {col}  {sz[0]}x{sz[1]:<5} {orient} {f}")
    if args.grid:
        grid([f for f, _, _, _ in sel[:args.top]], args.grid,
             title_fn=lambda i: f"{size_of(sel[i][0], base)[0]}x{size_of(sel[i][0], base)[1]}",
             crop_ratio=(EXPORT_W, EXPORT_H), cell=(300, 300))
        print(f"\n拼图已生成: {args.grid}（按 {EXPORT_W}×{EXPORT_H} cover 裁切预览，务必人工过一遍）")
    return 0


def main():
    ap = argparse.ArgumentParser(description="静心茶海报 · 背景照片判重 + 清晰度校验")
    ap.add_argument("--photo-dir", default=PHOTO_DIR)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p1 = sub.add_parser("check", help="检查某批次 HTML：清晰度 + 判重")
    p1.add_argument("html")
    p1.set_defaults(func=cmd_check)

    p1b = sub.add_parser("clarity", help="只查清晰度并给出同图高清版建议")
    p1b.add_argument("source", help="HTML 路径或照片清单 txt")
    p1b.set_defaults(func=cmd_clarity)

    p2 = sub.add_parser("candidates", help="列出未使用且清晰的视觉唯一候选")
    p2.add_argument("--top", type=int, default=60)
    p2.add_argument("--grid", help="输出拼图 PNG 路径")
    p2.add_argument("--allow-small", action="store_true", help="允许包含需放大的低清图")
    p2.add_argument("--batch-html", help="本批已保留图的 HTML，用于同时输出「距批内」距离")
    p2.set_defaults(func=cmd_candidates)

    p3 = sub.add_parser("verify", help="校验指定清单/HTML（清晰度 + 判重 + 批内距离）")
    p3.add_argument("source")
    p3.add_argument("--exclude", nargs="*", default=[],
                    help="同批次的兄弟 HTML（共用同一批图），一并从「历史集」中排除")
    p3.set_defaults(func=cmd_verify)

    args = ap.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
