"""Build one 1920x1080@48fps clip per EP38 shot from the shotlist.
- Wan hero shots: use the RIFE'd clip, setpts-stretched (capped 2.2x) then freeze-hold
  the tail with a continued micro-zoom so nothing is ever frozen-static.
- Still shots: 4K Codex still with a slow 2.5D zoompan push (+ gentle pan).
Outputs numbered clips into 08_edit/shots/NNNN.mp4 for deterministic concat.
Idempotent per shot (skips if up-to-date unless --force). --only S07 for a single test.
"""
from __future__ import annotations
import argparse, json, subprocess, sys
from pathlib import Path

ROOT = Path(r"C:\Users\aab15\Documents\prime-documentary")
EP = "PD-2026-038-kidsforcash"
SHOTLIST = ROOT / "episodes" / EP / "04_scenes" / "shotlist.v001.json"
STILL_DIR = Path(r"H:/pd-media/assets/ai/kidsforcash")
RIFE_DIR = Path(r"H:/pd-media/assets/ai_video/kidsforcash")
OUTDIR = ROOT / "episodes" / EP / "08_edit" / "shots"
FFMPEG = r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe"
FFPROBE = r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffprobe.exe"
FPS = 48
W, H = 1920, 1080
WAN = {"S03", "S05", "S07", "S08", "S10", "S12", "S14", "S16", "S22", "S23", "S29", "S37"}


def sh(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True)


def img_of(shot: dict) -> str:
    return shot.get("image") or shot.get("image_path") or ""


def stem_of(shot: dict) -> str:
    p = img_of(shot)
    return Path(p).stem.upper() if p else ""


OVERLAYS = [
    Path(r"H:/pd-media/assets/factory/particle_assets/AF-PART-0049__dust_particles_floating.mp4"),
    Path(r"H:/pd-media/assets/factory/light_assets/AF-LIGHT-0060__light_leak_overlay.mp4"),
]


# per-occurrence framing so a REUSED image reads as a different shot (owner: 同じ画像使いすぎ).
# (zoom_start, center_x_frac, center_y_frac, pan_dir)
FRAMINGS = [
    (1.00, 0.50, 0.50, (1, 0)),   # occ0: wide, push-in, pan right
    (1.20, 0.35, 0.40, (0, 1)),   # occ1: tight upper-left, pan down
    (1.20, 0.66, 0.60, (-1, 0)),  # occ2: tight lower-right, pan left
    (1.32, 0.50, 0.38, (1, 1)),   # occ3: tight top-center
    (1.26, 0.40, 0.64, (0, -1)),  # occ4: tight lower-left
    (1.28, 0.62, 0.42, (-1, -1)), # occ5: tight upper-right
]


def build_still(img: Path, dur: float, out: Path, idx: int, occ: int = 0) -> bool:
    # NOT a flat static zoom (reads as 紙芝居). Smooth push-in + pan (jitter-free linear crop)
    # + a real moving atmospheric overlay (drifting dust/light, screen-blended). Framing varies
    # by occurrence so reused stills look like different shots.
    frames = max(2, round(dur * FPS))
    N = frames - 1
    zstart, cxf, cyf, (dirx, diry) = FRAMINGS[occ % len(FRAMINGS)]
    z = f"({zstart:.3f}+0.15*n/{N})"                     # push in over the shot
    cw = f"floor((iw/{z})/2)*2"
    ch = f"floor((ih/{z})/2)*2"
    # window centered on (cxf,cyf), drifting a little (pan), clamped inside the frame.
    cx = (f"clip({cxf:.3f}*in_w+{0.10*dirx:.3f}*in_w*(n/{N}-0.5)-out_w/2,0,in_w-out_w)")
    cy = (f"clip({cyf:.3f}*in_h+{0.10*diry:.3f}*in_h*(n/{N}-0.5)-out_h/2,0,in_h-out_h)")
    ov = OVERLAYS[(idx + occ) % len(OVERLAYS)]
    op = 0.45 if "PART" in ov.name else 0.32
    fc = (
        f"[0:v]crop=w='{cw}':h='{ch}':x='{cx}':y='{cy}',scale={W}:{H}:flags=bicubic,setsar=1[base];"
        f"[1:v]scale={W}:{H},fps={FPS},format=gbrp,setsar=1[ovl];"
        f"[base][ovl]blend=all_mode=screen:all_opacity={op},format=yuv420p[v]"
    )
    r = sh([FFMPEG, "-y", "-hide_banner", "-loop", "1", "-framerate", str(FPS), "-i", str(img),
            "-stream_loop", "-1", "-i", str(ov), "-t", f"{dur:.4f}",
            "-filter_complex", fc, "-map", "[v]", "-r", str(FPS),
            "-c:v", "libx264", "-preset", "medium", "-crf", "18", str(out)])
    return r.returncode == 0 and out.exists()


def build_wan(rife_mp4: Path, dur: float, out: Path) -> bool:
    # native rife clip ~3.42s. Stretch up to 2.2x to fill; if still short, freeze-hold
    # the tail with a slow continued zoom so it never sits perfectly static.
    probe = sh([FFPROBE, "-v", "quiet", "-show_entries", "format=duration",
                "-of", "csv=p=0", str(rife_mp4)])
    try:
        native = float(probe.stdout.strip())
    except Exception:
        native = 3.42
    stretch = min(1.35, max(1.0, dur / native))   # keep motion near-natural speed (was too slow at 2.2x)
    stretched = native * stretch
    hold = max(0.0, dur - stretched)
    vf = (f"setpts={stretch:.4f}*PTS,scale={W}:{H}:force_original_aspect_ratio=increase,"
          f"crop={W}:{H}")
    if hold > 0.02:
        # tpad clones the last frame; add a tiny zoom on the hold via a second zoompan is
        # overkill in one graph, so use tpad clone (kept subtle since hold is short).
        vf += f",tpad=stop_mode=clone:stop_duration={hold:.4f}"
    vf += ",format=yuv420p"
    r = sh([FFMPEG, "-y", "-hide_banner", "-i", str(rife_mp4),
            "-vf", vf, "-r", str(FPS), "-t", f"{dur:.4f}",
            "-c:v", "libx264", "-preset", "medium", "-crf", "18", str(out)])
    return r.returncode == 0 and out.exists()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default=None, help="only build shots using this image id, e.g. S07")
    ap.add_argument("--limit", type=int, default=0, help="build only first N shots (test)")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    data = json.loads(SHOTLIST.read_text(encoding="utf-8"))
    shots = data.get("shots") or data
    OUTDIR.mkdir(parents=True, exist_ok=True)
    built = 0; failed = []
    occ_count: dict[str, int] = {}   # per-image occurrence -> vary framing on reuse
    for i, shot in enumerate(shots):
        start = float(shot.get("start_sec", shot.get("start", 0)))
        end = float(shot.get("end_sec", shot.get("end", 0)))
        dur = round(end - start, 4)
        if dur <= 0:
            continue
        sid = stem_of(shot)
        if args.only and sid != args.only.upper():
            continue
        out = OUTDIR / f"{i:04d}.mp4"
        # S23 (chair distortion) + S37 (robe distortion): the Wan i2v broke geometry, so
        # fall back to the clean Codex still with a smooth push instead.
        DISTORTED = {"S23", "S37"}
        ok = False
        if shot.get("wan") and sid not in DISTORTED and (RIFE_DIR / f"{sid}_rife.mp4").exists():
            ok = build_wan(RIFE_DIR / f"{sid}_rife.mp4", dur, out)
            kind = "WAN"
        else:
            img = STILL_DIR / f"{sid}.png"
            if not img.exists():
                failed.append((i, sid, "no still")); continue
            ok = build_still(img, dur, out, i)
            kind = "still"
        if ok:
            built += 1
            print(f"  [{i:04d}] {sid} {kind} {dur:.2f}s -> {out.name}", flush=True)
        else:
            failed.append((i, sid, "render failed"))
            print(f"  [{i:04d}] {sid} {kind} FAILED", flush=True)
        if args.limit and built >= args.limit:
            break
    print(f"\nbuilt {built} shots; failed {len(failed)}")
    for f in failed:
        print("  FAIL", f)
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
