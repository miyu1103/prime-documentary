#!/usr/bin/env python
"""Report cards that draw on top of each other in a built film json.

WHY THIS EXISTS. Figure beats and AE beats are produced by different functions that
never see each other, and until 2026-09-07 nothing compared them. Measured on EP83
max737: seven card-on-card overlaps survived a render, including 6.0 s of "THE 737 MAX
WAS DESIGNED TO LAND ON LEVEL B" printed through "DECEMBER 2011. A CONTRACT WITH THE
LAUNCH CUSTOMER." Two cards at once is one unreadable card.

The builder now de-collides and staggers. This is the check that proves it did, and it
runs on the file that ships -- not on the builder's intentions.

    py -3.11 scripts/check_card_overlaps.py --slug max737

Exit 0 when clean, 1 when anything overlaps. The AI disclosure is included: invariant 11
is not satisfied by a disclosure another card is covering.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
MIN_REPORT = 0.20  # a few frames of touch is not a legibility problem


def label(f: dict) -> str:
    kind = f.get("kind") or "?"
    for k in ("primary", "text", "quote", "title", "lines"):
        v = f.get(k)
        if isinstance(v, list) and v:
            v = " ".join(str(x) for x in v)
        if v:
            t = str(v).replace("\n", " ")
            return f"[{kind}] {t[:44]}"
    return f"[{kind}]"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    a = ap.parse_args()

    path = ROOT / f"remotion/src/data/{a.slug}_film.json"
    if not path.is_file():
        print(f"no film json at {path}", file=sys.stderr)
        return 1
    film = json.loads(path.read_text(encoding="utf-8"))
    figs = sorted(film.get("figures") or [], key=lambda x: x["start"])
    ae = [(b["atSec"], b["atSec"] + b["durSec"]) for b in (film.get("aeBeats") or [])]

    card_hits = []
    for i, f in enumerate(figs):
        for g in figs[i + 1:]:
            if g["start"] >= f["end"]:
                break
            ov = min(f["end"], g["end"]) - g["start"]
            if ov > MIN_REPORT:
                card_hits.append((ov, f, g))

    ae_hits = []
    for f in figs:
        for a0, a1 in ae:
            ov = min(f["end"], a1) - max(f["start"], a0)
            if ov > MIN_REPORT:
                ae_hits.append((ov, f, (a0, a1)))

    for ov, f, g in card_hits:
        print(f"  CARD-ON-CARD {ov:4.1f}s @{f['start']:7.1f}  {label(f)}  ||  {label(g)}")
    for ov, f, (a0, a1) in ae_hits:
        print(f"  CARD-ON-AE   {ov:4.1f}s @{f['start']:7.1f}  {label(f)}  ||  AE {a0:.1f}-{a1:.1f}")

    total = len(card_hits) + len(ae_hits)
    print(f"\n{a.slug}: {len(figs)} figures, {len(ae)} AE beats -- "
          f"{len(card_hits)} card-on-card, {len(ae_hits)} card-on-AE")
    return 1 if total else 0


if __name__ == "__main__":
    raise SystemExit(main())
