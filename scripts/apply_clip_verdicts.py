#!/usr/bin/env python
"""Move what visual QC rejected out of an episode's render-visible pools.

Recording a verdict is not the same as acting on it. The verdict file says which items must
not appear; this is what makes that true on disk, so the film builder cannot pick them.

TWO POOLS, ONE RESPONSIBILITY (plates lane added 2026-08-11)
------------------------------------------------------------
A film draws from two render-visible pools and both are judged per item:

    clips   remotion/public/<slug>/factory  <- runs/qc/<slug>_clip_verdicts.v001.json
    plates  remotion/public/<slug>/img      <- runs/qc/<slug>_plate_verdicts.v001.json

Only the clips lane existed. `check_plate_verdicts.py` REFUSES a build while a rejected plate
is still staged in img/ -- "which is the still pool the builder draws from" -- and named no
tool that could clear it, so the last step of a plate review had to be done by hand. EP65
marmet sat on that gate with 9 rejected plates staged. The lane is added here rather than in a
new script because the responsibility is identical (act on a recorded rejection so the builder
cannot pick it) and only the pool, the verdict file and the file extension differ.

Rejected files go to `remotion/public/<slug>/factory_rejected/` and
`remotion/public/<slug>/img_rejected/` (kept, not deleted, so a decision can be revisited and
so the evidence survives).

    python scripts/apply_clip_verdicts.py --slug flowers [--dry-run]
    python scripts/apply_clip_verdicts.py --slug marmet --lane plates [--dry-run]
    python scripts/apply_clip_verdicts.py --slug marmet --lane both

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


def _clip_rejects(slug: str) -> tuple[Path, dict[str, str]]:
    """{name: why} from the clip verdict file, whose rejects are a flat mapping."""
    path = ROOT / "runs" / "qc" / f"{slug}_clip_verdicts.v001.json"
    if not path.is_file():
        return path, {}
    data = json.loads(path.read_text(encoding="utf-8")).get("rejected", {})
    return path, {str(k): str(v) for k, v in data.items()}


def _plate_rejects(slug: str) -> tuple[Path, dict[str, str]]:
    """{id: note} for every plate whose verdict is a rejection.

    The reject vocabulary is READ FROM `check_plate_verdicts`, not restated here, so the tool
    that acts on a verdict can never disagree with the gate that refuses the build over it.
    """
    path = ROOT / "runs" / "qc" / f"{slug}_plate_verdicts.v001.json"
    if not path.is_file():
        return path, {}
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from check_plate_verdicts import REJECT_WORDS  # noqa: PLC0415
    plates = json.loads(path.read_text(encoding="utf-8")).get("plates", {})
    out = {}
    for pid, e in plates.items():
        if isinstance(e, dict) and str(e.get("verdict") or "").strip().lower() in REJECT_WORDS:
            out[str(pid)] = str(e.get("note") or "")
    return path, out


LANES = {
    # lane   -> (pool dir, destination dir, what remains counted by, noun, reject reader)
    "clips": ("factory", "factory_rejected", "*.mp4", "clip", _clip_rejects),
    "plates": ("img", "img_rejected", "*.png", "plate", _plate_rejects),
}


def apply_lane(slug: str, lane: str, dry_run: bool) -> int:
    pool_name, dst_name, glob, noun, reader = LANES[lane]
    verdicts, rejected = reader(slug)
    if not verdicts.is_file():
        print(f"[verdicts] no {verdicts.name} -- nothing to apply for {lane}")
        return 0

    pool = ROOT / "remotion" / "public" / slug / pool_name
    dst = pool.parent / dst_name
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
        if not dry_run:
            shutil.move(str(src), str(dst / name))

    for name, why in moved[:8]:
        print(f"  - {name}  ({why[:90]})")
    if len(moved) > 8:
        print(f"  ... and {len(moved) - 8} more")
    remaining = len(list(pool.glob(glob)))
    print(f"[verdicts] {slug}: {len(moved)} rejected {noun}(s) "
          f"{'would be ' if dry_run else ''}moved to {dst_name}/, {remaining} remain"
          + (f"; {len(missing)} named {noun}(s) were already gone" if missing else ""))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--lane", choices=("clips", "plates", "both"), default="clips",
                    help="which render-visible pool to clear (default: clips, as before)")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    for lane in (("clips", "plates") if a.lane == "both" else (a.lane,)):
        apply_lane(a.slug, lane, a.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
