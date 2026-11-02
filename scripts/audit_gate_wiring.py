#!/usr/bin/env python3
"""Which countermeasures are actually on a path someone walks?

Measured 2026-08-10: this repository holds 79 check_*/verify_* scripts. Eight are invoked by the
pipeline. check_final_acceptance imports none of them -- it reimplements 28 checks as its own
functions, so several of those scripts are a second copy of a live check, quietly rotting.

That is the answer to "the countermeasures exist but nothing uses them". A countermeasure written
as a standalone script only runs if somebody remembers to run it, and nobody remembers 79 things.
Every countermeasure that actually fired today was somewhere it could not be avoided: inside the
scheduling command, inside the film builder, inside the probe, inside a PreToolUse hook.

This turns the invisible pile into a work list. It does not fix anything by itself; it says which
of the four states each script is in, so the ones worth wiring can be wired and the ones that were
always one-offs can go to the archive.

    py -3.11 scripts/audit_gate_wiring.py
    py -3.11 scripts/audit_gate_wiring.py --state orphan
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:  # noqa: BLE001
    pass

ROOT = Path(__file__).resolve().parents[1]

# The files that make up a path someone actually walks. A script named in one of these runs
# whether or not anybody remembered it.
PIPELINE = [
    "scripts/_finish_episode.sh",
    "scripts/_finish_ep62_65.sh",
    "scripts/pd_render_guarded.sh",
    "scripts/probe_before_render.sh",
    "scripts/upload_schedule_case_v001.py",
    "scripts/check_final_acceptance.py",
    "scripts/preflight_render_gate.py",
    "scripts/daily_shorts_push.sh",
    "scripts/pd_run.sh",
    # Added 2026-08-11. Both are paths someone walks and both refuse to proceed: the first is
    # named in CLAUDE.md s4.5 item 3 as THE pre-spend input check, the second is the film
    # builder, which raises SystemExit on a blocklisted cut and on an undeclared target_cut_sec.
    # Leaving them out meant a gate called only from one of them was reported as an orphan --
    # check_design_doc.spec_document_drift was, on the day it was wired.
    "scripts/check_episode_inputs.py",
    "scripts/build_case_film_generic.py",
    ".claude/settings.json",
    ".claude/hooks/pd_safety_gate.py",
]

# A one-off written for a single episode is not an orphan, it is finished work. Recognise it by
# name rather than leaving it in the queue forever.
ONE_OFF = re.compile(
    r"_(ep\d+|atwater|caniglia|centralpark|cleveland|tyler|rolin|hinders|williams|florence|"
    r"kidsforcash|young|willingham|morton|norfolk|flowers|burge|postoffice|fieldtest|lejeune|"
    r"robosigning|surfside|weimer|greene|correa|memphis|marmet|riley|mapp|gideon|miranda|"
    r"strieff|glover|tekoh|thompson|titan|varsityblues|gardner|dbcooper|milken)_?", re.I)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--state", choices=["wired", "reimplemented", "one_off", "orphan"])
    ap.add_argument("--json", dest="json_out")
    a = ap.parse_args()

    pipeline_text = ""
    for rel in PIPELINE:
        p = ROOT / rel
        if p.is_file():
            pipeline_text += p.read_text(encoding="utf-8", errors="replace")

    # the check names check_final_acceptance implements itself, e.g. "def check_asset_reuse("
    acc = (ROOT / "scripts" / "check_final_acceptance.py")
    internal = set()
    if acc.is_file():
        internal = {m.group(1) for m in
                    re.finditer(r"^def (?:check|verify)_(\w+)\(", acc.read_text(encoding="utf-8"),
                                re.M)}

    rows = []
    for p in sorted(list((ROOT / "scripts").glob("check_*.py"))
                    + list((ROOT / "scripts").glob("verify_*.py"))):
        stem = p.stem
        topic = re.sub(r"^(check|verify)_", "", stem)
        # Match the STEM too. check_final_acceptance invokes eighteen of these through
        # _ext_gate("check_padding", ...) with no extension, and searching only for
        # "check_padding.py" reported eighteen live gates as orphans.
        if p.name in pipeline_text or stem in pipeline_text:
            state, note = "wired", "named in the pipeline"
        elif topic in internal:
            state, note = ("reimplemented",
                           f"check_final_acceptance implements '{topic}' itself and does not "
                           f"import this file -- two copies, one of them dead")
        elif ONE_OFF.search(stem):
            state, note = "one_off", "written for one episode; finished work, not a live gate"
        else:
            state, note = "orphan", "general-purpose, on no path -- runs only if remembered"
        rows.append({"script": p.name, "state": state, "note": note,
                     "lines": len(p.read_text(encoding="utf-8", errors="replace").splitlines())})

    order = ["wired", "reimplemented", "orphan", "one_off"]
    counts = {s: sum(1 for r in rows if r["state"] == s) for s in order}
    print(f"{len(rows)} countermeasure script(s)\n")
    for s in order:
        print(f"  {s:15s} {counts[s]:3d}")
    print()

    show = [r for r in rows if not a.state or r["state"] == a.state]
    for s in order:
        group = [r for r in show if r["state"] == s]
        if not group:
            continue
        print(f"--- {s} ({len(group)})")
        if s == "reimplemented":
            print("    a live check exists inside check_final_acceptance; these files are the "
                  "second copy")
        if s == "orphan":
            print("    THE WORK LIST: wire each into a stage, or archive it. A countermeasure "
                  "nobody runs is not a countermeasure.")
        for r in group:
            print(f"    {r['script']:44s} {r['lines']:4d} lines")
        print()

    if a.json_out:
        Path(a.json_out).write_text(json.dumps(
            {"schema_version": "gate_wiring.v001", "counts": counts, "scripts": rows},
            ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"report -> {a.json_out}")
    # Exit 1 while general-purpose orphans exist, so this can later become a real gate.
    return 1 if counts["orphan"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
