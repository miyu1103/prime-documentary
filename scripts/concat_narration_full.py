"""Concatenate S001-S023 narration MP3s into one master file."""
import subprocess, pathlib, sys, tempfile

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

NARR = pathlib.Path(r"H:\pd-media\episodes\PD-2026-001-miranda\06_audio\narration")
OUT  = NARR / "vc_s001_s023_v001.mp3"

# Individual per-scene files (S001 and S002 map to hook/opening in older scheme)
# S001 = vc_hook_v001.mp3 or vc_s001_v001.mp3? Check what exists.
FFMPEG = r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe"

CANDIDATES = [
    "vc_hook_v001.mp3",      # S001 hook
    "vc_opening_v001.mp3",   # S002 opening
    "vc_s003_v001.mp3",
    "vc_s004_v001.mp3",
    "vc_s005_v001.mp3",
    "vc_s006_v001.mp3",
    "vc_s007_v001.mp3",
    "vc_s008_v001.mp3",
    "vc_s009_v001.mp3",
    "vc_s010_v001.mp3",
    "vc_s011_v001.mp3",
    "vc_s012_v001.mp3",
    "vc_s013_v001.mp3",
    "vc_s014_v001.mp3",
    "vc_s015_v001.mp3",
    "vc_s016_v001.mp3",
    "vc_s017_v001.mp3",
    "vc_s018_v001.mp3",
    "vc_s019_v001.mp3",
    "vc_s020_v001.mp3",
    "vc_s021_v001.mp3",
    "vc_s022_v001.mp3",
    "vc_s023_v001.mp3",
]

def main():
    files = []
    for name in CANDIDATES:
        p = NARR / name
        if p.exists():
            files.append(p)
            print(f"  + {name}")
        else:
            print(f"  - MISSING: {name}")

    if not files:
        print("ERROR: no files found"); return

    # Write concat list
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8") as f:
        for fp in files:
            f.write(f"file '{fp}'\n")
        list_path = f.name

    print(f"\nConcatenating {len(files)} files -> {OUT}")
    result = subprocess.run(
        [FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", list_path,
         "-c", "copy", str(OUT)],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print("FFMPEG ERROR:", result.stderr[-500:])
    else:
        kb = OUT.stat().st_size // 1024
        print(f"OK: {OUT.name}  ({kb} KB)")

if __name__ == "__main__":
    main()
