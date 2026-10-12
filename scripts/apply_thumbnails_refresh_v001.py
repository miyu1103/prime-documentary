#!/usr/bin/env python3
r"""Apply the CTR-v002 "Night story-frame" thumbnail refresh to LIVE videos.

Clone of apply_thumbnails_v002.py mechanics (video_id-keyed thumbnails.set, dry-run by
default, ~42s spacing, exponential backoff, receipt JSON) but TARGETS come from a
mapping file instead of a hardcoded list:

    episodes/_planning/thumbnail_refresh_mapping.v001.json
    [{"slug": "029-hinton", "video_id": "Qyad4FejCIc", "thumb": "<abs-or-repo-rel path>"}, ...]

thumbnails.set swaps ONLY the image — publishAt / status / metadata are never touched.

    py -3.11 scripts/apply_thumbnails_refresh_v001.py            # dry run
    py -3.11 scripts/apply_thumbnails_refresh_v001.py --apply
    py -3.11 scripts/apply_thumbnails_refresh_v001.py --only 029-hinton,037-florence
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
ENV = ROOT / ".env"
MAPPING = ROOT / "episodes" / "_planning" / "thumbnail_refresh_mapping.v001.json"
RECEIPT = ROOT / "episodes" / "_planning" / "thumbnail_refresh_receipt.v001.json"
SPACING_S = 42
MAX_BYTES = 2 * 1024 * 1024


def load_env() -> dict:
    env = {}
    for line in ENV.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def token() -> str:
    env = load_env()
    data = urllib.parse.urlencode({
        "client_id": env["YOUTUBE_CLIENT_ID"], "client_secret": env["YOUTUBE_CLIENT_SECRET"],
        "refresh_token": env["YOUTUBE_REFRESH_TOKEN"], "grant_type": "refresh_token"}).encode()
    req = urllib.request.Request("https://oauth2.googleapis.com/token", data=data,
                                 headers={"Content-Type": "application/x-www-form-urlencoded"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())["access_token"]


def get_thumbs(tok, vid):
    req = urllib.request.Request(
        f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={vid}",
        headers={"Authorization": f"Bearer {tok}"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            b = json.loads(r.read().decode())
        items = b.get("items", [])
        if not items:
            return None
        return items[0]["snippet"].get("thumbnails", {})
    except urllib.error.HTTPError as e:
        return {"_error": e.code}


def set_thumb(tok, vid, img_bytes):
    url = f"https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId={vid}&uploadType=media"
    req = urllib.request.Request(url, data=img_bytes, method="POST",
                                 headers={"Authorization": f"Bearer {tok}",
                                          "Content-Type": "image/png"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return r.status, json.loads(r.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode() or "{}")


def set_with_retry(tok, vid, img_bytes, tries=5):
    delay = 20
    st, b = 0, {}
    for attempt in range(1, tries + 1):
        st, b = set_thumb(tok, vid, img_bytes)
        if st == 200:
            return st, b
        reason = (b.get("error", {}).get("errors", [{}])[0].get("reason", "")
                  if isinstance(b, dict) else "")
        hard = reason in ("quotaExceeded", "forbidden", "thumbnailSizeTooLarge",
                          "invalidImage", "mediaBodyRequired")
        transient = st in (403, 429, 500, 503) and not hard
        print(f"    attempt {attempt}: HTTP {st} reason={reason!r} {json.dumps(b)[:160]}", flush=True)
        if not transient or attempt == tries:
            return st, b
        print(f"    transient -> backoff {delay}s", flush=True)
        time.sleep(delay)
        delay = min(delay * 2, 180)
    return st, b


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--only", default="", help="comma-separated slug filter")
    ap.add_argument("--mapping", type=Path, default=MAPPING)
    a = ap.parse_args()

    global RECEIPT
    if a.mapping != MAPPING:
        # per-mapping receipt so a second batch never clobbers the first record
        RECEIPT = a.mapping.with_name(a.mapping.stem + ".receipt.json")
    entries = json.loads(a.mapping.read_text(encoding="utf-8"))
    only = {s.strip() for s in a.only.split(",") if s.strip()}
    targets = [e for e in entries if not only or e["slug"] in only]
    print(f"targets: {len(targets)} (mode: {'APPLY' if a.apply else 'dry-run'})", flush=True)

    tok = token()
    print("access token OK", flush=True)
    receipt = {"generated_at": datetime.now(timezone.utc).isoformat(),
               "mode": "apply" if a.apply else "dry-run", "results": []}

    for i, e in enumerate(targets):
        slug, vid = e["slug"], e["video_id"]
        p = Path(e["thumb"])
        if not p.is_absolute():
            p = ROOT / p
        print(f"\n[{slug}] {vid}", flush=True)
        if not p.exists():
            print(f"  MISSING FILE {p} -- SKIP", flush=True)
            receipt["results"].append({"slug": slug, "video_id": vid, "status": "missing_file"})
            continue
        nbytes = p.stat().st_size
        print(f"  file: {p.name} ({nbytes/1024:.0f} KB)", flush=True)
        if nbytes > MAX_BYTES:
            print("  FILE > 2MB -- SKIP", flush=True)
            receipt["results"].append({"slug": slug, "video_id": vid, "status": "too_large"})
            continue
        before = get_thumbs(tok, vid)
        if before is None:
            print("  VIDEO NOT FOUND -- SKIP", flush=True)
            receipt["results"].append({"slug": slug, "video_id": vid, "status": "video_not_found"})
            continue
        before_hi = before.get("high", {}).get("url", "") if isinstance(before, dict) else ""
        print(f"  before high thumb: {before_hi}", flush=True)
        if not a.apply:
            receipt["results"].append({"slug": slug, "video_id": vid, "status": "dry_run_ok",
                                       "bytes": nbytes, "before_high": before_hi})
            continue
        st, b = set_with_retry(tok, vid, p.read_bytes())
        ok = st == 200
        print(f"  {'OK' if ok else 'FAILED'} (HTTP {st})", flush=True)
        receipt["results"].append({"slug": slug, "video_id": vid,
                                   "status": "applied" if ok else f"failed_{st}",
                                   "bytes": nbytes, "before_high": before_hi})
        if i < len(targets) - 1:
            time.sleep(SPACING_S)

    RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=1), encoding="utf-8")
    n_ok = sum(1 for r in receipt["results"] if r["status"] in ("applied", "dry_run_ok"))
    print(f"\nreceipt -> {RECEIPT.name}  ok={n_ok}/{len(receipt['results'])}", flush=True)
    return 0 if n_ok == len(receipt["results"]) else 1


if __name__ == "__main__":
    raise SystemExit(main())
