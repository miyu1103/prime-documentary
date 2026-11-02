#!/usr/bin/env python
"""Generate the NEW SDXL stills for short48 (EP46 tlo) and short49 (EP47 atwater).

Self-contained clone of scripts/gen_newshort_images.py (identical SDXL params / NEG / seed scheme /
output path), but prompts are embedded here instead of runs/new_shorts/plan.v001.json so this batch
does not touch the shared plan file another agent is editing. Symbols only, no faces (R2), no minor,
no readable text. Writes remotion/public/shorts/short<NN>/short<NN>_<n>.png. Idempotent unless --force.

Usage: gen_short4647_images.py --short 48   |   --short 49 --only short49_01
"""
import argparse, base64, json, sys, time, urllib.request
from pathlib import Path

API = "http://127.0.0.1:7860"
ROOT = Path(__file__).resolve().parents[1]

STYLE = ("museum-grade cinematic symbolic documentary still, vertical 9:16 full-frame, black and "
         "deep-navy base, electric-blue signal light, silver highlights, restrained muted-gold accent, "
         "film grain, dramatic moody lighting, photorealistic, shallow depth of field, symbolic "
         "reconstruction not authentic footage. No on-screen text, no watermark, no logo, no "
         "identifiable real person, no readable letters or numerals, no government seal.")

NEG = (
    "on-screen text, caption, subtitle, letters, words, numerals, typography, watermark, logo, signature, brand, "
    "identifiable real person, recognizable face, celebrity, portrait, close-up face, visible facial features, child, "
    "minor, teenager, government seal, mugshot, "
    "deformed, distorted, extra fingers, bad hands, lowres, blurry, jpeg artifacts, oversaturated, cartoon"
)

PROMPTS = {
    # short48 — New Jersey v. T.L.O. (lane accent green; symbols only, no minor, drugs clinical/minimal)
    "short48_01": "A worn canvas school purse tipped over on a scuffed wooden administrator's desk under a hard desk lamp, a manila folder and the bare metal edge of a chair, cold institutional morning light, a faint restrained green signal glow; generous empty area in the upper third for a headline. " + STYLE,
    "short48_02": "A long empty high-school corridor lined with rows of steel lockers, a closed restroom door slightly ajar at the far end, a thin haze of light, polished floor reflecting cold overhead fluorescents, nobody present. " + STYLE,
    "short48_03": "Close on a wooden administrator's desk, a zippered canvas bag partly open beside a small folded index card and an empty plastic sleeve, a soft shadow falling across the surface, clinical restrained and minimal, muted tones, no hands. " + STYLE,
    "short48_04": "A wrought-iron schoolyard gate and a brick public-school facade at blue hour, a bare flagpole, the threshold between an empty street and the campus, cold documentary light, faint green rim, no people. " + STYLE,
    "short48_05": "The marble columns and stone steps of the United States Supreme Court building at dusk, low angle, deep shadow between fluted columns, restrained muted-gold rim light, monumental and quiet, no people, no seal. " + STYLE,
    "short48_06": "An empty classroom at golden hour, a single backpack resting on a wooden desk beside a window, soft warm light settling across empty rows, calm and resolved, no people. " + STYLE,
    # short49 — Atwater v. Lago Vista (lane accent violet; symbols only, no faces, children non-sensational)
    "short49_01": "A two-lane Texas farm road in flat afternoon light seen through a pickup-truck windshield, a loose unbuckled seatbelt hanging slack across the foreground of the cab, a dusty dashboard, open sky and an empty road ahead, faint violet-blue signal; empty space in the upper third for a headline. " + STYLE,
    "short49_02": "A pair of cold steel handcuffs lying open on a dark surface under a hard raking light, one cuff slightly ajar, chrome catching a faint violet-blue signal, shallow focus, tense and clinical, no hands, no people. " + STYLE,
    "short49_03": "A cold empty holding cell and a heavy institutional steel door with a small reinforced window, harsh green-white overhead light, a bare bench and the edge of a booking counter, no people, no signage. " + STYLE,
    "short49_04": "The interior of a pickup-truck cab with two empty child booster seats on the front bench, belts unfastened, soft afternoon light through the side windows, quiet and non-sensational, no people, no faces. " + STYLE,
    "short49_05": "The marble columns and stone steps of the United States Supreme Court building at dusk, low angle, deep shadow between fluted columns, restrained muted-gold rim light, monumental and quiet, no people, no seal. " + STYLE,
    "short49_06": "An empty two-lane Texas road at golden hour receding to the horizon beside a closed leather-bound law book resting on a wooden fence post, warm resolved light, calm and still, no people. " + STYLE,
}


def post(path, payload):
    req = urllib.request.Request(API + path, data=json.dumps(payload).encode("utf-8"),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as r:
        return json.load(r)


def gen(out_dir: Path, stem: str, prompt: str, force: bool):
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
    t0 = time.time()
    print(f"[gen ] {stem} (seed {seed}) ...", flush=True)
    res = post("/sdapi/v1/txt2img", payload)
    out_path.write_bytes(base64.b64decode(res["images"][0].split(",", 1)[-1]))
    print(f"[done] {stem} -> {out_path}  ({time.time()-t0:.0f}s)", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--short", required=True, help="48 or 49")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--only")
    args = ap.parse_args()
    short_id = f"short{args.short}"
    prompts = {k: v for k, v in PROMPTS.items() if k.startswith(short_id + "_")}
    if not prompts:
        raise SystemExit(f"no prompts for {short_id}")
    out_dir = ROOT / "remotion" / "public" / "shorts" / short_id
    out_dir.mkdir(parents=True, exist_ok=True)
    only = set(args.only.split(",")) if args.only else None
    for stem in sorted(prompts):
        if only and stem not in only:
            continue
        try:
            gen(out_dir, stem, prompts[stem], args.force)
        except Exception as e:
            print(f"[FAIL] {stem}: {e}", file=sys.stderr, flush=True)
    print(f"[all ] {short_id} NEW image generation finished", flush=True)


if __name__ == "__main__":
    main()
