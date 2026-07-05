#!/usr/bin/env python3
"""Pre-render preflight gate for Prime Documentary episodes.

Purpose (EP32 DESIGN_REMEDIATION defects B3, M5, M10, M6):
    Heavy renders were starting before their prerequisites existed, and the
    perceptual-motion budget was hand-typed JSON that NO code validated. The
    "pass": true flags in remotion_plan / scene_plan are decoration -- this gate
    RECOMPUTES the numbers from the underlying cut_plan / scene continuity data
    and cross-checks the assets that must physically exist on disk before a
    single frame is rendered.

    It HARD-FAILS (exit non-zero) so the render step can be made to require a
    green preflight receipt, exactly like the ship gate requires a green
    acceptance receipt after render.

What it checks (all thresholds are constants at the top of this file):

  CHECK 1 -- MOTION BUDGET (defect B3)
    Recomputed from remotion_plan cut_plan + scene_plan continuity_refs
    (and <slug>_film.json if one exists). The hand-typed motion_budget block
    is IGNORED for the verdict; it is only echoed for comparison.
      * depth-treated share of still cuts  >= DEPTH_FLOOR_PCT  (40%)
      * moving FigureBeats                 >= FIGURE_BEAT_FLOOR (6)
      * hero motion surfaces               >= HERO_SURFACE_FLOOR (2)
      * every graphic-dominated scene's claimed graphic_cuts is backed by
        enough DISTINCT graphics (>= ceil(graphic_cuts / CUTS_PER_GRAPHIC_MAX))

  CHECK 2 -- ASSETS EXIST (defects M5, M10)
      * every S0NN still referenced by the annotated script / scene_plan has a
        file on disk,
      * each still's long edge is >= MIN_LONG_EDGE_PX (3840, i.e. 4K),
      * every still that belongs to a scene with depth_cuts > 0 has a matching
        depth map "<stem>_depth.png",
      * ZERO staged stills => FAIL (never pass on absence).

  CHECK 3 -- COVERAGE (defect M10)
      * asset_selection binds a still / graphic / footage for every script span
        (no span left with no visual).

  CHECK 4 -- FILM CROSS-CHECK (defect M6, informational unless present)
      * if a <slug>_film.json render input exists, its actual cut list is
        compared against the plan totals (cut count, still/footage kinds,
        depth-treated share). Absence is reported (you cannot render without it)
        but is not by itself the reason for the exit code.

Output:
    Emits an immutable preflight receipt at
    episodes/<ep>/04_scenes/preflight_receipt.v{NNN}.json
    recording every check, pass/fail, and the recomputed budget numbers.

Usage:
    ./.venv/Scripts/python.exe scripts/preflight_render_gate.py --ep PD-2026-032-carsearch

Exit code:
    0  -> all hard checks passed (render may proceed)
    1  -> at least one hard check failed (render is blocked)
    2  -> the gate could not run (bad arguments / episode folder missing)

Side effects:
    Writes one receipt JSON (atomic temp+rename). No paid API, no git, no GPU,
    no render, no network. Read-only against every input.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import struct
import sys
from datetime import datetime, timezone
from pathlib import Path

# --------------------------------------------------------------------------- #
# Thresholds (single source of truth; mirror EP32 DESIGN sec3/sec5).
# --------------------------------------------------------------------------- #
DEPTH_FLOOR_PCT = 40.0        # depth-treated share of still cuts must be >= this
FIGURE_BEAT_FLOOR = 6         # moving FigureBeats
HERO_SURFACE_FLOOR = 2        # hero motion surfaces
MIN_LONG_EDGE_PX = 3840       # 4K long edge for every AI still
CUTS_PER_GRAPHIC_MAX = 4      # one distinct graphic may legitimately back <= this many cuts

# Regexes for still references. Stills live in the COD-S0NN namespace and their
# files are named PD-YYYY-NNN-S0NN-IMG-*.png. Scene IDs are ALSO S0NN but they
# are read from a structured field, never scraped from prose, so there is no
# namespace collision here.
RE_COD_TOKEN = re.compile(r"COD-(S\d{3})")            # scene_plan required_assets
RE_BARE_STILL = re.compile(r"\bS(\d{3})\b")            # annotated visual_intent prose
RE_GFX_TOKEN = re.compile(r"\bGFX-[A-Za-z0-9\-]+")     # graphic assets in required_assets


# --------------------------------------------------------------------------- #
# Small helpers
# --------------------------------------------------------------------------- #
class GateError(Exception):
    """Fatal: the gate itself cannot run (exit 2)."""


def load_json(path: Path):
    """Return (data, error). error is a human string when the file is missing
    or unparseable; data is None in that case. Never raises for missing input --
    reporting exactly what is missing IS the point of a preflight."""
    if not path.exists():
        return None, f"missing file: {path}"
    try:
        with path.open("r", encoding="utf-8") as fh:
            return json.load(fh), None
    except (json.JSONDecodeError, OSError) as exc:
        return None, f"unreadable ({type(exc).__name__}): {path} -> {exc}"


def png_long_edge(path: Path):
    """Return (long_edge_px, error). Reads the PNG IHDR directly (no PIL needed).
    Returns (None, reason) if the file is not a readable PNG."""
    try:
        with path.open("rb") as fh:
            head = fh.read(26)
    except OSError as exc:
        return None, f"cannot open ({exc})"
    if len(head) < 24 or head[:8] != b"\x89PNG\r\n\x1a\n":
        return None, "not a PNG (bad signature)"
    if head[12:16] != b"IHDR":
        return None, "no IHDR chunk"
    width, height = struct.unpack(">II", head[16:24])
    return max(width, height), None


def check_result(name, status, detail, **extra):
    """Uniform check record. status in {"PASS","FAIL","WARN","SKIP"}."""
    rec = {"check": name, "status": status, "detail": detail}
    rec.update(extra)
    return rec


# --------------------------------------------------------------------------- #
# CHECK 1 -- Motion budget (recomputed, hand-typed flags ignored)
# --------------------------------------------------------------------------- #
def check_motion_budget(remotion_plan, remotion_err, scene_plan, scene_err):
    subs = []
    numbers = {}

    if remotion_err:
        subs.append(check_result("motion.inputs", "FAIL", remotion_err))
    if scene_err:
        subs.append(check_result("motion.inputs", "FAIL", scene_err))
    if remotion_plan is None or scene_plan is None:
        return check_result(
            "motion_budget", "FAIL",
            "cannot recompute motion budget -- required plan file(s) missing",
            subchecks=subs, recomputed=numbers,
        )

    cut_plan = remotion_plan.get("cut_plan") or []
    if not cut_plan:
        subs.append(check_result("motion.cut_plan", "FAIL",
                                 "remotion_plan.cut_plan is empty/absent"))
        return check_result("motion_budget", "FAIL",
                            "no cut_plan to recompute from",
                            subchecks=subs, recomputed=numbers)

    # --- depth-treated share of still cuts ---------------------------------- #
    still_total = sum(int(c.get("still_cuts", 0)) for c in cut_plan)
    depth_total = sum(int(c.get("depth_cuts", 0)) for c in cut_plan)
    cut_total = sum(int(c.get("cuts", 0)) for c in cut_plan)
    depth_pct_of_stills = (100.0 * depth_total / still_total) if still_total else 0.0
    depth_pct_of_cuts = (100.0 * depth_total / cut_total) if cut_total else 0.0
    numbers["still_cuts"] = still_total
    numbers["depth_cuts"] = depth_total
    numbers["total_cuts"] = cut_total
    numbers["depth_pct_of_still_cuts"] = round(depth_pct_of_stills, 1)
    numbers["depth_pct_of_total_cuts"] = round(depth_pct_of_cuts, 1)
    depth_ok = depth_pct_of_stills >= DEPTH_FLOOR_PCT
    subs.append(check_result(
        "motion.depth_share", "PASS" if depth_ok else "FAIL",
        f"depth-treated={depth_total}/{still_total} still cuts = "
        f"{depth_pct_of_stills:.1f}% (floor {DEPTH_FLOOR_PCT:.0f}%)",
        value=round(depth_pct_of_stills, 1), floor=DEPTH_FLOOR_PCT))

    # --- moving FigureBeats (recomputed from scene continuity_refs) --------- #
    scenes = scene_plan.get("scenes") or []
    figure_scenes = []
    hero_numbers = {}
    for sc in scenes:
        sid = sc.get("scene_id")
        refs = " || ".join(str(r) for r in (sc.get("continuity_refs") or []))
        if "figurebeat" in refs.lower():
            figure_scenes.append(sid)
        for m in re.finditer(r"HERO motion surface\s*#?(\d+)", refs):
            hero_numbers[m.group(1)] = sid
    figure_count = len(figure_scenes)
    numbers["moving_figure_beats"] = figure_count
    numbers["moving_figure_beat_scenes"] = figure_scenes
    fig_ok = figure_count >= FIGURE_BEAT_FLOOR
    subs.append(check_result(
        "motion.figure_beats", "PASS" if fig_ok else "FAIL",
        f"{figure_count} moving FigureBeats recomputed from continuity_refs "
        f"(floor {FIGURE_BEAT_FLOOR}) scenes={figure_scenes}",
        value=figure_count, floor=FIGURE_BEAT_FLOOR))

    # --- hero motion surfaces ---------------------------------------------- #
    hero_count = len(hero_numbers)
    numbers["hero_motion_surfaces"] = hero_count
    numbers["hero_motion_surface_scenes"] = hero_numbers
    hero_ok = hero_count >= HERO_SURFACE_FLOOR
    subs.append(check_result(
        "motion.hero_surfaces", "PASS" if hero_ok else "FAIL",
        f"{hero_count} distinct hero motion surfaces recomputed "
        f"(floor {HERO_SURFACE_FLOOR}) scenes={hero_numbers}",
        value=hero_count, floor=HERO_SURFACE_FLOOR))

    # --- graphic-dominated scenes must be backed by distinct graphics ------ #
    key_graphics_by_scene = {}
    for g in (remotion_plan.get("key_graphics") or []):
        key_graphics_by_scene.setdefault(g.get("scene_id"), []).append(g)
    scene_by_id = {sc.get("scene_id"): sc for sc in scenes}

    unbacked = []
    graphic_scene_report = []
    for c in cut_plan:
        sid = c.get("scene_id")
        cuts = int(c.get("cuts", 0))
        graphic_cuts = int(c.get("graphic_cuts", 0))
        # "graphic-dominated" = graphics are at least half of the scene's cuts
        if cuts <= 0 or graphic_cuts * 2 < cuts:
            continue
        sc = scene_by_id.get(sid, {})
        required_assets = sc.get("required_assets") or []
        on_screen = sc.get("on_screen_text") or []
        # distinct graphic backing = distinct GFX-* assets + distinct on-screen
        # kinetic text lines + distinct key_graphics ids bound to this scene.
        backing = set()
        for a in required_assets:
            for gm in RE_GFX_TOKEN.findall(str(a)):
                backing.add(("gfx", gm.lower()))
        for t in on_screen:
            backing.add(("kin", str(t).strip().lower()))
        for g in key_graphics_by_scene.get(sid, []):
            backing.add(("key", str(g.get("id") or g.get("component")).lower()))
        distinct = len(backing)
        required = math.ceil(graphic_cuts / CUTS_PER_GRAPHIC_MAX)
        ok = distinct >= required
        graphic_scene_report.append({
            "scene_id": sid, "graphic_cuts": graphic_cuts,
            "distinct_graphics": distinct, "required": required, "ok": ok,
        })
        if not ok:
            unbacked.append(sid)
    numbers["graphic_dominated_scenes"] = graphic_scene_report
    back_ok = not unbacked
    subs.append(check_result(
        "motion.graphic_backing",
        "PASS" if back_ok else "FAIL",
        ("all graphic-dominated scenes backed by >= ceil(graphic_cuts/"
         f"{CUTS_PER_GRAPHIC_MAX}) distinct graphics"
         if back_ok else
         f"under-backed graphic scenes: {unbacked}"),
        unbacked_scenes=unbacked))

    all_ok = depth_ok and fig_ok and hero_ok and back_ok
    return check_result(
        "motion_budget", "PASS" if all_ok else "FAIL",
        "recomputed motion budget vs floors (hand-typed pass flags ignored)",
        subchecks=subs, recomputed=numbers)


# --------------------------------------------------------------------------- #
# Reference collection for stills
# --------------------------------------------------------------------------- #
def collect_referenced_stills(annotated, scene_plan):
    """Return dict still_id -> set(source tags) for every S0NN referenced by the
    annotated script visual_intent and the scene_plan required_assets."""
    refs = {}

    def add(sid, source):
        refs.setdefault(sid, set()).add(source)

    if annotated:
        for span in (annotated.get("spans") or []):
            vi = str(span.get("visual_intent", ""))
            for num in RE_BARE_STILL.findall(vi):
                add(f"S{num}", f"annotated:{span.get('span_id')}")

    if scene_plan:
        for sc in (scene_plan.get("scenes") or []):
            for a in (sc.get("required_assets") or []):
                for m in RE_COD_TOKEN.findall(str(a)):
                    add(m, f"scene_plan:{sc.get('scene_id')}")
    return refs


def depth_eligible_stills(scene_plan, remotion_plan):
    """Return the set of still IDs bound to scenes whose cut_plan depth_cuts > 0.
    Those stills must each carry a depth map before render."""
    if not scene_plan or not remotion_plan:
        return set()
    depth_scene_ids = {
        c.get("scene_id")
        for c in (remotion_plan.get("cut_plan") or [])
        if int(c.get("depth_cuts", 0)) > 0
    }
    eligible = set()
    for sc in (scene_plan.get("scenes") or []):
        if sc.get("scene_id") not in depth_scene_ids:
            continue
        for a in (sc.get("required_assets") or []):
            for m in RE_COD_TOKEN.findall(str(a)):
                eligible.add(m)
    return eligible


# --------------------------------------------------------------------------- #
# CHECK 2 -- Assets exist / resolution / depth maps
# --------------------------------------------------------------------------- #
def check_assets_exist(image_dir, annotated, scene_plan, remotion_plan):
    subs = []
    numbers = {}

    referenced = collect_referenced_stills(annotated, scene_plan)
    numbers["referenced_still_ids"] = sorted(referenced)
    numbers["referenced_still_count"] = len(referenced)

    if not image_dir.exists():
        subs.append(check_result("assets.image_dir", "FAIL",
                                 f"image dir missing: {image_dir}"))
        return check_result("assets_exist", "FAIL",
                            "image directory does not exist",
                            subchecks=subs, recomputed=numbers)

    staged = sorted(image_dir.glob("*.png"))
    staged = [p for p in staged if not p.stem.endswith("_depth")]
    numbers["staged_still_files"] = len(staged)

    # Zero staged stills => FAIL (never pass on absence).
    if not staged:
        subs.append(check_result("assets.staged", "FAIL",
                                 "zero staged stills on disk (never pass on absence)"))
        return check_result("assets_exist", "FAIL",
                            "no staged stills",
                            subchecks=subs, recomputed=numbers)

    # Index staged files by still id token (S0NN) found in the filename.
    by_still = {}
    for p in staged:
        m = RE_BARE_STILL.search(p.stem)
        if m:
            by_still.setdefault(f"S{m.group(1)}", []).append(p)

    if not referenced:
        subs.append(check_result(
            "assets.references", "FAIL",
            "no S0NN still references found in annotated/scene_plan "
            "(cannot verify prerequisites)"))

    missing_files = []
    under_res = []
    unreadable = []
    ok_files = 0
    for sid in sorted(referenced):
        files = by_still.get(sid)
        if not files:
            missing_files.append(sid)
            continue
        # Take the first matching file; verify its long edge.
        path = sorted(files)[0]
        long_edge, err = png_long_edge(path)
        if err:
            unreadable.append(f"{sid} ({path.name}): {err}")
            continue
        if long_edge < MIN_LONG_EDGE_PX:
            under_res.append(f"{sid} ({path.name}): {long_edge}px < {MIN_LONG_EDGE_PX}px")
            continue
        ok_files += 1
    numbers["stills_present_ok"] = ok_files
    numbers["stills_missing"] = missing_files
    numbers["stills_under_resolution"] = under_res
    numbers["stills_unreadable"] = unreadable

    exist_ok = referenced and not missing_files and not under_res and not unreadable
    subs.append(check_result(
        "assets.stills", "PASS" if exist_ok else "FAIL",
        f"{ok_files}/{len(referenced)} referenced stills present & >= "
        f"{MIN_LONG_EDGE_PX}px long edge; "
        f"missing={missing_files or 'none'}; "
        f"under_res={under_res or 'none'}; unreadable={unreadable or 'none'}"))

    # --- depth maps for depth-eligible stills ------------------------------ #
    eligible = depth_eligible_stills(scene_plan, remotion_plan)
    numbers["depth_eligible_still_count"] = len(eligible)
    missing_depth = []
    have_depth = 0
    for sid in sorted(eligible):
        files = by_still.get(sid)
        if not files:
            # Missing still already reported above; still owes a depth map.
            missing_depth.append(f"{sid} (still file absent)")
            continue
        stem = sorted(files)[0]
        depth_path = stem.with_name(stem.stem + "_depth.png")
        if depth_path.exists():
            have_depth += 1
        else:
            missing_depth.append(f"{sid} ({depth_path.name})")
    numbers["depth_maps_present"] = have_depth
    numbers["depth_maps_missing"] = missing_depth
    depth_ok = (not eligible) or (not missing_depth)
    subs.append(check_result(
        "assets.depth_maps", "PASS" if depth_ok else "FAIL",
        f"{have_depth}/{len(eligible)} depth maps present for depth-eligible "
        f"stills; missing={len(missing_depth)}"))

    all_ok = exist_ok and depth_ok
    return check_result(
        "assets_exist", "PASS" if all_ok else "FAIL",
        "referenced stills exist at 4K with depth maps for depth-treated scenes",
        subchecks=subs, recomputed=numbers)


# --------------------------------------------------------------------------- #
# CHECK 3 -- Coverage: every span bound to a visual
# --------------------------------------------------------------------------- #
def check_coverage(asset_selection, asset_err, annotated, scene_plan):
    numbers = {}

    # Expected span universe (prefer annotated, fall back to scene_plan).
    expected = []
    if annotated:
        expected = [s.get("span_id") for s in (annotated.get("spans") or [])]
    if not expected and scene_plan:
        seen = []
        for sc in (scene_plan.get("scenes") or []):
            for sp in (sc.get("script_span_ids") or []):
                if sp not in seen:
                    seen.append(sp)
        expected = seen
    numbers["expected_span_count"] = len(expected)

    if asset_err or asset_selection is None:
        return check_result("coverage", "FAIL",
                            asset_err or "asset_selection missing",
                            recomputed=numbers)

    selections = asset_selection.get("scene_selection") or []
    bound = {}
    for entry in selections:
        sid = entry.get("span_id")
        has_footage = bool(entry.get("factory_candidates"))
        has_graphic = bool(entry.get("remotion_motion_surfaces"))
        has_still = bool(entry.get("stills") or entry.get("ai_stills"))
        bound[sid] = has_footage or has_graphic or has_still
    numbers["spans_in_asset_selection"] = len(selections)

    unbound = [sp for sp in expected if not bound.get(sp)]
    # Spans present in the selection but flagged with no visual at all:
    empty = [sid for sid, ok in bound.items() if not ok]
    numbers["unbound_or_missing_spans"] = unbound
    numbers["bound_span_count"] = sum(1 for sp in expected if bound.get(sp))

    ok = expected and not unbound and not empty
    detail = (f"{numbers['bound_span_count']}/{len(expected)} spans bound to a "
              f"still/graphic/footage")
    if unbound:
        detail += f"; unbound/missing: {unbound}"
    return check_result("coverage", "PASS" if ok else "FAIL", detail,
                        recomputed=numbers)


# --------------------------------------------------------------------------- #
# CHECK 4 -- Film cross-check (informational unless the render input exists)
# --------------------------------------------------------------------------- #
def find_film_json(repo_root, slug):
    # slug like PD-2026-032-carsearch -> short name "carsearch"
    short = slug.split("-")[-1]
    candidates = [
        repo_root / "remotion" / "src" / "data" / f"{short}_film.json",
        repo_root / "remotion" / "src" / "data" / f"{slug}_film.json",
    ]
    for c in candidates:
        if c.exists():
            return c
    return None


def check_film_crosscheck(repo_root, slug, remotion_plan):
    film_path = find_film_json(repo_root, slug)
    if film_path is None:
        return check_result(
            "film_crosscheck", "WARN",
            "no <slug>_film.json render input found yet -- render cannot run "
            "until it is generated (motion budget was validated from the plan)",
            film_path=None)

    film, err = load_json(film_path)
    if err:
        return check_result("film_crosscheck", "WARN", err, film_path=str(film_path))

    cuts = film.get("cuts") or []
    kinds = {}
    depth_treated = 0
    still_like = 0
    for c in cuts:
        k = str(c.get("kind", "")).lower()
        kinds[k] = kinds.get(k, 0) + 1
        if k in ("img", "still", "image"):
            still_like += 1
        if "depth" in str(c.get("treatment", "")).lower():
            depth_treated += 1
    numbers = {
        "film_path": str(film_path),
        "film_cut_count": len(cuts),
        "film_kinds": kinds,
        "film_still_like_cuts": still_like,
        "film_depth_treated_cuts": depth_treated,
    }
    plan_total = sum(int(c.get("cuts", 0)) for c in (remotion_plan.get("cut_plan") or [])) if remotion_plan else 0
    numbers["plan_total_cuts"] = plan_total

    notes = []
    # depth share in the actual film, if it uses a depth treatment
    if still_like:
        film_depth_pct = 100.0 * depth_treated / still_like
        numbers["film_depth_pct_of_stills"] = round(film_depth_pct, 1)
        if film_depth_pct < DEPTH_FLOOR_PCT:
            notes.append(f"film depth share {film_depth_pct:.1f}% < {DEPTH_FLOOR_PCT:.0f}%")
    if plan_total and abs(len(cuts) - plan_total) > max(10, plan_total * 0.1):
        notes.append(f"film cut count {len(cuts)} deviates from plan {plan_total}")

    status = "FAIL" if notes else "PASS"
    detail = ("film cut list matches plan"
              if not notes else "film deviates from plan: " + "; ".join(notes))
    return check_result("film_crosscheck", status, detail, recomputed=numbers)


# --------------------------------------------------------------------------- #
# Receipt
# --------------------------------------------------------------------------- #
def next_receipt_path(scenes_dir):
    existing = list(scenes_dir.glob("preflight_receipt.v*.json"))
    max_n = 0
    for p in existing:
        m = re.search(r"preflight_receipt\.v(\d+)\.json$", p.name)
        if m:
            max_n = max(max_n, int(m.group(1)))
    return scenes_dir / f"preflight_receipt.v{max_n + 1:03d}.json"


def write_receipt_atomic(path, payload):
    tmp = path.with_name(path.name + ".tmp")
    with tmp.open("w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, ensure_ascii=False)
    tmp.replace(path)


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def run(ep_slug, repo_root, emit_receipt):
    ep_dir = repo_root / "episodes" / ep_slug
    if not ep_dir.exists():
        raise GateError(f"episode folder not found: {ep_dir}")

    scenes_dir = ep_dir / "04_scenes"
    image_dir = scenes_dir / "generated_images" / "codex_v001"

    remotion_plan, remotion_err = load_json(scenes_dir / "remotion_plan.v001.json")
    scene_plan, scene_err = load_json(scenes_dir / "scene_plan.v001.json")
    annotated, annotated_err = load_json(
        ep_dir / "03_script" / "script.annotated.v001.json")
    asset_selection, asset_err = load_json(
        ep_dir / "05_visuals" / "asset_selection.v001.json")

    inputs_report = {
        "remotion_plan": remotion_err or "ok",
        "scene_plan": scene_err or "ok",
        "script_annotated": annotated_err or "ok",
        "asset_selection": asset_err or "ok",
        "image_dir_exists": image_dir.exists(),
    }

    checks = [
        check_motion_budget(remotion_plan, remotion_err, scene_plan, scene_err),
        check_assets_exist(image_dir, annotated, scene_plan, remotion_plan),
        check_coverage(asset_selection, asset_err, annotated, scene_plan),
        check_film_crosscheck(repo_root, ep_slug, remotion_plan),
    ]

    # Hard verdict: any FAIL among the hard checks blocks the render.
    # WARN (e.g. film.json not generated yet) does not by itself set the exit
    # code, but is surfaced loudly.
    hard_fail = any(c["status"] == "FAIL" for c in checks)
    verdict = "BLOCK" if hard_fail else "GREEN"

    receipt = {
        "artifact_type": "preflight_render_receipt",
        "schema_version": "1.0.0",
        "episode_id": ep_slug,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "gate": "preflight_render_gate.py",
        "thresholds": {
            "depth_floor_pct": DEPTH_FLOOR_PCT,
            "figure_beat_floor": FIGURE_BEAT_FLOOR,
            "hero_surface_floor": HERO_SURFACE_FLOOR,
            "min_long_edge_px": MIN_LONG_EDGE_PX,
            "cuts_per_graphic_max": CUTS_PER_GRAPHIC_MAX,
        },
        "inputs": inputs_report,
        "verdict": verdict,
        "render_allowed": not hard_fail,
        "checks": checks,
    }

    receipt_path = None
    if emit_receipt:
        try:
            scenes_dir.mkdir(parents=True, exist_ok=True)
            receipt_path = next_receipt_path(scenes_dir)
            write_receipt_atomic(receipt_path, receipt)
        except OSError as exc:
            # Do not let receipt IO turn a real verdict into a crash.
            print(f"[warn] could not write receipt: {exc}", file=sys.stderr)

    return receipt, receipt_path, hard_fail


def print_report(receipt, receipt_path):
    print("=" * 72)
    print(f"PREFLIGHT RENDER GATE -- {receipt['episode_id']}")
    print(f"verdict: {receipt['verdict']}   render_allowed: {receipt['render_allowed']}")
    print("=" * 72)
    print("inputs:")
    for k, v in receipt["inputs"].items():
        print(f"  - {k}: {v}")
    print("-" * 72)
    for c in receipt["checks"]:
        print(f"[{c['status']:4}] {c['check']}: {c['detail']}")
        for sub in c.get("subchecks", []):
            print(f"        - [{sub['status']:4}] {sub['check']}: {sub['detail']}")
    print("-" * 72)
    # Surface the recomputed budget numbers compactly.
    mb = next((c for c in receipt["checks"] if c["check"] == "motion_budget"), None)
    if mb and mb.get("recomputed"):
        n = mb["recomputed"]
        print("recomputed motion budget:")
        print(f"  depth: {n.get('depth_cuts')}/{n.get('still_cuts')} still cuts "
              f"= {n.get('depth_pct_of_still_cuts')}% (floor {DEPTH_FLOOR_PCT}%)")
        print(f"  moving FigureBeats: {n.get('moving_figure_beats')} "
              f"(floor {FIGURE_BEAT_FLOOR})")
        print(f"  hero motion surfaces: {n.get('hero_motion_surfaces')} "
              f"(floor {HERO_SURFACE_FLOOR})")
    ae = next((c for c in receipt["checks"] if c["check"] == "assets_exist"), None)
    if ae and ae.get("recomputed"):
        n = ae["recomputed"]
        print("assets:")
        print(f"  staged still files: {n.get('staged_still_files')}")
        print(f"  referenced stills: {n.get('referenced_still_count')} "
              f"(present ok: {n.get('stills_present_ok')})")
        print(f"  depth-eligible stills: {n.get('depth_eligible_still_count')} "
              f"(depth maps present: {n.get('depth_maps_present')})")
    if receipt_path:
        print("-" * 72)
        print(f"receipt: {receipt_path}")
    print("=" * 72)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Pre-render preflight gate for a PD episode.")
    parser.add_argument("--ep", required=True,
                        help="episode slug, e.g. PD-2026-032-carsearch")
    parser.add_argument("--repo-root", default=None,
                        help="repo root (default: inferred from this script's location)")
    parser.add_argument("--no-receipt", action="store_true",
                        help="do not write a preflight receipt")
    args = parser.parse_args(argv)

    if args.repo_root:
        repo_root = Path(args.repo_root).resolve()
    else:
        # scripts/preflight_render_gate.py -> repo root is the parent of scripts/
        repo_root = Path(__file__).resolve().parent.parent

    try:
        receipt, receipt_path, hard_fail = run(
            args.ep, repo_root, emit_receipt=not args.no_receipt)
    except GateError as exc:
        print(f"[gate-error] {exc}", file=sys.stderr)
        return 2

    print_report(receipt, receipt_path)
    return 1 if hard_fail else 0


if __name__ == "__main__":
    sys.exit(main())
