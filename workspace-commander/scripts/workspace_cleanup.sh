#!/bin/bash

echo "[$(date)] 开始执行工作区安全清理任务 (Token 优化)..."

CORE_FILES=("AGENTS.md" "HEARTBEAT.md" "IDENTITY.md" "SOUL.md" "TOOLS.md" "USER.md" "MEMORY.md" "BOOTSTRAP.md" "README.md" "package.json" "package-lock.json")

for ws in /Users/lee/.openclaw/workspace-*; do
    [ -d "$ws" ] || continue
    agent_name=$(basename "$ws")
    
    mkdir -p "$ws/archive"
    
    # 使用 find 查找超过 3 天未修改的非隐藏文件 (排除子目录)
    # -maxdepth 1 确保只查根目录
    # -mtime +3 确保只查修改时间大于3天的
    find "$ws" -maxdepth 1 -type f -not -name ".*" -mtime +3 | while read -r f; do
        filename=$(basename "$f")
        
        is_core=false
        for core in "${CORE_FILES[@]}"; do
            if [ "$filename" = "$core" ]; then
                is_core=true
                break
            fi
        done
        
        if [ "$is_core" = false ]; then
            echo "  [$agent_name] 归档旧文件: $filename"
            mv "$f" "$ws/archive/"
        fi
    done
done

echo "[$(date)] 清理任务完成。"
