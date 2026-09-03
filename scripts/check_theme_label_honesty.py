#!/usr/bin/env python3
"""Score every usable asset against the theme it was filed under, and name the bad themes.

WHAT THE SHEETS SHOWED
----------------------
`sample_theme_sheets.py` put 20 tiles of `courtroom_justice` on one page on 2026-09-04. One of
them was a courthouse. The other nineteen were a mountain range, a park path, a Delhi mosque, a
bedroom, a supermarket drinks aisle, a garden swing, stacking stones, an Italian fruit market,
a hiking trail and a woman reading Chomsky on a green screen. `prison_jail` was better and still
carried table tennis, grapes, three spiders and a cowboy saddle.

The queries are not the problem. The ingest asked pixabay for "judge bench gavel" and "prison
yard" -- good queries. **Pixabay matched them a word at a time**, returned "bank wooden bench
bench relax to sit sea" and "insect fauna spider yard colombia", and the ingest filed whatever
came back under the theme it had asked for. Nothing ever compared the result to the request, so
66 per cent of the shelf (80,166 pixabay assets) carries a theme label nobody checked.

WHAT THIS DOES
--------------
For each theme it derives a DISTINCTIVE vocabulary from that theme's own query list: words that
appear in at most two themes and are not generic scene furniture. `courtroom_justice` keeps
courtroom, courthouse, gavel, jury, judicial, attorney; it loses bench, room, case, reading,
desk, papers -- the exact words that let a park bench in.

Then it asks one question per asset: **does its title contain any distinctive word of its own
theme?** No is not proof the asset is wrong, and yes is not proof it is right -- a title is not
a picture. What the count does prove is which themes are worth a human's time, and 5 per cent
is not a rounding error.

Nothing is deleted and no decision changes. This writes `runs/theme_label_honesty.v001.json`
and prints the worst themes first.

    py -3.11 scripts/check_theme_label_honesty.py
    py -3.11 scripts/check_theme_label_honesty.py --theme courtroom_justice --show 25
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ingest_archive_sources import THEMES  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "runs" / "asset_usability.v001.jsonl"
OUT = ROOT / "runs" / "theme_label_honesty.v001.json"

# Words that describe any scene at all. Every one of these was observed letting an unrelated
# asset into a theme: "bench" (park bench -> courtroom), "yard" (spider yard -> prison),
# "case" (fruit case -> court case), "cell" (spider cell -> jail cell), "bars" (metal bars).
GENERIC = {
    "a", "an", "and", "at", "close", "closing", "down", "empty", "for", "from", "in", "of", "on",
    "onto", "out", "over", "the", "to", "under", "up", "with",
    "background", "bars", "bench", "block", "board", "book", "books", "box", "building",
    "buildings", "case", "cell", "chair", "city", "corridor", "desk", "document", "documents",
    "door", "doors", "file", "files", "floor", "glass", "hall", "hand", "hands", "interior",
    "light", "line", "man", "metal", "night", "office", "paper", "papers", "pen", "person",
    "photo", "picture", "reading", "road", "room", "seat", "seats", "shelf", "sign", "signing",
    "stack", "stairs", "steps", "street", "table", "up", "view", "wall", "walking", "wood",
    "wooden", "window", "woman", "work", "yard", "shot", "scene", "old", "new", "top", "front",
}
WORD = re.compile(r"[a-z]+")


def theme_vocabularies() -> dict[str, set[str]]:
    """Words per theme, kept only when they are rare across themes and not generic."""
    per: dict[str, set[str]] = {}
    for name, spec in THEMES.items():
        words: set[str] = set()
        for key in ("video", "image", "audio", "all"):
            for q in (spec.get(key) or []):
                words.update(WORD.findall(str(q).lower()))
        per[name] = {w for w in words if len(w) > 3 and w not in GENERIC}
    spread: collections.Counter = collections.Counter()
    for words in per.values():
        spread.update(words)
    # A word in three or more themes cannot tell them apart.
    return {name: {w for w in words if spread[w] <= 2} for name, words in per.items()}


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--theme", default="")
    ap.add_argument("--show", type=int, default=0, help="print N off-label titles for --theme")
    args = ap.parse_args()
    if not RECORD.exists():
        sys.exit("run build_asset_usability.py first")

    vocab = theme_vocabularies()
    stats: dict[str, dict] = collections.defaultdict(
        lambda: {"total": 0, "on_label": 0, "examples": []})
    for line in RECORD.open(encoding="utf-8"):
        rec = json.loads(line)
        if rec["rights"] != "clear" or rec["kind"] not in ("image", "video"):
            continue
        theme = rec.get("theme") or "(none)"
        if args.theme and theme != args.theme:
            continue
        words = vocab.get(theme)
        if not words:
            continue
        s = stats[theme]
        s["total"] += 1
        title = (rec.get("title") or "").lower()
        if set(WORD.findall(title)) & words:
            s["on_label"] += 1
        elif len(s["examples"]) < 30:
            s["examples"].append(rec.get("title") or rec["path"])

    rows = []
    for theme, s in stats.items():
        if s["total"] < 20:
            continue
        pct = 100.0 * s["on_label"] / s["total"]
        rows.append({"theme": theme, "usable": s["total"], "on_label": s["on_label"],
                     "on_label_pct": round(pct, 1),
                     "distinctive_words": sorted(vocab[theme])[:14],
                     "off_label_examples": s["examples"][:12]})
    rows.sort(key=lambda r: r["on_label_pct"])
    OUT.write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"{'theme':28s} {'usable':>7s} {'on-label':>9s}   worst first")
    for r in rows[:28]:
        print(f"  {r['theme']:26s} {r['usable']:7d} {r['on_label_pct']:8.1f}%")
    if args.theme and args.show:
        r = rows[0]
        print(f"\ndistinctive words: {', '.join(r['distinctive_words'])}")
        print("\noff-label titles:")
        for t in stats[args.theme]["examples"][:args.show]:
            print("   ", str(t)[:88])
    print(f"\nwrote {OUT.relative_to(ROOT)}")
    print("A title is not a picture: this ranks themes for review, it does not condemn assets.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
