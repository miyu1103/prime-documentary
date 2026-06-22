#!/usr/bin/env python
"""Revert the factory theme-subfolder reorg: move files from
factory/<category>/<theme>/<file> back to factory/<category>/<file>.

Disk-only (does NOT touch the manifest), because a concurrent factory builder
owns/rewrites asset_manifest.v001.json with FLAT paths. Reverting the files to
flat restores manifest<->disk consistency while the builder keeps running.

Usage:
  .venv/Scripts/python.exe scripts/revert_factory_reorg.py          # dry-run
  .venv/Scripts/python.exe scripts/revert_factory_reorg.py --apply
"""
from __future__ import annotations
import os, sys, shutil, argparse, collections

sys.stdout.reconfigure(encoding="utf-8")
MEDIA = os.environ.get("PD_MEDIA_ROOT", r"H:\pd-media")
FACTORY = os.path.join(MEDIA, "assets", "factory")
CATS = ["backgrounds", "light_assets", "vfx_overlays", "particle_assets", "texture_assets", "loops"]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    moves = []          # (src, dst)
    per = collections.Counter()
    for cat in CATS:
        cdir = os.path.join(FACTORY, cat)
        if not os.path.isdir(cdir):
            continue
        for theme in os.listdir(cdir):
            tdir = os.path.join(cdir, theme)
            if not os.path.isdir(tdir):
                continue                                  # skip loose files already flat
            for fn in os.listdir(tdir):
                src = os.path.join(tdir, fn)
                if os.path.isfile(src):
                    moves.append((src, os.path.join(cdir, fn)))
                    per[f"{cat}/{theme}"] += 1
    print(f"theme-subfolder files to move back to flat: {len(moves)}")
    for k, v in sorted(per.items()):
        print(f"  {v:6}  {k}")
    if not a.apply:
        print("\n(DRY-RUN) nothing moved. Pass --apply.")
        return
    moved = skipped = 0
    for src, dst in moves:
        if os.path.exists(dst):
            skipped += 1                                  # already a flat file with that name
            continue
        shutil.move(src, dst)
        moved += 1
    # remove now-empty theme dirs
    for cat in CATS:
        cdir = os.path.join(FACTORY, cat)
        if not os.path.isdir(cdir):
            continue
        for theme in os.listdir(cdir):
            tdir = os.path.join(cdir, theme)
            if os.path.isdir(tdir) and not os.listdir(tdir):
                os.rmdir(tdir)
    print(f"\nREVERTED: moved {moved} back to flat, skipped {skipped} (name already flat).")


if __name__ == "__main__":
    main()
