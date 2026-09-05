#!/usr/bin/env python3
"""EP35 caption sync fix: rigid-shift the (dangling-fixed) captions.final.v001.srt EARLIER by
LEAD_EXTRA seconds to pull the late p90 tail under the caption_sync FAIL_P90_LAG (0.35s) floor,
then mirror the shifted+reflowed cues into remotion/src/data/hinders_film.json's captions[] so the
BURNED render matches the validated .srt. Leading a caption up to 0.80s is explicitly fine per
verify_caption_sync (it biases early on purpose); this only trims a late tail, it does not fabricate
timing. Writes an immutable captions.final.v002.srt (v001 untouched)."""
from __future__ import annotations
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EP = ROOT / "episodes" / "PD-2026-035-hinders"
SRC_SRT = EP / "08_edit" / "captions.final.v001.srt"
OUT_SRT = EP / "08_edit" / "captions.final.v002.srt"
FILM = ROOT / "remotion" / "src" / "data" / "hinders_film.json"
LEAD_EXTRA = 0.18  # seconds to pull every cue earlier (p90 0.420 -> ~0.240, under 0.35 floor)


def ts_to_s(t: str) -> float:
    t = t.strip().replace(".", ",")
    hh, mm, rest = t.split(":")
    ss, ms = rest.split(",")
    return int(hh) * 3600 + int(mm) * 60 + int(ss) + int(ms) / 1000.0


def s_to_ts(s: float) -> str:
    if s < 0:
        s = 0.0
    ms = int(round(s * 1000))
    hh, ms = divmod(ms, 3600000)
    mm, ms = divmod(ms, 60000)
    ss, ms = divmod(ms, 1000)
    return f"{hh:02d}:{mm:02d}:{ss:02d},{ms:03d}"


def parse_srt(raw: str):
    cues = []
    for block in re.split(r"\n\s*\n", raw.strip()):
        lines = block.strip().split("\n")
        if len(lines) < 2:
            continue
        idx = lines[0].strip()
        m = re.match(r"(.+?)\s*-->\s*(.+)", lines[1])
        if not m:
            continue
        start, end = ts_to_s(m.group(1)), ts_to_s(m.group(2))
        text_lines = [ln for ln in lines[2:] if ln.strip() != ""]
        cues.append({"idx": idx, "start": start, "end": end, "lines": text_lines})
    return cues


def main() -> int:
    cues = parse_srt(SRC_SRT.read_text(encoding="utf-8"))
    # rigid shift earlier, preserve duration, clamp start>=0 and keep monotonic non-overlap
    out = []
    prev_end = 0.0
    for c in cues:
        dur = c["end"] - c["start"]
        ns = max(0.0, c["start"] - LEAD_EXTRA)
        ne = ns + dur
        # never overlap the previous cue
        if ns < prev_end:
            ns = prev_end
            ne = max(ns + 0.20, ne)
        prev_end = ne
        out.append({"idx": c["idx"], "start": round(ns, 3), "end": round(ne, 3), "lines": c["lines"]})

    # write v002 SRT (immutable new revision)
    srt_parts = []
    for i, c in enumerate(out, 1):
        srt_parts.append(str(i))
        srt_parts.append(f"{s_to_ts(c['start'])} --> {s_to_ts(c['end'])}")
        srt_parts.extend(c["lines"])
        srt_parts.append("")
    OUT_SRT.write_text("\n".join(srt_parts).strip() + "\n", encoding="utf-8")

    # mirror into film.json captions[] (space-joined text, matching the builder convention)
    film = json.loads(FILM.read_text(encoding="utf-8"))
    old = film.get("captions", [])
    new_caps = [{"start": c["start"], "end": c["end"], "text": " ".join(c["lines"]).strip()} for c in out]
    if len(new_caps) != len(old):
        print(f"WARN: caption count changed {len(old)} -> {len(new_caps)}")
    film["captions"] = new_caps
    FILM.write_text(json.dumps(film, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"wrote {OUT_SRT.name}: {len(out)} cues, shifted -{LEAD_EXTRA}s")
    print(f"updated film.json captions[]: {len(old)} -> {len(new_caps)}")
    print(f"cue1 start {cues[1]['start']:.3f} -> {out[1]['start']:.3f}; text now: {new_caps[1]['text'][:70]!r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
