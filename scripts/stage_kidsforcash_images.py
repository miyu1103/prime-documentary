#!/usr/bin/env py -3.11
"""Stage EP38 "Kids for Cash" Codex hero stills + real DPT depth maps.

Idempotent, atomic copy. NO GPU, NO render, NO publish. Source on H: is treated
as read-only (never modified).

Two destinations, matching how ``scripts/build_case_film_assets.py`` actually
consumes the files:

1. ``episodes/PD-2026-038-kidsforcash/04_scenes/generated_images/``
   The builder ``rglob("*.png")`` here for stills, skips ``*_depth.png`` (line
   ~523), and flattens the stills into ``remotion/public/<slug>/img/``. We keep
   the depth maps alongside the stills here too so the episode carries its
   paired real-DPT maps (provenance), even though the builder itself will not
   copy them onward.

2. ``remotion/public/kidsforcash/img/``
   The builder's depth gate (``depth_map_path``) looks for ``<stem>_depth.png``
   HERE, not in generated_images. The staging loop never places depth maps here
   (it skips ``_depth`` files), so without this step every depth-treated cut
   hard-fails the builder. Placing the pre-generated real-DPT maps here is the
   exact end-state that ``tools/depth/gen_depth.py remotion/public/kidsforcash``
   would produce, minus the GPU pass.

Naming convention: the builder keeps original basenames unchanged
(``shutil.copy2(p, PUB/"img"/p.name)``), and ``depth_map_path`` maps
``S01.png`` -> ``S01_depth.png`` in the same dir. So the source names
``S01.png`` / ``S01_depth.png`` already satisfy the builder verbatim; no rename
is required.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(r"C:\Users\aab15\Documents\prime-documentary")
SRC = Path(r"E:\pd-media\assets\ai\kidsforcash")
EP = "PD-2026-038-kidsforcash"
SLUG = "kidsforcash"
N = 40
EXPECT_W, EXPECT_H = 3840, 2160

GEN_DIR = ROOT / "episodes" / EP / "04_scenes" / "generated_images"
PUB_IMG = ROOT / "remotion" / "public" / SLUG / "img"


def atomic_copy(src: Path, dst: Path) -> None:
    """Copy bytes src -> dst atomically (temp in same dir, then os.replace)."""
    dst.parent.mkdir(parents=True, exist_ok=True)
    tmp = dst.with_name(dst.name + ".tmp")
    data = src.read_bytes()
    with open(tmp, "wb") as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, dst)  # atomic on same filesystem; idempotent overwrite


def stems() -> list[str]:
    return [f"S{i:02d}" for i in range(1, N + 1)]


def preflight() -> None:
    missing = []
    for s in stems():
        for name in (f"{s}.png", f"{s}_depth.png"):
            if not (SRC / name).is_file():
                missing.append(name)
    if missing:
        sys.exit(f"ABORT: {len(missing)} source file(s) missing on H:: {missing[:10]}")


def stage() -> None:
    for s in stems():
        still = SRC / f"{s}.png"
        depth = SRC / f"{s}_depth.png"
        # 1) generated_images: stills + depth (paired, canonical still source)
        atomic_copy(still, GEN_DIR / f"{s}.png")
        atomic_copy(depth, GEN_DIR / f"{s}_depth.png")
        # 2) public/img: depth maps only (builder's depth-lookup location)
        atomic_copy(depth, PUB_IMG / f"{s}_depth.png")


def verify() -> None:
    errors: list[str] = []
    pairs = 0
    for s in stems():
        for base, wexp, hexp in ((GEN_DIR / f"{s}.png", EXPECT_W, EXPECT_H),
                                 (GEN_DIR / f"{s}_depth.png", EXPECT_W, EXPECT_H),
                                 (PUB_IMG / f"{s}_depth.png", EXPECT_W, EXPECT_H)):
            if not base.is_file():
                errors.append(f"missing {base}")
                continue
            try:
                with Image.open(base) as im:
                    im.verify()
                with Image.open(base) as im:
                    w, h = im.size
                    fmt = im.format
                if fmt != "PNG":
                    errors.append(f"{base} not PNG (format={fmt})")
                if (w, h) != (wexp, hexp):
                    errors.append(f"{base} dims {w}x{h} != {wexp}x{hexp}")
            except Exception as e:  # noqa: BLE001 - report any unreadable file
                errors.append(f"{base} unreadable: {e}")
        # builder depth-lookup check: <stem>_depth.png beside staged still in public/img
        still_pub_depth = PUB_IMG / f"{s}_depth.png"
        gen_still = GEN_DIR / f"{s}.png"
        gen_depth = GEN_DIR / f"{s}_depth.png"
        if gen_still.is_file() and gen_depth.is_file() and still_pub_depth.is_file():
            pairs += 1

    print(f"pairs OK (still + depth in generated_images + depth in public/img): {pairs}/{N}")
    print(f"generated_images stills: {len(list(GEN_DIR.glob('S[0-9][0-9].png')))}")
    print(f"generated_images depth : {len(list(GEN_DIR.glob('S[0-9][0-9]_depth.png')))}")
    print(f"public/img depth       : {len(list(PUB_IMG.glob('S[0-9][0-9]_depth.png')))}")
    if errors:
        print(f"\n{len(errors)} ERROR(S):")
        for e in errors[:40]:
            print("  " + e)
        sys.exit(1)
    if pairs != N:
        sys.exit(f"ABORT: expected {N} complete pairs, got {pairs}")
    print("\nALL VERIFIED: 40/40 pairs, PNG readable, 3840x2160.")
    print(f"  generated_images -> {GEN_DIR}")
    print(f"  public/img (depth-lookup) -> {PUB_IMG}")


def main() -> None:
    preflight()
    stage()
    verify()


if __name__ == "__main__":
    main()
