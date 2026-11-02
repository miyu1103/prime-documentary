#!/usr/bin/env python
"""Generate the 7 vertical stills + thumbnail for SHORT #18 (Flash Crash / "$1T gone in 36 min").

Source: episodes/_planning/SHORTS_EP16-18.md SHORT #18 + EP1-8 §1 style suffix.
R3 / sensitive: living person who pleaded guilty. NO real-person likeness, NO nameable firm, NO legible
real text. Causation stays neutral (visuals never imply one man caused the crash). Neutral key visuals only.
Backend: local SDXL (A1111) 127.0.0.1:7860, Juggernaut XL.
Output : E:/pd-media/assets/ai/shorts/short18/short18_01.png .. _07.png + short18_thumb.png
Idempotent unless --force. Note: hires.fix occasionally returns HTTP 500; --no-hr falls back to 1088x1920.
"""
import argparse
import base64
import os
import sys
import time
import urllib.request
import json

API = "http://127.0.0.1:7860"
OUT = r"E:/pd-media/assets/ai/shorts/short18"

SUFFIX = (
    ", vertical 9:16 full-frame composition, cinematic documentary still, dramatic moody "
    "lighting, deep navy-and-black palette with electric-blue and red accents, photorealistic, "
    "ultra-detailed, shallow depth of field. No on-screen text, no watermark, no logo, "
    "no identifiable real person."
)

NEG = (
    "on-screen text, caption, subtitle, letters, words, numerals, typography, watermark, logo, signature, brand, "
    "identifiable real person, recognizable face, celebrity, portrait, close-up face, "
    "deformed, distorted, extra fingers, bad hands, lowres, blurry, jpeg artifacts, oversaturated, cartoon"
)

SHOTS = [
    ("short18_01", "A glowing red stock chart line plunging off a cliff into darkness then curling back up, electric red and deep navy, conceptual, no text"),
    ("short18_02", "A wall of abstract market tickers in free-fall, numbers blurred and unreadable, vertigo motion, cold blue, no legible text"),
    ("short18_03", "A single glowing penny coin alone on a dark trading floor while a giant company silhouette towers behind it, quiet irony, no face"),
    ("short18_04", "A dim suburban bedroom with one glowing computer monitor under a drawn curtain, a lone empty chair, no person, faint planes crossing the night sky outside"),
    ("short18_05", "A towering wall of glowing blue sell-order blocks in an order book dissolving into drifting pixels, a ghost vanishing, electric blue, abstract"),
    ("short18_06", "A balance scale: one tiny lone human silhouette on one side, a massive faceless swarm of machine nodes and a huge weight on the other, gold rim light, no faces"),
    ("short18_07", "A solemn empty federal courtroom bathed in a single shaft of light, dignified and neutral, no people"),
    ("short18_thumb", "A glowing red market chart line crashing off a cliff into darkness with a single glowing penny coin far below, ominous key visual, no legible text"),
]


def post(path, payload):
    req = urllib.request.Request(API + path, data=json.dumps(payload).encode("utf-8"),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as r:
        return json.load(r)


def gen(stem, core, force, no_hr):
    out_path = os.path.join(OUT, stem + ".png")
    if os.path.exists(out_path) and not force:
        print(f"[skip] {stem} exists", flush=True)
        return
    seed = 180000 + int(stem.split("_")[1].replace("thumb", "99"))
    payload = {
        "prompt": core + SUFFIX, "negative_prompt": NEG,
        "width": 832, "height": 1472, "steps": 34, "cfg_scale": 6,
        "sampler_name": "DPM++ 2M Karras", "seed": seed,
        "enable_hr": True, "hr_scale": 1.5, "hr_upscaler": "R-ESRGAN 4x+",
        "denoising_strength": 0.35, "hr_second_pass_steps": 12,
    }
    if no_hr:
        payload.update({"width": 1088, "height": 1920, "enable_hr": False})
        payload.pop("hr_scale", None); payload.pop("hr_upscaler", None)
        payload.pop("denoising_strength", None); payload.pop("hr_second_pass_steps", None)
    t0 = time.time()
    print(f"[gen ] {stem} ...", flush=True)
    res = post("/sdapi/v1/txt2img", payload)
    with open(out_path, "wb") as f:
        f.write(base64.b64decode(res["images"][0].split(",", 1)[-1]))
    print(f"[done] {stem} -> {out_path}  ({time.time()-t0:.0f}s)", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--only")
    ap.add_argument("--no-hr", action="store_true", help="fallback: base 1088x1920, no hires.fix")
    args = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    only = set(args.only.split(",")) if args.only else None
    for stem, core in SHOTS:
        if only and stem not in only:
            continue
        try:
            gen(stem, core, args.force, args.no_hr)
        except Exception as e:
            print(f"[FAIL] {stem}: {e}", file=sys.stderr, flush=True)
    print("[all ] short18 image generation finished", flush=True)


if __name__ == "__main__":
    main()
