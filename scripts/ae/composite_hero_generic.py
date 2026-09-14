#!/usr/bin/env python
"""Composite AE hero cards over a finished film -- as OVERLAYS, and only if they improve it.

WHY THIS EXISTS (EP50, measured 2026-07-30): the per-episode composites shipped every card
with no blend mode, i.e. an opaque full-frame paste, at 5-10s each. On EP50 that put 132.9s of
frozen frames and 6.0s of pure black (card B8) into a 61-minute film -- the owner's two oldest
complaints, 黒画面 and 紙芝居, manufactured by the finishing step itself. The film without the
composite measured 0 black and 0 frozen.

So this composite:
  * forces `screen` blending unless a card explicitly asks otherwise -- the cards are cyan/bone
    type on black, and screen drops the black, so the film keeps MOVING under the card;
  * caps each card at --max-card-sec (default 3.0s), the single-freeze limit the ship gate uses;
  * MEASURES the result against the input and REFUSES to keep a composite that adds black or
    frozen time. A finishing step is not allowed to make the film worse.

    python scripts/ae/composite_hero_generic.py --slug morton \
        --base <in.mp4> --out <out.mp4> [--max-card-sec 3.0] [--dry-run]

Exit 0 = composite written and verified. Exit 1 = refused (the base file is left untouched).
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FFMPEG = shutil.which("ffmpeg") or r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe"
FFPROBE = shutil.which("ffprobe") or r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffprobe.exe"
W, H, FPS = 1920, 1080, 30


def probe_dur(p: Path) -> float:
    r = subprocess.run([FFPROBE, "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(p)], capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0


def probe_wh(p: Path) -> tuple[int, int]:
    r = subprocess.run([FFPROBE, "-v", "error", "-select_streams", "v:0", "-show_entries",
                        "stream=width,height", "-of", "csv=p=0:s=x", str(p)],
                       capture_output=True, text=True)
    try:
        w, h = r.stdout.strip().split("x")[:2]
        return int(w), int(h)
    except Exception:
        return 0, 0


def measure(p: Path) -> dict:
    """Black seconds and frozen seconds, the two things a composite must never add."""
    black = subprocess.run([FFMPEG, "-hide_banner", "-v", "info", "-i", str(p),
                            "-vf", "blackdetect=d=1.0:pix_th=0.10", "-an", "-f", "null", "-"],
                           capture_output=True, text=True).stderr
    frozen = subprocess.run([FFMPEG, "-hide_banner", "-v", "info", "-i", str(p),
                             "-vf", "freezedetect=n=-55dB:d=3", "-an", "-f", "null", "-"],
                            capture_output=True, text=True).stderr
    b = [float(x) for x in re.findall(r"black_duration:([0-9.]+)", black)]
    f = [float(x) for x in re.findall(r"freeze_duration: ?([0-9.]+)", frozen)]
    return {"black_sec": round(sum(b), 2), "black_max": round(max(b, default=0.0), 2),
            "frozen_sec": round(sum(f), 2), "frozen_max": round(max(f, default=0.0), 2)}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--base", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--beats", help="beats.json (default <ep>/08_edit/ae_hero/beats.json)")
    ap.add_argument("--cards", help="rendered card dir (default <ep>/08_edit/ae_hero/render)")
    ap.add_argument("--max-card-sec", type=float, default=3.0)
    ap.add_argument("--default-blend", default="screen", choices=("screen", "overlay", "multiply"))
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    ep_dirs = sorted((ROOT / "episodes").glob(f"PD-*-{a.slug}"))
    if not ep_dirs:
        print(f"no episode dir for slug {a.slug}", file=sys.stderr)
        return 1
    edit = ep_dirs[0] / "08_edit"
    beats_p = Path(a.beats) if a.beats else edit / "ae_hero" / "beats.json"
    cards_d = Path(a.cards) if a.cards else edit / "ae_hero" / "render"
    base, out = Path(a.base), Path(a.out)
    if not beats_p.is_file():
        print(f"[ae] no beats at {beats_p} -- nothing to composite (not an error)")
        return 0
    if out.exists():
        print(f"REFUSING to overwrite {out}", file=sys.stderr)
        return 1

    doc = json.loads(beats_p.read_text(encoding="utf-8"))
    beats = doc["beats"] if isinstance(doc, dict) else doc
    offset = float(doc.get("film_offset_sec", 0.0)) if isinstance(doc, dict) else 0.0
    base_dur = probe_dur(base)

    valid, skipped = [], 0
    for b in beats:
        card = cards_d / f"{b['id']}.mp4"
        if not card.is_file() or card.stat().st_size < 100_000:
            skipped += 1
            continue
        if probe_wh(card) != (W, H):
            skipped += 1
            continue
        dur = min(float(b.get("dur", 0.0)), a.max_card_sec, probe_dur(card))
        start = float(b.get("start", b.get("anchor", 0.0))) + offset
        if dur <= 0.2 or start + dur > base_dur:
            skipped += 1
            continue
        valid.append({"id": b["id"], "card": card, "start": start, "end": start + dur,
                      "blend": str(b.get("blend_mode") or a.default_blend)})

    print(f"[ae] {len(valid)} card(s) usable, {skipped} skipped, "
          f"cap {a.max_card_sec:.1f}s, blend={a.default_blend}")
    if not valid:
        print("[ae] nothing to composite")
        return 0
    if a.dry_run:
        for v in valid[:8]:
            print(f"    {v['id']:<16} {v['start']:8.2f}-{v['end']:8.2f}s  {v['blend']}")
        return 0

    inputs: list[str] = ["-i", str(base)]
    parts: list[str] = []
    prev = "0:v"
    for i, v in enumerate(valid):
        inputs += ["-i", str(v["card"])]
        lbl = f"v{i}"
        parts.append(f"[{i+1}:v]setpts=PTS-STARTPTS+{v['start']}/TB,"
                     f"trim=0:{v['end'] - v['start']:.3f},format=yuv420p[c{i}]")
        if v["blend"] in ("screen", "multiply"):
            parts.append(f"[{prev}][c{i}]blend=all_mode={v['blend']}:shortest=0:"
                         f"enable='between(t,{v['start']:.3f},{v['end']:.3f})'[{lbl}]")
        else:
            parts.append(f"[{prev}][c{i}]overlay=0:0:eof_action=pass:"
                         f"enable='between(t,{v['start']:.3f},{v['end']:.3f})'[{lbl}]")
        prev = lbl
    fg = ";".join(parts)

    cmd = [FFMPEG, "-y", "-hide_banner", *inputs, "-filter_complex", fg, "-map", f"[{prev}]",
           "-map", "0:a?", "-c:v", "libx264", "-preset", "medium", "-crf", "17",
           "-pix_fmt", "yuv420p", "-c:a", "copy", str(out)]
    print(f"[ae] compositing {len(valid)} card(s) -> {out.name} ...", flush=True)
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0 or not out.exists():
        print(r.stderr[-2500:], file=sys.stderr)
        return 1

    before, after = measure(base), measure(out)
    print(f"[ae] base  black {before['black_sec']}s (max {before['black_max']}) | "
          f"frozen {before['frozen_sec']}s (max {before['frozen_max']})")
    print(f"[ae] comp  black {after['black_sec']}s (max {after['black_max']}) | "
          f"frozen {after['frozen_sec']}s (max {after['frozen_max']})")
    worse = (after["black_sec"] > before["black_sec"] + 0.5
             or after["frozen_sec"] > before["frozen_sec"] + 0.5
             or after["black_max"] > max(before["black_max"], 1.0)
             or after["frozen_max"] > max(before["frozen_max"], 3.5))
    if worse:
        out.unlink(missing_ok=True)
        print("[ae] REFUSED: the composite added black/frozen time. Base film kept as-is.",
              file=sys.stderr)
        return 1
    print(f"[ae] OK {out} ({probe_dur(out):.1f}s) -- verified no added black/frozen time")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
