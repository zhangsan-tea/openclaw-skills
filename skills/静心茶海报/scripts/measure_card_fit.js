const puppeteer = require('puppeteer-core');
(async () => {
  const file = process.argv[2] || '/Users/sanzhang/企业云同步盘/海报制作素材/静心茶金句卡-9月版-双语.html';
  const b = await puppeteer.launch({ headless: true, executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', args: ['--no-sandbox', '--disable-setuid-sandbox'] });
  const p = await b.newPage();
  await p.setViewport({ width: 375, height: 667, deviceScaleFactor: 2 });
  await p.goto('file://' + file, { waitUntil: 'networkidle0' });
  await p.evaluate(async () => { await document.fonts.ready; });
  await new Promise(r => setTimeout(r, 2000));
  const res = await p.evaluate(() => {
    const out = [];
    document.querySelectorAll('.card').forEach((c, i) => {
      const ta = c.querySelector('.card-text-area');
      const cs = getComputedStyle(ta);
      const avail = ta.getBoundingClientRect().height - parseFloat(cs.paddingTop) - parseFloat(cs.paddingBottom);
      const flow = [...ta.children].filter(e => !e.classList.contains('brand-label'));
      const top = Math.min(...flow.map(e => e.getBoundingClientRect().top));
      const bottom = Math.max(...flow.map(e => e.getBoundingClientRect().bottom));
      const info = (sel) => {
        const el = c.querySelector(sel);
        if (!el) return null;
        const r = document.createRange();
        const lines = [];
        el.childNodes.forEach(n => {
          const txt = (n.textContent || '').trim();
          if (!txt) return;
          r.selectNodeContents(n);
          const rects = [...r.getClientRects()].filter(x => x.width > 1);
          lines.push({ t: txt, n: txt.length, rects: rects.length, w: Math.round(Math.max(...rects.map(x => x.width))) });
        });
        const boxW = Math.round(el.getBoundingClientRect().width);
        return { boxW, lines, wrapped: lines.filter(l => l.rects > 1) };
      };
      out.push({
        card: i + 1,
        tag: c.querySelector('.day-tag').textContent.trim(),
        slack: Math.round(avail - (bottom - top)),
        en: info('.quote-en'), cn: info('.quote-chinese')
      });
    });
    return out;
  });
  res.forEach(r => {
    const no = (r.card < 10 ? '0' : '') + r.card;
    const bad = [r.en, r.cn].filter(Boolean).map(o => o.wrapped.length).reduce((a, b) => a + b, 0);
    console.log(`卡${no} ${r.tag} | 余量 ${r.slack} | 容器宽 ${r.en ? r.en.boxW : '-'} | 折行 ${bad}`);
    if (bad) {
      [r.en, r.cn].filter(Boolean).forEach(o => o.wrapped.forEach(l => console.log(`      ✗ 折${l.rects}行 n=${l.n}: ${l.t}`)));
    }
  });
  await b.close();
})().catch(e => { console.error(e); process.exit(1); });
