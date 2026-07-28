#!/usr/bin/env python
"""Generate the 7 vertical stills + thumbnail for SHORT #3 (Mapp / "Can illegal-search evidence be used?").

Source: episodes/_planning/SHORTS_EP1-8.md SHORT #3 + §1 style suffix.
R1 / not sensitive (1961 case). NO real-person likeness, NO logo, NO legible real text.
Backend: local SDXL (A1111) 127.0.0.1:7860, Juggernaut XL.
Output : H:/pd-media/assets/ai/shorts/short03/short03_01.png .. _07.png + short03_thumb.png
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
OUT = r"H:/pd-media/assets/ai/shorts/short03"

SUFFIX = (
    ", vertical 9:16 full-frame composition, cinematic documentary still, dramatic moody "
    "lighting, deep navy-and-black palette with electric-blue and gold accents, photorealistic, "
    "ultra-detailed, shallow depth of field. No on-screen text, no watermark, no logo, "
    "no identifiable real person."
)

NEG = (
    "on-screen text, caption, subtitle, letters, words, numerals, typography, watermark, logo, signature, brand, "
    "identifiable real person, recognizable face, celebrity, portrait, close-up face, "
    "deformed, distorted, extra fingers, bad hands, lowres, blurry, jpeg artifacts, oversaturated, cartoon"
)

SHOTS = [
    ("short03_01", "A front door being forced open at night, splintering light blasting through the widening gap, tense, no people"),
    ("short03_02", "Faceless police silhouettes searching a modest living room at night without a warrant, no faces"),
    ("short03_03", "A blank empty document held up in a hand where a warrant should be, a conceptual absence, no legible text"),
    ("short03_04", "An old trunk opened to reveal a few worn books, an unexpected find, dramatic single light, no people"),
    ("short03_05", "An austere courtroom where a minor charge is read, a single shaft of light on an empty stand, no people"),
    ("short03_06", "Seized evidence on a table dissolving into drifting particles as it is excluded, conceptual, no people"),
    ("short03_07", "A glowing balance scale tipping toward an honest-policing symbol over a conviction gavel, gold rim light, no people"),
    ("short03_thumb", "A front door being forced open at night with splintering light through the gap, ominous key visual, no people, no legible text"),
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
    seed = 30000 + int(stem.split("_")[1].replace("thumb", "99"))
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
    print("[all ] short03 image generation finished", flush=True)


if __name__ == "__main__":
    main()
