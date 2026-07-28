#!/usr/bin/env python
"""Prepare and verify the EP34 Codex image prompt package."""
from __future__ import annotations

import argparse
import json
import re
import struct
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EP = "PD-2026-034-rolin"
EPDIR = ROOT / "episodes" / EP
PROMPTS = ROOT / "episodes" / "_planning" / "EP34_rolin_ai_prompts.v001.md"
SCENE_DIR = EPDIR / "04_scenes"
MANIFEST = SCENE_DIR / "ai_prompt_manifest.v001.json"
QUEUE_DIR = SCENE_DIR / "codex_prompt_queue.v001"
IMAGE_DIR = ROOT / "remotion" / "public" / "rolin" / "img"


def png_size(path: Path) -> tuple[int, int] | None:
    try:
        with path.open("rb") as fh:
            sig = fh.read(24)
    except OSError:
        return None
    if len(sig) < 24 or sig[:8] != b"\x89PNG\r\n\x1a\n" or sig[12:16] != b"IHDR":
        return None
    return struct.unpack(">II", sig[16:24])


def extract_prompts(text: str) -> list[dict]:
    matches = list(re.finditer(r"^### S(\d{3})\s+—\s+(.+?)\s*$", text, flags=re.MULTILINE))
    end_marker = text.find("\n---\n\n## 反映済みQC")
    items: list[dict] = []
    for pos, match in enumerate(matches):
        index = int(match.group(1))
        end = matches[pos + 1].start() if pos + 1 < len(matches) else (end_marker if end_marker != -1 else len(text))
        body = text[match.end() : end].strip()
        save_id = f"PD-2026-034-S{index:03d}-IMG-001"
        items.append(
            {
                "kind": "hero",
                "index": index,
                "heading": f"S{index:03d}",
                "title": match.group(2).strip(),
                "save_id": save_id,
                "filename": f"{save_id}.png",
                "target_path": str((IMAGE_DIR / f"{save_id}.png")).replace("\\", "/"),
                "prompt": body,
                "required_size_px": [3840, 2160],
            }
        )
    return items


def build_manifest() -> dict:
    if not PROMPTS.exists():
        raise SystemExit(f"missing prompt file: {PROMPTS}")
    items = extract_prompts(PROMPTS.read_text(encoding="utf-8"))
    return {
        "episode_id": EP,
        "revision": "v001",
        "source": str(PROMPTS.relative_to(ROOT)).replace("\\", "/"),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "hero_count": len(items),
        "hero_output_dir": str(IMAGE_DIR).replace("\\", "/"),
        "naming_rule": "PD-2026-034-S###-IMG-001.png",
        "items": items,
    }


def check_assets(manifest: dict) -> dict:
    results = []
    for item in manifest["items"]:
        path = Path(item["target_path"])
        size = png_size(path) if path.exists() else None
        ok = bool(size)
        reason = "missing"
        if size:
            req = tuple(item["required_size_px"])
            ok = size == req
            reason = f"{size[0]}x{size[1]} need={req[0]}x{req[1]}"
        results.append({**item, "exists": path.exists(), "size": list(size) if size else None, "ok": ok, "reason": reason})
    hero_ok = sum(1 for r in results if r["ok"])
    return {
        "episode_id": EP,
        "status": "PASS" if hero_ok == 68 else "FAIL",
        "hero_ok": hero_ok,
        "hero_required": 68,
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
                    f"TITLE: {item['title']}",
                    "",
                    item["prompt"],
                    "",
                ]
            ),
            encoding="utf-8",
        )
    index_lines = [
        "# EP34 Codex Prompt Queue v001",
        "",
        f"Source: `{manifest['source']}`",
        f"Hero output: `{manifest['hero_output_dir']}`",
        "",
        "Generate one file per row, then save exactly to the target path.",
        "",
    ]
    for item in manifest["items"]:
        index_lines.append(f"- `{item['filename']}` <- `{QUEUE_DIR.name}/{item['save_id']}.txt`")
    (QUEUE_DIR / "README.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-manifest", action="store_true")
    parser.add_argument("--write-queue", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    manifest = build_manifest()
    if manifest["hero_count"] != 68:
        raise SystemExit(f"prompt count mismatch: hero={manifest['hero_count']} need 68")
    if args.write_manifest:
        MANIFEST.parent.mkdir(parents=True, exist_ok=True)
        MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if args.write_queue:
        write_queue_files(manifest)

    report = check_assets(manifest)
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"EP34 prompts: {manifest['hero_count']} hero")
        print(f"Hero assets: {report['hero_ok']}/{report['hero_required']}")
        print(f"RESULT: {report['status']}")
        if report["missing_or_bad"]:
            print("Missing/bad examples:")
            for item in report["missing_or_bad"][:10]:
                print(f"- {item['filename']}: {item['reason']}")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
