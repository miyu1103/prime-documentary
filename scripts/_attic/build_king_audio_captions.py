#!/usr/bin/env python3
"""Build King timed narration, mixed audio, captions, and Remotion timing data."""
from __future__ import annotations

import json
import math
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-013-king"
MEDIA = Path(json.loads((ROOT / "config/storage.local.json").read_text("utf-8"))["roots"]["media"]["path"])
EP_MEDIA = MEDIA / "episodes" / EP
DRAFT = EP_MEDIA / "06_voice" / "draft"
VOICE_INDEX = ROOT / "episodes" / EP / "06_audio" / "narration_index.v001.json"
OUT_AUDIO = EP_MEDIA / "07_audio"
OUT_CAP = ROOT / "episodes" / EP / "08_edit"
REM_DATA = ROOT / "remotion" / "src" / "data"
REM_PUBLIC_AUDIO = ROOT / "remotion" / "public" / "king" / "audio"
LIB = MEDIA / "library"
ATEMPO = 0.782
FPS = 30
BRAND_OPENING = 3.5
ENDCARD = 9.0


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def dur(path: Path) -> float:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    return float(r.stdout.strip() or 0)


def ts(t: float) -> str:
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = int(t % 60)
    ms = int(round((t - int(t)) * 1000))
    if ms == 1000:
        s += 1
        ms = 0
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def norm(w: str) -> str:
    return re.sub(r"[^a-z0-9]", "", w.lower())


def split_lines(tokens: list[str]) -> list[tuple[str, int, int]]:
    lines = []
    cur: list[tuple[str, int]] = []
    for i, w in enumerate(tokens):
        trial = " ".join([x for x, _ in cur] + [w])
        if cur and (len(cur) >= 10 or len(trial) > 60):
            lines.append((" ".join(x for x, _ in cur), cur[0][1], cur[-1][1]))
            cur = []
        cur.append((w, i))
        if re.search(r"[.?!—]$", w) or (w.endswith(",") and len(cur) >= 5):
            lines.append((" ".join(x for x, _ in cur), cur[0][1], cur[-1][1]))
            cur = []
    if cur:
        lines.append((" ".join(x for x, _ in cur), cur[0][1], cur[-1][1]))
    return lines


def build_timed_narration(chunks: list[dict]) -> tuple[Path, list[dict], float]:
    stretch = OUT_AUDIO / "stretched_v001"
    stretch.mkdir(parents=True, exist_ok=True)
    timings = []
    cursor = 0.0
    concat_lines: list[str] = []
    silence_brand = stretch / "_silence_brand.mp3"
    silence_gap = stretch / "_silence_gap.mp3"
    silence_tail = stretch / "_silence_tail.mp3"
    run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono", "-t", str(BRAND_OPENING), "-c:a", "libmp3lame", "-b:a", "192k", str(silence_brand)])
    run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono", "-t", "0.35", "-c:a", "libmp3lame", "-b:a", "192k", str(silence_gap)])
    run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono", "-t", "0.50", "-c:a", "libmp3lame", "-b:a", "192k", str(silence_tail)])
    for i, c in enumerate(chunks):
        src = DRAFT / c["file"]
        out = stretch / c["file"]
        if not out.exists() or out.stat().st_size < 2048:
            run(["ffmpeg", "-y", "-i", str(src), "-filter:a", f"atempo={ATEMPO}", "-c:a", "libmp3lame", "-b:a", "192k", str(out)])
        d = dur(out)
        timings.append({**c, "file": out.name, "start": round(cursor, 3), "end": round(cursor + d, 3), "seconds": round(d, 3)})
        concat_lines.append(f"file '{out.as_posix()}'\n")
        cursor += d
        if i == 0:
            concat_lines.append(f"file '{silence_brand.as_posix()}'\n")
            cursor += BRAND_OPENING
        elif i != len(chunks) - 1:
            concat_lines.append(f"file '{silence_gap.as_posix()}'\n")
            cursor += 0.35
        else:
            concat_lines.append(f"file '{silence_tail.as_posix()}'\n")
            cursor += 0.50
    concat = stretch / "_concat_final.txt"
    concat.write_text("".join(concat_lines), "utf-8")
    final = OUT_AUDIO / "narration_timed_v001.mp3"
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat), "-c:a", "libmp3lame", "-b:a", "192k", str(final)])
    return final, timings, dur(final)


def build_mix(narration: Path, total_sec: float) -> Path:
    OUT_AUDIO.mkdir(parents=True, exist_ok=True)
    bgm = LIB / "music" / "explainer_bed" / "mus_20260614_explainer_bed_soft_explainer_v1.mp3"
    tension = LIB / "music" / "tension_build" / "mus_20260614_tension_build_courtroom_horizon_v1.mp3"
    outro = LIB / "music" / "outro" / "mus_20260614_outro_last_frame_v1.mp3"
    amb = LIB / "ambience" / "amb_institutional_drone.mp3"
    sfx = [
        (LIB / "sfx" / "sfx_riser_2s.mp3", 1.0, 0.34),
        (LIB / "sfx" / "sfx_data_blip.mp3", 92.0, 0.28),
        (LIB / "sfx" / "sfx_ui_tick.mp3", 100.0, 0.25),
        (LIB / "sfx" / "sfx_gavel_knock.mp3", 420.0, 0.48),
        (LIB / "sfx" / "sfx_low_boom.mp3", 420.1, 0.36),
        (LIB / "sfx" / "sfx_stamp_seal.mp3", 432.0, 0.42),
        (LIB / "sfx" / "sfx_soft_impact.mp3", 520.0, 0.26),
        (LIB / "sfx" / "sfx_whoosh_medium.mp3", total_sec - 34.0, 0.28),
    ]
    inputs = ["-i", str(narration), "-stream_loop", "-1", "-i", str(bgm), "-stream_loop", "-1", "-i", str(tension), "-stream_loop", "-1", "-i", str(outro), "-stream_loop", "-1", "-i", str(amb)]
    for path, _, _ in sfx:
        inputs += ["-i", str(path)]
    filters = [
        f"[1:a]volume=0.14,atrim=0:{total_sec},asetpts=PTS-STARTPTS[bgm0]",
        f"[2:a]volume=0.08,atrim=0:{total_sec},asetpts=PTS-STARTPTS[tension0]",
        f"[3:a]volume=0.10,atrim=0:{total_sec},asetpts=PTS-STARTPTS[outro0]",
        f"[4:a]volume=0.035,atrim=0:{total_sec},asetpts=PTS-STARTPTS[amb0]",
        "[bgm0][0:a]sidechaincompress=threshold=0.018:ratio=10:attack=40:release=650[bgmd]",
        "[tension0][0:a]sidechaincompress=threshold=0.018:ratio=8:attack=40:release=700[tensiond]",
        "[outro0][0:a]sidechaincompress=threshold=0.018:ratio=7:attack=40:release=800[outrod]",
        "[amb0][0:a]sidechaincompress=threshold=0.012:ratio=12:attack=50:release=850[ambd]",
    ]
    labels = ["[0:a]", "[bgmd]", "[tensiond]", "[outrod]", "[ambd]"]
    for idx, (_, delay, vol) in enumerate(sfx, start=5):
        ms = int(delay * 1000)
        label = f"sfx{idx}"
        filters.append(f"[{idx}:a]volume={vol},adelay={ms}|{ms}[{label}]")
        labels.append(f"[{label}]")
    filters.append("".join(labels) + f"amix=inputs={len(labels)}:duration=longest:normalize=0,loudnorm=I=-14:TP=-1:LRA=11[mix]")
    out = OUT_AUDIO / "final_mix_v001.mp3"
    run(["ffmpeg", "-y", *inputs, "-filter_complex", ";".join(filters), "-map", "[mix]", "-t", str(total_sec), "-c:a", "libmp3lame", "-b:a", "192k", str(out)])
    REM_PUBLIC_AUDIO.mkdir(parents=True, exist_ok=True)
    (REM_PUBLIC_AUDIO / out.name).write_bytes(out.read_bytes())
    return out


def transcribe_words(path: Path) -> list[dict]:
    from faster_whisper import WhisperModel

    print("loading faster-whisper small.en (cpu/int8)...")
    model = WhisperModel("small.en", device="cpu", compute_type="int8")
    segs, _ = model.transcribe(str(path), word_timestamps=True, vad_filter=False, beam_size=5, language="en")
    words = []
    for s in segs:
        for w in s.words or []:
            words.append({"w": w.word.strip(), "n": norm(w.word), "start": float(w.start), "end": float(w.end)})
    print(f"whisper_words={len(words)}")
    return words


def captions(chunks: list[dict], words: list[dict]) -> list[dict]:
    entries = []
    idx = 1
    for c in chunks:
        toks = c["spoken_text"].split()
        cw = [w for w in words if c["start"] - 0.2 <= (w["start"] + w["end"]) / 2 <= c["end"] + 0.2]
        times: list[tuple[float, float] | None] = [None] * len(toks)
        j = 0
        for ti, tk in enumerate(toks):
            tn = norm(tk)
            if not tn:
                continue
            found = None
            for k in range(j, min(j + 5, len(cw))):
                if cw[k]["n"] == tn or (len(tn) >= 4 and cw[k]["n"].startswith(tn[:4])):
                    found = k
                    break
            if found is None and j < len(cw):
                found = j
            if found is not None:
                times[ti] = (cw[found]["start"], cw[found]["end"])
                j = found + 1
        for ti in range(len(toks)):
            if times[ti] is None:
                frac = (ti + 0.5) / max(1, len(toks))
                t = c["start"] + frac * (c["end"] - c["start"])
                times[ti] = (t, t + 0.28)
        for line, a, b in split_lines(toks):
            s, _ = times[a] or (c["start"], c["start"] + 0.3)
            _, e = times[b] or (s, s + 0.65)
            if e <= s:
                e = s + 0.65
            entries.append({"index": idx, "start": round(s, 3), "end": round(e, 3), "text": line})
            idx += 1
    fixed = []
    for e in entries:
        if fixed and e["start"] < fixed[-1]["end"]:
            e["start"] = round(fixed[-1]["end"] + 0.001, 3)
        if e["end"] <= e["start"]:
            e["end"] = round(e["start"] + 0.55, 3)
        fixed.append(e)
    return fixed


def write_caption_files(entries: list[dict]) -> None:
    OUT_CAP.mkdir(parents=True, exist_ok=True)
    srt = OUT_CAP / "captions.v001.srt"
    srt.write_text("\n".join(f"{e['index']}\n{ts(e['start'])} --> {ts(e['end'])}\n{e['text']}\n" for e in entries), "utf-8")
    (OUT_CAP / "captions.v001.json").write_text(json.dumps(entries, indent=2, ensure_ascii=False) + "\n", "utf-8")
    data = "export type KingCaption = {start: number; end: number; text: string};\n"
    data += "export const KING_CAPTIONS: KingCaption[] = "
    data += json.dumps([{k: e[k] for k in ("start", "end", "text")} for e in entries], ensure_ascii=False, indent=2)
    data += ";\n"
    (REM_DATA / "king_captions.ts").write_text(data, "utf-8")


def write_timing(chunks: list[dict], total_sec: float) -> None:
    scene_ids = [
        "SPN-0001", "SPN-0002", "SPN-0003", "SPN-0004", "SPN-0005", "SPN-0006", "SPN-0007", "SPN-0008",
        "SPN-0009", "SPN-0010", "SPN-0011", "SPN-0022", "SPN-0012", "SPN-0013", "SPN-0023", "SPN-0014",
        "SPN-0015", "SPN-0016", "SPN-0017", "SPN-0018", "SPN-0019", "SPN-0020", "SPN-0021",
    ]
    timings = {}
    for sid, c in zip(scene_ids, chunks):
        end_extra = 0.0
        if sid != "SPN-0001" and sid != "SPN-0021":
            end_extra = 0.35
        if sid == "SPN-0021":
            end_extra = 0.50
        timings[sid] = {"start": c["start"], "dur": round(c["seconds"] + end_extra, 3)}
    visual_total = round(total_sec + ENDCARD, 3)
    text = "export type KingSceneTiming = {start: number; dur: number};\n"
    text += f"export const KING_TOTAL_SEC = {visual_total};\n"
    text += "export const KING_SCENE_TIMING: Record<string, KingSceneTiming> = "
    text += json.dumps(timings, indent=2)
    text += ";\n"
    (REM_DATA / "king_timing.ts").write_text(text, "utf-8")
    qc = {
        "episode_id": EP,
        "narration_timed_seconds": round(total_sec, 3),
        "visual_total_seconds": visual_total,
        "target_window_seconds": [690, 750],
        "atempo": ATEMPO,
        "brand_opening_gap_seconds": BRAND_OPENING,
        "endcard_seconds": ENDCARD,
    }
    (OUT_AUDIO / "audio_build_qc.v001.json").write_text(json.dumps(qc, indent=2) + "\n", "utf-8")


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    idx = json.loads(VOICE_INDEX.read_text("utf-8"))
    narration, timed, narration_sec = build_timed_narration(idx["chunks"])
    mix = build_mix(narration, narration_sec + ENDCARD)
    words = transcribe_words(narration)
    entries = captions(timed, words)
    write_caption_files(entries)
    write_timing(timed, narration_sec)
    timed_index = {**idx, "generated_total_seconds": round(narration_sec, 3), "timed_master": f"artifact://episodes/{EP}/07_audio/narration_timed_v001.mp3", "final_mix": f"artifact://episodes/{EP}/07_audio/final_mix_v001.mp3", "chunks": timed}
    (ROOT / "episodes" / EP / "06_audio" / "narration_index.v001.json").write_text(json.dumps(timed_index, indent=2, ensure_ascii=False) + "\n", "utf-8")
    print(f"narration={narration} {narration_sec:.2f}s")
    print(f"mix={mix} {dur(mix):.2f}s")
    print(f"captions={len(entries)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
