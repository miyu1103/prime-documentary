#!/usr/bin/env python3
"""Check a Short design against the script it claims to come from.

Invariant 1 says no unsupported factual statement enters an approved script, and a Short is a
script. The design file already carries `source_lines` for every line - this makes that field load
bearing by requiring each one to appear verbatim in the episode script. A design that passes cannot
contain a sentence somebody invented, because every sentence in it points at one that was written
and reviewed upstream.

What it checks:
  * every source_line appears verbatim in the referenced script
  * line ids are unique and sequential (L1..Ln)
  * each Short has 8 lines - the spine the render is built for
  * every kinetic beat names a line that exists, and its anchor appears in that line's text
  * angles do not repeat between Shorts of the same episode

Usage:
  py -3.11 scripts/check_short_design.py episodes/_planning/short_designs/PD-2026-066-openfields.design.v001.json
  py -3.11 scripts/check_short_design.py --all
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGNS = ROOT / "episodes" / "_planning" / "short_designs"
SPINE = 8
# The narration builder looks delivery up in a fixed table and dies on anything else. "flat" felt
# like a reasonable word and took all twelve Shorts down with a KeyError.
DELIVERIES = {"intense", "building", "calm"}


def check(path: Path) -> list[str]:
    problems: list[str] = []
    d = json.loads(path.read_text(encoding="utf-8"))
    name = path.name

    script_rel = d.get("script")
    script = ""
    if not script_rel:
        problems.append(f"{name}: no `script` field - nothing to check the lines against")
    else:
        sp = ROOT / script_rel
        if not sp.is_file():
            problems.append(f"{name}: script not found: {script_rel}")
        else:
            script = sp.read_text(encoding="utf-8")

    angles: dict[str, str] = {}
    for s in d.get("shorts", []):
        sid = s.get("short_id", "?")

        lines = s.get("lines", [])
        if len(lines) != SPINE:
            problems.append(f"{sid}: {len(lines)} lines, expected {SPINE}")
        want = [f"L{i + 1}" for i in range(len(lines))]
        got = [ln.get("id") for ln in lines]
        if got != want:
            problems.append(f"{sid}: line ids are {got}, expected {want}")

        for ln in lines:
            dlv = ln.get("delivery")
            if dlv not in DELIVERIES:
                problems.append(
                    f"{sid} {ln.get('id')}: delivery {dlv!r} is not one of {sorted(DELIVERIES)} - "
                    f"the narration builder has no settings for it")
            srcs = ln.get("source_lines") or []
            if not srcs:
                problems.append(f"{sid} {ln.get('id')}: no source_lines - unsourced sentence")
            if script:
                for src in srcs:
                    if src not in script:
                        problems.append(
                            f"{sid} {ln.get('id')}: source line is not in the script verbatim: "
                            f"{src[:70]!r}")

        by_id = {ln.get("id"): ln.get("text", "") for ln in lines}
        for kb in s.get("kinetic_beats", []):
            lid = kb.get("line")
            if lid not in by_id:
                problems.append(f"{sid}: kinetic beat points at {lid}, which has no line")
                continue
            anchor = (kb.get("anchor") or "").lower()
            if anchor and anchor not in by_id[lid].lower():
                problems.append(
                    f"{sid} {lid}: kinetic anchor {anchor!r} does not appear in that line - "
                    f"the overlay would be cut on a word nobody says")

        angle = (s.get("angle") or "").strip()
        if not angle:
            problems.append(f"{sid}: no angle")
        elif angle in angles:
            problems.append(f"{sid}: angle repeats {angles[angle]}")
        else:
            angles[angle] = sid

    return problems


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*")
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args()

    paths = sorted(DESIGNS.glob("*.json")) if a.all else [Path(f) for f in a.files]
    if not paths:
        ap.error("give a design file, or --all")

    total, checked = 0, 0
    for p in paths:
        probs = check(p)
        checked += 1
        if probs:
            print(f"\n{p.name}")
            for x in probs[:14]:
                print(f"  {x}")
            if len(probs) > 14:
                print(f"  ... and {len(probs) - 14} more")
            total += len(probs)
    print(f"\n{checked} design(s) checked, {total} problem(s)")
    return 1 if total else 0


if __name__ == "__main__":
    raise SystemExit(main())
