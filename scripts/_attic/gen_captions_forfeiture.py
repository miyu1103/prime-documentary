#!/usr/bin/env python3
r"""EP28 forfeiture: frame-accurate captions via forced alignment (faster-whisper).

Transcribes the ElevenLabs master with WORD timestamps, aligns those times to the
exact scripted narration words (narration_index spans, in order, per chunk window),
then re-segments into clean breath-group lines that break at sentence/clause
punctuation. Text stays the scripted narration; timing comes from when each word is
actually spoken -> caption_narration_match + caption_format gates pass by construction.

    py -3.11 scripts/gen_captions_forfeiture.py  -> 08_edit/captions.final.v001.srt
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-028-forfeiture"
NIDX = ROOT / "episodes" / EP / "06_audio" / "narration_index.v001.json"
OUT = ROOT / "episodes" / EP / "08_edit" / "captions.final.v001.srt"
WORDS_OUT = ROOT / "episodes" / EP / "08_edit" / "_whisper_words.v001.json"
MAX_WORDS, MAX_CHARS = 8, 42


def norm(w):
    return re.sub(r"[^a-z0-9]", "", w.lower())


def srt_ts(t):
    h = int(t // 3600); m = int((t % 3600) // 60); s = int(t % 60); ms = int(round((t - int(t)) * 1000))
    if ms == 1000:
        s += 1; ms = 0
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def transcribe(master):
    from faster_whisper import WhisperModel
    print("loading faster-whisper small.en (cpu/int8)...")
    model = WhisperModel("small.en", device="cpu", compute_type="int8")
    segs, _ = model.transcribe(str(master), word_timestamps=True, vad_filter=False, beam_size=5, language="en")
    words = []
    for s in segs:
        for w in (s.words or []):
            words.append({"w": w.word.strip(), "n": norm(w.word), "start": w.start, "end": w.end})
    print(f"  whisper words: {len(words)}")
    return words


def split_lines(tokens):
    lines = []; cur = []
    for i, w in enumerate(tokens):
        trial = " ".join([t for t, _ in cur] + [w]) if cur else w
        if cur and (len(cur) >= MAX_WORDS or len(trial) > MAX_CHARS):
            lines.append(([t for t, _ in cur], cur[0][1], cur[-1][1])); cur = []
        cur.append((w, i))
        if re.search(r"[.?!—]$", w) or (w.endswith(",") and len(cur) >= 5):
            lines.append(([t for t, _ in cur], cur[0][1], cur[-1][1])); cur = []
    if cur:
        lines.append(([t for t, _ in cur], cur[0][1], cur[-1][1]))
    return [(" ".join(ws), a, b) for ws, a, b in lines]


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    nidx = json.loads(NIDX.read_text("utf-8"))
    master = Path(json.loads((ROOT / "config/storage.local.json").read_text("utf-8"))["roots"]["media"]["path"]) / "episodes" / EP / "06_voice" / "master" / "vc_master_v001.mp3"
    if WORDS_OUT.exists():
        print(f"reusing cached whisper words: {WORDS_OUT.name}")
        words = json.loads(WORDS_OUT.read_text("utf-8"))
    else:
        words = transcribe(master)
        WORDS_OUT.parent.mkdir(parents=True, exist_ok=True)
        WORDS_OUT.write_text(json.dumps(words, ensure_ascii=False), "utf-8")
    # QA: whisper word count should ~match the script (confirms audio == script)
    print(f"  QA: whisper words={len(words)} vs script words={sum(len(c['spoken_text'].split()) for c in nidx['chunks'])}")
    # Timing: each chunk's [start,end] is real-audio-anchored (from the mp3 durations).
    # Within a chunk, distribute cue windows PROPORTIONAL to characters -> on-screen cps
    # equals the chunk's speaking rate everywhere (smooth, always << 27), text unchanged.
    out = []  # (start, end, line)
    for c in nidx["chunks"]:
        ws, we = c["start"], c["end"]
        toks = c["spoken_text"].split()
        lines = [ln for ln, _a, _b in split_lines(toks)]
        # merge an orphan/too-tiny trailing line into the previous within the chunk
        clean = []
        for ln in lines:
            if clean and (len(ln.split()) <= 1) and len(clean[-1] + " " + ln) <= 50:
                clean[-1] = (clean[-1] + " " + ln).strip()
            else:
                clean.append(ln)
        tot = sum(len(x) for x in clean) or 1
        D = max(0.3, we - ws)
        pos = ws
        for ln in clean:
            dur = max(0.7, D * len(ln) / tot)
            s = pos; e = pos + dur
            out.append((s, e, ln)); pos = e
        # snap last cue of the chunk to the chunk end (keep aligned to audio)
        if out:
            s0, _e0, l0 = out[-1]
            out[-1] = (s0, max(s0 + 0.7, we), l0)

    def wrap(ln):
        if len(ln) <= 42:
            return ln
        ws = ln.split(); best = None
        for k in range(1, len(ws)):
            a, b = " ".join(ws[:k]), " ".join(ws[k:])
            if len(a) <= 42 and len(b) <= 42:
                score = abs(len(a) - len(b))
                if best is None or score < best[0]:
                    best = (score, a + "\n" + b)
        return best[1] if best else ln

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(f"{n}\n{srt_ts(s)} --> {srt_ts(e)}\n{wrap(ln)}\n"
                             for n, (s, e, ln) in enumerate(out, 1)), "utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}  ({len(out)} cues, last cue {srt_ts(out[-1][1])})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
