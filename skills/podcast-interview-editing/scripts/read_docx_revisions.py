#!/usr/bin/env python3
"""读 .docx 的修订、删除线、黄底和批注。

用法：python read_docx_revisions.py 稿子.docx [--json out.json]
输出：
  1) 修订统计：w:del / w:ins / rPrChange 按作者计数
  2) 每个含改动的段落：〔删·作者:文字〕〖增·作者:文字〗~~删除线~~ 【黄:文字】 ⟨批N⟩
  3) 批注列表：编号 / 作者 / 内容 / 锚定文字（导出的 Word 常常没有 commentRangeStart，此时锚定为空，按批注前的划线或相邻句子定位）
"""
import sys, json, zipfile, argparse
from collections import Counter
from lxml import etree
W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'


def main(path, out=None):
    z = zipfile.ZipFile(path); x = etree.fromstring(z.read('word/document.xml'))
    stat = {t: dict(Counter(e.get(W + 'author') for e in x.iter(W + t))) for t in ['del', 'ins', 'rPrChange']}
    print('修订统计', json.dumps(stat, ensure_ascii=False))
    paras = []; anchors = {}; openk = {}
    for pi, p in enumerate(x.find(W + 'body').iter(W + 'p')):
        s = ''; changed = False
        for el in p.iter():
            if el.tag == W + 'commentRangeStart': openk[el.get(W + 'id')] = ''
            elif el.tag == W + 'commentRangeEnd': anchors[el.get(W + 'id')] = openk.pop(el.get(W + 'id'), '')
            elif el.tag == W + 'commentReference': s += '⟨批%s⟩' % el.get(W + 'id'); changed = True
            elif el.tag in (W + 't', W + 'delText'):
                t = el.text or ''
                for k in openk: openk[k] += t
                r = el.getparent(); anc = list(el.iterancestors())
                d = next((a for a in anc if a.tag == W + 'del'), None); i = next((a for a in anc if a.tag == W + 'ins'), None)
                rpr = r.find(W + 'rPr'); st = rpr is not None and rpr.find(W + 'strike') is not None and rpr.find(W + 'strike').get(W + 'val') not in ('0', 'false')
                hl = rpr is not None and ((rpr.find(W + 'shd') is not None and (rpr.find(W + 'shd').get(W + 'fill') or '').upper() == 'FFFF00') or rpr.find(W + 'highlight') is not None)
                if d is not None: s += '〔删·%s:%s〕' % (d.get(W + 'author'), t); changed = True
                elif i is not None: s += '〖增·%s:%s〗' % (i.get(W + 'author'), t); changed = True
                elif st: s += '~~%s~~' % t; changed = True
                elif hl: s += '【黄:%s】' % t; changed = True
                else: s += t
        if changed: paras.append(dict(p=pi, text=s))
    cms = []
    if 'word/comments.xml' in z.namelist():
        for e in etree.fromstring(z.read('word/comments.xml')):
            k = e.get(W + 'id'); cms.append(dict(id=k, author=e.get(W + 'author'), date=e.get(W + 'date'), text=''.join(e.itertext()), anchor=anchors.get(k, '')))
    for p in paras: print('P%d: %s' % (p['p'], p['text'][:800]))
    print('\n批注 %d 条' % len(cms))
    for c in cms: print('#%s [%s] %s | 锚:%s' % (c['id'], c['author'], c['text'], c['anchor'][:80]))
    if out: json.dump(dict(stat=stat, paras=paras, comments=cms), open(out, 'w'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('docx'); ap.add_argument('--json'); a = ap.parse_args(); main(a.docx, a.json)
