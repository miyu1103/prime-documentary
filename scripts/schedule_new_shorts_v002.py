#!/usr/bin/env python3
"""Schedule shorts short46-49 (EP44-47) to YouTube (private + publishAt).

Coverfirst render (designed cover baked into first ~1.5s) uploaded PRIVATE with
status.publishAt; YouTube flips to public at that time. Sets the cover as the
custom thumbnail too. Idempotent/resumable: skips any short whose result file
exists OR whose title already appears on the channel (avoids the mid-batch
double-upload orphan pattern seen on EP40/EP41). Writes per-short result JSON.

    py -3.11 scripts/schedule_new_shorts_v001.py --dry-run
    py -3.11 scripts/schedule_new_shorts_v001.py
"""
from __future__ import annotations
import argparse, json, sys, time
import urllib.request, urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src")); sys.path.insert(0, str(ROOT / "scripts"))
from pd_factory.providers import load_env
from pd_factory.providers.youtube import _access_token
from upload_episode import upload_chunks  # verified resumable chunk uploader

CHANNEL_ALLOWLIST = {"UCuQPtAz1rca9eJ4xhvX0yKA"}
OUT = ROOT / "remotion" / "out"
THUMBS = ROOT / "runs" / "new_shorts" / "thumbs"
RESULTS = ROOT / "runs" / "new_shorts" / "schedule"
AI_LINE = ("\n\nThis video uses AI-assisted visualizations (symbolic reconstructions; "
           "no real person is depicted). Educational summary of a public court case.")

SHORTS = [
    {"n": 46, "publishAt": "2026-08-08T03:00:00Z",
     "title": "Police Skipped His Rights. Then He Learned He Couldn't Sue. #Shorts",
     "desc": "Vega v. Tekoh (2022), 6-3: a Miranda warning skipped by police is not, by itself, something you can sue the officer over under Section 1983. Miranda still stands; unwarned words can still be kept out of your trial."},
    {"n": 47, "publishAt": "2026-08-09T03:00:00Z",
     "title": "She Was Jailed for Being Too Poor to Pay a Fine #Shorts",
     "desc": "Jailing someone only because they cannot afford a fine has been unconstitutional since Bearden v. Georgia (1983). Yet it continued. What finally freed Harriet Cleveland was a lower-court settlement in 2014, not the Supreme Court."},
    {"n": 48, "publishAt": "2026-08-10T03:00:00Z",
     "title": "Your School Doesn't Need a Warrant to Search Your Bag #Shorts",
     "desc": "New Jersey v. T.L.O. (1985), 6-3: the Fourth Amendment DOES apply at school, but the Court lowered the bar to reasonable suspicion, no warrant and no probable cause required."},
    {"n": 49, "publishAt": "2026-08-11T03:00:00Z",
     "title": "She Was Jailed Over a Seatbelt. The Court Said It's Legal. #Shorts",
     "desc": "Gail Atwater was handcuffed and jailed over a $50 seatbelt fine. In Atwater v. Lago Vista (2001), the Supreme Court upheld the arrest as constitutional, 5-4. The remedy, it said, is up to lawmakers."},
]


def get_channel_id(tok):
    r = urllib.request.Request("https://www.googleapis.com/youtube/v3/channels?part=id&mine=true",
                               headers={"Authorization": f"Bearer {tok}"})
    with urllib.request.urlopen(r, timeout=60) as resp:
        return json.loads(resp.read().decode())["items"][0]["id"]


def channel_titles(tok):
    r = urllib.request.Request("https://www.googleapis.com/youtube/v3/channels?part=contentDetails&mine=true",
                               headers={"Authorization": f"Bearer {tok}"})
    up = json.loads(urllib.request.urlopen(r, timeout=60).read().decode())["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    titles = {}
    tokp = ""
    while True:
        u = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&playlistId={up}" + (f"&pageToken={tokp}" if tokp else "")
        d = json.loads(urllib.request.urlopen(urllib.request.Request(u, headers={"Authorization": f"Bearer {tok}"}), timeout=60).read().decode())
        for it in d["items"]:
            titles[it["snippet"]["title"]] = it["snippet"]["resourceId"]["videoId"]
        tokp = d.get("nextPageToken")
        if not tokp:
            break
    return titles


def initiate(tok, meta, size):
    body = json.dumps({"snippet": {"title": meta["title"], "description": meta["desc"] + AI_LINE,
        "tags": ["Shorts", "law", "true crime", "supreme court"], "categoryId": "27",
        "defaultLanguage": "en", "defaultAudioLanguage": "en"},
        "status": {"privacyStatus": "private", "selfDeclaredMadeForKids": False,
                   "containsSyntheticMedia": True}}).encode()
    r = urllib.request.Request(
        "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status",
        data=body, headers={"Authorization": f"Bearer {tok}", "Content-Type": "application/json",
        "X-Upload-Content-Type": "video/mp4", "X-Upload-Content-Length": str(size)}, method="POST")
    with urllib.request.urlopen(r, timeout=30) as resp:
        return resp.headers.get("Location", "")


def set_thumb(tok, vid, path):
    r = urllib.request.Request(f"https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId={vid}",
        data=path.read_bytes(), headers={"Authorization": f"Bearer {tok}", "Content-Type": "image/png"}, method="POST")
    with urllib.request.urlopen(r, timeout=120) as resp:
        return json.loads(resp.read().decode())


def schedule(tok, vid, when):
    body = json.dumps({"id": vid, "status": {"privacyStatus": "private", "publishAt": when,
        "selfDeclaredMadeForKids": False}}).encode()
    r = urllib.request.Request("https://www.googleapis.com/youtube/v3/videos?part=status", data=body,
        headers={"Authorization": f"Bearer {tok}", "Content-Type": "application/json"}, method="PUT")
    with urllib.request.urlopen(r, timeout=60) as resp:
        return json.loads(resp.read().decode())


def main(argv):
    try: sys.stdout.reconfigure(encoding="utf-8")
    except Exception: pass
    ap = argparse.ArgumentParser(); ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)
    RESULTS.mkdir(parents=True, exist_ok=True)

    # preflight
    for s in SHORTS:
        v = OUT / f"short{s['n']}_yt_coverfirst.mp4"; t = THUMBS / f"short{s['n']}.png"
        if not v.exists(): print(f"BLOCKED: missing {v}"); return 1
        if not t.exists() or t.stat().st_size > 2_000_000: print(f"BLOCKED: thumb {t} missing/oversized"); return 1
    tok = _access_token(load_env())
    ch = get_channel_id(tok)
    if ch not in CHANNEL_ALLOWLIST: print(f"BLOCKED: channel {ch} not allowlisted"); return 1
    print(f"OK channel {ch}")
    existing = channel_titles(tok)

    if args.dry_run:
        for s in SHORTS:
            dup = " [ALREADY ON CHANNEL - would skip]" if s["title"] in existing else ""
            print(f"  [dry] short{s['n']} -> {s['publishAt']}  {s['title'][:45]}{dup}")
        print("[dry-run] no uploads."); return 0

    done = []
    for s in SHORTS:
        n = s["n"]; resfile = RESULTS / f"short{n}.result.json"
        if resfile.exists():
            print(f"  short{n}: result exists, skip"); done.append(json.loads(resfile.read_text())); continue
        if s["title"] in existing:
            vid = existing[s["title"]]
            print(f"  short{n}: title already on channel as {vid}, finalizing (thumb+schedule)")
        else:
            v = OUT / f"short{n}_yt_coverfirst.mp4"; size = v.stat().st_size
            print(f"  short{n}: uploading {size/1e6:.0f}MB private ...")
            up = initiate(tok, s, size)
            if not up.startswith("https://www.googleapis.com/"): print(f"  FAIL bad upload url"); continue
            vid = upload_chunks(up, tok, v)
            if not vid: print(f"  FAIL no video_id"); continue
            print(f"  short{n}: uploaded {vid}")
        try: set_thumb(tok, vid, THUMBS / f"short{n}.png"); tset = True; print(f"  short{n}: thumb set")
        except Exception as e: tset = False; print(f"  short{n}: WARN thumb {str(e)[:80]}")
        try: schedule(tok, vid, s["publishAt"]); print(f"  short{n}: scheduled {s['publishAt']}")
        except Exception as e:
            time.sleep(5); schedule(tok, vid, s["publishAt"]); print(f"  short{n}: scheduled {s['publishAt']} (retry)")
        res = {"short": n, "video_id": vid, "watch": f"https://youtu.be/{vid}", "title": s["title"],
               "publishAt": s["publishAt"], "privacy": "private", "thumbnail_set": tset,
               "channel_id": ch, "coverfirst": True}
        resfile.write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
        done.append(res); time.sleep(1)

    print(f"\nDONE: {len(done)}/6 shorts scheduled.")
    for d in done: print(f"  short{d['short']}: {d['watch']}  {d['publishAt']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
