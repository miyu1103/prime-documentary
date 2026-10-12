#!/usr/bin/env python3
r"""Upscale EP28 Codex hero stills to >=3840 long edge via the local A1111 extras API.

NOT image generation — a post-process upscale of the already-Codex-generated stills
(spec v2 row 5: "upscale + denoise if the raw gen is smaller"). Reads the 1672px
backups in 04_scenes/_codex_src_1672, upscales x2.5 with R-ESRGAN 4x+ (realistic),
writes 4K PNGs back into 04_scenes/generated_images/codex_v001 (same names) so
build_case_film_assets.py stages the 4K versions. Idempotent + resumable (skips
files already >=3840 in the destination).

    py -3.11 scripts/upscale_forfeiture_images_v001.py
"""
from __future__ import annotations
import base64, io, sys, time, urllib.request, json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "episodes/PD-2026-028-forfeiture/04_scenes/_codex_src_1672"
DST = ROOT / "episodes/PD-2026-028-forfeiture/04_scenes/generated_images/codex_v001"
API = "http://127.0.0.1:7860/sdapi/v1/extra-single-image"
UPSCALER = "R-ESRGAN 4x+"
RESIZE = 2.5           # 1672 -> 4180 long edge (>=3840)
MIN_EDGE = 3840


def upscale_one(png: Path, retries: int = 3) -> bytes:
    b64 = base64.b64encode(png.read_bytes()).decode()
    body = json.dumps({
        "resize_mode": 0, "upscaling_resize": RESIZE, "upscaler_1": UPSCALER,
        "image": b64, "show_extras_results": True,
    }).encode()
    last = None
    for a in range(retries):
        try:
            req = urllib.request.Request(API, data=body, method="POST",
                                         headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=180) as r:
                out = json.loads(r.read().decode())["image"]
            return base64.b64decode(out)
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(2 * (a + 1))
    raise RuntimeError(f"upscale failed after {retries}: {last}")


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    srcs = sorted(SRC.glob("*.png"))
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
        data = upscale_one(p)
        outp.write_bytes(data)
        w, h = Image.open(io.BytesIO(data)).size
        print(f"  [{i:02d}/{len(srcs)}] {p.name} -> {w}x{h} ({len(data)//1024}KB)")
        done += 1
    # verify
    bad = []
    for p in sorted(DST.glob("*.png")):
        w, h = Image.open(p).size
        if max(w, h) < MIN_EDGE:
            bad.append((p.name, f"{w}x{h}"))
    print(f"\nupscaled={done} skipped={skipped} total={len(list(DST.glob('*.png')))} "
          f"under-{MIN_EDGE}={len(bad)}")
    if bad:
        print("STILL SMALL:", bad[:10]); return 1
    print("OK all hero stills >= 3840 long edge (image_resolution gate will pass)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
