#!/usr/bin/env python
"""Take ONE already-uploaded, already-scheduled video public right now.

`upload_schedule_case_v001.py` only ever writes `privacyStatus=private` with a future
`publishAt`, which is the right default: it is the shape that cannot publish something by
accident. This script is the deliberate exception, for the case where the owner decides a
finished video should go out now rather than wait for its slot.

    py -3.11 scripts/publish_now_v001.py --video-id <id> --slug <slug>          # dry run
    py -3.11 scripts/publish_now_v001.py --video-id <id> --slug <slug> --apply

It refuses unless every one of these holds, because publication is irreversible in the way
that matters (subscribers are notified, the video enters the feed, and un-publishing later
does not undo either):

  * the id is on the channel allowlist,
  * the video is currently private WITH a publishAt -- i.e. a scheduled episode, not a
    draft and not something already public,
  * that publishAt is still in the future (if it has passed, YouTube already published it
    and there is nothing to do),
  * the slug's own schedule receipt names this same video id.

It prints what it is about to change and, on --apply, records the before/after in
runs/qc/<slug>_publish_now.v001.json so the decision is auditable.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from yt_channel_index import API, authorize, http  # noqa: E402
import yt_quota  # noqa: E402

ALLOWED_CHANNELS = {"UCuQPtAz1rca9eJ4xhvX0yKA"}  # PD only; a second channel needs a decision


def get_video(auth: dict, vid: str) -> dict:
    code, r = http("GET", f"{API}/videos?part=status,snippet&id={vid}", headers=auth)
    yt_quota.record("videos.list")
    if code != 200:
        raise SystemExit(f"[publish-now] videos.list HTTP {code}: {r}")
    items = r.get("items") or []
    if not items:
        raise SystemExit(f"[publish-now] no such video: {vid}")
    return items[0]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--video-id", required=True)
    ap.add_argument("--slug", required=True)
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()

    auth = authorize(ROOT)
    v = get_video(auth, a.video_id)
    st, sn = v["status"], v["snippet"]
    ch = sn.get("channelId")
    pub_at = st.get("publishAt")

    print(f"[publish-now] {a.video_id}  {sn.get('title','')[:70]}")
    print(f"[publish-now] channel={ch} privacy={st.get('privacyStatus')} publishAt={pub_at}")

    if ch not in ALLOWED_CHANNELS:
        raise SystemExit(f"[publish-now] REFUSED: channel {ch} is not on the allowlist")
    if st.get("privacyStatus") != "private":
        raise SystemExit(f"[publish-now] REFUSED: already {st.get('privacyStatus')} -- nothing to do")
    if not pub_at:
        raise SystemExit("[publish-now] REFUSED: private with no publishAt is a draft, not a "
                         "scheduled episode. Schedule it the normal way first.")
    if datetime.fromisoformat(pub_at.replace("Z", "+00:00")) <= datetime.now(timezone.utc):
        raise SystemExit("[publish-now] REFUSED: that publishAt is already in the past, so YouTube "
                         "has published it. Check the channel.")

    receipts = sorted((ROOT / "episodes").glob(f"PD-*-{a.slug}/09_package/youtube_schedule_result.v*.json"))
    if not receipts:
        raise SystemExit(f"[publish-now] REFUSED: no schedule receipt for {a.slug}")
    rec = json.loads(receipts[-1].read_text(encoding="utf-8"))
    if rec.get("video_id") != a.video_id:
        raise SystemExit(f"[publish-now] REFUSED: {receipts[-1].name} names {rec.get('video_id')}, "
                         f"not {a.video_id}")

    if not a.apply:
        print(f"[publish-now] DRY RUN -- would clear publishAt {pub_at} and set privacyStatus=public")
        print("[publish-now] re-run with --apply to publish. Subscribers are notified immediately.")
        return 0

    body = {"id": a.video_id,
            "status": {"privacyStatus": "public",
                       "selfDeclaredMadeForKids": st.get("selfDeclaredMadeForKids", False),
                       "license": st.get("license", "youtube"),
                       "embeddable": st.get("embeddable", True),
                       "publicStatsViewable": st.get("publicStatsViewable", True)}}
    code, resp = http("PUT", f"{API}/videos?part=status", headers=auth, body=body)
    yt_quota.record("videos.update")
    if code != 200:
        raise SystemExit(f"[publish-now] videos.update HTTP {code}: {resp}")

    after = get_video(auth, a.video_id)["status"]
    out = {"schema_version": "1.0.0", "slug": a.slug, "video_id": a.video_id,
           "at": datetime.now(timezone.utc).isoformat(),
           "before": {"privacyStatus": "private", "publishAt": pub_at},
           "after": {"privacyStatus": after.get("privacyStatus"),
                     "publishAt": after.get("publishAt")},
           "why": "owner decision: fill the empty publication day rather than hold the slot"}
    p = ROOT / "runs" / "qc" / f"{a.slug}_publish_now.v001.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(out, indent=1), encoding="utf-8")

    print(f"[publish-now] now {after.get('privacyStatus')} -- https://youtu.be/{a.video_id}")
    print(f"[publish-now] recorded {p}")
    return 0 if after.get("privacyStatus") == "public" else 1


if __name__ == "__main__":
    sys.exit(main())
