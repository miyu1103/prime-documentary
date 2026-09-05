#!/usr/bin/env python3
r"""Re-apply the fixed v002 face thumbnails to the LIVE videos (thumbnails.set).

Only the OVERLAP-fixed episodes that are actually uploaded get an API call:
  cleveland AxOlQ2NIaBU, tlo hC5KE6IqmhM, atwater i95peRcdtz4.
glover/strieff are local-only (not uploaded) -> never called. caniglia is queued for
SDXL regen -> no v002 yet -> not called here.

thumbnails.set is rate-limited: calls are spaced ~42s apart, with exponential backoff
retries on 403/429/5xx. Dry-run by default; pass --apply to write.

    py -3.11 scripts/apply_thumbnails_v002.py            # dry run (checks files+token)
    py -3.11 scripts/apply_thumbnails_v002.py --apply
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
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
ENV = ROOT / ".env"
OUTDIR = ROOT / "episodes" / "_planning"
SPACING_S = 42
MAX_BYTES = 2 * 1024 * 1024

# episode -> (video_id, thumb relative path). Only LIVE + fixed episodes.
TARGETS = [
    ("043-caniglia",  "yRwxBfrOY5o", "episodes/PD-2026-043-caniglia/09_package/thumbnail.face.v002.png"),
    ("045-cleveland", "AxOlQ2NIaBU", "episodes/PD-2026-045-cleveland/09_package/thumbnail.face.v002.png"),
    ("046-tlo",       "hC5KE6IqmhM", "episodes/PD-2026-046-tlo/09_package/thumbnail.face.v002.png"),
    ("047-atwater",   "i95peRcdtz4", "episodes/PD-2026-047-atwater/09_package/thumbnail.face.v002.png"),
]


def load_env() -> dict:
    env = {}
    for line in ENV.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def token() -> str:
    import urllib.parse
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
    for attempt in range(1, tries + 1):
        st, b = set_thumb(tok, vid, img_bytes)
        if st == 200:
            return st, b
        transient = st in (403, 429, 500, 503)
        reason = (b.get("error", {}).get("errors", [{}])[0].get("reason", "")
                  if isinstance(b, dict) else "")
        # a real quota/permission 403 (not rate) should not be retried forever
        hard = reason in ("quotaExceeded", "forbidden", "thumbnailSizeTooLarge",
                          "invalidImage", "mediaBodyRequired")
        print(f"    attempt {attempt}: HTTP {st} reason={reason!r} {json.dumps(b)[:160]}", flush=True)
        if st == 200 or hard or not transient or attempt == tries:
            return st, b
        print(f"    transient -> backoff {delay}s", flush=True)
        time.sleep(delay)
        delay = min(delay * 2, 180)
    return st, b


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--only", default="", help="comma-separated slug filter, e.g. 043-caniglia")
    a = ap.parse_args()

    only = {s.strip() for s in a.only.split(",") if s.strip()}
    targets = [t for t in TARGETS if not only or t[0] in only]

    tok = token()
    print("access token OK", flush=True)
    receipt = {"generated_at": datetime.now(timezone.utc).isoformat(),
               "mode": "apply" if a.apply else "dry-run", "results": []}

    for i, (ep, vid, rel) in enumerate(targets):
        p = ROOT / rel
        print(f"\n[{ep}] {vid}", flush=True)
        if not p.exists():
            print(f"  MISSING FILE {p} -- SKIP", flush=True)
            receipt["results"].append({"ep": ep, "video_id": vid, "status": "missing_file"})
            continue
        nbytes = p.stat().st_size
        print(f"  file: {p.name} ({nbytes/1024:.0f} KB)", flush=True)
        if nbytes > MAX_BYTES:
            print("  FILE > 2MB -- SKIP", flush=True)
            receipt["results"].append({"ep": ep, "video_id": vid, "status": "too_large"})
            continue
        before = get_thumbs(tok, vid)
        before_hi = (before or {}).get("high", {}).get("url", "") if before else ""
        print(f"  before high thumb: {before_hi}", flush=True)
        if not a.apply:
            print("  (dry run -- no write)", flush=True)
            receipt["results"].append({"ep": ep, "video_id": vid, "status": "dry_run_ok",
                                       "bytes": nbytes, "before_high": before_hi})
            continue
        img = p.read_bytes()
        st, b = set_with_retry(tok, vid, img)
        ok = st == 200
        got = b.get("items", [{}])[0] if ok else {}
        new_hi = got.get("high", {}).get("url", "") if ok else ""
        print(f"  set -> HTTP {st} {'OK' if ok else 'FAIL'}  new_high={new_hi}", flush=True)
        receipt["results"].append({"ep": ep, "video_id": vid,
                                   "status": "applied" if ok else f"error_{st}",
                                   "http": st, "new_high": new_hi,
                                   "error": None if ok else b})
        # space out the next call (rate limit) -- skip after the last
        if a.apply and i < len(targets) - 1:
            print(f"  spacing {SPACING_S}s before next call...", flush=True)
            time.sleep(SPACING_S)

    tag = "apply" if a.apply else "dryrun"
    out = OUTDIR / f"thumbnail_v002_apply_receipt.{tag}.json"
    out.write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nwrote {out}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
