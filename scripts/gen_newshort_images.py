#!/usr/bin/env python
"""Generate the NEW SDXL stills for the new-shorts batch (short38 williams x7, short39 florence x1).

Modeled on scripts/gen_short35_images.py. Prompts are pulled VERBATIM from
runs/new_shorts/plan.v001.json image_prompts (they already carry the full style suffix), so the
R2/no-face wording locks are preserved exactly. Juggernaut XL (currently loaded checkpoint).
Writes remotion/public/shorts/short<NN>/short<NN>_<n>.png (what the render reads).
--variants 1 (single high-precision image per slot, no variant spam). Idempotent unless --force.

Usage: gen_newshort_images.py --short 38   |   --short 39 --only short39_01
"""
import argparse, base64, json, os, sys, time, urllib.request
from pathlib import Path

API = "http://127.0.0.1:7860"
ROOT = Path(__file__).resolve().parents[1]
PLAN = json.loads((ROOT / "runs/new_shorts/plan.v001.json").read_text("utf-8"))

NEG = (
    "on-screen text, caption, subtitle, letters, words, numerals, typography, watermark, logo, signature, brand, "
    "identifiable real person, recognizable face, celebrity, portrait, close-up face, visible facial features, "
    "government seal, mugshot, "
    "deformed, distorted, extra fingers, bad hands, lowres, blurry, jpeg artifacts, oversaturated, cartoon"
)


def prompts_for(short_id: str) -> dict:
    for s in PLAN["shorts"]:
        if s["short_id"] == short_id:
            return s.get("image_prompts", {})
    raise SystemExit(f"no such short {short_id} in plan")


def post(path, payload):
    req = urllib.request.Request(API + path, data=json.dumps(payload).encode("utf-8"),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as r:
        return json.load(r)


def gen(out_dir: Path, stem: str, prompt: str, force: bool, no_hr: bool):
    out_path = out_dir / f"{stem}.png"
    if out_path.exists() and not force:
        print(f"[skip] {stem} exists", flush=True)
        return
    seed = 380000 + int("".join(ch for ch in stem if ch.isdigit())[-4:])
    payload = {
        "prompt": prompt, "negative_prompt": NEG,
        "width": 832, "height": 1472, "steps": 34, "cfg_scale": 6,
        "sampler_name": "DPM++ 2M Karras", "seed": seed,
        "enable_hr": True, "hr_scale": 1.5, "hr_upscaler": "R-ESRGAN 4x+",
        "denoising_strength": 0.35, "hr_second_pass_steps": 12,
    }
    if no_hr:
        payload.update({"width": 1088, "height": 1920, "enable_hr": False})
        for k in ("hr_scale", "hr_upscaler", "denoising_strength", "hr_second_pass_steps"):
            payload.pop(k, None)
    t0 = time.time()
    print(f"[gen ] {stem} (seed {seed}) ...", flush=True)
    res = post("/sdapi/v1/txt2img", payload)
    out_path.write_bytes(base64.b64decode(res["images"][0].split(",", 1)[-1]))
    print(f"[done] {stem} -> {out_path}  ({time.time()-t0:.0f}s)", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--short", required=True, help="38 or 39")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--only")
    ap.add_argument("--no-hr", action="store_true")
    args = ap.parse_args()
    short_id = f"short{args.short}"
    prompts = prompts_for(short_id)
    out_dir = ROOT / "remotion" / "public" / "shorts" / short_id
    out_dir.mkdir(parents=True, exist_ok=True)
    only = set(args.only.split(",")) if args.only else None
    for stem in sorted(prompts):
        if only and stem not in only:
            continue
        try:
            gen(out_dir, stem, prompts[stem], args.force, args.no_hr)
        except Exception as e:
            print(f"[FAIL] {stem}: {e}", file=sys.stderr, flush=True)
    print(f"[all ] {short_id} NEW image generation finished", flush=True)


if __name__ == "__main__":
    main()
