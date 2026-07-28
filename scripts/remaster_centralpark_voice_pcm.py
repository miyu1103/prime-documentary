#!/usr/bin/env python
"""Build an accurate EP50 narration master via PCM concat.

The ElevenLabs/local-draft chunks are MP3s. MP3 concat can produce timeline drift
between the calculated chunk offsets and the final master. This helper normalizes
each chunk to PCM WAV first, concatenates WAV files plus section silences, then
writes the master MP3 and narration_index with matching offsets.
"""
from __future__ import annotations

import argparse
import json
import math
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-050-centralpark"
VOICE_PLAN = ROOT / "episodes" / EP / "06_audio" / "voice_plan.v001.json"
INDEX = ROOT / "episodes" / EP / "06_audio" / "narration_index.v001.json"
DRAFT = Path("H:/pd-media/episodes/PD-2026-050-centralpark/06_voice/draft")
MASTER = Path("H:/pd-media/episodes/PD-2026-050-centralpark/06_voice/master/vc_master_v001.mp3")
CACHE = Path("H:/pd-media/episodes/PD-2026-050-centralpark/06_voice/_pcm_cache")
LOUDNORM = "loudnorm=I=-16:TP=-1.5:LRA=11"


def probe(path: Path) -> float:
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        capture_output=True,
        text=True,
    )
    try:
        return round(float(r.stdout.strip()), 3)
    except Exception:
        return 0.0


def convert_chunk(mp3: Path, wav: Path) -> None:
    if wav.exists() and wav.stat().st_size > 2048:
        return
    wav.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-i", str(mp3), "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", str(wav)],
        check=True,
    )


def silence(seconds: float) -> Path:
    key = round(seconds, 3)
    out = CACHE / f"_silence_{key:.3f}.wav"
    if out.exists() and out.stat().st_size > 1024:
        return out
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-v",
            "error",
            "-f",
            "lavfi",
            "-i",
            "anullsrc=r=48000:cl=stereo",
            "-t",
            f"{key:.3f}",
            "-c:a",
            "pcm_s16le",
            str(out),
        ],
        check=True,
    )
    return out


def q(path: Path) -> str:
    return path.as_posix().replace("'", "'\\''")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--gap-beat", type=float, default=0.0)
    ap.add_argument("--gap-section", type=float, default=1.0)
    args = ap.parse_args()

    plan = json.loads(VOICE_PLAN.read_text(encoding="utf-8"))
    chunks = plan["chunks"]
    CACHE.mkdir(parents=True, exist_ok=True)
    MASTER.parent.mkdir(parents=True, exist_ok=True)

    offsets: dict[str, dict] = {}
    cursor = 0.0
    concat_lines: list[str] = []
    for i, chunk in enumerate(chunks):
        cid = chunk["chunk_id"]
        mp3 = DRAFT / f"{cid}.mp3"
        if not mp3.is_file():
            raise SystemExit(f"missing chunk {mp3}")
        wav = CACHE / f"{cid}.wav"
        convert_chunk(mp3, wav)
        seconds = probe(wav)
        offsets[cid] = {"start": round(cursor, 3), "end": round(cursor + seconds, 3), "seconds": seconds}
        concat_lines.append(f"file '{q(wav)}'\n")
        cursor += seconds
        if i != len(chunks) - 1:
            if chunk["section"] != chunks[i + 1]["section"]:
                gap = args.gap_section
            else:
                gap = args.gap_beat
            if gap > 0:
                sil = silence(gap)
                concat_lines.append(f"file '{q(sil)}'\n")
                cursor += gap
        if (i + 1) % 100 == 0:
            print(f"[pcm] prepared {i + 1}/{len(chunks)} cursor={cursor:.1f}s", flush=True)

    concat = CACHE / "_concat_pcm.txt"
    concat.write_text("".join(concat_lines), encoding="utf-8")
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-v",
            "error",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat),
            "-af",
            LOUDNORM,
            "-c:a",
            "libmp3lame",
            "-b:a",
            "192k",
            str(MASTER),
        ],
        check=True,
    )
    total = probe(MASTER)
    words = sum(len(c["spoken_text"].split()) for c in chunks)
    index = {
        "schema_version": "centralpark_narration.v1",
        "episode_id": EP,
        "revision": "v001",
        "is_stub": False,
        "provider": "mixed: existing ElevenLabs chunks plus Windows System.Speech local draft fills",
        "source_script": "episodes/_planning/EP50_centralpark_script.en.v001.md",
        "master": f"artifact://episodes/{EP}/06_voice/master/vc_master_v001.mp3",
        "total_seconds": total,
        "totals": {
            "chunks": len(chunks),
            "words": words,
            "speech_seconds": round(sum(o["seconds"] for o in offsets.values()), 3),
            "measured_seconds": total,
            "measured_minutes": round(total / 60, 2),
            "measured_wpm": round(words / (sum(o["seconds"] for o in offsets.values()) / 60), 1),
        },
        "chunks": [
            {
                "voice_chunk_id": c["chunk_id"],
                "id": c["chunk_id"],
                "section": c["section"],
                "text": c["spoken_text"],
                "spoken_text": c["spoken_text"],
                "word_count": len(c["spoken_text"].split()),
                "start": offsets[c["chunk_id"]]["start"],
                "end": offsets[c["chunk_id"]]["end"],
                "seconds": offsets[c["chunk_id"]]["seconds"],
                "duration": offsets[c["chunk_id"]]["seconds"],
            }
            for c in chunks
        ],
        "provenance": {
            "producer": "scripts/remaster_centralpark_voice_pcm.py",
            "estimated_new_cost_usd": 0.0,
            "gap_beat_seconds": args.gap_beat,
            "gap_section_seconds": args.gap_section,
            "loudnorm": LOUDNORM,
            "master_path_expected": str(MASTER),
            "stamped_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        },
    }
    INDEX.write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    frames = round(8 * 30) + round(3.5 * 30) + math.ceil(total * 30) + round(9 * 30)
    print(f"PCM_MASTER total={total:.3f}s minutes={total/60:.2f} frames={frames} master={MASTER}")
    print(f"INDEX last_end={index['chunks'][-1]['end']:.3f}s index={INDEX}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
