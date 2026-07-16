#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
月报 HTML 生成器（可选）—— 依据同一份结构化 JSON 生成还原"阅览版"精致视觉的 HTML。
相比 Word，HTML 可呈现蓝色渐变卡片、圆角、彩色状态标签等 Word 做不到的效果，
适合贴回企微文档 / 转 PDF / 网页分享。

用法:
    python build_report_html.py <input.json> <output.html>
"""
import sys
import os
import json
import re
import html
import base64


def esc(s):
    return html.escape(str(s))


def rich(text):
    """**加粗** -> <strong>。"""
    text = esc(text)
    return re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)


def status_class(val):
    v = str(val)
    if v in ("已结束",):
        return "tag-done"
    if v in ("进行中",):
        return "tag-doing"
    if v in ("未开展",):
        return "tag-todo"
    if v in ("一级",):
        return "tag-l1"
    if v in ("二级",):
        return "tag-l2"
    if v in ("三级",):
        return "tag-l3"
    if v in ("顺利通过", "有条件通过", "运作中"):
        return "tag-pass"
    return ""


def render_table(node):
    out = []
    if node.get("caption"):
        out.append(f'<div class="tbl-cap">{esc(node["caption"])}</div>')
    out.append('<table class="rpt-table"><thead><tr>')
    for h in node["headers"]:
        out.append(f'<th>{esc(h)}</th>')
    out.append('</tr></thead><tbody>')
    for row in node["rows"]:
        out.append('<tr>')
        for cell in row:
            cls = status_class(cell)
            if cls:
                out.append(f'<td><span class="tag {cls}">{esc(cell)}</span></td>')
            else:
                out.append(f'<td>{esc(cell)}</td>')
        out.append('</tr>')
    out.append('</tbody></table>')
    return "\n".join(out)


def render_node(node):
    t = node.get("type")
    out = []
    if t == "h1":
        out.append(f'<div class="h1-bar">{esc(node["text"])}</div>')
    elif t == "h2":
        out.append(f'<div class="h2-title">{esc(node["text"])}</div>')
    elif t == "h3":
        out.append(f'<div class="h3-title">{rich(node["text"])}</div>')
    elif t == "para":
        out.append(f'<p class="para">{rich(node["text"])}</p>')
    elif t == "callout":
        out.append(f'<div class="callout">{rich(node["text"])}</div>')
    elif t == "note":
        out.append(f'<div class="note">{rich(node["text"])}</div>')
    elif t == "list":
        out.append('<ul class="rpt-list">')
        for it in node["items"]:
            out.append(f'<li>{rich(it)}</li>')
        out.append('</ul>')
    elif t == "table":
        out.append(render_table(node))
    elif t == "figure":
        cap = esc(node.get("caption", ""))
        note = esc(node.get("note", "配图"))
        image_path = node.get("image", "")

        if image_path and os.path.exists(image_path):
            # 嵌入真实图片（base64 data URI）
            ext = os.path.splitext(image_path)[1].lower()
            mime_map = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
                        ".gif": "image/gif", ".webp": "image/webp"}
            mime = mime_map.get(ext, "image/png")
            try:
                with open(image_path, "rb") as f:
                    b64 = base64.b64encode(f.read()).decode("ascii")
                data_uri = f"data:{mime};base64,{b64}"
                out.append(f'<div class="figure"><img class="figure-img" src="{data_uri}" alt="{cap}">'
                           f'<div class="figure-cap">{cap}</div></div>')
            except Exception as e:
                # 降级为占位
                out.append(f'<div class="figure"><div class="figure-ph">［{note}］</div>'
                           f'<div class="figure-cap">{cap}</div></div>')
        else:
            out.append(f'<div class="figure"><div class="figure-ph">［{note}］</div>'
                       f'<div class="figure-cap">{cap}</div></div>')
    for child in node.get("children", []):
        out.append(render_node(child))
    return "\n".join(out)


CSS = """
* { box-sizing: border-box; }
body { font-family: "微软雅黑","Microsoft YaHei",sans-serif; color:#333;
  background:#f0f2f5; margin:0; padding:24px; line-height:1.75; }
.page { max-width: 900px; margin:0 auto; background:#fff; padding:40px 48px;
  border-radius:8px; box-shadow:0 2px 16px rgba(0,0,0,.08); }
.title { text-align:center; font-size:26px; font-weight:700; color:#1f4e8c;
  border:1px solid #cfdcef; border-radius:8px; padding:20px; margin-bottom:4px; }
.period { text-align:center; color:#8a94a6; font-size:14px; margin:8px 0 20px; }
.intro { background:#eaf1fb; border-radius:8px; padding:16px 20px; margin-bottom:24px;
  border:1px solid #d8e5f7; }
.h1-bar { display:inline-block; background:linear-gradient(90deg,#1f4e8c,#2e6cc0);
  color:#fff; font-size:17px; font-weight:700; padding:8px 20px; border-radius:4px;
  margin:28px 0 12px; }
.h2-title { font-size:15px; font-weight:700; color:#2e5ca8; border-left:4px solid #2e5ca8;
  padding-left:10px; margin:18px 0 8px; }
.h3-title { font-size:14px; font-weight:700; color:#1f4e8c; margin:14px 0 6px; }
.para { text-indent:2em; margin:8px 0; }
.callout { background:#eaf1fb; border-left:4px solid #2e5ca8; border-radius:0 6px 6px 0;
  padding:12px 16px; margin:8px 0 14px; font-size:14px; }
.callout strong { color:#1f4e8c; }
.note { text-align:right; color:#8a94a6; font-size:13px; font-style:italic; margin:8px 0; }
.rpt-list { margin:8px 0; padding-left:1.4em; }
.rpt-list li { margin:5px 0; }
.tbl-cap { font-weight:700; color:#1f4e8c; margin:14px 0 6px; }
.rpt-table { width:100%; border-collapse:collapse; margin:6px 0 16px; font-size:13px; }
.rpt-table th { background:#1f4e8c; color:#fff; padding:8px 10px; text-align:center;
  border:1px solid #16406f; }
.rpt-table td { padding:8px 10px; border:1px solid #dfe6f0; vertical-align:top; }
.rpt-table tbody tr:nth-child(even){ background:#f5f8fc; }
.tag { display:inline-block; padding:2px 10px; border-radius:12px; font-size:12px; font-weight:600; }
.tag-done { background:#fff3d6; color:#a6791a; }
.tag-doing { background:#d9f2e3; color:#1e7a45; }
.tag-todo { background:#ececec; color:#888; }
.tag-l1 { background:#fde2e2; color:#c0392b; }
.tag-l2 { background:#fdf3d0; color:#a6791a; }
.tag-l3 { background:#dbe8fb; color:#2e5ca8; }
.tag-pass { background:#d9f2e3; color:#1e7a45; }
.figure { text-align:center; margin:12px 0 16px; }
.figure-img { max-width:100%; height:auto; border-radius:6px;
  box-shadow:0 2px 12px rgba(0,0,0,.08); }
.figure-ph { background:#f0f3f8; color:#8a94a6; border:1px dashed #c5cfdd;
  border-radius:6px; padding:24px; font-size:14px; }
.figure-cap { color:#8a94a6; font-size:13px; margin-top:6px; }
.footer { text-align:center; color:#8a94a6; font-size:14px; margin-top:32px;
  padding-top:16px; border-top:1px solid #eee; }
"""


def build(data, out_path):
    body = []
    meta = data["meta"]
    body.append(f'<div class="title">{esc(meta.get("title",""))}</div>')
    if meta.get("period"):
        body.append(f'<div class="period">{esc(meta["period"])}</div>')
    if data.get("intro"):
        intro_txt = data["intro"] if isinstance(data["intro"], str) else data["intro"].get("text", "")
        if intro_txt:
            body.append(f'<div class="intro">{rich(intro_txt)}</div>')
    for sec in data["sections"]:
        body.append(render_node(sec))
    if meta.get("footer"):
        body.append(f'<div class="footer">{esc(meta["footer"])}</div>')

    doc_html = f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(meta.get("title",""))}</title>
<style>{CSS}</style></head>
<body><div class="page">
{''.join(body)}
</div></body></html>"""

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(doc_html)
    print("已生成 HTML:", out_path)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python build_report_html.py <input.json> <output.html>")
        sys.exit(1)
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        data = json.load(f)
    build(data, sys.argv[2])
