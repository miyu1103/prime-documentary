#!/usr/bin/env python3
"""Write the per-Short lines file the narration builder reads, from the design.

The design JSON is where a Short's spine is authored and checked (check_short_design verifies every
line against the episode script). The narration builder reads a different file -
`episodes/<EPID>/09_package/short<NN>_lines.v001.json` - and until now that was written by hand,
which is one more place the same eight sentences can drift apart.

This derives it. The design stays the single source; the lines file becomes a build artefact.

Delivery is carried through as authored. `source` is always "rerecord": these are new Shorts with
no prior take to reuse.

Usage:
  py -3.11 scripts/emit_short_lines.py --designs PD-2026-066-openfields --dry-run
  py -3.11 scripts/emit_short_lines.py --all --apply
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGNS = ROOT / "episodes" / "_planning" / "short_designs"


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--designs", help="comma-separated design stems, e.g. PD-2026-066-openfields")
    g.add_argument("--all", action="store_true")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    if not a.apply and not a.dry_run:
        ap.error("pass --apply or --dry-run")

    if a.all:
        files = sorted(DESIGNS.glob("*.json"))
    else:
        files = [DESIGNS / f"{s.strip()}.design.v001.json" for s in a.designs.split(",")]

    written, skipped = 0, []
    for f in files:
        if not f.is_file():
            skipped.append(f"{f.name}: not found")
            continue
        d = json.loads(f.read_text(encoding="utf-8"))
        pkg = ROOT / "episodes" / d["episode_id"] / "09_package"
        if not pkg.is_dir():
            skipped.append(f"{d['episode_id']}: no 09_package directory")
            continue
        for s in d.get("shorts", []):
            nn = re.sub(r"\D", "", s["short_id"])
            out = pkg / f"short{nn}_lines.v001.json"
            lines = [
                {
                    "id": ln["id"],
                    "delivery": ln.get("delivery", "flat"),
                    "source": "rerecord",
                    "text": ln["text"],
                    "provenance": ln.get("source_lines", []),
                }
                for ln in s["lines"]
            ]
            print(f"  short{nn}: {len(lines)} lines -> {out.relative_to(ROOT)}")
            written += 1
            if a.apply:
                out.write_text(json.dumps(lines, ensure_ascii=False, indent=1) + "\n",
                               encoding="utf-8")

    print(f"\n{written} lines file(s)" + ("" if a.apply else "   (DRY RUN)"))
    for s in skipped:
        print("  " + s)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
