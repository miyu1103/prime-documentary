#!/usr/bin/env python3
"""Turn FOOTAGE plates the archive cannot actually serve into GENERATE plates.

Why: after indexing all four archive drives (31,480 clips, up from 15,681), 165 documentary
lookups for Shorts 182-192 still land like this:

    bound at >= 0.30 :  82     the picture is of the thing that was asked for
    bound at <  0.30 :  67     the band where every eye-QC miss was found
    refused outright :  16     nothing on the shelf clears the floor

Looking at frames rather than filenames settled it: at >= 0.30 the shelf genuinely delivers, and
below it the shelf is returning its least-bad guess - "gloved hands holding a nozzle" came back as
a farrier filing a horse's hoof, twice, from two different clips of the same series. Re-drawing
does not help when the composition simply is not in the library.

So the weak plates move to the pipeline's primary image route (Codex, project rule 19) and the
strong ones stay as real footage. Owner approved the extra generation load on 2026-08-04.

The prompt is built the same way the design's existing GENERATE prompts were: the plate's own
subject and footage_query supply the content, one practical light is named because SD-class models
return flat daylight otherwise (vocabulary rule R5), the subject is pinned to y560-1180 so it
clears the telop and caption bands (R2), and the shared style suffix carries era and grade.

Usage:
  py -3.11 scripts/convert_weak_footage_to_generate.py --shorts 182-192 --report
  py -3.11 scripts/convert_weak_footage_to_generate.py --shorts 182-192 --apply
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGNS = ROOT / "episodes" / "_planning" / "short_designs"
VOCAB = json.loads((ROOT / "episodes" / "_planning" /
                    "SHORTS_MOTIF_VOCABULARY.v001.json").read_text(encoding="utf-8"))
REPORT = ROOT / "runs" / "footage_semantic" / "bind_report.json"
INDEX_PAIRS = ROOT / "runs" / "footage_semantic" / "rejected_pairs.txt"

KEEP_FLOOR = 0.30

# One practical source, named, per setting. R5 exists because "empty interrogation room" came back
# as a bright minimalist interior with the lamp off; naming the source is what fixes it.
# Order matters: the first pattern that matches wins, so the specific settings come before the
# domestic catch-all. "bare metal table under a lamp" was picking up a kitchen ceiling light off
# the word "table" before this was ordered.
LIGHTS = [
    (r"\b(microscope|laborator|test tube|swab|specimen|bench)\b",
     "one laboratory bench task light which is switched on"),
    (r"\b(cell|prison|jail|holding)\b", "one caged ceiling bulb which is switched on"),
    (r"\b(corridor|hallway|stair|lobby|courthouse|chamber)\b",
     "one overhead fluorescent tube which is switched on"),
    (r"\b(desk|office|paper|file|folder|document|drawer|cabinet|typewriter|stamp|ledger|"
     r"tray|counter|shelves)\b", "one desk lamp which is switched on"),
    (r"\b(car|vehicle|driver|windscreen|windshield|glovebox|dashboard|passenger seat)\b",
     "the car's own interior light which is switched on"),
    (r"\b(street|road|highway|kerb|curb|alley)\b",
     "one sodium streetlight which is switched on"),
    (r"\b(porch|yard|driveway|garden|lawn|field|house exterior|roof|outdoors)\b",
     "hard low afternoon sunlight which is the only light in frame"),
    (r"\b(kitchen|living room|bedroom|home|domestic|table)\b",
     "one kitchen ceiling light which is switched on"),
]
DEFAULT_LIGHT = "one bare overhead bulb which is switched on"

# When the picture itself contains a light, that light IS the source. Naming a different one
# fights the description: "police lights flashing on a street" does not want a streetlight.
NAMED_IN_QUERY = [
    (r"\bpolice lights?|beacon|flashing lights?\b",
     "the police beacon itself which is switched on"),
    (r"\bheadlights?\b", "the headlights themselves which are switched on"),
    (r"\bdesk lamp|table lamp\b", "that desk lamp itself which is switched on"),
    (r"\bwindow\b.*\b(light|morning|sun)|\b(morning|sun)\w*\b.*\bwindow\b",
     "daylight through that window, the only light in frame"),
    (r"\bcandle\b", "that candle flame, the only light in frame"),
    (r"\btelevision|screen glow|monitor\b", "the screen's own glow, the only light in frame"),
]


def light_for(text: str) -> str:
    low = text.lower()
    for pat, lit in NAMED_IN_QUERY:
        if re.search(pat, low):
            return lit
    for pat, lit in LIGHTS:
        if re.search(pat, low):
            return lit
    return DEFAULT_LIGHT


def build_prompt(subject: str, query: str, era: str) -> str:
    """Build from the footage_query, not the subject.

    `subject` is the design's human-facing caption for the beat - "the stamp nobody had to press",
    "the dissent, tied shut". It is good writing and useless to an image model, which will try to
    render the abstraction. `footage_query` is the literal description of the same picture, written
    to be matched against real frames, and that is what the prompt needs.
    """
    query = (query or "").strip().rstrip(".")
    body = query or (subject or "").strip().rstrip(".")
    lit = light_for(f"{body} {subject or ''}")
    return (f"{body}, no face or likeness visible, lit ONLY by {lit}, "
            f"the subject held in the middle third of the tall frame between y560 and y1180 with "
            f"quiet empty darkness above it and below it"
            + VOCAB["style_suffix"].replace("{ERA}", era))



def parse_range(spec: str) -> set[int]:
    out: set[int] = set()
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-")
            out.update(range(int(a), int(b) + 1))
        elif part:
            out.add(int(part))
    return out


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--shorts", required=True)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--floor", type=float, default=KEEP_FLOOR)
    a = ap.parse_args()
    if not a.apply and not a.report:
        ap.error("pass --apply or --report")

    rep = json.loads(REPORT.read_text(encoding="utf-8"))
    # A plate is served by the archive only if it bound AND cleared the floor. Everything else -
    # weak binding or outright refusal - becomes an image.
    served = {(x["short"], x["n"]) for x in rep["bound"] if x["score"] >= a.floor}

    # ...and only if a human looking at the frame agreed. 263 bound frames were reviewed on
    # 2026-08-04 and 69 were wrong - green-screen keying plates, a film countdown leader, a frame
    # reading "428.NPC.1605", craft props on cutting mats. Re-drawing those 69 produced a WORSE
    # set: more green screens, more abstract 3D. The shelf does not hold those pictures, so the
    # eye verdict is final and the plate becomes an image rather than being re-drawn again.
    pairs = INDEX_PAIRS
    if pairs.exists():
        n_eye = 0
        for ln in pairs.read_text(encoding="utf-8").splitlines():
            ln = ln.strip()
            if not ln or ln.startswith("#"):
                continue
            p = ln.split(None, 2)
            if len(p) == 3 and served.discard((p[0], int(p[1]))) is None:
                n_eye += 1
        print(f"{n_eye} plate(s) removed from 'served' by eye QC")
    want = parse_range(a.shorts)

    converted, kept = [], 0
    for f in sorted(DESIGNS.glob("*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        touched = False
        for s in d["shorts"]:
            n = int(re.sub(r"\D", "", s["short_id"]))
            if n not in want:
                continue
            era = s.get("era") or "present day"
            for p in s["plates"]:
                if p.get("source") != "FOOTAGE":
                    continue
                if (s["short_id"], p["n"]) in served:
                    kept += 1
                    continue
                p["prompt"] = build_prompt(p.get("subject"), p.get("footage_query"), era)
                p["source"] = "GENERATE"
                p["converted_from"] = "FOOTAGE"
                p["conversion_reason"] = ("archive best match below %.2f after indexing all four "
                                          "drives" % a.floor)
                for k in ("bound_file", "bound_match", "bound_score"):
                    p.pop(k, None)
                p["footage_query"] = None
                converted.append((s["short_id"], p["n"], p["subject"], p["prompt"]))
                touched = True
        if touched and a.apply:
            f.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"kept as real footage : {kept}")
    print(f"converted to GENERATE: {len(converted)}" + ("" if a.apply else "   (REPORT ONLY)"))
    for sid, n, subj, pr in converted:
        print(f"\n  {sid} p{n:02d}  {subj}")
        print(f"      {pr[:150]}...")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
