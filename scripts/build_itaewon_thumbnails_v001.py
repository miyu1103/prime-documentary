#!/usr/bin/env python3
"""Build the six EP74 Itaewon thumbnail candidates and a labelled contact sheet.

The generated plates are backgrounds only. All claims, typography, and the T02
four-of-eleven graphic are composited deterministically here. The script never
creates ``thumbnail.selected``; owner selection remains a separate approval gate.

    py -3.11 scripts/build_itaewon_thumbnails_v001.py
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

from check_thumb_subject_luma import measure as measure_readability


ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path("E:/pd-media/assets/ai/itaewon/_thumb_v001")
OUT = ROOT / "episodes" / "PD-2026-074-itaewon" / "10_thumbnail"
PROMPT_ORDER = ROOT / "episodes" / "_planning" / "EP74_itaewon_thumb_prompts.v001.md"
CACHE_ROOT = Path("C:/Users/aab15/.codex/generated_images/01a0203d-a45b-7612-a636-5c9c09e36e5d")
W, H = 1280, 720

GOLD = "#E5B53A"
BLUE = "#1F6BFF"
WHITE = "#F4F1E8"
INK = "#05070A"
MUTED = "#BFC5CC"
FONT_HEAD = ROOT / "remotion" / "public" / "fonts" / "Anton.ttf"
FONT_KICK = ROOT / "remotion" / "public" / "fonts" / "Oswald.ttf"


SPECS = {
    "T01": {
        "headline": ["3.2 METRES"],
        "kicker": "159 DIED IN THIS ALLEY",
        "accent": GOLD,
        "box": (60, 42, 1220, 292),
        "align": "center",
        "exposure": 1.38,
        "preliminary_qc": "reject",
        "qc_note": "Generated plate looks downhill; order requires the lower-end square-on view.",
    },
    "T02": {
        "headline": ["FOUR OF", "ELEVEN"],
        "kicker": "EVERY CALL SAID THE SAME THING",
        "accent": GOLD,
        "box": (500, 72, 1220, 648),
        "align": "right",
        "exposure": 1.85,
        "graphic": "four_of_eleven",
        "preliminary_qc": "accept",
    },
    "T03": {
        "headline": ["137 OFFICERS"],
        "kicker": "FOR A HUNDRED THOUSAND PEOPLE",
        "accent": BLUE,
        "box": (58, 445, 1222, 692),
        "align": "center",
        "exposure": 2.05,
        "preliminary_qc": "accept",
    },
    "T04": {
        "headline": ["NOBODY", "ORGANISED IT"],
        "kicker": "AND SO NOBODY HAD TO PLAN FOR IT",
        "accent": GOLD,
        "box": (90, 110, 1190, 610),
        "align": "center",
        "exposure": 1.16,
        "preliminary_qc": "accept",
    },
    "T05": {
        "headline": ["ELEVEN", "CALLS"],
        "kicker": "THE FIRST CAME AT 6:34",
        "accent": GOLD,
        "box": (58, 28, 760, 620),
        "align": "left",
        "exposure": 1.62,
        "scrim_alpha": 70,
        "preliminary_qc": "accept",
    },
    "T06": {
        "headline": ["NO LAW", "REQUIRED IT"],
        "kicker": "THE COURT SAID SO IN WRITING",
        "accent": GOLD,
        "box": (470, 70, 1220, 650),
        "align": "right",
        "exposure": 2.0,
        "preliminary_qc": "accept",
    },
}

TITLES = {
    "A": "Eleven People Called The Police Before 159 Died In That Itaewon Alley",
    "B": "Police Went To Four Of Eleven Warnings Before The Itaewon Crowd Crush",
    "C": "The Court Convicted The Police Chief And Acquitted The District In Itaewon",
    "D": "No Law Required Anyone To Plan For The Crowd That Filled That Itaewon Alley",
}

CACHE_SOURCES = {
    "T01": "exec-36856524-d4ac-437e-b06c-f843f7431446.png",
    "T02": "exec-86e1ad03-9488-4778-8486-fc2bc79308c6.png",
    "T03": "exec-0194509f-62d6-42e8-be95-40998b001fa6.png",
    "T04": "exec-065dbbc8-789c-4d28-a014-925c399c0aa6.png",
    "T05": "exec-32ed55ff-baec-4c17-a7c3-78864b45c3a4.png",
    "T06": "exec-0eda1995-17f6-4493-8c08-140e0e6f7567.png",
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def check_claims(field: str, value: str) -> dict:
    """Run the repository's strict factual-support checker and retain its blockers."""
    checker = ROOT / "scripts" / "check_packaging_claims.py"
    completed = subprocess.run(
        [sys.executable, str(checker), "--slug", "itaewon", f"--{field}", value, "--strict", "--json"],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
    if not completed.stdout.strip():
        raise RuntimeError(f"claims checker returned no JSON for {field}: {completed.stderr.strip()}")
    payload = json.loads(completed.stdout)
    blockers = [
        {"claim": row["claim"], "verdict": row["verdict"]}
        for row in payload.get("results", [])
        if row.get("verdict") != "SUPPORTED"
    ]
    return {
        "strict": True,
        "ok": bool(payload.get("ok")),
        "record_has_narration": bool(payload.get("record_has_narration")),
        "claims_checked": int(payload.get("claims_checked", 0)),
        "unsupported": int(payload.get("unsupported", 0)),
        "soft_unsupported": int(payload.get("soft_unsupported", 0)),
        "blockers": blockers,
    }


def write_generation_receipt() -> Path:
    mappings = []
    for asset_id, cache_name in CACHE_SOURCES.items():
        cache = CACHE_ROOT / cache_name
        destination = SOURCE / f"{asset_id}.generated.png"
        if not cache.is_file() or not destination.is_file():
            raise FileNotFoundError(f"generation mapping missing: {asset_id}: {cache} -> {destination}")
        cache_hash = sha256(cache)
        destination_hash = sha256(destination)
        if cache_hash != destination_hash:
            raise RuntimeError(f"generation mapping hash mismatch: {asset_id}")
        with Image.open(destination) as im:
            dimensions = [im.width, im.height]
        mappings.append({
            "id": asset_id,
            "cache_source": str(cache),
            "destination": str(destination),
            "sha256": destination_hash,
            "dimensions": dimensions,
        })
    receipt = {
        "schema_version": "pd_builtin_image_generation_receipt.v1",
        "episode_id": "PD-2026-074-itaewon",
        "revision": "v001",
        "provider": "Codex built-in image generation",
        "one_prompt_one_image": True,
        "prompt_order": PROMPT_ORDER.relative_to(ROOT).as_posix(),
        "generated_count": len(mappings),
        "mappings": mappings,
    }
    path = SOURCE / "generation_receipt.v001.json"
    path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    if not path.is_file():
        raise FileNotFoundError(path)
    return ImageFont.truetype(str(path), size)


def fit_background(path: Path, exposure: float) -> Image.Image:
    image = Image.open(path).convert("RGB")
    image = ImageOps.fit(image, (W, H), method=Image.Resampling.LANCZOS)
    image = ImageEnhance.Contrast(image).enhance(1.08)
    # Lift midtones without flattening the photograph, then keep every background
    # pixel below the readability gate's bright-core threshold. This leaves the
    # composited white kicker as the only >200-luma core and makes its dark rim
    # measurable instead of letting street lights zero the outline score.
    import numpy as np

    arr = np.asarray(image, dtype=np.float64) / 255.0
    arr = np.power(arr, 1.0 / exposure) * 255.0
    luma = 0.299 * arr[..., 0] + 0.587 * arr[..., 1] + 0.114 * arr[..., 2]
    scale = np.minimum(1.0, 188.0 / np.maximum(luma, 1.0))
    arr *= scale[..., None]
    image = Image.fromarray(np.clip(arr, 0, 255).astype("uint8"), "RGB")
    return image


def add_scrim(
    image: Image.Image,
    box: tuple[int, int, int, int],
    align: str,
    alpha: int | None = None,
) -> Image.Image:
    x0, y0, x1, y1 = box
    pad_x, pad_y = 52, 38
    mask = Image.new("L", (W, H), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle(
        (max(0, x0 - pad_x), max(0, y0 - pad_y), min(W, x1 + pad_x), min(H, y1 + pad_y)),
        radius=34,
        fill=alpha if alpha is not None else (118 if align != "center" else 102),
    )
    mask = mask.filter(ImageFilter.GaussianBlur(34))
    return Image.composite(Image.new("RGB", (W, H), (2, 4, 8)), image, mask)


def fit_headline(draw: ImageDraw.ImageDraw, lines: list[str], max_w: int, max_h: int) -> ImageFont.FreeTypeFont:
    for size in range(280, 83, -2):
        candidate = font(FONT_HEAD, size)
        boxes = [draw.textbbox((0, 0), line, font=candidate, stroke_width=14) for line in lines]
        max_line_w = max(box[2] - box[0] for box in boxes)
        line_h = max(box[3] - box[1] for box in boxes)
        total_h = len(lines) * line_h + max(0, len(lines) - 1) * 4
        if max_line_w <= max_w and total_h <= max_h:
            return candidate
    raise RuntimeError(f"headline does not fit: {' / '.join(lines)}")


def draw_copy(image: Image.Image, spec: dict) -> None:
    draw = ImageDraw.Draw(image)
    x0, y0, x1, y1 = spec["box"]
    headline = spec["headline"]
    kicker = spec["kicker"]
    align = spec["align"]
    head_font = fit_headline(draw, headline, x1 - x0, int((y1 - y0) * 0.74))
    kick_font = font(FONT_KICK, 32)
    hboxes = [draw.textbbox((0, 0), line, font=head_font, stroke_width=14) for line in headline]
    line_h = max(box[3] - box[1] for box in hboxes)
    headline_h = len(headline) * line_h + max(0, len(headline) - 1) * 4
    kbox = draw.textbbox((0, 0), kicker, font=kick_font, stroke_width=4)
    kw = kbox[2] - kbox[0]
    if align == "left":
        kx = x0
    elif align == "right":
        kx = x1 - kw
    else:
        kx = x0 + (x1 - x0 - kw) // 2
    total_h = headline_h + 22 + 50
    hy = y0 + max(0, (y1 - y0 - total_h) // 2)
    for line, hbox in zip(headline, hboxes):
        hw = hbox[2] - hbox[0]
        if align == "left":
            hx = x0
        elif align == "right":
            hx = x1 - hw
        else:
            hx = x0 + (x1 - x0 - hw) // 2
        draw.text((hx, hy - hbox[1]), line, font=head_font, fill=spec["accent"], stroke_width=14, stroke_fill=INK)
        hy += line_h + 4
    ky = hy + 18
    draw.rounded_rectangle((kx - 16, ky - 5, kx + kw + 16, ky + 43), radius=10, fill=(3, 6, 11, 224))
    draw.text((kx, ky), kicker, font=kick_font, fill=WHITE, stroke_width=14, stroke_fill=INK)


def draw_four_of_eleven(image: Image.Image) -> None:
    draw = ImageDraw.Draw(image)
    x0, y0 = 72, 128
    row_w, row_h, gap = 410, 23, 17
    for i in range(11):
        y = y0 + i * (row_h + gap)
        if i < 4:
            draw.rounded_rectangle((x0, y, x0 + row_w, y + row_h), radius=8, fill=GOLD)
        else:
            draw.rounded_rectangle((x0, y, x0 + row_w, y + row_h), radius=8, outline=(220, 225, 230), width=4)


def build_one(asset_id: str, spec: dict) -> tuple[Path, dict]:
    src = SOURCE / f"{asset_id}.generated.png"
    if not src.is_file():
        raise FileNotFoundError(src)
    image = fit_background(src, spec["exposure"])
    image = add_scrim(image, spec["box"], spec["align"], spec.get("scrim_alpha"))
    if spec.get("graphic") == "four_of_eleven":
        draw_four_of_eleven(image)
    draw_copy(image, spec)
    out = OUT / f"thumbnail.itaewon.{asset_id}.v001.png"
    image.save(out, format="PNG", optimize=True)
    readability = measure_readability(out)
    technical_ok = (
        readability["subject_luma"] >= 60
        and readability["text_height_px"] >= 150
        and readability["outline_px"] >= 12
    )
    thumb_text = f'{" ".join(spec["headline"])} | {spec["kicker"]}'
    return out, {
        "id": asset_id,
        "source_uri": f"artifact://media/assets/ai/itaewon/_thumb_v001/{asset_id}.generated.png",
        "source_sha256": sha256(src),
        "output": out.relative_to(ROOT).as_posix(),
        "output_sha256": sha256(out),
        "dimensions": [W, H],
        "headline": " ".join(spec["headline"]),
        "kicker": spec["kicker"],
        "accent": spec["accent"],
        "technical_qc": {"ok": technical_ok, **readability},
        "claim_check": check_claims("thumb-text", thumb_text),
        "preliminary_qc": spec["preliminary_qc"],
        "qc_note": spec.get("qc_note"),
    }


def contact_sheet(paths: list[tuple[Path, dict]]) -> Path:
    cols, panel_w, gap, pad, label_h = 3, 560, 18, 18, 54
    panel_h = round(panel_w * H / W)
    rows = (len(paths) + cols - 1) // cols
    sheet = Image.new(
        "RGB",
        (pad * 2 + cols * panel_w + (cols - 1) * gap,
         pad * 2 + rows * (panel_h + label_h) + (rows - 1) * gap),
        (15, 17, 22),
    )
    draw = ImageDraw.Draw(sheet)
    label_font = font(FONT_KICK, 28)
    for i, (path, record) in enumerate(paths):
        row, col = divmod(i, cols)
        x = pad + col * (panel_w + gap)
        y = pad + row * (panel_h + label_h + gap)
        panel = Image.open(path).convert("RGB").resize((panel_w, panel_h), Image.Resampling.LANCZOS)
        sheet.paste(panel, (x, y))
        verdict = record["preliminary_qc"].upper()
        color = "#56D364" if verdict == "ACCEPT" else "#FF5A5F"
        draw.text((x + 4, y + panel_h + 8), f'{record["id"]}  PRELIM {verdict}', font=label_font, fill=color)
    out = OUT / "thumbnail.itaewon.contact_sheet.v001.png"
    sheet.save(out, format="PNG", optimize=True)
    return out


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    receipt = write_generation_receipt()
    built: list[tuple[Path, dict]] = []
    for asset_id, spec in SPECS.items():
        path, record = build_one(asset_id, spec)
        built.append((path, record))
        print(f"{asset_id}: {path}  {record['preliminary_qc']}")
    sheet = contact_sheet(built)
    manifest = {
        "schema_version": "pd_thumbnail_candidates.v1",
        "episode_id": "PD-2026-074-itaewon",
        "revision": "v001",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "generator": "Codex built-in image generation",
        "builder": "scripts/build_itaewon_thumbnails_v001.py",
        "prompt_order": PROMPT_ORDER.relative_to(ROOT).as_posix(),
        "selection_status": "owner_selection_required",
        "package_lock_status": "blocked_by_strict_claim_check_and_owner_selection",
        "contact_sheet": sheet.relative_to(ROOT).as_posix(),
        "contact_sheet_sha256": sha256(sheet),
        "candidates": [record for _, record in built],
        "title_candidates": [
            {
                "id": title_id,
                "title": title,
                "characters": len(title),
                "claim_check": check_claims("title", title),
            }
            for title_id, title in TITLES.items()
        ],
    }
    manifest_path = OUT / "thumbnail_candidates.v001.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"contact: {sheet}")
    print(f"manifest: {manifest_path}")
    print(f"generation receipt: {receipt}")


if __name__ == "__main__":
    main()
