#!/usr/bin/env python
"""Generate the 7 vertical stills + thumbnail for SHORT #19 (Varsity Blues / "the side door").

Source: episodes/_planning/SHORTS_EP19-24.md SHORT #19 image list + common style suffix (doc §0).
R3 / sensitive: living people who pleaded guilty. NO real-person likeness, NO nameable school/logo,
NO legible real text/numerals. Symbolic reconstruction only (invariant 11).
Backend: local SDXL (A1111) 127.0.0.1:7860, Juggernaut XL.
Output : H:/pd-media/assets/ai/shorts/short19/short19_01.png .. _07.png + short19_thumb.png
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
OUT = r"H:/pd-media/assets/ai/shorts/short19"

# Common style suffix from SHORTS_EP19-24.md §0 (EP1-8 §1) + vertical/no-text technicals.
SUFFIX = (
    ", museum-grade cinematic symbolic documentary still, vertical 9:16 full-frame composition, "
    "black and deep-navy base, electric-blue signal light, silver highlights, restrained muted-gold accent, "
    "film grain, dramatic moody lighting, photorealistic, ultra-detailed, shallow depth of field, "
    "symbolic reconstruction not authentic footage. No on-screen text, no watermark, no logo, "
    "no identifiable real person, no readable letters or numerals."
)

NEG = (
    "on-screen text, caption, subtitle, letters, words, numerals, typography, watermark, logo, signature, brand, "
    "team crest, school seal, identifiable real person, recognizable face, celebrity, portrait, close-up face, "
    "deformed, distorted, extra fingers, bad hands, lowres, blurry, jpeg artifacts, oversaturated, cartoon"
)

SHOTS = [
    ("short19_01", "A grand university gate at dusk with three doors implied — one bright front entrance and a small shadowed side door glowing faint gold, the symbolic side-door motif, no readable signage"),
    ("short19_02", "A faceless well-dressed parent's hands sliding a thick envelope of cash across a polished desk in low key, no faces, no logos, cold institutional light"),
    ("short19_03", "An empty ornate charity gala hall, one spotlight on a lectern, gold and navy, the hollow foundation, no people"),
    ("short19_04", "A blank sports jersey and a running shoe resting under a hard light beside a stack of cash, the bought athlete, no team marks, no numbers, symbolic"),
    ("short19_05", "A standardized-test answer sheet with rows of empty bubbles under a desk lamp, a single pencil, no readable text, tense stillness"),
    ("short19_06", "A dignified empty courtroom bench in a shaft of cold light, neutral and severe, no people, no seals"),
    ("short19_07", "A single empty chair on a bare stage under one gold spotlight, the displaced honest applicant, quiet and resonant, generous negative space for text"),
    ("short19_thumb", "A grand university gate at night with one glowing hidden side door and a stack of cash on the stone step, ominous symbolic key visual, gold and deep navy, no legible text"),
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
    seed = 190000 + int(stem.split("_")[1].replace("thumb", "99"))
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
    print("[all ] short19 image generation finished", flush=True)


if __name__ == "__main__":
    main()
