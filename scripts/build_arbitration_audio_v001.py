#!/usr/bin/env python3
"""Build local narration, captions, and final audio mix for ArbitrationPremium.

No paid provider call is made. Narration is generated through Windows SAPI,
then fitted to the locked 12-minute edit structure.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-012-arbitration"
TOTAL_SEC = 720.0
VOICE_TARGET_SEC = 711.0
EPDIR = ROOT / "episodes" / EP
SCRIPT = EPDIR / "03_script" / "script.en.v001.md"
ANNOTATED = EPDIR / "03_script" / "script.annotated.v001.json"
MEDIA = Path(json.loads((ROOT / "config/storage.local.json").read_text("utf-8"))["roots"]["media"]["path"])
EPM = MEDIA / "episodes" / EP
LIB = MEDIA / "library"
VOICE_PLAN = EPDIR / "06_audio" / "voice_plan.v001.json"
NARR_INDEX = EPDIR / "06_audio" / "narration_index.v001.json"
NARR_MASTER = EPM / "06_voice" / "master" / "vc_master_v001.wav"
NARR_FIT = EPM / "06_voice" / "master" / "vc_master_v001_fit_711s.wav"
CAPTIONS = EPDIR / "08_edit" / "captions.v001.srt"
CAPTIONS_JSON = EPDIR / "08_edit" / "captions.v001.json"
CAPTIONS_TS = ROOT / "remotion" / "src" / "data" / "arbitration_captions.ts"
PUBLIC_AUDIO = ROOT / "remotion" / "public" / "arbitration" / "audio" / "arbitration_final_mix_v001.mp3"
AUDIO_QC = EPDIR / "08_edit" / "audio_mix.v001.qc.json"

MUSIC = [
    (0.0, 32.0, LIB / "music" / "tension_build" / "mus_20260614_tension_build_courtroom_horizon_v1.mp3", 0.17),
    (32.0, 150.0, LIB / "music" / "opening" / "mus_20260614_opening_measured_arpeggio_v1.mp3", 0.11),
    (150.0, 390.0, LIB / "music" / "ambience" / "mus_20260614_ambience_paper_trail_static_v2.mp3", 0.12),
    (390.0, 560.0, LIB / "music" / "explainer_bed" / "mus_20260614_explainer_bed_soft_explainer_v1.mp3", 0.12),
    (560.0, 675.0, LIB / "music" / "reveal" / "mus_20260614_reveal_hidden_system_clicks_v1.mp3", 0.14),
    (675.0, 720.0, LIB / "music" / "outro" / "mus_20260614_outro_last_frame_v1.mp3", 0.18),
]

AMBIENCE = [
    (0.0, 200.0, LIB / "ambience" / "amb_office_hum.mp3", 0.026),
    (200.0, 430.0, LIB / "ambience" / "amb_institutional_drone.mp3", 0.03),
    (430.0, 590.0, LIB / "ambience" / "amb_courtroom_room_tone.mp3", 0.028),
    (590.0, 720.0, LIB / "ambience" / "amb_empty_hallway.mp3", 0.026),
]

SFX = [
    (4.4, LIB / "sfx" / "sfx_ui_tick.mp3", 0.32),
    (10.8, LIB / "sfx" / "sfx_binder_lock.mp3", 0.34),
    (28.2, LIB / "sfx" / "sfx_low_boom.mp3", 0.26),
    (174.0, LIB / "sfx" / "sfx_page_turn.mp3", 0.24),
    (286.0, LIB / "sfx" / "sfx_stamp_seal.mp3", 0.26),
    (392.0, LIB / "sfx" / "sfx_gavel_knock.mp3", 0.30),
    (548.0, LIB / "sfx" / "sfx_data_blip.mp3", 0.28),
    (654.0, LIB / "sfx" / "sfx_riser_2s.mp3", 0.18),
    (710.7, LIB / "sfx" / "sfx_soft_impact.mp3", 0.26),
]


def run(cmd: list[str], label: str) -> None:
    print(label)
    subprocess.run(cmd, check=True)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def duration(path: Path) -> float:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        capture_output=True,
        text=True,
    )
    return float(result.stdout.strip() or 0)


def clean_spoken_text(line: str) -> str:
    text = re.sub(r"\[CLM-[0-9]{4}\]", "", line)
    text = re.sub(r"^\[VO:\]\s*", "", text)
    return re.sub(r"\s+", " ", text).strip()


def script_hashes() -> dict[str, str]:
    return {
        "script": "sha256:" + sha256_file(SCRIPT),
        "annotated_script": "sha256:" + sha256_file(ANNOTATED),
    }


def parse_script() -> list[dict[str, str]]:
    chunks: list[dict[str, str]] = []
    current = "unknown"
    for raw in SCRIPT.read_text("utf-8").splitlines():
        line = raw.strip()
        if line.startswith("## "):
            current = re.sub(r"\s+[—-].*$", "", line[3:].strip())
            continue
        if not line.startswith("[VO:]"):
            continue
        chunks.append(
            {
                "chunk_id": f"VC-{len(chunks) + 1:04d}",
                "section": current,
                "spoken_text": clean_spoken_text(line),
            }
        )
    if not chunks:
        raise RuntimeError("No [VO:] chunks found")
    return chunks


def write_voice_plan(chunks: list[dict[str, str]]) -> None:
    chars = sum(len(c["spoken_text"]) for c in chunks)
    words = sum(len(c["spoken_text"].split()) for c in chunks)
    VOICE_PLAN.parent.mkdir(parents=True, exist_ok=True)
    VOICE_PLAN.write_text(
        json.dumps(
            {
                "schema_version": "1.0.0",
                "episode_id": EP,
                "revision": "v001",
                "provider": "Windows SAPI local",
                "external_paid_request": False,
                "script_revision": "v001",
                "script_hashes": script_hashes(),
                "estimated_words": words,
                "estimated_characters": chars,
                "chunks": chunks,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )


SAPI_PS = r"""
$ErrorActionPreference = 'Stop'
$Out = $env:PD_SAPI_OUT
$text = [Console]::In.ReadToEnd()
Add-Type -AssemblyName System.Speech
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
$voices = $synth.GetInstalledVoices() | ForEach-Object { $_.VoiceInfo }
$preferred = $voices | Where-Object { $_.Culture.Name -like 'en-*' -and $_.Gender -eq 'Male' } | Select-Object -First 1
if (-not $preferred) { $preferred = $voices | Where-Object { $_.Culture.Name -like 'en-*' } | Select-Object -First 1 }
if ($preferred) { $synth.SelectVoice($preferred.Name) }
$synth.Rate = -1
$synth.Volume = 100
$synth.SetOutputToWaveFile($Out)
$synth.Speak($text)
$synth.Dispose()
"""


def generate_sapi(chunks: list[dict[str, str]]) -> list[dict[str, object]]:
    outdir = EPM / "06_voice" / "draft"
    outdir.mkdir(parents=True, exist_ok=True)
    index: list[dict[str, object]] = []
    for chunk in chunks:
        out = outdir / f"{chunk['chunk_id']}.wav"
        if out.exists() and out.stat().st_size > 2048:
            print(f"  {chunk['chunk_id']} skip current")
        else:
            print(f"  {chunk['chunk_id']} local SAPI")
            env = {**__import__("os").environ, "PD_SAPI_OUT": str(out)}
            subprocess.run(
                ["powershell", "-NoProfile", "-NonInteractive", "-Command", SAPI_PS],
                input=chunk["spoken_text"],
                text=True,
                encoding="utf-8",
                env=env,
                check=True,
            )
        index.append(
            {
                **chunk,
                "file": out.name,
                "seconds": round(duration(out), 3),
                "characters": len(chunk["spoken_text"]),
            }
        )
    return index


def concat_master(index: list[dict[str, object]]) -> list[dict[str, object]]:
    outdir = EPM / "06_voice" / "draft"
    silence = outdir / "_silence_035.wav"
    run(
        ["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono", "-t", "0.35", "-c:a", "pcm_s16le", str(silence)],
        "build narration spacer",
    )
    concat = outdir / "_concat.txt"
    lines: list[str] = []
    cursor = 0.0
    timed: list[dict[str, object]] = []
    for i, chunk in enumerate(index):
        path = outdir / str(chunk["file"])
        seconds = duration(path)
        timed.append({**chunk, "start": round(cursor, 3), "end": round(cursor + seconds, 3), "seconds": round(seconds, 3)})
        lines.append(f"file '{path.as_posix()}'\n")
        cursor += seconds
        if i != len(index) - 1:
            lines.append(f"file '{silence.as_posix()}'\n")
            cursor += 0.35
    concat.write_text("".join(lines), encoding="utf-8")
    NARR_MASTER.parent.mkdir(parents=True, exist_ok=True)
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat), "-c:a", "pcm_s16le", str(NARR_MASTER)], "concat narration master")
    return timed


def fit_voice() -> float:
    src = duration(NARR_MASTER)
    atempo = src / VOICE_TARGET_SEC
    if not 0.5 <= atempo <= 2.0:
        raise RuntimeError(f"atempo out of range: {atempo}")
    NARR_FIT.parent.mkdir(parents=True, exist_ok=True)
    run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(NARR_MASTER),
            "-filter:a",
            f"atempo={atempo:.8f},aresample=48000",
            "-c:a",
            "pcm_s16le",
            str(NARR_FIT),
        ],
        f"fit narration {src:.1f}s -> {VOICE_TARGET_SEC:.1f}s",
    )
    return src


def split_caption_text(text: str) -> list[str]:
    text = re.sub(r"\s+", " ", text).strip()
    words = text.split()
    cues: list[list[str]] = []
    current: list[str] = []
    for word in words:
        trial_words = current + [word]
        trial = " ".join(trial_words)
        if current and (len(trial) > 68 or len(trial_words) > 7):
            cues.append(current)
            current = [word]
        else:
            current = trial_words
    if current:
        cues.append(current)

    def two_lines(cue_words: list[str]) -> str:
        if len(" ".join(cue_words)) <= 42:
            return " ".join(cue_words)
        best = max(1, len(cue_words) // 2)
        return " ".join(cue_words[:best]) + "\n" + " ".join(cue_words[best:])

    return [two_lines(cue) for cue in cues]


def fmt_srt(t: float) -> str:
    ms = int(round(t * 1000))
    h = ms // 3_600_000
    ms %= 3_600_000
    m = ms // 60_000
    ms %= 60_000
    s = ms // 1000
    ms %= 1000
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def write_captions(timed: list[dict[str, object]], src_total: float) -> list[dict[str, object]]:
    # Use the chunk timeline as the subtitle basis; the WAV container duration can drift
    # after concat because SAPI emits mixed sample rates.
    timeline_total = float(timed[-1]["end"])
    scale = VOICE_TARGET_SEC / timeline_total
    cues: list[dict[str, object]] = []
    for chunk in timed:
        text = str(chunk["spoken_text"])
        parts = split_caption_text(text)
        start = float(chunk["start"]) * scale
        end = float(chunk["end"]) * scale
        span = max(1.0, end - start)
        weights = [max(1, len(str(part).replace("\n", " ").split())) for part in parts]
        cursor = start
        for part, weight in zip(parts, weights):
            dur = span * weight / sum(weights)
            cue_end = min(end, cursor + dur)
            cues.append({"start": round(cursor, 3), "end": round(cue_end, 3), "text": part})
            cursor = cue_end
    CAPTIONS.parent.mkdir(parents=True, exist_ok=True)
    CAPTIONS.write_text(
        "\n".join(f"{i}\n{fmt_srt(float(c['start']))} --> {fmt_srt(float(c['end']))}\n{c['text']}\n" for i, c in enumerate(cues, 1)),
        encoding="utf-8",
    )
    CAPTIONS_JSON.write_text(
        json.dumps({"episode_id": EP, "revision": "v001", "voice": str(NARR_FIT), "cues": cues}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    CAPTIONS_TS.parent.mkdir(parents=True, exist_ok=True)
    CAPTIONS_TS.write_text(
        "export type ArbitrationCaptionCue = {\n  start: number;\n  end: number;\n  text: string;\n};\n\nexport const ARBITRATION_CAPTIONS: ArbitrationCaptionCue[] = "
        + json.dumps(cues, indent=2, ensure_ascii=False)
        + ";\n",
        encoding="utf-8",
    )
    return cues


def filter_inputs() -> tuple[list[str], str]:
    inputs = ["-i", str(NARR_FIT)]
    filters = [f"[0:a]atrim=0:{TOTAL_SEC:.3f},asetpts=PTS-STARTPTS,volume=1.0[v0]"]
    labels = ["[v0]"]
    input_index = 1
    for start, end, path, vol in MUSIC:
        inputs += ["-stream_loop", "-1", "-i", str(path)]
        delay = int(start * 1000)
        filters.append(f"[{input_index}:a]atrim=0:{end-start:.3f},asetpts=PTS-STARTPTS,volume={vol},adelay={delay}:all=1[m{input_index}]")
        labels.append(f"[m{input_index}]")
        input_index += 1
    for start, end, path, vol in AMBIENCE:
        inputs += ["-stream_loop", "-1", "-i", str(path)]
        delay = int(start * 1000)
        filters.append(f"[{input_index}:a]atrim=0:{end-start:.3f},asetpts=PTS-STARTPTS,volume={vol},adelay={delay}:all=1[a{input_index}]")
        labels.append(f"[a{input_index}]")
        input_index += 1
    for start, path, vol in SFX:
        inputs += ["-i", str(path)]
        delay = int(start * 1000)
        filters.append(f"[{input_index}:a]volume={vol},adelay={delay}:all=1[s{input_index}]")
        labels.append(f"[s{input_index}]")
        input_index += 1
    filters.append("".join(labels) + f"amix=inputs={len(labels)}:duration=longest:normalize=0,atrim=0:{TOTAL_SEC:.3f},loudnorm=I=-14:TP=-1:LRA=11:linear=false[mix]")
    return inputs, ";".join(filters)


def build_mix() -> None:
    PUBLIC_AUDIO.parent.mkdir(parents=True, exist_ok=True)
    inputs, graph = filter_inputs()
    run(["ffmpeg", "-y", *inputs, "-filter_complex", graph, "-map", "[mix]", "-c:a", "libmp3lame", "-b:a", "192k", str(PUBLIC_AUDIO)], "build final audio mix")


def loudnorm_qc() -> dict[str, object]:
    result = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", str(PUBLIC_AUDIO), "-af", "loudnorm=I=-14:TP=-1:LRA=11:print_format=json", "-f", "null", "-"],
        capture_output=True,
        text=True,
    )
    match = re.search(r"\{[\s\S]*\}", result.stderr)
    loud = json.loads(match.group(0)) if match else {}
    qc = {
        "episode_id": EP,
        "revision": "v001",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "audio_mix": str(PUBLIC_AUDIO),
        "audio_mix_sha256": "sha256:" + sha256_file(PUBLIC_AUDIO),
        "duration_seconds": round(duration(PUBLIC_AUDIO), 3),
        "target_duration_seconds": TOTAL_SEC,
        "target_lufs": -14,
        "loudnorm": loud,
        "external_paid_request": False,
        "provider": "Windows SAPI local + local FFmpeg mix",
    }
    AUDIO_QC.write_text(json.dumps(qc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return qc


def write_index(timed: list[dict[str, object]], src_total: float) -> None:
    NARR_INDEX.write_text(
        json.dumps(
            {
                "episode_id": EP,
                "revision": "v001",
                "provider": "Windows SAPI local",
                "external_paid_request": False,
                "script_hashes": script_hashes(),
                "generated_total_seconds": round(src_total, 3),
                "master": f"artifact://episodes/{EP}/06_voice/master/vc_master_v001.wav",
                "master_sha256": "sha256:" + sha256_file(NARR_MASTER),
                "fitted_master": str(NARR_FIT),
                "fitted_master_sha256": "sha256:" + sha256_file(NARR_FIT),
                "chunks": timed,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    chunks = parse_script()
    write_voice_plan(chunks)
    generated = generate_sapi(chunks)
    timed = concat_master(generated)
    src_total = fit_voice()
    write_index(timed, src_total)
    cues = write_captions(timed, src_total)
    build_mix()
    qc = loudnorm_qc()
    print(f"OK audio={PUBLIC_AUDIO} duration={qc['duration_seconds']} cues={len(cues)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
