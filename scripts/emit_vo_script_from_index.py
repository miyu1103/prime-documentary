#!/usr/bin/env python3
"""Write the [VO:] script that build_case_film_audio.py expects, from the narration index.

build_case_film_audio parses a beat sheet in an older format: one `[VO:]` line per spoken beat,
optionally followed by `(SFX: ...)` and `(VIS: ...)`. The EP62-65 scripts are written in the
current format -- plain narration under `## SECTION` headings -- so the builder found no beats and
refused, which is why all four films came out of the render with narration and nothing else: no
music bed, no room tone, no effects. The acceptance gate caught it as three separate hard failures
(bgm_present, sound_layers, loudness).

Rather than reformat the scripts by hand, derive the beat sheet from
``episodes/<ep>/06_audio/narration_index.v001.json``. That file is the record of what the voice
ACTUALLY said, chunk by chunk, with the section each chunk belongs to -- so the beat sheet cannot
drift from the audio, which a hand-maintained second copy of the script certainly would.

    py scripts/emit_vo_script_from_index.py --ep PD-2026-062-greene
    py scripts/emit_vo_script_from_index.py --ep PD-2026-062-greene --dry-run
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]

# What the narration says, mapped to the ONESHOT_MAP vocabulary that build_case_film_audio
# understands. The left side is a word the voice actually speaks; the right side is the cue name
# that selects the sample. Ordered: the most physical, most specific thing in a sentence wins.
SFX_TRIGGERS: list[tuple[str, str]] = [
    (r"\bknock(?:ed|ing|s)?\b", "knock"),
    (r"\bgavel\b", "gavel"),
    (r"\bstamp(?:ed|s)?\b", "stamp"),
    (r"\bseal(?:ed|s)?\b", "seal"),
    (r"\bslam(?:med|s)?\b", "slam"),
    (r"\bthud\b", "thud"),
    (r"\btore\b|\btorn\b|\btear(?:ing|s)?\b|\bripp?(?:ed|ing)\b", "tear"),
    (r"\bpage(?:s)?\b|\bleaf(?:ed|ing)?\b", "page turn"),
    (r"\bpaper(?:s)?\b|\bsheet(?:s)?\b|\bnotice(?:s)?\b|\bwrit(?:s)?\b|\bform(?:s)?\b", "rustle"),
    (r"\benvelope(?:s)?\b|\bmail(?:ed|ing|s)?\b|\bletter(?:s)?\b", "rustle"),
    (r"\block(?:ed|s)?\b|\blatch(?:ed|es)?\b|\bbolt(?:ed|s)?\b", "latch"),
    (r"\bbinder(?:s)?\b|\bfile(?:d|s)?\b|\bdrawer(?:s)?\b|\bcabinet\b", "binder"),
    (r"\bmeter(?:s)?\b|\bdial(?:s)?\b|\bswitch(?:ed|es)?\b", "click"),
    (r"\bphone\b|\btelephone(?:d|s)?\b|\bcall(?:ed|s)?\b|\brang\b|\bring(?:ing)?\b", "click"),
    (r"\btypewriter\b|\btyped?\b|\btyping\b", "type tick"),
    (r"\bclock\b|\bhour(?:s)?\b|\bminute(?:s)?\b|\bwaited\b|\bwaiting\b", "clock"),
    (r"\bfootstep(?:s)?\b|\bwalk(?:ed|ing|s)?\b|\bstep(?:ped|s)?\b", "footstep"),
    (r"\bdoor(?:s|way)?\b", "knock"),
    (r"\bglass\b|\bwindow(?:s)?\b", "clink"),
    (r"\bcourt(?:room|house)?\b|\bjudgment\b|\bruling\b|\bheld\b", "low boom"),
    # The gate wants at least 12 DISTINCT samples across a film, not merely enough cues. The
    # table above reaches only about ten; these point at the rest of ONESHOT_MAP using the words
    # the narration actually uses for those moments.
    (r"\bgavel\b|\bconvened\b|\badjourn(?:ed|ment)?\b", "gavel"),
    (r"\bphotograph(?:s|ed)?\b|\bcamera(?:s)?\b|\bpicture(?:s)?\b", "camera"),
    (r"\bsign(?:ed|ature|atures)\b|\bcertificate(?:s)?\b", "stamp"),
    (r"\bappeal(?:ed|s)?\b|\breversed\b|\bvacated\b|\bremanded\b", "riser"),
    (r"\bdissent(?:ed|ing|s)?\b|\bmajority\b|\bopinion(?:s)?\b", "sub-drop"),
    (r"\bterminat(?:ed|ion|e|ions)\b|\bdisconnect(?:ed|ion)?\b|\bshut off\b", "whoosh"),
    (r"\bdollar(?:s)?\b|\bpaid\b|\bpayment(?:s)?\b|\bbill(?:s|ed)?\b", "clink"),
    # OUTDOORS. Everything above this line is a courthouse, an office or a desk. EP66 openfields
    # is a film about land: its declared motif (FILM_BIBLE v001 s3) is a padlock on a chain across
    # a farm gate, and the narration speaks "gate" 11 times, "branch" 3, "gravel" 2 -- and reached
    # 1.93 designed cues/min against build_case_film_audio SFX_PER_MIN_FLOOR of 2.0, because the
    # table above has no word for anything outside a building. These are appended, never inserted,
    # so no sentence that already wins an earlier trigger changes its cue; they only speak where
    # the table was previously silent. Each maps to an existing ONESHOT_MAP sample -- a gate latch,
    # foliage, boots on gravel, a truck going past -- so the cue is the thing the voice just named,
    # not filler. (Padding a density number with meaningless pips is the EP32 rejection; do not.)
    (r"\bgate(?:s|way|ways)?\b|\bpadlock(?:ed|s)?\b|\bchain(?:ed|s)?\b", "latch"),
    (r"\bbranch(?:es)?\b|\bbrush\b|\bunderbrush\b|\bleaves\b|\bfoliage\b", "rustle"),
    (r"\bboot(?:s)?\b|\bgravel\b|\bmud\b", "footstep"),
    (r"\btruck(?:s)?\b|\bengine(?:s)?\b|\bvehicle(?:s)?\b|\bdrove\b|\bdriv(?:e|es|ing)\b", "pass-by"),
]
MIN_BEATS_BETWEEN_CUES = 3          # never two cues back to back; the bed has to breathe


def sfx_for(text: str, last_cue_beat: int) -> tuple[str, str] | None:
    """The spoken word to hang a cue on, and the cue name, or None.

    Returns the FIRST trigger in the table that the sentence actually contains, so the most
    physical reading wins over an incidental one, and only if enough beats have passed since the
    last cue.
    """
    if last_cue_beat < MIN_BEATS_BETWEEN_CUES:
        return None
    low = text.lower()
    for pat, kind in SFX_TRIGGERS:
        m = re.search(pat, low)
        if m:
            return m.group(0), kind
    return None



def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ep", required=True, help="episode id, e.g. PD-2026-062-greene")
    ap.add_argument("--index", type=Path, default=None)
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    ep_dir = ROOT / "episodes" / a.ep
    index = a.index or ep_dir / "06_audio" / "narration_index.v001.json"
    out = a.out or ep_dir / "03_script" / "script.en.v001.md"
    if not index.is_file():
        print(f"no narration index at {index}", file=sys.stderr)
        return 1

    idx = json.loads(index.read_text(encoding="utf-8"))
    chunks = idx.get("chunks") or []
    if not chunks:
        print("narration index has no chunks", file=sys.stderr)
        return 1

    lines = [
        f"# {a.ep} — VO beat sheet",
        "",
        "> GENERATED from 06_audio/narration_index.v001.json by "
        "scripts/emit_vo_script_from_index.py. Do not hand-edit: it is a projection of what the",
        "> narration master actually says, and build_case_film_audio.py times the music, room tone",
        "> and effects against it. Edit the real script, regenerate the narration, then re-emit.",
        "",
    ]
    section = None
    n = 0
    cues = 0
    last_cue = -99
    for c in chunks:
        sec = c.get("section") or "BODY"
        if sec != section:
            lines += ["", f"## {sec}", ""]
            section = sec
        text = (c.get("spoken_text") or c.get("text") or "").strip()
        if not text:
            continue
        lines.append(f"[VO:] {text}")
        n += 1
        cue = sfx_for(text, last_cue_beat=n - last_cue)
        if cue:
            word, kind = cue
            lines.append(f'    (SFX: {kind} "{word}")')
            last_cue = n
            cues += 1

    body = "\n".join(lines) + "\n"
    print(f"[vo] {a.ep}: {n} beat(s), {cues} SFX cue(s) across {len({c.get('section') for c in chunks})} section(s) -> {out}")
    if a.dry_run:
        print("\n".join(lines[:14]))
        return 0
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(body, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
