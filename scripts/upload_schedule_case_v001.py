#!/usr/bin/env python3
"""Upload a PD case episode privately and schedule its public release (private + publishAt).

Generic, config-driven version of upload_schedule_kyllo_v001.py (--ep katz|rodriguez).
Reuses the exact same resilient resumable uploader, thumbnail/caption set, hash guard, and
duplicate-refusal. Owner approved sequential scheduling 2026-07-04 ("順番ずつ予約投稿しよう":
EP25=7/10, EP26 Katz=7/11, EP27 Rodriguez=7/12, all 12:00 JST, private + publishAt).

Usage: python scripts/upload_schedule_case_v001.py --ep katz [--dry-run]
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

CONFIG = {
    "katz": {
        "ep": "PD-2026-026-katz",
        "video": r"H:/pd-media/episodes/PD-2026-026-katz/08_edit/final.v001.mp4",
        "sched_local": "2026-07-11T12:00:00+09:00",
        "sched_utc": "2026-07-11T03:00:00Z",
        "title": "The FBI Recorded His Calls — and Never Touched the Booth",
        "description": (
            "In 1965, FBI agents taped an electronic listening device to the OUTSIDE of a glass "
            "public phone booth in Los Angeles and recorded Charles Katz passing bets across state "
            "lines — without a warrant, and without ever setting foot inside the booth.\n\n"
            "In Katz v. United States (1967), the Supreme Court ruled 7–1 that this was a Fourth "
            "Amendment “search.” Justice Potter Stewart's majority opinion held that “the Fourth "
            "Amendment protects people, not places” — what a person seeks to keep private, even "
            "somewhere the public can go, can be constitutionally protected. A man who shuts a "
            "phone-booth door and pays the toll is entitled to assume his words will not be "
            "broadcast to the world. The decision buried the old “trespass” rule from Olmstead v. "
            "United States: a search no longer requires a physical intrusion. Justice Harlan's "
            "concurrence added the famous two-part “reasonable expectation of privacy” test; "
            "Justice Black dissented alone.\n\n"
            "That single line — “people, not places” — is why courts still reach for Katz whenever "
            "the government reaches for a new way to listen in.\n\n"
            "#SupremeCourt #FourthAmendment #Privacy #Katz #Wiretap #Law #Documentary"
        ),
        "tags": ["Supreme Court", "Fourth Amendment", "Katz", "Katz v United States", "Privacy",
                 "Wiretap", "Reasonable Expectation of Privacy", "Search and Seizure", "Law", "Documentary"],
    },
    "rodriguez": {
        "ep": "PD-2026-027-rodriguez",
        "video": r"H:/pd-media/episodes/PD-2026-027-rodriguez/08_edit/final.v001.mp4",
        "sched_local": "2026-07-12T12:00:00+09:00",
        "sched_utc": "2026-07-12T03:00:00Z",
        "title": "How Long Can the Police Keep You at a Traffic Stop?",
        "description": (
            "A Nebraska officer pulled Dennis Rodriguez over just after midnight for drifting onto "
            "the shoulder. He ran the checks, handed back the paperwork, and issued a written "
            "warning — the traffic stop was finished. Then he walked a drug dog around the car. The "
            "dog alerted about seven to eight minutes later.\n\n"
            "In Rodriguez v. United States (2015), the Supreme Court ruled 6–3 that this was an "
            "unlawful seizure. Justice Ruth Bader Ginsburg's majority held that a traffic stop may "
            "last no longer than the time needed to handle the matter that justified it — the "
            "stop's “mission.” Once the tasks tied to the traffic violation are done, authority for "
            "the stop ends; prolonging it for a dog sniff without independent reasonable suspicion "
            "violates the Fourth Amendment. The Court sent the case back to decide whether such "
            "suspicion existed. Justices Thomas, Alito, and Kennedy dissented.\n\n"
            "The rule is simple, and it still bites: the clock stops when the mission does.\n\n"
            "#SupremeCourt #FourthAmendment #TrafficStop #Rodriguez #K9 #Law #Documentary"
        ),
        "tags": ["Supreme Court", "Fourth Amendment", "Rodriguez", "Rodriguez v United States",
                 "Traffic Stop", "Dog Sniff", "K9", "Search and Seizure", "Law", "Documentary"],
    },
}


def sha(p: Path) -> str:
    return "sha256:" + sha256_file(p)


def initiate_upload(token, size, cfg):
    snippet = {"title": cfg["title"], "description": cfg["description"].rstrip(), "tags": cfg["tags"],
               "categoryId": "27", "defaultLanguage": "en", "defaultAudioLanguage": "en"}
    status = {"privacyStatus": "private", "publishAt": cfg["sched_utc"], "selfDeclaredMadeForKids": False,
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
                    return json.loads(r.read().decode()).get("id")
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


def upload_caption(token, vid, caps, slug):
    b = f"{slug}_caption_{int(time.time())}"
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
    ap = argparse.ArgumentParser()
    ap.add_argument("--ep", required=True, choices=sorted(CONFIG))
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)
    cfg = CONFIG[args.ep]
    slug = args.ep
    EP = cfg["ep"]
    EPDIR = ROOT / "episodes" / EP
    PKG = EPDIR / "09_package"
    VIDEO = Path(cfg["video"])
    THUMB = PKG / "thumbnail.selected.v001.png"
    CAPS = EPDIR / "08_edit" / "captions.final.v001.srt"
    DELIVERY = PKG / "final_delivery.v001.json"
    RESULT = PKG / "youtube_schedule_result.v001.json"

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
    # HARD LOCK: no upload without a green acceptance receipt bound to THIS render's bytes.
    # A video that did not pass scripts/check_final_acceptance.py --emit-receipt physically
    # cannot be scheduled. runtime_band is the one owner-accepted documented deviation.
    ALLOWED_DEVIATIONS = {"runtime_band"}
    receipt = PKG / "acceptance_receipt.v001.json"
    if not receipt.exists():
        raise RuntimeError(
            f"no acceptance receipt {receipt} -- run "
            f"`check_final_acceptance.py {EP} --render {VIDEO} --emit-receipt` first")
    rc = json.loads(receipt.read_text("utf-8"))
    if rc.get("video_sha256") != got:
        raise RuntimeError(f"receipt is for a different render (receipt sha {rc.get('video_sha256')} "
                           f"!= this video {got}); re-run the gate on THIS file")
    bad = [c for c in rc.get("hard_failures", []) if c not in ALLOWED_DEVIATIONS]
    if bad:
        raise RuntimeError(f"acceptance gate NOT green: unresolved hard failures {bad}. "
                           f"Fix them and re-emit the receipt before scheduling.")
    print(f"OK acceptance receipt green (sha match; tolerated={sorted(set(rc.get('hard_failures', [])) & ALLOWED_DEVIATIONS)})")
    print(f"OK {EP}: title={cfg['title']!r}")
    print(f"OK video={VIDEO.name} {VIDEO.stat().st_size/1e6:.0f}MB sha_ok=True")
    print(f"OK thumb={THUMB.name} caps={CAPS.name}")
    print(f"OK schedule local={cfg['sched_local']} utc={cfg['sched_utc']} (private + publishAt)")
    if args.dry_run:
        print("DRY_RUN_OK no external writes")
        return 0

    token = _access_token(load_env())
    ch = get_channel_id(token)
    if ch not in CHANNEL_ALLOWLIST:
        raise RuntimeError(f"channel {ch} not allowlisted")
    url = initiate_upload(token, VIDEO.stat().st_size, cfg)
    print(f"OK upload session started; uploading {VIDEO.stat().st_size/1e6:.0f}MB ...")
    vid = resilient_upload(url, token, VIDEO)
    if not vid:
        raise RuntimeError("no video_id")
    print(f"OK uploaded private video_id={vid}")
    set_thumbnail(token, vid, THUMB); print("OK thumbnail set")
    cap_err = None
    try:
        upload_caption(token, vid, CAPS, slug); print("OK captions uploaded")
    except Exception as e:
        cap_err = str(e); print(f"WARN captions upload failed (burned-in remain): {cap_err}")
    st = get_state(token, vid); status = ((st.get("items") or [{}])[0].get("status") or {})
    if status.get("privacyStatus") != "private" or status.get("publishAt") != cfg["sched_utc"]:
        raise RuntimeError(f"verify failed privacy={status.get('privacyStatus')} publishAt={status.get('publishAt')}")
    res = {"schema_version": "1.0.0", "episode_id": EP, "mode": "scheduled", "video_id": vid,
           "watch": f"https://youtu.be/{vid}", "studio": f"https://studio.youtube.com/video/{vid}/edit",
           "channel_id": ch, "privacy": "private", "publishAt": status.get("publishAt"),
           "scheduled_at_local": cfg["sched_local"], "title": cfg["title"], "video_sha256": got,
           "thumbnail_sha256": sha(THUMB), "thumbnail_set": True, "captions_uploaded": cap_err is None,
           "caption_error": cap_err, "public_immediate_publish": False, "external_upload": True,
           "owner_instruction": "順番ずつ予約投稿しよう (2026-07-04)", "scheduled_at": datetime.now(timezone.utc).isoformat()}
    RESULT.write_text(json.dumps(res, indent=2, ensure_ascii=False) + "\n", "utf-8")
    print(f"RESULT {RESULT.relative_to(ROOT)}")
    print(f"WATCH https://youtu.be/{vid}  SCHEDULED {cfg['sched_local']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
