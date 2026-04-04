#!/usr/bin/env python3
"""
Token Optimizer - L3 Automated Version
This script provides automated, scheduled token optimization for OpenClaw.
"""

import os
import sys
import shutil
import logging
from datetime import datetime, timedelta

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(SCRIPT_DIR, '..', 'logs', 'optimizer.log')

# Create logs directory if it doesn't exist
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

# Configure logging
logging.basicConfig(
    filename=LOG_FILE,
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
    # Get OpenClaw base path from environment or default to ~/.openclaw
    base_path = os.environ.get('OPENCLAW_PATH', os.path.expanduser('~/.openclaw'))
    if not os.path.exists(base_path):
        logging.error(f"OpenClaw base path not found: {base_path}")
        return []
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
