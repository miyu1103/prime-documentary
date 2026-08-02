#!/usr/bin/env python
"""Move the clips visual QC rejected out of an episode's render-visible pool.

Recording a verdict is not the same as acting on it. The verdict file says which clips must
not appear; this is what makes that true on disk, so the film builder cannot pick them.

Rejected files go to `remotion/public/<slug>/factory_rejected/` (kept, not deleted, so a
decision can be revisited and so the evidence survives).

    python scripts/apply_clip_verdicts.py --slug flowers [--dry-run]

Exit 0 always; prints what moved and what the pool is left with.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    verdicts = ROOT / "runs" / "qc" / f"{a.slug}_clip_verdicts.v001.json"
    if not verdicts.is_file():
        print(f"[verdicts] no {verdicts.name} -- nothing to apply")
        return 0
    rejected = json.loads(verdicts.read_text(encoding="utf-8")).get("rejected", {})

    pool = ROOT / "remotion" / "public" / a.slug / "factory"
    dst = pool.parent / "factory_rejected"
    if not pool.is_dir():
        print(f"[verdicts] no pool at {pool}")
        return 0
    dst.mkdir(parents=True, exist_ok=True)

    moved, missing = [], []
    for name, why in rejected.items():
        src = pool / name
        if not src.is_file():
            missing.append(name)
            continue
        moved.append((name, why))
        if not a.dry_run:
            shutil.move(str(src), str(dst / name))

    for name, why in moved[:8]:
        print(f"  - {name}  ({why[:90]})")
    if len(moved) > 8:
        print(f"  ... and {len(moved) - 8} more")
    remaining = len(list(pool.glob("*.mp4")))
    print(f"[verdicts] {a.slug}: {len(moved)} rejected clip(s) "
          f"{'would be ' if a.dry_run else ''}moved to factory_rejected/, {remaining} remain"
          + (f"; {len(missing)} named clip(s) were already gone" if missing else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
