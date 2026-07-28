#!/usr/bin/env python
"""Generate the 7 vertical stills + thumbnail for SHORT #20 (Gardner Heist / "still missing").

Source: episodes/_planning/SHORTS_EP19-24.md SHORT #20 image list + common style suffix (doc §0).
R2 / sensitive: unsolved crime. NO real-person likeness, NO named suspect, NO reproduction of the actual
stolen works (symbolic voids only), NO legible real text. Symbolic reconstruction only (invariant 11).
Backend: local SDXL (A1111) 127.0.0.1:7860, Juggernaut XL.
Output : H:/pd-media/assets/ai/shorts/short31/short31_01.png .. _07.png + short31_thumb.png
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
OUT = r"H:/pd-media/assets/ai/shorts/short35"

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

# EP35 Carole Hinders / IRS structuring — small cash restaurant / bank / seizure lane (distinct from EP33 home, EP34 airport).
# text-free symbolic, no real-person likeness, no readable text / signage / denominations / seals / brand marks.
SHOTS = [
    ("short35_01", "A small empty family diner at night after closing, chairs stacked on tables, a single warm light over an old cash register, cold blue window beyond, no people, no faces, no signage, no readable text, no logos"),
    ("short35_02", "A close-up of an open vintage cash register drawer filled with neat blank unmarked bills under warm diner light, honest small-business earnings, no denominations, no faces on the bills, no readable text, no logos"),
    ("short35_03", "A cold bank deposit counter at night, a small stack of blank cash beside a blank deposit slip and pen under clinical light, no people, no readable text, no seals, no logos"),
    ("short35_04", "A heavy padlock and chain clamped over a closed bank ledger book on a dark desk, a frozen account, single hard light, deep shadow, no readable text, no seals, no logos"),
    ("short35_05", "An empty vintage cash register drawer pulled fully open and scraped bare under a cold overhead light, a small paper seizure tag hanging blank, the money gone, no readable text, no seals, no logos"),
    ("short35_06", "A tall stack of blank folded newspapers isolated under a single bright spotlight in a dark void, symbolic national attention, no readable text, no headlines, no logos"),
    ("short35_07", "Warm golden morning light spilling through the front window of a small empty diner onto stacked chairs and a softly glowing old cash register, a sense of being restored and reopened, intimate interior only, absolutely no exterior signboard, no storefront lettering, no words anywhere, no readable text, no logos, no people"),
    ("short35_thumb", "A bare open cash register drawer with a single blank paper seizure tag, lit by a cold electric-blue shaft against deep navy, high-contrast iconic key visual, muted-gold edge, no faces, no denominations, no legible text, no logos"),
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
    seed = 350000 + int(stem.split("_")[1].replace("thumb", "99"))
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
    print("[all ] short35 image generation finished", flush=True)


if __name__ == "__main__":
    main()
