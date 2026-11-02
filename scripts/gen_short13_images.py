#!/usr/bin/env python
"""Generate the 7 vertical stills + thumbnail for SHORT #13 (arrest DNA collection / Maryland v. King).

Source: episodes/_planning/SHORTS_EP9-15.md SHORT #13 + EP1-8 §1 style suffix.
Backend: local SDXL (AUTOMATIC1111 API) 127.0.0.1:7860, Juggernaut XL.
Output : E:/pd-media/assets/ai/shorts/short13/short13_01.png .. _07.png + short13_thumb.png
No legible on-screen text, no identifiable real person. Idempotent unless --force.
Note: hires.fix occasionally returns HTTP 500; --no-hr falls back to a 1088x1920 base render.
"""
import argparse
import base64
import os
import sys
import time
import urllib.request
import json

API = "http://127.0.0.1:7860"
OUT = r"E:/pd-media/assets/ai/shorts/short13"

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

SHOTS = [
    ("short13_01", "A sterile cotton cheek swab held up under cold clinical booking-room light, latex-gloved hand, no face"),
    ("short13_02", "A gloved hand swabbing the inside of a cheek at a police booking desk, clinical and cold, no identifiable face"),
    ("short13_03", "A glowing electric-blue DNA double helix rising from the tip of a cotton swab, dark background"),
    ("short13_04", "A fingerprint card lying beside a glowing DNA helix, a direct side-by-side comparison, cold light"),
    ("short13_05", "A vast dark database grid of countless nodes with one single node suddenly lighting up, a hit"),
    ("short13_06", "A human body silhouette scanned by an investigative beam of light, a search of the body, no face"),
    ("short13_07", "An enormous national database structure swallowing one more ordinary glowing DNA helix into its archive"),
    ("short13_thumb", "A cotton cheek swab beside a glowing electric-blue DNA double helix, ominous clinical key visual, no legible text"),
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
    seed = 130000 + int(stem.split("_")[1].replace("thumb", "99"))
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
    print("[all ] short13 image generation finished", flush=True)


if __name__ == "__main__":
    main()
