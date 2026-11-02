#!/usr/bin/env python
"""Build a narration_index.v001.json (chunked spoken text) from a verified annotated script.

The ElevenLabs narration runner and gen_captions_forced.align_windowed both consume a
narration_index: an ordered list of spoken chunks (VC-NNNN) with section + text + word_count +
estimated_duration_seconds. This derives that index deterministically from
03_script/script.annotated.v001.json (chapters -> span_ids -> span.text), splitting each span into
sentence-level chunks of <= MAX_WORDS so windowed alignment stays tight.

Usage:
    python scripts/gen_narration_index.py --ep PD-2026-034-rolin
    python scripts/gen_narration_index.py --ep rolin --wpm 150
Writes episodes/<ep>/06_audio/narration_index.v001.json (estimated offsets; real offsets are
stamped by the narration runner after ElevenLabs generation).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EPISODES = ROOT / "episodes"
MAX_WORDS = 38          # cap per chunk (tight windows for drift-free alignment)
MIN_WORDS = 6           # avoid tiny fragments; merge forward if shorter


def resolve(ep: str) -> str:
    if (EPISODES / ep).is_dir():
        return ep
    hits = sorted(d.name for d in EPISODES.glob("PD-2026-*") if d.is_dir() and ep in d.name)
    if not hits:
        print(f"ERROR: no episode matching '{ep}'", file=sys.stderr); sys.exit(1)
    return hits[-1]


def split_sentences(text: str) -> list[str]:
    text = re.sub(r"\s+", " ", text.strip())
    # split on sentence enders while keeping them
    parts = re.split(r"(?<=[.!?])\s+", text)
    return [p.strip() for p in parts if p.strip()]


def chunk_text(text: str) -> list[str]:
    """Sentence-level chunks, each <= MAX_WORDS words; short trailing bits merge back."""
    out: list[str] = []
    for sent in split_sentences(text):
        words = sent.split()
        if len(words) <= MAX_WORDS:
            out.append(sent)
        else:  # long sentence: split on clause commas, then hard-wrap
            buf: list[str] = []
            for tok in sent.split():
                buf.append(tok)
                if len(buf) >= MAX_WORDS:
                    out.append(" ".join(buf)); buf = []
            if buf:
                out.append(" ".join(buf))
    # merge too-short chunks forward
    merged: list[str] = []
    for c in out:
        if merged and len(c.split()) < MIN_WORDS:
            merged[-1] = merged[-1] + " " + c
        else:
            merged.append(c)
    return merged


def main() -> int:
    ap = argparse.ArgumentParser(description="Build narration_index from an annotated script.")
    ap.add_argument("--ep", required=True)
    ap.add_argument("--wpm", type=float, default=150.0)
    a = ap.parse_args()
    ep = resolve(a.ep)
    epdir = EPISODES / ep
    ann_p = epdir / "03_script" / "script.annotated.v001.json"
    if not ann_p.exists():
        print(f"ERROR: {ann_p} not found", file=sys.stderr); return 1
    ann = json.loads(ann_p.read_text(encoding="utf-8"))
    spans = {s["span_id"]: s for s in ann.get("spans", [])}

    chunks: list[dict] = []
    n = 0
    total_words = 0
    for ch in ann.get("chapters", []):
        section = (ch.get("function") or ch.get("title") or ch.get("chapter_id") or "BODY").upper()
        for sid in ch.get("span_ids", []):
            sp = spans.get(sid)
            if not sp:
                continue
            text = (sp.get("text") or "").strip()
            if not text:
                continue
            for piece in chunk_text(text):
                wc = len(piece.split())
                n += 1
                total_words += wc
                chunks.append({
                    "voice_chunk_id": f"VC-{n:04d}",
                    "section": section,
                    "span_id": sid,
                    "text": piece,
                    "word_count": wc,
                    "estimated_duration_seconds": round(wc / a.wpm * 60.0, 3),
                })

    est_total = round(total_words / a.wpm * 60.0, 1)
    idx = {
        "schema_version": "1.0.0",
        "episode_id": ep,
        "revision": "v001",
        "language": ann.get("language", "en"),
        "mode": "chunked_verbatim",
        "provider": "elevenlabs",
        "voice_id": "(from .env ELEVENLABS_VOICE_ID at generation time)",
        "model_id": "eleven_multilingual_v2",
        "wpm_estimate": a.wpm,
        "source": "03_script/script.annotated.v001.json (chapters->spans)",
        "note": "Verbatim spoken text = caption source. Real per-chunk offsets stamped by the narration runner post-ElevenLabs.",
        "totals": {"chunks": len(chunks), "words": total_words, "estimated_seconds": est_total,
                   "estimated_minutes": round(est_total / 60.0, 2)},
        "chunks": chunks,
    }
    out = epdir / "06_audio" / "narration_index.v001.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(idx, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{ep}: {len(chunks)} chunks / {total_words} words / ~{idx['totals']['estimated_minutes']}min "
          f"@ {a.wpm}wpm -> {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
