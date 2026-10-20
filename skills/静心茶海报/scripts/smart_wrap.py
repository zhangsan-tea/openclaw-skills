#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
静心茶海报 · 文案智能分行

解决两件事：
  1. 行尾标点清除（Lee 2026-10-19 定稿口径）
  2. 中文按句读智能分行（短句合并填满、长句在句读处切开），消除"单字折行"

用法：
    python3 smart_wrap.py --json cards.json            # 预览全部分行
    python3 smart_wrap.py --json cards.json --apply    # 直接改写 JSON（加 cn_lines 字段）
    python3 smart_wrap.py --text "中文文案" --cn-size 17.5

⚠️ 行宽上限必须随字号重算（见 --cn-size / --cn-max）：
   16.5px + 2.5px 字距 -> 17 字（实测 298px）
   17.5px + 2.5px 字距 -> 16 字（16 字=320px 刚好，17 字=340px 超宽折断）
   上限算错 = 浏览器强行折行 = 行尾甩孤字，这是"排版很乱"的头号根因。
"""
import argparse
import json
import re

# ---- 行尾标点口径（Lee 2026-10-19 定稿）----
# 行尾一律不留标点，含 。？！；：，、—— 及收尾引号括号。
# 注意：行【中间】的句末标点要保留 —— 它用来分隔同一行里的两句话，
# 删掉会变成"谁在经验谁在观看谁在观察"，不可读。
TAIL_PUNCT = "，、；：,;:—–－-…·・。．？！?!、）)】」』》\"'’” "

# ---- 默认容量（17.5px 中文 / 16.5px 英文实测）----
CN_MAX_DEFAULT = 16
CN_MIN_GOOD = 10      # 低于此长度的行尝试与下一行合并
CN_TOL = 0            # 合并后允许超出上限的量 —— 必须为 0！
                      # 曾设 3，导致 7+10 并成 17 字行 = 340px 超宽被折断
EN_MAX_DEFAULT = 46
EN_MIN_GOOD = 22
EN_TOL = 0


def strip_tail(line):
    """行尾标点一律清除"""
    return line.rstrip(TAIL_PUNCT).rstrip()


def _cn_segments(text, cn_max):
    """中文细粒度切分：先按句末标点，超长再按逗号/顿号/破折号切。"""
    sentences = [s for s in re.split(r'(?<=[。！？；])', text) if s]
    segs = []
    for s in sentences:
        if len(s) <= cn_max:
            segs.append(s)
        else:
            segs.extend([p for p in re.split(r'(?<=[，、—])', s) if p])
    return segs


def _en_segments(text):
    """英文按单词切分（保留空格）。"""
    words = text.split(' ')
    return [w + ' ' for w in words[:-1]] + [words[-1]]


def _greedy(segs, max_len, min_good, tol):
    """贪心填满每行，避免过短行；后处理合并短行（不得超上限）。"""
    lines, cur = [], ''
    for s in segs:
        if not cur:
            cur = s
        elif len(cur) + len(s.rstrip()) <= max_len:
            cur += s
        else:
            lines.append(cur.rstrip())
            cur = s.lstrip()
    if cur.strip():
        lines.append(cur.rstrip())

    merged = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if (i + 1 < len(lines) and len(line) < min_good
                and len(line) + len(lines[i + 1]) <= max_len + tol):
            merged.append(line + lines[i + 1])
            i += 2
        else:
            merged.append(line)
            i += 1
    return merged


def wrap_cn(text, cn_max=CN_MAX_DEFAULT):
    """中文智能分行 + 行尾去标点"""
    return [strip_tail(x) for x in _greedy(_cn_segments(text, cn_max), cn_max, CN_MIN_GOOD, CN_TOL)]


def wrap_en(text, en_max=EN_MAX_DEFAULT):
    """英文分行。仅在你确实要手动分英文时用——默认应让浏览器自动折行 + text-wrap:balance"""
    return [strip_tail(x) for x in _greedy(_en_segments(text), en_max, EN_MIN_GOOD, EN_TOL)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--json', help='卡片 JSON（含 cn/en 字段）')
    ap.add_argument('--text', help='单条中文文案，直接预览')
    ap.add_argument('--cn-size', type=float, default=17.5, help='中文号（用于换算上限）')
    ap.add_argument('--cn-max', type=int, help='直接指定中文每行字数上限（优先于换算）')
    ap.add_argument('--apply', action='store_true', help='把 cn_lines 写回 JSON')
    args = ap.parse_args()

    if args.cn_max:
        cn_max = args.cn_max
    else:
        cn_max = 17 if args.cn_size <= 16.5 else 16

    if args.text:
        for x in wrap_cn(args.text, cn_max):
            print(x)
        return

    if not args.json:
        ap.error('需要 --json 或 --text')

    with open(args.json, encoding='utf-8') as f:
        cards = json.load(f)

    warn = []
    for i, c in enumerate(cards, 1):
        lines = wrap_cn(c['cn'], cn_max)
        if args.apply:
            c['cn_lines'] = lines
        widths = [len(x) for x in lines]
        flag = ''
        if min(widths) < 8:
            flag = '  ⚠ 存在短行'
            warn.append(i)
        print(f"卡{i:02d} {len(lines)}行 {widths}{flag}")
        for x in lines:
            print('      |' + x)

    if args.apply:
        with open(args.json, 'w', encoding='utf-8') as f:
            json.dump(cards, f, ensure_ascii=False, indent=2)
        print(f"\n已写回 {args.json}")

    print("\n存在短行的卡:", warn if warn else '无')


if __name__ == '__main__':
    main()
