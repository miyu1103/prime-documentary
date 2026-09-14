#!/usr/bin/env python3
"""Turn an id-keyed full-frame verdict file into the rejects.json --decide expects.

The reviewer reads `runs/qc/fullframe/<slug>_candidates/NNN_<clip_id>.png`, one clip at a
time, and writes verdicts keyed by CLIP ID -- that is what is printed on the strip. But
`prestage_footage_review.py --decide` matches on the full staged FILENAME. Typing the
64-character filenames by hand is how a verdict ends up describing a clip that is not there.

This maps id -> filename through the run's own plan file, and REFUSES when the two sides
disagree: every presented clip must carry a verdict, and every verdict must name a clip that
was presented. A silent partial decision is the failure this whole prestage order exists to
prevent.

    py -3.11 scripts/expand_candidate_reasons.py --slug keybridge \
        --reasons runs/qc/keybridge_candidate_reasons.v001.json \
        --plan runs/qc/keybridge_prestage.v001.json --out runs/qc/keybridge_rejects.json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--reasons", required=True)
    ap.add_argument("--plan")
    ap.add_argument("--out")
    a = ap.parse_args()

    plan_path = Path(a.plan) if a.plan else ROOT / "runs" / "qc" / f"{a.slug}_prestage.v001.json"
    out_path = Path(a.out) if a.out else ROOT / "runs" / "qc" / f"{a.slug}_rejects.json"
    reasons = json.loads(Path(a.reasons).read_text(encoding="utf-8"))
    plan = json.loads(plan_path.read_text(encoding="utf-8"))

    by_id: dict[str, str] = {}
    for row in plan.get("presented", []):
        by_id[str(row["clip"]).split("__")[0]] = str(row["clip"])

    accept = reasons.get("accept", {})
    reject = reasons.get("reject", {})
    judged = set(accept) | set(reject)
    presented = set(by_id)

    both = sorted(set(accept) & set(reject))
    missing = sorted(presented - judged)
    unknown = sorted(judged - presented)
    if both or missing or unknown:
        for i in both:
            print(f"  BOTH accepted and rejected: {i}")
        for i in missing:
            print(f"  presented but never judged: {i}  ({by_id[i]})")
        for i in unknown:
            print(f"  judged but not presented in this run: {i}")
        print(f"[expand] refusing to write {out_path.name}: the verdict set and the presented "
              f"set do not match ({len(judged)} judged vs {len(presented)} presented)")
        return 1

    out = {
        "reviewer": reasons.get("reviewer", "unknown"),
        "method": ("full-frame, one clip at a time, 3 frames stacked at 960 px "
                   "(build_fullframe_strips.py --from-frames --stack). Ambiguity fails closed."),
        "reject": {by_id[i]: r for i, r in sorted(reject.items())},
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[expand] {a.slug}: {len(accept)} accepted, {len(reject)} rejected, "
          f"{len(presented)} presented -> {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
