"""Hold caption ends forward to close chunk-tail coverage gaps (verify_caption_coverage fix).

The forced-alignment caption pipeline applies a uniform -CAPTION_LEAD_SECONDS shift so captions
lead the audio (owner-approved sync). That shift pulls every cue END earlier too, so the natural
sentence-end pause inside each narration chunk is left uncaptioned -> verify_caption_coverage FAILs
(chunks < 80% covered). This post-process extends each cue's END toward the next cue's start
(bounded) WITHOUT moving any start, so:
  - forced-alignment sync / "captions lead the audio" is preserved byte-for-byte (starts unchanged),
  - chunk-tail pauses stay captioned (coverage restored),
  - characters-per-second drops (more on-screen time to read).

Idempotent-ish: re-running only ever extends ends up to the same bound. Atomic temp+rename write.

Mirrors gen_captions_forced.py CAPTION_HOLD_MAX / CAPTION_HOLD_GAP so a fresh regen and this
post-process converge to the same timing.
"""
from __future__ import annotations
import argparse
import re
from pathlib import Path

CAPTION_HOLD_MAX = 2.5   # never linger more than this past the spoken end
CAPTION_HOLD_GAP = 0.06  # small visible gap kept before the next caption appears
CAPTION_LEAD_SECONDS = 0.60

TS = re.compile(r"(\d\d):(\d\d):(\d\d),(\d\d\d)\s*-->\s*(\d\d):(\d\d):(\d\d),(\d\d\d)")


def parse_ts(h, m, s, ms) -> float:
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000.0


def fmt_ts(t: float) -> str:
    if t < 0:
        t = 0.0
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def load_srt(path: Path):
    blocks = re.split(r"\n\s*\n", path.read_text("utf-8").strip())
    cues = []
    for b in blocks:
        lines = [ln for ln in b.splitlines() if ln.strip() != ""]
        if len(lines) < 2:
            continue
        # find the timestamp line (usually line 2, after the index)
        ti = next((i for i, ln in enumerate(lines) if TS.search(ln)), None)
        if ti is None:
            continue
        mt = TS.search(lines[ti])
        s = parse_ts(*mt.group(1, 2, 3, 4))
        e = parse_ts(*mt.group(5, 6, 7, 8))
        text = lines[ti + 1:]
        cues.append([s, e, text])
    return cues


def hold_ends(cues):
    n = len(cues)
    extended = 0
    for i in range(n - 1):
        nxt_start = cues[i + 1][0]
        hold_cap = min(nxt_start - CAPTION_HOLD_GAP, cues[i][1] + CAPTION_HOLD_MAX)
        if hold_cap > cues[i][1]:
            cues[i][1] = hold_cap
            extended += 1
    if n:
        cues[-1][1] = cues[-1][1] + min(CAPTION_HOLD_MAX, CAPTION_LEAD_SECONDS)
        extended += 1
    return extended


def write_srt(path: Path, cues):
    body = "\n".join(
        f"{i+1}\n{fmt_ts(s)} --> {fmt_ts(e)}\n" + "\n".join(text) + "\n"
        for i, (s, e, text) in enumerate(cues)
    )
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(body, "utf-8")
    tmp.replace(path)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", dest="out", required=True)
    args = ap.parse_args()
    src, dst = Path(args.inp), Path(args.out)
    cues = load_srt(src)
    # sanity: starts must remain non-decreasing and unchanged from source
    starts_before = [round(c[0], 3) for c in cues]
    ext = hold_ends(cues)
    starts_after = [round(c[0], 3) for c in cues]
    assert starts_before == starts_after, "starts changed -- would break sync"
    # no cue may end after the next begins
    for i in range(len(cues) - 1):
        assert cues[i][1] <= cues[i + 1][0] + 1e-6, f"cue {i} overlaps next"
    write_srt(dst, cues)
    dur = [c[1] - c[0] for c in cues]
    print(f"cues={len(cues)}  ends_extended={ext}  "
          f"median_cue_dur={sorted(dur)[len(dur)//2]:.2f}s  min={min(dur):.2f}s  max={max(dur):.2f}s")


if __name__ == "__main__":
    main()
