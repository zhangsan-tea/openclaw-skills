#!/usr/bin/env python3
"""
Token Optimizer - L3 Automated Version
This script provides automated, scheduled token optimization for OpenClaw.
"""

import os
import shutil
import logging
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(
    filename='/Users/lee/.openclaw/skills/token-optimizer/logs/optimizer.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Core files that should always remain in the root directory
CORE_FILES = {
    "AGENTS.md", "HEARTBEAT.md", "IDENTITY.md", "SOUL.md",
    "TOOLS.md", "USER.md", "MEMORY.md", "BOOTSTRAP.md"
}

def get_workspace_dirs():
    """Get all OpenClaw workspace directories."""
    base_path = "/Users/lee/.openclaw/"
    return [os.path.join(base_path, d) for d in os.listdir(base_path) if d.startswith("workspace-")]

def cleanup_workspace(workspace_dir):
    """Automatically clean up non-core files in a workspace."""
    logging.info(f"Starting cleanup for {workspace_dir}")
    
    # Create archive directory if it doesn't exist
    archive_dir = os.path.join(workspace_dir, "archive")
    os.makedirs(archive_dir, exist_ok=True)
    
    cleaned_files = []
    for item in os.listdir(workspace_dir):
        item_path = os.path.join(workspace_dir, item)
        
        # Skip directories and core files
        if os.path.isdir(item_path) or item in CORE_FILES:
            continue
            
        # Skip files modified in the last 3 days (dynamic protection)
        file_mtime = datetime.fromtimestamp(os.path.getmtime(item_path))
        if datetime.now() - file_mtime < timedelta(days=3):
            logging.info(f"Skipped recent file: {item_path}")
            continue
            
        # Move non-core, older files to archive
        try:
            shutil.move(item_path, os.path.join(archive_dir, item))
            cleaned_files.append(item)
            logging.info(f"Archived: {item_path} -> {archive_dir}")
        except Exception as e:
            logging.error(f"Failed to archive {item_path}: {e}")
    
    if cleaned_files:
        logging.info(f"Cleanup completed for {workspace_dir}. Archived: {cleaned_files}")
    else:
        logging.info(f"No files to clean in {workspace_dir}")

def main():
    """Main entry point for the automated optimizer."""
    logging.info("=== Starting Automated Token Optimizer (L3) ===")
    
    workspaces = get_workspace_dirs()
    for ws in workspaces:
        if os.path.isdir(ws):
            cleanup_workspace(ws)
    
    logging.info("=== Automated Token Optimizer finished ===")

if __name__ == "__main__":
    main()
