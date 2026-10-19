#!/usr/bin/env python
"""Generate the 7 vertical stills + thumbnail for SHORT #8 (Carpenter).

Source of truth: episodes/_planning/SHORTS_EP1-8.md  (SHORT #8 prompts + §1 common style suffix).
Backend: local SDXL (AUTOMATIC1111 API) on 127.0.0.1:7860, Juggernaut XL.
Output : E:/pd-media/assets/ai/shorts/short08/short08_01.png .. _07.png + short08_thumb.png

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
OUT = r"E:/pd-media/assets/ai/shorts/short08"

# §1 common style suffix (appended to every prompt, verbatim from the design doc).
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

# (filename stem, prompt core)  — from SHORTS_EP1-8.md SHORT #8.
SHOTS = [
    ("short08_01", "A glowing map dotted with a long trail of a single phone's movements, conceptual"),
    ("short08_02", "A phone pinging a cell tower as a location point lights up, night city"),
    ("short08_03", "A field of cell towers across a dark city, constant connection, conceptual"),
    ("short08_04", "Months of location dots accumulating into a detailed map of a life, abstract"),
    ("short08_05", "A carrier handing over a glowing location-history file, conceptual, no face"),
    ("short08_06", "A 5-4 split judicial bench, a narrow ruling, navy and gold"),
    ("short08_07", "A warrant scroll now required over a location map, the digital trail protected"),
    ("short08_thumb", "A glowing location-trail map of a phone seen on a dark surface, ominous key visual"),
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
    # Deterministic per-shot seed so reruns reproduce; varies by stem.
    seed = 80000 + int(stem.split("_")[1].replace("thumb", "99"))
    payload = {
        "prompt": core + SUFFIX,
        "negative_prompt": NEG,
        "width": 832,
        "height": 1472,            # 9:16-ish, /8-safe (832/1472 = 0.565)
        "steps": 34,
        "cfg_scale": 6,
        "sampler_name": "DPM++ 2M Karras",
        "seed": seed,
        "enable_hr": True,
        "hr_scale": 1.5,           # -> 1248x2208, above 1080x1920
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
    ap.add_argument("--only", help="comma list of stems to generate (e.g. short08_06)")
    args = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    only = set(args.only.split(",")) if args.only else None
    for stem, core in SHOTS:
        if only and stem not in only:
            continue
        try:
            gen(stem, core, args.force)
        except Exception as e:  # keep going; report per-shot
            print(f"[FAIL] {stem}: {e}", file=sys.stderr, flush=True)
    print("[all ] short08 image generation finished", flush=True)


if __name__ == "__main__":
    main()
