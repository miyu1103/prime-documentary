#!/usr/bin/env python
"""Create EP48 Glover local review narration and timing index with Windows SAPI."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-048-glover"
SCRIPT = ROOT / "episodes" / EP / "03_script" / "script.en.v001.md"
OUT_DIR = ROOT / "episodes" / EP / "06_audio"
TEXT_OUT = OUT_DIR / "spoken_text.v001.txt"
WAV_OUT = OUT_DIR / "narration_local_review.v001.wav"
MP3_OUT = OUT_DIR / "narration_local_review.v001.mp3"
INDEX = OUT_DIR / "narration_index.v001.json"
PUBLIC_AUDIO = ROOT / "remotion" / "public" / "glover" / "audio" / "narration_local_review.v001.mp3"
SECTION_ORDER = ["HOOK", "OP", "ACT_1", "ACT_2", "ACT_3", "ENDING"]
HEADING_MAP = {
    "[HOOK]": "HOOK",
    "[OPENING]": "OP",
    "[ACT_1]": "ACT_1",
    "[ACT_2]": "ACT_2",
    "[ACT_3]": "ACT_3",
    "[ENDING]": "ENDING",
}
TARGET_MIN = 690.0
TARGET_MAX = 750.0
TARGET = 719.6


def sha_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def clean_line(line: str) -> str:
    line = re.sub(r"【[^】]*】|〔[^〕]*〕|\[[^\]]*\]", " ", line)
    line = re.sub(r"\*\*|\*|`", "", line)
    return " ".join(line.split())


def split_sentences(text: str) -> list[str]:
    protected = (
        text.replace("U.S.", "U<S>")
        .replace("v.", "v<dot>")
        .replace("Mr.", "Mr<dot>")
        .replace("Jr.", "Jr<dot>")
        .replace("No.", "No<dot>")
    )
    parts = [p.strip() for p in re.split(r"(?<=[.!?])\s+", protected) if p.strip()]
    return [
        p.replace("U<S>", "U.S.").replace("v<dot>", "v.").replace("Mr<dot>", "Mr.").replace("Jr<dot>", "Jr.").replace("No<dot>", "No.")
        for p in parts
    ]


def word_count(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'’-]*", text))


def extract_chunks() -> list[dict]:
    chunks: list[dict] = []
    current: str | None = None
    pending_silence = 0.0
    for raw in SCRIPT.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line.startswith("## 事実対応表") or line.startswith("## SELF-CHECK"):
            break
        hm = re.match(r"^##\s+(\[[A-Z0-9_]+\])", line)
        if hm:
            current = HEADING_MAP.get(hm.group(1))
            continue
        if line.startswith("## "):
            current = None
            continue
        if current is None or not line or line == "---":
            continue
        sm = re.search(r"SILENCE\s+\d+\s+[—-]\s+([0-9]+(?:\.[0-9]+)?)s", line, re.IGNORECASE)
        if sm and chunks:
            chunks[-1]["silence_after_seconds"] = float(sm.group(1))
            pending_silence = 0.0
            continue
        if line.startswith("【") or line.startswith("|") or line.startswith("#"):
            continue
        text = clean_line(line)
        if not text:
            continue
        for sent in split_sentences(text):
            sent = clean_line(sent)
            if not sent:
                continue
            chunks.append({
                "id": f"VC-{len(chunks) + 1:04d}",
                "chunk_id": f"VC-{len(chunks) + 1:04d}",
                "section": current,
                "delivery": "intense" if current == "HOOK" else "calm" if current == "ENDING" else "building",
                "text": sent,
                "spoken_text": sent,
                "words": word_count(sent),
                "silence_after_seconds": pending_silence,
                "idempotency_key": "sha256:" + sha_text(sent),
            })
            pending_silence = 0.22
    return chunks


def ffprobe_duration(path: Path) -> float:
    out = subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(path),
    ], text=True)
    return float(out.strip())


def write_sapi_wav(text_path: Path, wav_path: Path, rate: int) -> None:
    ps = f"""
$text = Get-Content -LiteralPath '{text_path}' -Raw -Encoding UTF8
$voice = New-Object -ComObject SAPI.SpVoice
$voice.Rate = {rate}
$voice.Volume = 100
$stream = New-Object -ComObject SAPI.SpFileStream
$stream.Open('{wav_path}', 3, $false)
$voice.AudioOutputStream = $stream
[void]$voice.Speak($text)
$stream.Close()
"""
    subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps], check=True)


def build_index(chunks: list[dict], total: float, audio_public: str) -> dict:
    total_words = max(1, sum(int(c["words"]) for c in chunks))
    speech_total = max(1.0, total - sum(float(c.get("silence_after_seconds") or 0.0) for c in chunks))
    t = 0.0
    lines = []
    for c in chunks:
        dur = max(1.1, speech_total * int(c["words"]) / total_words)
        start = t
        end = min(total, start + dur)
        row = {**c, "start": round(start, 3), "end": round(end, 3), "seconds": round(end - start, 3)}
        lines.append(row)
        t = end + float(c.get("silence_after_seconds") or 0.0)
    if lines:
        lines[-1]["end"] = round(total, 3)
        lines[-1]["seconds"] = round(total - float(lines[-1]["start"]), 3)
    return {
        "schema_version": "glover_narration.v1",
        "episode_id": EP,
        "source": "windows_sapi_local_review_voice",
        "is_measured_audio": True,
        "audio_path": audio_public,
        "master": str(MP3_OUT),
        "total_seconds": round(total, 3),
        "sections": SECTION_ORDER,
        "chunks": lines,
        "lines": lines,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rate", type=int, default=4)
    args = ap.parse_args()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    PUBLIC_AUDIO.parent.mkdir(parents=True, exist_ok=True)
    chunks = extract_chunks()
    spoken = "\r\n\r\n".join(c["text"] for c in chunks)
    TEXT_OUT.write_text(spoken + "\n", encoding="utf-8")
    chosen_rate = args.rate
    for rate in [args.rate, 5, 6, 3, 7]:
        write_sapi_wav(TEXT_OUT, WAV_OUT, rate)
        subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(WAV_OUT), "-codec:a", "libmp3lame", "-q:a", "3", str(MP3_OUT)], check=True)
        total = ffprobe_duration(MP3_OUT)
        chosen_rate = rate
        if TARGET_MIN <= total <= TARGET_MAX:
            break
        if total <= TARGET_MAX and abs(total - TARGET) < 65:
            break
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(MP3_OUT), "-codec:a", "libmp3lame", "-q:a", "3", str(PUBLIC_AUDIO)], check=True)
    total = ffprobe_duration(MP3_OUT)
    data = build_index(chunks, total, "glover/audio/narration_local_review.v001.mp3")
    data["voice_rate"] = chosen_rate
    INDEX.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"episode_id": EP, "chunks": len(chunks), "seconds": round(total, 3), "rate": chosen_rate, "index": str(INDEX)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
