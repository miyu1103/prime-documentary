"""EP38 kidsforcash — composite AE hero beats onto the finished CaseFilm.

Overlays each rendered AE hero beat (render/<id>.mp4) fully over its narration
window in the current final (kidsforcash_final_bgm.v002.mp4). Beats are opaque,
same size/fps, with their own head/tail black dips, so each cleanly REPLACES the
CaseFilm figure at that window (no doubling). Audio is copied unchanged from
v002 (the -14 LUFS 3-layer mix). Output: kidsforcash_final_bgm.v003_ae.mp4.

Robustness ("破綻しないようにして"):
  - Any beat whose mp4 is missing / wrong-size / short is SKIPPED (that window
    stays exactly as the CaseFilm cut — never breaks the film).
  - Never overwrites v002; writes a new versioned file.
  - Verifies the output duration matches the base and streams are valid.
"""
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path

ROOT = Path(r"C:\Users\aab15\Documents\prime-documentary")
EP = "PD-2026-038-kidsforcash"
EDIT = ROOT / "episodes" / EP / "08_edit"
WORK = EDIT / "ae_hero"
RENDER = WORK / "render"
# base = finished video+audio mix; out = AE-composited result. Override via argv.
BASE = Path(sys.argv[1]) if len(sys.argv) > 1 else EDIT / "kidsforcash_final_bgm.v002.mp4"
OUT = Path(sys.argv[2]) if len(sys.argv) > 2 else EDIT / "kidsforcash_final_bgm.v003_ae.mp4"
FFMPEG = r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe"
FFPROBE = r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffprobe.exe"
W, H, FPS = 1920, 1080, 30


def probe_dur(f):
    r = subprocess.run([FFPROBE, "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(f)], capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return -1.0


def probe_wh(f):
    r = subprocess.run([FFPROBE, "-v", "error", "-select_streams", "v:0", "-show_entries",
                        "stream=width,height", "-of", "csv=p=0:s=x", str(f)],
                       capture_output=True, text=True)
    return r.stdout.strip()


def main() -> int:
    if not BASE.exists():
        print(f"MISSING base {BASE}", file=sys.stderr); return 2
    beats = json.loads((WORK / "beats.json").read_text(encoding="utf-8"))
    base_dur = probe_dur(BASE)
    print(f"[base] {BASE.name}  dur={base_dur:.2f}s  {probe_wh(BASE)}")

    valid, skipped = [], []
    for b in beats:
        mp4 = RENDER / f"{b['id']}.mp4"
        if not mp4.exists():
            skipped.append((b["id"], "missing mp4")); continue
        d, wh = probe_dur(mp4), probe_wh(mp4)
        if wh != f"{W}x{H}":
            skipped.append((b["id"], f"wrong size {wh}")); continue
        if d < b["dur"] - 0.3:
            skipped.append((b["id"], f"short {d:.2f}<{b['dur']:.2f}")); continue
        if b["end"] > base_dur:
            skipped.append((b["id"], "window past end")); continue
        valid.append(dict(b, mp4=str(mp4), rdur=d))
        print(f"  [ok] {b['id']}  {b['start']:.2f}-{b['end']:.2f}  {mp4.name} dur={d:.2f}")
    for sid, why in skipped:
        print(f"  [SKIP] {sid}: {why}", file=sys.stderr)

    if not valid:
        print("no valid beats — nothing to composite", file=sys.stderr); return 3

    # ---- build filter graph: base video + N opaque overlays gated to their windows ----
    inputs = ["-i", str(BASE)]
    parts, prev = [], "0:v"
    for k, b in enumerate(valid):
        inputs += ["-i", b["mp4"]]
        idx = k + 1
        parts.append(f"[{idx}:v]setpts=PTS-STARTPTS+{b['start']:.3f}/TB,format=yuv420p[b{k}]")
        out = f"v{k}"
        parts.append(f"[{prev}][b{k}]overlay=0:0:eof_action=pass:"
                     f"enable='between(t,{b['start']:.3f},{b['end']:.3f})'[{out}]")
        prev = out
    fg = ";".join(parts)

    cmd = [FFMPEG, "-y", "-hide_banner", *inputs, "-filter_complex", fg,
           "-map", f"[{prev}]", "-map", "0:a",
           "-r", str(FPS), "-c:v", "libx264", "-preset", "medium", "-crf", "16",
           "-pix_fmt", "yuv420p", "-c:a", "copy", str(OUT)]
    print(f"[composite] {len(valid)} beats -> {OUT.name} ...", flush=True)
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-3000:], file=sys.stderr); return 4

    od = probe_dur(OUT)
    print(f"[done] {OUT.name}  dur={od:.2f}s  {probe_wh(OUT)}")
    if abs(od - base_dur) > 0.5:
        print(f"WARN duration drift {od:.2f} vs base {base_dur:.2f}", file=sys.stderr)
    if skipped:
        print(f"NOTE: {len(skipped)} beat(s) skipped (windows left as original cut): "
              + ", ".join(s for s, _ in skipped), file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
