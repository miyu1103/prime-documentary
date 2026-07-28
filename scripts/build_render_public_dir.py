#!/usr/bin/env python
"""Build the per-episode slim public dir that a Remotion render is allowed to use.

Remotion COPIES the whole --public-dir into its bundle before rendering. Three separate
EP54 render attempts died on that fact (failures F-18a/b/c), so this script exists to make
the correct directory the easy one to produce:

  F-18a  Pointing at the shared remotion/public means copying 56 GB -- every other
         episode's assets plus EP54's 37 GB `rejected/` folder. Here only ONE episode's
         pools are linked in, so the copy is ~8 GB.
  F-18b  Building the slim dir from junctions/symlinks looks correct to every Python check
         (they follow links) but Remotion's copy does NOT follow them: the bundle ends up
         empty and every asset 404s mid-render. HARDLINKS are used instead -- they cost no
         disk, and a copy cannot tell them from ordinary files.
  F-18c  banner_sunrise.png and the three fonts are requested by literal name inside the
         compositions, so they never appear in film.json's src list and are easy to forget.
         They are copied in explicitly and verified.

Usage:
  py -3.11 scripts/build_render_public_dir.py --slug flowers [--out remotion/public_ep54]
  py -3.11 scripts/build_render_public_dir.py --slug flowers --verify-only

Then render ONLY through the guarded path:
  scripts/pd_render_guarded.sh <CompId> remotion/src/data/<slug>_film.json <out> out/<slug>.mp4 <sec>
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "remotion" / "public"
SLIM = ROOT / "remotion" / "public_slim"
POOL_DIRS = ("img", "motion", "factory", "overlay")
# referenced by literal name inside the compositions -> absent from film.json's src list
STATIC_ASSETS = ("banner_sunrise.png",)
FONT_FILES = ("Anton.ttf", "Archivo.ttf", "Oswald.ttf", "LICENSE_FONTS.md")

EPISODES = {p.name.split("-", 3)[-1]: p.name for p in sorted((ROOT / "episodes").glob("PD-*"))}


def link_or_copy(src: Path, dst: Path) -> str:
    if dst.exists():
        return "kept"
    try:
        os.link(src, dst)          # same volume: no extra bytes, indistinguishable from a file
        return "linked"
    except OSError:
        shutil.copy2(src, dst)     # cross-volume fallback
        return "copied"


def is_reparse(p: Path) -> bool:
    try:
        return os.path.islink(p) or bool(
            getattr(os.stat(p, follow_symlinks=False), "st_file_attributes", 0) & 0x400)
    except OSError:
        return False


def verify(out: Path, slug: str) -> list[str]:
    problems: list[str] = []
    for root_, dirs_, _ in os.walk(out):
        for d in dirs_:
            if is_reparse(Path(root_) / d):
                problems.append(f"junction/symlink dir (Remotion will not copy it): {Path(root_)/d}")
    for name in STATIC_ASSETS:
        if not (out / name).is_file():
            problems.append(f"missing static asset {name}")
    for name in FONT_FILES:
        if not (out / "fonts" / name).is_file():
            problems.append(f"missing font fonts/{name}")
    if not (out / slug / "narration.mp3").is_file():
        problems.append(f"missing {slug}/narration.mp3")
    film = ROOT / "remotion" / "src" / "data" / f"{slug}_film.json"
    if film.exists():
        srcs = {c["src"] for c in json.loads(film.read_text(encoding="utf-8"))["cuts"]}
        absent = [s for s in sorted(srcs) if not (out / s).is_file()]
        if absent:
            problems.append(f"{len(absent)} film.json srcs absent e.g. {absent[:3]}")
    return problems


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--verify-only", action="store_true")
    a = ap.parse_args()

    ep = EPISODES.get(a.slug)
    if not ep:
        raise SystemExit(f"unknown slug {a.slug}")
    # PD-2026-054-flowers -> "54": the dir is public_ep54, NOT public_ep054. Getting this
    # wrong makes the verifier inspect an empty directory and report a healthy dir as broken.
    num = ep.split("-")[2].lstrip("0")
    out = a.out or (ROOT / "remotion" / f"public_ep{num}")
    src_base = PUBLIC / a.slug

    if not a.verify_only:
        if not src_base.is_dir():
            raise SystemExit(f"nothing staged at {src_base}")
        # A pre-existing dir may hold junctions from an earlier attempt; clear those first.
        if out.exists():
            for root_, dirs_, _ in os.walk(out):
                for d in list(dirs_):
                    p = Path(root_) / d
                    if is_reparse(p):
                        os.rmdir(p)
        (out / a.slug).mkdir(parents=True, exist_ok=True)
        stats = {"linked": 0, "copied": 0, "kept": 0}
        for d in POOL_DIRS:
            s = src_base / d
            if not s.is_dir():
                continue
            (out / a.slug / d).mkdir(parents=True, exist_ok=True)
            for f in sorted(s.iterdir()):
                if f.is_file():
                    stats[link_or_copy(f, out / a.slug / d / f.name)] += 1
        for extra in ("narration.mp3",):
            if (src_base / extra).is_file():
                stats[link_or_copy(src_base / extra, out / a.slug / extra)] += 1
        for name in STATIC_ASSETS:
            cand = PUBLIC / name
            if cand.is_file():
                stats[link_or_copy(cand, out / name)] += 1
        (out / "fonts").mkdir(parents=True, exist_ok=True)
        font_src = SLIM / "fonts" if (SLIM / "fonts").is_dir() else PUBLIC / "fonts"
        for name in FONT_FILES:
            if (font_src / name).is_file():
                stats[link_or_copy(font_src / name, out / "fonts" / name)] += 1
        print(f"[{a.slug}] {out.name}: {stats}")

    problems = verify(out, a.slug)
    total = sum(1 for _ in out.rglob("*") if _.is_file()) if out.exists() else 0
    size = sum(f.stat().st_size for f in out.rglob("*") if f.is_file()) if out.exists() else 0
    print(f"[{a.slug}] {out} files={total} logical_size={size/1e9:.1f} GB")
    for p in problems:
        print(f"  [PROBLEM] {p}")
    if problems:
        print("RESULT: NOT render-ready")
        return 1
    print(f"RESULT: render-ready -> use --public-dir {out.name}")
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    raise SystemExit(main())
