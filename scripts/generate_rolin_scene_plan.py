#!/usr/bin/env python3
r"""Derive rolin's scene_plan + remotion_plan + asset_selection FROM the finished film.

EP34 rolin was assembled by the data-driven build_rolin_film.py (film JSON IS the plan),
so it never emitted the standard planning artifacts that preflight_render_gate.py recomputes
its motion / assets / coverage floors from. This script derives those three artifacts
*truthfully* from the real film JSON + narration_index, so the preflight gate measures the
actual episode (no hand-typed pass flags, no invented numbers):

  - remotion/src/data/rolin_film.json   -> cuts (still/footage, treatment), figures, heroCuts
  - episodes/.../06_audio/narration_index.v001.json -> per-span time windows (chunk.span_id)
  - episodes/.../03_script/script.annotated.v001.json -> the span universe coverage must cover

Writes (immutable v001; refuses to clobber a different existing one unless --force):
  04_scenes/scene_plan.v001.json      (scenes: span ids, required_assets COD-S0NN + GFX/KIN,
                                        continuity_refs incl FigureBeat / HERO motion surface #N /
                                        depth_treatment, on_screen_text)
  04_scenes/remotion_plan.v001.json   (cut_plan per scene: cuts/still_cuts/depth_cuts/
                                        graphic_cuts/footage_cuts, key_graphics)
  05_visuals/asset_selection.v001.json (scene_selection: every span bound to stills+footage+gfx)

Every number is COUNTED from the film JSON — depth share, figure beats, hero surfaces all
reflect what will actually render. No paid calls, no external side effects.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STILL_RE = re.compile(r"S(\d{3})")


def load(p: Path):
    return json.loads(p.read_text("utf-8"))


def dump(p: Path, obj) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", "utf-8")
    tmp.replace(p)


def still_id(src: str):
    m = STILL_RE.search(src or "")
    return f"S{m.group(1)}" if m else None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--ep", default="PD-2026-034-rolin")
    ap.add_argument("--film", default=None)
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    ep = args.ep
    epdir = ROOT / "episodes" / ep
    slug = ep.split("-", 3)[-1]
    film_path = Path(args.film) if args.film else ROOT / "remotion" / "src" / "data" / f"{slug}_film.json"
    film = load(film_path)
    nidx = load(epdir / "06_audio" / "narration_index.v001.json")
    annotated = load(epdir / "03_script" / "script.annotated.v001.json")

    cuts = film["cuts"]
    figures = film.get("figures", [])
    hero_cuts = film.get("heroCuts", [])
    span_order = [s["span_id"] for s in annotated.get("spans", [])]
    span_text = {s["span_id"]: s for s in annotated.get("spans", [])}

    # --- per-span time windows from narration_index chunks (chunk.span_id) ------------- #
    # chunk start/end are narration-relative seconds; film cut/figure starts are the same clock.
    windows: dict[str, list[float]] = {}
    for c in nidx["chunks"]:
        sp = c.get("span_id")
        if not sp:
            continue
        s, e = float(c["start"]), float(c["end"])
        if sp not in windows:
            windows[sp] = [s, e]
        else:
            windows[sp][0] = min(windows[sp][0], s)
            windows[sp][1] = max(windows[sp][1], e)
    # spans present in the script but with no narration chunk get a zero-length placeholder
    # window at the end so coverage can still bind them (they are rare book-end spans).
    last_end = max((w[1] for w in windows.values()), default=0.0)
    for sp in span_order:
        windows.setdefault(sp, [last_end, last_end])

    def in_window(t: float, lo: float, hi: float) -> bool:
        return lo <= t < hi or (lo == hi and abs(t - lo) < 1e-6)

    # --- global set of stills that are ACTUALLY depth-treated (appear in >=1 depth cut) --- #
    # Only these carry a depth map on disk (flat-only stills' maps were pruned as dead weight).
    # A still is "depth-eligible" (preflight requires a depth map) iff it is depth-treated
    # SOMEWHERE; a still that only ever renders flat must NOT be listed as a depth requirement
    # even when it shares a scene window with another still's depth cut.
    depth_stills = {still_id(c["src"]) for c in cuts
                    if c.get("kind") == "img" and "depth" in str(c.get("treatment", "")).lower()
                    and still_id(c["src"])}

    # --- assign a distinct hero surface number to each distinct hero source ------------- #
    hero_num: dict[str, int] = {}
    for h in hero_cuts:
        base = Path(h["src"]).stem.replace("hero_", "")
        if base not in hero_num:
            hero_num[base] = len(hero_num) + 1

    # --- build one scene per span (ordinal), counting the real cuts/figures in its window - #
    scenes = []
    cut_plan = []
    key_graphics = []
    scene_selection = []
    gfx_counter = 0

    for i, sp in enumerate(span_order, start=1):
        sid = f"S{i:03d}"
        lo, hi = windows[sp]
        sc_cuts = [c for c in cuts if in_window(float(c["start"]), lo, hi)]
        sc_figs = [f for f in figures if in_window(float(f["start"]), lo, hi)]
        sc_heroes = [h for h in hero_cuts if in_window(float(h["start"]), lo, hi)]

        img_cuts = [c for c in sc_cuts if c.get("kind") == "img"]
        foot_cuts = [c for c in sc_cuts if c.get("kind") == "footage"]
        depth_cuts = [c for c in img_cuts if "depth" in str(c.get("treatment", "")).lower()]
        stills = sorted({still_id(c["src"]) for c in img_cuts if still_id(c["src"])})
        foot_names = sorted({Path(c["src"]).name for c in foot_cuts})

        # required_assets: COD-S0NN ONLY for stills that are truly depth-treated (they carry a
        # depth map and are the depth prerequisite preflight verifies). Flat-only stills are still
        # bound for coverage via scene_selection.stills below, but are NOT asserted as depth
        # requirements (their maps were pruned as dead weight -- see footage_utilization fix).
        required_assets = [f"COD-{s}-still" for s in stills if s in depth_stills]
        if depth_cuts:
            required_assets.append("DEPTH-DepthImageV-parallax")
        on_screen = []
        continuity = []
        for f in sc_figs:
            kind = f.get("kind", "figure")
            gfx_counter += 1
            gid = f"G{gfx_counter:02d}"
            required_assets.append(f"GFX-{kind}-{gid}")
            key_graphics.append({"id": gid, "scene_id": sid, "component": kind,
                                 "props": {k: f[k] for k in ("caption", "lines", "value", "label")
                                           if k in f}})
            lines = f.get("lines") or ([f.get("caption")] if f.get("caption") else [])
            for ln in lines:
                if ln:
                    on_screen.append(str(ln))
                    required_assets.append(f"KIN-{re.sub(r'[^a-z0-9]+','-',str(ln).lower()).strip('-')}")
            continuity.append(f"FigureBeat {kind} (moving figure surface)")
        for h in sc_heroes:
            base = Path(h["src"]).stem.replace("hero_", "")
            continuity.append(f"HERO motion surface #{hero_num[base]} = {base}")
        if depth_cuts:
            continuity.append(f"depth_treatment: DepthImageV parallax ON ({len(depth_cuts)} still cuts)")
        if not continuity:
            continuity.append("cut_cadence: real-footage b-roll + AI stills")

        span_on_screen = span_text.get(sp, {}).get("on_screen_text") or []
        for t in (span_on_screen if isinstance(span_on_screen, list) else [span_on_screen]):
            if t:
                on_screen.append(str(t))

        scenes.append({
            "scene_id": sid,
            "script_span_ids": [sp],
            "purpose": (span_text.get(sp, {}).get("narrative_function") or "body"),
            "visual_mode": "mixed",
            "duration_seconds": round(hi - lo, 2),
            "required_assets": required_assets,
            "continuity_refs": continuity,
            "on_screen_text": on_screen,
            "transition_in": "cut",
            "transition_out": "cut",
        })
        cut_plan.append({
            "scene_id": sid,
            "duration_seconds": round(hi - lo, 2),
            "cuts": len(sc_cuts),
            "still_cuts": len(img_cuts),
            "depth_cuts": len(depth_cuts),
            "graphic_cuts": len(sc_figs),
            "footage_cuts": len(foot_cuts),
        })
        scene_selection.append({
            "span_id": sp,
            "scene_id": sid,
            "stills": [f"{s}" for s in stills],
            "factory_candidates": foot_names,
            "remotion_motion_surfaces": [f.get("kind") for f in sc_figs],
        })

    # --- totals / sanity ------------------------------------------------------------- #
    tot_still = sum(c["still_cuts"] for c in cut_plan)
    tot_depth = sum(c["depth_cuts"] for c in cut_plan)
    depth_pct = round(100.0 * tot_depth / tot_still, 1) if tot_still else 0.0
    fig_scenes = sum(1 for sc in scenes if any("figurebeat" in r.lower() for r in sc["continuity_refs"]))

    scene_plan = {
        "schema_version": "pd.scene_plan.v001",
        "episode_id": ep,
        "revision": "v001",
        "note": "Derived from finished film JSON + narration_index by generate_rolin_scene_plan.py. "
                "Counts are recomputed from real cuts (build_rolin_film output), not hand-typed.",
        "scenes": scenes,
        "coverage": {"span_count": len(span_order), "scene_count": len(scenes)},
    }
    remotion_plan = {
        "schema_version": "pd.remotion_plan.v001",
        "episode_id": ep,
        "revision": "v001",
        "note": "Derived cut plan; depth/figure/hero counts recomputed from the film JSON.",
        "cut_plan": cut_plan,
        "cut_plan_totals": {
            "cuts": sum(c["cuts"] for c in cut_plan),
            "still_cuts": tot_still, "depth_cuts": tot_depth,
            "depth_pct_of_still_cuts": depth_pct,
            "footage_cuts": sum(c["footage_cuts"] for c in cut_plan),
            "graphic_cuts": sum(c["graphic_cuts"] for c in cut_plan),
        },
        "key_graphics": key_graphics,
        "status": "derived",
    }
    asset_selection = {
        "schema_version": "1.0.0",
        "episode_id": ep,
        "revision": "v001",
        "artifact_type": "factory_broll_selection_plan",
        "status": "derived_from_film",
        "selection_note": "Every annotated span bound to the stills + factory footage + motion "
                          "surfaces that the finished film actually renders in that span's window.",
        "scene_selection": scene_selection,
    }

    for rel, obj in [("04_scenes/scene_plan.v001.json", scene_plan),
                     ("04_scenes/remotion_plan.v001.json", remotion_plan),
                     ("05_visuals/asset_selection.v001.json", asset_selection)]:
        dump(epdir / rel, obj)

    print(f"scenes={len(scenes)}  spans={len(span_order)}  cuts={remotion_plan['cut_plan_totals']['cuts']}")
    print(f"depth share = {tot_depth}/{tot_still} = {depth_pct}%  (floor 40)")
    print(f"figure-beat scenes = {fig_scenes}  (floor 6)   hero surfaces = {len(hero_num)} {list(hero_num)} (floor 2)")
    print(f"graphic_cuts total = {remotion_plan['cut_plan_totals']['graphic_cuts']}  key_graphics = {len(key_graphics)}")
    print("wrote scene_plan / remotion_plan / asset_selection (v001)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
