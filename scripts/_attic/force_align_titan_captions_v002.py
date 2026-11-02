#!/usr/bin/env python3
"""Force-align Titan captions to the actual narration timeline.

Uses faster-whisper word timestamps from the narration-only timeline WAV, keeps
the approved script text as the displayed text, and writes cleaner v002 caption
artifacts plus the Remotion data file used for burned-in captions.
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-016-titan"
EPDIR = ROOT / "episodes" / EP
SHOTLIST = EPDIR / "04_scenes" / "shotlist.v001.json"
CAPTIONS_SRT = EPDIR / "08_edit" / "captions.v002.srt"
CAPTIONS_JSON = EPDIR / "08_edit" / "captions.v002.json"
CAPTIONS_QC = EPDIR / "08_edit" / "captions.v002.qc.json"
REM_CAPTIONS = ROOT / "remotion" / "src" / "data" / "titan_captions.ts"
SILENCE_SPAN_ID = "SPN-0071"
OPENING_AFTER_SPAN_ID = "SPN-0005"
OPENING_SEC = 3.5
MAX_WORDS = 7
MAX_CHARS = 44


def media_root() -> Path:
    cfg = json.loads((ROOT / "config" / "storage.local.json").read_text("utf-8"))
    return Path(cfg["roots"]["media"]["path"])


MEDIA = media_root()
VOICE_DIR = MEDIA / "episodes" / EP / "06_voice" / "draft"
NARRATION_TIMELINE = MEDIA / "episodes" / EP / "06_audio" / "final_mix_v001_work" / "narration_timeline_v001.wav"


def norm_word(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.lower())


def norm_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def srt_ts(t: float) -> str:
    ms = max(0, int(round(t * 1000)))
    h = ms // 3_600_000
    ms %= 3_600_000
    m = ms // 60_000
    ms %= 60_000
    s = ms // 1000
    ms %= 1000
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def load_rows() -> list[dict[str, Any]]:
    manifest = json.loads((EPDIR / "manifest.json").read_text("utf-8"))
    script_rev = manifest["active_revisions"]["script"]
    spans = json.loads((EPDIR / "03_script" / f"script.annotated.{script_rev}.json").read_text("utf-8"))["spans"]
    shots = json.loads(SHOTLIST.read_text("utf-8"))["shots"]
    index = json.loads((EPDIR / "06_audio" / "narration_index.v001.json").read_text("utf-8"))["chunks"]
    by_span = {item["span_id"]: item for item in index}
    rows: list[dict[str, Any]] = []
    cursor = 0.0
    for span, shot in zip(spans, shots):
        if span["span_id"] != shot["span_id"]:
            raise RuntimeError(f"span/shot mismatch: {span['span_id']} != {shot['span_id']}")
        seconds = float(shot["estimated_seconds"])
        text = norm_text(span.get("text", ""))
        speak = bool(text and text != "..." and span["span_id"] != SILENCE_SPAN_ID)
        row: dict[str, Any] = {
            "span_id": span["span_id"],
            "chapter_id": shot["chapter_id"],
            "text": text,
            "shot_start": round(cursor, 3),
            "shot_end": round(cursor + seconds, 3),
            "shot_seconds": round(seconds, 3),
            "speak": speak,
        }
        if speak:
            item = by_span[span["span_id"]]
            src = VOICE_DIR / item["file"]
            if not src.exists():
                raise FileNotFoundError(src)
            raw = float(item.get("seconds") or item.get("raw_voice_seconds") or 0)
            available = max(0.45, seconds - 0.32)
            out_dur = min(raw, available)
            row.update(
                {
                    "chunk_id": item["chunk_id"],
                    "voice_start": round(cursor, 3),
                    "voice_end": round(cursor + out_dur, 3),
                    "voice_seconds": round(out_dur, 3),
                }
            )
        rows.append(row)
        cursor += seconds
        if span["span_id"] == OPENING_AFTER_SPAN_ID:
            cursor += OPENING_SEC
    return rows


def transcribe_words() -> list[dict[str, Any]]:
    from faster_whisper import WhisperModel

    if not NARRATION_TIMELINE.exists():
        raise FileNotFoundError(NARRATION_TIMELINE)
    print("loading faster-whisper small.en cpu/int8", flush=True)
    model = WhisperModel("small.en", device="cpu", compute_type="int8")
    segments, _info = model.transcribe(str(NARRATION_TIMELINE), word_timestamps=True, vad_filter=False, beam_size=5, language="en")
    words: list[dict[str, Any]] = []
    for segment in segments:
        for word in segment.words or []:
            text = word.word.strip()
            n = norm_word(text)
            if n:
                words.append({"word": text, "norm": n, "start": float(word.start), "end": float(word.end)})
    print(f"whisper words={len(words)}", flush=True)
    return words


def split_lines(tokens: list[str]) -> list[tuple[str, int, int]]:
    lines: list[tuple[str, int, int]] = []
    cur: list[tuple[str, int]] = []
    for i, token in enumerate(tokens):
        trial = " ".join([item[0] for item in cur] + [token])
        if cur and (len(cur) >= MAX_WORDS or len(trial) > MAX_CHARS):
            lines.append((" ".join(item[0] for item in cur), cur[0][1], cur[-1][1]))
            cur = []
        cur.append((token, i))
        if re.search(r"[.?!]$", token) or token.endswith("—") or (token.endswith(",") and len(cur) >= 4):
            lines.append((" ".join(item[0] for item in cur), cur[0][1], cur[-1][1]))
            cur = []
    if cur:
        lines.append((" ".join(item[0] for item in cur), cur[0][1], cur[-1][1]))
    return lines


def align_chunk(row: dict[str, Any], whisper_words: list[dict[str, Any]]) -> list[tuple[float, float]]:
    tokens = row["text"].split()
    start = float(row["voice_start"])
    end = float(row["voice_end"])
    if not tokens:
        return []
    centers = [w for w in whisper_words if start - 0.35 <= (w["start"] + w["end"]) / 2 <= end + 0.35]
    times: list[tuple[float, float] | None] = [None] * len(tokens)
    wi = 0
    for ti, token in enumerate(tokens):
        target = norm_word(token)
        if not target:
            continue
        found = None
        for offset in range(0, 7):
            idx = wi + offset
            if idx >= len(centers):
                break
            candidate = centers[idx]["norm"]
            prefix = target[: max(3, min(5, len(target)))]
            if candidate == target or candidate.startswith(prefix) or target.startswith(candidate[: max(3, min(5, len(candidate)))]):
                found = idx
                break
        if found is None and wi < len(centers):
            found = wi
        if found is not None:
            w = centers[found]
            times[ti] = (max(start, float(w["start"])), min(end, float(w["end"])))
            wi = found + 1
    for ti, value in enumerate(times):
        if value is None:
            frac = (ti + 0.5) / len(tokens)
            t = start + frac * max(0.5, end - start)
            times[ti] = (t, min(end, t + 0.24))
    return [t for t in times if t is not None]


def build_cues(rows: list[dict[str, Any]], whisper_words: list[dict[str, Any]]) -> list[dict[str, Any]]:
    cues: list[dict[str, Any]] = []
    idx = 1
    for row in rows:
        if not row["speak"]:
            continue
        tokens = row["text"].split()
        word_times = align_chunk(row, whisper_words)
        for line, start_i, end_i in split_lines(tokens):
            start = word_times[start_i][0]
            end = word_times[end_i][1]
            if end <= start:
                end = start + 0.45
            cues.append(
                {
                    "index": idx,
                    "start": round(start, 3),
                    "end": round(end, 3),
                    "text": line,
                    "span_id": row["span_id"],
                }
            )
            idx += 1
    fixed: list[dict[str, Any]] = []
    previous_end = 0.0
    for cue in cues:
        cue["start"] = max(float(cue["start"]), previous_end + 0.001 if fixed else 0.0)
        cue["end"] = max(float(cue["end"]), cue["start"] + 0.35)
        cue["start"] = round(cue["start"], 3)
        cue["end"] = round(cue["end"], 3)
        previous_end = cue["end"]
        fixed.append(cue)
    return fixed


def write_outputs(rows: list[dict[str, Any]], cues: list[dict[str, Any]]) -> None:
    CAPTIONS_SRT.parent.mkdir(parents=True, exist_ok=True)
    CAPTIONS_SRT.write_text(
        "\n".join(f"{c['index']}\n{srt_ts(c['start'])} --> {srt_ts(c['end'])}\n{c['text']}\n" for c in cues),
        "utf-8",
    )
    CAPTIONS_JSON.write_text(
        json.dumps({"episode_id": EP, "revision": "v002", "source": "faster-whisper forced alignment to narration_timeline_v001.wav", "cues": cues}, indent=2, ensure_ascii=False) + "\n",
        "utf-8",
    )
    REM_CAPTIONS.write_text(
        "export type TitanCaptionCue = {start: number; end: number; text: string};\n\n"
        "export const TITAN_CAPTIONS: TitanCaptionCue[] = "
        + json.dumps([{k: c[k] for k in ("start", "end", "text")} for c in cues], indent=2, ensure_ascii=False)
        + ";\n",
        "utf-8",
    )
    script_text = " ".join(row["text"] for row in rows if row["speak"])
    caption_text = " ".join(cue["text"] for cue in cues)
    longest_words = max(len(cue["text"].split()) for cue in cues)
    longest_chars = max(len(cue["text"]) for cue in cues)
    overlaps = sum(1 for prev, cur in zip(cues, cues[1:]) if float(cur["start"]) < float(prev["end"]))
    qc = {
        "episode_id": EP,
        "revision": "v002",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_audio": str(NARRATION_TIMELINE).replace("\\", "/"),
        "cue_count": len(cues),
        "text_exact_match_to_script": norm_text(script_text) == norm_text(caption_text),
        "script_words": len(script_text.split()),
        "caption_words": len(caption_text.split()),
        "longest_caption_words": longest_words,
        "longest_caption_chars": longest_chars,
        "overlap_count": overlaps,
        "qc_status": "pass" if norm_text(script_text) == norm_text(caption_text) and overlaps == 0 and longest_words <= MAX_WORDS and longest_chars <= MAX_CHARS else "review",
    }
    CAPTIONS_QC.write_text(json.dumps(qc, indent=2, ensure_ascii=False) + "\n", "utf-8")
    print(json.dumps(qc, indent=2, ensure_ascii=False), flush=True)


def main() -> int:
    rows = load_rows()
    words = transcribe_words()
    cues = build_cues(rows, words)
    write_outputs(rows, cues)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
