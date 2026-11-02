#!/usr/bin/env python
"""Take a scheduled video off the calendar without deleting it.

On 2026-08-05 `check_shipped_frames.py` was run for the first time against masters that were
already uploaded and scheduled. Four of the first four episodes measured came back FAIL, and
three defect classes were confirmed at full resolution by eye:

  * EP51 willingham: a real, identifiable child's face held ~4s, under the narration line about
    the three daughters who died in the fire. The design document bans any child in any form.
  * EP52 morton: another production's title card and burned-in subtitle, from a file named
    `AR-y_2mate_...` -- y2mate is a YouTube-ripping site. Also Rebel News broadcast footage
    with its reporter, chyron and watermark.
  * EP53 norfolk: a red London double-decker with a TfL roundel and a SHEIN advert, in a film
    set in Norfolk, Virginia -- the same failure that already shipped once in EP56.
  * EP61 weimer: a mortuary post-mortem table, and an identifiable real county courthouse, both
    named in that episode's own forbidden_subjects.

Scraped third-party footage is a copyright strike, and a strike is the channel's main ban
vector. So the schedule has to stop before the fix does.

This DOES NOT delete anything. It sets `privacyStatus` to private and clears `publishAt`, so
the upload, its thumbnail, its captions and its description all survive untouched. Restoring a
date is one `--restore` away. Every other status field is read back from YouTube and carried
over verbatim, because videos.update REPLACES the whole status part -- sending a partial one
silently drops `containsSyntheticMedia`, `license` and the made-for-kids declaration.

    python scripts/pause_schedule.py --video dueMY2lSu8w --reason "..." --dry-run
    python scripts/pause_schedule.py --video dueMY2lSu8w --reason "..."
    python scripts/pause_schedule.py --video dueMY2lSu8w --restore 2026-08-20T03:00:00Z

Cost: 1 unit to read + 50 units to update, per video. Exit 0 = every video reached the
intended state, verified by a fresh read afterwards.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:  # noqa: BLE001
    pass

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

API = "https://www.googleapis.com/youtube/v3/videos"
LEDGER = ROOT / "episodes" / "_planning" / "measurements" / "SCHEDULE_PAUSES.v001.json"

# videos.update replaces the whole status part. These are the fields YouTube returns and
# accepts on write; anything present on the video is carried over so nothing is silently lost.
CARRY = ("privacyStatus", "publishAt", "license", "embeddable", "publicStatsViewable",
         "selfDeclaredMadeForKids", "madeForKids", "containsSyntheticMedia")
# madeForKids is read-only on write; selfDeclaredMadeForKids is the writable one.
WRITE_ONLY = tuple(f for f in CARRY if f != "madeForKids")


def _request(url: str, token: str, data: bytes | None = None, method: str | None = None) -> dict:
    req = urllib.request.Request(
        url, data=data,
        headers={"Authorization": f"Bearer {token}",
                 "Content-Type": "application/json; charset=UTF-8"},
        method=method)
    with urllib.request.urlopen(req, timeout=90) as resp:
        return json.loads(resp.read().decode("utf-8"))


def get_status(video_id: str, token: str) -> dict:
    d = _request(f"{API}?part=status&id={video_id}", token)
    items = d.get("items") or []
    if not items:
        raise SystemExit(f"{video_id}: no such video, or it is not on this channel")
    return items[0].get("status") or {}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", action="append", required=True, help="video id (repeatable)")
    ap.add_argument("--reason", default="", help="why -- recorded in the ledger")
    ap.add_argument("--restore", metavar="RFC3339",
                    help="put a publishAt back instead of clearing it")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    from pd_factory.providers import load_env
    from pd_factory.providers.youtube import _access_token
    token = _access_token(load_env())

    now = datetime.now(timezone.utc).isoformat()
    records = []
    failures = 0

    for vid in a.video:
        before = get_status(vid, token)
        status = {k: before[k] for k in WRITE_ONLY if k in before}

        if a.restore:
            status["privacyStatus"] = "private"
            status["publishAt"] = a.restore
            intent = f"publishAt -> {a.restore}"
        else:
            status["privacyStatus"] = "private"
            status.pop("publishAt", None)
            intent = "publishAt cleared, stays private"

        print(f"[pause] {vid}: {before.get('privacyStatus')} "
              f"publishAt={before.get('publishAt')}  ->  {intent}")

        if a.dry_run:
            records.append({"video_id": vid, "dry_run": True, "before": before})
            continue

        body = {"id": vid, "status": status}
        try:
            _request(f"{API}?part=status", token,
                     data=json.dumps(body).encode("utf-8"), method="PUT")
        except urllib.error.HTTPError as exc:
            print(f"  FAILED: HTTP {exc.code} {(exc.read() or b'')[:300].decode('utf-8', 'replace')}")
            failures += 1
            records.append({"video_id": vid, "ok": False, "before": before})
            continue

        # Read it back. An accepted PUT is not proof the state changed.
        # The read is eventually consistent: on 2026-08-05 two videos read back with the OLD
        # publishAt immediately after a PUT that had in fact applied, and a plain read seconds
        # later showed them cleared. Reporting that as a failure is as harmful as reporting a
        # failure as success -- it invites a re-run that thrashes the schedule. So retry.
        want = a.restore or None
        for attempt in range(5):
            after = get_status(vid, token)
            ok = (after.get("publishAt") == want
                  and after.get("privacyStatus") == "private")
            if ok:
                break
            if attempt < 4:
                time.sleep(2 * (attempt + 1))
                print(f"  read back stale (publishAt={after.get('publishAt')}), retrying")
        print(f"  read back: privacy={after.get('privacyStatus')} "
              f"publishAt={after.get('publishAt')}  {'OK' if ok else 'MISMATCH'}")
        if not ok:
            failures += 1
        records.append({"video_id": vid, "ok": ok, "before": before, "after": after})

    if not a.dry_run:
        LEDGER.parent.mkdir(parents=True, exist_ok=True)
        led = json.loads(LEDGER.read_text(encoding="utf-8")) if LEDGER.is_file() else {"runs": []}
        led["runs"].append({"at": now, "reason": a.reason,
                            "action": "restore" if a.restore else "pause",
                            "videos": records})
        LEDGER.write_text(json.dumps(led, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"[pause] recorded in {LEDGER.relative_to(ROOT)}")

    if failures:
        print(f"[pause] {failures} video(s) did NOT reach the intended state")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
