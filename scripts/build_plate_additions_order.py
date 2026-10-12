#!/usr/bin/env python3
"""Write the ADDITIONS order for an episode: every ordered plate that is not on disk, plus any
plate a reviewer rejected, each with its original prompt and an optional FIX line.

The list is a MEASUREMENT, not a memory: it is rebuilt from the order and from the delivery
directory every time it runs. On 2026-08-25 an additions file went stale between being written
and being read because Codex was still delivering (31 plates -> 37 in four minutes).

    py -3.11 scripts/build_plate_additions_order.py --slug katrina \
        --order episodes/_planning/EP85_katrina_CODEX_BATCH_A.v001.md \
        --plates episodes/_planning/EP85_katrina_CODEX_PASTE/plates.v001.jsonl \
        --dest "E:\\pd-media\\05_visuals\\katrina\\img" --out <file> [--reject W012=why ...]
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--plates", required=True, help="plates.v001.jsonl from the paste exporter")
    ap.add_argument("--dest", required=True, help="delivery directory to measure")
    ap.add_argument("--out", required=True)
    ap.add_argument("--header", help="file whose contents are prepended verbatim")
    ap.add_argument("--reject", action="append", default=[],
                    help="ID=reason -- a delivered plate a reviewer rejected; repeatable")
    a = ap.parse_args()

    rows = [json.loads(l) for l in Path(a.plates).read_text(encoding="utf-8").splitlines() if l.strip()]
    have = {f[:-4] for f in os.listdir(a.dest) if f.lower().endswith(".png")}
    rejects = {}
    for r in a.reject:
        k, _, v = r.partition("=")
        rejects[k.strip()] = v.strip()

    want = [r for r in rows if r["id"] not in have or r["id"] in rejects]
    lines = []
    if a.header:
        lines.append(Path(a.header).read_text(encoding="utf-8").rstrip("\n"))
        lines.append("")
    lines.append(f"---- {a.slug}: {len(want)} plate(s) -- save to {a.dest}\\")
    lines.append("")
    style = rows[0].get("style", "") if rows else ""
    if style:
        lines += ["[STYLE] (prepend to every prompt)", f"  {style}", ""]
    for i, r in enumerate(want, 1):
        flag = "  [P: person present, face must not be visible]" if "P" in (r.get("flags") or []) else ""
        lines.append(f"{i}) {r['id']}.png{flag}")
        lines.append(f"   {r['prompt']}")
        if r["id"] in rejects:
            lines.append(f"   FIX: {rejects[r['id']]}")
        lines.append("")
    Path(a.out).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[additions] {a.slug}: ordered {len(rows)}, on disk {len(have)}, "
          f"to (re)generate {len(want)} -> {a.out}")
    if not want:
        print("[additions] nothing outstanding")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
