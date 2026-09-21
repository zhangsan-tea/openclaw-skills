#!/usr/bin/env node
/**
 * 静心茶海报 · 批量导出卡片为 JPG（puppeteer-core + 本机 Chrome）
 *
 * 用法：
 *   NODE_PATH=<node_modules> node export_cards.js \
 *     --html  静心茶金句卡-9月版-双语.html \
 *     --outdir 海报导出 \
 *     --prefix 202609-双语 \
 *     --sel    '#bcard-{i}'          # 中文版用 '.card-{i}'，双语版用 '#bcard-{i}'
 *     [--count 14] [--quality 94] [--topics '1:宁静叠加,2:信任']
 *
 * 要点（踩过的坑）：
 *  - 卡片 375×667，deviceScaleFactor=2 ⇒ 成品 750×1334；截图前 assert boundingBox 尺寸。
 *  - 必须 `await page.evaluate(() => document.fonts.ready)` + 短延迟，否则字体未就绪会截到回退字形。
 *  - 主题名默认从 HTML 注释 `<!-- ===== NN · 日期 · 主题 ===== -->` 自动提取；
 *    文件名带主题便于人工核对，同时 verify_export.py 按「文件名排序」取成品，编号必须补零。
 *  - 导出后必须跑 verify_export.py 做防串图校验（本脚本只负责截图，不校验）。
 */
const puppeteer = require('puppeteer-core');
const fs = require('fs');
const path = require('path');

const CHROME_CANDIDATES = [
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  '/Applications/Chromium.app/Contents/MacOS/Chromium',
];

function parseArgs(argv) {
  const a = {};
  for (let i = 2; i < argv.length; i += 2) {
    const k = argv[i].replace(/^--/, '');
    a[k] = argv[i + 1];
  }
  return a;
}

function extractTopics(html) {
  const map = {};
  const re = /<!--\s*={3,}\s*(\d+)\s*·\s*(\d+)\s*·\s*([^=]*?)\s*={3,}\s*-->/g;
  let m;
  while ((m = re.exec(html))) {
    map[parseInt(m[1], 10)] = m[3].trim().replace(/[·\s]+/g, '');
  }
  return map;
}

(async () => {
  const args = parseArgs(process.argv);
  if (!args.html) {
    console.error('缺少 --html');
    process.exit(1);
  }
  const outdir = args.outdir || '.';
  const prefix = args.prefix || 'card';
  const selTpl = args.sel || '#bcard-{i}';
  const quality = parseInt(args.quality || '94', 10);

  const html = fs.readFileSync(args.html, 'utf8');
  const topics = extractTopics(html);
  if (args.topics) {
    for (const kv of args.topics.split(',')) {
      const [k, v] = kv.split(':');
      topics[parseInt(k, 10)] = v;
    }
  }
  const count = parseInt(args.count || String(Object.keys(topics).length || 14), 10);

  const chrome = CHROME_CANDIDATES.find(p => fs.existsSync(p));
  if (!chrome) { console.error('未找到 Chrome/Chromium'); process.exit(1); }

  fs.mkdirSync(outdir, { recursive: true });
  const browser = await puppeteer.launch({
    executablePath: chrome,
    headless: 'new',
    // --no-sandbox / --disable-dev-shm-usage：本机（尤其从自动化环境唤起 Chrome 时）
    // 缺这两个参数会偶发 "Protocol error (Emulation.setTouchEmulationEnabled): Session closed"
    // ——浏览器一起来就崩，且报错完全看不出是沙箱问题（2026-09-21 实测）
    args: ['--font-render-hinting=none', '--force-color-profile=srgb',
           '--no-sandbox', '--disable-dev-shm-usage'],
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 500, height: 800, deviceScaleFactor: 2 });
  await page.goto('file://' + path.resolve(args.html), { waitUntil: 'networkidle0', timeout: 60000 });
  await page.evaluate(() => document.fonts.ready);
  await new Promise(r => setTimeout(r, 800));

  let ok = 0, warn = 0;
  for (let i = 1; i <= count; i++) {
    const sel = selTpl.replace('{i}', String(i));
    const el = await page.$(sel);
    if (!el) { console.log(`MISSING ${sel}`); continue; }
    const box = await el.boundingBox();
    if (Math.round(box.width) !== 375 || Math.round(box.height) !== 667) {
      console.log(`WARN card ${i} 尺寸 ${box.width}x${box.height}（应为 375x667）`);
      warn++;
    }
    const topic = topics[i] ? '-' + topics[i] : '';
    const name = `${prefix}${String(i).padStart(2, '0')}${topic}.jpg`;
    const out = path.join(outdir, name);
    await el.screenshot({ path: out, type: 'jpeg', quality });
    console.log(`OK ${name}  ${(fs.statSync(out).size / 1024).toFixed(0)}KB`);
    ok++;
  }
  await browser.close();
  console.log(`\n导出 ${ok} 张，尺寸告警 ${warn} 张。下一步：跑 verify_export.py 做防串图校验。`);
})();
