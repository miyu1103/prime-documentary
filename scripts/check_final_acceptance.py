#!/usr/bin/env python
"""Independently verify that an episode's FINAL render is publish-grade.

WHY THIS EXISTS (EP14 lange post-mortem): the per-episode build scripts write a
self-asserted `quality_gate` dict into their own QC json. EP14's gate claimed
four_part_structure/all_shots_filled/captions_burned_in/lange_premium_used = true,
yet the delivered file used the SAPI *review-proxy* narration (provider
local_windows_sapi, "Microsoft Zira"), had no final captions, and was missing
images/hook. The producer graded its own homework and the values did not match
the bytes on disk (CLAUDE.md invariant 13: "generated" != "usable"; rule 17:
report measured results, not "looks good").

This script is a SEPARATE verifier: it MEASURES the actual render + reads
narration/caption provenance from the repo, and emits PASS/FAIL. It must be run
as an independent gate; the rendering agent must NOT hand-write the acceptance.

Read-only. Probes the file with ffprobe/ffmpeg; no writes, no paid calls, no
upload. Exit 0 = PASS (all hard checks), 1 = FAIL or error.

Hard checks (block the final):
  - voice_is_master    : a non-proxy narration plan exists with an ElevenLabs
                         (master) provider -- NOT local SAPI / windows / proxy.
  - captions_final     : a non-proxy caption sidecar (.srt) exists, non-empty,
                         and (if render known) covers >=90% of the runtime.
  - caption_format     : captions break cleanly -- <=2 lines, <=42 chars/line,
                         cue <=7s, reading speed <=20 cps (the "captions unreadable"
                         rework class; "caption" appears 85x in event logs).
  - caption_narration_match : the burned captions are the SAME WORDS (>=90% token
                         match) as the approved narration spoken_text -- catches a
                         wrong / review-proxy .srt burned in (the EP14 "captions
                         != narration" class that caption_format cannot detect).
  - structure_4part    : narration sections run HOOK -> OPENING -> body -> ENDING
                         and (if film-data present) the render carries a real
                         cold-open hook -- reads the artifact, not a self-asserted
                         four_part_structure bool.
  - op_ed_bookends     : the episode composition uses the canonical BrandOpening +
                         BrandEndcard from components/Bookends (no off-brand OP/ED).
  - runtime_band       : finished runtime within the episode's duration profile
                         (standard 11.5-12.5 / mid 27-33 / feature 55-65 min),
                         read from manifest.target_duration_minutes.
  - render_resolution  : video stream >= 1920x1080 (catches a low-res / not-max
                         quality export).
  - images_present     : no excessive black (a "no images" / placeholder render
                         shows long black stretches).
  - motion_present     : no long FULLY motionless stretch (freezedetect).
  - animation_density  : the frame must actually MOVE, not merely be 'not frozen'
                         -- a raised freezedetect noise floor flags near-still
                         spans (pasted still / slow Ken Burns), fails if > 10% of
                         runtime is near-still or one hold > 3s. Catches the
                         '紙芝居 (slideshow)' that motion_present misses.
  - motion_energy      : the BODY must carry real MOTION MAGNITUDE, not merely be
                         'not frozen' -- mean inter-frame pixel change (ffmpeg
                         tblend=difference -> signalstats YAVG, via
                         measure_motion_energy.py) over the same body as
                         animation_density. Fails if body mean YAVG < 12.0 (or the
                         sustained-low p10 < 4.0). Calibrated: MotionSample 46.6 vs
                         slideshow 3.5. Catches a slow Ken Burns / weak parallax that
                         animation_density's fraction metric lets through (Goodhart).
  - bgm_present        : a continuous (ducked) music bed -- narration-only mixes
                         leave long silence between sentences (EP14 final = 109s).
  - thumbnail_ready    : >=3 thumbnail PNGs at 1280x720 + a selected one exist
                         (catches "no thumbnail prepared").
Soft checks (reported, do not block):
  - hook_added         : runtime exceeds (shotlist body + bookends) by enough to
                         hold a >=25s hook + breathing beats.
  - loudness           : integrated LUFS within [-16, -12].

See docs/PD_ONE_PASS_PRODUCTION_SPEC.v1.md for the full spec each check enforces.

Usage:
  .venv/Scripts/python.exe scripts/check_final_acceptance.py 15
  .venv/Scripts/python.exe scripts/check_final_acceptance.py PD-2026-015-theranos --render H:/.../final/x.mp4
  .venv/Scripts/python.exe scripts/check_final_acceptance.py 15 --json
"""
from __future__ import annotations

import argparse
import difflib
import glob
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EPDIR = ROOT / "episodes"

RUNTIME_LO, RUNTIME_HI = 690.0, 750.0           # 11.5-12.5 min finished runtime (standard default)
MAX_TOTAL_BLACK_S = 8.0                          # cumulative black tolerated
MAX_SINGLE_BLACK_S = 3.0                         # any single black gap
MAX_TOTAL_SILENCE_S = 25.0                       # >this => no continuous BGM bed
LUFS_LO, LUFS_HI = -16.0, -12.0
SAPI_MARKERS = ("sapi", "local_windows", "windows_sapi", "zira", "local-")
MASTER_MARKERS = ("eleven",)                     # ElevenLabs = the usual master voice

# caption formatting HARD limits -- tolerant: 42 chars / 17 cps are the spec
# *targets* (PD_ONE_PASS_PRODUCTION_SPEC §A row 4); these gate values fail only on
# genuinely broken captions so the channel's normal output is not false-flagged.
MAX_LINE_CHARS = 50
MAX_CUE_LINES = 2
MAX_CUE_SECONDS = 7.0
MAX_CPS = 27.0                                   # reading speed (chars/second)
# motion / quality / packaging
MAX_FREEZE_S = 2.5                               # any motionless stretch beyond this is flagged
MAX_FREEZE_LONGEST_S = 4.0                       # tolerate one designed hold beat
MAX_FREEZE_TOTAL_S = 8.0
# animation density (row 8): "not frozen" != "actually animated". A raised
# freezedetect noise floor flags NEAR-still spans (a pasted still or a slow Ken
# Burns zoom -- the "紙芝居" the owner keeps getting). Calibrated 2026-07-04 on
# real renders: approved MotionSample = 5.5% near-still; an old slideshow-style
# cut = 14.4%. So the enforceable floor sits between.
LOW_MOTION_NOISE_DB = -38.0                      # freezedetect noise tolerance (higher => catches slow motion)
LOW_MOTION_MIN_SPAN_S = 0.8                      # a near-still stretch must last this long to count
LOW_MOTION_MAX_FRACTION = 0.10                   # >10% of runtime near-still => too little animation
LOW_MOTION_MAX_SPAN_S = 3.0                      # any single near-still hold beyond this fails
# animation_density measures BODY dynamism (hook + acts). The canonical brand bookends are
# DESIGNED-calm brand moments, not body content, and must not be scored as "紙芝居": the gold
# BrandOpening title (OPENING_SEC) and the BrandEndcard outro/CTA (ENDCARD_SEC). Excluding
# these two regions measures the right thing (owner-approved 2026-07-05); the thresholds above
# are UNCHANGED (not weakened) -- they are simply applied to the body, where slideshow is the risk.
BOOKEND_OP_SEC = 3.5                             # gold BrandOpening title (lands after the hook)
BOOKEND_ED_SEC = 9.0                             # BrandEndcard outro (trailing, designed calm)
# motion_energy (row: EP32 §5): animation_density only measures "not frozen %" -- a slow
# Ken Burns / weak parallax passes it while still reading as a slideshow (Goodhart). This
# measures the ACTUAL amount of frame movement: mean inter-frame pixel change (ffmpeg
# tblend=difference -> signalstats YAVG, 0..255; via scripts/measure_motion_energy.py) over
# the SAME body definition animation_density uses (OP title + ED outro bookends excluded).
# Calibrated 2026-07-06: a genuinely dynamic reference (MotionSample) = body mean 46.6 /
# p10 45.2; a slideshow episode (EP-carsearch v004) = mean 3.5. The enforceable floor sits
# well above the slideshow number. p10 (sustained-low 10th percentile) is a secondary floor
# so a mostly-dynamic cut with long static holds (which drags p10 down) is still caught.
MOTION_ENERGY_BODY_MEAN_MIN = 12.0               # body (within-shot) mean YAVG must clear this (slideshow=3.5, MotionSample=46.6)
# EP32 §M1 recalibration (2026-07-06): the old p10 floor of 4.0 sat almost ON the slideshow
# BODY MEAN (3.5) -- a render that was a slideshow on average could still clear it, so the
# sustained-low floor barely bit. Raised WELL above the slideshow average (3.5) into the 8-10
# band so a render with long dead holds now fails on p10 alone. Strictly higher = stricter
# (invariant 15). MotionSample body p10 = 45.2, so genuinely dynamic renders keep huge margin.
MOTION_ENERGY_P10_MIN = 9.0                       # sustained-low floor, raised 4.0 -> 9.0 (>> slideshow 3.5; MotionSample 45.2)
# EP32 §M1 within-shot + per-segment. The plain body mean is INFLATED by ~314 hard-cut YAVG
# spikes (a cut = a huge one-frame inter-frame difference) + ForcefulCut transitions, so a
# render frozen BETWEEN cuts still cleared 12. Fix: (a) mask +/-CUT_GUARD_FRAMES frames around
# every cut boundary before averaging (WITHIN-SHOT mean, in measure_motion_energy.py), and
# (b) require EACH ~12s body window's within-shot mean to clear a per-segment floor so a dead
# 30s stretch fails even when the global mean passes. Cut boundaries come from the episode's
# <slug>_film.json cuts[].start; if absent they are auto-detected as YAVG spikes.
MOTION_ENERGY_SEGMENT_MEAN_MIN = 8.0             # per-~12s-window within-shot mean floor (dead-stretch catch; >> slideshow 3.5)
MOTION_ENERGY_MAX_FAIL_SEGMENTS = 0              # zero tolerance: any body window below the segment floor fails
# ending BGM must resolve, not get chopped mid-phrase at full volume. This is a
# FLOOR only (a hard full-volume cut fails); whether it lands on a musical cadence
# ("切りのいいところ") is an arrangement choice + a manual listen -- not amplitude.
BGM_END_MIN_BODY_DB = -45.0                      # if the last seconds are quieter than this, no bed to resolve -> skip
BGM_END_TAIL_SILENCE_DB = -45.0                  # final 0.3s ~silent => resolved/faded cleanly
BGM_END_MIN_DROP_DB = 10.0                       # OR final 0.3s >=10 dB below the body => resolving, not chopped
# EP32 §B5 check_sound_layers: prove the 4-LAYER mix (VO + music + ambience + SFX) actually
# reached the RENDER's audio track, not a lone music bed (the "音が薄い/孤児" failure). TWO parts,
# BOTH required (AND):
#   PART 1 -- acoustic floors measured directly on the render with ffmpeg (no plan dependency):
#     (a) SFX-like transients: per-50ms RMS windows on a >500Hz signal; an onset = a local rise of
#         >= SOUND_TRANSIENT_RISE_DB above the trailing-window median. A bare music bed is smooth
#         (few onsets); a real mix (VO word onsets + SFX hits) is dense.
#     (b) Ambience band energy: mean level in a 40-160Hz band must exceed a floor, i.e. a sustained
#         low-frequency bed exists; an empty band sits near -70..-90 dB.
#   PART 2 -- BINDING to the built mix (EP32 §B5(b), see _sound_mix_binding): load the highest-rev
#     06_audio/audio_provenance.v*.json, require its density_gate to pass, a CONTINUOUS music bed,
#     >= SOUND_PROV_MIN_BEDS distinct ambience beds AND >= SOUND_PROV_MIN_SFX_FILES distinct
#     MEANINGFUL SFX files (filler beds excluded), and assert the RENDER carries a container tag
#     `audio_mix_sha256` equal to the provenance mix sha (the mux stage stamps it). No tag => the mux
#     stage was never run => the sound is orphaned => FAIL. Fail-closed on missing provenance / mix sha.
#
# EP32 §B5(a) RECALIBRATION (2026-07-06, owner reject "意味のない効果音がうざい / ピコピコ鳴ってて
# 耳障り / 種類も少なくてしょぼい"): the previous onset-density floor (35/min) REWARDED THE WRONG
# PROXY -- the audio builder answered it by injecting a 326-hit tick/blip filler "transient bed"
# placed on a fixed cadence PURELY to clear the floor (provenance literally: "to lift the render
# onset density over the acceptance floor"). That gate-gaming made the audio WORSE (a machine-gun of
# meaningless pips). We keep the REAL INTENT (a genuine, rich 4-layer mix, invariant 15) but stop
# rewarding raw transients:
#   * The high raw-onset floor is DROPPED to a low presence backstop (SOUND_MIN_ONSETS_PER_MIN=6):
#     it only rejects a SMOOTH lone music bed (≈0 onsets). A tasteful meaningful mix at ~15-25/min
#     PASSES; the gate no longer pressures anyone to pad transients. (Honest limit, documented not
#     hidden: speech itself creates onsets, so this acoustic test alone cannot attribute a *distinct*
#     SFX layer -- that is exactly why the meaningful-richness proof lives in PART 2's sha-bound
#     provenance, not in a transient count.)
#   * Richness is now proven STRUCTURALLY in PART 2: distinct MEANINGFUL SFX files + distinct
#     ambience beds + a continuous music bed, all bound to the render by audio_mix_sha256. A thin
#     VO-only / single-music-bed render still FAILS (no distinct SFX files / no bound mix), and a
#     filler tick-bed no longer helps (excluded; distinct *files* is what counts, not hit count).
# The ambience-band energy floor (a real sustained bed exists) is retained.
SOUND_WINDOW_SAMPLES = 2400                       # 2400 samples @48kHz = 50ms RMS analysis window
SOUND_TRANSIENT_RISE_DB = 9.0                     # a window this far above the local median = an onset
SOUND_TRANSIENT_FLOOR_DB = -45.0                  # onset must also be above this absolute level (ignore noise floor)
SOUND_TRANSIENT_BASELINE_WIN = 10                 # trailing windows (10 * 50ms = 500ms) for the local median
SOUND_TRANSIENT_DEBOUNCE_WIN = 3                  # >=150ms between counted onsets (debounce)
# Low presence BACKSTOP only (recalibrated 35 -> 6): a smooth lone music bed (~0 onsets) fails; any
# VO/SFX mix clears it. Meaningful richness is proven in PART 2, NOT by this count (see header).
SOUND_MIN_ONSETS_PER_MIN = 6.0
SOUND_MIN_TRANSIENTS_PER_MIN = SOUND_MIN_ONSETS_PER_MIN  # back-compat alias
SOUND_AMBIENCE_HP, SOUND_AMBIENCE_LP = 40, 160    # ambience band-pass (Hz)
SOUND_AMBIENCE_MIN_DB = -33.0                     # ambience-band mean floor (real finals ~ -21.9 dB; a bed must be present)
SOUND_PROV_MIN_SFX = 20                           # EP32 §B5(b): audio_provenance density_gate.sfx_count floor (meaningful cues)
SOUND_PROV_MIN_SFX_FILES = 8                      # §B5(b) recal: distinct MEANINGFUL sfx files (variety; filler excluded)
SOUND_PROV_MIN_BEDS = 4                           # EP32 §B5(b): audio_provenance distinct ambience beds floor
SOUND_PROV_MIN_MUSIC = 1                          # §B5(b) recal: continuous music bed must be present (>=1 track)
MIN_VIDEO_W, MIN_VIDEO_H = 1920, 1080
THUMB_W, THUMB_H = 1280, 720
MIN_THUMB_VARIANTS = 3
# thumbnail visibility (row 7b): the selected thumbnail must not be a dull, dark
# panel -- the "しょぼい / 全く派手じゃない / CTRが下がる" reject class. Calibrated
# 2026-07-04 on real thumbs: rejected v001 (dark navy) = luma mean 24.9-29.5;
# approved v002 (bright hero + red tag + XL text) = 36.4-48.0. Floor sits between.
THUMB_MIN_MEAN_LUMA = 33.0                       # mean brightness (0-255) -- too dark => dull/low-CTR
THUMB_MIN_CONTRAST_STD = 40.0                    # luma stddev -- too flat => no punchy text/subject
# footage diversity (row 7c): the downloaded shelf must be used with VARIETY, not
# the same few clips (esp. generic symbols like the scales of justice) on repeat.
# Owner 2026-07-04: "毎作品同じ素材が使われてる ... 天秤の動画は何度も見てきた".
# Calibrated on real cutlists: kyllo reused a clip 7x (0.50 distinct); rodriguez
# 0.33 distinct. A well-built episode staging a wide pool clears 0.55+ / <=3.
FOOTAGE_MAX_USES_PER_CLIP = 4                    # any single clip cut in more than this => lazy reuse
FOOTAGE_MIN_DISTINCT_FRACTION = 0.40            # distinct srcs / total cuts must be >= this
FOOTAGE_GENERIC_PAT = r"scale|gavel|hourglass|clock|stopwatch|balance"  # over-familiar symbols
FOOTAGE_GENERIC_MAX_USES = 2                     # a generic symbol may recur at most this often
IMG_MIN_LONG_EDGE = 3840                         # spec row 5: hero stills upscaled to >=4K long edge
FACTORY_SECONDS_PER_CLIP = 45                    # spec row 7: >=1 distinct factory clip per ~45s
# caption<->narration identity + 4-part structure + canonical bookends
CAPTION_MATCH_MIN = 0.90                         # burned captions must be >=90% the narration words
HOOK_MIN_SEC = 5.0                               # render must open with a real cold-open hook
HOOK_SECTION = "HOOK"
OPENING_SECTION = "OPENING"
ENDING_MARKERS = ("ENDING", "OUTRO", "CTA", "CLOSE", "CONCLUSION", "CODA")


def runtime_band(epdir: Path) -> tuple[float, float]:
    """Pick the finished-runtime band from the episode's duration profile.

    Reads manifest.target_duration_minutes (standard if unset). Bands match
    validate_episode.py: standard 11.5-12.5, mid 27-33, feature 55-65 min.
    """
    m = _load(epdir / "manifest.json") or {}
    t = m.get("target_duration_minutes")
    if not t:
        return RUNTIME_LO, RUNTIME_HI
    if t >= 45:
        return 3300.0, 3900.0
    if t >= 20:
        return 1620.0, 1980.0
    return RUNTIME_LO, RUNTIME_HI


def resolve_episode(arg: str) -> str:
    if (EPDIR / arg).is_dir():
        return arg
    hits = [os.path.basename(p) for p in glob.glob(str(EPDIR / f"PD-*-{int(arg):03d}-*"))] if arg.isdigit() else []
    if not hits:
        hits = [os.path.basename(p) for p in glob.glob(str(EPDIR / f"*{arg}*")) if os.path.isdir(p)]
    if len(hits) == 1:
        return hits[0]
    raise SystemExit(f"Could not resolve episode '{arg}'. Matches: {hits}")


def _load(p: Path):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None


def check_voice(epdir: Path) -> dict:
    """A non-proxy narration plan must exist with a master (ElevenLabs) provider."""
    audio = epdir / "06_audio"
    plans = [p for p in audio.glob("*.json")
             if re.search(r"voice_plan|narration_index", p.name)]
    nonproxy = [p for p in plans if "review_proxy" not in p.name]
    proxy_providers, final_providers = [], []
    for p in plans:
        d = _load(p)
        blob = json.dumps(d).lower() if d is not None else ""
        prov = ""
        m = re.search(r'"provider"\s*:\s*"([^"]+)"', blob)
        if m:
            prov = m.group(1)
        (proxy_providers if "review_proxy" in p.name else final_providers).append(prov or "(none)")
    has_master = any(any(mk in prov for mk in MASTER_MARKERS) for prov in final_providers)
    has_sapi_final = any(any(mk in prov for mk in SAPI_MARKERS) for prov in final_providers)
    ok = bool(nonproxy) and has_master and not has_sapi_final
    if not nonproxy:
        reason = "no non-proxy narration plan exists -> final would use the SAPI review-proxy voice (the EP14 failure)"
    elif has_sapi_final:
        reason = f"final narration plan provider is SAPI/local: {final_providers}"
    elif not has_master:
        reason = f"final narration plan provider is not ElevenLabs master: {final_providers or proxy_providers}"
    else:
        reason = f"master narration present: {final_providers}"
    return {"check": "voice_is_master", "ok": ok, "hard": True, "reason": reason}


def _srt_last_end_seconds(p: Path) -> float:
    txt = p.read_text(encoding="utf-8", errors="ignore")
    ends = re.findall(r"-->\s*(\d\d):(\d\d):(\d\d)[,.](\d{1,3})", txt)
    if not ends:
        return 0.0
    h, m, s, ms = ends[-1]
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000.0


def check_captions(epdir: Path, render_dur: float | None) -> dict:
    edit = epdir / "08_edit"
    srts = [p for p in edit.glob("*.srt") if "review_proxy" not in p.name]
    srts = [p for p in srts if p.stat().st_size > 0]
    if not srts:
        return {"check": "captions_final", "ok": False, "hard": True,
                "reason": "no non-proxy caption .srt in 08_edit (only review-proxy captions, or none)"}
    best = max(srts, key=lambda p: _srt_last_end_seconds(p))
    cover = _srt_last_end_seconds(best)
    ok = True
    reason = f"final captions {best.name} (last cue {cover:.0f}s)"
    if render_dur and cover < 0.90 * render_dur:
        ok = False
        reason = f"captions {best.name} cover only {cover:.0f}s of {render_dur:.0f}s render (<90%)"
    return {"check": "captions_final", "ok": ok, "hard": True, "reason": reason}


def ffprobe_duration(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(path)],
        capture_output=True, text=True, check=True)
    return float(json.loads(out.stdout)["format"]["duration"])


def check_runtime(dur: float, lo: float, hi: float) -> dict:
    ok = lo <= dur <= hi
    return {"check": "runtime_band", "ok": ok, "hard": True,
            "reason": f"{dur:.1f}s = {dur/60:.2f}min (band {lo:.0f}-{hi:.0f}s)"}


def check_caption_format(epdir: Path) -> dict:
    """Captions must break cleanly: <=2 lines, <=42 chars/line, sane cue duration
    and reading speed. Catches the recurring 'captions cut at weird points'."""
    edit = epdir / "08_edit"
    srts = [p for p in edit.glob("*.srt")
            if "review_proxy" not in p.name and p.stat().st_size > 0]
    if not srts:
        return {"check": "caption_format", "ok": True, "hard": False, "skipped": True,
                "reason": "no final .srt to format-check"}
    best = max(srts, key=_srt_last_end_seconds)
    blocks = re.split(r"\n\s*\n", best.read_text(encoding="utf-8", errors="ignore").strip())
    viol: list[str] = []
    for b in blocks:
        lines = [ln for ln in b.splitlines() if ln.strip()]
        ts = [ln for ln in lines if "-->" in ln]
        if not ts:
            continue
        body = [ln for ln in lines if "-->" not in ln and not ln.strip().isdigit()]
        if len(body) > MAX_CUE_LINES:
            viol.append(f"{len(body)}lines")
        for ln in body:
            if len(ln) > MAX_LINE_CHARS:
                viol.append(f"{len(ln)}ch")
        mt = re.search(r"(\d\d):(\d\d):(\d\d)[,.](\d{1,3})\s*-->\s*"
                       r"(\d\d):(\d\d):(\d\d)[,.](\d{1,3})", ts[0])
        if mt:
            a = int(mt[1]) * 3600 + int(mt[2]) * 60 + int(mt[3]) + int(mt[4]) / 1000
            z = int(mt[5]) * 3600 + int(mt[6]) * 60 + int(mt[7]) + int(mt[8]) / 1000
            d = z - a
            chars = sum(len(x) for x in body)
            if d > MAX_CUE_SECONDS:
                viol.append(f"{d:.1f}s")
            if d > 0 and chars / d > MAX_CPS:
                viol.append(f"{chars / d:.0f}cps")
    ok = not viol
    head = "; ".join(viol[:6]) + (" ..." if len(viol) > 6 else "")
    return {"check": "caption_format", "ok": ok, "hard": True,
            "reason": (f"{best.name}: {len(viol)} violation(s): {head}" if viol
                       else f"{best.name}: line/duration/cps within limits")}


def _srt_text(p: Path) -> str:
    """All spoken caption text (index + timestamp lines dropped)."""
    out: list[str] = []
    for b in re.split(r"\n\s*\n", p.read_text(encoding="utf-8", errors="ignore").strip()):
        for ln in b.splitlines():
            s = ln.strip()
            if not s or "-->" in s or s.isdigit():
                continue
            out.append(s)
    return " ".join(out)


def _norm_tokens(s: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", s.lower())


def _latest_narration(epdir: Path) -> dict | None:
    """Latest non-proxy narration_index (carries per-chunk spoken_text + section)."""
    cands = [p for p in (epdir / "06_audio").glob("narration_index*.json")
             if "review_proxy" not in p.name]
    return _load(sorted(cands)[-1]) if cands else None


def check_caption_narration_match(epdir: Path) -> dict:
    """HARD: the burned final captions must be the SAME WORDS as the approved
    narration (spoken_text). Catches the EP14 class where a wrong / review-proxy
    .srt is burned in, so the on-screen text does not match the spoken audio --
    the exact 'captions != narration' complaint that caption_format cannot see."""
    nar = _latest_narration(epdir)
    ref = " ".join(c.get("spoken_text", "") for c in (nar or {}).get("chunks") or []).strip()
    srts = [p for p in (epdir / "08_edit").glob("*.srt")
            if "review_proxy" not in p.name and p.stat().st_size > 0]
    if not ref or not srts:
        return {"check": "caption_narration_match", "ok": True, "hard": False, "skipped": True,
                "reason": "no narration spoken_text and/or final .srt to compare"}
    best = max(srts, key=_srt_last_end_seconds)
    ref_t, hyp_t = _norm_tokens(ref), _norm_tokens(_srt_text(best))
    ratio = difflib.SequenceMatcher(None, ref_t, hyp_t, autojunk=False).ratio()
    ok = ratio >= CAPTION_MATCH_MIN
    return {"check": "caption_narration_match", "ok": ok, "hard": True,
            "reason": f"{best.name} vs narration: {ratio * 100:.1f}% token match "
                      f"(min {CAPTION_MATCH_MIN * 100:.0f}%; narration {len(ref_t)}w, "
                      f"captions {len(hyp_t)}w)"}


def check_structure(epdir: Path) -> dict:
    """HARD: the episode must be built HOOK -> OPENING -> body -> ENDING.
    Reads the approved narration section labels (a real artifact, not a
    self-asserted four_part_structure=true bool) and, when the render's
    film-data json exists, confirms it actually carries a cold-open hook."""
    nar = _latest_narration(epdir)
    secs = [str(c.get("section", "")).upper().strip() for c in (nar or {}).get("chunks") or []]
    ordered: list[str] = []
    for s in secs:
        if not ordered or ordered[-1] != s:
            ordered.append(s)
    if not ordered:
        return {"check": "structure_4part", "ok": True, "hard": False, "skipped": True,
                "reason": "no narration sections to check"}
    problems: list[str] = []
    if not ordered[0].startswith(HOOK_SECTION):
        problems.append(f"first section '{ordered[0]}' is not HOOK")
    if not any(s.startswith(OPENING_SECTION) for s in ordered):
        problems.append("no OPENING section")
    elif ordered[0].startswith(HOOK_SECTION) and len(ordered) > 1 \
            and not ordered[1].startswith(OPENING_SECTION):
        problems.append(f"OPENING does not follow HOOK (got '{ordered[1]}')")
    if not any(s.startswith(m) for s in ordered for m in ENDING_MARKERS):
        problems.append("no ENDING/CTA section")
    body = [s for s in ordered if not s.startswith(HOOK_SECTION)
            and not s.startswith(OPENING_SECTION)
            and not any(s.startswith(m) for m in ENDING_MARKERS)]
    if not body:
        problems.append("no body/ACT sections")
    slug = re.sub(r"^PD-\d{4}-\d{3}-", "", epdir.name)
    fdata = ROOT / "remotion" / "src" / "data" / f"{slug}_film.json"
    d = _load(fdata) if fdata.is_file() else None
    if d is not None:
        if (d.get("hookSeconds") or 0) < HOOK_MIN_SEC:
            problems.append(f"film hookSeconds={d.get('hookSeconds')} < {HOOK_MIN_SEC}")
        if not str(d.get("hookLine", "")).strip():
            problems.append("film hookLine empty")
    ok = not problems
    return {"check": "structure_4part", "ok": ok, "hard": True,
            "reason": (f"{' -> '.join(ordered)}" if ok else "; ".join(problems))}


def _resolve_bookends_comp(epdir: Path, cdir: Path) -> Path | None:
    """Resolve the composition .tsx whose OP/ED bookends must be inspected.

    EP32 false-positive fix: a DATA-DRIVEN CaseFilm episode (a
    `remotion/src/data/<slug>_film.json` exists) renders through the shared
    `CaseFilm.tsx` renderer -- so inspect THAT actual renderer, not a slug-named
    file that merely matches. EP32 (slug 'carsearch') added a THUMBNAIL still
    component `CarsearchThumbnails.tsx` which the old slug-glob picked up and, being
    a still, correctly carries no video bookends -> a wrong HARD FAIL.

    Resolution order:
      1. data-driven episode (`<slug>_film.json` present) -> `CaseFilm.tsx`.
      2. else the slug-name heuristic, but EXCLUDING thumbnail still components
         (files ending `Thumbnail.tsx` / `Thumbnails.tsx`) which are stills and
         never carry video bookends, so they can never be mis-picked.
    """
    slug = re.sub(r"^PD-\d{4}-\d{3}-", "", epdir.name)
    fdata = ROOT / "remotion" / "src" / "data" / f"{slug}_film.json"
    if fdata.is_file():
        casefilm = cdir / "CaseFilm.tsx"
        if casefilm.is_file():
            return casefilm
    return next((p for p in cdir.glob("*.tsx")
                 if slug.lower() in p.name.lower()
                 and not re.search(r"thumbnails?\.tsx$", p.name, re.IGNORECASE)), None)


def check_bookends(epdir: Path) -> dict:
    """HARD: OP/ED must be the canonical channel bookends (BrandOpening +
    BrandEndcard from components/Bookends), not a per-episode reinvention.
    For a data-driven CaseFilm episode inspects the real shared renderer
    (CaseFilm.tsx); otherwise resolves the slug-named composition (thumbnail
    stills excluded) and follows one import hop into the shared renderer
    (CaseFilm / CasePremiumFromRoughCut) when the composition delegates to it."""
    slug = re.sub(r"^PD-\d{4}-\d{3}-", "", epdir.name)
    cdir = ROOT / "remotion" / "src" / "compositions"
    comp = _resolve_bookends_comp(epdir, cdir)
    if comp is None:
        return {"check": "op_ed_bookends", "ok": True, "hard": False, "skipped": True,
                "reason": f"no composition matching slug '{slug}'"}
    texts = [comp.read_text(encoding="utf-8", errors="ignore")]
    for dep in ("CaseFilm", "CasePremiumFromRoughCut"):
        if re.search(rf"from '\./{dep}'", texts[0]) and (cdir / f"{dep}.tsx").is_file():
            texts.append((cdir / f"{dep}.tsx").read_text(encoding="utf-8", errors="ignore"))
    blob = "\n".join(texts)
    has_import = "components/Bookends" in blob
    has_open = "BrandOpening" in blob
    has_end = "BrandEndcard" in blob
    ok = has_import and has_open and has_end
    return {"check": "op_ed_bookends", "ok": ok, "hard": True,
            "reason": (f"{comp.name} uses canonical BrandOpening + BrandEndcard"
                       if ok else f"{comp.name}: canonical bookends missing "
                       f"(bookends_import={has_import} opening={has_open} endcard={has_end})")}


def check_leveled_animation(epdir: Path) -> dict:
    """HARD: the composition must actually WIRE IN the leveled-up premium animation, not
    just describe it in the design doc (the recurring "約束を守らない" failure). Verifies the
    episode composition (following the CaseFilm import hop) references: the AmbientMotion
    overlay (no-static-frame), @remotion/motion-blur Trail (real motion blur), and the
    mask-reveal kinetic typography (overflow-hidden + translateY). Skips non-CaseFilm comps."""
    slug = re.sub(r"^PD-\d{4}-\d{3}-", "", epdir.name)
    cdir = ROOT / "remotion" / "src" / "compositions"
    comp = next((p for p in cdir.glob("*.tsx") if slug.lower() in p.name.lower()), None)
    if comp is None:
        return {"check": "leveled_animation", "ok": True, "hard": False, "skipped": True,
                "reason": f"no composition matching slug '{slug}'"}
    texts = [comp.read_text(encoding="utf-8", errors="ignore")]
    is_casefilm = False
    for dep in ("CaseFilm", "CasePremiumFromRoughCut"):
        if re.search(rf"from '\./{dep}'", texts[0]) and (cdir / f"{dep}.tsx").is_file():
            texts.append((cdir / f"{dep}.tsx").read_text(encoding="utf-8", errors="ignore"))
            is_casefilm = True
    if not is_casefilm:
        return {"check": "leveled_animation", "ok": True, "hard": False, "skipped": True,
                "reason": f"{comp.name} is not a CaseFilm episode (leveled-anim check n/a)"}
    blob = "\n".join(texts)
    have = {
        "AmbientMotion": "AmbientMotion" in blob,
        "motion_blur(Trail)": "Trail" in blob and "@remotion/motion-blur" in blob,
        "mask_reveal_typo": ("overflow" in blob and "translateY" in blob),
    }
    missing = [k for k, v in have.items() if not v]
    ok = not missing
    return {"check": "leveled_animation", "ok": ok, "hard": True,
            "reason": ("wired: AmbientMotion + Trail motion-blur + mask-reveal kinetic type"
                       if ok else f"leveled-up animation NOT wired into the render: missing {missing}")}


def check_render_resolution(path: Path) -> dict:
    """Video stream must be >= 1920x1080 (catches a low-res / not-max export)."""
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream=width,height,codec_name", "-of", "json", str(path)],
            capture_output=True, text=True, check=True)
        st = json.loads(out.stdout)["streams"][0]
        w, h = int(st["width"]), int(st["height"])
    except Exception as exc:  # noqa: BLE001
        # EP32 §B1 FAIL-CLOSED: a render whose video stream cannot even be probed is broken,
        # not "fine" -- must FAIL, never a silent pass (mirrors check_motion_energy).
        return {"check": "render_resolution", "ok": False, "hard": True,
                "reason": f"could not probe video stream ({exc}); treat as FAIL, not a silent pass"}
    ok = max(w, h) >= MIN_VIDEO_W and min(w, h) >= MIN_VIDEO_H
    return {"check": "render_resolution", "ok": ok, "hard": True,
            "reason": f"{w}x{h} codec={st.get('codec_name')} (need >= {MIN_VIDEO_W}x{MIN_VIDEO_H})"}


def check_freeze(path: Path) -> dict:
    """No long motionless stretch -> a slideshow of static images / weak animation
    is caught. Tolerates one short designed hold beat."""
    try:
        out = subprocess.run(
            ["ffmpeg", "-hide_banner", "-nostats", "-i", str(path),
             "-vf", f"freezedetect=n=-60dB:d={MAX_FREEZE_S}", "-an", "-f", "null", os.devnull],
            capture_output=True, text=True, check=True, timeout=1200)
    except Exception as exc:  # noqa: BLE001
        # EP32 §B1 FAIL-CLOSED: an ffmpeg that cannot decode the render must FAIL, not pass.
        return {"check": "motion_present", "ok": False, "hard": True,
                "reason": f"freezedetect could not run ({exc}); treat as FAIL, not a silent pass"}
    durs = [float(x) for x in re.findall(r"freeze_duration:\s*(\d+(?:\.\d+)?)", out.stderr)]
    total, longest = sum(durs), (max(durs) if durs else 0.0)
    ok = longest <= MAX_FREEZE_LONGEST_S and total <= MAX_FREEZE_TOTAL_S
    return {"check": "motion_present", "ok": ok, "hard": True,
            "reason": f"frozen total {total:.1f}s / longest {longest:.1f}s "
                      f"(limits {MAX_FREEZE_TOTAL_S:.0f}/{MAX_FREEZE_LONGEST_S:.0f}s; high => static/slideshow)"}


def _png_dims(p: Path) -> tuple[int, int] | None:
    try:
        head = p.open("rb").read(24)
    except Exception:  # noqa: BLE001
        return None
    if head[:8] == b"\x89PNG\r\n\x1a\n":
        return int.from_bytes(head[16:20], "big"), int.from_bytes(head[20:24], "big")
    return None


def check_thumbnail(epdir: Path) -> dict:
    """>=3 thumbnail PNGs at 1280x720 + a selected one must exist."""
    cands = list((epdir / "10_thumbnail").glob("*.png")) + \
            list((epdir / "09_package").glob("thumbnail*.png"))
    good = [p for p in cands if _png_dims(p) == (THUMB_W, THUMB_H)]
    selected = list((epdir / "09_package").glob("thumbnail.selected*.png"))
    ok = len(good) >= MIN_THUMB_VARIANTS and bool(selected)
    return {"check": "thumbnail_ready", "ok": ok, "hard": True,
            "reason": f"{len(good)} thumb(s) at {THUMB_W}x{THUMB_H}, "
                      f"selected={'yes' if selected else 'NO'} "
                      f"(need >={MIN_THUMB_VARIANTS} + selected)"}


def check_black(path: Path) -> dict:
    """No excessive black -> a 'no images'/placeholder render is caught."""
    try:
        out = subprocess.run(
            ["ffmpeg", "-hide_banner", "-nostats", "-i", str(path),
             "-vf", "blackdetect=d=0.5:pic_th=0.98", "-an", "-f", "null", os.devnull],
            capture_output=True, text=True, check=True, timeout=900)
    except Exception as exc:  # noqa: BLE001
        # EP32 §B1 FAIL-CLOSED: an undecodable render must FAIL, not pass as "no black".
        return {"check": "images_present", "ok": False, "hard": True,
                "reason": f"blackdetect could not run ({exc}); treat as FAIL, not a silent pass"}
    spans = re.findall(r"black_duration:(\d+(?:\.\d+)?)", out.stderr)
    durs = [float(x) for x in spans]
    total, longest = sum(durs), (max(durs) if durs else 0.0)
    ok = total <= MAX_TOTAL_BLACK_S and longest <= MAX_SINGLE_BLACK_S
    return {"check": "images_present", "ok": ok, "hard": True,
            "reason": f"black total {total:.1f}s / longest {longest:.1f}s "
                      f"(limits {MAX_TOTAL_BLACK_S:.0f}/{MAX_SINGLE_BLACK_S:.0f})"}


def check_bgm(path: Path) -> dict:
    """No continuous music bed -> the mix is narration-only. A properly bedded
    (and ducked) 4-layer mix has near-zero silence; a narration-only render
    leaves long gaps between sentences (EP14 final = 109s, EP15 proxy = 102s)."""
    try:
        out = subprocess.run(
            ["ffmpeg", "-hide_banner", "-nostats", "-i", str(path),
             "-af", "silencedetect=n=-40dB:d=0.6", "-f", "null", os.devnull],
            capture_output=True, text=True, check=True, timeout=900)
    except Exception as exc:  # noqa: BLE001
        # EP32 §B1 FAIL-CLOSED: if the audio cannot be decoded, we cannot assert a bed exists -> FAIL.
        return {"check": "bgm_present", "ok": False, "hard": True,
                "reason": f"silencedetect could not run ({exc}); treat as FAIL, not a silent pass"}
    sil = [float(x) for x in re.findall(r"silence_duration:\s*(\d+(?:\.\d+)?)", out.stderr)]
    total = sum(sil)
    ok = total <= MAX_TOTAL_SILENCE_S
    return {"check": "bgm_present", "ok": ok, "hard": True,
            "reason": f"total silence {total:.0f}s (limit {MAX_TOTAL_SILENCE_S:.0f}s; "
                      f"high => no continuous BGM bed / narration-only mix)"}


def check_low_motion(path: Path, dur: float, epdir: Path) -> dict:
    """HARD: enough of the BODY frame must actually be MOVING, not merely 'not frozen'.
    `motion_present` (check_freeze) only catches a FULLY frozen frame -- a slow Ken
    Burns zoom or a barely-moving pasted still sails through it, which is exactly
    the '紙芝居 (slideshow)' the owner keeps getting despite the animation promise.
    This raises the freezedetect noise floor so near-still spans are flagged, and
    fails when too much of the BODY is near-still (or one hold runs too long).
    Calibrated on real renders: approved MotionSample ~5.5%; old slideshow ~14.4%.

    Scope (owner-approved 2026-07-05): the canonical brand bookends are DESIGNED-calm and
    are NOT body content, so the gold BrandOpening title region and the trailing BrandEndcard
    outro are excluded from the near-still measurement. Thresholds are UNCHANGED; they now
    apply to the body (hook + acts) where slideshow is the actual risk."""
    try:
        out = subprocess.run(
            ["ffmpeg", "-hide_banner", "-nostats", "-i", str(path),
             "-vf", f"freezedetect=n={LOW_MOTION_NOISE_DB}dB:d={LOW_MOTION_MIN_SPAN_S}",
             "-map", "0:v", "-an", "-f", "null", os.devnull],
            capture_output=True, text=True, check=True, timeout=1800)
    except Exception as exc:  # noqa: BLE001
        # EP32 §B1 FAIL-CLOSED: an undecodable render must FAIL the animation floor, never pass.
        # `check=True` (added to match check_freeze/check_black) turns a NON-ZERO ffmpeg exit -- a
        # decodable-but-broken render whose freezedetect run aborts -- into an exception, so this
        # branch fires instead of silently reading an empty span list as "fully animated".
        return {"check": "animation_density", "ok": False, "hard": True,
                "reason": f"freezedetect could not run ({exc}); treat as FAIL, not a silent pass"}
    starts = [float(x) for x in re.findall(r"freeze_start:\s*([0-9.]+)", out.stderr)]
    lens = [float(x) for x in re.findall(r"freeze_duration:\s*([0-9.]+)", out.stderr)]
    spans = list(zip(starts, lens))
    # EP32 §B1 belt-and-suspenders: at this SENSITIVE noise floor (-38 dB) over a multi-minute
    # render, real content ALWAYS registers SOME near-still spans (held beats, slow Ken Burns,
    # title cards; calibration: MotionSample 5.5%, slideshow 14.4% -- both non-zero). ZERO freeze
    # output on a file that ffprobe independently reports as having real content (dur > 1s) means
    # freezedetect exited 0 but never saw decodable frames -> the measurement is UNMEASURABLE, not
    # "perfectly animated". Fail-closed rather than award a silent pass.
    if not starts and not lens and dur and dur > 1.0:
        return {"check": "animation_density", "ok": False, "hard": True,
                "reason": f"freezedetect produced no spans/starts on a {dur:.0f}s render that ffprobe "
                          f"reports as having content -> unmeasurable animation density; "
                          f"treat as FAIL, not a silent pass"}
    # body = [0, op_lo] (hook) + [op_hi, ed_lo] (acts); OP title + ED outro excluded.
    slug = re.sub(r"^PD-\d{4}-\d{3}-", "", epdir.name)
    fdata = ROOT / "remotion" / "src" / "data" / f"{slug}_film.json"
    fd = _load(fdata) if fdata.is_file() else None
    hook = float((fd or {}).get("hookSeconds") or 0.0)
    op_lo, op_hi = hook, hook + BOOKEND_OP_SEC
    ed_lo = max(op_hi, dur - BOOKEND_ED_SEC)
    body_regions = [(0.0, op_lo), (op_hi, ed_lo)]
    total_lm = 0.0
    longest = 0.0
    for s, d in spans:                                    # keep only each span's BODY portion
        e = s + d
        for blo, bhi in body_regions:
            lo, hi = max(s, blo), min(e, bhi)
            if hi > lo:
                total_lm += hi - lo
                longest = max(longest, hi - lo)
    body_dur = max(1.0, op_lo + (ed_lo - op_hi))
    frac = total_lm / body_dur
    ok = frac <= LOW_MOTION_MAX_FRACTION and longest <= LOW_MOTION_MAX_SPAN_S
    return {"check": "animation_density", "ok": ok, "hard": True,
            "reason": f"BODY near-still {frac * 100:.1f}% ({total_lm:.0f}s over {body_dur:.0f}s body, "
                      f"longest {longest:.1f}s); limits <= {LOW_MOTION_MAX_FRACTION * 100:.0f}% and single <= "
                      f"{LOW_MOTION_MAX_SPAN_S:.0f}s (OP/ED bookends excluded; MotionSample ~5.5%)"}


def _ffprobe_fps(path: Path) -> float:
    """Video stream frame rate (frames/sec) from r_frame_rate, defaulting to 30."""
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream=r_frame_rate", "-of", "default=nw=1:nk=1", str(path)],
            capture_output=True, text=True, check=True)
        txt = out.stdout.strip()
        if "/" in txt:
            num, den = txt.split("/", 1)
            return float(num) / float(den) if float(den) else 30.0
        return float(txt) if txt else 30.0
    except Exception:  # noqa: BLE001
        return 30.0


def check_motion_energy(path: Path, dur: float, epdir: Path) -> dict:
    """HARD: the BODY must carry enough ACTUAL motion, not merely be 'not frozen'.

    animation_density (check_low_motion) only scores the FRACTION of near-still time, so a
    slow Ken Burns zoom / weak parallax that never fully freezes passes it while still reading
    as a slideshow (Goodhart). This measures the real MAGNITUDE of frame movement: the mean
    inter-frame pixel change (ffmpeg tblend=difference -> signalstats YAVG, 0..255) computed
    by scripts/measure_motion_energy.py, over the SAME body definition animation_density uses
    (the gold BrandOpening title region + the trailing BrandEndcard outro are excluded).

    Fails if the body mean YAVG < MOTION_ENERGY_BODY_MEAN_MIN, or (secondary sustained-low
    floor) the body p10 < MOTION_ENERGY_P10_MIN. Calibrated 2026-07-06: MotionSample body
    mean 46.6 / p10 45.2 vs a slideshow episode mean 3.5.

    If ffmpeg / the measurement cannot run, this is a HARD FAIL (a terminal error), never a
    silent pass -- an unmeasurable render must not slip through the motion floor.
    """
    try:
        import importlib.util
        here = Path(__file__).resolve().parent
        spec = importlib.util.spec_from_file_location(
            "measure_motion_energy", str(here / "measure_motion_energy.py"))
        mme = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mme)
        y = mme.per_frame_yavg(str(path))
    except Exception as exc:  # noqa: BLE001
        return {"check": "motion_energy", "ok": False, "hard": True,
                "reason": f"could not measure motion energy ({exc}); "
                          f"treat as FAIL, not a silent pass"}
    if not y:
        return {"check": "motion_energy", "ok": False, "hard": True,
                "reason": "no per-frame YAVG parsed (ffmpeg tblend/signalstats unavailable?); "
                          "treat as FAIL, not a silent pass"}
    fps = _ffprobe_fps(path)
    # BODY = [0, hook] (hook) + [hook+OP, dur-ED] (acts); OP title + ED outro excluded --
    # the SAME body as check_low_motion / animation_density.
    slug = re.sub(r"^PD-\d{4}-\d{3}-", "", epdir.name)
    fdata = ROOT / "remotion" / "src" / "data" / f"{slug}_film.json"
    fd = _load(fdata) if fdata.is_file() else None
    hook = float((fd or {}).get("hookSeconds") or 0.0)
    op_lo, op_hi = hook, hook + BOOKEND_OP_SEC
    ed_lo = max(op_hi, dur - BOOKEND_ED_SEC)
    body_regions = [(0.0, op_lo), (op_hi, ed_lo)]

    # EP32 §M1: cut boundaries from the episode's film-data (else auto-detect YAVG spikes), used to
    # mask +/-CUT_GUARD_FRAMES frames around every hard cut so cut-difference spikes don't inflate
    # the mean. Then compute the WITHIN-SHOT body stats + PER-SEGMENT floor.
    cut_times = mme.cut_times_from_film(fd) or mme.detect_spike_times(y, fps)
    ws_vals = mme.within_shot_values(y, fps, body_regions, cut_times)
    # EP32 §M1: an EMPTY within-shot window means every body frame was masked as a cut -- a
    # pathological hyper-cut that hides the whole body behind cut-difference spikes. The OLD code
    # fell back to stats over the full, spike-INFLATED series and could PASS on that inflation.
    # Fail-closed instead: we cannot verify SUSTAINED motion, so never re-inflate from the unmasked
    # series. Strictly stricter than the former fallback (invariant 15).
    if not ws_vals:
        return {"check": "motion_energy", "ok": False, "hard": True,
                "reason": "within-shot window empty -- cannot verify sustained motion "
                          "(pathological hyper-cut masks the whole body); treat as FAIL, not a "
                          "re-inflated pass from the unmasked series"}
    st = mme.stats(ws_vals)
    mean, p10, p50 = st["mean"], st["p10"], st["p50"]
    segs = mme.segment_means(y, fps, body_regions, cut_times)
    fail_segs = [s for s in segs if s["mean"] < MOTION_ENERGY_SEGMENT_MEAN_MIN]
    problems = []
    if mean < MOTION_ENERGY_BODY_MEAN_MIN:
        problems.append(f"within-shot mean {mean:.1f} < {MOTION_ENERGY_BODY_MEAN_MIN:.0f} (slideshow-flat)")
    if p10 < MOTION_ENERGY_P10_MIN:
        problems.append(f"p10 {p10:.1f} < {MOTION_ENERGY_P10_MIN:.0f} (sustained-low holds)")
    if len(fail_segs) > MOTION_ENERGY_MAX_FAIL_SEGMENTS:
        worst = min(fail_segs, key=lambda s: s["mean"])
        problems.append(f"{len(fail_segs)} body window(s) < {MOTION_ENERGY_SEGMENT_MEAN_MIN:.0f} "
                        f"(worst {worst['mean']:.1f} @ {worst['start']:.0f}s -- dead stretch)")
    ok = not problems
    return {"check": "motion_energy", "ok": ok, "hard": True,
            "body_mean": round(mean, 2), "body_p10": round(p10, 2), "body_p50": round(p50, 2),
            "min_mean": MOTION_ENERGY_BODY_MEAN_MIN, "min_p10": MOTION_ENERGY_P10_MIN,
            "segment_floor": MOTION_ENERGY_SEGMENT_MEAN_MIN, "segments": len(segs),
            "fail_segments": len(fail_segs), "cut_boundaries": len(cut_times),
            "reason": (f"WITHIN-SHOT motion mean {mean:.1f} / p10 {p10:.1f} / p50 {p50:.1f} "
                       f"({st['n']} frames, {len(cut_times)} cuts masked +/-{mme.CUT_GUARD_FRAMES}f; "
                       f"{len(segs)} body windows all >= {MOTION_ENERGY_SEGMENT_MEAN_MIN:.0f}; "
                       f"floors mean >= {MOTION_ENERGY_BODY_MEAN_MIN:.0f}, p10 >= {MOTION_ENERGY_P10_MIN:.0f}; "
                       f"MotionSample 46.6 vs slideshow 3.5)"
                       if ok else "BODY motion too low: " + "; ".join(problems) +
                       f" (MotionSample 46.6 vs slideshow 3.5)")}


def _mean_volume(path: Path, start: float, dur: float) -> float | None:
    """mean_volume (dB) of a [start, start+dur] audio window, or None."""
    out = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-ss", f"{start}", "-t", f"{dur}",
         "-i", str(path), "-map", "0:a:0", "-af", "volumedetect", "-f", "null", os.devnull],
        capture_output=True, text=True)
    m = re.search(r"mean_volume:\s*(-?\d+(?:\.\d+)?) dB", out.stderr)
    return float(m.group(1)) if m else None


def check_bgm_ending(path: Path, dur: float) -> dict:
    """HARD (floor): the ending BGM must NOT be chopped off at full volume -- the
    final ~0.3s must resolve, either to near-silence or clearly below the ending
    body (a fade / a composed cadence). This only catches the jarring hard cut;
    landing on a musical cadence ('切りのいいところ') is enforced by arrangement
    (align the ending cue's own end to the video end) + a manual listen, NOT here.
    Skips when there is no music bed under the tail (nothing to resolve)."""
    if not dur:
        return {"check": "bgm_ending", "ok": True, "hard": False, "skipped": True, "reason": "no duration"}
    body = _mean_volume(path, max(0.0, dur - 2.0), 1.5)   # 1.5s ending 0.5s before the end
    tail = _mean_volume(path, max(0.0, dur - 0.30), 0.30)  # the final 0.30s
    if body is None or tail is None or body < BGM_END_MIN_BODY_DB:
        return {"check": "bgm_ending", "ok": True, "hard": False, "skipped": True,
                "reason": f"no music bed under the tail to resolve (body {body} dB)"}
    drop = body - tail
    resolved = tail <= BGM_END_TAIL_SILENCE_DB or drop >= BGM_END_MIN_DROP_DB
    return {"check": "bgm_ending", "ok": resolved, "hard": True,
            "reason": (f"ending resolves: final 0.3s {tail:.1f} dB vs body {body:.1f} dB "
                       f"(drop {drop:.1f} dB)" if resolved else
                       f"ending HARD-CHOPPED: final 0.3s {tail:.1f} dB ~= body {body:.1f} dB "
                       f"(drop only {drop:.1f} dB; music cut mid-phrase at full volume)")}


def check_hook(epdir: Path, dur: float) -> dict:
    """Soft: runtime must exceed (shotlist body + bookends) enough to hold a hook."""
    sl = _load(epdir / "04_scenes" / "shotlist.v001.json") or {}
    body = (sl.get("totals") or {}).get("estimated_total_seconds")
    if not body:
        return {"check": "hook_added", "ok": True, "hard": False, "skipped": True,
                "reason": "shotlist totals missing"}
    bookends = 12.5  # BrandOpening 3.5 + BrandEndcard 9
    headroom = dur - (body + bookends)
    ok = headroom >= 25.0
    return {"check": "hook_added", "ok": ok, "hard": False,
            "reason": f"runtime exceeds body+bookends by {headroom:.0f}s "
                      f"(need >=25s for hook+breathing; body={body:.0f}s)"}


def check_loudness(path: Path) -> dict:
    try:
        out = subprocess.run(
            ["ffmpeg", "-hide_banner", "-nostats", "-i", str(path),
             "-af", "ebur128=framelog=quiet", "-f", "null", os.devnull],
            capture_output=True, text=True, check=True, timeout=900)
    except Exception as exc:  # noqa: BLE001
        return {"check": "loudness", "ok": True, "hard": False, "skipped": True,
                "reason": f"ebur128 skipped ({exc})"}
    m = re.findall(r"I:\s*(-?\d+(?:\.\d+)?)\s*LUFS", out.stderr)
    if not m:
        return {"check": "loudness", "ok": True, "hard": False, "skipped": True, "reason": "no LUFS parsed"}
    lufs = float(m[-1])
    ok = LUFS_LO <= lufs <= LUFS_HI
    # EP32 MINOR: promoted soft -> HARD. A MEASURED loudness outside [-16,-12] LUFS is a real
    # delivery defect (too quiet / too hot). Only a MEASURED value gates; the un-measurable
    # branches above stay soft (cannot penalize what ffmpeg could not read).
    return {"check": "loudness", "ok": ok, "hard": True,
            "reason": f"integrated {lufs:.1f} LUFS (target -14, band {LUFS_LO}..{LUFS_HI})"}


def _sha256(path: Path) -> str:
    """sha256:<hex> of a file, streamed (used by freshness + receipt)."""
    import hashlib
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def _prior_receipt_sha(epdir: Path) -> tuple[str | None, str | None]:
    """(sha, filename) recorded by the most recent existing acceptance receipt, or (None, None).
    Read BEFORE the new receipt is written, so it is genuinely the PRIOR render's sha."""
    recs = sorted((epdir / "09_package").glob("acceptance_receipt.v*.json"))
    for p in reversed(recs):
        d = _load(p) or {}
        sha = d.get("video_sha256")
        if sha:
            return sha, p.name
    return None, None


def check_freshness(epdir: Path, render: Path, cur_sha: str | None,
                    render_started_at: float | None) -> dict:
    """HARD (EP32 §B2): the render under test must be FRESH, not a stale good file the mixer
    grabbed after a crash (the documented 'crash -> stale green' false-pass). Two signals:
      - sha != prior: the new mp4's sha256 must differ from the last accepted render's sha
        (byte-identical to a previously-graded file => not a real new render).
      - mtime >= render start: if --render-started-at is supplied, the mp4 must have been
        written at/after the render kickoff (authoritative; a stale file predates it).
    With no prior receipt AND no timestamp there is nothing to compare, so it passes with a note
    (still strictly additive -- there was NO freshness gate before)."""
    prev_sha, prev_name = _prior_receipt_sha(epdir)
    try:
        mtime = render.stat().st_mtime
    except Exception as exc:  # noqa: BLE001
        return {"check": "render_freshness", "ok": False, "hard": True,
                "reason": f"could not stat render for freshness ({exc}); treat as FAIL"}
    problems = []
    if render_started_at is not None:
        if mtime < render_started_at:
            problems.append(f"mp4 mtime {mtime:.0f} predates render start {render_started_at:.0f} "
                            f"(stale file, not this render)")
    if prev_sha and cur_sha and cur_sha == prev_sha:
        problems.append(f"sha256 identical to prior receipt {prev_name} "
                        f"(byte-identical to an already-graded render -> not fresh; re-render or "
                        f"pass --render-started-at for a legitimate re-grade)")
    ok = not problems
    if ok:
        bits = []
        if render_started_at is not None:
            bits.append(f"mtime {mtime:.0f} >= start {render_started_at:.0f}")
        bits.append(f"sha {'differs from ' + prev_name if prev_sha else '(no prior receipt to compare)'}")
        reason = "fresh render: " + "; ".join(bits)
    else:
        reason = "; ".join(problems)
    return {"check": "render_freshness", "ok": ok, "hard": True, "reason": reason}


def _astats_rms_windows(path: Path, ss: float, dur: float, extra_af: str = "") -> list[float]:
    """Per-50ms RMS level (dB) windows over [ss, ss+dur] of the first audio stream.
    `extra_af` is prepended (e.g. a highpass) before the windowing/astats chain."""
    chain = (f"{extra_af}," if extra_af else "") + \
        f"aresample=48000,asetnsamples=n={SOUND_WINDOW_SAMPLES}:p=0," \
        "astats=metadata=1:reset=1,ametadata=print:key=lavfi.astats.Overall.RMS_level:file=-"
    out = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-ss", f"{ss}", "-t", f"{dur}",
         "-i", str(path), "-map", "0:a:0", "-af", chain, "-f", "null", os.devnull],
        capture_output=True, text=True, timeout=1200)
    return [float(x) for x in
            re.findall(r"astats\.Overall\.RMS_level=(-?\d+(?:\.\d+)?)", out.stdout + out.stderr)]


def _count_onsets(vals: list[float]) -> int:
    """Onset = a window rising >= SOUND_TRANSIENT_RISE_DB above the trailing-window median and
    above the absolute floor, debounced by SOUND_TRANSIENT_DEBOUNCE_WIN windows."""
    n = len(vals)
    cnt = 0
    last = -10 ** 9
    b = SOUND_TRANSIENT_BASELINE_WIN
    for i in range(b, n):
        window = vals[i - b:i]
        med = sorted(window)[len(window) // 2]
        if (vals[i] - med) >= SOUND_TRANSIENT_RISE_DB and vals[i] >= SOUND_TRANSIENT_FLOOR_DB \
                and (i - last) >= SOUND_TRANSIENT_DEBOUNCE_WIN:
            cnt += 1
            last = i
    return cnt


def _norm_sha(s) -> str:
    """Normalize a sha for comparison: strip an optional 'sha256:' prefix, lowercase, trim."""
    return re.sub(r"^sha256:", "", str(s).strip().lower())


def _ffprobe_tag(path: Path, tag: str) -> str | None:
    """Read a container metadata tag (format-level, then any stream-level) via ffprobe, or None."""
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries",
             f"format_tags={tag}:stream_tags={tag}", "-of", "json", str(path)],
            capture_output=True, text=True, check=True)
        d = json.loads(out.stdout)
    except Exception:  # noqa: BLE001
        return None
    fmt = (d.get("format") or {}).get("tags") or {}
    if tag in fmt and str(fmt[tag]).strip():
        return str(fmt[tag]).strip()
    for st in d.get("streams") or []:
        t = st.get("tags") or {}
        if tag in t and str(t[tag]).strip():
            return str(t[tag]).strip()
    return None


def _sound_mix_binding(epdir: Path, path: Path) -> tuple[list[str], dict]:
    """HARD (EP32 §B5(b)): BIND the render's audio to the BUILT 4-layer mix so an orphaned sound
    plan (mixed but never muxed into the video) cannot pass. Returns (problems, info); any missing
    provenance / mix sha / density-gate / container tag is a fail-closed problem. Reads the
    highest-rev 06_audio/audio_provenance.v*.json and compares its mix sha to a container tag
    `audio_mix_sha256` that the mux stage (build_case_film_mux.py) stamps onto the render."""
    problems: list[str] = []
    info: dict = {}
    provs = sorted((epdir / "06_audio").glob("audio_provenance.v*.json"))
    if not provs:
        problems.append("no 06_audio/audio_provenance.v*.json -- the 4-layer mix was never "
                        "built/registered (build_case_film_audio.py not run); render audio unverifiable")
        return problems, info
    prov = _load(provs[-1]) or {}
    info["provenance"] = provs[-1].name
    # (i) the mix WAV must actually have been rendered and carry a sha to bind against
    prov_sha = (prov.get("mux") or {}).get("audio_source_sha256") or (prov.get("mix") or {}).get("sha256")
    info["provenance_mix_sha"] = prov_sha
    if not prov_sha:
        problems.append(f"{provs[-1].name} has no mux.audio_source_sha256 / mix.sha256 -- the mix WAV "
                        f"was not actually rendered (ran_ffmpeg false); cannot bind the render's audio")
    # (ii) the mix must be a GENUINE 4-layer mix: density gate passes, a continuous music bed, >= N
    #      distinct ambience beds, and >= M distinct MEANINGFUL SFX *files* (variety, filler excluded).
    #      Recalibrated (2026-07-06): richness is proven by DISTINCT FILES here, not by a raw onset
    #      count in the render -- so a filler tick-bed can no longer earn a pass.
    layers = prov.get("layers") or {}
    dg = prov.get("density_gate") or {}
    if dg.get("pass") is not True:
        problems.append(f"audio_provenance density_gate.pass != true ({dg.get('pass')})")
    sfx_count = dg.get("sfx_count")
    if not isinstance(sfx_count, (int, float)) or sfx_count < SOUND_PROV_MIN_SFX:
        problems.append(f"audio_provenance density_gate.sfx_count {sfx_count} < {SOUND_PROV_MIN_SFX}")
    # distinct MEANINGFUL sfx files (layers.sfx.distinct_files counts discrete cue files only, NOT
    # any filler transient_bed) -- the anti-"種類が少なくてしょぼい" variety floor.
    sfx_layer = layers.get("sfx") or {}
    sfx_files = sfx_layer.get("distinct_files")
    info["distinct_sfx_files"] = sfx_files
    if not isinstance(sfx_files, (int, float)) or sfx_files < SOUND_PROV_MIN_SFX_FILES:
        problems.append(f"audio_provenance distinct MEANINGFUL sfx files {sfx_files} < "
                        f"{SOUND_PROV_MIN_SFX_FILES} (too few distinct SFX -- しょぼい/種類が少ない)")
    distinct_beds = dg.get("ambience_distinct_beds")
    if distinct_beds is None:
        distinct_beds = ((layers.get("ambience")) or {}).get("distinct_beds")
    if not isinstance(distinct_beds, (int, float)) or distinct_beds < SOUND_PROV_MIN_BEDS:
        problems.append(f"audio_provenance distinct ambience beds {distinct_beds} < {SOUND_PROV_MIN_BEDS}")
    # continuous music bed present (per-chapter ducked bed covering the body)
    music_layer = layers.get("music") or {}
    music_tracks = music_layer.get("cue_count")
    if music_tracks is None:
        music_tracks = music_layer.get("distinct_tracks")
    info["music_tracks"] = music_tracks
    if not isinstance(music_tracks, (int, float)) or music_tracks < SOUND_PROV_MIN_MUSIC:
        problems.append(f"audio_provenance music bed tracks {music_tracks} < {SOUND_PROV_MIN_MUSIC} "
                        f"(no continuous music layer)")
    # (iii) the RENDER must actually carry THIS mix: a container tag written by the mux stage
    tag = _ffprobe_tag(path, "audio_mix_sha256")
    info["render_audio_mix_tag"] = tag
    if tag is None:
        problems.append("render carries no 'audio_mix_sha256' container tag -- the mux stage "
                        "(build_case_film_mux.py) was NOT run, so the render's audio is not bound to "
                        "the built 4-layer mix (the orphaned-sound-plan failure)")
    elif prov_sha and _norm_sha(tag) != _norm_sha(prov_sha):
        problems.append(f"render audio_mix_sha256 tag {_norm_sha(tag)[:16]}.. != provenance mix sha "
                        f"{_norm_sha(prov_sha)[:16]}.. -- render carries a DIFFERENT/stale audio mix")
    return problems, info


def check_sound_layers(path: Path, dur: float, epdir: Path) -> dict:
    """HARD (EP32 §B5): prove the FINAL RENDER carries the real 4-layer mix (VO + music + ambience
    + SFX), not a lone music bed (the "音が薄い/孤児" failure). TWO parts, BOTH required (AND):
    PART 1 measures the render's audio directly (onset density + ambience-band energy). PART 2
    (_sound_mix_binding) binds the render to the BUILT mix via 06_audio/audio_provenance so an
    orphaned/never-muxed sound plan cannot pass. See the SOUND_* constants for calibration."""
    if not dur:
        return {"check": "sound_layers", "ok": False, "hard": True, "reason": "no duration to analyze"}
    body_hi = max(1.0, dur - BOOKEND_ED_SEC)      # analyze hook+body; drop only the calm endcard tail
    body_dur = body_hi
    try:
        rms = _astats_rms_windows(path, 0.0, body_dur, extra_af="highpass=f=500")
        amb = _mean_volume_af(path, 0.0, body_dur,
                              f"highpass=f={SOUND_AMBIENCE_HP},lowpass=f={SOUND_AMBIENCE_LP}")
    except Exception as exc:  # noqa: BLE001
        # FAIL-CLOSED: an audio track we cannot analyze cannot be certified as a 4-layer mix.
        return {"check": "sound_layers", "ok": False, "hard": True,
                "reason": f"could not analyze render audio ({exc}); treat as FAIL, not a silent pass"}
    if not rms:
        return {"check": "sound_layers", "ok": False, "hard": True,
                "reason": "no audio RMS windows parsed (render has no audio stream?); treat as FAIL"}
    onsets = _count_onsets(rms)
    per_min = onsets / (body_dur / 60.0) if body_dur else 0.0
    problems = []
    if per_min < SOUND_MIN_ONSETS_PER_MIN:
        problems.append(f"onset density {per_min:.1f}/min < {SOUND_MIN_ONSETS_PER_MIN:.0f} "
                        f"(smooth -> a lone music bed with no VO/SFX transients at all)")
    if amb is None or amb < SOUND_AMBIENCE_MIN_DB:
        problems.append(f"ambience band {SOUND_AMBIENCE_HP}-{SOUND_AMBIENCE_LP}Hz "
                        f"{('%.1f dB' % amb) if amb is not None else 'unmeasurable'} "
                        f"< {SOUND_AMBIENCE_MIN_DB:.0f} dB (no sustained bed)")
    # PART 2 -- bind to the built mix (fail-closed on missing provenance / tag / density gate).
    bind_problems, bind_info = _sound_mix_binding(epdir, path)
    problems.extend(bind_problems)
    ok = not problems
    return {"check": "sound_layers", "ok": ok, "hard": True,
            "onsets_per_min": round(per_min, 1),
            "ambience_db": round(amb, 1) if amb is not None else None,
            "provenance": bind_info.get("provenance"),
            "distinct_sfx_files": bind_info.get("distinct_sfx_files"),
            "music_tracks": bind_info.get("music_tracks"),
            "render_audio_mix_tag": bind_info.get("render_audio_mix_tag"),
            "reason": (f"genuine 4-layer mix present & bound: {per_min:.1f} onsets/min "
                       f"(backstop {SOUND_MIN_ONSETS_PER_MIN:.0f}), ambience {amb:.1f} dB "
                       f"(floor {SOUND_AMBIENCE_MIN_DB:.0f}); {bind_info.get('distinct_sfx_files')} distinct "
                       f"SFX files, {bind_info.get('music_tracks')} music tracks; bound to "
                       f"{bind_info.get('provenance')} via audio_mix_sha256 tag" if ok
                       else "render audio not a verified 4-layer mix: " + "; ".join(problems))}


def _mean_volume_af(path: Path, start: float, dur: float, af: str) -> float | None:
    """mean_volume (dB) of [start, start+dur] after applying audio filter `af`, or None."""
    out = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-ss", f"{start}", "-t", f"{dur}",
         "-i", str(path), "-map", "0:a:0", "-af", f"{af},volumedetect", "-f", "null", os.devnull],
        capture_output=True, text=True, timeout=1200)
    m = re.search(r"mean_volume:\s*(-?\d+(?:\.\d+)?) dB", out.stderr)
    return float(m.group(1)) if m else None


def _film_path(epdir: Path) -> Path:
    """Path to the episode's render input <slug>_film.json (may not exist)."""
    slug = re.sub(r"^PD-\d{4}-\d{3}-", "", epdir.name)
    return ROOT / "remotion" / "src" / "data" / f"{slug}_film.json"


def _current_film_sha(epdir: Path) -> str | None:
    """sha256 of the current <slug>_film.json render input, or None if it does not exist."""
    fp = _film_path(epdir)
    try:
        return _sha256(fp) if fp.is_file() else None
    except Exception:  # noqa: BLE001
        return None


def _iso_to_epoch(s) -> float | None:
    """Parse an ISO-8601 timestamp to epoch seconds, or None."""
    if not s:
        return None
    try:
        from datetime import datetime
        return datetime.fromisoformat(str(s).replace("Z", "+00:00")).timestamp()
    except Exception:  # noqa: BLE001
        return None


def check_preflight_receipt(epdir: Path) -> dict:
    """HARD (EP32 §M5): a GREEN pre-render preflight receipt must exist -- acceptance must REFUSE a
    render that was never preflighted. Reads the highest-rev 04_scenes/preflight_receipt.v*.json and
    requires overall pass (render_allowed == true AND verdict == 'GREEN'), i.e. the motion budget /
    asset existence / coverage floors were validated BEFORE the heavy render."""
    recs = sorted((epdir / "04_scenes").glob("preflight_receipt.v*.json"))
    if not recs:
        return {"check": "preflight_receipt", "ok": False, "hard": True,
                "reason": "no 04_scenes/preflight_receipt.v*.json -- run preflight_render_gate.py "
                          "BEFORE rendering; a render that never passed preflight is not acceptable"}
    d = _load(recs[-1]) or {}
    allowed = d.get("render_allowed") is True
    verdict = str(d.get("verdict", "")).upper()
    ok = allowed and verdict == "GREEN"
    return {"check": "preflight_receipt", "ok": ok, "hard": True,
            "reason": (f"{recs[-1].name} verdict={verdict} render_allowed={allowed}"
                       if ok else f"{recs[-1].name} preflight NOT green "
                       f"(verdict={verdict or 'none'} render_allowed={allowed}) -- fix the preflight "
                       f"BLOCK and re-run preflight_render_gate.py before acceptance")}


def check_probe_receipt(epdir: Path, render_started_at: float | None = None,
                        cur_film_sha: str | None = None) -> dict:
    """HARD (EP32 §M6): a 60-90s PROBE receipt (motion_energy + black + freeze on a slice) must
    exist, have PASSED, and be BOUND to THIS render -- so the operator cannot skip the pre-flight
    probe from memory AND a stale probe from an EARLIER render cannot satisfy the gate. Binding
    (either signal proves freshness): the probe receipt's recorded film_sha256 equals the current
    <slug>_film.json sha, OR (fallback) its generated_at is at/after --render-started-at. If neither
    can be shown, FAIL (cannot prove the probe belongs to this render). Produce it with
    `--probe <slice.mp4>` before the full acceptance run."""
    recs = sorted((epdir / "09_package").glob("probe_receipt.v*.json"))
    if not recs:
        return {"check": "probe_receipt", "ok": False, "hard": True,
                "reason": "no 09_package/probe_receipt.v*.json -- run "
                          "`check_final_acceptance.py <ep> --probe <slice.mp4>` on a 60-90s slice first"}
    d = _load(recs[-1]) or {}
    problems: list[str] = []
    if d.get("status") != "PASS":
        problems.append(f"status={d.get('status')} (probe did not pass)")
    # Binding: prove this probe corresponds to THIS render, not a stale earlier one.
    rec_film = d.get("film_sha256")
    bound_by = None
    if cur_film_sha and rec_film:
        if _norm_sha(rec_film) == _norm_sha(cur_film_sha):
            bound_by = "film_sha256"
        else:
            problems.append(f"probe film_sha256 {_norm_sha(rec_film)[:16]}.. != current film.json "
                            f"{_norm_sha(cur_film_sha)[:16]}.. (stale probe from an earlier render)")
    if bound_by is None and render_started_at is not None:
        ts = _iso_to_epoch(d.get("generated_at"))
        if ts is not None and ts >= render_started_at:
            bound_by = "generated_at>=render_start"
        else:
            problems.append(f"probe generated_at {d.get('generated_at')} predates --render-started-at "
                            f"{render_started_at:.0f} (stale probe, not this render)")
    if bound_by is None and not problems:
        # Passed + present, but nothing proves it belongs to THIS render -> fail-closed (the stale
        # probe hole). Re-run --probe on the current render's slice (stamps film_sha256) or supply
        # --render-started-at.
        problems.append("cannot bind probe to this render: receipt has no film_sha256 and no "
                        "--render-started-at supplied -- re-run --probe on the current render's slice")
    ok = not problems
    return {"check": "probe_receipt", "ok": ok, "hard": True,
            "reason": (f"{recs[-1].name} status=PASS bound_by={bound_by} "
                       f"(motion/black/freeze on {d.get('slice_seconds', '?')}s slice)"
                       if ok else f"{recs[-1].name}: " + "; ".join(problems))}


def run_probe(epdir: Path, slice_path: Path) -> int:
    """--probe mode: run motion_energy + black + freeze on a short slice and write an immutable
    probe receipt (EP32 §M6). Returns process exit code (0 = probe PASS)."""
    if not slice_path.is_file():
        raise SystemExit(f"probe slice not found: {slice_path}")
    sdur = 0.0
    try:
        sdur = ffprobe_duration(slice_path)
    except Exception:  # noqa: BLE001
        pass
    me = check_motion_energy(slice_path, sdur, epdir)
    bk = check_black(slice_path)
    fz = check_freeze(slice_path)
    results = [me, bk, fz]
    status = "PASS" if all(r["ok"] for r in results) else "FAIL"
    from datetime import datetime, timezone
    receipt = {
        "schema_version": "1.0.0", "episode_id": epdir.name, "gate": "check_final_acceptance.probe",
        "status": status, "slice_path": str(slice_path), "slice_seconds": round(sdur, 2),
        "slice_sha256": _sha256(slice_path),
        # EP32 §M6: bind this probe to the render's plan so a stale probe from an EARLIER render
        # cannot satisfy check_probe_receipt -- record the current <slug>_film.json sha.
        "film_sha256": _current_film_sha(epdir),
        "results": {r["check"]: {"ok": r["ok"], "reason": r["reason"]} for r in results},
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    outp = _next_version_path(epdir / "09_package", "probe_receipt", ".json")
    outp.parent.mkdir(parents=True, exist_ok=True)
    outp.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    try:
        disp = outp.relative_to(ROOT)
    except ValueError:
        disp = outp
    print(f"PROBE {disp}  status={status} ({sdur:.0f}s slice)")
    for r in results:
        print(f"  {'PASS' if r['ok'] else 'FAIL'} {r['check']}: {r['reason']}")
    return 0 if status == "PASS" else 1


def _next_version_path(dirp: Path, stem: str, ext: str) -> Path:
    """Next free immutable path <dir>/<stem>.v{NNN}<ext> (EP32 MINOR: never overwrite v001)."""
    existing = sorted(dirp.glob(f"{stem}.v*{ext}"))
    nxt = 1
    for p in existing:
        m = re.search(rf"{re.escape(stem)}\.v(\d+){re.escape(ext)}$", p.name)
        if m:
            nxt = max(nxt, int(m.group(1)) + 1)
    return dirp / f"{stem}.v{nxt:03d}{ext}"


def check_image_resolution(epdir: Path) -> dict:
    """Spec row 5: every hero still must be 4K-grade (long edge >= 3840 px).
    Catches 'images are coarse / low quality'. Reads staged PNGs in
    remotion/public/<slug> (factory overlays excluded)."""
    slug = re.sub(r"^PD-\d{4}-\d{3}-", "", epdir.name)
    pub = ROOT / "remotion" / "public" / slug
    pngs = list(pub.glob("*.png")) if pub.is_dir() else []
    if not pngs:
        return {"check": "image_resolution", "ok": True, "hard": True, "skipped": True,
                "reason": f"no hero PNGs staged in remotion/public/{slug}"}
    low = []
    for p in pngs:
        dim = _png_dims(p)
        if dim and max(dim) < IMG_MIN_LONG_EDGE:
            low.append(f"{p.name}={dim[0]}x{dim[1]}")
    ok = not low
    return {"check": "image_resolution", "ok": ok, "hard": True,
            "reason": (f"{len(pngs)} hero PNGs, all long-edge >= {IMG_MIN_LONG_EDGE}px"
                       if ok else f"{len(low)}/{len(pngs)} below {IMG_MIN_LONG_EDGE}px: {low[:4]}")}


def check_factory_used(epdir: Path, render_dur: float | None) -> dict:
    """Spec row 7: the downloaded factory shelf must actually be used as the
    decoration layer. Catches 'downloaded assets barely used'. Requires the
    factory dir to be non-empty AND referenced by the composition, with at least
    one distinct clip per ~45s of runtime."""
    slug = re.sub(r"^PD-\d{4}-\d{3}-", "", epdir.name)
    fdir = ROOT / "remotion" / "public" / slug / "factory"
    n = len([p for p in fdir.rglob("*") if p.is_file()]) if fdir.is_dir() else 0
    comp = next((p for p in (ROOT / "remotion" / "src" / "compositions").glob("*.tsx")
                 if slug.lower() in p.name.lower()), None)
    referenced = bool(comp and "factory" in comp.read_text(encoding="utf-8", errors="ignore").lower())
    # Data-driven episodes use the generic CaseFilm.tsx + <slug>_film.json, so the factory
    # clips are referenced in the built cutlist (src "<slug>/factory/..."), not a per-slug
    # .tsx. Accept that as a valid reference too (same source of truth as footage_diversity).
    if not referenced:
        fdata_fu = ROOT / "remotion" / "src" / "data" / f"{slug}_film.json"
        dfu = _load(fdata_fu) if fdata_fu.is_file() else None
        if dfu:
            referenced = any("/factory/" in str(c.get("src", "")) for c in dfu.get("cuts", []))
    need = max(1, int((render_dur or 0) // FACTORY_SECONDS_PER_CLIP)) if render_dur else 1
    ok = n >= need and referenced
    return {"check": "factory_used", "ok": ok, "hard": True,
            "reason": f"{n} factory clip(s) staged, referenced_in_composition={referenced}, "
                      f"need >= {need} (1 per {FACTORY_SECONDS_PER_CLIP}s)"}


def check_footage_diversity(epdir: Path) -> dict:
    """HARD: the shelf must be used with VARIETY -- not the same few clips (esp.
    generic symbols like the scales of justice) on repeat. Owner 2026-07-04:
    "毎作品同じ素材が使われてる ... 天秤の動画は何度も見てきた". Reads the built
    film-data cutlist and fails when any clip is reused too often, when a generic
    symbol recurs, or when the distinct/total ratio is too low (lazy small pool)."""
    slug = re.sub(r"^PD-\d{4}-\d{3}-", "", epdir.name)
    fdata = ROOT / "remotion" / "src" / "data" / f"{slug}_film.json"
    d = _load(fdata) if fdata.is_file() else None
    cuts = (d or {}).get("cuts") or []
    if not cuts:
        return {"check": "footage_diversity", "ok": True, "hard": False, "skipped": True,
                "reason": "no film-data cutlist to check"}
    from collections import Counter
    c = Counter(x.get("src", "") for x in cuts)
    total = len(cuts)
    distinct = len(c)
    frac = distinct / total if total else 0.0
    top_src, top_n = c.most_common(1)[0]
    over = [(s, n) for s, n in c.items() if n > FOOTAGE_MAX_USES_PER_CLIP]
    generic = [(s, n) for s, n in c.items()
               if re.search(FOOTAGE_GENERIC_PAT, s, re.I) and n > FOOTAGE_GENERIC_MAX_USES]
    problems = []
    if frac < FOOTAGE_MIN_DISTINCT_FRACTION:
        problems.append(f"distinct {frac:.2f} < {FOOTAGE_MIN_DISTINCT_FRACTION:.2f}")
    if over:
        problems.append(f"{len(over)} clip(s) reused > {FOOTAGE_MAX_USES_PER_CLIP}x "
                        f"(worst {top_src.split('/')[-1][:28]}={top_n})")
    if generic:
        problems.append(f"{len(generic)} generic symbol(s) reused > {FOOTAGE_GENERIC_MAX_USES}x: "
                        f"{[s.split('/')[-1][:20] for s, _ in generic][:3]}")
    ok = not problems
    return {"check": "footage_diversity", "ok": ok, "hard": True,
            "reason": (f"{distinct}/{total} distinct ({frac:.2f}), max reuse {top_n} -- varied"
                       if ok else "; ".join(problems))}


def check_thumbnail_visibility(epdir: Path) -> dict:
    """HARD: the SELECTED thumbnail must be bright/punchy, not a dull dark panel --
    the "しょぼい / 全く派手じゃない / CTRが下がる" reject class. Measures the newest
    selected thumbnail's mean luma + contrast. Calibrated 2026-07-04: rejected dark
    v001 = mean 24.9-29.5; approved bright v002 = 36.4-48.0."""
    sel = sorted((epdir / "09_package").glob("thumbnail.selected*.png"))
    if not sel:
        return {"check": "thumbnail_visibility", "ok": True, "hard": False, "skipped": True,
                "reason": "no selected thumbnail to measure"}
    thumb = sel[-1]
    try:
        from PIL import Image, ImageStat
        im = Image.open(thumb).convert("L")
        st = ImageStat.Stat(im)
        mean, std = st.mean[0], st.stddev[0]
    except Exception as exc:  # noqa: BLE001
        return {"check": "thumbnail_visibility", "ok": True, "hard": False, "skipped": True,
                "reason": f"luma probe skipped ({exc})"}
    problems = []
    if mean < THUMB_MIN_MEAN_LUMA:
        problems.append(f"mean luma {mean:.1f} < {THUMB_MIN_MEAN_LUMA:.0f} (too dark/dull)")
    if std < THUMB_MIN_CONTRAST_STD:
        problems.append(f"contrast {std:.1f} < {THUMB_MIN_CONTRAST_STD:.0f} (too flat)")
    ok = not problems
    return {"check": "thumbnail_visibility", "ok": ok, "hard": True,
            "reason": (f"{thumb.name}: mean luma {mean:.1f}, contrast {std:.1f} -- bright/punchy"
                       if ok else f"{thumb.name}: " + "; ".join(problems))}


def resolve_render(epdir: Path, override: str | None) -> Path | None:
    if override:
        return Path(override)
    fd = sorted(epdir.glob("09_package/final_delivery.v*.json"))
    for p in reversed(fd):
        d = _load(p) or {}
        fv = d.get("final_video")
        if fv:
            return Path(fv.replace("file://", ""))
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description="Independently verify a final render is publish-grade.")
    ap.add_argument("episode", help="episode number or id")
    ap.add_argument("--render", help="explicit path to the final .mp4 (else from final_delivery)")
    ap.add_argument("--json", action="store_true", help="emit JSON")
    ap.add_argument("--emit-receipt", action="store_true",
                    help="on completion write 09_package/acceptance_receipt.v{NNN}.json (next free "
                         "immutable version) binding PASS/FAIL to the exact render sha256 (the "
                         "scheduler REQUIRES a green receipt)")
    ap.add_argument("--probe", metavar="SLICE_MP4",
                    help="EP32 §M6: run motion_energy+black+freeze on a 60-90s slice and write an "
                         "immutable probe receipt, then exit (the full run REQUIRES a green probe)")
    ap.add_argument("--render-started-at", type=float, default=None,
                    help="EP32 §B2: epoch seconds of render kickoff; the mp4 mtime must be >= this "
                         "(freshness -- rejects a stale good file grabbed after a crash)")
    args = ap.parse_args()

    ep = resolve_episode(args.episode)
    epdir = EPDIR / ep

    # EP32 §M6 probe mode: measure a short slice, write the probe receipt, exit.
    if args.probe:
        return run_probe(epdir, Path(args.probe))

    render = resolve_render(epdir, args.render)
    render_dur = None
    render_sha = None
    results: list[dict] = []

    # sha256 of the render, computed ONCE (reused by freshness + the receipt).
    if render and render.is_file():
        try:
            render_sha = _sha256(render)
        except Exception:  # noqa: BLE001
            render_sha = None

    # media checks (only if the render is reachable)
    if render and render.is_file():
        try:
            render_dur = ffprobe_duration(render)
            lo, hi = runtime_band(epdir)
            results.append(check_runtime(render_dur, lo, hi))
            results.append(check_render_resolution(render))
            results.append(check_freshness(epdir, render, render_sha, args.render_started_at))
            results.append(check_black(render))
            results.append(check_freeze(render))
            results.append(check_low_motion(render, render_dur, epdir))
            results.append(check_motion_energy(render, render_dur, epdir))
            results.append(check_bgm(render))
            results.append(check_sound_layers(render, render_dur, epdir))
            results.append(check_bgm_ending(render, render_dur))
            results.append(check_hook(epdir, render_dur))
            results.append(check_loudness(render))
            results.append(check_probe_receipt(epdir, args.render_started_at, _current_film_sha(epdir)))
        except Exception as exc:  # noqa: BLE001
            results.append({"check": "render_probe", "ok": False, "hard": True,
                            "reason": f"could not probe render {render}: {exc}"})
    else:
        results.append({"check": "render_present", "ok": False, "hard": True,
                        "reason": f"final render not found (looked at {render}); "
                                  f"render the episode's *Premium final before acceptance"})

    # in-repo provenance / packaging checks (always)
    results.append(check_voice(epdir))
    results.append(check_captions(epdir, render_dur))
    results.append(check_caption_format(epdir))
    results.append(check_caption_narration_match(epdir))
    results.append(check_structure(epdir))
    results.append(check_bookends(epdir))
    results.append(check_leveled_animation(epdir))
    results.append(check_preflight_receipt(epdir))
    results.append(check_thumbnail(epdir))
    results.append(check_thumbnail_visibility(epdir))
    results.append(check_image_resolution(epdir))
    results.append(check_factory_used(epdir, render_dur))
    results.append(check_footage_diversity(epdir))

    hard_fail = [r for r in results if r["hard"] and not r["ok"]]
    soft_fail = [r for r in results if not r["hard"] and not r["ok"]]
    status = "PASS" if not hard_fail else "FAIL"

    report = {"check": "final_acceptance", "episode": ep,
              "render": str(render) if render else None,
              "render_duration_seconds": round(render_dur, 2) if render_dur else None,
              "status": status, "results": results}
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"FINAL ACCEPTANCE - {ep}")
        print(f"render: {render}  ({render_dur:.1f}s)" if render_dur else f"render: {render}")
        for r in results:
            mark = "PASS" if r["ok"] else ("FAIL" if r["hard"] else "warn")
            tag = "[hard]" if r["hard"] else "[soft]"
            print(f"  {mark:4} {tag} {r['check']}: {r['reason']}")
        print(f"\nRESULT: {status}" + (f"  ({len(soft_fail)} soft warning(s))" if soft_fail else ""))

    # Emit a receipt binding this PASS/FAIL to the EXACT render bytes. The scheduler
    # refuses to upload without a green receipt whose video_sha256 matches the file --
    # so a video that did not pass this gate physically cannot be scheduled.
    if args.emit_receipt:
        from datetime import datetime, timezone
        vsha = render_sha if (render and render.is_file()) else None
        receipt = {
            "schema_version": "1.0.0", "episode_id": ep, "gate": "check_final_acceptance",
            "status": status, "video_path": str(render) if render else None,
            "video_sha256": vsha, "hard_failures": [r["check"] for r in hard_fail],
            "checks": {r["check"]: r["ok"] for r in results},
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }
        # Record the MEASURED motion energy (not just pass/fail) so the receipt carries the
        # actual dynamism numbers the gate decided on (EP32 §5 motion_energy floor).
        me = next((r for r in results if r["check"] == "motion_energy"), None)
        if me is not None:
            receipt["motion_energy"] = {
                "ok": me["ok"],
                "body_mean": me.get("body_mean"), "body_p10": me.get("body_p10"),
                "body_p50": me.get("body_p50"),
                "min_mean": me.get("min_mean", MOTION_ENERGY_BODY_MEAN_MIN),
                "min_p10": me.get("min_p10", MOTION_ENERGY_P10_MIN),
            }
        # EP32 MINOR: immutable versioning -- never overwrite v001; write the next free v{NNN}.
        rp = _next_version_path(epdir / "09_package", "acceptance_receipt", ".json")
        rp.parent.mkdir(parents=True, exist_ok=True)
        rp.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"RECEIPT {rp.relative_to(ROOT)}  status={status} sha={'set' if vsha else 'none'}")
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
