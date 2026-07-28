#!/usr/bin/env python3
r"""Independent PREMIUM-ANIMATION density gate — catches a stills-heavy "紙芝居" film BEFORE render.

WHY THIS EXISTS (EP36 williams post-mortem)
-------------------------------------------
The owner watched EP36 and said it had "almost no animation". Yet the acceptance suite's three
existing motion gates ALL PASSED on that render:
  - motion_present (check_freeze)   — only asks "is the frame ever fully frozen?"
  - animation_density (check_low_motion) — only asks "what FRACTION of time is near-still?"
  - motion_energy (check_motion_energy)  — measures WITHIN-SHOT inter-frame pixel change.
All three measure PIXEL motion, so a slow Ken-Burns pan / parallax / depth-dolly over a STATIC
photo registers as "motion" and clears them. There was NO gate that enforced genuine PREMIUM
KINETIC ANIMATION — the motion-graphics beats (kinetic typography, data-viz figures, 3D hero
shots) that make the film read as a Kurzgesagt/Veritasium-grade documentary rather than a
slideshow with Ken-Burns. This is that gate, and it reads the film's COMPOSITION DATA (not the
rendered pixels), so it FAILS a low-animation cut CHEAPLY, before the expensive render (the
"cheap validation before expensive execution" lesson).

WHAT IT MEASURES (the real intent, not a pixel-motion proxy)
------------------------------------------------------------
Input: the episode's ``remotion/src/data/<slug>_film.json`` (the CaseFilm ``FilmData``). A
"premium kinetic beat" is any motion-graphics element the CaseFilm renderer animates with spring
easing + @remotion/motion-blur Trail + staggered mask-reveals — i.e. one of:
  - ``graphics[]``  : kinetic typography beats (``{start,end,lines[]}`` -> BeatText: Trail
                      motion-blur + spring mask-reveal "切り上がり").
  - ``figures[]``   : animated data-viz / MG components (``{start,end,kind,...}`` -> FigureBeats:
                      numberticker, votetally, pindropmap, timeline, stat, kinetic, map, ...).
  - ``heroCuts[]``  : pre-composed 3D hero videos (``{start,dur,src}`` -> Blender/Cycles shots).
The plain ``cuts[]`` (kind img/footage with a ``treatment`` of bleed/scan/duotone/focus/card/depth)
are DELIBERATELY NOT counted: they are Ken-Burns / parallax / depth-dolly over a still image —
exactly the "motion" the pixel gates already (wrongly) reward. Counting them here would re-open
the same Goodhart hole.

From those beats it computes three floors, ALL required (AND) — a film must be premium on rate,
on coverage AND on variety, so no single axis can be gamed:

  1. kinetic-beat DENSITY = (#graphics + #figures + #heroCuts) / body-minutes, where body-minutes
     = ``narrationSeconds`` / 60 (the acts runtime; hook + brand opening + endcard are excluded).
     FLOOR: MIN_KINETIC_BEATS_PER_MIN. A premium doc drops a real MG beat roughly every ~20-25s.

  2. animated COVERAGE = union of all beat [start,end] windows (clamped to the body) / body-seconds
     = the fraction of the body during which a kinetic beat is actually on screen.
     FLOOR: MIN_ANIMATED_COVERAGE.

  3. animated VARIETY = number of DISTINCT animated forms in play — each distinct figure ``kind``,
     plus "kinetic_typography" if any ``graphics`` beats exist, plus "hero3d" if any ``heroCuts``.
     FLOOR: MIN_ANIMATED_VARIETY. This is the "avoid ONE MG repeated" floor: EP36 williams was 16
     beats that were ALL ``kind:"kinetic"`` (variety 1) — a single device stamped over and over.

Best-effort SPRING / MOTION-BLUR presence (reported, non-blocking): the CaseFilm renderer wires
``spring`` easing + a @remotion/motion-blur ``Trail`` for every graphics/figure beat, so per-beat
easing is NOT encoded in the film data. We instead confirm the shared renderer
(``remotion/src/compositions/CaseFilm.tsx``) still wires ``spring`` + ``Trail`` and REPORT it; the
hard verdict rests on the density + coverage + variety floors above. (check_leveled_animation
already HARD-gates that the composition wires Trail/AmbientMotion/mask-reveal.)

CALIBRATION (measured 2026-07-11 over all remotion/src/data/*_film.json)
-----------------------------------------------------------------------
  film        dens/min  cover%  variety   verdict
  williams<-  1.56      15.6     1         FAIL   (EP36 reject: stills-heavy, one repeated MG)
  cotton      1.91      17.9     1         FAIL
  kyllo       2.00      18.7     1         FAIL
  hinton      2.04      18.8     1         FAIL
  hinders     2.06      32.6     6         FAIL   (fails on density)
  rodriguez   2.20      20.5     1         FAIL
  katz        2.26      21.1     1         FAIL
  forfeiture  2.45      22.5     3         FAIL
  rolin   <-  2.82      35.0    15         PASS   (animation-rich reference)
  unlock      2.85      26.6     1         FAIL   (rate+coverage ok but ONE MG repeated 33x)
  tyler   <-  2.93      31.7    13         PASS   (animation-rich reference)
  carsearch<- 4.08      47.6    14         PASS   (animation-rich reference)
The floors sit in the natural gap between the stills-heavy cluster and the animation-rich trio:
density 2.45->2.82, coverage 22.5->26.6, variety 6->13. The PASS set is EXACTLY the three genuinely
animation-rich reference episodes (variety 13-15); EP36 williams FAILS on all three axes. Floors are
kept in the gap (not scraped down to just-below-williams) so the stills-heavy back-catalogue does
NOT sneak through — per the owner: a low-animation film must not ship.

Usage:
  py -3.11 scripts/check_motion_density.py --ep PD-2026-036-williams
  py -3.11 scripts/check_motion_density.py --ep williams --json out.json
  py -3.11 scripts/check_motion_density.py --selftest        # RED fixture (must FAIL) + real run

Exit codes: 0 = PASS (or artifact-absent skip), 1 = FAIL / usage error.

check_final_acceptance imports this module and calls ``evaluate(epdir)``; the returned dict keys
(check / ok / hard / reason / skipped / density_per_min / coverage / variety / kinetic_beats /
body_minutes / floors) are the stable contract. ``evaluate`` NEVER calls sys.exit and never raises
on missing inputs — it returns a skip dict so the caller cannot crash.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any, Optional

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "remotion" / "src" / "data"
CASEFILM_TSX = ROOT / "remotion" / "src" / "compositions" / "CaseFilm.tsx"
DEFAULT_EP = "PD-2026-036-williams"
CHECK_NAME = "motion_density"

# ---- HARD floors (see the module docstring CALIBRATION table for the measured numbers) ----------
# A premium documentary must clear ALL THREE (AND): a genuine MG beat-rate, real on-screen coverage,
# and a varied device palette. Calibrated to sit in the gap between the stills-heavy back-catalogue
# and the animation-rich trio (carsearch/rolin/tyler); EP36 williams fails all three.
MIN_KINETIC_BEATS_PER_MIN = 2.5   # #(graphics+figures+heroCuts) per body-minute (williams 1.56; rich 2.82-4.08)
MIN_ANIMATED_COVERAGE = 0.25      # union of beat windows / body-seconds  (williams 0.156; rich 0.317-0.476)
MIN_ANIMATED_VARIETY = 3          # distinct animated forms; "avoid one MG repeated" (williams 1; rich 13-15)


# ------------------------------------------------------------------------------------------------
# film-data resolution + metric helpers
# ------------------------------------------------------------------------------------------------

def _slug_of(name: str) -> str:
    """Episode folder / slug -> the film-data core slug (strip a leading PD-YYYY-NNN- prefix),
    mirroring check_final_acceptance._film_path so this gate resolves the SAME <slug>_film.json."""
    return re.sub(r"^PD-\d{4}-\d{3}-", "", str(name))


def _load(p: Path) -> Optional[dict[str, Any]]:
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001 - unreadable/malformed json -> treat as absent
        return None
    return d if isinstance(d, dict) else None


def resolve_film(data_dir: Path, slug: str) -> Optional[Path]:
    """Find the episode's film json: prefer <slug>_film.json (the suite convention); else match a
    film whose episode_id ends with the slug / whose core slug equals the slug tail."""
    direct = data_dir / f"{slug}_film.json"
    if direct.is_file():
        return direct
    tail = slug.split("-")[-1].lower()
    for p in sorted(data_dir.glob("*_film.json")):
        d = _load(p)
        if not d:
            continue
        core = p.name[:-len("_film.json")].lower()
        eid = str(d.get("episode_id") or "").lower()
        if core == tail or core == slug.lower() or (eid and (eid == slug.lower() or eid.endswith(tail))):
            return p
    return None


def _union_seconds(intervals: list[tuple[float, float]], lo: float, hi: float) -> float:
    """Total length of the union of [a,b] intervals, each clamped to [lo,hi]."""
    ivs = sorted((max(lo, a), min(hi, b)) for a, b in intervals if b > a)
    total = 0.0
    cur_s: Optional[float] = None
    cur_e: Optional[float] = None
    for a, b in ivs:
        if b <= a:
            continue
        if cur_s is None:
            cur_s, cur_e = a, b
        elif a <= cur_e:  # overlap / touch -> extend
            cur_e = max(cur_e, b)
        else:
            total += cur_e - cur_s
            cur_s, cur_e = a, b
    if cur_s is not None:
        total += cur_e - cur_s
    return total


def compute_metrics(film: dict[str, Any]) -> dict[str, Any]:
    """Compute the premium-animation metrics from a FilmData dict.

    Returns density_per_min, coverage, variety, the raw beat counts, body_seconds, and the distinct
    animated-form tally. A "premium kinetic beat" = a graphics typography beat, an animated figure,
    or a 3D heroCut. Plain cuts[] (Ken-Burns/parallax/depth over stills) are NOT counted."""
    body_s = float(film.get("narrationSeconds") or 0.0)
    graphics = film.get("graphics") or []
    figures = film.get("figures") or []
    heroes = film.get("heroCuts") or []
    external = film.get("externalKineticBeats") or []
    n_g, n_f, n_h, n_e = len(graphics), len(figures), len(heroes), len(external)
    beats = n_g + n_f + n_h + n_e
    body_min = body_s / 60.0 if body_s > 0 else 0.0
    density = beats / body_min if body_min > 0 else 0.0

    ivs: list[tuple[float, float]] = []
    for b in graphics:
        ivs.append((float(b.get("start", 0.0)), float(b.get("end", 0.0))))
    for b in figures:
        ivs.append((float(b.get("start", 0.0)), float(b.get("end", 0.0))))
    for b in heroes:
        s = float(b.get("start", 0.0))
        ivs.append((s, s + float(b.get("dur", 0.0))))
    for b in external:
        ivs.append((float(b.get("start", 0.0)), float(b.get("end", 0.0))))
    covered = _union_seconds(ivs, 0.0, body_s) if body_s > 0 else 0.0
    coverage = covered / body_s if body_s > 0 else 0.0

    # distinct animated FORMS: each figure kind + kinetic typography + hero 3D.
    forms: Counter = Counter()
    for b in figures:
        forms["fig:" + str(b.get("kind", "?"))] += 1
    if n_g:
        forms["kinetic_typography"] += n_g
    if n_h:
        forms["hero3d"] += n_h
    for b in external:
        forms["external:" + str(b.get("kind", "?"))] += 1
    variety = len(forms)

    return {
        "body_seconds": round(body_s, 1),
        "body_minutes": round(body_min, 2),
        "kinetic_beats": beats,
        "graphics_beats": n_g,
        "figure_beats": n_f,
        "hero_cuts": n_h,
        "external_kinetic_beats": n_e,
        "plain_cuts": len(film.get("cuts") or []),
        "density_per_min": round(density, 2),
        "coverage": round(coverage, 3),
        "covered_seconds": round(covered, 1),
        "variety": variety,
        "forms": dict(forms),
    }


def _spring_motionblur_signal() -> dict[str, Any]:
    """Best-effort (non-blocking) presence signal: confirm the shared CaseFilm renderer still wires
    spring easing + @remotion/motion-blur Trail (per-beat easing is not in the film data). Reported
    only — the hard verdict rests on the density/coverage/variety floors."""
    try:
        blob = CASEFILM_TSX.read_text(encoding="utf-8", errors="ignore")
    except Exception:  # noqa: BLE001
        return {"detectable": False, "spring": None, "motion_blur_trail": None}
    return {
        "detectable": True,
        "spring": "spring(" in blob or "spring({" in blob,
        "motion_blur_trail": ("@remotion/motion-blur" in blob and "Trail" in blob),
    }


# ------------------------------------------------------------------------------------------------
# core evaluation (importable by check_final_acceptance via _ext_gate)
# ------------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------
# BEATSHEET source (code-driven premium compositions, e.g. WilliamsFilm) — the beatsheet is the
# SAME artifact the composition renders from, so the gate measures exactly what ships (no divergence
# between what we gate and what we render). Preferred over the CaseFilm <slug>_film.json when present.
# ------------------------------------------------------------------------------------------------
# Genuine premium-kinetic beat kinds: animated MG, kinetic typography, animated-hero-treatment,
# transitions. Texture/rest kinds are NOT counted as premium animation (no footage/breath padding).
BEATSHEET_KINETIC_KINDS = {"hero", "mg_hero", "opening", "act_title", "closing", "endcard", "transition"}
BEATSHEET_TEXTURE_KINDS = {"factory", "breath", "cold_open"}
# Only the real MG + kinetic-typography devices count toward VARIETY (NOT hero pans / footage /
# transitions) — so a film of only hero push-ins still FAILS variety, exactly the EP36 failure mode.
BEATSHEET_FORM_KINDS = {"mg_hero", "opening", "act_title", "closing", "endcard"}


def resolve_beatsheet(epdir: Path) -> Optional[Path]:
    """Latest episodes/<ep>/04_scenes/premium_beatsheet.v*.json, or None."""
    cands = sorted((epdir / "04_scenes").glob("premium_beatsheet.v*.json"))
    return cands[-1] if cands else None


def compute_metrics_from_beatsheet(bs: dict[str, Any]) -> Optional[dict[str, Any]]:
    meta = bs.get("meta") or {}
    beats = bs.get("beats")
    if not isinstance(beats, list) or not beats:
        return None
    fps = float(meta.get("fps") or 30) or 30.0
    body_seconds = float(meta.get("projected_runtime_seconds")
                         or meta.get("narration_master_seconds") or 0)
    if body_seconds <= 0:
        end_f = max((int(b.get("start_frame", 0)) + int(b.get("dur_frames", 0))) for b in beats)
        body_seconds = end_f / fps
    if body_seconds <= 0:
        return None
    body_minutes = body_seconds / 60.0

    def kind(b): return str(b.get("kind") or "")
    kinetic = [b for b in beats if kind(b) in BEATSHEET_KINETIC_KINDS]
    texture = [b for b in beats if kind(b) in BEATSHEET_TEXTURE_KINDS]
    total_frames = max(1, round(body_seconds * fps))
    covered = bytearray(total_frames)
    for b in kinetic:
        s = max(0, int(b.get("start_frame", 0)))
        e = min(total_frames, s + int(b.get("dur_frames", 0)))
        for f in range(s, e):
            covered[f] = 1
    covered_frames = sum(covered)
    forms = Counter(str(b.get("component") or kind(b))
                    for b in beats if kind(b) in BEATSHEET_FORM_KINDS)
    return {
        "density_per_min": round(len(kinetic) / body_minutes, 2) if body_minutes else 0.0,
        "coverage": round(covered_frames / total_frames, 3),
        "variety": len(forms),
        "kinetic_beats": len(kinetic),
        "graphics_beats": sum(1 for b in beats if kind(b) in {"opening", "act_title", "closing", "endcard"}),
        "figure_beats": sum(1 for b in beats if kind(b) == "mg_hero"),
        "hero_cuts": sum(1 for b in beats if kind(b) == "hero"),
        "plain_cuts": len(texture),
        "body_minutes": round(body_minutes, 2),
        "body_seconds": round(body_seconds, 1),
        "covered_seconds": round(covered_frames / fps, 1),
        "forms": dict(forms),
    }


def _verdict(m: dict[str, Any], extra: dict[str, Any]) -> dict[str, Any]:
    """Shared PASS/FAIL logic over a metrics dict (works for film-data OR beatsheet sources)."""
    sig = _spring_motionblur_signal()
    problems: list[str] = []
    if m["density_per_min"] < MIN_KINETIC_BEATS_PER_MIN:
        problems.append(f"kinetic-beat density {m['density_per_min']:.2f}/min < "
                        f"{MIN_KINETIC_BEATS_PER_MIN:.1f} ({m['kinetic_beats']} beats over "
                        f"{m['body_minutes']:.1f}min — mostly Ken-Burns stills)")
    if m["coverage"] < MIN_ANIMATED_COVERAGE:
        problems.append(f"animated coverage {m['coverage']*100:.1f}% < {MIN_ANIMATED_COVERAGE*100:.0f}% "
                        f"({m['covered_seconds']:.0f}s of {m['body_seconds']:.0f}s body has a kinetic beat)")
    if m["variety"] < MIN_ANIMATED_VARIETY:
        top = ", ".join(f"{k}x{v}" for k, v in sorted(m["forms"].items(), key=lambda kv: -kv[1])[:3])
        problems.append(f"animated variety {m['variety']} < {MIN_ANIMATED_VARIETY} distinct forms "
                        f"(one MG repeated: {top or 'none'})")
    common = {
        "check": CHECK_NAME, "density_per_min": m["density_per_min"], "coverage": m["coverage"],
        "variety": m["variety"], "kinetic_beats": m["kinetic_beats"], "graphics_beats": m["graphics_beats"],
        "figure_beats": m["figure_beats"], "hero_cuts": m["hero_cuts"], "plain_cuts": m["plain_cuts"],
        "body_minutes": m["body_minutes"], "forms": m["forms"], "spring_motionblur": sig,
        "floors": {"density_per_min": MIN_KINETIC_BEATS_PER_MIN, "coverage": MIN_ANIMATED_COVERAGE,
                   "variety": MIN_ANIMATED_VARIETY},
        **extra,
    }
    if problems:
        return {**common, "ok": False, "hard": True,
                "reason": "premium animation too sparse (紙芝居 risk): " + "; ".join(problems)}
    return {**common, "ok": True, "hard": True,
            "reason": (f"premium animation OK: {m['density_per_min']:.2f} beats/min "
                       f"(>= {MIN_KINETIC_BEATS_PER_MIN:.1f}), coverage {m['coverage']*100:.1f}% "
                       f"(>= {MIN_ANIMATED_COVERAGE*100:.0f}%), variety {m['variety']} forms "
                       f"(>= {MIN_ANIMATED_VARIETY}); {m['kinetic_beats']} kinetic beats "
                       f"[{m['graphics_beats']} typo / {m['figure_beats']} figures / {m['hero_cuts']} hero]")}


def evaluate(epdir: Path, *, data_dir: Optional[Path] = None) -> dict[str, Any]:
    """Premium-animation density gate. ``epdir`` is the episode directory (its ``.name`` is the
    episode id, e.g. ``episodes/PD-2026-036-williams``). NEVER raises, NEVER calls sys.exit.

    Source precedence: a code-driven composition's ``04_scenes/premium_beatsheet.v*.json`` (what the
    WilliamsFilm-style composition actually renders) is measured when present; otherwise the CaseFilm
    ``<slug>_film.json``. Measuring the beatsheet keeps the gate aligned with what actually ships.

    Returns a dict compatible with check_final_acceptance:
      {"check", "ok", "hard", "reason", density_per_min, coverage, variety, ..., optional "skipped"}
    A missing film json (assets on SSD / not in repo) -> non-blocking skip. A film below ANY of the
    three floors -> {"ok": False, "hard": True}."""
    epdir = Path(epdir)
    data_dir = Path(data_dir) if data_dir is not None else DATA_DIR
    slug = _slug_of(epdir.name)

    # Prefer the beatsheet (code-driven premium composition) — it is the artifact the composition
    # actually renders from, so the gate measures exactly what ships.
    bs_path = resolve_beatsheet(epdir)
    if bs_path is not None:
        bs = _load(bs_path)
        m = compute_metrics_from_beatsheet(bs) if bs else None
        if m is not None:
            return _verdict(m, {"source": "beatsheet", "beatsheet": str(bs_path),
                                "episode_id": str((bs.get("meta") or {}).get("episode_id") or slug)})
        # beatsheet unreadable/empty -> fall through to film-data path

    if not data_dir.is_dir():
        return {"check": CHECK_NAME, "ok": True, "hard": False, "skipped": True,
                "reason": f"film-data dir not present (skipping): {data_dir}"}

    film_path = resolve_film(data_dir, slug)
    if film_path is None:
        return {"check": CHECK_NAME, "ok": True, "hard": False, "skipped": True,
                "reason": f"no <slug>_film.json resolves to episode '{slug}' under {data_dir} "
                          f"(film data may be on SSD) — skipping"}
    film = _load(film_path)
    if not film or not isinstance(film.get("cuts"), list):
        return {"check": CHECK_NAME, "ok": True, "hard": False, "skipped": True,
                "reason": f"{film_path.name} is not a readable FilmData (no cuts[]) — skipping"}

    m = compute_metrics(film)
    if m["body_seconds"] <= 0:
        return {"check": CHECK_NAME, "ok": True, "hard": False, "skipped": True,
                "reason": f"{film_path.name} has no narrationSeconds body runtime — skipping"}

    sig = _spring_motionblur_signal()
    problems: list[str] = []
    if m["density_per_min"] < MIN_KINETIC_BEATS_PER_MIN:
        problems.append(f"kinetic-beat density {m['density_per_min']:.2f}/min < "
                        f"{MIN_KINETIC_BEATS_PER_MIN:.1f} ({m['kinetic_beats']} beats over "
                        f"{m['body_minutes']:.1f}min — mostly Ken-Burns stills)")
    if m["coverage"] < MIN_ANIMATED_COVERAGE:
        problems.append(f"animated coverage {m['coverage']*100:.1f}% < {MIN_ANIMATED_COVERAGE*100:.0f}% "
                        f"({m['covered_seconds']:.0f}s of {m['body_seconds']:.0f}s body has a kinetic beat)")
    if m["variety"] < MIN_ANIMATED_VARIETY:
        top = ", ".join(f"{k}x{v}" for k, v in sorted(m["forms"].items(), key=lambda kv: -kv[1])[:3])
        problems.append(f"animated variety {m['variety']} < {MIN_ANIMATED_VARIETY} distinct forms "
                        f"(one MG repeated: {top or 'none'})")

    common = {
        "check": CHECK_NAME,
        "film_json": str(film_path),
        "episode_id": str(film.get("episode_id") or slug),
        "density_per_min": m["density_per_min"],
        "coverage": m["coverage"],
        "variety": m["variety"],
        "kinetic_beats": m["kinetic_beats"],
        "graphics_beats": m["graphics_beats"],
        "figure_beats": m["figure_beats"],
        "hero_cuts": m["hero_cuts"],
        "plain_cuts": m["plain_cuts"],
        "body_minutes": m["body_minutes"],
        "forms": m["forms"],
        "spring_motionblur": sig,
        "floors": {
            "density_per_min": MIN_KINETIC_BEATS_PER_MIN,
            "coverage": MIN_ANIMATED_COVERAGE,
            "variety": MIN_ANIMATED_VARIETY,
        },
    }

    if problems:
        return {**common, "ok": False, "hard": True,
                "reason": "premium animation too sparse (紙芝居 risk): " + "; ".join(problems)}
    return {**common, "ok": True, "hard": True,
            "reason": (f"premium animation OK: {m['density_per_min']:.2f} beats/min "
                       f"(>= {MIN_KINETIC_BEATS_PER_MIN:.1f}), coverage {m['coverage']*100:.1f}% "
                       f"(>= {MIN_ANIMATED_COVERAGE*100:.0f}%), variety {m['variety']} forms "
                       f"(>= {MIN_ANIMATED_VARIETY}); {m['kinetic_beats']} kinetic beats "
                       f"[{m['graphics_beats']} typo / {m['figure_beats']} figures / {m['hero_cuts']} hero3d] "
                       f"vs {m['plain_cuts']} Ken-Burns cuts")}


# ------------------------------------------------------------------------------------------------
# reporting / CLI / selftest
# ------------------------------------------------------------------------------------------------

def _print_report(r: dict[str, Any]) -> None:
    if r.get("skipped"):
        print(f"\n[SKIP] {r.get('reason')}")
        return
    print("\n" + "=" * 78)
    print("PREMIUM-ANIMATION DENSITY REPORT")
    print("=" * 78)
    print(f"  film json   : {r.get('film_json')}")
    print(f"  episode     : {r.get('episode_id')}")
    print(f"  density     : {r.get('density_per_min')}/min   (floor {r['floors']['density_per_min']})")
    print(f"  coverage    : {r.get('coverage', 0)*100:.1f}%    (floor {r['floors']['coverage']*100:.0f}%)")
    print(f"  variety     : {r.get('variety')} forms   (floor {r['floors']['variety']})")
    print(f"  beats       : {r.get('kinetic_beats')}  "
          f"[{r.get('graphics_beats')} typo / {r.get('figure_beats')} figures / {r.get('hero_cuts')} hero3d]"
          f"  vs {r.get('plain_cuts')} Ken-Burns cuts")
    print(f"  spring/blur : {r.get('spring_motionblur')}")
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


def _run_selftest() -> int:
    """(a) a KNOWN-BAD stills-heavy film (williams-like: one MG repeated, low rate/coverage) MUST
    FAIL; (b) a KNOWN-GOOD animation-rich film MUST PASS; (c) a real run on DEFAULT_EP."""
    print("=" * 78)
    print("SELFTEST (a): RED FIXTURE — a stills-heavy, one-MG-repeated film MUST fail")
    print("=" * 78)
    with tempfile.TemporaryDirectory() as td:
        data_dir = Path(td) / "data"
        data_dir.mkdir()
        # RED: 600s body, 16 beats all the same 'kinetic' figure (density 1.6, cov ~16%, variety 1)
        red_film = {
            "episode_id": "PD-9999-999-redtest", "narrationSeconds": 600.0,
            "cuts": [{"start": i * 3.0, "dur": 3.0, "kind": "img", "src": f"x/{i}.png",
                      "treatment": "depth", "seed": str(i)} for i in range(200)],
            "figures": [{"start": i * 37.0, "end": i * 37.0 + 6.0, "kind": "kinetic",
                         "lines": ["x"], "style": "a"} for i in range(16)],
            "graphics": [], "heroCuts": [],
        }
        (data_dir / "redtest_film.json").write_text(json.dumps(red_film), "utf-8")
        red = evaluate(Path(td) / "episodes" / "PD-9999-999-redtest", data_dir=data_dir)
        red_ok = (red.get("ok") is False) and not red.get("skipped")
        print(f"  ok={red.get('ok')} density={red.get('density_per_min')} "
              f"coverage={red.get('coverage')} variety={red.get('variety')}")
        print(f"  reason: {red.get('reason')}")

        print("\n" + "=" * 78)
        print("SELFTEST (b): GREEN FIXTURE — an animation-rich film MUST pass")
        print("=" * 78)
        # GREEN: 600s body, ~40 beats across many distinct forms, ~30% coverage.
        kinds = ["numberticker", "votetally", "pindropmap", "timeline", "stat", "quote",
                 "lowerthird", "acttitle", "regionmap", "kinetic"]
        green_film = {
            "episode_id": "PD-9999-998-greentest", "narrationSeconds": 600.0,
            "cuts": [{"start": i * 3.0, "dur": 3.0, "kind": "img", "src": f"x/{i}.png",
                      "treatment": "scan", "seed": str(i)} for i in range(200)],
            "figures": [{"start": i * 15.0, "end": i * 15.0 + 5.0, "kind": kinds[i % len(kinds)]}
                        for i in range(36)],
            "graphics": [{"start": 590.0, "end": 596.0, "lines": ["A", "B"]}],
            "heroCuts": [{"start": 8.0, "dur": 10.0, "src": "x/hero.mp4"}],
        }
        (data_dir / "greentest_film.json").write_text(json.dumps(green_film), "utf-8")
        green = evaluate(Path(td) / "episodes" / "PD-9999-998-greentest", data_dir=data_dir)
        green_ok = (green.get("ok") is True) and not green.get("skipped")
        print(f"  ok={green.get('ok')} density={green.get('density_per_min')} "
              f"coverage={green.get('coverage')} variety={green.get('variety')}")
        print(f"  reason: {green.get('reason')}")

    ok = red_ok and green_ok
    print(f"\nRED-FIXTURE:   {'PASS' if red_ok else 'FAIL'} (gate {'correctly failed' if red_ok else 'DID NOT fail'} the stills-heavy film)")
    print(f"GREEN-FIXTURE: {'PASS' if green_ok else 'FAIL'} (gate {'correctly passed' if green_ok else 'DID NOT pass'} the rich film)")

    print("\n" + "=" * 78)
    print(f"SELFTEST (c): REAL run on {DEFAULT_EP}")
    print("=" * 78)
    _print_report(evaluate(ROOT / "episodes" / DEFAULT_EP))
    return 0 if ok else 1


def main(argv: Optional[list[str]] = None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass
    ap = argparse.ArgumentParser(
        description="Independent PREMIUM-ANIMATION density gate: FAIL a stills-heavy film whose "
                    "motion-graphics beat density / coverage / variety is below the premium floors.",
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
