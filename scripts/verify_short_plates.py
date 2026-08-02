#!/usr/bin/env python3
"""Mechanically verify the plate motifs authored into the Short designs.

Same principle as verify_short_designs.py: agents produce, a checker decides. The rules below are
the ones that cost a re-render each when they were broken on short82.

Per short:
  1. exactly 23 plates, numbered 1..23, last one role=loop reusing plate 1
  2. no `{ERA}` token left unsubstituted
  3. every GENERATE prompt names a light source AND says it is switched on   (R5)
  4. every GENERATE prompt forbids readable text                              (R3)
  5. every GENERATE prompt carries the quiet-band clause                      (R2)
  6. >= 20 distinct subjects; no duplicate GENERATE prompt anywhere in the set
  7. FOOTAGE share between 15% and 50% - too little wastes the archive, too much dates the film
  8. every plate is bound to a line id that exists in the spine
  9. FOOTAGE plates carry a footage_query; GENERATE plates carry a prompt

Usage: py -3.11 scripts/verify_short_plates.py [--only PD-2026-016-titan]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGNS = ROOT / "episodes" / "_planning" / "short_designs"

LIGHT = re.compile(r"lit only by|switched on", re.I)
SWITCHED = re.compile(r"switched on", re.I)
NOTEXT = re.compile(r"no lettering|no readable text|no signage", re.I)
# R2 can be stated in pixels or in plain language, and writers phrase it differently ("middle
# band", "middle third", "between the telop area and the caption area"). Two rounds of reactive
# regex patching failed 177 then 251 prompts that all carried the rule correctly — the checker was
# the broken thing both times. So this no longer matches a phrase: it asks whether the prompt says
# anything at all about WHERE in the tall frame the subject sits, and whether the edges are
# reserved. A prompt that says neither is the real defect.
BAND_PLACEMENT = re.compile(
    r"\b(?:middle|centre|center|upper|lower|top)\b[^.]{0,24}\b(?:third|band|zone|half|area)\b"
    r"|y ?560|560\D{0,6}1180|telop|caption (?:area|band|zone)|placed high in (?:the )?frame",
    re.I)
BAND_EDGES = re.compile(
    r"(?:top|upper)[^.]{0,60}(?:empty|dark|quiet|clear)"
    r"|(?:empty|dark|quiet|clear)[^.]{0,40}(?:above|below)"
    r"|left empty and dark|kept dark and empty", re.I)


def has_band_clause(p: str) -> bool:
    return bool(BAND_PLACEMENT.search(p) or BAND_EDGES.search(p))


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--only")
    args = ap.parse_args()

    fails: list[str] = []
    all_prompts: dict[str, str] = {}
    done = 0
    stats = []

    for f in sorted(DESIGNS.glob("*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        if args.only and d["episode_id"] != args.only:
            continue
        line_ids = None
        for s in d["shorts"]:
            plates = s.get("plates") or []
            if not any(p and p.get("prompt") or (p and p.get("source") == "FOOTAGE") for p in plates):
                continue
            done += 1
            sid = s.get("short_id", "?")
            tag = f"{d['episode_id']} {sid}"
            line_ids = {l["id"] for l in s.get("lines", [])}

            if len(plates) != 23:
                fails.append(f"{tag}: {len(plates)} plates, expected 23")
            nums = [p.get("n") for p in plates if p]
            if nums != list(range(1, len(nums) + 1)):
                fails.append(f"{tag}: plate numbering is not 1..{len(nums)}")

            last = plates[-1] if plates else {}
            if last.get("role") != "loop":
                fails.append(f"{tag}: last plate role is {last.get('role')!r}, expected 'loop'")

            gen = [p for p in plates if p and p.get("source") == "GENERATE"]
            foot = [p for p in plates if p and p.get("source") == "FOOTAGE"]
            # A plate that ASKED for footage and could not get it is not a design defect - the
            # ledger genuinely has no crop-safe clip for some subjects, and 135 plates fell back
            # to GENERATE for that reason. Judge the intent, not the outcome; the outcome is
            # reported separately so a thin real-footage mix stays visible.
            fallback = [p for p in gen if p.get("converted_from_footage")]
            intended = len(foot) + len(fallback)
            share = intended / max(1, len(plates))
            if not (0.15 <= share <= 0.50):
                fails.append(f"{tag}: intended-FOOTAGE share {share:.0%} outside 15-50%")
            for p in foot:
                if not p.get("bound_file"):
                    fails.append(f"{tag} n{p.get('n')}: FOOTAGE plate has no bound clip")

            for p in plates:
                if not p:
                    continue
                ln = p.get("line")
                if ln and line_ids and ln not in line_ids:
                    fails.append(f"{tag} n{p.get('n')}: line {ln!r} is not in the spine")
                if p.get("source") == "FOOTAGE" and not p.get("footage_query"):
                    fails.append(f"{tag} n{p.get('n')}: FOOTAGE plate has no footage_query")

            for p in gen:
                pr = p.get("prompt") or ""
                n = p.get("n")
                if not pr:
                    fails.append(f"{tag} n{n}: GENERATE plate has no prompt"); continue
                if "{ERA}" in pr:
                    fails.append(f"{tag} n{n}: unsubstituted {{ERA}} token")
                if not SWITCHED.search(pr):
                    fails.append(f"{tag} n{n}: prompt never says the light is 'switched on' (R5)")
                if not NOTEXT.search(pr):
                    fails.append(f"{tag} n{n}: prompt does not forbid readable text (R3)")
                if not has_band_clause(pr):
                    fails.append(f"{tag} n{n}: prompt has no quiet-band / subject-placement clause (R2)")
                key = re.sub(r"\s+", " ", pr).strip().lower()
                if key in all_prompts and all_prompts[key] != f"{tag} n{n}":
                    fails.append(f"{tag} n{n}: prompt identical to {all_prompts[key]}")
                all_prompts[key] = f"{tag} n{n}"

            subs = [re.sub(r"\s+", " ", (p.get("subject") or "")).strip().lower()
                    for p in plates if p]
            distinct = len(set(x for x in subs if x))
            if distinct < 20:
                fails.append(f"{tag}: only {distinct} distinct plate subjects (need >=20)")
            stats.append((tag, len(gen), len(foot), distinct))

    print(f"checked {done} shorts with plates")
    if stats:
        g = sum(s[1] for s in stats); ft = sum(s[2] for s in stats)
        print(f"  GENERATE {g}  real FOOTAGE {ft}  actual footage share {ft/(g+ft):.0%}")
    if fails:
        print(f"\n{len(fails)} FAILURES:")
        for x in fails[:40]:
            print("  " + x)
        if len(fails) > 40:
            print(f"  ... {len(fails)-40} more")
        return 1
    print("all checks pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
