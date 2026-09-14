#!/usr/bin/env python
"""Generate the 7 vertical stills + thumbnail for SHORT #11 (Mahanoy Area SD v. B.L.).

Source: episodes/_planning/SHORTS_EP9-15.md SHORT #11 + EP1-8 §1 style suffix.
Backend: local SDXL (AUTOMATIC1111 API) 127.0.0.1:7860, Juggernaut XL.
Output : E:/pd-media/assets/ai/shorts/short11/short11_01.png .. _07.png + short11_thumb.png
No identifiable real person (esp. no minors' faces). Idempotent unless --force.
"""
import argparse
import base64
import os
import sys
import time
import urllib.request
import json

API = "http://127.0.0.1:7860"
OUT = r"E:/pd-media/assets/ai/shorts/short11"

SUFFIX = (
    ", vertical 9:16 full-frame composition, cinematic documentary still, dramatic moody "
    "lighting, deep navy-and-black palette with electric-blue and gold accents, photorealistic, "
    "ultra-detailed, shallow depth of field. No on-screen text, no watermark, no logo, "
    "no identifiable real person."
)

NEG = (
    "on-screen text, caption, subtitle, letters, words, typography, watermark, logo, signature, "
    "identifiable real person, recognizable face, minor, child face, celebrity, portrait, close-up face, "
    "deformed, distorted, extra fingers, bad hands, lowres, blurry, jpeg artifacts, oversaturated, cartoon"
)

SHOTS = [
    ("short11_01", "A glowing smartphone in a dark room with a ghost-like vanishing icon, electric blue"),
    ("short11_02", "A lone teenager silhouette on empty gym bleachers at dusk, dejected, no face"),
    ("short11_03", "An ephemeral photo dissolving into drifting pixels, electric blue, conceptual"),
    ("short11_04", "One frozen frame remaining solid while images around it disappear, a screenshot motif"),
    ("short11_05", "A schoolhouse gate dissolving into drifting pixels, dramatic"),
    ("short11_06", "A soft fuzzy glowing boundary line in mist, deliberately fuzzy"),
    ("short11_07", "A wall with a deliberate doorway gap cut into it, not a wall, conceptual"),
    ("short11_thumb", "A glowing smartphone at night with a ghost-like vanishing icon, ominous key visual"),
]


def post(path, payload):
    req = urllib.request.Request(API + path, data=json.dumps(payload).encode("utf-8"),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as r:
        return json.load(r)


def gen(stem, core, force):
    out_path = os.path.join(OUT, stem + ".png")
    if os.path.exists(out_path) and not force:
        print(f"[skip] {stem} exists", flush=True)
        return
    seed = 110000 + int(stem.split("_")[1].replace("thumb", "99"))
    payload = {
        "prompt": core + SUFFIX, "negative_prompt": NEG,
        "width": 832, "height": 1472, "steps": 34, "cfg_scale": 6,
        "sampler_name": "DPM++ 2M Karras", "seed": seed,
        "enable_hr": True, "hr_scale": 1.5, "hr_upscaler": "R-ESRGAN 4x+",
        "denoising_strength": 0.35, "hr_second_pass_steps": 12,
    }
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
    print("[all ] short11 image generation finished", flush=True)


if __name__ == "__main__":
    main()
