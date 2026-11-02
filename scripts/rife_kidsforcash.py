"""RIFE-interpolate the 12 EP38 Wan hero cuts to smooth 48fps (4x = 2x twice).

Each Wan output dir holds 5 validate-probe frames (S##_00001..5) + 41 real frames
(S##_00006..46). We stage ONLY the 41 real frames, then RIFE 2x twice -> 164 frames.
164 @48fps = 3.42s of smooth slow-motion per hero cut (matches the ae-demo recipe).
Verifies frame counts (G-TIME-1). Outputs interpolated PNG frames + a preview mp4.
"""
from __future__ import annotations
import shutil, subprocess, sys
from pathlib import Path

RIFE = Path(r"D:/AI/tools/rife-ncnn-vulkan-20221029-windows/rife-ncnn-vulkan.exe")
SRC = Path(r"C:/Users/aab15/ComfyUI/output/wan_kfc")
WORK = Path(r"C:/Users/aab15/ComfyUI/output/_rife_work")
OUT = Path(r"E:/pd-media/assets/ai_video/kidsforcash")
FFMPEG = r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe"
SHOTS = ["S03", "S05", "S07", "S08", "S10", "S12", "S14", "S16", "S22", "S23", "S29", "S37"]
DROP_VALIDATE = 5  # first 5 frames per dir are the length=5 dry-validate probe


def rife_pass(src: Path, dst: Path) -> int:
    if dst.exists():
        shutil.rmtree(dst)
    dst.mkdir(parents=True, exist_ok=True)
    r = subprocess.run([str(RIFE), "-i", str(src), "-o", str(dst),
                        "-m", "rife-v4.6", "-f", "f%04d.png"],
                       capture_output=True, text=True)
    bad = [l for l in (r.stderr or "").splitlines() if "error" in l.lower() or "invalid" in l.lower()]
    if bad:
        print("  RIFE stderr:", bad[:3], file=sys.stderr)
    return len(list(dst.glob("f*.png")))


def main() -> int:
    if not RIFE.exists():
        print(f"MISSING RIFE: {RIFE}", file=sys.stderr); return 2
    WORK.mkdir(parents=True, exist_ok=True); OUT.mkdir(parents=True, exist_ok=True)
    results = []
    for s in SHOTS:
        allf = sorted(SRC.glob(f"{s}_000*.png"))
        real = allf[DROP_VALIDATE:] if len(allf) > 41 else allf
        if not real:
            print(f"  {s}: NO real frames"); results.append((s, 0)); continue
        # stage real frames renamed f0001.. so RIFE sees a clean ordered sequence
        stage = WORK / f"{s}_in"
        if stage.exists():
            shutil.rmtree(stage)
        stage.mkdir(parents=True)
        for i, p in enumerate(real, 1):
            shutil.copy2(p, stage / f"f{i:04d}.png")
        n0 = len(real)
        two = WORK / f"{s}_2x"
        n1 = rife_pass(stage, two)          # 2x
        four = OUT / f"{s}_rife"
        n2 = rife_pass(two, four)           # 2x again = 4x
        # preview mp4 @48fps
        mp4 = OUT / f"{s}_rife.mp4"
        subprocess.run([FFMPEG, "-y", "-hide_banner", "-framerate", "48",
                        "-i", str(four / "f%04d.png"), "-c:v", "libx264",
                        "-pix_fmt", "yuv420p", str(mp4)],
                       capture_output=True, text=True)
        dur = n2 / 48.0
        ok = "OK" if n2 >= 4 * n0 - 8 else "SHORT?"
        print(f"  {s}: {n0} -> {n1} -> {n2} frames  ({dur:.2f}s @48fps)  {ok}")
        results.append((s, n2))
        shutil.rmtree(two, ignore_errors=True)
        shutil.rmtree(stage, ignore_errors=True)
    good = sum(1 for _, n in results if n >= 150)
    print(f"\nRIFE DONE: {good}/{len(SHOTS)} cuts >=150 frames (>=3.1s @48fps). Output: {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
