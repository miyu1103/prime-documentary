#!/usr/bin/env python3
r"""Write EP74 itaewon's sound plan into its [VO:] script.

WHY THIS EXISTS
---------------
`gen_vo_script.py` emits ONLY `[VO:]` lines. It has never written a sound cue, so every episode
arrives at [4d] silent and fails the density gate. EP70 lost three pipeline runs to it; EP71 was
fixed before its i2v rather than after a render. EP74 is fixed here, before the build.

CALIBRATION, measured not guessed. Shipped EP69 hyatt: 60 cues / 28.3 min = 2.11/min PASS.
EP70 brought to 81 / 39.9 = 2.03 PASS. EP71 to 62 / 29.6 = 2.09 PASS. EP74's master is
1,886.8 s = 31.4 min, so the same density needs about **66 cues**.

WHAT THIS FILM SOUNDS LIKE
--------------------------
Itaewon, 29 October 2022. A sloping alley 3.2 m wide at its foot, eleven emergency calls across
three hours and thirty-seven minutes, and then four years of documents, hearings and two appeals
that stopped. The design bible says the event is carried by **sound, by the width of the walls
and by the slope** -- so the sound has to do real work here, more than in most PD films.

TWO BARS THIS FILM PUTS ON ITS OWN SOUND, and both are absolute:

  * **Nothing dramatises the crush.** No crowd roar, no scream, no siren wail over the event, no
    impact on the beat where people died. Quarantine rule 2 bars depicting it and that includes
    depicting it in the mix. The loudest thing in ACT_3 is a number card.
  * **NO GAVEL.** `sfx_gavel_knock.mp3` is available and is FORBIDDEN in this episode: Korean
    courts do not use one, and the image order bars it for the same reason. Court beats take
    `stamp`, `page turn` or `latch` instead. This is the single easiest way to put a register
    error into the mix of a Korean film, so it is written down rather than remembered.

The register is: a phone in a hand, a shutter coming down, feet on a wet slope, a radio, paper,
a date stamp, a door in an empty corridor, and a whistle in the present day.

CUE FORM: `(SFX: <kind> "<anchor>")` on the line after a beat. The anchor must be a word that
beat actually speaks; the kind selects the sample through build_case_film_audio.py's own table.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "episodes" / "PD-2026-074-itaewon" / "03_script" / "script.en.v001.md"

# (trigger word in the beat, SFX kind, anchor word). First match on a beat wins.
RULES: list[tuple[str, str, str]] = [
    # the call -- the film's spine
    ("called the police", "click", "police"),
    ("phone", "click", "phone"),
    ("call", "click", "call"),
    ("calls", "click", "calls"),
    ("caller", "click", "caller"),
    ("reports", "click", "reports"),
    ("switchboard", "click", "switchboard"),
    ("radio", "click", "radio"),
    ("whistle", "click", "whistle"),
    ("whistles", "click", "whistles"),
    ("bells", "click", "bells"),

    # the street itself
    ("shutter", "latch", "shutter"),
    ("shutters", "latch", "shutters"),
    ("kerb", "footstep", "kerb"),
    ("pavement", "footstep", "pavement"),
    ("walked", "footstep", "walked"),
    ("walking", "footstep", "walking"),
    ("pushed", "footstep", "pushed"),
    ("stairs", "footstep", "stairs"),
    ("station", "footstep", "station"),
    ("escalator", "footstep", "escalator"),
    ("train", "pass-by", "train"),
    ("traffic", "pass-by", "traffic"),
    ("scooter", "pass-by", "scooter"),
    ("vehicles", "pass-by", "vehicles"),
    ("road", "pass-by", "road"),
    ("street", "pass-by", "street"),
    ("rain", "rustle", "rain"),
    ("wet", "rustle", "wet"),
    ("hosed", "rustle", "hosed"),

    # the paperwork -- what the film is actually about
    ("statute", "page turn", "statute"),
    ("act", "page turn", "act"),
    ("decree", "page turn", "decree"),
    ("law", "page turn", "law"),
    ("regulations", "page turn", "regulations"),
    ("amendment", "page turn", "amendment"),
    ("plan", "stamp", "plan"),
    ("report", "stamp", "report"),
    ("audit", "stamp", "audit"),
    ("record", "stamp", "record"),
    ("records", "stamp", "records"),
    ("filed", "stamp", "filed"),
    ("appealed", "stamp", "appealed"),
    ("indicted", "stamp", "indicted"),
    ("bill", "rustle", "bill"),
    ("document", "rustle", "document"),
    ("papers", "rustle", "papers"),
    ("notice", "rustle", "notice"),
    ("fines", "stamp", "fines"),

    # the rooms -- NO GAVEL, deliberately
    ("court", "latch", "court"),
    ("courts", "latch", "courts"),
    ("bench", "latch", "bench"),
    ("hearing", "latch", "hearing"),
    ("commission", "latch", "commission"),
    ("committee", "latch", "committee"),
    ("chief", "latch", "chief"),
    ("sentenced", "stamp", "sentenced"),
    ("acquitted", "stamp", "acquitted"),
    ("judgment", "stamp", "judgment"),
    ("suspended", "stamp", "suspended"),
    ("stopped", "latch", "stopped"),

    # time -- the clock IS the plot here
    ("minutes", "clock", "minutes"),
    ("hours", "clock", "hours"),
    ("evening", "clock", "evening"),
    ("night", "clock", "night"),
    ("morning", "clock", "morning"),
    ("years", "clock", "years"),
    ("months", "clock", "months"),
    ("october", "clock", "October"),
    ("saturday", "clock", "Saturday"),

    # the present day
    ("barrier", "latch", "barrier"),
    ("cameras", "shutter", "cameras"),
    ("camera", "shutter", "camera"),
    ("signs", "rustle", "signs"),
    ("sign", "rustle", "sign"),
    ("door", "latch", "door"),
    ("window", "rustle", "window"),
]

MIN_GAP_BEATS = 3
MAX_PER_KIND = 14
TARGET = 66

# Beats that must stay silent. The crush is never dramatised, and the film's largest cards
# carry their own weight -- a sound effect on any of these is a register error.
SILENT_SUBSTRINGS = (
    "hundred and fifty-nine",
    "hundred and fifty-seven",
    "hundred and fifty-eight",
    "crushed to death",
    "fell over and got hurt",
    "terrible accident",
    "died",
    "dead",
    "asphyxiation",
    "crush syndrome",
    "rhabdomyolysis",
    "survived",
    "rescue",
    "thirteen minutes",
    "not concluded",
)


def main() -> int:
    if not SCRIPT.is_file():
        print(f"no [VO:] script at {SCRIPT} -- run gen_vo_script.py --ep PD-2026-074-itaewon --force")
        return 1

    lines = SCRIPT.read_text(encoding="utf-8").split("\n")
    out: list[str] = []
    last_cue = -99
    per_kind: dict[str, int] = {}
    beat = 0
    placed = 0
    silent = 0

    for line in lines:
        out.append(line)
        m = re.match(r"^\[VO:\]\s*(.+)$", line)
        if not m:
            continue
        beat += 1
        text = m.group(1)
        low = text.lower()

        if any(s in low for s in SILENT_SUBSTRINGS):
            silent += 1
            continue
        if beat - last_cue < MIN_GAP_BEATS or placed >= TARGET:
            continue

        for trigger, kind, anchor in RULES:
            if trigger not in low:
                continue
            if per_kind.get(kind, 0) >= MAX_PER_KIND:
                continue
            # the anchor must be a word this beat really speaks
            if not re.search(rf"\b{re.escape(anchor)}\b", text, re.I):
                continue
            out.append(f'(SFX: {kind} "{anchor}")')
            per_kind[kind] = per_kind.get(kind, 0) + 1
            last_cue = beat
            placed += 1
            break

    SCRIPT.write_text("\n".join(out), encoding="utf-8")
    minutes = 1886.8 / 60.0
    print(f"{SCRIPT.name}: {beat} beat(s), {placed} SFX cue(s) placed, "
          f"{silent} beat(s) held silent by the crush bar")
    print(f"density {placed / minutes:.2f}/min against a floor of 2.0 "
          f"({'PASS' if placed / minutes >= 2.0 else 'BELOW FLOOR'})")
    print("by kind: " + ", ".join(f"{k} {v}" for k, v in sorted(per_kind.items())))
    if "gavel" in per_kind:
        print("FAIL: a gavel cue was placed. Korean courts do not use one.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
