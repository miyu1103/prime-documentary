#!/usr/bin/env python3
"""Add the TikTok variant composition for every Short that only has the YouTube one.

The two differ by one prop: platform 'yt' vs 'tiktok'. The Short component swaps the closing CTA
for it, because a TikTok card must not name another platform - "Watch the full case on the
channel" becomes "Full case on our profile". Everything else, including the kinetic beats and the
funnel card artwork, is identical.

75 of 140 finished Shorts had the variant; 98 did not, which is why only 22 TikTok files existed
on disk. The block is inserted straight after the Short's own -yt Composition so the file stays
grouped by Short rather than by platform.

Usage:
  py -3.11 scripts/register_tiktok_compositions.py --dry-run
  py -3.11 scripts/register_tiktok_compositions.py --apply
"""
from __future__ import annotations

import argparse
import py_compile
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RTX = ROOT / "remotion" / "src" / "Root.tsx"
OUT = ROOT / "remotion" / "out"


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    if not a.apply and not a.dry_run:
        ap.error("pass --apply or --dry-run")

    text = RTX.read_text(encoding="utf-8")
    have_tt = {int(m) for m in re.findall(r'id="Short-short(\d+)-tt"', text)}
    rendered = sorted({int(re.sub(r"\D", "", p.stem.split("_")[0]))
                       for p in OUT.glob("short*_yt_coverfirst.mp4")})
    todo = [n for n in rendered if n not in have_tt]
    print(f"{len(have_tt)} variants exist; {len(todo)} to add")

    added = []
    for n in todo:
        yt_tag = f'<Composition id="Short-short{n}-yt" component={{Short}}'
        if yt_tag not in text:
            print(f"  short{n}: no -yt composition to anchor to - skipped")
            continue
        start = text.index(yt_tag)
        end = text.index("/>", start) + 2
        block = text[start:end]
        # the variant is the same block with the platform prop swapped
        tt = (block.replace(f'id="Short-short{n}-yt"', f'id="Short-short{n}-tt"')
                   .replace("platform: 'yt' as const", "platform: 'tiktok' as const"))
        if "platform: 'tiktok'" not in tt:
            print(f"  short{n}: platform prop not found in the -yt block - skipped")
            continue
        text = text[:end] + "\n      " + tt + text[end:]
        added.append(n)

    print(f"{len(added)} added" + ("" if a.apply else "   (DRY RUN)"))
    if a.apply and added:
        RTX.write_text(text, encoding="utf-8")
        n_now = len(re.findall(r'id="Short-short(\d+)-tt"', RTX.read_text(encoding="utf-8")))
        print(f"wrote {RTX.relative_to(ROOT)} - {n_now} TikTok compositions")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
