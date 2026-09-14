#!/usr/bin/env python
"""Derive ONE machine-readable production spec from the finalised script.

Why this exists (2026-07-20). The EP39/EP40 document set accumulated 28 BLOCKER-level
inconsistencies because the same facts were HAND-WRITTEN into six documents with no
single source of truth:

  * EP39's Codex A/B files never once name the protagonist (Barry Laughman) -- they were
    authored before the subject was chosen, and were never revisited when the script
    landed.
  * EP40's A file orders scenes S01-S64 while the finalised script contains exactly
    S01-S25.
  * EP39's v002 and CODEX_A use the SAME codes S01-S50 for DIFFERENT subjects (46 of 50
    disagree), so every asset would land on the wrong beat.
  * Runtime, word count, act splits, asset allocation and beat counts each appear with
    two or three different values across the set.

Patching those one by one is what produced them: every hand-fix leaves the other five
documents stale. So the numbers are COMPUTED here, from the script, once -- and the
downstream documents are generated from this file instead of restating it.

Everything emitted is checked against the real gate modules (check_script_length,
check_asset_reuse) rather than against a remembered threshold.

Read-only against the script. Writes one JSON per episode. No paid calls.

Usage:
    python scripts/build_production_spec.py --ep frazier
    python scripts/build_production_spec.py --ep lech --json
"""
from __future__ import annotations

import argparse
import importlib
import json
import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

try:
    sys.stdout.reconfigure(encoding="utf-8")  # cp932 guard (Windows)
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
PLANNING = ROOT / "episodes" / "_planning"

# Measured 2026-07-19 over 31 shipped episodes (real ElevenLabs clip durations).
WPM_MEDIAN = 178.1

EPISODES = {
    "frazier": {
        "episode_id": "PD-2026-039-frazier",
        "ep": "EP39",
        "script": "EP39_frazier_script.en.v001.md",
        "scene_source": "design_v002",   # script carries no scene codes
        "design": "EP39_frazier_DESIGN_and_CODEX_PROMPTS.v002.md",
    },
    "lech": {
        "episode_id": "PD-2026-040-lech",
        "ep": "EP40",
        "script": "EP40_lech_script.en.v001.md",
        "scene_source": "script",        # act headings carry [S01 S02 ...]
        "design": "EP40_lech_DESIGN_and_CODEX_PROMPTS.v002.md",
    },
    "thompson": {
        "episode_id": "PD-2026-041-thompson",
        "ep": "EP41",
        "script": "EP41_thompson_script.en.v001.md",
        "scene_source": "derive",        # no scene codes and no design yet: derive count
        "design": None,
    },
    "young": {
        "episode_id": "PD-2026-042-young",
        "ep": "EP42",
        "script": "EP42_young_script.en.v001.md",
        "scene_source": "derive",        # ACT headings only, no [S01 S02] codes: derive count
        "design": None,
    },
    "caniglia": {
        "episode_id": "PD-2026-043-caniglia",
        "ep": "EP43",
        "script": "EP43_caniglia_script.en.v001.md",
        "scene_source": "derive",        # ACT headings only, no [S01 S02] codes: derive count
        "design": None,
    },
    "tekoh": {
        "episode_id": "PD-2026-044-tekoh",
        "ep": "EP44",
        "script": "EP44_tekoh_script.en.v001.md",
        "scene_source": "derive",
        "design": None,
    },
    "cleveland": {
        "episode_id": "PD-2026-045-cleveland",
        "ep": "EP45",
        "script": "EP45_cleveland_script.en.v001.md",
        "scene_source": "derive",
        "design": None,
    },
    "tlo": {
        "episode_id": "PD-2026-046-tlo",
        "ep": "EP46",
        "script": "EP46_tlo_script.en.v001.md",
        "scene_source": "derive",
        "design": None,
    },
    "atwater": {
        "episode_id": "PD-2026-047-atwater",
        "ep": "EP47",
        "script": "EP47_atwater_script.en.v001.md",
        "scene_source": "derive",
        "design": None,
    },
    "glover": {
        "episode_id": "PD-2026-048-glover",
        "ep": "EP48",
        "script": "EP48_glover_script.en.v001.md",
        "scene_source": "derive",
        "design": None,
    },
    "strieff": {
        "episode_id": "PD-2026-049-strieff",
        "ep": "EP49",
        "script": "EP49_strieff_script.en.v001.md",
        "scene_source": "derive",
        "design": None,
    },
}

# Gate constants are IMPORTED, never retyped -- a retyped threshold is how the "<=4 uses"
# cap survived after the real cap became 2.
_reuse = importlib.import_module("check_asset_reuse")
MAX_FACTORY = _reuse.MAX_USES_FACTORY
MAX_MOTION = _reuse.MAX_USES_MOTION
MAX_STILL = _reuse.MAX_USES_STILL
MIN_FIRST_USE = _reuse.MIN_FIRST_USE_SHARE

MIN_BEATS_PER_MIN = 2.5      # check_motion_density floor
MIN_BEAT_VARIETY = 3
MAX_STILL_SHARE = 0.45       # check_animation_mix cap
MAX_SHOT_SECONDS = 6.0       # SPEC v2: average shot length


# Reuse the SAME word counter as the length gate rather than a second copy. The local
# copy here still stripped only ASCII brackets, so on EP41 it counted 2,672 words
# (incl. 【OST】/〔CARD〕 and the 事実対応表/タイトル appendix) vs the real 2,026 spoken
# -- a 15.0-min projection instead of ~11.4, i.e. the exact stale-number drift the whole
# single-source-of-truth pipeline exists to prevent. One definition, imported.
_csl = importlib.import_module("check_script_length")
narration_words = _csl.count_words


def parse_acts(script_text: str) -> list[dict]:
    """Split on '## ' headings; capture any [S01 S02 ...] scene codes on the heading."""
    parts = re.split(r"^##\s+(.+)$", script_text, flags=re.M)
    acts = []
    for i in range(1, len(parts), 2):
        heading, body = parts[i].strip(), parts[i + 1]
        if heading.startswith("事実対応表") or heading.startswith("改稿ログ"):
            continue
        codes = re.findall(r"\bS\d{2}\b", heading)
        acts.append({
            "heading": heading,
            "scene_codes": codes,
            "words": narration_words(body),
        })
    return acts


def allocate_assets(total_cuts: int) -> dict:
    """Pick a still/factory/motion split that clears BOTH gates.

    The trap this encodes: first_use_share == distinct/cuts == 1/mean_uses. Filling every
    asset to its cap therefore DRIVES THE SHARE DOWN -- the earlier hand-written plan
    (factory 50 + still 50x2 + i2v 15x2) scored 0.639 and would have hard-failed. A cap is
    a ceiling, not a target.
    """
    for still_uses in (1.2, 1.3, 1.4, 1.5, 1.6, 1.8, 2.0):
        motion_clips = max(12, round(total_cuts * 0.07))
        motion_cuts = motion_clips * MAX_MOTION
        still_cuts = math.floor(total_cuts * MAX_STILL_SHARE)
        factory_cuts = total_cuts - still_cuts - motion_cuts
        if factory_cuts < 1:
            continue
        factory_clips = factory_cuts  # cap 1 use -> one clip per cut
        still_imgs = math.ceil(still_cuts / still_uses)
        distinct = still_imgs + factory_clips + motion_clips
        share = distinct / total_cuts
        if share >= MIN_FIRST_USE and still_uses <= MAX_STILL:
            return {
                "total_cuts": total_cuts,
                "still": {"distinct": still_imgs, "cuts": still_cuts,
                          "mean_uses": round(still_cuts / still_imgs, 2), "cap": MAX_STILL},
                "factory": {"distinct": factory_clips, "cuts": factory_cuts,
                            "mean_uses": 1.0, "cap": MAX_FACTORY},
                "motion": {"distinct": motion_clips, "cuts": motion_cuts,
                           "mean_uses": float(MAX_MOTION), "cap": MAX_MOTION},
                "distinct_total": distinct,
                "first_use_share": round(share, 4),
                "first_use_floor": MIN_FIRST_USE,
                "still_share_of_cuts": round(still_cuts / total_cuts, 4),
                "still_share_cap": MAX_STILL_SHARE,
            }
    raise SystemExit("no allocation satisfies both gates -- widen the search")


def build(slug: str) -> dict:
    cfg = EPISODES[slug]
    script_path = PLANNING / cfg["script"]
    text = script_path.read_text(encoding="utf-8")

    acts = parse_acts(text)
    total_words = narration_words(text)
    narration_seconds = total_words / WPM_MEDIAN * 60

    scenes = sorted({c for a in acts for c in a["scene_codes"]})
    if not scenes and cfg["scene_source"] == "design_v002" and cfg.get("design"):
        design = (PLANNING / cfg["design"]).read_text(encoding="utf-8")
        scenes = sorted(set(re.findall(r"\bS\d{2}\b", design)))
    if not scenes and cfg["scene_source"] == "derive":
        # No scene codes and no design yet. Derive a target count from runtime: one
        # distinct subject roughly every ~15s of narration (matches the 48-50 scenes
        # the EP39/EP40 corrections landed on for a 12-min film). Emit S01..Snn codes
        # so downstream can bind assets by code.
        n = max(40, min(56, round(narration_seconds / 15)))
        scenes = [f"S{i:02d}" for i in range(1, n + 1)]

    for a in acts:
        a["seconds"] = round(a["words"] / WPM_MEDIAN * 60, 1)

    total_cuts = math.ceil(narration_seconds / 3.2)      # ~3.2s mean shot, under the 6.0 cap
    alloc = allocate_assets(total_cuts)
    beats_floor = math.ceil(narration_seconds / 60 * MIN_BEATS_PER_MIN)

    spec = {
        "_generated_by": "scripts/build_production_spec.py",
        "_source_of_truth": (
            "This file is DERIVED from the finalised script. Do not hand-edit it, and do "
            "not restate these numbers in prose documents -- generate from here. The "
            "EP39/EP40 document set accrued 28 blocker-level contradictions precisely "
            "because the same facts were hand-copied into six files."
        ),
        "schema": "pd_production_spec.v1",
        "episode_id": cfg["episode_id"],
        "ep": cfg["ep"],
        "slug": slug,
        "script_file": cfg["script"],
        "wpm_used": WPM_MEDIAN,
        "words_total": total_words,
        "narration_seconds": round(narration_seconds, 1),
        "acts": acts,
        "scenes": {
            "source": cfg["scene_source"],
            "codes": scenes,
            "count": len(scenes),
        },
        "assets": alloc,
        "motion": {
            "beats_floor": beats_floor,
            "beats_per_min_floor": MIN_BEATS_PER_MIN,
            "variety_floor": MIN_BEAT_VARIETY,
            "note": ("check_motion_density counts graphics+figures+heroCuts inside "
                     "film.json ONLY. AE cards composited afterwards do NOT count toward "
                     "it -- both EP39 and EP40 planned around AE cards and would have "
                     "failed. Put beats_floor beats in film.json regardless of AE."),
        },
        "mean_shot_seconds": round(narration_seconds / total_cuts, 2),
        "max_shot_seconds": MAX_SHOT_SECONDS,
    }
    return spec


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ep", choices=sorted(EPISODES), required=True)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    spec = build(a.ep)
    out = PLANNING / f"{spec['ep']}_{a.ep}_PRODUCTION_SPEC.v001.json"
    out.write_text(json.dumps(spec, ensure_ascii=False, indent=2), encoding="utf-8")

    if a.json:
        print(json.dumps(spec, ensure_ascii=False, indent=2))
        return 0

    al = spec["assets"]
    print(f"{spec['ep']} {spec['episode_id']}")
    print(f"  words {spec['words_total']:,}  -> narration {spec['narration_seconds']}s "
          f"({spec['narration_seconds']/60:.1f} min) @ {WPM_MEDIAN} wpm")
    print(f"  scenes {spec['scenes']['count']} (from {spec['scenes']['source']}): "
          f"{spec['scenes']['codes'][0] if spec['scenes']['codes'] else '-'}"
          f"..{spec['scenes']['codes'][-1] if spec['scenes']['codes'] else '-'}")
    print(f"  acts:")
    for act in spec["acts"]:
        print(f"    {act['words']:>5}w {act['seconds']:>6}s  {act['heading'][:58]}")
    print(f"  cuts {al['total_cuts']}  mean shot {spec['mean_shot_seconds']}s "
          f"(cap {MAX_SHOT_SECONDS})")
    print(f"    still   {al['still']['distinct']:>4} distinct / {al['still']['cuts']:>4} cuts "
          f"({al['still']['mean_uses']}x, cap {al['still']['cap']})")
    print(f"    factory {al['factory']['distinct']:>4} distinct / {al['factory']['cuts']:>4} cuts "
          f"({al['factory']['mean_uses']}x, cap {al['factory']['cap']})")
    print(f"    motion  {al['motion']['distinct']:>4} distinct / {al['motion']['cuts']:>4} cuts "
          f"({al['motion']['mean_uses']}x, cap {al['motion']['cap']})")
    print(f"    first-use {al['first_use_share']} (floor {al['first_use_floor']}) "
          f"| still share {al['still_share_of_cuts']} (cap {al['still_share_cap']})")
    print(f"  MG beats floor {spec['motion']['beats_floor']} in film.json "
          f"(AE cards do NOT count)")
    print(f"\nwrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
