#!/usr/bin/env python3
"""Correct EP28's scheduled publishAt to 2026-07-13 (the real next-open LONG-FORM slot).

The upload initiated with publishAt=7/23 (a mis-dated slot: 7/13-7/22 hold only SHORTS, so
7/13 was the true next long-form day). This does a metadata-only videos.update (part=status)
to move publishAt to 7/13 — no re-upload. Reads the video_id from the schedule result, keeps
privacyStatus=private, verifies, and rewrites the result file.
"""
from __future__ import annotations
import json, sys, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src")); sys.path.insert(0, str(ROOT / "scripts"))
from pd_factory.providers import load_env
from pd_factory.providers.youtube import _access_token
from upload_episode import CHANNEL_ALLOWLIST, get_channel_id

RESULT = ROOT / "episodes/PD-2026-028-forfeiture/09_package/youtube_schedule_result.v001.json"
NEW_UTC = "2026-07-13T03:00:00Z"
NEW_LOCAL = "2026-07-13T12:00:00+09:00"


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    if not RESULT.exists():
        raise SystemExit("no schedule result yet — upload not finished")
    res = json.loads(RESULT.read_text("utf-8"))
    vid = res["video_id"]
    tok = _access_token(load_env())
    ch = get_channel_id(tok)
    if ch not in CHANNEL_ALLOWLIST:
        raise SystemExit(f"channel {ch} not allowlisted")
    # fetch current status, change publishAt only
    req = urllib.request.Request(f"https://www.googleapis.com/youtube/v3/videos?part=status&id={vid}",
                                 headers={"Authorization": f"Bearer {tok}"})
    cur = json.loads(urllib.request.urlopen(req, timeout=60).read())["items"][0]["status"]
    if cur.get("publishAt") == NEW_UTC:
        print("already 7/13 — nothing to do"); return 0
    status = {"privacyStatus": "private", "publishAt": NEW_UTC,
              "selfDeclaredMadeForKids": cur.get("selfDeclaredMadeForKids", False),
              "license": cur.get("license", "youtube"), "embeddable": cur.get("embeddable", True),
              "publicStatsViewable": cur.get("publicStatsViewable", True),
              "containsSyntheticMedia": cur.get("containsSyntheticMedia", True)}
    body = json.dumps({"id": vid, "status": status}).encode()
    up = urllib.request.Request("https://www.googleapis.com/youtube/v3/videos?part=status",
                                data=body, method="PUT",
                                headers={"Authorization": f"Bearer {tok}", "Content-Type": "application/json"})
    urllib.request.urlopen(up, timeout=60).read()
    # verify
    v = json.loads(urllib.request.urlopen(urllib.request.Request(
        f"https://www.googleapis.com/youtube/v3/videos?part=status&id={vid}",
        headers={"Authorization": f"Bearer {tok}"}), timeout=60).read())["items"][0]["status"]
    if v.get("publishAt") != NEW_UTC or v.get("privacyStatus") != "private":
        raise SystemExit(f"verify failed: {v}")
    res["publishAt"] = NEW_UTC; res["scheduled_at_local"] = NEW_LOCAL
    res["date_corrected"] = "moved 7/23 -> 7/13 (real next long-form slot; 7/13-7/22 were shorts-only)"
    RESULT.write_text(json.dumps(res, indent=2, ensure_ascii=False) + "\n", "utf-8")
    print(f"OK publishAt -> {NEW_UTC} (7/13 12:00 JST), private. video {vid}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
