#!/usr/bin/env python3
r"""EP37 Florence: frame-accurate breath-unit captions from the scripted narration.

SCRIPT is source of truth for TEXT (03_script/script.en.v001.md); florence_words.json
(faster-whisper word + start/end) is source of truth for TIMING only. We align the
scripted word sequence to the ASR word stream (order-preserving, difflib) so every
scripted word gets its real spoken onset; unmatched words are interpolated. Text is
then re-segmented into clean breath-group lines that break at sentence/clause
punctuation and never end on a dangling function word. Each cue is pulled ~0.60 s
early (lead), kept monotonic / non-overlapping, held to a comfortable reading speed,
and clamped inside the narration duration.

    py -3.11 scripts/gen_captions_florence.py
      -> episodes/PD-2026-037-florence/04_scenes/captions.final.v001.srt
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-037-florence"
SCRIPT = ROOT / "episodes" / EP / "03_script" / "script.en.v001.md"
WORDS = ROOT / "remotion" / "public" / "florence" / "florence_words.json"
OUT = ROOT / "episodes" / EP / "04_scenes" / "captions.final.v001.srt"

DURATION = 542.98          # narration master duration (s) — hard clamp for every cue
LEAD = 0.60                # pull each cue ~0.60 s earlier than its first spoken word
MAX_WORDS, MAX_CHARS = 7, 42
MIN_DUR = 0.9
CPS_TARGET = 19.0          # extend ends toward this reading speed
CPS_MERGE = 22.0           # merge a cue faster than this into the next (if it still fits)
CPS_CAP = 24.0             # final hard cap: extend end (small overlap allowed) to reach it
WRAP_MAX = 46              # max chars per wrapped SRT line

# weak words a caption line must not END on (pull them onto the next line)
STOP = {
    "a", "an", "the", "of", "to", "in", "on", "at", "by", "for", "from", "into", "with",
    "as", "than", "and", "or", "but", "nor", "so", "yet", "is", "are", "was", "were",
    "be", "been", "being", "am", "has", "have", "had", "do", "does", "did", "will",
    "would", "can", "could", "shall", "should", "may", "might", "must", "his", "her",
    "its", "their", "my", "your", "our", "this", "that", "these", "those", "it", "he",
    "she", "we", "they", "you", "i", "not", "no", "if", "then", "when", "where", "which",
    "who", "whose", "whom", "up", "out", "off", "about", "because", "while", "though",
}


def norm(w: str) -> str:
    return re.sub(r"[^a-z0-9]", "", w.lower())


def srt_ts(t: float) -> str:
    t = max(0.0, t)
    h = int(t // 3600); m = int((t % 3600) // 60); s = int(t % 60)
    ms = int(round((t - int(t)) * 1000))
    if ms == 1000:
        s += 1; ms = 0
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def extract_narration(md: str) -> list[str]:
    """Scripted narration tokens in spoken order: HOOK + OPENING + ACT I-IV body only.
    Strips section markers (**[...]**), inline [beat] cues, italic/asterisk markup, and
    everything from the first horizontal rule after the body (brush-up passes, claim map)."""
    body = md.split("\n## Three brush-up", 1)[0]
    # drop the leading front-matter block (everything up to the first '---')
    parts = body.split("\n---\n")
    body = parts[1] if len(parts) > 1 else body
    tokens: list[str] = []
    for line in body.splitlines():
        line = line.strip()
        if not line or line == "---":
            continue
        if line.startswith("**["):                            # act/section marker on its own line
            continue
        line = re.sub(r"\[beat\]", " ", line)                 # leading/inline beat cue (keep narration)
        line = line.replace("*", "")                          # italic markup
        line = re.sub(r"\s+", " ", line).strip()
        if line:
            tokens.extend(line.split())
    return tokens


def align(script_toks: list[str], asr: list[dict]) -> tuple[list[float], list[float], list[str]]:
    """Return (starts, ends, unmatched) — spoken onset/offset for each scripted token via an
    order-preserving difflib match on normalized text; unmatched tokens are interpolated."""
    import difflib
    s_norm = [norm(t) for t in script_toks]
    a_norm = [w["n"] for w in asr]
    starts: list[float | None] = [None] * len(script_toks)
    ends: list[float | None] = [None] * len(script_toks)
    sm = difflib.SequenceMatcher(a=s_norm, b=a_norm, autojunk=False)
    for i, j, n in sm.get_matching_blocks():
        for k in range(n):
            starts[i + k] = asr[j + k]["start"]
            ends[i + k] = asr[j + k]["end"]
    unmatched = [script_toks[i] for i in range(len(script_toks)) if starts[i] is None]
    # interpolate any unmatched token between its nearest matched neighbours
    last = 0.0
    nxt_cache: dict[int, float] = {}
    for i in range(len(script_toks)):
        if starts[i] is not None:
            last = ends[i]
            continue
        # find next matched start
        j = i + 1
        while j < len(script_toks) and starts[j] is None:
            j += 1
        nxt = starts[j] if j < len(script_toks) else DURATION
        # count run to distribute evenly
        run_start = i
        while run_start > 0 and starts[run_start - 1] is None:
            run_start -= 1
        run_len = j - run_start
        pos = i - run_start
        span = max(0.0, nxt - last)
        s = last + span * (pos + 0.5) / (run_len + 1)
        starts[i] = s
        ends[i] = s + 0.25
    return [float(x) for x in starts], [float(x) for x in ends], unmatched


def split_lines(tokens: list[str]) -> list[tuple[list[str], int, int]]:
    """Break scripted tokens into breath-group lines at sentence/clause punctuation; on a
    length wrap, back up over trailing weak words so a line never ends on a/the/on/and…."""
    lines: list[tuple[list[str], int, int]] = []
    cur: list[tuple[str, int]] = []

    def flush(seq: list[tuple[str, int]]) -> None:
        if seq:
            lines.append(([t for t, _ in seq], seq[0][1], seq[-1][1]))

    for i, w in enumerate(tokens):
        cur.append((w, i))
        wl = len(" ".join(t for t, _ in cur))
        # hard clause/sentence boundary — always a clean break
        if re.search(r"[.?!—:;]$", w) or (w.endswith(",") and len(cur) >= 4):
            flush(cur); cur = []; continue
        if len(cur) >= MAX_WORDS or wl >= MAX_CHARS:
            cut = len(cur) - 1
            while cut > 0 and norm(cur[cut][0]) in STOP:
                cut -= 1
            if cut <= 0:
                cut = len(cur) - 1  # all-weak line: give up rather than loop
            head = cur[:cut + 1]; cur = cur[cut + 1:]
            flush(head)
    flush(cur)
    return lines


def wrap2(t: str, maxc: int = WRAP_MAX) -> str:
    """Balance a long cue onto at most two lines at a space near the midpoint."""
    if len(t) <= maxc:
        return t
    words = t.split()
    half = len(t) / 2
    for k in range(1, len(words)):
        if len(" ".join(words[:k])) >= half:
            for kk in (k, k - 1, k + 1):
                if 1 <= kk < len(words):
                    a = " ".join(words[:kk]); b = " ".join(words[kk:])
                    if len(a) <= 50 and len(b) <= 50:
                        return a + "\n" + b
            break
    return t


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    toks = extract_narration(SCRIPT.read_text("utf-8"))
    asr = json.loads(WORDS.read_text("utf-8"))["words"]
    for w in asr:
        w["n"] = norm(w["word"])
    starts, ends, unmatched = align(toks, asr)
    print(f"scripted tokens={len(toks)}  asr words={len(asr)}  unmatched={len(unmatched)}")

    # build cues from breath-group lines
    cues: list[list] = []  # [start, end, text]
    for words, a, b in split_lines(toks):
        text = re.sub(r"\s+([.,;:?!])", r"\1", " ".join(words)).strip()
        s = starts[a] - LEAD
        e = ends[b]
        if e <= s:
            e = s + MIN_DUR
        cues.append([s, e, text])

    # monotonic, no overlap; the lead may never push a cue before the previous one
    for i in range(len(cues)):
        if i > 0 and cues[i][0] < cues[i - 1][1]:
            cues[i][0] = cues[i - 1][1] + 0.001
        if cues[i][1] <= cues[i][0]:
            cues[i][1] = cues[i][0] + MIN_DUR
    cues[0][0] = max(0.0, cues[0][0])

    # merge a dangling single-word cue, OR an ultra-short (<0.75 s) sentence-tail cue,
    # backward into the previous cue so it reads as one line instead of flickering
    merged: list[list] = []
    for c in cues:
        tiny = (c[1] - c[0]) < 0.75
        single = len(c[2].split()) <= 1
        if merged and (single or tiny) and len(merged[-1][2]) + 1 + len(c[2]) <= 78:
            merged[-1][1] = c[1]
            merged[-1][2] = (merged[-1][2] + " " + c[2]).strip()
        else:
            merged.append(c)
    cues = merged

    # extend each cue toward a comfortable reading speed, into the gap before the next
    for i in range(len(cues)):
        s, e, t = cues[i]
        need = max(MIN_DUR, len(t) / CPS_TARGET)
        limit = (cues[i + 1][0] - 0.03) if i + 1 < len(cues) else min(DURATION, e + need)
        cues[i][1] = min(max(e, s + need), max(e, limit))

    # merge a still-too-fast cue into the next if the result still fits two wrapped lines
    out: list[list] = []
    i = 0
    while i < len(cues):
        s, e, t = cues[i]
        cps = len(t) / max(e - s, 0.001)
        if cps > CPS_MERGE and i + 1 < len(cues) and len(t) + len(cues[i + 1][2]) + 1 <= 92:
            ns, ne, nt = cues[i + 1]
            cues[i + 1] = [s, ne, (t + " " + nt).strip()]
            i += 1; continue
        out.append([s, e, t]); i += 1

    # final hard cap on reading speed (allow a <=0.35 s hold into the next cue)
    for i in range(len(out)):
        s, e, t = out[i]
        need = len(t) / CPS_CAP
        if e - s < need:
            cap = (out[i + 1][0] + 0.35) if i + 1 < len(out) else min(DURATION, s + need)
            out[i][1] = min(s + need, cap)

    # clamp everything inside the narration duration
    for c in out:
        c[1] = min(c[1], DURATION)
        if c[1] <= c[0]:
            c[0] = max(0.0, c[1] - MIN_DUR)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        "\n".join(f"{k+1}\n{srt_ts(s)} --> {srt_ts(e)}\n{wrap2(t)}\n"
                  for k, (s, e, t) in enumerate(out)), "utf-8")

    worst = max((len(t) / max(e - s, 0.001) for s, e, t in out), default=0.0)
    avg_chars = sum(len(t.replace("\n", " ")) for _, _, t in out) / max(len(out), 1)
    avg_dur = sum(e - s for s, e, _ in out) / max(len(out), 1)
    print(f"wrote {OUT.relative_to(ROOT)}")
    print(f"  cues={len(out)}  avg_chars/line={avg_chars:.1f}  avg_dur={avg_dur:.2f}s  "
          f"worst={worst:.0f}cps  last_end={out[-1][1]:.2f}s")
    if unmatched:
        print(f"  script words not found in ASR timing ({len(unmatched)}): "
              + ", ".join(unmatched[:40]) + (" ..." if len(unmatched) > 40 else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
