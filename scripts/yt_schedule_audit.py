"""Read-only: list every upload's scheduled publishAt from the LIVE channel (source of truth).

No writes, no cost, no publish. Prints all scheduled/future publishAt sorted, plus the
LAST reservation and the next open days (1 video/day at 12:00 JST rule). Secrets never printed.
"""
from __future__ import annotations
import json, sys, urllib.parse, urllib.request, urllib.error
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENV = ROOT / ".env"
JST = timezone(timedelta(hours=9))


def load_env():
    env = {}
    for l in ENV.read_text("utf-8").splitlines():
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


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    env = load_env()
    st, b = http("POST", "https://oauth2.googleapis.com/token", form={
        "client_id": env["YOUTUBE_CLIENT_ID"], "client_secret": env["YOUTUBE_CLIENT_SECRET"],
        "refresh_token": env["YOUTUBE_REFRESH_TOKEN"], "grant_type": "refresh_token"})
    if st != 200:
        print("TOKEN FAILED", st); return 3
    auth = {"Authorization": f"Bearer {b['access_token']}"}

    # Every video, from the shared unioned index. A schedule audit that cannot see a video will
    # report an empty slot on a day that is actually full (uploads playlist hid 9 on 2026-08-03).
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from yt_channel_index import list_video_ids
    ids = list_video_ids(auth)

    rows = []
    for i in range(0, len(ids), 50):
        chunk = ",".join(ids[i:i + 50])
        st, vs = http("GET", f"https://www.googleapis.com/youtube/v3/videos?part=snippet,status&id={chunk}", headers=auth)
        for v in vs.get("items", []):
            stt = v.get("status", {})
            rows.append({
                "id": v["id"],
                "title": v["snippet"]["title"][:52],
                "privacy": stt.get("privacyStatus"),
                "publishAt": stt.get("publishAt"),
            })

    sched = [r for r in rows if r["publishAt"]]
    def jst(iso):
        return datetime.fromisoformat(iso.replace("Z", "+00:00")).astimezone(JST)
    sched.sort(key=lambda r: r["publishAt"])
    print(f"total uploads={len(rows)}  scheduled(publishAt set)={len(sched)}")
    print("\n=== SCHEDULED (publishAt, JST) ===")
    for r in sched:
        print(f"  {jst(r['publishAt']):%Y-%m-%d %H:%M} JST  [{r['privacy']:8s}] {r['title']}")
    if sched:
        last = jst(sched[-1]["publishAt"])
        print(f"\nLAST reservation: {last:%Y-%m-%d %H:%M} JST  ({sched[-1]['title']})")
        # next open days at 12:00 JST after the last (1/day rule)
        taken = {jst(r["publishAt"]).date() for r in sched}
        d = last.date() + timedelta(days=1)
        openings = []
        while len(openings) < 8:
            if d not in taken:
                openings.append(d)
            d += timedelta(days=1)
        print("next open days (12:00 JST): " + ", ".join(x.strftime("%m/%d(%a)") for x in openings))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
