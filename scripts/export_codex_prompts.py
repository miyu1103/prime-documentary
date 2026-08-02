#!/usr/bin/env python3
"""Export every GENERATE plate as a Codex-ready prompt pack.

Emits three files so the pack is usable by a person, by a script, and by whoever has to check the
output later:

  SHORTS_CODEX_PROMPTS.v001.jsonl  one record per image — the machine-readable source of truth
  SHORTS_CODEX_PROMPTS.v001.md     the same, grouped and readable, for handing to Codex
  SHORTS_CODEX_PROMPTS.v001.csv    filename,prompt — for a bulk runner

Filenames are deterministic: short<NN>_<nn>.png. That is exactly the name the Remotion composition
already expects under remotion/public/shorts/short<NN>/, so returned images drop straight in with
no renaming step and no mapping file to lose.

Usage: py -3.11 scripts/export_codex_prompts.py
"""
from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGNS = ROOT / "episodes" / "_planning" / "short_designs"
OUT = ROOT / "episodes" / "_planning"
VOCAB = json.loads((OUT / "SHORTS_MOTIF_VOCABULARY.v001.json").read_text(encoding="utf-8"))


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    records = []
    for f in sorted(DESIGNS.glob("*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        for s in d["shorts"]:
            if not s.get("angle"):
                continue
            for p in (s.get("plates") or []):
                if not p or p.get("source") != "GENERATE" or not p.get("prompt"):
                    continue
                sid = s["short_id"]
                nn = int(re.sub(r"\D", "", sid))
                records.append({
                    "filename": f"{sid}_{p['n']:02d}.png",
                    "short_id": sid,
                    "episode_id": d["episode_id"],
                    "slug": d["episode_id"].split("-", 3)[3],
                    "plate": p["n"],
                    "role": p.get("role"),
                    "line": p.get("line"),
                    "subject": p.get("subject"),
                    "era": s.get("era"),
                    "prompt": p["prompt"],
                    "negative": VOCAB["negative"],
                    "width": 1080, "height": 1920,
                    "dest_dir": f"remotion/public/shorts/{sid}/",
                })
    records.sort(key=lambda r: (int(re.sub(r"\D", "", r["short_id"])), r["plate"]))

    jl = OUT / "SHORTS_CODEX_PROMPTS.v001.jsonl"
    with jl.open("w", encoding="utf-8") as fh:
        for r in records:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")

    cs = OUT / "SHORTS_CODEX_PROMPTS.v001.csv"
    with cs.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["filename", "width", "height", "prompt", "negative"])
        for r in records:
            w.writerow([r["filename"], r["width"], r["height"], r["prompt"], r["negative"]])

    by_short: dict[str, list] = {}
    for r in records:
        by_short.setdefault(r["short_id"], []).append(r)

    L = [
        "# Codex 縦型画像プロンプト v001",
        "",
        f"**{len(records)} 枚** / {len(by_short)} 本のショート / {len({r['slug'] for r in records})} 話ぶん。",
        "",
        "## 出力の指定（全枚共通）",
        "",
        "| | |",
        "|---|---|",
        "| サイズ | **1080 × 1920 ちょうど**（16:9で作って切るのは不可） |",
        "| 形式 | PNG / sRGB |",
        "| ファイル名 | 各プロンプトの見出しの名前をそのまま使ってください |",
        "| ネガティブ | 全枚共通。下記 |",
        "",
        "```",
        VOCAB["negative"],
        "```",
        "",
        "## 守ってほしいこと（全部、壊してから学んだものです）",
        "",
    ]
    for k, v in VOCAB["hard_rules_baked_into_every_prompt"].items():
        L.append(f"- **{k.split('_', 1)[1].replace('_', ' ')}** — {v}")
    L += [
        "",
        "プロンプト本文には既にこれらが書き込んであります。**文言を削らずにそのまま渡してください。**",
        "",
        "## 納品",
        "",
        "- ファイル名は `short<NN>_<nn>.png`。この名前のまま返してください（`remotion/public/shorts/short<NN>/` にそのまま入ります）",
        "- **ラベル付きコンタクトシート**を1バッチにつき1枚。目視選別に使います",
        "- 1枚ずつの説明は不要です（下の `subject` が対応します）",
        "",
        "---",
        "",
    ]
    for sid, rs in by_short.items():
        ep = rs[0]["slug"]
        L += [f"## {sid} — {ep}", f"*時代設定：{rs[0]['era']}* / {len(rs)} 枚", ""]
        for r in rs:
            L += [f"### `{r['filename']}`  ({r['role']} / {r['line']})",
                  f"> {r['subject']}", "", "```", r["prompt"], "```", ""]
    (OUT / "SHORTS_CODEX_PROMPTS.v001.md").write_text("\n".join(L), encoding="utf-8")

    print(f"{len(records)} prompts across {len(by_short)} shorts")
    print(f"  {jl.relative_to(ROOT)}   {jl.stat().st_size//1024} kB")
    print(f"  {cs.relative_to(ROOT)}   {cs.stat().st_size//1024} kB")
    md = OUT / 'SHORTS_CODEX_PROMPTS.v001.md'
    print(f"  {md.relative_to(ROOT)}   {md.stat().st_size//1024} kB")
    per = [len(v) for v in by_short.values()]
    print(f"  per short: min {min(per)} max {max(per)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
