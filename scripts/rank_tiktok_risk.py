#!/usr/bin/env python3
"""Order the TikTok queue so the least risky posts go out first.

Four of the account's earlier posts were flagged as violations. Which four, and under which policy,
is not knowable from here - the posts were deleted and the record went with them - so this does not
try to guess the rule. It orders by the thing that is visible: how much of the caption is about
killing, bodies and executions, versus procedure and court rulings.

The point is not to avoid the risky ones. It is that if a flag comes back, it comes back early,
while there is still a decision to make about the rest.

Usage:
  py -3.11 scripts/rank_tiktok_risk.py --in C:/temp/studio_auto/tt_queue_full.json \
                                       --out C:/temp/studio_auto/tt_queue.json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# Weighted by how squarely each lands in a TikTok policy area, not by how unpleasant it sounds.
HEAVY = {
    "execut": 5, "death row": 5, "lethal": 5, "hanged": 5, "gas chamber": 5,
    "murder": 3, "killed": 3, "killing": 3, "stabb": 3, "shot": 3, "shooting": 3,
    "rape": 5, "assault": 3, "abuse": 3, "torture": 5, "beating": 3,
    "body": 2, "bodies": 2, "corpse": 3, "blood": 3, "autopsy": 3,
    "suicide": 5, "overdose": 3, "child": 2, "children": 2, "teen": 2,
    "gun": 2, "weapon": 2, "knife": 2, "drug": 2, "cocaine": 3, "heroin": 3,
}
LIGHT = {
    "warrant": -2, "supreme court": -2, "ruling": -2, "appeal": -2, "statute": -2,
    "evidence": -1, "testimony": -1, "jury": -1, "attorney": -1, "search": -1,
    "forfeiture": -2, "settlement": -2, "regulator": -2, "contract": -2,
}


def score(text: str) -> int:
    t = text.lower()
    s = 0
    for k, v in HEAVY.items():
        if re.search(r"\b" + k, t):
            s += v
    for k, v in LIGHT.items():
        if re.search(r"\b" + k, t):
            s += v
    return s


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="src", required=True)
    ap.add_argument("--out", dest="dst", required=True)
    ap.add_argument("--show", type=int, default=6)
    a = ap.parse_args()

    q = json.loads(Path(a.src).read_text(encoding="utf-8"))
    for item in q:
        item["risk"] = score(item.get("caption", ""))
    q.sort(key=lambda x: (x["risk"], x["short"]))
    Path(a.dst).write_text(json.dumps(q, ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"{len(q)} ordered by risk -> {a.dst}")
    print(f"\nfirst out (safest):")
    for i in q[: a.show]:
        print(f"  {i['risk']:>3}  short{i['short']}  {i['caption'].splitlines()[0][:64]}")
    print(f"\nlast out (riskiest):")
    for i in q[-a.show :]:
        print(f"  {i['risk']:>3}  short{i['short']}  {i['caption'].splitlines()[0][:64]}")
    over = [i for i in q if i["risk"] >= 8]
    print(f"\n{len(over)} at risk>=8 - look at these by hand before they go out")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
