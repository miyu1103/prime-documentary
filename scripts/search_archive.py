# -*- coding: utf-8 -*-
"""
Search the PD archive shelf across ALL ingest ledgers (every agent/source) in seconds.

Queries the centralized rights ledger H:\\pd-media\\assets\\archive\\_ledger\\*.jsonl
(contract: CONTRACT.md in the same folder) by free-text keywords + optional filters,
printing file path, title, license and theme for each hit.

Usage:
  python scripts/search_archive.py courtroom 1950s --theme courtroom_justice
  python scripts/search_archive.py "post office" --source ia --license pd
  python scripts/search_archive.py train --kind video --limit 50
  python scripts/search_archive.py --theme japan --stats
"""
from __future__ import annotations

import argparse
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

LEDGER_DIR = r"H:\pd-media\assets\archive\_ledger"
VIDEO_EXT = {".mp4", ".mov", ".webm", ".mkv", ".avi", ".mpeg", ".mpg"}
IMAGE_EXT = {".jpg", ".jpeg", ".png", ".gif", ".tif", ".tiff", ".webp"}
AUDIO_EXT = {".mp3", ".wav", ".flac", ".ogg", ".m4a", ".aac"}


def kind_of(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    if ext in VIDEO_EXT:
        return "video"
    if ext in IMAGE_EXT:
        return "image"
    if ext in AUDIO_EXT:
        return "audio"
    return "other"


def main() -> int:
    ap = argparse.ArgumentParser(description="Search PD archive ledgers")
    ap.add_argument("keywords", nargs="*", help="free-text terms (ANDed, case-insensitive; "
                    "matched against title, id, matched_keywords, theme, filename)")
    ap.add_argument("--theme", help="exact theme filter")
    ap.add_argument("--source", help="source filter (ia, loc, nasa, wikimedia, ...)")
    ap.add_argument("--license", dest="license_", help="pd | cc0 | free_commercial | review_required")
    ap.add_argument("--kind", choices=["video", "image", "audio"], help="media kind by extension")
    ap.add_argument("--missing", action="store_true", help="only rows whose file is missing on disk")
    ap.add_argument("--limit", type=int, default=30, help="max rows printed (default 30)")
    ap.add_argument("--paths-only", action="store_true", help="print file paths only (pipeable)")
    ap.add_argument("--stats", action="store_true", help="print per-theme/source/license counts only")
    args = ap.parse_args()

    if not os.path.isdir(LEDGER_DIR):
        print(f"no ledger dir: {LEDGER_DIR}")
        return 2
    terms = [t.lower() for t in args.keywords]
    hits = []
    stats: dict[str, int] = {}
    for fn in sorted(os.listdir(LEDGER_DIR)):
        if not fn.endswith(".jsonl") or fn.startswith("rejects") or fn.endswith(
                ("_dedup_removed.jsonl", "_candidates.jsonl")):
            continue
        if args.source and fn != f"{args.source.lower()}.jsonl":
            continue
        with open(os.path.join(LEDGER_DIR, fn), encoding="utf-8") as f:
            for line in f:
                try:
                    rec = json.loads(line)
                except Exception:
                    continue
                if args.theme and rec.get("theme") != args.theme:
                    continue
                if args.license_ and rec.get("license_decision") != args.license_:
                    continue
                fp = rec.get("file_path", "")
                if args.kind and kind_of(fp) != args.kind:
                    continue
                if args.missing and os.path.exists(fp):
                    continue
                blob = " ".join([str(rec.get("title", "")), str(rec.get("id", "")),
                                 " ".join(rec.get("matched_keywords", []) or []),
                                 rec.get("theme", ""), os.path.basename(fp)]).lower()
                if all(t in blob for t in terms):
                    hits.append(rec)
                    for k in (f"theme:{rec.get('theme')}", f"source:{rec.get('source')}",
                              f"license:{rec.get('license_decision')}",
                              f"kind:{kind_of(fp)}"):
                        stats[k] = stats.get(k, 0) + 1
    if args.stats:
        print(f"{len(hits)} matching items")
        for k in sorted(stats):
            print(f"  {k:42} {stats[k]}")
        return 0
    for rec in hits[:args.limit]:
        if args.paths_only:
            print(rec.get("file_path", ""))
        else:
            mb = rec.get("bytes", 0) / 1e6
            print(f"[{rec.get('source'):>9}|{rec.get('license_decision'):>15}|"
                  f"{rec.get('theme', ''):22}|{mb:7.1f}MB] {str(rec.get('title', ''))[:60]}")
            print(f"    {rec.get('file_path', '')}")
    print(f"-- {len(hits)} hits total"
          + (f", showing first {args.limit}" if len(hits) > args.limit else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
