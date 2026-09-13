---
name: 静心茶海报
description: 生成静心茶金句卡海报 HTML（375×667px 竖版手机屏尺寸），品牌视觉风格延用既有设计规范。文字人工填充、背景图人工提交、二维码可选延用或自提。
read_when:
  - 用户要制作静心茶金句卡/海报
  - 用户提到"静心茶海报"、"静心茶金句卡"、"金句卡片"
  - 需要批量生成静心茶品牌风格的引语/金句图文卡
---

# 静心茶海报 Skill

生成符合静心茶品牌视觉规范的金句卡 HTML，配合下游 `html-card-poster-export` 技能即可导出高清 JPG 海报。

---

## 快速入口

用户说"帮我做几张静心茶海报"时的工作流：

1. **收集素材**：向用户索取文字内容（副标题 + 金句正文）和背景照片
2. **生成 HTML**：按本 Skill 的模板规范输出 `.html` 文件
3. **导出 JPG**：调用 `html-card-poster-export` 技能完成截图导出

---

## 设计规范（不可更改项）

### 画布

| 属性 | 值 | 说明 |
|---|---|---|
| 尺寸 | 375×667px | 手机屏竖版 |
| 输出倍率 | 3x → 1125×2001px | 导出时由 puppeteer 设置 |
| 圆角 | **直角 `border-radius: 0`** | 不可用圆角，否则手机全屏查看露出底色 |
| 布局 | `flex-direction: column` | 上文字区 + 下照片区 |

### 分区结构

```
┌─────────────────────────────┐
│ 静│                    ← 左上竖排"静心茶"品牌字 (.brand)
│ 心│  ┌───────────────┐       │
│ 茶│  │   副标题关键词  │       │  ← .card-subtitle  11px, letter-spacing:5px, opacity:0.45
│  │  │                │       │
│  │  │   金句正文正文   │       │  ← .quote-text    24px, line-height:1.95, letter-spacing:3px
│  │  │   正文正文正文   │       │     不加句号！多行用 <br>
│  │  │                │       │  ← .card-divider   36px宽 1px高 横线
│  │  └───────┬───────┘       │  ───── 文字区 58% ─────
│  │          │渐变过渡          │  ───── 照片区 42% ─────
│  │  ┌───────┴───────┐       │
│  │  │               │       │
│  │  │   背景照片      │  ┌──┐│  ← 右下毛玻璃二维码 (.qrcode)
│  │  │  object-fit:   │  │QR│ │     backdrop-filter:blur(12px)
│  │  │   cover        │  │文│ │     "中脉空间\n扫码咨询"
│  │  └───────────────┘  └──┘│
└─────────────────────────────┘
```

### 字体

```css
font-family: 'Noto Serif SC', 'Songti SC', 'STSong', serif;
```

- 副标题 `.card-subtitle`：11px，letter-spacing: 5px，opacity: 0.45
- 金句正文 `.quote-text`：24px，font-weight: 400，line-height: 1.95，letter-spacing: 3px，居中
- 品牌字 `.brand`：12px，letter-spacing: 5px，opacity: 0.55，`writing-mode: vertical-rl`

### 排版规则

- 金句正文**不加句号**
- 多行用 `<br>` 分隔，注意避免一两个字折行（可适当微调措辞）
- 副标题关键词用全角空格分隔（如"专 注 当 下"），让视觉更开阔

### 品牌标识 (.brand)

- 位置：`position: absolute; top: 26px; left: 30px;`
- 竖排：`writing-mode: vertical-rl`
- 颜色：`color: inherit`（继承卡片级 color，深色卡自动浅色可见）
- 透明度：`opacity: 0.55`

### 二维码 (.qrcode)

- 位置：`position: absolute; bottom: 10px; right: 10px;`
- 毛玻璃效果：`background: rgba(255,255,255,0.28); backdrop-filter: blur(12px);`
- 圆角容器：`border-radius: 8px`（仅二维码浮层可用圆角，卡片本身不可）
- 二维码图片：38×38px
- 双行文案：`"中脉空间<br>扫码咨询"`，7px 字号，继承卡片 color

---

## 可填充字段

每次生成时，向用户收集以下信息：

| 字段 | 必填 | 说明 | 示例 |
|---|---|---|---|
| **副标题** | ✅ | 关键词，用全角空格分隔 | `专 注 当 下` |
| **金句正文** | ✅ | 多行用 `<br>`，不加句号 | `你观察了世界<br>却没有观察到<br>观察者本身` |
| **背景照片** | ✅ | 提供图片路径或由 AI 生成 | `photos/01.jpeg` |
| **配色方案** | ❌ | 从配色池选序号，或自定义渐变 | `card-3` 或自定义 |
| **二维码图片** | ❌ | 不填则延用 `photos/qrcode.jpg` | `photos/qrcode.jpg` |
| **二维码文案** | ❌ | 不填则延用"中脉空间 / 扫码咨询" | `静心空间<br>扫码关注` |

如果用户未指定配色，按深浅交替原则自动分配（第1张深色、第2张浅色、第3张深色……）。

---

## 背景照片选择与判重（强制，最容易出错的一步）

### ⚠️ 铁律：判重必须按**图像内容**，不能按文件名

`photos/` 目录里混着**两套命名的同一批照片**（`IMG_xxxx.jpeg` 与 `<UUID>_x_xxxx_c.jpeg`，以及 `已用/` 子目录里的副本）。同一张照片可能有 2-3 个不同文件名的副本。

因此**按文件名筛选"未使用照片"一定会翻车** —— 会选出早已用过的照片的另一个副本。同时 `used-photos.json` 是按文件名记录的，照片一旦改名即失效，不能作为判重依据。

### 唯一可信的真值来源

| 来源 | 可信度 | 说明 |
|---|---|---|
| **所有历史 HTML 实际引用的 `photos/xxx`** | ✅ 权威 | 扫 `*.html` 提取，排除当前批次自身 |
| `photos/已用/` 子目录 | ✅ 权威 | 归档的已用照片 |
| `used-photos.json` | ⚠️ 参考 | 按文件名记录，改名即失效，仅用于辅助 |

### 判重算法：dhash + 汉明距离

```python
from PIL import Image
def dhash(p, s=16):                     # 256-bit 感知哈希
    im = Image.open(p).convert("L").resize((s+1, s), Image.LANCZOS)
    px = list(im.getdata()); b = 0
    for r in range(s):
        for c in range(s):
            b = (b << 1) | (1 if px[r*(s+1)+c] < px[r*(s+1)+c+1] else 0)
    return b
def ham(a, b): return bin(a ^ b).count("1")
```

**通过标准**（256-bit 尺度）：

| 对比对象 | 阈值 | 含义 |
|---|---|---|
| 与**历史已用**照片 | `ham > 10` | 不能撞任何历史批次用过的图 |
| 与本批次**其余**照片 | `ham > 10` | 本批次内部不重复 |
| 实测健康值 | 与历史 ≥ 90，与本批 ≥ 100 | 低于 30 视为可疑，需人工看图 |

### 机器判重不够，必须**用眼看一眼拼图**

dhash 只看整体明暗梯度，**对"同题材不同构图"不敏感**。以下情况 dhash 判不出、但人眼一眼看出重复，必须人工复核：

- 同场景连拍（同一片花田的 3 张）
- 同构图不同地（都是"绿林中间一条小径+透视消失点"）
- 题材扎堆（14 张里 5 张绿色田野 / 4 张雪山）

**标准动作**：把候选做成带编号的网格拼图 PNG，自己 Read 一遍再定稿。拼图同时也发给用户确认。

### 题材配比建议（14 张批次）

避免单一题材超过 4 张。推荐配比：

| 题材 | 建议张数 |
|---|---|
| 水（湖/海/倒影/雨） | 3 |
| 山与云（雪山/云海/雾） | 3 |
| 植被（林/野/花/枝） | 4 |
| 禅意建筑与器物（回廊/檐角/佛塔/石雕） | 2 |
| 抽象与光（云朵特写/极简海天） | 2 |

**调性红线**：静心茶海报背景禁用 —— 现代城市天际线、机场跑道、飞机、工业设施、多人合影、有明显时代感的建筑。优先选空灵、留白、有静气、光线柔和的画面。

### 执行顺序（每批必跑）

1. 扫描全部历史 `*.html` + `photos/已用/`，建"已用内容集"
2. 对候选池与已用集算 dhash，筛出 `ham > 10` 的候选
3. 候选之间也做 `ham > 10` 去重
4. **生成候选拼图 → 人工看图**，按题材配比挑选
5. 定稿后再做一次最终校验（14 张彼此 + 与历史）
6. 生成"最终 14 张一览图"留档，文件名 `<批次名>-背景图一览.png`

---

## 配色方案池

预制的 12 套配色（深色/浅色交替），每套包含：

1. 卡片级 `color`（文字颜色，品牌字和二维码文案继承）
2. `.card-text-area` 背景渐变（文字区底色）
3. `.card-photo-area::before` 顶部渐变（与文字区底部平滑过渡）

### 12 套配色速查

| 序号 | 类型 | 文字区渐变 | 文字色 |
|---|---|---|---|
| 1 | 深色 | `linear-gradient(160deg, #2c3e34, #1a221c)` | `#e8e0d4` |
| 2 | 浅色 | `linear-gradient(160deg, #f5ede0, #e8d9c4)` | `#5e4e3d` |
| 3 | 深色 | `linear-gradient(160deg, #3d2e2a, #221712)` | `#dcc8b8` |
| 4 | 浅色 | `linear-gradient(160deg, #e8dccf, #d4c0a8)` | `#6b5a4a` |
| 5 | 深色 | `linear-gradient(160deg, #2a3a4e, #141d2e)` | `#cee0f0` |
| 6 | 浅色 | `linear-gradient(160deg, #efe6da, #ddd0bd)` | `#574a3e` |
| 7 | 深色 | `linear-gradient(160deg, #3e2a3e, #241524)` | `#e8c8e0` |
| 8 | 浅色 | `linear-gradient(160deg, #f0e4dc, #ddc8b8)` | `#5e4e42` |
| 9 | 深色 | `linear-gradient(160deg, #2e3a2e, #16221a)` | `#d0e0c8` |
| 10 | 浅色 | `linear-gradient(160deg, #eae6dc, #d2ccb8)` | `#4e4e3e` |
| 11 | 深色 | `linear-gradient(160deg, #42342a, #261c16)` | `#e4d0c0` |
| 12 | 浅色 | `linear-gradient(160deg, #f2eae0, #e0d0c0)` | `#5a4a3e` |

> **扩展**：用户也可自定义配色，只需提供两个字段：文字色和文字区域的线性渐变方向+色值。

---

## 卡片 DOM 模板

```html
<div class="card card-N">
  <div class="brand">静心茶</div>
  <div class="card-text-area">
    <div class="card-subtitle">副 标 题</div>
    <div class="quote-text">金句正文<br>第二行<br>第三行</div>
    <div class="card-divider"></div>
  </div>
  <div class="card-photo-area">
    <img src="photos/背景图.jpeg" alt="">
  </div>
  <div class="qrcode">
    <img src="photos/qrcode.jpg" alt="">
    <div class="qr-caption">中脉空间<br>扫码咨询</div>
  </div>
</div>
```

---

## 完整 HTML 骨架

生成新批次时，从 `templates/template.html` 复制骨架文件，修改以下位置：

1. `<title>` 改为批次名
2. 复制 `.card-N` 配色块（按需数量）
3. 逐张填充文字内容和图片路径
4. 默认所有卡片共用同一二维码图，如需不同则逐张替换

---

## 交付预览：必须额外生成自包含版（必做）

**踩过的坑**：把带相对路径（`photos/xxx.jpeg`）的 HTML 直接丢给预览面板，浏览器只拿到 HTML 文件本身，同级 `photos/` 目录不在服务范围内 → 14 张背景图与二维码全部 404，用户看到的是一堆空白卡片，会直接反馈"没看到产物"。

**正确做法**：主 HTML 保持相对路径（供 Puppeteer 导出用，**不要动**），另存一份 `xxx-预览.html`，把所有 `src` 换成 base64 data URI 再交付预览。

```python
import re, io, base64
from PIL import Image

html = open(src_html, encoding='utf-8').read()
cache = {}
def embed(rel):
    if rel in cache: return cache[rel]
    im = Image.open(rel).convert('RGB')
    if 'qrcode' in rel:
        im.thumbnail((240, 240), Image.LANCZOS); q = 90
    else:
        im.thumbnail((760, 760), Image.LANCZOS); q = 82   # 2x 显示宽度，够用
    buf = io.BytesIO(); im.save(buf, 'JPEG', quality=q, optimize=True)
    uri = 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()
    cache[rel] = uri
    return uri

out = html
for s in sorted(set(re.findall(r'src="([^"]+)"', html))):
    out = out.replace(f'src="{s}"', f'src="{embed(s)}"')
open(dst_html, 'w', encoding='utf-8').write(out)
assert len(re.findall(r'src="(?!data:)', out)) == 0   # 确认无残留外部引用
```

**体积参考**：14 张卡（14 背景图 + 共用二维码）压缩后约 **1.3 MB**，预览面板可正常加载。
照片原图单张可达 4 MB（整库 300 MB+），**必须先压缩再内嵌**，否则预览会卡死。

---

## 下游导出

HTML 生成完毕后，调用 `html-card-poster-export` 技能（**用主 HTML，不是预览版**）：

1. 用 puppeteer-core + Chrome 远程调试端口（9333）
2. 每张 `.card` 截图为 1125×2001px（3倍率）的 JPG
3. 输出到指定目录

> ⚠️ puppeteer 新版已移除 `page.waitForTimeout`，等待须用 `await new Promise(r => setTimeout(r, 300))`

---

## 工作流示例对话

用户："帮我做3张静心茶海报，主题是'放下'"

助手：
1. 写出3条金句草案 → 用户确认/修改
2. 向用户索取3张背景照片（或建议用 AI 生成）
3. 选择配色方案（自动分配深浅交替，如 card-1/card-2/card-3）
4. 生成 HTML 文件
5. 调用 `html-card-poster-export` 导出 JPG
6. 交付海报文件

---

## 扩展模式：模块分区标签（跨卡片系列使用）

当同一批次有多张卡片需要分模块、且会被碎片传播时，可在卡片顶部右上角增加模块标识标签。

### 设计规范

```
╔═════════════════════════════════╗
║ 系列标签          ● 模块完整名称  ║  ← .card-header（flex两端对齐）
║                                 ║
║      …卡片主体内容…               ║
╚═════════════════════════════════╝
```

**标签格式**：`前缀 · 字母 · 模块名`  
**示例**：`冥想核心词 · A · 认知层`、`常见组合 · C · 常见组合`

### CSS 示例

```css
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}
.module-tag {
  font-size: 9px;
  font-weight: 600;
  letter-spacing: 2px;
  opacity: 0.6;
  white-space: nowrap;
  display: flex;
  align-items: center;
  gap: 5px;
}
.module-tag .mod-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  display: inline-block;
}
/* 每个主题模块分配专属圆点色 */
.theme-darkgreen .mod-dot { background: #8dba9f; }
.theme-darkbrown .mod-dot { background: #c4a87a; }
.theme-deepblue .mod-dot { background: #7fa3c8; }
```

### HTML 结构

```html
<div class="card theme-darkgreen">
  <div class="card-header">
    <div class="series-tag">跟着波密·庄西学英语</div>
    <div class="module-tag"><span class="mod-dot"></span>冥想核心词 · A · 认知层</div>
  </div>
  <!-- 正文 -->
</div>
```

### 要点

- 模块字母用大写英文字母（A/B/C…），前缀用中文描述系列类型
- 圆点色必须与卡片主题色呼应，每个模块独立一个色值
- 标签透明度 0.6，保持低调但可读
- 碎片传播时即使没看到系统性分区 banner，单张卡片也能传达归属信息

