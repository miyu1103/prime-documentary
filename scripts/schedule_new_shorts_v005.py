#!/usr/bin/env python3
"""Schedule short52-59 (EP42/43/50/51/52/53/54/55 topics) to YouTube (private + publishAt).

Clone of schedule_new_shorts_v004.py, retargeted to the 8 new shorts. Uploads the
*_yt_coverfirst.mp4 renders (designed cover baked into the first ~1.5s) PRIVATE with
status.publishAt; sets the cover still as the custom thumbnail (auto-compressed <2MB).
Idempotent/resumable: skips any short whose result file exists OR whose title already
appears on the channel. Owner-approved batch (2026-07-26 "55話まで作って予約して").

Slots: 1/day 12:00 JST (03:00Z). Free days audited 2026-07-26: 7/31-8/03 + 8/18-8/21.

    py -3.11 scripts/schedule_new_shorts_v005.py --dry-run
    py -3.11 scripts/schedule_new_shorts_v005.py
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
    {"n": 52, "publishAt": "2026-07-31T03:00:00Z",
     "title": "Police Raided the Wrong House. What Does the Law Owe You? #Shorts",
     "desc": "Chicago, 2019: officers with a judge-signed warrant raided the home of a social worker — the tip behind the warrant was wrong, and the man they sought was elsewhere wearing a court-ordered ankle monitor. The city fought release of the bodycam video, then paid a $2.9 million settlement with no admission of wrongdoing and no court ruling that any officer violated her rights."},
    {"n": 53, "publishAt": "2026-08-01T03:00:00Z",
     "title": "Can Police Enter Your Home Just to Check on You? #Shorts",
     "desc": "Caniglia v. Strom (2021), 9-0: after a welfare check, officers entered a Rhode Island man's home without a warrant and took his handguns, calling it 'community caretaking.' The Supreme Court held community caretaking does not justify warrantless entry into the home. Real emergencies remain a separate question."},
    {"n": 54, "publishAt": "2026-08-02T03:00:00Z",
     "title": "Why Did Five Innocent Kids Confess to a Crime They Didn't Commit? #Shorts",
     "desc": "New York, 1989: five teenagers confessed to the Central Park jogger attack after hours of unrecorded interrogation. The DNA from the scene matched none of them; they were convicted anyway. In 2002 a convicted murderer said he acted alone, his DNA matched, and every conviction was vacated."},
    {"n": 55, "publishAt": "2026-08-03T03:00:00Z",
     "title": "Texas Was Warned Before the Execution. Why Didn't Anyone Stop It? #Shorts",
     "desc": "Texas executed Cameron Todd Willingham in 2004 for an arson that killed his three daughters. Days before the execution, a fire scientist warned in writing that the arson indicators were scientifically invalid. The state's own later-hired expert concluded a finding of arson could not be sustained — the fire may never have been a crime at all."},
    {"n": 56, "publishAt": "2026-08-18T03:00:00Z",
     "title": "Can a prosecutor go to jail for hiding the truth? #Shorts",
     "desc": "Michael Morton spent nearly 25 years in a Texas prison for his wife's murder while the prosecution withheld evidence pointing to another man — including the eyewitness account of his own young son. DNA identified the real killer and freed Morton in 2011. The former prosecutor was sentenced to jail for concealing evidence — a first of its kind."},
    {"n": 57, "publishAt": "2026-08-19T03:00:00Z",
     "title": "Can police make you confess to a murder you didn't commit? #Shorts",
     "desc": "The Norfolk Four: four Navy sailors confessed to a 1997 murder the DNA said one man committed. The real killer confessed from prison and matched every test. A federal judge later declared the four actually innocent — writing that no sane human being could find them guilty."},
    {"n": 58, "publishAt": "2026-08-20T03:00:00Z",
     "title": "How many times can the state try you for the same crime? #Shorts",
     "desc": "Flowers v. Mississippi (2019), 7-2: Curtis Flowers was tried six times by the same prosecutor. The Supreme Court found a relentless, determined effort to keep Black citizens off the jury. In 2020 the charges were dropped with prejudice. The murders remain unsolved."},
    {"n": 59, "publishAt": "2026-08-21T03:00:00Z",
     "title": "Why does Chicago teach schoolkids about this police commander? #Shorts",
     "desc": "Chicago police commander Jon Burge and his 'Midnight Crew' were linked to the torture of more than one hundred Black men. The statute of limitations ran out on the torture itself; Burge was convicted only of lying under oath about it, and kept his pension. Chicago later passed the first municipal reparations ordinance in America — and the case is now taught in the city's schools."},
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


def ensure_thumb(n: int) -> Path:
    """Cover still -> <2MB PNG/JPG for thumbnails.set."""
    src = OUT / f"short{n}_thumb.png"
    THUMBS.mkdir(parents=True, exist_ok=True)
    dst = THUMBS / f"short{n}.png"
    if src.stat().st_size <= 2_000_000:
        dst.write_bytes(src.read_bytes())
        return dst
    from PIL import Image
    im = Image.open(src).convert("RGB")
    dst = THUMBS / f"short{n}.jpg"
    q = 92
    while q >= 60:
        im.save(dst, "JPEG", quality=q, optimize=True)
        if dst.stat().st_size <= 2_000_000:
            return dst
        q -= 8
    return dst


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


def set_thumb(tok, vid, path: Path):
    ctype = "image/png" if path.suffix == ".png" else "image/jpeg"
    r = urllib.request.Request(f"https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId={vid}",
        data=path.read_bytes(), headers={"Authorization": f"Bearer {tok}", "Content-Type": ctype}, method="POST")
    with urllib.request.urlopen(r, timeout=120) as resp:
        return json.loads(resp.read().decode())


def schedule(tok, vid, when):
    body = json.dumps({"id": vid, "status": {"privacyStatus": "private", "publishAt": when,
        "selfDeclaredMadeForKids": False}}).encode()
    r = urllib.request.Request("https://www.googleapis.com/youtube/v3/videos?part=status", data=body,
        headers={"Authorization": f"Bearer {tok}", "Content-Type": "application/json"}, method="PUT")
    with urllib.request.urlopen(r, timeout=60) as resp:
        return json.loads(resp.read().decode())


EP_BY_N = {52: "PD-2026-042-young", 53: "PD-2026-043-caniglia", 54: "PD-2026-050-centralpark",
           55: "PD-2026-051-willingham", 56: "PD-2026-052-morton", 57: "PD-2026-053-norfolk",
           58: "PD-2026-054-flowers", 59: "PD-2026-055-burge"}


def main(argv):
    try: sys.stdout.reconfigure(encoding="utf-8")
    except Exception: pass
    ap = argparse.ArgumentParser(); ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--only", default="", help="comma-separated short numbers")
    args = ap.parse_args(argv)
    RESULTS.mkdir(parents=True, exist_ok=True)
    only = {int(x) for x in args.only.split(",") if x.strip()}
    shorts = [s for s in SHORTS if not only or s["n"] in only]

    for s in shorts:
        v = OUT / f"short{s['n']}_yt_coverfirst.mp4"
        if not v.exists(): print(f"BLOCKED: missing {v}"); return 1
        if not (OUT / f"short{s['n']}_thumb.png").exists(): print(f"BLOCKED: missing thumb short{s['n']}"); return 1
    tok = _access_token(load_env())
    ch = get_channel_id(tok)
    if ch not in CHANNEL_ALLOWLIST: print(f"BLOCKED: channel {ch} not allowlisted"); return 1
    print(f"OK channel {ch}")
    existing = channel_titles(tok)

    if args.dry_run:
        for s in shorts:
            dup = " [ALREADY ON CHANNEL - would finalize]" if s["title"] in existing else ""
            v = OUT / f"short{s['n']}_yt_coverfirst.mp4"
            print(f"  [dry] short{s['n']} ({v.stat().st_size/1e6:.0f}MB) -> {s['publishAt']}  {s['title'][:50]}{dup}")
        print("[dry-run] no uploads."); return 0

    done = []
    for s in shorts:
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
        try:
            set_thumb(tok, vid, ensure_thumb(n)); tset = True; print(f"  short{n}: thumb set")
        except Exception as e:
            tset = False; print(f"  short{n}: WARN thumb {str(e)[:80]}")
        try:
            schedule(tok, vid, s["publishAt"]); print(f"  short{n}: scheduled {s['publishAt']}")
        except Exception:
            time.sleep(5); schedule(tok, vid, s["publishAt"]); print(f"  short{n}: scheduled {s['publishAt']} (retry)")
        res = {"short": n, "video_id": vid, "watch": f"https://youtu.be/{vid}", "title": s["title"],
               "publishAt": s["publishAt"], "privacy": "private", "thumbnail_set": tset,
               "channel_id": ch, "coverfirst": True}
        resfile.write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
        ep = EP_BY_N[n]
        pkg = ROOT / "episodes" / ep / "09_package"
        pkg.mkdir(parents=True, exist_ok=True)
        (pkg / f"short{n}_youtube_schedule_result.v001.json").write_text(
            json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
        done.append(res); time.sleep(1)

    print(f"\nDONE: {len(done)}/{len(shorts)} shorts scheduled.")
    for d in done: print(f"  short{d['short']}: {d['watch']}  {d['publishAt']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
