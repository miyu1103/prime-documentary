#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Grade the audio shelf by measurement, because a contact sheet cannot show sound.

8,635 freesound items sit in five themes with no verdict, and the visual QC that judged
every other theme x source pair is useless here: there is nothing to look at. Listening to
8,635 files is not a plan either.

So measure what actually makes a sound effect unusable, which is objective:

  near-silent      peak below -50 dBFS, or 90%+ of the file under -50 dB. A dud recording.
  clipped          peak at or above -0.1 dBFS with a high crest factor -- digital clipping
                   is audible the moment it is laid under narration.
  too short        under 0.4 s cannot be an ambience bed; it can still be a hit.
  mono bed         an ambience bed in mono has no width and cannot be laid under a stereo
                   mix without collapsing it. Fine for a spot effect.
  band-limited     spectral rolloff under 8 kHz means it was sourced from something already
                   compressed; it sounds muffled next to a 48 kHz ElevenLabs voice.
  low rate         under 44.1 kHz.

A theme's verdict comes from what fraction of its sample fails. The playlist is written
too, so the owner can spot-check the calls by ear.

    python scripts/qc_audio_stats.py                       # every unjudged audio pair
    python scripts/qc_audio_stats.py --theme ambience_beds --per-theme 120
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import random
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from shelf import shelf_rows  # noqa: E402

QC_DIR = r"E:\pd-media\assets\archive\_qc"
VERDICTS = os.path.join(QC_DIR, "archive_verdicts.jsonl")
AUDIO_EXT = {".mp3", ".wav", ".flac", ".ogg", ".m4a", ".aac", ".aif", ".aiff"}


def measure(path: str) -> dict | None:
    """One ffmpeg pass: peak, RMS, silence share, and spectral rolloff."""
    # -v error silences astats and silencedetect too: they log at info level. With it the
    # function returned only ffprobe fields and every peak was None, so near-silent and
    # clipped never fired and the tool reported "good" on evidence it had not collected.
    p = subprocess.run(
        ["ffmpeg", "-hide_banner", "-loglevel", "info", "-i", path,
         "-af", "astats=metadata=1:reset=0,aspectralstats=measure=rolloff,"
                "silencedetect=n=-50dB:d=0.3",
         "-f", "null", "-"],
        capture_output=True, text=True, errors="replace", timeout=120)
    err = p.stderr or ""
    out = {}
    m = re.search(r"Peak level dB:\s*(-?[\d.]+|-inf)", err)
    if m:
        out["peak_db"] = -99.0 if m.group(1) == "-inf" else float(m.group(1))
    m = re.search(r"RMS level dB:\s*(-?[\d.]+|-inf)", err)
    if m:
        out["rms_db"] = -99.0 if m.group(1) == "-inf" else float(m.group(1))
    m = re.search(r"Flat factor:\s*([\d.]+)", err)
    if m:
        out["flat"] = float(m.group(1))
    rolls = [float(x) for x in re.findall(r"Rolloff:\s*([\d.]+)", err)]
    if rolls:
        out["rolloff"] = sum(rolls) / len(rolls)
    out["silence_s"] = sum(float(x) for x in re.findall(r"silence_duration:\s*([\d.]+)", err))

    q = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries",
         "stream=sample_rate,channels:format=duration", "-of", "json", path],
        capture_output=True, text=True, errors="replace", timeout=60)
    try:
        j = json.loads(q.stdout)
        st = j["streams"][0]
        out["sr"] = int(st["sample_rate"])
        out["ch"] = int(st["channels"])
        out["dur"] = float(j["format"]["duration"])
    except Exception:
        return None
    return out


# Recordings of a proceeding, not effects. The Supreme Court distributes its own oral
# arguments as 22 kHz mono, so the sample-rate and mono floors below -- which exist to
# protect a stereo music bed -- graded Terry, Kelo and Carpenter "unusable" at 100%.
# They are primary source audio for the exact cases this channel covers. The floors do
# not apply to them; only genuine defects do.
SPEECH_SOURCES = {"oyez", "courtlistener"}


def faults(m: dict, theme: str, source: str = "") -> list[str]:
    f = []
    speech = source in SPEECH_SOURCES
    dur = m.get("dur", 0) or 0.001
    if m.get("peak_db", 0) <= -50:
        f.append("near-silent")
    elif m.get("silence_s", 0) / dur > 0.9:
        f.append("mostly-silence")
    # Peak alone does not mean clipped. An mp3 decodes to float and legitimately
    # overshoots full scale: the three court recordings flagged here measured +1.3,
    # +3.0 and +3.8 dBFS with a flat factor of exactly 0 -- not one run of repeated
    # samples, which is what actual clipping leaves behind. They need about 4dB of
    # headroom on the way to 16-bit, not rejection. `flat` is already collected by
    # measure() and was simply never consulted, so a file that overshoots is only a
    # fault when the flatness confirms the waveform was squared off.
    if m.get("peak_db", -99) >= -0.1 and (m.get("flat") or 0) > 0:
        f.append("clipped")
    if dur < 0.4:
        f.append("too-short")
    if m.get("sr", 48000) < 44100 and not speech:
        f.append("low-rate")
    if m.get("rolloff") and m["rolloff"] < 8000:
        f.append("band-limited")
    # A bed has to hold under a stereo mix; a spot effect does not.
    if (theme in ("ambience_beds", "bgm_general", "sfx_environment")
            and m.get("ch", 2) < 2 and not speech):
        f.append("mono-bed")
    return f


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--theme", help="one theme only")
    ap.add_argument("--per-theme", type=int, default=60,
                    help="files measured per theme x source (default 60)")
    ap.add_argument("--seed", type=int, default=11)
    args = ap.parse_args()

    judged = set()
    with open(VERDICTS, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            try:
                r = json.loads(line)
            except Exception:
                continue
            judged.add((r.get("theme"), r.get("source")))

    pairs = collections.defaultdict(list)
    for r in shelf_rows(include_factory=False):
        fp = r.get("file_path", "") or ""
        if os.path.splitext(fp)[1].lower() not in AUDIO_EXT:
            continue
        key = (r.get("theme"), r.get("source"))
        if key in judged or (args.theme and key[0] != args.theme):
            continue
        pairs[key].append(r)

    if not pairs:
        print("no unjudged audio pairs")
        return 0

    random.seed(args.seed)
    for key, rows in sorted(pairs.items(), key=lambda kv: -len(kv[1])):
        theme, source = key
        sample = random.sample(rows, min(args.per_theme, len(rows)))
        tally = collections.Counter()
        ok = bad = unreadable = 0
        durs = []
        examples = collections.defaultdict(list)
        for r in sample:
            fp = r["file_path"]
            if not os.path.exists(fp):
                continue
            m = measure(fp)
            if m is None:
                unreadable += 1
                continue
            durs.append(m.get("dur", 0))
            fl = faults(m, theme, source)
            if fl:
                bad += 1
                for x in fl:
                    tally[x] += 1
                    if len(examples[x]) < 2:
                        examples[x].append(f"{(r.get('title') or '')[:44]} "
                                           f"[{m.get('dur',0):.1f}s {m.get('sr')}Hz "
                                           f"{m.get('ch')}ch peak{m.get('peak_db')}]")
            else:
                ok += 1
        n = ok + bad
        rate = bad / max(n, 1)
        verdict = "good" if rate < 0.2 else "mixed" if rate < 0.5 else "unusable"
        med = sorted(durs)[len(durs) // 2] if durs else 0
        print(f"\n{theme} / {source}  ({len(rows):,} items, {n} measured, "
              f"{unreadable} unreadable)")
        print(f"  faults {bad}/{n} = {rate*100:.0f}%   median {med:.1f}s   -> {verdict}")
        for k, c in tally.most_common():
            print(f"    {k:16} {c:4}")
            for e in examples[k]:
                print(f"        {e}")

        # playlist so the calls can be checked by ear
        out = os.path.join(QC_DIR, theme)
        os.makedirs(out, exist_ok=True)
        m3u = os.path.join(out, f"listen_{source}.m3u8")
        with open(m3u, "w", encoding="utf-8") as fh:
            fh.write("#EXTM3U\n")
            for r in sample:
                fh.write(f"#EXTINF:-1,{r.get('title')}\n{r['file_path']}\n")
        print(f"  playlist: {m3u}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
