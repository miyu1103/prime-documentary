#!/usr/bin/env python3
r"""Regenerate captions.final.v001.srt for PD-2026-035-hinders so every narration
chunk window is >=80% covered (verify_caption_coverage) while staying within the
caption_format limits (<=2 lines, <=42 chars/line, <=7s cue, <=27 cps).

Method: for each narration chunk [start,end] we split its verbatim text into
readable cues (word-packed, <=2 lines <=42 chars, char budget bounded so cue
duration <=7s at the chunk's own reading rate) and lay those cues CONTIGUOUSLY
across the whole chunk window, proportional to each cue's character length. The
union of the cues therefore fills the window (coverage ~100% per chunk), with no
inter-cue gaps inside a chunk. Cues never leave the chunk window, so the natural
silence between chunks stays uncaptioned by design. Text is taken verbatim from
narration_index (no fabrication / summarisation).
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EP = ROOT / "episodes" / "PD-2026-035-hinders"
INDEX = EP / "06_audio" / "narration_index.v001.json"
OUT = EP / "08_edit" / "captions.final.v001.srt"

MAX_LINE = 42          # chars per line (format floor is 42)
MAX_LINES = 2
CPS_FOR_BUDGET = 6.6   # cue_chars <= CPS_FOR_BUDGET * chunk_cps keeps cue <=~7s


def wrap_two_lines(words: list[str]) -> list[str] | None:
    """Return <=2 lines each <=MAX_LINE from words, or None if impossible."""
    line1: list[str] = []
    for i, w in enumerate(words):
        cand = (" ".join(line1 + [w])).strip()
        if len(cand) <= MAX_LINE:
            line1.append(w)
        else:
            rest = words[i:]
            line2 = " ".join(rest)
            if len(line2) <= MAX_LINE and line1:
                return [" ".join(line1), line2]
            return None
    return [" ".join(line1)] if line1 else None


def pack_cues(text: str, max_chars: int) -> list[str]:
    """Greedily pack words into cues; each cue fits <=2 lines <=42 and <=max_chars."""
    words = text.split()
    cues: list[str] = []
    cur: list[str] = []
    for w in words:
        trial = cur + [w]
        joined = " ".join(trial)
        if len(joined) <= max_chars and wrap_two_lines(trial) is not None:
            cur = trial
        else:
            if cur:
                cues.append(" ".join(cur))
            cur = [w]
            # a single word longer than budget/line: emit alone (rare, none here)
            if wrap_two_lines(cur) is None:
                cues.append(" ".join(cur))
                cur = []
    if cur:
        cues.append(" ".join(cur))
    return cues


def ts(sec: float) -> str:
    if sec < 0:
        sec = 0.0
    ms = int(round(sec * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def main() -> int:
    data = json.loads(INDEX.read_text(encoding="utf-8"))
    chunks = sorted(data["chunks"], key=lambda c: c["start"])

    entries: list[tuple[float, float, str]] = []
    for c in chunks:
        ws, we = float(c["start"]), float(c["end"])
        dur = we - ws
        text = " ".join(str(c["text"]).split())
        if dur <= 0 or not text:
            continue
        cps = len(text) / dur
        budget = min(2 * MAX_LINE, max(24, int(CPS_FOR_BUDGET * cps)))
        cues = pack_cues(text, budget)
        # distribute the window proportional to char length, contiguously
        total = sum(len(x) for x in cues) or 1
        acc = ws
        for i, ct in enumerate(cues):
            frac = len(ct) / total
            end = we if i == len(cues) - 1 else acc + dur * frac
            entries.append((acc, end, ct))
            acc = end

    lines: list[str] = []
    for i, (a, b, ct) in enumerate(entries, 1):
        wrapped = wrap_two_lines(ct.split())
        body = "\n".join(wrapped) if wrapped else ct
        lines.append(f"{i}\n{ts(a)} --> {ts(b)}\n{body}\n")
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {OUT}  ({len(entries)} cues from {len(chunks)} chunks)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
