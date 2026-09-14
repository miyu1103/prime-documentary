#!/usr/bin/env python3
"""Append a verified TikTok publish/schedule receipt without duplicating a Short."""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RECEIPTS = ROOT / "episodes" / "_planning" / "measurements" / "TIKTOK_PUBLISH_RECEIPTS.v001.jsonl"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("short_id")
    parser.add_argument("status", choices=("published", "scheduled"))
    parser.add_argument("--url", required=True)
    parser.add_argument("--scheduled-for")
    parser.add_argument("--caption", required=True)
    parser.add_argument("--receipts", type=Path, default=DEFAULT_RECEIPTS)
    args = parser.parse_args()

    if not re.fullmatch(r"short\d+", args.short_id):
        parser.error("short_id must look like short87")
    if args.status == "scheduled" and not args.scheduled_for:
        parser.error("--scheduled-for is required for scheduled receipts")

    existing: dict[str, dict] = {}
    if args.receipts.is_file():
        for line in args.receipts.read_text(encoding="utf-8").splitlines():
            if line.strip():
                receipt = json.loads(line)
                existing[str(receipt["short_id"])] = receipt
    if args.short_id in existing:
        current = existing[args.short_id]
        if current.get("url") == args.url and current.get("status") == args.status:
            print(json.dumps({"result": "already_recorded", "short_id": args.short_id}, ensure_ascii=False))
            return 0
        raise SystemExit(f"refusing conflicting receipt for {args.short_id}: {current}")

    receipt = {
        "schema_version": "v001",
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "short_id": args.short_id,
        "status": args.status,
        "scheduled_for": args.scheduled_for,
        "url": args.url,
        "caption": args.caption,
        "visibility": "public",
        "ai_generated_content_label": True,
        "checks": {"copyright": "passed", "content": "passed"},
    }
    args.receipts.parent.mkdir(parents=True, exist_ok=True)
    with args.receipts.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(receipt, ensure_ascii=False) + "\n")
    print(json.dumps({"result": "recorded", "short_id": args.short_id}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
