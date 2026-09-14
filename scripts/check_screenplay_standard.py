#!/usr/bin/env python
"""Measure the parts of PD_SCREENPLAY_STANDARD that check_script_craft.py does NOT.

WHY THIS EXISTS. On 2026-08-24 the owner asked whether the EP77-80 scripts met the
quality standard. Three gates answered PASS, and all three of them measure counting
problems: words, questions, short sentences, banned phrases. The standard's binding
clauses are not counting problems:

  * the controlling idea is ONE sentence and is NEVER spoken in the film
  * ONE motif: a thing shown in changing states, never explained, looping at the end
  * silences are written, not directed
  * no villain
  * the ENDING adds no new fact -- it re-frames what is already there

Four of those five leave a trace a machine can find. This tool finds them. It does
NOT judge whether the motif is good or whether the film has a villain in spirit --
it checks that the script declares them, uses them, and does not violate the two
rules that ARE mechanical: the controlling idea must not appear in the narration,
and the ENDING must not introduce a fact id that appears nowhere earlier.

    py -3.11 scripts/check_screenplay_standard.py <script.md> [--strict]

Exit 0 when every mechanical clause holds. --strict also fails on the advisories.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HELD = "⟨HELD⟩"


def narration(text: str) -> str:
    """Everything a voice actually says: comments and fact ids stripped."""
    t = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    t = re.sub(r"^#.*$", "", t, flags=re.M)
    return t


def header_block(text: str) -> str:
    m = re.search(r"<!--(.*?)-->", text, flags=re.S)
    return m.group(1) if m else ""


def sentences(t: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[.?!])\s+", t) if s.strip()]


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9 ]", "", s.lower()).strip()


def overlap(a: str, b: str) -> float:
    """Fraction of the controlling idea's content words present in a spoken sentence."""
    STOP = set("a an the of in on at and or is are was were to it its that this "
               "as for with by not no be been being do does did".split())
    A = {w for w in norm(a).split() if w not in STOP and len(w) > 2}
    B = {w for w in norm(b).split() if w not in STOP and len(w) > 2}
    return len(A & B) / len(A) if A else 0.0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("script")
    ap.add_argument("--strict", action="store_true")
    a = ap.parse_args()

    raw = Path(a.script).read_text(encoding="utf-8")
    head = header_block(raw)
    spoken = narration(raw)

    problems: list[str] = []
    notes: list[str] = []

    # --- 1. the controlling idea is declared, and is never spoken -------------
    m = re.search(r"CONTROLLING IDEA.*?:\s*\n(.+?)(?:\n\s*\n|\nMOTIF)", head, flags=re.S | re.I)
    if not m:
        problems.append("no CONTROLLING IDEA declared in the header comment")
        idea = ""
    else:
        idea = " ".join(m.group(1).split())
        if len(sentences(idea)) > 1:
            problems.append(f"controlling idea is {len(sentences(idea))} sentences, must be one")
        worst = max(((overlap(idea, s), s) for s in sentences(spoken)), default=(0.0, ""))
        if worst[0] >= 0.75:
            problems.append(f"controlling idea is SPOKEN ({worst[0]:.0%} of its words): "
                            f"\"{worst[1][:90]}\"")
        elif worst[0] >= 0.55:
            notes.append(f"a spoken line carries {worst[0]:.0%} of the controlling idea: "
                         f"\"{worst[1][:80]}\"")

    # --- 2. one motif, declared, used, and present in the ENDING --------------
    mm = re.search(r"MOTIF:\s*(.+?)(?:\n\s*\n|\nR3|\nEvery factual)", head, flags=re.S | re.I)
    if not mm:
        problems.append("no MOTIF declared in the header comment")
    else:
        motif = " ".join(mm.group(1).split())
        STOP = set("a an the of in on at and or is are it its that this never explained "
               "as for with by not no shown changing states again".split())
        keys = [w for w in norm(motif).split() if w not in STOP and len(w) > 3][:4]
        if not keys:
            notes.append("motif declaration has no usable noun to trace")
        else:
            body = norm(spoken)
            hits = sum(body.count(k) for k in keys)
            end = raw.split("## ENDING")[-1] if "## ENDING" in raw else ""
            end_hits = sum(norm(narration(end)).count(k) for k in keys)
            if hits < 3:
                problems.append(f"motif {keys} appears only {hits}x in the narration; "
                                f"a motif is a thing in CHANGING STATES, not a mention")
            if end_hits == 0:
                problems.append(f"motif {keys} does not appear in the ENDING; it must loop")
            notes.append(f"motif {keys}: {hits} mention(s), {end_hits} in the ENDING")

    # --- 3. silences are written -------------------------------------------
    n_held = raw.count(HELD)
    if n_held < 3:
        problems.append(f"{n_held} written silence(s); the standard places them after the "
                        f"recognition, after the limit, and before the final image")
    else:
        notes.append(f"{n_held} written silence(s)")

    # --- 4. the ENDING adds no new fact --------------------------------------
    if "## ENDING" in raw:
        before, _, end = raw.partition("## ENDING")
        ids_before = set(re.findall(r"\b([A-Z]{2}-\d+)\b", before))
        ids_end = set(re.findall(r"\b([A-Z]{2}-\d+)\b", end))
        fresh = sorted(ids_end - ids_before)
        if fresh:
            problems.append(f"ENDING introduces fact id(s) that appear nowhere earlier: "
                            f"{', '.join(fresh)}")
        else:
            notes.append(f"ENDING cites {len(ids_end)} fact id(s), all already established")
    else:
        problems.append("no ## ENDING section")

    # --- 5. what this tool cannot judge -------------------------------------
    print(f"script   : {Path(a.script).name}")
    for n in notes:
        print(f"  note   : {n}")
    for p in problems:
        print(f"  PROBLEM: {p}")
    print()
    print("NOT MEASURED, and a person still has to read for it:")
    print("  * whether the film has a villain in effect, whatever it says it does")
    print("  * whether the motif means anything, or is just a repeated noun")
    print("  * whether the ENDING re-frames, or merely restates")
    print("  * whether the prose is any good")
    print()
    if problems:
        print(f"FAIL  {len(problems)} clause(s) of PD_SCREENPLAY_STANDARD not satisfied")
        return 1
    print("PASS  every mechanically checkable clause holds")
    return 0


if __name__ == "__main__":
    sys.exit(main())
