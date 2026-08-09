#!/usr/bin/env python3
"""Claude Code PreToolUse hook: block obviously destructive Bash commands.

Reads hook JSON from stdin. Exit code 2 blocks a tool call.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys

BLOCK_PATTERNS = [
    (re.compile(r"(^|[;&|]\s*)rm\s+-[^\n]*r[^\n]*f\s+/(?:\s|$)"), "recursive deletion of filesystem root"),
    (re.compile(r"\brm\s+-rf\s+\.(?:\s|$)"), "recursive deletion of current directory"),
    (re.compile(r"\bgit\s+reset\s+--hard\b"), "destructive git reset"),
    (re.compile(r"\bgit\s+clean\s+-[^\n]*f"), "destructive git clean"),
    (re.compile(r"\bgit\s+push\s+[^\n]*--force(?:-with-lease)?\b"), "force push"),
    (re.compile(r"\bDROP\s+(?:DATABASE|SCHEMA|TABLE)\b", re.I), "destructive SQL"),
    (re.compile(r"\bTRUNCATE\s+TABLE\b", re.I), "destructive SQL"),
    (re.compile(r"\b(public|publish)\b[^\n]*(youtube|video)", re.I), "public publishing requires explicit approval"),
]


# Commands that put a heavy, sustained load on the same disk a render is streaming frames to.
# A long-form render holds the disk for two hours; anything here run beside it can kill it, and
# the render dies with no error line, so the cause is not obvious from the log afterwards.
DISK_HEAVY = [
    (re.compile(r"\bdu\s+-\w*[sh]"), "du over a large tree"),
    (re.compile(r"\bfind\s+\S+\s+-(newermt|type|name|size)\b"), "find over a large tree"),
    (re.compile(r"\bbuild_asset_manifest\w*\.py"), "asset manifest rebuild (ffprobe over the pool)"),
    (re.compile(r"\bbuild_case_film\w*\.py"), "film.json build (ffprobe over every staged clip)"),
    (re.compile(r"\bbuild_\w*thumbnails?\w*\.py"), "thumbnail compositing (reads 4K plates)"),
    (re.compile(r"\bcheck_final_acceptance\.py"), "acceptance scan of a full-length master"),
    (re.compile(r"\bcheck_shipped_frames\.py"), "frame extraction from a full-length master"),
    (re.compile(r"\bpd_postrender_gate\.py"), "post-render gate frame extraction"),
    (re.compile(r"\bffmpeg\b(?![^\n]*-t\s+[0-9])"), "unbounded ffmpeg pass"),
    (re.compile(r"\bbuild_motion_from_plates\.py|\bcomfy_wan\.py|\bsd35_gen\.py"), "GPU generation"),
]


def render_in_flight() -> str | None:
    """The composition id of a live `remotion render`, or None.

    Reads the process table rather than a lock file: a lock is only as good as the last script
    that remembered to take it, and the renders here are started from several different places.
    """
    try:
        out = subprocess.run(
            ["powershell", "-NoProfile", "-Command",
             "Get-CimInstance Win32_Process | ForEach-Object { $_.CommandLine }"],
            capture_output=True, text=True, timeout=8).stdout
    except Exception:  # noqa: BLE001
        return None  # cannot tell -> do not block; this hook must never wedge the session
    for line in out.splitlines():
        if "remotion" in line and " render " in line:
            m = re.search(r"render\s+(\S+)", line)
            return m.group(1) if m else "a composition"
    return None


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0
    tool_input = payload.get("tool_input", {})
    command = tool_input.get("command", "") if isinstance(tool_input, dict) else ""
    for pattern, reason in BLOCK_PATTERNS:
        if pattern.search(command):
            print(f"Blocked: {reason}. Use an approved, scoped alternative.", file=sys.stderr)
            return 2

    for pattern, reason in DISK_HEAVY:
        if pattern.search(command):
            comp = render_in_flight()
            if comp:
                print(f"Blocked: {reason} while `remotion render {comp}` is running.\n"
                      f"EP62 greene died twice this way on 2026-08-09 -- no error line, two hours "
                      f"lost -- and EP52 morton before it. Wait for the render, or use a bounded "
                      f"read (a single ffprobe, `ls` on one directory, a log tail).",
                      file=sys.stderr)
                return 2
            break
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
