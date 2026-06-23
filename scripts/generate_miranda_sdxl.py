#!/usr/bin/env python3
"""Generate Miranda SDXL scene plates and thumbnail backgrounds with local A1111.

Outputs:
  H:/pd-media/assets/ai/miranda/SPN-XXXX*.png
  H:/pd-media/assets/ai/thumbs/miranda/THUMB-01..06.png
  episodes/PD-2026-001-miranda/05_stock/stock_ledger.v001.json
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import re
import time
import urllib.error
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-001-miranda"
SLUG = "miranda"
MEDIA = Path(json.loads((ROOT / "config/storage.local.json").read_text("utf-8"))["roots"]["media"]["path"])
AI_PROMPTS = ROOT / "episodes" / EP / "04_scenes" / "ai_prompts.v001.md"
THUMB_PROMPTS = ROOT / "episodes" / EP / "04_scenes" / "thumb_prompts.v001.md"
LEDGER = ROOT / "episodes" / EP / "05_stock" / "stock_ledger.v001.json"
OUT = MEDIA / "assets" / "ai" / SLUG
THUMB_OUT = MEDIA / "assets" / "ai" / "thumbs" / SLUG
API = "http://127.0.0.1:7860/sdapi/v1"
MODEL_HINT = "juggernautXL"


DEFAULT_NEG = (
    "readable text, letters, captions, watermark, logo, identifiable real person, public figure likeness, "
    "Ernesto Miranda likeness, Earl Warren likeness, judge portrait, celebrity face, warped face, visible face detail, "
    "distorted anatomy, extra fingers, bad hands, low resolution, blur artifacts, cheap stock photo, cartoon, anime, "
    "plastic CGI, overprocessed HDR"
)


def sha_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def sha_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def post(endpoint: str, payload: dict, timeout: int = 900) -> dict:
    req = urllib.request.Request(
        f"{API}/{endpoint}",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def get(endpoint: str, timeout: int = 30) -> object:
    with urllib.request.urlopen(f"{API}/{endpoint}", timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def set_model() -> str:
    models = get("sd-models")
    titles = [m.get("title", "") for m in models if isinstance(m, dict)]
    selected = next((t for t in titles if MODEL_HINT.lower() in t.lower()), None)
    if not selected:
        selected = next((t for t in titles if "xl" in t.lower()), titles[0] if titles else "")
    if selected:
        post("options", {"sd_model_checkpoint": selected}, timeout=120)
    return selected


def split_prompt(line: str) -> tuple[str, str]:
    prompt = line.strip()
    neg = DEFAULT_NEG
    if "Avoid:" in prompt:
        prompt, avoid = prompt.split("Avoid:", 1)
        neg = f"{avoid.strip()} {DEFAULT_NEG}"
    return prompt.strip().rstrip("."), neg


def parse_ai_prompts() -> list[dict]:
    text = AI_PROMPTS.read_text("utf-8")
    items: list[dict] = []
    current_file: str | None = None
    for raw in text.splitlines():
        m = re.match(r"\s*-\s+`([^`]+\.png)`\s*$", raw)
        if m:
            current_file = m.group(1)
            continue
        if current_file and raw.strip().startswith(tuple(["Wide", "Profile", "Extreme", "Macro", "Low-", "Over-", "Close", "Aerial", "Medium", "High-", "Dutch", "Symmetrical"])):
            prompt, neg = split_prompt(raw.strip())
            span = current_file.split("_", 1)[0].replace(".png", "")
            items.append({"file": current_file, "span_id": span, "prompt": prompt, "negative_prompt": neg})
            current_file = None
    return items


def parse_thumb_prompts() -> list[dict]:
    text = THUMB_PROMPTS.read_text("utf-8")
    items: list[dict] = []
    current_file: str | None = None
    for raw in text.splitlines():
        m = re.match(r"\s*-\s+`(THUMB-\d+\.png)`\s*$", raw)
        if m:
            current_file = m.group(1)
            continue
        if current_file and raw.startswith("    "):
            line = raw.strip()
            if line:
                prompt, neg = split_prompt(line)
                items.append({"file": current_file, "prompt": prompt, "negative_prompt": neg})
                current_file = None
    return items


def txt2img(prompt: str, negative_prompt: str, seed: int, *, thumb: bool = False) -> bytes:
    payload = {
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "seed": seed,
        "subseed": seed + 313,
        "subseed_strength": 0.08,
        "sampler_name": "DPM++ 2M Karras",
        "scheduler": "Karras",
        "steps": 30 if not thumb else 34,
        "cfg_scale": 5.0,
        "width": 1368,
        "height": 768,
        "batch_size": 1,
        "n_iter": 1,
        "enable_hr": True,
        "hr_resize_x": 2048,
        "hr_resize_y": 1152,
        "hr_second_pass_steps": 12 if not thumb else 14,
        "denoising_strength": 0.22,
        "hr_upscaler": "Latent",
        "restore_faces": False,
        "do_not_save_samples": True,
        "do_not_save_grid": True,
    }
    result = post("txt2img", payload)
    return base64.b64decode(result["images"][0])


def load_ledger() -> dict:
    if LEDGER.exists():
        return json.loads(LEDGER.read_text("utf-8"))
    return {"episode_id": EP, "revision": "v001", "assets": []}


def write_ledger(entries: dict[Path, dict]) -> None:
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    ledger = load_ledger()
    by_path = {a.get("file"): a for a in ledger.get("assets", [])}
    for path, meta in entries.items():
        by_path[meta["file"]] = meta
    ledger["assets"] = sorted(by_path.values(), key=lambda x: x["file"])
    ledger["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    LEDGER.write_text(json.dumps(ledger, indent=2, ensure_ascii=False) + "\n", "utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--scene", action="store_true", help="Generate scene plates.")
    ap.add_argument("--thumbs", action="store_true", help="Generate thumbnail backgrounds.")
    ap.add_argument("--max-new", type=int, default=0)
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    if not args.scene and not args.thumbs:
        args.scene = args.thumbs = True

    model = set_model()
    print(f"model={model}")
    entries: dict[Path, dict] = {}
    generated = skipped = failed = 0
    if args.scene:
        OUT.mkdir(parents=True, exist_ok=True)
        items = parse_ai_prompts()
        print(f"scene_prompts={len(items)} out={OUT}")
        for idx, item in enumerate(items, start=1):
            out = OUT / item["file"]
            if out.exists() and out.stat().st_size > 4096 and not args.force:
                skipped += 1
            else:
                if args.max_new and generated >= args.max_new:
                    break
                seed = 501001 + idx * 101
                try:
                    out.write_bytes(txt2img(item["prompt"], item["negative_prompt"], seed))
                    generated += 1
                    print(f"[scene {idx:03d}/{len(items):03d}] {out.name}")
                except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
                    failed += 1
                    print(f"[scene ERROR] {out.name}: {e}")
                    continue
            if out.exists():
                rel = f"assets/ai/{SLUG}/{out.name}"
                entries[out] = {
                    "asset_id": f"{EP}-{out.stem}",
                    "span_id": item["span_id"],
                    "file": rel,
                    "source": "ai_sdxl",
                    "generator": "local-a1111",
                    "model": model,
                    "commercial_use": "allowed",
                    "license": "generated_owned",
                    "ai_disclosure_required": True,
                    "no_real_person_likeness_policy": True,
                    "prompt_sha256": sha_text(item["prompt"]),
                    "sha256": sha_file(out),
                }
            if idx % 8 == 0:
                write_ledger(entries)
    if args.thumbs:
        THUMB_OUT.mkdir(parents=True, exist_ok=True)
        thumbs = parse_thumb_prompts()
        print(f"thumb_prompts={len(thumbs)} out={THUMB_OUT}")
        for idx, item in enumerate(thumbs, start=1):
            out = THUMB_OUT / item["file"]
            if out.exists() and out.stat().st_size > 4096 and not args.force:
                skipped += 1
            else:
                if args.max_new and generated >= args.max_new:
                    break
                seed = 601001 + idx * 173
                try:
                    out.write_bytes(txt2img(item["prompt"], item["negative_prompt"], seed, thumb=True))
                    generated += 1
                    print(f"[thumb {idx:02d}/{len(thumbs):02d}] {out.name}")
                except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
                    failed += 1
                    print(f"[thumb ERROR] {out.name}: {e}")
                    continue
            if out.exists():
                rel = f"assets/ai/thumbs/{SLUG}/{out.name}"
                entries[out] = {
                    "asset_id": f"{EP}-{out.stem}",
                    "file": rel,
                    "source": "ai_sdxl",
                    "generator": "local-a1111",
                    "model": model,
                    "commercial_use": "allowed",
                    "license": "generated_owned",
                    "ai_disclosure_required": True,
                    "no_real_person_likeness_policy": True,
                    "prompt_sha256": sha_text(item["prompt"]),
                    "sha256": sha_file(out),
                }
    write_ledger(entries)
    print(f"done generated={generated} skipped={skipped} failed={failed} ledger={LEDGER}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
