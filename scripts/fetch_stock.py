#!/usr/bin/env python
"""U2 - Free stock fetch (Pexels + Pixabay) driven by the episode shotlist.

For each stock shot in 04_scenes/shotlist.v001.json (or an explicit --query), searches the free
APIs, downloads candidates to the media SSD (05_stock/candidates/), and appends a rights record
(source/author/license/date/query/sha256/used_in_spans) to 05_stock/stock_ledger.v001.json.
Pexels and Pixabay grant commercial use, so records are written commercial_use=allowed; the rights
GATE (build_usable_assets.py) still re-checks before anything reaches the timeline.

API keys are read from <repo>/.env  (PEXELS_API_KEY=, PIXABAY_API_KEY=) - never committed.
Default is a DRY-RUN that prints the planned queries; --write performs the network fetch and
appends the ledger. Idempotent: a candidate whose sha256 is already in the ledger is skipped.

Usage:
  .venv/Scripts/python.exe scripts/fetch_stock.py 11                       # dry-run plan
  .venv/Scripts/python.exe scripts/fetch_stock.py 11 --write               # fetch + ledger
  .venv/Scripts/python.exe scripts/fetch_stock.py 11 --query "phone at night" --write
  .venv/Scripts/python.exe scripts/fetch_stock.py 11 --per-source 2 --images
"""
from __future__ import annotations
import sys, os, json, glob, hashlib, tempfile, urllib.request, urllib.parse
from typing import Any

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EPDIR = os.path.join(ROOT, "episodes")
UA = {"User-Agent": "Mozilla/5.0 PD-stock/1.0"}


def load_env() -> dict[str, str]:
    env: dict[str, str] = {}
    p = os.path.join(ROOT, ".env")
    if os.path.exists(p):
        for ln in open(p, encoding="utf-8"):
            ln = ln.strip()
            if ln and not ln.startswith("#") and "=" in ln:
                k, v = ln.split("=", 1)
                env[k.strip()] = v.strip().strip('"').strip("'")
    for k in ("PEXELS_API_KEY", "PIXABAY_API_KEY"):
        if os.environ.get(k):
            env[k] = os.environ[k]
    return env


def media_root() -> str | None:
    cfg = os.path.join(ROOT, "config", "storage.local.json")
    return json.load(open(cfg, encoding="utf-8"))["roots"]["media"]["path"] if os.path.exists(cfg) else None


def resolve_ep(arg: str) -> str:
    if os.path.isdir(os.path.join(EPDIR, arg)):
        return arg
    hits = [os.path.basename(p) for p in glob.glob(os.path.join(EPDIR, f"PD-*-{int(arg):03d}-*"))] if arg.isdigit() else []
    if not hits:
        hits = [os.path.basename(p) for p in glob.glob(os.path.join(EPDIR, f"*{arg}*")) if os.path.isdir(p)]
    if len(hits) == 1:
        return hits[0]
    raise SystemExit(f"Could not resolve episode '{arg}'. Matches: {hits}")


def http_json(url: str, headers: dict[str, str]) -> dict[str, Any]:
    req = urllib.request.Request(url, headers={**UA, **headers})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


def download(url: str, dest: str) -> tuple[str, int]:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=120) as r:
        data = r.read()
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(dest), suffix=".tmp")
    with os.fdopen(fd, "wb") as f:
        f.write(data)
    os.replace(tmp, dest)
    return "sha256:" + hashlib.sha256(data).hexdigest(), len(data)


def pexels_video(q: str, key: str, n: int) -> list[dict[str, Any]]:
    url = "https://api.pexels.com/videos/search?" + urllib.parse.urlencode(
        {"query": q, "per_page": n, "orientation": "landscape", "size": "medium"})
    out = []
    for v in http_json(url, {"Authorization": key}).get("videos", []):
        files = [f for f in v.get("video_files", []) if (f.get("height") or 0) <= 1080 and f.get("link")]
        files.sort(key=lambda f: f.get("height") or 0, reverse=True)
        if files:
            out.append({"id": f"pexels_v_{v['id']}", "dl": files[0]["link"], "ext": ".mp4", "type": "video",
                        "source": "pexels", "license": "Pexels License", "url": v.get("url", ""),
                        "author": (v.get("user") or {}).get("name")})
    return out


def pexels_image(q: str, key: str, n: int) -> list[dict[str, Any]]:
    url = "https://api.pexels.com/v1/search?" + urllib.parse.urlencode({"query": q, "per_page": n, "orientation": "landscape"})
    out = []
    for p in http_json(url, {"Authorization": key}).get("photos", []):
        link = (p.get("src") or {}).get("large2x") or (p.get("src") or {}).get("large")
        if link:
            out.append({"id": f"pexels_i_{p['id']}", "dl": link, "ext": ".jpg", "type": "image",
                        "source": "pexels", "license": "Pexels License", "url": p.get("url", ""),
                        "author": p.get("photographer")})
    return out


def pixabay_video(q: str, key: str, n: int) -> list[dict[str, Any]]:
    url = "https://pixabay.com/api/videos/?" + urllib.parse.urlencode({"key": key, "q": q, "per_page": max(3, n)})
    out = []
    for h in http_json(url, {}).get("hits", [])[:n]:
        vids = h.get("videos") or {}
        pick = vids.get("medium") or vids.get("large") or vids.get("small") or {}
        if pick.get("url"):
            out.append({"id": f"pixabay_v_{h['id']}", "dl": pick["url"], "ext": ".mp4", "type": "video",
                        "source": "pixabay", "license": "Pixabay Content License", "url": h.get("pageURL", ""),
                        "author": h.get("user")})
    return out


def pixabay_image(q: str, key: str, n: int) -> list[dict[str, Any]]:
    url = "https://pixabay.com/api/?" + urllib.parse.urlencode({"key": key, "q": q, "per_page": max(3, n), "image_type": "photo"})
    out = []
    for h in http_json(url, {}).get("hits", [])[:n]:
        if h.get("largeImageURL"):
            out.append({"id": f"pixabay_i_{h['id']}", "dl": h["largeImageURL"], "ext": ".jpg", "type": "image",
                        "source": "pixabay", "license": "Pixabay Content License", "url": h.get("pageURL", ""),
                        "author": h.get("user")})
    return out


def queries_from_shotlist(b: str) -> list[tuple[str, list[str]]]:
    sl = os.path.join(b, "04_scenes", "shotlist.v001.json")
    if not os.path.exists(sl):
        return []
    out = []
    for s in json.load(open(sl, encoding="utf-8"))["shots"]:
        if s["suggested_asset_type"] in ("stock_video", "stock_image") and s.get("search_keywords"):
            out.append((s["search_keywords"][0], [s["span_id"]]))
    return out


def load_ledger(path: str, ep_id: str) -> dict[str, Any]:
    if os.path.exists(path):
        return json.load(open(path, encoding="utf-8"))
    return {"schema_version": "1.0.0", "episode_id": ep_id, "revision": "v001", "kind": "ledger", "assets": []}


def save_ledger(path: str, doc: dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(path), suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
    os.replace(tmp, path)


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    argv = sys.argv[1:]
    write = "--write" in argv
    images = "--images" in argv
    per = int(argv[argv.index("--per-source") + 1]) if "--per-source" in argv else 1
    query = argv[argv.index("--query") + 1] if "--query" in argv else None
    pos = [a for a in argv if not a.startswith("--") and a != query and (not a.isdigit() or a == argv[0])]
    if not pos:
        raise SystemExit("usage: fetch_stock.py <episode> [--query Q] [--per-source N] [--images] [--write]")
    ep = resolve_ep(pos[0])
    b = os.path.join(EPDIR, ep)
    ep_id = os.path.basename(ep)
    env = load_env()
    pk, xk = env.get("PEXELS_API_KEY"), env.get("PIXABAY_API_KEY")

    plan = [(query, [])] if query else queries_from_shotlist(b)
    if not plan:
        print("No stock queries (no --query and no stock_video/stock_image keywords in shotlist).")
        return 0
    print(f"Episode: {ep_id}   queries: {len(plan)}   per-source: {per}   images: {images}")
    print(f"Keys: PEXELS={'set' if pk else 'MISSING'}  PIXABAY={'set' if xk else 'MISSING'}")
    for q, spans in plan[:20]:
        print(f"  q='{q}'  spans={spans or '-'}")

    if not write:
        print("\n(dry-run) pass --write to fetch. Needs PEXELS_API_KEY / PIXABAY_API_KEY in .env (free signup).")
        return 0
    if not (pk or xk):
        print("\nNO API KEYS. Add to <repo>/.env:\n  PEXELS_API_KEY=...\n  PIXABAY_API_KEY=...\n(both free). Aborting fetch.")
        return 1

    mr = media_root()
    cand_dir = (os.path.join(mr, "episodes", ep_id, "05_stock", "candidates") if mr
                else os.path.join(b, "05_stock", "candidates"))
    os.makedirs(cand_dir, exist_ok=True)
    ledger_path = os.path.join(b, "05_stock", "stock_ledger.v001.json")
    ledger = load_ledger(ledger_path, ep_id)
    seen_ids = {a["asset_id"] for a in ledger["assets"]}
    seen_hash = {a.get("sha256") for a in ledger["assets"]}
    added = 0
    for q, spans in plan:
        cands: list[dict[str, Any]] = []
        try:
            if pk:
                cands += pexels_video(q, pk, per) + (pexels_image(q, pk, per) if images else [])
            if xk:
                cands += pixabay_video(q, xk, per) + (pixabay_image(q, xk, per) if images else [])
        except Exception as e:
            print(f"  search error q='{q}': {e}")
            continue
        for c in cands:
            if c["id"] in seen_ids:
                continue
            dest = os.path.join(cand_dir, c["id"] + c["ext"])
            try:
                sha, nbytes = download(c["dl"], dest)
            except Exception as e:
                print(f"  download error {c['id']}: {e}")
                continue
            if sha in seen_hash:
                os.remove(dest)
                continue
            rel = (f"episodes/{ep_id}/05_stock/candidates/{c['id']}{c['ext']}" if mr
                   else os.path.relpath(dest, ROOT).replace(os.sep, "/"))
            ledger["assets"].append({
                "asset_id": c["id"], "asset_type": c["type"], "source": c["source"],
                "source_url": c["url"], "author": c["author"], "license": c["license"],
                "commercial_use": "allowed",
                "file": ("artifact://" + rel) if mr else rel,
                "sha256": sha, "bytes": nbytes, "query": q, "depicts": q,
                "fetched_at": "", "used_in_spans": spans,
            })
            seen_ids.add(c["id"]); seen_hash.add(sha); added += 1
            print(f"  + {c['source']:<7} {c['type']:<5} {c['id']}  ({nbytes//1024} KB)  q='{q}'")
    save_ledger(ledger_path, ledger)
    print(f"\nAdded {added} asset(s). Ledger: {os.path.relpath(ledger_path, ROOT)} (total {len(ledger['assets'])}).")
    print("Next: build_usable_assets.py <ep> --write   ->   import_to_remotion.py <ep> --write")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
