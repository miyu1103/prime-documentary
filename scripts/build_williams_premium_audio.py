#!/usr/bin/env python3
r"""Build the BEATSHEET-TIMED 4-layer audio mix for EP36 "williams" premium film.

WHY THIS FILE EXISTS
--------------------
EP36 was rebuilt as a premium code-driven Remotion composition ``WilliamsFilm``
(713.37s / 21401f @30fps). Unlike the flat CaseFilm layout that
``scripts/build_case_film_audio.py`` targets, WilliamsFilm INTERSPERSES the
narration with opening / act-title / breath / transition beats, so the narration
is NO LONGER one continuous block: each narration span must play at its OWN film
time (``beat.start_frame/30``). The previously-built continuous mix
(``..._film_audio_v001.wav`` ~635s) does NOT sync with this 713s film.

This tool EXTENDS ``build_case_film_audio`` (CLAUDE invariant 14: extend, don't
reinvent). It imports that module's proven library maps + mix/loudnorm helpers +
``build_ffmpeg`` VERBATIM, and only replaces the TIMING model: it drives the
NARRATION + SFX placement from the beatsheet's per-beat film times instead of a
single continuous narration lead.

THE TIMING MODEL (the one real difference from build_case_film_audio)
--------------------------------------------------------------------
Source of truth: ``episodes/<ep>/04_scenes/premium_beatsheet.v001.json``.
  * 106 of its beats carry narration (``beat.audio.master_start_s/end_s`` +
    ``beat.start_frame``); they map 1:1 BY ORDER to the 106 chunks in
    ``narration_index.v001.json`` (VC-0001..VC-0106).
  * The beats are laid out on a UNIFORM visual cadence (~155f hero cuts), so the
    raw per-chunk draft mp3 durations do NOT fit the per-beat gaps (they overlap
    by design of the visual rhythm). The narration's true unit is the SPAN: the
    106 chunks fall into 16 continuous audio SPANS (== the 16 script [VO:] beats),
    each a slice ``[master_start_s, master_end_s]`` of the continuous narration
    master ``vc_master_v001.mp3`` (613.707s). Placing each span's continuous
    master slice at its first beat's film time reproduces the exact narration,
    re-timed to the beatsheet, with the spans flowing back-to-back (< ~0.03s
    seam overlaps -> inaudible; NO chunk overrun).
  * Each chunk's film time is therefore
        chunk_film_start = span_first_beat_film_start + (chunk.master_start - span.master_start)
    which stays monotonic and non-overlapping (verified). SFX cues are placed on
    THIS film-time token stream (reusing build_case_film_audio.align_beats /
    build_cues), so a quoted (SFX:) trigger still lands on the real narrated word.

The four layers (identical roles to build_case_film_audio, re-timed):
  L1 NARRATION  : 106 master slices placed at their chunk film times -> one
                  continuous 713.37s narration bed WAV (stage 1). Gaps between
                  spans (opening/act-title/breath beats) are intentional silence.
  L2 MUSIC      : continuous per-section ducked bed spanning [0, 713.37], sidechain
                  under the narration bed (build_ffmpeg, lead=0).
  L3 AMBIENCE   : one distinct location bed per narration section (7 sections ->
                  6 distinct beds), constant ~-18 dB, NOT sidechained.
  L4 SFX        : the script's (SFX:) cues at their owning beat film times +
                  a transition whoosh on each of the 6 GlitchCut act boundaries.

OUTPUT
------
  * mix WAV  -> H:\pd-media\episodes\<ep>\06_audio\mix\<ep>_film_audio_v002.wav
               (+ a copy under 08_edit\audio\ so build_case_film_mux resolves it)
  * provenance -> episodes/<ep>/06_audio/audio_provenance.v002.json (bumped so
                  v001 is not clobbered) recording the layer inventory + mix sha,
                  in the exact shape build_case_film_mux reads
                  (mix.render_audio_copy / mix.wav_path_expected / mix.sha256).

This tool does NOT mux (run build_case_film_mux separately) and does NOT modify
the beatsheet, film data, or the composition. No network / paid API / GPU.

RUN:
    ./.venv/Scripts/python.exe scripts/build_williams_premium_audio.py --render
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import OrderedDict
from pathlib import Path
from typing import Optional

# reuse the proven library maps + helpers + build_ffmpeg VERBATIM (invariant 14)
sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_case_film_audio as B  # noqa: E402

ROOT = B.ROOT
GENERATOR = "scripts/build_williams_premium_audio.py"
SCHEMA_VERSION = "1.0.0"
EP = "PD-2026-036-williams"
REVISION_DEFAULT = "v002"

# transition whoosh placed on each GlitchCut act-boundary beat (component == GlitchCut).
# These are REAL visual transitions in WilliamsFilm; a whoosh there is meaningful (not filler)
# and lifts the SFX/min over the full 713s timeline unambiguously above the 2.0 floor.
TRANSITION_CUT_SFX = B.CHAPTER_CUT_SFX  # ("sfx_whoosh_short.mp3", 0.8, 0.16)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text("utf-8"))


# ============================================================================
# beatsheet -> film-timed chunks (THE timing model)
# ============================================================================
def build_film_chunks(beatsheet: dict, index: dict):
    """Return (narr_beats, chunks, master_offsets, spans_meta, chunk_mapping).

    chunks: build_case_film_audio.Chunk objects whose .start/.end are FILM times.
    master_offsets[i] = (master_start_s, master_end_s) for slicing the master.
    spans_meta: the 16 continuous narration spans (film start + master range).
    """
    narr = [b for b in beatsheet["beats"] if b.get("audio")]
    chunks_idx = index["chunks"]
    if len(narr) != len(chunks_idx):
        raise SystemExit(
            f"ERROR: narration beats ({len(narr)}) != narration_index chunks "
            f"({len(chunks_idx)}) -- 1:1-by-order mapping is broken.")

    # group narration beats into their audio spans (identical master range == one span)
    spanmap: "OrderedDict[tuple, list[int]]" = OrderedDict()
    for i, bt in enumerate(narr):
        key = (round(float(bt["audio"]["master_start_s"]), 3),
               round(float(bt["audio"]["master_end_s"]), 3))
        spanmap.setdefault(key, []).append(i)

    span_of: dict[int, tuple[float, float]] = {}   # chunk idx -> (span_film_start, span_master_start)
    spans_meta: list[dict] = []
    for (ms, me), members in spanmap.items():
        span_film_start = round(narr[members[0]]["start_frame"] / B.FPS, 3)
        for i in members:
            span_of[i] = (span_film_start, ms)
        spans_meta.append({
            "master_start_s": ms, "master_end_s": me,
            "master_dur_s": round(me - ms, 3),
            "film_start_s": span_film_start,
            "film_end_s": round(span_film_start + (me - ms), 3),
            "chunk_indices": [members[0], members[-1]],
            "chunk_count": len(members),
        })

    chunks: list[B.Chunk] = []
    master_offsets: list[tuple[float, float]] = []
    chunk_mapping: list[dict] = []
    for i, c in enumerate(chunks_idx):
        span_film_start, span_ms = span_of[i]
        c_ms = round(float(c["start"]), 3)
        c_me = round(float(c["end"]), 3)
        film_start = round(span_film_start + (c_ms - span_ms), 3)
        film_dur = round(c_me - c_ms, 3)
        vc = str(c.get("voice_chunk_id") or f"VC-{i + 1:04d}")
        section = str(c.get("section", ""))
        ch = B.Chunk(
            i=i, vc_id=vc, section=section,
            chapter_id=B.normalize_section(section),
            text=str(c.get("text", "")), tokens=B.alnum_tokens(str(c.get("text", ""))),
            duration=film_dur, duration_source="master_slice",
            start=film_start, end=round(film_start + film_dur, 3),
        )
        chunks.append(ch)
        master_offsets.append((c_ms, c_me))
        beat = narr[i]
        chunk_mapping.append({
            "vc_id": vc, "beat": beat["beat"], "section": section,
            "span_id": beat.get("span_id"),
            "beat_start_frame": beat["start_frame"],
            "master_start_s": c_ms, "master_end_s": c_me,
            "film_start_s": film_start, "film_end_s": round(film_start + film_dur, 3),
        })
    return narr, chunks, master_offsets, spans_meta, chunk_mapping


def verify_no_overlap(chunks: list[B.Chunk]) -> tuple[int, list[str]]:
    """Chunks must be monotonic on the film timeline with no meaningful overrun."""
    problems: list[str] = []
    overlaps = 0
    for i in range(len(chunks) - 1):
        if chunks[i + 1].start < chunks[i].end - 0.05:  # > 50ms overrun == real overlap
            overlaps += 1
            problems.append(
                f"{chunks[i].vc_id} film_end {chunks[i].end:.3f} > "
                f"{chunks[i + 1].vc_id} film_start {chunks[i + 1].start:.3f}")
    return overlaps, problems


# ============================================================================
# stage 1: the continuous narration bed (106 master slices at their film times)
# ============================================================================
def build_narration_bed_argv(master_path: Path, chunks: list[B.Chunk],
                             master_offsets: list[tuple[float, float]],
                             total: float, out_wav: Path) -> list[str]:
    n = len(chunks)
    parts: list[str] = [
        f"[0:a]aresample=48000,aformat=channel_layouts=stereo,asplit={n}"
        + "".join(f"[s{i}]" for i in range(n))
    ]
    labels: list[str] = []
    for i, ch in enumerate(chunks):
        ms, me = master_offsets[i]
        delay = int(round(ch.start * 1000))
        parts.append(
            f"[s{i}]atrim={ms:.3f}:{me:.3f},asetpts=PTS-STARTPTS,"
            f"adelay={delay}|{delay}[n{i}]")
        labels.append(f"[n{i}]")
    parts.append(
        "".join(labels)
        + f"amix=inputs={n}:normalize=0:dropout_transition=0,"
        f"atrim=0:{total:.3f},apad,atrim=0:{total:.3f},asetpts=PTS-STARTPTS[out]")
    graph = ";".join(parts)
    return ["ffmpeg", "-y", "-i", str(master_path), "-filter_complex", graph,
            "-map", "[out]", "-t", f"{total:.3f}", "-ar", "48000", "-ac", "2",
            "-c:a", "pcm_s16le", str(out_wav)]


# ============================================================================
# SFX: script (SFX:) cues (reused) + GlitchCut transition whooshes
# ============================================================================
def section_at(chunks: list[B.Chunk], t: float) -> str:
    cid = chunks[0].chapter_id
    for ch in chunks:
        if ch.start <= t:
            cid = ch.chapter_id
        else:
            break
    return cid


def add_transition_cuts(sfx_raw: list, beatsheet: dict, chunks: list[B.Chunk]) -> int:
    base_fname, base_dur, base_vol = TRANSITION_CUT_SFX
    glitch_times = sorted(round(b["start_frame"] / B.FPS, 3)
                          for b in beatsheet["beats"] if b.get("component") == "GlitchCut")
    for j, t in enumerate(glitch_times, start=1):
        fname = B.variant_of(base_fname, 1000 + j)  # rotate variants for palette variety
        sfx_raw.append(B.SfxCue(
            cue_id="", file=f"sfx/{fname}", chapter_id=section_at(chunks, t),
            time=t, dur=base_dur, volume=base_vol, gain_db=B.vol_to_db(base_vol),
            source="transition_cut", phrase="GlitchCut act-boundary transition",
            trigger="", timing="transition_beat"))
    return len(glitch_times)


# ============================================================================
# main
# ============================================================================
def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    ap = argparse.ArgumentParser(
        description="Build the beatsheet-timed 4-layer premium audio mix for EP36 williams.")
    ap.add_argument("--ep", default=EP)
    ap.add_argument("--beatsheet")
    ap.add_argument("--index")
    ap.add_argument("--script")
    ap.add_argument("--master")
    ap.add_argument("--revision", default=REVISION_DEFAULT)
    ap.add_argument("--out")
    ap.add_argument("--render", action="store_true",
                    help="run ffmpeg (stage1 narration bed + stage2 4-layer two-pass loudnorm)")
    ap.add_argument("--tail-fade-sec", type=float, default=5.0,
                    help="ENDING RESOLUTION: length (s) of a master fade-out applied to the "
                         "final mix over [total - tail_fade_sec, total]. Placed AFTER the two-pass "
                         "loudnorm + alimiter (last in the filter chain) so the DYNAMIC loudnorm "
                         "cannot boost the fading tail back up. Narration ends ~656s so this tail is "
                         "music/ambience only (safe to fade). Set 0 to disable (v002 behaviour).")
    ap.add_argument("--keep-bed", action="store_true", help="keep the intermediate narration bed WAV")
    ap.add_argument("--allow-fail", action="store_true")
    args = ap.parse_args()

    ep = args.ep
    ep_dir = ROOT / "episodes" / ep
    beatsheet_path = Path(args.beatsheet) if args.beatsheet else ep_dir / "04_scenes" / "premium_beatsheet.v001.json"
    index_path = Path(args.index) if args.index else ep_dir / "06_audio" / "narration_index.v001.json"
    script_md = Path(args.script) if args.script else ep_dir / "03_script" / "script.en.v001.md"
    out_path = Path(args.out) if args.out else ep_dir / "06_audio" / f"audio_provenance.{args.revision}.json"

    for p in (beatsheet_path, index_path, script_md):
        if not p.exists():
            print(f"ERROR: missing input: {p}", file=sys.stderr)
            return 2

    media = B.media_root()
    lib = media / "library"
    master_path = Path(args.master) if args.master else media / "episodes" / ep / "06_voice" / "master" / "vc_master_v001.mp3"

    beatsheet = load_json(beatsheet_path)
    index = B.load_index(index_path)

    total = round(float(beatsheet["meta"]["projected_runtime_seconds"]), 3)  # 713.37
    lead = 0.0
    body_len = total

    narr, chunks, master_offsets, spans_meta, chunk_mapping = build_film_chunks(beatsheet, index)
    overlaps, overlap_problems = verify_no_overlap(chunks)

    # ---- sections/chapters on the film timeline; extend to cover [0, total] ----
    spans = B.chapter_spans(chunks, total)          # gapless [chunks[0].start .. total]
    if spans:
        cid, _s, e, m = spans[0]
        spans[0] = (cid, 0.0, e, m)                  # music/ambience cover the 0..first-narration head
    beds = B.assign_ambience(spans, chunks, [])      # ambience uses chunk text (beats optional)

    # ---- SFX: reuse script-cue placement on the film-time token stream ----
    beats = B.parse_script_md(script_md)
    if not beats:
        print("ERROR: no [VO:] beats parsed from script", file=sys.stderr)
        return 2
    gtok, gtime, gchunk = B.build_global_tokens(chunks)
    B.align_beats(beats, gtok, gchunk)
    # ambience considered VIS text too (re-run assign with beats for parity with build_case_film_audio)
    beds = B.assign_ambience(spans, chunks, beats)
    sfx_raw, swells, unmapped = B.build_cues(beats, chunks, spans, gtok, gtime)
    n_transitions = add_transition_cuts(sfx_raw, beatsheet, chunks)
    # dedup_sfx assumes time-sorted input (it tracks last-seen time per file); the
    # transition cues were appended out of order, so sort before de-duping.
    sfx_raw.sort(key=lambda c: (c.time, c.file))
    sfx, dropped = B.dedup_sfx(sfx_raw)
    density = B.compute_density(sfx, beds, spans, total)

    # ---- output paths (shape build_case_film_mux resolves) ----
    wav_name = f"{ep}_film_audio_{args.revision}.wav"
    out_wav = media / "episodes" / ep / "06_audio" / "mix" / wav_name
    render_audio_copy = media / "episodes" / ep / "08_edit" / "audio" / wav_name
    bed_wav = media / "episodes" / ep / "06_audio" / "mix" / f"{ep}_narration_bed_{args.revision}.wav"

    loudnorm_apply = "loudnorm=I=-14:TP=-1.5:LRA=11:linear=true"
    graph, argv = B.build_ffmpeg(str(bed_wav), spans, beds, sfx, swells,
                                 lead, body_len, total, lib, str(out_wav), loudnorm_apply)

    # ---- ENDING RESOLUTION: master tail fade-out placed AFTER loudnorm+alimiter -----
    # build_ffmpeg ends the master chain with "...,{loudnorm},alimiter=...:limit=0.95[aout]".
    # For williams lead=0.0 (no bookends) so the built-in outro fade is never emitted, and
    # the DYNAMIC loudnorm would pull any pre-loudnorm fade back up. We therefore splice a
    # final afade=t=out AFTER the limiter (the very last stage before [aout]) so it survives
    # both passes and resolves the music/ambience-only tail toward silence. Injected into the
    # shared `graph` (and its mirror in `argv`) BEFORE the measure/apply passes derive from it.
    tail_fade_sec = round(float(args.tail_fade_sec), 3)
    tail_fade_applied: Optional[dict] = None
    if tail_fade_sec > 0.001:
        _alim = "alimiter=level_in=1:level_out=1:limit=0.95[aout]"
        if _alim not in graph:
            print(f"ERROR: could not locate limiter tail '{_alim}' in graph to splice the "
                  f"master fade; refusing to emit an un-faded ending.", file=sys.stderr)
            return 2
        fade_st = round(max(0.0, total - tail_fade_sec), 3)
        _faded = (f"alimiter=level_in=1:level_out=1:limit=0.95,"
                  f"afade=t=out:st={fade_st:.3f}:d={tail_fade_sec:.3f}[aout]")
        graph = graph.replace(_alim, _faded)
        fc_i = argv.index("-filter_complex")
        argv[fc_i + 1] = graph  # keep argv's filter_complex mirror in sync with graph
        tail_fade_applied = {"type": "out", "curve": "tri", "start_sec": fade_st,
                             "duration_sec": tail_fade_sec, "end_sec": total,
                             "placement": "post-loudnorm+alimiter (master tail, last stage before [aout])"}
        print(f"ending resolution: master afade=t=out st={fade_st:.3f} d={tail_fade_sec:.3f} "
              f"(post-loudnorm) -> tail resolves to silence at {total:.3f}s")

    command_str = " ".join(B.quote_arg(a) for a in argv)

    # ---- render (stage 1 bed + stage 2 two-pass loudnorm) ----
    ran_ffmpeg = False
    mix_sha: Optional[str] = None
    mix_duration: Optional[float] = None
    bed_duration: Optional[float] = None
    loudnorm_measured: Optional[dict] = None
    if args.render:
        needed = [master_path,
                  *[lib / "music" / B.CHAPTER_MUSIC.get(c, ("", "explainer_bed",
                    "mus_20260614_explainer_bed_soft_explainer_v2.mp3"))[1]
                    / B.CHAPTER_MUSIC.get(c, ("", "explainer_bed",
                    "mus_20260614_explainer_bed_soft_explainer_v2.mp3"))[2]
                    for c, _s, _e, _m in spans],
                  *[lib / "ambience" / beds[c] for c, _s, _e, _m in spans],
                  *[lib / c.file for c in sfx]]
        missing = [p for p in needed if not Path(p).exists()]
        if missing:
            print(f"--render aborted: {len(missing)} input(s) missing (e.g. {missing[0]})", file=sys.stderr)
            return 2

        out_wav.parent.mkdir(parents=True, exist_ok=True)
        render_audio_copy.parent.mkdir(parents=True, exist_ok=True)

        # stage 1: narration bed
        print("stage 1: building continuous narration bed (106 master slices) ...")
        bed_argv = build_narration_bed_argv(master_path, chunks, master_offsets, total, bed_wav)
        subprocess.run(bed_argv, check=True)
        bed_duration = B.ffprobe_duration(bed_wav)
        print(f"  narration bed -> {bed_wav}  ({bed_duration:.3f}s)")

        # stage 2: 4-layer mix, two-pass loudnorm (reuses build_ffmpeg graph)
        print("stage 2: 4-layer mix (music sidechain-ducked + ambience + sfx), pass 1 measure ...")
        measure_graph = graph.replace(
            loudnorm_apply, "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json")
        argv_measure = ["ffmpeg", "-hide_banner", "-nostats",
                        *argv[2:argv.index("-filter_complex")],
                        "-filter_complex", measure_graph, "-map", "[aout]", "-f", "null", "-"]
        loudnorm_measured = B.measure_loudnorm(argv_measure)
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
        print("stage 2: pass 2 apply ...")
        tmp = out_wav.with_suffix(".tmp.wav")
        subprocess.run([*argv2[:-1], str(tmp)], check=True)
        tmp.replace(out_wav)
        import shutil
        shutil.copy2(out_wav, render_audio_copy)
        mix_sha = B.sha256_file(out_wav)
        mix_duration = B.ffprobe_duration(out_wav)
        ran_ffmpeg = True
        print(f"rendered mix -> {out_wav}  ({mix_duration:.3f}s)")
        if not args.keep_bed:
            try:
                bed_wav.unlink()
            except OSError:
                pass

    # ---- music inventory (for provenance) ----
    music_tracks = []
    for cid, _s, _e, _m in spans:
        _role, folder, fname = B.CHAPTER_MUSIC.get(cid, ("bed", "explainer_bed",
                                                         "mus_20260614_explainer_bed_soft_explainer_v2.mp3"))
        music_tracks.append(f"music/{folder}/{fname}")

    provenance = {
        "schema_version": SCHEMA_VERSION,
        "kind": "case_film_audio_provenance",
        "episode_id": ep,
        "revision": args.revision,
        "generator": GENERATOR,
        "based_on": "scripts/build_case_film_audio.py (library maps + build_ffmpeg + loudnorm reused; timing re-driven from the premium beatsheet)",
        "fps": B.FPS,
        "timeline": {
            "total_sec": total,
            "lead_sec": lead,
            "body_len_sec": body_len,
            "timing_source": ("premium_beatsheet.v001.json: 106 narration beats -> 16 continuous "
                              "audio spans placed at their first-beat film times; each chunk sliced "
                              "from the narration master at its master offsets; SFX on the film-time token stream"),
            "narration_first_start_sec": chunks[0].start,
            "narration_last_end_sec": chunks[-1].end,
            "narration_active_span_sec": round(chunks[-1].end - chunks[0].start, 3),
            "chunks": len(chunks),
            "narration_spans": len(spans_meta),
            "beats_script_vo": len(beats),
            "chunk_overlaps_gt_50ms": overlaps,
            "chunk_overlap_problems": overlap_problems,
            "narration_master": str(master_path),
            "narration_master_seconds": round(float(beatsheet["meta"].get("narration_master_seconds", 0.0)), 3),
        },
        "chapters": [
            {"chapter_id": cid, "title": B.CHAPTER_TITLES.get(cid, cid),
             "start": round(s, 3), "end": round(e, 3), "ambience_bed": beds[cid]}
            for cid, s, e, _m in spans
        ],
        "narration_spans": spans_meta,
        "layers": {
            "narration": {
                "role": "front / sidechain-priority (VO wins); 106 chunks in 16 continuous spans at beatsheet film times",
                "master_uri": f"artifact://episodes/{ep}/06_voice/master/{master_path.name}",
                "master_path_expected": str(master_path),
                "master_exists": master_path.exists(),
                "chunks_placed": len(chunks),
                "spans_placed": len(spans_meta),
                "bed_duration_sec": round(bed_duration, 3) if bed_duration else None,
                "gain_db": 0.0,
            },
            "music": {
                "role": "per-section ducked musical bed (sidechained by VO), continuous over [0, total]",
                "cue_count": len(music_tracks),
                "distinct_tracks": len(set(music_tracks)),
                "tracks": music_tracks,
                "gain_db": B.vol_to_db(B.MUSIC_VOL),
                "ducked": True,
                "continuous_bed": True,
            },
            "ambience": {
                "role": "distinct constant location bed per section (audible; NOT sidechained)",
                "bed_count": len(spans),
                "distinct_beds": len(set(beds.values())),
                "beds": sorted(set(beds.values())),
                "beds_by_chapter": {cid: beds[cid] for cid, _s, _e, _m in spans},
                "floor_db": B.AMBIENCE_FLOOR_DB,
                "ducking_capped": True,
                "swell_automation_events": len(swells),
            },
            "sfx": {
                "role": "script (SFX:) one-shots at real narrated words + GlitchCut act-boundary transitions",
                "cue_count": len(sfx),
                "cues_before_dedup": len(sfx_raw),
                "deduped": dropped,
                "distinct_files": len(set(c.file for c in sfx)),
                "word_triggered": sum(1 for c in sfx if c.timing == "word_trigger"),
                "transition_cuts": n_transitions,
                "transient_bed": None,
            },
        },
        "mix": {
            "wav_uri": f"artifact://episodes/{ep}/06_audio/mix/{wav_name}",
            "wav_path_expected": str(out_wav),
            "render_audio_copy": str(render_audio_copy),
            "exists": bool(mix_sha),
            "sha256": mix_sha,
            "duration_sec": round(mix_duration, 3) if mix_duration else None,
            "sample_rate": 48000,
            "channels": 2,
            "codec": "pcm_s16le",
            "loudnorm": {"I": -14.0, "TP": -1.5, "LRA": 11.0, "passes": 2},
            "loudnorm_measured": loudnorm_measured,
            "tail_fade": tail_fade_applied,
            "final_weights": B.FINAL_WEIGHTS,
        },
        "mux": {
            "note": "This WAV is the ONLY audio in the final deliverable; mux with build_case_film_mux (-map 0:v -map 1:a).",
            "audio_source_uri": f"artifact://episodes/{ep}/06_audio/mix/{wav_name}",
            "audio_source_sha256": mix_sha,
            "command_template": (
                f"ffmpeg -y -i <williams_render.mp4> -i {out_wav} "
                f"-map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 320k -ar 48000 -shortest <final.mp4>"),
        },
        "density_gate": density,
        "sfx_per_min_over_active": round(len(sfx) / max(0.001, (chunks[-1].end - chunks[0].start) / 60.0), 3),
        "unmapped_sfx": unmapped,
        "narration_chunk_mapping": chunk_mapping,
        "sfx_cues": [
            {"cue_id": c.cue_id, "file": c.file, "chapter_id": c.chapter_id,
             "time": c.time, "dur": c.dur, "gain_db": c.gain_db,
             "source": c.source, "phrase": c.phrase, "trigger": c.trigger, "timing": c.timing}
            for c in sfx
        ],
        "ffmpeg": {
            "stage1_narration_bed": "106 master slices adelay'd to chunk film times -> continuous 713.37s bed",
            "stage2_mix": "narration(front) + music(sidechain-ducked) + ambience(constant) + sfx(one-shots), two-pass loudnorm I=-14",
            "output_expected": str(out_wav),
            "filter_complex": graph,
            "command": command_str,
        },
        "library_root": str(lib),
        "provenance": {
            "beatsheet": B.rel(beatsheet_path),
            "beatsheet_sha256": B.sha256_text(beatsheet_path.read_text("utf-8")),
            "narration_index": B.rel(index_path),
            "narration_index_sha256": B.sha256_text(index_path.read_text("utf-8")),
            "script_md": B.rel(script_md),
            "script_md_sha256": B.sha256_text(script_md.read_text("utf-8")),
            "deterministic": True,
        },
        "side_effects": {
            "external_cost_usd": 0,
            "external_calls": [],
            "wrote_files": [B.rel(out_path)] + ([str(out_wav), str(render_audio_copy)] if ran_ffmpeg else []),
            "ran_ffmpeg": ran_ffmpeg,
        },
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(provenance, indent=2, ensure_ascii=False) + "\n"
    tmp = out_path.with_suffix(out_path.suffix + ".tmp")
    tmp.write_text(payload, encoding="utf-8")
    tmp.replace(out_path)

    # ---- console summary ----
    print(f"provenance -> {out_path}")
    print(f"timeline: total={total:.3f}s  chunks={len(chunks)} in {len(spans_meta)} spans  "
          f"narration {chunks[0].start:.2f}..{chunks[-1].end:.2f}s  overlaps>50ms={overlaps}")
    print(f"sections={len(spans)}  ambience distinct beds={len(set(beds.values()))} -> "
          + ", ".join(f"{cid}:{beds[cid]}" for cid, _s, _e, _m in spans))
    print(f"music: {len(music_tracks)} cues ({len(set(music_tracks))} distinct) continuous bed")
    print(f"SFX: {len(sfx)} cues ({len(set(c.file for c in sfx))} distinct files; "
          f"{n_transitions} transitions; word-triggered={provenance['layers']['sfx']['word_triggered']}; "
          f"swells->L3={len(swells)}; unmapped={len(unmapped)})")
    print(f"density: sfx/min(total)={density['sfx_per_min']} sfx/min(active)="
          f"{provenance['sfx_per_min_over_active']} (floor {B.SFX_PER_MIN_FLOOR}); "
          f"distinct_beds={density['ambience_distinct_beds']} (floor {B.AMBIENCE_DISTINCT_FLOOR}) "
          f"-> {'PASS' if density['pass'] else 'FAIL: ' + '; '.join(density['failures'])}")
    if mix_sha:
        print(f"mix: {out_wav}  dur={mix_duration:.3f}s sha={mix_sha[:16]}...")
        if loudnorm_measured:
            print(f"loudnorm measured input_i={loudnorm_measured.get('input_i')} "
                  f"output_i={loudnorm_measured.get('output_i')} LUFS")
    else:
        print("ffmpeg NOT run (pass --render to build the WAV).")

    if not density["pass"] and not args.allow_fail:
        print("DENSITY GATE FAILED. Re-run with --allow-fail to keep provenance.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
