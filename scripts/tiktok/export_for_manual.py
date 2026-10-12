#!/usr/bin/env python3
"""Lay the TikTok queue out on the Desktop, numbered, for posting by hand.

Owner decision 2026-08-18: TikTok posting moves to manual. Automated posts through the
CDP-driven browser sat at 0 views while a phone-posted video on the same account got views, so
the machine stops touching TikTok and prepares material instead.

What it writes into one folder:

    001話.mp4, 002話.mp4, ...     the videos, in posting order
    カバー画像\\001話.png, ...      the cover for each - TikTok cannot add one after posting
    キャプション.txt               every caption, numbered to match

Anything already posted or scheduled (the ledger) is left out, so the numbering starts at the
next one to post and no video is offered twice.

Usage:
  py -3.11 scripts/tiktok/export_for_manual.py --check
  py -3.11 scripts/tiktok/export_for_manual.py --apply [--limit 40]
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path

QUEUE = Path("C:/temp/studio_auto/tt_queue.json")
LEDGER = Path("C:/temp/studio_auto/tt_clean_result.jsonl")
# NOT Path.home()/"Desktop": this machine\x27s Desktop is redirected to OneDrive, and the folder
# written to the old path was invisible to the owner. Read the real location from the registry.
def _desktop() -> Path:
    try:
        import winreg
        key = r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key) as k:
            raw, _ = winreg.QueryValueEx(k, "Desktop")
        return Path(os.path.expandvars(raw))
    except Exception:
        return Path.home() / "Desktop"


DEST = _desktop() / "TikTok投稿用"


def already_out() -> set[str]:
    done: set[str] = set()
    if LEDGER.exists():
        for line in LEDGER.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            if str(row.get("status", "")).startswith("SCHEDULED"):
                done.add(str(row["short"]).zfill(2))
    return done


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--limit", type=int, default=0, help="only the first N (0 = all)")
    a = ap.parse_args()
    if not a.apply and not a.check:
        ap.error("pass --check or --apply")

    queue = json.loads(QUEUE.read_text(encoding="utf-8"))
    done = already_out()
    todo = [q for q in queue if str(q["short"]).zfill(2) not in done]
    if a.limit:
        todo = todo[: a.limit]

    missing = [q["short"] for q in todo
               if not Path(q["file"]).exists() or not Path(q.get("cover", "")).exists()]
    size_gb = sum(Path(q["file"]).stat().st_size for q in todo if Path(q["file"]).exists()) / 1e9

    print(f"already posted or scheduled: {len(done)}")
    print(f"to hand over: {len(todo)}   about {size_gb:.1f} GB")
    print(f"destination: {DEST}")
    if missing:
        print(f"  MISSING video or cover: {missing[:10]}")
        return 1
    if a.check:
        print("(--check: nothing written)")
        return 0

    covers = DEST / "カバー画像"
    covers.mkdir(parents=True, exist_ok=True)
    lines = ["TikTok 投稿順リスト",
             "",
             "上から順に投稿してください。番号は動画のファイル名と同じです。",
             "カバー画像は「カバー画像」フォルダに同じ番号で入っています。",
             "投稿後にカバーは変更できないので、アップロード完了を待ってから設定してください。",
             ""]
    for i, q in enumerate(todo, start=1):
        name = f"{i:03d}話"
        # Hard links, not copies: Desktop and remotion/out are on the same volume, so this
        # costs 0 bytes instead of 7.8 GB on a drive that is 98% full. They behave like ordinary
        # files in Explorer and can be dragged into the TikTok uploader.
        for src, dst in ((q["file"], DEST / f"{name}.mp4"), (q["cover"], covers / f"{name}.png")):
            if dst.exists():
                dst.unlink()
            try:
                os.link(src, dst)
            except OSError:
                shutil.copy2(src, dst)
        lines.append("=" * 60)
        lines.append(f"{name}   （元: short{q['short']}）")
        lines.append("")
        lines.append(q["caption"])
        lines.append("")
        if i % 20 == 0:
            print(f"  ...{i}/{len(todo)}")
    (DEST / "キャプション.txt").write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {len(todo)} video(s), {len(todo)} cover(s) and キャプション.txt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
