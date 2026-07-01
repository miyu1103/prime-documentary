"""Read-only FULL audit of every video on the channel. No cost, no writes, no publish.

Pulls all uploads and dumps, per video, the fields that matter for two goals:
  (1) BAN/safety risk  -> uploadStatus, rejectionReason, failureReason,
                          madeForKids, license, privacyStatus
  (2) growth           -> title/description/tags presence, captions, category,
                          duration, views/likes/comments
Outputs human-readable lines AND a JSON blob to scripts/_yt_audit.json for follow-up.
Secrets are never printed.
"""
from __future__ import annotations

import json
import sys
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
OUT_PATH = Path(__file__).resolve().parent / "_yt_audit.json"


def load_env() -> dict[str, str]:
    env: dict[str, str] = {}
    for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def http(method: str, url: str, *, headers=None, form=None):
    data = urllib.parse.urlencode(form).encode() if form else None
    req = urllib.request.Request(url, data=data, method=method, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode() or "{}")


def iso_dur(d: str) -> str:
    return (d or "").replace("PT", "").replace("H", "h").replace("M", "m").replace("S", "s")


def main() -> int:
    env = load_env()
    status, body = http(
        "POST",
        "https://oauth2.googleapis.com/token",
        form={
            "client_id": env["YOUTUBE_CLIENT_ID"],
            "client_secret": env["YOUTUBE_CLIENT_SECRET"],
            "refresh_token": env["YOUTUBE_REFRESH_TOKEN"],
            "grant_type": "refresh_token",
        },
    )
    if status != 200:
        print(f"TOKEN FAILED HTTP {status} {body.get('error')}")
        return 3
    auth = {"Authorization": f"Bearer {body['access_token']}"}

    _, ch = http(
        "GET",
        "https://www.googleapis.com/youtube/v3/channels"
        "?part=snippet,statistics,contentDetails,status,brandingSettings&mine=true",
        headers=auth,
    )
    item = ch["items"][0]
    uploads = item["contentDetails"]["relatedPlaylists"]["uploads"]
    print("=== CHANNEL ===")
    print(f"title       : {item['snippet'].get('title')}")
    print(f"desc set    : {bool(item['snippet'].get('description'))}")
    print(f"country     : {item['snippet'].get('country')}")
    print(f"subs        : {item['statistics'].get('subscriberCount')}")
    print(f"views       : {item['statistics'].get('viewCount')}")
    print(f"videoCount  : {item['statistics'].get('videoCount')}")
    print(f"madeForKids : {item.get('status', {}).get('madeForKids')}")
    kw = item.get("brandingSettings", {}).get("channel", {}).get("keywords")
    print(f"channel kw  : {kw}")

    # collect all uploads (paginate)
    ids: list[str] = []
    page = ""
    while True:
        _, pl = http(
            "GET",
            "https://www.googleapis.com/youtube/v3/playlistItems"
            f"?part=contentDetails&maxResults=50&playlistId={uploads}{page}",
            headers=auth,
        )
        ids += [v["contentDetails"]["videoId"] for v in pl.get("items", [])]
        tok = pl.get("nextPageToken")
        if not tok:
            break
        page = f"&pageToken={tok}"

    _, vd = http(
        "GET",
        "https://www.googleapis.com/youtube/v3/videos"
        "?part=snippet,status,statistics,contentDetails,processingDetails,topicDetails"
        f"&id={','.join(ids)}",
        headers=auth,
    )
    videos = vd.get("items", [])
    dump = []
    print(f"\n=== VIDEOS ({len(videos)}) ===")
    for v in videos:
        sn, st = v["snippet"], v["status"]
        stt, cd = v.get("statistics", {}), v.get("contentDetails", {})
        rec = {
            "id": v["id"],
            "title": sn.get("title"),
            "publishedAt": sn.get("publishedAt"),
            "privacy": st.get("privacyStatus"),
            "uploadStatus": st.get("uploadStatus"),
            "rejectionReason": st.get("rejectionReason"),
            "failureReason": st.get("failureReason"),
            "madeForKids": st.get("madeForKids"),
            "license": st.get("license"),
            "embeddable": st.get("embeddable"),
            "category": sn.get("categoryId"),
            "audioLang": sn.get("defaultAudioLanguage"),
            "tagsCount": len(sn.get("tags", []) or []),
            "descLen": len(sn.get("description", "") or ""),
            "caption": cd.get("caption"),
            "duration": iso_dur(cd.get("duration", "")),
            "views": stt.get("viewCount"),
            "likes": stt.get("likeCount"),
            "comments": stt.get("commentCount"),
            "topics": v.get("topicDetails", {}).get("topicCategories"),
        }
        dump.append(rec)
        flags = []
        if rec["uploadStatus"] not in ("processed", None):
            flags.append(f"UPLOAD={rec['uploadStatus']}")
        if rec["rejectionReason"]:
            flags.append(f"REJECTED={rec['rejectionReason']}")
        if rec["failureReason"]:
            flags.append(f"FAIL={rec['failureReason']}")
        if rec["tagsCount"] == 0:
            flags.append("NO_TAGS")
        if rec["descLen"] < 100:
            flags.append("SHORT_DESC")
        if rec["caption"] == "false":
            flags.append("NO_CAPTION")
        if not rec["audioLang"]:
            flags.append("NO_AUDIO_LANG")
        flagstr = ("  ⚠ " + " ".join(flags)) if flags else ""
        print(
            f"\n[{rec['privacy']:7}] {rec['publishedAt'][:10]}  {rec['duration']}  "
            f"views={rec['views']} likes={rec['likes']} comments={rec['comments']}"
        )
        print(f"   {rec['title']}  ({rec['id']})")
        print(
            f"   cat={rec['category']} lang={rec['audioLang']} tags={rec['tagsCount']} "
            f"desc={rec['descLen']}ch caption={rec['caption']} mfk={rec['madeForKids']} "
            f"license={rec['license']}{flagstr}"
        )

    OUT_PATH.write_text(json.dumps(dump, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nwrote {OUT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
