#!/usr/bin/env python
"""Answer, BEFORE the render: "if I build and render this episode now, what will fail?"

WHY THIS EXISTS (2026-08-11). EP62 greene was blocked by check_spec_satisfied AFTER its film
json had been built, and greene / correa / marmet each surfaced acceptance failures AFTER a
1.6-hour render. Every one of those failures was computable from artifacts that already
existed on disk: a preflight receipt that was not green, a padding measurement over the
narration index, a mux stage that does not stamp the tag sound_layers demands. The line stopped
four times for answers that were sitting in the repo the whole time.

WHAT IT IS. A FORECAST, NOT A GATE. It always exits 0 (except when it cannot run at all) so it
can never become a fifth thing stopping the line. It runs every check in
scripts/check_final_acceptance.py that can be decided from the spec, the film json, the pools
and the packaging, and it says CANNOT PREDICT -- naming what the check will measure -- for
every check that genuinely needs the finished mp4.

HOW IT AVOIDS BEING A SECOND COPY OF THE GATE. It imports and CALLS the real check functions
out of check_final_acceptance and the standalone _ext_gate modules. It does not restate a
single threshold. Where it needs a number for a message (the near-still cap, the thumbnail
size, the luma floor) it reads the constant out of check_final_acceptance. A second copy of a
number is exactly how the builder and the gate drifted apart and cost three restaging waves.

THREE PREDICTIONS IT MAKES THAT NOTHING ELSE DOES

 1. RUNTIME, before a frame exists. CaseFilm's own placement arithmetic already lives in
    check_bookends(); its endcard_window upper bound IS the film's finished length. Measured
    against memphis: predicted 1930.08s, delivered 1930.10s.

 2. sound_layers, from the shell. Its PART 2 requires the render to carry an
    `audio_mix_sha256` container tag, which build_case_film_mux.py stamps. scripts/
    _finish_episode.sh step 7 does not call that script -- it calls build_case_bgm_generic.py,
    which never writes the tag. So sound_layers fails for structural reasons on every episode
    this pipeline produces, and it is knowable without rendering anything. This file works that
    out by reading the finisher and grepping the builder it names for
    build_case_film_mux.MIX_SHA_TAG, so it re-derives the answer if the pipeline changes rather
    than hard-coding tonight's one.

 3. CARRYOVER. _finish_episode.sh snapshots the film json beside the master as
    08_edit/<slug>_film.rendered.json. When that snapshot is byte-identical to the current
    remotion/src/data/<slug>_film.json, the next render is the SAME FILM, so the pixel results
    in the latest acceptance receipt are what the pixels will say again. Those come back as
    LIKELY FAIL / LIKELY PASS (carryover), never as PASS -- they are evidence from a previous
    render, not a prediction from inputs. --no-carryover turns it off and leaves them CANNOT
    PREDICT, which is the honest floor.

IT ALSO PREDICTS THE PAPERWORK the scheduler will refuse on, and -- the part that saves
round-trips -- which deviations will need an APR that does not yet exist, so one owner decision
can cover several episodes instead of one apiece.

    py -3.11 scripts/predict_acceptance.py --slug memphis
    py -3.11 scripts/predict_acceptance.py --slug greene --slug correa --matrix
    py -3.11 scripts/predict_acceptance.py --slug memphis --json

Read-only. No render, no ffmpeg decode, no network, no paid call, no GPU.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Callable, Optional

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

import check_final_acceptance as cfa  # noqa: E402  the real gate; every threshold comes from here

ROOT = cfa.ROOT

# Verdicts. Only PASS means "this will be green".
PASS = "PASS"
WILL_FAIL = "WILL FAIL"
SOFT_FAIL = "WILL WARN"           # a soft check: reported by the gate, blocks nothing
LIKELY_FAIL = "LIKELY FAIL"       # carried over from the previous render of an identical film
LIKELY_PASS = "LIKELY PASS"       # ditto
UNDECIDED = "UNDECIDED"           # the check skipped: its input does not exist yet
CANNOT = "CANNOT PREDICT"         # genuinely needs the finished mp4

_SYMBOL = {PASS: ".", WILL_FAIL: "X", SOFT_FAIL: "w", LIKELY_FAIL: "~",
           LIKELY_PASS: "+", UNDECIDED: "-", CANNOT: "?"}

# Pixel checks: what each one will measure once the mp4 exists. The numbers are READ from the
# gate's own constants -- nothing here is a second copy of a threshold.
def _pixel_catalogue() -> dict[str, str]:
    return {
        "render_resolution":
            f"video stream >= {cfa.MIN_VIDEO_W}x{cfa.MIN_VIDEO_H} (ffprobe)",
        "render_freshness":
            "mp4 sha differs from the last receipt, mtime >= render start, and the muxed "
            "master is newer than the out/<slug>.mp4 it contains",
        "images_present":
            f"blackdetect: total black <= {cfa.MAX_TOTAL_BLACK_S:.0f}s, "
            f"longest <= {cfa.MAX_SINGLE_BLACK_S:.0f}s",
        "motion_present":
            f"freezedetect -60dB: frozen total <= {cfa.MAX_FREEZE_TOTAL_S:.0f}s, "
            f"longest <= {cfa.MAX_FREEZE_LONGEST_S:.0f}s",
        "animation_density":
            f"freezedetect {cfa.LOW_MOTION_NOISE_DB:.0f}dB over the body: near-still fraction "
            f"<= {cfa.LOW_MOTION_MAX_FRACTION * 100:.0f}% and longest hold "
            f"<= {cfa.LOW_MOTION_MAX_SPAN_S:.0f}s",
        "motion_energy":
            f"within-shot inter-frame YAVG: body mean >= {cfa.MOTION_ENERGY_BODY_MEAN_MIN:.0f}, "
            f"p10 >= {cfa.MOTION_ENERGY_P10_MIN:.0f}, every ~12s window "
            f">= {cfa.MOTION_ENERGY_SEGMENT_MEAN_MIN:.0f}",
        "body_luma":
            f"signalstats every {1 / cfa.BODY_LUMA_SAMPLE_HZ:.0f}s: median YAVG "
            f">= {cfa.BODY_LUMA_MEDIAN_MIN:.0f}, at most "
            f"{cfa.BODY_LUMA_DARK_FRAC_MAX * 100:.0f}% of frames below "
            f"{cfa.BODY_LUMA_DARK_YAVG:.0f}",
        "image_cut_luma":
            "per-cut brightness sampled out of the render (check_image_cut_luma)",
        "bgm_present":
            f"silencedetect: total silence <= {cfa.MAX_TOTAL_SILENCE_S:.0f}s",
        "bgm_ending":
            f"the final {0.30:.2f}s must resolve -- <= {cfa.BGM_END_TAIL_SILENCE_DB:.0f} dB or "
            f">= {cfa.BGM_END_MIN_DROP_DB:.0f} dB below the ending body",
        "loudness":
            f"integrated loudness inside [{cfa.LUFS_LO:.0f}, {cfa.LUFS_HI:.0f}] LUFS",
        "check_encoder_settings":
            "codec / profile / pix_fmt / colour / audio bitrate ffprobed off the final mp4",
    }

# render_freshness is ABOUT the new file, so a previous render's answer says nothing about it.
CARRYOVER_EXCLUDE = {"render_freshness"}

# The standalone gates check_final_acceptance runs through _ext_gate, in its order. The two
# commented ones are pixel-bound and live in the catalogue above instead.
_EXT_MODULES = ("check_arc_nonrepeat", "verify_caption_coverage", "check_footage_utilization",
                "verify_script_lint", "check_thumb_subject_luma", "check_padding",
                "verify_onscreen_text", "check_motion_density", "check_animation_mix",
                "check_caption_integrity", "check_visual_asset_qc", "verify_script_structure",
                "check_script_craft", "check_script_length", "check_asset_reuse",
                "check_caption_breaks", "check_retention_cadence", "check_packaging_qc")


# --------------------------------------------------------------------------- #
# runtime, predicted from the film json using CaseFilm's own arithmetic
# --------------------------------------------------------------------------- #
def predicted_runtime(epdir: Path) -> tuple[float | None, str]:
    """Finished runtime in seconds, or (None, why).

    check_bookends already reproduces CaseFilm.tsx's placement arithmetic and returns the
    end-card window; its upper bound is lead + narration + ENDCARD_SEC, which IS the length of
    the finished film. Reading it back is how this avoids owning a second copy of that sum.
    """
    b = cfa.check_bookends(epdir)
    win = b.get("endcard_window")
    if isinstance(win, (list, tuple)) and len(win) == 2 and win[1]:
        return float(win[1]), f"from {epdir.name} film json via CaseFilm placement arithmetic"
    return None, b.get("reason", "no film json -- runtime is not yet computable")


# --------------------------------------------------------------------------- #
# sound_layers: decided from the shell, not from the audio
# --------------------------------------------------------------------------- #
def mux_tag_forecast() -> tuple[bool | None, str]:
    """Will the master carry the `audio_mix_sha256` tag that sound_layers PART 2 requires?

    Reads scripts/_finish_episode.sh for the builder that writes ${SLUG}_final_bgm.v001.mp4 and
    asks whether THAT builder writes the tag. Re-derived rather than remembered, so a change to
    the pipeline changes the answer. Returns (True/False/None-unknown, explanation).
    """
    fin = ROOT / "scripts" / "_finish_episode.sh"
    if not fin.is_file():
        return None, "scripts/_finish_episode.sh not found -- cannot tell which builder muxes"
    txt = fin.read_text(encoding="utf-8", errors="ignore")
    if "_final_bgm.v001.mp4" not in txt:
        return None, "_finish_episode.sh no longer names <slug>_final_bgm.v001.mp4"
    builders = re.findall(r"scripts/(\w+)\.py[^\n]*--out\s+\"\$OUT\"", txt)
    if not builders:
        return None, "could not identify the builder that writes $OUT in _finish_episode.sh"
    try:
        import build_case_film_mux as mux
        tag = mux.MIX_SHA_TAG
    except Exception as exc:  # noqa: BLE001
        return None, f"cannot read the tag name out of build_case_film_mux ({exc})"
    stamped = []
    for b in builders:
        p = ROOT / "scripts" / f"{b}.py"
        if p.is_file() and tag in p.read_text(encoding="utf-8", errors="ignore"):
            stamped.append(b)
    if stamped:
        return True, f"{'/'.join(stamped)} writes the {tag} tag"
    return False, (f"_finish_episode.sh muxes with {'/'.join(builders)}, and none of them writes "
                   f"the {tag} tag that build_case_film_mux.py exists to stamp -- so "
                   f"sound_layers PART 2 fails on every master this pipeline makes")


def sound_layers_forecast(epdir: Path) -> dict[str, Any]:
    """Everything about sound_layers that does not need the audio track.

    PART 2 (_sound_mix_binding) is called for real. Its container-tag problem is separated out
    and re-decided from the pipeline, because the dummy path handed to it obviously has no tag
    and that answer would be meaningless. PART 1 (onset density, ambience band) needs the mix
    and is reported as the residual unknown.
    """
    probs, info = cfa._sound_mix_binding(epdir, Path(os.devnull))
    structural = [p for p in probs if "audio_mix_sha256" not in p]
    will_stamp, why = mux_tag_forecast()
    if structural:
        return {"verdict": WILL_FAIL,
                "reason": "the built mix does not satisfy PART 2: " + "; ".join(structural),
                "detail": info}
    if will_stamp is False:
        return {"verdict": WILL_FAIL,
                "reason": (f"the mix itself is fine ({info.get('distinct_sfx_files')} distinct SFX "
                           f"files, {info.get('music_tracks')} music cues, bound in "
                           f"{info.get('provenance')}) but the render will not carry the tag: {why}"),
                "detail": info}
    if will_stamp is None:
        return {"verdict": CANNOT,
                "reason": (f"mix is fine ({info.get('provenance')}); the container tag could not "
                           f"be forecast: {why}"),
                "detail": info}
    return {"verdict": CANNOT,
            "reason": (f"PART 2 will pass ({why}); PART 1 still measures onset density "
                       f">= {cfa.SOUND_MIN_ONSETS_PER_MIN:.0f}/min and the "
                       f"{cfa.SOUND_AMBIENCE_HP}-{cfa.SOUND_AMBIENCE_LP}Hz ambience band "
                       f">= {cfa.SOUND_AMBIENCE_MIN_DB:.0f} dB on the finished audio"),
            "detail": info}


# --------------------------------------------------------------------------- #
# the .srt the RENDER will burn -- not the one lying in 08_edit right now
# --------------------------------------------------------------------------- #
# _finish_episode.sh does TWO things to the captions between the film build and the render, and
# a forecast that ignores them measures a file the render never sees:
#
#   [4/7]  build_case_film_generic.write_srt REGENERATES the whole srt from the narration index
#          at RAW chunk timings. Whatever is on disk now -- polished or not, shifted or not --
#          is discarded and rewritten. (Verified on EP63 correa 2026-08-12: re-running
#          build_captions() over its narration index reproduces the shipped srt byte for byte.)
#   [4b]   polish_captions_srt.py re-segments that stream (no orphan cues, no dangling
#          function-word line ends, <= 84 chars per cue) and shifts it to the episode's
#          captionLeadSeconds -- house default 0.25 s -- as a DESTINATION measured out of the
#          file, not an increment.
#
# So the on-disk srt is a PRE-POLISH artifact, and measuring it forecasts defects the finisher
# repairs before a frame is rendered. On EP63 correa that produced the whole of tonight's one
# remaining red: caption_sync p90 lag +0.368 s against a +0.35 s gate, plus 87 dangling breaks,
# on a file that [4b] shifts 0.25 s earlier and re-segments. Post-[4b] the same measurement is
# p90 +0.093 s with 0 dangling breaks -- a PASS. Two agents spent a night on that phantom.
#
# This reproduces both steps on a scratch copy under the OS temp dir. It never writes into the
# episode, and it runs polish_captions_srt.py as a subprocess with the same argv the finisher
# uses, so it cannot drift from what [4b] actually does.
_SIM_SRT_CACHE: dict[str, tuple[Optional[Path], str]] = {}


def finisher_caption_srt(epdir: Path) -> tuple[Optional[Path], str]:
    """Reproduce [4/7] write_srt + [4b] polish on a scratch copy. Returns (path, note).

    (None, why) when the simulation cannot be trusted -- a missing filmconfig, a missing
    narration index, or a polish that exits non-zero. A non-zero polish is itself a finding:
    step [4b] guards that call with `|| die`, so it stops the build.
    """
    key = str(epdir)
    if key in _SIM_SRT_CACHE:
        return _SIM_SRT_CACHE[key]
    result: tuple[Optional[Path], str]
    try:
        import subprocess
        import tempfile
        slug = epdir.name.split("-", 3)[-1]
        cfgs = sorted((ROOT / "episodes" / "_planning").glob(f"EP*_{slug}_filmconfig.v*.json"))
        if not cfgs:
            raise FileNotFoundError(f"no filmconfig EP*_{slug}_filmconfig.v*.json")
        cfg = json.loads(cfgs[-1].read_text(encoding="utf-8"))       # [4/7] takes the LATEST
        narr_p = Path(cfg.get("narration_index")
                      or epdir / "06_audio" / "narration_index.v001.json")
        if not narr_p.is_file():
            raise FileNotFoundError(f"narration index {narr_p}")
        sys.path.insert(0, str(ROOT / "scripts"))
        import build_case_film_generic as bcfg
        cues, _total = bcfg.build_captions(json.loads(narr_p.read_text(encoding="utf-8")))
        out_dir = Path(tempfile.gettempdir()) / "pd_caption_forecast" / slug
        out_dir.mkdir(parents=True, exist_ok=True)
        sim = out_dir / "captions.as_rendered.srt"
        bcfg.write_srt(cues, sim)                                     # [4/7]
        # [4b]: the lead is the EPISODE's, defaulting to the house 0.25 s -- the same expression
        # _finish_episode.sh evaluates. The narration index polish itself would resolve is the
        # latest one beside the REAL srt, which is what [4b] gets; the scratch copy lives
        # elsewhere, so it is passed explicitly.
        lead = cfg.get("captionLeadSeconds")
        lead = 0.25 if lead is None else float(lead)
        real_srt = Path(cfg.get("captions") or epdir / "08_edit" / "captions.final.v001.srt")
        import polish_captions_srt as pol
        narr_for_polish = pol.narration_index_for(real_srt) or narr_p
        proc = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "polish_captions_srt.py"),
             "--srt", str(sim), "--lead", str(lead), "--narr", str(narr_for_polish)],
            capture_output=True, text=True)
        tail = (proc.stdout or proc.stderr or "").strip().splitlines()
        tail = tail[-1] if tail else ""
        if proc.returncode != 0:
            result = (None, f"step [4b] polish would EXIT {proc.returncode} (it is guarded by "
                            f"`|| die`, so the build stops there): {tail}")
        else:
            result = (sim, f"measured on the post-[4b] stream (lead {lead}s from "
                           f"{cfgs[-1].name}; {tail})")
    except Exception as exc:  # noqa: BLE001 - a forecast never raises
        result = (None, f"could not reproduce the finisher's caption steps ({exc}); "
                        f"measured the PRE-POLISH srt on disk, which the render never burns")
    _SIM_SRT_CACHE[key] = result
    return result


# --------------------------------------------------------------------------- #
# caption_sync: only cheap when whisper already has a cached transcription
# --------------------------------------------------------------------------- #
def caption_sync_forecast(epdir: Path, force: bool) -> dict[str, Any]:
    try:
        import verify_caption_sync as vcs
    except Exception as exc:  # noqa: BLE001
        return {"verdict": UNDECIDED, "reason": f"verify_caption_sync unavailable: {exc}"}
    cached = False
    inputs_exist = True
    try:
        import tempfile
        master = vcs.resolve_master(epdir, None)
        srt = vcs.resolve_srt(epdir, None)
        # An episode with no master and no .srt has nothing to transcribe: let the real gate
        # skip and say so, rather than reporting a whisper run this episode cannot even have.
        inputs_exist = master.exists() and srt.exists()
        windows = vcs.load_windows(epdir)
        key = vcs._cache_key(master, windows, vcs.DEFAULT_MODEL)
        cached = (Path(tempfile.gettempdir()) / "pd_capsync_cache" / f"{key}.json").exists()
    except Exception:  # noqa: BLE001
        cached = False
    if inputs_exist and not (cached or force):
        return {"verdict": CANNOT,
                "reason": ("needs a whisper transcription of the narration master (~tens of "
                           "minutes, no cache present). It does NOT need the mp4 -- re-run with "
                           "--with-caption-sync to decide it now")}
    # Measure the stream the render will BURN (post-[4/7] rebuild, post-[4b] polish), not the
    # pre-polish file in 08_edit. The real gate is still the one doing the measuring: rather
    # than restating its formatting or its thresholds here, verify_caption_sync.evaluate is
    # pointed at the simulated srt for the duration of the call. cfa.check_caption_sync looks
    # that attribute up at call time, so nothing else in the process is affected.
    sim, note = finisher_caption_srt(epdir)
    if sim is None:
        out = _from_check_dict(cfa.check_caption_sync(epdir))
        out["reason"] = f"{out.get('reason', '')} | {note}"
        return out
    _orig_evaluate = vcs.evaluate

    def _on_simulated(ep_dir, srt=None, *args, **kwargs):
        return _orig_evaluate(ep_dir, srt=str(sim), *args, **kwargs)

    try:
        vcs.evaluate = _on_simulated
        r = cfa.check_caption_sync(epdir)
    finally:
        vcs.evaluate = _orig_evaluate
    out = _from_check_dict(r)
    out["reason"] = f"{out.get('reason', '')} | {note}"
    return out


def _ext_check_name(mod: str, r: dict) -> str:
    """The name a standalone gate reports itself under.

    _ext_gate falls back to the MODULE name whenever a gate returns early without setting
    "check" -- which is exactly what every one of them does on the skip path. So the same gate
    reports as "asset_reuse" when it runs and "check_asset_reuse" when it skips, and a matrix
    built from those names grows two rows for one gate and silently scores the empty one green.
    The module own CHECK_NAME constant settles it.
    """
    name = r.get("check", mod)
    if name == mod:
        try:
            import importlib
            name = getattr(importlib.import_module(mod), "CHECK_NAME", mod)
        except Exception:  # noqa: BLE001
            pass
    return name


# --------------------------------------------------------------------------- #
# turning a real check-dict into a verdict
# --------------------------------------------------------------------------- #
def _from_check_dict(r: dict) -> dict[str, Any]:
    reason = r.get("reason", "")
    if r.get("skipped"):
        return {"verdict": UNDECIDED, "reason": reason}
    if r.get("ok"):
        return {"verdict": PASS, "reason": reason}
    return {"verdict": SOFT_FAIL if not r.get("hard", True) else WILL_FAIL, "reason": reason}


def _run(name: str, fn: Callable[[], dict]) -> dict[str, Any]:
    """Call a real gate function and never let it take the forecast down with it."""
    try:
        out = _from_check_dict(fn())
    except Exception as exc:  # noqa: BLE001
        out = {"verdict": UNDECIDED, "reason": f"{type(exc).__name__}: {exc}"}
    out["check"] = name
    return out


# --------------------------------------------------------------------------- #
# carryover from the previous render of a byte-identical film
# --------------------------------------------------------------------------- #
def carryover_source(epdir: Path) -> tuple[dict[str, bool] | None, str]:
    """The latest receipt's per-check results, IF the film about to be rendered is the same film.

    _finish_episode.sh copies the film json next to the master as <slug>_film.rendered.json.
    Byte equality with the current render input means the next render reproduces the same
    pixels, so that receipt's pixel answers are evidence about them. Anything else -> no
    carryover, and the pixel checks stay CANNOT PREDICT.
    """
    slug = re.sub(r"^PD-\d{4}-\d{3}-", "", epdir.name)
    snap = epdir / "08_edit" / f"{slug}_film.rendered.json"
    cur = cfa._film_path(epdir)
    if not snap.is_file():
        return None, "no 08_edit/<slug>_film.rendered.json snapshot beside the master"
    if not cur.is_file():
        return None, "no current film json to compare the snapshot against"
    if cfa._sha256(snap) != cfa._sha256(cur):
        return None, ("the film json has changed since the last render -- its pixel results do "
                      "not carry over")
    recs = sorted((epdir / "09_package").glob("acceptance_receipt.v*.json"))
    if not recs:
        return None, "film json unchanged since the last render, but no acceptance receipt exists"
    d = cfa._load(recs[-1]) or {}
    checks = d.get("checks")
    if not isinstance(checks, dict):
        return None, f"{recs[-1].name} carries no per-check results"
    return checks, f"film json byte-identical to the render graded by {recs[-1].name}"


# --------------------------------------------------------------------------- #
# the forecast
# --------------------------------------------------------------------------- #
def forecast(slug: str, *, with_caption_sync: bool = False,
             use_carryover: bool = True) -> dict[str, Any]:
    ep = cfa.resolve_episode(slug)
    epdir = cfa.EPDIR / ep
    rows: list[dict[str, Any]] = []

    dur, dur_why = predicted_runtime(epdir)
    carry, carry_why = (carryover_source(epdir) if use_carryover else (None, "--no-carryover"))

    # ---- checks the gate runs only when the render exists ------------------- #
    if dur is not None:
        lo, hi = cfa.runtime_band(epdir)
        rows.append(_run("runtime_band", lambda: cfa.check_runtime(dur, lo, hi)))
        rows.append(_run("hook_added", lambda: cfa.check_hook(epdir, dur)))
    else:
        rows.append({"check": "runtime_band", "verdict": UNDECIDED, "reason": dur_why})
        rows.append({"check": "hook_added", "verdict": UNDECIDED, "reason": dur_why})

    catalogue = _pixel_catalogue()
    for name, will_measure in catalogue.items():
        row = {"check": name, "verdict": CANNOT, "reason": will_measure}
        if carry is not None and name not in CARRYOVER_EXCLUDE and name in carry:
            row = {"check": name,
                   "verdict": LIKELY_FAIL if carry[name] is False else LIKELY_PASS,
                   "reason": f"{will_measure} | carryover: {carry_why}"}
        rows.append(row)

    s = sound_layers_forecast(epdir)
    rows.append({"check": "sound_layers", **s})

    rows.append(_run("probe_receipt",
                     lambda: cfa.check_probe_receipt(epdir, None, cfa._current_film_sha(epdir))))

    # ---- checks the gate always runs from the repo -------------------------- #
    rows.append(_run("voice_is_master", lambda: cfa.check_voice(epdir)))
    rows.append(_run("captions_final", lambda: cfa.check_captions(epdir, dur)))
    rows.append(_run("caption_format", lambda: cfa.check_caption_format(epdir)))
    rows.append(_run("caption_narration_match",
                     lambda: cfa.check_caption_narration_match(epdir)))
    rows.append({"check": "caption_sync", **caption_sync_forecast(epdir, with_caption_sync)})

    for mod in _EXT_MODULES:
        r = cfa._ext_gate(mod, epdir)
        rows.append({**_from_check_dict(r), "check": _ext_check_name(mod, r)})

    rows.append(_run("structure_4part", lambda: cfa.check_structure(epdir)))
    rows.append(_run("op_ed_bookends", lambda: cfa.check_bookends(epdir)))
    rows.append(_run("leveled_animation", lambda: cfa.check_leveled_animation(epdir)))
    rows.append(_run("preflight_receipt", lambda: cfa.check_preflight_receipt(epdir)))
    rows.append(_run("thumbnail_ready", lambda: cfa.check_thumbnail(epdir)))
    rows.append(_run("thumbnail_visibility", lambda: cfa.check_thumbnail_visibility(epdir)))
    rows.append(_run("image_resolution", lambda: cfa.check_image_resolution(epdir)))
    rows.append(_run("factory_used", lambda: cfa.check_factory_used(epdir, dur)))
    rows.append(_run("footage_diversity", lambda: cfa.check_footage_diversity(epdir)))

    paper = paperwork(epdir, slug)
    apr = apr_gap(epdir, rows)

    return {
        "schema_version": "1.0.0",
        "tool": "predict_acceptance.py",
        "episode_id": ep, "slug": slug,
        "predicted_runtime_seconds": round(dur, 2) if dur else None,
        "predicted_runtime_source": dur_why,
        "carryover": carry_why,
        "checks": rows,
        "paperwork": paper,
        "apr": apr,
        "coverage": coverage_audit(rows),
    }


# --------------------------------------------------------------------------- #
# coverage: has an acceptance check appeared that this forecast does not classify?
# --------------------------------------------------------------------------- #
def coverage_audit(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """A forecast that silently stops covering a new check is worse than no forecast.

    Every check name any acceptance receipt in this repo has ever recorded must appear in the
    rows above. Anything missing is named, so adding a gate to check_final_acceptance surfaces
    here instead of quietly becoming an unforecast surprise.
    """
    known = {r["check"] for r in rows}
    seen: set[str] = set()
    for p in cfa.EPDIR.glob("*/09_package/acceptance_receipt.v*.json"):
        d = cfa._load(p) or {}
        seen |= set((d.get("checks") or {}).keys())
    # These exist only on a failed run and are not checks: they are the gate reporting it could
    # not reach the file at all.
    seen -= {"render_present", "render_probe"}
    # Legacy receipt spellings: _ext_gate falls back to the MODULE name when a gate module does
    # not set its own "check" key, so old receipts carry both spellings of the same gate.
    seen = {{"check_packaging_qc": "packaging_qc",
             "check_script_length": "script_length",
             "check_asset_reuse": "asset_reuse",
             "encoder_settings": "check_encoder_settings"}.get(s, s) for s in seen}
    return {"unclassified": sorted(seen - known), "classified": len(known)}


# --------------------------------------------------------------------------- #
# the paperwork the scheduler refuses on
# --------------------------------------------------------------------------- #
def paperwork(epdir: Path, slug: str) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []

    def add(name: str, ok: bool | None, reason: str) -> None:
        out.append({"item": name,
                    "verdict": PASS if ok else (UNDECIDED if ok is None else WILL_FAIL),
                    "reason": reason})

    pkg = epdir / "09_package"

    # 1. The scheduler builds its entry from youtube_meta.v001.json. Ask IT, not a copy of it.
    cfg = None
    try:
        import upload_schedule_case_v001 as sched
        cfg = sched.CONFIG.get(slug)
        if cfg is None:
            add("scheduler CONFIG entry", False,
                f"upload_schedule_case_v001.CONFIG has no '{slug}' entry -- --ep {slug} is not "
                f"even a valid argument; add the slug with its 12:00 JST slot")
        elif cfg.get("_error"):
            add("youtube_meta title/description/tags", False, cfg["_error"])
        else:
            add("youtube_meta title/description/tags", True,
                f"title {len(cfg['title'])}ch, description {len(cfg['description'])}ch, "
                f"{len(cfg['tags'])} tags (from {Path(cfg['meta_source']).name})")
    except Exception as exc:  # noqa: BLE001
        add("scheduler CONFIG entry", None, f"could not import the scheduler: {exc}")

    # 2. The master itself.
    video = Path(cfg["video"]) if (cfg and cfg.get("video")) else None
    if video is None:
        add("final master mp4", None, "no scheduler entry to name the master")
    else:
        add("final master mp4", video.is_file(),
            f"{video.as_posix()}" + ("" if video.is_file() else " -- not rendered yet"))

    # 3. Thumbnail: the scheduler takes the LAST selected revision and refuses at 2MB; the
    #    acceptance gate's own size constants say what the picture must be.
    thumbs = sorted(pkg.glob("thumbnail.selected.v*.png"))
    if not thumbs:
        add(f"thumbnail.selected.v*.png {cfa.THUMB_W}x{cfa.THUMB_H}", False,
            "no 09_package/thumbnail.selected.v*.png")
    else:
        t = thumbs[-1]
        dims = cfa._png_dims(t)
        mb = t.stat().st_size / 1e6
        ok = dims == (cfa.THUMB_W, cfa.THUMB_H) and t.stat().st_size < 2 * 1024 * 1024
        add(f"thumbnail.selected.v*.png {cfa.THUMB_W}x{cfa.THUMB_H}", ok,
            f"{t.name} {dims[0]}x{dims[1]} {mb:.2f}MB" if dims else f"{t.name} unreadable PNG")

    # 4. Captions: film-time sidecar if one exists, else captions.final.v001.srt.
    yt = sorted((epdir / "08_edit").glob("captions.youtube.v*.srt"))
    caps = yt[-1] if yt else epdir / "08_edit" / "captions.final.v001.srt"
    add("captions sidecar", caps.is_file(),
        f"{caps.name}" + ("" if caps.is_file() else " -- missing"))

    # 5. final_delivery + the sha binding, without re-hashing 1.7GB: the receipt sha and the
    #    delivery sha must already agree, and the recorded byte count must match the file.
    dels = sorted(pkg.glob("final_delivery.v*.json"))
    recs = sorted(pkg.glob("acceptance_receipt.v*.json"))
    if not dels:
        add("final_delivery.v*.json", False, "none written")
    else:
        d = cfa._load(dels[-1]) or {}
        canon = d.get("canonical_final") or {}
        dsha, dbytes = canon.get("video_sha256"), canon.get("bytes")
        notes = [f"{dels[-1].name} sha {str(dsha)[:23]}.."]
        ok = bool(dsha)
        if video and video.is_file() and dbytes:
            same = video.stat().st_size == dbytes
            ok = ok and same
            notes.append(f"bytes {'match' if same else 'DIFFER from'} the master on disk")
        if recs:
            rsha = (cfa._load(recs[-1]) or {}).get("video_sha256")
            same = rsha == dsha
            ok = ok and same
            notes.append(f"receipt {recs[-1].name} sha {'matches' if same else 'DIFFERS'}")
        add("final_delivery.v*.json", ok, "; ".join(notes))

    # 6. A green acceptance receipt, judged exactly as the scheduler judges it.
    allowed = allowed_deviations(epdir)
    if not recs:
        add("green acceptance receipt", False,
            "no 09_package/acceptance_receipt.v*.json -- the scheduler refuses outright")
    else:
        rc = cfa._load(recs[-1]) or {}
        bad = [c for c in rc.get("hard_failures", []) if c not in allowed]
        add("green acceptance receipt", not bad,
            f"{recs[-1].name} status={rc.get('status')}; "
            + (f"unresolved: {bad}" if bad
               else f"tolerated by APR/policy: {sorted(set(rc.get('hard_failures', [])))}"))

    # 7. The scheduler refuses to run twice.
    res = pkg / "youtube_schedule_result.v001.json"
    add("not already scheduled", not res.is_file(),
        f"{res.name} exists -- the scheduler refuses as a duplicate" if res.is_file()
        else "no youtube_schedule_result.v001.json")
    return out


def allowed_deviations(epdir: Path) -> set[str]:
    """The deviation set upload_schedule_case_v001 will tolerate for this episode.

    REWRITTEN 2026-08-12 with the scheduler. The old rule -- runtime_band plus whatever an
    approval named -- was replaced by config/ship_policy.v001.json: a failure stops a ship only
    when it maps to one of four blocking classes (real-person likeness, rights, factual support,
    fabricated record). Everything else ships and is recorded on the release.

    This now reads the policy's own machine contract rather than mirroring code text, so the two
    cannot drift by editing: `advisory_checks` IS the tolerated set. Owner approvals still count,
    and are now the only route past a blocking class. A check id in NEITHER map is reported as
    unresolved here on purpose -- a forecast should nag somebody into classifying it, even
    though the scheduler itself treats an unmapped id as advisory.
    """
    allowed = {"runtime_band"}
    try:
        import pd_ship_policy as _sp
        allowed |= set((_sp.load_policy()["machine_contract"]["advisory_checks"]).keys())
    except Exception:  # noqa: BLE001  a missing policy must not crash the forecast
        pass
    for f in sorted((epdir / "approvals").glob("*.json")):
        d = cfa._load(f) or {}
        if d.get("target_type") == "edit" and str(d.get("decision", "")).startswith("approved"):
            allowed |= {x for x in d.get("accepted_deviations", []) if isinstance(x, str)}
    return allowed


def scheduler_rule_drift() -> str | None:
    """None when the scheduler still applies the rule allowed_deviations() mirrors."""
    p = ROOT / "scripts" / "upload_schedule_case_v001.py"
    if not p.is_file():
        return "scripts/upload_schedule_case_v001.py is gone"
    t = p.read_text(encoding="utf-8", errors="ignore")
    for probe in ("import pd_ship_policy as SHIP_POLICY",
                  "SHIP_POLICY.evaluate(",
                  "SHIP_POLICY.write_release_record("):
        if probe not in t:
            return (f"the scheduler no longer contains {probe!r} -- allowed_deviations() in "
                    f"predict_acceptance.py mirrors a rule that has changed")
    if not (ROOT / "config" / "ship_policy.v001.json").is_file():
        return "config/ship_policy.v001.json is gone -- the scheduler cannot start without it"
    return None


def apr_gap(epdir: Path, rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Which deviations this episode will need an APR for, and which it already has."""
    allowed = allowed_deviations(epdir)
    have_dir = (epdir / "approvals").is_dir()
    hard_now = [r["check"] for r in rows if r["verdict"] == WILL_FAIL]
    likely = [r["check"] for r in rows if r["verdict"] == LIKELY_FAIL]
    unknown = [r["check"] for r in rows if r["verdict"] == CANNOT]
    need = sorted(set(hard_now + likely) - allowed)
    return {
        "approvals_dir": have_dir,
        "already_covered": sorted(allowed - {"runtime_band"}),
        "needed_now": need,
        "predicted_hard_failures": sorted(set(hard_now)),
        "carried_over_failures": sorted(set(likely)),
        "still_unknown_until_pixels": sorted(set(unknown)),
        "note": ("no approvals/ directory exists -- every deviation below needs one written"
                 if not have_dir else ""),
    }


# --------------------------------------------------------------------------- #
# calibration: does the forecast agree with the receipt this episode actually got?
# --------------------------------------------------------------------------- #
def calibrate(fc: dict[str, Any]) -> dict[str, Any]:
    """Compare this forecast against the episode's own latest acceptance receipt.

    The only calibration available is an episode that has already been graded. A disagreement
    means THIS FILE is wrong, not the receipt: the receipt measured bytes.

      agree      -- the forecast said what the receipt recorded
      DISAGREE   -- it did not; the predictor needs fixing
      blind      -- CANNOT PREDICT / UNDECIDED, so no claim was made (an honest miss, and the
                    count of these is the real measure of how much a forecast cannot buy you)

    Rows whose agreement came from CARRYOVER are marked, because carryover reads the receipt --
    agreeing with it there is bookkeeping, not prediction.
    """
    epdir = cfa.EPDIR / fc["episode_id"]
    recs = sorted((epdir / "09_package").glob("acceptance_receipt.v*.json"))
    if not recs:
        return {"receipt": None, "reason": "no acceptance receipt to calibrate against"}
    rc = cfa._load(recs[-1]) or {}
    actual = rc.get("checks") or {}
    rows = []
    for r in fc["checks"]:
        if r["check"] not in actual:
            continue
        was_ok = actual[r["check"]] is not False
        v = r["verdict"]
        if v in (CANNOT, UNDECIDED):
            outcome = "blind"
        elif v in (PASS, LIKELY_PASS):
            outcome = "agree" if was_ok else "DISAGREE"
        else:                                   # WILL FAIL / LIKELY FAIL / WILL WARN
            outcome = "agree" if not was_ok else "DISAGREE"
        rows.append({"check": r["check"], "forecast": v,
                     "receipt": "pass" if was_ok else "fail", "outcome": outcome,
                     "from_carryover": v in (LIKELY_FAIL, LIKELY_PASS)})
    return {"receipt": recs[-1].name, "rows": rows,
            "agree": sum(1 for r in rows if r["outcome"] == "agree"),
            "disagree": [r["check"] for r in rows if r["outcome"] == "DISAGREE"],
            "blind": [r["check"] for r in rows if r["outcome"] == "blind"],
            "agree_by_carryover": [r["check"] for r in rows
                                   if r["outcome"] == "agree" and r["from_carryover"]]}


def print_calibration(fc: dict[str, Any]) -> None:
    c = calibrate(fc)
    print(f"CALIBRATION -- {fc['episode_id']} vs {c.get('receipt')}")
    if not c.get("receipt"):
        print(f"  {c['reason']}")
        return
    for r in c["rows"]:
        if r["outcome"] == "agree" and not r["from_carryover"]:
            continue                            # the boring, correct majority
        mark = "  " if r["outcome"] == "agree" else ("!!" if r["outcome"] == "DISAGREE" else "..")
        print(f"  {mark} {r['check']:<26} forecast={r['forecast']:<15} "
              f"receipt={r['receipt']}  ({r['outcome']}"
              + (", via carryover" if r["from_carryover"] else "") + ")")
    # A RECEIPT OLDER THAN THE INPUTS IS NOT A CALIBRATION.
    # Measured 2026-08-11: memphis film json 02:42, receipt 03:05 -> 0 disagreements. greene,
    # correa and marmet all had their film json and srt rewritten AFTER their last receipt (by
    # 11h, 6h and 41h), and every disagreement on those three is the forecast describing the
    # film on disk while the receipt describes the one that was rendered. Saying so here stops
    # the next reader concluding the predictor is broken -- or, worse, that it is fine.
    epdir = cfa.EPDIR / fc["episode_id"]
    slug = re.sub(r"^PD-\d{4}-\d{3}-", "", fc["episode_id"])
    ts = cfa._iso_to_epoch((cfa._load(epdir / "09_package" / c["receipt"]) or {}).get("generated_at"))
    pool = ROOT / "remotion" / "public" / slug / "factory"
    newer = [p.name for p in (cfa._film_path(epdir),
                              epdir / "08_edit" / "captions.final.v001.srt")
             if p.is_file() and ts is not None and p.stat().st_mtime > ts]
    # The staged POOL counts too, and it is the one that moves without anybody noticing:
    # correa factory pool was pruned to 31 clips at 19:05 on 2026-08-11, twenty hours after its
    # receipt, which is why factory_used is the one disagreement that survives on that episode.
    if pool.is_dir() and ts is not None and pool.stat().st_mtime > ts:
        newer.append(f"{slug}/factory ({sum(1 for _ in pool.iterdir())} files)")
    if newer:
        print(f"  NOTE: {newer} were rewritten AFTER {c['receipt']} was emitted -- this receipt "
              f"grades a different film from the one now on disk, so a disagreement here is the "
              f"forecast reading today inputs, not necessarily an error")
    print(f"  agree {c['agree']} (of which {len(c['agree_by_carryover'])} via carryover) | "
          f"DISAGREE {len(c['disagree'])} {c['disagree'] or ''} | "
          f"blind {len(c['blind'])} {c['blind']}")


# --------------------------------------------------------------------------- #
# summary line (this is what check_episode_inputs.py prints)
# --------------------------------------------------------------------------- #
def one_line(fc: dict[str, Any]) -> str:
    c = fc["checks"]
    n = {v: sum(1 for r in c if r["verdict"] == v)
         for v in (WILL_FAIL, LIKELY_FAIL, CANNOT, UNDECIDED, SOFT_FAIL)}
    will = [r["check"] for r in c if r["verdict"] == WILL_FAIL]
    need = fc["apr"]["needed_now"]
    dur = fc.get("predicted_runtime_seconds")
    bits = [f"{fc['slug']}:",
            f"{n[WILL_FAIL]} will fail" + (f" ({', '.join(will[:6])})" if will else ""),
            f"{n[LIKELY_FAIL]} likely (carryover)",
            f"{n[CANNOT]} need pixels",
            f"{n[UNDECIDED]} undecided"]
    if dur:
        bits.append(f"runtime ~{dur / 60:.1f}min")
    if need:
        bits.append(f"APR needed for {', '.join(need)}")
    paper_bad = [p["item"] for p in fc["paperwork"] if p["verdict"] == WILL_FAIL]
    if paper_bad:
        bits.append(f"scheduler will refuse: {', '.join(paper_bad)}")
    return "[forecast] " + " | ".join(bits)


# --------------------------------------------------------------------------- #
# printing
# --------------------------------------------------------------------------- #
_ORDER = [WILL_FAIL, LIKELY_FAIL, CANNOT, UNDECIDED, SOFT_FAIL, LIKELY_PASS, PASS]


def print_report(fc: dict[str, Any]) -> None:
    print("=" * 78)
    print(f"PRE-RENDER FORECAST -- {fc['episode_id']}")
    d = fc.get("predicted_runtime_seconds")
    print(f"predicted finished runtime: "
          + (f"{d:.1f}s = {d / 60:.2f} min ({fc['predicted_runtime_source']})" if d
             else f"unknown ({fc['predicted_runtime_source']})"))
    print(f"carryover: {fc['carryover']}")
    print("=" * 78)
    rows = sorted(fc["checks"], key=lambda r: (_ORDER.index(r["verdict"]), r["check"]))
    for r in rows:
        print(f"  {r['verdict']:<15} {r['check']:<26} {r['reason']}")
    print("-" * 78)
    print("SCHEDULER PAPERWORK")
    for p in fc["paperwork"]:
        print(f"  {p['verdict']:<15} {p['item']:<34} {p['reason']}")
    print("-" * 78)
    a = fc["apr"]
    print("APPROVALS")
    print(f"  approvals dir     : {'present' if a['approvals_dir'] else 'ABSENT'}"
          + (f" -- {a['note']}" if a["note"] else ""))
    print(f"  already covered   : {a['already_covered'] or 'none (runtime_band only)'}")
    print(f"  APR NEEDED FOR    : {a['needed_now'] or 'nothing'}")
    print(f"  unknown til pixels: {a['still_unknown_until_pixels']}")
    cov = fc["coverage"]
    if cov["unclassified"]:
        print(f"  [coverage] acceptance checks this forecast does NOT classify: "
              f"{cov['unclassified']}")
    drift = scheduler_rule_drift()
    if drift:
        print(f"  [drift] {drift}")
    print("=" * 78)
    print(one_line(fc))


def print_matrix(fcs: list[dict[str, Any]]) -> None:
    interesting: list[str] = []
    for fc in fcs:
        for r in fc["checks"]:
            if r["verdict"] != PASS and r["check"] not in interesting:
                interesting.append(r["check"])
    order = {c: min(_ORDER.index(r["verdict"]) for fc in fcs for r in fc["checks"]
                    if r["check"] == c) for c in interesting}
    interesting.sort(key=lambda c: (order[c], c))
    width = max(len(c) for c in interesting) if interesting else 10
    slugs = [fc["slug"] for fc in fcs]
    head = " " * (width + 2) + " ".join(f"{s[:8]:>8}" for s in slugs)
    print(head)
    for c in interesting:
        cells = []
        for fc in fcs:
            # ABSENT IS NOT PASS. Defaulting a missing row to PASS is how a gate that reports
            # under two names paints a green cell for an episode it never ran on.
            v = next((r["verdict"] for r in fc["checks"] if r["check"] == c), None)
            sym = _SYMBOL[v] if v else " "
            cells.append(f"{sym:>8}")
        print(f"{c:<{width}}  " + " ".join(cells))
    print()
    print("  legend: " + "  ".join(f"{_SYMBOL[v]}={v}" for v in _ORDER))
    print()
    for fc in fcs:
        a = fc["apr"]
        print(f"  {fc['slug']:<11} APR needed: {a['needed_now'] or 'nothing'}"
              + ("" if a["approvals_dir"] else "   [NO approvals/ DIRECTORY]"))


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--slug", action="append", required=True,
                    help="episode slug (repeatable); a number or full episode id also resolves")
    ap.add_argument("--matrix", action="store_true", help="one row per check, one column per episode")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--one-line", action="store_true", help="just the summary line per episode")
    ap.add_argument("--with-caption-sync", action="store_true",
                    help="run the whisper caption-sync measurement even with no cached transcription")
    ap.add_argument("--calibrate", action="store_true",
                    help="compare the forecast against this episode's own latest acceptance "
                         "receipt; a disagreement means this predictor is wrong")
    ap.add_argument("--no-carryover", action="store_true",
                    help="do not reuse a previous render's pixel results even when the film json "
                         "is byte-identical; leaves every pixel check CANNOT PREDICT")
    a = ap.parse_args()

    fcs = []
    for s in a.slug:
        try:
            fcs.append(forecast(s, with_caption_sync=a.with_caption_sync,
                                use_carryover=not a.no_carryover))
        except SystemExit as exc:            # resolve_episode could not name one episode
            print(f"[forecast] {s}: {exc}")
        except Exception as exc:             # noqa: BLE001
            print(f"[forecast] {s}: could not run ({type(exc).__name__}: {exc})")

    if a.calibrate:
        for fc in fcs:
            print_calibration(fc)
        return 0 if fcs else 2
    if a.json:
        print(json.dumps(fcs if len(fcs) != 1 else fcs[0], ensure_ascii=False, indent=2))
    elif a.one_line:
        for fc in fcs:
            print(one_line(fc))
    elif a.matrix or len(fcs) > 1:
        print_matrix(fcs)
    else:
        for fc in fcs:
            print_report(fc)
    # A FORECAST NEVER BLOCKS. Exit 0 whatever it found; 2 only when nothing could be measured.
    return 0 if fcs else 2


if __name__ == "__main__":
    raise SystemExit(main())
