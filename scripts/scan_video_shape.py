#!/usr/bin/env python3
r"""Read-only: find archive clips that are not usable in a 1920x1080 film.

Two defects, neither visible in a filename, a path, or the ledger (which stores no
dimensions at all):

  PORTRAIT   the container itself is taller than wide.
  PILLARBOX  the container is 16:9 but the picture inside is a portrait clip with black
             bars painted down both sides. Found by eye in EP60's coastline pool
             (`pixabay_extra__v_281640`), where nothing else gave it away. Scaling one of
             these to full frame yields a 33%-wide image in a black surround.

Stage 1 (ffprobe, ~0.1s/clip) reads dimensions for everything.
Stage 2 (ffmpeg cropdetect, ~0.5s/clip) runs only on landscape clips and reports the
bounding box of the actual picture.

Resumable: results append to JSONL and already-scanned paths are skipped, so a killed run
costs only the clip it was on.

    py -3.11 scripts/scan_video_shape.py --dry-run
    py -3.11 scripts/scan_video_shape.py --root "H:/pd-media/assets" --workers 12
    py -3.11 scripts/scan_video_shape.py --stage crop --min-bar-frac 0.08
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


def _pd_media_root() -> Path:
    """The media root, resolved -- never assumed.

    FIXED 2026-08-22. This file hardcoded H:/pd-media. That drive stopped being enumerated by
    Windows around the 2026-08-16 reboot and config/storage.local.json was repointed to E:\pd-media
    on 2026-08-17. Rule 14: no OS-absolute path is a source of truth. The literal below is kept only
    as a last-resort fallback so an unconfigured checkout behaves as it used to instead of crashing.
    """
    import json as _json
    _cfg = Path(__file__).resolve().parents[1] / "config" / "storage.local.json"
    try:
        return Path(_json.loads(_cfg.read_text(encoding="utf-8"))["roots"]["media"]["path"])
    except Exception:
        return Path("H:/pd-media")


PD_MEDIA = _pd_media_root()


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "episodes" / "_planning" / "measurements" / "VIDEO_SHAPE_SCAN.jsonl"
VIDEO_EXT = {".mp4", ".mov", ".m4v", ".webm", ".mkv"}
CROP_RE = re.compile(r"crop=(\d+):(\d+):(\d+):(\d+)")


def probe(path: Path, timeout: int) -> dict:
    """Container dimensions. Returns width/height 0 when ffprobe cannot read the file."""
    try:
        r = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream=width,height,duration",
             "-of", "json", str(path)],
            capture_output=True, text=True, timeout=timeout)
        s = (json.loads(r.stdout or "{}").get("streams") or [{}])[0]
        return {"width": int(s.get("width") or 0), "height": int(s.get("height") or 0),
                "duration": float(s.get("duration") or 0.0)}
    except Exception as e:
        return {"width": 0, "height": 0, "duration": 0.0, "error": str(e)[:80]}


def cropbox(path: Path, timeout: int) -> tuple[int, int, int, int] | None:
    """Bounding box of the non-black picture, from 40 frames one second in."""
    try:
        r = subprocess.run(
            ["ffmpeg", "-hide_banner", "-nostats", "-ss", "1", "-i", str(path),
             "-vf", "cropdetect=limit=24:round=2:reset=0", "-frames:v", "40",
             "-f", "null", "-"],
            capture_output=True, text=True, timeout=timeout)
        m = CROP_RE.findall(r.stderr or "")
        if not m:
            return None
        w, h, x, y = (int(v) for v in m[-1])
        return w, h, x, y
    except Exception:
        return None


def verdict(rec: dict, min_bar: float) -> str:
    w, h = rec.get("width", 0), rec.get("height", 0)
    if not w or not h:
        return "unreadable"
    if h > w:
        return "portrait"
    cb = rec.get("crop")
    if cb:
        cw, ch = cb[0], cb[1]
        # "Narrow crop + full height" alone flags dark cinematic footage, which is most of
        # this shelf: measured crop aspects of 1.25-1.74 on unlit rooms and night streets,
        # where cropdetect simply trimmed dark edges. A genuinely pillarboxed portrait clip
        # has a PORTRAIT picture inside the landscape frame, so require that too.
        if cw and ch and (w - cw) / w >= min_bar and ch >= h * 0.9 and cw / ch < 1.0:
            return "pillarbox"
    if w < 1920 or h < 1080:
        return "under_hd"
    return "ok"


def main(argv: list[str]) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=str(PD_MEDIA / "assets"))
    ap.add_argument("--stage", choices=["probe", "crop", "both"], default="probe")
    ap.add_argument("--workers", type=int, default=12)
    ap.add_argument("--limit", type=int, default=0, help="0 = every clip")
    ap.add_argument("--timeout", type=int, default=30)
    ap.add_argument("--min-bar-frac", type=float, default=0.08,
                    help="side bars this fraction of width or more count as pillarbox")
    ap.add_argument("--output", default=str(OUT))
    ap.add_argument("--restart", action="store_true", help="ignore previous results")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)

    root = Path(a.root)
    if not root.is_dir():
        print(f"root not found: {root}", file=sys.stderr)
        return 2
    files = [p for p in root.rglob("*") if p.suffix.lower() in VIDEO_EXT]
    files.sort()
    if a.limit:
        files = files[:a.limit]

    out = Path(a.output)
    done: dict[str, dict] = {}
    if out.exists() and not a.restart:
        for line in out.read_text(encoding="utf-8").splitlines():
            try:
                r = json.loads(line)
                done[r["path"]] = r
            except Exception:
                continue
    todo = [p for p in files if str(p) not in done
            or (a.stage in ("crop", "both") and "crop" not in done[str(p)]
                and done[str(p)].get("width", 0) >= done[str(p)].get("height", 1))]

    print(f"{len(files)} clips under {root}\n"
          f"{len(done)} already scanned · {len(todo)} to do · stage={a.stage}")
    if a.dry_run:
        print("(dry run — nothing probed, nothing written)")
        return 0
    if not todo:
        print("nothing to do")
    else:
        out.parent.mkdir(parents=True, exist_ok=True)
        fh = out.open("a", encoding="utf-8")

        def work(p: Path) -> dict:
            rec = done.get(str(p)) or {"path": str(p), "name": p.name}
            if "width" not in rec:
                rec.update(probe(p, a.timeout))
            if a.stage in ("crop", "both") and rec.get("width", 0) >= rec.get("height", 1) > 0:
                cb = cropbox(p, a.timeout * 2)
                if cb:
                    rec["crop"] = list(cb)
            return rec

        n = 0
        with ThreadPoolExecutor(max_workers=a.workers) as ex:
            for rec in ex.map(work, todo):
                fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
                n += 1
                if n % 500 == 0:
                    fh.flush()
                    print(f"  {n}/{len(todo)}", flush=True)
        fh.close()
        for r in (json.loads(l) for l in out.read_text(encoding="utf-8").splitlines() if l):
            done[r["path"]] = r

    counts: dict[str, int] = {}
    flagged: dict[str, list[str]] = {}
    for r in done.values():
        v = verdict(r, a.min_bar_frac)
        counts[v] = counts.get(v, 0) + 1
        if v in ("portrait", "pillarbox", "unreadable"):
            flagged.setdefault(v, []).append(r["name"])
    print("\n--- verdicts ---")
    for k in sorted(counts, key=lambda k: -counts[k]):
        print(f"  {k:<12} {counts[k]}")
    for v, names in flagged.items():
        print(f"\n{v} ({len(names)}):")
        for nm in sorted(names)[:25]:
            print(f"    {nm}")
        if len(names) > 25:
            print(f"    ... and {len(names) - 25} more")
    try:
        shown = out.relative_to(ROOT)
    except ValueError:
        shown = out
    print(f"\nwrote {shown}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
