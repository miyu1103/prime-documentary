#!/usr/bin/env python3
"""Build local YouTube package artifacts for PD-2026-009 Timbs."""

from __future__ import annotations

import hashlib
import json
import textwrap
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-009-timbs"
EP_DIR = ROOT / "episodes" / EP
PKG = EP_DIR / "09_package"
THUMBS = Path(r"H:\pd-media\episodes\PD-2026-009-timbs\09_package\thumbnails")
PUBLIC_TIMBS = ROOT / "remotion" / "public" / "timbs"
VIDEO = ROOT / "remotion" / "out" / "timbs_rough.mp4"
CAPTIONS = EP_DIR / "08_edit" / "captions.v001.srt"
QC = EP_DIR / "08_edit" / "renders" / "rough.v001.qc.json"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", "utf-8")


def make_thumbnail(asset_id: str, background: Path, headline: str, kicker: str, subline: str, out: Path) -> None:
    try:
        from PIL import Image, ImageDraw, ImageFilter, ImageFont
    except ImportError as exc:
        raise SystemExit("Pillow is required to build thumbnails") from exc

    W, H = 1280, 720
    img = Image.open(background).convert("RGB")
    iw, ih = img.size
    scale = max(W / iw, H / ih)
    img = img.resize((int(iw * scale), int(ih * scale)))
    left = (img.width - W) // 2
    top = (img.height - H) // 2
    img = img.crop((left, top, left + W, top + H)).filter(ImageFilter.GaussianBlur(0.4))

    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pix = overlay.load()
    for x in range(W):
        a = int(225 * (1 - x / W) + 50)
        for y in range(H):
            pix[x, y] = (8, 10, 14, max(40, min(230, a)))
    img = Image.alpha_composite(img.convert("RGBA"), overlay)
    draw = ImageDraw.Draw(img)

    font_paths = [
        Path(r"C:\Windows\Fonts\arialbd.ttf"),
        Path(r"C:\Windows\Fonts\impact.ttf"),
        Path(r"C:\Windows\Fonts\segoeuib.ttf"),
    ]
    font_main = ImageFont.truetype(str(font_paths[1] if font_paths[1].exists() else font_paths[0]), 118)
    font_kicker = ImageFont.truetype(str(font_paths[0]), 38)
    font_sub = ImageFont.truetype(str(font_paths[0]), 46)

    gold = (219, 177, 98, 255)
    white = (245, 246, 248, 255)
    red = (204, 55, 45, 255)
    ink = (8, 10, 14, 235)

    draw.rectangle((66, 60, 390, 112), fill=ink, outline=gold, width=3)
    draw.text((86, 69), kicker.upper(), font=font_kicker, fill=gold)

    y = 188
    lines = textwrap.wrap(headline.upper(), width=11)
    for line in lines[:3]:
        draw.text((70 + 5, y + 6), line, font=font_main, fill=(0, 0, 0, 180))
        fill = red if "TOO" in line or "TAKE" in line else white
        draw.text((70, y), line, font=font_main, fill=fill)
        y += 118

    draw.rectangle((70, 592, 760, 654), fill=(8, 10, 14, 220))
    draw.text((92, 600), subline.upper(), font=font_sub, fill=gold)

    draw.ellipse((1120, 570, 1232, 682), outline=gold, width=5)
    draw.text((1142, 598), "PD", font=font_sub, fill=white)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.convert("RGB").save(out, quality=94)


def main() -> None:
    PKG.mkdir(parents=True, exist_ok=True)
    THUMBS.mkdir(parents=True, exist_ok=True)

    titles = [
        {
            "id": "T1",
            "title": "Police Took His $42,000 Car. The Supreme Court Drew a Line.",
            "score": 91,
            "reason": "Specific, accurate, emotional, and clear. It does not overclaim that Timbs was uncharged.",
        },
        {
            "id": "T2",
            "title": "Can Police Take Your Car Without Convicting You?",
            "score": 87,
            "reason": "Strong broad question and high curiosity, but the Timbs facts include a guilty plea, so description must clarify the system-level point.",
        },
        {
            "id": "T3",
            "title": "The Supreme Court Case That Put a Limit on Civil Forfeiture",
            "score": 82,
            "reason": "Very accurate and searchable, but less emotionally immediate.",
        },
        {
            "id": "T4",
            "title": "The Government Seized His Land Rover. A 700-Year-Old Rule Stopped It.",
            "score": 88,
            "reason": "Distinctive and story-driven. Slightly long, but the Magna Carta angle is memorable.",
        },
        {
            "id": "T5",
            "title": "When the Government Accuses Your Property Instead of You",
            "score": 79,
            "reason": "Conceptually strong, but less clickable and less tied to the Supreme Court payoff.",
        },
    ]

    thumb_specs = [
        ("PD-2026-009-THUMB-001", PUBLIC_TIMBS / "pexels_tow_truck.jpg", "TOO FAR", "$42K CAR", "MAX FINE $10K"),
        ("PD-2026-009-THUMB-002", PUBLIC_TIMBS / "scotus_gavel.jpg", "CAN THEY TAKE IT?", "CIVIL FORFEITURE", "9-0 SUPREME COURT"),
        ("PD-2026-009-THUMB-003", PUBLIC_TIMBS / "pexels_police_car.jpg", "TAKEN", "NO TRIAL?", "PROPERTY ACCUSED"),
    ]
    candidates = []
    for idx, (asset_id, bg, headline, kicker, subline) in enumerate(thumb_specs, 1):
        out = THUMBS / f"{EP}-thumb{idx:02}.v001.jpg"
        make_thumbnail(asset_id, bg, headline, kicker, subline, out)
        candidates.append(
            {
                "asset_id": asset_id,
                "rank": idx,
                "headline": headline,
                "kicker": kicker,
                "subline": subline,
                "file": str(out).replace("\\", "/"),
                "background": str(bg).replace("\\", "/"),
                "content_hash": sha256(out),
                "score": [90, 84, 76][idx - 1],
                "notes": [
                    "No real-person likeness.",
                    "Uses existing Timbs still/stock material and local typography.",
                    "AI/synthetic disclosure still required because the video contains AI symbolic reconstructions.",
                ],
            }
        )

    selected_title = titles[0]["title"]
    selected_thumb = candidates[0]
    description = (
        "Police took Tyson Timbs's Land Rover after a small drug case. The car was worth about $42,000. "
        "The maximum fine for his offense was $10,000. Could the state keep it anyway?\n\n"
        "This episode explains Timbs v. Indiana, the 2019 Supreme Court case that applied the Eighth Amendment's ban on excessive fines to the states. "
        "It also explains civil asset forfeiture: the legal system where the case can be aimed at the property itself, not the owner.\n\n"
        "The Court did not abolish forfeiture. It drew a constitutional line: a forfeiture can become an excessive fine if it is grossly out of proportion to the offense.\n\n"
        "This is an educational documentary, not legal advice.\n\n"
        "Visual note: this video uses AI-generated symbolic reconstructions, motion graphics, stock footage, and public-domain/legal-document imagery. "
        "They are not authentic footage of Tyson Timbs, and no real-person likeness is intended.\n\n"
        "Next episode: when the government takes your home for \"public use.\"\n\n"
        "Chapters:\n"
        "00:00 Police can take your property\n"
        "00:20 Opening\n"
        "01:03 Tyson Timbs and the Land Rover\n"
        "03:27 Civil forfeiture: the property is accused\n"
        "06:07 The Excessive Fines Clause\n"
        "09:02 A limit, not the end of forfeiture\n"
        "10:44 Next: public use and your home"
    )

    tags = [
        "Timbs v Indiana",
        "Timbs v. Indiana",
        "civil asset forfeiture",
        "asset forfeiture",
        "excessive fines clause",
        "Eighth Amendment",
        "Supreme Court cases",
        "constitutional law",
        "property rights",
        "criminal justice",
        "policing for profit",
        "Institute for Justice",
        "Prime Documentary",
    ]

    thumbs_json = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "revision": "v001",
        "generated_at": now(),
        "status": "ready_for_owner_review",
        "recommended_pair": {
            "title_id": "T1",
            "thumbnail_asset_id": selected_thumb["asset_id"],
            "reason": "Best accuracy/click balance: concrete $42k car + Supreme Court line, without implying Timbs himself was never charged.",
        },
        "title_candidates": titles,
        "thumbnail_candidates": candidates,
        "gate": {
            "current_gate": "title_thumbnail_review_required",
            "owner_approval_required_before_upload_or_publish": True,
            "upload_performed": False,
            "publish_performed": False,
        },
    }
    write_json(PKG / "title_thumbnail_candidates.v001.json", thumbs_json)
    write_json(PKG / "thumbnail_candidates.v001.json", thumbs_json)

    youtube_meta = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "revision": "v001",
        "status": "ready_for_owner_review",
        "title": selected_title,
        "description": description,
        "tags": tags,
        "categoryId": "27",
        "defaultLanguage": "en",
        "defaultAudioLanguage": "en",
        "thumbnail": selected_thumb["file"],
        "selected_thumbnail": selected_thumb["file"],
        "selected_thumbnail_sha256": selected_thumb["content_hash"],
        "thumbnail_candidates": f"episodes/{EP}/09_package/title_thumbnail_candidates.v001.json",
        "video": "remotion/out/timbs_rough.mp4",
        "video_actual_path": str(VIDEO),
        "video_sha256": sha256(VIDEO) if VIDEO.exists() else None,
        "synthetic_content_disclosure_required": True,
        "contains_ai_symbolic_reconstruction": True,
        "captions_burned_in": True,
        "captions_sidecar": f"episodes/{EP}/08_edit/captions.v001.srt",
        "approval_required_before_upload": True,
        "publish_performed": False,
        "created_at": now(),
    }
    write_json(PKG / "youtube_meta.v001.json", youtube_meta)

    rights = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "revision": "v001",
        "generated_at": now(),
        "status": "draft_ready_for_review",
        "assets": [
            {
                "asset_id": "PD-2026-009-RENDER-ROUGH-v001",
                "type": "render",
                "file": str(VIDEO),
                "content_hash": sha256(VIDEO) if VIDEO.exists() else None,
                "producer": "Remotion + FFmpeg/libx264 local render",
                "license": "Prime Documentary composite edit render from rights-tracked local inputs.",
                "rights_holder": "Prime Documentary",
                "ai_disclosure_required": True,
                "symbolic_reconstruction": True,
                "qc": str(QC),
            },
            {
                "asset_id": "PD-2026-009-CAPTIONS-v001",
                "type": "captions",
                "file": str(CAPTIONS),
                "content_hash": sha256(CAPTIONS) if CAPTIONS.exists() else None,
                "producer": "Codex local caption timing from ElevenLabs chunk timings",
                "license": "Prime Documentary script-derived subtitles.",
                "rights_holder": "Prime Documentary",
            },
            {
                "asset_id": "PD-2026-009-THUMB-001",
                "type": "thumbnail",
                "file": selected_thumb["file"],
                "content_hash": selected_thumb["content_hash"],
                "producer": "Local Pillow compositing over existing Timbs stock still",
                "license": "Prime Documentary local package thumbnail from rights-cleared episode material.",
                "rights_holder": "Prime Documentary",
                "ai_disclosure_required": True,
                "symbolic_reconstruction": False,
                "package_selected": True,
            },
        ],
        "verification_required": [
            "Final owner approval for title/thumbnail before upload.",
            "Confirm YouTube synthetic-content disclosure at upload because AI symbolic reconstructions are used.",
        ],
    }
    write_json(PKG / "rights_manifest.v001.json", rights)

    review = f"""# PD-2026-009 Timbs Package Review v001

Status: ready for title/thumbnail owner review. No upload or publish performed.

## Recommended title

{selected_title}

Why: concrete, accurate, clickable, and avoids implying Tyson Timbs himself was never charged.

## Recommended thumbnail

{selected_thumb['file']}

Text: `{selected_thumb['kicker']}` / `{selected_thumb['headline']}` / `{selected_thumb['subline']}`

## Description

{description}

## Tags

{', '.join(tags)}

## Gate

Owner approval is still required before YouTube upload, thumbnail upload, scheduling, or publish.
"""
    (PKG / "package_review.v001.md").write_text(review, "utf-8")

    print(f"package={PKG}")
    print(f"selected_title={selected_title}")
    print(f"selected_thumbnail={selected_thumb['file']}")


if __name__ == "__main__":
    main()
