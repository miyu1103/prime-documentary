#!/usr/bin/env python3
r"""Check a Short design against the episode's OWN machine contract and against length.

`check_short_design.py` proves every line traces to the script. It does not read the
`episode_spec`, so nothing was checking the two things that can actually stop a ship
(`.claude/rules/19`): a `forbidden_subjects` term in the narration, and a `forbidden_claims`
statement made in the film's own voice.

WHY THE HIGHEST REVISION AND NOT v001. The long-form thread measured this on 2026-08-24:
`episode_spec.v001.json` was hard-coded in 19 scripts, and lahaina's v001 says
`people_plates: null` while its v003 lists 24. Checking EP70 against v001 was correct only by
luck -- EP70 has no other revision. **EP71 oroville has v002 and EP75 lahaina has v003**, so the
very next episode in the queue would have been checked against a superseded contract. The
resolver is imported from `check_episode_spec`, not restated here.

WHAT IT MEASURES

  forbidden_subjects  word-boundary match against the spoken text of every line
  forbidden_claims    substring match for the short, quotable ones; the long prose entries are
                      PRINTED for a human instead, because a paragraph of policy cannot be
                      matched and pretending otherwise is worse than saying so
  plates              every source_plate exists on disk
  length              159-180 spoken words, measured off 28 finished Shorts that each run
                      58.0 s at a median 2.90 words/second

    py -3.11 scripts/check_short_constraints.py episodes/_planning/short_designs/*.json
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from check_episode_spec import spec_path  # noqa: E402 -- one resolver, not a second copy

WORDS_MIN, WORDS_MAX = 159, 180
WPS = 2.90


def plate_dir(slug: str) -> Path | None:
    for cand in (ROOT / "remotion" / "public" / slug / "img",
                 *sorted((ROOT / "remotion").glob(f"public_ep*/{slug}/img"))):
        if cand.is_dir():
            return cand
    return None


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 2

    problems = 0
    for path in args:
        d = json.loads(Path(path).read_text(encoding="utf-8"))
        epid, slug = d["episode_id"], d["slug"]
        epdir = ROOT / "episodes" / epid
        spec_file = spec_path(epdir)
        spec = json.loads(spec_file.read_text(encoding="utf-8"))
        subjects = [s.lower() for s in spec.get("forbidden_subjects", [])]
        short_subjects = [s for s in subjects if len(s) < 25 and " " not in s]
        claims = [c.lower() for c in spec.get("forbidden_claims", [])]
        short_claims = [c for c in claims if len(c) < 80]
        long_claims = [c for c in claims if len(c) >= 80]
        pdir = plate_dir(slug)
        avail = {p.stem for p in pdir.glob("*.png")} if pdir else set()

        print(f"\n{epid}   spec {spec_file.name}   plates {len(avail)}")
        for sh in d["shorts"]:
            text = " ".join(l["text"] for l in sh["lines"])
            low = text.lower()
            n = len(text.split())
            hits = [s for s in short_subjects if re.search(rf"\b{re.escape(s)}\b", low)]
            chits = [c[:50] for c in short_claims if c in low]
            miss = [p["source_plate"] for p in sh["plates"] if avail and p["source_plate"] not in avail]
            bad = bool(hits or chits or miss) or not (WORDS_MIN <= n <= WORDS_MAX)
            problems += bool(bad)
            print(f"  {sh['short_id']}  {n:>3} words ~{n / WPS:.0f}s"
                  f"{'' if WORDS_MIN <= n <= WORDS_MAX else '  <- OUTSIDE ' + str(WORDS_MIN) + '-' + str(WORDS_MAX)}")
            if hits:
                print(f"      forbidden_subjects in narration: {hits}")
            if chits:
                print(f"      forbidden_claims matched: {chits}")
            if miss:
                print(f"      plates not on disk: {miss}")
        if long_claims:
            print(f"  {len(long_claims)} forbidden_claim(s) are prose and CANNOT be matched by a "
                  f"machine. A person reads these against the Shorts:")
            for c in long_claims:
                print(f"      - {c[:150]}")

    print(f"\n{len(args)} design(s) checked, {problems} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
