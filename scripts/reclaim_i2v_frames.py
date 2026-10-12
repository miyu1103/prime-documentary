#!/usr/bin/env python3
"""Delete Wan frame directories whose mp4 already exists. Nothing else, ever.

An i2v conversion writes 81-121 PNGs to ae-demo/wan_frames_<slug>_<stem>/ and then assembles
them into remotion/public/<slug>/motion/<stem>.mp4. Once that mp4 exists the frames are spent
intermediate: the film reads the mp4, and re-making the frames costs GPU, not information that
cannot be recovered.

The guard is the mp4 itself. A frame directory is deleted only when its mp4 exists AND is larger
than the same MIN_OK_BYTES the assembler uses to decide a clip is finished rather than truncated
-- so a run that died mid-write keeps its frames. Anything that does not parse as
wan_frames_<slug>_<stem> is left alone.

    py -3.11 scripts/reclaim_i2v_frames.py --dry-run   # default is to show, not delete
    py -3.11 scripts/reclaim_i2v_frames.py --apply
"""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AE_DEMO = Path("C:/Users/aab15/ae-demo")
PUB = ROOT / "remotion" / "public"
MIN_OK_BYTES = 100_000     # the assembler's own "this clip is finished" threshold


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="actually delete; default is dry-run")
    a = ap.parse_args()

    freed = 0
    removed = kept = 0
    for d in sorted(AE_DEMO.glob("wan_frames_*")):
        if not d.is_dir():
            continue
        rest = d.name[len("wan_frames_"):]
        if "_" not in rest:
            kept += 1
            continue
        slug, stem = rest.rsplit("_", 1)
        mp4 = PUB / slug / "motion" / f"{stem}.mp4"
        if not (mp4.is_file() and mp4.stat().st_size > MIN_OK_BYTES):
            kept += 1
            continue
        size = sum(f.stat().st_size for f in d.glob("*.png"))
        freed += size
        removed += 1
        if a.apply:
            shutil.rmtree(d, ignore_errors=True)

    verb = "deleted" if a.apply else "would delete"
    print(f"[reclaim] {verb} {removed} frame dir(s), {freed / 1024**3:.1f} GB; "
          f"kept {kept} without a finished mp4"
          + ("" if a.apply else "  (DRY RUN)"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
