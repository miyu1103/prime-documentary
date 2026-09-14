#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
register_kidsforcash_images.py

Register the 40 Codex-generated images for Prime Documentary EP38
"Kids for Cash" (PD-2026-038-kidsforcash) into an image provenance ledger.

Idempotent: reads the source images + handoff prompts and writes a
deterministic JSON ledger. Re-running produces identical output (no
now()/Date.now(); generated_at is a fixed ISO string passed in).

Provenance invariants (PD CLAUDE.md constitution):
  - invariant 11: generated visuals are NOT authentic records -> truth_status=symbolic
  - invariant  7: every asset carries provenance + hash
  - media-truth-license rule: source_type / truth_status / license_decision as separate fields

Usage:
  py -3.11 scripts/register_kidsforcash_images.py
  py -3.11 scripts/register_kidsforcash_images.py --check   # verify only, non-zero exit on anomaly
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import struct
import sys
from pathlib import Path

EPISODE_ID = "PD-2026-038-kidsforcash"
SCHEMA_VERSION = "image_ledger.v1"
GENERATED_AT = "2026-07-17T00:00:00Z"  # fixed; do NOT use now()

IMAGE_DIR = Path(r"E:\pd-media\assets\ai\kidsforcash")
HANDOFF_MD = Path(
    r"C:\Users\aab15\Documents\prime-documentary\episodes\_planning"
    r"\EP38_kidsforcash_CODEX_HANDOFF.md"
)
OUT_PATH = Path(
    r"C:\Users\aab15\Documents\prime-documentary\episodes\PD-2026-038-kidsforcash"
    r"\04_scenes\image_ledger.v001.json"
)

N_SCENES = 40

# Keywords in a prompt that indicate a human/child figure is depicted -> record
# the anonymization safety note (no real face / no identifiable person).
PERSON_KEYWORDS = [
    "child", "children", "kid", "teen", "teenage", "teenager", "figure",
    "silhouette", "silhouetted", "person", "people", "families", "family",
    "hand", "hands", "wrist", "woman", "man ", "adult", "parent", "mother",
    "guard", "attorney", "lawyer", "judge", "suited", "press",
]
# Prompts touching self-harm / death, allowed only as symbolic per handoff.
SENSITIVE_KEYWORDS = ["grief", "absence", "empty chair", "folded jacket", "folded teenage jacket", "loss", "lost childhood"]


def parse_handoff_prompts(md_path: Path) -> dict[str, dict[str, str]]:
    """Parse the authoritative S01-S40 block (title + prompt) from the handoff.

    Only the first block ('## プロンプト（S01–S40・各1枚）') is used; parsing
    stops at the later '## 追加プロンプト' section, which re-uses S21-S36 names
    with alternate content and would otherwise collide.
    """
    text = md_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    prompts: dict[str, dict[str, str]] = {}
    # header like: **S01 — 学校の廊下（普通の子供）**
    hdr = re.compile(r"^\*\*S(\d{2})\s*[—\-–]\s*(.+?)\*\*\s*$")
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        if line.strip().startswith("## 追加プロンプト"):
            break  # stop before the alternate S21-S36 block
        m = hdr.match(line.strip())
        if m:
            sid = "S" + m.group(1)
            title = m.group(2).strip()
            # next non-empty line is the English prompt
            j = i + 1
            while j < n and not lines[j].strip():
                j += 1
            prompt = lines[j].strip() if j < n else ""
            if sid not in prompts:  # first (authoritative) occurrence wins
                prompts[sid] = {"title": title, "prompt": prompt}
            i = j + 1
            continue
        i += 1
    return prompts


def png_dimensions(path: Path) -> tuple[int, int]:
    """Read width/height from a PNG IHDR header without loading the pixels."""
    with path.open("rb") as f:
        sig = f.read(8)
        if sig != b"\x89PNG\r\n\x1a\n":
            raise ValueError(f"not a PNG: {path}")
        header = f.read(18)  # 4 len + 4 'IHDR' + 4 width + 4 height + ...
        if header[4:8] != b"IHDR":
            raise ValueError(f"missing IHDR: {path}")
        width, height = struct.unpack(">II", header[8:16])
    return width, height


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def is_16_9(w: int, h: int) -> bool:
    return w * 9 == h * 16


NO_PERSON_RE = re.compile(r"\bno (?:person|people|one|body)\b|\bnobody\b")


def flag_safety(prompt: str, title: str) -> tuple[bool, str]:
    blob = (prompt + " " + title).lower()
    has_person_kw = any(k in blob for k in PERSON_KEYWORDS)
    # Prompts that explicitly state "no person/people/one" show no human body in
    # frame even if they reference authority (judge's bench, judge's robe, etc.).
    no_figure_in_frame = bool(NO_PERSON_RE.search(blob))
    depicts = has_person_kw and not no_figure_in_frame
    sensitive = any(k in blob for k in SENSITIVE_KEYWORDS)
    notes = []
    if depicts:
        notes.append(
            "depicts an anonymized human/child figure (silhouette / back / hands only) -> "
            "must show no real face and no identifiable real person "
            "(handoff safety rule; invariant 11)"
        )
    elif has_person_kw and no_figure_in_frame:
        notes.append(
            "person/authority theme but no human figure in frame (prompt states no person); "
            "no real-person likeness (invariant 11)"
        )
    if sensitive:
        notes.append("loss/self-harm shown symbolically only (empty seat, absence); nothing graphic")
    if not notes:
        notes.append("no person depicted; symbolic objects/environment only")
    return depicts, " | ".join(notes)


def build_entries() -> tuple[list[dict], list[str]]:
    prompts = parse_handoff_prompts(HANDOFF_MD)
    entries: list[dict] = []
    anomalies: list[str] = []
    seen_sha: dict[str, str] = {}

    for k in range(1, N_SCENES + 1):
        sid = f"S{k:02d}"
        img = IMAGE_DIR / f"{sid}.png"
        if not img.exists():
            anomalies.append(f"MISSING image file: {img}")
            continue
        w, h = png_dimensions(img)
        sha = sha256_file(img)
        if sha in seen_sha:
            anomalies.append(f"DUPLICATE sha256: {sid} == {seen_sha[sha]} ({sha})")
        else:
            seen_sha[sha] = sid
        if not is_16_9(w, h):
            anomalies.append(f"ODD dimensions (not 16:9): {sid} {w}x{h}")

        meta = prompts.get(sid, {})
        title = meta.get("title", "")
        prompt = meta.get("prompt", "")
        if not prompt:
            anomalies.append(f"NO prompt found in handoff for {sid}")
        depicts, safety_note = flag_safety(prompt, title)

        entries.append({
            "asset_id": sid,
            "scene_id": sid,
            "sequence_number": k,
            "episode_id": EPISODE_ID,
            "path": str(img),
            "source": "ai_codex",
            "source_type": "ai_generated",
            "commercial_use": "allowed",
            "license_decision": "allowed",
            "truth_status": "symbolic",
            "width": w,
            "height": h,
            "aspect_ratio": "16:9",
            "sha256": sha,
            "caption": title,
            "prompt": prompt,
            "depicts_person_or_child": depicts,
            "safety_note": safety_note,
        })

    return entries, anomalies


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="verify only; do not write")
    args = ap.parse_args()

    entries, anomalies = build_entries()

    ledger = {
        "schema_version": SCHEMA_VERSION,
        "episode_id": EPISODE_ID,
        "generated_at": GENERATED_AT,
        "source": "ai_codex",
        "provenance_note": (
            "Codex-generated cinematic stills for EP38 'Kids for Cash'. "
            "AI dramatizations, NOT authentic records (CLAUDE.md invariant 11)."
        ),
        "count": len(entries),
        "entries": entries,
    }

    if not args.check:
        OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        tmp = OUT_PATH.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(ledger, ensure_ascii=False, indent=2), encoding="utf-8")
        tmp.replace(OUT_PATH)  # atomic
        print(f"wrote {OUT_PATH}")

    # ---- verification summary ----
    n = len(entries)
    all_sha = all(e["sha256"] for e in entries)
    all_169 = all(e["aspect_ratio"] == "16:9" and is_16_9(e["width"], e["height"]) for e in entries)
    shas = [e["sha256"] for e in entries]
    dup = len(shas) != len(set(shas))
    flagged = sum(1 for e in entries if e["depicts_person_or_child"])

    print(f"entries          : {n}/{N_SCENES}")
    print(f"all sha256 present: {all_sha}")
    print(f"all 16:9         : {all_169}")
    print(f"duplicate sha256 : {dup}")
    print(f"person/child flag : {flagged} entries")
    if anomalies:
        print("ANOMALIES:")
        for a in anomalies:
            print("  - " + a)
    else:
        print("ANOMALIES: none")

    ok = (n == N_SCENES) and all_sha and all_169 and (not dup) and (not anomalies)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
