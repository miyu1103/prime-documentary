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
OUT = r"H:/pd-media/assets/ai/shorts/short33"

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

# EP33 Tyler v. Hennepin County (home-equity theft) — home / county office / scales / high court.
# text-free symbolic, no real-person likeness, no readable text / seals / house numbers / plates.
SHOTS = [
    ("short33_01", "A quiet suburban home at night, a blank unmarked foreclosure notice placard hanging on the front door in silhouette, a single warm light in one window, cold blue moonlight, empty street, no people, no readable text, no house numbers, no logos"),
    ("short33_02", "A cold empty government service counter at night, a neat stack of blank unmarked documents and a single pen under clinical blue overhead light, no people, no faces, no readable text on the papers, no seals, no logos"),
    ("short33_03", "The doorway of an emptied condominium at dusk, a single key resting on the threshold, dust and a low raking shaft of light, no one present, no house numbers, no readable text, no logos"),
    ("short33_04", "A tall stack of blank unmarked paper currency lit from above by cold light, one portion of the stack sinking into shadow as if taken away, deep navy void, symbolic, no currency symbols, no numerals, no readable text, no logos"),
    ("short33_05", "A precise brass balance scale tipped hard to one side, one pan overloaded far beyond the other, deep negative space, dramatic single light, symbolic 'more than owed', no text, no numerals, no logos"),
    ("short33_06", "An abstract marble colonnade evoking a supreme courthouse, tall columns and a single shaft of solemn light, hushed and monumental, no signage, no words, no seals, no statues of real people, no readable text"),
    ("short33_07", "A home's front door at night with a single key and a warm shaft of light returning toward it, a sense of something restored, generous dark negative space, symbolic bright-line motif, no readable text, no house numbers, no logos"),
    ("short33_thumb", "A dark silhouette of a house with a cold bright band of light streaming out of it and away, never returning, high-contrast iconic key visual, deep navy and electric-blue, muted-gold edge, no faces, no legible text, no numerals, no logos"),
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
    seed = 330000 + int(stem.split("_")[1].replace("thumb", "99"))
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
    print("[all ] short33 image generation finished", flush=True)


if __name__ == "__main__":
    main()
