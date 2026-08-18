---
name: 静心茶英语金句卡
description: 基于波密英文原文×庄西中文翻译素材，生成「跟着波密·庄西学英语」竖版金句卡HTML并导出750×1334px高清JPG海报。
agent_created: true
read_when:
  - 用户要制作英语金句卡/海报
  - 用户提到"英语金句卡"、"跟着波密学英语"、"英语学习卡片"
  - 需要批量生成中英文对照的英语金句图文卡
---

# 静心茶英语金句卡 Skill

---

## 触发词
- "跟着波密·庄西学英语卡片"
- "英语学习金句卡"
- "中英文对照海报"

---

## 前置条件

1. **素材必须预整理**：向用户确认素材来源（7月/8月练习记录）或索取已整理的素材稿（五层结构）。
2. **puppeteer-core**：截图依赖 `puppeteer-core@19`，首次使用需 `cd /tmp && npm install puppeteer-core@19`。
3. **Chrome路径**：macOS 默认 `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`。需 `ls` 确认存在。
4. **二维码图片**：用户必须提供二维码图片附件，转为 Base64 data URI。**禁止用本地路径或网络URL**。

---

## 产出物规格

| 属性 | 值 |
|---|---|
| 卡片宽度 | 375px（固定），高度 `min-height:667px`（自适应，内容多自然增高） |
| 输出分辨率 | 750×1334px 起（deviceScaleFactor:2 高清截图，实际按内容自适应更高） |
| 圆角 | 直角 `border-radius: 0` |
| 二维码定位 | **正常文档流**，作为 `.card-main` 之后的独立同级区块（.qr-footer），不用绝对定位 |
| 输出格式 | JPEG, quality:95 |
| 标签 | 「跟着波密·庄西学英语」（中点间隔） |

---

## ⚠️ 核心教训：二维码与文字重叠/截断问题的根本解法

这是本 skill 最容易踩坑的地方，反复出现过三种失败方案，务必直接采用「最终方案」，不要重复试错：

| 方案 | 做法 | 失败原因 |
|---|---|---|
| ❌ 方案A | `.card` 固定 `height:667px` + 二维码 `position:absolute` 右下角 | 内容长的卡片文字被挤到二维码坐标处，**文字与二维码重叠** |
| ❌ 方案B | `.qrcode` 改为 flex 流式 + `margin-top:auto` | 在固定高度flex容器里行为不稳定：短内容卡片二维码"消失"（被挤出可视区后被 `overflow:hidden` 裁掉），或"居中"（受 `justify-content:center` 影响变成水平居中） |
| ❌ 方案C | 固定 `height:667px` 不变，仅调整 padding/间距 | 内容长的卡片（如五层结构都写满的）文字被 `overflow:hidden` 直接**截断丢字**，比重叠更糟 |
| ✅ **最终方案** | `.card` 改为 `min-height:667px`（**去掉** `overflow:hidden`），二维码作为独立 `.qr-footer` 区块跟在 `.card-main` 后面走正常文档流 | 内容多的卡片自然增高，二维码永远排在文字下方，物理上不可能重叠或被裁 |

**结论：固定高度 + 绝对定位/overflow:hidden 是这类"文字量不固定"卡片的天坑，一律用 min-height 自适应 + 正常文档流二维码。**

---

## HTML 结构与核心 CSS（最终定稿方案）

```html
<div class="card theme-darkgreen">
  <!-- 1. 顶部系列标签：绝对定位，挂在左上角（不占文档流，可以用absolute） -->
  <div class="series-tag">跟着波密·庄西学英语</div>

  <!-- 2. 中间正文容器：flex:1 + justify-content:center 实现垂直居中 -->
  <div class="card-main">
    <div class="card-meta">静心茶 · 存在体</div>
    <div class="english">The night gives this being the stillness, ...</div>
    <div class="label">机器翻译</div>
    <div class="machine">夜晚给了这个身体一份宁静...</div>
    <div class="label">庄西翻译</div>
    <div class="zhuangxi"><strong>黑夜给了这个存在体...</strong></div>
    <div class="divider"></div>
    <div class="contrast"><strong>对比点拨：</strong>...</div>
    <div class="awareness">
      <div class="tiny">觉 察 提 示</div>
      昨晚的沉静...
    </div>
  </div>

  <!-- 3. 底部二维码：独立区块，正常文档流，天然排在card-main之后不会重叠 -->
  <div class="qr-footer">
    <div class="qrcode">
      <div class="qr-box"><img src="data:image/jpeg;base64,..."></div>
      <div class="qr-text">波密静心茶<br>扫码咨询</div>
    </div>
  </div>
</div>
```

### 核心 CSS 样式定义（务必逐条对照，不要改回绝对定位方案）：

```css
  /* 父容器：min-height 而非固定 height，内容多时自然增高，避免裁切/重叠 */
  .card {
    width: 375px;
    min-height: 667px;       /* 关键：不是 height，不加 overflow:hidden */
    border-radius: 0;
    position: relative;
    display: flex;
    flex-direction: column;
    box-shadow: 0 10px 40px rgba(58,53,48,0.16);
    padding: 36px 38px 24px;
    box-sizing: border-box;
  }

  /* 顶部系列徽章：绝对定位，不占常规文档流空间（这个可以用absolute，因为高度固定不受内容影响） */
  .series-tag {
    position: absolute;
    top: 36px;
    left: 18px;
    z-index: 10;
    display: inline-block;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 1.5px;
    padding: 4px 10px 4px 12px;
    border-left: 3px solid currentColor;
    border-top: 1px solid currentColor;
    border-right: 1px solid currentColor;
    border-bottom: 1px solid currentColor;
    border-radius: 0 3px 3px 0;
    background: rgba(255, 255, 255, 0.08);
    opacity: 0.95;
    text-align: left;
  }

  /* 正文容器：flex:1 撑满剩余高度，justify-content:center 让文字整体垂直居中；
     不设固定 padding-bottom 防遮挡，因为二维码不再绝对定位，天然不会重叠 */
  .card-main {
    width: 100%;
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    box-sizing: border-box;
    margin-top: 16px;        /* 顶部给 series-tag 留出气隙 */
  }

  /* 二维码外层容器：正常文档流，排在 card-main 之后，与文字之间天然有间隔 */
  .qr-footer {
    width: 100%;
    display: flex;
    justify-content: flex-end;  /* 二维码靠右 */
    margin-top: 24px;           /* 与上方文字的最小间距，约一行文字高度 */
  }

  .qrcode {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
    opacity: 0.9;
  }

  .qr-box { width: 52px; height: 52px; }
```

---

## 排版细节优化经验
- **切忌加入零碎换行**：英文原文与庄西翻译中避免出现过碎的 `<br>` 换行，利用浏览器的默认流式换行折返，排版更加自然大气。
- **段段间隙拉开，突出呼吸感**：段落间隙放宽到 `12px ~ 24px` 呈现典雅松弛感。
- **12条素材全部统一样式**，通过 6 种配色循环交替呈现高级变化：`.theme-darkgreen` `.theme-lightcream` `.theme-darkbrown` `.theme-lightyellow` `.theme-deepblue` `.theme-lightclay`。
- **不要为了"卡片高度整齐"而牺牲内容完整性**：宁可让个别卡片比 667px 略高（min-height自适应），也不要截断文字或压二维码。

| 元素 | 正常值 | 收紧值（内容过长时可选用，但优先用 min-height 自适应解决，不必强行收紧） |
|---|---|---|
| `.card` padding | 20px 32px 20px | 18px 32px 20px |
| `.english` font-size | 17px | 15.5px |
| `.english` line-height | 1.65 | 1.45 |
| `.label` margin | 10px 0 4px | 3px 0 1px |
| `.machine` font-size | 14.5px | 12px |
| `.machine` line-height | 1.7 | 1.4 |
| `.zhuangxi` font-size | 16.5px | 14px |
| `.zhuangxi` line-height | 1.8 | 1.4 |
| `.divider` margin | 22px 0 18px | 6px 0 4px |
| `.contrast` font-size | 13.5px | 11px |
| `.contrast` line-height | 1.75 | 1.4 |
| `.awareness` margin-top | 14px | 3px |
| `.awareness` font-size | 14px | 11px |
| `.awareness` line-height | 1.7 | 1.4 |
| `.awareness` padding | 12px | 6px 8px 5px |

---

## 截图脚本规范

```javascript
const puppeteer = require('puppeteer-core');
const path = require('path');

(async () => {
  const htmlPath = '.../静心茶英语金句卡-批次.html';
  const outDir = '.../海报输出';
  const browser = await puppeteer.launch({
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  const page = await browser.newPage();
  // viewport 高度要给够（3000px），因为 min-height 自适应卡片可能比 667px 高很多
  await page.setViewport({ width: 1400, height: 3000, deviceScaleFactor: 2 });
  await page.goto('file://' + htmlPath, { waitUntil: 'networkidle0' });
  await page.waitForFunction(() => document.fonts.ready);

  const cards = await page.$$('.card');
  for (let i = 0; i < cards.length; i++) {
    await cards[i].screenshot({
      path: path.join(outDir, `英语金句卡-批次-${i + 1}.jpg`),
      type: 'jpeg',
      quality: 95
    });
  }
  await browser.close();
})();
```

**关键参数**：
- viewport width ≥ 1400px（避免flex挤压card）
- viewport height 给足 3000px（因为 min-height 自适应，卡片可能远超667px，`elementHandle.screenshot()` 会自动按实际内容截取实际高度，无需手动计算）
- `deviceScaleFactor: 2`（否则文字模糊）
- `document.fonts.ready`（字体加载后再截图）
- 用 `elementHandle.screenshot()` 对 `.card` 单独截图，而不是整页截图裁切——这样每张卡片按其真实（可能不同的）高度精确导出，不用手动量高度。

---

## 定稿前必做：逐张人工核查（不能只看CSS就下结论）

CSS 改完后，**必须实际跑一次截图**，把内容最长的几张卡片读出来肉眼检查，因为：
- 固定高度方案下的重叠/截断问题，靠读代码看不出来，必须看渲染结果；
- 不同卡片文字量差异很大，只测1张不能代表全部，至少抽查内容最长的2~3张。

检查清单：
1. 文字有没有被裁切/丢字（尤其是最后一句）
2. 二维码与文字之间是否有清晰间距（目标：约一行文字的空隙）
3. 二维码是否稳定在右下角，没有跑到中间或消失
4. 整体是否垂直居中，不会顶部大片空白+底部拥挤（或反之）

---

## 二维码规范

1. 用户必须提供二维码图片附件。
2. 用Python读取并转为 `data:image/jpeg;base64,...`。
3. 验证JPEG文件头 `FFD8FF` 和文件尾 `FFD9`。
4. 内嵌到HTML所有card的 `<img>` 标签中。
5. **禁止**使用本地文件路径 `file://` 或临时URL。

---

## 输出目录

`.../海报输出/英语金句卡-{批次}-{1..N}.jpg`

导出前确保目录存在：`mkdir -p .../海报输出`

---

## 工作流建议

1. 先只产出/修改 HTML 文件，用 `present_files` 给用户预览确认排版（不要急着截图导出）。
2. 用户确认无误后，才批量运行 Puppeteer 导出最终高清图片。
3. 导出后抽查内容最长的几张卡片图片，确认无重叠/截断，再交付给用户。

---

## 常见故障

| 现象 | 原因 | 解决 |
|---|---|---|
| 文字与二维码重叠 | `.card` 用固定 `height` + 二维码 `position:absolute` | 改用 `min-height` + `.qr-footer` 正常文档流方案 |
| 二维码"消失"或"跑到中间" | flex流式二维码放在固定高度容器内，被挤出可视区或受 `justify-content:center` 影响水平居中 | 同上，改用最终方案；且检查 CSS 是否与 HTML 结构真正对应（历史踩坑：改了8月文件CSS却漏改7月文件CSS，导致新HTML结构配旧CSS） |
| 内容超长文字被截断 | `.card` 固定高度 + `overflow:hidden` | 去掉 `overflow:hidden`，改 `min-height` 让卡片自然增高 |
| 截图文字模糊 | 缺 `deviceScaleFactor` | 设为 2 |
| card宽度<750px | viewport太窄，padding挤压 | viewport≥1400px |
| 二维码403/加载失败 | URL被shell截断或用了网络URL | 用Base64内嵌 |
| 英文换行过早 | `<br>`过多 | 尽量让英文自然换行，只在语义断点插入`<br>` |
| 改CSS只改了一个批次文件 | 多批次（如7月/8月）分别是独立HTML文件，容易漏改 | 每次改结构或CSS后，用 `grep` 检查所有批次文件是否同步一致 |
