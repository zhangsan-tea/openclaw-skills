#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从企业微信文档的 wecom-cli 原始输出中提取 base64 图片，保存到本地文件。

用法:
    python extract_images.py <wecom_raw_output.txt> <output_dir/>

输出:
    - 图片保存为 img_00.png, img_01.png, ...
    - 同时输出 results.json，记录每张图片的文件路径和在文档中出现的位置

用于 monthly-report-formatter 流水线：提取图片 → 写入 figure 节点 → 生成 Word/HTML。
"""
import sys
import os
import re
import json
import base64


def extract_images(raw_file, out_dir):
    """从原始输出文件中提取所有 base64 图片。"""
    os.makedirs(out_dir, exist_ok=True)

    with open(raw_file, "r", encoding="utf-8", errors="ignore") as f:
        data = f.read()

    # 匹配 data:image/xxx;base64,...
    pattern = re.compile(r'data:image/(png|jpeg|jpg|gif|webp);base64,([A-Za-z0-9+/=]+)')
    matches = pattern.findall(data)

    images = []
    for i, (ext, b64) in enumerate(matches):
        # 补全 base64 padding
        missing = len(b64) % 4
        if missing:
            b64 += "=" * (4 - missing)

        try:
            raw_bytes = base64.b64decode(b64)
        except Exception as e:
            print(f"  [跳过] img_{i:02d}: base64 解码失败: {e}")
            continue

        # 确定文件扩展名
        file_ext = ext
        if ext in ("jpeg", "jpg"):
            file_ext = "jpg"

        fname = f"img_{i:02d}.{file_ext}"
        fpath = os.path.join(out_dir, fname)

        with open(fpath, "wb") as out:
            out.write(raw_bytes)

        images.append({
            "index": i,
            "filename": fname,
            "path": fpath,
            "format": file_ext,
            "size_bytes": len(raw_bytes),
        })
        print(f"  ✓ img_{i:02d}.{file_ext} ({len(raw_bytes)} bytes)")

    # 写出结果清单
    result_path = os.path.join(out_dir, "results.json")
    with open(result_path, "w", encoding="utf-8") as f:
        json.dump(images, f, ensure_ascii=False, indent=2)

    print(f"\n提取完成: {len(images)} 张图片 → {out_dir}")
    print(f"结果清单: {result_path}")
    return images


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python extract_images.py <wecom_raw_output.txt> <output_dir/>")
        sys.exit(1)

    raw_file = sys.argv[1]
    out_dir = sys.argv[2]

    if not os.path.exists(raw_file):
        print(f"错误: 找不到文件 {raw_file}")
        sys.exit(1)

    extract_images(raw_file, out_dir)
