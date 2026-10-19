#!/usr/bin/env python3
r"""Upscale EP35 (PD-2026-035 "hinders") Codex stills to >=3840 long edge.

NOT image generation -- a CPU-only post-process upscale of the already-Codex-
generated 1672px stills so preflight_receipt's assets.stills 4K floor (>=3840 long
edge) resolves honestly. Uses Pillow LANCZOS (high-quality resample) instead of
R-ESRGAN because the full-episode Remotion render currently owns the GPU (100%
util, ~570MB free VRAM); a GPU upscale would risk OOM / crashing the live render,
which is the top constraint. LANCZOS is CPU-only and cannot touch the render.

Reads the live stills in remotion/public/hinders/img (68 base PNGs, excludes
*_depth.png and CONTACT_SHEET*), writes 4K PNGs with the SAME names into
remotion/public/hinders/img_4k. NEVER overwrites the source dir. Idempotent
(skips outputs already >=3840). The parent swaps img_4k -> img only AFTER the
render finishes.

    py -3.11 scripts/upscale_hinders_4k_lanczos_v001.py
"""
from __future__ import annotations
import glob, sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "remotion/public/hinders/img"
DST = ROOT / "remotion/public/hinders/img_4k"
MIN_EDGE = 3840


def base_pngs() -> list[Path]:
    out = []
    for f in sorted(glob.glob(str(SRC / "*.png"))):
        p = Path(f)
        n = p.name
        if "_depth" in n or n.startswith("CONTACT_SHEET"):
            continue
        out.append(p)
    return out


def target_size(w: int, h: int) -> tuple[int, int]:
    # scale so the LONG edge >= MIN_EDGE, preserving aspect ratio.
    long_edge = max(w, h)
    scale = MIN_EDGE / long_edge
    nw, nh = round(w * scale), round(h * scale)
    # guarantee the floor even after rounding
    if max(nw, nh) < MIN_EDGE:
        if w >= h:
            nw = MIN_EDGE; nh = round(h * MIN_EDGE / w)
        else:
            nh = MIN_EDGE; nw = round(w * MIN_EDGE / h)
    return nw, nh


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    srcs = base_pngs()
    if len(srcs) != 68:
        print(f"WARNING: expected 68 base stills, found {len(srcs)}")
    if not srcs:
        print(f"no source PNGs in {SRC}"); return 1
    DST.mkdir(parents=True, exist_ok=True)
    done = skipped = 0
    for i, p in enumerate(srcs, 1):
        outp = DST / p.name
        if outp.exists():
            w, h = Image.open(outp).size
            if max(w, h) >= MIN_EDGE:
                skipped += 1
                continue
        im = Image.open(p).convert("RGB")
        w, h = im.size
        nw, nh = target_size(w, h)
        up = im.resize((nw, nh), Image.LANCZOS)
        tmp = outp.with_suffix(".tmp.png")
        up.save(tmp, "PNG")
        tmp.replace(outp)
        print(f"  [{i:02d}/{len(srcs)}] {p.name} {w}x{h} -> {nw}x{nh}")
        done += 1
    # verify
    outs = base_verify()
    bad = [(n, s) for n, s in outs if max(map(int, s.split("x"))) < MIN_EDGE]
    print(f"\nupscaled={done} skipped={skipped} total={len(outs)} under-{MIN_EDGE}={len(bad)}")
    if bad:
        print("STILL SMALL:", bad[:10]); return 1
    print(f"OK all {len(outs)} EP35 stills >= {MIN_EDGE} long edge (stills 4K floor will pass)")
    return 0


def base_verify() -> list[tuple[str, str]]:
    res = []
    for f in sorted(glob.glob(str(DST / "*.png"))):
        p = Path(f)
        if "_depth" in p.name or p.name.startswith("CONTACT_SHEET"):
            continue
        w, h = Image.open(p).size
        res.append((p.name, f"{w}x{h}"))
    return res


if __name__ == "__main__":
    raise SystemExit(main())
