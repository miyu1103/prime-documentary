from __future__ import annotations

import argparse
import base64
import json
import os
from pathlib import Path

import requests

from sdxl_quality_profiles import available_sdxl_profiles, get_sdxl_profile


PROMPTS = [
    "documentary photo, a small wet stray tabby kitten sitting alone on rain-soaked neon-lit city pavement at night, puddle reflections, shallow depth of field, 35mm, muted natural colors, melancholic, photoreal, film still",
    "documentary photo, a small wet tabby kitten looking up, rain falling through warm streetlight, blurred neon bokeh, night, shallow depth of field, natural muted colors, photoreal, film still",
    "extreme close up documentary photo, face of a small wet tabby kitten, big reflective eyes, raindrops on fur, warm streetlight, night, shallow depth of field, photoreal, film still",
    "documentary photo, a warm glowing open doorway spilling golden light onto wet pavement on a rainy night, cozy inviting, blurred rain, natural muted colors, photoreal, film still",
    "documentary photo, a small wet tabby kitten walking toward a warm glowing doorway on a rainy night street, seen from behind, golden light, wet reflections, photoreal, film still",
    "documentary photo, a small tabby kitten curled up sleeping on a warm windowsill blanket, soft lamp light, rain streaks on the window behind, cozy peaceful, natural warm colors, photoreal, film still",
]

NEG = (
    "cgi, 3d render, illustration, painting, cartoon, anime, oversaturated, hdr, "
    "vibrant, fantasy, watermark, text, deformed, extra limbs, fused, mutated, plastic, oversharpened"
)

API = "http://127.0.0.1:7860"
OUT = Path(r"C:\Users\aab15\Documents\prime-documentary\_sdxl_test\cat_story")
OUT.mkdir(parents=True, exist_ok=True)


def request_body(prompt: str, seed: int, profile: dict[str, object]) -> dict[str, object]:
    return {
        "prompt": prompt,
        "negative_prompt": NEG,
        "steps": int(profile["steps"]),
        "cfg_scale": float(profile["cfg_scale"]),
        "width": int(profile["width"]),
        "height": int(profile["height"]),
        "sampler_name": str(profile["sampler_name"]),
        "scheduler": str(profile["scheduler"]),
        "seed": int(seed),
        "batch_size": 1,
        "n_iter": 1,
        "save_images": False,
        "override_settings": {"sd_model_checkpoint": str(profile["model"])},
        "override_settings_restore_afterwards": True,
    }


def set_model(profile: dict[str, object]) -> None:
    opts = requests.get(f"{API}/sdapi/v1/options", timeout=20)
    opts.raise_for_status()
    current = str(opts.json().get("sd_model_checkpoint", ""))
    model = str(profile["model"])
    if model not in current:
        patch = requests.post(f"{API}/sdapi/v1/options", json={"sd_model_checkpoint": model}, timeout=120)
        patch.raise_for_status()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--offset", type=int, default=0)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument(
        "--profile",
        default=os.getenv("SDXL_PROFILE", "max"),
        choices=available_sdxl_profiles(),
        help="Quality preset. max=highest quality output.",
    )
    args = ap.parse_args()
    profile = get_sdxl_profile(args.profile)

    prompts = PROMPTS[args.offset :]
    if args.limit:
        prompts = prompts[: args.limit]

    if not args.dry_run:
        set_model(profile)

    for idx, p in enumerate(prompts, start=args.offset):
        body = request_body(p, idx + 1000, profile)
        if args.dry_run:
            print(f"[{idx+1}/{len(PROMPTS)}] dry_run {profile['name']} -> shot{idx}.png")
            continue
        response = requests.post(f"{API}/sdapi/v1/txt2img", json=body, timeout=360)
        response.raise_for_status()
        data = response.json()
        with open(OUT / f"shot{idx}.png", "wb") as f:
            f.write(base64.b64decode(data["images"][0]))
        print(f"shot{idx} OK [{profile['name']}]", flush=True)

    manifest = {
        "quality_profile": str(profile["name"]),
        "count": len(prompts),
        "offset": args.offset,
        "limit": args.limit,
        "output_dir": str(OUT),
        "seed_base": 1000,
    }
    (OUT / "cat_story_manifest.v001.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print("ALL DONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
