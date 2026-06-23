#!/usr/bin/env python3
"""Build Miranda Premium narration timeline, mix, captions, and Remotion timing data."""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-001-miranda"
MEDIA = Path(json.loads((ROOT / "config/storage.local.json").read_text("utf-8"))["roots"]["media"]["path"])
EP_MEDIA = MEDIA / "episodes" / EP
VOICE_PLAN = ROOT / "episodes" / EP / "06_audio" / "voice_plan.v001.json"
SLOW = EP_MEDIA / "06_voice" / "slow_v001"
DRAFT = EP_MEDIA / "06_voice" / "draft"
MASTER = EP_MEDIA / "06_voice" / "master" / "vc_master_premium_v001.mp3"
OUT_AUDIO = EP_MEDIA / "07_audio"
REM_AUDIO = ROOT / "remotion" / "public" / "miranda" / "audio"
OUT_CAP = ROOT / "episodes" / EP / "08_edit"
REM_DATA = ROOT / "remotion" / "src" / "data"
LIB = MEDIA / "library"
FPS = 30
BRAND_GAP = 3.5
INTER_GAP = 0.25
CTA_SEC = 4.0
ENDCARD_SEC = 9.0


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def dur(path: Path) -> float:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    return float((r.stdout or "0").strip() or 0)


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
        if cur and (len(cur) >= 9 or len(trial) > 58):
            lines.append((" ".join(x for x, _ in cur), cur[0][1], cur[-1][1]))
            cur = []
        cur.append((w, i))
        if re.search(r"[.?!—]$", w) or (w.endswith(",") and len(cur) >= 5):
            lines.append((" ".join(x for x, _ in cur), cur[0][1], cur[-1][1]))
            cur = []
    if cur:
        lines.append((" ".join(x for x, _ in cur), cur[0][1], cur[-1][1]))
    return lines


def silence(path: Path, seconds: float) -> None:
    if not path.exists():
        run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono", "-t", f"{seconds:.3f}", "-c:a", "libmp3lame", "-b:a", "192k", str(path)])


def build_narration(chunks: list[dict]) -> tuple[Path, list[dict], dict[str, float], float]:
    OUT_AUDIO.mkdir(parents=True, exist_ok=True)
    scratch = OUT_AUDIO / "miranda_timeline_v001"
    scratch.mkdir(parents=True, exist_ok=True)
    brand_silence = scratch / "_brand_gap.mp3"
    gap_silence = scratch / "_inter_gap.mp3"
    tail_silence = scratch / "_tail_gap.mp3"
    silence(brand_silence, BRAND_GAP)
    silence(gap_silence, INTER_GAP)

    cursor = 0.0
    concat_lines: list[str] = []
    timed: list[dict] = []
    scene_durations: dict[str, float] = {}
    for idx, c in enumerate(chunks):
        cid = c["chunk_id"]
        src = SLOW / f"{cid}.mp3"
        if not src.exists():
            src = DRAFT / f"{cid}.mp3"
        if not src.exists():
            raise FileNotFoundError(f"missing narration chunk {cid}")
        d = dur(src)
        span = c["span_ids"][0]
        gap_after = BRAND_GAP if idx == 0 else (INTER_GAP if idx != len(chunks) - 1 else 0.0)
        scene_durations[span] = round(d + (INTER_GAP if 0 < idx < len(chunks) - 1 else 0.0), 3)
        timed.append({**c, "file": src.name, "start": round(cursor, 3), "end": round(cursor + d, 3), "seconds": round(d, 3)})
        concat_lines.append(f"file '{src.as_posix()}'\n")
        cursor += d
        if gap_after:
            concat_lines.append(f"file '{(brand_silence if idx == 0 else gap_silence).as_posix()}'\n")
            cursor += gap_after
    scene_durations["brand"] = BRAND_GAP
    scene_durations["SPN-0024"] = CTA_SEC
    scene_durations["endcard"] = ENDCARD_SEC
    visual_total = round(cursor + CTA_SEC + ENDCARD_SEC, 3)
    tail = max(0.001, visual_total - cursor)
    silence(tail_silence, tail)
    concat_lines.append(f"file '{tail_silence.as_posix()}'\n")
    concat = scratch / "_concat_narration.txt"
    concat.write_text("".join(concat_lines), "utf-8")
    MASTER.parent.mkdir(parents=True, exist_ok=True)
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat), "-c:a", "libmp3lame", "-b:a", "192k", str(MASTER)])
    return MASTER, timed, scene_durations, visual_total


def build_mix(narration: Path, total_sec: float, starts: dict[str, float]) -> Path:
    OUT_AUDIO.mkdir(parents=True, exist_ok=True)
    bgm = LIB / "music" / "explainer_bed" / "mus_20260614_explainer_bed_soft_explainer_v1.mp3"
    tension = LIB / "music" / "tension_build" / "mus_20260614_tension_build_courtroom_horizon_v1.mp3"
    reveal = LIB / "music" / "reveal" / "mus_20260614_reveal_verdict_at_dawn_v1.mp3"
    outro = LIB / "music" / "outro" / "mus_20260614_outro_last_frame_v1.mp3"
    amb = LIB / "ambience" / "amb_tension_drone.mp3"
    clock = LIB / "sfx" / "sfx_clock_tick_loop.mp3"
    sfx = [
        (LIB / "sfx" / "sfx_riser_2s.mp3", 1.0, 0.28),
        (LIB / "sfx" / "sfx_low_boom.mp3", starts.get("SPN-0012", 340.0) + 2.35, 0.42),
        (LIB / "sfx" / "sfx_gavel_knock.mp3", starts.get("SPN-0012", 340.0) + 2.55, 0.54),
        (LIB / "sfx" / "sfx_stamp_seal.mp3", starts.get("SPN-0012", 340.0) + 6.0, 0.48),
        (LIB / "sfx" / "sfx_ui_tick.mp3", starts.get("SPN-0013", 380.0) + 1.0, 0.22),
        (LIB / "sfx" / "sfx_ui_tick.mp3", starts.get("SPN-0013", 380.0) + 3.0, 0.22),
        (LIB / "sfx" / "sfx_ui_tick.mp3", starts.get("SPN-0013", 380.0) + 5.0, 0.22),
        (LIB / "sfx" / "sfx_ui_tick.mp3", starts.get("SPN-0013", 380.0) + 7.0, 0.22),
        (LIB / "sfx" / "sfx_whoosh_medium.mp3", starts.get("SPN-0023", total_sec - 45), 0.24),
    ]
    inputs = [
        "-i", str(narration),
        "-stream_loop", "-1", "-i", str(bgm),
        "-stream_loop", "-1", "-i", str(tension),
        "-stream_loop", "-1", "-i", str(reveal),
        "-stream_loop", "-1", "-i", str(outro),
        "-stream_loop", "-1", "-i", str(amb),
        "-stream_loop", "-1", "-i", str(clock),
    ]
    for path, _, _ in sfx:
        inputs += ["-i", str(path)]
    filters = [
        f"[1:a]volume=0.115,atrim=0:{total_sec},asetpts=PTS-STARTPTS[bgm0]",
        f"[2:a]volume=0.085,atrim=0:{total_sec},asetpts=PTS-STARTPTS[tension0]",
        f"[3:a]volume=0.060,atrim=0:{total_sec},asetpts=PTS-STARTPTS[reveal0]",
        f"[4:a]volume=0.095,atrim=0:{total_sec},asetpts=PTS-STARTPTS[outro0]",
        f"[5:a]volume=0.038,atrim=0:{total_sec},asetpts=PTS-STARTPTS[amb0]",
        f"[6:a]volume=0.030,atrim=0:{total_sec},asetpts=PTS-STARTPTS[clock0]",
        "[bgm0][0:a]sidechaincompress=threshold=0.018:ratio=10:attack=35:release=650[bgmd]",
        "[tension0][0:a]sidechaincompress=threshold=0.018:ratio=9:attack=35:release=700[tensiond]",
        "[reveal0][0:a]sidechaincompress=threshold=0.018:ratio=8:attack=35:release=650[reveald]",
        "[outro0][0:a]sidechaincompress=threshold=0.018:ratio=8:attack=40:release=800[outrod]",
        "[amb0][0:a]sidechaincompress=threshold=0.014:ratio=12:attack=45:release=850[ambd]",
        "[clock0][0:a]sidechaincompress=threshold=0.014:ratio=12:attack=30:release=500[clockd]",
    ]
    labels = ["[0:a]", "[bgmd]", "[tensiond]", "[reveald]", "[outrod]", "[ambd]", "[clockd]"]
    for idx, (_, delay, vol) in enumerate(sfx, start=7):
        ms = int(delay * 1000)
        label = f"sfx{idx}"
        filters.append(f"[{idx}:a]volume={vol},adelay={ms}|{ms}[{label}]")
        labels.append(f"[{label}]")
    filters.append("".join(labels) + f"amix=inputs={len(labels)}:duration=longest:normalize=0,loudnorm=I=-14:TP=-1:LRA=11[mix]")
    out = OUT_AUDIO / "final_mix_v001.mp3"
    run(["ffmpeg", "-y", *inputs, "-filter_complex", ";".join(filters), "-map", "[mix]", "-t", f"{total_sec:.3f}", "-c:a", "libmp3lame", "-b:a", "192k", str(out)])
    REM_AUDIO.mkdir(parents=True, exist_ok=True)
    shutil.copy2(out, REM_AUDIO / out.name)
    return out


def transcribe_words(path: Path) -> list[dict]:
    try:
        from faster_whisper import WhisperModel
    except Exception:
        return []
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
        cw = [w for w in words if c["start"] - 0.2 <= (w["start"] + w["end"]) / 2 <= c["end"] + 0.2] if words else []
        times: list[tuple[float, float] | None] = [None] * len(toks)
        j = 0
        for ti, tk in enumerate(toks):
            tn = norm(tk)
            found = None
            for k in range(j, min(j + 6, len(cw))):
                if cw[k]["n"] == tn or (len(tn) >= 4 and cw[k]["n"].startswith(tn[:4])):
                    found = k
                    break
            if found is not None:
                times[ti] = (cw[found]["start"], cw[found]["end"])
                j = found + 1
        for ti in range(len(toks)):
            if times[ti] is None:
                frac = (ti + 0.5) / max(1, len(toks))
                t = c["start"] + frac * (c["end"] - c["start"])
                times[ti] = (t, min(c["end"], t + 0.32))
        for line, a, b in split_lines(toks):
            s, _ = times[a] or (c["start"], c["start"] + 0.35)
            _, e = times[b] or (s, s + 0.7)
            if e <= s:
                e = s + 0.7
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


def write_outputs(chunks: list[dict], entries: list[dict], scene_durations: dict[str, float], total_sec: float, mix: Path) -> None:
    OUT_CAP.mkdir(parents=True, exist_ok=True)
    srt = OUT_CAP / "captions.v001.srt"
    srt.write_text("\n".join(f"{e['index']}\n{ts(e['start'])} --> {ts(e['end'])}\n{e['text']}\n" for e in entries), "utf-8")
    (OUT_CAP / "captions.v001.json").write_text(json.dumps(entries, indent=2, ensure_ascii=False) + "\n", "utf-8")
    cap_ts = "export type MirandaCaption = {start: number; end: number; text: string};\n"
    cap_ts += "export const MIRANDA_CAPTIONS: MirandaCaption[] = "
    cap_ts += json.dumps([{k: e[k] for k in ("start", "end", "text")} for e in entries], indent=2, ensure_ascii=False)
    cap_ts += ";\n"
    (REM_DATA / "miranda_captions.ts").write_text(cap_ts, "utf-8")
    timing_ts = "export const MIRANDA_SCENE_DURATIONS: Record<string, number> = "
    timing_ts += json.dumps(scene_durations, indent=2)
    timing_ts += ";\n"
    timing_ts += f"export const MIRANDA_TOTAL_SEC: number | null = {total_sec:.3f};\n"
    (REM_DATA / "miranda_timing.ts").write_text(timing_ts, "utf-8")
    index = {
        "episode_id": EP,
        "voice_source": "ElevenLabs existing/generated chunks",
        "generated_total_seconds": round(total_sec, 3),
        "master": f"artifact://episodes/{EP}/06_voice/master/vc_master_premium_v001.mp3",
        "final_mix": f"artifact://episodes/{EP}/07_audio/final_mix_v001.mp3",
        "captions": f"episodes/{EP}/08_edit/captions.v001.srt",
        "chunks": chunks,
        "mix_file": str(mix),
    }
    (ROOT / "episodes" / EP / "06_audio" / "narration_index.v001.json").write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n", "utf-8")


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    plan = json.loads(VOICE_PLAN.read_text("utf-8"))
    narration, timed, scene_durations, total_sec = build_narration(plan["chunks"])
    cursor = 0.0
    starts = {}
    for sid in ["SPN-0001", "brand", *[c["span_ids"][0] for c in plan["chunks"][1:]], "SPN-0024", "endcard"]:
        starts[sid] = cursor
        cursor += scene_durations[sid]
    mix = build_mix(narration, total_sec, starts)
    words = transcribe_words(narration)
    entries = captions(timed, words)
    write_outputs(timed, entries, scene_durations, total_sec, mix)
    print(f"narration={narration} {dur(narration):.2f}s")
    print(f"mix={mix} {dur(mix):.2f}s")
    print(f"captions={len(entries)} total={total_sec:.2f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
