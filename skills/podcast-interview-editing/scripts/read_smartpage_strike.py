#!/usr/bin/env python3
"""读企业微信智能文档里的删除线（Markdown 导出不带删除线，只能解析块数据）。

先落盘块数据：
  wecom-cli smartpage pages get --json '{"docid":"…","page_id":"…","content_type":"block"}'
  → 返回 JSON 里 pages[0].file_path 指向块数据文件
用法：
  python read_smartpage_strike.py 块数据.json --list-attrs      # 先看每个样式编号套在哪些文字上，认出哪个是删除线
  python read_smartpage_strike.py 块数据.json --strike 4         # 按表格逐行输出，删除线文字用 ~~ ~~ 标出
说明：块文本的样式是 etherpad 式编码，如 "*0*1+2*4+1c"＝样式0、1作用于接下来 2 个字，样式4作用于 0x1c 个字（36 进制）。
样式编号是每份文档自己的，没有全局表：必须用 --list-attrs 对照文字确认，不能照搬上一份文档的编号。
"""
import json, re, argparse
from collections import defaultdict


def parse(at, text):
    out = []; pos = 0
    for m in re.finditer(r'((?:\*[0-9a-z]+)*)(?:\|[0-9a-z]+)?\+([0-9a-z]+)', at):
        n = int(m.group(2), 36); out.append((re.findall(r'\*([0-9a-z]+)', m.group(1)), text[pos:pos + n])); pos += n
    if pos < len(text): out.append(([], text[pos:]))
    return out


def main(path, strike=None, list_attrs=False):
    d = json.load(open(path)); by = {b['id']: b for b in d}
    if list_attrs:
        samp = defaultdict(list)
        for b in d:
            t = (b.get('property') or {}).get('title')
            if t and t.get('text'):
                for a, s in parse(t.get('attribs', ''), t['text']):
                    if s.strip(): samp[tuple(a)].append(s[:30])
        for k, v in sorted(samp.items(), key=lambda x: -len(x[1])): print(list(k), len(v), v[:3])
        return

    def txt(b):
        t = (b.get('property') or {}).get('title')
        if not t or not t.get('text'): return ''
        return ''.join(('~~%s~~' % s) if strike is not None and str(strike) in a else s for a, s in parse(t.get('attribs', ''), t['text']))

    def flat(j):
        return txt(by[j]) + ''.join(flat(c) for c in by[j].get('children', []))
    page = next(b for b in d if b['type'] == 'page')
    for cid in page['children']:
        b = by[cid]
        if b['type'] == 'unspecified' and 'simple_table_props' in json.dumps(b.get('property', {})):
            print('=== 表格'); [print(' | '.join(flat(c) for c in by[r].get('children', []))) for r in b['children']]
        else:
            s = flat(cid)
            if s.strip(): print('[%s] %s' % (b['type'], s[:300]))


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('json'); ap.add_argument('--strike'); ap.add_argument('--list-attrs', action='store_true')
    a = ap.parse_args(); main(a.json, a.strike, a.list_attrs)
