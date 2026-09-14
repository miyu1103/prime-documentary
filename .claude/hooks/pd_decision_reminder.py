#!/usr/bin/env python
"""A decision written without a review date gets caught at the moment it is written.

WHY. `scripts/check_decisions.py` requires two lines on any decision accepted from 2026-08-23.
Requiring them is worthless if someone has to remember to run the checker. This fires on the
write itself, so the agent that wrote the file is told before it moves on.

The burden lands on whoever writes the file -- an agent, never the owner. The owner says the
thing; turning it into a dated decision is the assistant's job.

Wired as a PostToolUse hook on Write|Edit in .claude/settings.json. Never blocks: it prints
to stdout, which goes into the agent's context. A hook that stops work over a missing markdown
line would be worse than the problem.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0
    p = (payload.get("tool_input") or {}).get("file_path") or ""
    if not p:
        return 0
    path = Path(p)
    if path.parent.name != "decisions" or path.suffix != ".md" or not path.exists():
        return 0

    try:
        import check_decisions
        text = path.read_text(encoding="utf-8", errors="replace")
        acc = check_decisions.accepted_on(text)
        if acc is None or acc < check_decisions.CUTOFF:
            return 0
        missing = []
        if not check_decisions.RE_REVIEW.search(text):
            missing.append("**Review by:** YYYY-MM-DD")
        if not check_decisions.RE_REVOKE.search(text):
            missing.append("**Revoke if:** <a measurable condition, and the file or command "
                           "that measures it>")
        if missing:
            print(f"[decisions] {path.name} is missing:")
            for m in missing:
                print(f"    {m}")
            print("    Put them under the **Status:** line. Without them this decision binds "
                  "forever and `py -3.11 scripts/check_decisions.py` will report it. "
                  "Ask the owner only if the number is genuinely theirs to choose.")
    except Exception as exc:                      # never break a write over a reminder
        print(f"[decisions] reminder unavailable: {exc}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
