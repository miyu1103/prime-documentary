"""YouTube hook-health check. Read-only, no cost, no external writes.

Measures EARLY retention (the first ~30 seconds) for every long-form video,
using the Analytics `audienceRetention` report, and flags the videos whose
opening loses viewers faster than comparable videos.

Why: measured 2026-07-13, long-form APV is ~19% but the whole loss happens in
the first ~30s (viewers who survive the intro watch fine). So the lever is the
opening, and this tool makes that measurable on every video, every time.

Per video it reports:
- rel_perf_30s      : mean relativeRetentionPerformance over the first 30s.
                      0.50 = median of similar videos; below that = weak opening.
- watch_ratio_30s   : fraction of viewers still watching at ~30s.
- steepest_drop_pt  : largest single-bucket viewer drop before the 30s mark.

Verdict floors (owner 2026-07-13):
- rel_perf_30s      >= 0.50   else FAIL (opening below peer median)
- steepest_drop_pt  <= 15     else FAIL (a cliff inside the first 30s)

Usage:
    python scripts/yt_hook_health.py [START] [END]   (YYYY-MM-DD; default = channel start .. today)
    python scripts/yt_hook_health.py --video VIDEO_ID [START] [END]

Writes scripts/_yt_hook_health.json
"""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = ROOT / ".env"
OUT = Path(__file__).resolve().parent / "_yt_hook_health.json"

# --- verdict floors (owner 2026-07-13) ---
REL_PERF_FLOOR = 0.50      # first-30s relativeRetentionPerformance must be >= median
DROP_FLOOR_PT = 15.0       # no single viewer drop > 15 points before the 30s mark
LONGFORM_MIN_SEC = 90      # shorts are excluded
WINDOW_SEC = 30.0          # "the opening" = first 30 seconds


def load_env() -> dict:
    env = {}
    for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def access_token(env: dict) -> str:
    body = urllib.parse.urlencode({
        "client_id": env["YOUTUBE_CLIENT_ID"],
        "client_secret": env["YOUTUBE_CLIENT_SECRET"],
        "refresh_token": env["YOUTUBE_REFRESH_TOKEN"],
        "grant_type": "refresh_token",
    }).encode()
    r = json.load(urllib.request.urlopen("https://oauth2.googleapis.com/token", body, timeout=30))
    return r["access_token"]


def api_get(url: str, token: str) -> dict:
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=45) as resp:
        return json.loads(resp.read().decode())


def iso_seconds(iso: str) -> int:
    """PT#M#S -> seconds (durations here are minutes/seconds)."""
    import re
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso or "")
    if not m:
        return 0
    h, mi, s = (int(x) if x else 0 for x in m.groups())
    return h * 3600 + mi * 60 + s


def list_videos(token: str, start: str, end: str) -> list[dict]:
    """All videos with views in the window (video id + views), most-viewed first."""
    p = urllib.parse.urlencode({
        "ids": "channel==MINE", "startDate": start, "endDate": end,
        "metrics": "views", "dimensions": "video",
        "sort": "-views", "maxResults": "200",
    })
    data = api_get("https://youtubeanalytics.googleapis.com/v2/reports?" + p, token)
    return [{"id": row[0], "views": row[1]} for row in data.get("rows", [])]


def durations(token: str, ids: list[str]) -> dict:
    out = {}
    for i in range(0, len(ids), 50):
        batch = ids[i:i + 50]
        url = ("https://www.googleapis.com/youtube/v3/videos"
               "?part=contentDetails,snippet&id=" + ",".join(batch))
        for it in api_get(url, token).get("items", []):
            out[it["id"]] = {
                "sec": iso_seconds(it["contentDetails"]["duration"]),
                "title": it["snippet"]["title"],
            }
    return out


def retention_curve(token: str, vid: str, start: str, end: str) -> list[list]:
    p = urllib.parse.urlencode({
        "ids": "channel==MINE", "startDate": start, "endDate": end,
        "metrics": "audienceWatchRatio,relativeRetentionPerformance",
        "dimensions": "elapsedVideoTimeRatio", "filters": "video==" + vid,
    })
    try:
        data = api_get("https://youtubeanalytics.googleapis.com/v2/reports?" + p, token)
    except urllib.error.HTTPError:
        return []
    return sorted(data.get("rows", []), key=lambda r: r[0])


def analyze(rows: list[list], dur_sec: int) -> dict | None:
    """rows: [elapsedRatio, watchRatio, relPerf]. Returns hook metrics or None."""
    if not rows or dur_sec <= 0:
        return None
    window = max(WINDOW_SEC / dur_sec, 0.03)  # keep a few buckets even for long videos
    win = [r for r in rows if r[0] <= window]
    if len(win) < 3:
        win = rows[:4]
    watch_30 = min(win, key=lambda r: abs(r[0] - WINDOW_SEC / dur_sec))[1]
    rels = [r[2] for r in win if len(r) > 2 and r[2] is not None]
    rel_perf_30 = sum(rels) / len(rels) if rels else None
    steepest = 0.0
    at = 0.0
    for a, b in zip(win, win[1:]):
        d = a[1] - b[1]
        if d > steepest:
            steepest, at = d, b[0]
    return {
        "watch_ratio_30s": round(watch_30, 3),
        "rel_perf_30s": round(rel_perf_30, 3) if rel_perf_30 is not None else None,
        "steepest_drop_pt": round(steepest * 100, 1),
        "steepest_drop_at_sec": int(at * dur_sec),
    }


def verdict(m: dict) -> str:
    if m.get("rel_perf_30s") is None:
        return "NO_DATA"
    fails = []
    if m["rel_perf_30s"] < REL_PERF_FLOOR:
        fails.append("weak-opening")
    if m["steepest_drop_pt"] > DROP_FLOOR_PT:
        fails.append("early-cliff")
    return "PASS" if not fails else "FAIL(" + ",".join(fails) + ")"


def main() -> int:
    args = [a for a in sys.argv[1:]]
    only = None
    if "--video" in args:
        i = args.index("--video")
        only = args[i + 1]
        del args[i:i + 2]
    start = args[0] if len(args) > 0 else "2026-06-01"
    end = args[1] if len(args) > 1 else date.today().isoformat()

    env = load_env()
    token = access_token(env)

    vids = list_videos(token, start, end)
    if only:
        vids = [v for v in vids if v["id"] == only] or [{"id": only, "views": 0}]
    meta = durations(token, [v["id"] for v in vids])

    results = []
    for v in vids:
        d = meta.get(v["id"], {})
        if d.get("sec", 0) < LONGFORM_MIN_SEC:
            continue
        rows = retention_curve(token, v["id"], start, end)
        m = analyze(rows, d["sec"])
        rec = {
            "video": v["id"], "title": d.get("title", ""),
            "views": v["views"], "duration_sec": d.get("sec", 0),
        }
        if m:
            rec.update(m)
        rec["verdict"] = verdict(m) if m else "NO_DATA"
        results.append(rec)

    results.sort(key=lambda r: -r["views"])
    payload = {
        "window": f"{start} .. {end}",
        "floors": {"rel_perf_30s>=": REL_PERF_FLOOR, "steepest_drop_pt<=": DROP_FLOOR_PT},
        "videos": results,
    }
    tmp = OUT.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(tmp, OUT)

    print(f"HOOK HEALTH — first {int(WINDOW_SEC)}s  ({start} .. {end})")
    print(f"floors: rel_perf_30s >= {REL_PERF_FLOOR}, steepest drop <= {DROP_FLOOR_PT}pt\n")
    print(f"{'views':>5}  {'rel30':>5}  {'keep30':>6}  {'drop':>5}  verdict   title")
    n_fail = 0
    for r in results:
        if r["verdict"].startswith("FAIL"):
            n_fail += 1
        rel = f"{r.get('rel_perf_30s'):.2f}" if r.get("rel_perf_30s") is not None else "  -"
        keep = f"{r.get('watch_ratio_30s'):.2f}" if r.get("watch_ratio_30s") is not None else "  -"
        drop = f"{r.get('steepest_drop_pt'):.0f}pt" if r.get("steepest_drop_pt") is not None else " -"
        print(f"{r['views']:5}  {rel:>5}  {keep:>6}  {drop:>5}  {r['verdict']:<9} {r['title'][:44]}")
    print(f"\n{n_fail}/{len([r for r in results if r['verdict']!='NO_DATA'])} measured videos FAIL the hook floor.")
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
