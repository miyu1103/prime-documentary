#!/usr/bin/env python
"""Generate EP40 Lech captions with syntax-aware cue boundaries."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from fix_caption_dangling import NO_DANGLE_END, wrap as safe_wrap

EPDIR = ROOT / "episodes" / "PD-2026-040-lech"
OUT = EPDIR / "08_edit" / "captions.final.v001.srt"
TERMINAL = ".?!—:;"
MAX_WORDS = 7
MAX_CHARS = 42
MIN_WORDS = 3
ABBR = {"Mr.", "Mrs.", "Ms.", "Dr.", "U.S.", "No.", "v."}
BOUNDARY_WORDS = {"because", "while", "when", "after", "before", "since", "until", "unless", "although", "though", "whether", "if", "that", "which", "who", "whose", "whom"}
PREPS = {"of", "to", "in", "on", "at", "for", "with", "from", "by", "into", "over", "under", "against", "between", "through", "about"}


def split_sentences(text: str) -> list[str]:
    toks = text.replace("\n", " ").split()
    out, cur = [], []
    for tok in toks:
        cur.append(tok)
        if any(tok.endswith(p) for p in TERMINAL) and tok not in ABBR:
            out.append(" ".join(cur))
            cur = []
    if cur:
        out.append(" ".join(cur))
    return out


def words(text: str) -> list[str]:
    return text.split()


def wc(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9]+(?:['-][A-Za-z0-9]+)?", text))


def internal_split(tokens: list[str]) -> int | None:
    for i in range(1, len(tokens)):
        prev = tokens[i - 1].lower().strip(",")
        cur = tokens[i].lower().strip(",")
        pair = f"{prev} {cur}"
        left_tail = " ".join(t.lower().strip(",.;:?!") for t in tokens[max(0, i - 2):i])
        if cur == "to" and left_tail == "the right":
            continue
        if prev.endswith(",") and cur in {"and", "but", "so", "or", "yet", "nor"}:
            return i
        if cur in BOUNDARY_WORDS:
            return i
        if cur in PREPS and len(tokens) - i >= 3:
            return i
        if tokens[i - 1].endswith(","):
            return i
        if pair.startswith("to "):
            return i
    legal = [i for i in range(2, len(tokens) - 1) if re.sub(r"[^a-z]", "", tokens[i - 1].lower()) not in NO_DANGLE_END]
    if legal:
        mid = len(tokens) / 2
        return min(legal, key=lambda x: abs(x - mid))
    return None


def chunk_sentence(sentence: str) -> list[str]:
    queue = [words(sentence)]
    chunks = []
    while queue:
        toks = queue.pop(0)
        text = " ".join(toks)
        if len(toks) <= MAX_WORDS and len(text) <= MAX_CHARS:
            chunks.append(text)
            continue
        idx = internal_split(toks)
        if idx is None:
            chunks.append(text)
            continue
        left, right = toks[:idx], toks[idx:]
        if len(left) < MIN_WORDS or len(right) < MIN_WORDS:
            chunks.append(text)
        else:
            queue.insert(0, right)
            queue.insert(0, left)
    merged: list[str] = []
    for c in chunks:
        if wc(c) < MIN_WORDS and merged:
            merged[-1] = merged[-1] + " " + c
        else:
            merged.append(c)
    if len(merged) > 1 and wc(merged[-1]) < MIN_WORDS:
        merged[-2] += " " + merged.pop()
    return merged


def make_cues(text: str, duration: float = 720.8) -> list[str]:
    chunks = []
    for s in split_sentences(text):
        chunks.extend(chunk_sentence(s))
    chunks = [c for c in chunks if c.strip()]
    merged: list[str] = []
    for chunk in chunks:
        if wc(chunk) < MIN_WORDS and merged:
            merged[-1] = f"{merged[-1]} {chunk}"
        else:
            merged.append(chunk)
    chunks = merged
    if not chunks:
        return []
    total_words = sum(max(1, wc(c)) for c in chunks)
    t = 0.0
    cues = []
    for c in chunks:
        dur = max(0.9, duration * max(1, wc(c)) / total_words)
        cues.append((t, min(duration, t + dur), c))
        t += dur
    return cues


def fmt_ts(t: float) -> str:
    ms = int(round(t * 1000))
    h, rem = divmod(ms, 3600000)
    m, rem = divmod(rem, 60000)
    s, ms = divmod(rem, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def write_srt(cues, path: Path) -> None:
    lines = []
    for i, (start, end, text) in enumerate(cues, start=1):
        wrapped = safe_wrap(text)
        lines += [str(i), f"{fmt_ts(start)} --> {fmt_ts(end)}", *wrapped, ""]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")


def source_text() -> str:
    slot = EPDIR / "03_script" / "lech_slots.v001.json"
    if not slot.exists():
        slot = EPDIR / "03_script" / "lech_slots.stub.v001.json"
    if not slot.exists():
        return "Nothing. This is a stub caption file."
    data = json.loads(slot.read_text(encoding="utf-8"))
    parts = []
    parts.extend(data.get("hook", {}).get("lines", []))
    parts.extend(a.get("narration", "") for a in data.get("acts", []))
    ed = data.get("ed", {})
    parts.extend([ed.get("payoff_line", ""), ed.get("cta_line", ""), ed.get("question_line", "")])
    return " ".join(parts)


def selftest() -> int:
    samples = [
        "...ends with a warning and a ride home.",
        "A child was handed a form giving up the right to a lawyer.",
        "...taught to trust the adults in the room, signed away...",
        "Something happened before. Nothing.",
    ]
    text = " ".join(samples)
    tmp = EPDIR / "08_edit" / "_dryrun" / "captions.selftest.srt"
    write_srt(make_cues(text, 20.0), tmp)
    cue_text = [c[2] for c in make_cues(text, 20.0)]
    broken_phrase = any(c.lower().rstrip(".,?!") == "the right" for c in cue_text) or any(c.lower().startswith("to a lawyer") for c in cue_text)
    isolated = any(wc(c) < MIN_WORDS for c in cue_text)
    if broken_phrase or isolated:
        print(json.dumps({"selftest": "FAIL", "broken_phrase": broken_phrase, "isolated": isolated, "cues": cue_text}, ensure_ascii=False, indent=2))
        return 1
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "check_caption_breaks.py"), str(tmp)], cwd=ROOT, capture_output=True, text=True)
    print(r.stdout.strip())
    if r.returncode != 0:
        print(r.stderr[-1000:], file=sys.stderr)
    return r.returncode


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ep", default="PD-2026-040-lech")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    write_srt(make_cues(source_text()), OUT)
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
