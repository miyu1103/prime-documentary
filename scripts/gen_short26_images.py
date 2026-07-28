#!/usr/bin/env python
"""Generate the 7 vertical stills + thumbnail for SHORT #20 (Gardner Heist / "still missing").

Source: episodes/_planning/SHORTS_EP19-24.md SHORT #20 image list + common style suffix (doc §0).
R2 / sensitive: unsolved crime. NO real-person likeness, NO named suspect, NO reproduction of the actual
stolen works (symbolic voids only), NO legible real text. Symbolic reconstruction only (invariant 11).
Backend: local SDXL (A1111) 127.0.0.1:7860, Juggernaut XL.
Output : H:/pd-media/assets/ai/shorts/short26/short26_01.png .. _07.png + short26_thumb.png
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
OUT = r"H:/pd-media/assets/ai/shorts/short26"

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
    ("short26_01", "A lone 1960s glass telephone booth glowing warm on a rain-slick empty night street, an anonymous silhouette inside seen through misted glass, deep-navy void around it, one shaft of muted-gold light, no readable signage, no face"),
    ("short26_02", "An extreme macro of a small hidden microphone and a thin wire taped to the metal top edge on the outside of a glass phone booth, cold electric-blue rim light, clandestine surveillance detail, no logos, no text"),
    ("short26_03", "A vintage reel-to-reel recorder turning slowly in shadow with one faint red record glow and headphones nearby, surveillance noir, electric blue on black, no faces, no text"),
    ("short26_04", "A heavy old wooden door and a brass keyhole in deep shadow, the outdated idea that privacy needs a physical wall to breach, cold navy with a single muted-gold light, no readable text"),
    ("short26_05", "An anonymous silhouette pulling a phone-booth door shut and dropping a coin, a warm interior glow sealing the space while a cold electric-blue sound-wave leaks out through the glass, intimacy versus intrusion, faceless, no readable numbers"),
    ("short26_06", "A minimalist balance scale in low key, a small model house on one pan sinking and a small warm human figure of light on the other pan rising, people not places, symbolic, no faces, no text"),
    ("short26_07", "A modern smartphone glowing on a dark table with faint electric-blue data-streams and signal arcs rising into the night, ambient surveillance, no readable screen, no icons, no faces, no logos, generous negative space at top"),
    ("short26_thumb", "A lone glowing glass phone booth on a dark wet street with a cold electric-blue sound-wave leaking through the glass and a faint muted-gold aura around the unseen person inside, iconic key visual, no faces, no legible text"),
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
    seed = 260000 + int(stem.split("_")[1].replace("thumb", "99"))
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
    print("[all ] short26 image generation finished", flush=True)


if __name__ == "__main__":
    main()
