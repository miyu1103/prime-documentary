#!/usr/bin/env python
"""Generate the 7 vertical stills + thumbnail for SHORT #9 (Timbs v. Indiana).

Source of truth: episodes/_planning/SHORTS_EP9-15.md  (SHORT #9 prompts + EP1-8 §1 common style suffix).
Backend: local SDXL (AUTOMATIC1111 API) on 127.0.0.1:7860, Juggernaut XL.
Output : E:/pd-media/assets/ai/shorts/short09/short09_01.png .. _07.png + short09_thumb.png

Invariants: vertical 9:16, >=1080x1920 (hires fix), no on-screen text, no identifiable real person.
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
OUT = r"E:/pd-media/assets/ai/shorts/short09"

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

# (filename stem, prompt core)  — from SHORTS_EP9-15.md SHORT #9 (Timbs).
SHOTS = [
    ("short09_01", "A car key with a blank red evidence tag on a cold steel government table"),
    ("short09_02", "A plain life-insurance envelope on a worn kitchen table, a quiet sense of loss"),
    ("short09_03", "A black SUV silhouette under a dealership light at night, rain-slick asphalt"),
    ("short09_04", "A brass balance scale with a full-size SUV dwarfing a tiny stack of coins, gold rim"),
    ("short09_05", "An SUV being winched onto a flatbed tow truck at night, headlights flaring"),
    ("short09_06", "Nine unified judicial chairs, a 9-0 result, navy and gold"),
    ("short09_07", "Endless rows of seized vehicles in a vast impound lot, aerial, cold blue"),
    ("short09_thumb", "A single car key with an ominous red evidence tag on a dark government table, key visual"),
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
    seed = 90000 + int(stem.split("_")[1].replace("thumb", "99"))
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
    ap.add_argument("--force", action="store_true", help="regenerate even if file exists")
    ap.add_argument("--only", help="comma list of stems to generate (e.g. short09_06)")
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
    print("[all ] short09 image generation finished", flush=True)


if __name__ == "__main__":
    main()
