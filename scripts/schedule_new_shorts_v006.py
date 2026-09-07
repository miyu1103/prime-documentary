"""Schedule short60/63/66 (EP53 Norfolk / EP54 Flowers / EP55 Burge) to YouTube (private + publishAt).

Clone of schedule_new_shorts_v005.py, retargeted to the first three shorts of the
SHORTS_SLATE_EP53-56.v001 slate. Uploads the *_yt_coverfirst.mp4 renders (designed cover baked
into the first ~1.5s) PRIVATE with status.publishAt; sets the cover still as the custom thumbnail
(auto-compressed <2MB). Idempotent/resumable: skips any short whose result file exists OR whose
title already appears on the channel.

Slots: 1/day 12:00 JST (03:00Z). Free days audited live 2026-07-30 with scripts/yt_schedule_audit.py
-- the last reservation on the channel was 2026-08-21, and 8/14 + 8/15 are a genuine two-day hole
between 8/13 and 8/16, so they are filled first; 8/22 is the next free day after the hole.

HOLD: the matching long-forms (EP53/54/55) are not built or public. Do NOT post the pinned comment
or set the Studio Related-video for these three until each long-form is public
(SHORTS_SLATE_EP53-56.v001.md section 6).

    py -3.11 scripts/schedule_new_shorts_v006.py --dry-run
    py -3.11 scripts/schedule_new_shorts_v006.py
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
    {"n": 60, "publishAt": "2026-08-14T03:00:00Z",
     "title": "What happens when a confession doesn't match the murder? #Shorts",
     "desc": "Norfolk, Virginia, 1997. After eleven hours of overnight interrogation — and after being told he had failed a polygraph, which was false and, in the United States, perfectly legal — a young sailor confessed. His account of how the victim died did not match how she died. The method was wrong. The details were wrong. So the statement was taken again, and corrected, and taken again, until it agreed with the crime scene. Every DNA test excluded him and the three other sailors who followed. A federal judge later ruled all four actually innocent, and all four hold absolute pardons."},
    {"n": 66, "publishAt": "2026-08-15T03:00:00Z",
     "title": "A jail doctor reported police torture in 1982. What happened to his letter? #Shorts",
     "desc": "Chicago, February 1982. A doctor at the Cook County Jail examined a new prisoner, found injuries he could not explain away, and wrote to the superintendent of the Chicago Police Department demanding — his words — a thorough investigation. The letter went up the chain of command, landed on the desk of one of the most powerful men in Illinois, and died there. No answer. No investigation. Nothing. Twenty-eight years later that same page was carried into a federal courtroom as an exhibit. Jon Burge was convicted of perjury and obstruction of justice; he was never charged with torture."},
    {"n": 63, "publishAt": "2026-08-22T03:00:00Z",
     "title": "What happens to a juror who votes not guilty? #Shorts",
     "desc": "Mississippi, 2008. The fifth trial of Curtis Flowers ended in a hung jury after one holdout, James Bibbs, was not persuaded. When the mistrial was declared he was handcuffed in open court and charged with perjury; the prosecution pursuing him was the office of District Attorney Doug Evans. The state attorney general's office stepped in, took the case away and dropped the charge entirely — Bibbs was never convicted. Flowers was tried six times for the same four murders; in 2019 the Supreme Court reversed 7-2 over jury strikes, and he is now fully cleared. The murders remain unsolved."},
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


EP_BY_N = {60: "PD-2026-053-norfolk", 63: "PD-2026-054-flowers", 66: "PD-2026-055-burge"}


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
