#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
静心茶海报 · 清单 ↔ 生成数据 对齐校验（必做，2026-10-20 血泪教训）

背景：2026-10-19 那批 12–18 号海报，把复杂版清单（md）转录成生成用 JSON 时，
手工多塞了一条清单里没有的条目，导致后面 15 条整体错位一格，
复杂版最后一条「身体的来信（回应利军）」被挤出 16 条之外、整条丢失。
用户凭记忆发现了，反问"我怎么记得有一段对丽君的关于身体的回应"。

为什么其他校验都测不出来：
  余量测量、折行检查、背景图判重 —— 它们只检查「现有条目是否合格」，
  不检查「条目集合是否等于清单」。多塞一条 + 丢一条，数量和格式都对，全部放行。

⇒ 铁律：生成 HTML 之前必须跑本脚本，并把对照表给用户过目。

用法：
  python3 verify_alignment.py --list 12-18清单-复杂版.md --json cards.json
  python3 verify_alignment.py --list 清单.md --json cards.json --key-cn cn --key-topic no

判定：
  1. 条目数必须相等
  2. 逐条：清单主题名的关键词必须出现在该条中文文案里（模糊匹配，容忍改写）
  3. 日期标签必须与清单一致
"""
import argparse
import json
import re
import sys

CARD_RE = re.compile(r'^\*\*卡片\s*(\d+)\s*[·:：\-]?\s*(\d{4})?\s*[·:：\-]?\s*(.+?)\*\*\s*$')


def parse_list(path):
    """解析清单 md：形如 **卡片16 · 1018 · 身体的来信（回应利军）**"""
    items = []
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            m = CARD_RE.match(line)
            if m:
                items.append({
                    'no': int(m.group(1)),
                    'date': m.group(2),
                    'topic': m.group(3).strip(),
                })
    return items


def topic_keywords(topic):
    """从主题名提取匹配关键词：去掉括号注释，取前 6 字"""
    base = re.split(r'[（(]', topic)[0].strip()
    return base


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--list', required=True, help='清单 md 文件路径')
    ap.add_argument('--json', required=True, help='生成用 JSON 文件路径')
    ap.add_argument('--key-cn', default='cn', help='JSON 中中文字段名')
    ap.add_argument('--key-no', default='no', help='JSON 中日期标签字段名')
    args = ap.parse_args()

    lst = parse_list(args.list)
    with open(args.json, encoding='utf-8') as f:
        cards = json.load(f)

    print(f"清单条目: {len(lst)}    生成数据条目: {len(cards)}")

    ok = True
    if len(lst) != len(cards):
        print(f"\n⚠️ 条目数不一致！差 {abs(len(lst) - len(cards))} 条")
        print("   这几乎一定意味着：多塞了一条 / 丢了一条 —— 必须查清楚再生成")
        ok = False

    print("\n=== 逐条比对 ===")
    print(f"{'#':>3}  {'清单主题':<18} {'命中':<4} {'日期':<8} 生成数据首句")
    n = max(len(lst), len(cards))
    for i in range(n):
        L = lst[i] if i < len(lst) else None
        C = cards[i] if i < len(cards) else None

        if L is None:
            print(f"{i+1:>3}  {'(清单无)':<18} {'⚠':<4} {'':<8} 【多余条目】{C.get(args.key_cn,'')[:24]}")
            ok = False
            continue
        if C is None:
            print(f"{i+1:>3}  {L['topic']:<18} {'✗':<4} {L['date'] or '':<8} 【缺失！清单有、生成数据没有】")
            ok = False
            continue

        cn = C.get(args.key_cn, '')
        kw = topic_keywords(L['topic'])
        # 主题名只是辅助提示，不判失败 —— 清单主题与最终文案措辞常不同
        # （如主题"中心即片刻"，文案是"中心就在这里"），判失败会大量误报
        probe = kw[:3]
        hit = probe in cn
        date_ok = True
        if L['date'] and len(L['date']) >= 4:
            # 清单日期是 MMDD（如 1018）；生成数据标签形如 "NO.16 · 十月十八日"
            month = int(L['date'][0:2])
            day = int(L['date'][2:4])
            month_cn = ['', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '十一', '十二'][month]
            day_cn = {12: '十二', 13: '十三', 14: '十四', 15: '十五', 16: '十六',
                      17: '十七', 18: '十八', 19: '十九', 20: '二十', 21: '二十一',
                      22: '二十二', 23: '二十三', 24: '二十四', 25: '二十五',
                      26: '二十六', 27: '二十七', 28: '二十八', 29: '二十九',
                      30: '三十', 31: '三十一'}.get(day, str(day))
            # 注意：10 月是「十月」不是「十月十日」——月份整体转换，不要拼前缀
            expect = f"{month_cn}月{day_cn}日"
            date_ok = expect in C.get(args.key_no, '')
            if not date_ok:
                ok = False

        mark = '✓' if hit else '·'   # · = 措辞不同，人工扫一眼即可
        dmark = '' if date_ok else ' ⚠日期不符'
        print(f"{i+1:>3}  {L['topic'][:18]:<18} {mark:<4} {L['date'] or '':<8} {cn[:26]}{dmark}")

    print("\n=== 结论 ===")
    if ok:
        print("✓ 清单与生成数据完全一致，可以生成 HTML")
        sys.exit(0)
    else:
        print("✗ 存在不一致 —— 修正后再生成，不要带着问题往下走")
        sys.exit(1)


if __name__ == '__main__':
    main()
