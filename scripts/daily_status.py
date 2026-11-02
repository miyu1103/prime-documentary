#!/usr/bin/env python3
"""Where the daily publishing work stands, and the exact command to run next.

A hand-written status note goes stale the first time anything runs. This measures instead: file
counts on disk, the schedule result logs, and the live quota ledger. Run it after opening a new
session and it will say what to do.

It does not touch the channel or TikTok - reading only, no cost.

Usage:
  py -3.11 scripts/daily_status.py
"""
from __future__ import annotations

import datetime as dt
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "remotion" / "out"
DATA = ROOT / "remotion" / "src" / "data"
TT_DIR = Path("C:/temp/studio_auto")
JST = dt.timezone(dt.timedelta(hours=9))
TARGET = 195          # 65 episodes x 3 Shorts


def ids(pattern: str, glob: str, where: Path) -> set[str]:
    return {m.group(1) for p in where.glob(glob) if (m := re.match(pattern, p.stem))}


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    now = dt.datetime.now(JST)
    print(f"=== {now:%Y-%m-%d %H:%M} JST ===\n")

    made = ids(r"(short\d+)$", "short*.ts", DATA)
    made = {s for s in made if re.fullmatch(r"short\d+", s)}
    tt = ids(r"short(\d+)_tt$", "short*_tt.mp4", OUT)
    cov = ids(r"short(\d+)_ttcover$", "short*_ttcover.png", OUT)
    yt = ids(r"short(\d+)_yt_coverfirst$", "short*_yt_coverfirst.mp4", OUT)
    yt16 = {p.stem[5:] for p in (ROOT / "runs" / "shorts_thumbs" / "samples").glob("short*.png")}

    uploaded: set[str] = set()
    for f in ROOT.glob("episodes/*/09_package/short*_youtube_schedule_result.*.json"):
        d = json.loads(f.read_text(encoding="utf-8"))
        m = re.match(r"short(\d+)_youtube", f.name)
        if d.get("video_id") and m:
            uploaded.add(m.group(1))

    print(f"制作済みショート : {len(made)} / {TARGET}   (不足 {TARGET - len(made)})")
    print()
    print("YouTube")
    print(f"  レンダー済み   : {len(yt)}")
    print(f"  投稿/予約済み  : {len(uploaded)}     未投稿 {len(yt) - len(uploaded)}")
    print(f"  16:9サムネイル : {len(yt16)}")
    try:
        sys.path.insert(0, str(ROOT / "scripts"))
        import yt_quota
        left = yt_quota.remaining()
        can = left // yt_quota.UNITS["videos.insert"]
        print(f"  クォータ残     : {left}  → 今すぐ {can} 本  (回復は 16:00 JST)")
    except Exception as e:
        print(f"  クォータ       : 読めず ({e})")

    print()
    print("TikTok")
    print(f"  レンダー済み   : {len(tt)}")
    print(f"  カバー         : {len(cov)}")
    done, last = set(), None
    res = TT_DIR / "tt_clean_result.jsonl"
    if res.is_file():
        for line in res.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            if r.get("status") == "SCHEDULED":
                done.add(str(r["short"]))
                if r.get("when"):
                    last = max(last or r["when"], r["when"])
    q = TT_DIR / "tt_queue.json"
    queued = len(json.loads(q.read_text(encoding="utf-8"))) if q.is_file() else 0
    print(f"  キュー         : {queued}     予約済み {len(done)}     残り {queued - len(done)}")
    print(f"  最後の予約     : {last or '(none)'}")

    print("\n--- 次にやること ---")
    if last:
        d, t = last.split()
        day = dt.date.fromisoformat(d)
        slots = ["10:00", "14:00", "18:00", "22:00"]
        i = slots.index(t) + 1 if t in slots else 4
        if i >= 4:
            day, i = day + dt.timedelta(days=1), 0
        print(f"  TikTok  : node tt_batch_clean.js {day} {i} 6")
        print("            (cd /c/temp/studio_auto; 先に chrome を taskkill して start_chrome.js)")
        print("            埋まり具合は Studio の一覧で確認してから。公開グリッドは遅れる")
    else:
        print("  TikTok  : node tt_batch_clean.js <開始日> <埋まっている枠数> 6")
    print("  YouTube : bash scripts/daily_shorts_push.sh        (16:00 JST 以降)")
    print("\n  罠と作業のやり方 : docs/PD_CANON.md §7 §8")
    print("  このスレの記録   : docs/PD_RETRO_20260810_TIKTOK_AND_CALENDAR.v001.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
