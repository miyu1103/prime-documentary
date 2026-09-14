#!/usr/bin/env python3
"""Generate EP39 captions using syntax-aware cue and line boundaries."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from fix_caption_dangling import NO_DANGLE_END

EP = "PD-2026-039-frazier"
EPDIR = ROOT / "episodes" / EP
MAX_WORDS = 14
MAX_LINE = 42
MAX_CUE_CHARS = 84
MIN_WORDS = 3
MIN_DUR = 1.0
MAX_DUR = 6.0
MAX_CPS = 17.0
GAP = 2 / 30

SUBORDINATORS = {"because", "although", "while", "when", "if", "since", "after", "before", "until", "unless", "whereas", "though", "so", "that", "who", "which", "whose"}
COORDINATORS = {"and", "but", "or", "nor", "yet"}
PREPOSITIONS = {"in", "on", "at", "to", "for", "with", "from", "into", "over", "under", "during", "without", "through", "against", "between"}
DETERMINERS = {"a", "an", "the", "this", "that", "these", "those", "my", "your", "his", "her", "its", "our", "their"}
AUXILIARIES = {"am", "is", "are", "was", "were", "be", "been", "being", "has", "have", "had", "do", "does", "did", "will", "would", "can", "could", "shall", "should", "may", "might", "must"}
COMMON_VERBS = {"be", "have", "do", "say", "tell", "make", "go", "take", "come", "see", "know", "get", "give", "find", "think", "hold", "sign", "trust", "confess", "lie", "admit", "ask", "leave", "run", "call", "show", "use", "allow", "become"}
UNITS = {"seconds", "minutes", "hours", "days", "weeks", "months", "years", "percent", "miles", "feet"}


def norm(token: str) -> str:
    return re.sub(r"[^a-z0-9'-]", "", token.lower())


def word_count(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9]+(?:['-][A-Za-z0-9]+)?", text))


def ends_sentence(token: str) -> bool:
    return bool(re.search(r"[.?!][\"')]*$", token))


def is_verb(token: str) -> bool:
    value = norm(token)
    return value in COMMON_VERBS or value.endswith(("ed", "ing", "en", "ize", "ise"))


def protected_boundary(tokens: list[str], index: int) -> bool:
    """Return true when a split before tokens[index] would break a phrase."""
    if index <= 0 or index >= len(tokens):
        return True
    left, right = norm(tokens[index - 1]), norm(tokens[index])
    if left in DETERMINERS:
        return True
    if left in PREPOSITIONS:
        return True
    if left in AUXILIARIES or left == "not":
        return True
    if right in UNITS and (left[:1].isdigit() or "-" in left):
        return True
    if left in NO_DANGLE_END and not ends_sentence(tokens[index - 1]):
        return True
    return False


def boundary_priority(tokens: list[str], index: int) -> int | None:
    if index <= 0 or index >= len(tokens) or protected_boundary(tokens, index):
        return None
    prev, current = tokens[index - 1], norm(tokens[index])
    if ends_sentence(prev):
        return 1
    if re.search(r"[;:—][\"')]*$", prev) or (prev.rstrip('"\'').endswith(",") and len(tokens) - index >= 3):
        return 2
    if current in SUBORDINATORS:
        return 3
    if current in COORDINATORS and any(is_verb(t) for t in tokens[index + 1:index + 3]):
        return 4
    if current in PREPOSITIONS and len(tokens) - index >= 3:
        return 5
    if current == "to" and index + 1 < len(tokens) and is_verb(tokens[index + 1]):
        return 6
    return None


def best_boundary(tokens: list[str], require_limit: bool = False) -> int | None:
    candidates: list[tuple[int, float, int]] = []
    middle = len(tokens) / 2
    for index in range(1, len(tokens)):
        priority = boundary_priority(tokens, index)
        if priority is None:
            continue
        left = " ".join(tokens[:index])
        right = " ".join(tokens[index:])
        if require_limit and (len(left) > MAX_CUE_CHARS or len(right) > MAX_CUE_CHARS):
            continue
        candidates.append((priority, abs(index - middle), index))
    if candidates:
        return min(candidates)[2]
    legal = [i for i in range(MIN_WORDS, len(tokens) - MIN_WORDS + 1) if not protected_boundary(tokens, i)]
    return min(legal, key=lambda i: abs(i - middle)) if legal else None


def split_syntax(text: str) -> list[str]:
    tokens = text.replace("\n", " ").split()
    if not tokens:
        return []
    queue = [tokens]
    chunks: list[list[str]] = []
    while queue:
        current = queue.pop(0)
        rendered = " ".join(current)
        if len(current) <= MAX_WORDS and len(rendered) <= MAX_CUE_CHARS:
            chunks.append(current)
            continue
        split_at = best_boundary(current, require_limit=True) or best_boundary(current)
        if split_at is None:
            chunks.append(current)
            continue
        queue.insert(0, current[split_at:])
        queue.insert(0, current[:split_at])

    merged: list[list[str]] = []
    for chunk_index, chunk in enumerate(chunks):
        if len(chunk) >= MIN_WORDS or (chunk and ends_sentence(chunk[-1]) and chunk[0][:1].isupper()):
            merged.append(chunk)
            continue
        if merged and chunk[0][:1].islower():
            merged[-1].extend(chunk)
        elif merged and ends_sentence(merged[-1][-1]):
            if chunk_index + 1 < len(chunks):
                chunks[chunk_index + 1][0:0] = chunk
            else:
                merged[-1].extend(chunk)
        elif merged:
            merged[-1].extend(chunk)
        else:
            merged.append(chunk)
    return [" ".join(chunk) for chunk in merged if chunk]


def wrap_syntax(text: str) -> list[str]:
    if len(text) <= MAX_LINE:
        return [text]
    tokens = text.split()
    candidates = []
    for index in range(1, len(tokens)):
        if protected_boundary(tokens, index):
            continue
        left, right = " ".join(tokens[:index]), " ".join(tokens[index:])
        if len(left) <= MAX_LINE and len(right) <= MAX_LINE:
            candidates.append((boundary_priority(tokens, index) or 99, abs(len(left) - len(right)), index))
    if not candidates:
        return [text]
    index = min(candidates)[2]
    return [" ".join(tokens[:index]), " ".join(tokens[index:])]


def srt_ts(seconds: float) -> str:
    total_ms = int(round(seconds * 1000))
    hours, rem = divmod(total_ms, 3_600_000)
    minutes, rem = divmod(rem, 60_000)
    secs, millis = divmod(rem, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def make_stub_cues(duration: float = 46.0) -> list[dict]:
    text = (
        "A warning and a ride home. A child was handed a form giving up the right to a lawyer. "
        "He was taught to trust the adults in the room, although the officer did not tell him the truth. "
        "He was held for forty-eight hours before the statement was signed. Police can lie during an interrogation, "
        "but a court must still decide whether a confession was voluntary."
    )
    chunks = split_syntax(text)
    weights = [max(1, word_count(chunk)) for chunk in chunks]
    available = duration - GAP * max(0, len(chunks) - 1)
    total = sum(weights)
    cues, cursor = [], 0.0
    for i, (chunk, weight) in enumerate(zip(chunks, weights)):
        natural = max(MIN_DUR, min(MAX_DUR, available * weight / total))
        natural = max(natural, len(chunk) / MAX_CPS)
        end = min(duration, cursor + natural)
        cues.append({"start": round(cursor, 3), "end": round(end, 3), "text": chunk})
        cursor = end + GAP
    return cues


def write_outputs(cues: list[dict], stem: str) -> Path:
    scenes = EPDIR / "04_scenes"
    edit = EPDIR / "08_edit"
    scenes.mkdir(parents=True, exist_ok=True)
    edit.mkdir(parents=True, exist_ok=True)
    srt_path = edit / f"captions.{stem}.srt"
    srt_lines: list[str] = []
    json_cues = []
    for index, cue in enumerate(cues, start=1):
        lines = wrap_syntax(cue["text"])
        srt_lines.extend([str(index), f"{srt_ts(cue['start'])} --> {srt_ts(cue['end'])}", *lines, ""])
        json_cues.append({**cue, "lines": lines})
    payload = "\n".join(srt_lines).strip() + "\n"
    srt_path.write_text(payload, encoding="utf-8")
    (scenes / f"captions.{stem}.srt").write_text(payload, encoding="utf-8")
    (scenes / f"captions.{stem}.json").write_text(json.dumps({"episode_id": EP, "cues": json_cues}, indent=2), encoding="utf-8")
    ass_events = []
    for cue in cues:
        ass_text = r"\N".join(wrap_syntax(cue["text"]))
        ass_events.append(
            f"Dialogue: 0,{srt_ts(cue['start']).replace(',', '.')},{srt_ts(cue['end']).replace(',', '.')},Default,,0,0,0,,{ass_text}"
        )
    ass = "[Script Info]\nScriptType: v4.00+\nPlayResX: 1920\nPlayResY: 1080\n\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BorderStyle, Outline, Alignment\nStyle: Default,Oswald,54,&H00F5F7FA,&H00000000,3,3,2\n\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n" + "\n".join(ass_events) + "\n"
    (scenes / f"captions.{stem}.ass").write_text(ass, encoding="utf-8")
    return srt_path


def validate(path: Path) -> None:
    result = subprocess.run([sys.executable, str(ROOT / "scripts" / "check_caption_breaks.py"), str(path)], cwd=ROOT)
    if result.returncode != 0:
        raise SystemExit("caption breaks gate FAILED - do not ship this SRT")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ep", default=EP)
    parser.add_argument("--stub", action="store_true")
    args = parser.parse_args()
    if args.ep != EP:
        raise SystemExit(f"This generator is locked to {EP}")
    if not args.stub:
        raise SystemExit("Production forced alignment requires the approved narration master; run with --stub for B-6 smoke validation.")
    out = write_outputs(make_stub_cues(), "final.stub.syntax.v001")
    validate(out)
    print(f"wrote {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
