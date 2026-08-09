#!/usr/bin/env python3
"""Assemble one Short from its finished design: stage the footage, emit the Remotion data file.

This is the step that runs once a Short's images arrive. Everything it needs already exists:
the design (angle, five lines, 23 plates), the -14 LUFS mix and the caption timing, the bound
archive clips, and the generated plates dropped into remotion/public/shorts/short<NN>/.

What it does:
  1. verifies every GENERATE/REUSE plate has a delivered image (refuses to assemble a Short with holes)
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
JOBS = ROOT / "runs" / "ae_jobs"          # After Effects job lists, one per Short


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
                        # Clamp the crop to the frame. A source TALLER than 9:16 makes ih*9/16
                        # wider than the picture and ffmpeg refuses outright: a 2160x3844 clip
                        # asked for 2162 px of a 2160 px frame and took the whole assembly down.
                        # Now that the archive drives are indexed there are vertical sources in
                        # the pool, so this is not a rare case any more.
                        "-vf", "crop='min(iw,ih*9/16)':ih,scale=1080:1920:flags=lanczos,fps=30",
                        "-an", "-c:v", "libx264", "-crf", "18", "-preset", "medium",
                        "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out)], check=True)
        rights.append({"file": out.name, "plate": p["n"], "ledger_title": p.get("bound_title"),
                       "license": p.get("bound_license"), "source": p.get("bound_source"),
                       "src_path": str(src)})
    (fx / "RIGHTS.json").write_text(json.dumps(rights, ensure_ascii=False, indent=2), encoding="utf-8")
    return rights


_WORD_NUM = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7,
    "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13,
    "fourteen": 14, "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18,
    "nineteen": 19, "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60,
    "seventy": 70, "eighty": 80, "ninety": 90, "hundred": 100, "thousand": 1000,
    "million": 1000000, "billion": 1000000000,
}


def _eval_run(ws: list[str]) -> int | None:
    """Value of one run of number words/digits: ['fifty','seven'] -> 57, ['209','million'] -> 209000000."""
    total = cur = 0
    seen = False
    for w in ws:
        if w.replace(".", "").isdigit():
            f = float(w)
            if f != int(f):
                return None
            cur += int(f)
            seen = True
            continue
        if w == "and":
            continue
        v = _WORD_NUM.get(w)
        if v is None:
            return None
        seen = True
        if v == 100:
            cur = (cur or 1) * 100
        elif v >= 1000:
            total += (cur or 1) * v
            cur = 0
        else:
            cur += v
    return total + cur if seen else None


def _split_digit_hyphen(text: str) -> str:
    """A hyphen between two DIGITS separates them; between two words it joins them.

    "twenty-two" is one number and must stay joined. "5-4" is a split decision and is two, but the
    joining rule read it as 5+4=9 and failed a correct card reading "5-4" over a line saying "five
    to four". Digits get the separator the words already have.
    """
    return re.sub(r"(?<=\d)-(?=\d)", " to ", text)


def _values(text: str) -> set[int]:
    """Every quantity the text states, including sub-phrases.

    Sub-phrases matter: a line that says "two hundred nine million dollars" legitimately supports
    type reading "209 MILLION" or "$209M", so the run's value AND the value of every contiguous
    part of it count as spoken.
    """
    toks = re.findall(r"\d+(?:\.\d+)?|[a-z]+",
                      _split_digit_hyphen(text.lower()).replace(",", "").replace("-", " "))
    vals: set[int] = set()
    run: list[str] = []

    def flush() -> None:
        for i in range(len(run)):
            for j in range(i + 1, len(run) + 1):
                v = _eval_run(run[i:j])
                if v is not None:
                    vals.add(v)

    for t in toks:
        # "and" holds a number together rather than ending it: the scripts write "two hundred and
        # fifty-one" and "four hundred and five dollars", and breaking there turned 251 and 405
        # into unspoken figures that failed real, correct type.
        if t.replace(".", "").isdigit() or t in _WORD_NUM or (t == "and" and run):
            run.append(t)
        else:
            flush()
            run = []
    flush()
    return vals


def numbers_not_spoken(phrase: "str | list[str]", line: str) -> list[str]:
    """Quantities on screen that the narration line never says, in either digits or words.

    Wording is free (owner, 2026-08-04); numbers are not. A viewer reads a figure as a fact from
    the documentary, so a figure the voice does not say is indistinguishable from invention. Both
    sides are reduced to values first, because the script spells numbers out for the narrator
    ("fifty-seven arrests") while the type shows digits ("57 ARRESTS") - the same fact.

    Values under two are not enforced: "one" is nearly always rhetorical ("NOT ONE CHARGE") rather
    than a count, and failing that would push writers back to quoting. A figure written in digits
    is always enforced, however small.
    """
    spoken = _values(line)
    missing = []
    # One segment per line of type. Joining them first merged "$209 MILLION" with "5,000 TRAVELERS"
    # into the single figure 209,005,000, which is spoken by nobody - the check failed correct type
    # on eight of thirty-one Shorts before this was split.
    segments = [phrase] if isinstance(phrase, str) else list(phrase)
    for seg in segments:
        toks = re.findall(r"\d+(?:\.\d+)?|[A-Za-z]+",
                          _split_digit_hyphen(seg or "").replace(",", "").replace("-", " "))
        run: list[str] = []
        for t in toks + [""]:
            low = t.lower()
            if low.replace(".", "").isdigit() or low in _WORD_NUM or (low == "and" and run):
                run.append(low)
                continue
            if run:
                v = _eval_run(run)
                digits = any(w.replace(".", "").isdigit() for w in run)
                if v is not None and (digits or v >= 2) and v not in spoken:
                    missing.append(" ".join(run))
                run = []
    return missing


def plan_kinetic(sid: str, short: dict, cut_bounds: dict[str, list[tuple[float, float]]]):
    """Turn the design's `kinetic_beats` into a ShortData field plus an After Effects job list.

    A beat names the line and the 1-based cut it lands on; this works out the absolute seconds and
    refuses to let the overlay outlive the cut. That constraint is the whole point: on short118's
    first pass the type left correctly but the rule and the scrim carried on over the next shot,
    which reads as a graphic someone forgot to take off rather than an emphasis.

    Owner approved the look on 2026-08-04. One or two beats per Short - more reads as decoration.
    """
    beats = short.get("kinetic_beats") or []
    if not beats:
        return "", []
    if len(beats) > 2:
        sys.exit(f"{sid}: {len(beats)} kinetic beats - the approved density is one or two")

    lines = {l["id"]: l["text"] for l in short.get("lines", [])}
    rows, jobs = [], []
    for b in beats:
        lid, sfx = b["line"], b["suffix"]
        cuts = cut_bounds.get(lid)
        if not cuts:
            sys.exit(f"{sid}: kinetic beat on {lid}, which has no cuts")
        # Where in the line the beat lands. `anchor` is the verbatim phrase the voice is saying at
        # that moment; the cut is derived from its word position, so the type appears WITH the
        # words instead of near them. A hand-picked cut number drifts the moment a line is re-timed.
        if "anchor" in b:
            text = lines.get(lid, "")
            pos = text.lower().find(b["anchor"].lower())
            if pos < 0:
                sys.exit(f"{sid}: anchor {b['anchor']!r} is not in {lid}: {text!r}")
            frac = len(text[:pos].split()) / max(1, len(text.split()))
            ci = min(len(cuts) - 1, int(frac * len(cuts)))
        else:
            ci = int(b.get("cut", 1)) - 1
        span = int(b.get("span_cuts", 1))
        span = min(span, len(cuts) - ci)
        # If the anchor lands late in its line there may be under a second left, and a 1.2 s flash
        # is worse than arriving a beat early: the type animates in over ~0.5 s anyway. Extend
        # BACKWARDS into earlier cuts of the same line rather than truncating.
        want_sec = float(b.get("seconds", 2.2))

        def room() -> float:
            return cuts[ci + span - 1][1] - cuts[ci][0] - 0.10

        # Extend backwards first - arriving a beat early is better than a flash, and the type takes
        # ~0.5 s to animate in anyway. Then forwards, for an anchor that lands on the FIRST cut of
        # its line, where there is nothing behind it: short92's L4 opens on a 0.78 s cut.
        while ci > 0 and room() < want_sec:
            ci -= 1
            span += 1
        while ci + span < len(cuts) and room() < want_sec:
            span += 1
        if ci < 0 or ci + span > len(cuts):
            sys.exit(f"{sid}: kinetic beat wants cuts {ci + 1}..{ci + span} of {lid}, "
                     f"which has {len(cuts)}")
        start, end = cuts[ci][0], cuts[ci + span - 1][1]
        at = round(start + 0.05, 2)
        room = round(end - at - 0.05, 2)
        want = float(b.get("seconds", 2.2))
        dur = round(min(want, room), 2)
        if dur < want - 0.01:
            print(f"  {sid} {sfx}: {want:.2f}s trimmed to {dur:.2f}s to stay inside "
                  f"{lid} cut {ci + 1}")
        if dur < 1.2:
            sys.exit(f"{sid}: {lid} cut {ci + 1} leaves only {dur:.2f}s - too short to read")

        phrase = b.get("big") and f"{b['big']} / {b.get('label', '')}".strip(" /") or \
            " ".join(b.get("words") or [])
        # Wording is free (owner, 2026-08-04): the type may sharpen what the line says rather than
        # quote it, so "THEY TOOK IT ALL" is allowed over a line that never uses those words.
        # Quantities are NOT free. A figure on screen that the voice never says is the one error
        # here that is indistinguishable from making something up, so it stays a hard stop.
        bad = numbers_not_spoken(b.get("words") or [b.get("big", ""), b.get("label", "")],
                                 lines.get(lid, ""))
        if bad:
            sys.exit(f"{sid} {sfx}: {', '.join(bad)} on screen, but {lid} does not say it")
        rows.append(f"    {{src: 'shorts/{sid}/{sid}_kin_{sfx}.webm', atSec: {at}, "
                    f"durSec: {dur}, phrase: {json.dumps(phrase)}}},")
        requested_style = b.get("style", "number")
        # The AE template has two concrete renderers: `number` and `punch`.  Editorial designs use
        # `turn` as the semantic name for a story turn, so map it to the punch renderer here instead
        # of letting the JSX fall through to `number` with an undefined `big` value.  Likewise, a
        # one-line number beat is commonly authored as `words`; promote it to `big`, which is the
        # schema the number renderer actually consumes.
        if requested_style in ("turn", "punch"):
            ae_style = "punch"
        elif requested_style == "number":
            ae_style = "number"
        else:
            sys.exit(f"{sid} {sfx}: unsupported kinetic style {requested_style!r}")
        job = {"id": f"{sid}_{sfx}", "style": ae_style, "seconds": dur}
        for k in ("big", "bigSize", "label", "labelSize", "words"):
            if k in b:
                job[k] = b[k]
        if ae_style == "number" and not job.get("big"):
            words = job.get("words") or []
            if not words:
                sys.exit(f"{sid} {sfx}: number kinetic beat needs `big` or `words`")
            job["big"] = " ".join(words)
        if ae_style == "punch" and not job.get("words"):
            sys.exit(f"{sid} {sfx}: punch kinetic beat needs `words`")
        jobs.append(job)

    src = ("  // Mid-roll kinetic type, built in After Effects (runs/ae_jobs/%s.json) and installed\n"
           "  // into this Short's public directory by scripts/ae/render_beats.sh. Words are taken\n"
           "  // verbatim from the narration line each beat sits on.\n"
           "  kineticBeats: [\n%s\n  ],\n") % (sid, "\n".join(rows))
    return src, jobs


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
                 if q.get("role") == "hook" and q.get("source") in {"GENERATE", "REUSE"}] or [1]
    loop_plates = [q["n"] for q in short["plates"] if q.get("role") == "loop"]

    for p in short["plates"]:
        n, line = p["n"], p.get("line", "L1")
        role = p.get("role")
        if p.get("source") == "FOOTAGE" and p.get("bound_file"):
            src = f"shorts/{sid}/fx/fx_{n:02d}.mp4"
            kind, motion = "video", "video"
        elif p.get("source") in {"GENERATE", "REUSE"}:
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
__KINETIC__}};
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
    cut_bounds: dict[str, list[tuple[float, float]]] = {}
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
        # Absolute [start, end] of every cut on this line, in the order buildBeats lays them out.
        # The kinetic overlays are placed against these: an overlay that outlives its cut leaves
        # the rule and the scrim hanging over an unrelated shot (measured on short118's first pass).
        t = a0
        for c in mine:
            d = cta if "isCta: true" in c else rest
            cut_bounds.setdefault(w["id"], []).append((t, t + d))
            t += d

    kinetic_ts, jobs = plan_kinetic(sid, short, cut_bounds)
    ts = ts.replace("__KINETIC__", kinetic_ts)
    if jobs:
        JOBS.mkdir(parents=True, exist_ok=True)
        (JOBS / f"{sid}.json").write_text(json.dumps(jobs, ensure_ascii=False, indent=2),
                                          encoding="utf-8")
        print(f"  {len(jobs)} kinetic beat(s) -> {(JOBS / f'{sid}.json')}")
        print(f"    render them BEFORE the Short: bash scripts/ae/render_beats.sh "
              f"runs/ae_jobs/{sid}.json")

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

    want = {p["n"] for p in short["plates"] if p.get("source") in {"GENERATE", "REUSE"}}
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
        got = False
        vid = design["destination"]["video_id"]
        # The local package thumbnail first. i.ytimg serves nothing for a video that is still
        # private, and every long-form is private until its scheduled date - so nineteen Shorts
        # fetched a 1 kB 404 body, were told "fetched", and died at render time on
        # "Error loading image". The bytes we uploaded are on disk anyway.
        pkg = ROOT / "episodes" / design["episode_id"] / "09_package"
        local = sorted(list(pkg.glob("thumbnail.ctr*.png")) + list(pkg.glob("thumbnail.auto*.png"))
                       + list(pkg.glob("thumbnail*.jpg")))
        if local:
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(local[0]),
                            "-vf", "scale=1280:720", "-q:v", "3", str(thumb)], check=True)
            got = thumb.exists() and thumb.stat().st_size > 3000
            if got:
                print(f"  destination thumbnail from {local[0].name}")
        if not got:
            for q in ("maxresdefault", "hqdefault"):
                try:
                    urllib.request.urlretrieve(f"https://i.ytimg.com/vi/{vid}/{q}.jpg", thumb)
                    if thumb.exists() and thumb.stat().st_size > 3000:
                        got = True
                        print(f"  fetched destination thumbnail from YouTube ({q})")
                        break
                except Exception:
                    pass
        # Loud, not silent: the funnel card renders this image, and a missing one does not degrade
        # the card, it aborts the whole render.
        if not got:
            thumb.unlink(missing_ok=True)
            sys.exit(f"{sid}: no destination thumbnail. {vid} serves none (private?) and "
                     f"{pkg.relative_to(ROOT)} has no thumbnail*.png")

    rights = stage_footage(sid, short["plates"], args.force)
    print(f"{sid}: {len(have)} image plates present, {len(rights)} archive clips staged")
    out = emit_ts(sid, design["episode_id"], design, short)
    print(f"  wrote {out.relative_to(ROOT)}")
    print(f"  rights recorded in {(PUB/sid/'fx'/'RIGHTS.json').relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
