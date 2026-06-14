#!/usr/bin/env python3
"""Local download sorter/watcher for Prime Documentary.

Watches an SSD inbox folder and, when a manual download (Midjourney / Suno / Runway)
finishes, renames it and moves it into images / music / video by file type. Local-only:
no network, no cost, no upload. Heavy media stays on the SSD (not in the git repo).

Run (keeps running):
    py scripts\\download_watcher.py
Stop with Ctrl+C.
"""
from __future__ import annotations

import logging
import shutil
import sys
import time
from datetime import datetime
from pathlib import Path

# SSD working area (machine-local; change here if the drive letter differs).
BASE = Path(r"H:\pd-media\downloads")
INBOX = BASE / "inbox"
DEST = {"image": BASE / "images", "music": BASE / "music", "video": BASE / "video"}
LOGDIR = BASE / "logs"

# Files still downloading — wait until they are gone/renamed by the browser.
TEMP_SUFFIXES = {".crdownload", ".part", ".tmp", ".download", ".partial", ".opdownload"}
EXT_KIND = {
    ".png": "image", ".jpg": "image", ".jpeg": "image", ".webp": "image",
    ".mp3": "music", ".wav": "music", ".m4a": "music", ".ogg": "music",
    ".mp4": "video", ".mov": "video", ".webm": "video",
}
PREFIX = {"image": "img", "music": "mus", "video": "vid"}
POLL_SECONDS = 2
STABLE_CHECKS = 2  # size must be unchanged this many polls before we treat it as complete


def classify(name: str) -> str | None:
    """Return 'image' / 'music' / 'video' from the extension, or None if unknown."""
    return EXT_KIND.get(Path(name).suffix.lower())


def is_temp(p: Path) -> bool:
    return p.suffix.lower() in TEMP_SUFFIXES or p.name.startswith("~")


def next_name(dest: Path, kind: str, ext: str, *, today: str) -> str:
    """Pick a non-colliding name like img_20260614_001.png (per type, per day)."""
    prefix = PREFIX[kind]
    ext = ext.lower()
    nums = []
    for p in dest.glob(f"{prefix}_{today}_*{ext}"):
        tail = p.stem.split("_")[-1]
        if tail.isdigit():
            nums.append(int(tail))
    n = (max(nums) + 1) if nums else 1
    return f"{prefix}_{today}_{n:03d}{ext}"


def _setup() -> None:
    for d in (INBOX, *DEST.values(), LOGDIR):
        d.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(message)s",
        handlers=[logging.FileHandler(LOGDIR / "watcher.log", encoding="utf-8"),
                  logging.StreamHandler(sys.stdout)],
    )


def run() -> None:
    _setup()
    logging.info("download watcher started. inbox=%s", INBOX)
    print(f"監視中: {INBOX}  （止めるには Ctrl+C）")
    seen: dict[Path, tuple[int, int]] = {}  # path -> (last_size, stable_count)
    while True:
        try:
            for p in list(INBOX.iterdir()):
                if not p.is_file() or is_temp(p):
                    continue
                try:
                    size = p.stat().st_size
                except OSError:
                    continue
                prev = seen.get(p)
                count = prev[1] + 1 if (prev and prev[0] == size) else 1
                seen[p] = (size, count)
                if count < STABLE_CHECKS:
                    continue  # still changing — wait
                kind = classify(p.name)
                if kind is None:
                    logging.info("skip (unknown type): %s", p.name)
                    seen.pop(p, None)
                    continue
                today = datetime.now().strftime("%Y%m%d")
                target = DEST[kind] / next_name(DEST[kind], kind, p.suffix, today=today)
                try:
                    shutil.move(str(p), str(target))
                    logging.info("moved: %s  ->  %s", p.name, target)
                except (PermissionError, OSError) as exc:
                    logging.info("locked, will retry: %s (%s)", p.name, exc)
                    continue
                seen.pop(p, None)
            for gone in [k for k in seen if not k.exists()]:
                seen.pop(gone, None)
            time.sleep(POLL_SECONDS)
        except KeyboardInterrupt:
            logging.info("download watcher stopped.")
            break
        except Exception as exc:  # keep running through transient errors
            logging.info("loop error: %s", exc)
            time.sleep(POLL_SECONDS)


if __name__ == "__main__":
    run()
