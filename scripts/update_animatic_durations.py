"""
scripts/update_animatic_durations.py
スロー後ナレーション(VC-0001..VC-0023)の実尺を読み取り、
miranda_animatic.ts の durationSec を更新する。
"""
from __future__ import annotations
import pathlib, re, subprocess

FFPROBE  = r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffprobe.exe"
SLOW_DIR = pathlib.Path(r"H:\pd-media\episodes\PD-2026-001-miranda\06_voice\slow_v001")
TS_FILE  = pathlib.Path(__file__).resolve().parents[1] / "remotion/src/data/miranda_animatic.ts"

def probe(p: pathlib.Path) -> float:
    r = subprocess.run(
        [FFPROBE, "-v", "quiet", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(p)],
        capture_output=True, text=True,
    )
    return float(r.stdout.strip())

durations: list[int] = []
cumulative = 0.0
for i in range(1, 24):
    p = SLOW_DIR / f"VC-{i:04d}.mp3"
    d = probe(p)
    rounded = round(d)
    durations.append(rounded)
    cumulative += rounded
    print(f"VC-{i:04d}: {d:.2f}s -> {rounded}s  (cum={cumulative:.0f}s)")

print(f"\nTotal animatic: {cumulative:.0f}s")

# patch durationSec values in miranda_animatic.ts
text = TS_FILE.read_text(encoding="utf-8")

# each scene has: {sceneId: "S001", visualMode: "...", durationSec: 30, ...}
# replace durationSec values in order of appearance
pattern = r'(durationSec:\s*)(\d+)'
matches = list(re.finditer(pattern, text))
assert len(matches) == 23, f"Expected 23 durationSec fields, found {len(matches)}"

# rebuild string with new values (work backwards to keep offsets valid)
for match, new_dur in reversed(list(zip(matches, durations))):
    start, end = match.span(2)   # span of just the number
    text = text[:start] + str(new_dur) + text[end:]

TS_FILE.write_text(text, encoding="utf-8")
print(f"\nUpdated: {TS_FILE}")
