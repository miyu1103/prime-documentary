#!/usr/bin/env python3
r"""Check a Short design against the episode's OWN machine contract and against length.

`check_short_design.py` proves every line traces to the script. It does not read the
`episode_spec`, so nothing was checking the two things that can actually stop a ship
(`.claude/rules/19`): a `forbidden_subjects` term in the narration, and a `forbidden_claims`
statement made in the film's own voice.

WHY THE HIGHEST REVISION AND NOT v001. The long-form thread measured this on 2026-08-24:
`episode_spec.v001.json` was hard-coded in 19 scripts, and lahaina's v001 says
`people_plates: null` while its v003 lists 24. Checking EP70 against v001 was correct only by
luck -- EP70 has no other revision. **EP71 oroville has v002 and EP75 lahaina has v003**, so the
very next episode in the queue would have been checked against a superseded contract. The
resolver is imported from `check_episode_spec`, not restated here.

WHAT IT MEASURES

  forbidden_subjects  word-boundary match against the spoken text of every line
  forbidden_claims    substring match for the short, quotable ones; the long prose entries are
                      PRINTED for a human instead, because a paragraph of policy cannot be
                      matched and pretending otherwise is worse than saying so
  plates              every source_plate exists on disk
  length              159-180 spoken words, measured off 28 finished Shorts that each run
                      58.0 s at a median 2.90 words/second

    py -3.11 scripts/check_short_constraints.py episodes/_planning/short_designs/*.json
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from check_episode_spec import spec_path  # noqa: E402 -- one resolver, not a second copy

WORDS_MIN, WORDS_MAX = 159, 180
WPS = 2.90
# The render gate refuses a YouTube Short composition longer than 58 s
# (preflight_short_render.py). The word band is a PROXY for that, calibrated at 2.90
# words/second on 28 finished Shorts -- and on 2026-08-25 eight Shorts sat inside the
# band and still rendered long, because a line delivered "calm" runs at 2.6 w/s and a
# spoken figure ("twenty-four million, six hundred and ten thousand") runs slower still.
# So when the mix exists, measure it; the proxy only stands in until it does.
DUR_MIN, DUR_MAX = 45.0, 57.0


def mix_seconds(short_id: str) -> float | None:
    """Measured duration of the Short's final mix, or None if it has not been built."""
    mix = (ROOT / "remotion" / "public" / "shorts" / short_id / "audio"
           / f"{short_id}_final_mix_v002_en_us.mp3")
    if not mix.is_file():
        return None
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", str(mix)], capture_output=True, text=True,
                         encoding="utf-8", errors="replace")
    try:
        return float(out.stdout.strip())
    except ValueError:
        return None


def plate_dirs(slug: str) -> list[Path]:
    """Every directory that can hold this episode's plates, best first.

    `img/` is curated while other threads work -- on 2026-08-25 the itaewon set went
    116 -> 94 files mid-session because the assembly thread re-ran its selection, and
    eleven plates a Short had already staged read as "not on disk" although their bytes
    were untouched one directory away. A plate that exists in the episode's own raw or
    upscaled set still exists; reporting otherwise measures the curation, not the plate.
    """
    pub = ROOT / "remotion" / "public" / slug
    cands = [pub / "img", *sorted(pub.glob("img_raw_codex*")), *sorted(pub.glob("img_esrgan*")),
             *sorted((ROOT / "remotion").glob(f"public_ep*/{slug}/img"))]
    return [c for c in cands if c.is_dir()]


def plate_dir(slug: str) -> Path | None:
    dirs = plate_dirs(slug)
    return dirs[0] if dirs else None


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 2

    problems = 0
    for path in args:
        d = json.loads(Path(path).read_text(encoding="utf-8"))
        epid, slug = d["episode_id"], d["slug"]
        epdir = ROOT / "episodes" / epid
        spec_file = spec_path(epdir)
        spec = json.loads(spec_file.read_text(encoding="utf-8"))
        subjects = [s.lower() for s in spec.get("forbidden_subjects", [])]
        short_subjects = [s for s in subjects if len(s) < 25 and " " not in s]
        claims = [c.lower() for c in spec.get("forbidden_claims", [])]
        short_claims = [c for c in claims if len(c) < 80]
        long_claims = [c for c in claims if len(c) >= 80]
        dirs = plate_dirs(slug)
        avail = {p.stem for d in dirs for p in d.glob("*.png")}

        print(f"\n{epid}   spec {spec_file.name}   plates {len(avail)}")
        for sh in d["shorts"]:
            text = " ".join(l["text"] for l in sh["lines"])
            low = text.lower()
            n = len(text.split())
            hits = [s for s in short_subjects if re.search(rf"\b{re.escape(s)}\b", low)]
            chits = [c[:50] for c in short_claims if c in low]
            miss = [p["source_plate"] for p in sh["plates"] if avail and p["source_plate"] not in avail]
            secs = mix_seconds(sh["short_id"])
            if secs is None:
                length_bad = not (WORDS_MIN <= n <= WORDS_MAX)
                length_note = ("" if not length_bad
                               else f"  <- OUTSIDE {WORDS_MIN}-{WORDS_MAX} words (no mix yet)")
                length_desc = f"{n:>3} words ~{n / WPS:.0f}s est"
            else:
                length_bad = not (DUR_MIN <= secs <= DUR_MAX)
                length_note = ("" if not length_bad
                               else f"  <- OUTSIDE {DUR_MIN:.0f}-{DUR_MAX:.0f}s measured")
                length_desc = f"{n:>3} words {secs:.1f}s measured"
            bad = bool(hits or chits or miss) or length_bad
            problems += bool(bad)
            print(f"  {sh['short_id']}  {length_desc}{length_note}")
            if hits:
                print(f"      forbidden_subjects in narration: {hits}")
            if chits:
                print(f"      forbidden_claims matched: {chits}")
            if miss:
                print(f"      plates not on disk: {miss}")
        if long_claims:
            print(f"  {len(long_claims)} forbidden_claim(s) are prose and CANNOT be matched by a "
                  f"machine. A person reads these against the Shorts:")
            for c in long_claims:
                print(f"      - {c[:150]}")

    print(f"\n{len(args)} design(s) checked, {problems} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
