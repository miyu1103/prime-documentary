"""
scripts/gen_srt_v2.py
Generate master narration MP3 + SRT from 06_voice/draft chunks.
Reads voice_plan.v001.json for text; actual durations from ffprobe.

Output:
  H:\pd-media\episodes\PD-2026-001-miranda\06_voice\master\vc_master_v001.mp3
  H:\pd-media\episodes\PD-2026-001-miranda\07_edit\sample\subs_vc_v001.srt
"""
from __future__ import annotations

import json
import pathlib
import re
import subprocess
import sys
import tempfile

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

VOICE_PLAN  = pathlib.Path(
    r"C:\Users\aab15\Documents\prime-documentary\episodes"
    r"\PD-2026-001-miranda\06_audio\voice_plan.v001.json"
)
DRAFT_DIR   = pathlib.Path(r"H:\pd-media\episodes\PD-2026-001-miranda\06_voice\draft")
MASTER_DIR  = pathlib.Path(r"H:\pd-media\episodes\PD-2026-001-miranda\06_voice\master")
MASTER_MP3  = MASTER_DIR / "vc_master_v001.mp3"
OUT_SRT     = pathlib.Path(
    r"H:\pd-media\episodes\PD-2026-001-miranda\07_edit\sample\subs_vc_v001.srt"
)
FFMPEG      = r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe"
FFPROBE     = r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffprobe.exe"

TARGET_WORDS = 5  # slightly looser than before for longer phrases


def probe_duration(path: pathlib.Path) -> float:
    r = subprocess.run(
        [FFPROBE, "-v", "quiet", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(path)],
        capture_output=True, text=True,
    )
    return round(float(r.stdout.strip()), 3)


def to_srt_ts(t: float) -> str:
    t = max(0.0, t)
    h  = int(t // 3600)
    m  = int((t % 3600) // 60)
    s  = int(t % 60)
    ms = int(round((t % 1) * 1000))
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def to_chunks(text: str, target: int = TARGET_WORDS) -> list[str]:
    """Split at natural phrase boundaries."""
    sents = re.split(r'(?<=[.!?])\s+', text.strip())
    chunks: list[str] = []
    for sent in sents:
        words = sent.split()
        if len(words) <= int(target * 1.6):
            chunks.append(sent.strip())
            continue
        clauses = re.split(r'\s*(?:—|–)\s*|(?<=[,;:])\s+', sent)
        buf: list[str] = []
        for clause in clauses:
            cw = clause.split()
            if len(buf) + len(cw) <= int(target * 1.6):
                buf.extend(cw)
            else:
                if buf:
                    chunks.append(" ".join(buf))
                buf = cw
        if buf:
            chunks.append(" ".join(buf))
    result: list[str] = []
    for ch in chunks:
        w = ch.split()
        if len(w) > int(target * 2):
            mid = len(w) // 2
            result.append(" ".join(w[:mid]))
            result.append(" ".join(w[mid:]))
        else:
            result.append(ch)
    return [r for r in result if r.strip()]


def concat_mp3(chunk_paths: list[pathlib.Path], out: pathlib.Path) -> None:
    MASTER_DIR.mkdir(parents=True, exist_ok=True)
    tmp_dir = pathlib.Path(tempfile.gettempdir()) / "pd_master"
    tmp_dir.mkdir(exist_ok=True)
    concat_txt = tmp_dir / "concat_narr.txt"
    concat_txt.write_text(
        "".join(f"file '{p.as_posix()}'\n" for p in chunk_paths),
        encoding="utf-8",
    )
    tmp_out = out.with_suffix(".partial.mp3")
    r = subprocess.run([
        FFMPEG, "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_txt),
        "-f", "mp3", "-c:a", "copy",
        str(tmp_out),
    ], capture_output=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        raise RuntimeError(f"concat failed: {r.stderr[-500:]}")
    tmp_out.replace(out)


def main() -> None:
    plan = json.loads(VOICE_PLAN.read_text(encoding="utf-8"))
    chunks = plan["chunks"]

    chunk_paths: list[pathlib.Path] = []
    for c in chunks:
        p = DRAFT_DIR / f"{c['chunk_id']}.mp3"
        if not p.exists():
            raise FileNotFoundError(f"Missing: {p}")
        chunk_paths.append(p)

    # ── 1. Concat into master MP3 ──────────────────────────────────────────
    print("Concatenating master narration…")
    concat_mp3(chunk_paths, MASTER_MP3)
    master_dur = probe_duration(MASTER_MP3)
    print(f"  ✓ {MASTER_MP3.name}  {master_dur:.1f}s")

    # ── 2. Build SRT from per-chunk timings ────────────────────────────────
    print("\nBuilding SRT…")
    OUT_SRT.parent.mkdir(parents=True, exist_ok=True)
    entries: list[str] = []
    idx    = 1
    cursor = 0.0

    for c, path in zip(chunks, chunk_paths):
        dur    = probe_duration(path)
        text   = c["spoken_text"]
        subs   = to_chunks(text, TARGET_WORDS)
        cpf    = dur / len(subs) if subs else 0.0

        print(f"  {c['chunk_id']}  {dur:.1f}s → {len(subs)} subtitles @ {cpf:.2f}s each")

        for si, sub in enumerate(subs):
            t_start = cursor + si * cpf
            t_end   = cursor + (si + 1) * cpf - 0.05
            entries.append(
                f"{idx}\n{to_srt_ts(t_start)} --> {to_srt_ts(t_end)}\n{sub}"
            )
            idx += 1

        cursor += dur

    OUT_SRT.write_text("\n\n".join(entries) + "\n", encoding="utf-8")
    print(f"\n✓ {OUT_SRT}  ({idx-1} subtitle entries, {cursor:.1f}s total)")
    print(f"\nMaster : {MASTER_MP3}")
    print(f"SRT    : {OUT_SRT}")


if __name__ == "__main__":
    main()
