#!/usr/bin/env python3
"""Generate stronger Riley v003 cinematic stills via local A1111 SDXL.

Codex-controlled local generation. No upload, no publish.
Outputs go to E:/pd-media and are later copied into remotion/public/riley.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-007-riley"
MEDIA = Path(json.loads((ROOT / "config/storage.local.json").read_text("utf-8"))["roots"]["media"]["path"])
OUT = MEDIA / "episodes" / EP / "05_visuals" / "codex_beauty_v003"
API = "http://127.0.0.1:7860/sdapi/v1/txt2img"

STYLE = (
    "premium cinematic documentary key visual, physically plausible editorial photography, "
    "legal-tech noir, deep black shadows, navy atmosphere, electric-blue practical light, restrained warm gold accent, "
    "silver highlights, tactile material detail, elegant negative space, shallow depth of field, 35mm film grain, "
    "high production value, strong subject hierarchy, mature serious tone, no cheap stock-photo look"
)
NEG = (
    "readable text, fake letters, logo, brand logo, watermark, user interface text, app logo, official seal, badge text, "
    "license plate, real address, identifiable face, public figure likeness, David Riley likeness, Brima Wurie likeness, "
    "judge portrait, police brutality, gore, weapon pointed at viewer, gang sign, sensational imagery, cartoon, anime, "
    "plastic CGI, low detail, blurry, overprocessed HDR, cyberpunk clutter, neon overload, bad anatomy, deformed hands, "
    "extra fingers, warped phone, melted phone, duplicate phone, crooked screen, messy composition"
)

PROMPTS = [
    {
        "id": "RILEY_V3_HOOK_PHONE",
        "scene": "S001",
        "file": "riley_v003_hook_phone.png",
        "prompt": (
            "extreme macro close-up, a modern black smartphone half pulled from a dark coat pocket on a wet roadside at night, "
            "only anonymous hands cropped at the wrist, phone screen black, blue police-light reflection across glass, "
            "fabric texture sharp, no face, no badge, no weapon, composition leaves dark negative space on left"
        ),
    },
    {
        "id": "RILEY_V3_PHONE_LIFE",
        "scene": "S002",
        "file": "riley_v003_phone_life.png",
        "prompt": (
            "generic smartphone upright on black glass, the phone opens into translucent layers of private life, "
            "abstract photo tiles without faces, unreadable message blocks, calendar shapes, map dots, cloud panes, "
            "elegant layered depth, no real app icons, no readable UI, central object with negative space"
        ),
    },
    {
        "id": "RILEY_V3_ROADSIDE_CASE",
        "scene": "S003",
        "file": "riley_v003_roadside_case.png",
        "prompt": (
            "anonymous Southern California roadside stop at night, cropped car door, rain-slick asphalt, blue police light bokeh, "
            "a generic phone and keys on the hood edge, no people visible, no readable plate or sign, tense but restrained"
        ),
    },
    {
        "id": "RILEY_V3_WARRANT_PHONE",
        "scene": "S017",
        "file": "riley_v003_warrant_phone.png",
        "prompt": (
            "locked generic smartphone on a dark evidence table inside an anonymous courthouse interior, "
            "gold beam of light like a warrant path falls onto the phone, marble columns blurred in background, "
            "solemn authoritative mood, no real seal, no readable document, no people"
        ),
    },
    {
        "id": "RILEY_V3_PRIVACY_MOSAIC",
        "scene": "S022",
        "file": "riley_v003_privacy_mosaic.png",
        "prompt": (
            "anonymous human silhouette made from floating private phone data fragments, unreadable messages, blurred photos without faces, "
            "map dots, health symbol shapes, calendar blocks, all emerging from a locked phone, intimate and beautiful, no logos"
        ),
    },
    {
        "id": "RILEY_V3_LOCATION_TRAIL",
        "scene": "S027",
        "file": "riley_v003_location_trail.png",
        "prompt": (
            "generic smartphone in lower left on a dark glass map surface, a thin electric-blue trail of location points arcs into the distance "
            "toward anonymous cell towers and a cloud shape, no real place names, quiet ominous cliffhanger, clean negative space"
        ),
    },
]


def post(payload: dict) -> dict:
    req = urllib.request.Request(API, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=900) as r:
        return json.loads(r.read().decode("utf-8"))


def save(b64: str, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(base64.b64decode(b64))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidates", type=int, default=2)
    parser.add_argument("--base-seed", type=int, default=930000)
    parser.add_argument("--ids", nargs="*")
    args = parser.parse_args()
    wanted = set(args.ids or [])

    OUT.mkdir(parents=True, exist_ok=True)
    manifest = {
        "episode_id": EP,
        "set": "codex_beauty_v003",
        "generator": "codex-controlled-local-a1111-sdxl",
        "style": STYLE,
        "negative_prompt": NEG,
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "items": [],
    }
    n = 0
    for item in PROMPTS:
        if wanted and item["id"] not in wanted:
            continue
        for c in range(args.candidates):
            n += 1
            seed = args.base_seed + n * 211
            prompt = f"{item['prompt']}, {STYLE}"
            payload = {
                "prompt": prompt,
                "negative_prompt": NEG,
                "seed": seed,
                "subseed": seed + 1009,
                "subseed_strength": 0.05,
                "sampler_name": "DPM++ 2M Karras",
                "scheduler": "Karras",
                "steps": 48,
                "cfg_scale": 4.2,
                "width": 1536,
                "height": 864,
                "batch_size": 1,
                "n_iter": 1,
                "enable_hr": True,
                "hr_resize_x": 2304,
                "hr_resize_y": 1296,
                "hr_second_pass_steps": 20,
                "denoising_strength": 0.18,
                "hr_upscaler": "Latent",
                "restore_faces": False,
                "do_not_save_samples": True,
                "do_not_save_grid": True,
            }
            result = post(payload)
            out = OUT / item["scene"] / f"{Path(item['file']).stem}_c{c+1:02d}_seed{seed}.png"
            save(result["images"][0], out)
            meta = {
                "asset_id": f"{EP}-{item['scene']}-CODEX-BEAUTY-{c+1:03d}",
                "item_id": item["id"],
                "scene": item["scene"],
                "candidate": c + 1,
                "seed": seed,
                "file": str(out),
                "sha256": "sha256:" + sha256(out),
                "prompt": prompt,
                "negative_prompt": NEG,
                "status": "candidate",
                "ai_disclosure_required": True,
                "symbolic_reconstruction": True,
            }
            out.with_suffix(".json").write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            manifest["items"].append(meta)
            print(f"[{n:02d}] {out}", flush=True)
    manifest["finished_at"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    manifest["count"] = len(manifest["items"])
    (OUT / "asset_manifest.v001.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"done count={len(manifest['items'])} out={OUT}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
