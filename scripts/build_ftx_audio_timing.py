"""Build slowed narration master, timing JSON, and captions for PD-2026-004-ftx."""

from __future__ import annotations

import json
import math
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-004-ftx"
MEDIA = Path(r"H:\pd-media")
PLAN = ROOT / "episodes" / EP / "06_audio" / "voice_plan.v001.json"
DRAFT = MEDIA / "episodes" / EP / "06_voice" / "draft"
MASTER_DIR = MEDIA / "episodes" / EP / "06_voice" / "master"
EDIT_DIR = ROOT / "episodes" / EP / "08_edit"
TMP = MEDIA / "episodes" / EP / "tmp" / "audio_build"
FFMPEG = "ffmpeg"
FFPROBE = "ffprobe"

ATEMPO = 0.78
OPENING_SEC = 3.5
ENDCARD_SEC = 9.0
MIN_TOTAL_SEC = 720.0


def duration(path: Path) -> float:
    result = subprocess.run(
        [FFPROBE, "-v", "quiet", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        capture_output=True,
        text=True,
        check=True,
    )
    return float(result.stdout.strip())


def srt_ts(t: float) -> str:
    if t < 0:
        t = 0
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = int(t % 60)
    ms = int(round((t - math.floor(t)) * 1000))
    if ms == 1000:
        s += 1
        ms = 0
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def split_caption_lines(text: str, max_words: int = 7, max_chars: int = 42) -> list[str]:
    words = text.split()
    lines: list[list[str]] = []
    cur: list[str] = []
    for word in words:
        trial = " ".join(cur + [word])
        if cur and (len(cur) >= max_words or len(trial) > max_chars):
            lines.append(cur)
            cur = []
        cur.append(word)
        if re.search(r"[.?!—]$", word) and len(cur) >= 3:
            lines.append(cur)
            cur = []
    if cur:
        lines.append(cur)
    return [" ".join(line) for line in lines]


def main() -> int:
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    chunks = plan["chunks"]
    TMP.mkdir(parents=True, exist_ok=True)
    MASTER_DIR.mkdir(parents=True, exist_ok=True)
    EDIT_DIR.mkdir(parents=True, exist_ok=True)

    timeline = []
    cursor = 0.0
    prev_section = None
    pieces: list[Path] = []

    def add_silence(seconds: float, name: str) -> None:
        nonlocal cursor
        if seconds <= 0:
            return
        out = TMP / f"{len(pieces):04d}_{name}.wav"
        if not out.exists():
            subprocess.run(
                [FFMPEG, "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono", "-t", f"{seconds:.3f}", str(out)],
                check=True,
                capture_output=True,
                text=True,
            )
        pieces.append(out)
        cursor += seconds

    for index, chunk in enumerate(chunks):
        src = DRAFT / f"{chunk['chunk_id']}.mp3"
        slowed = TMP / f"{index:04d}_{chunk['chunk_id']}_slow.wav"
        if not slowed.exists():
            subprocess.run(
                [
                    FFMPEG,
                    "-y",
                    "-i",
                    str(src),
                    "-af",
                    f"atempo={ATEMPO},loudnorm=I=-16:TP=-1.5:LRA=11",
                    "-ar",
                    "44100",
                    "-ac",
                    "1",
                    str(slowed),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
        if prev_section is not None and prev_section != chunk["section"]:
            add_silence(1.05, "section_gap")
        if index == 1:
            # BrandOpening plays after the flash-forward hook.
            add_silence(OPENING_SEC, "brand_opening_gap")
        start = cursor
        dur = duration(slowed)
        pieces.append(slowed)
        cursor += dur
        end = cursor
        timeline.append({**chunk, "start": round(start, 3), "end": round(end, 3), "duration_sec": round(dur, 3)})
        text = chunk["spoken_text"].lower()
        if "it's theft" in text or text == "guilty.":
            add_silence(1.15, "payoff_pause")
        else:
            add_silence(0.32, "micro_gap")
        prev_section = chunk["section"]

    # Keep a 12-minute premium frame without stretching speech into mud.
    total_with_endcard = cursor + ENDCARD_SEC
    if total_with_endcard < MIN_TOTAL_SEC:
        add_silence(MIN_TOTAL_SEC - total_with_endcard, "final_breath")

    concat_list = TMP / "concat.txt"
    concat_list.write_text("".join(f"file '{p.as_posix()}'\n" for p in pieces), encoding="utf-8")
    master = MASTER_DIR / "vc_master_v001.mp3"
    subprocess.run(
        [
            FFMPEG,
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_list),
            "-c:a",
            "libmp3lame",
            "-b:a",
            "192k",
            str(master),
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    timing = {
        "episode_id": EP,
        "revision": "v001",
        "narration_master": str(master),
        "atempo": ATEMPO,
        "opening_sec": OPENING_SEC,
        "endcard_sec": ENDCARD_SEC,
        "content_end_sec": round(cursor, 3),
        "total_with_endcard_sec": round(cursor + ENDCARD_SEC, 3),
        "scenes": timeline,
    }
    (EDIT_DIR / "timing.v001.json").write_text(json.dumps(timing, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    entries = []
    n = 1
    for item in timeline:
        lines = split_caption_lines(item["spoken_text"])
        words_total = max(1, sum(len(line.split()) for line in lines))
        pos = item["start"]
        dur = max(0.8, item["end"] - item["start"])
        for line in lines:
            frac = len(line.split()) / words_total
            line_dur = max(0.75, dur * frac)
            entries.append((n, pos, min(item["end"], pos + line_dur), line))
            pos += line_dur
            n += 1
    (EDIT_DIR / "captions.v001.srt").write_text(
        "\n".join(f"{i}\n{srt_ts(s)} --> {srt_ts(e)}\n{text}\n" for i, s, e, text in entries),
        encoding="utf-8",
    )
    print(master)
    print(EDIT_DIR / "timing.v001.json")
    print(EDIT_DIR / "captions.v001.srt")
    print(json.dumps({"content_end_sec": round(cursor, 2), "total_with_endcard_sec": round(cursor + ENDCARD_SEC, 2), "captions": len(entries)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
