#!/usr/bin/env python3
"""Generate ~180 SDXL stills for PD-2026-005 Madoff via local A1111 API.

Target:
  26 hero prompts x 6 candidates = 156
  24 additional chapter/B-roll prompts = 180

No upload. Local SDXL only. Outputs are media artifacts, not committed source.
"""
from __future__ import annotations

import base64
import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-005-madoff"
EPDIR = ROOT / "episodes" / EP
MEDIA = Path(json.loads((ROOT / "config/storage.local.json").read_text("utf-8"))["roots"]["media"]["path"])
OUT = MEDIA / "episodes" / EP / "05_visuals" / "sdxl_hq_v001_180"
PROMPTS_MD = EPDIR / "04_scenes" / "sdxl_prompts.v001.md"
API = "http://127.0.0.1:7860/sdapi/v1/txt2img"

STYLE = (
    "cinematic symbolic noir, dark and gold amber palette, low-key single-source lighting, "
    "deep shadows, volumetric haze, fine film grain, faceless anonymous silhouettes seen from behind or in profile shadow, "
    "allegorical documentary still, high detail, 16:9, no visible facial features"
)
NEG = (
    "pink, magenta, neon, candy colors, text, words, letters, watermark, signature, logo, "
    "face, facial features, recognizable person, portrait likeness, celebrity, Bernie Madoff likeness, "
    "deformed hands, extra fingers, mutated, lowres, jpeg artifacts, oversaturated, cartoon, anime"
)
VARIANTS = [
    "wide establishing frame, negative space for documentary typography, 35mm lens",
    "medium cinematic frame, strong foreground silhouette, shallow depth of field",
    "macro detail, paper texture and dust motes, dramatic desk lamp",
    "low angle institutional scale, imposing shadows, slow dread",
    "overhead geometric composition, clean visual metaphor, editorial clarity",
    "side-lit tableau, layered depth, parallax-ready foreground and background",
]


EXTRA = [
    ("B01", "hook", "a black screen-like void with a single golden return curve reflected on polished marble, no people"),
    ("B02", "hook", "a hand-drawn chart on cream paper under a brass lamp, the line is unnaturally smooth"),
    ("B03", "opening", "gold streams flowing from university, charity, and bank symbols toward a dark central office"),
    ("B04", "opening", "an empty Wall Street lobby at night, brass directory glowing, faceless reflections"),
    ("B05", "actI", "a velvet rope outside a private investment office, warm light behind frosted glass"),
    ("B06", "actI", "fund managers as faceless silhouettes around a table, all looking at one golden chart"),
    ("B07", "actI", "a stack of elegant investor statements tied with black ribbon, ominous gold edge light"),
    ("B08", "actI", "a calm golden line crossing storm clouds and falling market papers in the background"),
    ("B09", "actII", "a bank account ledger drawer swallowing cash, no trading screens active"),
    ("B10", "actII", "empty trading terminals in a dark office, dust on keyboards, amber exit light"),
    ("B11", "actII", "faceless hands passing coins in a circular loop, the loop feels trapped"),
    ("B12", "actII", "paper account statements falling through darkness like fake snow"),
    ("B13", "actII", "a huge number made of paper peeling away into smoke, gold fragments"),
    ("B14", "actII", "a vault interior with only a thin trail of coins on the floor"),
    ("B15", "actIII", "a lone analyst silhouette at midnight with calculator, coffee, annotated chart"),
    ("B16", "actIII", "red pencil circles around a too-smooth golden line on a printed chart"),
    ("B17", "actIII", "warning envelopes piled outside a closed regulator door, institutional stone hallway"),
    ("B18", "actIII", "a dark watchtower with its searchlight off, gold fog at the base"),
    ("B19", "actIV", "faceless crowd rushing toward a single teller window during financial panic"),
    ("B20", "actIV", "a drained vault with one last coin rolling into shadow"),
    ("B21", "actIV", "federal courthouse steps at dusk, lone anonymous silhouette ascending"),
    ("B22", "actIV", "a prison corridor with a closing steel door and thin gold light"),
    ("B23", "ending", "two return lines side by side, one smooth gold, one jagged silver, symbolic abstract"),
    ("B24", "ending", "a single anonymous investor silhouette stopping before a perfect golden line, choosing doubt"),
]


def post_json(url: str, payload: dict) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=240) as r:
        return json.loads(r.read().decode("utf-8"))


def get_json(url: str) -> dict | list:
    with urllib.request.urlopen(url, timeout=20) as r:
        return json.loads(r.read().decode("utf-8"))


def parse_heroes() -> list[tuple[str, str, str]]:
    text = PROMPTS_MD.read_text("utf-8")
    rows: list[tuple[str, str, str]] = []
    for line in text.splitlines():
        if not line.startswith("| H"):
            continue
        parts = [p.strip() for p in line.strip("|").split("|")]
        if len(parts) >= 3:
            rows.append((parts[0], parts[1], parts[2]))
    return rows


def save_image(b64: str, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(base64.b64decode(b64))


def generate_one(item_id: str, section: str, prompt_core: str, variant_idx: int, seed: int) -> Path:
    variant = VARIANTS[variant_idx % len(VARIANTS)]
    prompt = f"{prompt_core}, {variant}, {STYLE}"
    payload = {
        "prompt": prompt,
        "negative_prompt": NEG,
        "seed": seed,
        "subseed": seed + 100000,
        "subseed_strength": 0.18,
        "sampler_name": "DPM++ 2M Karras",
        "scheduler": "Karras",
        "steps": 44,
        "cfg_scale": 5.2,
        "width": 1344,
        "height": 768,
        "batch_size": 1,
        "n_iter": 1,
        "enable_hr": True,
        "hr_resize_x": 1920,
        "hr_resize_y": 1080,
        "hr_second_pass_steps": 18,
        "denoising_strength": 0.28,
        "hr_upscaler": "Latent",
        "restore_faces": False,
        "tiling": False,
        "do_not_save_samples": True,
        "do_not_save_grid": True,
    }
    res = post_json(API, payload)
    out = OUT / section / f"{item_id}_c{variant_idx+1:02d}_seed{seed}.png"
    save_image(res["images"][0], out)
    meta = {
        "id": item_id,
        "section": section,
        "candidate": variant_idx + 1,
        "seed": seed,
        "prompt": prompt,
        "negative_prompt": NEG,
        "model": "local A1111 current checkpoint",
        "width": 1920,
        "height": 1080,
        "base_width": 1344,
        "base_height": 768,
        "steps": 44,
        "hires_steps": 18,
        "cfg_scale": 5.2,
        "denoising_strength": 0.28,
        "sampler": "DPM++ 2M Karras",
        "rights": "local generated symbolic reconstruction; no real-person likeness intended",
    }
    out.with_suffix(".json").write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n", "utf-8")
    return out


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    OUT.mkdir(parents=True, exist_ok=True)
    try:
        options = get_json("http://127.0.0.1:7860/sdapi/v1/options")
        print(f"model={options.get('sd_model_checkpoint')} vae={options.get('sd_vae')}")
    except Exception as e:
        print(f"ERROR: local SDXL API not reachable: {e}")
        return 1

    heroes = parse_heroes()
    plan: list[tuple[str, str, str, int]] = []
    for hid, section, core in heroes:
        for i in range(6):
            plan.append((hid, section, core, i))
    for eid, section, core in EXTRA:
        plan.append((eid, section, core, 0))
    plan = plan[:180]
    manifest = {
        "episode_id": EP,
        "set": "sdxl_hq_v001_180",
        "target_count": len(plan),
        "api": "A1111 txt2img local, SDXL high-quality Hires.fix 1920x1080",
        "output_dir": str(OUT),
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "items": [],
    }
    base_seed = 505001
    failures = 0
    for n, (item_id, section, core, variant_idx) in enumerate(plan, 1):
        seed = base_seed + n * 37
        try:
            out = generate_one(item_id, section, core, variant_idx, seed)
            manifest["items"].append({"n": n, "id": item_id, "section": section, "candidate": variant_idx + 1, "seed": seed, "path": str(out)})
            print(f"[{n:03d}/{len(plan)}] {item_id} c{variant_idx+1:02d} -> {out.name}")
        except urllib.error.HTTPError as e:
            failures += 1
            msg = e.read().decode(errors="replace")[:400]
            print(f"[{n:03d}] HTTP {e.code}: {msg}")
        except Exception as e:
            failures += 1
            print(f"[{n:03d}] ERR {item_id}: {e}")
        if n % 10 == 0:
            (OUT / "asset_manifest.v001.partial.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", "utf-8")
    manifest["finished_at"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    manifest["generated_count"] = len(manifest["items"])
    manifest["failures"] = failures
    (OUT / "asset_manifest.v001.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", "utf-8")
    print(f"generated={len(manifest['items'])} failures={failures} out={OUT}")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
