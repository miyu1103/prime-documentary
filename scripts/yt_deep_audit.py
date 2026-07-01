"""Read-only DEEP audit using the youtube.force-ssl scope. No cost, no writes.

Pulls everything the current scope allows, per video:
  - full thumbnails set (is a maxres/custom thumb present?)
  - full tag list, full description
  - captions track list (languages, draft/autosync)  -> A/B & localization readiness
  - top comments (spam / sentiment / unanswered)
Plus channel-level: channelSections, playlists (binge/SEO structure).
Writes scripts/_yt_deep.json. Secrets never printed.
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
OUT = Path(__file__).resolve().parent / "_yt_deep.json"


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


def main():
    env = load_env()
    _, b = http("POST", "https://oauth2.googleapis.com/token", form={
        "client_id": env["YOUTUBE_CLIENT_ID"], "client_secret": env["YOUTUBE_CLIENT_SECRET"],
        "refresh_token": env["YOUTUBE_REFRESH_TOKEN"], "grant_type": "refresh_token"})
    auth = {"Authorization": f"Bearer {b['access_token']}"}

    _, ch = http("GET", "https://www.googleapis.com/youtube/v3/channels"
                 "?part=contentDetails,brandingSettings,snippet&mine=true", headers=auth)
    chitem = ch["items"][0]
    cid = chitem["id"]
    uploads = chitem["contentDetails"]["relatedPlaylists"]["uploads"]

    # channel structure
    _, secs = http("GET", f"https://www.googleapis.com/youtube/v3/channelSections?part=snippet&channelId={cid}", headers=auth)
    _, pls = http("GET", f"https://www.googleapis.com/youtube/v3/playlists?part=snippet,contentDetails&channelId={cid}&maxResults=50", headers=auth)
    print("=== CHANNEL STRUCTURE ===")
    print(f"channelSections : {len(secs.get('items', []))}")
    print(f"playlists       : {len(pls.get('items', []))}")
    for p in pls.get("items", []):
        print(f"  - {p['snippet']['title']} ({p['contentDetails']['itemCount']} items)")

    # all uploads
    ids = []
    page = ""
    while True:
        _, pl = http("GET", "https://www.googleapis.com/youtube/v3/playlistItems"
                     f"?part=contentDetails&maxResults=50&playlistId={uploads}{page}", headers=auth)
        ids += [v["contentDetails"]["videoId"] for v in pl.get("items", [])]
        tok = pl.get("nextPageToken")
        if not tok:
            break
        page = f"&pageToken={tok}"

    _, vd = http("GET", "https://www.googleapis.com/youtube/v3/videos"
                 f"?part=snippet,status,statistics&id={','.join(ids)}", headers=auth)

    dump = []
    for v in vd.get("items", []):
        vid = v["id"]
        sn = v["snippet"]
        thumbs = sn.get("thumbnails", {})
        # captions
        _, caps = http("GET", f"https://www.googleapis.com/youtube/v3/captions?part=snippet&videoId={vid}", headers=auth)
        cap_tracks = [{"lang": c["snippet"].get("language"), "name": c["snippet"].get("name"),
                       "kind": c["snippet"].get("trackKind"), "draft": c["snippet"].get("isDraft"),
                       "autosync": c["snippet"].get("isAutoSynced")} for c in caps.get("items", [])]
        # comments
        _, cm = http("GET", "https://www.googleapis.com/youtube/v3/commentThreads"
                     f"?part=snippet&maxResults=20&videoId={vid}", headers=auth)
        comments = []
        for t in cm.get("items", []):
            top = t["snippet"]["topLevelComment"]["snippet"]
            comments.append({"author": top.get("authorDisplayName"), "text": top.get("textDisplay"),
                             "likes": top.get("likeCount"), "replies": t["snippet"].get("totalReplyCount")})
        rec = {
            "id": vid, "title": sn.get("title"), "privacy": v["status"].get("privacyStatus"),
            "tags": sn.get("tags", []),
            "thumb_res": sorted(thumbs.keys()),
            "has_maxres": "maxres" in thumbs,
            "has_standard": "standard" in thumbs,
            "desc": sn.get("description", ""),
            "captions": cap_tracks,
            "comments": comments,
        }
        dump.append(rec)

    print(f"\n=== PER-VIDEO DEEP ({len(dump)}) ===")
    for r in dump:
        cap_langs = ",".join(f"{c['lang']}{'(asr)' if c['kind']=='asr' else ''}{'(draft)' if c['draft'] else ''}" for c in r["captions"]) or "NONE"
        print(f"\n[{r['privacy']:7}] {r['title'][:58]}  ({r['id']})")
        print(f"   thumbs={r['thumb_res']} maxres={r['has_maxres']}")
        print(f"   captions: {cap_langs}")
        print(f"   tags({len(r['tags'])}): {', '.join(r['tags'][:20])}")
        if r["comments"]:
            for c in r["comments"]:
                print(f"   💬 {c['author']}: {c['text'][:120]}  (likes={c['likes']} replies={c['replies']})")
        else:
            print("   💬 (no comments)")

    OUT.write_text(json.dumps(dump, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()
