#!/usr/bin/env python3
"""Generate EP7 Riley SDXL still candidates locally.

Local A1111 only. No paid API, no upload. Outputs go to H:/pd-media.
"""
from __future__ import annotations

import base64
import hashlib
import json
import argparse
import time
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-007-riley"
MEDIA = Path(json.loads((ROOT / "config/storage.local.json").read_text("utf-8"))["roots"]["media"]["path"])
OUT = MEDIA / "episodes" / EP / "05_visuals" / "sdxl_ultra_v001"
API = "http://127.0.0.1:7860/sdapi/v1/txt2img"

STYLE = (
    "museum-grade cinematic documentary still, Prime Documentary legal-tech noir, deep black and navy palette, "
    "motivated electric-blue practical glow, restrained gold accent, silver highlights, tactile realistic materials, "
    "controlled chiaroscuro, subtle haze, fine 35mm film grain, decisive composition, strong subject hierarchy, "
    "negative space for documentary titles, symbolic reconstruction, not authentic footage, no identifiable face, "
    "no real-person likeness, no readable text, no logos, no watermark"
)
NEG = (
    "David Riley likeness, Brima Wurie likeness, identifiable defendant, identifiable officer face, justice portrait, "
    "public figure likeness, readable text, fake letters, phone UI text, app brand, logo, watermark, badge text, "
    "license plate, real address, gang sign, sensational gang imagery, gore, weapon pointed at viewer, police brutality, "
    "authentic evidence photo, cheap stock photo, cyberpunk UI, cartoon, anime, CGI plastic, overprocessed HDR, "
    "bad anatomy, deformed hands, extra fingers, warped phone, duplicate phone, melted glass, low detail, blurry"
)

PROMPTS = [
    (
        "RILEY_H01_phone_lift_pocket",
        "hook",
        "S001",
        "S001-SH001",
        "museum-grade extreme macro object portrait, no people: a folded dark coat on a black studio surface, one coat pocket sharply visible, a modern black smartphone protruding halfway from the pocket, pocket seam and heavy woven fabric in crisp detail, phone screen off and mostly black, only a narrow electric-blue police-light reflection streak across the glass, subtle silver phone edge, no glowing blue screen, no hand, no fingers, no standing person, no torso, no head, no body, no visible UI, intimate privacy violation symbol",
        8,
    ),
    (
        "RILEY_H02_phone_window_life",
        "opening",
        "S002",
        "S002-SH001",
        "dark tabletop with wallet, keys, and generic smartphone, the phone opening into layered abstract life data, blurred photo tiles without faces, unreadable message blocks, map dots, calendar shapes",
        5,
    ),
    (
        "RILEY_A1_roadside_san_diego",
        "act1",
        "S003",
        "S003-SH001",
        "anonymous Southern California roadside traffic stop at night, car body reflecting blue police lights, no license plate, no street signs, palm silhouettes subtle in distance, no faces",
        4,
    ),
    (
        "RILEY_A1_car_search_symbolic",
        "act1",
        "S004",
        "S004-SH001",
        "close detail of anonymous car interior being searched with flashlight beam across dark upholstery, sealed evidence markers suggested but unreadable, neutral documentary tone, no faces",
        4,
    ),
    (
        "RILEY_A1_phone_evidence_table",
        "act1",
        "S005",
        "S005-SH001",
        "generic smartphone on detective desk under cold blue overhead light, anonymous hands near the device, blurred folders in background, no readable documents, no face",
        5,
    ),
    (
        "RILEY_A1_two_phones",
        "act1",
        "S007",
        "S007-SH001",
        "modern smartphone beside a basic flip phone on a dark evidence table, both closed or unreadable, electric-blue rim light, subtle gold divider, clean negative space",
        4,
    ),
    (
        "RILEY_A2_wallet_phone_analogy",
        "act2",
        "S010",
        "S010-SH001",
        "macro still life of a simple wallet with a few cards next to a generic smartphone, dark matte tabletop, phone screen black, composition designed for overlays",
        4,
    ),
    (
        "RILEY_A2_data_layers",
        "act2",
        "S011",
        "S011-SH001",
        "generic smartphone emitting many abstract data layers into dark space, non-branded generic icons, blurred photo tiles without faces, electric-blue and silver layers with tiny gold highlights",
        5,
    ),
    (
        "RILEY_A2_pocket_cloud",
        "act2",
        "S012",
        "S012-SH001",
        "anonymous hand holding a generic phone while thin electric-blue data threads rise toward abstract cloud server shapes in dark distance, no logos, no readable UI, no face",
        5,
    ),
    (
        "RILEY_A3_scotus_empty",
        "act3",
        "S014",
        "S014-SH001",
        "empty symbolic Supreme Court chamber or marble courthouse corridor, no justices, no portraits, dramatic navy shadows and restrained gold light, space for lower-third citation",
        4,
    ),
    (
        "RILEY_A3_privacies_life",
        "act3",
        "S015",
        "S015-SH001",
        "anonymous human silhouette formed from phone data fragments, unreadable messages, calendar shapes, map pins, photos with no faces, intimate restrained privacy image, dark negative space",
        5,
    ),
    (
        "RILEY_A3_katz_booth",
        "act3",
        "S018",
        "S018-SH001",
        "1960s public phone booth at night, human silhouette inside with face fully hidden by shadow and glass reflection, privacy field suggested by electric-blue light, no readable signage",
        4,
    ),
    (
        "RILEY_A4_apps_life",
        "act4",
        "S022",
        "S022-SH001",
        "generic non-branded app-like tiles floating from a locked phone, abstract prayer symbol, heart, medical cross, book, map dot, message bubbles, all unreadable, no real app logos, no faces",
        5,
    ),
    (
        "RILEY_A4_location_to_carrier",
        "act4",
        "S023",
        "S023-SH001",
        "phone on dark surface emitting pulsing location points to distant abstract cell tower and cloud, no real map, no carrier logo, no readable place names",
        5,
    ),
    (
        "RILEY_END_locked_warrant",
        "ending",
        "S025",
        "S025-SH001",
        "locked generic smartphone on dark table with a restrained gold light path leading toward an abstract judge bench or warrant seal shape, no readable text",
        4,
    ),
    (
        "RILEY_END_location_trail",
        "ending",
        "S027",
        "S027-SH001",
        "abstract night map with a continuous electric-blue location trail leaving a generic phone, no real streets, no readable labels, clean space for next-episode text",
        5,
    ),
]


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def post(payload: dict) -> dict:
    req = urllib.request.Request(
        API,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=900) as r:
        return json.loads(r.read().decode("utf-8"))


def save(b64: str, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(base64.b64decode(b64))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ids", nargs="*", help="Optional item_id filter, e.g. RILEY_H01_phone_lift_pocket")
    parser.add_argument("--candidates", type=int, default=None, help="Override candidate count per selected item.")
    parser.add_argument("--set-name", default="sdxl_ultra_v001", help="Output set name under 05_visuals.")
    parser.add_argument("--base-seed", type=int, default=807000, help="Base seed for deterministic candidate families.")
    args = parser.parse_args()
    wanted = set(args.ids or [])

    out_root = MEDIA / "episodes" / EP / "05_visuals" / args.set_name
    out_root.mkdir(parents=True, exist_ok=True)
    manifest = {
        "episode_id": EP,
        "set": args.set_name,
        "generator": "local-a1111-sdxl",
        "api": API,
        "ai_disclosure_required": True,
        "rights_status": "candidate_requires_qc",
        "style": STYLE,
        "negative_prompt": NEG,
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "items": [],
    }
    base_seed = args.base_seed
    n = 0
    for item_id, section, scene_id, shot_id, core, candidate_count in PROMPTS:
        if wanted and item_id not in wanted:
            continue
        if args.candidates is not None:
            candidate_count = args.candidates
        for c in range(candidate_count):
            n += 1
            seed = base_seed + n * 149
            prompt = f"{core}, {STYLE}"
            payload = {
                "prompt": prompt,
                "negative_prompt": NEG,
                "seed": seed,
                "subseed": seed + 997,
                "subseed_strength": 0.08,
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
                "hr_second_pass_steps": 24,
                "denoising_strength": 0.20,
                "hr_upscaler": "Latent",
                "restore_faces": False,
                "do_not_save_samples": True,
                "do_not_save_grid": True,
            }
            result = post(payload)
            out = out_root / section / f"{item_id}_c{c+1:02d}_seed{seed}.png"
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
            print(f"[{n:03d}] {out}", flush=True)
            if n % 8 == 0:
                (out_root / "asset_manifest.v001.partial.json").write_text(
                    json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", "utf-8"
                )
    manifest["finished_at"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    manifest["count"] = len(manifest["items"])
    (out_root / "asset_manifest.v001.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", "utf-8")
    print(f"done count={len(manifest['items'])} out={out_root}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
