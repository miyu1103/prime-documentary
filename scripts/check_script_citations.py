#!/usr/bin/env python3
"""Cross-check an episode's script against its own facts ledgers.

Why this exists: the citation convention -- every narrated factual line followed by an HTML
comment carrying its ledger row id -- has been in every PD design document since EP66, and until
now nothing read it. Four things can go wrong and all four are silent:

  1. A narration line carries no citation at all. The convention says such a line "does not enter
     the script"; nothing checked whether one had.
  2. A citation names a row id that does not exist in any ledger -- a typo, or a row that was
     renumbered by a later revision. EP74 renumbered IT-40..IT-54 mid-session when a row was
     inserted; a stale citation would have pointed at the wrong fact, not at nothing.
  3. A citation names a row the ledger itself marks UNREAD -- seen only in a search-engine summary
     and explicitly not usable. EP74 carried four of those and the quarantine rule says none may
     enter a script line. Nothing enforced it.
  4. A citation names a row a later revision SUPERSEDED. EP74's IT-58 was replaced by IT-93/IT-94
     after the article was actually fetched; a line still citing IT-58 would be sourced to a row
     its own ledger has retired.

It also reports quarantine rules that are cited by the script but are not written as table rows,
because a rule a machine cannot find is the "decoration" problem this repository already names:
EP74's quarantine rule 15 was written as a bold prose paragraph and was invisible to every tool.

    py -3.11 scripts/check_script_citations.py --slug itaewon
    py -3.11 scripts/check_script_citations.py --slug itaewon --verbose
    py -3.11 scripts/check_script_citations.py --all

Exit 0 = every citation resolves to a live, readable ledger row. Exit 1 = at least one does not.
This does NOT judge whether a cited row actually supports the sentence citing it. Only a person
reading both can do that.
"""
from __future__ import annotations

import argparse
import collections
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
PLANNING = ROOT / "episodes" / "_planning"

# The lookbehind is load-bearing, added 2026-08-21 on EP76. Without it `[A-Z]{2}-\d+` matches
# INSIDE a longer id: a citation comment that names its source as SRC-0001 yields a phantom
# `RC-0001`, and the gate reports an UNDEFINED ID that no script ever wrote. Measured the same day:
# it was firing on EP71 (RC-0005), EP75 (RC-0014) and EP76 (RC-0001, RC-0003). The same run found a
# REAL defect on EP76 -- a line citing a source id instead of a row -- so this fix must not silence
# the check, only stop it inventing ids.
ID = r"(?<![A-Za-z])(?:(?:IT|LM|[A-Z]{2})-\d+[a-z]?|AB-\d+|⛔-\d+)"
ROW_DEF = re.compile(r"^\|\s*(" + ID + r")\s*\|", re.M)
UNREAD_ROW = re.compile(r"^\|\s*(" + ID + r")\s*\|.*?\|\s*\*{0,2}UNREAD\*{0,2}\s*\|", re.M)
SUPERSEDED = re.compile(r"`(" + ID + r")`\s+is hereby superseded|\*\*(" + ID + r") is cut\*\*")
CITE = re.compile(ID)

SKIP_PREFIX = ("#", "|", ">", "---", "<!--", "【", "*", "```", "- ", "1.", "2.", "3.", "4.", "5.")
# A stage direction written as bare capitals ("DESIGNED SILENCE 3.0 s") is not a narrated line.
DIRECTION = re.compile(r"^[A-Z0-9 .,:;/&()\x27-]+$")


def newest_script(prefix: str) -> Path | None:
    cands = sorted(PLANNING.glob(f"{prefix}_script.en.v*.md"))
    return cands[-1] if cands else None


def check(prefix: str, verbose: bool = False, strict: bool = False) -> bool:
    script = newest_script(prefix)
    ledgers = sorted(PLANNING.glob(f"{prefix}_FACTS_LEDGER.v*.md"))
    if not script or not ledgers:
        print(f"[skip] {prefix}: script={bool(script)} ledgers={len(ledgers)}")
        return True

    led = "\n".join(p.read_text(encoding="utf-8") for p in ledgers)
    defined = set(ROW_DEF.findall(led))
    unread = set(UNREAD_ROW.findall(led))
    superseded = {g for m in SUPERSEDED.finditer(led) for g in m.groups() if g}

    lines = script.read_text(encoding="utf-8").split("\n")
    # Front matter -- everything before the first section heading -- is design prose, not narration.
    body_starts = next((i for i, l in enumerate(lines) if l.startswith("## ")), 0)
    narr, uncited = 0, []
    for i, line in enumerate(lines):
        s = line.strip()
        if i < body_starts or not s or s.startswith(SKIP_PREFIX) or DIRECTION.match(s):
            continue
        narr += 1
        nxt = lines[i + 1].strip() if i + 1 < len(lines) else ""
        if not nxt.startswith("<!--"):
            uncited.append((i + 1, s))

    used = collections.Counter(
        CITE.findall("\n".join(l for l in lines if l.strip().startswith("<!--")))
    )
    missing = sorted(k for k in used if k not in defined)
    hit_unread = sorted(k for k in used if k in unread)
    hit_super = sorted(k for k in used if k in superseded)

    # HARD vs SOFT, the same split check_packaging_claims uses and for the same reason. An id that
    # does not resolve is unambiguous. "No citation" is not: the convention began at EP66, older
    # scripts never adopted it, and across 43 scripts it reports 1,653 lines -- noise that would
    # bury the real findings. Advisory by default, blocking under --strict.
    bad = bool(missing or hit_unread or hit_super) or (strict and bool(uncited))
    tag = "FAIL" if bad else "ok  "
    print(f"[{tag}] {prefix}: {script.name} vs {len(ledgers)} ledger(s) -- "
          f"{narr} narration line(s), {len(used)} distinct id(s) cited, "
          f"{len(defined)} defined, {len(unread)} UNREAD, {len(superseded)} superseded")

    if uncited:
        label = "NO CITATION" if strict else "note: no citation"
        for n, s in uncited[:5]:
            print(f"       {label}  {script.name}:{n}  {s[:82]}")
        if len(uncited) > 5:
            print(f"       ... and {len(uncited) - 5} more uncited line(s)")
    if missing:
        print(f"       UNDEFINED ID cited, not a table row in any ledger: {', '.join(missing)}")
    if hit_unread:
        print(f"       UNREAD ROW CITED (quarantine): {', '.join(hit_unread)}")
    if hit_super:
        print(f"       SUPERSEDED ROW CITED: {', '.join(hit_super)}")

    if verbose:
        never = sorted(k for k in defined if k not in used and not k.startswith("⛔"))
        print(f"       [info] {len(never)} ledger row(s) never cited: {', '.join(never) or '-'}")

    return not bad


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--strict", action="store_true", help="make uncited narration lines blocking too")
    a = ap.parse_args()

    if a.all:
        prefixes = sorted({p.name.split("_script.en.")[0] for p in PLANNING.glob("*_script.en.v*.md")})
    elif a.slug:
        prefixes = sorted({p.name.split("_script.en.")[0] for p in PLANNING.glob(f"*{a.slug}_script.en.v*.md")})
        if not prefixes:
            print(f"no script found for slug {a.slug!r} in {PLANNING}")
            return 1
    else:
        ap.error("give --slug or --all")

    ok = all([check(p, a.verbose) for p in prefixes])
    print(f"\n{len(prefixes)} script(s) checked -- {'all citations resolve' if ok else 'PROBLEMS ABOVE'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
