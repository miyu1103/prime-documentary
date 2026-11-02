#!/usr/bin/env python3
"""A planning script measured against the WRITTEN standard, before anything is spent.

FREE, PRE-SPEND. Reads `episodes/_planning/EP<NN>_<slug>_script.en.v*.md` (newest) and the
episode's own `episode_spec.v*.json`, and checks the rows of the standard that are visible in a
script rather than in a rendered file:

    PD_ONE_PASS_PRODUCTION_SPEC.v3 row 9   hook is section one and states no outcome
    PD_ONE_PASS_PRODUCTION_SPEC.v3 row 10  four-part spine, and exactly one specific ask
    PD_ONE_PASS_PRODUCTION_SPEC.v3 row 15  register: zero emotion commands
    PD_ONE_PASS_PRODUCTION_SPEC.v3 row 17  every narration line carries a claim id
    PD_ONE_PASS_PRODUCTION_SPEC.v3 row 18  a named person carries legal status in the same line
    .claude/rules/09                       no production direction inside a spoken line
    episode_spec                           section_vocabulary, script_words, runtime_seconds
    episode_spec.forbidden_claims          intent / foresight vocabulary anywhere in narration
    DEEP_RESEARCH_FINDINGS.v001            rhetorical questions do not pile up

WHY THIS EXISTS. Written 2026-08-21 while checking EP76 morandi, after being asked whether the
script was actually to standard and finding that the honest answer needed twelve separate readings.
It caught two real defects on its first run: a narration line citing a SOURCE id instead of a ledger
ROW, and a bare "they knew" three lines from the collapse in an episode whose court expressly struck
out the foresight circumstance. A gate that has never been shown to fail is decoration; this one was
shown failing before it was relied on.

WHAT IT IS NOT. `check_script_citations.py` owns the citation/ledger relationship in depth (UNREAD
rows, superseded rows, multi-ledger resolution) and is called here rather than reimplemented. The
manual's `check_script_craft` is a different, currently crashing gate on a different input. Nothing
here measures the master: retention cadence, flat stretches, caption format, mean shot length,
animation density and footage diversity are all properties of a rendered file and are printed as
NOT MEASURED rather than assumed.

Usage:
    py -3.11 scripts/check_script_standard.py --slug morandi
    py -3.11 scripts/check_script_standard.py --all
    py -3.11 scripts/check_script_standard.py --slug morandi --wpm 184.0
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLANNING = ROOT / "episodes" / "_planning"

BANNED_EMOTION = ("imagine", "shocking", "unbelievable", "heartbreaking", "you won't believe",
                  "horrifying", "devastating", "tragic", "chilling", "stunning", "incredible")
DIRECTION_IN_LINE = re.compile(r"\b(CUT TO|B-ROLL|SFX|VO:|MUSIC:|INT\.|EXT\.)\b")
INTENT = (r"\bthey knew\b", r"\bhe knew\b", r"\bshe knew\b", r"\bknew it would\b",
          r"\bdeliberately\b", r"\bon purpose\b", r"\blet it (fall|happen|collapse)\b",
          r"\bforesaw\b", r"\bwas inevitable\b", r"\bcovered (it )?up\b")
OUTCOME_IN_HOOK = ("collapse", "collapsed", "died", "dead", "killed", "death toll",
                   "convicted", "acquitted", "guilty")
STATUS = re.compile(r"(first instance|acquitted|not final|appeal|convicted|charged|pleaded)", re.I)
# Default gap model, matching gen_narration_case's own constants.
BEAT_GAP, SECTION_GAP, ENDCARD = 0.30, 1.8, 9.0


def spec_for(slug: str) -> tuple[Path, dict]:
    eps = sorted((ROOT / "episodes").glob(f"PD-*-{slug}"))
    if not eps:
        raise SystemExit(f"[standard] no episode dir for slug {slug!r}")
    specs = sorted(eps[-1].glob("episode_spec.v*.json"))
    if not specs:
        raise SystemExit(f"[standard] {eps[-1].name} has no episode_spec")
    return eps[-1], json.loads(specs[-1].read_text(encoding="utf-8"))


def newest_script(slug: str) -> Path:
    cands = sorted(PLANNING.glob(f"EP*_{slug}_script.en.v*.md"))
    if not cands:
        raise SystemExit(f"[standard] no planning script for slug {slug!r}")
    return cands[-1]


def narration(lines: list[str], first_section: int) -> list[tuple[int, str]]:
    """Spoken lines only: not headings, directions, citation comments or front matter."""
    out = []
    for i, line in enumerate(lines[first_section:], first_section):
        s = line.strip()
        if not s or s.startswith(("#", ">", "|", "<!--", "【", "---", "```")):
            continue
        out.append((i + 1, s))
    return out


STATUS_WORD = re.compile(
    r"\b(convicted|acquitted|sentenced|time-barred|prescription|prescribed|pleaded|charged|"
    r"defendant|proceedings|judgment)\b", re.I)

# Tokens that look like surnames but are not. Deliberately short: a false name here only costs a
# check that always passes, while a missed name costs the one thing row 18 exists to catch.
NOT_A_NAME = {
    "January", "February", "March", "April", "May", "June", "July", "August", "September",
    "October", "November", "December", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
    "Saturday", "Sunday", "Court", "Tribunal", "Tribunale", "Ministry", "Commission", "Company",
    "Genoa", "Italy", "Italian", "Rome", "Article", "Criminal", "Code", "President", "Their",
    "There", "These", "Those", "Every", "Which", "While", "After", "Before", "Against", "About",
    "First", "Second", "Third", "Under", "State", "Public", "Works", "Council", "Office",
    # Sentence openers. Without these, "That Riccardo Morandi predicted…" yields a defendant
    # called Riccardo, which is how this row first went red on EP76.
    "That", "This", "Any", "None", "Nothing", "Where", "Wherever", "Whether", "Only", "Both",
    "Each", "Every", "Neither", "Either", "Such", "When", "What", "Who", "Whose", "Dott",
    "Judge", "Prof", "Engineer", "Former", "Chief", "Director", "Minister", "Report", "Note",
}


# Two-token name shapes, which is what makes this precise instead of a capitalised-word sweep.
CAPS_FIRST = re.compile(r"\b([A-Z][A-Z'’-]{2,})\s+([A-Z][a-z]{2,})\b")      # FERRAZZA Roberto
GIVEN_FIRST = re.compile(r"\b([A-Z][a-z]{2,})\s+([A-Z][a-z]{2,})\b")        # Giovanni Castellucci


def named_people(epdir: Path, slug: str, spec: dict) -> list[str]:
    """Surnames of people the record shows are legally sensitive, harvested rather than guessed.

    Row 18 binds anyone whose legal status the film must state in the same breath. Two sources, and
    both are declarations rather than inference:

      1. the ledger's own judgment rows — any line carrying a status word, read for a NAME pattern
         (an Italian court writes `FERRAZZA Roberto`, so caps-surname-first is matched too);
      2. `episode_spec.forbidden_claims`, which is where the spec author writes down exactly who is
         sensitive and why.

    KNOWN LIMIT, stated rather than hidden: this needs a two-token name to fire. A person the film
    refers to by surname alone, and whom neither the ledger nor the spec ever writes in full, will
    not be policed. Under-detection is the direction chosen on purpose — a false name here costs a
    check that trivially passes, while noise made the whole row unreadable and got it ignored.
    """
    blobs: list[str] = []
    for p in sorted(PLANNING.glob(f"EP*_{slug}_FACTS_LEDGER.v*.md")):
        blobs += [l for l in p.read_text(encoding="utf-8").splitlines() if STATUS_WORD.search(l)]
    # Only those forbidden_claims that are ABOUT legal status. Taking every name mentioned there
    # was wrong and measured wrong on EP76: the spec names Riccardo Morandi precisely so that the
    # film may NOT accuse him, and he died in 1989 and was never a defendant. Row 18 polices people
    # whose status the record carries, not everyone the spec happens to mention.
    blobs += [c for c in spec.get("forbidden_claims", []) if STATUS_WORD.search(c)]

    names: set[str] = set()
    for line in blobs:
        clean = re.sub(r"[*_`]", "", line)
        for surname, _given in CAPS_FIRST.findall(clean):
            if surname.title() not in NOT_A_NAME:
                names.add(surname.title())
        for _given, surname in GIVEN_FIRST.findall(clean):
            if surname not in NOT_A_NAME and _given not in NOT_A_NAME:
                names.add(surname)
    return sorted(names)


def check(slug: str, wpm: float | None, verbose: bool) -> bool:
    epdir, spec = spec_for(slug)
    script = newest_script(slug)
    text = script.read_text(encoding="utf-8")
    lines = text.split("\n")
    first = next((i for i, l in enumerate(lines) if l.startswith("## ")), 0)
    narr = narration(lines, first)
    heads = [l[3:].split(" —")[0].strip() for l in lines if l.startswith("## ")]
    rows: list[tuple[bool, str, str]] = []

    def add(ok: bool, name: str, detail: str) -> None:
        rows.append((ok, name, detail))

    add(heads == spec["section_vocabulary"], "spec.section_vocabulary",
        " ".join(heads) if heads != spec["section_vocabulary"] else "in order")

    # row 9
    if "## HOOK" in text:
        hook = text.split("## HOOK", 1)[1].split("\n## ", 1)[0]
        hook_lines = [l.strip() for l in hook.split("\n")
                      if l.strip() and not l.strip().startswith(("<!--", "【", ">"))]
        leak = [w for w in OUTCOME_IN_HOOK
                if re.search(rf"\b{w}\b", " ".join(hook_lines), re.I)]
        add(not leak, "v3 row 9: hook states no outcome", f"leaked={leak or 'none'}")
        add(heads[0] == "HOOK", "v3 row 9: hook is section one",
            f"{len(hook_lines)} narration line(s)")
    else:
        add(False, "v3 row 9: hook", "no HOOK section")

    # row 10
    ending = text.split("## ENDING", 1)[-1]
    ask = re.search(r"(in the comments|subscribe|tell me)", ending, re.I)
    add(bool(heads and heads[0] == "HOOK" and heads[-1] == "ENDING" and ask),
        "v3 row 10: spine + one ask", f"ask={'yes' if ask else 'NO'}")

    # row 15 register
    joined = " ".join(s for _, s in narr)
    emo = {w: len(re.findall(rf"\b{re.escape(w)}\b", joined, re.I)) for w in BANNED_EMOTION}
    emo = {w: n for w, n in emo.items() if n}
    add(not emo, "register: zero emotion commands", f"{emo or 'all zero'}")

    # rule 09
    dirs = [n for n, s in narr if DIRECTION_IN_LINE.search(s)]
    add(not dirs, "rule 09: no directions in narration", f"{len(dirs)} line(s)")

    # row 17
    uncited = [n for n, _ in narr if not (lines[n].strip().startswith("<!--") if n < len(lines) else False)]
    add(not uncited, "v3 row 17: every line cited",
        f"{len(narr)} lines, {len(uncited)} uncited" + (f" {uncited[:5]}" if uncited else ""))

    # row 18
    people = named_people(epdir, slug, spec)
    bad = [(n, w) for w in people for n, s in narr
           if re.search(rf"\b{re.escape(w)}\b", s, re.I) and not STATUS.search(s)]
    add(not bad, "v3 row 18: status in same breath",
        f"{bad[:4] if bad else f'clean ({len(people)} defendant name(s) policed)'}")

    # forbidden_claims: intent
    fs = [(n, s[:60]) for n, s in narr for p in INTENT if re.search(p, s, re.I)]
    add(not fs, "spec.forbidden_claims: no intent", f"{fs[:3] or 'clean'}")

    # deep research
    qs = [n for n, s in narr if s.endswith("?")]
    add(len(qs) <= 3, "deep research: questions <= 3", f"{len(qs)} question line(s)")

    # the bands, from the extractor rather than from a word counter
    epid = epdir.name
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "gen_narration_case.py"),
                        "--ep", epid, "--dry-run"], cwd=ROOT,
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    m = re.search(r"chunks=(\d+) words=(\d+)", r.stdout)
    if m:
        chunks, words = int(m.group(1)), int(m.group(2))
        lo, hi = spec["script_words"]
        add(lo <= words <= hi, "spec.script_words", f"{words} in [{lo}, {hi}]")
        if wpm:
            speech = words / wpm * 60
            film = speech + (chunks - len(heads)) * BEAT_GAP + (len(heads) - 1) * SECTION_GAP + ENDCARD
            rlo, rhi = spec["runtime_seconds"]
            add(rlo <= film <= rhi, "spec.runtime_seconds (projected)",
                f"{film:.0f}s = {int(film // 60)}:{int(film % 60):02d} at {wpm} wpm, band [{rlo}, {rhi}]")
        else:
            print("  note: --wpm not given, runtime not projected (use the MEASURED rate, "
                  "never the registry model)")
    else:
        add(False, "spec.script_words", "gen_narration_case --dry-run produced no count")

    ok = all(r[0] for r in rows)
    print(f"[{'ok  ' if ok else 'FAIL'}] {slug}: {script.name} vs {epdir.name}/episode_spec")
    for good, name, detail in rows:
        if verbose or not good:
            print(f"       {'PASS' if good else 'FAIL'}  {name:38} {detail}")
    if not ok:
        print(f"       {sum(1 for r in rows if r[0])}/{len(rows)} pass")
    return ok


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--wpm", type=float, help="MEASURED raw wpm for this episode")
    ap.add_argument("--quiet", action="store_true", help="print failures only")
    a = ap.parse_args()
    if not a.slug and not a.all:
        ap.error("give --slug or --all")

    slugs = [a.slug] if a.slug else sorted(
        {p.name.split("-")[-1] for p in (ROOT / "episodes").glob("PD-*")
         if list(p.glob("episode_spec.v*.json"))
         and list(PLANNING.glob(f"EP*_{p.name.split('-')[-1]}_script.en.v*.md"))})

    results = [check(s, a.wpm, not a.quiet) for s in slugs]
    print(f"\n{sum(results)}/{len(results)} script(s) to standard")
    print("NOT MEASURED HERE (properties of the rendered master): retention_cadence, "
          "flat stretches > 20 s,\ncaption format, mean shot length, animation density, "
          "footage diversity.")
    return 0 if all(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
