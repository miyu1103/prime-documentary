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

**アスペクト比は全枚 16:9（横1.778）で固定してください。**
シネスコ（2.35:1 / 2.25:1 / 2.13:1）にしないでください。16:9の映像に入れると、
誰も選んでいない切り取りか黒帯になります。**実測（EP75 lahaina・納品117枚時点）: 6枚が
シネスコで返ってきて作り直しになりました**（1881x836 = 2.25:1 と 1832x859 = 2.13:1）。
納品前に確認してください: 横÷縦 = 1.778 ちょうど。1672x941 でも 3840x2160 でも構いません。

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
    ap.add_argument("--only", help="comma-separated plate ids -- emit ONLY these, as a re-order")
    ap.add_argument("--outstanding", action="store_true",
                    help="compute --only automatically from the delivery dir: every ordered plate "
                         "that has not arrived, plus every delivered plate whose aspect ratio is "
                         "not 16:9. This is the file you hand back to the generator")
    ap.add_argument("--media", default="E:/pd-media/assets/ai",
                    help="delivery root for --outstanding (H: is gone; the media root moved to E:)")
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
    slug = eptag.split("_", 1)[1] if "_" in eptag else eptag

    # --- re-order modes ---------------------------------------------------------------------
    # A batch is never delivered clean in one pass, and hand-typing the leftovers is how an id
    # gets dropped. --outstanding reads the delivery directory and works out what is still owed:
    # never-arrived plates, plus delivered plates whose aspect ratio is not 16:9 (measured on
    # EP75 at 5-12% -- a tendency, not an accident, and invisible until the film letterboxes).
    only = None
    redo: set[str] = set()
    if a.outstanding:
        try:
            from PIL import Image
        except ImportError:
            print("[paste] FAIL --outstanding needs Pillow to read image dimensions")
            return 1
        dd = Path(a.media) / slug
        if not dd.is_dir():
            print(f"[paste] FAIL delivery dir not found: {dd}")
            return 1
        have = {p.stem.upper(): p for p in dd.glob("*.png")}
        missing = [r["id"] for r in rows if r["id"] not in have]
        bad = []
        for r in rows:
            p = have.get(r["id"])
            if p is None:
                continue
            w, h = Image.open(p).size
            if abs(w / h - 16 / 9) / (16 / 9) > 0.02:
                bad.append(r["id"])
        redo = set(bad)
        only = missing + bad
        print(f"[paste] outstanding: {len(missing)} never delivered, {len(bad)} wrong aspect ratio")
    elif a.only:
        only = [x.strip().upper() for x in a.only.split(",") if x.strip()]

    if only is not None:
        keep = set(only)
        rows = [r for r in rows if r["id"] in keep]
        if not rows:
            print(f"[paste] nothing outstanding -- every ordered plate is delivered at 16:9")
            return 0
        out_dir = Path(a.out) if a.out else order.parent / f"{eptag}_CODEX_REDO"
    else:
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
            tag = "  ★ 作り直し（既存ファイルを上書き）" if r["id"] in redo else ""
            body += (f"\n{k}) {r['id']}.png{tag}"
                     f"\n   [{r['beat']}]  flags: {flags}"
                     f"\n   {r['prompt']}\n")
        name = f"redo_{n:02d}.txt" if only is not None else f"batch_{n:02d}.txt"
        (out_dir / name).write_text(body, encoding="utf-8")

    # One combined file as well: the batches are for pasting eight at a time, this is for handing
    # the whole order to somebody in one piece. Same house convention as EP62_greene_CODEX_PASTE_ALL.
    stem = "redo" if only is not None else "batch"
    all_path = out_dir.parent / (f"{eptag}_CODEX_REDO_ALL.txt" if only is not None
                                 else f"{eptag}_CODEX_PASTE_ALL.txt")
    all_path.write_text(
        "\n\n".join((out_dir / f"{stem}_{n:02d}.txt").read_text(encoding="utf-8")
                    for n in range(1, len(chunks) + 1)),
        encoding="utf-8")
    print(f"[paste] wrote {all_path.name}")

    rec = out_dir / "plates.v001.jsonl"
    with rec.open("w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps({**r, "file": f"{r['id']}.png",
                                 "style": style, "neg": neg}, ensure_ascii=False) + "\n")
    print(f"[paste] wrote {len(chunks)} batch files + {rec.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
