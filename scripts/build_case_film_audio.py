#!/usr/bin/env python3
r"""Build the REAL narration-timed 4-layer audio mix for a PD case film.

WHY THIS FILE EXISTS (5-critic review, EP32 remediation defects B5/B6/M3/M4)
---------------------------------------------------------------------------
``scripts/build_case_sound_design.py`` produces a sound *plan* that is an
ORPHAN: it is never muxed into the render, its SFX are timed by a flat
175-wpm GUESS (so a cue meant for a specific word drifts), its ambience is one
looped file ducked into inaudibility, and no hard gate checks the render's
layers. This tool fixes all four, reusing the proven flash-crash pattern
(``scripts/build_flashcrash_audio_v001.py`` -- "reuses already-generated
ElevenLabs chunk files, builds a 4-layer mix", CLAUDE invariant 14: extend,
don't reinvent) and salvaging the SFX / ambience / music library maps from
``build_case_sound_design.py`` (invariant 14 again).

WHAT IT DOES
------------
Reads the REAL per-chunk narration timing from
``episodes/<ep>/06_audio/narration_index.v001.json`` (verbatim spoken text +
``estimated_duration_seconds`` per VC chunk) and the ``(SFX:)`` parentheticals
embedded in ``episodes/<ep>/03_script/script.en.v001.md``, then:

  B6  Places every SFX cue at an offset DERIVED FROM THE NARRATION INDEX, not a
      wpm guess. Each script beat ([VO:] line) is matched to its owning VC chunk
      by alnum-token equality (chunk text == concatenation of its beats). Within
      the chunk, the cue is placed by TOKEN POSITION: a quoted trigger such as
      (SFX: ... on "hundred years.") is located in the chunk's spoken tokens and
      the cue lands on that word; with no quoted trigger the cue lands at the
      beat's token offset inside the chunk. time = chunk_start + (tok/total)*dur.
      Per-chunk audio files are preferred (MEASURED duration) when present; else
      the index's estimated durations are used (recorded as an estimate).

  M3  Assigns a DISTINCT ambience bed per chapter/location (courtroom / office /
      institutional / night / road / hallway -- the six real beds, not one file
      everywhere), at a ~-18 dB floor, and CAPS ducking: the ambience bed is a
      constant weighted layer (NOT sidechained), so it stays audible under VO.
      The density gate scores ambience DISTINCTNESS, not just coverage.

  M4  One ``(SFX:)`` parenthetical == one cue by default; it is only split into a
      sequence on explicit sequencing words (``;`` ``then`` ``into`` ``->``), NOT
      on commas (the old double-hit bug). Identical files firing within ~0.5 s are
      de-duped. Atmospheric-swell cues ("bed/hum/pulse/swell/ambient/drone/...")
      are ROUTED to a temporary Layer-3 gain automation (a timed volume bump on
      the ambience bed) instead of being discarded.

  B5  Emits the final 4-layer mix as ONE WAV (narration front; music ducked via
      sidechain; ambience an audible constant bed; SFX one-shots; two-pass
      loudnorm I=-14) AND a provenance JSON recording the mix sha + full layer
      inventory (SFX count, distinct ambience beds, music cues, loudnorm), so
      ``scripts/check_final_acceptance.py``'s check_sound_layers can verify the
      render actually used it.

HOW THIS WAV BECOMES THE EPISODE'S SOLE AUDIO IN THE FINAL MUX
-------------------------------------------------------------
The Remotion/CaseFilm video is rendered WITHOUT audio (or its audio is dropped).
The final deliverable is muxed as:

    ffmpeg -y -i <case_film_video.mp4> -i <this_mix.wav> \
        -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 320k -ar 48000 \
        -shortest <final.mp4>

Because only ``1:a:0`` (this WAV) is mapped, this mix is the ONLY audio in the
final file. The provenance JSON's ``mux`` block records that command and the WAV
uri/sha so the acceptance gate can confirm the shipped audio == this mix.

SIDE EFFECTS / SAFETY
---------------------
No network, no paid API, no GPU, no video render. Writes exactly one small
in-repo provenance JSON always (atomic temp+rename). Writes the mix WAV to the
SSD media root ONLY when ``--render`` is passed, all inputs exist, and
``--dry-run`` is absent. ``--dry-run`` emits the ffmpeg command + provenance
WITHOUT requiring the narration master to exist (only narration_index does).
Deterministic/idempotent: no wall-clock in the output; provenance keyed on input
hashes; numbers rounded to 3 decimals; cues sorted. Windows paths use pathlib /
raw strings (past ``\\Users`` unicode-escape crash).

SELF-TEST (dry-run on EP32):
    ./.venv/Scripts/python.exe scripts/build_case_film_audio.py \
        --ep PD-2026-032-carsearch --dry-run
"""
from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import math
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parents[1]

SCHEMA_VERSION = "1.0.0"
GENERATOR = "scripts/build_case_film_audio.py"
REVISION_DEFAULT = "v001"
FPS = 30

# ---- video-timeline bookends (SYNC FIX) ------------------------------------
# The CaseFilm render (remotion/src/compositions/CaseFilm.tsx) lays out:
#   Hook[0, hookSeconds] -> Opening[hookSeconds, hookSeconds+OPENING_SEC]
#   -> Body[lead, lead+narrationSeconds] -> Endcard[.., +ENDCARD_SEC]
#   where lead = hookSeconds + OPENING_SEC.
# The narration audio + burned captions + moving-diagram figures ALL live in the
# Body, offset by `lead`. So this mix MUST place the whole 4-layer body at `lead`
# and fill the hook/opening lead + endcard tail; otherwise the narration plays
# ~lead seconds too early and drifts ahead of every caption/figure (the owner's
# #1 failure: caption != narration).
# OPENING_SEC / ENDCARD_SEC are exported from remotion/src/components/Bookends.tsx
#   ("export const OPENING_SEC = 3.5;" / "export const ENDCARD_SEC = 9;").
OPENING_SEC = 3.5
ENDCARD_SEC = 9.0

# hook/opening intro + endcard outro fills (no VO in these regions, so no ducking
# needed and the bed can sit a touch louder than the ducked body bed).
INTRO_MUSIC_VOL = 0.30       # hook->opening bed that builds into the body
OUTRO_MUSIC_VOL = 0.26       # endcard bed, gently resolving
RISER_FILL = ("sfx_riser_2s.mp3", 2.0, 0.24)  # optional riser landing on body start (lead)

# ---- outro fade-out (bgm_ending HARD gate: no hard chop) --------------------
# The final deliverable is muxed with `-shortest`, so the muxed video is ~1-1.5s
# SHORTER than this mix (body_len carries a TAIL_SEC=1.5 air the video Body does
# not). If the outro fade ends AT the mix end it is TRIMMED away, leaving the
# ending music at near-full volume -> check_final_acceptance.check_bgm_ending
# reports a HARD-CHOP. Fix: the outro must ramp fully to silence and COMPLETE the
# fade OUTRO_FADE_END_MARGIN seconds BEFORE the mix end, a margin larger than the
# `-shortest` trim, so the last seconds of the shipped video are genuinely quiet
# (a clean 切りのいい fade, never a chop) no matter where the trim lands.
OUTRO_FADE_DUR = 3.0          # ending music ramps down to silence over 3.0s
OUTRO_FADE_END_MARGIN = 3.5   # fade is DONE this many sec before the mix end (> the ~1-1.5s -shortest trim)

# ---- timeline model --------------------------------------------------------
# Chunk starts are the CUMULATIVE narration-index durations (measured per-chunk
# audio when it exists, else the index's estimated_duration_seconds). This
# anchors every SFX to the real narrated word instead of a flat wpm guess.
INTER_CHUNK_GAP = 0.0     # keep the timeline == the index's own total (no drift)
TAIL_SEC = 1.5            # air after the last word

# ---- density gate floors (anti-"しょぼい") ---------------------------------
SFX_TOTAL_FLOOR = 20            # de-duped SFX one-shots minimum
SFX_PER_MIN_FLOOR = 2.0        # de-duped SFX per minute minimum
AMBIENCE_COVERAGE_FLOOR = 0.85  # fraction of runtime under an ambience bed
AMBIENCE_DISTINCT_FLOOR = 4     # M3: distinct beds used (of 6) -- distinctness, not just coverage

# ---- layer gains -----------------------------------------------------------
NARRATION_VOL = 1.0
MUSIC_VOL = 0.22               # ducked bed
AMBIENCE_FLOOR_DB = -18.0      # M3: audible bed floor
SWELL_BUMP = 0.6              # multiplicative L3 gain bump during an atmos swell
SWELL_DUR_DEFAULT = 2.8       # seconds a routed swell holds

DEDUP_WINDOW_SEC = 0.5        # M4: drop identical file within this window

# final amix weights: VO front, music ducked, ambience audible constant bed, sfx
FINAL_WEIGHTS = "1 0.90 0.80 0.95"

# ---- chapter -> layer-2 music slot (salvaged from build_case_sound_design) --
CHAPTER_MUSIC: dict[str, tuple[str, str, str]] = {
    "hook":    ("hook",      "hook",          "mus_20260614_hook_glass_air_bed_v2.mp3"),
    "opening": ("opening",   "opening",       "mus_20260614_opening_measured_arpeggio_v2.mp3"),
    "act1":    ("tension",   "tension_build", "mus_20260614_tension_build_courtroom_horizon_v2.mp3"),
    "act2":    ("explainer", "explainer_bed", "mus_20260614_explainer_bed_soft_explainer_v2.mp3"),
    "act3":    ("reveal",    "reveal",        "mus_20260614_reveal_verdict_at_dawn_v2.mp3"),
    "act4":    ("somber",    "somber",        "mus_20260614_somber_ledger_of_ash_v2.mp3"),
    "ending":  ("outro",     "outro",         "mus_20260614_outro_last_frame_v2.mp3"),
}

# ---- M3: the six real ambience beds + per-chapter candidates ---------------
# location keyword -> bed. Ranked per chapter; assignment maximises distinctness.
AMBIENCE_BEDS = (
    "amb_courtroom_room_tone.mp3",
    "amb_empty_hallway.mp3",
    "amb_institutional_drone.mp3",
    "amb_night_window.mp3",
    "amb_office_hum.mp3",
    "amb_tension_drone.mp3",
    "amb_rain_street.mp3",
    "amb_highway_traffic.mp3",
    "amb_engine_idle.mp3",
    "amb_light_wind.mp3",
    "amb_road_rumble_1920s.mp3",
)
AMBIENCE_KEYWORDS: list[tuple[tuple[str, ...], str]] = [
    (("prohibition", "1920s", "1925", "model-t", "period", "lazyback", "whisky", "gin"), "amb_road_rumble_1920s.mp3"),
    (("highway", "traffic", "aerial", "thousands of cars", "multi-lane", "shoulder"), "amb_highway_traffic.mp3"),
    (("rain", "wet asphalt", "rain-slick", "downpour", "storm"), "amb_rain_street.mp3"),
    (("engine", "idle", "motor", "pull over", "pulled over", "ignition"), "amb_engine_idle.mp3"),
    # RETIRED amb_light_wind.mp3 everywhere: its broadband roar reads as a jet/airplane
    # (owner flagged twice — 2026-07-06 ending, 2026-07-10 EP33 opening). Route outdoor/wind
    # cues to the calm night-window bed instead so no section ever gets the "飛行機の音" bed.
    (("wind", "breeze", "rustling", "open road", "field", "outdoor"), "amb_night_window.mp3"),
    (("courthouse", "supreme court", "courtroom", "bench", "marble", "verdict", "gavel", "justice"), "amb_courtroom_room_tone.mp3"),
    (("driveway", "porch", "home", "house", "suburban", "residential", "window", "curb", "dusk", "tarp"), "amb_night_window.mp3"),
    (("highway", "road", "street", "traffic", "shoulder", "stop", "sweep", "map"), "amb_tension_drone.mp3"),
    (("office", "paper", "document", "warrant", "rental", "agreement", "ledger", "prohibition", "hum"), "amb_office_hum.mp3"),
    (("nation", "states", "america", "grid", "doctrine", "rule", "meter", "diagram"), "amb_institutional_drone.mp3"),
    (("hallway", "corridor", "footsteps", "approach", "quiet"), "amb_empty_hallway.mp3"),
]
# fallback default per chapter (used only if keyword scan is empty)
CHAPTER_AMBIENCE_DEFAULT: dict[str, str] = {
    "hook":    "amb_rain_street.mp3",         # night traffic stop on wet asphalt
    "opening": "amb_highway_traffic.mp3",     # 1925->2018 highway sweep
    "act1":    "amb_road_rumble_1920s.mp3",   # Prohibition night highway / Carroll
    "act2":    "amb_institutional_drone.mp3", # probable-cause doctrine / diagrams
    "act3":    "amb_night_window.mp3",         # suburban driveway / the tarp
    "act4":    "amb_courtroom_room_tone.mp3", # map of rights / rulings
    "ending":  "amb_night_window.mp3",         # calm indoor resolve for the CTA (bookends the hook).
                                               # NOT amb_light_wind: its broadband roar read as a
                                               # "飛行機の音みたいな変な音" under the outro (owner 2026-07-06).
    # Named-chapter defaults (data-driven CaseFilm episodes use descriptive ids, not act1..4).
    # reckoning_and_limits = legal doctrine's boundaries -> institutional weight, NOT highway traffic.
    # A ~4min legal-reckoning chapter under highway hum reads as an ambience mismatch (owner 2026-07-10:
    # "変な効果音でミスマッチはないか気を付けて").
    "reckoning_and_limits": "amb_institutional_drone.mp3",
}

# Chapters whose ambience bed is LOCKED to CHAPTER_AMBIENCE_DEFAULT and never overridden by keyword
# matching. The Ending is the CTA/outro: its VO says "open road", which would otherwise trigger the
# outdoor/wind bed (amb_light_wind) whose roar sounds like a jet under the quiet outro. The CTA tone
# must be controlled, not driven by an incidental word.
FORCED_DEFAULT_CHAPTERS = {"ending", "reckoning_and_limits"}

# ---- M4: one-shot SFX map (curated from build_case_sound_design) -----------
# (keywords, filename, dur_hint_sec, linear_volume). First match wins; order matters.
ONESHOT_MAP: list[tuple[tuple[str, ...], str, float, float]] = [
    # emotional hero hits sit a touch louder so REVEALS / the Collins driveway slam /
    # the ruling actually LAND (still well under the VO; ticks/blips stay subtle).
    (("sub-drop", "sub drop"),                          "sfx_sub_drop.mp3",        1.4, 0.24),
    (("riser", "rise"),                                 "sfx_riser_2s.mp3",        2.0, 0.22),
    (("low boom", "boom"),                              "sfx_low_boom.mp3",        1.6, 0.26),
    (("gavel", "knock"),                                "sfx_gavel_knock.mp3",     1.0, 0.24),
    (("page turn", "page-turn"),                        "sfx_page_turn.mp3",       0.9, 0.18),
    (("stamp", "seal"),                                 "sfx_stamp_seal.mp3",      0.9, 0.20),
    (("shutter", "camera", "photo"),                    "sfx_camera_shutter.mp3",  0.7, 0.16),
    (("tarp", "tear", "fabric", "upholstery", "cloth", "rustle"), "sfx_paper_rustle.mp3", 1.0, 0.16),
    (("pass-by", "pass by", "whip"),                    "sfx_whoosh_medium.mp3",   1.2, 0.18),
    (("engine pull", "pull"),                           "sfx_whoosh_medium.mp3",   1.2, 0.18),
    (("whoosh", "swoosh"),                              "sfx_whoosh_short.mp3",    0.8, 0.18),
    # Owner directive (2026-07-10, EP32 retro): retire the UI "pico-pico" blip/tick
    # timbre. Data/ledger/typing beats now fire ORGANIC, meaningful textures
    # (paper rustle for ledger data, page turn for typed captions, soft counter
    # taps) instead of sfx_data_blip / sfx_ui_tick. The keywords still LAND a
    # one-shot on the same word — only the sample changes to a non-UI sound.
    (("data-blip", "data blip", "blip"),                "sfx_paper_rustle.mp3",    0.9, 0.16),
    (("period-beat", "type tick", "type ticks", "ui-tick", "ui tick"), "sfx_page_turn.mp3", 0.9, 0.16),
    (("clink", "glass"),                                "sfx_soft_impact.mp3",     0.6, 0.16),
    (("tick", "check"),                                 "sfx_soft_impact.mp3",     0.6, 0.16),
    (("click", "mechanical", "metallic", "lock", "latch", "binder", "turn"), "sfx_binder_lock.mp3", 0.7, 0.16),
    (("footstep", "steps"),                             "sfx_soft_impact.mp3",     0.8, 0.12),
    (("impact", "thud", "hit", "slam"),                 "sfx_soft_impact.mp3",     1.0, 0.24),
    (("clock", "spins", "spinning"),                    "sfx_clock_tick_loop.mp3", 1.0, 0.10),
]
# hard transients keep their one-shot even if an atmospheric word is nearby.
HARD_WORDS = (
    "boom", "stamp", "seal", "gavel", "knock", "whoosh", "swoosh", "blip",
    "tick", "click", "impact", "thud", "slam", "tear", "riser", "rise",
    "shutter", "camera", "photo", "page turn", "sub-drop", "sub drop",
    "pull", "clink", "pass-by", "pass by", "whip",
)
# atmospheric markers routed to L3 gain automation instead of a one-shot.
STRONG_ATMOS = (
    "bed", "drone", "hum", "swell", "pulse", "ambient", "ambience", "shimmer",
    "hush", "reassuring", "night road", "highway bed", "engine hum", "room tone",
    "tone", "note", "beat", "steady", "wind",
)

# transition whoosh auto-placed at every chapter cut boundary (layer 4)
CHAPTER_CUT_SFX = ("sfx_whoosh_short.mp3", 0.8, 0.16)

# NOTE (EP32 sound remediation, 2026-07-06 owner reject: "意味のない効果音がうざい / ピコピコ
# 鳴ってて耳障り / 種類も少なくてしょぼい"):
# The former "transient-density bed" (a 326-hit tick/blip/whoosh filler placed on a
# fixed cadence PURELY to lift the render's measured onset density over an
# acceptance floor of 35/min) has been REMOVED ENTIRELY. It was gate-gaming: it made
# the audio WORSE (a machine-gun of meaningless pips) while satisfying a wrong
# proxy. SFX now come ONLY from the script's DESIGNED (SFX:) cues + chapter-cut
# transitions -- each placed at the real narrated word/beat -- rotated through the
# library variants for variety (VARIANT_POOLS). The acceptance gate was recalibrated
# to reward a genuine 4-layer mix (distinct SFX files + distinct ambience beds bound
# by sha), NOT raw transient count -- see check_final_acceptance.check_sound_layers.

CHAPTER_TITLES = {
    "hook": "Hook", "opening": "Opening", "act1": "ACT I", "act2": "ACT II",
    "act3": "ACT III", "act4": "ACT IV", "ending": "Ending / CTA",
}


# ============================================================================
# helpers
# ============================================================================
def round3(x: float) -> float:
    return round(float(x), 3)


def vol_to_db(vol: float) -> float:
    return -120.0 if vol <= 0 else round(20.0 * math.log10(vol), 1)


def db_to_vol(db: float) -> float:
    return round(10.0 ** (db / 20.0), 5)


def media_root() -> Path:
    """Resolve the media (SSD) root from machine-local config, raw-string fallback."""
    cfg_path = ROOT / "config" / "storage.local.json"
    try:
        cfg = json.loads(cfg_path.read_text("utf-8"))
        return Path(cfg["roots"]["media"]["path"])
    except Exception:
        return Path(r"H:\pd-media")


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> Optional[str]:
    if not path.exists():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def alnum_tokens(s: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", s.lower())


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)


def ffprobe_duration(path: Path) -> Optional[float]:
    if not path.exists():
        return None
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "csv=p=0", str(path)],
            capture_output=True, text=True, check=False)
        return float(out.stdout.strip())
    except Exception:
        return None


def find_film_data(ep: str, override: Optional[str]) -> Optional[Path]:
    """Locate the CaseFilm data JSON that defines the render's video timeline
    (hookSeconds / narrationSeconds). Tries the two canonical locations, then
    scans remotion/public/*/film_data*.json for a matching episode_id."""
    if override:
        p = Path(override)
        return p if p.exists() else None
    slug = ep.rsplit("-", 1)[-1]  # PD-2026-032-carsearch -> carsearch
    candidates = [
        ROOT / "remotion" / "public" / slug / "film_data.v001.json",
        ROOT / "remotion" / "src" / "data" / f"{slug}_film.json",
    ]
    for c in candidates:
        if c.exists():
            return c
    for c in sorted((ROOT / "remotion" / "public").glob("*/film_data*.json")):
        try:
            if json.loads(c.read_text("utf-8")).get("episode_id") == ep:
                return c
        except Exception:
            continue
    return None


def read_video_timeline(ep: str, override: Optional[str]) -> tuple[float, float, Optional[Path]]:
    """Return (hookSeconds, narrationSeconds, film_data_path) from the CaseFilm data
    so the mix can be offset by `lead` and span the whole composition. Falls back to
    (0.0, 0.0, None) if no film_data is found (mix then stays body-only == legacy)."""
    fd = find_film_data(ep, override)
    if fd is None:
        return 0.0, 0.0, None
    data = json.loads(fd.read_text("utf-8"))
    hook = float(data.get("hookSeconds") or 0.0)
    narr = float(data.get("narrationSeconds") or 0.0)
    return hook, narr, fd


def normalize_section(section: str) -> str:
    h = (section or "").upper().strip()
    if h.startswith("HOOK"):
        return "hook"
    if h.startswith("OPENING"):
        return "opening"
    if h.startswith("ENDING") or "CTA" in h:
        return "ending"
    m = re.match(r"ACT\s+([IV]+)", h)
    if m:
        roman = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5}.get(m.group(1))
        if roman:
            return f"act{roman}"
    return h.lower().replace(" ", "_") or "unknown"


# ============================================================================
# parse the script (beats + their (SFX:) parentheticals)
# ============================================================================
@dataclass
class Beat:
    index: int
    text: str
    sfx_parens: list[str] = field(default_factory=list)
    vis_text: str = ""
    # filled once aligned to the spoken (narration_index) token stream:
    tokens: list[str] = field(default_factory=list)
    gstart: int = 0      # global token index where this beat's content is spoken
    chunk_i: int = -1     # owning chunk (for chapter attribution)


def clean_vo(line: str) -> str:
    text = re.sub(r"^\[VO:\]\s*", "", line.strip())
    text = text.replace("**", "")
    text = re.sub(r"\s*(?:\[CLM-[0-9]{4}\]\s*)+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def parse_script_md(md_path: Path) -> list[Beat]:
    lines = md_path.read_text("utf-8").splitlines()
    beats: list[Beat] = []
    idx = 0
    pending: Optional[Beat] = None
    for raw in lines:
        line = raw.rstrip()
        if line.startswith("## ") or line.startswith("# "):
            continue
        if line.startswith("[VO:]"):
            pending = Beat(index=idx, text=clean_vo(line))
            beats.append(pending)
            idx += 1
            continue
        if pending is not None and ("(SFX:" in line or "(VIS:" in line):
            for m in re.finditer(r"\(SFX:\s*(.+?)\)", line):
                pending.sfx_parens.append(m.group(1).strip())
            vm = re.search(r"\(VIS:\s*(.+?)\)", line)
            if vm:
                pending.vis_text = (pending.vis_text + " " + vm.group(1)).strip()
    return beats


# ============================================================================
# narration-index timeline (B6) + beat->chunk matching
# ============================================================================
@dataclass
class Chunk:
    i: int
    vc_id: str
    section: str
    chapter_id: str
    text: str
    tokens: list[str]
    duration: float
    duration_source: str
    start: float = 0.0
    end: float = 0.0


def load_index(path: Path) -> dict:
    data = json.loads(path.read_text("utf-8"))
    if "eleven" not in str(data.get("provider", "")).lower():
        raise RuntimeError(f"narration provider is not ElevenLabs: {data.get('provider')}")
    if not data.get("chunks"):
        raise RuntimeError("narration_index has no chunks")
    return data


def find_chunk_audio(media: Path, ep: str, vc_id: str) -> Optional[Path]:
    """Prefer a per-chunk audio file (measured duration) if one exists."""
    voice = media / "episodes" / ep / "06_voice"
    for sub in ("draft_nPcz", "draft", "chunks", "master/chunks", "master"):
        d = voice / sub
        if not d.exists():
            continue
        for p in sorted(d.glob(f"*{vc_id}*")):
            if p.suffix.lower() in (".mp3", ".wav", ".m4a", ".flac"):
                return p
    return None


def build_chunks(index: dict, media: Path, ep: str) -> list[Chunk]:
    chunks: list[Chunk] = []
    cursor = 0.0
    for i, c in enumerate(index["chunks"]):
        vc = str(c.get("voice_chunk_id") or c.get("chunk_id") or f"VC-{i + 1:04d}")
        section = str(c.get("section", ""))
        text = str(c.get("text", "") or c.get("spoken_text", ""))
        est = float(c.get("estimated_duration_seconds") or c.get("seconds") or 0.0)
        audio = find_chunk_audio(media, ep, vc)
        measured = ffprobe_duration(audio) if audio else None
        if measured and measured > 0:
            dur, src = measured, f"measured:{audio.name}"
        else:
            dur, src = est, "narration_index_estimate"
        # Prefer the narration_index's OWN start/end — the AUTHORITATIVE master
        # timeline WITH inter-chunk silences (the master mp3 the video plays). A
        # bare cursor (no silence) sums ~16s short, drifting SFX cues off the
        # spoken word by the end. Using the index times keeps every SFX aligned
        # with the continuously-playing master (which is adelay'd by `lead`).
        idx_start = c.get("start")
        idx_end = c.get("end")
        if idx_start is not None and idx_end is not None:
            st = round3(float(idx_start))
            en = round3(float(idx_end))
        else:
            st = round3(cursor)
            en = round3(cursor + dur)
        ch = Chunk(
            i=i, vc_id=vc, section=section, chapter_id=normalize_section(section),
            text=text, tokens=alnum_tokens(text), duration=round3(en - st),
            duration_source=src, start=st, end=en,
        )
        chunks.append(ch)
        cursor = en + INTER_CHUNK_GAP
    return chunks


def build_global_tokens(chunks: list[Chunk]) -> tuple[list[str], list[float], list[int]]:
    """Flatten every chunk into one spoken-order token stream, each token stamped
    with a time = chunk_start + (local_index / chunk_len) * chunk_duration. This
    is the REAL narration timeline (B6): SFX cues are placed on these times, not a
    wpm guess."""
    gtok: list[str] = []
    gtime: list[float] = []
    gchunk: list[int] = []
    for ch in chunks:
        n = max(1, len(ch.tokens))
        for j, tok in enumerate(ch.tokens):
            gtok.append(tok)
            gtime.append(round3(ch.start + (j / n) * ch.duration))
            gchunk.append(ch.i)
    return gtok, gtime, gchunk


def time_at_global(gtime: list[float], gidx: int) -> float:
    if not gtime:
        return 0.0
    return gtime[max(0, min(len(gtime) - 1, gidx))]


def align_beats(beats: list[Beat], gtok: list[str], gchunk: list[int]) -> None:
    """Locate each script beat in the spoken token stream by best fuzzy block
    match (difflib). The script (03_script) and narration_index can diverge in
    wording/order after remediation edits; the SPOKEN audio follows the index,
    so a beat's SFX must fire where that content is actually narrated. Records
    the beat's global start index (gstart) and owning chunk (chunk_i)."""
    hint = 0
    for beat in beats:
        beat.tokens = alnum_tokens(beat.text)
        if not beat.tokens:
            beat.gstart = min(hint, max(0, len(gtok) - 1))
            beat.chunk_i = gchunk[beat.gstart] if gchunk else -1
            continue
        sm = difflib.SequenceMatcher(None, gtok, beat.tokens, autojunk=False)
        best: Optional[tuple[float, int]] = None
        for a, b, size in sm.get_matching_blocks():
            if size == 0:
                continue
            gs = max(0, a - b)                    # implied global start of the beat
            score = size - 0.001 * abs(gs - hint)  # big block, near the running cursor
            if best is None or score > best[0]:
                best = (score, gs)
        beat.gstart = best[1] if best is not None else min(hint, max(0, len(gtok) - 1))
        beat.chunk_i = gchunk[min(beat.gstart, len(gchunk) - 1)] if gchunk else -1
        hint = beat.gstart + len(beat.tokens)


def find_trigger_global(gtok: list[str], trig: list[str], near: int) -> int:
    """Global token index of the trigger phrase occurrence nearest ``near``."""
    if not trig:
        return -1
    n = len(trig)
    best: Optional[tuple[int, int]] = None
    for i in range(len(gtok) - n + 1):
        if gtok[i:i + n] == trig:
            d = abs(i - near)
            if best is None or d < best[0]:
                best = (d, i)
    return best[1] if best is not None else -1


# ============================================================================
# chapter spans + ambience assignment (M3)
# ============================================================================
def chapter_spans(chunks: list[Chunk], total: float) -> list[tuple[str, float, float, list[int]]]:
    """Gapless [start, end) span per chapter in first-appearance order,
    with the list of chunk indices in that chapter."""
    order: list[str] = []
    members: dict[str, list[int]] = {}
    starts: dict[str, float] = {}
    for ch in chunks:
        if ch.chapter_id not in starts:
            starts[ch.chapter_id] = ch.start
            order.append(ch.chapter_id)
            members[ch.chapter_id] = []
        members[ch.chapter_id].append(ch.i)
    spans: list[tuple[str, float, float, list[int]]] = []
    for j, cid in enumerate(order):
        s = starts[cid]
        e = starts[order[j + 1]] if j + 1 < len(order) else total
        spans.append((cid, round3(s), round3(e), members[cid]))
    return spans


def rank_beds(chapter_id: str, text: str) -> list[str]:
    """Ranked ambience-bed candidates for a chapter (keyword hits desc)."""
    low = text.lower()
    scored: list[tuple[int, int, str]] = []
    for order, (keywords, fname) in enumerate(AMBIENCE_KEYWORDS):
        hits = sum(low.count(k) for k in keywords)
        scored.append((-hits, order, fname))
    scored.sort()
    ranked = [f for _, _, f in scored]
    default = CHAPTER_AMBIENCE_DEFAULT.get(chapter_id)
    if default and default in ranked:
        ranked.remove(default)
        ranked.insert(0 if ranked and text.strip() == "" else 1, default)
    return ranked


def assign_ambience(spans: list[tuple[str, float, float, list[int]]],
                    chunks: list[Chunk], beats: list[Beat]) -> dict[str, str]:
    """M3: distinct bed per chapter -- greedily prefer an unused bed to
    MAXIMISE distinctness (deterministic)."""
    text_by_chapter: dict[str, str] = {}
    beats_by_chunk: dict[int, list[Beat]] = {}
    for b in beats:
        beats_by_chunk.setdefault(b.chunk_i, []).append(b)
    for cid, _s, _e, members in spans:
        parts: list[str] = []
        for ci in members:
            parts.append(chunks[ci].text)
            for b in beats_by_chunk.get(ci, []):
                parts.append(b.vis_text)
        text_by_chapter[cid] = " ".join(parts)

    used: set[str] = set()
    assigned: dict[str, str] = {}
    for cid, _s, _e, _m in spans:
        # Locked chapters (e.g. Ending/CTA) always use their controlled default bed, regardless of
        # keyword hits or distinctness -- so an incidental word can't inject a roaring outdoor bed.
        if cid in FORCED_DEFAULT_CHAPTERS and CHAPTER_AMBIENCE_DEFAULT.get(cid):
            assigned[cid] = CHAPTER_AMBIENCE_DEFAULT[cid]
            used.add(assigned[cid])
            continue
        ranked = rank_beds(cid, text_by_chapter.get(cid, ""))
        pick = next((f for f in ranked if f not in used), None)
        if pick is None:  # all beds used -> allow reuse of top-ranked
            pick = ranked[0] if ranked else CHAPTER_AMBIENCE_DEFAULT.get(cid, AMBIENCE_BEDS[0])
        assigned[cid] = pick
        used.add(pick)
    return assigned


# ============================================================================
# cue construction (B6 timing + M4 sequencing/dedup/atmos-routing)
# ============================================================================
@dataclass
class SfxCue:
    cue_id: str
    file: str            # library-relative, e.g. "sfx/sfx_low_boom.mp3"
    chapter_id: str
    time: float
    dur: float
    volume: float
    gain_db: float
    source: str          # chapter_cut | script_sfx
    phrase: str
    trigger: str
    timing: str          # word_trigger | beat_offset | chapter_start


@dataclass
class SwellEvent:
    chapter_id: str
    time: float
    dur: float
    bump: float
    phrase: str
    trigger: str
    timing: str


def split_sequence(phrase: str) -> list[str]:
    """M4: one parenthetical == one cue UNLESS explicit sequencing words appear."""
    # NB: do not strip quote chars here -- a trailing quote closes a quoted
    # trigger like on "hundred years." and quoted_trigger() needs it intact.
    parts = re.split(r";|->|→|\bthen\b|\binto\b", phrase, flags=re.IGNORECASE)
    return [p.strip(" .,;:-") for p in parts if p.strip(" .,;:-")]


def map_oneshot(low: str) -> Optional[tuple[str, float, float]]:
    for keywords, fname, dur, vol in ONESHOT_MAP:
        for kw in keywords:
            if kw in low:
                return fname, dur, vol
    return None


# Variant rotation (kills the "same one-shot repeats" cheap tell). Each base file
# rotates deterministically through its synthesized variants by cue index, so
# consecutive whoosh/tick/blip/etc. cues never fire the identical file.
VARIANT_POOLS: dict[str, tuple[str, ...]] = {
    "sfx_whoosh_short.mp3": ("sfx_whoosh_short.mp3", "sfx_whoosh_v2_short.mp3", "sfx_whoosh_v2_med.mp3", "sfx_whoosh_v2_long.mp3"),
    "sfx_whoosh_medium.mp3": ("sfx_whoosh_medium.mp3", "sfx_whoosh_v2_med.mp3", "sfx_whoosh_v2_long.mp3"),
    # sfx_ui_tick / sfx_data_blip pools retired (2026-07-10): the UI blip/tick
    # timbre is no longer mapped by ONESHOT_MAP, so these bases are never selected
    # and their variant rotation would only reintroduce the "pico-pico" sound.
    "sfx_sub_drop.mp3": ("sfx_sub_drop.mp3", "sfx_subdrop_v2_a.mp3", "sfx_subdrop_v2_b.mp3"),
    "sfx_riser_2s.mp3": ("sfx_riser_2s.mp3", "sfx_riser_v2_1s.mp3", "sfx_riser_v2_3s.mp3"),
    "sfx_soft_impact.mp3": ("sfx_soft_impact.mp3", "sfx_impact_v2_tight.mp3"),
    "sfx_low_boom.mp3": ("sfx_low_boom.mp3", "sfx_boom_v2_deep.mp3"),
}


def variant_of(fname: str, idx: int) -> str:
    pool = VARIANT_POOLS.get(fname)
    return pool[idx % len(pool)] if pool else fname


def quoted_trigger(fragment: str) -> str:
    m = re.search(r'["“]([^"”]+)["”]', fragment)
    return m.group(1).strip() if m else ""


def place_time(beat: Beat, trigger: str, nth: int,
               gtok: list[str], gtime: list[float]) -> tuple[float, str, str]:
    """B6: place the cue on the REAL narration timeline. A quoted trigger lands
    on that spoken word (nearest occurrence to the beat); otherwise the cue lands
    a little into the beat, staggered for multiple cues on one beat."""
    trig_toks = alnum_tokens(trigger)
    if trig_toks:
        gi = find_trigger_global(gtok, trig_toks, beat.gstart)
        if gi >= 0:
            return time_at_global(gtime, gi), trigger, "word_trigger"
    off = beat.gstart + min(len(beat.tokens), int(round(0.15 * len(beat.tokens))) + 2 * nth)
    return time_at_global(gtime, off), "", "beat_offset"


def build_cues(beats: list[Beat], chunks: list[Chunk],
               spans: list[tuple[str, float, float, list[int]]],
               gtok: list[str], gtime: list[float]):
    """Return (sfx_cues, swells, unmapped)."""
    sfx: list[SfxCue] = []
    swells: list[SwellEvent] = []
    unmapped: list[dict] = []
    n = 0

    # chapter-cut transition whooshes (skip the very first chapter start at t=0).
    # ROTATE through the whoosh variant pool so consecutive chapter transitions never fire the
    # IDENTICAL file — previously every chapter cut used sfx_whoosh_short.mp3 (6x), which read as
    # "same sound repeating / few types" (owner 2026-07-06: 効果音の種類が少ない・違和感). Now each
    # act transition gets a distinct whoosh variant.
    base_fname, base_dur, base_vol = CHAPTER_CUT_SFX
    for cid, s, _e, _m in spans:
        if s <= 0.001:
            continue
        n += 1
        fname = variant_of(base_fname, n)
        sfx.append(SfxCue(
            cue_id=f"L4-{n:03d}", file=f"sfx/{fname}", chapter_id=cid,
            time=round3(s), dur=base_dur, volume=base_vol, gain_db=vol_to_db(base_vol),
            source="chapter_cut", phrase=f"cut into {CHAPTER_TITLES.get(cid, cid)}",
            trigger="", timing="chapter_start"))

    for beat in beats:
        if beat.chunk_i < 0 or not beat.sfx_parens:
            continue
        chunk = chunks[beat.chunk_i]
        for paren in beat.sfx_parens:
            fragments = split_sequence(paren)
            for k, frag in enumerate(fragments):
                low = frag.lower()
                trigger = quoted_trigger(frag)
                hard = any(hw in low for hw in HARD_WORDS)
                atmos = any(m in low for m in STRONG_ATMOS)
                oneshot = map_oneshot(low)
                t, trig, timing = place_time(beat, trigger, k, gtok, gtime)

                if "silence" in low and not hard:
                    unmapped.append({"chunk": chunk.vc_id, "beat": beat.index,
                                     "phrase": frag, "reason": "rest_silence"})
                    continue
                if hard and oneshot is None:
                    oneshot = ("sfx_whoosh_short.mp3", 0.8, 0.16)
                if hard or (oneshot is not None and not atmos):
                    fname, dur, vol = oneshot
                    n += 1
                    fname = variant_of(fname, n)
                    sfx.append(SfxCue(
                        cue_id=f"L4-{n:03d}", file=f"sfx/{fname}", chapter_id=chunk.chapter_id,
                        time=t, dur=dur, volume=vol, gain_db=vol_to_db(vol),
                        source="script_sfx", phrase=frag, trigger=trig, timing=timing))
                elif atmos:
                    swells.append(SwellEvent(
                        chapter_id=chunk.chapter_id, time=t, dur=SWELL_DUR_DEFAULT,
                        bump=SWELL_BUMP, phrase=frag, trigger=trig, timing=timing))
                elif oneshot is not None:
                    fname, dur, vol = oneshot
                    n += 1
                    fname = variant_of(fname, n)
                    sfx.append(SfxCue(
                        cue_id=f"L4-{n:03d}", file=f"sfx/{fname}", chapter_id=chunk.chapter_id,
                        time=t, dur=dur, volume=vol, gain_db=vol_to_db(vol),
                        source="script_sfx", phrase=frag, trigger=trig, timing=timing))
                else:
                    unmapped.append({"chunk": chunk.vc_id, "beat": beat.index,
                                     "phrase": frag, "reason": "no_keyword_match"})

    sfx.sort(key=lambda c: (c.time, c.file))
    swells.sort(key=lambda s: (s.time, s.file if hasattr(s, "file") else s.phrase))
    return sfx, swells, unmapped


def dedup_sfx(sfx: list[SfxCue]) -> tuple[list[SfxCue], int]:
    """M4: drop identical files firing within DEDUP_WINDOW_SEC of a kept cue."""
    kept: list[SfxCue] = []
    last_by_file: dict[str, float] = {}
    dropped = 0
    for c in sfx:
        prev = last_by_file.get(c.file)
        if prev is not None and (c.time - prev) < DEDUP_WINDOW_SEC:
            dropped += 1
            continue
        kept.append(c)
        last_by_file[c.file] = c.time
    # renumber deterministically
    for i, c in enumerate(kept, start=1):
        c.cue_id = f"L4-{i:03d}"
    return kept, dropped


# ============================================================================
# density gate (M3 distinctness + SFX floor)
# ============================================================================
def compute_density(sfx: list[SfxCue], beds: dict[str, str],
                    spans: list[tuple[str, float, float, list[int]]], total: float) -> dict:
    sfx_count = len(sfx)
    minutes = max(0.001, total / 60.0)
    sfx_per_min = sfx_count / minutes

    # ambience coverage = union of per-chapter spans / total (gapless -> ~1.0)
    covered = sum((e - s) for _c, s, e, _m in spans)
    coverage = covered / total if total > 0 else 0.0
    distinct_beds = len(set(beds.values()))

    failures: list[str] = []
    if sfx_count < SFX_TOTAL_FLOOR:
        failures.append(f"sfx_count {sfx_count} < floor {SFX_TOTAL_FLOOR}")
    if sfx_per_min < SFX_PER_MIN_FLOOR:
        failures.append(f"sfx_per_min {sfx_per_min:.2f} < floor {SFX_PER_MIN_FLOOR}")
    if coverage < AMBIENCE_COVERAGE_FLOOR:
        failures.append(f"ambience_coverage {coverage:.3f} < floor {AMBIENCE_COVERAGE_FLOOR}")
    if distinct_beds < AMBIENCE_DISTINCT_FLOOR:
        failures.append(f"ambience_distinct_beds {distinct_beds} < floor {AMBIENCE_DISTINCT_FLOOR}")

    return {
        "sfx_count": sfx_count,
        "sfx_per_min": round3(sfx_per_min),
        "ambience_coverage": round3(coverage),
        "ambience_distinct_beds": distinct_beds,
        "floors": {
            "sfx_total": SFX_TOTAL_FLOOR,
            "sfx_per_min": SFX_PER_MIN_FLOOR,
            "ambience_coverage": AMBIENCE_COVERAGE_FLOOR,
            "ambience_distinct_beds": AMBIENCE_DISTINCT_FLOOR,
        },
        "pass": not failures,
        "failures": failures,
    }


# ============================================================================
# ffmpeg 4-layer graph
# ============================================================================
def intro_segments_for(lead: float) -> list[tuple[str, float, float]]:
    """Split the hook/opening lead [0, lead] into a hook bed then an opening bed
    (hookSeconds == lead - OPENING_SEC). If there is no hook, one opening bed fills
    the whole lead."""
    if lead <= 0.001:
        return []
    hook_end = round3(max(0.0, lead - OPENING_SEC))  # == hookSeconds
    if hook_end > 0.1:
        return [("hook", 0.0, hook_end), ("opening", round3(hook_end), round3(lead))]
    return [("opening", 0.0, round3(lead))]


def build_ffmpeg(narration_path: str, spans, beds: dict[str, str],
                 sfx: list[SfxCue], swells: list[SwellEvent],
                 lead: float, body_len: float, total: float,
                 lib: Path, out_wav: str,
                 loudnorm: str) -> tuple[str, list[str]]:
    """Assemble the 4-layer ducked filter_complex + full argv (string only), spanning
    the WHOLE video composition [0, total] with the body offset by `lead`.

    L1 narration front (placed at `lead`, splits a sidechain key), L2 music
    (hook/opening intro fill [0, lead] + per-chapter ducked body bed offset by
    `lead` + outro fill over the endcard tail), L3 ambience distinct constant body
    bed offset by `lead` + swell gain automation, L4 SFX one-shots offset by `lead`
    (plus an optional riser landing on the body start). Nothing plays under the hook
    narration's future energy; there is no VO in the lead so the intro is not ducked.
    """
    amb_floor = db_to_vol(AMBIENCE_FLOOR_DB)
    lead_ms = int(round(lead * 1000))
    has_bookends = lead > 0.001

    music_cues = [(cid, s, e) for (cid, s, e, _m) in spans]
    amb_cues = [(cid, s, e, beds[cid]) for (cid, s, e, _m) in spans]
    intro_segs = intro_segments_for(lead)

    # ---- inputs (order fixes the [idx:a] references below) -------------------
    inputs: list[str] = ["-i", narration_path]
    cursor = 1

    intro_idx: list[int] = []
    for role_key, _s, _e in intro_segs:
        _r, folder, fname = CHAPTER_MUSIC[role_key]
        inputs += ["-stream_loop", "-1", "-i", str(lib / "music" / folder / fname)]
        intro_idx.append(cursor); cursor += 1

    music_idx0 = cursor
    for cid, _s, _e in music_cues:
        _r, folder, fname = CHAPTER_MUSIC.get(cid, ("bed", "explainer_bed",
                                                    "mus_20260614_explainer_bed_soft_explainer_v2.mp3"))
        inputs += ["-stream_loop", "-1", "-i", str(lib / "music" / folder / fname)]
        cursor += 1

    outro_idx: Optional[int] = None
    if has_bookends:
        _r, folder, fname = CHAPTER_MUSIC["ending"]  # ("outro","outro", outro track)
        inputs += ["-stream_loop", "-1", "-i", str(lib / "music" / folder / fname)]
        outro_idx = cursor; cursor += 1

    amb_idx0 = cursor
    for _cid, _s, _e, bed in amb_cues:
        inputs += ["-stream_loop", "-1", "-i", str(lib / "ambience" / bed)]
        cursor += 1

    sfx_idx0 = cursor
    for c in sfx:
        inputs += ["-i", str(lib / c.file)]
        cursor += 1

    riser_idx: Optional[int] = None
    if has_bookends:
        inputs += ["-i", str(lib / "sfx" / RISER_FILL[0])]
        riser_idx = cursor; cursor += 1

    filters: list[str] = []
    # narration -> placed at `lead`, padded to the full composition -> [vo] + [key]
    filters.append(
        f"[0:a]aresample=48000,volume={NARRATION_VOL},apad,atrim=0:{body_len:.3f},"
        f"asetpts=PTS-STARTPTS,adelay={lead_ms}|{lead_ms},apad,atrim=0:{total:.3f},"
        f"asetpts=PTS-STARTPTS,asplit=2[vo][key]")

    # music layer: intro fill [0,lead] + per-chapter body bed (+lead) + outro tail
    m_labels: list[str] = []
    for k, (idx, (_role, s, e)) in enumerate(zip(intro_idx, intro_segs)):
        seg = max(0.1, e - s)
        delay = int(round(s * 1000))
        filters.append(
            f"[{idx}:a]atrim=0:{seg:.3f},asetpts=PTS-STARTPTS,volume={INTRO_MUSIC_VOL},"
            f"afade=t=in:st=0:d=0.6,afade=t=out:st={max(0.0, seg - 0.8):.3f}:d=0.8,"
            f"adelay={delay}|{delay}[mi{k}]")
        m_labels.append(f"[mi{k}]")
    for i, (_cid, s, e) in enumerate(music_cues):
        idx = music_idx0 + i
        seg = max(0.1, e - s)
        delay = int(round((s + lead) * 1000))
        filters.append(
            f"[{idx}:a]atrim=0:{seg:.3f},asetpts=PTS-STARTPTS,volume={MUSIC_VOL},"
            f"afade=t=in:st=0:d=0.5,afade=t=out:st={max(0.0, seg - 0.7):.3f}:d=0.7,"
            f"adelay={delay}|{delay}[m{i}]")
        m_labels.append(f"[m{i}]")
    if outro_idx is not None:
        o_s = round3(lead + body_len)
        seg = max(0.1, total - o_s)
        delay = int(round(o_s * 1000))
        # fade COMPLETES OUTRO_FADE_END_MARGIN before the mix end so the -shortest
        # mux trim still leaves a fully-faded (silent) ending -- no hard chop.
        o_fade_st = round3(max(0.0, seg - OUTRO_FADE_END_MARGIN - OUTRO_FADE_DUR))
        filters.append(
            f"[{outro_idx}:a]atrim=0:{seg:.3f},asetpts=PTS-STARTPTS,volume={OUTRO_MUSIC_VOL},"
            f"afade=t=in:st=0:d=0.8,afade=t=out:st={o_fade_st:.3f}:d={OUTRO_FADE_DUR:.3f},"
            f"adelay={delay}|{delay}[mo]")
        m_labels.append("[mo]")
    filters.append(f"{''.join(m_labels)}amix=inputs={len(m_labels)}:normalize=0:dropout_transition=0[musraw]")
    filters.append("[musraw][key]sidechaincompress=threshold=0.03:ratio=8:attack=25:release=320[musd]")

    # ambience layer (distinct per-chapter constant beds, +lead; NOT sidechained -> capped duck)
    a_labels: list[str] = []
    for i, (_cid, s, e, _bed) in enumerate(amb_cues):
        idx = amb_idx0 + i
        seg = max(0.1, e - s)
        delay = int(round((s + lead) * 1000))
        filters.append(
            f"[{idx}:a]atrim=0:{seg:.3f},asetpts=PTS-STARTPTS,volume={amb_floor},"
            f"afade=t=in:st=0:d=0.6,afade=t=out:st={max(0.0, seg - 0.6):.3f}:d=0.6,"
            f"adelay={delay}|{delay}[a{i}]")
        a_labels.append(f"[a{i}]")
    filters.append(f"{''.join(a_labels)}amix=inputs={len(a_labels)}:normalize=0:dropout_transition=0[ambraw]")
    # L3 gain automation: multiplicative swell bumps (routed atmospheric cues), +lead
    terms = "+".join(
        f"{sw.bump:.3f}*between(t,{sw.time + lead:.3f},{sw.time + sw.dur + lead:.3f})" for sw in swells)
    expr = f"1+{terms}" if terms else "1"
    filters.append(f"[ambraw]volume=eval=frame:volume='{expr}'[ambd]")

    # sfx layer (one-shots, +lead) + optional riser landing on the body start
    s_labels: list[str] = []
    for i, c in enumerate(sfx):
        idx = sfx_idx0 + i
        delay = int(round((c.time + lead) * 1000))
        filters.append(
            f"[{idx}:a]atrim=0:{c.dur:.3f},asetpts=PTS-STARTPTS,volume={c.volume},"
            f"adelay={delay}|{delay}[s{i}]")
        s_labels.append(f"[s{i}]")
    if riser_idx is not None:
        r_dur, r_vol = RISER_FILL[1], RISER_FILL[2]
        r_start = round3(max(0.0, lead - r_dur))  # climax lands on the body start
        delay = int(round(r_start * 1000))
        filters.append(
            f"[{riser_idx}:a]atrim=0:{r_dur:.3f},asetpts=PTS-STARTPTS,volume={r_vol},"
            f"adelay={delay}|{delay}[sriser]")
        s_labels.append("[sriser]")
    if s_labels:
        filters.append(f"{''.join(s_labels)}amix=inputs={len(s_labels)}:normalize=0:dropout_transition=0[sfxraw]")
    else:
        filters.append(f"anullsrc=r=48000:cl=stereo,atrim=0:{total:.3f}[sfxraw]")

    # final mix: VO front, ducked music, audible ambience bed, sfx; loudnorm I=-14
    filters.append(
        f"[vo][musd][ambd][sfxraw]amix=inputs=4:weights={FINAL_WEIGHTS}:normalize=0:"
        f"duration=first,atrim=0:{total:.3f},{loudnorm},"
        f"alimiter=level_in=1:level_out=1:limit=0.95[aout]")

    graph = ";".join(filters)
    argv = ["ffmpeg", "-y", *inputs, "-filter_complex", graph,
            "-map", "[aout]", "-t", f"{total:.3f}",
            "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", out_wav]
    return graph, argv


def quote_arg(a: str) -> str:
    if a == "" or re.search(r"[\s\\]", a):
        return '"' + a.replace('"', r"\"") + '"'
    return a


# ============================================================================
# render (two-pass loudnorm) -- only with --render and all inputs present
# ============================================================================
def measure_loudnorm(argv_measure: list[str]) -> Optional[dict]:
    out = subprocess.run(argv_measure, capture_output=True, text=True, check=False)
    m = re.search(r"\{\s*\"input_i\".*?\}", out.stderr, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except Exception:
        return None


# ============================================================================
# main
# ============================================================================
def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    ap = argparse.ArgumentParser(description="Build the real narration-timed 4-layer audio mix for a PD case film.")
    ap.add_argument("--ep", required=True, help="episode slug, e.g. PD-2026-032-carsearch")
    ap.add_argument("--script", help="script.en markdown (default: episodes/<ep>/03_script/script.en.v001.md)")
    ap.add_argument("--index", help="narration_index JSON (default: episodes/<ep>/06_audio/narration_index.v001.json)")
    ap.add_argument("--out", help="provenance JSON (default: episodes/<ep>/06_audio/audio_provenance.<rev>.json)")
    ap.add_argument("--film-data", help="CaseFilm data JSON for the video timeline (default: remotion/public/<slug>/film_data.v001.json)")
    ap.add_argument("--narration-master", help="narration master audio path (default: media/episodes/<ep>/06_voice/master/vc_master_v001.mp3). Use to point at a re-voiced/time-fit master without renaming the v001 artifact.")
    ap.add_argument("--revision", default=REVISION_DEFAULT)
    ap.add_argument("--dry-run", action="store_true", help="emit ffmpeg command + provenance only; never run ffmpeg")
    ap.add_argument("--render", action="store_true", help="run ffmpeg (only if not --dry-run and every input exists)")
    ap.add_argument("--allow-fail", action="store_true", help="write provenance even if the density gate fails (exit still non-zero)")
    args = ap.parse_args()

    ep = args.ep
    ep_dir = ROOT / "episodes" / ep
    script_md = Path(args.script) if args.script else ep_dir / "03_script" / "script.en.v001.md"
    index_path = Path(args.index) if args.index else ep_dir / "06_audio" / "narration_index.v001.json"
    out_path = Path(args.out) if args.out else ep_dir / "06_audio" / f"audio_provenance.{args.revision}.json"

    if not script_md.exists():
        print(f"ERROR: script not found: {script_md}", file=sys.stderr)
        return 2
    if not index_path.exists():
        print(f"ERROR: narration_index not found: {index_path}", file=sys.stderr)
        return 2

    media = media_root()
    lib = media / "library"

    index = load_index(index_path)
    chunks = build_chunks(index, media, ep)
    # internal narration timeline (cue/token placement) = summed chunk durations + tail
    body_internal = round3(chunks[-1].end + TAIL_SEC)

    # SYNC FIX: read the render's video timeline so the body sits at `lead` and the
    # mix spans the WHOLE composition (hook/opening lead + body + endcard tail).
    hook_seconds, narration_seconds, film_data_path = read_video_timeline(ep, args.film_data)
    if film_data_path is not None and narration_seconds > 0:
        lead = round3(hook_seconds + OPENING_SEC)
        # body_len == the render's Body length (narrationSeconds); guard so it always
        # covers the internal narration timeline (no cue ever falls outside the body).
        body_len = round3(max(body_internal, narration_seconds))
        total = round3(lead + body_len + ENDCARD_SEC)
    else:
        # legacy / no film_data: body-only mix at t=0 (unchanged behaviour)
        lead = 0.0
        body_len = body_internal
        total = body_internal

    beats = parse_script_md(script_md)
    if not beats:
        print("ERROR: no [VO:] beats parsed from script", file=sys.stderr)
        return 2
    gtok, gtime, gchunk = build_global_tokens(chunks)
    align_beats(beats, gtok, gchunk)

    # chapter spans stay body-local [0, body_len]; the last chapter extends to
    # body_len so the ambience bed covers the full Body region.
    spans = chapter_spans(chunks, body_len)
    beds = assign_ambience(spans, chunks, beats)
    sfx_raw, swells, unmapped = build_cues(beats, chunks, spans, gtok, gtime)
    sfx, dropped = dedup_sfx(sfx_raw)
    density = compute_density(sfx, beds, spans, total)

    # ---- expected (not-yet-existing) narration master + outputs -------------
    narration_master = (Path(args.narration_master) if args.narration_master
                        else media / "episodes" / ep / "06_voice" / "master" / "vc_master_v001.mp3")
    wav_name = f"{ep}_film_audio_{args.revision}.wav"
    out_wav = media / "episodes" / ep / "06_audio" / "mix" / wav_name
    render_audio_copy = media / "episodes" / ep / "08_edit" / "audio" / wav_name

    loudnorm_apply = "loudnorm=I=-14:TP=-1.5:LRA=11:linear=true"
    graph, argv = build_ffmpeg(str(narration_master), spans, beds, sfx, swells,
                               lead, body_len, total, lib, str(out_wav), loudnorm_apply)
    command_str = " ".join(quote_arg(a) for a in argv)

    # ---- optional render (two-pass loudnorm) --------------------------------
    ran_ffmpeg = False
    mix_sha: Optional[str] = None
    mix_duration: Optional[float] = None
    loudnorm_measured: Optional[dict] = None
    if args.render and not args.dry_run:
        needed = [narration_master,
                  *[lib / "music" / CHAPTER_MUSIC.get(c, ("", "explainer_bed", "mus_20260614_explainer_bed_soft_explainer_v2.mp3"))[1]
                    / CHAPTER_MUSIC.get(c, ("", "explainer_bed", "mus_20260614_explainer_bed_soft_explainer_v2.mp3"))[2]
                    for c, _s, _e, _m in spans],
                  *[lib / "ambience" / beds[c] for c, _s, _e, _m in spans],
                  *[lib / c.file for c in sfx]]
        if lead > 0.001:  # hook/opening intro + endcard outro + riser fills
            for key in ("hook", "opening", "ending"):
                _r, folder, fname = CHAPTER_MUSIC[key]
                needed.append(lib / "music" / folder / fname)
            needed.append(lib / "sfx" / RISER_FILL[0])
        missing = [p for p in needed if not Path(p).exists()]
        if missing:
            print(f"--render skipped: {len(missing)} input(s) missing (e.g. {missing[0]})")
        else:
            out_wav.parent.mkdir(parents=True, exist_ok=True)
            render_audio_copy.parent.mkdir(parents=True, exist_ok=True)
            # pass 1: measure
            measure_graph = graph.replace(
                loudnorm_apply, "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json")
            argv_measure = ["ffmpeg", "-hide_banner", "-nostats", *argv[2:argv.index("-filter_complex")],
                            "-filter_complex", measure_graph, "-map", "[aout]",
                            "-f", "null", "-"]
            loudnorm_measured = measure_loudnorm(argv_measure)
            if loudnorm_measured:
                applied = (f"loudnorm=I=-14:TP=-1.5:LRA=11:linear=true:"
                           f"measured_I={loudnorm_measured['input_i']}:"
                           f"measured_TP={loudnorm_measured['input_tp']}:"
                           f"measured_LRA={loudnorm_measured['input_lra']}:"
                           f"measured_thresh={loudnorm_measured['input_thresh']}:"
                           f"offset={loudnorm_measured['target_offset']}")
                graph2 = graph.replace(loudnorm_apply, applied)
                argv2 = ["ffmpeg", "-y", *argv[2:argv.index("-filter_complex")],
                         "-filter_complex", graph2, *argv[argv.index("-map"):]]
            else:
                argv2 = argv
            tmp = out_wav.with_suffix(".tmp.wav")
            subprocess.run([*argv2[:-1], str(tmp)], check=True)
            tmp.replace(out_wav)
            import shutil
            shutil.copy2(out_wav, render_audio_copy)
            mix_sha = sha256_file(out_wav)
            mix_duration = ffprobe_duration(out_wav)
            ran_ffmpeg = True
            print(f"rendered mix -> {out_wav}")

    # ---- provenance JSON (the artifact check_sound_layers reads) ------------
    music_tracks = []
    for cid, _s, _e, _m in spans:
        role, folder, fname = CHAPTER_MUSIC.get(cid, ("bed", "explainer_bed",
                                                      "mus_20260614_explainer_bed_soft_explainer_v2.mp3"))
        music_tracks.append(f"music/{folder}/{fname}")

    # hook/opening intro + endcard outro fills that keep the lead + tail from being
    # silent (premium intro that builds; outro gently resolving).
    music_fills = []
    if lead > 0.001:
        for role_key, s, e in intro_segments_for(lead):
            _r, folder, fname = CHAPTER_MUSIC[role_key]
            music_fills.append({"role": role_key, "file": f"music/{folder}/{fname}",
                                "start": round3(s), "end": round3(e), "vol": INTRO_MUSIC_VOL})
        _r, folder, fname = CHAPTER_MUSIC["ending"]
        music_fills.append({"role": "outro", "file": f"music/{folder}/{fname}",
                            "start": round3(lead + body_len), "end": total, "vol": OUTRO_MUSIC_VOL})

    provenance = {
        "schema_version": SCHEMA_VERSION,
        "kind": "case_film_audio_provenance",
        "episode_id": ep,
        "revision": args.revision,
        "generator": GENERATOR,
        "fps": FPS,
        "timeline": {
            "total_sec": total,
            "lead_sec": lead,
            "body_len_sec": body_len,
            "body_internal_sec": body_internal,
            "narration_starts_at_sec": lead,
            "voice_end_sec": round3(lead + chunks[-1].end),
            "tail_sec": TAIL_SEC,
            "chunks": len(chunks),
            "beats": len(beats),
            "video_timeline": {
                "note": "mix spans the whole CaseFilm composition; body (narration+cues) offset by lead so it aligns with the burned captions + figures",
                "hook_seconds": round3(hook_seconds),
                "opening_sec": OPENING_SEC,
                "endcard_sec": ENDCARD_SEC,
                "narration_seconds": round3(narration_seconds),
                "film_data": rel(film_data_path) if film_data_path else None,
            },
            "timing_source": "narration_index chunk durations (measured per-chunk audio when present, else estimate); SFX placed by token position within the owning chunk; whole body shifted by lead",
            "measured_chunks": sum(1 for c in chunks if c.duration_source.startswith("measured")),
            "estimated_chunks": sum(1 for c in chunks if c.duration_source == "narration_index_estimate"),
        },
        "chapters": [
            {"chapter_id": cid, "title": CHAPTER_TITLES.get(cid, cid),
             "start": round3(s + lead), "end": round3(e + lead), "ambience_bed": beds[cid]}
            for cid, s, e, _m in spans
        ],
        # ---- LAYER INVENTORY that check_sound_layers verifies ----
        "layers": {
            "narration": {
                "role": "front / sidechain-priority (VO wins)",
                "master_uri": f"artifact://episodes/{ep}/06_voice/master/{narration_master.name}",
                "master_path_expected": str(narration_master),
                "master_exists": narration_master.exists(),
                "gain_db": 0.0,
            },
            "music": {
                "role": "per-chapter ducked musical bed (sidechained by VO) + hook/opening intro fill + endcard outro fill",
                "cue_count": len(music_tracks),
                "distinct_tracks": len(set(music_tracks)),
                "tracks": music_tracks,
                "gain_db": vol_to_db(MUSIC_VOL),
                "ducked": True,
                "fills": music_fills,
                "fill_count": len(music_fills),
            },
            "ambience": {
                "role": "distinct constant location bed per chapter (audible; NOT sidechained -> capped duck)",
                "bed_count": len(spans),
                "distinct_beds": len(set(beds.values())),
                "beds": sorted(set(beds.values())),
                "beds_by_chapter": {cid: beds[cid] for cid, _s, _e, _m in spans},
                "floor_db": AMBIENCE_FLOOR_DB,
                "ducking_capped": True,
                "swell_automation_events": len(swells),
            },
            "sfx": {
                "role": "narration-timed one-shots at real words + chapter cuts (cue times are body-local; add timeline.lead_sec for absolute)",
                "cue_count": len(sfx),
                "cues_before_dedup": len(sfx_raw),
                "deduped": dropped,
                "distinct_files": len(set(c.file for c in sfx)),
                "word_triggered": sum(1 for c in sfx if c.timing == "word_trigger"),
                "riser_fill": (RISER_FILL[0] if lead > 0.001 else None),
                "transient_bed": None,
                "transient_bed_removed_note": (
                    "The former onset-density filler bed (326 meaningless tick/blip/whoosh hits placed "
                    "on a fixed cadence to game the acceptance onset floor) was REMOVED (EP32 owner "
                    "reject 2026-07-06). SFX are now ONLY the script's designed (SFX:) cues + chapter "
                    "cuts at real narrated beats; the gate rewards distinct SFX files + beds, not raw "
                    "transient count."),
            },
        },
        "mix": {
            "wav_uri": f"artifact://episodes/{ep}/06_audio/mix/{wav_name}",
            "wav_path_expected": str(out_wav),
            "render_audio_copy": str(render_audio_copy),
            "exists": bool(mix_sha),
            "sha256": mix_sha,
            "duration_sec": round3(mix_duration) if mix_duration else None,
            "sample_rate": 48000,
            "channels": 2,
            "codec": "pcm_s16le",
            "loudnorm": {"I": -14.0, "TP": -1.5, "LRA": 11.0, "passes": 2},
            "loudnorm_measured": loudnorm_measured,
            "final_weights": FINAL_WEIGHTS,
        },
        # ---- how this WAV becomes the episode's SOLE audio ----
        "mux": {
            "note": "This WAV is the ONLY audio in the final deliverable; the video is muxed with -map 0:v -map 1:a so the render carries exactly this mix.",
            "audio_source_uri": f"artifact://episodes/{ep}/06_audio/mix/{wav_name}",
            "audio_source_sha256": mix_sha,
            "command_template": (
                f"ffmpeg -y -i <case_film_video.mp4> -i {out_wav} "
                f"-map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 320k -ar 48000 -shortest <final.mp4>"),
        },
        "density_gate": density,
        "unmapped_sfx": unmapped,
        "swells": [
            {"chapter_id": s.chapter_id, "time": s.time, "dur": s.dur,
             "bump": s.bump, "phrase": s.phrase, "trigger": s.trigger, "timing": s.timing}
            for s in swells
        ],
        "sfx_cues": [
            {"cue_id": c.cue_id, "file": c.file, "chapter_id": c.chapter_id,
             "time": c.time, "dur": c.dur, "gain_db": c.gain_db,
             "source": c.source, "phrase": c.phrase, "trigger": c.trigger, "timing": c.timing}
            for c in sfx
        ],
        "ffmpeg": {
            "mixing": "narration(front) + music(sidechain-ducked) + ambience(constant audible bed + swell automation) + sfx(one-shots), two-pass loudnorm I=-14",
            "output_expected": str(out_wav),
            "filter_complex": graph,
            "command": command_str,
        },
        "library_root": str(lib),
        "provenance": {
            "script_md": rel(script_md),
            "script_md_sha256": sha256_text(script_md.read_text("utf-8")),
            "narration_index": rel(index_path),
            "narration_index_sha256": sha256_text(index_path.read_text("utf-8")),
            "deterministic": True,
        },
        "side_effects": {
            "external_cost_usd": 0,
            "external_calls": [],
            "wrote_files": [rel(out_path)] + ([str(out_wav)] if ran_ffmpeg else []),
            "ran_ffmpeg": ran_ffmpeg,
        },
    }

    # atomic write (temp + rename) per rule 14
    out_path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(provenance, indent=2, ensure_ascii=False) + "\n"
    tmp = out_path.with_suffix(out_path.suffix + ".tmp")
    tmp.write_text(payload, encoding="utf-8")
    tmp.replace(out_path)

    # ---- console summary ----
    print(f"provenance -> {out_path}")
    print(f"chapters={len(spans)} chunks={len(chunks)} beats={len(beats)} "
          f"total={total:.1f}s ({total / 60:.2f} min)")
    print(f"video-sync: lead={lead:.3f}s (hook {hook_seconds:.2f}+opening {OPENING_SEC}) "
          f"body_len={body_len:.3f}s endcard={ENDCARD_SEC}s -> narration starts at {lead:.3f}s"
          + (f"  [film_data={rel(film_data_path)}]" if film_data_path else "  [no film_data -> legacy body-only]"))
    print(f"timing: measured_chunks={provenance['timeline']['measured_chunks']} "
          f"estimated_chunks={provenance['timeline']['estimated_chunks']}")
    print(f"ambience: {len(set(beds.values()))} distinct beds -> "
          + ", ".join(f"{cid}:{beds[cid]}" for cid, _s, _e, _m in spans))
    print(f"SFX cues: {len(sfx)} (before dedup {len(sfx_raw)}, dropped {dropped}); "
          f"word-triggered={provenance['layers']['sfx']['word_triggered']}; "
          f"swells routed to L3={len(swells)}; unmapped={len(unmapped)}")
    _body_min = max(0.001, (total - ENDCARD_SEC) / 60.0)
    print(f"transient bed: REMOVED (no filler ticks) -> {len(sfx)} meaningful SFX "
          f"({len(set(c.file for c in sfx))} distinct files) "
          f"~{len(sfx) / _body_min:.1f} cues/min over the {_body_min:.1f}-min body")
    print(f"music cues: {len(music_tracks)} ({len(set(music_tracks))} distinct)")
    print(f"density: sfx/min={density['sfx_per_min']} (floor {SFX_PER_MIN_FLOOR}), "
          f"distinct_beds={density['ambience_distinct_beds']} (floor {AMBIENCE_DISTINCT_FLOOR}), "
          f"coverage={density['ambience_coverage']} (floor {AMBIENCE_COVERAGE_FLOOR}) "
          f"-> {'PASS' if density['pass'] else 'FAIL: ' + '; '.join(density['failures'])}")
    if not ran_ffmpeg:
        print("ffmpeg command emitted in provenance.ffmpeg.command (NOT executed).")

    if not density["pass"] and not args.allow_fail:
        print("DENSITY GATE FAILED (anti-しょぼい). Re-run with --allow-fail to keep the provenance.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
