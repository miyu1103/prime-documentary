"""Convert EP38 captions SRT -> styled ASS with: low position, Oswald, kinetic entrance
(fade + subtle scale-settle), and captions SUPPRESSED during the full-screen motion-graphic
card shots (so they never collide with the card's own text)."""
from __future__ import annotations
import json, re
from pathlib import Path

ROOT = Path(r"C:\Users\aab15\Documents\prime-documentary")
EP = "PD-2026-038-kidsforcash"
SC = ROOT / "episodes" / EP / "04_scenes"
SRT = SC / "captions.final.v001.srt"
SHOTLIST = SC / "shotlist.v001.json"
OUT = SC / "captions.final.v001.ass"
CARD_SHOTS = {12, 30, 32, 35, 57, 64, 71}   # full-screen motion-graphic cards


def ts_to_s(ts: str) -> float:
    h, m, rest = ts.split(":")
    s, ms = rest.split(",")
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000.0


def s_to_ass(t: float) -> str:
    cs = int(round(t * 100)); h = cs // 360000; cs %= 360000
    m = cs // 6000; cs %= 6000; s = cs // 100; cs %= 100
    return f"{h:d}:{m:02d}:{s:02d}.{cs:02d}"


def card_windows() -> list[tuple[float, float]]:
    data = json.loads(SHOTLIST.read_text(encoding="utf-8"))
    shots = data.get("shots") or data
    w = []
    for i in CARD_SHOTS:
        sh = shots[i]
        w.append((float(sh["start_sec"]), float(sh["end_sec"])))
    w.append((23.4, 27.4))   # OP title overlay window (keep captions clear of the brand sting)
    return w


def overlaps(a0, a1, windows) -> bool:
    for w0, w1 in windows:
        if a0 < w1 and a1 > w0:   # any overlap
            return True
    return False


def parse_srt(text: str):
    blocks = re.split(r"\n\s*\n", text.strip())
    for b in blocks:
        lines = [l for l in b.splitlines() if l.strip()]
        if len(lines) < 2:
            continue
        ti = next((i for i, l in enumerate(lines) if "-->" in l), None)
        if ti is None:
            continue
        a, _, c = lines[ti].partition("-->")
        start = ts_to_s(a.strip()); end = ts_to_s(c.strip())
        txt = " ".join(lines[ti + 1:]).strip()
        yield start, end, txt


HEADER = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Oswald,52,&H00FAF7F5,&H00FAF7F5,&H00161616,&H96000000,0,0,0,0,100,100,0,0,1,3,2,2,220,220,64,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

# low MarginV=64 (near bottom), Alignment 2 (bottom-center). Kinetic entrance:
# fade 150/90 ms + subtle scale-settle 106->100 over 180ms.
ANIM = r"{\fad(150,90)\fscx106\fscy106\t(0,180,\fscx100\fscy100)}"


def main() -> int:
    windows = card_windows()
    events = []
    dropped = 0
    for start, end, txt in parse_srt(SRT.read_text(encoding="utf-8")):
        if overlaps(start, end, windows):
            dropped += 1
            continue
        txt = txt.replace("\n", r"\N")
        events.append(f"Dialogue: 0,{s_to_ass(start)},{s_to_ass(end)},Cap,,0,0,0,,{ANIM}{txt}")
    OUT.write_text(HEADER + "\n".join(events) + "\n", encoding="utf-8")
    print(f"wrote {OUT}")
    print(f"events={len(events)} dropped_over_cards={dropped} card_windows={len(windows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
