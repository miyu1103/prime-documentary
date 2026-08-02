#!/usr/bin/env python3
"""Assemble one Short from its finished design: stage the footage, emit the Remotion data file.

This is the step that runs once a Short's images arrive. Everything it needs already exists:
the design (angle, five lines, 23 plates), the -14 LUFS mix and the caption timing, the bound
archive clips, and the generated plates dropped into remotion/public/shorts/short<NN>/.

What it does:
  1. verifies every GENERATE plate has a delivered image (refuses to assemble a Short with holes)
  2. copies each bound archive clip into fx/, centre-cropped to a native 1080x1920 at 30 fps,
     and records provenance (ledger title, licence, source) in fx/RIGHTS.json
  3. writes remotion/src/data/short<NN>.ts, laying the 23 plates across the five line windows

Beat length is taken from the mix's own LINE_WINDOWS, so the cut always matches the voice; the
CTA beat is weighted heavier because the funnel card needs about 4 s to be read, and the loop
tail is dropped so the card holds to the final frame.

Usage: py -3.11 scripts/assemble_short.py --short 86 [--force]
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import urllib.request
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGNS = ROOT / "episodes" / "_planning" / "short_designs"
PUB = ROOT / "remotion" / "public" / "shorts"
DATA = ROOT / "remotion" / "src" / "data"


def short_title(t: str, cap: int = 38) -> str:
    """Trim to whole words. A title cut mid-word ("...pure waste and do") reads as a defect."""
    if len(t) <= cap:
        return t
    out = []
    for w in t.split():
        if len(" ".join(out + [w])) > cap:
            break
        out.append(w)
    return " ".join(out) or t[:cap]


def find_design(sid: str):
    for f in sorted(DESIGNS.glob("*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        for s in d["shorts"]:
            if s.get("short_id") == sid:
                return d, s
    return None, None


def stage_footage(sid: str, plates: list[dict], force: bool) -> list[dict]:
    fx = PUB / sid / "fx"
    fx.mkdir(parents=True, exist_ok=True)
    rights = []
    for p in plates:
        if p.get("source") != "FOOTAGE" or not p.get("bound_file"):
            continue
        src = Path(p["bound_file"])
        out = fx / f"fx_{p['n']:02d}.mp4"
        if out.exists() and not force:
            rights.append({"file": out.name, "plate": p["n"], "ledger_title": p.get("bound_title"),
                           "license": p.get("bound_license"), "source": p.get("bound_source"),
                           "src_path": str(src)})
            continue
        if not src.exists():
            print(f"  plate {p['n']}: bound clip missing on disk -> {src}")
            continue
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(src),
                        "-vf", "crop=ih*9/16:ih,scale=1080:1920:flags=lanczos,fps=30",
                        "-an", "-c:v", "libx264", "-crf", "18", "-preset", "medium",
                        "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out)], check=True)
        rights.append({"file": out.name, "plate": p["n"], "ledger_title": p.get("bound_title"),
                       "license": p.get("bound_license"), "source": p.get("bound_source"),
                       "src_path": str(src)})
    (fx / "RIGHTS.json").write_text(json.dumps(rights, ensure_ascii=False, indent=2), encoding="utf-8")
    return rights


def emit_ts(sid: str, ep: str, design: dict, short: dict) -> Path:
    nn = sid.replace("short", "")
    up = f"SHORT{nn}"
    cuts = []
    # The closing line used to be one short beat, so a single reused hook image covered it. It is
    # now the eighth line of eight and runs about seven seconds; one still image over seven seconds
    # is the "kamishibai" the owner keeps rejecting, and it walks straight into the 2 s stillness
    # ceiling. Replay the hook's own images in order instead: it fills the time with real cuts and
    # it is what a loop should look like — the ending hands you back the opening.
    hook_imgs = [q["n"] for q in short["plates"]
                 if q.get("role") == "hook" and q.get("source") == "GENERATE"] or [1]
    loop_plates = [q["n"] for q in short["plates"] if q.get("role") == "loop"]

    for p in short["plates"]:
        n, line = p["n"], p.get("line", "L1")
        role = p.get("role")
        if p.get("source") == "FOOTAGE" and p.get("bound_file"):
            src = f"shorts/{sid}/fx/fx_{n:02d}.mp4"
            kind, motion = "video", "video"
        elif p.get("source") == "GENERATE":
            src = f"shorts/{sid}/{sid}_{n:02d}.png"
            kind = "image"
            motion = ("pushin", "parallax", "kenburns")[n % 3]
        elif role == "loop":
            # Replay the hook, in order. The last loop plate mirrors hook plate 1 exactly and then
            # rewinds - same picture, same motion type, same focal travel - so the final frame lands
            # where the first frame starts and the loop is seamless.
            # The loop plates are the ONLY cuts the designs put on the closing line, so dropping
            # them left that whole line with no beat at all: the render went black for the last
            # eight seconds (measured on short86 v1) and the funnel card landed mid-story.
            pos = loop_plates.index(n)
            last = pos == len(loop_plates) - 1
            # walk backwards through the hook so the final beat is hook plate 1
            hook_n = hook_imgs[0] if last else hook_imgs[min(len(loop_plates) - 1 - pos,
                                                            len(hook_imgs) - 1)]
            src = f"shorts/{sid}/{sid}_{hook_n:02d}.png"
            kind = "image"
            motion = ("pushin", "parallax", "kenburns")[hook_n % 3]   # that hook plate's motion
        else:
            continue
        # only the final loop plate carries the funnel card and the rewind
        is_cta = role == "loop" and n == loop_plates[-1]
        cut = (f"  {{line: '{line}', id: 'p{n:02d}', src: '{src}', kind: '{kind}', "
               f"motion: '{motion}'"
               + (", fast: true" if role == "hook" and n <= 3 else "")
               + (", isCta: true, rewind: true, fast: true" if is_cta else "")
               + f"}},   // {p.get('subject','')[:58]}")
        cuts.append(cut)

    ts = f'''import type {{ShortBeat, ShortData}} from '../compositions/Short';
import {{LINE_WINDOWS, {up}_CAPTIONS, {up}_TOTAL_SEC}} from './{sid}_timing';

/**
 * {sid} — {short["angle"]}
 * Episode {ep}.  Type {short.get("type", "?")}.
 *
 * AVOIDS: {short.get("avoids", "")}
 * LEAVES FOR THE LONG-FORM: {short.get("funnel_question_left_for_longform", "")}
 *
 * GENERATED BY scripts/assemble_short.py from the design at
 * episodes/_planning/short_designs/{ep}.design.v001.json — edit the design, not this file.
 *
 * The funnel card is the last thing on screen and holds to the final frame: Shorts loops on its
 * own, and conversion is the measured bottleneck (0.77 subs/1000 views on Shorts against 3.67 on
 * long-form), so the destination is worth more than a seamless loop seam.
 */

type Cut = {{line: string; id: string; src: string; kind: 'image' | 'video';
  motion: ShortBeat['motion']; fast?: boolean; isCta?: boolean; rewind?: boolean}};

const r3 = (n: number) => Math.round(n * 1000) / 1000;

const CUTS: Cut[] = [
{chr(10).join(cuts)}
];

const buildBeats = (): ShortBeat[] => {{
  const beats: ShortBeat[] = [];
  LINE_WINDOWS.forEach((win, i) => {{
    const start = win.start;
    const end = i + 1 < LINE_WINDOWS.length ? LINE_WINDOWS[i + 1].start : {up}_TOTAL_SEC;
    const cuts = CUTS.filter((c) => c.line === win.id);
    // The card needs ~2.5 s to be read, but METHOD rule 6 caps any held frame at 2 s and a
    // weight-based share breaks that whenever a line carries few cuts: at weight 1.9 the card
    // ran 3.20 s on short94 and 2.63 s on short90, while short93 sat at 0.83 s. Give it a fixed
    // 1.9 s and let the other cuts of that line share what is left, so the ceiling holds
    // whatever the cut count is.
    // Capping the card at a fixed 1.9 s left 7.8 s of L5 with NO beat at all on short87 - the
    // screen went black under the captions. A line window must always be covered end to end.
    // So: the card takes at most 1.9 s of MOTION, then holds the same beat to the end of the
    // line rather than handing the remainder to nobody. Every second of every window is owned.
    const span = end - start;
    const nCta = cuts.filter((c) => c.isCta).length;
    const others = cuts.length - nCta;
    // when the card is the only cut in its line it simply takes the whole window
    const ctaDur = others === 0 ? span : Math.min(1.9, span / cuts.length * 2);
    const rest = others > 0 ? (span - ctaDur * nCta) / others : 0;
    let cursor = start;
    cuts.forEach((c) => {{
      const dur = c.isCta ? ctaDur : rest;
      const {{line: _l, isCta, ...keep}} = c;
      beats.push({{...keep, id: isCta ? 'cta' : c.id, startSec: r3(cursor), durSec: r3(dur)}});
      cursor += dur;
    }});
  }});
  return beats;
}};

export const {up}: ShortData = {{
  shortId: '{sid}',
  episodeId: '{ep}',
  durationSec: {up}_TOTAL_SEC,
  narrationSrc: 'shorts/{sid}/audio/{sid}_final_mix_v002_en_us.mp3',
  captions: {up}_CAPTIONS,
  bgmSrc: null,
  ctaTextYT: 'Watch the full case on the channel',
  ctaTextTT: 'Full case on our profile',
  ctaLongThumbSrc: 'shorts/{sid}/{sid}_ctathumb.jpg',
  ctaLongTitle: {json.dumps(short_title(design["destination"]["title"]))},
  ctaHeadline: 'FULL CASE',
  captionTop: 1210,
  ctaFadeOutSec: 0.8,
  beats: buildBeats(),
}};
'''
    # Refuse to emit a cut with a hole in it. Twice now a line window has ended up partly or
    # wholly uncovered and the render went black under the captions; both times it was caught by
    # eye on a finished file, which is far too late.
    tim = (DATA / f"{sid}_timing.ts").read_text(encoding="utf-8")
    total = float(re.search(r"_TOTAL_SEC = ([\d.]+)", tim).group(1))
    i = tim.index("LINE_WINDOWS"); j = tim.index("[", tim.index("=", i)); depth = 0
    for k in range(j, len(tim)):
        depth += (tim[k] == "[") - (tim[k] == "]")
        if depth == 0:
            wins = json.loads(tim[j:k + 1]); break
    for wi, w in enumerate(wins):
        a0 = w["start"]; a1 = wins[wi + 1]["start"] if wi + 1 < len(wins) else total
        mine = [c for c in cuts if f"line: '{w['id']}'" in c]
        if not mine:
            sys.exit(f"{sid}: line {w['id']} ({a0:.2f}-{a1:.2f}s) has no cut - that window "
                     f"would render black")
        n_cta = sum(1 for c in mine if "isCta: true" in c)
        span = a1 - a0
        cta = span if len(mine) - n_cta == 0 else min(1.9, span / len(mine) * 2)
        rest = (span - cta * n_cta) / max(1, len(mine) - n_cta) if len(mine) - n_cta else 0.0
        covered = cta * n_cta + rest * (len(mine) - n_cta)
        if abs(covered - span) > 0.02:
            sys.exit(f"{sid}: line {w['id']} covers {covered:.2f}s of a {span:.2f}s window")

    out = DATA / f"{sid}.ts"
    out.write_text(ts, encoding="utf-8")
    return out


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--short", required=True)
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    sid = f"short{args.short}"

    design, short = find_design(sid)
    if not short:
        sys.exit(f"no design for {sid}")

    want = {p["n"] for p in short["plates"] if p.get("source") == "GENERATE"}
    have = {int(m.group(1)) for f in (PUB / sid).glob(f"{sid}_[0-9]*.png")
            if (m := re.search(r"_(\d+)\.png$", f.name)) and "_depth" not in f.name}
    if want - have:
        sys.exit(f"{sid}: images missing for plates {sorted(want-have)} — refusing to assemble "
                 f"a cut with holes in it")

    by_line: dict[str, int] = {}
    for p in short["plates"]:
        by_line[p.get("line", "?")] = by_line.get(p.get("line", "?"), 0) + 1
    empty = [l for l in ("L1", "L2", "L3", "L4", "L5") if by_line.get(l, 0) == 0]
    if empty:
        sys.exit(f"{sid}: no plates on {empty} — those seconds would render black")

    # the funnel card needs the destination's own thumbnail; without it the card renders an
    # empty box, which is worse than no card - it reads as a broken element
    thumb = PUB / sid / f"{sid}_ctathumb.jpg"
    if not thumb.exists():
        vid = design["destination"]["video_id"]
        for q in ("maxresdefault", "hqdefault"):
            try:
                urllib.request.urlretrieve(f"https://i.ytimg.com/vi/{vid}/{q}.jpg", thumb)
                if thumb.stat().st_size > 3000:
                    break
            except Exception:
                pass
        print(f"  fetched destination thumbnail -> {thumb.name}")

    rights = stage_footage(sid, short["plates"], args.force)
    print(f"{sid}: {len(have)} generated plates, {len(rights)} archive clips staged")
    out = emit_ts(sid, design["episode_id"], design, short)
    print(f"  wrote {out.relative_to(ROOT)}")
    print(f"  rights recorded in {(PUB/sid/'fx'/'RIGHTS.json').relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
