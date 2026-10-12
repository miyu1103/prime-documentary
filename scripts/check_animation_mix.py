#!/usr/bin/env python3
r"""Independent ANIMATION-MIX gate — FAIL a STILL-DEPENDENT plan at PREFLIGHT, before spend.

WHY THIS EXISTS (EP36 williams post-mortem -> EP37 commitment)
-------------------------------------------------------------
EP36 williams' core weakness is STILL-IMAGE DEPENDENCE: ~52 of its beats are WilliamsScene hero
stills carried only by a Ken-Burns drift, so even after the other fixes ~half the body is a photo
with a slow pan — it never feels as "alive" as a real premium doc. The owner committed to investing
in MOVING assets "as much as possible" from EP37. This gate ENFORCES a healthy animation MIX at
PREFLIGHT (from the beatsheet, before the expensive render) so a still-heavy PLAN is flagged/blocked
cheaply — the "cheap validation before expensive execution" lesson.

HOW THIS DIFFERS FROM check_motion_density (motion_density gate)
---------------------------------------------------------------
motion_density counts KINETIC beats (it lumps hero + mg_hero + typography + transitions into one
"kinetic" bucket and rewards beat-rate / coverage / variety) — on that gate williams' 54 hero pans
help it and the still-dependence is invisible. THIS gate does the opposite: it puts STILL beats on
the scale explicitly and CAPS them. It measures still DEPENDENCE, not motion presence. The two gates
are complementary: motion_density = "is there enough animation?"; animation_mix = "is it leaning on
lingering stills?".

WHAT COUNTS AS A "STILL" (data-driven, by the rendering COMPONENT — not the kind label)
--------------------------------------------------------------------------------------
A beat is a STILL iff its ``component`` is ``WilliamsScene`` — the still-photo renderer (a single PNG
+ Ken-Burns push/parallax/pixel drift). In williams this correctly captures every ``hero`` beat, the
held ``breath`` beats AND the ``closing`` beats (williams' closing is a WilliamsScene still, NOT
kinetic typography — so classifying by component rather than by ``kind`` is the robust choice the
task calls for: "hero; also cold_open/breath if they are stills"). A ``cold_open`` rendered by
``FactoryClip`` (moving footage, as in williams) is therefore NOT a still.

Everything else is genuine on-screen MOTION, split into two reported buckets:
  - ANIMATED (real motion-graphics / kinetic typography): kind in {mg_hero, opening, act_title,
    endcard, closing} whose component is not WilliamsScene (spring + Trail motion-blur + mask-reveal
    MG figures, brand opening, act cards, endcard).
  - FOOTAGE (graded MOVING stock): kind in {factory, cold_open} (FactoryClip) — real inter-frame
    motion, so it counts toward the mix (weight-1), unlike a still-with-pan (weight-0).
  - transition GlitchCuts are structural boundary wipes; they are neither still nor a mix credit.

THE THREE METRICS (all frame-accurate, over a union bitmap so overlapping glitch-cuts don't double
count; body = the composition length = max(start_frame + dur_frames)):

  1. STILL-BEAT SHARE = still-frames / body-frames. HARD CAP: MAX_STILL_SHARE.
     If most of the body is a photo-with-a-pan -> FAIL "still-dependent".

  2. GENUINELY-ANIMATED + FOOTAGE COVERAGE = (animated ∪ footage) frames / body-frames.
     HARD FLOOR: MIN_MOTION_COVERAGE. Stills are weighted 0, so a wall of Ken-Burns cannot satisfy
     it. (mg-only and footage-only coverage are also reported, for insight.)

  3. LONG STILL HOLDS = number of single ``hero`` still beats that linger longer than
     LONG_HOLD_SECONDS. HARD CAP: MAX_LONG_STILL_HOLDS. Plus total OPENING length (sum of ``opening``
     beats) HARD CAP: MAX_OPENING_SECONDS (williams' old 26s brand opening was the defect; this cut
     is 8s). A premium doc may hold a hero still for effect a handful of times — 52 lingering stills
     is the 紙芝居 defect.

Verdict = AND of all four floors/caps (a still-heavy plan fails on any). This is calibrated so EP36
williams is FLAGGED (intended — it signals the EP37 moving-asset work), while an animation-rich plan
(mostly mg_hero + moving footage, few short hero stills) PASSES.

CALIBRATION (measured 2026-07-11 on the only beatsheet episode + the selftest fixtures)
--------------------------------------------------------------------------------------
  plan              still%  motion%  mg%    long-holds  open  verdict
  williams  (EP36)  50.0    50.0     15.5   52          8s    FAIL  (still-dependent; 52 lingering)
  GREEN fixture     ~7      ~93      ~55    0           8s    PASS  (animation-rich reference)
  RED fixture       ~89     ~11      0      50          8s    FAIL  (all hero stills)
Thresholds sit in the gap between williams (50% stills / 52 long holds) and an animation-rich plan
(<20% stills / 0-few long holds):
  * MAX_STILL_SHARE 0.45 — TIGHTENED from the task's ~0.55 suggestion: at 0.55 williams (0.50) would
    PASS metric #1, defeating the purpose (the gate exists to catch williams-grade still-dependence).
    0.45 places the cap just below williams so still-dependence at/above williams' baseline FAILS,
    while a moving-asset-forward plan (~7-20% stills) clears it comfortably. Read: "keep photo-with-
    pan under ~45% of runtime".
  * MIN_MOTION_COVERAGE 0.45 — the task's floor; williams (0.50) clears it (it is caught by the two
    axes below). Secondary safety against a plan with large uncovered gaps.
  * MAX_LONG_STILL_HOLDS 8 @ LONG_HOLD_SECONDS 5.0 — a premium doc may linger on a hero still a few
    times; williams' 52 is the headline defect and fails decisively.
  * MAX_OPENING_SECONDS 12.0 — williams' 26s opening was the old defect; this cut is 8s.

Usage:
  py -3.11 scripts/check_animation_mix.py --ep PD-2026-036-williams
  py -3.11 scripts/check_animation_mix.py --ep williams --json out.json
  py -3.11 scripts/check_animation_mix.py --selftest   # RED (must FAIL) + GREEN (must PASS) + real

Exit codes: 0 = PASS (or beatsheet-absent skip), 1 = FAIL / usage error.

A parent suite may import this module and call ``evaluate(epdir)``; the returned dict keys
(check / ok / hard / reason / skipped / still_share / motion_coverage / long_still_holds /
opening_seconds / floors / ...) are the stable contract. ``evaluate`` NEVER calls sys.exit and never
raises on missing/malformed inputs — it returns a skip dict so the caller cannot crash.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Any, Optional

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EP = "PD-2026-036-williams"
CHECK_NAME = "animation_mix"

# ---- HARD floors / caps (see the module docstring CALIBRATION table for the measured numbers) ----
MAX_STILL_SHARE = 0.45        # still-frames / body-frames        (williams 0.50 FAIL; rich ~0.07-0.20)
MIN_MOTION_COVERAGE = 0.45    # (animated ∪ footage) / body        (williams 0.50 pass; rich ~0.85+)
LONG_HOLD_SECONDS = 5.0       # a single hero still longer than this "lingers"
MAX_LONG_STILL_HOLDS = 8      # count of lingering hero stills     (williams 52 FAIL; rich 0-few)
MAX_OPENING_SECONDS = 12.0    # sum of 'opening' beats             (williams 8.0 pass; old defect 26)

# beat classification (by rendering COMPONENT first, then kind) --------------------------------------
STILL_COMPONENT = "WilliamsScene"                       # the still-photo + Ken-Burns renderer
ANIMATED_KINDS = {"mg_hero", "opening", "act_title", "endcard", "closing"}  # real MG / kinetic typo
FOOTAGE_KINDS = {"factory", "cold_open"}                # graded MOVING stock (FactoryClip)


# ------------------------------------------------------------------------------------------------
# beatsheet resolution + helpers
# ------------------------------------------------------------------------------------------------

def _slug_of(name: str) -> str:
    """Episode folder -> core slug (strip a leading PD-YYYY-NNN- prefix)."""
    return re.sub(r"^PD-\d{4}-\d{3}-", "", str(name))


def _load(p: Path) -> Optional[dict[str, Any]]:
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001 - unreadable/malformed json -> treat as absent
        return None
    return d if isinstance(d, dict) else None


def resolve_beatsheet(epdir: Path) -> Optional[Path]:
    """Latest episodes/<ep>/04_scenes/premium_beatsheet.v*.json, or None."""
    cands = sorted((epdir / "04_scenes").glob("premium_beatsheet.v*.json"))
    return cands[-1] if cands else None


def _is_still(b: dict[str, Any]) -> bool:
    """A beat is a STILL iff rendered by the still-photo component (WilliamsScene). This captures
    hero + breath + williams' closing (all WilliamsScene) but NOT a FactoryClip cold_open."""
    return str(b.get("component") or "") == STILL_COMPONENT


def _kind(b: dict[str, Any]) -> str:
    return str(b.get("kind") or "")


def _paint(beats: list[dict[str, Any]], total: int, pred) -> int:
    """Frame count of the union of [start, start+dur) windows of beats matching pred (dedups the
    ~half-frame glitch-cut overlaps so coverage is never double-counted)."""
    bm = bytearray(total)
    for b in beats:
        if not pred(b):
            continue
        s = max(0, int(b.get("start_frame", 0)))
        e = min(total, s + int(b.get("dur_frames", 0)))
        for f in range(s, e):
            bm[f] = 1
    return sum(bm)


def compute_metrics_from_beatsheet(bs: dict[str, Any]) -> Optional[dict[str, Any]]:
    """Compute the animation-mix metrics from a premium_beatsheet dict, or None if unusable."""
    meta = bs.get("meta") or {}
    beats = bs.get("beats")
    if not isinstance(beats, list) or not beats:
        return None
    fps = float(meta.get("fps") or 30) or 30.0
    total = max((int(b.get("start_frame", 0)) + int(b.get("dur_frames", 0))) for b in beats)
    if total <= 0:
        return None

    def still(b): return _is_still(b)
    def animated(b): return (not still(b)) and _kind(b) in ANIMATED_KINDS
    def footage(b): return (not still(b)) and _kind(b) in FOOTAGE_KINDS
    def motion(b): return animated(b) or footage(b)

    still_f = _paint(beats, total, still)
    mg_f = _paint(beats, total, animated)
    foot_f = _paint(beats, total, footage)
    motion_f = _paint(beats, total, motion)

    long_holds = [round(int(b.get("dur_frames", 0)) / fps, 2)
                  for b in beats
                  if still(b) and _kind(b) == "hero" and int(b.get("dur_frames", 0)) / fps > LONG_HOLD_SECONDS]
    opening_s = sum(int(b.get("dur_frames", 0)) for b in beats if _kind(b) == "opening") / fps

    n_still = sum(1 for b in beats if still(b))
    n_hero = sum(1 for b in beats if still(b) and _kind(b) == "hero")

    return {
        "fps": fps,
        "body_frames": total,
        "body_seconds": round(total / fps, 1),
        "still_share": round(still_f / total, 3),
        "motion_coverage": round(motion_f / total, 3),
        "mg_coverage": round(mg_f / total, 3),
        "footage_coverage": round(foot_f / total, 3),
        "still_seconds": round(still_f / fps, 1),
        "motion_seconds": round(motion_f / fps, 1),
        "still_beats": n_still,
        "hero_beats": n_hero,
        "long_still_holds": len(long_holds),
        "longest_still_hold_s": round(max(long_holds), 2) if long_holds else 0.0,
        "opening_seconds": round(opening_s, 1),
        "total_beats": len(beats),
    }


def compute_metrics_from_film(film: dict[str, Any]) -> Optional[dict[str, Any]]:
    """Adapt CaseFilm data to the same frame-accurate mix model used for beatsheets."""
    fps = float(film.get("fps") or 30.0)
    body_s = float(film.get("narrationSeconds") or 0.0)
    if body_s <= 0:
        return None
    beats: list[dict[str, Any]] = []
    for cut in film.get("cuts") or []:
        is_still = str(cut.get("kind")) == "img"
        beats.append({
            "start_frame": round(float(cut.get("start", 0.0)) * fps),
            "dur_frames": max(1, round(float(cut.get("dur", 0.0)) * fps)),
            "component": STILL_COMPONENT if is_still else "FactoryClip",
            "kind": "hero" if is_still else "factory",
        })
    for key in ("graphics", "figures", "externalKineticBeats"):
        for item in film.get(key) or []:
            beats.append({
                "start_frame": round(float(item.get("start", 0.0)) * fps),
                "dur_frames": max(1, round((float(item.get("end", 0.0)) - float(item.get("start", 0.0))) * fps)),
                "component": "KineticFigure",
                "kind": "mg_hero",
            })
    for item in film.get("heroCuts") or []:
        beats.append({
            "start_frame": round(float(item.get("start", 0.0)) * fps),
            "dur_frames": max(1, round(float(item.get("dur", 0.0)) * fps)),
            "component": "HeroVideo",
            "kind": "mg_hero",
        })
    beats.append({"start_frame": round(body_s * fps) - 1, "dur_frames": 1, "component": "Boundary", "kind": "transition"})
    return compute_metrics_from_beatsheet({"meta": {"fps": fps}, "beats": beats})


def _floors() -> dict[str, Any]:
    return {
        "max_still_share": MAX_STILL_SHARE,
        "min_motion_coverage": MIN_MOTION_COVERAGE,
        "long_hold_seconds": LONG_HOLD_SECONDS,
        "max_long_still_holds": MAX_LONG_STILL_HOLDS,
        "max_opening_seconds": MAX_OPENING_SECONDS,
    }


def _verdict(m: dict[str, Any], extra: dict[str, Any]) -> dict[str, Any]:
    """Shared PASS/FAIL logic over a metrics dict — all four floors/caps AND together."""
    problems: list[str] = []
    if m["still_share"] > MAX_STILL_SHARE:
        problems.append(f"still-share {m['still_share']*100:.1f}% > {MAX_STILL_SHARE*100:.0f}% cap "
                        f"({m['still_seconds']:.0f}s of {m['body_seconds']:.0f}s body is WilliamsScene "
                        f"photo-with-pan — still-dependent)")
    if m["motion_coverage"] < MIN_MOTION_COVERAGE:
        problems.append(f"animated+footage coverage {m['motion_coverage']*100:.1f}% < "
                        f"{MIN_MOTION_COVERAGE*100:.0f}% floor ({m['motion_seconds']:.0f}s of "
                        f"{m['body_seconds']:.0f}s body has genuine motion)")
    if m["long_still_holds"] > MAX_LONG_STILL_HOLDS:
        problems.append(f"{m['long_still_holds']} hero stills linger > {LONG_HOLD_SECONDS:.0f}s "
                        f"(cap {MAX_LONG_STILL_HOLDS}; longest {m['longest_still_hold_s']:.1f}s) "
                        f"— lingering photos, not motion")
    if m["opening_seconds"] > MAX_OPENING_SECONDS:
        problems.append(f"opening {m['opening_seconds']:.0f}s > {MAX_OPENING_SECONDS:.0f}s cap")

    common = {
        "check": CHECK_NAME,
        "still_share": m["still_share"],
        "motion_coverage": m["motion_coverage"],
        "mg_coverage": m["mg_coverage"],
        "footage_coverage": m["footage_coverage"],
        "long_still_holds": m["long_still_holds"],
        "longest_still_hold_s": m["longest_still_hold_s"],
        "opening_seconds": m["opening_seconds"],
        "still_beats": m["still_beats"],
        "hero_beats": m["hero_beats"],
        "total_beats": m["total_beats"],
        "body_seconds": m["body_seconds"],
        "floors": _floors(),
        **extra,
    }
    if problems:
        return {**common, "ok": False, "hard": True,
                "reason": "still-dependent plan (紙芝居 risk): " + "; ".join(problems)}
    return {**common, "ok": True, "hard": True,
            "reason": (f"animation mix OK: stills {m['still_share']*100:.1f}% (<= {MAX_STILL_SHARE*100:.0f}%), "
                       f"motion {m['motion_coverage']*100:.1f}% (>= {MIN_MOTION_COVERAGE*100:.0f}%; "
                       f"mg {m['mg_coverage']*100:.0f}% / footage {m['footage_coverage']*100:.0f}%), "
                       f"{m['long_still_holds']} lingering stills (<= {MAX_LONG_STILL_HOLDS}), "
                       f"opening {m['opening_seconds']:.0f}s (<= {MAX_OPENING_SECONDS:.0f}s)")}


# ------------------------------------------------------------------------------------------------
# core evaluation (importable by a parent suite)
# ------------------------------------------------------------------------------------------------

def evaluate(epdir: Path) -> dict[str, Any]:
    """Animation-mix gate. ``epdir`` is the episode directory (its ``.name`` is the episode id,
    e.g. ``episodes/PD-2026-036-williams``). NEVER raises, NEVER calls sys.exit.

    Reads the episode's latest ``04_scenes/premium_beatsheet.v*.json`` (the artifact the composition
    renders from, so the gate measures exactly what would ship). Returns a dict compatible with a
    parent suite: {"check", "ok", "hard", "reason", still_share, motion_coverage, long_still_holds,
    opening_seconds, ..., optional "skipped"}. A missing/unreadable beatsheet -> non-blocking skip.
    A plan breaching ANY cap/floor -> {"ok": False, "hard": True}."""
    epdir = Path(epdir)
    slug = _slug_of(epdir.name)

    bs_path = resolve_beatsheet(epdir)
    if bs_path is None:
        film_path = ROOT / "remotion" / "src" / "data" / f"{slug}_film.json"
        film = _load(film_path) if film_path.exists() else None
        m = compute_metrics_from_film(film) if film else None
        if m is None:
            return {"check": CHECK_NAME, "ok": True, "hard": False, "skipped": True,
                    "reason": f"no premium beatsheet or usable CaseFilm data for {slug} — skipping"}
        return _verdict(m, {
            "source": "casefilm",
            "beatsheet": str(film_path),
            "episode_id": str(film.get("episode_id") or slug),
        })
    bs = _load(bs_path)
    if not bs:
        return {"check": CHECK_NAME, "ok": True, "hard": False, "skipped": True,
                "reason": f"{bs_path.name} is not readable JSON — skipping"}
    m = compute_metrics_from_beatsheet(bs)
    if m is None:
        return {"check": CHECK_NAME, "ok": True, "hard": False, "skipped": True,
                "reason": f"{bs_path.name} has no usable beats/runtime — skipping"}

    return _verdict(m, {
        "source": "beatsheet",
        "beatsheet": str(bs_path),
        "episode_id": str((bs.get("meta") or {}).get("episode_id") or slug),
    })


# ------------------------------------------------------------------------------------------------
# reporting / CLI / selftest
# ------------------------------------------------------------------------------------------------

def _print_report(r: dict[str, Any]) -> None:
    if r.get("skipped"):
        print(f"\n[SKIP] {r.get('reason')}")
        return
    fl = r.get("floors", {})
    print("\n" + "=" * 78)
    print("ANIMATION-MIX REPORT")
    print("=" * 78)
    print(f"  beatsheet   : {r.get('beatsheet')}")
    print(f"  episode     : {r.get('episode_id')}")
    print(f"  still-share : {r.get('still_share', 0)*100:.1f}%   (cap {fl.get('max_still_share', 0)*100:.0f}%)"
          f"   [{r.get('still_beats')} still beats / {r.get('total_beats')} total]")
    print(f"  motion cov  : {r.get('motion_coverage', 0)*100:.1f}%   (floor {fl.get('min_motion_coverage', 0)*100:.0f}%)"
          f"   [mg {r.get('mg_coverage', 0)*100:.0f}% / footage {r.get('footage_coverage', 0)*100:.0f}%]")
    print(f"  long holds  : {r.get('long_still_holds')} hero stills > {fl.get('long_hold_seconds')}s "
          f"(cap {fl.get('max_long_still_holds')}; longest {r.get('longest_still_hold_s')}s)")
    print(f"  opening     : {r.get('opening_seconds')}s   (cap {fl.get('max_opening_seconds')}s)")
    print("-" * 78)
    print(f"  RESULT: {'PASS' if r.get('ok') else 'FAIL'}  — {r.get('reason')}")
    print("-" * 78)


def _atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2, ensure_ascii=False, default=str)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)


def _write_fixture(epdir: Path, meta: dict[str, Any], beats: list[dict[str, Any]]) -> None:
    d = epdir / "04_scenes"
    d.mkdir(parents=True, exist_ok=True)
    (d / "premium_beatsheet.v001.json").write_text(
        json.dumps({"meta": meta, "beats": beats}, ensure_ascii=False), encoding="utf-8")


def _contiguous(specs: list[tuple[str, str, int]], fps: int) -> list[dict[str, Any]]:
    """specs = [(kind, component, dur_frames), ...] -> beats laid end-to-end from frame 0."""
    out: list[dict[str, Any]] = []
    f = 0
    for i, (kind, comp, dur) in enumerate(specs, 1):
        out.append({"beat": i, "kind": kind, "component": comp, "start_frame": f, "dur_frames": dur})
        f += dur
    return out


def _run_selftest() -> int:
    """(a) a KNOWN-BAD still-heavy plan (all hero stills) MUST FAIL; (b) a KNOWN-GOOD animation-rich
    plan (mostly mg_hero + moving footage, short hero stills) MUST PASS; (c) a real run on DEFAULT_EP."""
    fps = 30
    meta = {"schema_version": "1.0.0", "fps": fps, "episode_id": "PD-9999-999-fixture"}

    print("=" * 78)
    print("SELFTEST (a): RED FIXTURE — a still-heavy plan (all hero stills) MUST fail")
    print("=" * 78)
    with tempfile.TemporaryDirectory() as td:
        ep = Path(td) / "episodes" / "PD-9999-999-redtest"
        # 50 hero stills @ 6s (all lingering) + 5 factory + 8s opening -> still ~89%, 50 long holds
        red_specs = [("opening", "BrandOpening", 8 * fps)]
        for _ in range(50):
            red_specs.append(("hero", "WilliamsScene", 6 * fps))
        for _ in range(5):
            red_specs.append(("factory", "FactoryClip", 6 * fps))
        _write_fixture(ep, {**meta, "episode_id": "PD-9999-999-redtest"}, _contiguous(red_specs, fps))
        red = evaluate(ep)
        red_ok = (red.get("ok") is False) and not red.get("skipped")
        print(f"  ok={red.get('ok')} still_share={red.get('still_share')} "
              f"motion_cov={red.get('motion_coverage')} long_holds={red.get('long_still_holds')}")
        print(f"  reason: {red.get('reason')}")

    print("\n" + "=" * 78)
    print("SELFTEST (b): GREEN FIXTURE — an animation-rich plan MUST pass")
    print("=" * 78)
    with tempfile.TemporaryDirectory() as td:
        ep = Path(td) / "episodes" / "PD-9999-998-greentest"
        # mostly mg_hero + moving footage; only 4 SHORT (4s) hero stills -> still ~7%, 0 long holds
        mg = ["FaceMatchGrid", "NumberTicker30", "BiasBars", "PinDropMap", "CaseTimeline",
              "StampCharges", "DatasetImbalance", "LineupLoop"]
        green_specs = [("opening", "BrandOpening", 8 * fps), ("act_title", "ActTitle", 6 * fps)]
        for i in range(20):
            green_specs.append(("mg_hero", mg[i % len(mg)], 6 * fps))
        for _ in range(10):
            green_specs.append(("factory", "FactoryClip", 6 * fps))
        for _ in range(4):
            green_specs.append(("hero", "WilliamsScene", 4 * fps))   # short holds, under the 5s linger line
        green_specs.append(("endcard", "BrandEndcard", 6 * fps))
        _write_fixture(ep, {**meta, "episode_id": "PD-9999-998-greentest"}, _contiguous(green_specs, fps))
        green = evaluate(ep)
        green_ok = (green.get("ok") is True) and not green.get("skipped")
        print(f"  ok={green.get('ok')} still_share={green.get('still_share')} "
              f"motion_cov={green.get('motion_coverage')} long_holds={green.get('long_still_holds')}")
        print(f"  reason: {green.get('reason')}")

    ok = red_ok and green_ok
    print(f"\nRED-FIXTURE:   {'PASS' if red_ok else 'FAIL'} "
          f"(gate {'correctly failed' if red_ok else 'DID NOT fail'} the still-heavy plan)")
    print(f"GREEN-FIXTURE: {'PASS' if green_ok else 'FAIL'} "
          f"(gate {'correctly passed' if green_ok else 'DID NOT pass'} the animation-rich plan)")

    print("\n" + "=" * 78)
    print(f"SELFTEST (c): REAL run on {DEFAULT_EP} (expected: FAIL — still-dependent)")
    print("=" * 78)
    _print_report(evaluate(ROOT / "episodes" / DEFAULT_EP))
    return 0 if ok else 1


def main(argv: Optional[list[str]] = None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass
    ap = argparse.ArgumentParser(
        description="Independent ANIMATION-MIX gate: FAIL a STILL-DEPENDENT plan (too much of the body "
                    "is a WilliamsScene photo-with-pan / too many lingering hero stills) at PREFLIGHT.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ap.add_argument("--ep", default=DEFAULT_EP, help="episode id or slug (e.g. PD-2026-036-williams)")
    ap.add_argument("--dry-run", action="store_true", help="run and report, but always exit 0")
    ap.add_argument("--selftest", action="store_true",
                    help="run the RED (must fail) + GREEN (must pass) fixtures, then the real episode")
    ap.add_argument("--json", default=None, metavar="PATH", help="also write the raw result dict to PATH")
    args = ap.parse_args(argv)

    if args.selftest:
        return _run_selftest()

    epdir = ROOT / "episodes" / args.ep
    r = evaluate(epdir)
    _print_report(r)
    if args.json:
        _atomic_write_json(Path(args.json), r)
        print(f"  wrote {args.json}")
    if args.dry_run:
        return 0
    return 0 if r.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
