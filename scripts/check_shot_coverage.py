#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Run each channel's shot list against the shelf and report what can actually be cut.

The item count answers "how big is the shelf", which is not a production question. On
2026-08-06 that distinction was measured: Prime Business reached 90% coverage on 19,704
items and needed nothing more, while Prime Finance would not reach 100% at any item count,
because seven of its shots are not on any free source at all.

This was done by hand then. It has to be a script, because every purge changes the answer
and there is no way to tell from a deletion count whether an episode still dresses. 498 GB
came off the shelf on 2026-08-09 alone.

Scoring is imported from search_archive, not reimplemented, so a change to relevance moves
this measurement with it (CLAUDE invariant 14). One pass over the ledgers scores every shot
of every channel at once; running search_archive 60 times would re-read 286k rows each time.

    python scripts/check_shot_coverage.py
    python scripts/check_shot_coverage.py --channel "Prime Finance" --verbose
    python scripts/check_shot_coverage.py --md   # table for the planning doc
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import search_archive as sa  # noqa: E402  scoring, verdicts and quarantine all live here
from shelf import shelf_rows  # noqa: E402  the one definition of "on the shelf"

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHOTS = os.path.join(ROOT, "config", "shot_coverage_shots.v002.json")


def shot_terms(shot: str) -> tuple[list[str], list[str]]:
    """Split a shot into the words and adjacent pairs search_archive scores against."""
    words = [w for w in re.findall(r"[a-z]+", shot.lower()) if len(w) > 2]
    bigrams = [f"{a} {b}" for a, b in zip(words, words[1:])]
    return words, bigrams


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--channel", help="measure one channel only")
    ap.add_argument("--kind", default="", help="video / image / audio (default: any)")
    ap.add_argument("--verbose", action="store_true", help="list every shot")
    ap.add_argument("--md", action="store_true", help="emit a markdown table")
    args = ap.parse_args()

    with open(SHOTS, encoding="utf-8") as fh:
        cfg = json.load(fh)
    serviceable_min = cfg["thresholds"]["serviceable_min_hits"]
    still_short = cfg.get("still_short", {})
    channels = {k: v for k, v in cfg["channels"].items()
                if not args.channel or k == args.channel}
    if not channels:
        print(f"unknown channel; known: {', '.join(cfg['channels'])}")
        return 2

    verdicts = sa.load_verdicts()
    quarantined = sa.load_quarantined()
    feedback = sa.load_feedback()

    # shot -> hit count, and the per-shot term lists, prepared once.
    terms = {}
    counts = {}      # score > 15: what a shot spec may actually cite
    weak = {}        # score > 0:  material that exists but the phrasing does not reach
    for ch, shots in channels.items():
        for s in shots:
            terms[s] = shot_terms(s)
            counts[s] = 0
            weak[s] = 0

    scanned = 0
    for rec in shelf_rows():
        fp = rec.get("file_path", "") or ""
        if args.kind and sa.kind_of(fp) != args.kind:
            continue
        if f"{rec.get('source')}:{rec.get('id')}" in quarantined:
            continue
        if "_quarantine" in fp.lower():
            continue
        if verdicts.get((rec.get("theme", ""), rec.get("source", ""))) == "unusable":
            continue
        scanned += 1
        fbkey = f"{rec.get('source')}:{rec.get('id')}"
        exists = None
        for shot, (words, bigrams) in terms.items():
            sc = sa.apply_feedback(
                sa.shot_score(rec, words, bigrams, True), fbkey, feedback)
            if sc <= 0:
                continue
            if exists is None:            # stat once per row, not once per shot
                exists = os.path.exists(fp)
            if not exists:
                continue
            weak[shot] += 1
            if sc > 15:
                counts[shot] += 1

    print(f"scored {scanned:,} shelf rows"
          + (f" (kind={args.kind})" if args.kind else "") + "\n")

    rows = []
    for ch, shots in channels.items():
        serv = [s for s in shots if counts[s] >= serviceable_min]
        thin = [s for s in shots if 0 < counts[s] < serviceable_min]
        none = [s for s in shots if counts[s] == 0]
        pct = len(serv) / max(len(shots), 1) * 100
        rows.append((ch, len(serv), len(shots), len(thin), len(none), pct))
        print(f"{ch}")
        print(f"  使える {len(serv)}/{len(shots)}   薄い(1-2) {len(thin)}   ゼロ {len(none)}"
              f"   → {pct:.0f}%")
        if none:
            # A weak-hit count alone cannot tell a wording problem from a supply problem:
            # `savings passbook close up` has 5,072 weak hits and exactly two real
            # passbooks behind them, the rest banknote stills carrying the tag. So a shot
            # someone has actually LOOKED at reports what they found; only an unexamined
            # one falls back to the weak count, and says so.
            for s in none:
                if s in still_short:
                    print(f"  確認済み・不足: {s} — {still_short[s]}")
                elif weak[s] == 0:
                    print(f"  素材なし（買う/生成する）: {s}")
                else:
                    print(f"  未確認・弱一致 {weak[s]}件: {s}"
                          f" (search_archive --shot \"{s}\" --weak-ok --sheet で見ること)")
        if thin:
            print(f"  薄い: {', '.join(f'{s}({counts[s]}/弱{weak[s]})' for s in thin)}")
        if args.verbose:
            for s in shots:
                mark = "OK " if counts[s] >= serviceable_min else (
                    "thin" if counts[s] else "NONE")
                print(f"    {mark:4} {counts[s]:5,}  {s}")
        print()

    if args.md:
        print("| Channel | Serviceable | Thin (1-2) | None | Coverage |")
        print("|---|---:|---:|---:|---:|")
        for ch, s, t, th, n, pct in rows:
            print(f"| **{ch}** | {s}/{t} | {th} | {n} | {pct:.0f}% |")
    return 0


if __name__ == "__main__":
    sys.exit(main())
