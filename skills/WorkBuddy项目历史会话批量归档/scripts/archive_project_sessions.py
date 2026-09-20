#!/usr/bin/env python3
"""Safely batch-archive WorkBuddy project sessions by title.

Dry-run is the default. Execution requires both --execute and an exact confirmation
phrase. The script backs up workbuddy.db, moves matching session files into a
reversible archive, updates session status in a transaction, and verifies results.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
from pathlib import Path
import re
import shutil
import sqlite3
import sys
from typing import Any

CONFIRM_PHRASE = "ARCHIVE_MATCHED_SESSIONS"
BLOCKED_STATUSES = {"working", "planning", "pending", "running", "active"}
DEFAULT_STATUSES = "completed,Completed,error"


def parse_args() -> argparse.Namespace:
    home = Path.home()
    parser = argparse.ArgumentParser(
        description="Batch-archive WorkBuddy project sessions matched by title."
    )
    parser.add_argument("--title-pattern", required=True, help="Substring to match in title/custom_title")
    parser.add_argument(
        "--match-mode",
        choices=("contains", "exact"),
        default="contains",
        help="Title matching mode (default: contains)",
    )
    parser.add_argument(
        "--statuses",
        default=DEFAULT_STATUSES,
        help=f"Comma-separated statuses eligible for archive (default: {DEFAULT_STATUSES})",
    )
    parser.add_argument("--cwd", action="append", default=[], help="Optional exact cwd filter; repeatable")
    parser.add_argument("--exclude-session-id", action="append", default=[], help="Session ID to preserve; repeatable")
    parser.add_argument("--db", type=Path, default=home / ".workbuddy" / "workbuddy.db")
    parser.add_argument("--projects-root", type=Path, default=home / ".workbuddy" / "projects")
    parser.add_argument("--archive-root", type=Path, default=home / ".workbuddy" / "session-archives")
    parser.add_argument("--archive-label", default="workbuddy-session-batch-archive")
    parser.add_argument("--execute", action="store_true", help="Perform the archive; otherwise dry-run")
    parser.add_argument("--confirm", default="", help=f"Required with --execute: {CONFIRM_PHRASE}")
    return parser.parse_args()


def safe_label(value: str) -> str:
    value = re.sub(r"[^0-9A-Za-z._\-\u4e00-\u9fff]+", "-", value.strip())
    return value.strip("-._") or "archive"


def title_matches(value: str | None, pattern: str, mode: str) -> bool:
    if not value:
        return False
    return value == pattern if mode == "exact" else pattern in value


def connect_db(path: Path) -> sqlite3.Connection:
    if not path.is_file():
        raise FileNotFoundError(f"Database not found: {path}")
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    table = conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name='sessions'"
    ).fetchone()
    if not table:
        conn.close()
        raise RuntimeError("sessions table not found")
    return conn


def select_sessions(conn: sqlite3.Connection, args: argparse.Namespace) -> list[dict[str, Any]]:
    requested_statuses = {s.strip() for s in args.statuses.split(",") if s.strip()}
    blocked_requested = {s for s in requested_statuses if s.lower() in BLOCKED_STATUSES}
    if blocked_requested:
        raise ValueError(f"Unsafe active statuses are forbidden: {sorted(blocked_requested)}")

    excluded = set(args.exclude_session_id)
    cwd_filter = set(args.cwd)
    rows = conn.execute(
        "SELECT id, cwd, title, custom_title, status, created_at, updated_at "
        "FROM sessions ORDER BY created_at"
    ).fetchall()
    matched: list[dict[str, Any]] = []
    for row in rows:
        item = dict(row)
        if item["id"] in excluded:
            continue
        if item["status"] not in requested_statuses:
            continue
        if str(item["status"]).lower() in BLOCKED_STATUSES:
            continue
        if cwd_filter and item["cwd"] not in cwd_filter:
            continue
        if title_matches(item["title"], args.title_pattern, args.match_mode) or title_matches(
            item["custom_title"], args.title_pattern, args.match_mode
        ):
            matched.append(item)
    return matched


def locate_payloads(projects_root: Path, session_id: str) -> list[Path]:
    payloads: list[Path] = []
    for project_dir in projects_root.iterdir() if projects_root.is_dir() else []:
        if not project_dir.is_dir():
            continue
        for suffix in (".jsonl", ".meta.json"):
            candidate = project_dir / f"{session_id}{suffix}"
            if candidate.exists():
                payloads.append(candidate)
        support_dir = project_dir / session_id
        if support_dir.is_dir():
            payloads.append(support_dir)
    return payloads


def build_plan(args: argparse.Namespace, sessions: list[dict[str, Any]]) -> dict[str, Any]:
    items = []
    payload_count = 0
    payload_bytes = 0
    for session in sessions:
        payloads = locate_payloads(args.projects_root, session["id"])
        payload_count += len(payloads)
        for payload in payloads:
            if payload.is_file():
                payload_bytes += payload.stat().st_size
        items.append(
            {
                **session,
                "payloads": [str(p) for p in payloads],
            }
        )
    return {
        "mode": "execute" if args.execute else "dry-run",
        "title_pattern": args.title_pattern,
        "match_mode": args.match_mode,
        "eligible_statuses": args.statuses.split(","),
        "cwd_filter": args.cwd,
        "session_count": len(items),
        "payload_count": payload_count,
        "payload_file_bytes": payload_bytes,
        "sessions": items,
    }


def backup_database(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    src = sqlite3.connect(source)
    dst = sqlite3.connect(destination)
    try:
        src.backup(dst)
        check = dst.execute("PRAGMA integrity_check").fetchone()
        if not check or check[0] != "ok":
            raise RuntimeError(f"Backup integrity check failed: {check}")
    finally:
        dst.close()
        src.close()


def destination_for(payload: Path, projects_root: Path, archive_dir: Path) -> Path:
    project_name = payload.parent.name
    if payload.parent.parent == projects_root and payload.is_dir():
        project_name = payload.parent.name
        bucket = "support_dirs"
    elif payload.parent.parent == projects_root:
        bucket = "session_files"
    else:
        raise RuntimeError(f"Unexpected payload location: {payload}")
    return archive_dir / "projects" / project_name / bucket / payload.name


def execute_archive(args: argparse.Namespace, plan: dict[str, Any]) -> dict[str, Any]:
    if args.confirm != CONFIRM_PHRASE:
        raise ValueError(f"--execute requires --confirm {CONFIRM_PHRASE}")
    if not plan["sessions"]:
        return {**plan, "result": "nothing-to-archive"}

    timestamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    archive_dir = args.archive_root / f"{timestamp}_{safe_label(args.archive_label)}"
    if archive_dir.exists():
        raise FileExistsError(f"Archive destination already exists: {archive_dir}")

    backup_path = args.archive_root / "db-backups" / f"workbuddy-{timestamp}.sqlite"
    backup_database(args.db, backup_path)

    moves: list[tuple[Path, Path]] = []
    for session in plan["sessions"]:
        for raw_path in session["payloads"]:
            source = Path(raw_path)
            destination = destination_for(source, args.projects_root, archive_dir)
            if destination.exists():
                raise FileExistsError(f"Archive collision: {destination}")
            moves.append((source, destination))

    moved: list[tuple[Path, Path]] = []
    try:
        for source, destination in moves:
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(source), str(destination))
            moved.append((source, destination))

        ids = [session["id"] for session in plan["sessions"]]
        placeholders = ",".join("?" for _ in ids)
        conn = connect_db(args.db)
        try:
            now_ms = int(dt.datetime.now().timestamp() * 1000)
            conn.execute("BEGIN IMMEDIATE")
            cursor = conn.execute(
                f"UPDATE sessions SET status='archived', updated_at=? WHERE id IN ({placeholders})",
                [now_ms, *ids],
            )
            if cursor.rowcount != len(ids):
                raise RuntimeError(f"Expected to update {len(ids)} rows, updated {cursor.rowcount}")
            remaining = conn.execute(
                f"SELECT COUNT(*) FROM sessions WHERE id IN ({placeholders}) AND status!='archived'",
                ids,
            ).fetchone()[0]
            if remaining:
                raise RuntimeError(f"Verification failed: {remaining} sessions are not archived")
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    except Exception:
        for source, destination in reversed(moved):
            if destination.exists() and not source.exists():
                source.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(destination), str(source))
        raise

    result = {
        **plan,
        "result": "archived",
        "archive_dir": str(archive_dir),
        "database_backup": str(backup_path),
        "moved_payload_count": len(moved),
    }
    manifest = archive_dir / "manifest.json"
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    result["manifest"] = str(manifest)
    return result


def main() -> int:
    args = parse_args()
    try:
        conn = connect_db(args.db)
        try:
            sessions = select_sessions(conn, args)
        finally:
            conn.close()
        plan = build_plan(args, sessions)
        result = execute_archive(args, plan) if args.execute else plan
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
