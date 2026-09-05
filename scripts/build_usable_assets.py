#!/usr/bin/env python
"""U3 - Rights gate: classify a rights ledger into usable / review / blocked.

Only COMMERCIAL-USE-OK, allowlisted-license, hashed assets become 'usable' (the only thing
import_to_remotion.py is allowed to place on the Remotion timeline). Denylisted sources
(YouTube/TikTok/Instagram/X/news/etc., and Google Images) are BLOCKED. Anything ambiguous
(unknown/editorial/non-commercial license, or no hash) goes to 'review' for a human - it is
never auto-placed.

Input (auto-detected):
  - episodes/<ep>/05_stock/stock_ledger.v001.json  (stock-ledger.schema.json), or
  - --from <path>  e.g. references/stock_manifest.json (legacy list) for a one-off check.
Output (with --write): 05_stock/usable_assets.v001.json + 05_stock/review_queue.v001.json.
Read-only by default (prints the classification summary). No network.

Usage:
  .venv/Scripts/python.exe scripts/build_usable_assets.py 12
  .venv/Scripts/python.exe scripts/build_usable_assets.py 12 --write
  .venv/Scripts/python.exe scripts/build_usable_assets.py 12 --from references/stock_manifest.json
"""
from __future__ import annotations
import sys, os, json, glob, tempfile
from typing import Any
from urllib.parse import urlparse
from jsonschema import Draft202012Validator

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EPDIR = os.path.join(ROOT, "episodes")

# Hosts we never source from (owner denylist). Substring match on netloc.
DENY_HOSTS = ("youtube.com", "youtu.be", "tiktok.com", "instagram.com", "twitter.com", "x.com",
              "facebook.com", "fbcdn.net", "pinterest.", "reddit.com", "ggpht.com",
              "googleusercontent.com", "gstatic.com", "encrypted-tbn", "nytimes.com", "cnn.com",
              "bbc.co", "bbc.com", "foxnews.com", "nbcnews.com", "cbsnews.com", "reuters.com",
              "apnews.com", "washingtonpost.com", "theguardian.com", "dailymail.")
# Licenses we accept for commercial use (substring, lowercased).
ALLOW_LICENSE = ("pexels", "pixabay", "mixkit", "cc0", "public domain", "public-domain", "nasa",
                 "cc by", "cc-by", "attribution 4.0", "attribution 3.0", "wikimedia", "ai", "codex",
                 "sdxl", "generated", "youtube audio library")
# Licenses that force manual review even if otherwise fine.
REVIEW_LICENSE = ("editorial", "non-commercial", "noncommercial", "-nc", " nc", "rights-managed", "unknown")


def host_of(url: str) -> str:
    try:
        return (urlparse(url).netloc or "").lower()
    except Exception:
        return ""


def asset_type_of(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    if ext in (".mp4", ".mov", ".webm", ".m4v"):
        return "video"
    if ext in (".mp3", ".wav", ".m4a", ".aac", ".flac"):
        return "audio"
    return "image"


def source_of(host: str, license_: str) -> str:
    h, l = host, license_.lower()
    if "pexels" in h or "pexels" in l:
        return "pexels"
    if "pixabay" in h or "pixabay" in l:
        return "pixabay"
    if "mixkit" in h or "mixkit" in l:
        return "mixkit"
    if "wikimedia" in h or "wikipedia" in h:
        return "wikimedia"
    if "nasa" in h or "nasa" in l:
        return "nasa"
    if "public domain" in l or "cc0" in l:
        return "public_domain"
    return "other"


def normalize(item: dict[str, Any]) -> dict[str, Any]:
    """Accept both the native ledger item and the legacy stock_manifest item."""
    file = item.get("file") or item.get("uri") or ""
    url = item.get("source_url") or item.get("reference") or ""
    lic = item.get("license") or ""
    host = host_of(url)
    sha = item.get("sha256") or item.get("content_hash")
    out = {
        "asset_id": item.get("asset_id") or os.path.splitext(os.path.basename(file))[0] or "asset",
        "asset_type": item.get("asset_type") or asset_type_of(file),
        "source": item.get("source") or source_of(host, lic),
        "source_url": url,
        "author": item.get("author") or item.get("attribution") or None,
        "license": lic or "unknown",
        "commercial_use": item.get("commercial_use") or "unknown",
        "file": file,
    }
    if sha:
        out["sha256"] = sha if str(sha).startswith("sha256:") else f"sha256:{sha}"
    for k in ("bytes", "query", "depicts", "fetched_at"):
        if item.get(k) is not None:
            out[k] = item[k]
    if item.get("used_in_spans"):
        out["used_in_spans"] = item["used_in_spans"]
    return out


def load_editorial(ep_dir: str) -> dict[str, dict[str, str]]:
    """Verdicts from the human eyeball pass, if one has been done for this episode.

    WHY THIS GATE GREW AN EDITORIAL ARM (2026-08-22, EP72). This script is a RIGHTS gate and it
    was doing its job: all 108 of EP72's harvested clips are Pexels/Pixabay, commercially
    licensed, hashed -- 108 'usable'. Then the clips were watched
    (`runs/qc/lacmegantic_stock_verdicts.v001.md`) and 55 of them could not appear in the film:
    snow in a July story, passenger and steam trains the film bible bars, catenary on an
    unelectrified line, and thirteen clips that are not documentary objects at all -- jellyfish,
    tortoises, an insect, Tokyo at night, five separate Christmas-light toy trains.

    Rights-clean and unusable are different properties, and nothing downstream was checking the
    second one. A clip a human has rejected must not be placeable on the timeline just because
    its licence is fine, so it is routed to `blocked` with the reason carried through. Absent a
    verdicts file this function returns {} and the gate behaves exactly as it always has.
    """
    # `resolve()` returns the episode FOLDER NAME, not a path -- join it onto EPDIR like
    # load_items() does, or this silently finds nothing and the gate reports "NONE".
    p = os.path.join(EPDIR, ep_dir, "05_stock", "editorial_verdicts.v001.json")
    if not os.path.exists(p):
        return {}
    with open(p, encoding="utf-8") as fh:
        return {r["asset_id"]: r for r in json.load(fh)["verdicts"]}


EDITORIAL: dict[str, dict[str, str]] = {}


def _media_root() -> str:
    try:
        with open(os.path.join(ROOT, "config", "storage.local.json"), encoding="utf-8") as fh:
            return json.load(fh)["roots"]["media"]["path"]
    except Exception:
        return ""


MEDIA_ROOT = _media_root()


def on_disk(a: dict[str, Any]) -> bool:
    """Is the byte stream this row describes actually present on this machine?

    MEASURED 2026-08-22 on EP72. This gate reported `usable=274` on 351 rows. 234 of those 274 are
    the shared library in references/stock_manifest.json, and NOT ONE of its files exists: every
    path is `assets/stock/images/...`, which lived on the H: drive that died on 2026-08-16. The
    gate was counting ROWS, not FILES, so a library that is entirely gone read as the healthiest
    part of the pool -- a false green in exactly the place a false green is most expensive,
    because the next step places these on a timeline.

    Rights-clean, editorially fit and PRESENT are three different properties. This checks the
    third. Paths resolve through config/storage.local.json (rule 14: no OS-absolute path is a
    source of truth), trying the media root first and the repo second, because the two manifest
    generations disagree about which one their relative paths are relative to.
    """
    f = str(a.get("file") or "")
    if not f:
        return False
    if f.startswith("artifact://"):
        f = f[len("artifact://"):]
    elif os.path.isabs(f):
        return os.path.exists(f)
    return any(os.path.exists(os.path.join(base, f))
               for base in (MEDIA_ROOT, ROOT) if base)


def classify(a: dict[str, Any]) -> tuple[str, str]:
    if not on_disk(a):
        return "blocked", (f"file not on disk ('{a.get('file', '')}') - the row survives, the "
                           f"bytes do not; it cannot be placed")
    ed = EDITORIAL.get(a.get("asset_id", ""))
    if ed and ed["verdict"] == "reject":
        return "blocked", f"editorial reject ({ed['reason']}) - {ed.get('note', '')}".strip(" -")
    if ed and ed["verdict"] == "conditional":
        return "review", f"editorial conditional ({ed['reason']}) - {ed.get('note', '')}".strip(" -")
    host = host_of(a["source_url"])
    lic = (a["license"] or "").lower()
    if host and any(d in host for d in DENY_HOSTS):
        return "blocked", f"denylisted source host '{host}'"
    if a.get("commercial_use") == "not_allowed":
        return "blocked", "commercial_use marked not_allowed"
    if any(r in lic for r in REVIEW_LICENSE):
        return "review", f"license needs manual check ('{a['license']}')"
    allowed = any(x in lic for x in ALLOW_LICENSE) or a.get("source") in (
        "pexels", "pixabay", "mixkit", "nasa", "public_domain", "ai_codex", "ai_sdxl")
    if not allowed:
        return "review", f"unrecognized license ('{a['license']}') - verify commercial use"
    if not a.get("sha256"):
        return "review", "no content hash - download/verify and hash before use"
    return "usable", "ok"


def load_items(ep: str, from_path: str | None) -> tuple[list[dict[str, Any]], str]:
    if from_path:
        data = json.load(open(os.path.join(ROOT, from_path), encoding="utf-8"))
        items = data["assets"] if isinstance(data, dict) and "assets" in data else data
        return [normalize(x) for x in items], from_path
    items: list[dict[str, Any]] = []
    srcs: list[str] = []
    led = os.path.join(EPDIR, ep, "05_stock", "stock_ledger.v001.json")
    if os.path.exists(led):
        items += [normalize(x) for x in json.load(open(led, encoding="utf-8"))["assets"]]
        srcs.append("episode ledger")
    lib = os.path.join(ROOT, "references", "stock_manifest.json")  # reusable shared, rights-clean library
    if os.path.exists(lib):
        items += [normalize(x) for x in json.load(open(lib, encoding="utf-8"))]
        srcs.append("shared library")
    if not items:
        raise SystemExit(f"no episode ledger ({led}) and no shared library; run fetch_stock.py first")
    seen: set[str] = set()
    deduped: list[dict[str, Any]] = []
    for a in items:                                  # de-dup so shared + episode assets don't double up
        if a["asset_id"] in seen:
            continue
        seen.add(a["asset_id"])
        deduped.append(a)
    return deduped, " + ".join(srcs)


def write_doc(path: str, ep_id: str, kind: str, assets: list[dict[str, Any]], schema: dict) -> None:
    doc = {"schema_version": "1.0.0", "episode_id": ep_id, "revision": "v001", "kind": kind, "assets": assets}
    errs = [f"{list(e.path)} {e.message}" for e in Draft202012Validator(schema).iter_errors(doc)]
    if errs:
        raise SystemExit("SCHEMA ERROR in " + os.path.basename(path) + ": " + "; ".join(errs[:4]))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(path), suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
    os.replace(tmp, path)


def resolve(arg: str) -> str:
    if os.path.isdir(os.path.join(EPDIR, arg)):
        return arg
    hits = [os.path.basename(p) for p in glob.glob(os.path.join(EPDIR, f"PD-*-{int(arg):03d}-*"))] if arg.isdigit() else []
    if not hits:
        hits = [os.path.basename(p) for p in glob.glob(os.path.join(EPDIR, f"*{arg}*")) if os.path.isdir(p)]
    if len(hits) == 1:
        return hits[0]
    raise SystemExit(f"Could not resolve episode '{arg}'. Matches: {hits}")


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    argv = sys.argv[1:]
    write = "--write" in argv
    from_path = None
    if "--from" in argv:
        from_path = argv[argv.index("--from") + 1]
    pos = [a for a in argv if not a.startswith("--") and a != from_path]
    if not pos:
        raise SystemExit("usage: build_usable_assets.py <episode> [--from <manifest>] [--write]")
    ep = resolve(pos[0])
    ep_id = os.path.basename(ep)
    items, src = load_items(ep, from_path)
    schema = json.load(open(os.path.join(ROOT, "schemas", "stock-ledger.schema.json"), encoding="utf-8"))

    global EDITORIAL
    EDITORIAL = load_editorial(ep)
    if EDITORIAL:
        print(f"Editorial verdicts: {len(EDITORIAL)} clip(s) carry a human verdict")
    else:
        print("Editorial verdicts: NONE. This gate is checking rights only -- it cannot tell you "
              "whether the footage belongs in the film. Watch the clips before the timeline.")

    usable, review, blocked = [], [], []
    for a in items:
        gate, reason = classify(a)
        a["gate"], a["gate_reason"] = gate, reason
        (usable if gate == "usable" else review if gate == "review" else blocked).append(a)

    print(f"Episode: {ep_id}   source: {src}")
    print(f"Assets: {len(items)}  ->  usable={len(usable)}  review={len(review)}  blocked={len(blocked)}")
    for a in blocked:
        print(f"  BLOCKED  {a['asset_id']}: {a['gate_reason']}")
    for a in review[:12]:
        print(f"  REVIEW   {a['asset_id']}: {a['gate_reason']}")

    if write:
        out_dir = os.path.join(EPDIR, ep, "05_stock")
        write_doc(os.path.join(out_dir, "usable_assets.v001.json"), ep_id, "usable", usable, schema)
        write_doc(os.path.join(out_dir, "review_queue.v001.json"), ep_id, "review", review + blocked, schema)
        print(f"\nWROTE 05_stock/usable_assets.v001.json ({len(usable)}) + review_queue.v001.json ({len(review)+len(blocked)})")
    else:
        print("\n(dry-run) pass --write to persist usable_assets.v001.json + review_queue.v001.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
