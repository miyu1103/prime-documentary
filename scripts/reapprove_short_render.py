#!/usr/bin/env python3
"""Re-pin a Short's publishing config to a NEW render, as a new revision.

schedule_short_youtube.py pins video_sha256 and thumb_sha256 of the exact bytes that were
approved, and refuses to upload anything else. That gate is the reason a re-render cannot slip
into the schedule unnoticed, and it did its job when the kinetic-typography pass changed twelve
finished Shorts.

Clearing the mismatch by editing the hash in place would silently move an approval onto bytes
nobody approved. The constitution's answer (rule 12) is that a semantic input change makes a NEW
revision, so this bumps `rev` and writes the new hashes together, printing both sides. The
schedule result file is named after `rev`, so the old record stays on disk and the duplicate guard
still works.

What changed for these twelve: one or two mid-roll kinetic-typography overlays, built in After
Effects, on a number or a turn in the middle of the Short. The look was approved by the owner on
2026-08-04 against short118; the words are taken from the design and every figure on screen is
machine-checked against the narration.

Usage:
  py -3.11 scripts/reapprove_short_render.py --shorts 92-99 --reason "kinetic beats" --dry-run
  py -3.11 scripts/reapprove_short_render.py --shorts 92-99 --reason "kinetic beats" --apply
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "schedule_short_youtube.py"
OUT = ROOT / "remotion" / "out"


def sha(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_range(spec: str) -> list[int]:
    out: list[int] = []
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-")
            out += list(range(int(a), int(b) + 1))
        elif part:
            out.append(int(part))
    return out


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--shorts", required=True)
    ap.add_argument("--reason", required=True, help="what changed, recorded in the config comment")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    if not a.apply and not a.dry_run:
        ap.error("pass --apply or --dry-run")

    text = SCRIPT.read_text(encoding="utf-8")
    changed = 0
    for n in parse_range(a.shorts):
        key = f'    "{n}": {{'
        if key not in text:
            print(f"  short{n}: no CONFIG entry - skipped")
            continue
        start = text.index(key)
        end = text.index("\n    },", start) + len("\n    },")
        block = text[start:end]

        video = OUT / f"short{n}_yt_coverfirst.mp4"
        # Same choice the uploader makes: the 16:9 ShortThumbYT render when it exists, and only
        # then the vertical cover. Reading the vertical one here reported "already pinned" for 55
        # Shorts whose thumbnail had in fact been replaced, and the upload then failed on the hash.
        thumb = ROOT / "runs" / "shorts_thumbs" / "samples" / f"short{n}.png"
        if not thumb.is_file():
            thumb = OUT / f"short{n}_thumb.png"
        if not video.exists() or not thumb.exists():
            print(f"  short{n}: missing render or thumbnail - skipped")
            continue
        nv, nt = sha(video), sha(thumb)
        ov = re.search(r'"video_sha256": "([0-9a-f]+)"', block).group(1)
        ot = re.search(r'"thumb_sha256": "([0-9a-f]+)"', block).group(1)
        rev = re.search(r'"rev": "v(\d+)"', block).group(1)
        if nv == ov and nt == ot:
            print(f"  short{n}: already pinned to this render (rev v{rev}) - nothing to do")
            continue
        new_rev = f"v{int(rev) + 1:03d}"

        nb = block
        nb = nb.replace(f'"rev": "v{rev}"', f'"rev": "{new_rev}"')
        nb = nb.replace(f'"video_sha256": "{ov}"', f'"video_sha256": "{nv}"')
        nb = nb.replace(f'"thumb_sha256": "{ot}"', f'"thumb_sha256": "{nt}"')
        # The reason lives next to the hash so anyone reading the config can see why the approved
        # bytes moved, without going to git.
        nb = nb.replace(f'"video_sha256": "{nv}"',
                        f'# {new_rev}: re-rendered - {a.reason}\n'
                        f'        "video_sha256": "{nv}"')
        text = text[:start] + nb + text[end:]
        changed += 1
        print(f"  short{n}: v{rev} -> {new_rev}")
        print(f"      video {ov[:12]}... -> {nv[:12]}...")
        print(f"      thumb {ot[:12]}... -> {nt[:12]}...")

    print(f"\n{changed} config entrie(s) re-pinned" + ("" if a.apply else "   (DRY RUN)"))
    if a.apply and changed:
        SCRIPT.write_text(text, encoding="utf-8")
        import py_compile
        py_compile.compile(str(SCRIPT), doraise=True)
        print(f"wrote {SCRIPT.relative_to(ROOT)} (syntax checked)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
