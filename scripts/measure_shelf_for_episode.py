#!/usr/bin/env python3
r"""Measure what the shelf can actually supply for ONE episode, term by term.

WHY THIS EXISTS
---------------
`prestage_footage_review.py` refuses to run for any slug with no entry in
`config/episode_footage_queries.v001.json`, and that entry is supposed to be derived from a
`FOOTAGE_PLAN` in which **every term is one somebody measured a usable count for**. EP69
hyatt's plan says so in its own note, and lists five terms it deliberately excluded because
their high hit counts were measured to be misleading ('plant' -> botany, 'rig' -> the word
'bright', 'sign' -> readable signage that places the shot elsewhere).

Until 2026-08-20 that measurement was done by hand each time. EP70 and EP71 have no plan at
all, and the H: loss means the shelf they would have been measured against no longer exists —
what remains is 54,315 reindexed rows of which only ~2,750 videos carry a licence that clears
commercial use. Guessing terms against a shelf that changed this much produces a query set
that stages nothing, or worse, stages the wrong thing and passes.

WHAT IT MEASURES, AND WHAT IT REFUSES TO GUESS
----------------------------------------------
For each candidate term, against video rows whose `license_decision` is `pd`:

  usable      word-boundary hits in title + path
  blocked     of those, how many have a `forbidden_subjects` word in the FILENAME --
              because `check_spec_satisfied` matches those against the staged filename, so
              such a clip is an automatic build failure however good it looks
  net         usable - blocked, i.e. what the term would really contribute
  sources     which sources it draws from, so a term supplied by one source is visible

A term that IS a forbidden word is reported as such and must never enter the query set.

It does NOT decide the query set. A hit count is not a supply count: EP71's own spec measured
1,293 candidates and a 70-clip sample judged **50% off-register**. This narrows the list a
human then looks at.

    py -3.11 scripts/measure_shelf_for_episode.py --slug wronghouse
    py -3.11 scripts/measure_shelf_for_episode.py --slug wronghouse --terms terms.txt
    py -3.11 scripts/measure_shelf_for_episode.py --slug wronghouse --min 3 --json out.json
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from shelf import shelf_rows  # noqa: E402

VIDEO_EXT = (".mp4", ".mov", ".mkv", ".webm")

# A starting vocabulary. It is deliberately broad and ordinary -- the point is to find out
# which of these the shelf answers, not to be clever. Override with --terms.
DEFAULT_TERMS = """
house home suburban suburb driveway porch doorway door lawn fence mailbox garage
hallway corridor stairs staircase bedroom kitchen window curtain blinds room interior
street neighborhood residential road sidewalk rain night dusk dawn
courthouse court judge lawyer legal justice government federal columns marble civic
office desk paperwork document paper file folder cabinet typewriter computer keyboard
car vehicle police patrol siren truck van driving
flashlight dark silhouette shadow walking hands feet
atlanta georgia pine forest trees field
vintage retro telephone rotary television radio archive
"""


def spec_for(slug: str) -> dict:
    hits = sorted((ROOT / "episodes").glob(f"PD-*-{slug}/episode_spec.v001.json"))
    if not hits:
        raise SystemExit(f"no episode_spec.v001.json for slug {slug!r}")
    return json.loads(hits[-1].read_text(encoding="utf-8"))


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--terms", help="file with whitespace-separated candidate terms")
    ap.add_argument("--min", type=int, default=1, help="hide terms below this net count")
    ap.add_argument("--json", help="also write the table here")
    args = ap.parse_args()

    spec = spec_for(args.slug)
    forb = {t.lower() for t in (spec.get("forbidden_subjects") or [])}
    era = spec.get("era_setting", {})
    print(f"slug   : {args.slug}")
    print(f"place  : {str(era.get('place', ''))[:90]}")
    print(f"years  : {era.get('years')}")
    print(f"forbidden terms: {len(forb)}   distinct_video_assets required: "
          f"{spec.get('distinct_video_assets')}")

    rows: list[tuple[str, str, str]] = []
    total = usable = 0
    for r in shelf_rows():
        p = str(r.get("file_path", ""))
        if not p.lower().endswith(VIDEO_EXT):
            continue
        total += 1
        if r.get("license_decision") != "pd":
            continue
        usable += 1
        # Match the TITLE and the FILENAME only. Measured 2026-08-20: including the
        # full path made every single row match the term "archive", because every row lives
        # under `D:\pd-archive` and the separator normalisation turns that into "pd archive".
        # 1,928 hits, all of them the folder name. A term measured against its own storage
        # path is the same class of lie as a process check that matches its own signature.
        base = p.replace("\\", "/").rsplit("/", 1)[-1]
        hay = (str(r.get("title", "")) + " " + base).lower()
        hay = hay.replace("_", " ").replace("-", " ")
        rows.append((hay, base.lower().replace("_", " ").replace("-", " "),
                     str(r.get("source", "?"))))
    print(f"shelf  : {total} video rows, {usable} with a clear commercial licence "
          f"({total - usable} review_required and NOT counted below)")

    terms = (Path(args.terms).read_text(encoding="utf-8") if args.terms
             else DEFAULT_TERMS).split()
    forb_pat = {f: re.compile(r"\b" + re.escape(f) + r"\b") for f in forb}

    out = []
    for term in dict.fromkeys(t.lower() for t in terms):
        if term in forb:
            out.append({"term": term, "usable": 0, "blocked": 0, "net": 0,
                        "sources": {}, "verdict": "FORBIDDEN -- never put this in a query"})
            continue
        pat = re.compile(r"\b" + re.escape(term) + r"\b")
        hits = blocked = 0
        src: collections.Counter = collections.Counter()
        for hay, base, source in rows:
            if not pat.search(hay):
                continue
            hits += 1
            if any(fp.search(base) for fp in forb_pat.values()):
                blocked += 1
            else:
                src[source] += 1
        out.append({"term": term, "usable": hits, "blocked": blocked,
                    "net": hits - blocked, "sources": dict(src),
                    "verdict": "ok" if hits else "zero -- the shelf does not answer this word"})

    out.sort(key=lambda d: -d["net"])
    print()
    print(f"{'term':<16}{'net':>6}{'blocked':>9}  sources")
    for d in out:
        if d["verdict"].startswith("FORBIDDEN"):
            print(f"  {d['term']:<14}{'--':>6}{'--':>9}  {d['verdict']}")
        elif d["net"] >= args.min:
            s = ", ".join(f"{k} {v}" for k, v in
                          sorted(d["sources"].items(), key=lambda kv: -kv[1])[:3])
            print(f"  {d['term']:<14}{d['net']:>6}{d['blocked']:>9}  {s}")
    zero = [d["term"] for d in out if d["net"] < args.min
            and not d["verdict"].startswith("FORBIDDEN")]
    if zero:
        print()
        print(f"below --min ({args.min}): {', '.join(zero)}")

    print()
    print("A hit count is NOT a supply count. Before any of these enters the query set, "
          "open a labelled contact sheet and look: EP71's spec measured a 70-clip sample "
          "at 50% off-register.")

    if args.json:
        Path(args.json).write_text(json.dumps(out, ensure_ascii=False, indent=1),
                                   encoding="utf-8")
        print(f"wrote {args.json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
