#!/usr/bin/env python3
r"""Apply the CTR-v002 title rewrites to LIVE videos (videos.update, snippet only).

Reads episodes/_planning/title_refresh_mapping.v001.json
    [{"slug": "...", "video_id": "...", "new_title": "..."}, ...]

Safety:
- GETs the CURRENT full snippet first and resends it with ONLY the title replaced
  (videos.update with part=snippet WIPES any omitted snippet field — description,
  tags, categoryId etc. are preserved by round-tripping them verbatim).
- status/publishAt is NEVER part of the request (part=snippet only).
- Dry-run by default; --apply to write. Receipt JSON with before/after titles.

    py -3.11 scripts/apply_title_refresh_v001.py            # dry run
    py -3.11 scripts/apply_title_refresh_v001.py --apply
    py -3.11 scripts/apply_title_refresh_v001.py --only 029-hinton
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
MAPPING = ROOT / "episodes" / "_planning" / "title_refresh_mapping.v001.json"
RECEIPT = ROOT / "episodes" / "_planning" / "title_refresh_receipt.v001.json"
SPACING_S = 8


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


def get_snippet(tok: str, vid: str) -> dict | None:
    req = urllib.request.Request(
        f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={vid}",
        headers={"Authorization": f"Bearer {tok}"})
    with urllib.request.urlopen(req, timeout=30) as r:
        items = json.loads(r.read().decode()).get("items", [])
    return items[0]["snippet"] if items else None


def put_title(tok: str, vid: str, snippet: dict, new_title: str):
    body = {"id": vid, "snippet": {**snippet, "title": new_title}}
    # thumbnails/localized are read-only echoes; drop to keep the payload clean
    body["snippet"].pop("thumbnails", None)
    body["snippet"].pop("localized", None)
    req = urllib.request.Request(
        "https://www.googleapis.com/youtube/v3/videos?part=snippet",
        data=json.dumps(body).encode(), method="PUT",
        headers={"Authorization": f"Bearer {tok}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode() or "{}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--only", default="")
    a = ap.parse_args()

    entries = json.loads(MAPPING.read_text(encoding="utf-8"))
    only = {s.strip() for s in a.only.split(",") if s.strip()}
    targets = [e for e in entries if not only or e["slug"] in only]
    print(f"targets: {len(targets)} (mode: {'APPLY' if a.apply else 'dry-run'})", flush=True)

    tok = token()
    receipt = {"generated_at": datetime.now(timezone.utc).isoformat(),
               "mode": "apply" if a.apply else "dry-run", "results": []}

    for i, e in enumerate(targets):
        slug, vid, new_title = e["slug"], e["video_id"], e["new_title"]
        print(f"\n[{slug}] {vid}", flush=True)
        snip = get_snippet(tok, vid)
        if snip is None:
            print("  VIDEO NOT FOUND -- SKIP", flush=True)
            receipt["results"].append({"slug": slug, "video_id": vid, "status": "video_not_found"})
            continue
        before = snip.get("title", "")
        print(f"  before: {before}", flush=True)
        print(f"  after : {new_title}", flush=True)
        if before == new_title:
            receipt["results"].append({"slug": slug, "video_id": vid, "status": "unchanged"})
            continue
        if not a.apply:
            receipt["results"].append({"slug": slug, "video_id": vid, "status": "dry_run_ok",
                                       "before": before, "after": new_title})
            continue
        st, b = put_title(tok, vid, snip, new_title)
        ok = st == 200
        print(f"  {'OK' if ok else 'FAILED'} (HTTP {st}) {json.dumps(b)[:120] if not ok else ''}", flush=True)
        receipt["results"].append({"slug": slug, "video_id": vid,
                                   "status": "applied" if ok else f"failed_{st}",
                                   "before": before, "after": new_title})
        if i < len(targets) - 1:
            time.sleep(SPACING_S)

    RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=1), encoding="utf-8")
    n_ok = sum(1 for r in receipt["results"] if r["status"] in ("applied", "dry_run_ok", "unchanged"))
    print(f"\nreceipt -> {RECEIPT.name}  ok={n_ok}/{len(receipt['results'])}", flush=True)
    return 0 if n_ok == len(receipt["results"]) else 1


if __name__ == "__main__":
    raise SystemExit(main())
