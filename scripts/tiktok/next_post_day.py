#!/usr/bin/env python3
"""Print the next day that TikTok posting should fill, as YYYY-MM-DD.

The day after the last day already in the ledger - not "tomorrow". A day whose run failed stays
unfilled, and asking for tomorrow every morning would step over it and never come back.

If the ledger is empty, or holds no successful post, the answer is today: a fresh account has
nothing scheduled and the current day's slots are the first ones to use.
"""
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

LEDGER = Path("C:/temp/studio_auto/tt_clean_result.jsonl")


def main() -> int:
    days: list[str] = []
    if LEDGER.exists():
        for line in LEDGER.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            if row.get("status") == "SCHEDULED" and row.get("when"):
                days.append(str(row["when"]).split(" ")[0])
    if not days:
        print(dt.date.today().isoformat())
        return 0
    print((dt.date.fromisoformat(max(days)) + dt.timedelta(days=1)).isoformat())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
