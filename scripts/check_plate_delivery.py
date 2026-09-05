#!/usr/bin/env python3
"""Read the plates a generator has delivered so far and report every way they are not usable yet.

Run it repeatedly while a batch is being generated. It answers four questions that otherwise only
surface after the pool is built, or after a render:

  1. Which ordered plate ids have NOT arrived?
  2. Which delivered plates are the wrong ASPECT RATIO? A 16:9 film cannot use a 2.25:1 plate
     without cropping or pillarboxing it, and the crop is decided by whoever notices last.
  3. Which are under the resolution floor and therefore still need the upscale pass?
  4. Are there files in the delivery directory that the order never asked for?

Found on EP75 lahaina, 2026-08-21, at the second delivered plate: H002 arrived 1881x836 (2.25:1)
while every other plate arrived 1672x941 (16:9). One frame in 132, and it would have been a
letterbox in the finished film.

    py -3.11 scripts/check_plate_delivery.py --slug lahaina \
        --order episodes/_planning/EP75_lahaina_CODEX_BATCH_A.v001.md

Exit code is 0 when every DELIVERED plate is the right shape (missing plates are reported, not
failed -- a batch in progress is not a defect). Use --require-all to fail on missing ones too.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEDIA = Path("E:/pd-media/assets/ai")          # H: is gone; the media root moved to E: (2026-08)
FLOOR_LONG_EDGE = 3840
TARGET_AR = 16 / 9
AR_TOLERANCE = 0.02                            # 1.778 +- 2% still crops invisibly


def ordered_ids(order: Path) -> list[str]:
    rows = re.findall(r"^\|\s*([A-Z]{1,2}\d{2,3})\s*\|[^|]*\|[^|]+\|", order.read_text(encoding="utf-8"), re.M)
    seen, out = set(), []
    for r in rows:
        if r not in seen:
            seen.add(r)
            out.append(r)
    return out


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--order", required=True)
    ap.add_argument("--dir", help="delivery dir (default: E:/pd-media/assets/ai/<slug>)")
    ap.add_argument("--require-all", action="store_true", help="also fail when plates are missing")
    a = ap.parse_args()

    try:
        from PIL import Image
    except ImportError:
        print("[plates] FAIL Pillow is not installed; cannot read image dimensions")
        return 1

    want = ordered_ids(Path(a.order))
    d = Path(a.dir) if a.dir else MEDIA / a.slug
    if not d.is_dir():
        print(f"[plates] FAIL delivery directory does not exist: {d}")
        return 1

    delivered = {p.stem.upper(): p for p in sorted(d.glob("*.png"))}
    missing = [i for i in want if i not in delivered]
    unexpected = sorted(set(delivered) - set(want))

    bad_ar, under_floor, ok = [], [], []
    for pid in want:
        p = delivered.get(pid)
        if p is None:
            continue
        w, h = Image.open(p).size
        ar = w / h
        if abs(ar - TARGET_AR) / TARGET_AR > AR_TOLERANCE:
            bad_ar.append((pid, w, h, ar))
        elif max(w, h) < FLOOR_LONG_EDGE:
            under_floor.append((pid, w, h))
        else:
            ok.append(pid)

    print(f"[plates] {a.slug}: ordered {len(want)} | delivered {len(delivered)} | "
          f"missing {len(missing)}")
    if bad_ar:
        print(f"\n[plates] WRONG ASPECT RATIO -- {len(bad_ar)} plate(s). "
              f"A 16:9 film cannot use these without a crop nobody chose:")
        for pid, w, h, ar in bad_ar:
            print(f"   {pid}  {w}x{h}  = {ar:.3f}:1  (want {TARGET_AR:.3f}) -- REGENERATE at 16:9")
    if under_floor:
        print(f"\n[plates] under the {FLOOR_LONG_EDGE}px floor -- {len(under_floor)} plate(s). "
              f"Expected: Codex tops out at 1672x941. These need the Real-ESRGAN x4 -> LANCZOS "
              f"pass BEFORE they enter the pool, not after.")
        sizes = sorted({f"{w}x{h}" for _, w, h in under_floor})
        print(f"   sizes seen: {', '.join(sizes)}")
    if unexpected:
        print(f"\n[plates] NOT IN THE ORDER -- {len(unexpected)}: {', '.join(unexpected[:12])}")
    if missing:
        head = ", ".join(missing[:12])
        print(f"\n[plates] not delivered yet -- {len(missing)}: {head}"
              f"{' ...' if len(missing) > 12 else ''}")

    print(f"\n[plates] ready to enter the pool as delivered: {len(ok)}")
    bad = bool(bad_ar) or bool(unexpected) or (a.require_all and bool(missing))
    print(f"RESULT: {'FAIL' if bad else 'OK'} "
          f"({len(bad_ar)} wrong-aspect, {len(under_floor)} need upscale, "
          f"{len(unexpected)} unexpected, {len(missing)} missing)")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
