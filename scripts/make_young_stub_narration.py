#!/usr/bin/env python
"""Build a deterministic EP42 narration_index stub from the approved script."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-042-young"
SCRIPT = ROOT / "episodes" / "_planning" / "EP42_young_script.en.v001.md"
OUT = ROOT / "episodes" / EP / "06_audio" / "narration_index.stub.v001.json"
TARGET_SECONDS = 720.9

SECTION_HEADINGS = [
    ("HOOK", r"^## \[HOOK\]"),
    ("OP", r"^## \[OPENING NARRATION\]"),
    ("ACT_1", r"^## ACT 1"),
    ("ACT_2", r"^## ACT 2"),
    ("ACT_3", r"^## ACT 3"),
    ("ACT_4", r"^## ACT 4"),
    ("ENDING", r"^## ENDING"),
]
STOP_HEADINGS = [r"^## \[BrandOpening\]", r"^## \[BrandEndcard\]", r"^## 事実対応表", r"^## 改稿ログ"]


def words(text: str) -> int:
    return len(re.findall(r"[A-Za-z][A-Za-z'’-]*", text))


def clean_quote(line: str) -> str:
    line = re.sub(r"^>\s?", "", line).strip()
    line = re.sub(r"\*\*|\*|`", "", line)
    return line


def collect_sections(raw: str) -> dict[str, list[str]]:
    lines = raw.splitlines()
    starts: list[tuple[int, str]] = []
    for i, line in enumerate(lines):
        for sec, pat in SECTION_HEADINGS:
            if re.search(pat, line):
                starts.append((i, sec))
    out: dict[str, list[str]] = {sec: [] for sec, _ in SECTION_HEADINGS}
    for pos, (start, sec) in enumerate(starts):
        end = starts[pos + 1][0] if pos + 1 < len(starts) else len(lines)
        body = lines[start + 1:end]
        paras: list[str] = []
        cur: list[str] = []
        for line in body:
            if any(re.search(pat, line) for pat in STOP_HEADINGS):
                break
            stripped = line.strip()
            if not stripped:
                if cur:
                    paras.append(" ".join(cur).strip())
                    cur = []
                continue
            if stripped.startswith(">"):
                cur.append(clean_quote(stripped))
            elif stripped.startswith("**【SILENCE"):
                if cur:
                    paras.append(" ".join(cur).strip())
                    cur = []
            elif stripped.startswith("**[") or stripped.startswith("*("):
                continue
            elif not stripped.startswith("#") and not stripped.startswith("|"):
                # Keep only narration prose, not tables or apparatus.
                cur.append(re.sub(r"\*\*", "", stripped))
        if cur:
            paras.append(" ".join(cur).strip())
        out[sec] = [p for p in paras if words(p) >= 3]
    return out


def main() -> int:
    raw = SCRIPT.read_text(encoding="utf-8")
    sections = collect_sections(raw)
    chunks_raw: list[tuple[str, str]] = []
    for sec, _ in SECTION_HEADINGS:
        for para in sections[sec]:
            chunks_raw.append((sec, para))
    if not chunks_raw:
        raise SystemExit("no narration paragraphs parsed")

    total_words = sum(words(text) for _, text in chunks_raw)
    chunks = []
    t = 0.0
    for i, (sec, text) in enumerate(chunks_raw):
        dur = TARGET_SECONDS * words(text) / total_words
        if i == len(chunks_raw) - 1:
            end = TARGET_SECONDS
        else:
            end = round(t + dur, 3)
        chunks.append({
            "id": f"YC-{i+1:04d}",
            "section": sec,
            "start": round(t, 3),
            "end": round(end, 3),
            "duration": round(end - t, 3),
            "text": text,
            "spoken_text": text,
            "is_stub": True,
        })
        t = end

    OUT.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": "narration_index.stub.v1",
        "episode_id": EP,
        "source_script": str(SCRIPT.relative_to(ROOT)).replace("\\", "/"),
        "is_stub": True,
        "target_seconds": TARGET_SECONDS,
        "word_count": total_words,
        "chunks": chunks,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {OUT} chunks={len(chunks)} words={total_words} seconds={TARGET_SECONDS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
