#!/usr/bin/env python3
"""Generate and QC EP16 Titan SDXL hero stills via local A1111.

This script is intentionally limited to image generation/registration for
PD-2026-016-titan. It does not touch audio, edit, render, publish, or other
episodes.
"""

from __future__ import annotations

import argparse
import base64
import datetime as dt
import hashlib
import json
import math
import os
import random
import re
import shutil
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import cv2
import numpy as np
import requests
from PIL import Image, ImageDraw, ImageStat


EPISODE_ID = "PD-2026-016-titan"
WIDTH = 1344
HEIGHT = 768
VARIATIONS = 6
TARGET_KEEP = 110


@dataclass
class PromptSpec:
    prompt_id: str
    title: str
    motion: str
    body: str


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def read_text(path: Path) -> str:
    for enc in ("utf-8-sig", "utf-8"):
        try:
            return path.read_text(encoding=enc)
        except UnicodeDecodeError:
            continue
    return path.read_text()


def parse_prompt_pack(path: Path) -> tuple[str, str, list[PromptSpec]]:
    text = read_text(path)
    base_match = re.search(r"\*\*BASE_SUFFIX\*\*.*?:\s*\r?\n`([^`]*)`", text, re.S)
    neg_match = re.search(r"\*\*NEG\*\*.*?:\s*\r?\n`([^`]*)`", text, re.S)
    if not base_match or not neg_match:
        raise RuntimeError(f"Could not parse BASE_SUFFIX/NEG from {path}")

    prompt_re = re.compile(
        r"^\*\*(T-IMG-\d{3})\s*/\s*([^*]+?)\*\*\s*[-—]\s*Motion:\s*(.*?)\r?\n`([^`]*)`",
        re.M | re.S,
    )
    prompts = [
        PromptSpec(
            prompt_id=m.group(1).strip(),
            title=m.group(2).strip(),
            motion=m.group(3).strip(),
            body=" ".join(m.group(4).strip().split()),
        )
        for m in prompt_re.finditer(text)
    ]
    if len(prompts) != 76:
        raise RuntimeError(f"Expected 76 prompts, parsed {len(prompts)}")
    expected = [f"T-IMG-{i:03d}" for i in range(1, 77)]
    actual = [p.prompt_id for p in prompts]
    if actual != expected:
        raise RuntimeError(f"Prompt IDs are not contiguous: {actual[:3]} ... {actual[-3:]}")
    return base_match.group(1).strip(), neg_match.group(1).strip(), prompts


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def valid_image(path: Path) -> bool:
    if not path.exists() or path.stat().st_size < 50_000:
        return False
    try:
        with Image.open(path) as img:
            return img.size == (WIDTH, HEIGHT) and img.mode in {"RGB", "RGBA"}
    except Exception:
        return False


def image_path(hero_dir: Path, prompt_id: str, variation: int) -> Path:
    return hero_dir / f"{prompt_id}_v{variation}.png"


def existing_image_path(hero_dir: Path, candidates_dir: Path, prompt_id: str, variation: int) -> Path:
    root_path = image_path(hero_dir, prompt_id, variation)
    if valid_image(root_path):
        return root_path
    candidate_path = candidates_dir / root_path.name
    if valid_image(candidate_path):
        return candidate_path
    return root_path


def all_six_valid(hero_dir: Path, prompt_id: str) -> bool:
    return all(valid_image(image_path(hero_dir, prompt_id, v)) for v in range(1, VARIATIONS + 1))


def post_json(url: str, payload: dict[str, Any], timeout: int) -> dict[str, Any]:
    resp = requests.post(url, json=payload, timeout=timeout)
    resp.raise_for_status()
    return resp.json()


def get_json(url: str, timeout: int) -> dict[str, Any]:
    resp = requests.get(url, timeout=timeout)
    resp.raise_for_status()
    return resp.json()


def ensure_a1111(base_url: str, checkpoint: str) -> str:
    options = get_json(f"{base_url}/sdapi/v1/options", timeout=10)
    current = str(options.get("sd_model_checkpoint", ""))
    if checkpoint not in current:
        post_json(
            f"{base_url}/sdapi/v1/options",
            {"sd_model_checkpoint": checkpoint},
            timeout=120,
        )
        time.sleep(2)
        current = str(get_json(f"{base_url}/sdapi/v1/options", timeout=10).get("sd_model_checkpoint", ""))
    if checkpoint not in current:
        raise RuntimeError(f"A1111 checkpoint mismatch. wanted={checkpoint!r} current={current!r}")
    return current


def generate_one(
    base_url: str,
    prompt: str,
    negative: str,
    out_path: Path,
    checkpoint: str,
    seed: int,
) -> dict[str, Any]:
    payload = {
        "prompt": prompt,
        "negative_prompt": negative,
        "width": WIDTH,
        "height": HEIGHT,
        "steps": 34,
        "cfg_scale": 5.5,
        "sampler_name": "DPM++ 2M Karras",
        "seed": seed,
        "batch_size": 1,
        "n_iter": 1,
        "restore_faces": False,
        "tiling": False,
        "enable_hr": False,
        "save_images": False,
        "override_settings": {"sd_model_checkpoint": checkpoint},
    }
    result = post_json(f"{base_url}/sdapi/v1/txt2img", payload, timeout=900)
    images = result.get("images") or []
    if not images:
        raise RuntimeError("A1111 returned no images")
    encoded = images[0]
    if "," in encoded and encoded[:32].lower().startswith("data:image"):
        encoded = encoded.split(",", 1)[1]
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(base64.b64decode(encoded))
    if not valid_image(out_path):
        raise RuntimeError(f"Generated image is invalid: {out_path}")

    info = {}
    raw_info = result.get("info")
    if isinstance(raw_info, str):
        try:
            info = json.loads(raw_info)
        except json.JSONDecodeError:
            info = {"raw": raw_info[:5000]}
    return {
        "path": str(out_path),
        "seed": info.get("seed", seed),
        "sha256": sha256_file(out_path),
        "bytes": out_path.stat().st_size,
    }


def create_contact_sheet(hero_dir: Path, contact_dir: Path, prompt_id: str) -> Path | None:
    paths = [image_path(hero_dir, prompt_id, v) for v in range(1, VARIATIONS + 1)]
    if not all(valid_image(p) for p in paths):
        return None
    contact_dir.mkdir(parents=True, exist_ok=True)
    thumb_w = WIDTH // 3
    thumb_h = HEIGHT // 3
    sheet = Image.new("RGB", (thumb_w * 3, thumb_h * 2), (4, 7, 12))
    for idx, path in enumerate(paths):
        with Image.open(path) as img:
            thumb = img.convert("RGB").resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        sheet.paste(thumb, ((idx % 3) * thumb_w, (idx // 3) * thumb_h))
    out = contact_dir / f"{prompt_id}.jpg"
    sheet.save(out, "JPEG", quality=92, optimize=True)
    return out


def laplacian_variance(img: Image.Image) -> float:
    arr = np.array(img.convert("L"))
    return float(cv2.Laplacian(arr, cv2.CV_64F).var())


def avg_hash(img: Image.Image, size: int = 16) -> int:
    gray = img.convert("L").resize((size, size), Image.Resampling.BILINEAR)
    arr = np.asarray(gray, dtype=np.float32)
    mean = float(arr.mean())
    bits = (arr > mean).flatten()
    value = 0
    for bit in bits:
        value = (value << 1) | int(bit)
    return value


def hamming(a: int, b: int) -> int:
    return int((a ^ b).bit_count())


def detect_faces(img: Image.Image) -> int:
    gray = np.array(img.convert("L"))
    cascade_path = Path(cv2.data.haarcascades) / "haarcascade_frontalface_default.xml"
    cascade = cv2.CascadeClassifier(str(cascade_path))
    if cascade.empty():
        return 0
    faces = cascade.detectMultiScale(gray, scaleFactor=1.08, minNeighbors=5, minSize=(64, 64))
    return int(len(faces))


def image_metrics(path: Path) -> dict[str, Any]:
    with Image.open(path) as img:
        rgb = img.convert("RGB")
        blur = laplacian_variance(rgb)
        hsv = rgb.convert("HSV")
        stat = ImageStat.Stat(hsv)
        sat_mean = float(stat.mean[1])
        sat_extreme = float((np.asarray(hsv)[:, :, 1] > 235).mean())
        brightness = float(ImageStat.Stat(rgb.convert("L")).mean[0])
        face_count = detect_faces(rgb)
        ah = avg_hash(rgb)
    return {
        "blur": blur,
        "sat_mean": sat_mean,
        "sat_extreme_ratio": sat_extreme,
        "brightness": brightness,
        "face_count": face_count,
        "avg_hash": ah,
    }


def score_metrics(metrics: dict[str, Any]) -> tuple[float, list[str]]:
    reasons: list[str] = []
    blur = float(metrics["blur"])
    sat_mean = float(metrics["sat_mean"])
    sat_extreme = float(metrics["sat_extreme_ratio"])
    brightness = float(metrics["brightness"])
    face_count = int(metrics["face_count"])

    if blur < 18:
        reasons.append("blurry")
    # Titan's art direction intentionally uses electric blue and gold. Treat
    # only truly clipped/neon frames as rejects; rank the rest by score.
    if sat_extreme > 0.92 or sat_mean > 248:
        reasons.append("oversaturated")
    if face_count > 0:
        reasons.append("face_detected")
    if brightness < 10:
        reasons.append("too_dark")

    score = 0.0
    score += min(blur / 130.0, 1.2) * 45.0
    score += max(0.0, 1.0 - abs(sat_mean - 82.0) / 90.0) * 25.0
    score += max(0.0, 1.0 - abs(brightness - 78.0) / 80.0) * 20.0
    score += max(0.0, 1.0 - sat_extreme / 0.18) * 10.0
    score -= face_count * 100.0
    return score, reasons


def load_generation_log(path: Path) -> dict[str, dict[str, Any]]:
    if not path.exists():
        return {}
    records: dict[str, dict[str, Any]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        key = f"{rec.get('prompt_id')}:{rec.get('variation')}"
        records[key] = rec
    return records


def append_jsonl(path: Path, record: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def qc_images(hero_dir: Path, candidates_dir: Path, prompts: list[PromptSpec], log_path: Path) -> dict[str, Any]:
    generation_log = load_generation_log(log_path)
    candidates_dir.mkdir(parents=True, exist_ok=True)
    by_prompt: dict[str, list[dict[str, Any]]] = {}
    rejected: list[dict[str, Any]] = []

    for spec in prompts:
        entries = []
        for v in range(1, VARIATIONS + 1):
            path = existing_image_path(hero_dir, candidates_dir, spec.prompt_id, v)
            if not valid_image(path):
                rejected.append(
                    {
                        "prompt_id": spec.prompt_id,
                        "variation": v,
                        "file": str(path),
                        "gate": "missing_or_invalid",
                    }
                )
                continue
            metrics = image_metrics(path)
            score, reasons = score_metrics(metrics)
            key = f"{spec.prompt_id}:{v}"
            log_rec = generation_log.get(key, {})
            entries.append(
                {
                    "prompt_id": spec.prompt_id,
                    "variation": v,
                    "file": str(path),
                    "filename": path.name,
                    "score": score,
                    "reasons": reasons,
                    "metrics": {k: val for k, val in metrics.items() if k != "avg_hash"},
                    "avg_hash": metrics["avg_hash"],
                    "seed": log_rec.get("seed"),
                    "sha256": sha256_file(path),
                    "bytes": path.stat().st_size,
                }
            )
        by_prompt[spec.prompt_id] = entries

    keep_keys: set[tuple[str, int]] = set()
    prompt_status: dict[str, dict[str, Any]] = {}

    for spec in prompts:
        entries = by_prompt[spec.prompt_id]
        viable = [e for e in entries if not e["reasons"]]
        if not viable:
            viable = sorted(entries, key=lambda e: e["score"], reverse=True)[:1]
            prompt_status[spec.prompt_id] = {"status": "needs_review", "kept": len(viable), "reason": "no_clean_candidate"}
        else:
            prompt_status[spec.prompt_id] = {"status": "ok", "kept": 1, "reason": "clean_candidate"}

        selected: list[dict[str, Any]] = []
        for entry in sorted(viable, key=lambda e: e["score"], reverse=True):
            if any(hamming(int(entry["avg_hash"]), int(prev["avg_hash"])) <= 10 for prev in selected):
                entry["reasons"].append("near_duplicate")
                continue
            selected.append(entry)
            break
        if not selected and viable:
            selected.append(sorted(viable, key=lambda e: e["score"], reverse=True)[0])
        for entry in selected:
            keep_keys.add((entry["prompt_id"], entry["variation"]))

    second_candidates: list[dict[str, Any]] = []
    for spec in prompts:
        selected_hashes = [
            int(e["avg_hash"])
            for e in by_prompt[spec.prompt_id]
            if (e["prompt_id"], e["variation"]) in keep_keys
        ]
        for entry in by_prompt[spec.prompt_id]:
            key = (entry["prompt_id"], entry["variation"])
            if key in keep_keys or entry["reasons"]:
                continue
            if any(hamming(int(entry["avg_hash"]), h) <= 10 for h in selected_hashes):
                entry["reasons"].append("near_duplicate")
                continue
            second_candidates.append(entry)

    need_second = max(0, TARGET_KEEP - len(keep_keys))
    for entry in sorted(second_candidates, key=lambda e: e["score"], reverse=True)[:need_second]:
        keep_keys.add((entry["prompt_id"], entry["variation"]))
        prompt_status[entry["prompt_id"]]["kept"] += 1

    kept: list[dict[str, Any]] = []
    for spec in prompts:
        for entry in by_prompt[spec.prompt_id]:
            key = (entry["prompt_id"], entry["variation"])
            src = Path(entry["file"])
            if key in keep_keys:
                if src.parent == candidates_dir:
                    dest = hero_dir / src.name
                    if dest.exists():
                        dest.unlink()
                    shutil.move(str(src), str(dest))
                    entry["file"] = str(dest)
                    src = dest
                entry["gate"] = "usable"
                entry["sha256"] = sha256_file(src)
                entry["bytes"] = src.stat().st_size
                entry.pop("avg_hash", None)
                kept.append(entry)
            else:
                if not entry["reasons"]:
                    entry["reasons"] = ["ranked_out"]
                dest = candidates_dir / src.name
                if src.exists() and src.resolve() != dest.resolve():
                    if dest.exists():
                        dest.unlink()
                    shutil.move(str(src), str(dest))
                entry["gate"] = "rejected"
                entry["file"] = str(dest)
                entry.pop("avg_hash", None)
                rejected.append(entry)

    return {
        "generated_at": now_iso(),
        "kept": kept,
        "rejected": rejected,
        "prompt_status": prompt_status,
        "counts": {
            "kept": len(kept),
            "rejected": len(rejected),
            "needs_review": sum(1 for s in prompt_status.values() if s["status"] != "ok"),
        },
    }


def artifact_uri(filename: str) -> str:
    return f"artifact://episodes/{EPISODE_ID}/05_stock/hero/{filename}"


def write_usable_assets(
    usable_path: Path,
    kept: list[dict[str, Any]],
    prompts_by_id: dict[str, PromptSpec],
) -> None:
    usable_path.parent.mkdir(parents=True, exist_ok=True)
    assets = []
    for entry in sorted(kept, key=lambda e: (e["prompt_id"], e["variation"])):
        prompt_id = entry["prompt_id"]
        spec = prompts_by_id[prompt_id]
        assets.append(
            {
                "asset_id": f"PD16-{prompt_id}-V{entry['variation']}",
                "asset_type": "image",
                "source": "generated",
                "sourceTool": "sdxl",
                "source_url": None,
                "author": "local A1111 Stable Diffusion WebUI",
                "license": "generated",
                "commercial_use": "allowed",
                "file": artifact_uri(entry["filename"]),
                "sha256": entry["sha256"],
                "bytes": entry["bytes"],
                "width": WIDTH,
                "height": HEIGHT,
                "query": prompt_id,
                "source_prompt_id": prompt_id,
                "depicts": spec.title,
                "motion_hint": spec.motion,
                "seed": entry.get("seed"),
                "generated_at": now_iso(),
                "used_in_spans": [],
                "gate": "usable",
                "gate_reason": "qc_keep",
                "disclosure": True,
            }
        )
    payload = {
        "schema_version": "1.0.0",
        "episode_id": EPISODE_ID,
        "revision": "v001",
        "kind": "usable",
        "generated_at": now_iso(),
        "assets": assets,
    }
    usable_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_asset_manifest(
    manifest_path: Path,
    kept: list[dict[str, Any]],
    prompts_by_id: dict[str, PromptSpec],
    negative: str,
) -> None:
    if manifest_path.exists():
        payload = json.loads(read_text(manifest_path))
    else:
        payload = {"schema": "asset-manifest/v1", "assets": []}
    assets = payload.setdefault("assets", [])
    assets = [
        a
        for a in assets
        if not str(a.get("id", "")).startswith("PD16-T-IMG-")
        and EPISODE_ID not in (a.get("tags") or [])
        and a.get("subtype") != "titan_hero"
    ]

    max_bg = 0
    for asset in assets:
        m = re.match(r"^AF-BG-(\d+)$", str(asset.get("id", "")))
        if m:
            max_bg = max(max_bg, int(m.group(1)))

    for entry in sorted(kept, key=lambda e: (e["prompt_id"], e["variation"])):
        max_bg += 1
        prompt_id = entry["prompt_id"]
        spec = prompts_by_id[prompt_id]
        assets.append(
            {
                "id": f"AF-BG-{max_bg:04d}",
                "type": "backgrounds",
                "subtype": "titan_sdxl",
                "path": artifact_uri(entry["filename"]),
                "previewPath": artifact_uri(entry["filename"]),
                "sourceTool": "sdxl",
                "source": "generated",
                "kind": "image",
                "width": WIDTH,
                "height": HEIGHT,
                "hasAlpha": False,
                "loopable": False,
                "durationFrames": None,
                "fps": None,
                "mood": "somber",
                "intensity": "strong",
                "useCases": ["backgrounds", "episode_hero"],
                "compatibleSceneTypes": ["reenactment", "abstract_emotion", "emotional_pause"],
                "colorTone": "high_contrast",
                "tags": [EPISODE_ID, "titan", "hero", prompt_id],
                "sourcePrompt": prompt_id,
                "negativePrompt": negative,
                "seed": entry.get("seed"),
                "model": "juggernautXL_ragnarokBy",
                "license": "generated_owned",
                "licenseOriginal": "generated",
                "sourceUrl": "",
                "sha256": str(entry["sha256"]).removeprefix("sha256:"),
                "bytes": entry["bytes"],
                "notes": f"Illustrative symbolic generated asset; disclosure=true; depicts={spec.title}",
                "disclosure": True,
            }
        )
    payload["assets"] = assets
    manifest_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default=r"C:\Users\aab15\Documents\prime-documentary")
    parser.add_argument("--media-root", default=fr"H:\pd-media\episodes\{EPISODE_ID}\05_stock\hero")
    parser.add_argument("--a1111", default="http://127.0.0.1:7860")
    parser.add_argument("--checkpoint", default="juggernautXL_ragnarokBy")
    parser.add_argument("--generate-only", action="store_true")
    parser.add_argument("--qc-only", action="store_true")
    parser.add_argument("--force", action="store_true", help="Regenerate all variations regardless of existing files")
    args = parser.parse_args()

    repo = Path(args.repo)
    episode_dir = repo / "episodes" / EPISODE_ID
    prompt_path = episode_dir / "04_scenes" / "ai_prompts.v001.md"
    usable_path = episode_dir / "05_stock" / "usable_assets.v001.json"
    manifest_path = repo / "assets" / "asset_manifest.v001.json"
    hero_dir = Path(args.media_root)
    contact_dir = hero_dir / "_contact"
    candidates_dir = hero_dir / "candidates"
    log_path = hero_dir / "_generation_log.jsonl"
    qc_report_path = hero_dir / "_qc_report.v001.json"

    base_suffix, negative, prompts = parse_prompt_pack(prompt_path)
    prompts_by_id = {p.prompt_id: p for p in prompts}
    hero_dir.mkdir(parents=True, exist_ok=True)
    contact_dir.mkdir(parents=True, exist_ok=True)
    candidates_dir.mkdir(parents=True, exist_ok=True)

    generated = 0
    skipped_prompts = 0
    failed: list[dict[str, Any]] = []

    if not args.qc_only:
        try:
            current_checkpoint = ensure_a1111(args.a1111, args.checkpoint)
            print(f"A1111 OK checkpoint={current_checkpoint}", flush=True)
        except Exception as exc:
            existing = sum(1 for p in prompts for v in range(1, VARIATIONS + 1) if valid_image(image_path(hero_dir, p.prompt_id, v)))
            print(f"A1111 unavailable before generation. valid_images={existing}/456 error={exc}", file=sys.stderr)
            return 2

        for idx, spec in enumerate(prompts, start=1):
            if not args.force and all_six_valid(hero_dir, spec.prompt_id):
                skipped_prompts += 1
                create_contact_sheet(hero_dir, contact_dir, spec.prompt_id)
                print(f"[{idx:02d}/76] skip {spec.prompt_id}: 6 valid images", flush=True)
                continue

            full_prompt = f"{spec.body}{base_suffix}"
            print(f"[{idx:02d}/76] generate {spec.prompt_id}: {spec.title}", flush=True)
            for variation in range(1, VARIATIONS + 1):
                out_path = image_path(hero_dir, spec.prompt_id, variation)
                if not args.force and valid_image(out_path):
                    continue
                seed = random.randint(1, 2_147_483_000)
                try:
                    rec = generate_one(args.a1111, full_prompt, negative, out_path, args.checkpoint, seed)
                    rec.update(
                        {
                            "time": now_iso(),
                            "episode_id": EPISODE_ID,
                            "prompt_id": spec.prompt_id,
                            "variation": variation,
                            "title": spec.title,
                            "sourceTool": "sdxl",
                            "width": WIDTH,
                            "height": HEIGHT,
                        }
                    )
                    append_jsonl(log_path, rec)
                    generated += 1
                    print(f"  v{variation}: seed={rec['seed']} sha={rec['sha256'][:19]}", flush=True)
                except Exception as exc:
                    failed.append({"prompt_id": spec.prompt_id, "variation": variation, "error": str(exc)})
                    existing = sum(1 for p in prompts for v in range(1, VARIATIONS + 1) if valid_image(image_path(hero_dir, p.prompt_id, v)))
                    status = {
                        "time": now_iso(),
                        "generated_this_run": generated,
                        "valid_images": existing,
                        "failed": failed,
                    }
                    (hero_dir / "_generation_failed.json").write_text(
                        json.dumps(status, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8",
                    )
                    print(f"FAILED after generated_this_run={generated} valid_images={existing}/456", file=sys.stderr)
                    print(f"{spec.prompt_id} v{variation}: {exc}", file=sys.stderr)
                    return 3
            create_contact_sheet(hero_dir, contact_dir, spec.prompt_id)

    if not args.generate_only:
        print("QC start", flush=True)
        qc = qc_images(hero_dir, candidates_dir, prompts, log_path)
        write_usable_assets(usable_path, qc["kept"], prompts_by_id)
        update_asset_manifest(manifest_path, qc["kept"], prompts_by_id, negative)
        qc["generation"] = {
            "generated_this_run": generated,
            "skipped_prompts": skipped_prompts,
            "failed": failed,
            "raw_output": str(hero_dir),
            "contact_output": str(contact_dir),
            "candidates_output": str(candidates_dir),
            "usable_assets": str(usable_path),
            "asset_manifest": str(manifest_path),
        }
        qc_report_path.write_text(json.dumps(qc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(
            f"QC done kept={qc['counts']['kept']} rejected={qc['counts']['rejected']} "
            f"needs_review={qc['counts']['needs_review']}",
            flush=True,
        )
        print(f"usable_assets={usable_path}", flush=True)
        print(f"qc_report={qc_report_path}", flush=True)

    print(f"DONE generated_this_run={generated} skipped_prompts={skipped_prompts}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
