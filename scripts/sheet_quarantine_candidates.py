#!/usr/bin/env python3
"""Labeled contact sheets for quarantine-restore candidates.

Input is the JSON that the gate-pass measurement writes
(runs/quarantine_gate_pass_*.json: {theme: [{id,title,file_path},...]}).
One middle frame per clip, tiled 6x4 per sheet with `NNN theme | title` burned in, so a
human can mark restore verdicts by index. A filename is not evidence; the frame is.

    py -3.11 scripts/sheet_quarantine_candidates.py runs/quarantine_gate_pass_20260825.json
Output: runs/qc/quarantine_restore_<date>/sheet_NN.jpg + index.json (index -> id/file_path)
"""
from __future__ import annotations

import json
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COLS, ROWS = 6, 4
CELL_W, CELL_H = 480, 300
FONT = "C\\:/Windows/Fonts/consola.ttf"


def grab(mp4: Path, out_png: Path) -> bool:
    r = subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-ss", "2", "-i", str(mp4),
         "-frames:v", "1", "-vf", f"scale={CELL_W}:{CELL_H}:force_original_aspect_ratio=decrease,"
         f"pad={CELL_W}:{CELL_H}:(ow-iw)/2:(oh-ih)/2", str(out_png)],
        capture_output=True)
    return r.returncode == 0 and out_png.is_file()


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass
    src = Path(sys.argv[1])
    data = json.loads(src.read_text(encoding="utf-8"))
    out_dir = ROOT / "runs" / "qc" / f"quarantine_restore_{date.today().strftime('%Y%m%d')}"
    tmp = out_dir / "_frames"
    tmp.mkdir(parents=True, exist_ok=True)

    rows = [dict(theme=t, **rec) for t, recs in data.items() for rec in recs]
    index = {}
    cells = []
    for i, rec in enumerate(rows):
        fp = Path(rec["file_path"])
        png = tmp / f"{i:03d}.png"
        ok = fp.is_file() and grab(fp, png)
        if not ok:
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi",
                            "-i", f"color=c=black:s={CELL_W}x{CELL_H}", "-frames:v", "1",
                            str(png)], capture_output=True)
        label = f"{i:03d} {rec['theme'][:18]} | {rec['title'][:44]}"
        label = label.replace("'", "").replace('"', "").replace(":", " ").replace("\\", "/")
        lab = tmp / f"{i:03d}_l.png"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(png),
                        "-vf", f"drawtext=fontfile='{FONT}':text='{label}':x=4:y=h-20:"
                        "fontsize=13:fontcolor=white:box=1:boxcolor=black@0.65",
                        str(lab)], capture_output=True)
        cells.append(lab if lab.is_file() else png)
        index[i] = {"id": rec["id"], "theme": rec["theme"], "file_path": rec["file_path"],
                    "title": rec["title"]}

    per = COLS * ROWS
    n_sheets = (len(cells) + per - 1) // per
    for s in range(n_sheets):
        chunk = cells[s * per:(s + 1) * per]
        while len(chunk) < per:
            chunk.append(chunk[-1])
        args = ["ffmpeg", "-v", "error", "-y"]
        for c in chunk:
            args += ["-i", str(c)]
        args += ["-filter_complex", f"xstack=inputs={per}:layout=" + "|".join(
            f"{(k % COLS) * CELL_W}_{(k // COLS) * CELL_H}" for k in range(per)),
            "-q:v", "4", str(out_dir / f"sheet_{s:02d}.jpg")]
        subprocess.run(args, capture_output=True)
        print(f"sheet_{s:02d}.jpg  ({len(chunk)} cells)")
    (out_dir / "index.json").write_text(json.dumps(index, indent=1, ensure_ascii=False),
                                        encoding="utf-8")
    print(f"{len(rows)} candidates -> {n_sheets} sheets in {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
