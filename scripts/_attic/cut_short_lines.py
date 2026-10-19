#!/usr/bin/env python3
"""Cut a Short's body lines out of an episode's long-form VO master (SHORTS_SLATE §7 step A-1).

The hybrid-audio path: a Short's body lines already exist inside the episode's
`vc_master_v001.mp3`, so they are cut (free) instead of re-synthesized, and only the hook and the
CTA go to ElevenLabs. This script performs the cut half and fills in the verbatim text of the cut
lines from the episode's narration index, so `gen_newshort_narration.py --text-json` can consume
the same file and synthesize only what is missing.

Input spec (`episodes/<EP>/09_package/short<NN>_lines.v001.json`) is the list that
`gen_newshort_narration.py` reads — `[{id, delivery, text}, ...]` — plus one extra key per line:

    {"id": "L2", "delivery": "building", "source": {"spans": [["VC-0080", "VC-0082"]]}}
    {"id": "L1", "delivery": "intense",  "source": "rerecord", "text": "..."}

`spans` is a list of inclusive [firstVC, lastVC] ranges; several ranges are cut separately and
concatenated (that is how a line drops an interjection sitting in the middle of it). `text` is
written back into the file for `spans` lines, so the caption builder and the narration index carry
the real wording. `rerecord` lines are left untouched.

Writes (idempotent — an existing chunk >2048 bytes is left alone, matching gen_newshort_narration):
  <media>/episodes/<EP>/06_voice/draft/short<NN>/en_us/short<NN>_L?.mp3

NOTE the naming trap (memory `pd-shorts-pipeline`): shorts drafts MUST live under
`06_voice/draft/short<NN>/en_us/`. Writing into `06_voice/draft/` collides with the episode's own
`VC-####.mp3` chunks and silently splices long-form audio into the short.

Usage:
  python scripts/cut_short_lines.py --short 60 --ep PD-2026-053-norfolk \
      --spec episodes/PD-2026-053-norfolk/09_package/short60_lines.v001.json [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAD_IN = 0.12   # start earlier so the breath before the line survives
PAD_OUT = 0.18  # end later so the tail is not clipped


def media_root() -> Path:
    cfg = json.loads((ROOT / "config/storage.local.json").read_text("utf-8"))
    return Path(cfg["roots"]["media"]["path"])


def dur(path: Path) -> float:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    try:
        return round(float(r.stdout.strip()), 3)
    except ValueError:
        return 0.0


def load_index(ep: str) -> dict:
    p = ROOT / "episodes" / ep / "06_audio" / "narration_index.v001.json"
    d = json.loads(p.read_text("utf-8"))
    chunks = d["chunks"] if isinstance(d, dict) and "chunks" in d else d
    return {c["id"]: c for c in chunks}


def resolve(index: dict, src: dict) -> tuple[list[tuple[float, float]], str]:
    """Turn {"spans": [[firstVC, lastVC], ...]} into concrete (start, end) seconds + verbatim text.

    `start_sec` / `end_sec` override the first span's start and the last span's end in master
    seconds. Use them to end a line mid-chunk at a measured pause (`silencedetect`) — e.g. when the
    Short's re-recorded hook already says the second half of that chunk and repeating it verbatim
    would read as a stutter. An override makes the derived text wrong, so a line that carries one
    must state its own `text`; the caller keeps it.
    """
    ids = sorted(index)
    ranges: list[tuple[float, float]] = []
    words: list[str] = []
    for first, last in src["spans"]:
        for vc in (first, last):
            if vc not in index:
                raise SystemExit(f"ERROR: {vc} not in narration index")
        i, j = ids.index(first), ids.index(last)
        if j < i:
            raise SystemExit(f"ERROR: span {first}..{last} runs backwards")
        ranges.append((index[first]["start"], index[last]["end"]))
        words.extend(index[v]["text"].strip() for v in ids[i:j + 1])
    if "start_sec" in src:
        ranges[0] = (float(src["start_sec"]), ranges[0][1])
    if "end_sec" in src:
        ranges[-1] = (ranges[-1][0], float(src["end_sec"]))
    for start, end in ranges:
        if end <= start:
            raise SystemExit(f"ERROR: span resolves to a non-positive range {start}..{end}")
    return ranges, " ".join(words)


def cut(master: Path, ranges: list[tuple[float, float]], out: Path, tmp: Path) -> None:
    parts: list[Path] = []
    for k, (start, end) in enumerate(ranges):
        seg = tmp / f"{out.stem}_seg{k}.mp3"
        subprocess.run(["ffmpeg", "-y", "-ss", f"{max(0.0, start - PAD_IN):.3f}",
                        "-to", f"{end + PAD_OUT:.3f}", "-i", str(master),
                        "-c:a", "libmp3lame", "-b:a", "192k", str(seg)],
                       check=True, capture_output=True)
        parts.append(seg)
    if len(parts) == 1:
        parts[0].replace(out)
        return
    lst = tmp / f"{out.stem}_concat.txt"
    lst.write_text("".join(f"file '{p.as_posix()}'\n" for p in parts), "utf-8")
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst),
                    "-c:a", "libmp3lame", "-b:a", "192k", str(out)], check=True, capture_output=True)
    for p in parts:
        p.unlink(missing_ok=True)
    lst.unlink(missing_ok=True)


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--short", required=True)
    ap.add_argument("--ep", required=True)
    ap.add_argument("--spec", required=True)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    short = f"short{args.short}"
    spec_path = Path(args.spec)
    spec = json.loads(spec_path.read_text("utf-8"))
    index = load_index(args.ep)
    master = media_root() / "episodes" / args.ep / "06_voice" / "master" / "vc_master_v001.mp3"
    if not master.exists():
        raise SystemExit(f"ERROR: VO master missing: {master}")
    draft = media_root() / "episodes" / args.ep / "06_voice" / "draft" / short / "en_us"

    total_cut = 0.0
    for line in spec:
        src = line.get("source")
        if src == "rerecord" or not isinstance(src, dict):
            print(f"  {line['id']:3s} RE-RECORD  {len(line.get('text', '').split()):3d}w  "
                  f"{line.get('text', '')[:60]}")
            continue
        ranges, text = resolve(index, src)
        overridden = "start_sec" in src or "end_sec" in src
        if overridden and not line.get("text", "").strip():
            raise SystemExit(f"ERROR: {line['id']} overrides span seconds, so it must state its own text")
        if not overridden:
            line["text"] = text
        text = line["text"]
        secs = sum(e - s + PAD_IN + PAD_OUT for s, e in ranges)
        total_cut += secs
        print(f"  {line['id']:3s} CUT        {len(text.split()):3d}w  {secs:6.2f}s  "
              f"{' + '.join(f'{a:.2f}-{b:.2f}' for a, b in ranges)}")
        if args.dry_run:
            continue
        draft.mkdir(parents=True, exist_ok=True)
        out = draft / f"{short}_{line['id']}.mp3"
        if out.exists() and out.stat().st_size > 2048:
            print(f"      exists, kept ({dur(out):.2f}s)")
            continue
        cut(master, ranges, out, draft)
        print(f"      -> {out.name} {out.stat().st_size // 1024}KB {dur(out):.2f}s")

    print(f"cut total ≈ {total_cut:.2f}s")
    if not args.dry_run:
        spec_path.write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n", "utf-8")
        print(f"spec text back-filled -> {spec_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
