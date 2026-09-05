#!/usr/bin/env python3
"""Generate max-quality SDXL image plates for PD14/PD15.

Usage:
  python scripts/generate_pd14_15_sdxl.py --episode 14 --force
  python scripts/generate_pd14_15_sdxl.py --episode PD-2026-015-theranos --write
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
from dataclasses import dataclass
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
MEDIA = Path(json.loads((ROOT / "config" / "storage.local.json").read_text("utf-8"))["roots"]["media"]["path"])

EPISODES = {
    "14": {
        "episode_id": "PD-2026-014-lange",
        "slug": "lange",
        "prompt_path": ROOT / "episodes" / "PD-2026-014-lange" / "04_scenes" / "ai_prompts.v001.md",
        "ledger_path": ROOT / "episodes" / "PD-2026-014-lange" / "05_stock" / "stock_ledger.v001.json",
    },
    "15": {
        "episode_id": "PD-2026-015-theranos",
        "slug": "theranos",
        "prompt_path": ROOT / "episodes" / "PD-2026-015-theranos" / "04_scenes" / "ai_prompts.v001.md",
        "ledger_path": ROOT / "episodes" / "PD-2026-015-theranos" / "05_stock" / "stock_ledger.v001.json",
    },
    "PD-2026-014-lange": {
        "episode_id": "PD-2026-014-lange",
        "slug": "lange",
        "prompt_path": ROOT / "episodes" / "PD-2026-014-lange" / "04_scenes" / "ai_prompts.v001.md",
        "ledger_path": ROOT / "episodes" / "PD-2026-014-lange" / "05_stock" / "stock_ledger.v001.json",
    },
    "PD-2026-015-theranos": {
        "episode_id": "PD-2026-015-theranos",
        "slug": "theranos",
        "prompt_path": ROOT / "episodes" / "PD-2026-015-theranos" / "04_scenes" / "ai_prompts.v001.md",
        "ledger_path": ROOT / "episodes" / "PD-2026-015-theranos" / "05_stock" / "stock_ledger.v001.json",
    },
}

API = "http://127.0.0.1:7860/sdapi/v1"
MODEL_HINT = "juggernautXL_ragnarokBy"
DEFAULT_NEG = (
    "no recognizable or identifiable real person, no real public figures or celebrity likeness,"
    " no on-screen text or letters, no watermark, no logo, no distorted anatomy, no extra fingers,"
    " no warped faces, no low-resolution or blur artifacts."
)

WIDTH = 1536
HEIGHT = 864
HR_WIDTH = 3072
HR_HEIGHT = 1728
STEPS = 34
CFG = 5.5
SAMPLER = "DPM++ 2M Karras"


@dataclass
class Item:
    file: str
    span_id: str
    prompt: str
    negative_prompt: str


def _hash(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def _hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _post(endpoint: str, payload: dict, timeout: int = 900) -> dict:
    req = urllib.request.Request(
        f"{API}/{endpoint}",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def _get(endpoint: str, timeout: int = 30) -> object:
    with urllib.request.urlopen(f"{API}/{endpoint}", timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def _set_model() -> str:
    try:
        current = _get("options").get("sd_model_checkpoint", "")
        if MODEL_HINT.lower() in current.lower():
            return current
    except Exception:
        pass

    models = _get("sd-models")
    titles = [m.get("title", "") for m in models if isinstance(m, dict)]
    selected = next((t for t in titles if MODEL_HINT.lower() in t.lower()), None)
    if not selected:
        selected = next((t for t in titles if "xl" in t.lower()), titles[0] if titles else "")
    if selected:
        _post("options", {"sd_model_checkpoint": selected}, timeout=120)
    return selected


def _split_prompt(line: str) -> tuple[str, str]:
    line = line.strip()
    if "Avoid:" not in line:
        return line.rstrip("."), DEFAULT_NEG
    prompt, avoid = line.split("Avoid:", 1)
    neg = f"{avoid.strip()}"
    return prompt.strip().rstrip("."), neg


def _read_prompts(path: Path) -> list[Item]:
    text = path.read_text(encoding="utf-8-sig")
    current_file: str | None = None
    out: list[Item] = []
    for raw in text.splitlines():
        m = re.match(r"\s*-\s+`([^`]+\.png)`\s*$", raw)
        if m:
            current_file = m.group(1).strip()
            continue

        if not current_file:
            continue
        if "Avoid:" not in raw:
            continue
        prompt, neg = _split_prompt(raw)
        file = current_file
        span = file.replace(".png", "")
        span = span.split("_")[0]
        out.append(Item(file=file, span_id=span, prompt=prompt, negative_prompt=neg))
        current_file = None
    return out


def _index_by_name(items: list[Item], name: str | None) -> int:
    if not name:
        return 1
    for i, item in enumerate(items, start=1):
        if item.file == name or item.file == f"{name}.png":
            return i
    return 1


def _valid_image(path: Path) -> bool:
    if not path.exists() or path.stat().st_size < 50000:
        return False
    try:
        with Image.open(path) as img:
            w, h = img.size
        return w >= 2048 and abs((w / h) - (16 / 9)) < 0.01
    except Exception:
        return False


def _txt2img(prompt: str, negative_prompt: str, seed: int) -> bytes:
    payload = {
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "seed": seed,
        "sampler_name": SAMPLER,
        "steps": STEPS,
        "cfg_scale": CFG,
        "width": WIDTH,
        "height": HEIGHT,
        "batch_size": 1,
        "n_iter": 1,
        "restore_faces": False,
        "tiling": False,
        "enable_hr": True,
        "denoising_strength": 0.22,
        "hr_resize_x": HR_WIDTH,
        "hr_resize_y": HR_HEIGHT,
        "hr_upscaler": "Latent",
        "hr_second_pass_steps": 16,
        "save_images": False,
        "do_not_save_grid": True,
        "override_settings": {"sd_model_checkpoint": MODEL_HINT},
    }
    result = _post("txt2img", payload)
    if not result.get("images"):
        raise RuntimeError("A1111 returned no image")
    encoded = result["images"][0]
    if "," in encoded and encoded[:32].lower().startswith("data:image"):
        encoded = encoded.split(",", 1)[1]
    return base64.b64decode(encoded)


def _load_ledger(path: Path) -> dict:
    if path.exists():
        return json.loads(path.read_text("utf-8"))
    return {
        "schema_version": "1.0.0",
        "episode_id": path.parent.parent.parent.name,
        "revision": "v001",
        "kind": "ledger",
        "assets": [],
    }


def _write_ledger(path: Path, episode_id: str, slug: str, items: list[tuple[Item, int]]) -> None:
    # Keep original non-AI entries, and overwrite AI entries by stable asset_id.
    existing = _load_ledger(path)
    existing_assets = existing.get("assets", [])
    keep: list[dict] = []
    replace_assets = {f"{episode_id}-{Path(item.file).stem}" for item, _ in items}
    for a in existing_assets:
        if a.get("asset_id") in replace_assets:
            continue
        keep.append(a)

    for item, seed in items:
        out_path = MEDIA / "assets" / "ai" / slug / item.file
        keep.append(
            {
                "asset_id": f"{episode_id}-{Path(item.file).stem}",
                "asset_type": "image",
                "span_id": item.span_id,
                "file": f"assets/ai/{slug}/{item.file}",
                "source": "ai_sdxl",
                "generator": "local-a1111",
                "model": MODEL_HINT,
                "commercial_use": "allowed",
                "license": "generated_owned",
                "ai_disclosure_required": True,
                "no_real_person_likeness_policy": True,
                "query": item.span_id,
                "depicts": item.prompt[:140],
                "prompt_sha256": _hash_text(item.prompt),
                "sha256": _hash(out_path),
                "bytes": out_path.stat().st_size,
                "seed": seed,
            }
        )

    existing["assets"] = sorted(keep, key=lambda x: x.get("asset_id", ""))
    existing["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(existing, indent=2, ensure_ascii=False) + "\n", "utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--episode", required=True, help='"14", "15", or episode id')
    ap.add_argument("--force", action="store_true", help="Overwrite existing files")
    ap.add_argument("--start-index", type=int, default=1, help="Start index in prompt list (1-based)")
    ap.add_argument("--start-name", type=str, default="", help="Start from this filename (e.g. SPN-0015_09.png)")
    ap.add_argument("--max-new", type=int, default=0)
    ap.add_argument("--register-existing", action="store_true", help="Register valid existing images without regenerating them")
    args = ap.parse_args()

    ep = EPISODES.get(args.episode)
    if not ep:
        raise SystemExit(f"unknown episode {args.episode}")

    model = MODEL_HINT
    if not args.register_existing:
        model = _set_model()
        if MODEL_HINT not in model:
            print(f"warn: requested model {MODEL_HINT} not selected, using {model}")

    cfg = ep
    ep_id = cfg["episode_id"]
    slug = cfg["slug"]
    out_dir = MEDIA / "assets" / "ai" / slug
    out_dir.mkdir(parents=True, exist_ok=True)

    items = _read_prompts(cfg["prompt_path"])
    start_idx = args.start_index
    if args.start_name:
        start_idx = _index_by_name(items, args.start_name)
    print(f"start_index={start_idx}")
    print(f"episode={ep_id} prompts={len(items)} out={out_dir}")

    generated = skipped = failed = 0
    wrote: list[tuple[Item, int]] = []

    for idx, item in enumerate(items, start=1):
        if idx < start_idx:
            continue
        out = out_dir / item.file
        seed = 500000 + idx * 101
        if out.exists() and out.stat().st_size > 4096 and _valid_image(out) and not args.force:
            skipped += 1
            if args.register_existing:
                wrote.append((item, seed))
            continue
        if args.max_new and generated >= args.max_new:
            break

        try:
            out.write_bytes(_txt2img(item.prompt, item.negative_prompt, seed))
            if not _valid_image(out):
                raise RuntimeError("generated image is invalid")
            generated += 1
            wrote.append((item, seed))
            print(f"[{idx:03d}/{len(items):03d}] {item.file} seed={seed}")
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, RuntimeError) as exc:
            failed += 1
            print(f"ERROR {item.file}: {exc}")
            continue

    # even skipped prompts should be reflected in ledger with their seed if known; for skipped entries use
    # a deterministic seed derived from position.
    if wrote:
        for idx, item in enumerate(items, start=1):
            if any(item.file == w[0].file for w in wrote):
                continue
            seed = 500000 + idx * 101
            if (out_dir / item.file).exists():
                wrote.append((item, seed))
    wrote = sorted(wrote, key=lambda x: x[0].file)

    _write_ledger(cfg["ledger_path"], ep_id, slug, wrote)
    print(f"done generated={generated} skipped={skipped} failed={failed} ledger={cfg['ledger_path']}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
