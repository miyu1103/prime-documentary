#!/usr/bin/env python3
"""Per long-form, where its views came from -- the table that decides whether the related links work.

The table in `docs/PD_SHORTS_RELATED_VIDEO_LINKING.v001.md` (views / REL / SUB / SRCH / SHRT, and
`SHRT` zero on all twelve episodes) had no script behind it: it was assembled by hand on
2026-08-07 and the number that mattered could not be re-measured. This is that table, as a command.

The query the channel-level report cannot do: `dimensions=insightTrafficSourceType` combined with
`dimensions=video` is rejected (HTTP 400), so each long-form is asked for separately with
`filters=video==<id>`. That is one Analytics request per episode -- the Analytics API does not
draw on the 10,000-unit Data API budget.

Read this after the related links are set:

    py -3.11 scripts/studio/measure_shorts_to_longform.py 2026-08-07 2026-08-16

`SHRT` is views whose traffic source is the Shorts feed. `REL` is the related-video surface, which
is where a Short's related link sends a viewer. Both were the target of the linking work; either
one moving off zero settles it.

NOTE ON LAG: YouTube Analytics runs about two days behind. A window whose end date is today or
yesterday comes back empty and looks like a catastrophic result. Measured 2026-08-09: the window
08-07..08-09 returned no rows at all while 08-01..08-07 returned a full report.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from pd_factory.providers import load_env                    # noqa: E402
from pd_factory.providers.youtube import _access_token       # noqa: E402

API = "https://youtubeanalytics.googleapis.com/v2/reports"
WORKLIST_V002 = ROOT / "runs" / "_cache" / "related_link_worklist.v002.json"
WORKLIST_V001 = ROOT / "runs" / "_cache" / "related_link_worklist.json"
COLS = [("REL", "RELATED_VIDEO"), ("SHRT", "SHORTS"), ("SUB", "SUBSCRIBER"),
        ("SRCH", "YT_SEARCH"), ("EXT", "EXT_URL"), ("PL", "PLAYLIST")]


def query(tok: str, **params) -> dict:
    params.setdefault("ids", "channel==MINE")
    req = urllib.request.Request(API + "?" + urllib.parse.urlencode(params),
                                 headers={"Authorization": f"Bearer {tok}"})
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return {"error": e.read().decode()[:200]}


def destinations() -> dict[str, str]:
    """long-form id -> title, taken from whichever worklist exists. Never a typed list."""
    out: dict[str, str] = {}
    if WORKLIST_V002.exists():
        for r in json.loads(WORKLIST_V002.read_text(encoding="utf-8"))["eligible"]:
            out[r["longform_video_id"]] = r["longform_title"]
    elif WORKLIST_V001.exists():
        for r in json.loads(WORKLIST_V001.read_text(encoding="utf-8")):
            if r.get("longform_video_id"):
                out[r["longform_video_id"]] = r["longform_title"]
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("start", nargs="?", default="2026-08-07")
    ap.add_argument("end", nargs="?", default=(date.today() - timedelta(days=2)).isoformat())
    args = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    tok = _access_token(load_env())
    dests = destinations()
    if not dests:
        sys.exit("no worklist found - run scripts/studio/build_related_link_worklist.py first")
    print(f"window {args.start} .. {args.end}   {len(dests)} long-form destinations\n")
    print(f"{'views':>6}" + "".join(f"{c:>6}" for c, _ in COLS) + "  long-form")

    totals = {c: 0 for c, _ in COLS}
    grand = 0
    rows_out = []
    for vid, title in dests.items():
        r = query(tok, startDate=args.start, endDate=args.end, metrics="views",
                  dimensions="insightTrafficSourceType", filters=f"video=={vid}", sort="-views")
        if "error" in r:
            print(f"{'ERR':>6}{'':>36}  {vid} {r['error'][:60]}")
            continue
        by = {row[0]: row[1] for row in r.get("rows", [])}
        views = sum(by.values())
        grand += views
        for c, k in COLS:
            totals[c] += by.get(k, 0)
        rows_out.append((views, by, vid, title))

    for views, by, vid, title in sorted(rows_out, key=lambda x: -x[0]):
        print(f"{views:>6}" + "".join(f"{by.get(k, 0):>6}" for _, k in COLS) + f"  {title[:52]}")
    print(f"{grand:>6}" + "".join(f"{totals[c]:>6}" for c, _ in COLS) + "  TOTAL")

    if grand == 0:
        print("\nEvery row is zero. Before reading anything into that: Analytics lags about two "
              "days, so an end date inside the last 48 hours returns an empty report.")
    print(f"\nSHRT total {totals['SHRT']}  REL total {totals['REL']}"
          "   <- these were 0 and 578 respectively before the related links were set")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
