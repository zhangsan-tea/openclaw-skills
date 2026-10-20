#!/usr/bin/env node
/**
 * 静心茶海报 · 逐行实测（排版质量的唯一可信检查）
 *
 * 为什么必须有它：measure_card_fit.js 打印的"容器宽"只是【英文】div 的宽度，
 * 中文行是否超宽它看不出来。而中文行一旦超宽，浏览器会强行折断，
 * 第二行甩出两三个孤字 —— 这就是用户说的"排版好乱 / 单字折行"。
 * 只有用 Range 逐行测真实渲染宽度才能发现。
 *
 * 用法：
 *   NODE_PATH=... node probe_lines.js "<卡片 HTML 绝对路径>"
 *
 * 检查三项：
 *   1. 超宽行（宽 > 容器内容宽）—— 会被浏览器折断
 *   2. 行数与实测宽度数不符 —— 已经发生折断
 *   3. 中文行尾标点残留 —— 违反 Lee 2026-10-19 定稿口径
 */
const puppeteer = require('puppeteer-core');
const file = process.argv[2];

if (!file) {
  console.error('用法: node probe_lines.js "<卡片 HTML 绝对路径>"');
  process.exit(1);
}

(async () => {
  const b = await puppeteer.launch({
    headless: true,
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--allow-file-access-from-files'],
    defaultViewport: { width: 375, height: 667, deviceScaleFactor: 1 },
  });
  const p = await b.newPage();
  await p.goto('file://' + encodeURI(file), { waitUntil: 'domcontentloaded' });
  await p.evaluate(async () => { await document.fonts.ready; });
  await p.evaluate(async () => {
    await Promise.all([...document.querySelectorAll('img')].map(
      i => i.complete ? null : new Promise(r => { i.onload = r; i.onerror = r; })
    ));
  });
  await new Promise(r => setTimeout(r, 1200));

  const info = await p.evaluate(() => {
    // 自动探测卡片数量，不写死
    let n = 0;
    while (document.getElementById('bcard-' + (n + 1))) n++;
    // 容器内容宽 = 设计规范硬约束（375 - 左右留白）
    const CONTENT_LIMIT = 323;

    const res = [];
    for (let i = 1; i <= n; i++) {
      const card = document.getElementById('bcard-' + i);
      const out = { i, cn: null, en: null };

      for (const sel of ['.quote-chinese', '.quote-en']) {
        const el = card.querySelector(sel);
        if (!el) continue;

        // 逐文本节点用 Range 测每行实际宽度
        const widths = [];
        const r = document.createRange();
        const walk = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
        let node;
        while ((node = walk.nextNode())) {
          if (!node.textContent.trim()) continue;
          r.selectNodeContents(node);
          [...r.getClientRects()].filter(x => x.width > 1)
            .forEach(x => widths.push(Math.round(x.width)));
        }

        // 逻辑行数（按 <br> 切）；hasBr=false 表示是自然流动段落（英文常态）
        const parts = el.innerHTML.split(/<br\s*\/?>/i)
          .map(s => s.replace(/<[^>]+>/g, '').trim()).filter(Boolean);
        const hasBr = /<br\s*\/?>/i.test(el.innerHTML);
        const logical = hasBr ? parts : [];

        // 硬约束用设计规范里的容器内容宽 323px，
        // 不用 div 自身宽度 —— 居中布局下 div 会收缩到内容宽，会误导
        const rec = { widths, logical: logical.length, hasBr, limit: CONTENT_LIMIT };
        if (sel === '.quote-chinese') out.cn = rec; else out.en = rec;
      }
      res.push(out);
    }
    return res;
  });

  console.log('=== 逐行实测 ===');
  let problems = 0;

  info.forEach(o => {
    const parts = [];
    for (const [name, rec] of [['中', o.cn], ['英', o.en]]) {
      if (!rec) continue;
      const over = rec.widths.filter(w => w > rec.limit).length;
      // 只有手动分行（有 <br>）的元素才谈"折断"：
      // 英文是自然流动段落，逻辑1行/实测多行是正常自动折行，不是折断
      const broken = rec.hasBr && rec.logical && rec.widths.length !== rec.logical
        ? `⚠折断(逻辑${rec.logical}行/实测${rec.widths.length}行)` : '';
      const overFlag = over ? `⚠超宽${over}行` : '';
      if (over || broken) problems++;
      parts.push(`${name}${rec.widths.length}行宽[${rec.widths.join(',')}]${overFlag}${broken}`);
    }
    console.log(`卡${String(o.i).padStart(2, '0')} ${parts.join('  ')}`);
  });

  // 中文行尾标点（Lee 口径：含 。？！ 一律清除）
  const tails = await p.evaluate(() => {
    const bad = [];
    let n = 0;
    while (document.getElementById('bcard-' + (n + 1))) n++;
    for (let i = 1; i <= n; i++) {
      const el = document.getElementById('bcard-' + i).querySelector('.quote-chinese');
      if (!el) continue;
      el.innerHTML.split(/<br\s*\/?>/i).forEach(l => {
        const t = l.trim();
        if (t && /[，、；：—–…。．？！?!,;:）)】」』》]$/.test(t)) {
          bad.push(`卡${i}: …${t.slice(-8)}`);
        }
      });
    }
    return bad;
  });

  console.log('\n=== 中文行尾标点残留 ===');
  console.log(tails.length ? tails.join('\n') : '无 ✓');

  console.log('\n=== 结论 ===');
  console.log(problems === 0 && tails.length === 0
    ? '✓ 全部卡片：无超宽行、无折断、行尾无标点'
    : `⚠ ${problems} 张存在超宽/折断，${tails.length} 处行尾标点残留`);

  await b.close();
})();
