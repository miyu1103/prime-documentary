#!/usr/bin/env python
"""Generate a MotionSample-era shotlist.v001.json from a script.annotated.v001.json.

Image-independent PLAN: it fixes, per narration span, the estimated seconds, the
number of fast cuts (~2.8s each, MotionSample pace), the still-treatment rotation
(bleed/scan/duotone/focus -- NEVER ken_burns/wipe), the 0.35s crossfade, the
on-screen-text beats, and the asset pool (which of the 40 Codex hero stills + which
factory-footage keywords a span may draw from), targeting image:footage ~= 4:6 and
>= 1 distinct asset per 30s with no clip reused > 3x. The only things left for the
build step (once images + narration audio exist) are the real file names and the
audio-aligned exact timings.

Reads:  episodes/_planning/<EP>_<slug>_script.annotated.v001.json  (+ an inline
        per-episode footage keyword bank below)
Writes: episodes/_planning/<EP>_<slug>_shotlist.v001.json

Usage:  python scripts/build_planning_shotlist.py            # all 3 (EP28-30)
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

try:
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
PLAN = ROOT / "episodes" / "_planning"
TREATMENTS = ["bleed", "scan", "duotone", "focus"]   # MotionSample still techniques; ken_burns/wipe forbidden
SEC_PER_CUT = 2.8                                       # MotionSample fast pace (avg shot <= ~6s, aim ~2.5-3s)

# per-episode: chapter_id -> factory-footage search keyword bank (rights-cleared shelf),
# and the ai_prompts hero-still ID ranges that belong to each act (IMG-01..40).
EPISODES = {
    "EP28_forfeiture": {
        "slug": "forfeiture",
        "footage": {
            "hook": ["row house night", "police lights brick street", "sealed door notice"],
            "opening": ["front door threshold", "official seal paper"],
            "act1": ["philadelphia row houses", "family kitchen window night", "porch bike", "night street"],
            "act2": ["empty courtroom", "government hallway benches", "case files stack", "padlock door", "evidence room", "gavel shadow", "cash counted table"],
            "act3": ["case boxes wall", "city map markers", "lawyer office night", "ledger desk lamp", "seizure envelopes", "supreme court marble"],
            "act4": ["key in door dawn", "sunrise row houses", "porch light dusk", "settlement document pen", "quiet street golden hour"],
            "ending": ["sealed door removed", "family doorway warm", "street golden hour"],
        },
        "img_ranges": {"hook": (1, 4), "opening": (4, 5), "act1": (1, 10), "act2": (11, 21), "act3": (22, 31), "act4": (32, 40), "ending": (32, 40)},
    },
    "EP29_hinton": {
        "slug": "hinton",
        "footage": {
            "hook": ["death row cell door", "bullet macro", "prison bars"],
            "opening": ["barred window light"],
            "act1": ["closed restaurant night", "empty safe", "police cruiser fog", "warehouse night shift", "punch clock", "photo lineup"],
            "act2": ["revolver evidence bag", "comparison microscope", "empty courtroom", "jury box", "gavel shadow", "clock sweep"],
            "act3": ["death row corridor", "prison cell bunk", "tally marks wall", "prison library books", "barred window shaft light", "execution chamber door"],
            "act4": ["supreme court marble", "prison gate daylight", "sunrise horizon", "open field sky", "case file closing"],
            "ending": ["cold case files", "free man silhouette daylight"],
        },
        "img_ranges": {"hook": (1, 5), "opening": (21, 24), "act1": (1, 10), "act2": (11, 20), "act3": (21, 31), "act4": (32, 40), "ending": (32, 40)},
    },
    "EP30_cotton": {
        "slug": "cotton",
        "footage": {
            "hook": ["police lineup silhouettes", "eyes macro", "two hands reaching"],
            "opening": ["single eye lineup"],
            "act1": ["dark apartment window night", "sketch artist pencil", "photo lineup array", "physical lineup room", "detective desk night"],
            "act2": ["witness stand light", "jury box", "prison cell door", "two similar silhouettes", "prison corridor"],
            "act3": ["forensic lab", "dna autoradiograph lightbox", "double helix macro", "prison cell tally", "prison gate daylight"],
            "act4": ["church office two chairs", "two hands table warm", "two microphones stage", "lab building golden hour", "two shadows walking"],
            "ending": ["eyes lineup callback", "two shadows warm path"],
        },
        "img_ranges": {"hook": (1, 5), "opening": (1, 5), "act1": (1, 10), "act2": (11, 20), "act3": (21, 31), "act4": (32, 40), "ending": (32, 40)},
    },
}


def word_count(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9']+", text))


def build(ep_key: str) -> Path:
    cfg = EPISODES[ep_key]
    slug = cfg["slug"]
    ann_path = PLAN / f"{ep_key}_script.annotated.v001.json"
    ann = json.loads(ann_path.read_text(encoding="utf-8"))
    spans = ann["spans"]
    span_chapter = {sid: c["chapter_id"] for c in ann["chapters"] for sid in c["span_ids"]}
    est_total = float(ann.get("estimated_duration_seconds") or 705)

    total_words = sum(word_count(s["text"]) for s in spans) or 1
    # distribute est_total across spans proportional to spoken words
    shots = []
    img_counter = {}   # per-chapter rotating index into its IMG range
    for i, s in enumerate(spans):
        ch = span_chapter.get(s["span_id"], "act1")
        w = word_count(s["text"])
        secs = round(est_total * w / total_words, 1)
        cut_count = max(1, round(secs / SEC_PER_CUT))
        # cut-level treatment rotation (start offset by span index so neighbours differ)
        treats = [TREATMENTS[(i + k) % len(TREATMENTS)] for k in range(cut_count)]
        # asset pool: hero-still IDs for this act (rotating, no-repeat within span) + footage keywords
        lo, hi = cfg["img_ranges"].get(ch, (1, 40))
        pool = list(range(lo, hi + 1))
        start = img_counter.get(ch, 0)
        pick = [pool[(start + k) % len(pool)] for k in range(min(cut_count, len(pool)))]
        img_counter[ch] = (start + len(pick)) % len(pool)
        image_ids = [f"PD-2026-0{ep_key[2:4]}-IMG-{n:02d}" for n in pick]
        kw = cfg["footage"].get(ch, [])
        # image:footage ~ 4:6 -> ~40% of cuts are stills, rest footage
        n_still = max(1, round(cut_count * 0.4))
        shots.append({
            "span_id": s["span_id"],
            "chapter_id": ch,
            "narrative_function": s.get("narrative_function", ""),
            "estimated_seconds": secs,
            "cut_count": cut_count,
            "sec_per_cut": SEC_PER_CUT,
            "cut_plan": {
                "stills": n_still, "footage": cut_count - n_still,
                "treatments_rotation": treats,
                "transition": "crossfade_0.35s",
                "no_naked_hardcut": True,
            },
            "hero_still_ids": image_ids,
            "footage_search_keywords": kw,
            "on_screen_text": s.get("on_screen_text", []),
            "graphics_note": "on_screen_text = large kinetic typography (spring+scale, motion-blur), upper 1/5, separate layer from bottom captions.",
            "motion": "motionsample (2.5-3s cuts, bleed/scan/duotone/focus rotation; NO ken_burns, NO wipe, NO yellow wash)",
            "rights_note": "Hero stills = Codex (no real-person likeness, inv.11, always animate). Footage = rights-cleared factory shelf. Darken + navy + vignette; drop featureless clips.",
            "visual_intent": s.get("visual_intent", ""),
        })

    cut_total = sum(sh["cut_count"] for sh in shots)
    distinct_target = int(est_total // 30)
    totals = {
        "span_count": len(shots),
        "cut_count": cut_total,
        "estimated_total_seconds": round(sum(sh["estimated_seconds"] for sh in shots), 1),
        "avg_cut_seconds": round(est_total / cut_total, 2) if cut_total else None,
        "image_footage_ratio_target": "≈4:6",
        "distinct_asset_target": f">= {distinct_target} (runtime/30)",
        "max_reuse_per_clip": 3,
        "hero_stills_available": 40,
    }
    out = {
        "schema_version": "1.0.0-motionsample",
        "episode_id": ann["episode_id"],
        "revision": "v001",
        "generated_from": f"{ep_key}_script.annotated.v001.json",
        "source_annotated_sha256": hashlib.sha256(ann_path.read_bytes()).hexdigest(),
        "note": "PLAN only. Build step (build_case_film assets) resolves real image filenames + audio-aligned per-cut start/dur into remotion/src/data/%s_film.json. avg_cut<=~6s and freeze/animation_density gates apply at acceptance." % slug,
        "shots": shots,
        "totals": totals,
    }
    out_path = PLAN / f"{ep_key}_shotlist.v001.json"
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{ep_key}: {out_path.name}  spans={totals['span_count']} cuts={totals['cut_count']} "
          f"avg_cut={totals['avg_cut_seconds']}s est_total={totals['estimated_total_seconds']}s "
          f"distinct_target={totals['distinct_asset_target']}")
    return out_path


def main() -> int:
    for ep in EPISODES:
        build(ep)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
