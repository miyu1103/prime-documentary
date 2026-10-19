#!/usr/bin/env python3
"""Set the thumbnail of ONE live video (thumbnails.set), with a receipt.

apply_thumbnails_v002.py carries the proven token/retry/set machinery but a hardcoded
four-episode target list -- the one-off shape invariant 14 exists to stop. This is the
generic door: one video, one file, dry-run by default, receipt on disk either way.

    py -3.11 scripts/set_video_thumbnail.py --video-id Xc_PxdC_75c \
        --file episodes/PD-2026-035-hinders/09_package/thumbnail.selected.v003.png
    ... --apply           # actually write (≈50 quota units)

Side effects (--apply only): one thumbnails.set call against the live channel.
Idempotent: setting the same image twice is harmless; the receipt records each call.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from apply_thumbnails_v002 import MAX_BYTES, get_thumbs, set_with_retry, token  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--video-id", required=True)
    ap.add_argument("--file", required=True, type=Path)
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()

    p = a.file if a.file.is_absolute() else ROOT / a.file
    if not p.is_file():
        print(f"missing file: {p}")
        return 2
    nbytes = p.stat().st_size
    if nbytes > MAX_BYTES:
        print(f"file is {nbytes} bytes > {MAX_BYTES} limit")
        return 2

    tok = token()
    before = get_thumbs(tok, a.video_id)
    if before is None:
        print(f"video {a.video_id} not found on the channel -- refusing")
        return 2
    print(f"video {a.video_id}: current maxres/high url present = "
          f"{bool(before.get('maxres') or before.get('high'))}")
    print(f"file: {p} ({nbytes/1024:.0f} KB)")

    receipt = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "video_id": a.video_id,
        "file": str(p),
        "bytes": nbytes,
        "mode": "apply" if a.apply else "dry-run",
        "before": {k: v.get("url") for k, v in before.items() if isinstance(v, dict)},
    }
    if a.apply:
        st, body = set_with_retry(tok, a.video_id, p.read_bytes())
        receipt["status_code"] = st
        receipt["response"] = body
        print(f"thumbnails.set -> HTTP {st}")
        ok = st == 200
    else:
        print("DRY-RUN: no API write. Re-run with --apply.")
        ok = True

    out = ROOT / "episodes" / "_planning" / (
        f"thumbnail_set_receipt.{a.video_id}."
        f"{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.json")
    out.write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    print(f"receipt: {out}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
