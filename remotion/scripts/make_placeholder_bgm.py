#!/usr/bin/env python3
"""Generate a $0 placeholder ambient BGM WAV (pure stdlib, no paid asset).

Writes remotion/public/bgm_placeholder.wav — a soft low drone for style tests only.
This is a PLACEHOLDER; real music comes from the Suno reuse library (decisions/0002 §C).
The file is git-ignored (remotion/public/). Run from anywhere:
    py remotion/scripts/make_placeholder_bgm.py
"""
from __future__ import annotations

import math
import struct
import wave
from pathlib import Path

RATE = 22050
SECONDS = 60
OUT = Path(__file__).resolve().parents[1] / "public" / "bgm_placeholder.wav"

# Soft low pad: a few quiet detuned sines + slow tremolo. Low amplitude (headroom for VO).
TONES = (110.0, 146.83, 220.0)  # A2, D3, A3
AMP = 0.16


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    n = RATE * SECONDS
    frames = bytearray()
    for i in range(n):
        t = i / RATE
        trem = 0.85 + 0.15 * math.sin(2 * math.pi * 0.1 * t)  # slow swell
        s = sum(math.sin(2 * math.pi * f * t) for f in TONES) / len(TONES)
        # gentle fade in/out over 2s
        fade = min(1.0, t / 2.0, (SECONDS - t) / 2.0)
        val = int(max(-1.0, min(1.0, s * AMP * trem * fade)) * 32767)
        frames += struct.pack("<h", val)
    with wave.open(str(OUT), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(bytes(frames))
    print(f"wrote {OUT} ({OUT.stat().st_size // 1024} KB, {SECONDS}s mono {RATE}Hz)")


if __name__ == "__main__":
    main()
