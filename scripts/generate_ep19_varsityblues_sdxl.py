#!/usr/bin/env python
"""Generate EP19 Operation Varsity Blues still candidates via local A1111 SDXL.

Local-only workflow:
- reads the EP19 prompt plan already extracted under H:\\pd-media
- generates missing candidate images with local A1111 txt2img
- writes 4K PNG candidates under one folder per prompt ID
- selects one candidate per ID with deterministic image-quality heuristics
- writes selection_index.json and a contact sheet

No external upload, no paid API, no publish/render step.
"""
from __future__ import annotations

import argparse
import base64
import datetime as dt
import hashlib
import io
import json
import math
import re
import shutil
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageStat


ROOT = Path(__file__).resolve().parent.parent
EPISODE_ID = "PD-2026-019-varsityblues"
MEDIA_BASE = Path(r"H:\pd-media\episodes") / EPISODE_ID / "05_visuals"
PLAN_PATH = MEDIA_BASE / "ep19_prompt_plan.json"
API = "http://127.0.0.1:7860"

MODEL_HINT = "juggernautXL_ragnarokBy"
SAMPLER = "DPM++ 2M Karras"
STEPS = 36
CFG = 5.7
WIDTH = 1344
HEIGHT = 768
HR_W = 2688
HR_H = 1536
FINAL_W = 3840
FINAL_H = 2160
UPSCALER = "R-ESRGAN 4x+"
BASE_SEED = 1901900

EXTRA_NEGATIVE = (
    "real person likeness, known actor, known celebrity, specific real campus, official seal, "
    "letterforms, typography, alphanumeric marks, printed words, readable marks, "
    "currency portrait, banknote design, license plate, house number, signature, "
    "deformed anatomy, bad hands, low quality"
)


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).astimezone().isoformat(timespec="seconds")


def request_json(path: str, payload: dict[str, Any] | None = None, timeout: int = 1200) -> Any:
    url = f"{API}/sdapi/v1/{path}"
    if payload is None:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def ensure_model() -> None:
    options = request_json("options", timeout=30)
    current = str(options.get("sd_model_checkpoint", ""))
    if MODEL_HINT.lower() in current.lower():
        return
    models = request_json("sd-models", timeout=30)
    pick = next((m["title"] for m in models if MODEL_HINT.lower() in m.get("title", "").lower()), None)
    if not pick:
        raise RuntimeError(f"SDXL model not found: {MODEL_HINT}")
    request_json("options", {"sd_model_checkpoint": pick}, timeout=180)


def ensure_plan() -> dict[str, Any]:
    if PLAN_PATH.exists():
        return json.loads(PLAN_PATH.read_text(encoding="utf-8"))

    src = ROOT / "episodes" / EPISODE_ID / "04_scenes" / "codex_image_prompts.v001.md"
    text = src.read_text(encoding="utf-8-sig")
    neg_match = re.search(r"## 2\. UNIVERSAL NEGATIVE.*?`(.*?)`", text, re.S)
    if not neg_match:
        raise RuntimeError("Universal negative not found")
    universal_negative = " ".join(neg_match.group(1).split())
    pat = re.compile(
        r"\*\*(EP19-IMG-\d{3})\s+·\s+([^·]+?)\s+·\s+([AB])\s+·\s+(\d+)\*\*\s*\n"
        r"(.*?)(?=\n\*\*EP19-IMG-|\n## 10\.|\Z)",
        re.S,
    )
    items = []
    for m in pat.finditer(text):
        items.append(
            {
                "id": m.group(1),
                "role": m.group(2).strip(),
                "priority": m.group(3),
                "candidate_count": int(m.group(4)),
                "prompt": " ".join(m.group(5).strip().split()),
                "universal_negative": universal_negative,
            }
        )
    MEDIA_BASE.mkdir(parents=True, exist_ok=True)
    plan = {
        "source": str(src),
        "total_ids": len(items),
        "total_candidates": sum(item["candidate_count"] for item in items),
        "items": items,
    }
    PLAN_PATH.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
    return plan


def final_prompt(item: dict[str, Any]) -> str:
    return (
        f"{item['prompt']}\n\n"
        "Prime Documentary brand palette: deep black and midnight-navy base, electric-blue #1F6BFF, "
        "muted gold #E5B53A, silver-grey highlights. Museum-grade cinematic symbolic documentary still, "
        "prestige investigative documentary, controlled motivated lighting, strong depth, fine film grain, "
        "16:9 landscape, one clear subject, intentional negative space for later Remotion typography. "
        "Do not create authentic news footage, surveillance footage, real documents, or real institutional identifiers."
    )


def final_negative(item: dict[str, Any]) -> str:
    return f"{item['universal_negative']}, {EXTRA_NEGATIVE}"


def decode_image(data: str) -> Image.Image:
    if "," in data:
        data = data.split(",", 1)[1]
    return Image.open(io.BytesIO(base64.b64decode(data))).convert("RGB")


def fit_4k(img: Image.Image) -> Image.Image:
    if img.size != (FINAL_W, FINAL_H):
        img = img.resize((FINAL_W, FINAL_H), Image.Resampling.LANCZOS)
    # Light finishing only: avoid changing content while reducing upscale softness.
    img = img.filter(ImageFilter.MedianFilter(size=3))
    img = img.filter(ImageFilter.UnsharpMask(radius=1.05, percent=110, threshold=3))
    return img


def generate_one(prompt: str, negative: str, seed: int) -> tuple[Image.Image, dict[str, Any]]:
    payload = {
        "prompt": prompt,
        "negative_prompt": negative,
        "seed": seed,
        "sampler_name": SAMPLER,
        "steps": STEPS,
        "cfg_scale": CFG,
        "width": WIDTH,
        "height": HEIGHT,
        "enable_hr": True,
        "denoising_strength": 0.22,
        "hr_resize_x": HR_W,
        "hr_resize_y": HR_H,
        "hr_upscaler": "Latent",
        "hr_second_pass_steps": 16,
        "save_images": False,
        "do_not_save_grid": True,
        "override_settings": {"sd_model_checkpoint": MODEL_HINT},
    }
    result = request_json("txt2img", payload, timeout=1800)
    first = result["images"][0]
    try:
        up = request_json(
            "extra-single-image",
            {
                "image": first,
                "resize_mode": 1,
                "upscaling_resize_w": FINAL_W,
                "upscaling_resize_h": FINAL_H,
                "upscaling_crop": True,
                "upscaler_1": UPSCALER,
            },
            timeout=900,
        )
        img = decode_image(up["image"])
        stage = "a1111-extra-upscale"
    except (urllib.error.URLError, TimeoutError, KeyError):
        img = fit_4k(decode_image(first))
        stage = "pillow-upscale-fallback"
    return img, {"seed": seed, "stage": stage}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def image_score(path: Path) -> tuple[float, dict[str, float]]:
    img = Image.open(path).convert("RGB")
    small = img.resize((384, 216), Image.Resampling.BILINEAR)
    stat = ImageStat.Stat(small)
    brightness = sum(stat.mean) / 3.0
    contrast = sum(stat.stddev) / 3.0
    edges = ImageStat.Stat(small.filter(ImageFilter.FIND_EDGES).convert("L")).mean[0]

    hsv = small.convert("HSV")
    pixels = list(hsv.getdata())
    blue = sum(1 for h, s, v in pixels if 135 <= h <= 175 and s > 70 and v > 55) / len(pixels)
    gold = sum(1 for h, s, v in pixels if 20 <= h <= 45 and s > 55 and v > 70) / len(pixels)
    too_dark_penalty = max(0.0, 35.0 - brightness) * 0.9
    too_bright_penalty = max(0.0, brightness - 185.0) * 0.4
    brand_bonus = min(18.0, (blue + gold) * 260.0)
    score = contrast * 1.15 + edges * 0.75 + brand_bonus - too_dark_penalty - too_bright_penalty
    metrics = {
        "brightness": round(brightness, 3),
        "contrast": round(contrast, 3),
        "edge_mean": round(edges, 3),
        "blue_ratio": round(blue, 5),
        "gold_ratio": round(gold, 5),
        "score": round(score, 3),
    }
    return score, metrics


def valid_png_4k(path: Path) -> bool:
    if not path.exists() or path.stat().st_size < 100_000:
        return False
    try:
        with Image.open(path) as img:
            return img.size == (FINAL_W, FINAL_H)
    except Exception:
        return False


def generate_candidates(items: list[dict[str, Any]], start_id: str | None, only_missing: bool, limit: int | None) -> None:
    selected_dir = MEDIA_BASE / "selected"
    selected_dir.mkdir(parents=True, exist_ok=True)
    ensure_model()

    started = start_id is None
    processed = 0
    for item in items:
        item_id = item["id"]
        if not started:
            started = item_id == start_id
        if not started:
            continue
        if limit is not None and processed >= limit:
            break
        selected_file = selected_dir / f"{item_id}.png"
        if only_missing and selected_file.exists():
            continue

        out_dir = MEDIA_BASE / item_id
        out_dir.mkdir(parents=True, exist_ok=True)
        records: list[dict[str, Any]] = []
        meta_file = out_dir / "candidates.json"
        if meta_file.exists():
            try:
                records = json.loads(meta_file.read_text(encoding="utf-8")).get("records", [])
            except json.JSONDecodeError:
                records = []

        count = int(item["candidate_count"])
        print(f"[id] {item_id} candidates={count} role={item['role']}", flush=True)
        prompt = final_prompt(item)
        negative = final_negative(item)
        for c in range(1, count + 1):
            out = out_dir / f"{item_id}_c{c:02d}.png"
            if valid_png_4k(out):
                print(f"  [skip] {out.name}", flush=True)
                continue
            seed = BASE_SEED + int(item_id.rsplit("-", 1)[1]) * 10_000 + c * 997
            last_error = None
            for attempt in range(1, 4):
                t0 = time.time()
                try:
                    img, gen_meta = generate_one(prompt, negative, seed + (attempt - 1) * 131)
                    img = fit_4k(img)
                    img.save(out, format="PNG", optimize=True)
                    score, metrics = image_score(out)
                    record = {
                        "candidate": c,
                        "file": str(out),
                        "sha256": sha256_file(out),
                        "seed": gen_meta["seed"],
                        "generator": "local-a1111-sdxl",
                        "model": MODEL_HINT,
                        "sampler": SAMPLER,
                        "steps": STEPS,
                        "cfg": CFG,
                        "size": [FINAL_W, FINAL_H],
                        "stage": gen_meta["stage"],
                        "generated_at": now_iso(),
                        "seconds": round(time.time() - t0, 1),
                        "auto_metrics": metrics,
                        "qc_status": "auto_pass_pending_visual_review",
                    }
                    records = [r for r in records if r.get("candidate") != c] + [record]
                    meta_file.write_text(
                        json.dumps({"id": item_id, "prompt": prompt, "negative": negative, "records": sorted(records, key=lambda r: r["candidate"])}, ensure_ascii=False, indent=2),
                        encoding="utf-8",
                    )
                    print(f"  [gen] {out.name} seed={record['seed']} score={score:.2f} {record['seconds']}s", flush=True)
                    break
                except Exception as exc:  # noqa: BLE001
                    last_error = exc
                    print(f"  [retry] {item_id} c{c:02d} attempt={attempt} error={exc}", flush=True)
                    time.sleep(5)
            else:
                fail = {
                    "candidate": c,
                    "file": str(out),
                    "qc_status": "generation_failed",
                    "error": str(last_error),
                    "generated_at": now_iso(),
                }
                records = [r for r in records if r.get("candidate") != c] + [fail]
                meta_file.write_text(
                    json.dumps({"id": item_id, "prompt": prompt, "negative": negative, "records": sorted(records, key=lambda r: r["candidate"])}, ensure_ascii=False, indent=2),
                    encoding="utf-8",
                )

        select_best(item)
        processed += 1


def select_best(item: dict[str, Any]) -> None:
    item_id = item["id"]
    out_dir = MEDIA_BASE / item_id
    selected_dir = MEDIA_BASE / "selected"
    selected_dir.mkdir(parents=True, exist_ok=True)
    candidates = sorted(out_dir.glob(f"{item_id}_c??.png"))
    scored = []
    for path in candidates:
        if valid_png_4k(path):
            score, metrics = image_score(path)
            scored.append((score, path, metrics))
    if not scored:
        append_exception(item_id, "no_valid_4k_candidate", "No valid 3840x2160 PNG candidate was generated.")
        return

    scored.sort(key=lambda row: row[0], reverse=True)
    _, best, metrics = scored[0]
    selected = selected_dir / f"{item_id}.png"
    shutil.copyfile(best, selected)

    index_path = MEDIA_BASE / "selection_index.json"
    if index_path.exists():
        index = json.loads(index_path.read_text(encoding="utf-8"))
    else:
        index = {"episode_id": EPISODE_ID, "generated_with": "local A1111 SDXL; local upscale/denoise", "selected": {}, "exceptions": []}
    index["generated_with"] = "mixed: EP19-IMG-001..006 Codex built-in; remaining local A1111 SDXL unless noted"
    index["updated_at"] = now_iso()
    index.setdefault("selected", {})[item_id] = {
        "chosen_file": str(selected),
        "source_candidate": str(best),
        "candidate_count_generated": len(scored),
        "auto_metrics": metrics,
        "qc": "auto-selected from valid 16:9 3840x2160 candidates; hard-rule visual review still recommended before edit lock",
        "origin": "local-a1111-sdxl",
        "license": "AI-generated symbolic reconstruction; rights review required before publication package",
    }
    index_path.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  [select] {item_id} <- {best.name} score={metrics['score']}", flush=True)


def append_exception(item_id: str, code: str, detail: str) -> None:
    index_path = MEDIA_BASE / "selection_index.json"
    if index_path.exists():
        index = json.loads(index_path.read_text(encoding="utf-8"))
    else:
        index = {"episode_id": EPISODE_ID, "generated_with": "local A1111 SDXL", "selected": {}, "exceptions": []}
    exceptions = index.setdefault("exceptions", [])
    if not any(e.get("id") == item_id and e.get("code") == code for e in exceptions):
        exceptions.append({"id": item_id, "code": code, "detail": detail, "ts": now_iso()})
    index["updated_at"] = now_iso()
    index_path.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")


def make_contact_sheet(items: list[dict[str, Any]]) -> Path:
    selected_dir = MEDIA_BASE / "selected"
    ids = [item["id"] for item in items]
    thumb_w, thumb_h = 320, 180
    label_h = 34
    cols = 8
    rows = math.ceil(len(ids) / cols)
    sheet = Image.new("RGB", (cols * thumb_w, rows * (thumb_h + label_h)), (11, 13, 18))
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("arial.ttf", 18)
    except Exception:
        font = None
    for idx, item_id in enumerate(ids):
        x = (idx % cols) * thumb_w
        y = (idx // cols) * (thumb_h + label_h)
        path = selected_dir / f"{item_id}.png"
        if path.exists():
            im = Image.open(path).convert("RGB")
            im.thumbnail((thumb_w, thumb_h), Image.Resampling.LANCZOS)
            sheet.paste(im, (x, y))
        else:
            draw.rectangle((x, y, x + thumb_w, y + thumb_h), fill=(32, 24, 24))
            draw.text((x + 12, y + 72), "MISSING", fill=(235, 90, 90), font=font)
        draw.rectangle((x, y + thumb_h, x + thumb_w, y + thumb_h + label_h), fill=(19, 23, 31))
        draw.text((x + 8, y + thumb_h + 7), item_id, fill=(229, 181, 58), font=font)
    out = MEDIA_BASE / "contact_sheet.selected.v001.png"
    sheet.save(out, quality=95)
    return out


def write_progress(items: list[dict[str, Any]], contact_sheet: str | None = None) -> None:
    selected_dir = MEDIA_BASE / "selected"
    selected = sorted(selected_dir.glob("EP19-IMG-*.png")) if selected_dir.exists() else []
    index_path = MEDIA_BASE / "selection_index.json"
    exceptions = []
    if index_path.exists():
        exceptions = json.loads(index_path.read_text(encoding="utf-8")).get("exceptions", [])
    completed_ids = [p.stem for p in selected]
    remaining = [item["id"] for item in items if item["id"] not in completed_ids]
    progress = {
        "episode_id": EPISODE_ID,
        "mode": "mixed; local A1111 SDXL used from EP19-IMG-007 onward",
        "updated_at": now_iso(),
        "completed_ids": completed_ids,
        "completed_id_count": len(completed_ids),
        "total_required_ids": len(items),
        "total_required_candidates": sum(int(item["candidate_count"]) for item in items),
        "remaining_ids": len(remaining),
        "remaining": remaining,
        "exceptions": exceptions,
        "contact_sheet": contact_sheet,
    }
    (MEDIA_BASE / "generation_progress.json").write_text(json.dumps(progress, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start-id", default="EP19-IMG-007")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--include-existing", action="store_true", help="Regenerate IDs even if selected file exists.")
    parser.add_argument("--select-only", action="store_true")
    parser.add_argument("--contact-sheet-only", action="store_true")
    args = parser.parse_args()

    plan = ensure_plan()
    items = plan["items"]
    if args.contact_sheet_only:
        sheet = make_contact_sheet(items)
        write_progress(items, str(sheet))
        print(json.dumps({"contact_sheet": str(sheet)}, ensure_ascii=False), flush=True)
        return 0
    if args.select_only:
        for item in items:
            select_best(item)
        sheet = make_contact_sheet(items)
        write_progress(items, str(sheet))
        return 0

    generate_candidates(items, args.start_id, not args.include_existing, args.limit)
    sheet = make_contact_sheet(items)
    write_progress(items, str(sheet))
    selected_count = len(list((MEDIA_BASE / "selected").glob("EP19-IMG-*.png")))
    print(json.dumps({"selected_count": selected_count, "contact_sheet": str(sheet), "progress": str(MEDIA_BASE / "generation_progress.json")}, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
