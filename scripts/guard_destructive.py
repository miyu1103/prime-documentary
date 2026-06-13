#!/usr/bin/env python3
"""Claude Code PreToolUse hook: block obviously destructive Bash commands.

Reads hook JSON from stdin. Exit code 2 blocks a tool call.
"""
from __future__ import annotations

import json
import re
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
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
