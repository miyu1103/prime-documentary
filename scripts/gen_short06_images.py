#!/usr/bin/env python
"""Generate the 7 vertical stills + thumbnail for SHORT #6 (Terry v. Ohio) at MAX quality.

Source of truth: episodes/_planning/SHORTS_EP1-8.md  (SHORT #6 prompts + §1 common style suffix).
Backend: local SDXL (AUTOMATIC1111 API) on 127.0.0.1:7860, Juggernaut XL Ragnarok.
Output : E:/pd-media/assets/ai/shorts/short06/short06_01.png .. _07.png + short06_thumb.png

Quality-first (project policy [[render-quality-first]]): native 832x1472 9:16, hires-fix to ~4K
vertical via DAT x4, 60 base steps + 25 hires steps, DPM++ 2M SDE Karras. No NVENC / no shortcuts.

Invariants: vertical 9:16, well above 1080x1920, no on-screen text, no identifiable real person
(SHORTS_EP1-8 §0). Idempotent: skips an existing file unless --force.
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import time
import urllib.request

API = "http://127.0.0.1:7860"
OUT = r"E:/pd-media/assets/ai/shorts/short06"
MODEL = "juggernautXL_ragnarokBy"  # photoreal flagship ([[reference_sdxl_launch]])

# §1 common style suffix (appended to every prompt, verbatim from the design doc).
SUFFIX = (
    ", vertical 9:16 full-frame composition, cinematic documentary still, dramatic moody "
    "lighting, deep navy-and-black palette with electric-blue and gold accents, photorealistic, "
    "ultra-detailed, shallow depth of field. No on-screen text, no watermark, no logo, "
    "no identifiable real person."
)

NEG = (
    "on-screen text, caption, subtitle, letters, words, numbers, typography, watermark, logo, "
    "signature, identifiable real person, recognizable face, celebrity, portrait, close-up face, "
    "deformed, distorted, extra fingers, bad hands, lowres, blurry, jpeg artifacts, "
    "oversaturated, cartoon, illustration, 3d render"
)

# (filename stem, prompt core) — from SHORTS_EP1-8.md SHORT #6 (Terry).
# _02 and _03 are reworded to express the concept WITHOUT literal quoted words, so SDXL
# does not render text (keeps the §0 "no on-screen text" invariant); meaning is unchanged.
SHOTS = [
    ("short06_01", "A police officer's silhouette stopping a lone figure on a rain-slicked night "
                   "street for a pat-down, hands raised against a wall, tense, no faces"),
    ("short06_02", "An empty document frame where an arrest warrant should be, a conceptual absence, "
                   "a faint glowing outline of nothing, symbolic of 'no warrant needed'"),
    ("short06_03", "A glowing analog gauge needle resting midway between a faint vague guess and "
                   "solid hard proof, the threshold of reasonable suspicion, electric-blue dial"),
    ("short06_04", "Two shadowy figures pacing back and forth before a darkened storefront at night, "
                   "casing it, repeated motion, no faces"),
    ("short06_05", "A watchful detective observing a dark city street at night from the shadows, "
                   "intent gaze, no identifiable face, silhouette and reflections"),
    ("short06_06", "The outline of a concealed handgun revealed beneath a heavy coat, dramatic edge "
                   "lighting, ominous, no face"),
    ("short06_07", "A lower second boundary line drawn faintly across a night street below a higher "
                   "line, a weaker legal standard, conceptual, navy and gold"),
    ("short06_thumb", "A lone night-street stop-and-frisk silhouette under a cold streetlight, an "
                      "officer and a figure against a wall, ominous cinematic key visual, no faces"),
]


def post(path: str, payload: dict) -> dict:
    req = urllib.request.Request(
        API + path,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=1200) as r:
        return json.load(r)


def gen(stem: str, core: str, force: bool, hr_scale: float, upscaler: str) -> None:
    out_path = os.path.join(OUT, stem + ".png")
    if os.path.exists(out_path) and not force:
        print(f"[skip] {stem} exists", flush=True)
        return
    # Deterministic per-shot seed so reruns reproduce; varies by stem.
    seed = 60000 + int(stem.split("_")[1].replace("thumb", "99"))
    payload = {
        "prompt": core + SUFFIX,
        "negative_prompt": NEG,
        "width": 832,
        "height": 1472,                 # 9:16-ish, /8-safe (832/1472 = 0.565)
        "steps": 60,                    # max-quality base pass
        "cfg_scale": 6.5,
        "sampler_name": "DPM++ 2M SDE",
        "scheduler": "Karras",
        "seed": seed,
        "enable_hr": True,
        "hr_scale": hr_scale,           # default 2.4 -> ~1997x3533 (4K-class vertical)
        "hr_upscaler": upscaler,        # DAT x4 = highest-quality photoreal upscaler available
        "denoising_strength": 0.35,
        "hr_second_pass_steps": 25,
        "override_settings": {
            "sd_model_checkpoint": MODEL,
            "CLIP_stop_at_last_layers": 2,
        },
        "override_settings_restore_afterwards": False,
    }
    t0 = time.time()
    w = int(round(832 * hr_scale))
    h = int(round(1472 * hr_scale))
    print(f"[gen ] {stem} -> {w}x{h} ({upscaler}) ...", flush=True)
    res = post("/sdapi/v1/txt2img", payload)
    img_b64 = res["images"][0]
    tmp = out_path + ".part"
    with open(tmp, "wb") as f:
        f.write(base64.b64decode(img_b64.split(",", 1)[-1]))
    os.replace(tmp, out_path)           # atomic
    print(f"[done] {stem} -> {out_path}  ({time.time()-t0:.0f}s)", flush=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true", help="regenerate even if file exists")
    ap.add_argument("--only", help="comma list of stems (e.g. short06_03,short06_thumb)")
    ap.add_argument("--hr-scale", type=float, default=2.4,
                    help="hires-fix scale (2.4=~4K; lower to 2.0 if VRAM-bound)")
    ap.add_argument("--upscaler", default="DAT x4",
                    help="hires upscaler (DAT x4 best; R-ESRGAN 4x+ as fallback)")
    args = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    only = set(args.only.split(",")) if args.only else None
    failed = []
    for stem, core in SHOTS:
        if only and stem not in only:
            continue
        try:
            gen(stem, core, args.force, args.hr_scale, args.upscaler)
        except Exception as e:  # keep going; report per-shot
            print(f"[FAIL] {stem}: {e}", file=sys.stderr, flush=True)
            failed.append(stem)
    print(f"[all ] short06 image generation finished; failed={failed or 'none'}", flush=True)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
