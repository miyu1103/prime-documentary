#!/usr/bin/env python3
"""Generate EP39 captions from the narration index (real per-chunk audio timings),
split at phrase boundaries so no cue breaks mid-phrase / ends on a function word.
Emits captions.final.v001.json (cues for build_frazier_film.py) + .srt (for the gate).

Alignment: each cue's [start,end] is interpolated by word position inside its source
chunk's measured [start,end] window -> real-audio aligned, NOT an even grid."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fix_caption_dangling import NO_DANGLE_END  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
EPDIR = ROOT / "episodes/PD-2026-039-frazier"
INDEX = EPDIR / "06_audio/narration_index.v001.json"
OUT_JSON = EPDIR / "08_edit/captions.final.v001.json"
OUT_SRT = EPDIR / "08_edit/captions.final.v001.srt"

MAX_WORDS = 11
MAX_CHARS = 84
MIN_WORDS = 3
BREAK_PUNCT = set(",.;:!?—–")  # comma . ; : ! ? em-dash en-dash


def last_word(s: str) -> str:
    w = re.findall(r"[A-Za-z']+", s)
    return w[-1].lower() if w else ""


def normalize_tokens(text: str) -> list[str]:
    toks = text.split()
    out: list[str] = []
    for t in toks:
        if t in ("—", "–", "-") and out:  # attach standalone dash to previous word
            out[-1] = out[-1] + " " + t
        else:
            out.append(t)
    return out


def split_chunk(text: str) -> list[tuple[int, int]]:
    """Return list of (start_word, end_word) exclusive ranges over normalized tokens."""
    toks = normalize_tokens(text)
    n = len(toks)
    result: list[tuple[int, int]] = []
    cur_start = 0
    cur: list[str] = []
    for idx in range(n):
        cur.append(toks[idx])
        so_far = " ".join(cur)
        wc = len(cur)
        at_break = so_far[-1] in BREAK_PUNCT
        overflow = wc >= MAX_WORDS or len(so_far) >= MAX_CHARS
        if at_break and wc >= MIN_WORDS + 1 and (overflow or len(so_far) >= MAX_CHARS - 20):
            result.append((cur_start, idx + 1))
            cur, cur_start = [], idx + 1
        elif overflow:
            # forced break: cut at the latest safe boundary whose preceding word is NOT a
            # function word (-> a benign "soft" split, never a hard mid-phrase break).
            safe = None
            for j in range(len(cur) - 1, MIN_WORDS - 1, -1):
                # match the gate: judge the LAST ALPHA WORD of the whole earlier cue,
                # so a cue ending "...by 2026" is rejected (last alpha word "by").
                if last_word(" ".join(cur[:j])) not in NO_DANGLE_END:
                    safe = j
                    break
            if safe is None:
                safe = len(cur)
            result.append((cur_start, cur_start + safe))
            cur = toks[cur_start + safe: idx + 1]
            cur_start = cur_start + safe
    if cur:
        if result and len(cur) < MIN_WORDS:
            s, _ = result[-1]
            result[-1] = (s, n)
        else:
            result.append((cur_start, n))
    # final safety merge: absorb any <MIN_WORDS cue that is not sentence-terminal into neighbour
    merged: list[tuple[int, int]] = []
    for s, e in result:
        frag = " ".join(toks[s:e])
        words = re.findall(r"[A-Za-z0-9']+", frag)
        terminal = frag[-1:] in ".?!—" and frag[:1].isupper()
        if len(words) < MIN_WORDS and not terminal and merged:
            ps, _ = merged[-1]
            merged[-1] = (ps, e)
        else:
            merged.append((s, e))
    return merged


def srt_time(t: float) -> str:
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def main() -> int:
    idx = json.loads(INDEX.read_text(encoding="utf-8"))
    cues: list[dict] = []
    for ch in idx["chunks"]:
        text = ch["text"].strip()
        toks = normalize_tokens(text)
        n = len(toks)
        cs, ce = float(ch["start"]), float(ch["end"])
        span = ce - cs
        for (a, b) in split_chunk(text):
            frac_a = a / n
            frac_b = b / n
            start = round(cs + frac_a * span, 3)
            end = round(cs + frac_b * span, 3)
            ctext = " ".join(toks[a:b]).strip()
            cues.append({"start": start, "end": end, "text": ctext})

    # enforce monotonic non-overlapping ordering
    for i in range(1, len(cues)):
        if cues[i]["start"] < cues[i - 1]["end"]:
            cues[i]["start"] = cues[i - 1]["end"]
        if cues[i]["end"] <= cues[i]["start"]:
            cues[i]["end"] = round(cues[i]["start"] + 0.4, 3)

    payload = {
        "episode_id": "PD-2026-039-frazier",
        "revision": "v001",
        "source": "narration_index.v001.json",
        "fps": 30,
        "cues": cues,
    }
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = []
    for i, c in enumerate(cues, 1):
        lines.append(str(i))
        lines.append(f"{srt_time(c['start'])} --> {srt_time(c['end'])}")
        lines.append(c["text"])
        lines.append("")
    OUT_SRT.write_text("\n".join(lines), encoding="utf-8")

    print(f"wrote {OUT_JSON}")
    print(f"wrote {OUT_SRT}")
    print(f"cues={len(cues)} last_end={cues[-1]['end']}")
    wc = [len(re.findall(r"[A-Za-z0-9']+", c['text'])) for c in cues]
    print(f"words/cue min={min(wc)} max={max(wc)} mean={sum(wc)/len(wc):.1f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
