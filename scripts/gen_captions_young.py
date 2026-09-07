#!/usr/bin/env python
"""Generate EP42 Young captions from narration_index text.

The generator uses the narration chunks verbatim and keeps cue boundaries on
chunk/sentence boundaries. It does not invent or rewrite narration text.
"""
from __future__ import annotations

import argparse
import json
import re
import tempfile
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-042-young"
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
        .replace("Sgt.", "Sgt<dot>")
    )
    parts = [p.strip() for p in re.split(r"(?<=[.?!])\s+", protected) if p.strip()]
    return [p.replace("U<S>", "U.S.").replace("v<dot>", "v.").replace("Mr<dot>", "Mr.").replace("Sgt<dot>", "Sgt.") for p in parts]


def word_count(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'’-]*", text))


def cues_from_narr(narr: dict) -> list[dict]:
    cues: list[dict] = []
    for chunk in narr["chunks"]:
        text = str(chunk.get("text") or chunk.get("spoken_text") or "").strip()
        if not text:
            continue
        parts = sentences(text)
        if not parts:
            parts = [text]
        total_words = max(1, sum(word_count(p) for p in parts))
        start = float(chunk["start"])
        end = float(chunk["end"])
        span = max(0.9, end - start)
        t = start
        for i, part in enumerate(parts):
            if i == len(parts) - 1:
                e = end
            else:
                e = t + span * word_count(part) / total_words
            if e - t < 0.9:
                e = min(end, t + 0.9)
            cues.append({"start": round(t, 3), "end": round(e, 3), "text": part})
            t = e
    return cues


def write_srt(cues: list[dict], out: Path) -> None:
    lines: list[str] = []
    for i, c in enumerate(cues, 1):
        lines += [str(i), f"{srt_ts(c['start'])} --> {srt_ts(c['end'])}", c["text"], ""]
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")


def selftest() -> int:
    narr = {
        "chunks": [
            {"start": 0, "end": 4, "text": "Her wrists are cuffed before she can cover herself."},
            {"start": 4, "end": 8, "text": "Hudson v. Michigan, 547 U.S. 586, stays together."},
            {"start": 8, "end": 12, "text": "A settlement, not a finding. The door stays closed."},
        ]
    }
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "captions.srt"
        write_srt(cues_from_narr(narr), p)
        r = subprocess.run([str(ROOT / ".venv" / "Scripts" / "python.exe"), str(ROOT / "scripts" / "check_caption_breaks.py"), str(p)])
        return r.returncode


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--narr", type=Path, required=False, default=ROOT / "episodes" / EP / "06_audio" / "narration_index.stub.v001.json")
    ap.add_argument("--out", type=Path, default=OUT)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    narr = json.loads(args.narr.read_text(encoding="utf-8"))
    cues = cues_from_narr(narr)
    write_srt(cues, args.out)
    print(f"wrote {args.out} cues={len(cues)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
