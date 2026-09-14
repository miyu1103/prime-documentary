#!/usr/bin/env python
"""Generate EP49 Strieff captions from narration_index text."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-049-strieff"
OUT = ROOT / "episodes" / EP / "08_edit" / "captions.final.v001.srt"


def srt_ts(t: float) -> str:
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def sentences(text: str) -> list[str]:
    protected = (
        text.replace("U.S.", "U<S>")
        .replace("v.", "v<dot>")
        .replace("Mr.", "Mr<dot>")
        .replace("Dr.", "Dr<dot>")
        .replace("Jr.", "Jr<dot>")
    )
    parts = [p.strip() for p in re.split(r"(?<=[.?!])\s+", protected) if p.strip()]
    return [
        p.replace("U<S>", "U.S.")
        .replace("v<dot>", "v.")
        .replace("Mr<dot>", "Mr.")
        .replace("Dr<dot>", "Dr.")
        .replace("Jr<dot>", "Jr.")
        for p in parts
    ]


def word_count(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'’-]*", text))


def cues_from_narr(narr: dict, offset: float = 0.0) -> list[dict]:
    cues: list[dict] = []
    for chunk in narr["chunks"]:
        text = str(chunk.get("text") or chunk.get("spoken_text") or "").strip()
        if not text:
            continue
        parts = sentences(text) or [text]
        total_words = max(1, sum(word_count(p) for p in parts))
        start = float(chunk["start"]) + offset
        end = float(chunk["end"]) + offset
        span = max(0.9, end - start)
        t = start
        for idx, part in enumerate(parts):
            e = end if idx == len(parts) - 1 else t + span * word_count(part) / total_words
            if e - t < 0.9:
                e = min(end, t + 0.9)
            cues.append({"start": round(t, 3), "end": round(e, 3), "text": part})
            t = e
    return cues


def write_srt(cues: list[dict], out: Path) -> None:
    lines: list[str] = []
    for idx, cue in enumerate(cues, 1):
        lines += [str(idx), f"{srt_ts(cue['start'])} --> {srt_ts(cue['end'])}", cue["text"], ""]
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")


def selftest() -> int:
    narr = {"chunks": [{"start": 0, "end": 5, "text": "Utah v. Strieff, 579 U.S. 232, stays together."}]}
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "captions.srt"
        write_srt(cues_from_narr(narr), out)
        return subprocess.run([str(ROOT / ".venv" / "Scripts" / "python.exe"), str(ROOT / "scripts" / "check_caption_breaks.py"), str(out)]).returncode


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--narr", type=Path, default=ROOT / "episodes" / EP / "06_audio" / "narration_index.v001.json")
    parser.add_argument("--out", type=Path, default=OUT)
    parser.add_argument("--offset", type=float, default=0.0)
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    if args.selftest:
        return selftest()
    narr = json.loads(args.narr.read_text(encoding="utf-8"))
    cues = cues_from_narr(narr, args.offset)
    write_srt(cues, args.out)
    print(f"wrote {args.out} cues={len(cues)} offset={args.offset}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
