#!/usr/bin/env python
"""Generate EP50 Central Park captions from narration_index text."""
from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-050-centralpark"
DEFAULT_NARR = ROOT / "episodes" / EP / "06_audio" / "narration_index.v001.json"
DEFAULT_OUT = ROOT / "episodes" / EP / "08_edit" / "captions.final.v001.srt"


def srt_ts(t: float) -> str:
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def cues_from_narr(narr: dict) -> list[dict]:
    cues: list[dict] = []
    for chunk in narr["chunks"]:
        text = str(chunk.get("text") or chunk.get("spoken_text") or "").strip()
        if text:
            cues.append({"start": round(float(chunk["start"]), 3), "end": round(float(chunk["end"]), 3), "text": text})
    return cues


def write_srt(cues: list[dict], out: Path) -> None:
    lines: list[str] = []
    for i, cue in enumerate(cues, 1):
        lines += [str(i), f"{srt_ts(cue['start'])} --> {srt_ts(cue['end'])}", cue["text"], ""]
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")


def selftest() -> int:
    narr = {"chunks": [{"start": 0, "end": 2.5, "text": "A room. A promise."}]}
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "captions.srt"
        write_srt(cues_from_narr(narr), p)
        return subprocess.run([str(ROOT / ".venv" / "Scripts" / "python.exe"), str(ROOT / "scripts" / "check_caption_breaks.py"), str(p)]).returncode


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--narr", type=Path, default=DEFAULT_NARR)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
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
