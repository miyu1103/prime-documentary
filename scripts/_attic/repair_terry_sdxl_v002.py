#!/usr/bin/env python3
"""Repair selected Terry v002 plate groups that failed visual QC."""
from __future__ import annotations

import base64
import hashlib
import json
import shutil
import sys
import time
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-006-terry"
MEDIA = Path(json.loads((ROOT / "config/storage.local.json").read_text("utf-8"))["roots"]["media"]["path"])
OUT = MEDIA / "episodes" / EP / "05_visuals" / "sdxl_hq_v002_180"
REJECTED = OUT / "rejected_initial"
REPO_CONTACT = ROOT / "episodes" / EP / "05_visuals" / "v002_180_contact_sheet.jpg"
API = "http://127.0.0.1:7860/sdapi/v1/txt2img"

STYLE = (
    "museum-grade premium documentary key art, cinematic constitutional-law thriller, deep black and navy palette, "
    "electric-blue rim light, restrained gold boundary line, wet stone, glass reflection, fine texture, volumetric haze, "
    "rich atmospheric depth, elegant editorial lighting, high contrast, realistic but painterly, expensive poster finish, "
    "symbolic reconstruction, not authentic footage"
)

NEG = (
    "readable text, pseudo text, gibberish text, letters, numbers, signage, plaques, inscriptions, labels, captions, UI text, "
    "logos, watermark, signature, real person likeness, recognizable person, face, portrait, eyes, head, hands, fingers, body, "
    "police badge, official seal, uniform patch, gun, weapon, blood, gore, handcuffs, cartoon, anime, flat vector, plastic CGI, "
    "low detail, blurry, pixelated, jpeg artifacts, warped anatomy, oversaturated, muddy shadows"
)

VARIANTS = [
    "wide establishing composition, clean negative space, pure geometry only",
    "low-angle cinematic frame, monumental abstract scale, no human figure",
    "overhead editorial composition, crisp geometry, one gold line crossing blue-black stone",
    "macro detail plate, tactile surface, shallow depth of field, no markings",
    "side-lit tableau, strong diagonal light, foreground obstruction for parallax",
    "minimal black-space composition, one precise gold line, restrained blue glow",
    "rainy reflective stone surface, elegant highlights, no signage",
    "architectural depth frame, corridor receding into darkness, blank surfaces",
    "compressed telephoto look, luminous abstract boundary through dark slabs",
    "final hero frame, balanced poster composition, premium documentary finish",
]

REPAIRS: dict[str, tuple[str, str]] = {
    "t02": (
        "opening_wall_no_text",
        "pure abstract constitutional wall made only of unmarked black stone slabs, electric-blue light seams, and one narrow gold gap, no framed plaque, no signboard, no inscription surface, no writing area",
    ),
    "t03": (
        "street_1963_no_signage",
        "generic empty 1960s downtown street canyon at night with blank architectural facades and dark glass, no storefront words, no awnings with names, no street signs, no posters, no labels, no human figures",
    ),
    "t08": (
        "outer_clothing_no_person",
        "extreme macro of dark woven coat fabric and a single gold seam, blue scan light stopping at the seam, fabric texture only, no person, no body, no hands, no weapon",
    ),
    "t10": (
        "warrant_threshold_no_text",
        "blank featureless paper-like rectangle as a legal symbol on black stone beside a gold threshold line, no writing, no redactions, no labels, no printed marks",
    ),
}


def sha_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def post(payload: dict) -> dict:
    req = urllib.request.Request(API, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=900) as r:
        return json.loads(r.read().decode("utf-8"))


def save_image(b64: str, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(base64.b64decode(b64))


def archive_existing(path: Path) -> None:
    if not path.exists():
        return
    rel = path.relative_to(OUT)
    dst = REJECTED / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    if not dst.exists():
        shutil.move(str(path), dst)
    else:
        path.unlink()


def write_contact_sheet() -> None:
    try:
        from PIL import Image, ImageDraw
    except Exception as exc:
        print(f"contact_sheet skipped: {exc}", flush=True)
        return
    images = [p for p in sorted(OUT.rglob("*.png")) if "rejected_initial" not in p.parts]
    thumbs: list[Image.Image] = []
    for p in images[:180]:
        im = Image.open(p).convert("RGB")
        im.thumbnail((256, 144), Image.Resampling.LANCZOS)
        canvas = Image.new("RGB", (256, 170), (8, 8, 10))
        canvas.paste(im, (0, 0))
        ImageDraw.Draw(canvas).text((8, 148), p.parent.name + "/" + p.stem[-3:], fill=(229, 181, 58))
        thumbs.append(canvas)
    cols = 10
    rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 256, rows * 170), (5, 6, 9))
    for i, thumb in enumerate(thumbs):
        sheet.paste(thumb, ((i % cols) * 256, (i // cols) * 170))
    REPO_CONTACT.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(REPO_CONTACT, quality=92)
    print(f"contact_sheet={REPO_CONTACT}", flush=True)


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    selected = sys.argv[1:] if len(sys.argv) > 1 else sorted(REPAIRS)
    unknown = [name for name in selected if name not in REPAIRS]
    if unknown:
        raise SystemExit(f"Unknown repair targets: {unknown}")
    repairs_manifest = {
        "episode_id": EP,
        "set": "sdxl_hq_v002_180",
        "repair": "v002_targeted_no_text_no_person",
        "targets": selected,
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "items": [],
    }
    base_seed = 626200
    total = len(selected) * len(VARIANTS)
    n = 0
    failures = 0
    for scene_order, scene_id in enumerate(selected, start=1):
        kind, core = REPAIRS[scene_id]
        for variant_index, variant in enumerate(VARIANTS, start=1):
            n += 1
            seed = base_seed + scene_order * 2000 + variant_index * 53
            out = OUT / scene_id / f"{scene_id}_{variant_index:03d}.png"
            meta_path = out.with_suffix(".json")
            archive_existing(out)
            archive_existing(meta_path)
            prompt = f"{core}, {variant}, {STYLE}, no text, no letters, no people"
            meta = {
                "asset_id": f"{EP}-V002-REPAIR-{scene_id.upper()}-{variant_index:03d}",
                "scene_id": scene_id,
                "kind": kind,
                "candidate": variant_index,
                "seed": seed,
                "path": str(out),
                "prompt_sha256": sha_text(prompt),
                "prompt": prompt,
                "negative_prompt": NEG,
                "model_profile": "local-a1111-sdxl-hq-v002-repair",
                "status": "repaired_candidate",
                "ai_disclosure_required": True,
                "rights_origin": "AI-generated local SDXL symbolic reconstruction",
                "no_real_person_likeness_intended": True,
                "no_authentic_footage_claim": True,
                "repair_reason": "Initial group contained generated pseudo-text or human-form drift.",
            }
            payload = {
                "prompt": prompt,
                "negative_prompt": NEG,
                "seed": seed,
                "subseed": seed + 719,
                "subseed_strength": 0.12,
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
                "hr_second_pass_steps": 24,
                "denoising_strength": 0.22,
                "hr_upscaler": "Latent",
                "restore_faces": False,
                "tiling": False,
                "do_not_save_samples": True,
                "do_not_save_grid": True,
            }
            try:
                result = post(payload)
                save_image(result["images"][0], out)
                print(f"[{n:03d}/{total}] repaired {scene_id} v{variant_index:03d} -> {out.name}", flush=True)
            except Exception as exc:
                failures += 1
                meta["status"] = "failed"
                meta["error"] = repr(exc)
                print(f"[{n:03d}/{total}] ERROR {scene_id} v{variant_index:03d}: {exc}", flush=True)
            meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n", "utf-8")
            repairs_manifest["items"].append(meta)
    repairs_manifest["finished_at"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    repairs_manifest["failures"] = failures
    (OUT / "asset_manifest.v002.repair.json").write_text(json.dumps(repairs_manifest, indent=2, ensure_ascii=False) + "\n", "utf-8")
    write_contact_sheet()
    print(f"repaired={total - failures} failures={failures}", flush=True)
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
