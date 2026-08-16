#!/usr/bin/env python3
"""Believe the account, not the ledger, about what has already been posted.

On 2026-08-17 short01 went up twice for the same slot: a run died mid-upload, the ledger never
recorded the first copy, and the next run treated it as unposted. Duplicate posting is a spam
signal on an account that cannot afford one.

This reads the captions actually on the account (scripts/tiktok/list_posted.js) and, for any queued
Short whose opening line is already there but which the ledger calls unposted, appends a
`SCHEDULED_FOUND_ON_ACCOUNT` row so the poster will skip it.

Reads the account, writes only the local ledger. Never posts, never deletes.

Usage:
  py -3.11 scripts/tiktok/reconcile_ledger.py            # report only
  py -3.11 scripts/tiktok/reconcile_ledger.py --apply
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

STUDIO = Path("C:/temp/studio_auto")
QUEUE = STUDIO / "tt_queue.json"
LEDGER = STUDIO / "tt_clean_result.jsonl"
LISTER = Path(__file__).with_name("list_posted.js")


def norm(s: str) -> str:
    s = re.sub(r"#\w+", " ", s.split("\n")[0].lower())
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    return re.sub(r"\s+", " ", s).strip()[:60]


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()

    env_node = str(STUDIO / "node_modules")
    proc = subprocess.run(["node", str(LISTER)], capture_output=True, text=True,
                          encoding="utf-8", errors="replace",
                          env={**__import__("os").environ, "NODE_PATH": env_node})
    if proc.returncode != 0:
        print("FAILED to read the account:", (proc.stderr or "")[:200])
        return 1
    # Studio prints the whole caption as one line, so the queued hook is a PREFIX of it, never
    # equal to it. Comparing with set membership found nothing even when the video was plainly
    # there - the first version of this check passed a deliberately broken ledger.
    on_account = [norm(l) for l in proc.stdout.splitlines() if l.strip()]
    print(f"captions on the account: {len(on_account)}")

    done = set()
    if LEDGER.exists():
        for line in LEDGER.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            if str(row.get("status", "")).startswith("SCHEDULED"):
                done.add(str(row["short"]).zfill(2))

    queue = json.loads(QUEUE.read_text(encoding="utf-8"))
    def already_up(caption: str) -> bool:
        hook = norm(caption)
        return bool(hook) and any(line.startswith(hook) for line in on_account)

    found = [q for q in queue
             if str(q["short"]).zfill(2) not in done and already_up(q["caption"])]

    print(f"queued but already on the account: {len(found)} -> {[q['short'] for q in found]}")
    if not found:
        return 0
    if not a.apply:
        print("(report only; pass --apply to record them)")
        return 0
    with LEDGER.open("a", encoding="utf-8") as fh:
        for q in found:
            fh.write(json.dumps({"status": "SCHEDULED_FOUND_ON_ACCOUNT",
                                 "short": str(q["short"]).zfill(2)}) + "\n")
    print(f"recorded {len(found)} row(s); the poster will skip them")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
