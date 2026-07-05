#!/usr/bin/env python3
r"""Build a 4-layer sound-design PLAN for a long-form PD case film.

The Prime Documentary channel's biggest quality gap is SOUND: episodes ship
with almost no SFX / ambience / musical bed, which makes them feel cheap
("しょぼい"). This tool closes that gap deterministically, the same way
``build_short_mix.py`` / ``build_flashcrash_audio_v001.py`` build shorts and
long-form mixes -- but it operates as a *planner*: it never requires the
narration or bed audio to exist, and it never runs ffmpeg to produce the plan.

It reads the annotated script (chapter / ACT structure) and the ``script.en``
markdown (the literal ``(SFX: ...)`` cues embedded per line), then emits:

  (a) a sound-plan JSON describing every cue on 4 layers:
        L1 narration (front, ducking key / VO priority)
        L2 music     (per-ACT ducked bed -- reveal/tension/somber/outro slots)
        L3 ambience  (continuous low-volume location bed)
        L4 SFX       (one-shots at narration beats and cut boundaries)
  (b) an ffmpeg filter-graph + full command string that mixes the 4 layers
      with sidechain ducking (VO priority) and a final loudnorm I=-14.

A "sound density" self-check FAILS (non-zero exit) if the SFX count / rate or
the ambience coverage falls below a floor -- this is the anti-"しょぼい" gate,
so an empty / silent plan is caught mechanically.

DETERMINISM / IDEMPOTENCY: given the same input scripts the output bytes are
identical (no wall-clock timestamp in the plan; provenance is input-hash based;
all numbers rounded to 3 decimals; cues sorted by (start, layer, id)).

SIDE EFFECTS: writes exactly one JSON file (the plan). No network, no paid API,
no GPU, no video render. ffmpeg is only invoked if BOTH ``--render`` is passed
and ``--dry-run`` is absent AND every input audio file exists; otherwise the
command is only emitted as a string. Default behaviour = plan only.

Usage (self-test on EP32):
  ./.venv/Scripts/python.exe scripts/build_case_sound_design.py \
      --ep PD-2026-032-carsearch --dry-run

Windows paths are handled with pathlib / raw strings (past bug: ``\\Users``
unicode-escape crash).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import subprocess
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parents[1]

SCHEMA_VERSION = "1.0.0"
GENERATOR = "scripts/build_case_sound_design.py"
REVISION_DEFAULT = "v001"
FPS = 30

# ---- timing model (design plan; real narration retimes later) --------------
WPM_DEFAULT = 175.0            # spoken words per minute
GAP_BETWEEN_LINES = 0.35      # breath between narration beats (s)
GAP_BETWEEN_CHAPTERS = 1.0    # longer breath at ACT turns (s)
MIN_BEAT_SEC = 1.2            # floor for a very short narration line
TAIL_SEC = 1.5               # air after the last word

# ---- density gate floors (anti-"しょぼい") ---------------------------------
SFX_TOTAL_FLOOR = 20          # mapped SFX one-shots minimum
SFX_PER_MIN_FLOOR = 2.0       # mapped SFX per minute minimum
AMBIENCE_COVERAGE_FLOOR = 0.85  # fraction of runtime under an ambience bed

# ---- layer gains -----------------------------------------------------------
NARRATION_VOL = 1.0
MUSIC_VOL = 0.22              # ducked bed
AMBIENCE_VOL = 0.06          # very low continuous bed

# ---- chapter -> layer-2 music slot ----------------------------------------
# category folder names under H:\pd-media\library\music\<category>\
CHAPTER_MUSIC: dict[str, tuple[str, str, str]] = {
    # chapter_id: (slot_role, category_folder, candidate_file)
    "hook":    ("hook",     "hook",          "mus_20260614_hook_glass_air_bed_v2.mp3"),
    "opening": ("opening",  "opening",       "mus_20260614_opening_measured_arpeggio_v2.mp3"),
    "act1":    ("tension",  "tension_build", "mus_20260614_tension_build_courtroom_horizon_v2.mp3"),
    "act2":    ("explainer","explainer_bed", "mus_20260614_explainer_bed_soft_explainer_v2.mp3"),
    "act3":    ("reveal",   "reveal",        "mus_20260614_reveal_verdict_at_dawn_v2.mp3"),
    "act4":    ("somber",   "somber",        "mus_20260614_somber_ledger_of_ash_v2.mp3"),
    "ending":  ("outro",    "outro",         "mus_20260614_outro_last_frame_v2.mp3"),
}

# ---- chapter -> default continuous ambience bed (layer 3) ------------------
CHAPTER_AMBIENCE_DEFAULT: dict[str, str] = {
    "hook":    "amb_night_window.mp3",
    "opening": "amb_night_window.mp3",
    "act1":    "amb_night_window.mp3",
    "act2":    "amb_tension_drone.mp3",
    "act3":    "amb_night_window.mp3",
    "act4":    "amb_institutional_drone.mp3",
    "ending":  "amb_night_window.mp3",
}

# location keyword -> ambience file (scanned per chapter to refine the default)
AMBIENCE_KEYWORDS: list[tuple[tuple[str, ...], str]] = [
    (("courthouse", "supreme court", "courtroom", "bench", "marble court"), "amb_courtroom_room_tone.mp3"),
    (("driveway", "porch", "home", "house", "suburban", "residential", "window", "living room"), "amb_night_window.mp3"),
    (("highway", "road", "street", "traffic", "curb", "shoulder"), "amb_night_window.mp3"),
    (("office", "paper", "document", "rental", "agreement", "ledger", "warrant doc"), "amb_office_hum.mp3"),
    (("map", "grid", "nation", "states", "america"), "amb_institutional_drone.mp3"),
    (("hallway", "corridor"), "amb_empty_hallway.mp3"),
]

# ---- SFX phrase -> library file (first match wins; order matters) ----------
# A None target means "not a one-shot" (it is a bed / silence, handled elsewhere).
SFX_SKIP_MARKERS: tuple[str, ...] = (
    "silence", "quiet", "ambient", "room tone", "highway bed", " hum", "engine hum",
    "reassuring pulse", "steady", "ambience",
)
SFX_KEYWORD_MAP: list[tuple[tuple[str, ...], str, float, float]] = [
    # (keywords, filename, dur_hint_sec, linear_volume)
    (("sub-drop", "sub drop"),                         "sfx_sub_drop.mp3",     1.4, 0.20),
    (("riser", "rise", "build"),                       "sfx_riser_2s.mp3",     2.0, 0.20),
    (("low boom", "boom"),                             "sfx_low_boom.mp3",     1.6, 0.22),
    (("gavel", "knock"),                               "sfx_gavel_knock.mp3",  1.0, 0.22),
    (("stamp", "seal"),                                "sfx_stamp_seal.mp3",   0.9, 0.20),
    (("page turn", "page-turn"),                       "sfx_page_turn.mp3",    0.9, 0.18),
    (("shutter", "camera", "photo"),                   "sfx_camera_shutter.mp3", 0.7, 0.16),
    (("pass-by whoosh", "pass by", "pass-by", "whip"), "sfx_whoosh_medium.mp3", 1.2, 0.18),
    (("engine pull", "engine", " pull"),               "sfx_whoosh_medium.mp3", 1.2, 0.18),
    (("whoosh", "swoosh"),                              "sfx_whoosh_short.mp3", 0.8, 0.18),
    (("data-blip", "data blip", "blip", "confirmed"),  "sfx_data_blip.mp3",    0.8, 0.14),
    (("type tick", "period-beat", "period beat"),      "sfx_ui_tick.mp3",      0.5, 0.12),
    (("tick", "check"),                                "sfx_ui_tick.mp3",      0.5, 0.12),
    (("clink", "glass"),                               "sfx_ui_tick.mp3",      0.4, 0.12),
    (("click", "mechanical", "metallic", "lock", "latch", "binder"), "sfx_binder_lock.mp3", 0.7, 0.16),
    (("footstep", "steps"),                            "sfx_soft_impact.mp3",  0.8, 0.12),
    (("impact", "thud", "hit", "slam"),                "sfx_soft_impact.mp3",  1.0, 0.18),
    (("clock", "spins", "spinning"),                   "sfx_clock_tick_loop.mp3", 1.0, 0.10),
    (("swell", "resolving", "warm", "dust", "shimmer", "uncertain"), "sfx_dust_swell.mp3", 1.5, 0.16),
    (("rustle", "paper", "fabric", "tarp", "tear", "upholstery", "cloth", "wind"), "sfx_paper_rustle.mp3", 1.0, 0.16),
    (("note", "pulse", "beat", "tone", "drone", "deep", "drop"), "sfx_sub_drop.mp3", 1.4, 0.18),
]

# transition whoosh auto-placed at every chapter cut boundary (layer 4)
CHAPTER_CUT_SFX = ("sfx_whoosh_short.mp3", 0.8, 0.16)


# ============================================================================
# helpers
# ============================================================================
def round3(x: float) -> float:
    return round(float(x), 3)


def vol_to_db(vol: float) -> float:
    if vol <= 0:
        return -120.0
    return round(20.0 * math.log10(vol), 1)


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


def normalize_header(header: str) -> Optional[str]:
    """Map a markdown ``## ...`` header to a canonical chapter_id."""
    h = header.upper()
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
    return None


CHAPTER_TITLES = {
    "hook": "Hook",
    "opening": "Opening",
    "act1": "ACT I",
    "act2": "ACT II",
    "act3": "ACT III",
    "act4": "ACT IV",
    "ending": "Ending / CTA",
}


# ============================================================================
# parse the script
# ============================================================================
@dataclass
class Beat:
    chapter_id: str
    index: int
    text: str
    sfx_text: str = ""
    vis_text: str = ""
    start: float = 0.0
    end: float = 0.0


def clean_vo(line: str) -> str:
    text = re.sub(r"^\[VO:\]\s*", "", line.strip())
    text = re.sub(r"\s*(?:\[CLM-[0-9]{4}\]\s*)+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def extract_bracket(line: str, tag: str) -> str:
    """Return the text inside ``(TAG: ...)`` on this line, else empty."""
    m = re.search(rf"\({tag}:\s*(.+?)\)\s*(?:\({tag}|\(SFX:|\(VIS:|$)", line)
    if not m:
        m = re.search(rf"\({tag}:\s*(.+)\)", line)
    return m.group(1).strip() if m else ""


def parse_script_md(md_path: str | Path) -> list[Beat]:
    """Parse [VO:] beats + their (VIS:)/(SFX:) production notes, per chapter."""
    lines = Path(md_path).read_text("utf-8").splitlines()
    beats: list[Beat] = []
    chapter: Optional[str] = None
    idx = 0
    pending: Optional[Beat] = None
    for raw in lines:
        line = raw.rstrip()
        if line.startswith("## "):
            chapter = normalize_header(line[3:].strip())
            continue
        if chapter is None:
            continue
        if line.startswith("[VO:]"):
            pending = Beat(chapter_id=chapter, index=idx, text=clean_vo(line))
            beats.append(pending)
            idx += 1
            continue
        # production annotation line attached to the most recent beat
        if pending is not None and ("(SFX:" in line or "(VIS:" in line):
            sfx = extract_bracket(line, "SFX")
            vis = extract_bracket(line, "VIS")
            if sfx:
                pending.sfx_text = (pending.sfx_text + " " + sfx).strip() if pending.sfx_text else sfx
            if vis:
                pending.vis_text = (pending.vis_text + " " + vis).strip() if pending.vis_text else vis
    return beats


def schedule_beats(beats: list[Beat], wpm: float) -> float:
    """Assign start/end to each beat from a WPM word-count model. Returns total."""
    cursor = 0.0
    for i, beat in enumerate(beats):
        words = max(1, len(beat.text.split()))
        dur = max(MIN_BEAT_SEC, words / wpm * 60.0)
        beat.start = round3(cursor)
        beat.end = round3(cursor + dur)
        cursor += dur
        nxt = beats[i + 1] if i + 1 < len(beats) else None
        if nxt is not None:
            cursor += GAP_BETWEEN_CHAPTERS if nxt.chapter_id != beat.chapter_id else GAP_BETWEEN_LINES
    return round3(cursor + TAIL_SEC)


# ============================================================================
# cue construction
# ============================================================================
@dataclass
class Cue:
    cue_id: str
    layer: int
    role: str
    chapter_id: str
    file: Optional[str]        # library-relative path, or None (marker / unmapped)
    start: float
    end: Optional[float]
    volume: float
    gain_db: float
    source: str
    phrase: str = ""
    ducked: bool = False
    marker: bool = False


def chapter_spans(beats: list[Beat], total: float) -> list[tuple[str, float, float]]:
    """Gapless [start, end) span per chapter in first-appearance order."""
    order: list[str] = []
    starts: dict[str, float] = {}
    for beat in beats:
        if beat.chapter_id not in starts:
            starts[beat.chapter_id] = beat.start
            order.append(beat.chapter_id)
    spans: list[tuple[str, float, float]] = []
    for i, ch in enumerate(order):
        s = starts[ch]
        e = starts[order[i + 1]] if i + 1 < len(order) else total
        spans.append((ch, round3(s), round3(e)))
    return spans


def choose_ambience(chapter_id: str, text: str) -> str:
    """Refine the per-chapter default bed by scanning location keywords."""
    best_file = CHAPTER_AMBIENCE_DEFAULT.get(chapter_id, "amb_tension_drone.mp3")
    best_hits = 0
    low = text.lower()
    for keywords, fname in AMBIENCE_KEYWORDS:
        hits = sum(low.count(k) for k in keywords)
        if hits > best_hits:
            best_hits = hits
            best_file = fname
    return best_file


def split_sfx_phrase(phrase: str) -> list[str]:
    parts = re.split(r";|,|\bthen\b|\binto\b", phrase)
    return [p.strip(" .'\"") for p in parts if p.strip(" .'\"")]


def map_sfx_fragment(fragment: str) -> Optional[tuple[str, float, float]]:
    low = fragment.lower()
    for marker in SFX_SKIP_MARKERS:
        if marker in low:
            return None
    for keywords, fname, dur, vol in SFX_KEYWORD_MAP:
        for kw in keywords:
            if kw in low:
                return fname, dur, vol
    return None


def build_cues(
    beats: list[Beat],
    spans: list[tuple[str, float, float]],
    total: float,
) -> tuple[list[Cue], list[Cue], list[Cue], list[Cue], list[dict]]:
    """Return (music, ambience, sfx, narration_key_cues, unmapped)."""
    music: list[Cue] = []
    ambience: list[Cue] = []
    sfx: list[Cue] = []
    unmapped: list[dict] = []

    # L2 music -- one ducked slot marker per chapter
    for i, (ch, s, e) in enumerate(spans, start=1):
        role, folder, fname = CHAPTER_MUSIC.get(ch, ("bed", "explainer_bed",
                                                     "mus_20260614_explainer_bed_soft_explainer_v2.mp3"))
        music.append(Cue(
            cue_id=f"L2-{i:02d}",
            layer=2, role=f"music_{role}", chapter_id=ch,
            file=f"music/{folder}/{fname}", start=s, end=e,
            volume=MUSIC_VOL, gain_db=vol_to_db(MUSIC_VOL),
            source="act_slot", ducked=True, marker=True,
        ))

    # L3 ambience -- continuous location bed per chapter (gapless)
    beats_by_ch: dict[str, list[Beat]] = {}
    for beat in beats:
        beats_by_ch.setdefault(beat.chapter_id, []).append(beat)
    for i, (ch, s, e) in enumerate(spans, start=1):
        ch_text = " ".join(b.vis_text + " " + b.text for b in beats_by_ch.get(ch, []))
        fname = choose_ambience(ch, ch_text)
        ambience.append(Cue(
            cue_id=f"L3-{i:02d}",
            layer=3, role="ambience_bed", chapter_id=ch,
            file=f"ambience/{fname}", start=s, end=e,
            volume=AMBIENCE_VOL, gain_db=vol_to_db(AMBIENCE_VOL),
            source="location_bed", ducked=True,
        ))

    # L4 SFX -- chapter-cut whooshes + literal (SFX:) cues per beat
    sfx_n = 0
    seen_cuts: set[str] = set()
    for ch, s, e in spans:
        if ch in seen_cuts:
            continue
        seen_cuts.add(ch)
        fname, dur, vol = CHAPTER_CUT_SFX
        sfx_n += 1
        sfx.append(Cue(
            cue_id=f"L4-{sfx_n:03d}",
            layer=4, role="transition_cut", chapter_id=ch,
            file=f"sfx/{fname}", start=round3(s), end=round3(s + dur),
            volume=vol, gain_db=vol_to_db(vol),
            source="chapter_cut", phrase=f"cut into {CHAPTER_TITLES.get(ch, ch)}",
        ))

    for beat in beats:
        if not beat.sfx_text:
            continue
        fragments = split_sfx_phrase(beat.sfx_text)
        offset = 0.10
        for frag in fragments:
            mapped = map_sfx_fragment(frag)
            if mapped is None:
                unmapped.append({"chapter_id": beat.chapter_id, "beat": beat.index,
                                 "phrase": frag, "reason": "no_keyword_or_bed_or_silence"})
                continue
            fname, dur, vol = mapped
            start = round3(min(beat.start + offset, max(beat.start, beat.end - 0.05)))
            sfx_n += 1
            sfx.append(Cue(
                cue_id=f"L4-{sfx_n:03d}",
                layer=4, role="sfx_cue", chapter_id=beat.chapter_id,
                file=f"sfx/{fname}", start=start, end=round3(start + dur),
                volume=vol, gain_db=vol_to_db(vol),
                source="script_sfx", phrase=frag,
            ))
            offset += 0.45

    sfx.sort(key=lambda c: (c.start, c.cue_id))

    # L1 narration ducking keys (documented, not audio one-shots)
    narration = [Cue(
        cue_id="L1-01", layer=1, role="narration_master", chapter_id="all",
        file=None, start=0.0, end=total, volume=NARRATION_VOL,
        gain_db=0.0, source="voice_master", marker=True,
    )]
    return music, ambience, sfx, narration, unmapped


# ============================================================================
# ffmpeg filter-graph + command
# ============================================================================
def build_ffmpeg(
    narration_path: str,
    music: list[Cue],
    ambience: list[Cue],
    sfx: list[Cue],
    total: float,
    lib: Path,
    out_wav: str,
) -> tuple[str, list[str]]:
    """Assemble a 4-layer ducked filter_complex + full argv. String only."""
    inputs: list[str] = ["-i", narration_path]
    filters: list[str] = []

    music_idx0 = 1
    for _ in music:
        inputs += ["-stream_loop", "-1", "-i", ""]  # path filled below
    amb_idx0 = music_idx0 + len(music)
    for _ in ambience:
        inputs += ["-stream_loop", "-1", "-i", ""]
    sfx_idx0 = amb_idx0 + len(ambience)
    for _ in sfx:
        inputs += ["-i", ""]

    # fill real library paths into the placeholder -i slots
    slot = 0
    input_paths: list[str] = []
    for cue in [*music, *ambience, *sfx]:
        input_paths.append(str(lib / cue.file))
    # rewrite inputs list with paths
    inputs = ["-i", narration_path]
    for cue in music:
        inputs += ["-stream_loop", "-1", "-i", str(lib / cue.file)]
    for cue in ambience:
        inputs += ["-stream_loop", "-1", "-i", str(lib / cue.file)]
    for cue in sfx:
        inputs += ["-i", str(lib / cue.file)]

    # narration -> [vo] + two ducking keys (music, ambience)
    filters.append(f"[0:a]aresample=48000,volume={NARRATION_VOL},"
                   f"apad,atrim=0:{total:.3f},asetpts=PTS-STARTPTS,asplit=3[vo][kmus][kamb]")

    # music layer (looped per-chapter segments)
    m_labels: list[str] = []
    for i, cue in enumerate(music):
        idx = music_idx0 + i
        seg = max(0.1, (cue.end or total) - cue.start)
        delay = int(round(cue.start * 1000))
        filters.append(
            f"[{idx}:a]atrim=0:{seg:.3f},asetpts=PTS-STARTPTS,volume={cue.volume},"
            f"afade=t=in:st=0:d=0.4,afade=t=out:st={max(0.0, seg - 0.6):.3f}:d=0.6,"
            f"adelay={delay}|{delay}[m{i}]")
        m_labels.append(f"[m{i}]")
    filters.append(f"{''.join(m_labels)}amix=inputs={len(m_labels)}:normalize=0:dropout_transition=0[musraw]")
    filters.append("[musraw][kmus]sidechaincompress=threshold=0.03:ratio=8:attack=25:release=320[musd]")

    # ambience layer (looped continuous beds)
    a_labels: list[str] = []
    for i, cue in enumerate(ambience):
        idx = amb_idx0 + i
        seg = max(0.1, (cue.end or total) - cue.start)
        delay = int(round(cue.start * 1000))
        filters.append(
            f"[{idx}:a]atrim=0:{seg:.3f},asetpts=PTS-STARTPTS,volume={cue.volume},"
            f"afade=t=in:st=0:d=0.5,afade=t=out:st={max(0.0, seg - 0.5):.3f}:d=0.5,"
            f"adelay={delay}|{delay}[a{i}]")
        a_labels.append(f"[a{i}]")
    filters.append(f"{''.join(a_labels)}amix=inputs={len(a_labels)}:normalize=0:dropout_transition=0[ambraw]")
    filters.append("[ambraw][kamb]sidechaincompress=threshold=0.02:ratio=6:attack=40:release=500[ambd]")

    # sfx layer (one-shots)
    s_labels: list[str] = []
    for i, cue in enumerate(sfx):
        idx = sfx_idx0 + i
        delay = int(round(cue.start * 1000))
        dur = max(0.1, (cue.end or cue.start + 0.5) - cue.start)
        filters.append(
            f"[{idx}:a]atrim=0:{dur:.3f},asetpts=PTS-STARTPTS,volume={cue.volume},"
            f"adelay={delay}|{delay}[s{i}]")
        s_labels.append(f"[s{i}]")
    filters.append(f"{''.join(s_labels)}amix=inputs={len(s_labels)}:normalize=0:dropout_transition=0[sfxraw]")

    # final mix: VO front, ducked music + ambience beds, SFX at cuts; loudnorm -14
    filters.append(
        "[vo][musd][ambd][sfxraw]amix=inputs=4:weights=1 0.9 0.7 0.95:normalize=0:duration=first,"
        f"atrim=0:{total:.3f},loudnorm=I=-14:TP=-1.5:LRA=11:linear=false,"
        "alimiter=level_in=1:level_out=1:limit=0.95[aout]")

    graph = ";".join(filters)
    argv = ["ffmpeg", "-y", *inputs,
            "-filter_complex", graph,
            "-map", "[aout]", "-t", f"{total:.3f}",
            "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", out_wav]
    return graph, argv


def quote_arg(arg: str) -> str:
    if arg == "" or re.search(r"[\s\\]", arg):
        return '"' + arg.replace('"', r"\"") + '"'
    return arg


# ============================================================================
# density gate
# ============================================================================
def compute_density(sfx: list[Cue], ambience: list[Cue], total: float) -> dict:
    mapped = [c for c in sfx if c.file]
    sfx_count = len(mapped)
    minutes = max(0.001, total / 60.0)
    sfx_per_min = sfx_count / minutes

    # ambience coverage = union of bed spans / total
    intervals = sorted((c.start, c.end or total) for c in ambience if c.file)
    covered = 0.0
    cur_s: Optional[float] = None
    cur_e: Optional[float] = None
    for s, e in intervals:
        if cur_s is None:
            cur_s, cur_e = s, e
        elif s <= (cur_e or s):
            cur_e = max(cur_e or e, e)
        else:
            covered += (cur_e or cur_s) - cur_s
            cur_s, cur_e = s, e
    if cur_s is not None:
        covered += (cur_e or cur_s) - cur_s
    coverage = covered / total if total > 0 else 0.0

    failures: list[str] = []
    if sfx_count < SFX_TOTAL_FLOOR:
        failures.append(f"sfx_count {sfx_count} < floor {SFX_TOTAL_FLOOR}")
    if sfx_per_min < SFX_PER_MIN_FLOOR:
        failures.append(f"sfx_per_min {sfx_per_min:.2f} < floor {SFX_PER_MIN_FLOOR}")
    if coverage < AMBIENCE_COVERAGE_FLOOR:
        failures.append(f"ambience_coverage {coverage:.3f} < floor {AMBIENCE_COVERAGE_FLOOR}")

    return {
        "sfx_mapped": sfx_count,
        "sfx_per_min": round3(sfx_per_min),
        "ambience_coverage": round3(coverage),
        "floors": {
            "sfx_total": SFX_TOTAL_FLOOR,
            "sfx_per_min": SFX_PER_MIN_FLOOR,
            "ambience_coverage": AMBIENCE_COVERAGE_FLOOR,
        },
        "pass": not failures,
        "failures": failures,
    }


# ============================================================================
# main
# ============================================================================
def cue_dict(cue: Cue) -> dict:
    d = asdict(cue)
    return {k: v for k, v in d.items() if not (v == "" and k == "phrase")}


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    ap = argparse.ArgumentParser(description="Build a 4-layer sound-design plan for a PD case film.")
    ap.add_argument("--ep", required=True, help="episode slug, e.g. PD-2026-032-carsearch")
    ap.add_argument("--script", help="path to script.en markdown (default: episodes/<ep>/03_script/script.en.v001.md)")
    ap.add_argument("--annotated", help="path to annotated script JSON (optional structure cross-check)")
    ap.add_argument("--scene-plan", help="optional scene_plan cut list JSON (reserved; not required)")
    ap.add_argument("--out", help="output plan path (default: episodes/<ep>/06_audio/sound_design.v001.json)")
    ap.add_argument("--revision", default=REVISION_DEFAULT)
    ap.add_argument("--wpm", type=float, default=WPM_DEFAULT)
    ap.add_argument("--dry-run", action="store_true", help="emit plan + ffmpeg command only; never run ffmpeg")
    ap.add_argument("--render", action="store_true", help="run ffmpeg (only if inputs exist and not --dry-run)")
    ap.add_argument("--allow-fail", action="store_true", help="write plan even if density gate fails (exit still non-zero)")
    args = ap.parse_args()

    ep = args.ep
    ep_dir = ROOT / "episodes" / ep
    script_md = Path(args.script) if args.script else ep_dir / "03_script" / "script.en.v001.md"
    annotated = Path(args.annotated) if args.annotated else ep_dir / "03_script" / "script.annotated.v001.json"
    out_path = Path(args.out) if args.out else ep_dir / "06_audio" / f"sound_design.{args.revision}.json"

    if not script_md.exists():
        print(f"ERROR: script not found: {script_md}", file=sys.stderr)
        return 2

    lib = media_root() / "library"

    # optional annotated cross-check (episode id, span/chapter count, thesis)
    annotated_meta: dict = {}
    if annotated.exists():
        try:
            adata = json.loads(annotated.read_text("utf-8"))
            annotated_meta = {
                "episode_id": adata.get("episode_id"),
                "chapters": len(adata.get("chapters", [])),
                "spans": len(adata.get("spans", [])),
                "estimated_duration_seconds": adata.get("estimated_duration_seconds"),
            }
        except Exception as err:  # untrusted input -> never fatal
            annotated_meta = {"warning": f"could not parse annotated JSON: {err}"}

    md_text = script_md.read_text("utf-8")
    beats = parse_script_md(script_md)
    if not beats:
        print("ERROR: no [VO:] beats parsed from script", file=sys.stderr)
        return 2
    total = schedule_beats(beats, args.wpm)
    spans = chapter_spans(beats, total)
    music, ambience, sfx, narration, unmapped = build_cues(beats, spans, total)
    density = compute_density(sfx, ambience, total)

    # expected (not-yet-existing) narration master + mix output paths (media root)
    narration_master = str(media_root() / "episodes" / ep / "06_voice" / "master" / "vc_master_v001.mp3")
    out_wav = str(media_root() / "episodes" / ep / "06_audio" / "mix" / f"{ep}_sound_design_{args.revision}.wav")
    graph, argv = build_ffmpeg(narration_master, music, ambience, sfx, total, lib, out_wav)
    command_str = " ".join(quote_arg(a) for a in argv)

    plan = {
        "schema_version": SCHEMA_VERSION,
        "episode_id": ep,
        "revision": args.revision,
        "generator": GENERATOR,
        "fps": FPS,
        "timeline": {
            "wpm": args.wpm,
            "estimated_total_sec": total,
            "voice_end_sec": round3(max(b.end for b in beats)),
            "tail_sec": TAIL_SEC,
            "beats": len(beats),
            "source": "wpm_word_count_model (design plan; real narration retimes downstream)",
        },
        "chapters": [
            {"chapter_id": ch, "title": CHAPTER_TITLES.get(ch, ch), "start": s, "end": e}
            for ch, s, e in spans
        ],
        "layers": {
            "L1_narration": {
                "role": "front / ducking-priority (VO wins)",
                "master_uri": f"artifact://episodes/{ep}/06_voice/master/vc_master_v001.mp3",
                "master_path_expected": narration_master,
                "gain_db": 0.0,
                "note": "narration audio may not exist yet; this is a plan.",
                "cues": [cue_dict(c) for c in narration],
            },
            "L2_music": {
                "role": "per-ACT ducked musical bed (slot markers: reveal/tension/somber/outro/...)",
                "count": len(music),
                "cues": [cue_dict(c) for c in music],
            },
            "L3_ambience": {
                "role": "continuous low-volume location bed",
                "count": len(ambience),
                "cues": [cue_dict(c) for c in ambience],
            },
            "L4_sfx": {
                "role": "one-shots at narration beats + cut boundaries",
                "count": len(sfx),
                "cues": [cue_dict(c) for c in sfx],
            },
        },
        "density_gate": density,
        "unmapped_sfx": unmapped,
        "ffmpeg": {
            "mixing": "narration(front) + music(ducked) + ambience(bed) + sfx(cuts), sidechain VO priority, loudnorm I=-14",
            "output_expected": out_wav,
            "filter_complex": graph,
            "command": command_str,
        },
        "library_root": str(lib),
        "annotated_crosscheck": annotated_meta,
        "provenance": {
            "script_md": str(script_md.relative_to(ROOT)) if script_md.is_relative_to(ROOT) else str(script_md),
            "script_md_sha256": sha256_text(md_text),
            "annotated_json": str(annotated.relative_to(ROOT)) if annotated.exists() and annotated.is_relative_to(ROOT) else None,
            "wpm": args.wpm,
            "deterministic": True,
        },
        "side_effects": {
            "external_cost_usd": 0,
            "external_calls": [],
            "wrote_files": [str(out_path.relative_to(ROOT)) if out_path.is_relative_to(ROOT) else str(out_path)],
            "ran_ffmpeg": False,
        },
    }

    # atomic write (temp + rename) per rule 14
    out_path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(plan, indent=2, ensure_ascii=False) + "\n"
    tmp = out_path.with_suffix(out_path.suffix + ".tmp")
    tmp.write_text(payload, encoding="utf-8")
    tmp.replace(out_path)

    print(f"plan -> {out_path}")
    print(f"chapters={len(spans)} beats={len(beats)} total={total:.1f}s ({total/60:.2f} min)")
    print(f"L2 music slots={len(music)}  L3 ambience beds={len(ambience)}  "
          f"L4 sfx cues={len(sfx)} (mapped={density['sfx_mapped']}, unmapped={len(unmapped)})")
    print(f"density: sfx/min={density['sfx_per_min']} (floor {SFX_PER_MIN_FLOOR}), "
          f"ambience_coverage={density['ambience_coverage']} (floor {AMBIENCE_COVERAGE_FLOOR}) "
          f"-> {'PASS' if density['pass'] else 'FAIL: ' + '; '.join(density['failures'])}")
    print("ffmpeg command emitted in plan.ffmpeg.command (NOT executed).")

    ran_ffmpeg = False
    if args.render and not args.dry_run:
        missing = [p for p in [narration_master, *[str(lib / c.file) for c in [*music, *ambience, *sfx]]]
                   if not Path(p).exists()]
        if missing:
            print(f"--render skipped: {len(missing)} input(s) missing (e.g. {missing[0]})")
        else:
            Path(out_wav).parent.mkdir(parents=True, exist_ok=True)
            subprocess.run(argv, check=True)
            ran_ffmpeg = True
            print(f"rendered mix -> {out_wav}")

    if not density["pass"] and not args.allow_fail:
        print("DENSITY GATE FAILED (anti-しょぼい). Re-run with --allow-fail to keep the plan.", file=sys.stderr)
        return 1
    return 0 if (density["pass"] or args.allow_fail) and (ran_ffmpeg or not args.render or args.dry_run) else 1


if __name__ == "__main__":
    raise SystemExit(main())
