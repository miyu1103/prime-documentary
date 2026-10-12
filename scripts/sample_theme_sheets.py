#!/usr/bin/env python3
"""One labelled contact sheet per shelf theme, so a person can see whether the theme is honest.

WHY THIS EXISTS
---------------
`build_asset_usability.py` ends every record with the same two lines, because they are true:

    - no human has confirmed the content matches the label
    - no check for a watermark, a logo or an identifiable real face

121,336 assets are marked usable and **not one of them has been looked at**. Reviewing them all
is not real work -- at 20 tiles a sheet that is 6,000 sheets. But the failure that has actually
reached shipped films is not a bad single clip, it is a **bad theme**: `evidence_bag` returned
cartoons, and every machine gate passed them because no gate reads a pixel. A wrong theme
poisons every episode that asks for it.

So this samples each theme instead. One sheet, 20 tiles, spread evenly across that theme's
usable assets rather than taken from the front (the first 20 files of a theme are usually one
ingest batch from one source, which would make a broken theme look consistent). Read the sheets;
a theme whose tiles do not match its own name gets quarantined wholesale.

Deterministic: the same shelf gives the same sample, so a second reviewer sees what the first
one saw.

    py -3.11 scripts/sample_theme_sheets.py                  # every theme
    py -3.11 scripts/sample_theme_sheets.py --theme prison_jail
    py -3.11 scripts/sample_theme_sheets.py --kind image     # image | video | all
"""
from __future__ import annotations

import argparse
import collections
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "runs" / "asset_usability.v001.jsonl"
SEL_DIR = ROOT / "runs" / "qc" / "_theme_selections"
OUT_DIR = ROOT / "runs" / "qc" / "theme_sheets"
PER_SHEET = 20


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--theme", default="", help="one theme (default: all)")
    ap.add_argument("--kind", default="all", choices=("image", "video", "all"))
    ap.add_argument("--per-sheet", type=int, default=PER_SHEET)
    args = ap.parse_args()

    if not RECORD.exists():
        sys.exit("run build_asset_usability.py first")

    by_theme: dict[str, list[dict]] = collections.defaultdict(list)
    for line in RECORD.open(encoding="utf-8"):
        rec = json.loads(line)
        if rec["rights"] != "clear":
            continue
        if args.kind != "all" and rec["kind"] != args.kind:
            continue
        if rec["kind"] not in ("image", "video"):
            continue
        if args.theme and rec.get("theme") != args.theme:
            continue
        by_theme[rec.get("theme") or "(none)"].append(rec)

    if not by_theme:
        sys.exit("nothing matched")
    SEL_DIR.mkdir(parents=True, exist_ok=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    made = 0
    for theme in sorted(by_theme):
        rows = sorted(by_theme[theme], key=lambda r: r["path"])
        # Even stride, not the first N: a theme's opening files are typically one ingest batch
        # from one source, which hides exactly the inconsistency this sheet exists to expose.
        step = max(1, len(rows) // args.per_sheet)
        picked = rows[::step][:args.per_sheet]
        items = [{"path": r["path"],
                  "label": f"{r['source']} | {(r.get('title') or '')[:40]}"} for r in picked]
        sel = SEL_DIR / f"{theme}.json"
        sel.write_text(json.dumps({"title": f"{theme} ({len(rows)} usable)", "items": items},
                                  ensure_ascii=False), encoding="utf-8")
        r = subprocess.run(["py", "-3.11", "scripts/build_footage_contact_sheet.py",
                            "--from-json", str(sel), "--out-dir", str(OUT_DIR)],
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        ok = r.returncode == 0
        print(f"  {theme:28s} {len(rows):6d} usable -> {len(picked):2d} tiles"
              f"{'' if ok else '   SHEET FAILED: ' + (r.stdout + r.stderr)[-90:]}")
        made += ok
    print(f"\n{made} sheet(s) in {OUT_DIR.relative_to(ROOT)}")
    print("OPEN THEM. A theme whose tiles do not match its own name is the defect this finds.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
