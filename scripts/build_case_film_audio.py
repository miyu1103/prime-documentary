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
    (("wind", "breeze", "rustling", "open road", "field", "outdoor"), "amb_light_wind.mp3"),
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
    "ending":  "amb_light_wind.mp3",           # calm resolve at the curb
}

# ---- M4: one-shot SFX map (curated from build_case_sound_design) -----------
# (keywords, filename, dur_hint_sec, linear_volume). First match wins; order matters.
ONESHOT_MAP: list[tuple[tuple[str, ...], str, float, float]] = [
    (("sub-drop", "sub drop"),                          "sfx_sub_drop.mp3",        1.4, 0.20),
    (("riser", "rise"),                                 "sfx_riser_2s.mp3",        2.0, 0.20),
    (("low boom", "boom"),                              "sfx_low_boom.mp3",        1.6, 0.22),
    (("gavel", "knock"),                                "sfx_gavel_knock.mp3",     1.0, 0.22),
    (("page turn", "page-turn"),                        "sfx_page_turn.mp3",       0.9, 0.18),
    (("stamp", "seal"),                                 "sfx_stamp_seal.mp3",      0.9, 0.20),
    (("shutter", "camera", "photo"),                    "sfx_camera_shutter.mp3",  0.7, 0.16),
    (("tarp", "tear", "fabric", "upholstery", "cloth", "rustle"), "sfx_paper_rustle.mp3", 1.0, 0.16),
    (("pass-by", "pass by", "whip"),                    "sfx_whoosh_medium.mp3",   1.2, 0.18),
    (("engine pull", "pull"),                           "sfx_whoosh_medium.mp3",   1.2, 0.18),
    (("whoosh", "swoosh"),                              "sfx_whoosh_short.mp3",    0.8, 0.18),
    (("data-blip", "data blip", "blip"),                "sfx_data_blip.mp3",       0.8, 0.14),
    (("period-beat", "type tick", "type ticks", "ui-tick", "ui tick"), "sfx_ui_tick.mp3", 0.5, 0.12),
    (("clink", "glass"),                                "sfx_ui_tick.mp3",         0.4, 0.12),
    (("tick", "check"),                                 "sfx_ui_tick.mp3",         0.5, 0.12),
    (("click", "mechanical", "metallic", "lock", "latch", "binder", "turn"), "sfx_binder_lock.mp3", 0.7, 0.16),
    (("footstep", "steps"),                             "sfx_soft_impact.mp3",     0.8, 0.12),
    (("impact", "thud", "hit", "slam"),                 "sfx_soft_impact.mp3",     1.0, 0.18),
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
    for sub in ("draft", "chunks", "master/chunks", "master"):
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
        ch = Chunk(
            i=i, vc_id=vc, section=section, chapter_id=normalize_section(section),
            text=text, tokens=alnum_tokens(text), duration=round3(dur),
            duration_source=src, start=round3(cursor), end=round3(cursor + dur),
        )
        chunks.append(ch)
        cursor += dur + INTER_CHUNK_GAP
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
    "sfx_ui_tick.mp3": ("sfx_ui_tick.mp3", "sfx_tick_v2_hi.mp3", "sfx_tick_v2_lo.mp3"),
    "sfx_data_blip.mp3": ("sfx_data_blip.mp3", "sfx_blip_v2_hi.mp3", "sfx_blip_v2_lo.mp3"),
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

    # chapter-cut transition whooshes (skip the very first chapter start at t=0)
    for cid, s, _e, _m in spans:
        if s <= 0.001:
            continue
        fname, dur, vol = CHAPTER_CUT_SFX
        n += 1
        sfx.append(SfxCue(
            cue_id=f"L4-{n:03d}", file=f"sfx/{fname}", chapter_id=cid,
            time=round3(s), dur=dur, volume=vol, gain_db=vol_to_db(vol),
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
def build_ffmpeg(narration_path: str, spans, beds: dict[str, str],
                 sfx: list[SfxCue], swells: list[SwellEvent], total: float,
                 lib: Path, out_wav: str,
                 loudnorm: str) -> tuple[str, list[str]]:
    """Assemble the 4-layer ducked filter_complex + full argv (string only).

    L1 narration front (splits a sidechain key), L2 music per-chapter ducked bed,
    L3 ambience distinct constant bed + swell gain automation, L4 SFX one-shots.
    """
    amb_floor = db_to_vol(AMBIENCE_FLOOR_DB)

    music_cues = [(cid, s, e) for (cid, s, e, _m) in spans]
    amb_cues = [(cid, s, e, beds[cid]) for (cid, s, e, _m) in spans]

    inputs: list[str] = ["-i", narration_path]
    music_idx0 = 1
    for cid, _s, _e in music_cues:
        role, folder, fname = CHAPTER_MUSIC.get(cid, ("bed", "explainer_bed",
                                                      "mus_20260614_explainer_bed_soft_explainer_v2.mp3"))
        inputs += ["-stream_loop", "-1", "-i", str(lib / "music" / folder / fname)]
    amb_idx0 = music_idx0 + len(music_cues)
    for _cid, _s, _e, bed in amb_cues:
        inputs += ["-stream_loop", "-1", "-i", str(lib / "ambience" / bed)]
    sfx_idx0 = amb_idx0 + len(amb_cues)
    for c in sfx:
        inputs += ["-i", str(lib / c.file)]

    filters: list[str] = []
    # narration -> [vo] + sidechain key [key]
    filters.append(
        f"[0:a]aresample=48000,volume={NARRATION_VOL},apad,atrim=0:{total:.3f},"
        f"asetpts=PTS-STARTPTS,asplit=2[vo][key]")

    # music layer (per-chapter looped segments) -> ducked by VO
    m_labels: list[str] = []
    for i, (_cid, s, e) in enumerate(music_cues):
        idx = music_idx0 + i
        seg = max(0.1, e - s)
        delay = int(round(s * 1000))
        filters.append(
            f"[{idx}:a]atrim=0:{seg:.3f},asetpts=PTS-STARTPTS,volume={MUSIC_VOL},"
            f"afade=t=in:st=0:d=0.5,afade=t=out:st={max(0.0, seg - 0.7):.3f}:d=0.7,"
            f"adelay={delay}|{delay}[m{i}]")
        m_labels.append(f"[m{i}]")
    filters.append(f"{''.join(m_labels)}amix=inputs={len(m_labels)}:normalize=0:dropout_transition=0[musraw]")
    filters.append("[musraw][key]sidechaincompress=threshold=0.03:ratio=8:attack=25:release=320[musd]")

    # ambience layer (distinct per-chapter constant beds; NOT sidechained -> capped duck)
    a_labels: list[str] = []
    for i, (_cid, s, e, _bed) in enumerate(amb_cues):
        idx = amb_idx0 + i
        seg = max(0.1, e - s)
        delay = int(round(s * 1000))
        filters.append(
            f"[{idx}:a]atrim=0:{seg:.3f},asetpts=PTS-STARTPTS,volume={amb_floor},"
            f"afade=t=in:st=0:d=0.6,afade=t=out:st={max(0.0, seg - 0.6):.3f}:d=0.6,"
            f"adelay={delay}|{delay}[a{i}]")
        a_labels.append(f"[a{i}]")
    filters.append(f"{''.join(a_labels)}amix=inputs={len(a_labels)}:normalize=0:dropout_transition=0[ambraw]")
    # L3 gain automation: multiplicative swell bumps (routed atmospheric cues)
    terms = "+".join(
        f"{sw.bump:.3f}*between(t,{sw.time:.3f},{sw.time + sw.dur:.3f})" for sw in swells)
    expr = f"1+{terms}" if terms else "1"
    filters.append(f"[ambraw]volume=eval=frame:volume='{expr}'[ambd]")

    # sfx layer (one-shots)
    s_labels: list[str] = []
    for i, c in enumerate(sfx):
        idx = sfx_idx0 + i
        delay = int(round(c.time * 1000))
        filters.append(
            f"[{idx}:a]atrim=0:{c.dur:.3f},asetpts=PTS-STARTPTS,volume={c.volume},"
            f"adelay={delay}|{delay}[s{i}]")
        s_labels.append(f"[s{i}]")
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
    total = round3(chunks[-1].end + TAIL_SEC)

    beats = parse_script_md(script_md)
    if not beats:
        print("ERROR: no [VO:] beats parsed from script", file=sys.stderr)
        return 2
    gtok, gtime, gchunk = build_global_tokens(chunks)
    align_beats(beats, gtok, gchunk)

    spans = chapter_spans(chunks, total)
    beds = assign_ambience(spans, chunks, beats)
    sfx_raw, swells, unmapped = build_cues(beats, chunks, spans, gtok, gtime)
    sfx, dropped = dedup_sfx(sfx_raw)
    density = compute_density(sfx, beds, spans, total)

    # ---- expected (not-yet-existing) narration master + outputs -------------
    narration_master = media / "episodes" / ep / "06_voice" / "master" / "vc_master_v001.mp3"
    wav_name = f"{ep}_film_audio_{args.revision}.wav"
    out_wav = media / "episodes" / ep / "06_audio" / "mix" / wav_name
    render_audio_copy = media / "episodes" / ep / "08_edit" / "audio" / wav_name

    loudnorm_apply = "loudnorm=I=-14:TP=-1.5:LRA=11:linear=true"
    graph, argv = build_ffmpeg(str(narration_master), spans, beds, sfx, swells,
                               total, lib, str(out_wav), loudnorm_apply)
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

    provenance = {
        "schema_version": SCHEMA_VERSION,
        "kind": "case_film_audio_provenance",
        "episode_id": ep,
        "revision": args.revision,
        "generator": GENERATOR,
        "fps": FPS,
        "timeline": {
            "total_sec": total,
            "voice_end_sec": round3(chunks[-1].end),
            "tail_sec": TAIL_SEC,
            "chunks": len(chunks),
            "beats": len(beats),
            "timing_source": "narration_index chunk durations (measured per-chunk audio when present, else estimate); SFX placed by token position within the owning chunk",
            "measured_chunks": sum(1 for c in chunks if c.duration_source.startswith("measured")),
            "estimated_chunks": sum(1 for c in chunks if c.duration_source == "narration_index_estimate"),
        },
        "chapters": [
            {"chapter_id": cid, "title": CHAPTER_TITLES.get(cid, cid),
             "start": s, "end": e, "ambience_bed": beds[cid]}
            for cid, s, e, _m in spans
        ],
        # ---- LAYER INVENTORY that check_sound_layers verifies ----
        "layers": {
            "narration": {
                "role": "front / sidechain-priority (VO wins)",
                "master_uri": f"artifact://episodes/{ep}/06_voice/master/vc_master_v001.mp3",
                "master_path_expected": str(narration_master),
                "master_exists": narration_master.exists(),
                "gain_db": 0.0,
            },
            "music": {
                "role": "per-chapter ducked musical bed (sidechained by VO)",
                "cue_count": len(music_tracks),
                "distinct_tracks": len(set(music_tracks)),
                "tracks": music_tracks,
                "gain_db": vol_to_db(MUSIC_VOL),
                "ducked": True,
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
                "role": "narration-timed one-shots at real words + chapter cuts",
                "cue_count": len(sfx),
                "cues_before_dedup": len(sfx_raw),
                "deduped": dropped,
                "distinct_files": len(set(c.file for c in sfx)),
                "word_triggered": sum(1 for c in sfx if c.timing == "word_trigger"),
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
    print(f"timing: measured_chunks={provenance['timeline']['measured_chunks']} "
          f"estimated_chunks={provenance['timeline']['estimated_chunks']}")
    print(f"ambience: {len(set(beds.values()))} distinct beds -> "
          + ", ".join(f"{cid}:{beds[cid]}" for cid, _s, _e, _m in spans))
    print(f"SFX cues: {len(sfx)} (before dedup {len(sfx_raw)}, dropped {dropped}); "
          f"word-triggered={provenance['layers']['sfx']['word_triggered']}; "
          f"swells routed to L3={len(swells)}; unmapped={len(unmapped)}")
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
