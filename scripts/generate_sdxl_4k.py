#!/usr/bin/env python
"""Generate MAX-quality 4K (long edge >= 3840) SDXL plates for a PD episode.

Pipeline (spec ONE-PASS row 5: SDXL gen -> upscale to >=3840 with R-ESRGAN):
  txt2img  base 1536x864  -> hires-fix (Latent) 3072x1728  (JuggernautXL, 34 steps)
  -> extras R-ESRGAN 4x+  -> 3840x2160 final  (4K, sharp)

Reads prompts from episodes/<ep>/04_scenes/ai_prompts.v001.md in the established
format (a `- ` + backticked `*.png` line, then a line with `... Avoid: <neg>`).
Produces N seed variants per listed file (S01.png, S01_02.png, ...). Saves to the
media shelf and copies to remotion/public/<slug>/. Idempotent: a valid >=3840
file is skipped. Local A1111 API on 127.0.0.1:7860 (no paid API, no upload).

Usage:
  .venv/Scripts/python.exe scripts/generate_sdxl_4k.py PD-2026-018-flashcrash --variants 3
  .venv/Scripts/python.exe scripts/generate_sdxl_4k.py 18 --variants 3 --only S07
"""
from __future__ import annotations

import argparse
import base64
import json
import re
import shutil
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API = "http://127.0.0.1:7860"
MODEL_HINT = "juggernautXL_ragnarokBy"
WIDTH, HEIGHT = 1536, 864
HR_W, HR_H = 3072, 1728
FINAL_W, FINAL_H = 3840, 2160          # spec row 5: long edge >= 3840 (4K)
STEPS, CFG, SAMPLER = 34, 5.5, "DPM++ 2M Karras"
UPSCALER = "R-ESRGAN 4x+"
BASE_SEED = 720180
DEFAULT_NEG = ("real person, real face, portrait, recognizable individual, celebrity likeness, "
               "deepfake, readable text, paragraph, company logo, brand name, trademark, signature, "
               "watermark, lowres, blurry, jpeg artifacts, cartoon, anime, 3d render, distorted, "
               "extra limbs, deformed, bad anatomy")


def _post(path: str, payload: dict, timeout: int = 600) -> dict:
    req = urllib.request.Request(f"{API}/sdapi/v1/{path}",
                                 data=json.dumps(payload).encode("utf-8"),
                                 headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def _get(path: str, timeout: int = 60) -> dict | list:
    with urllib.request.urlopen(f"{API}/sdapi/v1/{path}", timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def media_root() -> Path:
    cfg = json.loads((ROOT / "config" / "storage.local.json").read_text("utf-8"))
    return Path(cfg["roots"]["media"]["path"])


def resolve_ep(arg: str) -> str:
    epdir = ROOT / "episodes"
    if (epdir / arg).is_dir():
        return arg
    import glob
    hits = [Path(p).name for p in glob.glob(str(epdir / f"PD-*-{int(arg):03d}-*"))] if arg.isdigit() else []
    if len(hits) == 1:
        return hits[0]
    raise SystemExit(f"cannot resolve episode '{arg}': {hits}")


def read_prompts(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8-sig")
    cur, out = None, []
    for raw in text.splitlines():
        m = re.match(r"\s*-\s+`([^`]+\.png)`\s*$", raw)
        if m:
            cur = m.group(1).strip()
            continue
        if cur and "Avoid:" in raw:
            pos, _, neg = raw.strip().partition("Avoid:")
            out.append({"file": cur, "prompt": pos.strip().rstrip("."),
                        "neg": (neg.strip() + ", " + DEFAULT_NEG)})
            cur = None
    return out


def set_model() -> None:
    cur = _get("options").get("sd_model_checkpoint", "")
    if MODEL_HINT.lower() in cur.lower():
        return
    titles = [m.get("title", "") for m in _get("sd-models")]
    pick = next((t for t in titles if MODEL_HINT.lower() in t.lower()), None)
    if pick:
        _post("options", {"sd_model_checkpoint": pick}, timeout=180)


def gen_one(prompt: str, neg: str, seed: int) -> bytes:
    res = _post("txt2img", {
        "prompt": prompt, "negative_prompt": neg, "seed": seed,
        "sampler_name": SAMPLER, "steps": STEPS, "cfg_scale": CFG,
        "width": WIDTH, "height": HEIGHT,
        "enable_hr": True, "denoising_strength": 0.22,
        "hr_resize_x": HR_W, "hr_resize_y": HR_H,
        "hr_upscaler": "Latent", "hr_second_pass_steps": 16,
        "save_images": False, "do_not_save_grid": True,
        "override_settings": {"sd_model_checkpoint": MODEL_HINT},
    })
    b64 = res["images"][0]
    up = _post("extra-single-image", {
        "image": b64, "resize_mode": 1,
        "upscaling_resize_w": FINAL_W, "upscaling_resize_h": FINAL_H,
        "upscaling_crop": True, "upscaler_1": UPSCALER,
    })
    return base64.b64decode(up["image"])


def png_long_edge(p: Path) -> int:
    try:
        h = p.open("rb").read(24)
        if h[:8] == b"\x89PNG\r\n\x1a\n":
            return max(int.from_bytes(h[16:20], "big"), int.from_bytes(h[20:24], "big"))
    except Exception:
        pass
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("episode")
    ap.add_argument("--variants", type=int, default=3)
    ap.add_argument("--only", help="only this shot stem, e.g. S07")
    args = ap.parse_args()

    ep = resolve_ep(args.episode)
    slug = re.sub(r"^PD-\d{4}-\d{3}-", "", ep)
    prompts = read_prompts(ROOT / "episodes" / ep / "04_scenes" / "ai_prompts.v001.md")
    if args.only:
        prompts = [p for p in prompts if Path(p["file"]).stem == args.only]
    media_dir = media_root() / "assets" / "ai" / slug
    pub_dir = ROOT / "remotion" / "public" / slug
    media_dir.mkdir(parents=True, exist_ok=True)
    pub_dir.mkdir(parents=True, exist_ok=True)

    set_model()
    made = skipped = failed = 0
    total = len(prompts) * args.variants
    print(f"episode={ep} slug={slug} shots={len(prompts)} variants={args.variants} "
          f"target={FINAL_W}x{FINAL_H} model={MODEL_HINT} -> {total} images", flush=True)

    for p in prompts:
        stem = Path(p["file"]).stem
        for v in range(args.variants):
            name = f"{stem}.png" if v == 0 else f"{stem}_{v+1:02d}.png"
            out = media_dir / name
            if png_long_edge(out) >= FINAL_W:
                skipped += 1
                continue
            seed = BASE_SEED + (hash(stem) % 100000) + v * 9973
            try:
                t0 = time.time()
                data = gen_one(p["prompt"], p["neg"], seed)
                out.write_bytes(data)
                shutil.copyfile(out, pub_dir / name)
                le = png_long_edge(out)
                print(f"  {name:14s} seed={seed} {le}px {out.stat().st_size//1024}KB {time.time()-t0:.0f}s", flush=True)
                made += 1 if le >= FINAL_W else 0
                failed += 0 if le >= FINAL_W else 1
            except Exception as e:  # noqa: BLE001
                failed += 1
                print(f"  {name:14s} ERR {e}", flush=True)
    print(f"made={made} skipped={skipped} failed={failed}", flush=True)
    print(f"media -> {media_dir}\npublic -> {pub_dir}", flush=True)
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
