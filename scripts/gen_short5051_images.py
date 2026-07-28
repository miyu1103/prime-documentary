#!/usr/bin/env python
"""Generate the NEW SDXL stills for short50 (EP48 glover) and short51 (EP49 strieff).

Self-contained clone of scripts/gen_short4647_images.py (identical SDXL params / NEG / seed scheme /
output path), prompts embedded here. Symbols only, no faces (R2), no readable text, no seal.
Writes remotion/public/shorts/short<NN>/short<NN>_<n>.png. Idempotent unless --force.

Usage: gen_short5051_images.py --short 50   |   --short 51 --only short51_01
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
    # short50 — Kansas v. Glover (lane accent patrol-blue; symbols only, no face, traffic-stop/plate)
    "short50_01": "A two-lane rural Kansas highway at the edge of town seen from inside a parked patrol car, a pickup truck receding down the empty road ahead through the windshield, a glowing dashboard-mounted laptop out of focus in the foreground, flat overcast afternoon light, faint patrol-blue signal glow; generous empty area in the upper third for a headline. " + STYLE,
    "short50_02": "Close on a rugged laptop bolted to a police dashboard, its screen a cold abstract blue glow with an out-of-focus data readout and no readable characters, a hint of a paused red status block, dark cab interior, shallow focus, tense and clinical, no hands, no people. " + STYLE,
    "short50_03": "The interior of a pickup-truck cab from behind, a driver reduced to a featureless dark silhouette against the bright windshield, hands only suggested on the steering wheel, no visible face, cold documentary light, faint blue rim, anonymous and quiet. " + STYLE,
    "short50_04": "A police cruiser light bar flicking on at dusk on an empty two-lane road, hard blue and red strobe flare cutting across wet asphalt, deep shadow, dramatic and cinematic, no people, no readable markings. " + STYLE,
    "short50_05": "The marble columns and stone steps of the United States Supreme Court building at dusk, low angle, deep shadow between fluted columns, restrained muted-gold rim light, monumental and quiet, no people, no seal. " + STYLE,
    "short50_06": "An empty two-lane Kansas road at golden hour receding to a flat horizon under a wide prairie sky, a lone roadside utility pole, warm resolved light, calm and still, no people, no vehicles. " + STYLE,
    # short51 — Utah v. Strieff (lane accent plum; symbols only, no face, drugs minimal, attenuation motif)
    "short51_01": "A man seen only from behind as a dark silhouette walking across an empty asphalt parking lot toward a car at dusk, an unmarked detective's sedan across the lot in soft focus, long shadows, a faint plum-violet signal glow, cinematic surveillance mood, no visible face; generous empty area in the upper third for a headline. " + STYLE,
    "short51_02": "A close symbolic shot of a plain plastic identification card held at the edge of frame beside a handheld police radio on a dark surface, a cold abstract database glow with an out-of-focus flag indicator and no readable characters, plum-violet signal light, clinical and tense, no faces. " + STYLE,
    "short51_03": "A heavy iron chain stretched taut across a dark surface with one single thinned, nearly-broken corroded link catching a raking plum-violet light, macro shallow focus, tense symbolic metaphor of a weakened connection, no people, no text. " + STYLE,
    "short51_04": "A pair of cold steel handcuffs lying open on a dark reflective surface under a hard raking light, one cuff slightly ajar, chrome catching a faint plum-violet signal, shallow focus, tense and clinical, no hands, no people. " + STYLE,
    "short51_05": "The marble columns and stone steps of the United States Supreme Court building at dusk, low angle, deep shadow between fluted columns, restrained muted-gold rim light, monumental and quiet, no people, no seal. " + STYLE,
    "short51_06": "An empty asphalt parking lot at golden hour beside a plain doorway propped open into darkness, long warm light raking across the ground, calm resolved and still, no people, no faces, no text. " + STYLE,
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
    seed = 500000 + int("".join(ch for ch in stem if ch.isdigit())[-4:])
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
    ap.add_argument("--short", required=True, help="50 or 51")
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
