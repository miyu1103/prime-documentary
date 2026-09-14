#!/usr/bin/env python3
"""Refuse any script that enumerates the channel from a single index.

The incident this prevents, 2026-08-03: `playlistItems` on the uploads playlist returned 115 rows
containing only 106 unique ids. Nine videos were absent, three of them PUBLISHED long-forms
(EP34 rolin, EP35 hinders, EP37 florence). Every tool here enumerated that way, so every tool
believed the channel had 106 videos and 43 public long-forms. The real numbers were 115 and 48.

Nothing crashed. `daily_funnel_sync` simply reported "15 still waiting for their long-form to
publish" and skipped them, day after day, while their destinations were live. A silent undercount
is the worst failure mode available to us: it looks exactly like correct output.

The fix is `yt_channel_index.list_video_ids`, which unions the uploads playlist with
`search.list?forMine` and prints a warning when the two disagree. This check exists so the broken
pattern cannot quietly come back in the next script someone writes.

Exit codes: 0 clean, 1 a violation was found.

Usage:
  py -3.11 scripts/check_yt_enumeration.py
  py -3.11 scripts/check_yt_enumeration.py --list-legacy    # show the frozen one-off scripts
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
CANON = "yt_channel_index.py"

# One-off upload scripts written for a single episode and already run. They are kept for the audit
# trail, are never re-run, and are not worth rewriting. Anything NOT on this list must use the
# shared index. Do not add to this list to silence a new script — fix the new script instead.
LEGACY_FROZEN = {
    "_audit_tmp.py",
    "schedule_atwater.py", "schedule_caniglia.py", "schedule_cleveland.py",
    "schedule_glover.py", "schedule_strieff.py", "schedule_tekoh.py",
    "schedule_thompson.py", "schedule_tlo.py", "schedule_young.py",
    "schedule_new_shorts_v001.py", "schedule_new_shorts_v002.py",
    "schedule_new_shorts_v003.py", "schedule_new_shorts_v004.py",
    "schedule_new_shorts_v005.py", "schedule_new_shorts_v006.py",
}

# Narrow on purpose. The bug is *enumerating the channel* from the uploads playlist, and the only
# way to reach that playlist is `relatedPlaylists`. Writing to a playlist (POST/PUT playlistItems)
# is ordinary playlist management and is not a bug — an earlier, broader pattern flagged 20 lines
# of which 13 were innocent playlist writes, which is how a real finding gets lost in noise.
BANNED = re.compile(r"relatedPlaylists")

# A file that reads the uploads playlist AND cross-checks against `search.list?forMine` is doing
# the safe thing by hand, so it passes. `yt_distribution_state.py` already did exactly this and
# even documented the gap — that knowledge just never reached the other nine scripts, which is the
# whole reason this check exists.
UNIONS_BOTH = re.compile(r"forMine")


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--list-legacy", action="store_true")
    args = ap.parse_args()

    if args.list_legacy:
        for n in sorted(LEGACY_FROZEN):
            print(f"  frozen: {n}")
        return 0

    if not (SCRIPTS / CANON).exists():
        print(f"FAIL: the canonical enumerator {CANON} is missing")
        return 1

    violations: list[tuple[str, int, str]] = []
    checked = 0
    for f in sorted(SCRIPTS.glob("*.py")):
        if f.name == CANON or f.name == Path(__file__).name or f.name in LEGACY_FROZEN:
            continue
        checked += 1
        src = f.read_text(encoding="utf-8", errors="replace")
        if UNIONS_BOTH.search(src):
            continue
        for i, line in enumerate(src.splitlines(), 1):
            if BANNED.search(line) and not line.lstrip().startswith("#"):
                violations.append((f.name, i, line.strip()[:96]))

    print(f"checked {checked} scripts, {len(LEGACY_FROZEN)} frozen one-offs skipped")
    if not violations:
        print("PASS: channel enumeration goes through yt_channel_index everywhere")
        return 0

    print(f"\nFAIL: {len(violations)} single-index enumeration(s). The uploads playlist alone is\n"
          f"      known to omit videos on this channel — it hid 9 on 2026-08-03. Use\n"
          f"      `from yt_channel_index import authorize, list_video_ids, fetch_videos`.\n")
    for name, ln, txt in violations:
        print(f"  {name}:{ln}  {txt}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
