#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
静心茶海报背景 · iCloud 照片相簿 → 海报照片池 同步脚本

作用:
  1. 从 macOS「照片」App 的相簿「静心茶海报背景」导出全部图片
  2. 按【内容哈希 md5】与照片池已有照片比对 —— 只入库真正的新照片
     （关键: 不按文件名判重，IMG_xxxx 会撞车）
  3. HEIC/PNG 等统一转 JPEG（Chrome/puppeteer 导出海报不认 HEIC）
  4. 维护 photo-index.json 全量索引，标记每张照片的 未用/已用/黑名单 状态
  5. 输出本次同步报告

用法:
  python3 sync_bg_photos.py              # 从 iCloud 相簿同步（需照片授权）
  python3 sync_bg_photos.py --from-dir X # 从手动导出的文件夹同步（免授权兜底）
  python3 sync_bg_photos.py --dry-run    # 只报告不落盘
  python3 sync_bg_photos.py --rebuild    # 只重建索引，不导入
"""

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import unicodedata
from datetime import datetime

# ---------- 配置 ----------
ALBUM_NAME = "静心茶海报背景"
ASSET_DIR = "/Users/sanzhang/企业云同步盘/海报制作素材"
POOL_DIR = os.path.join(ASSET_DIR, "photos")
USED_DIR = os.path.join(POOL_DIR, "已用")           # 物理隔离区(已用)
INDEX_PATH = os.path.join(ASSET_DIR, "photo-index.json")
USED_JSON = os.path.join(ASSET_DIR, "used-photos.json")
EXPORT_TMP = "/tmp/jxtea_album_export"

IMG_EXT = {".jpg", ".jpeg", ".heic", ".heif", ".png", ".tif", ".tiff", ".webp"}


def log(msg):
    print(msg, flush=True)


def md5_of(path, block=1 << 20):
    h = hashlib.md5()
    with open(path, "rb") as f:
        while True:
            b = f.read(block)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def normalize(name):
    """NFD/NFC 归一，规避 macOS 中文与·字符的存储差异"""
    return unicodedata.normalize("NFC", name)


def sips_size(path):
    try:
        out = subprocess.run(
            ["sips", "-g", "pixelWidth", "-g", "pixelHeight", path],
            capture_output=True, text=True, timeout=30,
        ).stdout
        w = h = None
        for line in out.splitlines():
            if "pixelWidth" in line:
                w = int(line.split(":")[1].strip())
            if "pixelHeight" in line:
                h = int(line.split(":")[1].strip())
        return w, h
    except Exception:
        return None, None


def to_jpeg(src, dst):
    """非 JPEG 统一转 JPEG；已是 JPEG 直接拷贝"""
    ext = os.path.splitext(src)[1].lower()
    if ext in (".jpg", ".jpeg"):
        shutil.copy2(src, dst)
        return True
    r = subprocess.run(
        ["sips", "-s", "format", "jpeg", src, "--out", dst],
        capture_output=True, text=True, timeout=60,
    )
    return r.returncode == 0 and os.path.exists(dst)


def export_album(dest_dir):
    """从照片 App 相簿导出。返回 (ok, message)"""
    os.makedirs(dest_dir, exist_ok=True)
    script = f'''
    tell application "Photos"
        if not (exists album "{ALBUM_NAME}") then
            return "ALBUM_NOT_FOUND"
        end if
        set theItems to every media item of album "{ALBUM_NAME}"
        set n to count of theItems
        if n is 0 then return "EMPTY"
        export theItems to (POSIX file "{dest_dir}")
        return "OK:" & n
    end tell
    '''
    try:
        r = subprocess.run(["osascript", "-e", script], capture_output=True, text=True, timeout=600)
    except Exception as e:
        return False, f"osascript 执行失败: {e}"
    out = (r.stdout or "").strip()
    err = (r.stderr or "").strip()
    if r.returncode != 0 or not out.startswith("OK"):
        if "ALBUM_NOT_FOUND" in out:
            return False, f"相簿「{ALBUM_NAME}」不存在（检查名称是否完全一致）"
        if "EMPTY" in out:
            return False, "相簿为空"
        if "-10004" in err or "权限" in err or "not authorized" in err.lower():
            return False, PERMISSION_HELP
        return False, f"导出失败: {err or out}"
    return True, out


PERMISSION_HELP = """照片访问被系统拒绝（错误 -10004）。需做一次授权（只需一次，之后全自动）:

  1) 系统设置 → 隐私与安全性 → 自动化 → WorkBuddy → 勾选「Photos」
  2) 系统设置 → 隐私与安全性 → 照片   → 允许 WorkBuddy 访问

  若列表里没有 WorkBuddy 条目，或之前误点过「不允许」，先在终端重置该授权记录:
     sudo tccutil reset AppleEvents com.tencent.workbuddy.mac
  重置后重跑本脚本，系统会重新弹窗，点「好」即可。
  （WorkBuddy bundle id: com.tencent.workbuddy.mac）

  备注：直接读照片图库 SQLite 也走同一套 TCC，未授权时同样 PermissionError，绕不开。

  若只想免授权，照片 App 打开相簿 → 全选 → 文件 → 导出 → 导出 N 张照片 → 选文件夹，然后:
    python3 sync_bg_photos.py --from-dir <那个文件夹路径>
"""


def scan_dir(root):
    """收集目录下所有图片文件(排除隐藏)"""
    out = []
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if not d.startswith(".")]
        for f in fn:
            if f.startswith("."):
                continue
            if os.path.splitext(f)[1].lower() in IMG_EXT:
                out.append(os.path.join(dp, f))
    return out


def build_existing_hashes():
    """扫描照片池(顶层 + 已用子目录)，建立 md5 → 相对路径 映射"""
    m = {}
    for base, tag in ((POOL_DIR, "unused"), (USED_DIR, "used")):
        if not os.path.isdir(base):
            continue
        for f in os.listdir(base):
            p = os.path.join(base, f)
            if not os.path.isfile(p):
                continue
            if os.path.splitext(f)[1].lower() not in IMG_EXT:
                continue
            try:
                m.setdefault(md5_of(p), []).append(os.path.join(tag, f) if tag == "used" else f)
            except Exception:
                pass
    return m


def name_in_pool(stem, ext=".jpeg"):
    """生成不冲突的目标文件名，冲突沿用 ' 2' 风格"""
    cand = f"{stem}{ext}"
    if not os.path.exists(os.path.join(POOL_DIR, cand)):
        return cand
    i = 2
    while True:
        cand = f"{stem} {i}{ext}"
        if not os.path.exists(os.path.join(POOL_DIR, cand)):
            return cand
        i += 1


def load_used_state():
    """从 used-photos.json 读取已用集合与黑名单规则"""
    used, black_patterns = set(), []
    if os.path.exists(USED_JSON):
        try:
            j = json.load(open(USED_JSON, encoding="utf-8"))
            for b in j.get("batches", []):
                used.update(b.get("photos", []))
            used.update(j.get("all_used", []))
            early = j.get("早期批次已用")
            if isinstance(early, dict):
                for v in early.values():
                    if isinstance(v, list):
                        used.update(v)
            for it in j.get("黑名单", {}).get("items", []):
                if it.get("pattern"):
                    black_patterns.append(it["pattern"])
                used.update(it.get("photos", []))
        except Exception as e:
            log(f"[警告] used-photos.json 解析失败: {e}")
    return used, black_patterns


def rebuild_index():
    """全量重建 photo-index.json"""
    used_set, black = load_used_state()
    idx = {"说明": "静心茶海报背景照片池全量索引（由 sync_bg_photos.py 自动维护）",
           "生成时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
           "照片池路径": POOL_DIR,
           "photos": []}
    for base, default_status in ((POOL_DIR, "unused"), (USED_DIR, "used")):
        if not os.path.isdir(base):
            continue
        for f in sorted(os.listdir(base)):
            p = os.path.join(base, f)
            if not os.path.isfile(p) or os.path.splitext(f)[1].lower() not in IMG_EXT:
                continue
            nf = normalize(f)
            status = "used" if (default_status == "used" or nf in used_set) else "unused"
            if any(b.lower() in nf.lower() for b in black):
                status = "blacklist"
            w, h = sips_size(p)
            idx["photos"].append({
                "file": f,
                "path": os.path.join(os.path.basename(base) if default_status == "used" else "", f) or f,
                "status": status,
                "width": w, "height": h,
                "bytes": os.path.getsize(p),
                "mtime": datetime.fromtimestamp(os.path.getmtime(p)).strftime("%Y-%m-%d"),
                "md5": md5_of(p),
            })
    json.dump(idx, open(INDEX_PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    n_unused = sum(1 for p in idx["photos"] if p["status"] == "unused")
    n_used = sum(1 for p in idx["photos"] if p["status"] == "used")
    n_bl = sum(1 for p in idx["photos"] if p["status"] == "blacklist")
    log(f"[索引] 已重建 → {INDEX_PATH}")
    log(f"       总计 {len(idx['photos'])} 张 | 未用 {n_unused} | 已用 {n_used} | 黑名单 {n_bl}")
    return idx


GALLERY_PATH = os.path.join(ASSET_DIR, "背景照片一览.html")

GALLERY_TPL = """<!DOCTYPE html><html lang="zh"><head><meta charset="utf-8">
<title>静心茶背景照片一览</title><style>
body{{font-family:-apple-system,"PingFang SC",sans-serif;background:#f7f6f3;color:#2c2a26;
margin:0;padding:28px 32px 60px}}
h1{{font-size:19px;font-weight:600;margin:0 0 4px}}
.meta{{font-size:12.5px;color:#8a8578;margin-bottom:22px}}
.bar{{display:flex;gap:8px;margin-bottom:24px;flex-wrap:wrap}}
.tab{{padding:6px 15px;border:1px solid #ddd9cf;border-radius:999px;font-size:12.5px;
cursor:pointer;background:#fff;color:#6b675d}}
.tab.on{{background:#4a5d4e;color:#fff;border-color:#4a5d4e}}
.tab.on.used{{background:#8a8578;border-color:#8a8578}}
.tab.on.bl{{background:#a5675c;border-color:#a5675c}}
.sec{{display:none}}.sec.on{{display:block}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(158px,1fr));gap:14px}}
.c{{background:#fff;border:1px solid #e8e4da;border-radius:2px;overflow:hidden}}
.c img{{width:100%;height:112px;object-fit:cover;display:block;background:#efece5}}
.c .n{{font-size:10.5px;padding:6px 8px;color:#6b675d;word-break:break-all;line-height:1.35}}
.c .s{{font-size:10px;padding:0 8px 7px;color:#a8a396}}
.note{{font-size:12px;color:#8a8578;margin:0 0 10px}}
</style></head><body>
<h1>静心茶 · 背景照片一览</h1>
<div class="meta">生成时间 {ts} ｜ 照片池：{total} 张 ｜ 未用 {nu} ｜ 已用 {ns} ｜ 退役 {nb}</div>
<div class="bar">
<div class="tab on" data-s="unused">未用 {nu}</div>
<div class="tab" data-s="used">已用 {ns}</div>
<div class="tab" data-s="blacklist">退役/黑名单 {nb}</div>
</div>
{body}
<script>
document.querySelectorAll('.tab').forEach(t=>t.onclick=()=>{{
 document.querySelectorAll('.tab').forEach(x=>x.classList.remove('on'));
 document.querySelectorAll('.sec').forEach(x=>x.classList.remove('on'));
 t.classList.add('on');
 document.querySelector('.sec-'+t.dataset.s+'').classList.add('on');
}});
</script></body></html>
"""


def build_gallery(idx):
    """生成未用/已用/退役三组缩略图一览（图片用相对路径，不内嵌，文件很小）"""
    groups = [("unused", "未用", "可直接用于新批次"),
              ("used", "已用", "已出现在往期海报，复用前先确认"),
              ("blacklist", "退役/黑名单", "用户明确指定不再使用")]
    secs = []
    for key, label, note in groups:
        items = [p for p in idx["photos"] if p["status"] == key]
        cards = []
        for p in items:
            rel = "photos/" + (("已用/" + p["file"]) if p.get("path", "").startswith("已用") else p["file"])
            cards.append(
                f'<div class="c"><img loading="lazy" src="{rel}" alt="">'
                f'<div class="n">{p["file"]}</div>'
                f'<div class="s">{p.get("width") or "?"}×{p.get("height") or "?"} · {p.get("mtime","")}</div></div>'
            )
        secs.append(
            f'<div class="sec sec-{key}"><div class="note">{note}（{len(items)} 张）</div>'
            f'<div class="grid">{"".join(cards) or "<i>无</i>"}</div></div>'
        )
    counts = {k: sum(1 for p in idx["photos"] if p["status"] == k) for k, _, _ in groups}
    html = GALLERY_TPL.format(
        ts=idx["生成时间"], total=len(idx["photos"]),
        nu=counts["unused"], ns=counts["used"], nb=counts["blacklist"],
        body="".join(secs),
    )
    open(GALLERY_PATH, "w", encoding="utf-8").write(html)
    log(f"[一览] 已生成 → {GALLERY_PATH}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--from-dir", help="从手动导出的文件夹导入(免照片授权)")
    ap.add_argument("--dry-run", action="store_true", help="只报告不落盘")
    ap.add_argument("--rebuild", action="store_true", help="只重建索引")
    ap.add_argument("--gallery", action="store_true", help="生成未用/已用一览 HTML")
    args = ap.parse_args()

    if args.rebuild:
        idx = rebuild_index()
        if args.gallery:
            build_gallery(idx)
        return

    # 1. 取源
    if args.from_dir:
        src_dir = os.path.abspath(args.from_dir)
        if not os.path.isdir(src_dir):
            log(f"[错误] 目录不存在: {src_dir}")
            sys.exit(1)
        log(f"[源] 手动导出目录: {src_dir}")
    else:
        log(f"[源] iCloud 照片相簿「{ALBUM_NAME}」")
        if os.path.isdir(EXPORT_TMP):
            shutil.rmtree(EXPORT_TMP)
        ok, msg = export_album(EXPORT_TMP)
        if not ok:
            log(f"[错误] {msg}")
            sys.exit(2)
        src_dir = EXPORT_TMP
        log(f"[源] 导出成功: {msg}")

    files = scan_dir(src_dir)
    log(f"[源] 待处理图片 {len(files)} 张")

    # 2. 现有照片哈希
    existing = build_existing_hashes()
    log(f"[池] 现有照片 {sum(len(v) for v in existing.values())} 张(顶层+已用)")

    # 3. 逐个比对入库
    added, dup, failed = [], [], []
    for src in files:
        try:
            h = md5_of(src)
        except Exception as e:
            failed.append((src, str(e)))
            continue
        if h in existing:
            dup.append((os.path.basename(src), existing[h][0]))
            continue
        stem = normalize(os.path.splitext(os.path.basename(src))[0])
        target = name_in_pool(stem, ".jpeg")
        dst = os.path.join(POOL_DIR, target)
        if not args.dry_run:
            if not to_jpeg(src, dst):
                failed.append((src, "格式转换失败"))
                continue
        existing.setdefault(h, []).append(target)
        w, hh = sips_size(dst) if not args.dry_run else sips_size(src)
        added.append({"file": target, "src": os.path.basename(src), "md5": h,
                      "width": w, "height": hh})

    # 4. 报告
    log("")
    log(f"[结果] 新增入库 {len(added)} 张 | 重复跳过 {len(dup)} 张 | 失败 {len(failed)} 张")
    if args.dry_run:
        log("[dry-run] 未实际落盘")
    if added:
        log("\n新增明细:")
        for a in added:
            log(f"  + {a['file']}  ({a['width']}×{a['height']})  ← {a['src']}")
    if dup[:10]:
        log("\n重复跳过(示例):")
        for s, e in dup[:10]:
            log(f"  = {s}  已存在于池: {e}")
    if failed:
        log("\n失败:")
        for s, e in failed:
            log(f"  ! {s}  {e}")

    # 5. 重建索引
    if not args.dry_run:
        log("")
        idx = rebuild_index()
        if args.gallery:
            build_gallery(idx)
        # 同步照片池总数到 used-photos.json
        try:
            j = json.load(open(USED_JSON, encoding="utf-8"))
            n = len([f for f in os.listdir(POOL_DIR)
                     if os.path.isfile(os.path.join(POOL_DIR, f))
                     and os.path.splitext(f)[1].lower() in IMG_EXT])
            if j.get("照片池总数") != n:
                j["照片池总数"] = n
                json.dump(j, open(USED_JSON, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
                log(f"[清单] used-photos.json 照片池总数已更新为 {n}")
        except Exception as e:
            log(f"[警告] used-photos.json 更新失败: {e}")


if __name__ == "__main__":
    main()
