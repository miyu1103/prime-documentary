#!/usr/bin/env python3
"""Generic SHORT audio mix + caption timing builder (English shorts, #11 onward).

Reads episodes/<ep>/06_audio/short<NN>_narration_index.v002.en_us.json and writes:
  - remotion/src/data/short<NN>_timing.ts  (SHORT<NN>_TOTAL_SEC / LINE_WINDOWS / SHORT<NN>_CAPTIONS)
  - 4-layer ducked mix at -14 LUFS -> H:/.../07_audio + copied to remotion/public/shorts/short<NN>/audio/
Bed/tension/ambience bases kept high so the inter-line gaps don't sag (same values as short08-10).

Usage: python scripts/build_short_mix.py --short 11 --ep PD-2026-011-mahanoy
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from gen_captions_forced import _smart_split  # noqa: E402 -- the long-form caption break rule
MEDIA = Path(json.loads((ROOT / "config/storage.local.json").read_text("utf-8"))["roots"]["media"]["path"])
LIB = MEDIA / "library"


def newest_take(directory: Path, stem_prefix: str) -> Path:
    """Resolve a music cue to its HIGHEST revision on disk.

    2026-08-25: every one of 21 Shorts failed its mix because this file named
    `..._soft_explainer_v1.mp3` and the library holds only `_v2`. ffmpeg exits -2 on a
    missing input, which surfaced as an opaque status 4294967294 with no filename in it.
    Naming a revision by hand is the bug; resolving it is the fix.
    """
    takes = sorted(p for p in directory.glob(f"{stem_prefix}*.mp3") if "UNUSED" not in p.name)
    if not takes:
        raise SystemExit(f"no take found for {directory}/{stem_prefix}* -- library changed?")
    return takes[-1]
REM_DATA = ROOT / "remotion" / "src" / "data"
TAIL = 1.0
MIN_CAP = 0.7


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True, capture_output=True)


def dur(path: Path) -> float:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                       capture_output=True, text=True)
    return float(r.stdout.strip() or 0)


def measure_lufs(path: Path) -> float:
    """Return the integrated loudness (LUFS) of an audio file via ffmpeg's ebur128 summary."""
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path),
                        "-af", "ebur128=framelog=verbose", "-f", "null", "-"],
                       capture_output=True, text=True)
    integrated = None
    for line in r.stderr.splitlines():
        s = line.strip()
        if s.startswith("I:") and "LUFS" in s:
            try:
                integrated = float(s.split("I:")[1].replace("LUFS", "").strip())
            except (ValueError, IndexError):
                pass
    if integrated is None:
        raise RuntimeError(f"could not measure loudness of {path}")
    return integrated


def loudnorm_stats(path: Path) -> dict:
    r = subprocess.run([
        "ffmpeg", "-hide_banner", "-nostats", "-i", str(path),
        "-af", "loudnorm=I=-14:TP=-1.5:LRA=6:print_format=json", "-f", "null", "-",
    ], capture_output=True, text=True, check=True)
    matches = re.findall(r"\{[\s\S]*?\}", r.stderr)
    if not matches:
        raise RuntimeError(f"could not parse loudnorm analysis for {path}")
    return json.loads(matches[-1])


def split_caption_segments(text: str) -> list[str]:
    # 1) split at sentence AND soft boundaries: . ! ? ; : , 。、 and spaced em/en dashes " — "
    raw = re.split(r"(?<=[.!?;:,。、])\s+|\s+[—–]\s+", text)
    segs = [s.strip(" ,、—–") for s in raw if s and s.strip(" ,、—–")]
    # 2) enforce a breath-unit max length (~7 words) so mobile captions stay 1–2 lines,
    #    splitting any long run at word boundaries
    MAX_WORDS, MAX_CHARS = 7, 42
    broken: list[str] = []
    for s in segs:
        words = s.split()
        if len(words) <= MAX_WORDS:
            broken.append(s)
        else:
            # Break where the GRAMMAR allows, not where the word count runs out. Equal-size
            # parts were an improvement on chunk-from-the-left and still cut mid-phrase: read
            # off the finished frames of shorts 259-270 on 2026-08-22, cues ended on "tried to
            # get", "would stop unless", "could also refer callers to", "contract principles
            # not", "It did not itself decide whether". A cue that ends on a preposition or a
            # conjunction reads as a mistake on a phone.
            #
            # gen_captions_forced._smart_split is the long-form rule for exactly this: never end
            # a line on a dangling function word, prefer a break after punctuation or before a
            # phrase-starting word. It is imported rather than copied (rule 18); its caps are
            # parameters so Shorts can keep a 7-word mobile cue while long-form keeps 10.
            toks = [(w, i) for i, w in enumerate(words)]
            for part in _smart_split(toks, max_words=MAX_WORDS, max_chars=MAX_CHARS):
                broken.append(" ".join(t for t, _ in part))
    # 3) fold tiny fragments (≤2 words) into the previous cue so nothing flashes alone
    merged: list[str] = []
    for s in broken:
        # Fold only when the RESULT stays inside the breath-unit cap. Without this guard the
        # fold cascades: a 7-word cue swallows every following short fragment and the caption
        # becomes a 13-word wall sitting on screen for ~6 s (short67 L2, measured 2026-08-01).
        if merged and len(s.split()) <= 2 and len(merged[-1].split()) + len(s.split()) <= MAX_WORDS:
            merged[-1] = merged[-1] + " " + s
        else:
            merged.append(s)
    return merged or [text]


def build_captions(lines: list[dict]) -> list[dict]:
    caps: list[dict] = []
    for ln in lines:
        segs = split_caption_segments(ln["text"])
        span = max(0.1, ln["end"] - ln["start"])
        weights = [max(1, len(s)) for s in segs]
        wsum = sum(weights)
        cursor = ln["start"]
        for s, w in zip(segs, weights):
            d = max(MIN_CAP, span * w / wsum)
            caps.append({"word": s.rstrip("、"), "startSec": round(cursor, 3), "endSec": round(cursor + d, 3)})
            cursor += d
        if caps:
            caps[-1]["endSec"] = round(ln["end"], 3)
    for i in range(1, len(caps)):
        if caps[i]["startSec"] < caps[i - 1]["endSec"]:
            caps[i]["startSec"] = caps[i - 1]["endSec"]
        if caps[i]["endSec"] <= caps[i]["startSec"]:
            caps[i]["endSec"] = round(caps[i]["startSec"] + MIN_CAP, 3)
    return caps


def write_timing(short: str, lines: list[dict], caps: list[dict], total: float) -> None:
    up = f"SHORT{short}"
    windows = [{"id": ln["id"], "start": round(ln["start"], 3), "end": round(ln["end"], 3)} for ln in lines]
    out = REM_DATA / f"short{short}_timing.ts"
    text = f"// AUTO-GENERATED by scripts/build_short_mix.py — narration-driven timing for SHORT #{short}.\n"
    text += "import type {ShortCaption} from '../compositions/Short';\n\n"
    text += "export type LineWindow = {id: string; start: number; end: number};\n\n"
    text += f"export const {up}_TOTAL_SEC = {round(total, 3)};\n\n"
    text += f"export const LINE_WINDOWS: LineWindow[] = " + json.dumps(windows, ensure_ascii=False, indent=2) + ";\n\n"
    text += f"export const {up}_CAPTIONS: ShortCaption[] = " + json.dumps(caps, ensure_ascii=False, indent=2) + ";\n"
    out.write_text(text, "utf-8")
    print(f"timing -> {out.relative_to(ROOT)}  (lines={len(windows)} captions={len(caps)})")


def build_mix(short: str, ep: str, narration: Path, total: float, lines: list[dict], voice_tempo: float = 1.0) -> Path:
    out_audio = MEDIA / "episodes" / ep / "07_audio"
    rem_public = ROOT / "remotion" / "public" / "shorts" / f"short{short}" / "audio"
    out_audio.mkdir(parents=True, exist_ok=True)
    bed = newest_take(LIB / "music" / "explainer_bed", "mus_20260614_explainer_bed_soft_explainer")
    tension = newest_take(LIB / "music" / "tension_build", "mus_20260614_tension_build_courtroom_horizon")
    amb = LIB / "ambience" / "amb_night_window.mp3"
    climax = next((ln["start"] for ln in lines if ln["id"] == "L4"), total - 12)
    cta = next((ln["start"] for ln in lines if ln["id"] == "L5"), total - 4)
    l2 = lines[1]["start"] if len(lines) > 1 else 6.0
    sfx = [
        (LIB / "sfx" / "sfx_riser_2s.mp3", 0.2, 0.34),
        (LIB / "sfx" / "sfx_page_turn.mp3", l2 + 0.2, 0.24),
        (LIB / "sfx" / "sfx_sub_drop.mp3", climax + 0.0, 0.30),
        (LIB / "sfx" / "sfx_low_boom.mp3", climax + 0.1, 0.22),
        (LIB / "sfx" / "sfx_stamp_seal.mp3", climax + 4.5, 0.40),
        (LIB / "sfx" / "sfx_whoosh_short.mp3", cta + 0.1, 0.26),
    ]
    inputs = ["-i", str(narration),
              "-stream_loop", "-1", "-i", str(bed),
              "-stream_loop", "-1", "-i", str(tension),
              "-stream_loop", "-1", "-i", str(amb)]
    for path, _, _ in sfx:
        inputs += ["-i", str(path)]
    # Volume consistency (owner feedback 2026-06-28: "中盤で音量が下がる"):
    # 1) speechnorm levels the narration line-to-line at the source so quieter "building"
    #    lines in the middle sit at the same level as the intense ones (split to also key ducking).
    # 2) a gentle full-mix glue compressor lifts quiet passages.
    # 3) loudnorm with a tighter LRA (=6) plus a final limiter keep the loudness constant over time.
    filters = [
        f"[0:a]atempo={voice_tempo:.6f},speechnorm=p=0.95:e=6.25:r=0.0008:l=1,"
        "asplit=4[vmix][vk1][vk2][vk3]",
        # Owner 2026-08-02: "音量が地中で下がる。何の意味もなく。" Measured on short82 and
        # short41: there is NO mid-video sag (thirds are -15.0 / -14.9 / -14.6 dBFS). What is
        # audible is a ~10 dB HOLE every 8-10 s, landing exactly on the inter-line gaps, because
        # the beds were ducked 7:1 and then took 450-600 ms to come back - so the 0.5 s gap was
        # nearly silent. Shallower ratios and much faster release keep the floor up between lines.
        f"[1:a]volume=0.30,atrim=0:{total},asetpts=PTS-STARTPTS[bed0]",
        f"[2:a]volume=0.14,atrim=0:{total},asetpts=PTS-STARTPTS[ten0]",
        f"[3:a]volume=0.07,atrim=0:{total},asetpts=PTS-STARTPTS[amb0]",
        "[bed0][vk1]sidechaincompress=threshold=0.03:ratio=3.5:attack=25:release=180[bedd]",
        "[ten0][vk2]sidechaincompress=threshold=0.03:ratio=3:attack=25:release=200[tend]",
        "[amb0][vk3]sidechaincompress=threshold=0.02:ratio=4:attack=30:release=240[ambd]",
    ]
    labels = ["[vmix]", "[bedd]", "[tend]", "[ambd]"]
    for idx, (_, delay, vol) in enumerate(sfx, start=4):
        ms = int(delay * 1000)
        filters.append(f"[{idx}:a]volume={vol},adelay={ms}|{ms}[sfx{idx}]")
        labels.append(f"[sfx{idx}]")
    filters.append(
        "".join(labels)
        + f"amix=inputs={len(labels)}:duration=longest:normalize=0,"
        + "acompressor=threshold=-20dB:ratio=3:attack=15:release=250:makeup=3[mix]"
    )
    # Pass 1: render the pre-master (no final normalization — keeps dynamics steady, no loudnorm pumping).
    premaster = out_audio / f"short{short}_premaster.wav"
    run(["ffmpeg", "-y", *inputs, "-filter_complex", ";".join(filters),
         "-map", "[mix]", "-t", str(total), "-c:a", "pcm_s16le", str(premaster)])
    # Pass 2: two-pass linear loudnorm. Supplying the measured values makes this a static
    # transform (no mid-short pumping) while the true-peak constraint remains codec-safe.
    stats = loudnorm_stats(premaster)
    measured = float(stats["input_i"])
    loudnorm = (
        "loudnorm=I=-14:TP=-1.5:LRA=6:linear=true"
        f":measured_I={stats['input_i']}:measured_TP={stats['input_tp']}"
        f":measured_LRA={stats['input_lra']}:measured_thresh={stats['input_thresh']}"
        f":offset={stats['target_offset']}:print_format=summary"
    )
    out = out_audio / f"short{short}_final_mix_v002_en_us.mp3"
    run(["ffmpeg", "-y", "-i", str(premaster),
         "-af", loudnorm,
         "-t", str(total), "-c:a", "libmp3lame", "-b:a", "192k", str(out)])
    premaster.unlink(missing_ok=True)
    print(f"loudness: premaster={measured:.2f} LUFS -> two-pass linear -14 LUFS / -1.5 dBTP")
    rem_public.mkdir(parents=True, exist_ok=True)
    (rem_public / out.name).write_bytes(out.read_bytes())
    return out


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--short", required=True, help="zero-padded number, e.g. 11")
    ap.add_argument("--ep", required=True, help="episode slug, e.g. PD-2026-011-mahanoy")
    ap.add_argument("--tail", type=float, default=TAIL,
                    help=f"trailing pad seconds after the last spoken line (default {TAIL}). "
                         "Lower it (e.g. 0.4) to land a short under the 40s method target.")
    ap.add_argument("--max-total", type=float, default=0.0,
                    help="pitch-preserving tempo fit to this total duration; 0 disables fitting")
    args = ap.parse_args()
    index = ROOT / "episodes" / args.ep / "06_audio" / f"short{args.short}_narration_index.v002.en_us.json"
    idx = json.loads(index.read_text("utf-8"))
    source_lines = idx["lines"]
    narration = Path(idx["master"])
    source_voice_end = max(ln["end"] for ln in source_lines)
    voice_tempo = 1.0
    if args.max_total:
        available = args.max_total - args.tail
        if available <= 0:
            raise SystemExit("--max-total must be greater than --tail")
        voice_tempo = max(1.0, source_voice_end / available)
        if voice_tempo > 1.15:
            raise SystemExit(f"required voice tempo {voice_tempo:.3f} exceeds the review limit 1.15")
    lines = [{**ln, "start": ln["start"] / voice_tempo, "end": ln["end"] / voice_tempo}
             for ln in source_lines]
    voice_end = max(ln["end"] for ln in lines)
    total = round(voice_end + args.tail, 3)
    caps = build_captions(lines)
    write_timing(args.short, lines, caps, total)
    mix = build_mix(args.short, args.ep, narration, total, lines, voice_tempo)
    print(f"voice_tempo={voice_tempo:.3f} voice_end={voice_end:.2f}s total={total:.2f}s")
    print(f"mix -> {mix}  ({dur(mix):.2f}s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
