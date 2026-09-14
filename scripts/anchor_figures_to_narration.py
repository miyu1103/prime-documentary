#!/usr/bin/env python
"""Pin each figure beat to the narration line it is ABOUT, by matching words.

WHY THIS EXISTS. build_case_film_generic.build_figures spreads a section's figure
payloads evenly across that section's window whenever they carry no `at_seconds`.
Measured 2026-09-07 on EP85 katrina: the figures track lagged the narration by a
MEDIAN 52 s and the lag GREW through the film (19 s -> 132 s), because even spacing
and real speech drift apart. That is not a cosmetic problem. Three cards in the first
three minutes told the viewer the opposite of the film:

    1:52  card "WATER WENT OVER THE TOP. THE WALLS FELL BACKWARDS."
          over caption "Floodwalls at the 17th Street and London Avenue Canals
          were NOT overtopped."
    2:05  card "THAT IS A BAD DAY. IT IS NOT A SCANDAL."
          over caption "The wall failed anyway."
    2:48  17th Street's as-built depth over London Avenue captions.

A true card on the wrong second asserts something false. The same defect on EP83
max737 put "FIFTEEN CRASHES. BELOW THE THRESHOLD." directly above the caption
"All one hundred and fifty-seven people aboard died."

WHAT IT DOES. For every figure in the built film json, take its own words, find the
caption cue whose words overlap it most, and write that cue's start into the episode's
filmconfig as `at_seconds` (which build_figures already honours -- see its `pinned`
branch). A figure whose best match is weak is LEFT ALONE and reported, because a
confident wrong anchor is worse than the drift it replaces.

    py -3.11 scripts/anchor_figures_to_narration.py --slug katrina --dry-run
    py -3.11 scripts/anchor_figures_to_narration.py --slug katrina --apply

It never edits the film json (that is a build output) and never touches captions,
cuts or narration. It writes only `at_seconds`/`hold_seconds` into filmconfig payloads.
"""
from __future__ import annotations

import argparse
import glob
import json
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]

# Words that say nothing about WHICH line a card belongs to.
STOP = {
    "the", "a", "an", "and", "or", "but", "if", "of", "to", "in", "on", "at", "for",
    "with", "that", "this", "it", "is", "was", "are", "were", "be", "been", "by",
    "from", "as", "not", "no", "any", "all", "its", "their", "they", "them", "he",
    "she", "his", "her", "one", "two", "had", "has", "have", "did", "do", "does",
    "what", "who", "why", "how", "when", "where", "which", "there", "then", "than",
    "so", "up", "out", "into", "over", "under", "after", "before", "about", "would",
    "could", "said", "says", "you", "your", "we", "our", "i",
}

MIN_OVERLAP = 4        # a match needs at least this many shared content words
LEAD = 0.4             # land the card just after the words are spoken
DEFAULT_HOLD = 6.0


def words(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z0-9']{3,}", text.lower()) if w not in STOP}


def figure_text(f: dict) -> str:
    parts = []
    for k in ("lines", "primary", "secondary", "text", "quote", "attribution", "title", "label"):
        v = f.get(k)
        if isinstance(v, list):
            parts += [str(x) for x in v]
        elif v:
            parts.append(str(v))
    for k in ("rows", "bars", "items", "nodes"):
        for row in f.get(k) or []:
            if isinstance(row, dict):
                parts += [str(v) for v in row.values() if isinstance(v, (str, int, float))]
            else:
                parts.append(str(row))
    return " ".join(parts)


def load_cues(srt: Path) -> list[tuple[float, str]]:
    def sec(t: str) -> float:
        h, m, rest = t.split(":")
        s, ms = rest.split(",")
        return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000
    out = []
    for block in srt.read_text(encoding="utf-8").strip().split("\n\n"):
        lines = block.strip().split("\n")
        if len(lines) < 3 or "-->" not in lines[1]:
            continue
        out.append((sec(lines[1].split(" --> ")[0]), " ".join(lines[2:])))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    film = ROOT / f"remotion/src/data/{a.slug}_film.json"
    if not film.is_file():
        print(f"no built film json at {film} -- build the episode first", file=sys.stderr)
        return 1
    cfgs = sorted(glob.glob(str(ROOT / f"episodes/_planning/EP*_{a.slug}_filmconfig.v*.json")))
    if not cfgs:
        print(f"no filmconfig for {a.slug}", file=sys.stderr)
        return 1
    cfg_path = Path(cfgs[-1])
    epdirs = sorted(glob.glob(str(ROOT / f"episodes/PD-*-{a.slug}")))
    srt = Path(epdirs[-1]) / "08_edit/captions.final.v001.srt"
    if not srt.is_file():
        print(f"no captions at {srt}", file=sys.stderr)
        return 1

    figures = json.loads(film.read_text(encoding="utf-8")).get("figures") or []
    cues = load_cues(srt)
    cue_words = [(t, words(txt), txt) for t, txt in cues]
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))

    # index filmconfig payloads by their own text, so a match can be written back
    by_text: dict[str, dict] = {}
    for sec_name, payloads in (cfg.get("figures_by_section") or {}).items():
        for p in payloads:
            by_text.setdefault(figure_text(p).strip().lower(), p)

    pinned = weak = skipped = 0
    # THE CARDS ARE AUTHORED IN NARRATIVE ORDER AND SO IS THE NARRATION, so a match may
    # never run backwards past the card before it. Without this, a 3-word overlap on a
    # common noun threw katrina's "THE WALL WAS SUPPOSED TO BE FOURTEEN FEET" card 164 s
    # BACKWARDS onto the hook, which is a worse lie than the drift being fixed.
    floor = 0.0
    for f in figures:
        ftxt = figure_text(f)
        fw = words(ftxt)
        if f.get("kind") in ("acttitle", "lowerthird") or not fw:
            skipped += 1
            continue
        best_t, best_n, best_line = None, 0, ""
        for t, cw, raw in cue_words:
            if t < floor:
                continue
            n = len(fw & cw)
            if n > best_n:
                best_t, best_n, best_line = t, n, raw
        payload = by_text.get(ftxt.strip().lower())
        label = (ftxt[:52] + "...") if len(ftxt) > 52 else ftxt
        if best_n < MIN_OVERLAP or best_t is None:
            weak += 1
            print(f"  WEAK  (overlap {best_n}) leave as built @{f['start']:7.1f}s  {label}")
            continue
        target = round(best_t + LEAD, 3)
        floor = best_t + 0.5          # the next card must land after this one
        drift = target - f["start"]
        print(f"  pin   @{target:7.1f}s (was {f['start']:7.1f}, drift {drift:+6.1f}s, "
              f"overlap {best_n})  {label}")
        if payload is not None and a.apply:
            payload["at_seconds"] = target
            payload.setdefault("hold_seconds", round(f["end"] - f["start"], 3) or DEFAULT_HOLD)
            pinned += 1
        elif payload is None:
            print("        (no matching filmconfig payload -- not written)")

    if a.apply:
        cfg_path.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"\nwrote {cfg_path.name}: {pinned} payload(s) pinned, {weak} weak, {skipped} skipped")
    else:
        print(f"\nDRY RUN -- {weak} weak, {skipped} skipped (act titles and disclosures never move)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
