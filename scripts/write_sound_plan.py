#!/usr/bin/env python3
r"""Write an episode's sound plan into its `[VO:]` script. Generic: `--slug`, `--rules`.

WHY THIS EXISTS
---------------
`gen_vo_script.py` emits ONLY `[VO:]` lines and has never written a sound cue, so every new
episode arrives silent and nobody notices until `_finish_episode.sh` [4d] dry-runs the four-layer
mix and the density gate refuses. EP70 lost three pipeline runs to it; EP71 arrived at 7 cues
against a 2.0/min floor.

The fix was written twice as a one-off -- `write_wronghouse_sound_plan.py` and
`write_oroville_sound_plan.py` -- each with its episode's path AND its rule table hard-coded.
A third copy would have been the obvious wrong move (invariant 14), so this is the generic one.
**Migrate EP70 and EP71 onto it and delete both one-offs.**

WHAT IT DOES NOT DO
-------------------
It does not define what a `kind` is. The vocabulary lives in `build_case_film_audio.ONESHOT_MAP`
and is IMPORTED, never retyped -- the same discipline `check_design_doc` uses for the opening
checks. A rule naming a kind that map cannot resolve is rejected before anything is written, so a
typo cannot reach the mix as a silently-dropped cue.

THE TWO THINGS A RULE MUST GET RIGHT
------------------------------------
1. `kind` must resolve in ONESHOT_MAP (first match wins there, so order matters there, not here).
2. `anchor` must be a word the beat ACTUALLY SPEAKS. The one-shot is placed on that word; an
   anchor the beat does not contain places nothing, and the gate then reports a density failure
   whose cause is a typo three files away.

Both are checked. `--dry-run` reports and writes nothing.

    py -3.11 scripts/write_sound_plan.py --slug lahaina --rules config/sound_rules/lahaina.json
    py -3.11 scripts/write_sound_plan.py --slug lahaina --dry-run
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

MIN_GAP_BEATS = 4      # beats between cues, so nothing machine-guns
MAX_PER_KIND = 14      # no single texture carries the film


def kinds_available() -> dict[str, str]:
    """kind keyword -> sample file, IMPORTED from the mixer. Never retyped here."""
    from build_case_film_audio import ONESHOT_MAP  # noqa: PLC0415 - deliberate runtime import
    out: dict[str, str] = {}
    for keywords, sample, _dur, _vol in ONESHOT_MAP:
        for k in keywords:
            out.setdefault(k.lower(), sample)
    return out


def episode_dir(slug: str) -> Path:
    hits = sorted((ROOT / "episodes").glob(f"PD-*-{slug}"))
    if not hits:
        raise SystemExit(f"[sound] no episode directory for slug {slug!r}")
    return hits[-1]


def load_rules(path: Path | None, default: Path) -> list[tuple[str, str, str]]:
    p = path or default
    if not p.is_file():
        raise SystemExit(
            f"[sound] no rule file at {p}.\n"
            f"        Rules are per-EPISODE -- what a film sounds like is not generic. Write one:\n"
            f'        [{{"needle": "siren", "kind": "click", "anchor": "siren"}}, ...]\n'
            f"        needle = the word that selects the beat, anchor = the word the cue lands on.")
    rows = json.loads(p.read_text(encoding="utf-8"))
    # a row whose needle starts with __ is documentation, not a rule. A rule file has to
    # carry the reasoning for what the film sounds like, and JSON has no comments.
    return [(r["needle"], r["kind"], r["anchor"]) for r in rows
            if not str(r.get("needle", "")).startswith("__")]


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--rules", type=Path, help="json rule list (default config/sound_rules/<slug>.json)")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--min-gap", type=int, default=MIN_GAP_BEATS)
    ap.add_argument("--max-per-kind", type=int, default=MAX_PER_KIND)
    a = ap.parse_args()

    epdir = episode_dir(a.slug)
    script = epdir / "03_script" / "script.en.v001.md"
    if not script.is_file():
        raise SystemExit(f"[sound] no [VO:] script at {script}\n"
                         f"        run: py -3.11 scripts/gen_vo_script.py --ep {epdir.name} --force")

    rules = load_rules(a.rules, ROOT / "config" / "sound_rules" / f"{a.slug}.json")
    vocab = kinds_available()
    bad = sorted({k for _n, k, _a in rules if k.lower() not in vocab})
    if bad:
        print(f"[sound] FAIL {len(bad)} rule(s) name a kind ONESHOT_MAP cannot resolve: {', '.join(bad)}")
        print(f"        available: {', '.join(sorted(vocab))}")
        return 1

    lines = script.read_text(encoding="utf-8").splitlines()
    if any("(SFX:" in ln for ln in lines):
        print("[sound] this script already carries (SFX:) cues -- refusing to double them")
        return 1

    out: list[str] = []
    last, beat, placed = -99, 0, 0
    per: dict[str, int] = {}
    unmatched_anchor = 0
    for ln in lines:
        out.append(ln)
        if not ln.startswith("[VO:]"):
            continue
        beat += 1
        if beat - last < a.min_gap:
            continue
        low = ln[5:].strip().lower()
        for needle, kind, anchor in rules:
            if needle.lower() not in low:
                continue
            if per.get(kind, 0) >= a.max_per_kind:
                continue
            # the anchor must be a word this beat actually speaks
            if not re.search(r"\b" + re.escape(anchor.split()[-1].lower()), low):
                unmatched_anchor += 1
                continue
            out.append(f'    (SFX: {kind} "{anchor}")')
            per[kind] = per.get(kind, 0) + 1
            last, placed = beat, placed + 1
            break

    idx = epdir / "06_audio" / "narration_index.v001.json"
    minutes = (json.loads(idx.read_text(encoding="utf-8"))["total_seconds"] / 60.0) if idx.is_file() else 0.0
    density = (placed / minutes) if minutes else 0.0

    print(f"[sound] {a.slug}: {beat} beat(s), {placed} cue(s) placed")
    if minutes:
        print(f"[sound] {minutes:.1f} min -> {density:.2f} cues/min "
              f"(floors: 2.0/min AND 20 total, build_case_film_audio)")
        short = max(0, int(minutes * 2.0) + 1 - placed)
        if placed < 20 or density < 2.0:
            print(f"[sound] BELOW FLOOR -- add about {short} more rule hits, or widen the needles")
    for k, v in sorted(per.items(), key=lambda kv: -kv[1]):
        print(f"           {v:3d}  {k}  -> {vocab[k.lower()]}")
    if unmatched_anchor:
        print(f"[sound] {unmatched_anchor} rule match(es) skipped: the beat did not speak the anchor word")

    if a.dry_run:
        print("[sound] --dry-run: nothing written")
        return 0
    script.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"[sound] wrote {script.relative_to(ROOT)}")
    return 0 if (placed >= 20 and density >= 2.0) else 1


if __name__ == "__main__":
    raise SystemExit(main())
