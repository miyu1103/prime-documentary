#!/usr/bin/env python3
"""Drop rows from the semantic footage index whose file no longer exists.

WHY. `index_footage_semantic.py` resumes by keeping every path it has ever embedded, and it
never checks that those files are still there. Measured 2026-08-25: of 31,480 indexed clips,
**15,955 point at H:\\pd-media\\assets\\factory** -- the drive that died in August -- and every
one of them resolves to nothing. Another ~12 % of the pd-archive rows are gone too (files
quarantined, renamed for search, or pruned). So half of "search by what is on screen" returns
ghosts, and the caller cannot tell a ghost from a hit until it opens the file.

paths.json and embeddings.npy are ROW ALIGNED. This rewrites both together, or neither: the
new pair is written to temp files and renamed into place only after both are complete.

    py -3.11 scripts/prune_semantic_index.py            # report only
    py -3.11 scripts/prune_semantic_index.py --apply
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "runs" / "footage_semantic"


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()

    import numpy as np

    paths_file, emb_file = OUT / "paths.json", OUT / "embeddings.npy"
    if not (paths_file.exists() and emb_file.exists()):
        sys.exit(f"no index at {OUT} -- nothing to prune")

    paths = json.loads(paths_file.read_text(encoding="utf-8"))
    embs = np.load(emb_file)
    if len(paths) != embs.shape[0]:
        sys.exit(f"index is already inconsistent: {len(paths)} paths vs {embs.shape[0]} rows "
                 f"-- rebuild rather than prune")

    keep = [i for i, p in enumerate(paths) if Path(p).is_file()]
    dead = len(paths) - len(keep)
    by_drive: dict[str, int] = {}
    for i, p in enumerate(paths):
        if i not in set(keep):
            by_drive[p[:2].upper()] = by_drive.get(p[:2].upper(), 0) + 1

    print(f"index rows      : {len(paths)}")
    print(f"still on disk   : {len(keep)}")
    print(f"dead rows       : {dead}   {by_drive}")

    if not a.apply:
        print("\n(report only -- add --apply to rewrite paths.json + embeddings.npy)")
        return 0
    if dead == 0:
        print("nothing to do")
        return 0

    new_paths = [paths[i] for i in keep]
    new_embs = embs[keep]
    # np.save APPENDS .npy unless the name already ends in it, so a temp called
    # "embeddings.npy.tmp" is written as "embeddings.npy.tmp.npy" and the rename then fails --
    # after paths.json has already been replaced, leaving the two files misaligned. Write both
    # temps first, verify both exist, and only then rename either one.
    tmp_p = paths_file.with_name("paths.tmp.json")
    tmp_e = emb_file.with_name("embeddings.tmp.npy")
    tmp_p.write_text(json.dumps(new_paths), encoding="utf-8")
    np.save(tmp_e, new_embs)
    if not (tmp_p.is_file() and tmp_e.is_file()):
        sys.exit("temp files were not both written -- index left untouched")
    tmp_e.replace(emb_file)
    tmp_p.replace(paths_file)
    (OUT / "state.json").write_text(json.dumps({"done": len(new_paths), "pruned": dead}),
                                    encoding="utf-8")
    print(f"\npruned {dead} row(s); index now {len(new_paths)} clips, embeddings {new_embs.shape}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
