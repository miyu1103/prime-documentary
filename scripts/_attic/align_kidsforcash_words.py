"""
scripts/align_kidsforcash_words.py
Role: caption-aligner — extract word-level timings from EP38 master narration.

Uses faster-whisper (medium.en, word_timestamps) on narration_master.mp3.
Keeps approved script text for display later; here we only capture word start/end times
(the sync backbone for captions + 〔CARD〕 number cards + motion word-sync).
Output: episodes/PD-2026-038-kidsforcash/06_audio/word_timings.v001.json
CPU int8 by default (avoid GPU contention with image gen). Deterministic-ish; no network.
"""
from __future__ import annotations
import json, sys, time
from pathlib import Path

try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

ROOT = Path(r"C:\Users\aab15\Documents\prime-documentary")
EP = "PD-2026-038-kidsforcash"
AUDIO = ROOT / "remotion" / "public" / "kidsforcash" / "narration_master.mp3"
OUT = ROOT / "episodes" / EP / "06_audio" / "word_timings.v001.json"
MODEL = "medium.en"


def main() -> int:
    if not AUDIO.exists():
        print(f"MISSING audio: {AUDIO}", file=sys.stderr); return 2
    from faster_whisper import WhisperModel
    t0 = time.time()
    print(f"loading {MODEL} (cpu/int8) ...")
    model = WhisperModel(MODEL, device="cpu", compute_type="int8")
    print(f"transcribing {AUDIO.name} with word timestamps ...")
    segments, info = model.transcribe(str(AUDIO), language="en", word_timestamps=True,
                                      vad_filter=True, beam_size=5)
    words = []
    seg_list = []
    for seg in segments:
        seg_list.append({"start": round(seg.start, 3), "end": round(seg.end, 3), "text": seg.text.strip()})
        for w in (seg.words or []):
            words.append({"word": w.word.strip(), "start": round(w.start, 3), "end": round(w.end, 3)})
        if len(words) % 100 < 5:
            print(f"  ... {len(words)} words, t={time.time()-t0:.0f}s")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    data = {"schema_version": "1", "episode_id": EP, "model": MODEL, "audio": str(AUDIO),
            "duration_sec": round(info.duration, 3), "word_count": len(words),
            "words": words, "segments": seg_list}
    tmp = OUT.with_suffix(".tmp"); tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    tmp.replace(OUT)
    print(f"\nWROTE {OUT}")
    print(f"words={len(words)} duration={info.duration:.1f}s elapsed={time.time()-t0:.0f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
