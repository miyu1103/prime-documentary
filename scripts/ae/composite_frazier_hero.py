"""EP39 frazier - composite the AE hero beats onto the finished CaseFilm.

Each rendered beat (ae_hero/<id>.mp4) is an opaque full-frame 1920x1080@30 clip
with its own head/tail black dips, so overlaying it across its narration window
cleanly REPLACES whatever the CaseFilm cut had there (no doubling). Audio is
copied unchanged. A new versioned file is written; the shipped input is never
touched.

Usage:
  py -3.11 scripts/ae/composite_frazier_hero.py <base.mp4> <out_v003_ae.mp4>

Windows come from beats.json (start/end, resolved from the spec design_t). If
the real cut's narration timings move, regenerate beats.json first - or pass
--windows <json> with {"hb01": [start, end], ...} to override.

Robustness (same contract as EP38):
  - Any beat whose mp4 is missing / wrong size / short / past the end of the
    base is SKIPPED; that window simply stays as the original cut.
  - Never overwrites the base; verifies the output duration afterwards.
"""
from __future__ import annotations
import json
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

WORK = Path("E:/pd-media/episodes/PD-2026-039-frazier/08_edit/ae_hero")
RENDER = WORK
FFMPEG = r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe"
FFPROBE = r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffprobe.exe"
W, H, FPS = 1920, 1080, 30


def probe_dur(f) -> float:
    r = subprocess.run([FFPROBE, "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(f)], capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return -1.0


def probe_wh(f) -> str:
    r = subprocess.run([FFPROBE, "-v", "error", "-select_streams", "v:0", "-show_entries",
                        "stream=width,height", "-of", "csv=p=0:s=x", str(f)],
                       capture_output=True, text=True)
    return r.stdout.strip()


def main() -> int:
    args = [a for a in sys.argv[1:]]
    override = {}
    if "--windows" in args:
        i = args.index("--windows")
        override = json.loads(Path(args[i + 1]).read_text(encoding="utf-8"))
        del args[i:i + 2]
    if len(args) < 2:
        print(__doc__, file=sys.stderr)
        return 1
    base, out = Path(args[0]), Path(args[1])
    if not base.exists():
        print(f"MISSING base {base}", file=sys.stderr)
        return 2
    if out.resolve() == base.resolve():
        print("REFUSING to overwrite the base file", file=sys.stderr)
        return 2
    if out.exists():
        print(f"REFUSING to overwrite existing output {out}", file=sys.stderr)
        return 2

    beats = json.loads((WORK / "beats.json").read_text(encoding="utf-8"))
    base_dur = probe_dur(base)
    print(f"[base] {base.name}  dur={base_dur:.2f}s  {probe_wh(base)}")

    valid, skipped = [], []
    for b in beats:
        if b["id"] in override:
            b = dict(b, start=float(override[b["id"]][0]), end=float(override[b["id"]][1]))
        mp4 = RENDER / f"{b['id']}.mp4"
        if not mp4.exists():
            skipped.append((b["id"], "missing mp4")); continue
        d, wh = probe_dur(mp4), probe_wh(mp4)
        if wh != f"{W}x{H}":
            skipped.append((b["id"], f"wrong size {wh}")); continue
        if d < b["dur"] - 0.3:
            skipped.append((b["id"], f"short {d:.2f}<{b['dur']:.2f}")); continue
        if b["end"] > base_dur:
            skipped.append((b["id"], "window past end of base")); continue
        valid.append(dict(b, mp4=str(mp4), rdur=d))
        print(f"  [ok] {b['id']}  {b['start']:.2f}-{b['end']:.2f}  {mp4.name} dur={d:.2f}")
    for sid, why in skipped:
        print(f"  [SKIP] {sid}: {why}", file=sys.stderr)
    if not valid:
        print("no valid beats - nothing to composite", file=sys.stderr)
        return 3

    inputs, parts, prev = ["-i", str(base)], [], "0:v"
    for k, b in enumerate(valid):
        inputs += ["-i", b["mp4"]]
        idx = k + 1
        parts.append(f"[{idx}:v]setpts=PTS-STARTPTS+{b['start']:.3f}/TB,format=yuv420p[b{k}]")
        outl = f"v{k}"
        parts.append(f"[{prev}][b{k}]overlay=0:0:eof_action=pass:"
                     f"enable='between(t,{b['start']:.3f},{b['end']:.3f})'[{outl}]")
        prev = outl
    fg = ";".join(parts)

    cmd = [FFMPEG, "-y", "-hide_banner", *inputs, "-filter_complex", fg,
           "-map", f"[{prev}]", "-map", "0:a",
           "-r", str(FPS), "-c:v", "libx264", "-preset", "medium", "-crf", "16",
           "-pix_fmt", "yuv420p", "-c:a", "copy", str(out)]
    print(f"[composite] {len(valid)} beats -> {out.name} ...", flush=True)
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-3000:], file=sys.stderr)
        return 4

    od = probe_dur(out)
    print(f"[done] {out.name}  dur={od:.2f}s  {probe_wh(out)}")
    if abs(od - base_dur) > 0.5:
        print(f"WARN duration drift {od:.2f} vs base {base_dur:.2f}", file=sys.stderr)
    if skipped:
        print(f"NOTE: {len(skipped)} beat(s) skipped (windows left as original cut): "
              + ", ".join(s for s, _ in skipped), file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
