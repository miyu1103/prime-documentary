#!/usr/bin/env python
"""Generate the 7 vertical stills + thumbnail for SHORT #10 (Kelo v. City of New London).

Source of truth: episodes/_planning/SHORTS_EP9-15.md  (SHORT #10 prompts + EP1-8 §1 common style suffix).
Backend: local SDXL (AUTOMATIC1111 API) on 127.0.0.1:7860, Juggernaut XL.
Output : H:/pd-media/assets/ai/shorts/short10/short10_01.png .. _07.png + short10_thumb.png
Idempotent: skips a file that already exists unless --force.
"""
import argparse
import base64
import os
import sys
import time
import urllib.request
import json

API = "http://127.0.0.1:7860"
OUT = r"H:/pd-media/assets/ai/shorts/short10"

SUFFIX = (
    ", vertical 9:16 full-frame composition, cinematic documentary still, dramatic moody "
    "lighting, deep navy-and-black palette with electric-blue and gold accents, photorealistic, "
    "ultra-detailed, shallow depth of field. No on-screen text, no watermark, no logo, "
    "no identifiable real person."
)

NEG = (
    "on-screen text, caption, subtitle, letters, words, typography, watermark, logo, signature, "
    "identifiable real person, recognizable face, celebrity, portrait, close-up face, "
    "deformed, distorted, extra fingers, bad hands, lowres, blurry, jpeg artifacts, oversaturated, cartoon"
)

# (filename stem, prompt core)  — from SHORTS_EP9-15.md SHORT #10 (Kelo).
SHOTS = [
    ("short10_01", "A small lone house standing in the middle of a vast cleared dirt lot at dusk, isolated"),
    ("short10_02", "A modest pink clapboard house with a water view, warm light, small and defiant"),
    ("short10_03", "A bulldozer silhouette at the edge of a quiet neighborhood at dawn, ominous"),
    ("short10_04", "A glossy architectural model of glass towers looming over a single tiny real house"),
    ("short10_05", "An aged Fifth Amendment parchment under a museum spotlight"),
    ("short10_06", "Nine judicial chairs split five blue and four gold, a 5-4 ruling"),
    ("short10_07", "A weed-grown empty lot years later, desolate, the project never built"),
    ("short10_thumb", "A small lone pink house standing alone in a vast cleared dirt lot at dusk, ominous key visual"),
]


def post(path, payload):
    req = urllib.request.Request(
        API + path,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=600) as r:
        return json.load(r)


def gen(stem, core, force):
    out_path = os.path.join(OUT, stem + ".png")
    if os.path.exists(out_path) and not force:
        print(f"[skip] {stem} exists", flush=True)
        return
    seed = 100000 + int(stem.split("_")[1].replace("thumb", "99"))
    payload = {
        "prompt": core + SUFFIX,
        "negative_prompt": NEG,
        "width": 832,
        "height": 1472,
        "steps": 34,
        "cfg_scale": 6,
        "sampler_name": "DPM++ 2M Karras",
        "seed": seed,
        "enable_hr": True,
        "hr_scale": 1.5,
        "hr_upscaler": "R-ESRGAN 4x+",
        "denoising_strength": 0.35,
        "hr_second_pass_steps": 12,
    }
    t0 = time.time()
    print(f"[gen ] {stem} ...", flush=True)
    res = post("/sdapi/v1/txt2img", payload)
    img_b64 = res["images"][0]
    with open(out_path, "wb") as f:
        f.write(base64.b64decode(img_b64.split(",", 1)[-1]))
    print(f"[done] {stem} -> {out_path}  ({time.time()-t0:.0f}s)", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--only")
    args = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    only = set(args.only.split(",")) if args.only else None
    for stem, core in SHOTS:
        if only and stem not in only:
            continue
        try:
            gen(stem, core, args.force)
        except Exception as e:
            print(f"[FAIL] {stem}: {e}", file=sys.stderr, flush=True)
    print("[all ] short10 image generation finished", flush=True)


if __name__ == "__main__":
    main()
