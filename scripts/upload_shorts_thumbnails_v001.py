#!/usr/bin/env python3
"""Set the dedicated ShortThumbYT 16:9 thumbnail on every published Short.

Reads runs/shorts_thumbs/mapping.v001.json (video_id -> matched_short_data),
and for each unique video_id uploads runs/shorts_thumbs/samples/<short_id>.png
via thumbnails.set. Idempotent; reversible (thumbnails can be replaced anytime).

    py -3.11 scripts/upload_shorts_thumbnails_v001.py --dry-run
    py -3.11 scripts/upload_shorts_thumbnails_v001.py
"""
from __future__ import annotations
import argparse, json, sys, time
import urllib.request, urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))
from pd_factory.providers import load_env
from pd_factory.providers.youtube import _access_token

MAP = ROOT / "runs" / "shorts_thumbs" / "mapping.v001.json"
THUMB_DIR = ROOT / "runs" / "shorts_thumbs" / "samples"
CHANNEL_ALLOWLIST = {"UCuQPtAz1rca9eJ4xhvX0yKA"}


def get_channel_id(token):
    r = urllib.request.Request(
        "https://www.googleapis.com/youtube/v3/channels?part=id&mine=true",
        headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(r, timeout=60) as resp:
        return json.loads(resp.read().decode())["items"][0]["id"]


def set_thumbnail(token, video_id, path: Path):
    data = path.read_bytes()
    r = urllib.request.Request(
        f"https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId={video_id}",
        data=data, headers={"Authorization": f"Bearer {token}", "Content-Type": "image/png"},
        method="POST")
    with urllib.request.urlopen(r, timeout=120) as resp:
        return json.loads(resp.read().decode())


def main(argv):
    try: sys.stdout.reconfigure(encoding="utf-8")
    except Exception: pass
    ap = argparse.ArgumentParser(); ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    entries = json.loads(MAP.read_text(encoding="utf-8"))
    if isinstance(entries, dict):
        entries = entries.get("shorts", entries.get("mapping", []))
    # dedupe by video_id (playlist can list dupes)
    seen = {}
    for e in entries:
        seen.setdefault(e["video_id"], e)
    uniq = list(seen.values())
    print(f"{len(uniq)} unique shorts to thumbnail")

    # preflight: every thumb file exists + <2MB
    missing = []
    for e in uniq:
        p = THUMB_DIR / f"{e['matched_short_data']}.png"
        if not p.exists(): missing.append(str(p))
        elif p.stat().st_size > 2_000_000: missing.append(f"{p} OVER 2MB")
    if missing:
        print("BLOCKED: thumbnail files missing/oversized:"); [print("  ", m) for m in missing]
        return 1

    env = load_env(); token = _access_token(env)
    ch = get_channel_id(token)
    if ch not in CHANNEL_ALLOWLIST:
        print(f"BLOCKED: channel {ch} not allowlisted"); return 1
    print(f"OK channel {ch}")

    if args.dry_run:
        for e in uniq:
            print(f"  [dry] {e['video_id']}  <- {e['matched_short_data']}.png  ({e['title'][:40]})")
        print(f"[dry-run] would set {len(uniq)} thumbnails. No API writes.")
        return 0

    ok = 0; fails = []
    for i, e in enumerate(uniq, 1):
        vid = e["video_id"]; p = THUMB_DIR / f"{e['matched_short_data']}.png"
        for attempt in range(3):
            try:
                set_thumbnail(token, vid, p); ok += 1
                print(f"  [{i}/{len(uniq)}] OK {vid} <- {p.name}")
                break
            except urllib.error.HTTPError as ex:
                body = ex.read().decode()[:120]
                if attempt == 2:
                    fails.append((vid, f"HTTP {ex.code} {body}"))
                    print(f"  [{i}/{len(uniq)}] FAIL {vid}: HTTP {ex.code} {body}")
                else:
                    time.sleep(5)
            except Exception as ex:
                if attempt == 2:
                    fails.append((vid, str(ex)[:120]))
                    print(f"  [{i}/{len(uniq)}] FAIL {vid}: {str(ex)[:120]}")
                else:
                    time.sleep(5)
        time.sleep(0.5)

    result = {"total": len(uniq), "ok": ok, "failed": len(fails),
              "failures": [{"video_id": v, "error": er} for v, er in fails]}
    (ROOT / "runs" / "shorts_thumbs" / "upload_result.v001.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nDONE: {ok}/{len(uniq)} thumbnails set. {len(fails)} failed.")
    return 0 if not fails else 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
