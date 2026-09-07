#!/usr/bin/env python3
"""Generate S027 Riley cliffhanger stills without map-wave patterns."""
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
OUT = MEDIA / "episodes" / EP / "05_visuals" / "codex_beauty_v003_refine" / "S027_nowaves"
API = "http://127.0.0.1:7860/sdapi/v1/txt2img"

STYLE = (
    "premium cinematic documentary key visual, physically plausible editorial photography, legal-tech noir, "
    "dark navy and black, restrained electric-blue rim light, small warm gold accent, elegant negative space, "
    "shallow depth of field, 35mm film grain, serious quiet cliffhanger"
)
NEG = (
    "map roads, road map, street map, flowing lines, wavy lines, curving route, route line, ripple, water, grid waves, "
    "wind turbines, text, readable UI, fake letters, logo, app icon, watermark, license plate, identifiable face, "
    "public figure, cyberpunk clutter, neon overload, cartoon, anime, plastic CGI, low detail, bad anatomy, deformed hands"
)
PROMPT = (
    "a modern black smartphone lying on a dark matte evidence table in the lower left foreground, "
    "far in the background are three soft-focus cell tower silhouettes with tiny blue signal dots above them, "
    "one isolated gold location pin standing upright on the table, no map, no roads, no connecting lines, "
    "large clean dark negative space on the right for title overlay"
)


def post(payload: dict) -> dict:
    req = urllib.request.Request(API, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=900) as r:
        return json.loads(r.read().decode("utf-8"))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    items = []
    for idx, seed in enumerate([936101, 936307, 936509], start=1):
        payload = {
            "prompt": f"{PROMPT}, {STYLE}",
            "negative_prompt": NEG,
            "seed": seed,
            "subseed": seed + 1009,
            "subseed_strength": 0.03,
            "sampler_name": "DPM++ 2M Karras",
            "scheduler": "Karras",
            "steps": 50,
            "cfg_scale": 4.8,
            "width": 1536,
            "height": 864,
            "batch_size": 1,
            "n_iter": 1,
            "enable_hr": True,
            "hr_resize_x": 2304,
            "hr_resize_y": 1296,
            "hr_second_pass_steps": 18,
            "denoising_strength": 0.14,
            "hr_upscaler": "Latent",
            "restore_faces": False,
            "do_not_save_samples": True,
            "do_not_save_grid": True,
        }
        result = post(payload)
        out = OUT / f"riley_v003_location_nowaves_c{idx:02d}_seed{seed}.png"
        out.write_bytes(base64.b64decode(result["images"][0]))
        meta = {
            "asset_id": f"{EP}-S027-CODEX-NOWAVES-{idx:03d}",
            "scene": "S027",
            "candidate": idx,
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
        items.append(meta)
        print(f"[{idx:02d}] {out}", flush=True)
    (OUT / "asset_manifest.v001.json").write_text(json.dumps({
        "episode_id": EP,
        "set": "codex_beauty_v003_s027_nowaves",
        "generator": "codex-controlled-local-a1111-sdxl",
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "items": items,
        "count": len(items),
    }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
