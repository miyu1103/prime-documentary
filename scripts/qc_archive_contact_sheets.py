#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Labeled contact sheets for the ARCHIVE shelf, so a human can see what a label really holds.

Why this exists: a filename is not evidence. The factory shelf proved it — every file
there is named after the SEARCH QUERY that fetched it (`AF-BG-45540__graduation_cap_toss`),
so a mislabeled clip reads as perfectly labeled and no machine gate can tell
(pd-factory-shelf-mislabeled / EP32 postmortem D-contact). The archive shelf names
files after the SOURCE's own title, which is better but still not the picture: NOAA
titles are survey codes and 27k NYPL scans all read `new-york-city-directory`.

So: sample each theme, tile the real frames with the real metadata burned in, and let
the owner mark verdicts. `archive_verdicts.jsonl` is what the inventory and the search
tool then trust — not the filenames.

`build_footage_contact_sheet.py` does this for ONE episode's staged pool; this does it
for the shelf itself, stratified across every source that fed a theme.

Usage:
    python scripts/qc_archive_contact_sheets.py                      # every theme
    python scripts/qc_archive_contact_sheets.py --theme courtroom_justice
    python scripts/qc_archive_contact_sheets.py --per-theme 96 --refresh
Output:
    H:\\pd-media\\assets\\archive\\_qc\\<theme>\\labeled_NN.jpg   (visual themes)
    H:\\pd-media\\assets\\archive\\_qc\\<theme>\\listen_NN.m3u8   (audio themes)
    H:\\pd-media\\assets\\archive\\_qc\\verdicts.template.jsonl   (fill in + save as archive_verdicts.jsonl)
"""
from __future__ import annotations

import argparse
import collections
import glob
import hashlib
import json
import os
import random
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

LEDGER_DIR = r"H:\pd-media\assets\archive\_ledger"
QC_DIR = r"H:\pd-media\assets\archive\_qc"
VIDEO_EXT = {".mp4", ".mov", ".webm", ".mkv", ".avi", ".mpeg", ".mpg", ".m4v"}
IMAGE_EXT = {".jpg", ".jpeg", ".png", ".gif", ".tif", ".tiff", ".webp", ".bmp"}
AUDIO_EXT = {".mp3", ".wav", ".flac", ".ogg", ".m4a", ".aac", ".aif", ".aiff"}

COLS, ROWS = 6, 4          # 24 tiles per sheet
THUMB_W, THUMB_H = 300, 170
LABEL_H = 34
PAD = 5
BG = (24, 24, 28)
FG = (232, 232, 236)
DIM = (150, 150, 158)


def kind_of(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    if ext in VIDEO_EXT:
        return "video"
    if ext in IMAGE_EXT:
        return "image"
    if ext in AUDIO_EXT:
        return "audio"
    return "other"


def load_ledgers(theme_filter: str | None) -> dict[str, list[dict]]:
    """theme -> records. Skips rejects/tombstones and the pre-archive factory ledger."""
    by_theme: dict[str, list[dict]] = collections.defaultdict(list)
    for path in sorted(glob.glob(os.path.join(LEDGER_DIR, "*.jsonl"))):
        base = os.path.basename(path)
        if base.startswith("rejects") or base.endswith(
                ("_dedup_removed.jsonl", "_removed.jsonl", "_candidates.jsonl")) \
                or base in ("factory.jsonl",):
            continue
        with open(path, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except Exception:
                    continue
                theme = rec.get("theme") or "_unthemed"
                if theme_filter and theme != theme_filter:
                    continue
                by_theme[theme].append(rec)
    return by_theme


def stratified_sample(recs: list[dict], n: int, seed: str) -> list[dict]:
    """Round-robin across sources so one whale source cannot fill the sheet.

    NOAA alone is 363 GB of near-identical flood aerials — an unstratified random
    sample of weather_disasters would be 24 tiles of the same grey square, which
    tells the owner nothing about the rest of the theme.
    """
    by_src: dict[str, list[dict]] = collections.defaultdict(list)
    for r in recs:
        by_src[r.get("source", "?")].append(r)
    rng = random.Random(hashlib.sha1(seed.encode()).hexdigest())
    for lst in by_src.values():
        rng.shuffle(lst)
    out: list[dict] = []
    srcs = sorted(by_src)
    i = 0
    while len(out) < n and any(by_src[s] for s in srcs):
        s = srcs[i % len(srcs)]
        if by_src[s]:
            out.append(by_src[s].pop())
        i += 1
    return out


def video_frame(path: str) -> tuple[Image.Image | None, str]:
    """Frame ~12% in (archival prints open on black leader), plus the SOURCE resolution.

    The label must report the source's own dimensions, never the thumbnail's — a label
    reading 255x170 for a 4707x4707 TIF is a measuring instrument that lies, and the
    whole point of this sheet is that you can trust what it says.
    """
    ss, wh = 3.0, "-"
    try:
        pr = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream=width,height:format=duration",
             "-of", "default=nw=1:nk=1", path],
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=30)
        vals = [v.strip() for v in (pr.stdout or "").splitlines() if v.strip()]
        if len(vals) >= 2 and vals[0].isdigit() and vals[1].isdigit():
            wh = f"{vals[0]}x{vals[1]}"
        dur = float(vals[2]) if len(vals) >= 3 else 0.0
        if dur > 8:
            ss = min(dur * 0.12, 600.0)
    except Exception:
        pass
    try:
        pr = subprocess.run(
            ["ffmpeg", "-v", "error", "-ss", f"{ss:.2f}", "-i", path, "-frames:v", "1",
             "-vf", f"scale={THUMB_W}:-1", "-f", "image2pipe", "-vcodec", "png", "-"],
            capture_output=True, timeout=120)
        if pr.returncode == 0 and pr.stdout:
            import io
            return Image.open(io.BytesIO(pr.stdout)).convert("RGB"), wh
    except Exception:
        pass
    return None, wh


def image_thumb(path: str) -> tuple[Image.Image | None, str]:
    try:
        im = Image.open(path)
        wh = f"{im.width}x{im.height}"          # read BEFORE any downscale
        # draft() decodes JPEG at reduced scale — the difference between seconds and
        # minutes on the 100 MB 4707x4707 NOAA TIFs.
        try:
            im.draft("RGB", (THUMB_W * 2, THUMB_H * 2))
        except Exception:
            pass
        im = im.convert("RGB")
        im.thumbnail((THUMB_W, THUMB_H))
        return im, wh
    except Exception:
        return None, "-"


def _font(size: int):
    for name in ("arial.ttf", "segoeui.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except Exception:
            continue
    return ImageFont.load_default()


F_MAIN = _font(12)
F_SUB = _font(11)


def tile(rec: dict, idx: int) -> Image.Image:
    """One labeled cell: the frame, plus who/what/where it actually is."""
    path = rec.get("file_path", "")
    k = kind_of(path)
    cell = Image.new("RGB", (THUMB_W, THUMB_H + LABEL_H), BG)
    thumb, wh = None, "-"
    if os.path.exists(path):
        thumb, wh = video_frame(path) if k == "video" else image_thumb(path)
    if thumb is not None:
        thumb.thumbnail((THUMB_W, THUMB_H))
        cell.paste(thumb, ((THUMB_W - thumb.width) // 2, (THUMB_H - thumb.height) // 2))
    else:
        d = ImageDraw.Draw(cell)
        msg = "MISSING ON DISK" if not os.path.exists(path) else f"no preview ({k})"
        d.text((8, THUMB_H // 2 - 6), msg, fill=(220, 90, 90), font=F_MAIN)
    d = ImageDraw.Draw(cell)
    title = (str(rec.get("title", "")) or os.path.basename(path))[:46]
    mb = (rec.get("bytes", 0) or 0) / 1e6
    size = f"{mb:.1f}MB" if mb < 10 else f"{mb:.0f}MB"
    lic = str(rec.get("license_decision", ""))[:16]
    d.text((4, THUMB_H + 2), f"#{idx} {rec.get('source', '?')} | {title}", fill=FG, font=F_MAIN)
    d.text((4, THUMB_H + 17),
           f"{k} {wh} {size} | {lic} | s={rec.get('relevance_score', '?')}",
           fill=DIM, font=F_SUB)
    return cell


def sheet_path(theme: str, n: int, kind: str = "labeled") -> str:
    out_dir = os.path.join(QC_DIR, theme)
    os.makedirs(out_dir, exist_ok=True)
    return os.path.join(out_dir, f"{kind}_{n:02d}.jpg")


def build_theme(theme: str, recs: list[dict], per_theme: int, refresh: bool) -> dict:
    picked = stratified_sample(recs, per_theme, theme)
    visual = [r for r in picked if kind_of(r.get("file_path", "")) in ("video", "image")]
    audio = [r for r in picked if kind_of(r.get("file_path", "")) == "audio"]
    stat = {"theme": theme, "total": len(recs), "sampled": len(picked),
            "sheets": 0, "playlists": 0, "missing": 0, "nopreview": 0}

    per_sheet = COLS * ROWS
    for n in range(0, len(visual), per_sheet):
        chunk = visual[n:n + per_sheet]
        out = sheet_path(theme, n // per_sheet + 1)
        if os.path.exists(out) and not refresh:
            stat["sheets"] += 1
            continue
        W = COLS * (THUMB_W + PAD) + PAD
        H = ROWS * (THUMB_H + LABEL_H + PAD) + PAD + 26
        canvas = Image.new("RGB", (W, H), BG)
        d = ImageDraw.Draw(canvas)
        srcs = collections.Counter(r.get("source") for r in recs)
        d.text((PAD, 6), f"{theme}  —  {len(recs):,} items in ledger  |  sources: "
                         + ", ".join(f"{s}:{c}" for s, c in srcs.most_common(8)),
               fill=FG, font=F_MAIN)
        for i, rec in enumerate(chunk):
            cell = tile(rec, n + i + 1)
            if not os.path.exists(rec.get("file_path", "")):
                stat["missing"] += 1
            x = PAD + (i % COLS) * (THUMB_W + PAD)
            y = 26 + PAD + (i // COLS) * (THUMB_H + LABEL_H + PAD)
            canvas.paste(cell, (x, y))
        canvas.save(out, "JPEG", quality=86, optimize=True)
        stat["sheets"] += 1
        print(f"  sheet -> {out}  ({len(chunk)} tiles)")

    if audio:
        out = sheet_path(theme, 1, "listen").replace(".jpg", ".m3u8")
        with open(out, "w", encoding="utf-8") as fh:
            fh.write("#EXTM3U\n")
            for r in audio:
                fh.write(f"#EXTINF:-1,{r.get('source')} | {str(r.get('title',''))[:70]}\n")
                fh.write(f"{r.get('file_path','')}\n")
        stat["playlists"] = 1
        print(f"  playlist -> {out}  ({len(audio)} clips — audio cannot be eyeballed)")
    return stat


def write_verdict_template(by_theme: dict[str, list[dict]]) -> str:
    """One row per theme x source: the unit the owner can actually accept or kill."""
    out = os.path.join(QC_DIR, "verdicts.template.jsonl")
    rows = []
    for theme, recs in sorted(by_theme.items()):
        for src, cnt in collections.Counter(r.get("source", "?") for r in recs).most_common():
            gb = sum((r.get("bytes", 0) or 0) for r in recs if r.get("source") == src) / 1e9
            rows.append({"theme": theme, "source": src, "items": cnt, "gb": round(gb, 1),
                         "verdict": "", "note": ""})
    with open(out, "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--theme", help="one theme only (default: all)")
    ap.add_argument("--per-theme", type=int, default=48,
                    help="items sampled per theme, stratified by source (default 48 = 2 sheets)")
    ap.add_argument("--refresh", action="store_true", help="rebuild sheets that already exist")
    ap.add_argument("--min-items", type=int, default=1, help="skip themes smaller than this")
    args = ap.parse_args()

    by_theme = load_ledgers(args.theme)
    if not by_theme:
        print(f"no ledger rows found in {LEDGER_DIR}"
              + (f" for theme={args.theme}" if args.theme else ""))
        return 2
    print(f"{sum(len(v) for v in by_theme.values()):,} ledger rows across "
          f"{len(by_theme)} themes")
    stats = []
    for theme, recs in sorted(by_theme.items(), key=lambda kv: -len(kv[1])):
        if len(recs) < args.min_items:
            continue
        print(f"[{theme}] {len(recs):,} items")
        stats.append(build_theme(theme, recs, args.per_theme, args.refresh))
    tmpl = write_verdict_template(by_theme)

    print("\n=== summary ===")
    print(f"{'theme':28} {'items':>8} {'sampled':>8} {'sheets':>7} {'missing':>8}")
    for s in stats:
        print(f"{s['theme']:28} {s['total']:8,} {s['sampled']:8} {s['sheets']:7} {s['missing']:8}")
    print(f"\nverdict template: {tmpl}")
    print("Mark each row verdict= good | mixed | unusable, then save as "
          f"{os.path.join(QC_DIR, 'archive_verdicts.jsonl')}")
    print("The inventory and search tools read that file — unusable rows stop being offered.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
