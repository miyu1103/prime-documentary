#!/usr/bin/env python3
"""Generate 180 premium symbolic plates for EP6 Terry v002.

Local A1111 only. No upload, no paid API. Outputs stay under H:/pd-media.
18 visual chapters x 10 variants = 180 hero plates for Remotion motion.
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
EP = "PD-2026-006-terry"
MEDIA = Path(json.loads((ROOT / "config/storage.local.json").read_text("utf-8"))["roots"]["media"]["path"])
OUT = MEDIA / "episodes" / EP / "05_visuals" / "sdxl_hq_v002_180"
REPO_CONTACT = ROOT / "episodes" / EP / "05_visuals" / "v002_180_contact_sheet.jpg"
API = "http://127.0.0.1:7860/sdapi/v1/txt2img"

STYLE = (
    "museum-grade premium documentary key art, cinematic constitutional-law thriller, "
    "deep black and navy palette, electric-blue rim light, restrained gold constitutional line, "
    "wet stone, glass reflection, fine fabric texture, volumetric haze, rich atmospheric depth, "
    "elegant editorial lighting, high contrast, realistic but painterly, expensive poster finish, "
    "symbolic reconstruction, not authentic footage, no readable text, no logos, no identifiable person"
)

NEG = (
    "readable text, letters, numbers, signage, captions, UI text, logos, watermark, signature, "
    "real person likeness, recognizable person, face, portrait, detailed eyes, celebrity, Timothy Carpenter, "
    "Terry, McFadden, police badge, official seal, realistic uniform patch, gun, weapon glamour, blood, gore, "
    "sensational crime scene, aggressive violence, handcuffs, cheap cyberpunk, clutter, cartoon, anime, "
    "flat vector, plastic CGI, low detail, blurry, pixelated, jpeg artifacts, warped anatomy, extra fingers, "
    "oversaturated, muddy shadows, duplicate body parts"
)

VARIANTS = [
    "wide establishing composition with strong foreground and deep background, clean negative space for documentary titles",
    "low-angle cinematic frame with monumental scale, layered architecture, faceless silhouettes only if needed",
    "overhead editorial composition, crisp geometry, one gold boundary line crossing blue street grid",
    "macro detail plate with glass reflection, dust motes, shallow depth of field, tactile surface",
    "side-lit tableau with strong diagonal light, foreground obstruction for parallax",
    "minimal black-space composition, one precise gold line, restrained blue glow",
    "rainy reflective pavement or polished stone, elegant highlights, no signage",
    "architectural depth frame, corridor or sidewalk receding into darkness",
    "compressed telephoto look, luminous street path through abstract city blocks",
    "final hero frame, balanced poster composition, premium YouTube documentary finish",
]

SCENES: list[tuple[str, str, str]] = [
    ("t01", "hook_stop", "present-tense viewer POV on a dark city sidewalk, a thin gold boundary line blooming between private space and state power, no faces, no readable signs"),
    ("t02", "opening_wall", "abstract Fourth Amendment wall made of black stone and blue light, a narrow gold gap labeled only by visual design, no text"),
    ("t03", "street_1963", "generic 1960s downtown storefront street at night, no city names, no signs, wet sidewalk, empty frame, Cleveland-inspired but not identifiable"),
    ("t04", "window_path", "empty store window and sidewalk reflected in dark glass, repeated blue path traces and gold dots suggesting repeated trips, no people"),
    ("t05", "observer", "detective observation as symbolic notebook, street grid, coat sleeve edge, no badge, no face, no readable writing"),
    ("t06", "suspicion_proof", "two abstract evidence thresholds suspended over black stone, suspicion as blue vapor, proof as heavier gold line, no text"),
    ("t07", "decision_point", "officer safety and innocent contact as two opposing light fields on a dark sidewalk, no uniforms, no faces, no weapons"),
    ("t08", "outer_clothing", "macro coat fabric and outer-clothing boundary motif, blue scan line stopping at a gold seam, no hands, no body, no weapon"),
    ("t09", "case_becomes_law", "street encounter dissolving into courthouse columns, black pavement transforming into legal stone, no seal, no people"),
    ("t10", "probable_warrant", "blank warrant-like paper shape and gold probable-cause threshold on dark desk, redaction-like blocks without readable text"),
    ("t11", "below_threshold", "thin blue suspicion line falling short of a luminous gold threshold, abstract legal scale, no text"),
    ("t12", "unknown_moment", "dark sidewalk corner before certainty, long shadows, blue haze, gold caution line, faceless and nonviolent"),
    ("t13", "brief_stop", "three-step street encounter ladder shown as architectural platforms in darkness, encounter to stop to arrest as visual tiers without text"),
    ("t14", "two_truths", "real street and abuse-risk tension shown as split black pavement, blue order on one side, gold warning crack on the other, no people"),
    ("t15", "ruling_1968", "abstract Supreme Court-style columns at night, eight blue light blocks and one gold light block implied as composition, no seal, no text"),
    ("t16", "articulable_facts", "specific articulable facts as pinned light points on a dark sidewalk map, blue dots connected by a restrained gold line, no labels"),
    ("t17", "cost_today", "modern urban sidewalk under surveillance-like streetlights, judgment lines branching, bias-risk implied by warped reflections, no people or signs"),
    ("t18", "ending_phone", "street-body question transitioning to a generic unbranded phone in a pocket-like dark space, next privacy door glowing blue and gold, no logo"),
]


def sha_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def post(payload: dict) -> dict:
    req = urllib.request.Request(API, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=900) as r:
        return json.loads(r.read().decode("utf-8"))


def save_image(b64: str, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(base64.b64decode(b64))


def write_contact_sheet(images: list[Path]) -> None:
    try:
        from PIL import Image, ImageDraw
    except Exception as exc:
        print(f"contact_sheet skipped: {exc}", flush=True)
        return
    thumbs: list[Image.Image] = []
    labels: list[str] = []
    for p in images[:180]:
        im = Image.open(p).convert("RGB")
        im.thumbnail((256, 144), Image.Resampling.LANCZOS)
        canvas = Image.new("RGB", (256, 170), (8, 8, 10))
        canvas.paste(im, (0, 0))
        ImageDraw.Draw(canvas).text((8, 148), p.parent.name + "/" + p.stem[-3:], fill=(229, 181, 58))
        thumbs.append(canvas)
        labels.append(p.name)
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
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = {
        "episode_id": EP,
        "set": "sdxl_hq_v002_180",
        "target_count": len(SCENES) * len(VARIANTS),
        "generator": "local-a1111-sdxl",
        "api": API,
        "ai_disclosure_required": True,
        "rights_status": "generated_symbolic_reconstruction_requires_qc_before_publish",
        "output_dir": str(OUT),
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "items": [],
    }
    base_seed = 606200
    total = len(SCENES) * len(VARIANTS)
    generated_paths: list[Path] = []
    failures = 0
    n = 0
    for scene_index, (scene_id, kind, core) in enumerate(SCENES, start=1):
        for variant_index, variant in enumerate(VARIANTS, start=1):
            n += 1
            seed = base_seed + scene_index * 1000 + variant_index * 41
            out = OUT / scene_id / f"{scene_id}_{variant_index:03d}.png"
            prompt = f"{core}, {variant}, {STYLE}"
            meta = {
                "asset_id": f"{EP}-V002-{scene_id.upper()}-{variant_index:03d}",
                "scene_id": scene_id,
                "kind": kind,
                "candidate": variant_index,
                "seed": seed,
                "path": str(out),
                "prompt_sha256": sha_text(prompt),
                "prompt": prompt,
                "negative_prompt": NEG,
                "model_profile": "local-a1111-sdxl-hq-v002-180",
                "status": "candidate",
                "ai_disclosure_required": True,
                "rights_origin": "AI-generated local SDXL symbolic reconstruction",
                "no_real_person_likeness_intended": True,
                "no_authentic_footage_claim": True,
            }
            if out.exists() and out.stat().st_size > 1024:
                print(f"[{n:03d}/{total}] skip {out.name}", flush=True)
            else:
                payload = {
                    "prompt": prompt,
                    "negative_prompt": NEG,
                    "seed": seed,
                    "subseed": seed + 613,
                    "subseed_strength": 0.14,
                    "sampler_name": "DPM++ 2M Karras",
                    "scheduler": "Karras",
                    "steps": 48,
                    "cfg_scale": 5.0,
                    "width": 1536,
                    "height": 864,
                    "batch_size": 1,
                    "n_iter": 1,
                    "enable_hr": True,
                    "hr_resize_x": 2304,
                    "hr_resize_y": 1296,
                    "hr_second_pass_steps": 22,
                    "denoising_strength": 0.23,
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
            if out.exists() and out.stat().st_size > 1024:
                generated_paths.append(out)
            out.with_suffix(".json").write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n", "utf-8")
            manifest["items"].append(meta)
            if n % 10 == 0:
                (OUT / "asset_manifest.v002.partial.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", "utf-8")
                write_contact_sheet(sorted(set(generated_paths)))
    manifest["finished_at"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    manifest["generated_count"] = len([x for x in manifest["items"] if x.get("status") != "failed"])
    manifest["failures"] = failures
    (OUT / "asset_manifest.v002.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", "utf-8")
    write_contact_sheet(sorted(set(generated_paths)))
    print(f"generated={manifest['generated_count']} failures={failures} out={OUT}", flush=True)
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
