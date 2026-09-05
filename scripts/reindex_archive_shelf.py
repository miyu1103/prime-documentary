#!/usr/bin/env python3
r"""Rebuild the archive ledger from the files that are still on disk.

WHY THIS EXISTS
---------------
2026-08-20. The plain Samsung T7 that held `E:\pd-media` failed its USB interface --
proven by swapping only the drive in a port and cable the T7 Shield then used
successfully. It carried `_ledger`, and the ledger was the shelf's only memory: what each
file is, where it came from, and on what licence basis it may be used.

The FILES on D:, E: and F: survived. Their MEMORY did not. `ingest_archive_sources.py`
reads the ledger to know what it already has, so with an empty ledger it would re-download
13,875 videos and 8,635 audio files it is standing on. This rebuilds the memory first.

WHAT IT CAN RECOVER, AND WHAT IT CANNOT
---------------------------------------
Every file the ingest wrote is named `<source>__<id>__<slug>.<ext>`, so the SOURCE and the
source's own ITEM ID survive in the filename. From those two the licence basis is
recoverable, because it is a property of the source, not of the individual file --
Mixkit, Coverr, Pixabay and Pexels licences are blanket, NASA/NOAA/NARA output is US
federal public domain, Internet Archive items vary and are marked for review.

What is NOT recoverable is the per-item licence FIELD the source served at download time
(`license_field_raw`), the relevance score, and the matched keywords. Those are written as
empty, and every row carries `reindexed_at` and `reindex_basis` so that no later reader
mistakes a derived licence for a verified one.

**10,262 of the surviving videos carry no source prefix at all.** For those, nothing
identifies where they came from. They are written to `unattributed.jsonl` with
`license_decision: review_required` and they must not enter a cut. Recording them is not
the same as clearing them -- it is the honest alternative to pretending they are fine
(rule: unknown is never converted to approved) and to silently re-downloading duplicates.

    py -3.11 scripts/reindex_archive_shelf.py --dry-run --limit 200   # look first
    py -3.11 scripts/reindex_archive_shelf.py                          # write the ledger
    py -3.11 scripts/reindex_archive_shelf.py --no-hash                # skip sha256 (fast, weaker dedup)

Resumable: a file already present in the ledger by (source, id) is skipped, so an
interrupted run costs nothing. Hashing 884 GB is the slow part; --no-hash trades
content-level dedup for speed and says so in every row it writes.
"""
from __future__ import annotations

import argparse
import atexit
import hashlib
import json
import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from typing import TextIO

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ingest_archive_sources import LEDGER_DIR, TIERS, atomic_append  # noqa: E402

VIDEO_EXT = {".mp4", ".mov", ".mkv", ".webm", ".m4v"}
IMAGE_EXT = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".webp", ".gif"}
AUDIO_EXT = {".mp3", ".wav", ".flac", ".m4a", ".aif", ".aiff", ".ogg"}

# Licence basis per source. This is a property of the SOURCE's terms, which is why it
# survives the loss of the per-item record. `review_required` is not a soft no -- nothing
# downstream may use it until a human clears it.
SOURCE_LICENCE: dict[str, tuple[str, str]] = {
    "mixkit":      ("pd", "Mixkit Free License -- free for commercial use, no attribution"),
    "coverr":      ("pd", "Coverr licence -- free for commercial use, no attribution"),
    "pixabay":     ("pd", "Pixabay Content License -- commercial use permitted"),
    "pixabay_extra": ("pd", "Pixabay Content License -- commercial use permitted "
                            "(the modern-web lane writes this prefix)"),
    "pexels":      ("pd", "Pexels License -- commercial use permitted"),
    "unsplash":    ("pd", "Unsplash License -- commercial use permitted"),
    "freesound":   ("review_required", "Freesound is PER-ITEM (CC0 / CC-BY / CC-BY-NC): "
                                       "the item licence must be re-read from the id"),
    "nasa":        ("pd", "NASA media is US public domain except logos and insignia"),
    "noaa":        ("pd", "NOAA media is US federal public domain"),
    "nara":        ("review_required", "NARA holdings are mixed: federal records are PD, "
                                       "donated materials may carry rights"),
    "loc":         ("review_required", "Library of Congress items carry per-item rights"),
    "ia":          ("review_required", "Internet Archive items carry per-item rights"),
    "wikimedia":   ("review_required", "Wikimedia files carry per-file licences"),
    "met":         ("pd", "The Met Open Access -- CC0"),
    "smithsonian": ("review_required", "Smithsonian Open Access is per-item"),
    "nypl":        ("review_required", "NYPL Digital Collections are per-item"),
}


def kind_of(ext: str) -> str | None:
    e = ext.lower()
    if e in VIDEO_EXT:
        return "video"
    if e in IMAGE_EXT:
        return "image"
    if e in AUDIO_EXT:
        return "audio"
    return None


def parse_name(name: str) -> tuple[str, str, str] | None:
    """`<source>__<id>__<slug>.<ext>` -> (source, id, title-ish slug). None if not ours."""
    stem = os.path.splitext(name)[0]
    parts = stem.split("__")
    if len(parts) < 3:
        return None
    src, ident = parts[0].strip().lower(), parts[1].strip()
    # `isalnum()` was wrong here and it cost 24,364 files. The ingest lane writes
    # `pixabay_extra__i_10240499__...`, and an underscore is not alnum, so every one of them
    # fell through to "unattributed" and was recorded as licence-unknown -- including the 473
    # small_town and ~900 government_buildings clips EP70 needs. The measurement then said the
    # shelf could not dress the episode, which was my instrument talking, not the shelf.
    if not src or not ident or not src.replace("_", "").isalnum():
        return None
    return src, ident, "__".join(parts[2:]).replace("-", " ").strip()


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def single_instance() -> None:
    """Refuse to start when another reindex is already writing this ledger.

    2026-08-20: two copies ran concurrently. Between them they appended 66,324 rows for
    60,572 files, tore 586 lines in half, and destroyed 117 files\x27 rows entirely -- the
    ledger looked FULLER than the shelf while holding less of it. Nothing in the repo
    launches this script, so the second copy was started from outside it; a guard that
    depends on the caller behaving would not have helped.
    """
    lock = Path(LEDGER_DIR) / "reindex.lock"
    os.makedirs(LEDGER_DIR, exist_ok=True)
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        raise SystemExit(
            f"[reindex] REFUSING TO START: {lock} exists, so another reindex is writing "
            f"this ledger. Two writers is exactly what corrupted it on 2026-08-20. If you "
            f"are certain none is running, delete that file and re-run.")
    os.write(fd, f"{os.getpid()}\n".encode())
    os.close(fd)
    atexit.register(lambda: lock.unlink(missing_ok=True))


def already_indexed() -> set[tuple[str, str]]:
    seen: set[tuple[str, str]] = set()
    d = Path(LEDGER_DIR)
    if not d.exists():
        return seen
    for f in d.glob("*.jsonl"):
        if f.name.startswith("rejects"):
            continue
        with f.open(encoding="utf-8") as fh:
            for line in fh:
                try:
                    r = json.loads(line)
                except Exception:
                    continue
                if r.get("source") and r.get("id") is not None:
                    seen.add((str(r["source"]), str(r["id"])))
    return seen


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="report only, write nothing")
    ap.add_argument("--limit", type=int, default=0, help="stop after N files (smoke test)")
    ap.add_argument("--no-hash", action="store_true",
                    help="skip sha256 -- much faster, but content-level dedup is lost "
                         "and every row it writes records that it was skipped")
    ap.add_argument("--workers", type=int, default=8)
    args = ap.parse_args()

    roots = [Path(t["root"]) for t in TIERS if Path(t["root"]).exists()]
    print(f"ledger : {LEDGER_DIR}")
    print(f"roots  : {', '.join(str(r) for r in roots) or 'NONE FOUND'}")
    if not roots:
        print("no archive root exists -- nothing to reindex")
        return 1

    if not args.dry_run:
        single_instance()
    seen = already_indexed()
    print(f"already in ledger: {len(seen)} item(s) -- these are skipped")

    files: list[Path] = []
    for r in roots:
        for p in r.rglob("*"):
            if p.is_file() and kind_of(p.suffix):
                files.append(p)
                if args.limit and len(files) >= args.limit:
                    break
        if args.limit and len(files) >= args.limit:
            break
    print(f"media files on the shelf: {len(files)}")

    stats = {"indexed": 0, "skipped": 0, "unattributed": 0}
    by_source: dict[str, int] = {}
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")

    def build(p: Path) -> dict | None:
        parsed = parse_name(p.name)
        theme = p.parent.name
        if parsed is None:
            src, ident, title = "unattributed", str(p.relative_to(p.anchor)), p.stem
            decision, basis = "review_required", (
                "no source prefix in the filename and the original ledger is gone: "
                "nothing identifies where this file came from")
        else:
            src, ident, title = parsed
            decision, basis = SOURCE_LICENCE.get(
                src, ("review_required", f"source {src!r} has no recorded licence basis"))
        if (src, ident) in seen:
            return None
        try:
            nbytes = p.stat().st_size
        except OSError:
            return None
        sha = "" if args.no_hash else sha256_of(p)
        return {
            "id": ident, "source": src, "source_url": "", "title": title,
            "license_field_raw": "", "license_decision": decision,
            "theme": theme, "file_path": str(p), "bytes": nbytes, "sha256": sha,
            "fetched_at": "", "relevance_score": 0, "matched_keywords": [],
            "reindexed_at": now,
            "reindex_basis": basis,
            "reindex_note": ("sha256 SKIPPED (--no-hash): this row cannot participate in "
                             "content-level dedup" if args.no_hash else
                             "sha256 computed from the file on disk at reindex time"),
        }

    # Rows are written AS THEY COMPLETE, not buffered to the end. The docstring above
    # promises that an interrupted run costs nothing, and that is only true if the rows it
    # already finished are on disk. Buffering 60k rows behind a multi-hour hash of 1.1 TB
    # across USB drives -- one of which died this week -- meant any interruption, and any
    # single unreadable file, threw the entire run away. Measured 2026-08-20.
    def emit(rec: dict) -> None:
        if args.dry_run:
            return
        os.makedirs(LEDGER_DIR, exist_ok=True)
        # ONE O_APPEND write per row, through the ingest lane's own helper rather than a
        # second implementation of it. A buffered handle tore 586 lines and lost 117 files'
        # rows outright on 2026-08-20, when two copies of this script appended to the same
        # ledger at the same time. `single_instance()` makes that impossible; this makes it
        # survivable if it ever happens again by another route.
        atomic_append(str(Path(LEDGER_DIR) / f"{rec['source']}.jsonl"),
                      json.dumps(rec, ensure_ascii=False))

    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        for rec in ex.map(build, files):
            if rec is None:
                stats["skipped"] += 1
                continue
            emit(rec)
            stats["indexed"] += 1
            by_source[rec["source"]] = by_source.get(rec["source"], 0) + 1
            if rec["source"] == "unattributed":
                stats["unattributed"] += 1
            if stats["indexed"] % 2000 == 0:
                print(f"  ... {stats['indexed']} indexed")

    print()
    print(f"{'source':<16}{'items':>8}  licence decision")
    for s in sorted(by_source, key=lambda k: -by_source[k]):
        dec = SOURCE_LICENCE.get(s, ("review_required", ""))[0] if s != "unattributed" \
            else "review_required"
        print(f"  {s:<14}{by_source[s]:>8}  {dec}")
    print()
    print(f"indexed {stats['indexed']}, already known {stats['skipped']}, "
          f"unattributed {stats['unattributed']}")

    if args.dry_run:
        print("\nDRY-RUN: nothing written.")
        return 0

    for src in sorted(by_source, key=lambda k: -by_source[k]):
        out = Path(LEDGER_DIR) / f"{src}.jsonl"
        print(f"wrote {by_source[src]:>7} row(s) -> {out}")
    print("\nThe ledger now describes the shelf. `ingest_archive_sources.py` will no "
          "longer re-download what is already here.")
    print("REMEMBER: review_required rows are NOT cleared for use. That includes every "
          "unattributed file.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
