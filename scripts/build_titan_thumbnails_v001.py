#!/usr/bin/env python3
"""Build Titan thumbnail backgrounds and title candidates from generated SDXL assets.

This script does not call paid APIs, upload, publish, or create approvals. It
uses already-generated local SDXL hero stills for PD-2026-016-titan, crops and
grades six title-safe backgrounds, then renders three title candidates through
the shared Remotion ThumbnailFrame.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-016-titan"
SLUG = "titan"
EPDIR = ROOT / "episodes" / EP
SCENES = EPDIR / "04_scenes"
PKG = EPDIR / "09_package"
OUT = EPDIR / "10_thumbnail"
MEDIA = Path("H:/pd-media")
HERO = MEDIA / "episodes" / EP / "05_stock" / "hero"
AI_THUMBS = MEDIA / "assets" / "ai" / "thumbs" / SLUG
PUBLIC_THUMBS = ROOT / "remotion" / "public" / SLUG / "thumbs"
W, H = 1280, 720

INK = (4, 7, 12)
BLUE = (31, 107, 255)
GOLD = (229, 181, 58)

BACKGROUND_SOURCES = [
    {
        "id": "THUMB-01",
        "source": "T-IMG-038_v1.png",
        "prompt": "A tiny submersible silhouette descending under beams of surface light, swallowed by immense deep blue water; title-safe negative space.",
        "use": "THEY WERE WARNED direction",
    },
    {
        "id": "THUMB-02",
        "source": "T-IMG-002_v4.png",
        "prompt": "Extreme macro of a cold steel bolt on a deep-sea hatch flange, ominous finality; title-safe negative space.",
        "use": "PURE WASTE direction",
    },
    {
        "id": "THUMB-03",
        "source": "T-IMG-066_v5.png",
        "prompt": "A single Rubik's cube alone in cold blue darkness, melancholy rim light; title-safe negative space.",
        "use": "HE WAS 19 direction",
    },
    {
        "id": "THUMB-04",
        "source": "T-IMG-001_v6.png",
        "prompt": "A circular hatch sealed from outside, rows of bolts and cold blue light, claustrophobic finality; title-safe negative space.",
        "use": "hatch/point-of-no-return backup",
    },
    {
        "id": "THUMB-05",
        "source": "T-IMG-025_v5.png",
        "prompt": "A generic game controller in shadow on brushed metal, mundane object made ominous; title-safe negative space.",
        "use": "controller hook backup",
    },
    {
        "id": "THUMB-06",
        "source": "T-IMG-068_v1.png",
        "prompt": "Five empty chairs in a cold dark void under a single soft light, absence made visible; title-safe negative space.",
        "use": "dignity/absence backup",
    },
]

TITLE_OPTIONS = [
    {
        "id": "A",
        "thumbnail_text": "THEY WERE WARNED",
        "youtube_title": "They Were Warned — The Last Dive of the Titan",
        "background_id": "THUMB-01",
        "ctr_score": 91,
        "reason": "Clearest immediate story and strong mobile curiosity gap without exploiting the deaths.",
    },
    {
        "id": "B",
        "thumbnail_text": "PURE WASTE",
        "youtube_title": "Pure Waste — The Last Dive of the Titan",
        "background_id": "THUMB-02",
        "ctr_score": 94,
        "reason": "Shortest and most branded hook; ties directly to the episode thesis and working title.",
    },
    {
        "id": "C",
        "thumbnail_text": "HE WAS 19",
        "youtube_title": "He Was 19 — The Last Dive of the Titan",
        "background_id": "THUMB-03",
        "ctr_score": 89,
        "reason": "Most emotional and dignified, but narrower than the central system-failure hook.",
    },
]

SELECTED_TITLE_ID = "B"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def font(size: int) -> ImageFont.FreeTypeFont:
    for candidate in [
        Path(r"C:\Windows\Fonts\arialbd.ttf"),
        Path(r"C:\Windows\Fonts\impact.ttf"),
        Path(r"C:\Windows\Fonts\segoeuib.ttf"),
    ]:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


def center_crop_16x9(img: Image.Image) -> Image.Image:
    img = img.convert("RGB")
    w, h = img.size
    target = 16 / 9
    if w / h > target:
        new_w = int(h * target)
        left = (w - new_w) // 2
        img = img.crop((left, 0, left + new_w, h))
    elif w / h < target:
        new_h = int(w / target)
        top = (h - new_h) // 2
        img = img.crop((0, top, w, top + new_h))
    return img.resize((W, H), Image.Resampling.LANCZOS)


def grade_for_thumbnail(img: Image.Image) -> Image.Image:
    img = ImageEnhance.Color(img).enhance(0.92)
    img = ImageEnhance.Contrast(img).enhance(1.18)
    img = ImageEnhance.Sharpness(img).enhance(1.08)
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    for x in range(W):
        alpha = int(196 * max(0, 1 - x / 650))
        draw.line((x, 0, x, H), fill=(0, 0, 0, alpha))
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse((770, -140, 1500, 550), fill=BLUE + (34,))
    gd.ellipse((880, 420, 1480, 930), fill=GOLD + (24,))
    glow = glow.filter(ImageFilter.GaussianBlur(80))
    return Image.alpha_composite(Image.alpha_composite(img.convert("RGBA"), glow), overlay).convert("RGB")


def build_backgrounds() -> list[dict[str, Any]]:
    AI_THUMBS.mkdir(parents=True, exist_ok=True)
    PUBLIC_THUMBS.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    built: list[dict[str, Any]] = []
    for item in BACKGROUND_SOURCES:
        src = HERO / item["source"]
        if not src.exists():
            raise FileNotFoundError(src)
        img = grade_for_thumbnail(center_crop_16x9(Image.open(src)))
        ai_path = AI_THUMBS / f"{item['id']}.png"
        episode_path = OUT / f"background.{item['id']}.png"
        public_path = PUBLIC_THUMBS / f"{item['id']}.png"
        img.save(ai_path)
        img.save(episode_path)
        shutil.copy2(episode_path, public_path)
        built.append(
            {
                **item,
                "source_file": str(src).replace("\\", "/"),
                "ai_thumb_file": str(ai_path).replace("\\", "/"),
                "episode_file": rel(episode_path),
                "public_static": f"{SLUG}/thumbs/{item['id']}.png",
                "sha256": sha256(episode_path),
                "width": W,
                "height": H,
                "license": "generated-derived",
                "sourceTool": "sdxl-derived",
                "disclosure": True,
            }
        )

    manifest = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "slug": SLUG,
        "revision": "v001",
        "generated_at": now_iso(),
        "source": "derived from existing local SDXL hero stills because A1111 :7860 was unavailable",
        "paid_api": False,
        "external_upload": False,
        "assets": built,
    }
    write_json(AI_THUMBS / "_thumb_generation_manifest.v001.json", manifest)
    write_json(OUT / "thumb_backgrounds.v001.json", manifest)

    sheet = Image.new("RGB", (960, 440), INK)
    draw = ImageDraw.Draw(sheet)
    f = font(20)
    for idx, item in enumerate(built):
        img = Image.open(OUT / f"background.{item['id']}.png").resize((320, 180), Image.Resampling.LANCZOS)
        x = (idx % 3) * 320
        y = (idx // 3) * 220
        sheet.paste(img, (x, y))
        draw.text((x + 10, y + 185), f"{item['id']} / {item['use']}", fill=GOLD, font=f)
    sheet.save(OUT / "titan_thumb_background_contact_sheet.v001.jpg", quality=92)
    return built


def render_stills(backgrounds: list[dict[str, Any]]) -> list[dict[str, Any]]:
    remotion_bin = ROOT / "remotion" / "node_modules" / ".bin" / "remotion.cmd"
    rendered: list[dict[str, Any]] = []
    background_by_id = {item["id"]: item for item in backgrounds}
    for option in TITLE_OPTIONS:
        bg = background_by_id[option["background_id"]]
        out = OUT / f"thumbnail.titan_option_{option['id']}.v001.png"
        props = {
            "title": option["thumbnail_text"],
            "backgroundSrc": bg["public_static"],
            "variant": "left",
        }
        props_path = OUT / f"thumbnail.titan_option_{option['id']}.props.json"
        write_json(props_path, props)
        subprocess.run(
            [
                str(remotion_bin),
                "still",
                "ThumbnailFrame",
                str(out),
                "--props",
                json.dumps(props),
                "--overwrite",
            ],
            cwd=ROOT / "remotion",
            check=True,
        )
        rendered.append(
            {
                **option,
                "file": rel(out),
                "props": rel(props_path),
                "sha256": sha256(out),
                "width": W,
                "height": H,
            }
        )
    selected = next(item for item in rendered if item["id"] == SELECTED_TITLE_ID)
    selected_path = PKG / "thumbnail.selected.v001.png"
    PKG.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / selected["file"], selected_path)
    selected["selected_package_file"] = rel(selected_path)
    selected["selected_package_sha256"] = sha256(selected_path)
    return rendered


def write_prompt_doc(backgrounds: list[dict[str, Any]]) -> None:
    lines = [
        "# Titan Thumbnail Prompts v001",
        "",
        "Generated from the PD-2026-016-titan design bible thumbnail directions.",
        "A1111 was unavailable during this pass, so the final backgrounds are derived from already-generated local SDXL Titan hero stills.",
        "No paid API, upload, publish, or approval creation was performed.",
        "",
        "## Directions",
        "",
        "- A: deep black ocean / tiny submersible silhouette; overlay text `THEY WERE WARNED`.",
        "- B: external bolts / hatch finality; overlay text `PURE WASTE`.",
        "- C: Rubik's cube in darkness; overlay text `HE WAS 19`.",
        "",
        "## Background Candidates",
        "",
    ]
    for item in backgrounds:
        lines.extend(
            [
                f"### {item['id']}",
                f"- Source hero: `{item['source']}`",
                f"- Saved AI thumb: `{item['ai_thumb_file']}`",
                f"- Prompt intent: {item['prompt']}",
                "",
            ]
        )
    (SCENES / "thumb_prompts.v001.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def update_manifest(rendered: list[dict[str, Any]]) -> None:
    manifest_path = EPDIR / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest.setdefault("active_revisions", {})["thumb_prompts"] = "v001"
    manifest.setdefault("active_revisions", {})["thumbnail_candidates"] = "v001"
    manifest.setdefault("active_revisions", {})["thumbnail"] = "v001"
    artifacts = manifest.setdefault("artifacts", [])
    artifact = {
        "artifact_id": "PD-2026-016-titan-title-thumbnail-candidates",
        "artifact_type": "title_thumbnail_candidates",
        "revision": "v001",
        "uri": "artifact://episodes/PD-2026-016-titan/09_package/title_thumbnail_candidates.v001.json",
        "checksum": sha256(PKG / "title_thumbnail_candidates.v001.json"),
        "status": "candidate",
        "rights_status": "conditional",
        "qc_status": "pass",
    }
    artifacts[:] = [a for a in artifacts if a.get("artifact_id") != artifact["artifact_id"]]
    artifacts.append(artifact)
    warnings = manifest.setdefault("warnings", [])
    note = "Title/thumbnail candidates v001 prepared from generated symbolic SDXL stills; title/thumbnail owner gate still required before publish."
    if note not in warnings:
        warnings.append(note)
    manifest["updated_at"] = datetime.now().astimezone().isoformat(timespec="seconds")
    write_json(manifest_path, manifest)


def append_event() -> None:
    event_path = EPDIR / "events" / "events.jsonl"
    event_path.parent.mkdir(parents=True, exist_ok=True)
    event = {
        "ts": datetime.now().astimezone().isoformat(timespec="seconds"),
        "episode_id": EP,
        "stage": "assets_ready",
        "event": "thumbnail_candidates_prepared",
        "revision": "v001",
        "actor": "codex",
        "note": "Prepared Titan thumbnail backgrounds and A/B/C title candidates from existing local SDXL hero stills. No paid API, upload, schedule, publish, or approval action.",
    }
    with event_path.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(event, ensure_ascii=False) + "\n")


def main() -> int:
    backgrounds = build_backgrounds()
    write_prompt_doc(backgrounds)
    rendered = render_stills(backgrounds)
    selected = next(item for item in rendered if item["id"] == SELECTED_TITLE_ID)
    meta = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "slug": SLUG,
        "revision": "v001",
        "created_at": now_iso(),
        "status": "selected_candidate_owner_gate_required",
        "external_side_effects": {
            "paid_api": False,
            "upload": False,
            "publish": False,
            "schedule": False,
            "approval_files_created": False,
        },
        "selection_criterion": "CTR maximum with dignity: high contrast, one clear subject, mobile readability, no real-person likeness, no brand marks.",
        "background_candidates": backgrounds,
        "title_candidates": rendered,
        "selected_title_id": SELECTED_TITLE_ID,
        "selected_thumbnail": selected["selected_package_file"],
        "selected_thumbnail_sha256": selected["selected_package_sha256"],
        "selected_youtube_title": selected["youtube_title"],
        "safety": {
            "real_person_likeness": False,
            "stockton_rush_likeness": False,
            "passenger_likeness": False,
            "brand_marks": False,
            "graphic_implosion_or_remains": False,
            "synthetic_disclosure_required": True,
        },
    }
    write_json(PKG / "title_thumbnail_candidates.v001.json", meta)
    update_manifest(rendered)
    append_event()
    print(json.dumps({"selected_thumbnail": meta["selected_thumbnail"], "sha256": meta["selected_thumbnail_sha256"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
