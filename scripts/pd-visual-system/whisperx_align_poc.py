#!/usr/bin/env python
"""PD Visual System — P07 WhisperX word-timestamp PoC.

Produces WORD-level timestamps for the narration so on-screen reveals (core-5,
KineticCaptions) can fire on a spoken word. The SCRIPT is source of truth — this
POC records ASR words + times and flags numbers/years/statutes/case-numbers/
names/places/courts as requires_review (a wrong onset on those = a factually
mis-timed graphic). It does NOT overwrite the script.

Run with the ISOLATED venv (NOT the Remotion/global env):
  D:\\PD_AI_Tools\\WhisperX\\.venv\\Scripts\\python.exe \
    scripts/pd-visual-system/whisperx_align_poc.py --ep PD-2026-009-timbs

Output (immutable revision):
  episodes/<ep>/08_edit/whisperx/whisperx_words.v001.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

# review-flag regexes (per owner brief §2: money/year/statute/case/name/place/court)
RE_MONEY = re.compile(r"\$[\d,]+(\.\d+)?|\b(dollars?|cents?|thousand|million|billion)\b", re.I)
RE_YEAR = re.compile(r"\b(1[6-9]\d\d|20\d\d)\b")
RE_STATUTE = re.compile(r"§|\bU\.?S\.?C\.?\b|\bAmendment\b|\bSection\b|\bclause\b", re.I)
RE_CASE = re.compile(r"\bNo\.\s?\d|\b\d{2}-\d{3,4}\b|\b\d+\s+U\.?S\.?\s+\d+\b|\bv\.?\b", re.I)
RE_COURT = re.compile(r"\b(Supreme Court|Court of Appeals|District Court|Circuit|SCOTUS)\b", re.I)
NUM_WORD = re.compile(r"\b(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
                      r"thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|"
                      r"thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand|million)\b", re.I)


def flags_for(word: str) -> list[str]:
    r = []
    if RE_MONEY.search(word):
        r.append("money")
    if RE_YEAR.search(word):
        r.append("year")
    if RE_STATUTE.search(word):
        r.append("statute")
    if RE_CASE.search(word):
        r.append("case_number")
    if RE_COURT.search(word):
        r.append("court")
    if NUM_WORD.search(word):
        r.append("number")
    # capitalized mid-token proper-noun heuristic (name/place) — regex tier only
    if word[:1].isupper() and word.lower() not in {"the", "a", "an", "in", "on", "of", "and", "but"}:
        r.append("proper_noun_maybe")
    return r


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for c in iter(lambda: fh.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ep", default="PD-2026-009-timbs")
    ap.add_argument("--audio", default="remotion/public/timbs/timbs_final_mix_v001.mp3")
    ap.add_argument("--model", default="medium.en")  # matches repo gen_captions_forced.py
    ap.add_argument("--out", default=None)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    audio = Path(a.audio)
    if not audio.exists():
        print(f"missing audio: {audio}", file=sys.stderr)
        return 2
    out = Path(a.out) if a.out else Path(f"episodes/{a.ep}/08_edit/whisperx/whisperx_words.v001.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    if a.dry_run:
        print(f"[dry-run] would align {audio} with whisperx {a.model} -> {out}")
        return 0

    # NOTE: word timing via faster-whisper (ctranslate2) — the same ASR family the
    # repo's gen_captions_forced.py uses. Robust vs WhisperX's torch/transformers
    # dependency conflict on this machine. wav2vec2 phoneme-align is a later upgrade.
    from faster_whisper import WhisperModel
    try:
        model = WhisperModel(a.model, device="cuda", compute_type="float16")
        device = "cuda"
    except Exception as e:
        print(f"cuda unavailable ({type(e).__name__}); falling back to cpu int8")
        model = WhisperModel(a.model, device="cpu", compute_type="int8")
        device = "cpu"
    print(f"faster-whisper device={device} model={a.model}")

    segments, info = model.transcribe(str(audio), language="en", word_timestamps=True,
                                      vad_filter=True, beam_size=5)

    words = []
    i = 0
    for seg in segments:
        for w in (seg.words or []):
            token = str(w.word).strip()
            if not token:
                continue
            reasons = flags_for(token)
            words.append({
                "i": i, "word": token,
                "start": round(float(w.start), 3),
                "end": round(float(w.end), 3),
                "confidence": round(float(w.probability), 3),
                "requires_review": bool(reasons),
                "review_reasons": reasons,
            })
            i += 1
    print(f"transcribed segments -> {len(words)} words")

    payload = {
        "schema_version": "1.0.0",
        "episode_id": a.ep,
        "audio_uri": f"artifact://{a.audio}",
        "audio_sha256": sha256(audio),
        "model": {"asr": a.model, "engine": "faster-whisper (ctranslate2)", "word_timestamps": True, "device": device},
        "note": "SCRIPT is source of truth; ASR words are for TIMING only. review-flagged tokens need human onset confirmation before pinning a reveal.",
        "word_count": len(words),
        "review_count": sum(1 for w in words if w["requires_review"]),
        "words": words,
    }
    tmp = out.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(payload, indent=1, ensure_ascii=False), encoding="utf-8")
    tmp.replace(out)
    print(f"wrote {out}  words={len(words)} review={payload['review_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
