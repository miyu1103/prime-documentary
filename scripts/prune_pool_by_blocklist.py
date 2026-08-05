#!/usr/bin/env python
"""Move shelf clips that failed visual QC out of an episode's staged pool.

The factory shelf's labels lie, so off-topic clips (a cartoon gravestone under `cemetery_fog`,
a child's face under `evidence_bag`, rainbow school beakers under `laboratory_glassware`) keep
reaching finished films; the machine gates cannot see semantics and pass them (EP30 shipped a
cartoon cowboy). Once a clip has been looked at and rejected, that judgement belongs to every
episode, not just the one that caught it -- so it lives in config/footage_blocklist.v001.json
and this prunes any pool against it.

    python scripts/prune_pool_by_blocklist.py --slug morton [--dry-run]

Clips are MOVED to <pool>/../factory_pruned_offtopic/ (never deleted), so a decision can be
reviewed and reversed. Exit 0 always -- an episode with nothing to prune is a normal result.
"""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

import pd_footage_blocklist

ROOT = Path(__file__).resolve().parents[1]
BLOCKLIST = pd_footage_blocklist.BLOCKLIST


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--pool", default="factory")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    # global rows plus the rows scoped to this episode: a clip that is fine elsewhere but barred
    # here still has to leave this pool.
    blocked = pd_footage_blocklist.load_blocked(a.slug)

    src = ROOT / "remotion" / "public" / a.slug / a.pool
    dst = src.parent / f"{a.pool}_pruned_offtopic"
    if not src.is_dir():
        print(f"[prune] no pool at {src}")
        return 0
    dst.mkdir(parents=True, exist_ok=True)

    # Not only *.mp4: the episode-scoped rows name generated plates (W059.png, P01.png) that
    # live in the img pool, and a pool prune that skipped stills would leave them staged.
    media = [p for p in sorted(src.iterdir())
             if p.is_file() and p.suffix.lower() in {".mp4", ".mov", ".webm", ".m4v",
                                                     ".png", ".jpg", ".jpeg", ".webp"}]
    moved = []
    for p in media:
        why = pd_footage_blocklist.reason_for(p.name, blocked)
        if why:
            moved.append((p.name, why))
            if not a.dry_run:
                shutil.move(str(p), str(dst / p.name))
    for name, why in moved:
        print(f"  - {name}  ({why})")
    kept = len(media) - (0 if a.dry_run else len(moved))
    print(f"[prune] {a.slug}/{a.pool}: {len(moved)} blocked clip(s) "
          f"{'would be ' if a.dry_run else ''}removed, {kept} remain")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
