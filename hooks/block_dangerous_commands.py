#!/usr/bin/env python3
"""Claude Code PreToolUse-style guard for obviously dangerous shell commands.
Reads JSON from stdin when available and exits 2 to block.
This is a conservative example; adapt the actual hook payload to installed Claude Code docs.
"""
from __future__ import annotations
import json, re, sys

BLOCK = [
    r"\brm\s+-rf\s+/(?:\s|$)",
    r"\brm\s+-rf\s+~(?:/|\s|$)",
    r"\bmkfs(?:\.|\s)",
    r"\bdd\s+if=.*\s+of=/dev/",
    r"\bgit\s+reset\s+--hard\b",
    r"\bgit\s+clean\s+-[a-zA-Z]*f",
    r"\bDROP\s+(?:DATABASE|TABLE)\b",
    r"\bTRUNCATE\s+TABLE\b",
]

def extract_command(payload: object) -> str:
    if isinstance(payload, dict):
        for key in ("command", "input", "tool_input"):
            value = payload.get(key)
            if isinstance(value, str): return value
            if isinstance(value, dict) and isinstance(value.get("command"), str):
                return value["command"]
    return ""

def main() -> int:
    raw = sys.stdin.read()
    try: payload = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError: payload = {"input": raw}
    command = extract_command(payload)
    for pattern in BLOCK:
        if re.search(pattern, command, re.IGNORECASE):
            print(json.dumps({"decision":"block","reason":f"Dangerous command matched: {pattern}"}))
            return 2
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
