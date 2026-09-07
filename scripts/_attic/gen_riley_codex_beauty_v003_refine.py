#!/usr/bin/env python3
"""Regenerate only the weak Riley v003 visual candidates.

Local A1111 SDXL generation. No upload or publish side effects.
"""
from __future__ import annotations

import base64
import hashlib
import json
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-007-riley"
MEDIA = Path(json.loads((ROOT / "config/storage.local.json").read_text("utf-8"))["roots"]["media"]["path"])
OUT = MEDIA / "episodes" / EP / "05_visuals" / "codex_beauty_v003_refine"
API = "http://127.0.0.1:7860/sdapi/v1/txt2img"

STYLE = (
    "premium cinematic documentary key visual, physically plausible editorial photography, legal-tech noir, "
    "deep black shadows, navy atmosphere, electric-blue practical light, restrained warm gold accent, "
    "silver highlights, tactile material detail, elegant negative space, shallow depth of field, 35mm film grain, "
    "high production value, strong subject hierarchy, mature serious tone, no cheap stock-photo look"
)
NEG = (
    "readable text, fake letters, logo, brand logo, watermark, user interface text, app logo, official seal, badge text, "
    "license plate, real address, identifiable face, public figure likeness, David Riley likeness, Brima Wurie likeness, "
    "judge portrait, police brutality, gore, weapon pointed at viewer, gang sign, sensational imagery, cartoon, anime, "
    "plastic CGI, low detail, blurry, overprocessed HDR, cyberpunk clutter, neon overload, bad anatomy, deformed hands, "
    "extra fingers, warped phone, melted phone, duplicate phone, crooked screen, messy composition, "
    "wavy lines, water ripple, sine wave pattern, flowing wave effect, abstract wave grid, wind turbines"
)

PROMPTS = [
    {
        "id": "RILEY_V3_PHONE_LIFE_REFINED",
        "scene": "S002",
        "file": "riley_v003_phone_life_refined.png",
        "prompt": (
            "a single modern black smartphone standing upright on a dark evidence-table surface, "
            "around it are six clean translucent rectangular memory panels: blurred family photo silhouettes without faces, "
            "unreadable message blocks, calendar squares, a simple map pin card, a cloud storage cube, and health data bars, "
            "all arranged in clear layered depth like museum glass, no app icons, no text, no wave patterns"
        ),
    },
    {
        "id": "RILEY_V3_LOCATION_TRAIL_REFINED",
        "scene": "S027",
        "file": "riley_v003_location_trail_refined.png",
        "prompt": (
            "generic smartphone in the lower left foreground on a dark city map table, "
            "a series of separate glowing blue map pins and small cell-tower silhouettes recede along a clean diagonal route, "
            "one quiet gold endpoint in the distance, no continuous wavy line, no ripples, no wind turbines, "
            "cinematic cliffhanger composition with large dark negative space for title"
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
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = {
        "episode_id": EP,
        "set": "codex_beauty_v003_refine",
        "generator": "codex-controlled-local-a1111-sdxl",
        "style": STYLE,
        "negative_prompt": NEG,
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "items": [],
    }
    base_seed = 934000
    n = 0
    for item in PROMPTS:
        for c in range(3):
            n += 1
            seed = base_seed + n * 193
            payload = {
                "prompt": f"{item['prompt']}, {STYLE}",
                "negative_prompt": NEG,
                "seed": seed,
                "subseed": seed + 1009,
                "subseed_strength": 0.05,
                "sampler_name": "DPM++ 2M Karras",
                "scheduler": "Karras",
                "steps": 50,
                "cfg_scale": 4.6,
                "width": 1536,
                "height": 864,
                "batch_size": 1,
                "n_iter": 1,
                "enable_hr": True,
                "hr_resize_x": 2304,
                "hr_resize_y": 1296,
                "hr_second_pass_steps": 20,
                "denoising_strength": 0.16,
                "hr_upscaler": "Latent",
                "restore_faces": False,
                "do_not_save_samples": True,
                "do_not_save_grid": True,
            }
            result = post(payload)
            out = OUT / item["scene"] / f"{Path(item['file']).stem}_c{c+1:02d}_seed{seed}.png"
            save(result["images"][0], out)
            meta = {
                "asset_id": f"{EP}-{item['scene']}-CODEX-BEAUTY-REFINE-{c+1:03d}",
                "item_id": item["id"],
                "scene": item["scene"],
                "candidate": c + 1,
                "seed": seed,
                "file": str(out),
                "sha256": "sha256:" + sha256(out),
                "prompt": payload["prompt"],
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
