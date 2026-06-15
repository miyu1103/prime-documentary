#!/usr/bin/env python3
"""Route owner-downloaded assets from the SSD inbox into the episode's asset folders.

Workflow: the owner downloads everything (Midjourney stills, Runway clips, etc.) into the
SSD inbox. Claude views the files, picks the best variant per scene, and routes them here
to stable, scene-mapped filenames. No deletion — originals stay in the inbox (or are copied
to an `_archive/` subfolder with --archive) so nothing the owner downloaded is destroyed.

Default inbox  : <media-root>/downloads/inbox   (media-root from config/storage.local.json)
Default dest   : remotion/public/mj             (Remotion reads stills from here; gitignored)

Usage (from repo root, py 3.11):
    py -3.11 scripts/route_inbox.py --list
    py -3.11 scripts/route_inbox.py --route "A_lone_shaft=s005_empty_chair" --route "hand-print=s009_hand_writing" --apply
    py -3.11 scripts/route_inbox.py --route "thumb-pencil=thumb_gideon_pencil" --dest remotion/public --apply

Each --route is "<substr>=<stem>". <substr> is matched (case-insensitive) against inbox
filenames; it must match exactly one file (disambiguate with a longer substring, e.g. the
MJ variant index like "..._2"). The file is COPIED to <dest>/<stem>.png (extension kept
from the source). Dry-run by default; pass --apply to write.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
IMG_EXT = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".mp4", ".mov", ".wav", ".mp3"}


def media_root() -> Path:
    cfg = REPO_ROOT / "config" / "storage.local.json"
    if cfg.exists():
        data = json.loads(cfg.read_text(encoding="utf-8"))
        p = data.get("roots", {}).get("media", {}).get("path")
        if p:
            return Path(p)
    raise SystemExit("media root not found in config/storage.local.json")


def list_inbox(inbox: Path) -> list[Path]:
    if not inbox.exists():
        raise SystemExit(f"inbox not found: {inbox}")
    return sorted(
        (p for p in inbox.iterdir() if p.is_file() and p.suffix.lower() in IMG_EXT),
        key=lambda p: p.name.lower(),
    )


def match_one(files: list[Path], substr: str) -> Path:
    s = substr.lower()
    hits = [p for p in files if s in p.name.lower()]
    if not hits:
        raise SystemExit(f"no inbox file matches substring {substr!r}")
    if len(hits) > 1:
        names = "\n  ".join(p.name for p in hits)
        raise SystemExit(f"substring {substr!r} matches {len(hits)} files (make it more specific):\n  {names}")
    return hits[0]


def main(argv: list[str]) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    except Exception:
        pass

    ap = argparse.ArgumentParser(description="Route SSD inbox assets into episode folders")
    ap.add_argument("--inbox", default=None, help="override inbox path")
    ap.add_argument("--dest", default="remotion/public/mj", help="dest dir (repo-relative)")
    ap.add_argument("--route", action="append", default=[], metavar="SUBSTR=STEM",
                    help="route an inbox file (matched by SUBSTR) to <dest>/<STEM><ext>")
    ap.add_argument("--list", action="store_true", help="list inbox image/video files and exit")
    ap.add_argument("--apply", action="store_true", help="actually copy (default: dry-run)")
    args = ap.parse_args(argv)

    inbox = Path(args.inbox) if args.inbox else (media_root() / "downloads" / "inbox")
    files = list_inbox(inbox)

    if args.list or not args.route:
        print(f"inbox: {inbox}  ({len(files)} files)")
        for i, p in enumerate(files):
            mb = p.stat().st_size / (1024 * 1024)
            print(f"  [{i:2d}] {p.name}  ({mb:.1f} MB)")
        if not args.route:
            return 0

    dest_dir = (REPO_ROOT / args.dest).resolve()
    dest_dir.mkdir(parents=True, exist_ok=True)

    plan: list[tuple[Path, Path]] = []
    for spec in args.route:
        if "=" not in spec:
            raise SystemExit(f"bad --route {spec!r} (expected SUBSTR=STEM)")
        substr, stem = spec.split("=", 1)
        src = match_one(files, substr.strip())
        dst = dest_dir / f"{stem.strip()}{src.suffix.lower()}"
        plan.append((src, dst))

    print(f"\nrouting plan ({'APPLY' if args.apply else 'dry-run'}):  dest = {dest_dir}")
    for src, dst in plan:
        print(f"  {src.name}\n    -> {dst.name}")
        if args.apply:
            shutil.copy2(src, dst)
    if args.apply:
        print(f"\n[done] copied {len(plan)} file(s). Originals left in the inbox.")
    else:
        print("\n[dry-run] nothing written. Re-run with --apply.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
