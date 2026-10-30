# reference/wow9：第九期完整管线（参考实现）

| 顺序 | 脚本 | 作用 | 产出 |
|---|---|---|---|
| 1 | `asr.py` | mlx-whisper 字级识别 | `asr.json` |
| 2 | `build_lines.py` | 原始逐字稿 + 剪辑台本（删除线、✂ 区间）合成逐行状态表；同一秒多行按文本相似度分配 | `lines_v02.json` |
| 3 | `align_cut.py` | 参考字流与 ASR 字流分块对齐、插值；保留段吸附能量最低点 | `align.json`、`keep_runs.json` |
| 4 | `(v0x_state.py)` | 把每轮人的修订/批注落到逐字保留状态（含原文，未收录） | `state_v0x.json` |
| 5 | `cut_v06.py` | 逐字状态 → 保留段；手工剪点（overrides）；转场音乐位置与乐句；音乐接口修正 | `keep_runs_v06.json`、`map_v06.json` |
| 6 | `render_coldopen_v08.py` | 开场金句：原片切段、压长停顿、句间 1.6s、钢琴垫底与空档抬升 | `coldopen_*.npy` |
| 7 | `render_v08.py` | 拼接正片 + 转场音乐 + 前接开场，V0.8 母带链，一次出片；支持 `mono 160k` 出试听版 | 成片 mp3 |
| 8 | `build_tracked_v06.py` | 生成 Word 修订稿：删除作者按“谁剪的”、批注、黄底、成片时间 | `.docx` |
| 9 | `qa_v06.py`、`music_check.py`、`refine_music.py` | 接口重新识别比对；音乐接口检查；多候选剪点试剪 | `junction_qa_*.json` |
| 10 | `tone_cmp.py`、`make_blind.py` | 音色对比；响度对齐的 A/B/C 盲听小样 | — |

注意：脚本里写死了第九期的时间点和手工剪点；原文引文已替换为〔原文略〕。新一期请用 `../../scripts/` 的通用脚本，并把本期参数写进项目目录的 `episode.yaml`。
