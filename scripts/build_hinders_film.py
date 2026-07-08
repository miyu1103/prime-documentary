#!/usr/bin/env python3
r"""Assemble the EP35 (hinders) CaseFilm FilmData from the scene plan.

$0 assembly wiring. Emits remotion/src/data/hinders_film.json (consumed by the
CaseFilm composition registered as "Ep35Hinders"). Wires the REAL assets:
  - figures: one {kind:'hinders', fid, lane} beat per scene (+ secondary beats),
    resolved by FigureBeats' FIGURE_REGISTRY (all 27 figures + 3 hero mp4s).
  - cuts:    the existing S001-S068 stills, treatment per scene plan.
  - captions: verbatim [VO:] text per scene.

TIMING: narration is the audio thread's lane. Until narration_index.v001.json
carries per-chunk durations, this uses PLACEHOLDER timing derived from the
script's act minute-anchors, so the film is PREVIEWABLE now. Re-run after the
audio lands (narration_index with durations) to stamp exact seconds. The
placeholder is clearly flagged in the output (`timing: "placeholder_anchors"`).
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-035-hinders"
SCENE_PLAN = ROOT / "episodes" / EP / "04_scenes" / "scene_plan.v001.json"
NARR_INDEX = ROOT / "episodes" / EP / "06_audio" / "narration_index.v001.json"
IMG_DIR = ROOT / "remotion" / "public" / "hinders" / "img"
OUT = ROOT / "remotion" / "src" / "data" / "hinders_film.json"

FILM_END_SEC = 1224.0  # 20:24 (script ED end); band 1170-1230
OP_SEC = 12.0          # 0:07-0:19 title (CaseFilm OPENING_SEC)
HOOK_END = 7.0         # 0:07

# Lane per scene (Iowa=Carole/diner warm amber · Federal=law/govt cool steel ·
# NC=McLellan cool green) — keeps the 3 lanes separated (manifest §6).
LANE = {
    "S001": "federal", "S003": "iowa", "S004": "federal", "S005": "federal",
    "S006": "federal", "S007": "federal", "S008": "iowa", "S009": "iowa",
    "S010": "iowa", "S011": "federal", "S012": "federal", "S013": "federal",
    "S014": "federal", "S015": "iowa", "S016": "federal", "S017": "federal",
    "S018": "federal", "S019": "federal", "S020": "federal", "S021": "nc",
    "S022": "nc", "S023": "nc", "S024": "federal", "S025": "iowa",
    "S026": "nc", "S027": "federal", "S028": "federal", "S029": "iowa", "S030": "federal",
}


def anchor_sec(a: str) -> float:
    m, s = a.split(":")
    return int(m) * 60 + int(s)


def available_images() -> list[str]:
    imgs = sorted(p.name for p in IMG_DIR.glob("*.png") if not p.name.endswith("_depth.png"))
    return [f"hinders/img/{n}" for n in imgs]


def narration_has_durations() -> bool:
    if not NARR_INDEX.exists():
        return False
    try:
        d = json.loads(NARR_INDEX.read_text(encoding="utf-8"))
    except Exception:
        return False
    ch = d.get("chunks") or []
    return bool(ch) and any(float(c.get("estimated_duration_seconds") or c.get("seconds") or 0) > 0 for c in ch)


def main() -> int:
    plan = json.loads(SCENE_PLAN.read_text(encoding="utf-8"))
    scenes = plan["scenes"]
    imgs = available_images()
    if not imgs:
        print("no images in", IMG_DIR)
        return 1

    # ---- placeholder timing from anchors (audio not ready) ----
    body_scenes = [s for s in scenes if s["act"] not in ("HOOK", "OP")]
    body_start = anchor_sec(body_scenes[0]["script_anchor"])  # 0:19
    # per-scene [start,end] within the BODY timeline (rebased to 0 at body start)
    spans: dict[str, tuple[float, float]] = {}
    for i, s in enumerate(body_scenes):
        a = anchor_sec(s["script_anchor"]) - body_start
        nxt = (anchor_sec(body_scenes[i + 1]["script_anchor"]) - body_start) if i + 1 < len(body_scenes) else (FILM_END_SEC - body_start)
        spans[s["scene_id"]] = (round(a, 2), round(nxt, 2))
    narration_seconds = round(FILM_END_SEC - body_start, 2)

    cuts, figures, captions = [], [], []
    img_i = 0
    for s in body_scenes:
        sid = s["scene_id"]
        st, en = spans[sid]
        lane = LANE.get(sid, "federal")
        # one image cut spanning the scene (real still, treatment from plan)
        src = imgs[img_i % len(imgs)]
        img_i += 1
        cuts.append({"start": st, "dur": round(en - st, 2), "kind": "img", "src": src,
                     "treatment": s["treatment"], "seed": f"{sid}-cut"})
        # primary figure beat (overlays the cut)
        if s["figure"]:
            figures.append({"start": st, "end": en, "kind": "hinders", "fid": s["figure"], "lane": lane})
        # secondary figure beats (offset into the scene so they don't fully overlap)
        for k, fid in enumerate(s.get("secondary_figures", []), 1):
            mid = round(st + (en - st) * 0.5, 2)
            figures.append({"start": mid, "end": en, "kind": "hinders", "fid": fid, "lane": lane})
        # caption (verbatim; re-timed to the master when audio lands)
        if s["caption_verbatim"]:
            captions.append({"start": st, "end": en, "text": s["caption_verbatim"]})

    hook_scene = next(s for s in scenes if s["act"] == "HOOK")
    hook_cuts = []
    for j in range(4):
        hook_cuts.append({"start": round(j * (HOOK_END / 4), 2), "dur": round(HOOK_END / 4, 2),
                          "kind": "img", "src": imgs[j % len(imgs)], "seed": f"hook-{j}"})

    film = {
        "episode_id": EP,
        "fps": 30,
        # This scaffold ALWAYS uses anchor-derived placeholder timing. Consuming the audio thread's
        # per-chunk durations (token-matching 170 chunks -> 30 scenes) is the film builder's next step,
        # done once real narration exists. narration_index_ready flags when that data has landed.
        "timing": "placeholder_anchors",
        "narration_index_ready": narration_has_durations(),
        "narration": "hinders/audio/hinders_final_mix.v001.wav",
        "narrationSeconds": narration_seconds,
        "hookSeconds": HOOK_END,
        "hookLine": hook_scene["caption_verbatim"].split(" — ")[0] if hook_scene["caption_verbatim"] else "",
        "hook": hook_cuts,
        "cuts": cuts,
        "captions": captions,
        "graphics": [],  # motion-graphics text layer (required by FilmData); captions carry the text
        "figures": figures,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(film, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}")
    print(f"timing={film['timing']} narrationSeconds={narration_seconds} images_available={len(imgs)}")
    print(f"cuts={len(cuts)} figures={len(figures)} captions={len(captions)}")
    fids = sorted({f['fid'] for f in figures}, key=lambda x: (len(x), x))
    print(f"figure ids wired ({len(fids)}): {fids}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
