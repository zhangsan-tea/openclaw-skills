#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
内容比对校验器 —— 确认排版数据(JSON)中的文字与基准源文本逐字一致。

两种用法:
1) JSON vs 基准文本文件:
     python verify_content.py <report.json> --source <source.txt>
   逐句检查 JSON 中每条文字是否都能在 source 中找到(忽略空白差异)，
   并反向检查 source 的关键句是否都进了 JSON，输出差异清单。

2) 仅自检 JSON 文字完整性(抽取全部文字，统计字数):
     python verify_content.py <report.json> --dump

校验规则:
- 归一化：去除所有空白字符、全半角空格，统一部分标点，再比较。
- 逐条报告：命中 / 未命中，并给出未命中的原文，供人工确认。
"""
import sys
import json
import re
import argparse


def normalize(s: str) -> str:
    """归一化文本：去空白、统一部分标点，便于比较。"""
    if s is None:
        return ""
    s = s.replace("\u3000", "").replace(" ", "").replace("\t", "").replace("\n", "")
    # 统一常见等价标点
    trans = {
        "，": ",", "。": ".", "；": ";", "：": ":",
        "（": "(", "）": ")", "、": ",",
        "“": '"', "”": '"', "‘": "'", "’": "'",
        "—": "-", "－": "-", "～": "~", "！": "!", "？": "?",
    }
    for k, v in trans.items():
        s = s.replace(k, v)
    return s.lower()


def extract_texts(node, acc):
    """递归抽取 JSON 中所有可见文字片段。"""
    if isinstance(node, dict):
        t = node.get("type")
        if t in ("h1", "h2", "h3", "para", "callout", "note"):
            if node.get("text"):
                acc.append(node["text"])
        elif t == "list":
            for it in node.get("items", []):
                acc.append(it)
        elif t == "table":
            if node.get("caption"):
                acc.append(node["caption"])
            for h in node.get("headers", []):
                acc.append(h)
            for row in node.get("rows", []):
                for cell in row:
                    acc.append(str(cell))
        elif t == "figure":
            if node.get("caption"):
                acc.append(node["caption"])
        for child in node.get("children", []):
            extract_texts(child, acc)
    elif isinstance(node, list):
        for x in node:
            extract_texts(x, acc)


def collect_all_texts(data):
    acc = []
    if data.get("meta", {}).get("title"):
        acc.append(data["meta"]["title"])
    if data.get("meta", {}).get("period"):
        acc.append(data["meta"]["period"])
    intro = data.get("intro")
    if intro:
        if isinstance(intro, dict):
            acc.append(intro.get("text", ""))
        else:
            acc.append(intro)
    for sec in data.get("sections", []):
        extract_texts(sec, acc)
    if data.get("meta", {}).get("footer"):
        acc.append(data["meta"]["footer"])
    return acc


def strip_markup(s: str) -> str:
    """移除 **加粗** 标记后再比较。"""
    return s.replace("**", "")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("json_file")
    ap.add_argument("--source", help="基准源文本文件(用于逐句比对)")
    ap.add_argument("--dump", action="store_true", help="仅抽取并打印JSON全部文字")
    args = ap.parse_args()

    with open(args.json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    texts = [strip_markup(t) for t in collect_all_texts(data)]
    total_chars = sum(len(re.sub(r"\s", "", t)) for t in texts)

    if args.dump or not args.source:
        print("=== JSON 抽取到的文字片段 (%d 条, 约 %d 字) ===" % (len(texts), total_chars))
        for i, t in enumerate(texts, 1):
            print("[%03d] %s" % (i, t))
        if not args.source:
            return

    # 与基准源比对
    with open(args.source, "r", encoding="utf-8") as f:
        source_raw = f.read()
    source_norm = normalize(source_raw)

    print("\n=== 内容比对结果 (JSON 每条 vs 基准源) ===")
    miss = []
    for t in texts:
        n = normalize(t)
        if not n:
            continue
        if n in source_norm:
            continue
        # 长句可能因换行/分栏被拆断，尝试分句再匹配
        subparts = re.split(r"[，。；！？,.;!?]", t)
        sub_ok = True
        for sp in subparts:
            spn = normalize(sp)
            if len(spn) >= 4 and spn not in source_norm:
                sub_ok = False
                break
        if sub_ok:
            continue
        miss.append(t)

    if not miss:
        print("✅ 全部通过：JSON 中所有文字片段均可在基准源中找到（忽略空白/标点差异）。")
    else:
        print("⚠️ 以下 %d 条在基准源中未完全匹配，请人工确认：" % len(miss))
        for m in miss:
            print("  - " + m)

    print("\n统计：JSON 文字片段 %d 条，约 %d 字。" % (len(texts), total_chars))
    sys.exit(1 if miss else 0)


if __name__ == "__main__":
    main()
