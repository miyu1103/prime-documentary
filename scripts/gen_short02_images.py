#!/usr/bin/env python
"""Generate the 7 vertical stills + thumbnail for SHORT #2 (Gideon / "A pencil that changed every court").

Source: episodes/_planning/SHORTS_EP1-8.md SHORT #2 + §1 style suffix.
R1 / not sensitive (1963 case). NO real-person likeness, NO logo, NO legible real text.
Backend: local SDXL (A1111) 127.0.0.1:7860, Juggernaut XL.
Output : E:/pd-media/assets/ai/shorts/short02/short02_01.png .. _07.png + short02_thumb.png
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
OUT = r"E:/pd-media/assets/ai/shorts/short02"

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
    ("short02_01", "A lone empty defense table in a dim empty courtroom with no lawyer present, a single shaft of light, no people"),
    ("short02_02", "A closed courthouse door with a faceless figure's long shadow turned away, denied entry, no face"),
    ("short02_03", "A simple pencil and a single sheet of prison stationery on a bare cell bunk under barred-window light, no people"),
    ("short02_04", "A humble handwritten petition page lit dramatically on a dark surface, no legible text"),
    ("short02_05", "A plain envelope rising and drifting up toward a distant grand marble institution, conceptual, no people"),
    ("short02_06", "Nine empty judicial chairs unified in a single row, a nine-to-zero result, navy and gold, no people"),
    ("short02_07", "A glowing wooden gavel over a small model courtroom, change rippling outward, gold rim light, no people"),
    ("short02_thumb", "A simple pencil resting on a handwritten page on a prison cell bunk under barred-window light, ominous key visual, no people, no legible text"),
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
    seed = 20000 + int(stem.split("_")[1].replace("thumb", "99"))
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
    print("[all ] short02 image generation finished", flush=True)


if __name__ == "__main__":
    main()
