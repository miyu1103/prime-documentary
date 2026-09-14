#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from gen_captions_syntax import split_syntax, wrap_syntax, word_count


def flattened(text: str) -> str:
    return " | ".join(" / ".join(wrap_syntax(cue)) for cue in split_syntax(text))


def main() -> int:
    cases = [
        ("A warning and a ride home.", "ride | home."),
        ("A child was handed a form giving up the right to a lawyer.", "the right | to a lawyer"),
        ("They taught him to trust the adults in the room.", "the adults | in the room"),
        ("He was held for forty-eight hours before dawn.", "forty-eight | hours"),
        ("The officer did not tell him the truth.", "did not | tell"),
    ]
    for text, forbidden in cases:
        rendered = flattened(text)
        assert forbidden not in rendered, f"forbidden split {forbidden!r}: {rendered}"
    cues = split_syntax("Police can lie during an interrogation, but a court must decide whether a confession was voluntary.")
    assert all(word_count(cue) >= 3 for cue in cues), cues
    print("PASS caption_syntax: 6 syntax boundary cases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
