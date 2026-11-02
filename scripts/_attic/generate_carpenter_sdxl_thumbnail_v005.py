#!/usr/bin/env python3
"""Generate EP8 Carpenter premium SDXL thumbnail backgrounds.

Local A1111 only. No paid API, no upload.
"""
from __future__ import annotations

import base64
import hashlib
import json
import time
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-008-carpenter"
MEDIA = Path(json.loads((ROOT / "config/storage.local.json").read_text("utf-8"))["roots"]["media"]["path"])
OUT = MEDIA / "episodes" / EP / "05_visuals" / "sdxl_thumbnail_v005"
API = "http://127.0.0.1:7860/sdapi/v1/txt2img"

STYLE = (
    "breathtaking museum-quality cinematic documentary key art, premium legal-tech privacy thriller, "
    "expensive editorial poster finish, deep black and navy, electric-blue data glow, restrained gold location trail, "
    "glossy black glass smartphone, abstract aerial city map at night, rich atmospheric depth, volumetric light, "
    "elegant negative space on the left for typography, dramatic but sober, advertiser-safe, ultra detailed, "
    "photoreal with painterly polish, refined texture, high contrast thumbnail readability"
)

NEG = (
    "text, letters, numbers, UI text, app icons, logos, watermark, signature, readable map labels, city names, "
    "people, face, hand, police badge, gavel, court seal, gun, gore, real landmark, cheap cyberpunk neon, "
    "cluttered interface, cartoon, anime, flat vector, plastic CGI, ugly stock photo, warped phone, deformed phone, "
    "low detail, blurry, jpeg artifacts, overprocessed HDR"
)

PROMPTS = [
    (
        "carpenter_codex_style_phone_map_v005_a",
        "A generic unbranded black-glass smartphone floating on the right over a dark aerial city grid; "
        "a graceful gold location trail emerges from the phone and blooms across the map, with thousands of subtle blue data points; "
        "left half is clean dark negative space, no text anywhere. "
        + STYLE,
    ),
    (
        "carpenter_codex_style_phone_map_v005_b",
        "A vast deep-navy city-at-night map dissolving into a constellation of electric-blue cell-site points; "
        "a premium generic smartphone on the right edge reflects the map in its glass, with a single elegant gold path crossing toward it; "
        "left side nearly black, polished documentary poster composition, no text anywhere. "
        + STYLE,
    ),
    (
        "carpenter_codex_style_phone_map_v005_c",
        "A close cinematic hero view of a generic smartphone tilted over an abstract blue city grid, "
        "gold location pings curve through the glass and out into the background like a luminous ribbon; "
        "large empty dark title area on left, sophisticated legal privacy mood, no text anywhere. "
        + STYLE,
    ),
]


def sha_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def post(payload: dict) -> dict:
    req = urllib.request.Request(API, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=900) as r:
        return json.loads(r.read().decode("utf-8"))


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = {
        "episode_id": EP,
        "set": "sdxl_thumbnail_v005",
        "generator": "local-a1111-sdxl",
        "ai_disclosure_required": True,
        "rights_status": "candidate_requires_qc",
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "items": [],
    }
    for idx, (stem, prompt) in enumerate(PROMPTS, start=1):
        seed = 931000 + idx * 1009
        out = OUT / f"{stem}_seed{seed}.png"
        payload = {
            "prompt": prompt,
            "negative_prompt": NEG,
            "seed": seed,
            "subseed": seed + 221,
            "subseed_strength": 0.12,
            "sampler_name": "DPM++ 2M Karras",
            "scheduler": "Karras",
            "steps": 56,
            "cfg_scale": 5.2,
            "width": 1536,
            "height": 864,
            "batch_size": 1,
            "n_iter": 1,
            "enable_hr": True,
            "hr_resize_x": 2304,
            "hr_resize_y": 1296,
            "hr_second_pass_steps": 26,
            "denoising_strength": 0.20,
            "hr_upscaler": "Latent",
            "restore_faces": False,
            "do_not_save_samples": True,
            "do_not_save_grid": True,
        }
        result = post(payload)
        out.write_bytes(base64.b64decode(result["images"][0]))
        meta = {
            "asset_id": f"{EP}-THUMB-V005-{idx:03d}",
            "item_id": stem,
            "section": "thumbnail",
            "candidate": idx,
            "seed": seed,
            "path": str(out),
            "prompt_sha256": sha_text(prompt),
            "prompt": prompt,
            "negative_prompt": NEG,
            "model_profile": "local-a1111-sdxl-thumbnail-v005",
            "status": "candidate",
            "ai_disclosure_required": True,
            "rights_origin": "AI-generated local SDXL symbolic reconstruction",
        }
        out.with_suffix(".json").write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n", "utf-8")
        manifest["items"].append(meta)
        print(out)
    manifest["finished_at"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    manifest["count"] = len(manifest["items"])
    (OUT / "asset_manifest.v005.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", "utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
