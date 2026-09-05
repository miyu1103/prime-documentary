#!/usr/bin/env python3
"""Is this episode's film already built? Answered from bytes, never from a file's mtime.

THE BUG THIS REPLACES
---------------------
`queue_unattended.sh:already_done()` answered with two proxies, and both are wrong:

    m=".../08_edit/${slug}_final_bgm.v001.mp4"      # hard-coded v001
    [ -f "$m" ] && [ -f "$f" ] && [ "$f" -ot "$m" ] # film json older than master

1. **It tests v001.** Measured 2026-08-23: six of the seven live episodes shipped **v002**.
2. **mtime is not content.** Touching the film json flips the answer in one direction; rebuilding
   the master flips it back. Neither says anything about what is in the file.

Both failure directions have already happened. A false "not done" re-rendered two finished,
scheduled films -- about three GPU-hours for nothing (the comment at `queue_unattended.sh:88`).
A false "done" is worse and quieter: `check_queue_will_stall.py` currently prints
"SILENTLY SKIPPED -- queue thinks it is done" for five episodes, which reads as five lost
episodes. Measured today, **all five are genuinely finished**; the alarm was the defect.

THE ANSWER IT USES INSTEAD
--------------------------
The same test the ship gate already treats as authoritative (`.claude/rules/19-ship-gate.md`):
an episode is built when its acceptance receipt's `video_sha256` equals the SHA-256 of a master
that is actually on disk. Content, not clocks. No new definition of "done" is invented here.

    A trap, hit while writing this: the receipt stores `sha256:2d368d...`. Comparing that string
    to a bare hex digest reports NO MATCH for every episode on the channel, which looks exactly
    like a real finding. Strip the prefix.

WHAT IT DOES NOT PROVE
----------------------
That the film is good, or that a newer film json would not produce a better one. It proves only
that the accepted bytes still exist. Deliberate rebuilds are driven by the queue's explicit JOBS
list; this is the guard against building the same thing twice, not the thing that decides what
to build.

Usage:
    py -3.11 scripts/episode_is_done.py <slug>            # exit 0 done, 1 not done, 2 unusable
    py -3.11 scripts/episode_is_done.py <slug> --quiet     # exit code only, for shell guards
    py -3.11 scripts/episode_is_done.py --all              # every episode with a receipt
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHUNK = 1 << 22

DONE, NOT_DONE, UNUSABLE = 0, 1, 2


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(CHUNK), b""):
            h.update(block)
    return h.hexdigest()


def episode_dir(slug: str) -> Path | None:
    hits = sorted(ROOT.glob(f"episodes/PD-2026-*-{slug}"))
    return hits[-1] if hits else None


def verdict(slug: str) -> tuple[int, str]:
    d = episode_dir(slug)
    if d is None:
        return UNUSABLE, f"no episode directory matches slug {slug!r}"

    receipts = sorted((d / "09_package").glob("acceptance_receipt.v*.json"))
    if not receipts:
        return NOT_DONE, "no acceptance receipt -- nothing has been accepted for this episode"

    receipt = receipts[-1]
    try:
        data = json.loads(receipt.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return UNUSABLE, f"{receipt.name} cannot be read: {exc}"

    raw = data.get("video_sha256") or (data.get("render") or {}).get("video_sha256") or ""
    want = str(raw).split(":")[-1].strip().lower()   # the `sha256:` prefix trap, see docstring
    if len(want) != 64:
        return UNUSABLE, f"{receipt.name} has no usable video_sha256 (got {raw!r})"

    masters = sorted((d / "08_edit").glob(f"{slug}_final_bgm.v*.mp4"))
    if not masters:
        return NOT_DONE, f"{receipt.name} exists but no master is on disk"

    for m in masters:
        if sha256_of(m) == want:
            return DONE, f"{m.name} is byte-for-byte the film {receipt.name} accepted"
    return NOT_DONE, (f"{receipt.name} accepts {want[:12]}..., which is none of "
                      f"{', '.join(m.name for m in masters)} -- the accepted film is not here")


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("slug", nargs="?")
    ap.add_argument("--all", action="store_true", help="every episode that has a receipt")
    ap.add_argument("--quiet", action="store_true", help="exit code only")
    a = ap.parse_args()

    if a.all:
        worst = DONE
        for d in sorted(ROOT.glob("episodes/PD-2026-*")):
            if not (d / "09_package").is_dir():
                continue
            slug = d.name.split("-", 3)[-1]
            if not sorted((d / "09_package").glob("acceptance_receipt.v*.json")):
                continue
            rc, why = verdict(slug)
            print(f"{['DONE', 'NOT_DONE', 'UNUSABLE'][rc]:<9} {slug:<14} {why}")
            worst = max(worst, rc)
        return worst

    if not a.slug:
        ap.error("a slug is required unless --all")
    rc, why = verdict(a.slug)
    if not a.quiet:
        print(f"{['DONE', 'NOT_DONE', 'UNUSABLE'][rc]:<9} {a.slug:<14} {why}")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
