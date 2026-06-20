#!/usr/bin/env python3
"""Generate EP6 Terry SDXL still candidates locally.

Local A1111 only. No paid API, no upload. Outputs go to H:/pd-media.
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
EP = "PD-2026-006-terry"
MEDIA = Path(json.loads((ROOT / "config/storage.local.json").read_text("utf-8"))["roots"]["media"]["path"])
OUT = MEDIA / "episodes" / EP / "05_visuals" / "sdxl_ultra_v001"
API = "http://127.0.0.1:7860/sdapi/v1/txt2img"

STYLE = (
    "museum-grade cinematic documentary still, symbolic noir reconstruction, deep navy and black environment, "
    "motivated electric-blue rim light, restrained gold streetlight accent, silver highlights, tactile realistic materials, "
    "controlled shadows with readable detail, crisp cinematic focus, high micro-contrast, fine 35mm film grain, "
    "precise composition, strong negative space for documentary titles, advertiser-safe, neutral tone, "
    "no identifiable face, no real-person likeness, no readable text, no logos, no watermark"
)
NEG = (
    "Martin McFadden likeness, John Terry likeness, Richard Chilton likeness, identifiable person, public figure likeness, "
    "face, facial features, portrait, police badge logo, badge patch, uniform patch, insignia, readable sign, readable text, fake letters, watermark, signature, "
    "court seal, violence, weapon aimed at viewer, glamorized gun, gore, sensational crime scene, cheap stock photo, "
    "cartoon, anime, CGI plastic, overprocessed HDR, neon, candy colors, bad anatomy, deformed hands, extra fingers, "
    "duplicated person, melted clothing, low detail, blurry, jpeg artifacts"
)

PROMPTS = [
    (
        "TERRY_H01_pov_street_stop",
        "hook",
        "S001",
        "S001-SH001",
        "present-day sidewalk from first-person POV at standing chest height, viewer's dark jacket sleeve and torso edge in foreground, two anonymous adult hands in plain dark sleeves clearly touching only the outside of the jacket sleeve for a pat-down, all heads completely outside frame, no uniform, no badge, no patch, no full-body walking pose, no weapon, dusk wet pavement reflections, no readable signs, sharp hands, clear legal-boundary gesture",
        8,
    ),
    (
        "TERRY_H02_cleveland_street",
        "act1",
        "S003",
        "S003-SH002",
        "1963 downtown Cleveland symbolic office street, blank stone and brick building facades, tall windows without signs, wet pavement, anonymous pedestrians as distant silhouettes, period cars only as soft shapes, no storefront signage, no awnings, no shop signs, no logos, brass streetlight, historically plausible but not authentic footage",
        8,
    ),
    (
        "TERRY_H03_store_window_passes",
        "act1",
        "S004",
        "S004-SH001",
        "two faceless anonymous men in 1960s coats walking past a single store window, wide shot from across the street, no faces, no readable signage, repeated-path feeling, muted gold window glow, navy shadows",
        8,
    ),
    (
        "TERRY_H04_observer_over_shoulder",
        "act1",
        "S005",
        "S005-SH001",
        "behind-shoulder view of an anonymous plainclothes observer watching a storefront from a distance, face hidden by shadow and framing, 1960s urban sidewalk, no police badge, no readable signs, pattern-recognition tension",
        8,
    ),
    (
        "TERRY_H05_approach_hands_only",
        "act1",
        "S007",
        "S007-SH001",
        "close low-angle street moment, officer hands and coat sleeves only approaching two anonymous torsos, all faces cropped out, no weapons visible, neutral documentary tension, enough negative space for later captions",
        8,
    ),
    (
        "TERRY_H06_outer_clothing_patdown",
        "act1",
        "S008",
        "S008-SH001",
        "restrained close-up of hands patting the outside of a heavy coat, face completely out of frame, no visible weapon, no badge, tactile coat fabric, legal-boundary motif, not violent",
        8,
    ),
    (
        "TERRY_H07_unknown_person_silhouette",
        "act2",
        "S012",
        "S012-SH001",
        "abstract street encounter silhouette, officer at safe distance from unknown anonymous figure, no faces, no weapon, empty negative space between them, electric-blue edge light, neutral officer-safety tension",
        6,
    ),
    (
        "TERRY_H08_empty_sidewalk_night",
        "act2",
        "S014",
        "S014-SH001",
        "empty city sidewalk at night, rain-dark pavement, one thin line of gold streetlight, no people, reflective and tense, black navy gold palette, quiet reset shot",
        4,
    ),
    (
        "TERRY_H09_coat_fabric_boundary",
        "act3",
        "S018",
        "S018-SH001",
        "macro detail of heavy coat fabric and open hands near outer clothing, no face, no weapon, no pockets searched, tactile legal-boundary motif, low-key gold light and navy shadow",
        8,
    ),
    (
        "TERRY_H10_modern_stop_wide",
        "act4",
        "S022",
        "S022-SH001",
        "modern urban street stop shown wide from behind, anonymous silhouettes only, no identifiable faces, no city landmarks, no logos, respectful neutral framing, electric-blue street reflections",
        8,
    ),
    (
        "TERRY_H11_sidewalk_crowd",
        "act4",
        "S023",
        "S023-SH002",
        "modern sidewalk crowd as faceless silhouettes moving through a narrow pool of light, one person paused at the edge, no police insignia, no faces, restrained documentary tension, excellent depth and negative space",
        6,
    ),
    (
        "TERRY_H12_modern_facts_montage",
        "act4",
        "S024",
        "S024-SH001",
        "contemporary street detail still, shoes at curb, hand near jacket seam, storefront reflection, patrol light as abstract reflection only, no faces, no readable signs, neutral symbolic reconstruction",
        8,
    ),
    (
        "TERRY_H13_thin_line_sidewalk",
        "act4",
        "S026",
        "S026-SH001",
        "empty sidewalk seen from above, a thin electric-blue and gold line drawn along the concrete seam, night texture, quiet city atmosphere, symbolic legal line motif, minimalist composition",
        6,
    ),
    (
        "TERRY_H14_physical_objects",
        "ending",
        "S028",
        "S028-SH001",
        "close-up still life of a coat pocket, a house key, a folded paper, and sidewalk texture, no logos, no text, physical-things motif, navy and gold light, precise still-life composition",
        4,
    ),
    (
        "TERRY_H15_phone_pocket_glow",
        "ending",
        "S029",
        "S029-SH001",
        "smartphone silhouette inside a jacket pocket glowing electric blue, hand nearby but not touching, no app icons, no readable screen, dark navy background, gold rim light, next-episode tease",
        8,
    ),
]


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def post(payload: dict) -> dict:
    req = urllib.request.Request(API, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=480) as r:
        return json.loads(r.read().decode("utf-8"))


def save(b64: str, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(base64.b64decode(b64))


def selected_prompts(ids: set[str] | None) -> list[tuple[str, str, str, str, str, int]]:
    if not ids:
        return PROMPTS
    matches = [p for p in PROMPTS if p[0] in ids or p[2] in ids]
    missing = ids - {p[0] for p in matches} - {p[2] for p in matches}
    if missing:
        raise SystemExit(f"unknown ids: {', '.join(sorted(missing))}")
    return matches


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ids", nargs="*", help="Prompt ids or scene ids to generate. Default: all prompts.")
    parser.add_argument("--max-candidates", type=int, default=None, help="Optional cap per prompt for test runs.")
    args = parser.parse_args()

    prompts = selected_prompts(set(args.ids) if args.ids else None)
    OUT.mkdir(parents=True, exist_ok=True)
    manifest_path = OUT / "asset_manifest.v001.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text("utf-8"))
    else:
        manifest = {
            "episode_id": EP,
            "set": "sdxl_ultra_v001",
            "generator": "local-a1111-sdxl",
            "model_profile": "juggernautXL_ragnarokBy.safetensors [dd08fa32f9]",
            "ai_disclosure_required": True,
            "rights_status": "candidate_requires_qc",
            "started_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "items": [],
        }

    base_seed = 606000
    n = 0
    total = sum(min(p[5], args.max_candidates) if args.max_candidates else p[5] for p in prompts)
    for item_id, section, scene_id, shot_id, core, default_count in prompts:
        candidate_count = min(default_count, args.max_candidates) if args.max_candidates else default_count
        for c in range(candidate_count):
            n += 1
            global_index = len(manifest["items"]) + 1
            seed = base_seed + global_index * 149
            prompt = f"{core}, {STYLE}"
            payload = {
                "prompt": prompt,
                "negative_prompt": NEG,
                "seed": seed,
                "subseed": seed + 911,
                "subseed_strength": 0.10,
                "sampler_name": "DPM++ 2M Karras",
                "scheduler": "Karras",
                "steps": 40,
                "cfg_scale": 4.8,
                "width": 1536,
                "height": 864,
                "batch_size": 1,
                "n_iter": 1,
                "enable_hr": False,
                "restore_faces": False,
                "do_not_save_samples": True,
                "do_not_save_grid": True,
            }
            result = post(payload)
            out = OUT / section / scene_id / f"{item_id}_c{c+1:02d}_seed{seed}.png"
            save(result["images"][0], out)
            file_hash = hashlib.sha256(out.read_bytes()).hexdigest()
            meta = {
                "asset_id": f"{EP}-{scene_id}-IMG-{global_index:03d}",
                "item_id": item_id,
                "scene_id": scene_id,
                "shot_id": shot_id,
                "section": section,
                "candidate": c + 1,
                "seed": seed,
                "path": str(out),
                "sha256": file_hash,
                "prompt_sha256": sha256_text(prompt),
                "prompt": prompt,
                "negative_prompt": NEG,
                "model_profile": "local-a1111-sdxl-ultra-v001",
                "status": "candidate",
                "qc_status": "not_run",
                "ai_disclosure_required": True,
                "rights_origin": "AI-generated local SDXL symbolic reconstruction",
                "rights_basis": "owner-local-generation_candidate_requires_qc",
                "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            }
            out.with_suffix(".json").write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n", "utf-8")
            manifest["items"].append(meta)
            manifest["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
            manifest["count"] = len(manifest["items"])
            manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", "utf-8")
            print(f"[{n:03d}/{total:03d}] {out}")
    print(f"done generated={n} total_manifest={len(manifest['items'])} out={OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
