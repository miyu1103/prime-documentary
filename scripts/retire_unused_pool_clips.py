#!/usr/bin/env python
"""Move staged clips the finished film never references out of the pool.

`footage_utilization` measures the owner's oldest complaint -- material collected and then not
used (EP51: 19 of 140 staged clips referenced zero times, 64% overall). Once the film is built,
the unreferenced clips are not "held back for later": they are staged material the episode
decided against. Retiring them makes the pool tell the truth, and the next episode's staging
(which excludes ids already used elsewhere) can pick them up instead.

    python scripts/retire_unused_pool_clips.py --slug willingham [--dry-run]

Clips are MOVED to <pool>_unused/, never deleted. Run AFTER the film json is built.
"""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--pools", default="factory,motion,img,stock,motion2")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    film = ROOT / "remotion" / "src" / "data" / f"{a.slug}_film.json"
    if not film.is_file():
        print(f"[retire] no film json for {a.slug}")
        return 0
    d = json.loads(film.read_text(encoding="utf-8"))
    used = {str(c.get("src", "")).split("/")[-1] for c in d.get("cuts", [])}
    for key in ("hook", "heroCuts", "overlays"):
        for c in d.get(key) or []:
            if isinstance(c, dict) and c.get("src"):
                used.add(str(c["src"]).split("/")[-1])

    moved_total = 0
    for pool in a.pools.split(","):
        src = ROOT / "remotion" / "public" / a.slug / pool
        if not src.is_dir():
            continue
        dst = src.parent / f"{pool}_unused"
        moved = [p for p in sorted(src.iterdir())
                 if p.is_file() and p.suffix.lower() in {".mp4", ".mov", ".png", ".jpg"}
                 and p.name not in used]
        if moved and not a.dry_run:
            dst.mkdir(parents=True, exist_ok=True)
            for p in moved:
                shutil.move(str(p), str(dst / p.name))
        moved_total += len(moved)
        if moved:
            print(f"[retire]   {pool}: {len(moved)} unused -> {dst.name}")
    print(f"[retire] {a.slug}: {moved_total} staged file(s) "
          f"{'would be ' if a.dry_run else ''}retired as unused")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
