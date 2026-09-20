#!/usr/bin/env python3
"""
WorkBuddy 会话历史瘦身 / 备份 / 归档 / 回滚工具。

用途：当某条会话（如企微 bot 路由进的固定会话）历史文件膨胀到几十~上百 MB，
导致桌面"助理"界面发消息无反应、或模型请求报 400 invalid parameter value 时，
对该会话的 .jsonl 历史文件做安全瘦身：
  - 备份原件（带时间戳）
  - 递归把所有内联 data:image base64（含不被支持的 image/heic）替换为占位符
  - 清空 file-history-snapshot.trackedFileBackups 指针（仅索引，不是版本内容）
  - 原子替换为瘦身后文件
  - 把大备份移到独立归档目录，避免拖慢会话扫描

关键安全保证：
  - 不删除任何行，不改 id/parentId/logicalParentId 链，结构完整可继续对话。
  - 绝不触碰 ~/.workbuddy/file-history/<session>/ 真正的文件版本库（文件级回滚命根子）。

用法：
  分析（只读，不改任何东西）：
    python slim_session.py --analyze <session_id 或 .jsonl 绝对路径>
  执行瘦身：
    python slim_session.py --slim <session_id 或 .jsonl 绝对路径>
  回滚（用最近一次备份覆盖回去）：
    python slim_session.py --rollback <session_id 或 .jsonl 绝对路径>

session_id 会在 ~/.workbuddy/projects/*/ 下自动定位 <id>.jsonl。
"""
import sys, os, json, glob, shutil, datetime, argparse

HOME = os.path.expanduser("~")
PROJECTS = os.path.join(HOME, ".workbuddy", "projects")
ARCHIVE = os.path.join(HOME, ".workbuddy", "session-archives")
BIG_BACKUP_BYTES = 30 * 1024 * 1024  # 备份>30MB 则移到归档目录


def resolve_path(arg):
    """接受 .jsonl 绝对路径，或 session_id（在 projects 下查找）。"""
    if arg.endswith(".jsonl") and os.path.isabs(arg):
        return arg
    if os.path.isfile(arg):
        return os.path.abspath(arg)
    # 当作 session_id 在 projects 下找
    hits = glob.glob(os.path.join(PROJECTS, "*", f"{arg}.jsonl"))
    if not hits:
        sys.exit(f"[ERR] 找不到会话文件：{arg}\n  已搜索 {PROJECTS}/*/{arg}.jsonl")
    if len(hits) > 1:
        print("[WARN] 匹配到多个，使用第一个：")
        for h in hits:
            print("   ", h)
    return hits[0]


def human(n):
    return f"{n/1048576:.1f} MB"


def analyze(path):
    total = 0
    by_type = {}
    img_lines = 0
    heic_lines = 0
    snap_lines = 0
    n = 0
    with open(path, "rb") as f:
        for line in f:
            n += 1
            total += len(line)
            if b"data:image" in line:
                img_lines += 1
            if b"image/heic" in line:
                heic_lines += 1
            try:
                o = json.loads(line)
            except Exception:
                continue
            t = o.get("type", "NA")
            by_type[t] = by_type.get(t, 0) + len(line)
            if t == "file-history-snapshot":
                snap = o.get("snapshot")
                if isinstance(snap, dict) and snap.get("trackedFileBackups"):
                    snap_lines += 1
    print(f"文件: {path}")
    print(f"总大小: {human(total)}  行数: {n}")
    print(f"含内联图(data:image)行: {img_lines}   其中 heic: {heic_lines}")
    print(f"带 trackedFileBackups 的快照行: {snap_lines}")
    print("--- 各类型字节占用 ---")
    for k, v in sorted(by_type.items(), key=lambda x: -x[1]):
        print(f"  {human(v):>10}  {k}")
    return total


def slim(path):
    if not os.path.isfile(path):
        sys.exit(f"[ERR] 文件不存在：{path}")
    in_size = os.path.getsize(path)
    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    base = path[:-len(".jsonl")] if path.endswith(".jsonl") else path
    backup = f"{base}.backup-{ts}.jsonl"
    shutil.copy2(path, backup)
    print(f"[1/4] 已备份 -> {backup}  ({human(in_size)})")

    tmp = path + ".tmp_clean"
    n = 0
    bad = 0

    def clean(o):
        if isinstance(o, dict):
            for k, v in list(o.items()):
                if isinstance(v, str) and "data:image" in v:
                    o[k] = "[inline-image-removed]"
                else:
                    clean(v)
        elif isinstance(o, list):
            for i, v in enumerate(o):
                if isinstance(v, str) and "data:image" in v:
                    o[i] = "[inline-image-removed]"
                else:
                    clean(v)

    with open(path, "rb") as f, open(tmp, "w", encoding="utf-8") as out:
        for line in f:
            n += 1
            try:
                o = json.loads(line)
            except Exception:
                out.write(line.decode("utf-8", "replace"))
                bad += 1
                continue
            if o.get("type") == "file-history-snapshot":
                snap = o.get("snapshot")
                if isinstance(snap, dict) and snap.get("trackedFileBackups"):
                    snap["trackedFileBackups"] = {}
            clean(o)
            out.write(json.dumps(o, ensure_ascii=False) + "\n")
    print(f"[2/4] 已生成瘦身文件  处理 {n} 行  无法解析保留 {bad} 行")

    # 校验
    ok = vbad = 0
    with open(tmp, "rb") as f:
        for line in f:
            try:
                json.loads(line)
                ok += 1
            except Exception:
                vbad += 1
    if vbad and not bad:
        os.remove(tmp)
        sys.exit(f"[ERR] 校验失败：瘦身后出现 {vbad} 个无效 JSON 行，已放弃替换（原文件未动，备份在 {backup}）")
    print(f"[3/4] 校验通过  有效 {ok} 行  无效 {vbad} 行")

    os.replace(tmp, path)  # 原子替换
    out_size = os.path.getsize(path)
    print(f"[4/4] 已原子替换  {human(in_size)} -> {human(out_size)}")

    # 大备份移到独立归档目录
    if os.path.getsize(backup) > BIG_BACKUP_BYTES:
        os.makedirs(ARCHIVE, exist_ok=True)
        dst = os.path.join(ARCHIVE, os.path.basename(backup))
        shutil.move(backup, dst)
        print(f"[+] 备份较大，已移到归档目录避免拖慢扫描 -> {dst}")
        backup = dst
    print(f"\n完成。回滚命令：python slim_session.py --rollback {path}")
    print(f"（或手动复制 {backup} 覆盖回 {path}）")


def compact(path, keep_lines=2000, fcr_keep=2000, msg_keep=15000):
    """深度压缩：裁掉早期历史，只保留最近 keep_lines 行（从干净的 user 消息边界起），
    并压缩工具结果文本 + 清 providerData。用于 --slim 仍降不下来、UI 渲染不动时。
    早期历史不会真丢——依赖前置的整段备份做回滚。"""
    if not os.path.isfile(path):
        sys.exit(f"[ERR] 文件不存在：{path}")
    in_size = os.path.getsize(path)
    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    base = path[:-len(".jsonl")] if path.endswith(".jsonl") else path
    backup = f"{base}.precompact-{ts}.jsonl"
    shutil.copy2(path, backup)
    print(f"[1/5] 已备份当前版本 -> {backup}  ({human(in_size)})")

    import copy
    lines = [json.loads(l) for l in open(path, "rb")]
    n = len(lines)
    if keep_lines >= n:
        print(f"[i] 当前仅 {n} 行 <= keep_lines={keep_lines}，无需裁切。")
        os.remove(backup)
        return
    target = n - keep_lines
    start = None
    for i in range(target, n):
        o = lines[i]
        if o.get("type") == "message" and o.get("role") == "user":
            start = i
            break
    if start is None:
        start = target
    print(f"[2/5] 共 {n} 行，从干净起点 idx={start} 保留（{n-start} 行对话）")

    # 保留标题元数据，让会话仍有名字
    seen = {}
    for o in lines[:start]:
        if o.get("type") in ("ai-title", "custom-title"):
            seen[o["type"]] = o
    head_meta = list(seen.values())

    def trunc(s, keep):
        if not isinstance(s, str) or len(s) <= keep:
            return s
        h = keep * 3 // 4
        return s[:h] + f"\n…[truncated {len(s)-keep} chars]…\n" + s[-(keep - h):]

    out = list(head_meta)
    first = True
    for o in lines[start:]:
        o = copy.deepcopy(o)
        t = o.get("type")
        if first and t == "message":
            for k in ("parentId", "logicalParentId"):
                if k in o:
                    o[k] = None
            first = False
        if t == "function_call_result":
            ot = o.get("output")
            if isinstance(ot, dict) and isinstance(ot.get("text"), str):
                ot["text"] = trunc(ot["text"], fcr_keep)
            if o.get("providerData") is not None:
                o["providerData"] = {}
        elif t == "message":
            c = o.get("content")
            if isinstance(c, list):
                for seg in c:
                    if isinstance(seg, dict) and isinstance(seg.get("text"), str):
                        seg["text"] = trunc(seg["text"], msg_keep)
        out.append(o)

    tmp = path + ".tmp_compact"
    with open(tmp, "w", encoding="utf-8") as f:
        for o in out:
            f.write(json.dumps(o, ensure_ascii=False) + "\n")
    ok = vbad = 0
    with open(tmp, "rb") as f:
        for line in f:
            try:
                json.loads(line)
                ok += 1
            except Exception:
                vbad += 1
    if vbad:
        os.remove(tmp)
        sys.exit(f"[ERR] 校验失败：{vbad} 个无效行，已放弃（原件未动，备份在 {backup}）")
    print(f"[3/5] 校验通过  {ok} 行全部有效")
    os.replace(tmp, path)
    print(f"[4/5] 已原子替换  {human(in_size)} -> {human(os.path.getsize(path))}")
    if os.path.getsize(backup) > BIG_BACKUP_BYTES:
        os.makedirs(ARCHIVE, exist_ok=True)
        dst = os.path.join(ARCHIVE, os.path.basename(backup))
        shutil.move(backup, dst)
        print(f"[5/5] 备份较大，已移到归档 -> {dst}")
    else:
        print(f"[5/5] 备份保留在 {backup}")
    print(f"\n完成。回滚：python slim_session.py --rollback {path}")


def rollback(path):
    base = path[:-len(".jsonl")] if path.endswith(".jsonl") else path
    name = os.path.basename(base)
    candidates = glob.glob(f"{base}.backup-*.jsonl")
    candidates += glob.glob(f"{base}.precompact-*.jsonl")
    candidates += glob.glob(os.path.join(ARCHIVE, f"{name}.backup-*.jsonl"))
    candidates += glob.glob(os.path.join(ARCHIVE, f"{name}.precompact-*.jsonl"))
    if not candidates:
        sys.exit(f"[ERR] 找不到任何备份（{base}.backup-*.jsonl 或 {ARCHIVE}/）")
    latest = max(candidates, key=os.path.getmtime)
    print(f"最近备份: {latest}  ({human(os.path.getsize(latest))})")
    safety = f"{base}.pre-rollback-{datetime.datetime.now():%Y%m%d-%H%M%S}.jsonl"
    if os.path.isfile(path):
        shutil.copy2(path, safety)
        print(f"已先把当前文件存为 {safety}")
    shutil.copy2(latest, path)
    print(f"已回滚: {latest} -> {path}  ({human(os.path.getsize(path))})")


def main():
    ap = argparse.ArgumentParser(description="WorkBuddy 会话瘦身/备份/归档/回滚")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--analyze", metavar="SESSION")
    g.add_argument("--slim", metavar="SESSION")
    g.add_argument("--compact", metavar="SESSION",
                   help="深度压缩：裁掉早期历史只留最近行（配合 --keep-lines），用于 --slim 仍降不下来时")
    g.add_argument("--rollback", metavar="SESSION")
    ap.add_argument("--keep-lines", type=int, default=2000,
                    help="--compact 保留的最近行数（默认 2000）")
    args = ap.parse_args()
    if args.analyze:
        analyze(resolve_path(args.analyze))
    elif args.slim:
        p = resolve_path(args.slim)
        print("=== 瘦身前分析 ===")
        analyze(p)
        print("\n=== 开始瘦身 ===")
        slim(p)
    elif args.compact:
        p = resolve_path(args.compact)
        print("=== 压缩前分析 ===")
        analyze(p)
        print(f"\n=== 开始深度压缩（保留最近 {args.keep_lines} 行）===")
        compact(p, keep_lines=args.keep_lines)
    elif args.rollback:
        rollback(resolve_path(args.rollback))


if __name__ == "__main__":
    main()
