#!/usr/bin/env python3
"""
静心茶海报 · 导出前统一门禁（Pre-Export Gate）

为什么要有它（2026-10-20 立，直接回应 Lee 的观察："规则写进 skill 了，前面你也没遵循"）：

  SKILL.md 里写得很细的规则（分行优先 / 行尾不留标点 / 英文不手动分行 / 文字图片区重叠 1px）……
  在真正动手排版时并不会被逐条回读。原因不是态度问题，是结构问题：
    1. 规则是【陈述性文档】，不在执行路径上 —— 生成脚本一旦开跑，靠的是当下推断，不是查表
    2. SKILL.md 已 4.7 万字节，规则埋在几百行之后，读不全
    3. 事后才写进 skill 的规则，下一次开工时同样会被跳过
  ⇒ 唯一可靠的办法：把规则翻译成**可机判的断言**，并放在「生成 HTML → 导出 JPG」的必经关口。
  想跳过门禁，就得显式加 --force，而那会留下痕迹。

用法（生成 HTML 之后、导出 JPG 之前，必跑）：

  python3 scripts/pre_export_gate.py --html "<卡片 HTML 绝对路径>"
  python3 scripts/pre_export_gate.py --html X.html --list 12-18清单-复杂版.md --json cards.json
  python3 scripts/pre_export_gate.py --html X.html --photos "/path/to/海报制作素材/photos"

检查项（每项 PASS / FAIL，任一 FAIL 退出码非 0 ⇒ 不许导出）：

  A 图片引用        相对路径 + 文件真实存在 + 卡片数 == 图片数（不含二维码）
  B 中文分行        长中文（>16 字）却一个 <br> 都没有 ⇒ 未按句读分行
  C 中文行尾标点    行尾残留 ，。？！；：、—— 等 ⇒ 违反 Lee 2026-10-19 定稿口径
  D 英文不手动分行  .quote-en 里出现 <br> ⇒ 会甩出孤词行，交给 text-wrap:balance
  E 白线结构        .card-photo-area 必须有 flex + margin-top:-1px（百分比小数高度会露缝）
  F 排版实测        调 probe_lines.js（需 node + Chrome）：超宽行 / 折断 / 行尾标点
  G 清单对齐        给了 --list/--json 才跑，调 verify_alignment.py（防漏条）
  H 已用图判重      给了 --photos 才跑，调 photo_dupe_check.py check
"""
import argparse
import glob
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TAIL_PUNCT = r'[，、；：。．？！?!,;:\-—–…）)】」』》"\']'


def find_node():
    """定位 node：优先环境变量，再找托管目录，最后 PATH。不要写死用户名。"""
    for k in ("NODE_BIN", "NODE"):
        v = os.environ.get(k)
        if v and os.path.exists(v):
            return v
    for pat in (os.path.expanduser("~/.workbuddy/binaries/node/versions/*/bin/node"),
                "/opt/homebrew/bin/node", "/usr/local/bin/node"):
        hits = sorted(glob.glob(pat))
        if hits:
            return hits[-1]
    return "node"


def find_node_modules():
    v = os.environ.get("NODE_PATH")
    if v:
        return v
    hits = glob.glob(os.path.expanduser("~/.workbuddy/binaries/node/workspace/node_modules"))
    return hits[0] if hits else ""


class Report:
    def __init__(self):
        self.rows = []

    def add(self, code, name, ok, detail, hard=True):
        self.rows.append((code, name, ok, detail, hard))

    def failed(self):
        return [r for r in self.rows if not r[2] and r[4]]

    def warn(self):
        return [r for r in self.rows if not r[2] and not r[4]]

    def render(self):
        print("\n=== 导出前门禁 ===")
        print(f"{'项':<3}{'检查':<16}{'结果':<6}说明")
        for code, name, ok, detail, hard in self.rows:
            mark = "✓" if ok else ("✗" if hard else "!")
            print(f"{code:<3}{name:<16}{mark:<6}{detail}")
        hard_f, warn_f = self.failed(), self.warn()
        print(f"\n硬失败 {len(hard_f)} 项，提醒 {len(warn_f)} 项")
        if hard_f:
            print("⇒ 不可导出：" + "、".join(r[1] for r in hard_f))
        return 1 if hard_f else 0


def split_br(inner_html):
    return [re.sub(r"<[^>]+>", "", s).strip()
            for s in re.split(r"<br\s*/?>", inner_html, flags=re.I)]


def block(html, cls):
    """取第一个含该 class 的元素内部 HTML（够用：每张卡结构一致）。"""
    m = re.search(r'class="[^"]*\b' + cls + r'\b[^"]*"[^>]*>(.*?)</div>', html, re.S)
    return m.group(1) if m else None


def check_images(html, html_path, rep):
    base = os.path.dirname(os.path.abspath(html_path))
    srcs = [s for s in re.findall(r'<img\s+[^>]*src="([^"]+)"', html, re.I)
            if not s.startswith("data:")]
    if not srcs:
        rep.add("A", "图片引用", False,
                "全是 base64 内嵌 ⇒ 这是自包含预览版，请对【源 HTML】跑门禁")
        return
    abs_hits = [s for s in srcs if s.startswith(("/", "file:", "http"))]
    if abs_hits:
        rep.add("A", "图片引用", False,
                f"{len(abs_hits)} 处绝对路径（换电脑会失效），必须改相对：{abs_hits[:2]}")
        return
    miss = [s for s in srcs if not os.path.exists(os.path.join(base, s))]
    if miss:
        rep.add("A", "图片引用", False, f"{len(miss)} 张文件不存在，如 {miss[0]}")
        return
    # 背景图一律走 photos/ 前缀（换电脑也能显示）；二维码是同级裸文件名
    # 二维码现在使用真实 <img>（便于自包含预览内嵌），统计背景图时必须排除它
    photo = [s for s in srcs
             if s.startswith("photos/")
             and not any(k in s.lower() for k in ("qrcode", "二维码", "qr_", "qr."))]
    if not photo:  # 退化：没有 photos/ 前缀时按关键词排除
        photo = [s for s in srcs
                 if not any(k in s.lower() for k in ("qrcode", "二维码", "qr_", "qr."))]
    cards = len(re.findall(r'id="bcard-\d+"', html))
    ok = (cards == 0) or (cards == len(photo))
    rep.add("A", "图片引用", ok,
            f"相对路径 {len(srcs)} 张全部存在；卡 {cards} / 背景图 {len(photo)}"
            + ("" if ok else " ⇒ 数量不等，多半多塞或漏了一条"))


def check_static_rules(html, rep):
    """纯静态检查：不依赖浏览器，先把最容易「忘了遵循」的几条钉死。"""
    # B 中文分行
    cn_all = re.findall(r'class="[^"]*quote-chinese[^"]*"[^>]*>(.*?)</div>', html, re.S)
    flat = [s for blk in cn_all for s in split_br(blk) if s]
    no_br = [s for s in flat if len(re.sub(r"\s", "", s)) > 16]
    rep.add("B", "中文分行", not no_br,
            f"{len(flat)} 个中文行，超 16 字且未分行 {len(no_br)} 行"
            + ("" if not no_br else f"，如：{no_br[0][:18]}…"),
            hard=False)

    # C 中文行尾标点
    bad = [s for s in flat if re.search(TAIL_PUNCT + r"$", s)]
    rep.add("C", "中文行尾标点", not bad,
            "行尾无标点 ✓" if not bad else f"{len(bad)} 行行尾有标点：…{bad[0][-10:]}")

    # D 英文不手动分行
    en_all = re.findall(r'class="[^"]*quote-en[^"]*"[^>]*>(.*?)</div>', html, re.S)
    en_br = [b for b in en_all if re.search(r"<br\s*/?>", b, re.I)]
    rep.add("D", "英文不手动分行", not en_br,
            f"{len(en_all)} 个英文块，手动分行 {len(en_br)} 个（会甩孤词行）")

    # E 白线结构
    m = re.search(r"\.card-photo-area\s*\{([^}]*)\}", html)
    css = m.group(1) if m else ""
    ok_e = ("flex" in css) and re.search(r"margin-top\s*:\s*-?1px", css)
    rep.add("E", "白线结构", ok_e,
            ".card-photo-area flex + margin-top:-1px ✓" if ok_e
            else "缺 flex/重叠，百分比小数高度会露白线")


def run_probe(html_path, rep, force):
    node, nm = find_node(), find_node_modules()
    env = dict(os.environ)
    if nm:
        env["NODE_PATH"] = nm
    try:
        out = subprocess.run([node, os.path.join(HERE, "probe_lines.js"), html_path],
                             capture_output=True, text=True, timeout=180, env=env)
    except Exception as e:
        rep.add("F", "排版实测", False, f"跑不起来（{e}）", hard=not force)
        return
    txt = out.stdout or ""
    over = len(re.findall(r"⚠超宽", txt))
    broken = len(re.findall(r"⚠折断", txt))
    tail = re.search(r"行尾标点残留\s*\n(.*)", txt)
    tail_n = 0 if (tail and tail.group(1).strip().startswith("无")) else len(
        [l for l in (tail.group(1).splitlines() if tail else []) if l.strip() and not l.startswith("无")])
    ok = (over == 0 and broken == 0 and tail_n == 0)
    rep.add("F", "排版实测", ok,
            f"超宽 {over} / 折断 {broken} / 行尾残留 {tail_n}"
            + ("" if ok else " ⇒ 见 probe_lines.js 明细"))
    if not ok:
        print("\n--- probe_lines.js 输出 ---\n" + txt)


def run_alignment(listf, jsonf, rep):
    r = subprocess.run([sys.executable, os.path.join(HERE, "verify_alignment.py"),
                        "--list", listf, "--json", jsonf],
                       capture_output=True, text=True)
    ok = (r.returncode == 0)
    first = (r.stdout.strip().splitlines() or [""])[-1][:70]
    rep.add("G", "清单对齐", ok, first)
    if not ok:
        print("\n--- verify_alignment.py 输出 ---\n" + r.stdout)


def run_dupe(html_path, photos, rep):
    r = subprocess.run([sys.executable, os.path.join(HERE, "photo_dupe_check.py"),
                        "check", "--html", html_path, "--photos", photos],
                       capture_output=True, text=True)
    ok = (r.returncode == 0)
    first = (r.stdout.strip().splitlines() or [""])[-1][:70]
    rep.add("H", "已用图判重", ok, first, hard=False)
    if not ok:
        print("\n--- photo_dupe_check.py 输出 ---\n" + r.stdout)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--html", required=True)
    ap.add_argument("--list", help="金句清单 md（配合 --json 跑清单对齐）")
    ap.add_argument("--json", help="生成用 JSON（配合 --list）")
    ap.add_argument("--photos", help="照片池目录（跑已用图判重）")
    ap.add_argument("--no-probe", action="store_true", help="跳过浏览器实测（快检）")
    ap.add_argument("--force", action="store_true", help="明知有问题仍要导出（会留痕）")
    a = ap.parse_args()

    html = open(a.html, encoding="utf-8").read()
    rep = Report()
    check_images(html, a.html, rep)
    check_static_rules(html, rep)
    if not a.no_probe:
        run_probe(a.html, rep, a.force)
    if a.list and a.json:
        run_alignment(a.list, a.json, rep)
    if a.photos:
        run_dupe(a.html, a.photos, rep)

    code = rep.render()
    if a.force and code:
        print("⚠️ --force 已启用：带着问题导出，请自行确认后果")
        return 0
    if code == 0:
        print("⇒ 门禁通过，可以导出")
    return code


if __name__ == "__main__":
    sys.exit(main())
