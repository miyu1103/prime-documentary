#!/usr/bin/env python
"""Prepare and verify the EP31 Codex image prompt package.

Reads episodes/PD-2026-031-unlock/04_scenes/ai_prompts.v001.md, extracts the
42 hero prompts and 5 thumbnail-background prompts, writes a machine-readable
manifest, and checks whether the expected generated PNGs exist.
"""
from __future__ import annotations

import argparse
import json
import re
import struct
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EP = "PD-2026-031-unlock"
EPDIR = ROOT / "episodes" / EP
PROMPTS = EPDIR / "04_scenes" / "ai_prompts.v001.md"
MANIFEST = EPDIR / "04_scenes" / "ai_prompt_manifest.v001.json"
QUEUE_DIR = EPDIR / "04_scenes" / "codex_prompt_queue.v001"
MEDIA = Path("E:/pd-media/episodes") / EP
HERO_DIR = MEDIA / "05_visuals" / "selected"
THUMB_BG_DIR = MEDIA / "10_thumbnail" / "backgrounds"


def png_size(path: Path) -> tuple[int, int] | None:
    try:
        with path.open("rb") as fh:
            sig = fh.read(24)
    except OSError:
        return None
    if len(sig) < 24 or sig[:8] != b"\x89PNG\r\n\x1a\n" or sig[12:16] != b"IHDR":
        return None
    return struct.unpack(">II", sig[16:24])


def extract_ready_prompt(text: str) -> tuple[list[dict], list[dict]]:
    hero_matches = list(re.finditer(r"^## IMG-(\d{2})\s*$", text, flags=re.MULTILINE))
    thumb_start = text.find("# サムネ背景アート")
    heroes: list[dict] = []
    for pos, match in enumerate(hero_matches):
        n = int(match.group(1))
        if thumb_start != -1 and match.start() > thumb_start:
            continue
        end = hero_matches[pos + 1].start() if pos + 1 < len(hero_matches) else (thumb_start if thumb_start != -1 else len(text))
        body = text[match.end() : end].strip()
        save_id = f"PD-2026-031-S{n:03d}-IMG-{n:03d}"
        heroes.append(
            {
                "kind": "hero",
                "index": n,
                "heading": f"IMG-{n:02d}",
                "save_id": save_id,
                "filename": f"{save_id}.png",
                "target_path": str((HERO_DIR / f"{save_id}.png")).replace("\\", "/"),
                "prompt": body,
                "required_long_edge_min_px": 3840,
            }
        )

    thumbs: list[dict] = []
    if thumb_start != -1:
        thumb_text = text[thumb_start:]
        thumb_matches = list(re.finditer(r"^## T(\d)\s*（見出し:\s*([^）]+)）\s*$", thumb_text, flags=re.MULTILINE))
        for pos, match in enumerate(thumb_matches):
            n = int(match.group(1))
            end = thumb_matches[pos + 1].start() if pos + 1 < len(thumb_matches) else len(thumb_text)
            body = thumb_text[match.end() : end].strip()
            save_id = f"PD-2026-031-THUMB-T{n}"
            thumbs.append(
                {
                    "kind": "thumbnail_background",
                    "index": n,
                    "heading": f"T{n}",
                    "headline": match.group(2).strip(),
                    "save_id": save_id,
                    "filename": f"{save_id}.png",
                    "target_path": str((THUMB_BG_DIR / f"{save_id}.png")).replace("\\", "/"),
                    "prompt": body,
                    "required_size_px": [1280, 720],
                }
            )
    return heroes, thumbs


def build_manifest() -> dict:
    if not PROMPTS.exists():
        raise SystemExit(f"missing prompt file: {PROMPTS}")
    text = PROMPTS.read_text(encoding="utf-8")
    heroes, thumbs = extract_ready_prompt(text)
    return {
        "episode_id": EP,
        "revision": "v001",
        "source": str(PROMPTS.relative_to(ROOT)).replace("\\", "/"),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "hero_count": len(heroes),
        "thumbnail_background_count": len(thumbs),
        "hero_output_dir": str(HERO_DIR).replace("\\", "/"),
        "thumbnail_background_output_dir": str(THUMB_BG_DIR).replace("\\", "/"),
        "naming_rule": {
            "hero": "PD-2026-031-S###-IMG-###.png",
            "thumbnail_background": "PD-2026-031-THUMB-T#.png",
        },
        "items": heroes + thumbs,
    }


def check_assets(manifest: dict) -> dict:
    results = []
    for item in manifest["items"]:
        path = Path(item["target_path"])
        size = png_size(path) if path.exists() else None
        ok = bool(size)
        reason = "missing"
        if size:
            if item["kind"] == "hero":
                ok = max(size) >= int(item["required_long_edge_min_px"])
                reason = f"{size[0]}x{size[1]} long_edge={max(size)}"
            else:
                req = tuple(item["required_size_px"])
                ok = size == req
                reason = f"{size[0]}x{size[1]} need={req[0]}x{req[1]}"
        results.append({**item, "exists": path.exists(), "size": list(size) if size else None, "ok": ok, "reason": reason})
    hero_ok = sum(1 for r in results if r["kind"] == "hero" and r["ok"])
    thumb_ok = sum(1 for r in results if r["kind"] == "thumbnail_background" and r["ok"])
    return {
        "episode_id": EP,
        "status": "PASS" if hero_ok == 42 and thumb_ok == 5 else "FAIL",
        "hero_ok": hero_ok,
        "hero_required": 42,
        "thumbnail_background_ok": thumb_ok,
        "thumbnail_background_required": 5,
        "missing_or_bad": [r for r in results if not r["ok"]],
    }


def write_queue_files(manifest: dict) -> None:
    QUEUE_DIR.mkdir(parents=True, exist_ok=True)
    for item in manifest["items"]:
        target = QUEUE_DIR / f"{item['save_id']}.txt"
        target.write_text(
            "\n".join(
                [
                    f"SAVE AS: {item['target_path']}",
                    f"SAVE ID: {item['save_id']}",
                    "",
                    item["prompt"],
                    "",
                ]
            ),
            encoding="utf-8",
        )
    index_lines = [
        f"# EP31 Codex Prompt Queue v001",
        "",
        f"Source: `{manifest['source']}`",
        f"Hero output: `{manifest['hero_output_dir']}`",
        f"Thumbnail background output: `{manifest['thumbnail_background_output_dir']}`",
        "",
        "Generate one file per row, then save exactly to the target path.",
        "",
    ]
    for item in manifest["items"]:
        index_lines.append(f"- `{item['filename']}` ← `{QUEUE_DIR.name}/{item['save_id']}.txt`")
    (QUEUE_DIR / "README.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-manifest", action="store_true")
    parser.add_argument("--write-queue", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    HERO_DIR.mkdir(parents=True, exist_ok=True)
    THUMB_BG_DIR.mkdir(parents=True, exist_ok=True)
    manifest = build_manifest()
    if manifest["hero_count"] != 42 or manifest["thumbnail_background_count"] != 5:
        raise SystemExit(
            f"prompt count mismatch: hero={manifest['hero_count']} thumb={manifest['thumbnail_background_count']} need 42/5"
        )
    if args.write_manifest:
        MANIFEST.parent.mkdir(parents=True, exist_ok=True)
        MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if args.write_queue:
        write_queue_files(manifest)

    report = check_assets(manifest)
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"EP31 prompts: {manifest['hero_count']} hero + {manifest['thumbnail_background_count']} thumbnail backgrounds")
        print(f"Hero assets: {report['hero_ok']}/{report['hero_required']}")
        print(f"Thumbnail backgrounds: {report['thumbnail_background_ok']}/{report['thumbnail_background_required']}")
        print(f"RESULT: {report['status']}")
        if report["missing_or_bad"]:
            print("Missing/bad examples:")
            for item in report["missing_or_bad"][:10]:
                print(f"- {item['filename']}: {item['reason']}")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
