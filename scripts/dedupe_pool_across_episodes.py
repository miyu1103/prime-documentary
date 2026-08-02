#!/usr/bin/env python
"""Remove clips from an episode's pool that another episode's pool already holds.

`arc_nonrepeat` measures the owner's 「素材の被り」 across episodes, and staging by ledger title
hands the same top-N match to every episode that asks a similar question -- EP51 measured 143
of 263 cuts as clips it shared with morton and flowers. This keeps the FIRST episode to stage a
clip and clears it from the one being built now, which then tops up with fresh titles.

    python scripts/dedupe_pool_across_episodes.py --slug flowers [--dry-run]

Clips are MOVED to <pool>_shared_removed/, never deleted.
"""
from __future__ import annotations

import argparse
import collections
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--pool", default="factory")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    pub = ROOT / "remotion" / "public"
    pools = {p.parent.name: {q.name.split("__")[0]: q for q in p.glob("*.mp4")}
             for p in pub.glob(f"*/{a.pool}")}
    if a.slug not in pools:
        print(f"[dedupe] no {a.pool} pool for {a.slug}")
        return 0

    counts: collections.Counter[str] = collections.Counter()
    for ids in pools.values():
        counts.update(ids.keys())
    shared = {i for i, n in counts.items() if n > 1}

    dst = pub / a.slug / f"{a.pool}_shared_removed"
    moved = 0
    for ident, path in sorted(pools[a.slug].items()):
        if ident in shared:
            if not a.dry_run:
                dst.mkdir(parents=True, exist_ok=True)
                shutil.move(str(path), str(dst / path.name))
            moved += 1
    left = len(list((pub / a.slug / a.pool).glob("*.mp4")))
    print(f"[dedupe] {a.slug}: {moved} clip(s) shared with another episode "
          f"{'would be ' if a.dry_run else ''}removed, {left} remain")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
