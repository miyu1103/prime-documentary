#!/usr/bin/env python3
"""Turn every FOOTAGE plate that could not be bound to a real clip into a GENERATE plate.

An unbound FOOTAGE plate is a hole: it carries `prompt: null` because it was never meant to be
generated, so it would reach the build with nothing to show. 135 of 562 footage plates could not
be bound — either the ledger has no clip whose TITLE matches, or the only matches do not survive a
9:16 centre crop. Leaving them as FOOTAGE would fail silently at assembly time.

The replacement prompt is composed from the plate's own `subject` plus the same five hard rules
every other prompt carries, so it passes verify_short_plates.py by construction rather than by
hand. `converted_from_footage: true` is recorded so the next reader knows this plate is a
fallback and not a first choice.

Usage: py -3.11 scripts/convert_unbound_footage.py [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGNS = ROOT / "episodes" / "_planning" / "short_designs"
VOCAB = json.loads((ROOT / "episodes" / "_planning" / "SHORTS_MOTIF_VOCABULARY.v001.json")
                   .read_text(encoding="utf-8"))
SUFFIX = VOCAB["style_suffix"]

RULES = (", lit ONLY by one hard practical light source which is switched on and is the only "
         "light in frame, no lettering, no signage and no readable text anywhere, every document "
         "surface and dial blank, no face or likeness visible, the subject held in the middle "
         "third of the tall vertical frame with the top and the bottom of the frame left empty "
         "and dark")


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    converted = 0
    still_bad = []
    for f in sorted(DESIGNS.glob("*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        dirty = False
        for s in d["shorts"]:
            era = s.get("era") or "the period of the case"
            for p in (s.get("plates") or []):
                if not p or p.get("source") != "FOOTAGE" or p.get("bound_file"):
                    continue
                subj = (p.get("subject") or "").strip().rstrip(".")
                if not subj:
                    still_bad.append(f"{s['short_id']} n{p.get('n')}: no subject to build from")
                    continue
                p["source"] = "GENERATE"
                p["converted_from_footage"] = True
                p["prompt"] = subj + RULES + SUFFIX.replace("{ERA}", era)
                p.pop("footage_query", None)
                converted += 1
                dirty = True
        if dirty and not args.dry_run:
            f.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"converted {converted} unbound FOOTAGE plates to GENERATE")
    if still_bad:
        print(f"  {len(still_bad)} could not be converted:")
        for x in still_bad[:10]:
            print("    " + x)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
