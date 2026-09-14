"""EP39 frazier - composite ALL AE overlays (8 hero beats + resolvable cards) onto
the finished BGM base in a SINGLE re-encode pass. Each overlay mp4 is a full-frame
1920x1080@30 opaque clip with its own head/tail dips, so it cleanly REPLACES the
base for its window. Audio (the master VO + BGM) is copied unchanged. Never
overwrites the base; a new versioned file is written.

Hero windows come from ae_hero/beats.json. Card windows come from
scripts/ae/frazier_cards_timing.json (start + dur, film time). Any overlay whose
mp4 is missing / wrong size / too short / past the end of the base is SKIPPED
(that window stays as the original cut).

Usage: python scripts/ae/composite_frazier_all.py <base.mp4> <out_v002_ae.mp4>
"""
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EDIT = Path("E:/pd-media/episodes/PD-2026-039-frazier/08_edit")
HERO = EDIT / "ae_hero"
CARDS_DIR = EDIT / "ae_cards"
TIMING = ROOT / "scripts" / "ae" / "frazier_cards_timing.json"
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
    if len(sys.argv) < 3:
        print(__doc__, file=sys.stderr); return 1
    base, out = Path(sys.argv[1]), Path(sys.argv[2])
    if not base.exists():
        print(f"MISSING base {base}", file=sys.stderr); return 2
    if out.resolve() == base.resolve():
        print("REFUSING to overwrite the base", file=sys.stderr); return 2
    if out.exists():
        print(f"REFUSING to overwrite existing output {out}", file=sys.stderr); return 2
    base_dur = probe_dur(base)
    print(f"[base] {base.name} dur={base_dur:.2f}s {probe_wh(base)}")

    overlays = []  # (label, mp4, start, end)
    for b in json.loads((HERO / "beats.json").read_text("utf-8")):
        overlays.append((b["id"], HERO / f"{b['id']}.mp4", float(b["start"]),
                         float(b["end"]), float(b["dur"])))
    tim = json.loads(TIMING.read_text("utf-8"))
    for c in tim["cards"]:
        s = float(c["start"]); dur = float(c["dur"])
        overlays.append((c["id"], CARDS_DIR / f"{c['id']}.mp4", s, s + dur, dur))

    valid, skipped = [], []
    for oid, mp4, s, e, dur in sorted(overlays, key=lambda x: x[2]):
        if not mp4.exists():
            skipped.append((oid, "missing mp4")); continue
        d, wh = probe_dur(mp4), probe_wh(mp4)
        if wh != f"{W}x{H}":
            skipped.append((oid, f"wrong size {wh}")); continue
        if d < dur - 0.3:
            skipped.append((oid, f"short {d:.2f}<{dur:.2f}")); continue
        if e > base_dur:
            skipped.append((oid, "window past end")); continue
        valid.append((oid, mp4, s, e));
        print(f"  [ok] {oid:16s} {s:7.2f}-{e:7.2f}  ({mp4.parent.name}/{mp4.name})")
    for oid, why in skipped:
        print(f"  [SKIP] {oid}: {why}", file=sys.stderr)
    if not valid:
        print("no valid overlays", file=sys.stderr); return 3

    inputs = ["-i", str(base)]
    parts, prev = [], "0:v"
    for k, (oid, mp4, s, e) in enumerate(valid):
        inputs += ["-i", str(mp4)]
        parts.append(f"[{k+1}:v]setpts=PTS-STARTPTS+{s:.3f}/TB,format=yuv420p[b{k}]")
        parts.append(f"[{prev}][b{k}]overlay=0:0:eof_action=pass:"
                     f"enable='between(t,{s:.3f},{e:.3f})'[v{k}]")
        prev = f"v{k}"
    cmd = [FFMPEG, "-y", "-hide_banner", *inputs, "-filter_complex", ";".join(parts),
           "-map", f"[{prev}]", "-map", "0:a", "-r", str(FPS),
           "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p",
           "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
           "-c:a", "copy", str(out)]
    print(f"[composite] {len(valid)} overlays -> {out.name} ...", flush=True)
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-3000:], file=sys.stderr); return 4
    od = probe_dur(out)
    print(f"[done] {out.name} dur={od:.2f}s {probe_wh(out)} overlays={len(valid)} skipped={len(skipped)}")
    if abs(od - base_dur) > 0.5:
        print(f"WARN duration drift {od:.2f} vs {base_dur:.2f}", file=sys.stderr)
    if skipped:
        print("NOTE skipped: " + ", ".join(s for s, _ in skipped), file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
