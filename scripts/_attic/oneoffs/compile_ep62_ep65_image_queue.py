#!/usr/bin/env python
"""Compile the EP62-EP65 Codex image orders into a validated JSON queue.

The source Markdown remains authoritative. This helper only expands [STYLE]/[NEG],
applies the explicitly documented thumbnail exceptions, and refuses ambiguous IDs.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class EpisodeOrder:
    episode: int
    slug: str
    prefix: str
    body_end: int
    order_path: Path
    thumb_path: Path
    body_thumb_ids: tuple[str, ...]
    new_thumb_id: str


ORDERS = (
    EpisodeOrder(
        62,
        "greene",
        "G",
        225,
        ROOT / "episodes/_planning/EP62_greene_CODEX_BATCH_A.v002.md",
        ROOT / "episodes/PD-2026-062-greene/04_scenes/thumb_prompts.v001.md",
        ("G220", "G221", "G222"),
        "G226",
    ),
    EpisodeOrder(
        63,
        "correa",
        "C",
        226,
        ROOT / "episodes/_planning/EP63_correa_CODEX_BATCH_A.v001.md",
        ROOT / "episodes/PD-2026-063-correa/04_scenes/thumb_prompts.v001.md",
        ("C221", "C222", "C223"),
        "C227",
    ),
    EpisodeOrder(
        64,
        "memphis",
        "M",
        218,
        ROOT / "episodes/_planning/EP64_memphis_CODEX_BATCH_A.v001.md",
        ROOT / "episodes/PD-2026-064-memphis/04_scenes/thumb_prompts.v001.md",
        ("M208", "M209", "M210"),
        "M219",
    ),
    EpisodeOrder(
        65,
        "marmet",
        "R",
        223,
        ROOT / "episodes/_planning/EP65_marmet_CODEX_BATCH_A.v001.md",
        ROOT / "episodes/PD-2026-065-marmet/04_scenes/thumb_prompts.v001.md",
        ("R217", "R218", "R219"),
        "R224",
    ),
)


THUMB_BRIGHTNESS = {
    62: (
        "bright even key light, the subject clearly separated from the ground, "
        "deep blacks kept but the subject held well above mid-grey, high micro-contrast"
    ),
    63: (
        "the subject itself brightly and evenly lit and clearly the brightest thing in the frame, "
        "the background dark but never crushed and still holding visible detail, high local contrast "
        "between the subject and the ground, graded up for legibility on a phone screen at 320 pixels wide"
    ),
    64: (
        "bright overall exposure, the main subject clearly separated and held well above mid-grey, "
        "deep blacks retained without crushing, very high local contrast, graded for legibility on a "
        "phone screen at 320 pixels wide"
    ),
    # The EP65 thumbnail order explicitly locks R217-R219 byte-for-byte and applies
    # brightness in compositing. R224 carries its own bright thumbnail-only style.
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def blockquote_after(text: str, marker: str) -> str:
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if marker in line:
            for candidate in lines[i + 1 :]:
                if candidate.startswith("> "):
                    return candidate[2:].strip()
                if candidate.strip() and not candidate.startswith(">"):
                    break
    raise ValueError(f"definition not found after {marker}")


def prompt_map(text: str, prefix: str) -> dict[str, list[str]]:
    lines = text.splitlines()
    found: dict[str, list[str]] = {}
    pattern = re.compile(rf"^- `(?P<id>{re.escape(prefix)}\d{{3}})\.png`(?:\s|$)")
    for i, line in enumerate(lines):
        match = pattern.match(line)
        if not match:
            continue
        asset_id = match.group("id")
        prompt = ""
        for candidate in lines[i + 1 :]:
            stripped = candidate.strip()
            if not stripped:
                continue
            if stripped.startswith(("*", ">", "#", "|", "- `")):
                break
            prompt = stripped
            break
        if prompt:
            found.setdefault(asset_id, []).append(prompt)
    return found


def exact_prompt(prompts: dict[str, list[str]], asset_id: str, source: Path) -> str:
    values = prompts.get(asset_id, [])
    unique = list(dict.fromkeys(values))
    if len(unique) != 1:
        raise ValueError(f"{source}: {asset_id} has {len(unique)} distinct prompt bodies")
    return unique[0]


def expand(prompt: str, style: str, neg: str, *, neg_without_wheelchair: bool = False) -> str:
    if neg_without_wheelchair:
        replaced = re.sub(r"(?i)(?:^|,\s*)wheelchair(?=,|$)", "", neg, count=1)
        replaced = re.sub(r"^,\s*", "", replaced).replace(", ,", ",")
        if replaced == neg:
            raise ValueError("wheelchair exception requested but token was not found")
        neg = replaced
    expanded = prompt.replace("[STYLE]", style).replace("[NEG]", neg)
    if "[STYLE]" in expanded or "[NEG]" in expanded:
        raise ValueError("unexpanded token remains")
    return re.sub(r"\s+", " ", expanded).strip()


def insert_before_style(prompt: str, phrase: str) -> str:
    if "[STYLE]" not in prompt:
        raise ValueError("thumbnail brightness insertion requires [STYLE]")
    return prompt.replace("[STYLE]", f", {phrase} [STYLE]", 1)


def build_queue() -> list[dict[str, object]]:
    queue: list[dict[str, object]] = []
    seen: set[str] = set()
    for order in ORDERS:
        order_text = read(order.order_path)
        thumb_text = read(order.thumb_path)
        style = blockquote_after(order_text, "**`[STYLE]`**")
        neg = blockquote_after(order_text, "**`[NEG]`**")
        body_prompts = prompt_map(order_text, order.prefix)
        thumb_prompts = prompt_map(thumb_text, order.prefix)
        expected = [f"{order.prefix}{i:03d}" for i in range(1, order.body_end + 1)]
        for asset_id in expected:
            prompt = exact_prompt(body_prompts, asset_id, order.order_path)
            is_thumb = asset_id in order.body_thumb_ids
            if is_thumb and order.episode in THUMB_BRIGHTNESS:
                prompt = insert_before_style(prompt, THUMB_BRIGHTNESS[order.episode])
            full_prompt = expand(
                prompt,
                style,
                neg,
                neg_without_wheelchair=asset_id in {"R220", "R221"},
            )
            queue.append(
                {
                    "episode": order.episode,
                    "slug": order.slug,
                    "asset_id": asset_id,
                    "filename": f"{asset_id}.png",
                    "kind": "body_thumbnail_shared" if is_thumb else "body",
                    "destination": str(Path(f"E:/pd-media/assets/ai/{order.slug}/{asset_id}.png")),
                    "source_markdown": str(order.order_path),
                    "prompt": full_prompt,
                }
            )
            seen.add(asset_id)

        new_prompt = exact_prompt(thumb_prompts, order.new_thumb_id, order.thumb_path)
        # G226 is already fully expanded in its thumbnail order. The other three
        # intentionally retain one or both tokens and are expanded from the body order.
        if "[STYLE]" in new_prompt or "[NEG]" in new_prompt:
            new_prompt = expand(new_prompt, style, neg)
        if "[STYLE]" in new_prompt or "[NEG]" in new_prompt:
            raise ValueError(f"{order.new_thumb_id}: unexpanded token remains")
        if order.new_thumb_id in seen:
            raise ValueError(f"duplicate queue id: {order.new_thumb_id}")
        queue.append(
            {
                "episode": order.episode,
                "slug": order.slug,
                "asset_id": order.new_thumb_id,
                "filename": f"{order.new_thumb_id}.png",
                "kind": "thumbnail_only",
                "destination": str(Path(f"E:/pd-media/assets/ai/{order.slug}/{order.new_thumb_id}.png")),
                "source_markdown": str(order.thumb_path),
                "prompt": re.sub(r"\s+", " ", new_prompt).strip(),
            }
        )
        seen.add(order.new_thumb_id)

    expected_total = sum(order.body_end for order in ORDERS) + len(ORDERS)
    if len(queue) != expected_total or len(seen) != expected_total:
        raise ValueError(f"queue contract mismatch: items={len(queue)} unique={len(seen)} expected={expected_total}")
    return queue


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path)
    parser.add_argument("--item", help="Print one queue item as JSON")
    args = parser.parse_args()
    queue = build_queue()
    if args.item:
        matches = [item for item in queue if item["asset_id"] == args.item]
        if len(matches) != 1:
            raise SystemExit(f"queue item not found or ambiguous: {args.item}")
        print(json.dumps(matches[0], ensure_ascii=False))
        return 0
    payload = {
        "schema_version": 1,
        "body_contract": {"greene": 225, "correa": 226, "memphis": 218, "marmet": 223},
        "body_total": 892,
        "thumbnail_only_ids": [order.new_thumb_id for order in ORDERS],
        "unique_total": len(queue),
        "items": queue,
    }
    rendered = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
