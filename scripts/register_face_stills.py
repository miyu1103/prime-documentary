#!/usr/bin/env python
"""Register the stills that actually contain a face as the episode's PEOPLE pool.

The pre-render gate blocks a film with "NO people/face stills -- the film would have no human
faces", and the builder recognises people by the P-prefix filename convention. EP57-59 arrived
named S###/M##_src, so every face they DID have was invisible to both. Rather than renaming
generated art by hand, faces are detected (the same haarcascade the channel's own thumbnail
study used) and the qualifying stills are copied to P###.png beside the originals.

    python scripts/register_face_stills.py --slug fieldtest [--min-share 0.04] [--dry-run]

Copies, never moves: the original S### file stays where the film already references it.
"""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def face_share(path: Path) -> float:
    """Largest detected face area as a share of the image area (0 when no face)."""
    # A MISSING LIBRARY IS NOT "NO FACE".
    # `.venv` has no cv2, so this returned 0.0 for every image and the tool reported
    # "0 still(s) carry a face" as though it had looked. Run under an interpreter that has
    # cv2 (py -3.11 does) or fix the environment -- do not let a silent zero stand in for a
    # measurement. This is the same failure shape as the QC that stamped without looking.
    try:
        import cv2
    except ImportError as exc:  # noqa: BLE001
        raise SystemExit(
            f"cv2 is not available to this interpreter ({exc}); face detection cannot run. "
            f"Re-run with `py -3.11 scripts/register_face_stills.py ...`, which has cv2 4.10.")
    try:
        img = cv2.imread(str(path))
        if img is None:
            return 0.0
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        faces = cascade.detectMultiScale(gray, scaleFactor=1.08, minNeighbors=6,
                                         minSize=(int(img.shape[0] * 0.05),) * 2)
        if len(faces) == 0:
            return 0.0
        x, y, w, h = max(faces, key=lambda f: f[2] * f[3])
        return (w * h) / float(img.shape[0] * img.shape[1])
    except Exception:
        return 0.0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--min-share", type=float, default=0.02,
                    help="a face must cover at least this share of the frame")
    ap.add_argument("--max", type=int, default=40)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    img = ROOT / "remotion" / "public" / a.slug / "img"
    if not img.is_dir():
        print(f"[faces] no img dir for {a.slug}")
        return 0
    # Newly delivered plates have to be able to JOIN an existing pool. This used to return
    # the moment any P*.png existed, so a Codex batch dropped in later was silently ignored --
    # EP57 was about to receive 12 new people plates into a pool of 2 and none of them would
    # have been picked up. Existing P### files are kept; new numbering continues past them.
    existing = sorted(img.glob("P*.png"))
    taken = set()
    for p in existing:
        try:
            taken.add(int(p.stem[1:]))
        except ValueError:
            pass
    next_n = (max(taken) + 1) if taken else 1
    if existing:
        print(f"[faces] {a.slug}: {len(existing)} plate(s) already registered; "
              f"new ones will continue from P{next_n:03d}")

    scored = []
    already = {p.name for p in existing}
    for p in sorted(img.glob("*.png")):
        if p.name in already:
            continue                      # do not re-register a plate as a copy of itself
        share = face_share(p)
        if share >= a.min_share:
            scored.append((share, p))
    scored.sort(reverse=True)
    picked = scored[:a.max]
    for i, (share, src) in enumerate(picked, next_n):
        dst = img / f"P{i:03d}.png"
        if not a.dry_run:
            shutil.copy2(src, dst)
    print(f"[faces] {a.slug}: {len(scored)} still(s) carry a face; "
          f"{len(picked)} registered as P### {'(dry run)' if a.dry_run else ''}"
          f"{' -- largest %.1f%% of frame' % (picked[0][0] * 100) if picked else ''}")
    return 0 if picked else 1


if __name__ == "__main__":
    raise SystemExit(main())
