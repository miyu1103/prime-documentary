#!/usr/bin/env python
"""Fill missing EP50 narration chunks with local Windows SAPI draft voice.

This is a no-network, no-paid fallback so the local edit/render pipeline can
continue when ElevenLabs chunks are incomplete. Existing paid/master chunks are
never overwritten.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-050-centralpark"
VOICE_PLAN = ROOT / "episodes" / EP / "06_audio" / "voice_plan.v001.json"
DRAFT = Path("E:/pd-media/episodes/PD-2026-050-centralpark/06_voice/draft")
VOICE = "Microsoft Zira Desktop"


def ps_quote(text: str) -> str:
    return "'" + text.replace("'", "''") + "'"


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


def synth(text: str, wav: Path, voice: str, rate: int) -> None:
    cmd = (
        "$ErrorActionPreference='Stop'; "
        "Add-Type -AssemblyName System.Speech; "
        "$s=New-Object System.Speech.Synthesis.SpeechSynthesizer; "
        f"$s.SelectVoice({ps_quote(voice)}); "
        f"$s.Rate={rate}; $s.Volume=100; "
        f"$s.SetOutputToWaveFile({ps_quote(str(wav))}); "
        f"$s.Speak({ps_quote(text)}); "
        "$s.Dispose();"
    )
    subprocess.run(["powershell", "-NoProfile", "-Command", cmd], check=True)


def convert(wav: Path, mp3: Path) -> None:
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-i", str(wav), "-c:a", "libmp3lame", "-b:a", "192k", str(mp3)],
        check=True,
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rate", type=int, default=-1)
    ap.add_argument("--voice", default=VOICE)
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    DRAFT.mkdir(parents=True, exist_ok=True)
    plan = json.loads(VOICE_PLAN.read_text(encoding="utf-8"))
    made = skipped = failed = 0
    for chunk in plan["chunks"]:
        cid = chunk["chunk_id"]
        mp3 = DRAFT / f"{cid}.mp3"
        meta = DRAFT / f"{cid}.json"
        if mp3.exists() and mp3.stat().st_size > 2048:
            skipped += 1
            continue
        if args.limit and made >= args.limit:
            break
        wav = DRAFT / f"{cid}.wav"
        try:
            synth(chunk["spoken_text"], wav, args.voice, args.rate)
            convert(wav, mp3)
            seconds = probe(mp3)
            meta.write_text(
                json.dumps(
                    {
                        "episode_id": EP,
                        "chunk_id": cid,
                        "section": chunk["section"],
                        "delivery": chunk["delivery"],
                        "idempotency_key": chunk["idempotency_key"],
                        "model_id": "windows_sapi",
                        "voice_id": args.voice,
                        "characters": len(chunk["spoken_text"]),
                        "seconds": seconds,
                        "estimated_cost_usd": 0.0,
                        "provider": "Windows System.Speech local draft",
                        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
                    },
                    indent=2,
                    ensure_ascii=False,
                )
                + "\n",
                encoding="utf-8",
            )
            made += 1
            if made % 25 == 0:
                print(f"[local-draft] made={made} skipped={skipped} last={cid}", flush=True)
        except Exception as exc:  # noqa: BLE001
            failed += 1
            print(f"[local-draft] FAIL {cid}: {exc}", flush=True)
        finally:
            wav.unlink(missing_ok=True)
    print(f"local_draft_voice made={made} skipped={skipped} failed={failed} draft={DRAFT}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
