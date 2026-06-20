#!/usr/bin/env python3
"""Render PD-2026-006 Terry thumbnail options.

No upload and no publish. Outputs repo-side PNGs because thumbnails are package
artifacts, while approved source stills remain under H:/pd-media.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-006-terry"
EPDIR = ROOT / "episodes" / EP
MEDIA = Path(json.loads((ROOT / "config/storage.local.json").read_text("utf-8"))["roots"]["media"]["path"])
SELECTED = MEDIA / "episodes" / EP / "05_visuals" / "selected"
REMOTION = ROOT / "remotion"
PUBLIC_TERRY = REMOTION / "public" / "terry"
OUT_DIR = EPDIR / "10_thumbnail"
OPTIONS_JSON = OUT_DIR / "thumbnail_options.v001.json"
CONTACT = OUT_DIR / "thumbnail_contact_sheet.v001.jpg"
NPX = shutil.which("npx.cmd") or shutil.which("npx") or "npx"
FFMPEG = Path(r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe")
if not FFMPEG.exists():
    FFMPEG = Path("ffmpeg")

VARIANTS = [
    {
        "id": "thumb01",
        "headline": "NO WARRANT?",
        "kicker": "HERE IS THE CATCH",
        "assessment": "Recommended primary. Fastest read, broadest hook, and directly pairs with the working title.",
    },
    {
        "id": "thumb02",
        "headline": "STOPPED. FRISKED. LEGAL?",
        "kicker": "TERRY v. OHIO",
        "assessment": "Strongest legal-drama angle; slightly more text but the stakes are clear.",
    },
    {
        "id": "thumb03",
        "headline": "SUSPICION IS ENOUGH?",
        "kicker": "THE 1968 RULE",
        "assessment": "Best doctrine-first option; useful if the audience responds to rights-standard framing.",
    },
    {
        "id": "thumb04",
        "headline": "THE 8-1 EXCEPTION",
        "kicker": "NO WARRANT - LOWER STANDARD",
        "assessment": "Most case-specific; good for legal-history viewers, less emotional than option 01.",
    },
    {
        "id": "thumb05",
        "headline": "THE LINE IS THIN",
        "kicker": "FROM YOUR BODY TO YOUR PHONE",
        "assessment": "Best series-bridge option into Riley; more elegant than urgent.",
    },
    {
        "id": "thumb06",
        "headline": "NO WARRANT?",
        "kicker": "TERRY STOP - 1968 - 8-1",
        "assessment": "Denser alternate requested by owner: adds the trip path, 8-1 ruling, suspicion scale, and GAP motif while keeping the main hook readable.",
    },
    {
        "id": "thumb07",
        "headline": "NO WARRANT?",
        "kicker": "TERRY STOP - 1968 - 8-1",
        "assessment": "Selected. Codex-polished cinematic variant: keeps the dense Terry-specific cues from option 06, but improves depth, lighting, hierarchy, and small-size readability.",
    },
    {
        "id": "thumb08",
        "headline": "NO WARRANT?",
        "kicker": "TERRY STOP - 1968 - 8-1",
        "assessment": "Selected. Codex-generated detailed key-art background with richer storefront texture, wet-pavement reflections, blue path light, and cleaner documentary hierarchy.",
    },
]


def run(cmd: list[str | os.PathLike[str]], desc: str, cwd: Path | None = None) -> None:
    print(f">> {desc}")
    p = subprocess.run([str(x) for x in cmd], cwd=str(cwd) if cwd else None, capture_output=True, encoding="utf-8", errors="replace")
    if p.returncode != 0:
        print((p.stdout or "")[-1200:])
        print((p.stderr or "")[-3000:])
        raise RuntimeError(desc)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def prepare_public_images() -> None:
    PUBLIC_TERRY.mkdir(parents=True, exist_ok=True)
    copied = 0
    for src in sorted(SELECTED.rglob("*.png")):
        dst = PUBLIC_TERRY / src.name
        if not dst.exists() or dst.stat().st_size != src.stat().st_size:
            shutil.copy2(src, dst)
        copied += 1
    keyart = OUT_DIR / "codex_keyart_background.v008.png"
    if keyart.exists():
        shutil.copy2(keyart, PUBLIC_TERRY / keyart.name)
    if copied < 3:
        raise FileNotFoundError(f"Expected approved Terry images under {SELECTED}, found {copied}")
    print(f"copied_or_verified_images={copied} -> {PUBLIC_TERRY}")


def render_options() -> list[dict]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    options: list[dict] = []
    for i, variant in enumerate(VARIANTS, start=1):
        out = OUT_DIR / f"thumbnail_option_{i:02d}.v001.png"
        run([
            NPX,
            "remotion",
            "still",
            "src/terry_index.tsx",
            f"Terry-{variant['id']}",
            str(out),
            "--overwrite",
        ], f"render {variant['id']}", cwd=REMOTION)
        options.append({
            "id": variant["id"],
            "file": f"episodes/{EP}/10_thumbnail/{out.name}",
            "headline": variant["headline"],
            "kicker": variant["kicker"],
            "sha256": sha256(out),
            "assessment": variant["assessment"],
        })
    return options


def build_contact_sheet() -> str:
    inputs: list[str] = []
    for i in range(1, len(VARIANTS) + 1):
        inputs.extend(["-i", str(OUT_DIR / f"thumbnail_option_{i:02d}.v001.png")])
    labels = "".join(f"[{i}:v]scale=384:216[t{i}];" for i in range(len(VARIANTS)))
    positions = [f"{(i % 3) * 384}_{(i // 3) * 216}" for i in range(len(VARIANTS))]
    layout = "".join(f"[t{i}]" for i in range(len(VARIANTS)))
    layout += f"xstack=inputs={len(VARIANTS)}:layout={'|'.join(positions)}[out]"
    run([
        FFMPEG,
        "-y",
        *inputs,
        "-filter_complex",
        labels + layout,
        "-map",
        "[out]",
        "-frames:v",
        "1",
        CONTACT,
    ], "build thumbnail contact sheet")
    return sha256(CONTACT)


def write_options(options: list[dict], contact_hash: str) -> None:
    data = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "revision": "v001",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": "thumbnail_selected_not_published",
        "publish_performed": False,
        "upload_performed": False,
        "ai_disclosure_required": True,
        "synthetic_content_disclosure_required": True,
        "source_visuals": [
            "artifact://episodes/PD-2026-006-terry/05_visuals/selected/S003/PD-2026-006-terry-S003-IMG-001.v001.png",
            "artifact://episodes/PD-2026-006-terry/05_visuals/selected/S004/PD-2026-006-terry-S004-IMG-001.v001.png",
            "artifact://episodes/PD-2026-006-terry/05_visuals/selected/S018/PD-2026-006-terry-S018-IMG-001.v001.png",
            "artifact://episodes/PD-2026-006-terry/10_thumbnail/codex_keyart_background.v008.png",
        ],
        "recommended_shortlist": [
            "thumbnail_option_08.v001.png",
            "thumbnail_option_07.v001.png",
            "thumbnail_option_06.v001.png",
        ],
        "selected": "thumbnail_option_08.v001.png",
        "selection_reason": "Owner asked for a more beautiful and more detailed Codex-generated image. Option 08 uses a Codex-generated key-art background and keeps exact project-rendered text and legal motifs for reliability.",
        "options": options,
        "contact_sheet": {
            "file": f"episodes/{EP}/10_thumbnail/{CONTACT.name}",
            "sha256": contact_hash,
        },
        "title_candidates": [
            "A Cop Can Search You Without a Warrant - Here's the Catch",
            "No Warrant, No Crime Seen - Why This Search Was Legal",
            "The Supreme Court Case That Made Stop-and-Frisk Legal",
            "Suspicion Is Not Proof - But It Can Still Get You Searched",
            "Terry v. Ohio: The Rule Behind Every Street Stop",
        ],
        "recommended_title": "A Cop Can Search You Without a Warrant - Here's the Catch",
    }
    OPTIONS_JSON.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"options={OPTIONS_JSON}")


def main() -> None:
    prepare_public_images()
    options = render_options()
    contact_hash = build_contact_sheet()
    write_options(options, contact_hash)
    print(json.dumps({"options": len(options), "contact_sheet_sha256": contact_hash}, indent=2))


if __name__ == "__main__":
    main()
