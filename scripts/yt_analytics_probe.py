"""Read-only YouTube Analytics API probe. No cost, no writes.

Pulls the real analytics the Data API can't give: watch time, average view duration,
average view percentage (retention proxy), subscribers gained/lost, traffic sources,
device types, and per-video lifetime metrics. Impression CTR is Studio-only and not
available here. Secrets never printed. Writes scripts/_yt_analytics.json.

Usage: python scripts/yt_analytics_probe.py [START_DATE] [END_DATE]   (YYYY-MM-DD)
"""
from __future__ import annotations

import json
import sys
from datetime import date
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = ROOT / ".env"
OUT = Path(__file__).resolve().parent / "_yt_analytics.json"
START = sys.argv[1] if len(sys.argv) > 1 else "2026-06-01"
END = sys.argv[2] if len(sys.argv) > 2 else date.today().isoformat()


def load_env():
    env = {}
    for l in ENV_PATH.read_text(encoding="utf-8").splitlines():
        l = l.strip()
        if l and not l.startswith("#") and "=" in l:
            k, v = l.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def http(m, u, headers=None, form=None):
    data = urllib.parse.urlencode(form).encode() if form else None
    req = urllib.request.Request(u, data=data, method=m, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode() or "{}")


def query(auth, **params):
    base = "https://youtubeanalytics.googleapis.com/v2/reports?"
    params.setdefault("ids", "channel==MINE")
    params.setdefault("startDate", START)
    params.setdefault("endDate", END)
    return http("GET", base + urllib.parse.urlencode(params), headers=auth)


def show(title, status, body):
    print(f"\n=== {title} ===")
    if status != 200:
        print(f"  HTTP {status}: {json.dumps(body.get('error', body))[:300]}")
        return None
    heads = [h["name"] for h in body.get("columnHeaders", [])]
    rows = body.get("rows", [])
    print(f"  cols: {heads}")
    for r in rows[:50]:
        print("   " + "  ".join(str(x) for x in r))
    if not rows:
        print("   (no rows)")
    return {"cols": heads, "rows": rows}


def main():
    env = load_env()
    st, b = http("POST", "https://oauth2.googleapis.com/token", form={
        "client_id": env["YOUTUBE_CLIENT_ID"], "client_secret": env["YOUTUBE_CLIENT_SECRET"],
        "refresh_token": env["YOUTUBE_REFRESH_TOKEN"], "grant_type": "refresh_token"})
    if st != 200:
        print(f"TOKEN FAILED {st} {b.get('error')}")
        return 3
    auth = {"Authorization": f"Bearer {b['access_token']}"}
    print(f"window: {START} .. {END}")

    out = {}
    core = "views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,subscribersGained,subscribersLost,likes,comments,shares"
    out["channel_total"] = show("CHANNEL TOTAL", *query(auth, metrics=core))
    out["per_video"] = show("PER VIDEO (by views)", *query(
        auth, metrics=core, dimensions="video", sort="-views", maxResults=50))
    out["traffic"] = show("TRAFFIC SOURCES", *query(
        auth, metrics="views,estimatedMinutesWatched", dimensions="insightTrafficSourceType", sort="-views"))
    out["device"] = show("DEVICE TYPES", *query(
        auth, metrics="views", dimensions="deviceType", sort="-views"))
    out["country"] = show("TOP COUNTRIES", *query(
        auth, metrics="views,averageViewPercentage", dimensions="country", sort="-views", maxResults=15))
    out["daily"] = show("DAILY", *query(
        auth, metrics="views,subscribersGained", dimensions="day", sort="day"))
    out["sharing"] = show("SHARING SERVICE", *query(
        auth, metrics="shares", dimensions="sharingService", sort="-shares"))

    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nwrote {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
