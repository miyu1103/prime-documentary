#!/usr/bin/env python3
"""Place SFX annotations on the beats where the narration NAMES the thing that makes the sound.

2026-08-17. build_case_film_audio.py requires at least 20 SFX cues and 2.0 per body-minute, and
takes them from `(SFX: keyword "spoken word")` lines authored into
`episodes/<EPID>/03_script/script.en.v001.md`. EP66 openfields has 49 such lines and passes at
2.08/min. EP67 ramirez, EP68 pinto and EP69 hyatt have none, so each had only the 7 automatic
chapter whooshes -- 0.24/min -- and all three died at the gate before rendering.

The rule here is the owner's standing one: sound follows meaning. A cue is placed ONLY where the
narration says the word out loud, and the quoted trigger puts it on that word in the real
narration timeline. Nothing is placed to make a number. The builder itself already deleted a
"transient bed" of filler ticks for exactly this reason.

Only the 19 keyword groups in ONESHOT_MAP resolve to a file; anything else is dropped as
`no_keyword_match`, so this maps spoken vocabulary onto those groups and nothing else.

    py -3.11 scripts/author_sfx_beats.py --ep PD-2026-067-ramirez --dry-run
    py -3.11 scripts/author_sfx_beats.py --ep PD-2026-067-ramirez
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# spoken word (regex, matched on word boundaries) -> ONESHOT_MAP keyword that fits its sound.
# Ordered: the first match on a beat wins, so the more specific sounds come first.
RULES: list[tuple[str, str]] = [
    (r"gavel|courtroom|the court (?:said|held|ruled)|verdict|judgment", "gavel"),
    (r"stamp|seal|signature|signed|notaris|certif", "stamp"),
    (r"photograph|photo|camera|snapshot|picture", "camera"),
    (r"page|pages|file|files|document|documents|report|form|forms|letter|letters|envelope|record|records|paperwork", "page turn"),
    (r"door|doors|gate|gates|lock|locked|latch|bolt|key|keys|padlock|chain|chained|drawer|cabinet", "latch"),
    (r"telephone|phone|rang|ring|dial|receiver|call came|hung up", "click"),
    (r"car|cars|truck|van|vehicle|engine|drove|driving|traffic|road|highway|sedan", "pass-by"),
    (r"clock|hour|hours|minutes|waited|waiting|time passed|years later", "clock"),
    # `ran` and `hit` are excluded on purpose: the dry run put a footstep under "the dealership
    # RAN his credit" and an impact is as likely to be "hit a deadline" as a blow. A cue on the
    # wrong sense of a word is worse than no cue -- it tells the viewer the wrong thing happened.
    (r"footstep|footsteps|walked|walking|stepped|on foot", "footstep"),
    (r"glass|bottle|window|windows|cup|jar", "clink"),
    (r"slammed|struck|crash|crashed|broke open|torn|tore|smashed", "impact"),
    (r"knock|knocked|banging|hammer", "knock"),
    # `fabric` alone matched "a FABRICator's shop". Require the material sense.
    (r"rustle|cloth\b|fabric of|coat\b|curtain|blanket|sheet\b", "rustle"),
    # Weight cues rather than literal objects. This is the house style -- EP66 openfields uses
    # `low boom "court"` the same way -- and they are placed only on beats that carry the weight,
    # never as spacing. Kept last so a literal sound always wins the beat.
    (r"\bdied\b|\bdeath\b|\bdeaths\b|\bkilled\b|\bdead\b|fatal|\bburned\b|collapse", "low boom"),
    (r"but nobody|what nobody|the truth|in fact|instead|and then everything|it turned out", "riser"),
]

MIN_GAP_BEATS = 3          # never two cues within three beats: sound must punctuate, not carpet
TARGET_PER_MIN = 2.6       # comfortably over the 2.0 floor without becoming wallpaper


def pick_trigger(text: str, pattern: str) -> str | None:
    m = re.search(pattern, text, re.IGNORECASE)
    if not m:
        return None
    word = m.group(0).split()[0]
    return word.strip(".,;:\"'") or None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ep", required=True)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    path = ROOT / "episodes" / a.ep / "03_script" / "script.en.v001.md"
    if not path.is_file():
        raise SystemExit(f"no VO script at {path} -- run gen_vo_script.py first")
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    if any("(SFX:" in ln for ln in lines):
        raise SystemExit(f"{path.name} already carries (SFX: annotations -- refusing to double up")

    vo_idx = [i for i, ln in enumerate(lines) if ln.startswith("[VO:]")]
    # Target the REAL per-minute figure the gate measures, not a fraction of the beat count.
    # The first pass sized cues at 0.16 x beats and landed ramirez at 1.71/min and pinto at
    # 1.05 against a 2.0 floor, because beats-per-minute differs a lot between scripts.
    import json as _json
    idx = ROOT / "episodes" / a.ep / "06_audio" / "narration_index.v001.json"
    minutes = 0.0
    if idx.is_file():
        d = _json.loads(idx.read_text(encoding="utf-8"))
        minutes = float(d.get("total_seconds") or d.get("narrationSeconds") or 0) / 60.0
    want = max(24, round(TARGET_PER_MIN * minutes)) if minutes else max(24, int(len(vo_idx) * 0.16))

    # Spacing is a preference, the floor is a requirement. EP68 pinto writes long beats -- 162 of
    # them over 29.4 minutes -- so at one cue per three beats its ceiling is 54 cues against the
    # 59 the 2.0/min floor needs. It cannot reach the floor at that spacing no matter how good
    # the matching is. Loosen the gap only as far as the target requires, never further.
    gap = MIN_GAP_BEATS
    while gap > 1 and len(vo_idx) // gap < want:
        gap -= 1
    if gap != MIN_GAP_BEATS:
        print(f"[sfx] beat spacing relaxed {MIN_GAP_BEATS} -> {gap}: {len(vo_idx)} long beats "
              f"cannot carry {want} cues at the wider spacing")

    placed: list[tuple[int, str, str]] = []
    last = -99
    for n, i in enumerate(vo_idx):
        if n - last < gap:
            continue
        text = lines[i][len("[VO:]"):].strip()
        for pattern, keyword in RULES:
            trig = pick_trigger(text, pattern)
            if trig:
                placed.append((i, keyword, trig))
                last = n
                break
        if len(placed) >= want:
            break

    print(f"[sfx] {a.ep}: {len(vo_idx)} beats, placing {len(placed)} cue(s) (target {want})")
    for i, kw, trig in placed[:6]:
        print(f'   beat {i}: (SFX: {kw} "{trig}")   <- {lines[i][6:70]}')
    if a.dry_run:
        print("[sfx] DRY RUN -- nothing written")
        return 0

    out: list[str] = []
    ann = {i: (kw, t) for i, kw, t in placed}
    for i, ln in enumerate(lines):
        out.append(ln)
        if i in ann:
            kw, trig = ann[i]
            out.append(f'    (SFX: {kw} "{trig}")')
    path.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"[sfx] wrote {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
