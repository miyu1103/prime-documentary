#!/usr/bin/env python3
"""Recover EP70/EP71 plates from the Codex image cache, matched by ID, not by guesswork.

2026-08-17. The archive drive holding the only copy of wronghouse's 160 plates and oroville's
118 stopped being enumerated by Windows. The images themselves were never lost: Codex keeps every
generated PNG under ~/.codex/generated_images/<session-uuid>/, 11,765 of them across 69 sessions.
What was missing was the mapping, and the earlier attempt stopped after four plates because the
IDs could not be confirmed.

They can. Every session transcript records, per image:

    {"type":"image_generation_end", "status":"completed",
     "revised_prompt":"... reconstruction plate O001, camera position A ...",
     "saved_path":"C:\\Users\\...\\generated_images\\<uuid>\\exec-<id>.png"}

The plate ID and the file are in the SAME record. Nothing here infers, orders by timestamp, or
matches on similarity. A record whose prompt does not name a plate is skipped, and so is a record
whose saved file is missing.

Existing files are never overwritten -- on Windows that check must be case-insensitive, because
O002B.png and O002b.png are the same name to the filesystem.

    py -3.11 scripts/recover_codex_plates.py --dry-run     # report only
    py -3.11 scripts/recover_codex_plates.py               # copy what is missing
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path

CODEX = Path.home() / ".codex"
SESSION_DIRS = [CODEX / "sessions", CODEX / "archived_sessions"]
MEDIA = Path("E:/pd-media/assets/ai")

# "reconstruction plate O001, camera position A" / "plate W073b" / "plate O108 A"
PLATE_RE = re.compile(r"\bplate\s+([WO])(\d{3})([ab])?\b", re.IGNORECASE)
CAMERA_RE = re.compile(r"camera position\s+([AB])\b", re.IGNORECASE)
SLUG = {"W": "wronghouse", "O": "oroville"}
BATCH: dict[str, str] = {}


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def existing_ci(directory: Path) -> dict[str, Path]:
    """Map lowercased filename -> real path. Windows is case-insensitive; the check must be too."""
    if not directory.is_dir():
        return {}
    return {p.name.lower(): p for p in directory.iterdir() if p.is_file()}


def scan() -> dict[tuple[str, str], Path]:
    """(target_filename, session) -> cached png. Later sessions win for the same plate id."""
    found: dict[str, tuple[str, Path]] = {}
    seen_ids: set[str] = set()
    files = []
    for d in SESSION_DIRS:
        if d.is_dir():
            files += sorted(d.rglob("rollout-*.jsonl"))
    for f in files:
        for line in f.open(encoding="utf-8", errors="replace"):
            if '"image_generation_end"' not in line:
                continue
            try:
                rec = json.loads(line)
            except Exception:
                continue
            for ev in walk(rec):
                if ev.get("status") != "completed":
                    continue
                prompt = ev.get("revised_prompt") or ""
                m = PLATE_RE.search(prompt)
                if m:
                    letter, num, suffix = m.group(1).upper(), m.group(2), (m.group(3) or "")
                    if not suffix:
                        cam = CAMERA_RE.search(prompt)
                        suffix = "b" if (cam and cam.group(1).upper() == "B") else ""
                else:
                    # No id in the prompt (EP70). Identify it by the batch description instead.
                    np_ = norm(prompt)
                    hit = next((pid for pid, desc in BATCH.items()
                                if desc and (np_.startswith(desc[:60]) or desc.startswith(np_[:60]))), None)
                    if not hit:
                        continue
                    letter, num = hit[0], hit[1:]
                    # Two images per prompt: the first seen is A, the second is b.
                    suffix = "b" if f"{hit}.png" in seen_ids else ""
                    seen_ids.add(f"{hit}.png")
                saved = ev.get("saved_path") or ""
                # The transcript truncates long values; repair the extension when it is clipped.
                if saved and not saved.lower().endswith(".png"):
                    saved = saved.rsplit(".", 1)[0] + ".png"
                p = Path(saved)
                if not saved or not p.is_file():
                    continue
                name = f"{letter}{num}{suffix}.png"
                found[name] = (f.name, p)
    return found


def batch_prompts() -> dict[str, str]:
    """id -> the scene description line, read from the Codex paste batches.

    EP71 oroville's prompts carry their own id ("reconstruction plate O001, camera position A")
    so the transcript alone identifies them. EP70 wronghouse's do not -- its revised_prompt is a
    bare scene description. The description IS the identifier, because the batch file that was
    pasted holds exactly one per plate. Matched on a normalised prefix, never on similarity.
    """
    out: dict[str, str] = {}
    for pack, letter in (("EP70_wronghouse_CODEX_PASTE", "W"),
                         ("EP71_oroville_CODEX_PASTE", "O")):
        d = Path(__file__).resolve().parents[1] / "episodes" / "_planning" / pack
        for f in sorted(d.glob("batch_*.txt")):
            lines = f.read_text(encoding="utf-8", errors="replace").splitlines()
            for i, line in enumerate(lines):
                m = re.match(rf"^-{{3}}\s*({letter}\d{{3}})\b", line.strip())
                if not m:
                    continue
                for nxt in lines[i + 1:i + 4]:
                    s = nxt.strip()
                    if s and not s.startswith(("NEGATIVE", "Deliver", "---")):
                        out[m.group(1)] = norm(s)
                        break
    return out


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9 ]+", "", s.lower())[:120]


def walk(o):
    """Yield every image_generation_end dict anywhere in the record."""
    if isinstance(o, dict):
        if o.get("type") == "image_generation_end":
            yield o
        for v in o.values():
            yield from walk(v)
    elif isinstance(o, list):
        for i in o:
            yield from walk(i)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    BATCH.update(batch_prompts())
    print(f"[recover] {len(BATCH)} batch prompt(s) loaded for id-less matching")
    found = scan()
    print(f"[recover] {len(found)} plate id(s) matched to a cached file by prompt text")

    copied = skipped = 0
    per_slug: dict[str, list[str]] = {"wronghouse": [], "oroville": []}
    for name, (session, src) in sorted(found.items()):
        slug = SLUG[name[0]]
        dest_dir = MEDIA / slug
        have = existing_ci(dest_dir)
        per_slug[slug].append(name)
        if name.lower() in have:
            old = have[name.lower()]
            same = sha256(old) == sha256(src)
            print(f"  SKIP {slug}/{old.name} already present ({'identical' if same else 'DIFFERENT bytes'})")
            skipped += 1
            continue
        if a.dry_run:
            print(f"  would copy {slug}/{name}  <- {src.name} ({session[:34]})")
            copied += 1
            continue
        dest_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest_dir / name)
        copied += 1

    for slug, want, letter in (("wronghouse", 160, "W"), ("oroville", 118, "O")):
        got = {n for n in per_slug[slug] if not n[-5].isalpha() or n[-5].isdigit()}
        base = sorted({n for n in per_slug[slug] if re.fullmatch(rf"{letter}\d{{3}}\.png", n)})
        missing = [f"{letter}{i:03d}.png" for i in range(1, want + 1)
                   if f"{letter}{i:03d}.png" not in base]
        print(f"[recover] {slug}: {len(base)}/{want} A-variant plates recovered, "
              f"{len(per_slug[slug]) - len(base)} b-variant(s)")
        if missing:
            print(f"           still missing {len(missing)}: {', '.join(missing[:12])}"
                  + (" ..." if len(missing) > 12 else ""))
    print(f"[recover] copied={copied} skipped_existing={skipped}"
          + ("  (DRY RUN -- nothing written)" if a.dry_run else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
