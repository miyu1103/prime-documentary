#!/usr/bin/env python3
"""Generate premium local SDXL backdrops for EP8 Carpenter motion cut v006.

Local A1111 only. No upload. Outputs go to H:/pd-media and are registered
later in the episode rights manifest.
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
OUT = MEDIA / "episodes" / EP / "05_visuals" / "sdxl_motion_v006"
API = "http://127.0.0.1:7860/sdapi/v1/txt2img"

STYLE = (
    "breathtaking premium documentary key art, museum-quality cinematic still, legal-tech privacy thriller, "
    "deep black and navy palette, electric-blue data light, restrained gold accents, glossy glass, rich atmospheric depth, "
    "volumetric haze, sophisticated editorial lighting, high contrast, no text, no logos, no people, no faces, "
    "symbolic reconstruction, elegant composition, expensive poster finish, realistic but painterly, not cartoon"
)

NEG = (
    "readable text, letters, numbers, UI text, app icons, logos, watermark, signature, map labels, city names, "
    "person, face, hand, police badge, gavel, court seal, real landmark, gore, gun, sensational crime scene, "
    "cheap cyberpunk, cluttered interface, cartoon, anime, flat vector, plastic CGI, warped phone, low detail, blurry"
)

PROMPTS = [
    ("hook_phone_map", "floating generic black-glass smartphone over a dark aerial city map, gold location trail and blue data points, left side clean dark negative space, no text, " + STYLE),
    ("ordinary_phone_desk", "generic unbranded smartphone on a dark polished desk, blue location trail reflected in glass, subtle keys and wallet shapes out of focus, ordinary private life made ominous, no text, " + STYLE),
    ("detroit_store_symbolic", "generic closed electronics storefront at night in rain, wet pavement reflecting blue and gold light, no signage, no readable labels, no people, serious factual crime-case atmosphere, " + STYLE),
    ("cell_tower_city", "abstract cell towers as glowing points over a vast night city grid, overlapping blue coverage circles and one restrained gold route, no labels, no real map, " + STYLE),
    ("blank_order_phone", "blank court-order-like paper shape beside a generic phone on black stone table, redaction bars as pure abstract blocks with no text, blue rim light and gold edge glow, " + STYLE),
    ("doctrine_split", "split visual metaphor: thin paper strip on one side and deep luminous location map on the other, black void between them, no text, no numbers, elegant legal contrast, " + STYLE),
    ("supreme_columns_abstract", "abstract columned courthouse silhouette at night, no official seal, deep blue sky, gold light on stone, floating phone-location data particles in foreground, no text, " + STYLE),
    ("data_doors_corridor", "dark minimalist corridor of unmarked doors, first door cracked open with electric-blue data light spilling out and gold dust, no labels, no people, cinematic privacy metaphor, " + STYLE),
    ("viewer_device_final", "generic smartphone lying face-up in darkness, its black glass reflecting a gold location path and blue city points, intimate final-frame viewer device, no brand, no text, " + STYLE),
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
        "set": "sdxl_motion_v006",
        "generator": "local-a1111-sdxl",
        "ai_disclosure_required": True,
        "rights_status": "candidate_requires_qc",
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "items": [],
    }
    for idx, (stem, prompt) in enumerate(PROMPTS, start=1):
        seed = 948000 + idx * 991
        out = OUT / f"carpenter_{stem}_v006_seed{seed}.png"
        if out.exists() and out.stat().st_size > 1024:
            print(f"skip {out}")
        else:
            payload = {
                "prompt": prompt,
                "negative_prompt": NEG,
                "seed": seed,
                "subseed": seed + 307,
                "subseed_strength": 0.12,
                "sampler_name": "DPM++ 2M Karras",
                "scheduler": "Karras",
                "steps": 52,
                "cfg_scale": 5.0,
                "width": 1536,
                "height": 864,
                "batch_size": 1,
                "n_iter": 1,
                "enable_hr": True,
                "hr_resize_x": 2304,
                "hr_resize_y": 1296,
                "hr_second_pass_steps": 24,
                "denoising_strength": 0.21,
                "hr_upscaler": "Latent",
                "restore_faces": False,
                "do_not_save_samples": True,
                "do_not_save_grid": True,
            }
            result = post(payload)
            out.write_bytes(base64.b64decode(result["images"][0]))
            print(out)
        meta = {
            "asset_id": f"{EP}-MOTION-V006-{idx:03d}",
            "item_id": stem,
            "section": "motion_backdrop",
            "candidate": idx,
            "seed": seed,
            "path": str(out),
            "prompt_sha256": sha_text(prompt),
            "prompt": prompt,
            "negative_prompt": NEG,
            "model_profile": "local-a1111-sdxl-motion-v006",
            "status": "candidate",
            "ai_disclosure_required": True,
            "rights_origin": "AI-generated local SDXL symbolic reconstruction",
        }
        out.with_suffix(".json").write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n", "utf-8")
        manifest["items"].append(meta)
    manifest["finished_at"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    manifest["count"] = len(manifest["items"])
    (OUT / "asset_manifest.v006.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", "utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
