#!/usr/bin/env python3
r"""Flip PD-2026-002-gideon from PRIVATE to PUBLIC on YouTube (owner-approved final step).

Guards: APR-0004 approved + video_id from upload_result.json. Sets privacyStatus=public.
    py -3.11 scripts/publish_gideon.py [--dry-run]
"""
from __future__ import annotations
import argparse, json, sys, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from pd_factory.providers import load_env
from pd_factory.providers.youtube import _access_token

EP = "PD-2026-002-gideon"
EPDIR = ROOT / "episodes" / EP
APR = EPDIR / "approvals" / "APR-0004.json"
UPLOAD = EPDIR / "09_package" / "upload_result.json"


def main(argv):
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(); ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    apr = json.loads(APR.read_text("utf-8"))
    if apr.get("decision") != "approved":
        print(f"BLOCKED: APR-0004 decision={apr.get('decision')!r}"); return 1
    vid = json.loads(UPLOAD.read_text("utf-8"))["video_id"]
    print(f"✓ APR-0004 approved; video_id={vid}")
    if args.dry_run:
        print("[dry-run] would set privacyStatus=public."); return 0

    env = load_env(); token = _access_token(env)
    body = json.dumps({"id": vid, "status": {"privacyStatus": "public", "selfDeclaredMadeForKids": False}}).encode()
    req = urllib.request.Request(
        "https://www.googleapis.com/youtube/v3/videos?part=status",
        data=body, headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}, method="PUT")
    with urllib.request.urlopen(req, timeout=60) as r:
        res = json.loads(r.read().decode())
    status = res.get("status", {}).get("privacyStatus")
    print(f"✓ privacyStatus = {status}")
    print(f"\nPUBLIC: https://youtu.be/{vid}")
    return 0 if status == "public" else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
