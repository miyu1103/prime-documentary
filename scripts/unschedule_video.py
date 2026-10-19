#!/usr/bin/env python3
"""Take a video OFF the publishing calendar without destroying it — fail-closed.

WHY THIS EXISTS
---------------
Twice now an upload has died mid-transfer while YouTube kept the metadata it was sent in
the resumable-session header — title, description, and `publishAt` — and applied them
immediately. The result reads as "scheduled" from every angle (`status.publishAt` is set,
the video is on the channel, the calendar looks full) while `processingStatus` is still
`processing` and the bytes are incomplete. EP64 memphis on 2026-08-17 and EP69 hyatt on
2026-08-19, the second one aborting at 1,334 MB of 1,645 MB after 13 network write
timeouts. Left alone, both would have reached their slot and published something broken.

The only tool that existed for this was `delete_scheduled_video.py`, which is irreversible
and needs an owner decision. Clearing the date is neither: it removes the danger — the
video can no longer auto-publish — and leaves every byte and every field in place, so a
later delete, replace or re-schedule is still open. Do this first; decide about the video
itself afterwards, with time.

Note that this does NOT make a broken upload good. It only stops the clock. The re-upload
still has to happen and still has to be proven `processed`/`succeeded` on the live API.

GUARDS (all must pass or it refuses)
  - the video is on our channel
  - privacyStatus == "private"        (never touch the calendar of a public video)
  - snippet.title starts with --expect-title-prefix   (never the wrong video)
  - status.publishAt is actually set  (otherwise there is nothing to clear, and a silent
                                       no-op that reports success is how instruments lie)

Dry-run by default. Costs 1 unit to read, 50 units to write.

    py -3.11 scripts/unschedule_video.py --id VIDEO_ID --expect-title-prefix "One Rod Became Two"
    py -3.11 scripts/unschedule_video.py --id VIDEO_ID --expect-title-prefix "One Rod Became Two" --apply
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from pd_factory.providers import load_env                    # noqa: E402
from pd_factory.providers.youtube import _access_token       # noqa: E402

CHANNEL = "UCuQPtAz1rca9eJ4xhvX0yKA"
API = "https://www.googleapis.com/youtube/v3/videos"


def api_get(token: str, url: str) -> dict:
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def main(argv: list[str]) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", required=True)
    ap.add_argument("--expect-title-prefix", required=True)
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args(argv)

    token = _access_token(load_env())
    d = api_get(token, f"{API}?" + urllib.parse.urlencode({"part": "snippet,status,processingDetails",
                                                           "id": a.id}))
    items = d.get("items", [])
    if not items:
        print(f"BLOCKED: video {a.id} not found")
        return 1
    it = items[0]
    snip, st = it["snippet"], it["status"]
    proc = it.get("processingDetails", {}).get("processingStatus", "?")
    ch, priv, title = snip.get("channelId"), st.get("privacyStatus"), snip.get("title", "")
    when = st.get("publishAt")
    print(f"  id={a.id} channel={ch} privacy={priv} upload={st.get('uploadStatus')} "
          f"processing={proc}")
    print(f"  title={title!r}")
    print(f"  publishAt={when}")

    if ch != CHANNEL:
        print(f"BLOCKED: not our channel ({ch})")
        return 1
    if priv != "private":
        print(f"BLOCKED: privacy is {priv!r} -- refusing to touch a non-private video")
        return 1
    if not title.startswith(a.expect_title_prefix):
        print(f"BLOCKED: title {title!r} does not start with {a.expect_title_prefix!r}")
        return 1
    if not when:
        print("BLOCKED: this video carries no publishAt -- nothing to clear. "
              "Reporting success here would be a no-op pretending to be an action.")
        return 1

    if not a.apply:
        print(f"DRY-RUN ok -- all guards pass. Would clear publishAt {when}. "
              "Re-run with --apply.")
        return 0

    # `publishAt` must be sent as an explicit null. Measured on Ms9wVUPsO3Y, 2026-08-19:
    # a status part that simply OMITS publishAt returns HTTP 200 and echoes the old date
    # back unchanged -- the write succeeds and changes nothing. Sending null on the same
    # video, seconds later, cleared it. So the `status` part is NOT replace-not-merge for
    # this field, whatever the reference implies. This is why the read-back below exists
    # and why it must never be removed: the first version of this tool reported success
    # from the echo and was wrong.
    body = {
        "id": a.id,
        "status": {
            "publishAt": None,
            "privacyStatus": "private",
            "license": st.get("license", "youtube"),
            "embeddable": st.get("embeddable", True),
            "publicStatsViewable": st.get("publicStatsViewable", True),
            "selfDeclaredMadeForKids": st.get("selfDeclaredMadeForKids", False),
        },
    }
    req = urllib.request.Request(
        f"{API}?" + urllib.parse.urlencode({"part": "status"}),
        data=json.dumps(body).encode("utf-8"),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        method="PUT")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            got = json.load(r)
    except urllib.error.HTTPError as e:
        print(f"UPDATE FAILED HTTP {e.code}: {e.read().decode()[:400]}")
        return 1

    # Do not trust the write's own echo. Read it back.
    back = api_get(token, f"{API}?" + urllib.parse.urlencode({"part": "status", "id": a.id}))
    now = back["items"][0]["status"] if back.get("items") else {}
    still = now.get("publishAt")
    print(f"  echoed publishAt={got.get('status', {}).get('publishAt')}")
    print(f"  read back  privacy={now.get('privacyStatus')} publishAt={still}")
    if still:
        print(f"FAILED: {a.id} still carries publishAt {still} -- it is STILL on the calendar")
        return 1
    print(f"UNSCHEDULED {a.id} -- private, no publish date. It cannot auto-publish.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
