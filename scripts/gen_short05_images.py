#!/usr/bin/env python
"""Generate the 7 vertical stills + thumbnail for SHORT #5 (Madoff / "Steady returns, zero trades").

Source: episodes/_planning/SHORTS_EP1-8.md SHORT #5 + §1 style suffix.
R3 / sensitive: real Ponzi-scheme operator (deceased 2021). DO NOT depict him. NO human figure at all,
NO real-person likeness, NO nameable real logo, NO legible real text. Conceptual key visuals only.
Backend: local SDXL (A1111) 127.0.0.1:7860, Juggernaut XL.
Output : E:/pd-media/assets/ai/shorts/short05/short05_01.png .. _07.png + short05_thumb.png
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
OUT = r"E:/pd-media/assets/ai/shorts/short05"

SUFFIX = (
    ", vertical 9:16 full-frame composition, cinematic documentary still, dramatic moody "
    "lighting, deep navy-and-black palette with electric-blue and gold accents, photorealistic, "
    "ultra-detailed, shallow depth of field. No on-screen text, no watermark, no logo, "
    "no identifiable real person, no people."
)

# Strengthened: no human figure of any kind (operator must never be depicted).
NEG = (
    "person, people, human, human figure, man, silhouette of a person, face, recognizable face, "
    "celebrity, portrait, crowd, hands, body, "
    "on-screen text, caption, subtitle, letters, words, numerals, typography, watermark, logo, signature, brand, "
    "deformed, distorted, extra fingers, bad hands, lowres, blurry, jpeg artifacts, oversaturated, cartoon"
)

SHOTS = [
    ("short05_01", "An impossibly smooth ever-rising profit curve glowing in the dark, too perfect, a single gold line, no people"),
    ("short05_02", "A prestigious Wall Street office tower at dusk, gleaming and trusted, gold-lit windows, no people"),
    ("short05_03", "Polished steady financial account statements neatly stacked under warm light, no legible text, no people"),
    ("short05_04", "An empty glowing trading screen with no real trades, conceptual silence, deep blue, no people"),
    ("short05_05", "Glowing coins flowing in a closed circular loop, new money passed straight back out, conceptual, no people"),
    ("short05_06", "A tall tower of building blocks collapsing in slow motion, a 2008 crash, dramatic, no people"),
    ("short05_07", "A long dim corridor of receding archways stretching into darkness, the passage of long years, abstract, no people"),
    ("short05_thumb", "An impossibly smooth ever-rising golden profit curve glowing in the dark, too perfect to be real, ominous key visual, no people, no legible text"),
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
    seed = 50000 + int(stem.split("_")[1].replace("thumb", "99"))
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
    print("[all ] short05 image generation finished", flush=True)


if __name__ == "__main__":
    main()
