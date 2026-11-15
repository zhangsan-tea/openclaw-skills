#!/usr/bin/env python3
"""周报机判门禁（规则77、88、91 配套）。

用法：
  python3 weekly_gate.py 当期.md [--prev 上期1.md --prev 上期2.md] [--force]

输入为周报的 Markdown/纯文本导出：
  栏目行：一、xxx（可带 "- " 或 "## " 前缀）
  条目行：1. 标题（可带缩进、"### " 前缀）
  其余非空行为该条正文。

输出 PASS/FAIL 表，存在 ERROR 时退出码为 1；确需放行须显式 --force，并在交付说明中留痕。
"""
import re, sys, difflib, argparse

SEC = re.compile(r'^(?:[-#]+\s*)?((?:[一二三四五六七八九十]、)?[^\s\d].*?)\s*$')  # 栏目：顶格行（企微导出为“- 栏目名”，成稿为“一、栏目名”）
ENT = re.compile(r'^\s*(?:#+\s*)?(\d+)\.\s+(.+?)\s*$')


def parse(path):
    secs, cur, ent = [], None, None
    for raw in open(path, encoding='utf-8').read().split('\n'):
        line = raw.replace('**', '').rstrip()
        if not line.strip() or line.strip().startswith(('内部信息', '团队周报（', '# ')):
            continue
        m = SEC.match(line)
        if m and not ENT.match(line) and not line.startswith((' ', '\t')) and (line.startswith(('- ', '#')) or re.match(r'[一二三四五六七八九十]、', line)):
            cur = {'name': m.group(1), 'entries': []}
            secs.append(cur); ent = None
            continue
        m = ENT.match(line)
        if m and cur is not None:
            ent = {'no': int(m.group(1)), 'title': m.group(2), 'body': ''}
            cur['entries'].append(ent)
            continue
        if ent is not None:
            ent['body'] += line.strip()
    out = []
    for s in secs:
        for e in s['entries']:
            out.append((s['name'][:2], e['no'], e['title'], e['body']))
    return out


def lcs(a, b):
    m = difflib.SequenceMatcher(None, a, b, autojunk=False).find_longest_match(0, len(a), 0, len(b))
    return a[m.a:m.a + m.size]


def first_sentence(s):
    m = re.search(r'[。；]', s)
    return s[:m.end()] if m else s


STANCE = re.compile(r'(后续|下一步|接下来)?(将)?(继续|持续)(关注|跟进|推进|跟踪)[^。]*。?$')
REL = re.compile(r'(上周|本周|下周)')
NAME = re.compile(r'(?:局长|副局长|部长|副部长|主任|副主任|司长|副司长|处长|书记|厅长|总监)([\u4e00-\u9fa5]{2,3})')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cur'); ap.add_argument('--prev', action='append', default=[])
    ap.add_argument('--force', action='store_true')
    a = ap.parse_args()
    cur = parse(a.cur)
    prevs = {p: parse(p) for p in a.prev}
    rows = []  # (level, rule, where, msg)

    for sec, no, t, b in cur:
        where = f'{sec}-{no} {t[:16]}'
        fs = first_sentence(b)
        common = lcs(t, fs)
        if len(common) >= 7:
            rows.append(('WARN', '规则9/76/77', where, f'标题与正文首句重合“{common[:20]}”，正文首句是否在复述标题'))
        n = len(b)
        if n > 300:
            rows.append(('WARN', '规则 篇幅', where, f'{n}字，超300字，提示压缩（不为达标删核心事实）'))
        if STANCE.search(b):
            rows.append(('WARN', '规则25', where, '结尾为“持续关注/跟进”类表态，核对是否有新增信息'))
        for w in set(REL.findall(b)):
            rows.append(('WARN', '规则10/43', where, f'含相对时间“{w}”，周一发出时会错位'))
        if re.search(r'([，。、；：])\1', b + t):
            rows.append(('ERROR', '标点', where, '出现连续重复标点'))
        if '（1）' in b and '（2）' not in b:
            rows.append(('WARN', '规则45', where, '有“（1）”无“（2）”'))

    # 跨期：重复报送与人名/数字口径
    names = {}
    for src, data in [('当期', cur)] + [(p, d) for p, d in prevs.items()]:
        for sec, no, t, b in data:
            for nm in NAME.findall(t + b):
                if nm[0] in '带赴巡出参陪到在率随主一二三四五六七八九十': continue
                names.setdefault(nm, set()).add(src)
    keys = sorted(names)
    for x in keys:
        for y in keys:
            if x != y and y.startswith(x) and len(y) - len(x) == 1:
                rows.append(('ERROR', '规则88', '人名', f'“{x}”与“{y}”疑为同一人写法不一致（出处：{sorted(names[x])} / {sorted(names[y])}）'))
    for p, data in prevs.items():
        for sec, no, t, b in cur:
            for psec, pno, pt, pb in data:
                c = lcs(b, pb)
                if len(c) >= 40:
                    rows.append(('ERROR', '规则88', f'{sec}-{no} {t[:14]}', f'与{p.split("/")[-1]} {psec}-{pno} 有{len(c)}字连续雷同，疑重复报送：“{c[:24]}…”'))
                    nums_c = {x.replace(' ', '') for x in re.findall(r'\d[\d,.]*\s*(?:万|亿|%|元|家|条|名|人|项)', b)}
                    nums_p = {x.replace(' ', '') for x in re.findall(r'\d[\d,.]*\s*(?:万|亿|%|元|家|条|名|人|项)', pb)}
                    if nums_c != nums_p:
                        rows.append(('ERROR', '规则88', f'{sec}-{no}', f'同一事项数字口径不同：当期{sorted(nums_c - nums_p)} vs 上期{sorted(nums_p - nums_c)}'))
                    break

    # 同一专项集中：标题关键词重复出现
    for i, (s1, n1, t1, b1) in enumerate(cur):
        for s2, n2, t2, b2 in cur[i + 1:]:
            c = lcs(t1, t2)
            if len(c) >= 6:
                rows.append(('WARN', '规则91', f'{s1}-{n1} / {s2}-{n2}', f'标题含相同词“{c}”，是否同一事件、可提整合建议（合并后篇幅不大才建议）'))

    gaps = sum(len(re.findall(r'[\u4e00-\u9fa5][A-Za-z]{2,}|[A-Za-z]{2,}[\u4e00-\u9fa5]', b)) for _, _, _, b in cur)
    if gaps:
        rows.append(('WARN', '规则93', '全文', f'汉字与英文之间缺半角空格共{gaps}处，集中提示一次；被要求改时统一改出'))

    ne = sum(1 for r in rows if r[0] == 'ERROR')
    nw = sum(1 for r in rows if r[0] == 'WARN')
    print(f'条目 {len(cur)}；ERROR {ne}；WARN {nw}')
    print('| 级别 | 依据 | 位置 | 说明 |\n|---|---|---|---|')
    for r in sorted(rows, key=lambda r: r[0]):
        print('| ' + ' | '.join(r) + ' |')
    if ne:
        print('\nFAIL：存在 ERROR，不得交付；确需放行须 --force 并在交付说明中留痕。')
        sys.exit(0 if a.force else 1)
    print('\nPASS（WARN 为提醒，由编辑人工判断）')


if __name__ == '__main__':
    main()
