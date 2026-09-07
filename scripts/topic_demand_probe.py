#!/usr/bin/env python3
"""Read-only: measure real YouTube demand + saturation for a candidate topic, via the Data API.

Four consecutive topic-selection sessions recorded saturation as "not re-measured" because
"YouTube blocks fetching" (TOPIC_PIPELINE.v004 §5.8, open gate 6). That is true of WebFetch and
false of the Data API, which we already hold credentials for. This script closes that gate.

Per query it reports, for the top search results:
  - view counts, duration, channel, age  -> DEMAND (does this premise carry?)
  - how many are >= 20 min               -> SATURATION (is the long-form slot already taken?)
  - distinct channels clearing a view bar -> R-36 TWO-CHANNEL PREMISE TEST

Quota: search.list is 100 units per query, videos.list 1. Default 10 queries = ~1,010 units of the
10,000/day default. No writes, no cost beyond quota.

    py -3.11 scripts/topic_demand_probe.py "surfside condo collapse" "camp fire pge paradise"
    py -3.11 scripts/topic_demand_probe.py --preset ep60
"""
from __future__ import annotations
import argparse, json, sys, urllib.parse, urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src")); sys.path.insert(0, str(ROOT / "scripts"))
from pd_factory.providers import load_env
from pd_factory.providers.youtube import _access_token

OUT = ROOT / "episodes" / "_planning" / "measurements" / "TOPIC_DEMAND_PROBE.json"
PRESETS = {
    "ep60": [
        # controls: the channel's own two biggest wins, to calibrate what "carries" looks like
        ("CONTROL Titan submersible", "titan submersible oceangate documentary"),
        ("CONTROL DB Cooper", "db cooper hijacking documentary"),
        # candidates
        ("Surfside collapse", "surfside condo collapse documentary"),
        ("PG&E Camp Fire", "pg&e camp fire paradise california documentary"),
        ("Upper Big Branch", "upper big branch mine disaster blankenship documentary"),
        ("Boeing 737 MAX", "boeing 737 max crashes documentary"),
        ("Guardianship / Fierle", "guardianship abuse elderly court documentary"),
        ("Delphi pensions", "delphi salaried retirees pension pbgc"),
    ],
}


def dur_sec(iso: str) -> int:
    s, n = 0, ""
    for c in iso[2:]:
        if c.isdigit():
            n += c
        else:
            s += int(n or 0) * {"H": 3600, "M": 60, "S": 1}.get(c, 0)
            n = ""
    return s


def main(argv):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("queries", nargs="*")
    ap.add_argument("--preset")
    ap.add_argument("--max", type=int, default=15, help="results per query")
    args = ap.parse_args(argv)

    pairs = PRESETS[args.preset] if args.preset else [(q, q) for q in args.queries]
    if not pairs:
        ap.error("give queries or --preset")

    tok = _access_token(load_env())
    H = {"Authorization": f"Bearer {tok}"}

    def api(url):
        with urllib.request.urlopen(urllib.request.Request(url, headers=H), timeout=60) as r:
            return json.loads(r.read().decode())

    now = datetime.now(timezone.utc)
    report = {}
    for label, q in pairs:
        s = api("https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&maxResults="
                f"{args.max}&order=relevance&q={urllib.parse.quote(q)}")
        ids = [i["id"]["videoId"] for i in s.get("items", [])]
        if not ids:
            print(f"\n### {label}: no results"); continue
        vs = api("https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id="
                 + ",".join(ids))["items"]
        rows = []
        for v in vs:
            secs = dur_sec(v["contentDetails"]["duration"])
            if secs < 180:
                continue  # ignore Shorts/news clips: we are sizing the LONG-FORM slot
            pub = datetime.fromisoformat(v["snippet"]["publishedAt"].replace("Z", "+00:00"))
            rows.append({"views": int(v["statistics"].get("viewCount", 0)), "sec": secs,
                         "ch": v["snippet"]["channelTitle"], "t": v["snippet"]["title"],
                         "days": max(1, (now - pub).days), "pub": pub.strftime("%Y-%m")})
        rows.sort(key=lambda r: -r["views"])
        longs = [r for r in rows if r["sec"] >= 20 * 60]
        big = [r for r in rows if r["views"] >= 100_000]
        chans = {r["ch"] for r in big}
        print(f"\n### {label}   (long-form results: {len(rows)})")
        print(f"    demand: median views {sorted(r['views'] for r in rows)[len(rows)//2]:,} | "
              f"max {rows[0]['views']:,} | >=100k: {len(big)} across {len(chans)} channels "
              f"-> two-channel test {'PASS' if len(chans) >= 2 else 'FAIL'}")
        print(f"    saturation: {len(longs)} result(s) >= 20 min"
              + (f" | biggest {longs[0]['views']:,} views ({longs[0]['sec']//60}m, {longs[0]['ch']})" if longs else ""))
        for r in rows[:6]:
            print(f"      {r['views']:>10,}  {r['sec']//60:>3}m  {r['pub']}  {r['ch'][:26]:<26} {r['t'][:44]}")
        report[label] = {"query": q, "rows": rows,
                         "two_channel_pass": len(chans) >= 2, "long_results": len(longs)}

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"measured_at": now.isoformat(), "topics": report},
                              ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nwrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
