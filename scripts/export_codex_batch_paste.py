#!/usr/bin/env python3
"""Split a long-form CODEX_BATCH_A image order into paste-ready batches for Codex.

Reads an order written in the EP72-onward markdown-table shape:

    **`[STYLE]`** — prepend to every plate:
    > <the style macro>
    **`[NEG]`** — append to every plate...
    > <the negative macro>
    ### <SECTION HEADING>
    | id | beat | prompt | flags |
    | H001 | the beat | the subject | R D W |

and writes, into `<order-dir>/<EPTAG>_CODEX_PASTE/`:

    batch_01.txt … batch_NN.txt   what a person pastes into Codex, house format, Japanese header
    plates.v001.jsonl             one record per plate — the machine-readable source of truth

This is NOT a second implementation of `export_codex_prompts.py`. That script serves the SHORTS
pipeline: it reads `_planning/short_designs/*` plus `SHORTS_MOTIF_VOCABULARY.v001.json` and emits
`short<NN>_<nn>.png` names for the vertical compositions. It cannot read a long-form order and has
no notion of `[STYLE]`/`[NEG]` macros or plate flags. The two share no inputs and no outputs.

Filenames are deterministic: `<ID>.png`, which is exactly what `remotion/public/<slug>/img/`
already expects, so returned images drop straight in with no renaming and no mapping file to lose.

Usage:
    py -3.11 scripts/export_codex_batch_paste.py \
        --order episodes/_planning/EP75_lahaina_CODEX_BATCH_A.v001.md --per-batch 8
    py -3.11 scripts/export_codex_batch_paste.py --order <path> --dry-run
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROW = re.compile(
    r"^\|\s*([A-Z]{1,2}\d{2,3})\s*\|\s*([^|]*?)\s*\|\s*([^|]+?)\s*\|\s*([^|]*?)\s*\|\s*$"
)
SECTION = re.compile(r"^###\s+(.+?)\s*$")


def macro(text: str, label: str) -> str:
    """The blockquote that follows the `**`[LABEL]`**` announcement line."""
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if f"`[{label}]`" in line and "—" in line:
            buf = []
            for j in range(i + 1, len(lines)):
                s = lines[j].strip()
                if s.startswith(">"):
                    buf.append(s.lstrip("> ").strip())
                elif buf:
                    break
            if buf:
                return " ".join(buf)
    raise SystemExit(f"[paste] no [{label}] blockquote found in the order")


def plates(text: str) -> list[dict]:
    out: list[dict] = []
    section = ""
    for line in text.splitlines():
        m = SECTION.match(line)
        if m:
            section = m.group(1)
            continue
        m = ROW.match(line)
        if not m:
            continue
        pid, beat, prompt, flags = (g.strip() for g in m.groups())
        if pid.lower() == "id" or len(prompt) < 20:
            continue
        out.append({"id": pid, "section": section, "beat": beat,
                    "prompt": prompt, "flags": flags.replace("**", "").split()})
    return out


HEADER = """{eptag} — 画像発注 バッチ {n}/{total}（{count}枚）
区分: {sections}

以下を1枚ずつ生成してください。**1プロンプト＝1枚**です。
複数のプロンプトをまとめて1枚にしないでください。
ファイル名は指定のとおりにしてください（連番がそのまま組み立てに使われます）。

──────── 全プロンプト共通の指定 ────────

各プロンプトの先頭に、次の [STYLE] を必ず付けてください:

{style}

各プロンプトに、次の [NEG] を「避けるもの」として必ず適用してください:

{neg}

──────── このバッチの{count}枚 ────────
"""


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001 - not worth failing an export over
        pass

    ap = argparse.ArgumentParser()
    ap.add_argument("--order", required=True, help="path to the *_CODEX_BATCH_A.v*.md order")
    ap.add_argument("--per-batch", type=int, default=8)
    ap.add_argument("--out", help="output dir (default: <order-dir>/<EPTAG>_CODEX_PASTE)")
    ap.add_argument("--dry-run", action="store_true", help="report and write nothing")
    a = ap.parse_args()

    order = Path(a.order)
    text = order.read_text(encoding="utf-8")
    style, neg = macro(text, "STYLE"), macro(text, "NEG")
    rows = plates(text)
    if not rows:
        print("[paste] FAIL no plate rows parsed — check the order's table shape")
        return 1

    ids = [r["id"] for r in rows]
    if len(set(ids)) != len(ids):
        dupes = sorted({i for i in ids if ids.count(i) > 1})
        print(f"[paste] FAIL duplicate plate ids: {', '.join(dupes)}")
        return 1

    eptag = order.name.split("_CODEX_BATCH")[0]
    out_dir = Path(a.out) if a.out else order.parent / f"{eptag}_CODEX_PASTE"
    chunks = [rows[i:i + a.per_batch] for i in range(0, len(rows), a.per_batch)]

    print(f"[paste] {order.name}: {len(rows)} plates -> {len(chunks)} batches of "
          f"{a.per_batch} into {out_dir}")
    print(f"[paste] STYLE {len(style)} chars | NEG {len(neg)} chars")
    people = [r["id"] for r in rows if "P" in r["flags"]]
    print(f"[paste] people plates (P): {len(people)}")
    if a.dry_run:
        print("[paste] --dry-run: nothing written")
        return 0

    out_dir.mkdir(parents=True, exist_ok=True)
    for n, chunk in enumerate(chunks, 1):
        secs = []
        for r in chunk:
            if r["section"] not in secs:
                secs.append(r["section"])
        body = HEADER.format(eptag=eptag, n=n, total=len(chunks), count=len(chunk),
                             sections=" / ".join(s.split("·")[0].strip() for s in secs),
                             style=style, neg=neg)
        for k, r in enumerate(chunk, 1):
            flags = " ".join(r["flags"])
            body += (f"\n{k}) {r['id']}.png"
                     f"\n   [{r['beat']}]  flags: {flags}"
                     f"\n   {r['prompt']}\n")
        (out_dir / f"batch_{n:02d}.txt").write_text(body, encoding="utf-8")

    rec = out_dir / "plates.v001.jsonl"
    with rec.open("w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps({**r, "file": f"{r['id']}.png",
                                 "style": style, "neg": neg}, ensure_ascii=False) + "\n")
    print(f"[paste] wrote {len(chunks)} batch files + {rec.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
