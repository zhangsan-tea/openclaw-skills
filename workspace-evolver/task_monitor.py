#!/usr/bin/env python3
"""
Task Execution Monitor - 监控所有 Agent 的任务执行状态
确保没有任务半途而废，所有任务都有明确的完成状态
"""

import json
import time
from pathlib import Path

class TaskMonitor:
    def __init__(self):
        self.active_tasks = {}
        self.completed_tasks = []
        self.failed_tasks = []
        
    def start_task(self, agent_id: str, task_description: str):
        """开始新任务"""
        task_id = f"{agent_id}_{int(time.time())}"
        self.active_tasks[task_id] = {
            "agent_id": agent_id,
            "description": task_description,
            "start_time": time.time(),
            "last_update": time.time(),
            "status": "running"
        }
        print(f"✅ 任务启动: {agent_id} - {task_description}")
        
    def update_task(self, task_id: str, progress: str):
        """更新任务进度"""
        if task_id in self.active_tasks:
            self.active_tasks[task_id]["last_update"] = time.time()
            self.active_tasks[task_id]["progress"] = progress
            print(f"🔄 任务进度: {task_id} - {progress}")
            
    def complete_task(self, task_id: str, result: str):
        """完成任务"""
        if task_id in self.active_tasks:
            task = self.active_tasks.pop(task_id)
            task["end_time"] = time.time()
            task["result"] = result
            task["status"] = "completed"
            self.completed_tasks.append(task)
            print(f"✅ 任务完成: {task['agent_id']} - {result}")
            
    def fail_task(self, task_id: str, error: str):
        """任务失败"""
        if task_id in self.active_tasks:
            task = self.active_tasks.pop(task_id)
            task["end_time"] = time.time()
            task["error"] = error
            task["status"] = "failed"
            self.failed_tasks.append(task)
            print(f"❌ 任务失败: {task['agent_id']} - {error}")
            
    def check_stale_tasks(self, timeout_seconds: int = 300):
        """检查超时任务"""
        current_time = time.time()
        stale_tasks = []
        
        for task_id, task in self.active_tasks.items():
            if current_time - task["last_update"] > timeout_seconds:
                stale_tasks.append(task_id)
                
        for task_id in stale_tasks:
            print(f"⚠️ 超时任务: {task_id} - 自动标记为需要关注")
            # 这里可以触发自动重试或通知
            
    def get_task_summary(self):
        """获取任务摘要"""
        return {
            "active": len(self.active_tasks),
            "completed": len(self.completed_tasks),
            "failed": len(self.failed_tasks)
        }

# 全局任务监控器实例
task_monitor = TaskMonitor()