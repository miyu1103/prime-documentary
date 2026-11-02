#!/usr/bin/env python3
"""Record a pool_frame_review block after a human has read every staged clip full frame.

`check_pool_frames.py --sheets-only` produces the evidence and refuses to pass; the reviewer
then has to write the block by hand into `runs/qc/<slug>_clip_verdicts.v001.json`, including a
pool hash that changes the moment a rejected clip is moved out of the pool. Hand-editing that
is how a verdict ends up bound to a pool that no longer exists.

This takes the decision as {accept: {clip_id: why}, reject: {clip_id: why}}, moves the rejects
out FIRST, recomputes the hash of the pool that actually remains, and only then writes. It
refuses when a staged clip carries no verdict, or a verdict names a clip that is not staged.

    py -3.11 scripts/write_pool_frame_review.py --slug keybridge \
        --decision runs/qc/keybridge_pool_decision.v001.json --reviewer "name"
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from check_pool_frames import pool_id_hash  # noqa: E402


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--decision", required=True,
                    help="json {accept: {clip_id: why}, reject: {clip_id: why}} -- clip IDs, "
                         "the prefix before '__', which is what the review strips are labelled with")
    ap.add_argument("--reviewer", required=True)
    ap.add_argument("--method", default="full frame, one clip at a time, 3 frames stacked at "
                                        "960 px. Ambiguity fails closed.")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    pool = ROOT / "remotion" / "public" / a.slug / "factory"
    verdicts_path = ROOT / "runs" / "qc" / f"{a.slug}_clip_verdicts.v001.json"
    decision = json.loads(Path(a.decision).read_text(encoding="utf-8"))
    accept, reject = decision.get("accept", {}), decision.get("reject", {})

    staged = {p.name.split("__")[0]: p for p in sorted(pool.glob("*.mp4"))}
    # A reject whose file has already been moved out is DONE, not unknown. Without this the
    # script cannot be run twice, and a run that dies between the move and the write leaves
    # the pool clean and the verdict unrecorded -- which is the worst of the two states.
    out_dir = pool / "_eyeball_reject"
    already_out = {p.name.split("__")[0]: p for p in sorted(out_dir.glob("*.mp4"))} if out_dir.is_dir() else {}
    judged = set(accept) | set(reject)
    missing = sorted(set(staged) - judged)
    unknown = sorted(judged - set(staged) - set(already_out))
    if missing or unknown or (set(accept) & set(reject)):
        for i in missing:
            print(f"  staged but not judged: {i}")
        for i in unknown:
            print(f"  judged but not staged: {i}")
        for i in sorted(set(accept) & set(reject)):
            print(f"  both accepted and rejected: {i}")
        print("[pool-review] refusing to write: the verdicts and the pool do not match")
        return 1

    verdicts = json.loads(verdicts_path.read_text(encoding="utf-8"))
    rejected_block = verdicts.setdefault("rejected", {})

    for cid, why in sorted(reject.items()):
        src = staged.get(cid)
        if src is None:                      # already moved out by an earlier run
            rejected_block[already_out[cid].name] = why
            print(f"  rejected (already out): {already_out[cid].name}")
            continue
        rejected_block[src.name] = why
        if not a.dry_run:
            out_dir.mkdir(exist_ok=True)
            shutil.move(str(src), str(out_dir / src.name))
        print(f"  rejected -> _eyeball_reject: {src.name}")

    remaining = sorted(p.name for p in pool.glob("*.mp4"))
    pool_hash = pool_id_hash(remaining)
    verdicts["pool_frame_review"] = {
        "reviewer": a.reviewer,
        "reviewed_at": date.today().isoformat(),
        "method": a.method,
        "pool_id_sha256": pool_hash,
        "reviewed_clips": sorted((staged.get(c) or already_out[c]).name for c in judged),
        "accepted": remaining,
        "accept_reasons": {staged[c].name: w for c, w in sorted(accept.items())},
    }
    if a.dry_run:
        print(f"[pool-review] DRY RUN: would record {len(accept)} accepted, {len(reject)} "
              f"rejected; pool would hold {len(remaining)} clip(s)")
        return 0
    verdicts_path.write_text(json.dumps(verdicts, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[pool-review] {a.slug}: {len(accept)} accepted, {len(reject)} rejected. "
          f"Pool holds {len(remaining)} clip(s), hash {pool_hash[:12]} -> {verdicts_path.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
