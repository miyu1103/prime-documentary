#!/usr/bin/env python3
"""Upload PD-2026-025 Kyllo privately and schedule public release (private + publishAt).

Owner instructed the schedule 2026-07-04 after reviewing the final. The full one-pass
gate FAILs only on runtime_band (10:20, owner-accepted); every other hard check PASSes,
so this uses the same simple, safe upload path as the shorts (private + publishAt +
thumbnail + sidecar captions), not immediate public. Verifies file hashes against
final_delivery before any write. Refuses to duplicate.

Usage: python scripts/upload_schedule_kyllo_v001.py [--dry-run]
"""
from __future__ import annotations
import argparse, json, mimetypes, ssl, sys, time, urllib.error, urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))
from pd_factory.providers import load_env
from pd_factory.providers.youtube import _access_token
from upload_episode import CHANNEL_ALLOWLIST, get_channel_id, sha256_file, upload_chunks

EP = "PD-2026-025-kyllo"
EPDIR = ROOT / "episodes" / EP
PKG = EPDIR / "09_package"
VIDEO = Path(r"E:/pd-media/episodes/PD-2026-025-kyllo/08_edit/final.v007.mp4")
THUMB = PKG / "thumbnail.selected.v001.png"
CAPS = EPDIR / "08_edit" / "captions.final.v001.srt"
DELIVERY = PKG / "final_delivery.v001.json"
RESULT = PKG / "youtube_schedule_result.v001.json"

# long-form daily cadence: EP20=7/5 … EP24=7/9, so EP25 (next long-form) = 7/10.
# (7/10-7/13 already hold a daily SHORT each; long-form + short share the 12:00 slot, per 7/5-7/9.)
SCHED_LOCAL = "2026-07-10T12:00:00+09:00"
SCHED_UTC = "2026-07-10T03:00:00Z"

TITLE = "Can the Police Scan Your Home From the Street?"
DESCRIPTION = (
    "A federal agent pointed a thermal-imaging camera at a private home from a public "
    "street — no warrant, no foot on the property — and used the heat leaking off the "
    "walls to guess what was happening inside.\n\n"
    "In Kyllo v. United States (2001), the Supreme Court ruled 5–4 that using a device "
    "“not in general public use” to reveal details of a home's interior that could not "
    "be known without physically going inside is a Fourth Amendment “search” — so it "
    "needs a warrant. The Court did not ban thermal imaging; it required a warrant and sent "
    "the case back down. Justice Scalia wrote the majority opinion; Justice Stevens dissented, "
    "calling it “off-the-wall” observation, not “through-the-wall” surveillance.\n\n"
    "That one phrase — “not in general public use” — is why courts keep returning to "
    "Kyllo when they ask how far the government can push drones, cameras, and new sensors "
    "before it needs a warrant.\n\n"
    "#SupremeCourt #FourthAmendment #Privacy #Kyllo #ThermalImaging #Law #Documentary"
)
TAGS = ["Supreme Court", "Fourth Amendment", "Kyllo", "Kyllo v United States", "Privacy",
        "Thermal Imaging", "Search and Seizure", "Warrant", "Law", "Documentary"]


def sha(p: Path) -> str:
    return "sha256:" + sha256_file(p)


def initiate_upload(token, size):
    snippet = {"title": TITLE, "description": DESCRIPTION.rstrip(), "tags": TAGS,
               "categoryId": "27", "defaultLanguage": "en", "defaultAudioLanguage": "en"}
    status = {"privacyStatus": "private", "publishAt": SCHED_UTC, "selfDeclaredMadeForKids": False,
              "containsSyntheticMedia": True, "license": "youtube", "embeddable": True, "publicStatsViewable": True}
    body = json.dumps({"snippet": snippet, "status": status}, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status",
        data=body, method="POST",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json; charset=UTF-8",
                 "X-Upload-Content-Type": "video/mp4", "X-Upload-Content-Length": str(size)})
    with urllib.request.urlopen(req, timeout=60) as r:
        url = r.headers.get("Location", "")
    if not url.startswith("https://www.googleapis.com/"):
        raise RuntimeError(f"bad upload url {url[:80]}")
    return url


def _query_position(url, token, size):
    """Ask the resumable session how many bytes it actually has (recover after a drop)."""
    req = urllib.request.Request(url, data=b"", method="PUT",
                                 headers={"Authorization": f"Bearer {token}", "Content-Range": f"bytes */{size}"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return ("done", json.loads(r.read().decode()).get("id"))
    except urllib.error.HTTPError as e:
        if e.code in (200, 201):
            return ("done", json.loads(e.read().decode()).get("id"))
        if e.code == 308:
            rng = e.headers.get("Range")
            return ("inc", (int(rng.split("-")[1]) + 1) if rng else 0)
        raise


def resilient_upload(url, token, path, chunk=8 * 1024 * 1024, max_fail=12):
    """Chunked resumable upload that survives intermittent SSL/network drops by querying the
    session position and resuming, with exponential backoff. One session -> no duplicate videos."""
    size = path.stat().st_size
    sent = 0
    fails = 0
    f = open(path, "rb")
    try:
        while sent < size:
            f.seek(sent)
            data = f.read(chunk)
            end = sent + len(data) - 1
            req = urllib.request.Request(url, data=data, method="PUT",
                                         headers={"Authorization": f"Bearer {token}", "Content-Type": "video/mp4",
                                                  "Content-Range": f"bytes {sent}-{end}/{size}", "Content-Length": str(len(data))})
            try:
                with urllib.request.urlopen(req, timeout=300) as r:
                    return json.loads(r.read().decode()).get("id")  # final chunk -> 200/201 + id
            except urllib.error.HTTPError as e:
                if e.code == 308:
                    rng = e.headers.get("Range")
                    sent = (int(rng.split("-")[1]) + 1) if rng else end + 1
                    fails = 0
                    print(f"  {sent/1e6:.0f}/{size/1e6:.0f} MB ({sent/size*100:.0f}%)")
                    continue
                raise
            except (urllib.error.URLError, ssl.SSLError, TimeoutError, ConnectionError, OSError) as e:
                fails += 1
                if fails > max_fail:
                    raise RuntimeError(f"upload aborted after {fails} network failures: {e}")
                wait = min(2 ** fails, 30)
                print(f"  net drop at {sent/1e6:.0f} MB — resume attempt {fails} in {wait}s ({type(e).__name__})")
                time.sleep(wait)
                st = _query_position(url, token, size)
                if st[0] == "done":
                    return st[1]
                sent = st[1]
                continue
        raise RuntimeError("upload ended without a video id")
    finally:
        f.close()


def set_thumbnail(token, vid, path):
    ct = mimetypes.guess_type(path.name)[0] or "image/png"
    req = urllib.request.Request(f"https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId={vid}",
                                 data=path.read_bytes(), method="POST",
                                 headers={"Authorization": f"Bearer {token}", "Content-Type": ct})
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.loads(r.read().decode())


def upload_caption(token, vid, caps):
    b = f"kyllo_caption_{int(time.time())}"
    meta = {"snippet": {"videoId": vid, "language": "en", "name": "English", "isDraft": False}}
    body = b"".join([f"--{b}\r\n".encode(), b"Content-Type: application/json; charset=UTF-8\r\n\r\n",
                     json.dumps(meta).encode(), b"\r\n", f"--{b}\r\n".encode(),
                     b"Content-Type: application/x-subrip\r\n\r\n", caps.read_bytes(), b"\r\n", f"--{b}--\r\n".encode()])
    req = urllib.request.Request("https://www.googleapis.com/upload/youtube/v3/captions?uploadType=multipart&part=snippet",
                                 data=body, method="POST",
                                 headers={"Authorization": f"Bearer {token}", "Content-Type": f"multipart/related; boundary={b}"})
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.loads(r.read().decode())


def get_state(token, vid):
    req = urllib.request.Request(f"https://www.googleapis.com/youtube/v3/videos?part=snippet,status&id={vid}",
                                 headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode())


def main(argv):
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(); ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)
    if RESULT.exists():
        raise RuntimeError(f"Refusing duplicate: {RESULT} exists")
    for p in (VIDEO, THUMB, CAPS, DELIVERY):
        if not p.exists():
            raise RuntimeError(f"missing {p}")
    delivery = json.loads(DELIVERY.read_text("utf-8"))
    want = delivery["canonical_final"]["video_sha256"]
    got = sha(VIDEO)
    if got != want:
        raise RuntimeError(f"VIDEO hash != final_delivery canonical: {got} vs {want}")
    if THUMB.stat().st_size >= 2 * 1024 * 1024:
        raise RuntimeError("thumbnail >= 2MB")
    print(f"OK {EP}: title={TITLE!r}")
    print(f"OK video={VIDEO.name} {VIDEO.stat().st_size/1e6:.0f}MB sha_ok=True")
    print(f"OK thumb={THUMB.name} caps={CAPS.name}")
    print(f"OK schedule local={SCHED_LOCAL} utc={SCHED_UTC} (private + publishAt)")
    if args.dry_run:
        print("DRY_RUN_OK no external writes")
        return 0

    token = _access_token(load_env())
    ch = get_channel_id(token)
    if ch not in CHANNEL_ALLOWLIST:
        raise RuntimeError(f"channel {ch} not allowlisted")
    url = initiate_upload(token, VIDEO.stat().st_size)
    print(f"OK upload session started; uploading {VIDEO.stat().st_size/1e6:.0f}MB ...")
    vid = resilient_upload(url, token, VIDEO)
    if not vid:
        raise RuntimeError("no video_id")
    print(f"OK uploaded private video_id={vid}")
    thumb_status = set_thumbnail(token, vid, THUMB); print("OK thumbnail set")
    cap_err = None
    try:
        upload_caption(token, vid, CAPS); print("OK captions uploaded")
    except Exception as e:
        cap_err = str(e); print(f"WARN captions upload failed (burned-in remain): {cap_err}")
    st = get_state(token, vid); status = ((st.get("items") or [{}])[0].get("status") or {})
    if status.get("privacyStatus") != "private" or status.get("publishAt") != SCHED_UTC:
        raise RuntimeError(f"verify failed privacy={status.get('privacyStatus')} publishAt={status.get('publishAt')}")
    res = {"schema_version": "1.0.0", "episode_id": EP, "mode": "scheduled", "video_id": vid,
           "watch": f"https://youtu.be/{vid}", "studio": f"https://studio.youtube.com/video/{vid}/edit",
           "channel_id": ch, "privacy": "private", "publishAt": status.get("publishAt"),
           "scheduled_at_local": SCHED_LOCAL, "title": TITLE, "video_sha256": got,
           "thumbnail_sha256": sha(THUMB), "thumbnail_set": True, "captions_uploaded": cap_err is None,
           "caption_error": cap_err, "public_immediate_publish": False, "external_upload": True,
           "owner_instruction": "予約投稿して (2026-07-04)", "scheduled_at": datetime.now(timezone.utc).isoformat()}
    RESULT.write_text(json.dumps(res, indent=2, ensure_ascii=False) + "\n", "utf-8")
    print(f"RESULT {RESULT.relative_to(ROOT)}")
    print(f"WATCH https://youtu.be/{vid}  SCHEDULED {SCHED_LOCAL}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
