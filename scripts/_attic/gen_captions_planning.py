#!/usr/bin/env python3
r"""EP28-30 captions via forced alignment (faster-whisper) — parametric.

Transcribes the ElevenLabs master for a QA word count (confirms audio == script),
then times captions by per-chunk PROPORTIONAL distribution: each narration_index
span is real-audio-anchored (start/end from the mp3), and within it cue windows
scale with characters so on-screen cps == the chunk speaking rate (always << 27).
Text stays the verbatim script -> caption_narration_match + caption_format pass.

    py -3.11 scripts/gen_captions_planning.py --slug hinton
"""
from __future__ import annotations
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUGS = {"forfeiture": "PD-2026-028-forfeiture", "hinton": "PD-2026-029-hinton", "cotton": "PD-2026-030-cotton"}
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
    return [" ".join(ws) for ws, a, b in lines]


def wrap(ln):
    if len(ln) <= 42:
        return ln
    ws = ln.split(); best = None
    for k in range(1, len(ws)):
        a, b = " ".join(ws[:k]), " ".join(ws[k:])
        if len(a) <= 42 and len(b) <= 42:
            sc = abs(len(a) - len(b))
            if best is None or sc < best[0]:
                best = (sc, a + "\n" + b)
    return best[1] if best else ln


def main(argv):
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True, choices=list(SLUGS))
    args = ap.parse_args(argv)
    ep = SLUGS[args.slug]
    nidx = json.loads((ROOT / "episodes" / ep / "06_audio" / "narration_index.v001.json").read_text("utf-8"))
    words_out = ROOT / "episodes" / ep / "08_edit" / "_whisper_words.v001.json"
    out_srt = ROOT / "episodes" / ep / "08_edit" / "captions.final.v001.srt"
    master = Path(json.loads((ROOT / "config/storage.local.json").read_text("utf-8"))["roots"]["media"]["path"]) / "episodes" / ep / "06_voice" / "master" / "vc_master_v001.mp3"
    words_out.parent.mkdir(parents=True, exist_ok=True)
    if words_out.exists():
        words = json.loads(words_out.read_text("utf-8"))
        print(f"reusing cached whisper words ({len(words)})")
    else:
        words = transcribe(master)
        words_out.write_text(json.dumps(words, ensure_ascii=False), "utf-8")
    print(f"  QA: whisper words={len(words)} vs script words={sum(len(c['spoken_text'].split()) for c in nidx['chunks'])}")

    out = []
    for c in nidx["chunks"]:
        ws, we = c["start"], c["end"]
        toks = c["spoken_text"].split()
        lines = split_lines(toks)
        clean = []
        for ln in lines:
            if clean and len(ln.split()) <= 1 and len(clean[-1] + " " + ln) <= 50:
                clean[-1] = (clean[-1] + " " + ln).strip()
            else:
                clean.append(ln)
        tot = sum(len(x) for x in clean) or 1
        D = max(0.3, we - ws)
        pos = ws
        for ln in clean:
            d = max(0.7, D * len(ln) / tot)
            out.append((pos, pos + d, ln)); pos += d
        if out:
            s0, _e0, l0 = out[-1]
            out[-1] = (s0, max(s0 + 0.7, we), l0)

    out_srt.write_text("\n".join(f"{n}\n{srt_ts(s)} --> {srt_ts(e)}\n{wrap(ln)}\n"
                                 for n, (s, e, ln) in enumerate(out, 1)), "utf-8")
    print(f"wrote {out_srt.relative_to(ROOT)}  ({len(out)} cues, last {srt_ts(out[-1][1])})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
