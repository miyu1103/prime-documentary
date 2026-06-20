#!/usr/bin/env python3
"""Generate EP8 Carpenter SDXL still candidates locally.

Local A1111 only. No paid API, no upload. Outputs go to H:/pd-media.
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
OUT = MEDIA / "episodes" / EP / "05_visuals" / "sdxl_ultra_v001"
API = "http://127.0.0.1:7860/sdapi/v1/txt2img"

STYLE = (
    "museum-grade cinematic documentary still, elegant noir legal-tech visual, deep navy and black environment, "
    "motivated electric-blue rim light, restrained gold accent, silver highlights, tactile realistic materials, "
    "volumetric light, controlled haze, shallow depth of field, fine 35mm film grain, precise composition, "
    "strong negative space for documentary titles, symbolic reconstruction, no identifiable face, no real-person likeness, "
    "no readable text, no logos, no watermark"
)
NEG = (
    "Timothy Carpenter likeness, identifiable person, public figure likeness, real store logo, carrier logo, readable text, "
    "numbers in image, fake letters, watermark, signature, badge text, court seal, violence, gun aimed at viewer, gore, "
    "sensational crime scene, cyberpunk UI, cheap stock photo, cartoon, anime, CGI plastic, overprocessed HDR, "
    "bad anatomy, deformed hands, extra fingers, warped phone, melted tower, low detail, blurry, jpeg artifacts"
)

PROMPTS = [
    ("CARP_H01_phone_map_hand", "hook", "S001", "SH004", "anonymous adult hand holding a generic smartphone in a dark room, blue location trail reflected on black glass, screen mostly dark, no face, no brand, intimate present-tense opening"),
    ("CARP_H02_dark_location_bloom", "hook", "S001", "SH002", "vast dark city map as abstract geometry, thousands of tiny electric-blue location points blooming into a single gold path, no street names, overhead editorial composition"),
    ("CARP_H03_phone_on_desk", "opening", "S002", "SH009", "generic smartphone resting on a dark walnut desk beside blurred keys and transit card, screen glow draws a thin blue line across the surface, ordinary life made ominous"),
    ("CARP_A1_store_exterior", "act1", "S003", "SH012", "generic small electronics store exterior at night, shutters down, wet pavement reflecting blue and gold light, no logo, no readable signs, no people, restrained crime-case atmosphere"),
    ("CARP_A1_caseboard_number", "act1", "S003", "SH014", "anonymous hand placing a redacted phone-number card on a dark investigative case board, strings and pins as abstract lines, no readable numbers, no badges"),
    ("CARP_A1_blank_order", "act1", "S005", "SH018", "macro of a blank court-order-like document on black desk, generic phone carrier icon shape blurred in background, redaction bars added as objects not readable text, blue rim light"),
    ("CARP_A1_city_overhead", "act1", "S006", "SH024", "overhead night city blocks rendered as realistic abstract grid, cell tower glow points in the distance, route overlay space left empty for Remotion, no labels"),
    ("CARP_A1_legal_scale", "act1", "S008", "SH033", "antique brass legal scale on a black desk, one pan holds a blank warrant-like paper, the other a glowing data point cloud, electric-blue and gold chiaroscuro"),
    ("CARP_A2_thin_list", "act2", "S012", "SH042", "narrow redacted dialed-number paper strip on a dark 1970s desk, period phone blurred in background, lots of negative space, no readable numbers"),
    ("CARP_A2_bedside_phone", "act2", "S013", "SH046", "smartphone glowing on bedside table at night, empty room, soft blue network halo, ordinary private life, no brand, no readable text"),
    ("CARP_A2_commuter_phone", "act2", "S014", "SH050", "anonymous commuter on train holding generic phone, face cropped out of frame, muted public transit interior without ads or logos, blue phone glow"),
    ("CARP_A3_scotus_columns", "act3", "S017", "SH062", "generic Supreme-Court-inspired columned building silhouette at night, no official seal, no readable text, gold light on columns, deep blue sky"),
    ("CARP_A3_quiet_phone_network", "act3", "S018", "SH069", "generic phone on dark kitchen counter, screen off, invisible network represented by faint blue light threads around it, quiet automatic tracking"),
    ("CARP_A3_balanced_scale", "act3", "S020", "SH079", "soft-focus balanced legal scale with an electric-blue boundary line projected through haze behind it, abstract court debate, no text"),
    ("CARP_A4_parchment_phone", "act4", "S022", "SH083", "aged parchment texture beside a modern generic smartphone on deep navy table, blue constitutional line crossing into phone glass, no readable writing"),
    ("CARP_A4_data_doors", "act4", "S024", "SH094", "dark minimalist corridor with several unmarked doors, first door cracked open with electric-blue light spilling out, data-door metaphor, no labels"),
    ("CARP_A4_public_life_phones", "act4", "S025", "SH095", "anonymous crowd silhouettes in transit station, phones glowing softly, faces obscured, no ads, no branding, network lines implied by light"),
    ("CARP_END_device_landing", "ending", "S028", "SH107", "anonymous hand holding a generic phone toward camera, black glass reflecting a blue location trail, no face, no logo, final viewer-device landing"),
    ("CARP_THUMB_phone_map", "thumbnail", "S028", "TH001", "premium YouTube documentary thumbnail background, huge generic smartphone over dark map, blue route trail and gold warning glow, clean negative space, no text"),
    ("CARP_THUMB_127_days", "thumbnail", "S001", "TH002", "cinematic dark map covered with thousands of blue points forming a gold trail into a phone silhouette, dramatic high contrast, thumbnail-ready, no text")
]


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def post(payload: dict) -> dict:
    req = urllib.request.Request(API, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=420) as r:
        return json.loads(r.read().decode("utf-8"))


def save(b64: str, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(base64.b64decode(b64))


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = {
        "episode_id": EP,
        "set": "sdxl_ultra_v001",
        "generator": "local-a1111-sdxl",
        "ai_disclosure_required": True,
        "rights_status": "candidate_requires_qc",
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "items": [],
    }
    base_seed = 826000
    total = len(PROMPTS) * 4
    n = 0
    for item_id, section, scene_id, shot_id, core in PROMPTS:
        candidate_count = 6 if section in {"hook", "thumbnail"} else 4
        for c in range(candidate_count):
            n += 1
            seed = base_seed + n * 137
            prompt = f"{core}, {STYLE}"
            payload = {
                "prompt": prompt,
                "negative_prompt": NEG,
                "seed": seed,
                "subseed": seed + 777,
                "subseed_strength": 0.10,
                "sampler_name": "DPM++ 2M Karras",
                "scheduler": "Karras",
                "steps": 48,
                "cfg_scale": 4.8,
                "width": 1536,
                "height": 864,
                "batch_size": 1,
                "n_iter": 1,
                "enable_hr": True,
                "hr_resize_x": 2304,
                "hr_resize_y": 1296,
                "hr_second_pass_steps": 22,
                "denoising_strength": 0.22,
                "hr_upscaler": "Latent",
                "restore_faces": False,
                "do_not_save_samples": True,
                "do_not_save_grid": True,
            }
            result = post(payload)
            out = OUT / section / f"{item_id}_c{c+1:02d}_seed{seed}.png"
            save(result["images"][0], out)
            meta = {
                "asset_id": f"{EP}-{scene_id}-IMG-{c+1:03d}",
                "item_id": item_id,
                "scene_id": scene_id,
                "shot_id": shot_id,
                "section": section,
                "candidate": c + 1,
                "seed": seed,
                "path": str(out),
                "prompt_sha256": sha256_text(prompt),
                "prompt": prompt,
                "negative_prompt": NEG,
                "model_profile": "local-a1111-sdxl-ultra-v001",
                "status": "candidate",
                "ai_disclosure_required": True,
                "rights_origin": "AI-generated local SDXL symbolic reconstruction",
            }
            out.with_suffix(".json").write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n", "utf-8")
            manifest["items"].append(meta)
            print(f"[{n:03d}] {out}")
            if n % 8 == 0:
                (OUT / "asset_manifest.v001.partial.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", "utf-8")
    manifest["finished_at"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    manifest["count"] = len(manifest["items"])
    (OUT / "asset_manifest.v001.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", "utf-8")
    print(f"done count={len(manifest['items'])} out={OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
