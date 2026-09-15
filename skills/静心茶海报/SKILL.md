---
name: 静心茶海报
description: 生成静心茶金句卡海报 HTML（375×667px 竖版手机屏尺寸），品牌视觉风格延用既有设计规范。文字人工填充、背景图人工提交、二维码可选延用或自提。
read_when:
  - 用户要制作静心茶金句卡/海报
  - 用户提到"静心茶海报"、"静心茶金句卡"、"金句卡片"
  - 需要批量生成静心茶品牌风格的引语/金句图文卡
---

# 静心茶海报 Skill

生成符合静心茶品牌视觉规范的金句卡 HTML，使用本 Skill 自带的 `scripts/export_cards.js` 导出 750×1334 高清 JPG 海报，并以 `scripts/verify_export.py` 防串图校验。

---

## 快速入口

用户说"帮我做几张静心茶海报"时的工作流：

1. **收集素材**：向用户索取文字内容（副标题 + 金句正文）和背景照片
2. **生成 HTML**：按本 Skill 的模板规范输出 `.html` 文件
3. **导出 JPG**：跑 `scripts/export_cards.js`（本技能自带）⇒ 750×1334，导出后跑 `scripts/verify_export.py` 防串图

> `scripts/` 现有：`export_cards.js`（批量导出）、`verify_export.py`（防串图校验）、
> `measure_card_fit.js`（余量/行宽/折行实测）、`photo_dupe_check.py`（选图判重）。
> 新增脚本一律落这里，**不要留在 `/tmp`**——被系统清理后只能重写。

---

## 设计规范（不可更改项）

### 画布

| 属性 | 值 | 说明 |
|---|---|---|
| 尺寸 | 375×667px | 手机屏竖版 |
| 输出倍率 | **2x → 750×1334px**（q94） | 导出时由 puppeteer 设置，见「下游导出」 |
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

- 位置：`position: absolute; top: 26px; left: 30px;`（**必须左上角**）
- 竖排：`writing-mode: vertical-rl`
- 颜色：`color: inherit`（继承卡片级 color，深色卡自动浅色可见）
- 透明度：`opacity: 0.55`

> ⚠️ **位置纠偏（2026-09-14 用户明确要求）**：品牌字「静心茶」一律放**左上角**。
> 九月版实物误放在右上（`top:18px; right:18px; opacity:.35`），用户指出"改放左上角，看起来画面更平衡"。
> 新建/改版时一律左上；**右上角只留给模块标识标签**（见后文分模块章节）。

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
| `used-photos.json` | ⚠️ 参考 | 按文件名记录，改名即失效，**唯一不可替代的用途是「黑名单」**（用户指定退役的画面，只存在这里） |

> **⚠️ 踩过的坑（2026-09-13 第四轮）**：自己写临时脚本筛候选时，只从 `used-photos.json` 读历史集，没扫历史 HTML，结果选中的 `IMG_8043` 其实已在「横幅版」HTML 里用过，`check` 才报 d=0。
> **硬性要求：筛候选一律用 `photo_dupe_check.py candidates`（它内部调 `build_used_set()`，与 `check` 同源），不要再自己写临时脚本。** 换批次中某几张时用 `--batch-html <本批HTML>` 一次拿到「距历史 + 距批内」双距离。

### 清晰度门槛（**先过滤，再判重** —— 顺序不能反）

用户在手机上看到的"糊"，根源是选到了 iCloud 同步下来的**缩略图**。`photos/` 里同一张照片常有多种规格，缩略图混在其中，选图时必须先按清晰度过滤。

**门槛按导出尺寸判定，不是按"长边≥1000"**：

| 判据 | 值 | 说明 |
|---|---|---|
| 导出卡片 | 750 × 1334 px | `deviceScaleFactor: 2` 下的输出尺寸 |
| **图片区** | **750 × 494 px** | 实际占图区域 = 卡高 37% × 2 |
| **合格条件** | **`w ≥ 750` 且 `h ≥ 494`** | 两者都要满足，只看长边会漏掉"长边够但宽不够"的竖图 |
| 放大倍数 | `max(750/w, 494/h)` | `≤ 1.0` 合格；`≤ 1.15` 可接受；`> 1.5` 必须换 |

**规格对照表**（文件名后缀 → 分辨率，实测）：

| 后缀/命名 | 典型分辨率 | 判定 |
|---|---|---|
| `<UUID>_4_5005_c` | 310×552、360×480、552×310、672×360 | ❌ **缩略图，一律排除** |
| `<UUID>_1_105_c` | 664×1182、1182×664、768×1024 | ⚠️ 多数合格，竖版 664 宽会差一点（1.13×） |
| `<UUID>_1_102_a` | 1330×2364 | ✅ 合格 |
| `<UUID>_1_102_o` | 1536×2048 | ✅ 合格 |
| `IMG_xxxx` / `DSC_xxxx` | 3000 ~ 8000 长边 | ✅ 原图，最优 |

**同图高清版优先（重要）**：同一张照片常同时有 `_4_5005_c`（缩略）与 `_1_102_a`（高清）两个文件，**是同一张图**。发现低清版时不要急着换画面 —— 先找同 UUID 的高清版：

```python
uuid = name.split('_')[0]                    # 文件名第一段即 UUID
cands = [f for f in allfiles if f.startswith(uuid)]
# 用 dhash 确认是同一张（ham <= 12），再取分辨率最高的那个
```

**判重与清晰度的协作顺序**：
1. 先按清晰度过滤候选池（排除 `_4_5005_c`，保留 `w≥750 且 h≥494`）
2. 对**在用的**缩略图，先找同 UUID 高清版；找不到才换画面
3. 再做 dhash 判重（与历史、与批内）
4. 最后人工拼图复核题材配比

### 判重算法：dhash + 汉明距离

```python
from PIL import Image, ImageOps
def dhash(p, s=16):                     # 256-bit 感知哈希
    im = Image.open(p)
    im = ImageOps.exif_transpose(im)    # ① 先摆正：哈希必须反映"实际渲染的样子"
    im = im.convert("L")
    im = ImageOps.equalize(im)          # ② 再均衡：暗图恢复结构（见下方陷阱说明）
    im = im.resize((s+1, s), Image.LANCZOS)
    px = im.tobytes(); b = 0            # 灰度图 tobytes = 行优先单字节序列（避免 getdata 弃用告警）
    for r in range(s):
        row = r * (s + 1)
        for c in range(s):
            b = (b << 1) | (1 if px[row+c] < px[row+c+1] else 0)
    return b
def ham(a, b): return bin(a ^ b).count("1")
```

**这两个预处理不是可选优化，是必需的** —— 漏掉任一个都会导致漏判：

| 陷阱 | 现象 | 后果 | 修复 |
|---|---|---|---|
| **极暗图梯度退化** | 夜景/烛光等图均色 < `rgb(30,30,30)`，梯度几乎全为 0，哈希位由噪声主导 | 两张**毫不相干**的暗图也算出偏小距离。实测：一对真·近重复图原始 `d=27`（看着像不同图），均衡后 `d=10`（正确判定为撞） | `equalize` 直方图均衡后再取梯度 |
| **EXIF 方向未应用** | 磁盘像素与用户所见画面差 90° | 哈希算的是磁盘版本，判重与实际观感脱节 | `exif_transpose` 摆正后再算 |

对照组实测（均衡后）：同图 `0`、正常不同图 `136`、真·近重复暗图 `10`。正常光照图均衡前后距离不变，无副作用。

判定为"近重复"的**强信号**：两张图**整幅均色完全相同**（如都恰为 `rgb(21,14,9)`）+ `dhash8 d ≤ 3`。出现这个组合时，即使 `dhash16` 距离超过阈值，也要按撞图处理。

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

1. 扫描全部历史 `*.html` + `photos/已用/` + `used-photos.json` 黑名单，建"已用内容集"
   —— 直接用 `candidates` 子命令（内部 `build_used_set()` + `load_blacklist()`），不要自己写脚本
2. **按清晰度过滤**：排除 `_4_5005_c` 缩略图，保留 `w≥750 且 h≥494`（见上一节）
3. 对候选池与**历史已用集**算 dhash，筛出 `ham > 10` 的候选
4. 候选之间**以及候选与本批保留的图**都做 `ham > 10` 去重
   （一次拿到：`candidates --batch-html 本批.html` 会同时输出「距历史」与「距批内」两列）

   > ⚠️ **这两步必须都做，且顺序不能省**。上一轮就是只做了第 4 步（比"与本批保留图的距离"），漏了第 3 步（比"与历史已用集的距离"），结果新选的 3 张全部撞上历史的另命名副本（`A529B602`→`IMG_4848`、`IMG_8328`→`15AFAF64`、`88F6AA80`→`new3`），白换一轮。
   > 选图时把**两个距离一起打出来**核对：`距历史` 与 `距批内`，两个都要 ≥ 80 才保险。
5. **生成候选拼图 → 人工看图**，按题材配比挑选（按 750×494 cover 裁切预览，看实际入画效果）
6. 定稿后再做一次最终校验（14 张彼此 + 与历史 + 清晰度）
7. **整卡渲染复核**（关键，换图后必做）：用 Puppeteer 截图看每张卡的完整效果，确认
   - 图片区顶部与文字区底色的渐隐过渡（`.card-N .card-photo-area::before` 的起点色）没有出现色带穿帮
   - 若新图顶部色与该卡渐变起点色差异过大，需按新图顶部主色改 `::before` 起点色
8. 生成"最终 14 张一览图"留档，文件名 `<批次名>-背景图一览.png`（红框标出本轮换过/升级过的卡）

### 用户指定"这张以后都别用了"时的处理（退役流程）

用户点名要换掉某张背景、且说"后续不再使用"时，光改 HTML 不够 —— 下次选图还会把它（或它的另命名副本 / 高清版）选回来。必须**三处同时落地**：

1. **HTML**：替换该卡 `src`
2. **`used-photos.json` → 黑名单**：新增 item，`pattern` 用 **UUID 前缀**（UUID 命名）或 **文件名前缀**（`IMG_xxxx` 命名），这样同图的其它规格一并封禁；把 `reason` 写清是哪张卡、哪天、为什么
3. **`used-photos.json` → `all_used`**：把退役文件名加入（含同图的其它命名副本，如 `IMG_7558.jpeg` 与 `IMG_7558-r90.jpeg`）

脚本侧已配套：`load_blacklist()` 会在 `candidates` 里过滤这些 pattern（2026-09-13 补上 —— 之前脚本不读 JSON 黑名单，退役图会被重新选中）。

> ⚠️ 改 `used-photos.json` 前**先 `cp` 一份到 /tmp**（该目录无 git）。`早期批次已用` 是 `{"说明":…,"photos":[…]}` 结构，取 `.photos`，别当 list 遍历 —— 踩过一次，把 `all_used` 从 79 缩到 65。

### 换图后的两个连带检查

| 检查项 | 方法 | 处理 |
|---|---|---|
| **EXIF 方向** | `Image.open(p).getexif().get(274)`，若为 5/6/7/8 则横躺风险 | `ImageOps.exif_transpose()` 烧录方向另存 `-r90.jpeg`，清掉 orientation 标记 |

同一批照片里往往混有竖持拍摄的图，**每批都应全量查一遍 EXIF**，不要只查用户指出的那一张。上一轮就因为只查新换的 3 张，漏掉了卡 05 的 `orient=6`。

#### 关于"渐隐过渡色"——不要用色差数值做硬判据

`.card-photo-area::before` 的渐变起点色**就是该卡文字区底色**（如 `#1a2634`），这是设计意图：让图片顶部压暗、平滑融进深色文字区。因此**图片顶部色与起点色差异大是常态**（实测 14 张里有 10 张 `|Δr|+|Δg|+|Δb| > 150`，全部渲染正常）。拿这个数值当阈值改配色，会把正常设计改坏。

真正的判据是**渲染后的色带检测**，对整卡截图逐行取均色：

| 指标 | 取法 | 合格线 |
|---|---|---|
| 交界硬边 | 文字区/图片区交界上下各 3 行，相邻行最大 `Σ|ΔRGB|` | `< 60` |
| 渐隐色带 | 图片区顶部 35% 带内，相邻采样行最大 `Σ|ΔRGB|` | `< 25` |
| 图片区有内容 | 图片区下半部分缩到 32×16 后的 RGB 标准差 | `> 12`（过小说明是纯色/空白） |

只有这三项不合格时才调 `::before` 起点色。

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

## 变体：中英对照双语卡（2026-09 新增）

从**纯中文金句卡**反向做双语版：选中文字少的卡 → 找波密英文原话 → 同卡上下对照。
英文原文去 `~/obsidian-private/向内看/静心茶/练习记录/YYYYMMDD_静心茶练习.md` 按关键词（`camera`/`trust`/`light and dark`/`listener`/`observer` 等）grep **Bommie** 段落。

### ⚠️ 品牌标签（2026-09-14 踩坑纠正）
双语金句卡**只有** `静心茶` 竖排角标 + `日期 · 主题` 标签，**不加任何系列标签**。
`跟着波密 · 庄西学英语` 属于**另一个项目**（英语金句卡：英文原文/机翻/庄西译/对比点拨/觉察提示五层），
不可混用到金句卡上。

### DOM 与视觉层级
```
day-tag（0907 · 信任）
→ quote-en（辅，15.5px，opacity .76）
→ bi-divider（28×1px，opacity .22，margin: 18px 0 16px）
→ quote-chinese（主，16.5px，opacity .96，letter-spacing 2.5px，line-height 1.9）
```
中文为主、英文为辅，靠**字号 + 透明度**拉开，差异要克制（用户原话："中文更突出，但差异不要太明显"）。

**长英文行收窄用类名，不要用 `.card-N`**：卡数会增减，位置类名必然错位。
```css
.en-xs { font-size: 13.5px; letter-spacing: 0; line-height: 1.75; }
.en-sm { font-size: 14.5px; letter-spacing: 0; line-height: 1.72; }
```

### 选卡判据（实测校准，375×667）
- text-area = 63% = 420px，padding 30/14 ⇒ **可用 376px**；加了 `.tight` 后 **可用 404px**
- 固定抬头（day-tag + margin 20 + divider 35）≈ **90px**（早期记的 71px 偏小，按 90 算才准）
- **中文行 ≈ 31.4px**（16.5×1.9）；**英文行 ≈ 26.4px**（15.5×1.7）；en-xs 行 ≈ 23.6px
- **行宽上限（硬约束，超了就折行）**：容器内容宽 **323px**
  - 中文 16.5px + 2.5px 字距：**≤17 字**安全（17 字实测 298px），**18 字必折**（311px）
  - 英文 15.5px：**单行宽 ≤300px**（约 41 字符）
  - 英文 `.en-xs` 13.5px：**单行宽 ≤300px**（约 45 字符；含 `synchronicity` 这类长词要更短）
- 结论：中文 **≤7 行**基本可容纳；**8 行以上**必须并行 / 局部收紧 / 交替换行

### ⭐⭐⭐ 保内容优先：能并行解决的，绝不删内容（2026-09-14 用户定稿，最高优先级）

> 用户原话："从分别开始，后面几张的内容，精简之后，感觉原有的味道消失了。再调整一下，
> **能用并行解决的，就不要精简内容**；要精简，也尽量在**原版本的基础上做少量的压缩**。"

**调整顺序（从上到下，能解决就停，不要跳到删除）**：

| 顺序 | 手段 | 说明 |
|---|---|---|
| 1 | **并行短句** | 语义同组的短句用空格并入一行，**一个字都不删**。这是首选手段 |
| 2 | **英文压行数** | 中文是主、英文是辅：英文从 4 行并成 3 行、或换 `.en-sm`/`.en-xs`，腾出的空间全给中文 |
| 3 | **局部收紧留白** | 给该卡加 `.tight`（`padding-top:18px; padding-bottom:8px;`、`.bi-divider{margin:12px 0 10px;}`），单卡省约 28px，不影响其他卡 |
| 4 | **超长卡微调中文行距** | 给该卡加 `.cn-snug`（`font-size:16px; line-height:1.7; letter-spacing:2px;`）。原中文版对最长卡本来就用 `dense`（16px/1.6），故这是沿用旧规 |
| 5 | **最后才少量压缩** | 只删虚词（"的/会/去"）或在原句上做最小改动，**保留原句的用词与节奏**，不要重写 |

**绝对不要做的**：把一个 9 行的原卡压成 5 行、把排比句拆散、把结尾句整句删掉——这就是"味道消失"。
特别地：**排比句（"不需要困惑 / 不需要评论 / 不需要贴任何标签"、"从比较到合一 / 从分离到合一"）
一句一行，不许并**；语义转折处不并。

### ⭐⭐ 分行优先，并行为辅

**默认按语义分行，不要主动合并。** 短句各占一行是原卡自带的**呼吸节奏**，读起来更透气。

| 情形 | 做法 |
|---|---|
| **内容短**（中文 ≤6 行） | **保持原有分行，一个字都不要并。** 光与暗卡 3 行、余量 133px 是理想状态 |
| **内容长**（中文 ≥7 行） | **先按上面的 5 级顺序腾空间**；确实放不下才并句，且只并在最适合的那几处 |

⚠️ **「短句并一行」是应急手段，不是默认手法**（用户原话："这并不是一个强行的要求，
是一个方法的提示…能分行也尽量分行，不用把所有短句全合并到一行"）。

**冲突时的优先级：内容完整 + 分行节奏 > 留白余量。** 宁可余量压到 24px，也不要为了宽松而删句。

> 2026-09-14 两轮修正：
> ① 第一版把 14 张里大部分短句都并了，被否决 → 恢复分行（余量 24–133px）。
> ② 第二版为了塞进版面，把卡 9–14 大幅精简（9 行→5 行、删掉结尾句），用户指出"味道消失了"
> → 改用「并行 + 压英文 + `.tight` + 卡14 用 `.cn-snug`」，卡 9–14 中文回到 6–8 行、
> 内容基本全保，实测余量 46–54px、零折行。

### 双项实测（必做，用脚本跑）

```bash
NODE_PATH=/Users/sanzhang/.workbuddy/binaries/node/workspace/node_modules \
/Users/sanzhang/.workbuddy/binaries/node/versions/22.22.2-3/bin/node \
~/.workbuddy/skills/静心茶海报/scripts/measure_card_fit.js "<卡片 HTML 绝对路径>"
```

1. **余量** `avail - content ≥ ~35px`；<20px 视觉上偏挤，先走上面 5 级顺序腾空间。
2. **折行** 逐行用 `Range.getClientRects().length > 1` 判定。

> ⚠️ **折行检测的致命陷阱**：早期用"该行高度 > 最小行高 ×1.6"判定，当**整卡所有行都折行**时
> 最小行高本身就是折行高度，判定会**静默返回 0 折行**——实测卡13 曾报"0 折行"但余量 -34px
> （真实是 3 行英文全折）。**一律用 `getClientRects().length`，并与余量互相印证**：
> 余量为负却有"0 折行"= 检测失效，不是没问题。

超宽时的处理顺序：**改短句 > 换 `.en-sm`/`.en-xs` > 再缩字号**（13.5px 已是下限）。
⚠️ 别用 `getBoundingClientRect` 累加子树高度做溢出检测，会得出荒谬数值（实测报过 2850px）。

---

## 下游导出

HTML 生成完毕后，**直接跑本技能自带脚本**（用主 HTML，不是预览版）：

```bash
cd "<素材目录>"
NODE_PATH=/Users/sanzhang/.workbuddy/binaries/node/workspace/node_modules \
  /Users/sanzhang/.workbuddy/binaries/node/versions/22.22.2-3/bin/node \
  ~/.workbuddy/skills/静心茶海报/scripts/export_cards.js \
  --html 静心茶金句卡-9月版-双语.html \
  --outdir 海报导出 --prefix 202609-双语 --sel '#bcard-{i}'
```

| 参数 | 说明 |
|---|---|
| `--sel` | 中文版用 `.card-{i}`；双语版用 `#bcard-{i}` |
| `--prefix` | 文件名前缀；脚本自动补零编号 + 从注释提取主题名 ⇒ `<前缀>NN-<主题>.jpg` |
| `--count` | 默认从注释条数推断（14） |
| `--quality` | 默认 94 |

脚本内置：等字体就绪（`document.fonts.ready` + 800ms 缓冲）、逐卡尺寸 assert（≠375×667 告警）、
自动建输出目录。**导出后紧接着跑 `verify_export.py`**（见下）。

> ⚠️ puppeteer 新版已移除 `page.waitForTimeout`，等待须用 `await new Promise(r => setTimeout(r, 300))`
> ⚠️ 导出脚本曾只存在于 `/tmp`，被系统清理后不得不重写——**凡是要复用的脚本，一律落进 `scripts/`**。

### 静心茶金句卡的标准导出参数（已验证，直接复用）

```js
await page.setViewport({ width: 375, height: 667, deviceScaleFactor: 2 });  // → 750×1334
await page.goto('file://' + htmlPath, { waitUntil: 'networkidle0' });
await page.evaluate(async () => {            // 等字体 + 全部图片
  await document.fonts.ready;
  await Promise.all([...document.querySelectorAll('img')].map(img =>
    img.complete ? null : new Promise(r => { img.onload = r; img.onerror = r; })));
});
await new Promise(r => setTimeout(r, 2500));  // 缓冲，2s 够、2.5s 更稳
await el.screenshot({ path, type: 'jpeg', quality: 94 });
```
- 逐张 `page.$('.card-N')` 截图，文件名沿用 `<批次>-NN-<主题>.jpg`（导出前先 `ls` 目标目录，避免编号撞车）
- **导出前先 `ls` 检查编号是否被占**：曾发生旧批次误用 `202609-01..07`、与新批次撞号的事故

### ⚠️ 导出后必做：防串图校验（必做，不要靠肉眼）

```bash
/usr/bin/python3 ~/.workbuddy/skills/静心茶海报/scripts/verify_export.py \
  --html 静心茶金句卡-9月版.html --dir 海报导出 --prefix 202609
```

- 判定用**相对距离**：成品图区与其应有源图的 dhash 距离必须是全场最小，且与次近的差值 ≥3
  （同一张图因 JPEG 压缩会在 6~26 浮动，**不能用绝对阈值**，但"自己 vs 别的图"是 15 vs 110 的数量级差）
- **最大的坑：图片区在卡片【底部】**。卡片是 flex-column，DOM 顺序为 `text-area(63%)` → `photo-area(37%)`。
  若按"图在上"去裁，14 张的距离会全部飙到 100+，看着像整批全错，其实只是裁错位置。脚本默认 `--photo bottom`。

---

## 工作流示例对话

用户："帮我做3张静心茶海报，主题是'放下'"

助手：
1. 写出3条金句草案 → 用户确认/修改
2. 向用户索取3张背景照片（或建议用 AI 生成）
3. 选择配色方案（自动分配深浅交替，如 card-1/card-2/card-3）
4. 生成 HTML 文件
5. 跑 `scripts/export_cards.js` 导出 JPG，并用 `scripts/verify_export.py` 校验
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

