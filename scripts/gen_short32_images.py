#!/usr/bin/env python
"""Generate the 7 vertical stills + thumbnail for SHORT #20 (Gardner Heist / "still missing").

Source: episodes/_planning/SHORTS_EP19-24.md SHORT #20 image list + common style suffix (doc §0).
R2 / sensitive: unsolved crime. NO real-person likeness, NO named suspect, NO reproduction of the actual
stolen works (symbolic voids only), NO legible real text. Symbolic reconstruction only (invariant 11).
Backend: local SDXL (A1111) 127.0.0.1:7860, Juggernaut XL.
Output : E:/pd-media/assets/ai/shorts/short31/short31_01.png .. _07.png + short31_thumb.png
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
OUT = r"E:/pd-media/assets/ai/shorts/short32"

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
    ("short32_01", "A night highway traffic stop seen from behind, red-and-blue emergency light washing across wet black asphalt, the trunk lid of a dark sedan lifting open into the glare, faceless silhouettes only, cold rain sheen, no license plates, no readable text, no logos"),
    ("short32_02", "A lonely 1920s Prohibition-era highway at night, a single pair of round vintage headlights cutting through darkness, wooden liquor crates stacked on the back seat of an old car, anonymous, moody amber-and-navy period atmosphere, no plates, no labels, no readable text"),
    ("short32_03", "Anonymous gloved hands tearing open a car seat cushion, unlabeled dark glass bottles emerging one after another from behind the ripped upholstery, tight dramatic light, no faces, no bottle labels, no readable text, no logos"),
    ("short32_04", "A stark split composition, on one side a house wrapped in a warm glowing protective outline, on the other side a car covered by a thin cracking blue shield, a single bright hairline of light dividing them, symbolic diagram feel, no text, no signage"),
    ("short32_05", "A glowing blue x-ray style cutaway of a car interior, the glovebox, the trunk and a duffel bag each lit up as separate glowing zones, clean holographic motion-graphic look, deep navy void, no text, no numerals, no logos"),
    ("short32_06", "A quiet suburban house at dusk, a motorcycle-shaped form hidden under a taut tarp in the driveway pressed close against the side wall of the home, a faint bright line of light along the ground, hushed blue evening, no plates, no readable text"),
    ("short32_07", "A bright hairline line of pure light running across a driveway, separating an exposed car on one side from a home wrapped in a warm protective glow on the other, generous dark negative space, symbolic bright-line motif, no text, no logos"),
    ("short32_thumb", "A car and a house separated by a single blazing vertical line of light, the car exposed in cold blue, the home shielded in warm gold, iconic high-contrast key visual, deep navy background, no faces, no legible text, no logos"),
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
    seed = 320000 + int(stem.split("_")[1].replace("thumb", "99"))
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
    print("[all ] short32 image generation finished", flush=True)


if __name__ == "__main__":
    main()
