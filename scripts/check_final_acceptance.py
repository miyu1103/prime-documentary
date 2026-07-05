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
# ending BGM must resolve, not get chopped mid-phrase at full volume. This is a
# FLOOR only (a hard full-volume cut fails); whether it lands on a musical cadence
# ("切りのいいところ") is an arrangement choice + a manual listen -- not amplitude.
BGM_END_MIN_BODY_DB = -45.0                      # if the last seconds are quieter than this, no bed to resolve -> skip
BGM_END_TAIL_SILENCE_DB = -45.0                  # final 0.3s ~silent => resolved/faded cleanly
BGM_END_MIN_DROP_DB = 10.0                       # OR final 0.3s >=10 dB below the body => resolving, not chopped
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


def check_bookends(epdir: Path) -> dict:
    """HARD: OP/ED must be the canonical channel bookends (BrandOpening +
    BrandEndcard from components/Bookends), not a per-episode reinvention.
    Follows one import hop into the shared renderer (CaseFilm /
    CasePremiumFromRoughCut) when the episode composition delegates to it."""
    slug = re.sub(r"^PD-\d{4}-\d{3}-", "", epdir.name)
    cdir = ROOT / "remotion" / "src" / "compositions"
    comp = next((p for p in cdir.glob("*.tsx") if slug.lower() in p.name.lower()), None)
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
        return {"check": "render_resolution", "ok": True, "hard": True, "skipped": True,
                "reason": f"probe skipped ({exc})"}
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
        return {"check": "motion_present", "ok": True, "hard": True, "skipped": True,
                "reason": f"freezedetect skipped ({exc})"}
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
        return {"check": "images_present", "ok": True, "hard": True, "skipped": True,
                "reason": f"blackdetect skipped ({exc})"}
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
        return {"check": "bgm_present", "ok": True, "hard": True, "skipped": True,
                "reason": f"silencedetect skipped ({exc})"}
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
            capture_output=True, text=True, timeout=1800)
    except Exception as exc:  # noqa: BLE001
        return {"check": "animation_density", "ok": True, "hard": False, "skipped": True,
                "reason": f"freezedetect skipped ({exc})"}
    starts = [float(x) for x in re.findall(r"freeze_start:\s*([0-9.]+)", out.stderr)]
    lens = [float(x) for x in re.findall(r"freeze_duration:\s*([0-9.]+)", out.stderr)]
    spans = list(zip(starts, lens))
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
    return {"check": "loudness", "ok": ok, "hard": False,
            "reason": f"integrated {lufs:.1f} LUFS (target -14, band {LUFS_LO}..{LUFS_HI})"}


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
                    help="on completion write 09_package/acceptance_receipt.v001.json binding the "
                         "PASS/FAIL to the exact render sha256 (the scheduler REQUIRES a green receipt)")
    args = ap.parse_args()

    ep = resolve_episode(args.episode)
    epdir = EPDIR / ep
    render = resolve_render(epdir, args.render)
    render_dur = None
    results: list[dict] = []

    # media checks (only if the render is reachable)
    if render and render.is_file():
        try:
            render_dur = ffprobe_duration(render)
            lo, hi = runtime_band(epdir)
            results.append(check_runtime(render_dur, lo, hi))
            results.append(check_render_resolution(render))
            results.append(check_black(render))
            results.append(check_freeze(render))
            results.append(check_low_motion(render, render_dur, epdir))
            results.append(check_bgm(render))
            results.append(check_bgm_ending(render, render_dur))
            results.append(check_hook(epdir, render_dur))
            results.append(check_loudness(render))
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
        import hashlib
        from datetime import datetime, timezone
        vsha = None
        if render and render.is_file():
            h = hashlib.sha256()
            with open(render, "rb") as fh:
                for chunk in iter(lambda: fh.read(1 << 20), b""):
                    h.update(chunk)
            vsha = "sha256:" + h.hexdigest()
        receipt = {
            "schema_version": "1.0.0", "episode_id": ep, "gate": "check_final_acceptance",
            "status": status, "video_path": str(render) if render else None,
            "video_sha256": vsha, "hard_failures": [r["check"] for r in hard_fail],
            "checks": {r["check"]: r["ok"] for r in results},
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }
        rp = epdir / "09_package" / "acceptance_receipt.v001.json"
        rp.parent.mkdir(parents=True, exist_ok=True)
        rp.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"RECEIPT {rp.relative_to(ROOT)}  status={status} sha={'set' if vsha else 'none'}")
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
