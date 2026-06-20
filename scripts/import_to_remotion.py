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
import sys, os, json, glob, shutil, tempfile, re, subprocess, math
from typing import Any


def conform_video(srcp: str, dstp: str, fps: int = 30) -> bool:
    """Re-encode a clip to the timeline fps (no crop), so mixed-fps clips don't judder in the
    fixed-fps composition. Near-transparent quality (crf 16). Returns True on success."""
    try:
        subprocess.run(
            ["ffmpeg", "-y", "-i", srcp, "-vf", f"fps={fps}", "-c:v", "libx264",
             "-crf", "16", "-preset", "medium", "-an", dstp],
            capture_output=True, timeout=600)
        return os.path.exists(dstp) and os.path.getsize(dstp) > 0
    except Exception:
        return False


def probe_seconds(path: str | None) -> float | None:
    """Clip length via ffprobe, so RoughCut can play a short clip once (slowed) instead of looping."""
    if not path or not os.path.exists(path):
        return None
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
            capture_output=True, text=True, timeout=30)
        return round(float(out.stdout.strip()), 2)
    except Exception:
        return None

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


def ai_images_for(slug: str, span_id: str) -> list[str]:
    """Hand-made AI images for a span, dropped by the Codex app at
    <media>/assets/ai/<slug>/<span_id>*.{png,jpg,...}. These take priority over stock."""
    mr = media_root()
    if not mr:
        return []
    d = os.path.join(mr, "assets", "ai", slug)
    if not os.path.isdir(d):
        return []
    out: list[str] = []
    for ext in ("png", "jpg", "jpeg", "webp"):
        out += glob.glob(os.path.join(d, f"{span_id}*.{ext}"))
    return sorted(out)


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


def pick_videos(shot: dict[str, Any], pool: list[dict[str, Any]], used: set[str], max_n: int = 5) -> list[dict[str, Any]]:
    """Several usable VIDEO clips for one shot, best keyword match first, so a long narration
    span is covered by cutting between clips at normal speed (not one clip looped/slowed)."""
    kw = tokens(*shot.get("search_keywords", []), *shot.get("on_screen_text", []), shot.get("visual_intent", ""))
    scored = []
    for a in pool:
        if a["asset_id"] in used or a.get("asset_type") != "video":
            continue
        score = len(kw & tokens(a.get("depicts"), a.get("query"), a.get("asset_id")))
        if shot["span_id"] in (a.get("used_in_spans") or []):
            score += 100
        if score >= 1:
            scored.append((score, a))
    scored.sort(key=lambda x: -x[0])
    return [a for _, a in scored[:max_n]]


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
    img_pool = [a for a in pool if a.get("asset_type") == "image"]  # for filling empty picture slots
    img_i = 0
    vid_pool = [a for a in pool if a.get("asset_type") == "video"]   # for guaranteeing real footage
    vid_i = 0

    def queue_copy(asset: dict[str, Any]) -> str:
        fname = os.path.basename(asset["file"])
        pair = (asset["file"], os.path.join(dest_dir, fname))
        if pair not in copies:
            copies.append(pair)
        return f"{slug}/{fname}"
    for sh in shotlist["shots"]:
        src = None
        clips_out: list[dict[str, Any]] = []
        images_out: list[str] = []
        atype = sh["suggested_asset_type"]
        ai_paths = ai_images_for(slug, sh["span_id"])  # hand-made AI images win over stock/placeholders
        if ai_paths:
            images_out = [queue_copy({"file": p}) for p in ai_paths]
            src = images_out[0]
            bound += 1
        elif atype == "stock_video":
            vids = pick_videos(sh, pool, used)        # keyword-matched clips first
            for a in vids:
                used.add(a["asset_id"])
            while len(vids) < 2 and vid_pool:          # guarantee real motion (cut between >=2 clips)
                vids.append(vid_pool[vid_i % len(vid_pool)])
                vid_i += 1
            for a in vids:
                clips_out.append({"src": queue_copy(a),
                                  "clipSeconds": probe_seconds(resolve_file(a["file"])) or 6.0})
            if clips_out:
                src = clips_out[0]["src"]
                bound += 1
        else:
            # Every non-video shot gets ENOUGH photos to cut every ~6s, so nothing dwells/looks static.
            n = max(1, math.ceil(sh["estimated_seconds"] / 6.0))
            chosen: list[dict[str, Any]] = []
            while len(chosen) < n:                       # keyword-matched photos first
                a = pick_asset(sh, pool, used)
                if not a:
                    break
                used.add(a["asset_id"])
                chosen.append(a)
            while len(chosen) < n and img_pool:          # fill the rest from the pool (may reuse)
                chosen.append(img_pool[img_i % len(img_pool)])
                img_i += 1
            images_out = [queue_copy(a) for a in chosen]
            if images_out:
                src = images_out[0]
                bound += 1
        shot_out: dict[str, Any] = {
            "spanId": sh["span_id"],
            "chapterId": sh.get("chapter_id"),
            "seconds": sh["estimated_seconds"],
            "assetType": sh["suggested_asset_type"],
            "motion": sh["motion"],
            "src": src,
            "telop": sh.get("on_screen_text", []),
            "priority": sh["priority"],
        }
        if clips_out:
            shot_out["clips"] = clips_out
        if images_out:
            shot_out["images"] = images_out
        shots_out.append(shot_out)

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
                is_video = dstf.lower().endswith((".mp4", ".mov", ".webm", ".m4v"))
                if is_video and conform_video(rp, dstf):
                    copied += 1
                else:
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
        print(f"Register in Root.tsx: import {{RoughCut, roughCutDurationInFrames}} + {{{const}}} and add a <Composition id=\"RoughCut-{slug}\" ...> (hyphen only; '_' is invalid in Remotion ids).")
    else:
        print(f"\n(dry-run) would write the .ts and copy {len(copies)} usable asset(s). Pass --write.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
