#!/usr/bin/env python
"""Generate the 7 vertical stills + thumbnail for SHORT #20 (Gardner Heist / "still missing").

Source: episodes/_planning/SHORTS_EP19-24.md SHORT #20 image list + common style suffix (doc §0).
R2 / sensitive: unsolved crime. NO real-person likeness, NO named suspect, NO reproduction of the actual
stolen works (symbolic voids only), NO legible real text. Symbolic reconstruction only (invariant 11).
Backend: local SDXL (A1111) 127.0.0.1:7860, Juggernaut XL.
Output : H:/pd-media/assets/ai/shorts/short27/short27_01.png .. _07.png + short27_thumb.png
Idempotent unless --force. --no-hr falls back to base 1088x1920 if hires.fix 500s.
"""
import argparse
import base64
import os
import sys
import time
import urllib.request
import json

API = "http://127.0.0.1:7860"
OUT = r"H:/pd-media/assets/ai/shorts/short27"

SUFFIX = (
    ", museum-grade cinematic symbolic documentary still, vertical 9:16 full-frame composition, "
    "black and deep-navy base, electric-blue signal light, silver highlights, restrained muted-gold accent, "
    "film grain, dramatic moody lighting, photorealistic, ultra-detailed, shallow depth of field, "
    "symbolic reconstruction not authentic footage. No on-screen text, no watermark, no logo, "
    "no identifiable real person, no readable letters or numerals."
)

NEG = (
    "on-screen text, caption, subtitle, letters, words, numerals, typography, watermark, logo, signature, brand, "
    "identifiable real person, recognizable face, celebrity, portrait, close-up face, "
    "deformed, distorted, extra fingers, bad hands, lowres, blurry, jpeg artifacts, oversaturated, cartoon"
)

SHOTS = [
    ("short27_01", "A lone car pulled onto the shoulder of an empty two-lane highway just after midnight, cold headlight cones on wet asphalt, restrained red-and-blue patrol light reflected low on the road, no license plates, no faces, generous empty sky for text"),
    ("short27_02", "A working police-dog silhouette resting alert in the back seat of a patrol car at night, cold blue cast through the glass, procedural and neutral, no handler, no badge, no logo"),
    ("short27_03", "Anonymous hands passing a single folded blank paper slip through a dark car window, faint dashboard glow, the written warning its business finished, no readable text on the paper"),
    ("short27_04", "An analog stopwatch hovering over an empty gravel roadside shoulder at night, sweeping second hand caught in electric-blue light, the dead time of waiting, no legible numerals, tense stillness"),
    ("short27_05", "A leashed police-dog silhouette circling a stopped car in cold headlight beams on a dark road, restrained blue light on the paint, procedural and calm, never attacking, no faces, no plates, no logos"),
    ("short27_06", "A symbolic hourglass in deep-navy low key, the sand rendered as electric-blue light running low, a single muted-gold rim, the constitutional limit measured in time, no text"),
    ("short27_07", "A thin electric-blue line drawn cleanly across dark asphalt with a car's red taillights just past it, the moment a lawful stop becomes an unlawful seizure, minimalist premium composition, wide empty space at top"),
    ("short27_thumb", "An empty night highway shoulder with restrained red-and-blue light low on wet asphalt and an analog stopwatch overlaid glowing electric-blue, iconic key visual, no plates, no legible numerals, no text"),
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
    seed = 270000 + int(stem.split("_")[1].replace("thumb", "99"))
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
    print("[all ] short27 image generation finished", flush=True)


if __name__ == "__main__":
    main()
