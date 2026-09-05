#!/usr/bin/env python
"""Generate the 7 vertical stills + thumbnail for SHORT #15 (Theranos / when a bold promise becomes a crime).

Source: episodes/_planning/SHORTS_EP9-15.md SHORT #15 + EP1-8 §1 style suffix.
R3 topic (real, litigated): NO real-person likeness, NO legible real names/logos, neutral key visuals only.
Backend: local SDXL (AUTOMATIC1111 API) 127.0.0.1:7860, Juggernaut XL.
Output : E:/pd-media/assets/ai/shorts/short15/short15_01.png .. _07.png + short15_thumb.png
Idempotent unless --force. Note: hires.fix occasionally returns HTTP 500; --no-hr falls back to 1088x1920 base.
"""
import argparse
import base64
import os
import sys
import time
import urllib.request
import json

API = "http://127.0.0.1:7860"
OUT = r"E:/pd-media/assets/ai/shorts/short15"

SUFFIX = (
    ", vertical 9:16 full-frame composition, cinematic documentary still, dramatic moody "
    "lighting, deep navy-and-black palette with electric-blue and gold accents, photorealistic, "
    "ultra-detailed, shallow depth of field. No on-screen text, no watermark, no logo, "
    "no identifiable real person."
)

NEG = (
    "on-screen text, caption, subtitle, letters, words, typography, watermark, logo, signature, brand, "
    "identifiable real person, recognizable face, celebrity, portrait, close-up face, "
    "deformed, distorted, extra fingers, bad hands, lowres, blurry, jpeg artifacts, oversaturated, cartoon"
)

SHOTS = [
    ("short15_01", "A single luminous drop of blood suspended in darkness, electric-blue rim light, hyper detailed"),
    ("short15_02", "A sleek black-box blood-testing machine glowing on the outside but hollow and dark and empty within, no logo"),
    ("short15_03", "An empty illuminated award pedestal under a single dramatic golden spotlight on a dark empty stage, fame and acclaim implied, absolutely no person, no figure, no silhouette, no face, no portrait"),
    ("short15_04", "Rows of ordinary commercial lab analyzers behind a curtain quietly doing the real work, cold light"),
    ("short15_05", "A single finger-prick drop of blood producing shaky unreliable glowing readings, no face"),
    ("short15_06", "A solemn empty federal courtroom, dramatic grand chamber, shafts of light, no people"),
    ("short15_07", "An abstract verdict board with mixed neutral outcome icons, some marked some cleared, no text"),
    ("short15_thumb", "A single glowing drop of blood beside a hollow dark testing device, ominous key visual, no legible text"),
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
    seed = 150000 + int(stem.split("_")[1].replace("thumb", "99"))
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
    print("[all ] short15 image generation finished", flush=True)


if __name__ == "__main__":
    main()
