#!/usr/bin/env python
"""U4 - Import usable assets into Remotion and generate the rough-cut data file.

Reads the episode shotlist (04_scenes/shotlist.v001.json) and, if present, the rights-gated
usable list (05_stock/usable_assets.v001.json). Assigns one usable asset per shot that needs
real footage (stock_video / stock_image / ai_image / archival_pd), copies ONLY usable files
into remotion/public/<slug>/, and emits a typed remotion/src/data/<slug>_roughcut.ts consumed
by the RoughCut composition. Shots with no usable asset get src=null -> RoughCut renders a
branded motion card (telop) so the timeline is complete. motion_graphic shots are always coded.

NEVER copies a review/blocked asset. Default dry-run; --write performs copies + writes the .ts.

Usage:
  .venv/Scripts/python.exe scripts/import_to_remotion.py 11
  .venv/Scripts/python.exe scripts/import_to_remotion.py 11 --write
"""
from __future__ import annotations
import sys, os, json, glob, shutil, tempfile, re
from typing import Any

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EPDIR = os.path.join(ROOT, "episodes")
PUBLIC = os.path.join(ROOT, "remotion", "public")
DATA = os.path.join(ROOT, "remotion", "src", "data")


def media_root() -> str | None:
    cfg = os.path.join(ROOT, "config", "storage.local.json")
    if not os.path.exists(cfg):
        return None
    return json.load(open(cfg, encoding="utf-8"))["roots"]["media"]["path"]


def resolve_file(file: str) -> str | None:
    mr = media_root()
    if file.startswith("artifact://"):
        return os.path.join(mr, file[len("artifact://"):]) if mr else None
    if file.startswith(("remotion/", "references/", "schemas/", "episodes/")):
        return os.path.join(ROOT, file)
    if os.path.isabs(file):
        return file
    if file.startswith("assets/"):                      # legacy stock_manifest -> media SSD
        return os.path.join(mr, file) if mr else None
    for cand in ([os.path.join(ROOT, file)] + ([os.path.join(mr, file)] if mr else [])):
        if os.path.exists(cand):
            return cand
    return os.path.join(ROOT, file)


def resolve_ep(arg: str) -> str:
    if os.path.isdir(os.path.join(EPDIR, arg)):
        return arg
    hits = [os.path.basename(p) for p in glob.glob(os.path.join(EPDIR, f"PD-*-{int(arg):03d}-*"))] if arg.isdigit() else []
    if not hits:
        hits = [os.path.basename(p) for p in glob.glob(os.path.join(EPDIR, f"*{arg}*")) if os.path.isdir(p)]
    if len(hits) == 1:
        return hits[0]
    raise SystemExit(f"Could not resolve episode '{arg}'. Matches: {hits}")


def slug_of(ep_id: str) -> str:
    parts = ep_id.split("-", 3)
    return parts[3] if len(parts) > 3 else ep_id


def tokens(*strs: Any) -> set[str]:
    text = " ".join(str(s or "") for s in strs).lower()
    return {w for w in re.findall(r"[a-z]{3,}", text)}


def pick_asset(shot: dict[str, Any], pool: list[dict[str, Any]], used: set[str]) -> dict[str, Any] | None:
    """Best unused usable asset of a compatible media type, by keyword overlap."""
    want_video = shot["suggested_asset_type"] == "stock_video"
    kw = tokens(*shot.get("search_keywords", []), *shot.get("on_screen_text", []), shot.get("visual_intent", ""))
    best, best_score = None, -1
    for a in pool:
        if a["asset_id"] in used:
            continue
        is_video = a.get("asset_type") == "video"
        if want_video and not is_video:
            continue
        if not want_video and is_video:
            continue                                    # image shot -> image asset
        score = len(kw & tokens(a.get("depicts"), a.get("query"), a.get("asset_id")))
        if shot["span_id"] in (a.get("used_in_spans") or []):
            score += 100                                # explicit assignment wins
        if score > best_score:
            best, best_score = a, score
    return best if best_score >= 1 else None


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    argv = sys.argv[1:]
    write = "--write" in argv
    pos = [a for a in argv if not a.startswith("--")]
    if not pos:
        raise SystemExit("usage: import_to_remotion.py <episode> [--write]")
    ep = resolve_ep(pos[0])
    b = os.path.join(EPDIR, ep)
    ep_id = os.path.basename(ep)
    slug = slug_of(ep_id)

    shotlist = json.load(open(os.path.join(b, "04_scenes", "shotlist.v001.json"), encoding="utf-8"))
    usable_path = os.path.join(b, "05_stock", "usable_assets.v001.json")
    pool = json.load(open(usable_path, encoding="utf-8"))["assets"] if os.path.exists(usable_path) else []
    try:
        title = json.load(open(os.path.join(b, "manifest.json"), encoding="utf-8")).get("title_working", ep_id)
    except Exception:
        title = ep_id

    dest_dir = os.path.join(PUBLIC, slug)
    used: set[str] = set()
    copies: list[tuple[str, str]] = []
    shots_out: list[dict[str, Any]] = []
    bound = 0
    for sh in shotlist["shots"]:
        src = None
        if sh["suggested_asset_type"] != "motion_graphic":
            a = pick_asset(sh, pool, used)
            if a:
                used.add(a["asset_id"])
                fname = os.path.basename(a["file"])
                src = f"{slug}/{fname}"
                copies.append((a["file"], os.path.join(dest_dir, fname)))
                bound += 1
        shots_out.append({
            "spanId": sh["span_id"],
            "chapterId": sh.get("chapter_id"),
            "seconds": sh["estimated_seconds"],
            "assetType": sh["suggested_asset_type"],
            "motion": sh["motion"],
            "src": src,
            "telop": sh.get("on_screen_text", []),
            "priority": sh["priority"],
        })

    data = {"episodeId": ep_id, "title": title, "fps": 30,
            "narrationSrc": None, "bgmSrc": None, "shots": shots_out}
    const = slug.upper().replace("-", "_") + "_ROUGHCUT"
    ts_path = os.path.join(DATA, f"{slug}_roughcut.ts")
    header = (f"// AUTO-GENERATED by scripts/import_to_remotion.py from {ep_id}/04_scenes/shotlist.v001.json\n"
              f"// + 05_stock/usable_assets.v001.json. Do NOT edit by hand; re-run the importer.\n"
              f"import type {{RoughCutData}} from '../compositions/RoughCut';\n\n"
              f"export const {const}: RoughCutData = ")
    ts = header + json.dumps(data, ensure_ascii=False, indent=2) + ";\n"

    print(f"Episode: {ep_id}  slug: {slug}")
    print(f"Shots: {len(shots_out)}   usable pool: {len(pool)}   bound to real assets: {bound}   coded/cards: {len(shots_out)-bound}")
    print(f"Data file: remotion/src/data/{slug}_roughcut.ts   export: {const}")
    if write:
        os.makedirs(dest_dir, exist_ok=True)
        copied = 0
        for srcf, dstf in copies:
            rp = resolve_file(srcf)
            if rp and os.path.exists(rp):
                shutil.copy2(rp, dstf)
                copied += 1
            else:
                print(f"  WARN missing usable file, leaving card: {srcf}")
        os.makedirs(DATA, exist_ok=True)
        fd, tmp = tempfile.mkstemp(dir=DATA, suffix=".tmp")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(ts)
        os.replace(tmp, ts_path)
        print(f"\nWROTE {os.path.relpath(ts_path, ROOT)}  (+{copied} assets -> remotion/public/{slug}/)")
        print(f"Register in Root.tsx: import {{RoughCut, roughCutDurationInFrames}} + {{{const}}} and add a <Composition id=\"RoughCut_{slug}\" ...>.")
    else:
        print(f"\n(dry-run) would write the .ts and copy {len(copies)} usable asset(s). Pass --write.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
