"""List every private video's scheduled publish time. Read-only, no writes, no cost beyond quota.

The full audit dumps privacyStatus but not publishAt, so "is it actually scheduled or just
sitting private?" could not be answered from its output - and a private video with no publishAt
never goes public on its own. This asks status.publishAt directly.
"""
from __future__ import annotations

import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from yt_full_audit import http, load_env  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    env = load_env()
    st, body = http(
        "POST",
        "https://oauth2.googleapis.com/token",
        form={
            "client_id": env["YOUTUBE_CLIENT_ID"],
            "client_secret": env["YOUTUBE_CLIENT_SECRET"],
            "refresh_token": env["YOUTUBE_REFRESH_TOKEN"],
            "grant_type": "refresh_token",
        },
    )
    if st != 200:
        print(f"TOKEN FAILED HTTP {st}")
        return 3
    auth = {"Authorization": f"Bearer {body['access_token']}"}

    audit = json.loads((Path(__file__).resolve().parent / "_yt_audit.json").read_text(encoding="utf-8"))
    ids = [v["id"] for v in audit if v.get("privacy") == "private"]

    rows = []
    for i in range(0, len(ids), 50):
        chunk = ids[i : i + 50]
        _, r = http(
            "GET",
            "https://www.googleapis.com/youtube/v3/videos?part=status,snippet&id="
            + urllib.parse.quote(",".join(chunk)),
            headers=auth,
        )
        for it in r.get("items", []):
            rows.append(
                {
                    "id": it["id"],
                    "title": it["snippet"]["title"],
                    "publishAt": it["status"].get("publishAt"),
                }
            )

    scheduled = sorted([r for r in rows if r["publishAt"]], key=lambda r: r["publishAt"])
    stuck = [r for r in rows if not r["publishAt"]]
    for r in scheduled:
        print(f"{r['publishAt']}  {r['id']}  {r['title'][:60]}")
    print(f"\nscheduled={len(scheduled)}  private-with-no-date={len(stuck)}")
    for r in stuck:
        print(f"  UNSCHEDULED  {r['id']}  {r['title'][:60]}")
    out = ROOT / "runs" / "shorts_thumbs" / "yt_scheduled.v001.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"scheduled": scheduled, "unscheduled": stuck}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
