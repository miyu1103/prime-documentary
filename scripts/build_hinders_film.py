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
import re
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


OPENING_SEC = 3.5  # Bookends.tsx OPENING_SEC (CaseFilm lead = hookSeconds + OPENING_SEC)


def _norm(t: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", t.lower())).strip()


def map_chunks_to_scenes(body_chunks: list[dict], body_scenes: list[dict]) -> dict[str, list[dict]]:
    """Assign each narration chunk to the scene whose verbatim caption contains it
    (text match on a normalized prefix); unmatched chunks inherit the previous
    chunk's scene so the timeline stays contiguous."""
    norm_caps = {s["scene_id"]: _norm(s["caption_verbatim"]) for s in body_scenes}
    order = [s["scene_id"] for s in body_scenes]
    out: dict[str, list[dict]] = {sid: [] for sid in order}
    last = order[0]
    search_from = 0  # scenes are in narration order; only look forward
    for c in body_chunks:
        key = " ".join(_norm(c["text"]).split()[:7])
        hit = None
        for j in range(search_from, len(order)):
            if key and key in norm_caps[order[j]]:
                hit = order[j]
                search_from = j
                break
        if hit is None:
            hit = last
        out[hit].append(c)
        last = hit
    return out


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

    body_scenes = [s for s in scenes if s["act"] not in ("HOOK", "OP")]
    hook_scene = next(s for s in scenes if s["act"] == "HOOK")
    real = narration_has_durations()

    # ---- per-scene BODY-relative [start,end] + captions ----
    spans: dict[str, tuple[float, float]] = {}
    captions: list[dict] = []
    if real:
        # REAL timing from narration_index (authoritative master timeline: chunk start/end).
        narr = json.loads(NARR_INDEX.read_text(encoding="utf-8"))
        chunks = narr["chunks"]
        hook_chunks = [c for c in chunks if c["section"] == "COLD_OPEN_THREAT"]
        body_chunks = [c for c in chunks if c["section"] != "COLD_OPEN_THREAT"]
        abs_body = float(body_chunks[0]["start"])  # body starts here on the master timeline
        # CaseFilm lead = hookSeconds + OPENING_SEC must equal abs_body so body aligns to the master.
        hook_seconds = round(abs_body - OPENING_SEC, 2)
        narration_seconds = round(float(body_chunks[-1]["end"]) - abs_body, 2)
        mapping = map_chunks_to_scenes(body_chunks, body_scenes)
        prev_end = 0.0
        for s in body_scenes:
            cs = mapping[s["scene_id"]]
            if cs:
                st = round(float(cs[0]["start"]) - abs_body, 2)
                en = round(float(cs[-1]["end"]) - abs_body, 2)
            else:
                st = en = prev_end  # unmatched scene -> zero-length at the seam (no black gap)
            spans[s["scene_id"]] = (st, en)
            prev_end = max(prev_end, en)
        # captions straight from the body chunks -> caption == narration (the #1-failure guard)
        for c in body_chunks:
            captions.append({"start": round(float(c["start"]) - abs_body, 2),
                             "end": round(float(c["end"]) - abs_body, 2), "text": c["text"]})
        hook_line = hook_chunks[0]["text"] if hook_chunks else ""
        timing_label = "narration_index"
    else:
        # placeholder anchors (audio not ready)
        body_start = anchor_sec(body_scenes[0]["script_anchor"])
        for i, s in enumerate(body_scenes):
            a = anchor_sec(s["script_anchor"]) - body_start
            nxt = (anchor_sec(body_scenes[i + 1]["script_anchor"]) - body_start) if i + 1 < len(body_scenes) else (FILM_END_SEC - body_start)
            spans[s["scene_id"]] = (round(a, 2), round(nxt, 2))
            if s["caption_verbatim"]:
                captions.append({"start": round(a, 2), "end": round(nxt, 2), "text": s["caption_verbatim"]})
        narration_seconds = round(FILM_END_SEC - body_start, 2)
        hook_seconds = HOOK_END
        hook_line = hook_scene["caption_verbatim"].split(" — ")[0] if hook_scene["caption_verbatim"] else ""
        timing_label = "placeholder_anchors"

    # ---- cuts (CONTIGUOUS tiling so there is never a black gap) + figures ----
    order = sorted(body_scenes, key=lambda s: spans[s["scene_id"]][0])
    cuts, figures = [], []
    img_i = 0
    for idx, s in enumerate(order):
        sid = s["scene_id"]
        st, _ = spans[sid]
        nxt = spans[order[idx + 1]["scene_id"]][0] if idx + 1 < len(order) else narration_seconds
        dur = round(max(0.0, nxt - st), 2)
        lane = LANE.get(sid, "federal")
        src = imgs[img_i % len(imgs)]
        img_i += 1
        if dur > 0:
            cuts.append({"start": st, "dur": dur, "kind": "img", "src": src,
                         "treatment": s["treatment"], "seed": f"{sid}-cut"})
        sc_end = spans[sid][1] if spans[sid][1] > st else nxt
        if s["figure"]:
            figures.append({"start": st, "end": max(sc_end, st + 0.5), "kind": "hinders", "fid": s["figure"], "lane": lane})
        for fid in s.get("secondary_figures", []):
            mid = round(st + (sc_end - st) * 0.5, 2)
            figures.append({"start": mid, "end": max(sc_end, mid + 0.5), "kind": "hinders", "fid": fid, "lane": lane})

    hook_cuts = [{"start": round(j * (hook_seconds / 4), 2), "dur": round(hook_seconds / 4, 2),
                  "kind": "img", "src": imgs[j % len(imgs)], "seed": f"hook-{j}"} for j in range(4)]

    film = {
        "episode_id": EP,
        "fps": 30,
        "timing": timing_label,
        "narration_index_ready": real,
        "narration": "hinders/audio/hinders_final_mix.v001.wav",
        "narrationSeconds": narration_seconds,
        "hookSeconds": hook_seconds,
        "hookLine": hook_line,
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
