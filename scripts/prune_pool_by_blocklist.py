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

ROOT = Path(__file__).resolve().parents[1]
BLOCKLIST = ROOT / "config" / "footage_blocklist.v001.json"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--pool", default="factory")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    spec = json.loads(BLOCKLIST.read_text(encoding="utf-8"))
    blocked: dict[str, str] = {}
    for row in spec["blocked"]:
        for i in row["ids"]:
            blocked[i] = f'{row["label"]}: {row["reason"]}'

    src = ROOT / "remotion" / "public" / a.slug / a.pool
    dst = src.parent / f"{a.pool}_pruned_offtopic"
    if not src.is_dir():
        print(f"[prune] no pool at {src}")
        return 0
    dst.mkdir(parents=True, exist_ok=True)

    moved = []
    for p in sorted(src.glob("*.mp4")):
        ident = p.name.split("__")[0].replace("AF-BG-", "")
        if ident in blocked:
            moved.append((p.name, blocked[ident]))
            if not a.dry_run:
                shutil.move(str(p), str(dst / p.name))
    for name, why in moved:
        print(f"  - {name}  ({why})")
    kept = len(list(src.glob('*.mp4')))
    print(f"[prune] {a.slug}/{a.pool}: {len(moved)} blocked clip(s) "
          f"{'would be ' if a.dry_run else ''}removed, {kept} remain")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
