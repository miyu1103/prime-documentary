#!/usr/bin/env python
"""Build/extend the shared reusable stock library (references/stock_manifest.json).

Fetches a FEW rights-clean clips/photos per common documentary B-roll theme (courtroom, money,
phone, city, ...) from Pexels/Pixabay, so every episode can reuse them (build_usable_assets.py
auto-merges this manifest). This is a curated handful per theme - NOT a mass mirror (mass
downloading violates both sites' terms and risks a ban). Idempotent: skips assets already logged.

Keys from <repo>/.env (PEXELS_API_KEY / PIXABAY_API_KEY). Default dry-run; --write fetches.
Usage:
  .venv/Scripts/python.exe scripts/build_library.py                 # show the plan
  .venv/Scripts/python.exe scripts/build_library.py --write         # build it
  .venv/Scripts/python.exe scripts/build_library.py --per-source 3 --write
"""
from __future__ import annotations
import sys, os, json, tempfile
import fetch_stock as fs  # reuse the search/download helpers (no duplicate implementation)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(ROOT, "references", "stock_manifest.json")
TODAY = "2026-06-21"

# Common, recurring B-roll themes for this channel (US court cases / rights / fraud).
THEMES = {
    "courtroom": "empty courtroom",
    "gavel": "judge gavel",
    "supreme_court": "supreme court building washington",
    "law_books": "law books shelf",
    "scales_of_justice": "scales of justice",
    "american_flag": "american flag waving",
    "us_capitol": "us capitol building",
    "constitution": "constitution document parchment",
    "police_car": "police car street",
    "police_lights": "police car lights night",
    "handcuffs": "handcuffs",
    "fingerprint": "fingerprint scan",
    "surveillance_camera": "surveillance camera city",
    "smartphone": "hand holding smartphone",
    "phone_typing": "typing on phone screen",
    "social_media": "social media app phone",
    "data_server": "data server room",
    "laptop": "person typing laptop",
    "cash": "stack of cash money",
    "dollars": "us dollar bills",
    "stock_market": "stock market chart screen",
    "bank": "bank building exterior",
    "contract_signing": "signing contract document",
    "business_meeting": "business meeting handshake",
    "city_street_night": "city street at night",
    "suburban_house": "suburban house exterior",
    "classroom": "high school classroom",
    "students_hallway": "students school hallway",
    "prison_bars": "prison cell bars",
    "crowd": "crowd of people walking",
    "protest": "protest signs crowd",
    "hands_closeup": "close up hands",
    "office_workers": "office workers working",
    "highway": "highway cars driving",
    "clock": "clock ticking close up",
    "blood_lab": "blood test laboratory",
}


def load_manifest() -> list[dict]:
    return json.load(open(MANIFEST, encoding="utf-8")) if os.path.exists(MANIFEST) else []


def save_manifest(items: list[dict]) -> None:
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(MANIFEST), suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
    os.replace(tmp, MANIFEST)


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    argv = sys.argv[1:]
    write = "--write" in argv
    per = int(argv[argv.index("--per-source") + 1]) if "--per-source" in argv else 2
    env = fs.load_env()
    pk, xk = env.get("PEXELS_API_KEY"), env.get("PIXABAY_API_KEY")
    mr = fs.media_root()

    print(f"Themes: {len(THEMES)}   per-source: {per} images + 1 video each")
    print(f"Keys: PEXELS={'set' if pk else 'MISSING'}  PIXABAY={'set' if xk else 'MISSING'}   media={mr}")
    if not write:
        print("\n(dry-run) pass --write to build. A few assets per theme only (ToS-friendly).")
        return 0
    if not (pk or xk):
        print("\nNO API KEYS in .env. Aborting.")
        return 1
    if not mr:
        print("\nNo media root (config/storage.local.json). Aborting.")
        return 1

    manifest = load_manifest()
    seen_url = {m.get("source_url") for m in manifest}
    seen_sha = {m.get("sha256") for m in manifest}
    img_dir = os.path.join(mr, "assets", "stock", "images")
    vid_dir = os.path.join(mr, "assets", "stock", "video")
    os.makedirs(img_dir, exist_ok=True)
    os.makedirs(vid_dir, exist_ok=True)
    added = 0
    for theme, q in THEMES.items():
        cands: list[dict] = []
        try:
            if pk:
                cands += fs.pexels_image(q, pk, per) + fs.pexels_video(q, pk, 1)
            if xk:
                cands += fs.pixabay_image(q, xk, per) + fs.pixabay_video(q, xk, 1)
        except Exception as e:
            print(f"  search error '{theme}': {e}")
            continue
        for c in cands:
            if c["url"] in seen_url:
                continue
            sub = vid_dir if c["type"] == "video" else img_dir
            dest = os.path.join(sub, c["id"] + c["ext"])
            try:
                sha, nbytes = fs.download(c["dl"], dest)
            except Exception as e:
                print(f"  download error {c['id']}: {e}")
                continue
            if sha in seen_sha:
                os.remove(dest)
                continue
            rel = "assets/stock/" + ("video/" if c["type"] == "video" else "images/") + c["id"] + c["ext"]
            manifest.append({
                "file": rel, "source_url": c["url"], "license": c["license"],
                "attribution": c.get("author") or "", "depicts": theme, "episode": "all",
                "sha256": sha, "bytes": nbytes, "verified_at": TODAY,
            })
            seen_url.add(c["url"]); seen_sha.add(sha); added += 1
            save_manifest(manifest)  # persist incrementally (resumable / crash-safe)
        print(f"  {theme}: library now {len(manifest)}")
    print(f"\nAdded {added} asset(s). Shared library: references/stock_manifest.json (total {len(manifest)}).")
    print("All episodes auto-reuse these via build_usable_assets.py.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
