---
name: 静心茶背景照片同步
description: 从 macOS 照片 App 的 iCloud 相簿「静心茶海报背景」增量同步照片到静心茶海报照片池，按内容哈希去重，维护未用/已用/退役索引与缩略图一览页。触发词：同步背景照片、更新海报背景库、从 iCloud 导入背景图、哪些背景照片没用过、背景照片一览。
agent_created: true
---

# 静心茶背景照片同步

把 iCloud 照片相簿「静心茶海报背景」的新照片增量汇入海报照片池，并回答「哪些没用过」。

## 资产位置（本机固定，勿改）

| 项目 | 路径 |
|------|------|
| 照片池（未用） | `/Users/sanzhang/企业云同步盘/海报制作素材/photos/` |
| 已用物理区 | 同目录 `photos/已用/` |
| 已用清单 | `/Users/sanzhang/企业云同步盘/海报制作素材/used-photos.json` |
| 全量索引（本技能生成） | 同目录 `photo-index.json` |
| 缩略图一览 | 同目录 `背景照片一览.html` |
| 同步脚本 | `{baseDir}/scripts/sync_bg_photos.py` |

## 前置：照片授权（只需做一次）

系统默认拒绝脚本访问照片（错误 -10004）。两种解法：

**A. 授权（推荐，之后全自动）**
1. 系统设置 → 隐私与安全性 → 自动化 → **WorkBuddy** → 勾选「Photos」
2. 系统设置 → 隐私与安全性 → 照片 → 允许 **WorkBuddy** 访问

WorkBuddy bundle id：`com.tencent.workbuddy.mac`。
若列表无此条目或曾误点「不允许」，先重置授权记录再重跑脚本（会重新弹窗）：
`sudo tccutil reset AppleEvents com.tencent.workbuddy.mac`

> 已实测的死路，别再试：直读图库 SQLite（`~/Pictures/Photos Library.photoslibrary/database/`）
> 同样受 TCC 管控，未授权时 PermissionError，绕不开 AppleScript。

**B. 手动导出兜底（免授权）**
照片 App 打开该相簿 → 全选 → 文件 → 导出 → 导出 N 张照片 → 选文件夹，然后：
`python3 sync_bg_photos.py --from-dir <文件夹>`

## 命令

```bash
cd /Users/sanzhang/obsidian-private/向内看/静心茶/Skills
python3 sync_bg_photos.py --dry-run           # 先看会新增哪些，不落盘
python3 sync_bg_photos.py --gallery           # 同步 + 重建索引 + 生成一览页
python3 sync_bg_photos.py --from-dir <路径>   # 手动导出目录导入
python3 sync_bg_photos.py --rebuild --gallery # 只重建索引与一览页
```

## 核心规则（踩过的坑，勿改）

1. **必须按 md5 内容哈希判重，绝不用文件名。** 池里已有 `IMG_7558.jpeg`、`IMG_8043.jpeg` 等，iCloud 导出的同名文件是另一张照片。
2. **HEIC/PNG 一律转 JPEG。** Chrome headless 导出海报不认 HEIC，靠 `sips -s format jpeg`。
3. **文件名冲突沿用「空格+序号」**：`IMG_8043 2.jpeg`（与池内既有风格一致）。
4. **中文/`·` 文件名走 NFC 归一。** macOS 磁盘存 NFD，直接字符串比对会静默失效。
5. **已用判定三来源并集**：`photos/已用/` 物理目录 + `used-photos.json` 的 `all_used` 与 `batches` + `黑名单.items` 的 pattern。命中黑名单标 `blacklist`（退役），优先级最高。
6. **新入库照片默认进顶层池（未用）**，不自动进 `已用/`；制卡选用后由人工或制卡流程移入。

## 输出

- 终端报告：新增 / 重复跳过 / 失败 三栏 + 新增明细（文件名、尺寸、来源）
- `photo-index.json`：每张照片的 file / status / 尺寸 / md5 / 日期
- `背景照片一览.html`：未用 / 已用 / 退役 三个可切换分组的缩略图网格，供挑图

## 典型问答

- 「还有哪些没用过」→ 看 `photo-index.json` 里 `status == "unused"` 的数量，或直接打开 `背景照片一览.html`
- 「这批新照片哪些是新的」→ `--dry-run`，脚本只报不落盘
