#!/usr/bin/env python3
"""Generate 180 high-quality symbolic plates for EP8 Carpenter v007.

Local A1111 only. No upload, no paid API. Outputs stay under H:/pd-media.
Each of the 18 narrative scenes gets 10 plates for Remotion crossfades,
pan/zoom motion, and parallax-like visual variety.
"""
from __future__ import annotations

import base64
import hashlib
import json
import sys
import time
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-008-carpenter"
MEDIA = Path(json.loads((ROOT / "config/storage.local.json").read_text("utf-8"))["roots"]["media"]["path"])
OUT = MEDIA / "episodes" / EP / "05_visuals" / "sdxl_hq_v007_180"
API = "http://127.0.0.1:7860/sdapi/v1/txt2img"

STYLE = (
    "museum-quality premium documentary key art, cinematic legal-tech privacy thriller, "
    "deep black and navy palette, electric-blue data light, restrained gold accents, "
    "glossy glass, wet stone, fine surface texture, volumetric haze, rich atmospheric depth, "
    "elegant editorial lighting, high contrast, realistic but painterly, expensive poster finish, "
    "symbolic reconstruction, no authentic footage, no text, no logos, no people, no faces"
)

NEG = (
    "readable text, letters, numbers, captions, UI text, app icons, logos, watermark, signature, "
    "map labels, city names, real landmark, official court seal, person, face, portrait, hands, "
    "police badge, gun, blood, gore, sensational crime scene, cheap cyberpunk, cluttered interface, "
    "cartoon, anime, flat vector, plastic CGI, low detail, blurry, pixelated, jpeg artifacts, "
    "warped phone, broken perspective, oversaturated, muddy, duplicate objects"
)

VARIANTS = [
    "wide establishing composition, strong foreground and deep background, clean negative space at left",
    "low-angle cinematic frame, dramatic scale, layered silhouettes only as abstract architecture",
    "overhead editorial composition, crisp geometry, route lines and data points as light",
    "macro detail plate, glass reflection, dust motes, shallow depth of field",
    "side-lit tableau, strong diagonal light, foreground obstruction for parallax",
    "minimal black-space composition, one precise gold trail, restrained blue glow",
    "rainy reflective surface, wet pavement or polished stone, elegant highlights",
    "architectural depth frame, corridor or grid receding into darkness",
    "compressed telephoto look, luminous data trail through abstract city blocks",
    "final hero frame, balanced poster composition, premium YouTube documentary finish",
]

SCENES: list[tuple[str, str, str]] = [
    ("s01", "trail", "generic unbranded black-glass smartphone floating over a dark abstract city map, many tiny electric-blue location points blooming into one restrained gold route"),
    ("s02", "trilogy", "ordinary unbranded smartphone on a dark private desk, reflected map trail in glass, subtle wallet and keys as out-of-focus shapes, private life made visible"),
    ("s03", "detroit", "generic closed electronics storefront at night in rain, no signage, wet pavement reflecting blue and gold light, factual crime-case atmosphere without people"),
    ("s04", "tower", "abstract cell towers as glowing points above a vast night city grid, overlapping blue coverage rings and one restrained gold route"),
    ("s05", "points", "dense constellation of location points above a dark city map, gold path emerging from hundreds of blue dots, data accumulation made physical"),
    ("s06", "warrant", "blank court-order-like paper shape beside an unbranded phone on black stone, redaction bars as abstract blocks only, no readable text"),
    ("s07", "doctrine", "two old legal records as abstract paper forms dissolving into a modern phone-location map, 1970s doctrine meeting smartphone data"),
    ("s08", "thinList", "thin paper strip of dialed-number marks on one side versus deep luminous location map on the other, black void between them, no readable marks"),
    ("s09", "lifeMap", "large life-map metaphor from phone data: home-like glow, work-like grid, clinic-like corridor, faith-like quiet doorway, all symbolic and unlabelled"),
    ("s10", "collision", "old paper doctrine and modern glass phone colliding in midair, electric-blue and gold fragments, restrained legal metaphor"),
    ("s11", "ruling", "abstract columned courthouse silhouette at night, no official seal, gold light on stone, phone-location particles in the foreground"),
    ("s12", "boundary", "thin glowing warrant line crossing a dark map and stopping a field of data points, precise boundary in blue and gold"),
    ("s13", "choice", "phone location trail continuing automatically from pocket-like darkness into city grid, unavoidable data record as elegant symbolic image"),
    ("s14", "dissent", "four shadowed abstract legal desks around a glowing uncertain boundary line, no people or faces, ambiguity made cinematic"),
    ("s15", "warrantline", "gold warrant line as a luminous barrier between a private phone and a vast data map, rich unavoidable record still private"),
    ("s16", "doors", "dark minimalist corridor of unmarked doors, first door cracked open with electric-blue data light spilling out and gold dust"),
    ("s17", "ending_trilogy", "three symbolic panels in one cinematic frame: street boundary, phone contents glow, location map trail, no text"),
    ("s18", "viewer_device", "generic smartphone lying face-up in darkness, black glass reflecting a gold location path and blue city points, intimate final viewer device"),
]


def sha_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def post(payload: dict) -> dict:
    req = urllib.request.Request(API, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=900) as r:
        return json.loads(r.read().decode("utf-8"))


def save_image(b64: str, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = base64.b64decode(b64)
    path.write_bytes(raw)


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = {
        "episode_id": EP,
        "set": "sdxl_hq_v007_180",
        "target_count": len(SCENES) * len(VARIANTS),
        "generator": "local-a1111-sdxl",
        "api": API,
        "ai_disclosure_required": True,
        "rights_status": "generated_symbolic_reconstruction_requires_qc_before_publish",
        "output_dir": str(OUT),
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "items": [],
    }
    base_seed = 707000
    total = len(SCENES) * len(VARIANTS)
    n = 0
    failures = 0
    for scene_index, (scene_id, kind, core) in enumerate(SCENES, start=1):
        for variant_index, variant in enumerate(VARIANTS, start=1):
            n += 1
            seed = base_seed + scene_index * 1000 + variant_index * 37
            out = OUT / scene_id / f"{scene_id}_{variant_index:03d}.png"
            prompt = f"{core}, {variant}, {STYLE}"
            meta = {
                "asset_id": f"{EP}-V007-{scene_id.upper()}-{variant_index:03d}",
                "scene_id": scene_id,
                "kind": kind,
                "candidate": variant_index,
                "seed": seed,
                "path": str(out),
                "prompt_sha256": sha_text(prompt),
                "prompt": prompt,
                "negative_prompt": NEG,
                "model_profile": "local-a1111-sdxl-hq-v007-180",
                "status": "candidate",
                "ai_disclosure_required": True,
                "rights_origin": "AI-generated local SDXL symbolic reconstruction",
                "no_real_person_likeness_intended": True,
            }
            if out.exists() and out.stat().st_size > 1024:
                print(f"[{n:03d}/{total}] skip {out.name}", flush=True)
            else:
                payload = {
                    "prompt": prompt,
                    "negative_prompt": NEG,
                    "seed": seed,
                    "subseed": seed + 411,
                    "subseed_strength": 0.16,
                    "sampler_name": "DPM++ 2M Karras",
                    "scheduler": "Karras",
                    "steps": 46,
                    "cfg_scale": 5.1,
                    "width": 1536,
                    "height": 864,
                    "batch_size": 1,
                    "n_iter": 1,
                    "enable_hr": True,
                    "hr_resize_x": 2304,
                    "hr_resize_y": 1296,
                    "hr_second_pass_steps": 20,
                    "denoising_strength": 0.24,
                    "hr_upscaler": "Latent",
                    "restore_faces": False,
                    "tiling": False,
                    "do_not_save_samples": True,
                    "do_not_save_grid": True,
                }
                try:
                    result = post(payload)
                    save_image(result["images"][0], out)
                    print(f"[{n:03d}/{total}] {scene_id} v{variant_index:03d} -> {out.name}", flush=True)
                except Exception as exc:
                    failures += 1
                    meta["status"] = "failed"
                    meta["error"] = repr(exc)
                    print(f"[{n:03d}/{total}] ERROR {scene_id} v{variant_index:03d}: {exc}", flush=True)
            out.with_suffix(".json").write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n", "utf-8")
            manifest["items"].append(meta)
            if n % 10 == 0:
                (OUT / "asset_manifest.v007.partial.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", "utf-8")
    manifest["finished_at"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    manifest["generated_count"] = len([x for x in manifest["items"] if x.get("status") != "failed"])
    manifest["failures"] = failures
    (OUT / "asset_manifest.v007.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", "utf-8")
    print(f"generated={manifest['generated_count']} failures={failures} out={OUT}", flush=True)
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
