#!/usr/bin/env python3
"""Build an idempotent TikTok scheduling queue from finished PD Shorts.

The queue is planning data only. It does not upload, schedule, or publish anything.
TikTok side effects are recorded separately in a JSONL receipt after the UI confirms them.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "remotion" / "out"
DESIGNS = ROOT / "episodes" / "_planning" / "short_designs"
DEFAULT_QUEUE = ROOT / "episodes" / "_planning" / "measurements" / "TIKTOK_SCHEDULE_QUEUE.v001.json"
DEFAULT_RECEIPTS = ROOT / "episodes" / "_planning" / "measurements" / "TIKTOK_PUBLISH_RECEIPTS.v001.jsonl"
HANDLE = "@primedocumentarystudio"

TAG_MAP = {
    "miranda": ["MirandaRights", "SupremeCourt", "LegalHistory"],
    "gideon": ["RightToCounsel", "SupremeCourt", "LegalHistory"],
    "mapp": ["FourthAmendment", "SupremeCourt", "LegalHistory"],
    "ftx": ["FTX", "Crypto", "BusinessHistory"],
    "madoff": ["Madoff", "Fraud", "FinancialHistory"],
    "terry": ["StopAndFrisk", "SupremeCourt", "LegalHistory"],
    "riley": ["DigitalPrivacy", "SupremeCourt", "LegalHistory"],
    "carpenter": ["DigitalPrivacy", "SupremeCourt", "LegalHistory"],
    "timbs": ["CivilForfeiture", "SupremeCourt", "LegalHistory"],
    "kelo": ["EminentDomain", "SupremeCourt", "LegalHistory"],
    "mahanoy": ["FreeSpeech", "SupremeCourt", "LegalHistory"],
    "titan": ["Titan", "OceanGate", "Submersible"],
    "onecoin": ["OneCoin", "Crypto", "Fraud"],
    "flashcrash": ["FlashCrash", "Markets", "FinancialHistory"],
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_design_entries() -> dict[int, dict[str, str]]:
    entries: dict[int, dict[str, str]] = {}
    for path in sorted(DESIGNS.glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        destination = data.get("destination") or {}
        for short in data.get("shorts") or []:
            match = re.fullmatch(r"short(\d+)", str(short.get("short_id", "")))
            if not match:
                continue
            entries[int(match.group(1))] = {
                "angle": str(short.get("angle") or "").strip(),
                "episode_id": str(data.get("episode_id") or "").strip(),
                "slug": str(data.get("slug") or "").strip(),
                "long_title": str(destination.get("title") or "").strip(),
                "source": str(path.relative_to(ROOT)).replace("\\", "/"),
            }
    return entries


def load_timing_hook(number: int) -> str:
    path = ROOT / "remotion" / "src" / "data" / f"short{number}_timing.ts"
    if not path.is_file():
        return ""
    text = path.read_text(encoding="utf-8")
    parts = []
    for encoded in re.findall(r'"word":\s*("(?:[^"\\]|\\.)*")', text):
        try:
            part = json.loads(encoded).strip()
        except json.JSONDecodeError:
            continue
        if not part:
            continue
        parts.append(part)
        joined = " ".join(parts)
        if len(joined) >= 55 and re.search(r"[.!?][\"']?$", joined):
            return joined[:220]
        if len(joined) >= 180:
            return joined[:220].rstrip() + ("." if joined[-1] not in ".!?" else "")
    return " ".join(parts[:4])[:220]


def load_ts_fallback(number: int) -> dict[str, str]:
    path = ROOT / "remotion" / "src" / "data" / f"short{number}.ts"
    if not path.is_file():
        return {"angle": "", "episode_id": "", "slug": "", "long_title": "", "source": ""}
    text = path.read_text(encoding="utf-8")
    angle_match = re.search(rf"^\s*\*\s*(?:short{number}|SHORT\s*#{number})\s+[—-]\s+(.+?)\s*$", text, re.MULTILINE)
    episode_match = re.search(r"episodeId:\s*'([^']+)'", text)
    title_match = re.search(r"ctaLongTitle:\s*([\"'])(.*?)\1", text)
    episode_id = episode_match.group(1).strip() if episode_match else ""
    slug = episode_id.split("-", 3)[-1] if episode_id else ""
    return {
        "angle": load_timing_hook(number) or (angle_match.group(1).strip() if angle_match else ""),
        "episode_id": episode_id,
        "slug": slug,
        "long_title": title_match.group(2).strip() if title_match else "",
        "source": str(path.relative_to(ROOT)).replace("\\", "/"),
    }


def clean_hook(value: str, number: int) -> str:
    hook = re.sub(r"\s*#Shorts\s*$", "", value.strip(), flags=re.IGNORECASE)
    if not hook:
        raise ValueError(f"short{number}: no hook/angle in design or TypeScript fallback")
    return hook


def load_receipts(path: Path) -> dict[str, dict]:
    receipts: dict[str, dict] = {}
    if not path.is_file():
        return receipts
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            receipt = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_number}: invalid JSON receipt") from exc
        short_id = str(receipt.get("short_id") or "")
        if not re.fullmatch(r"short\d+", short_id):
            raise ValueError(f"{path}:{line_number}: invalid short_id {short_id!r}")
        receipts[short_id] = receipt
    return receipts


def hashtags(slug: str) -> list[str]:
    specific = TAG_MAP.get(slug.lower())
    if specific is None:
        words = re.findall(r"[A-Za-z0-9]+", slug)
        specific = ["".join(word[:1].upper() + word[1:] for word in words)] if words else []
    tags = [*specific, "Documentary", "TrueStory"]
    return [f"#{tag}" for tag in tags if tag][:5]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_QUEUE)
    parser.add_argument("--receipts", type=Path, default=DEFAULT_RECEIPTS)
    parser.add_argument("--published", nargs="*", type=int, default=[86])
    args = parser.parse_args()

    designs = load_design_entries()
    receipts = load_receipts(args.receipts)
    target_numbers = sorted(
        int(match.group(1))
        for path in OUT.glob("short*_yt_coverfirst.mp4")
        if (match := re.fullmatch(r"short(\d+)_yt_coverfirst", path.stem))
    )
    items = []
    for number in target_numbers:
        meta = designs.get(number) or load_ts_fallback(number)
        hook = clean_hook(meta["angle"], number)
        video = OUT / f"short{number}_tt.mp4"
        caption = f"{hook}\n\nFull case on YouTube: {HANDLE}\n\n{' '.join(hashtags(meta['slug']))}"
        short_id = f"short{number}"
        receipt = receipts.get(short_id)
        status = str(receipt.get("status")) if receipt else ("published" if number in args.published else "pending")
        items.append(
            {
                "short_id": short_id,
                "number": number,
                "episode_id": meta["episode_id"],
                "slug": meta["slug"],
                "hook": hook,
                "long_title": meta["long_title"],
                "caption": caption,
                "video_file": str(video.resolve()),
                "video_exists": video.is_file(),
                "video_bytes": video.stat().st_size if video.is_file() else None,
                "sha256": sha256(video) if video.is_file() else None,
                "source": meta["source"],
                "status": status,
                "tiktok_receipt": receipt,
            }
        )

    payload = {
        "schema_version": "v001",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "account": "prime.documentary8",
        "youtube_handle": HANDLE,
        "target_count": len(items),
        "rendered_count": sum(bool(item["video_exists"]) for item in items),
        "published_count": sum(item["status"] == "published" for item in items),
        "scheduled_count": sum(item["status"] == "scheduled" for item in items),
        "pending_count": sum(item["status"] == "pending" for item in items),
        "policy": {
            "cadence_per_day": 4,
            "visibility": "public",
            "high_quality_upload": True,
            "automatic_content_checks": True,
            "ai_generated_content_label": True,
            "location": None,
            "cover": "automatic",
        },
        "items": items,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: payload[key] for key in ("target_count", "rendered_count", "published_count", "scheduled_count", "pending_count")}, ensure_ascii=False))
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
