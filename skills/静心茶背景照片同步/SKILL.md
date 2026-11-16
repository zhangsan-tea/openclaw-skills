---
name: 静心茶背景照片同步
description: 把 macOS「照片」App 的 iCloud 相簿「静心茶海报背景」里的新增照片，增量导出原片到静心茶海报素材收件箱，再按内容哈希自动归类到未用/已用/退役/重复/低清。也回答「哪些背景照片没用过」「照片 App 授权怎么弄」「定时同步」。触发词：同步背景照片、iCloud 相簿同步、读取相簿新增照片、照片授权、更新海报背景库、哪些背景照片没用过、背景照片一览。
agent_created: true
---

# 静心茶背景照片同步

> **唯一权威**：`~/企业云同步盘/海报制作素材/00-资产约定.md`
> **授权与定时专文**：`~/企业云同步盘/海报制作素材/00-iCloud相簿同步-授权与定时.md`
> **给其他 AI 窗口的交接版**：同目录 `00-交接指引-给其他窗口.md`
> 本技能只管「新照片怎么进来」；选图来源与用完处置见交接指引。路径一律相对锚点，**不写 `/Users/<用户名>`**。

---

## 一、完整链路（Lee 2026-11-16 确认）

```
Lee 看到照片 → 存进 iCloud 相簿「静心茶海报背景」
  → 本机「照片」App 同步（系统照片图库）
  → scripts/sync_album_to_inbox.py 读相簿 media item 的 id，与 台账/相簿同步状态.json 比对，只取新增
  → AppleScript `export ... using originals true` 导出**原片**（不是渲染 JPG）
  → 放进 收件箱/ 顶层
  → scripts/ingest_inbox.py --apply 自动判重并分流
  → scripts/fix_paths.py --apply --index 刷新 HTML src 与 photo-index.json
  → 登记本次 id，下次不重复导出
```

分流落点：`photos/`（全新，宽 ≥2250px）｜`photos/已用/`｜`photos/已用/退役/`｜`photos/已用/重复副本/`｜`低清归档/`。

## 二、唯一运行入口（脚本本体只此一份）

```
~/企业云同步盘/海报制作素材/scripts/sync_album_to_inbox.py
```

路径由同目录 `asset_paths.py` 解析（可用 `JXTEA_ASSET_ROOT` 覆盖），跨电脑不写死用户名。
**本技能目录内不含可运行副本**，避免多份脚本分叉。

## 三、⛔ 已废弃：本技能目录里的 `scripts/sync_bg_photos.py`

保留作历史参考，**禁止运行**。三个致命问题：

1. 直接写 `photos/` 顶层，**绕过收件箱判重** → 已用过的旧图会被当新图塞回未用池；
2. `export` 不带 `using originals`，默认导出**渲染后的低清 JPG**（11-16 首批 247 张低清副本即由此而来）；
3. 硬编码 `/Users/sanzhang/...`，另一台电脑（`/Users/lee`）必挂；且会重建 `photo-index.json`，覆盖现行 5 分区口径。

同理不要跑 `scene_dedup.py build` 扫全库（SKIP_DIRS 未含 低清归档/台账/成品/收件箱）。

## 四、前置：一次性授权（当前未打通）

实测 `osascript -e 'tell application "Photos" ...'` 返回 **`-10004` 权限违例**，脚本会打印完整指引。

1. 系统设置 → 隐私与安全性 → **自动化** → WorkBuddy → 勾选「照片 / Photos」
2. 系统设置 → 隐私与安全性 → **照片** → 有 WorkBuddy 就设为允许
3. 列表里没有 WorkBuddy，或曾误点「不允许」→ 终端执行
   `sudo tccutil reset AppleEvents com.tencent.workbuddy.mac`，**完全重启 WorkBuddy**，重跑 `--check` 等弹窗点「好」
4. 前提：照片 App 已开 iCloud 照片，并建议选「将原片下载到此 Mac」（选「优化储存」会让导出原片触发下载、可能超时）

WorkBuddy bundle id：`com.tencent.workbuddy.mac`。
验证：`python scripts/sync_album_to_inbox.py --check` 输出 `[授权] ✅ 可访问照片 App` + 相簿张数即成功。

> 已验证的死路：直读 `~/Pictures/*.photoslibrary/database/` 的 SQLite 同样受 TCC 管控，绕不开 AppleScript。

## 五、命令

```bash
cd ~/企业云同步盘/海报制作素材
PY=~/.workbuddy/binaries/python/envs/default/bin/python

$PY scripts/sync_album_to_inbox.py --check        # 测授权 + 盘点相簿（只读，最安全）
$PY scripts/sync_album_to_inbox.py               # dry-run：列出会导出哪些新增，不动文件
$PY scripts/sync_album_to_inbox.py --init        # 首次基线：登记现有 id，不导出
$PY scripts/sync_album_to_inbox.py --apply       # 导出新增原片 → 收件箱 → 自动归类 → 刷新索引
$PY scripts/sync_album_to_inbox.py --apply --all # 忽略 seen 全量导出（换电脑/图库重建后用）

$PY scripts/ingest_inbox.py --apply              # 只想归类收件箱现有文件
$PY scripts/fix_paths.py --apply --index         # 移动后兜底：全库修 HTML src + 重建索引
```

## 六、首次接手必须先建基线

相簿里已有大量历史照片，状态文件初始为空 → 直接 `--apply` 会全量导出几百张。顺序：

```bash
$PY scripts/sync_album_to_inbox.py --init   # ① 把相簿现有照片全登记为「已见」
$PY scripts/sync_album_to_inbox.py --check # ② 新增应为 0
# ③ 之后往相簿加新照片，才由定时任务 / --apply 只导新增
```

脚本自带保护：单次新增 **> 40 个**直接中止并提示先 `--init`。
状态文件 `台账/相簿同步状态.json` 按 Photos 的 `media item id` 记录，**不按文件名**；图库重建后 id 全变，重新 `--init` 即可。

## 七、定时任务

| 项 | 值 |
|---|---|
| 名称 | 静心茶 · iCloud 相簿背景照片增量同步 |
| ID | `32bafd96-1bbd-43e1-9fd8-352191101299` |
| 频率 | 每天 09:30 |
| 状态 | **PAUSED** → 授权验证通过后改 ACTIVE |

行为：先 `--check`；无新增安静结束；新增 ≤40 跑 `--apply`；跑完读 `台账/入库报告.md` 用中文简报。
授权失效时只输出一句说明，**不重试、不改动文件**。WorkBuddy 需在运行、Mac 未休眠。

## 八、核心规则（踩过的坑，勿改）

1. **按 md5 内容哈希判重，绝不按文件名。** 池里 `IMG_7558.jpeg` 等与 iCloud 导出同名文件是不同照片。
2. **必须 `using originals true`**，否则拿到渲染低清 JPG。
3. **HEIC/PNG 转 JPEG**（`sips`），Chrome headless 导出海报不认 HEIC；原始 HEIC 留 `收件箱/已转换/` 备查。
4. **中文 / `·` 文件名 NFC 归一**：APFS 存 NFD，手写字符串比对会静默失配；一律用 Python `os.listdir()`，绝不用 shell `grep`/`sed` 匹配中文名。
5. **重名用「空格+序号」**（`IMG_8043 2.jpeg`），绝不覆盖。
6. **已用判定三来源并集**：`photos/已用/` 物理目录 + `used-photos.json` 的 `all_used`/`batches` + 黑名单 pattern；黑名单优先级最高（退役）。
7. **新照片一律先过 `收件箱/`**，不直接进 `photos/`；`used-photos.json` 主台账**不写**，每批单独落 `台账/批次-入库-*.json`。
8. **收件箱视频（.mov/.mp4 等）直接删除**（Lee 11-16 定）：不归档、不写台账、不进池，优先移废纸篓以便回退。
9. **高清门槛宽 ≥ 2250px**（2250×4002 导出的真实下限）；不足的进 `低清归档/`，不进选图池。
10. 判定链顺序：黑名单 → 已用证据 md5 → 文件名台账 → 定稿成品指纹(≥0.90) → 池内原图整图指纹(≥0.97) → 池内同内容 md5 → 宽 <2250 归档 → 全新。

## 九、免授权兜底

照片 App 打开相簿 → 全选 → 文件 → 导出 → 导出 N 张照片（格式选**原片**）→ 存到文件夹，然后：

```bash
$PY scripts/ingest_inbox.py --apply --from-dir ~/Downloads/相簿导出
```

从这一步往后完全一样，只是「读相簿」改成手动。Lee 手动把照片拷进 `收件箱/` 也走同一条归类流程。

## 十、输出

- 终端：导出张数、新增明细（文件名 / 尺寸 / id）、入库归类汇总
- `台账/入库报告.md` / `.json`：每张照片的 `verdict` 与 `reasons`
- `台账/批次-入库-<时间戳>.json`：一批一文件，不写主台账
- `台账/相簿同步状态.json`：已处理的 Photos id
- `photo-index.json`（5 分区）、`台账/场次表.json`（EXIF 场次）
- `背景照片一览.html`：未用 / 已用 / 退役缩略图，切到「未用」挑图

## 典型问答

- 「还有哪些没用过」→ `photo-index.json` 里 `zone=unused`，或打开 `背景照片一览.html`
- 「这批新照片哪些是新的」→ `sync_album_to_inbox.py`（dry-run）或 `ingest_inbox.py` 看 `台账/入库报告.md`
- 「照片 App 授权怎么弄」→ 指向 `00-iCloud相簿同步-授权与定时.md` 第 2 节
