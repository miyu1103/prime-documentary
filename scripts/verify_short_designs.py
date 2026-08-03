#!/usr/bin/env python3
"""Mechanically verify authored Short designs. Written BEFORE any fan-out, on purpose.

A previous run of this project had a verification agent fabricate 10 of 15 items, URLs included
(memory: feedback_subagent_fabrication). The lesson is not "trust agents less", it is "make the
output checkable". So every design carries `source_lines`: the verbatim sentence(s) from the
episode's own verified script that a spoken line was built from. This checks that each one
actually appears in that script. An invented quotation cannot survive.

Checks per short:
  1. required fields present (angle, funnel question, >=8 lines, delivery shape)
  2. every source_lines entry appears VERBATIM in the episode's script (whitespace-normalised)
  3. spoken word count inside 150-195 (the band that lands 55-60 s at this voice speed)
  4. the angle does not simply restate what the episode's EXISTING Short already said
  5. short_id is unique across the whole set and outside the 60-81 range reserved by the
     EP53-56 / EP57-59 slates
  6. no invented claim ids (claims must be empty or bound later by pd-verify)

Exit code 1 if anything fails, so it can gate a batch.

Usage: py -3.11 scripts/verify_short_designs.py [--only PD-2026-016-titan]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGNS = ROOT / "episodes" / "_planning" / "short_designs"
RESERVED = set(range(60, 82))
DELIVERY_VALUES = {"intense", "building", "calm"}

# Length spec, revised 2026-08-03 against the channel's own delivered work rather than a guess:
#   already published/delivered Shorts   median 55.0 s   (29 files, only 3 under 45 s)
#   the 5-line batch built before this   median 33.1 s   (14 of 14 under 45 s)
# Narration drives duration at ~3.0 words/sec, so 55-60 s needs ~165-180 words, which is 8 lines
# at this line length. The band is widened from 75-135 because the SPEC changed, not to let a
# failing design through — a 100-word design is now genuinely too short to ship.
MIN_LINES = 8
# The opening line. 22 was tried first and was wrong: it came from the earlier batch's MEAN
# hook length (18.5 words), and a mean makes a useless ceiling - it failed 38 designs
# including ones already rendered and scheduled. There is no measurement showing a
# 23-word hook performs worse than a 22-word one, so failing on it would have forced 42
# re-renders on a guess. HOOK_WARN reports the drift; HOOK_MAX_WORDS fails only where
# length is indefensible on its face.
HOOK_WARN_WORDS = 24
HOOK_MAX_WORDS = 32
WORD_BAND = (150, 195)

# Owner 2026-08-02: the Shorts are to loop. A spoken "watch the full case on the channel" ends the
# audio dead, and it has not earned its place anyway - 46 published Shorts carry that line and 45
# of them converted zero subscribers. The destination now lives on the card, the description and
# the related-video link; L5's job is to hand the viewer back to L1.
CTA_WORDS = re.compile(r"\b(on the channel|full case|follow for|subscribe|link below|"
                       r"watch the full|our profile)\b", re.I)


def norm(s: str) -> str:
    """Whitespace/case normalisation, plus: never let a space before punctuation decide a match.

    Removing a "[CLM-0008]" tag leaves "judge  ." where the quotation reads "judge." — a
    one-character difference that failed four genuinely verbatim lines on the first run.
    """
    s = re.sub(r"\s+", " ", s or "").strip().lower()
    return re.sub(r"\s+([.,;:!?])", r"\1", s)


def strip_apparatus(text: str) -> str:
    """Same transform build_short_design_skeletons.py applies before offering candidate lines.

    Without it every legitimately-derived quotation fails: the candidate lines were extracted from
    text with the shot notes and [CLM-####] tags removed, so they carry the gaps those removals
    left, while the raw script does not. The first run of this checker flagged five such lines as
    "NOT FOUND" when they were verbatim.
    """
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.S)
    text = re.sub(r"【.*?】", " ", text, flags=re.S)
    text = re.sub(r"〔.*?〕", " ", text, flags=re.S)
    text = re.sub(r"\((?:VIS|SFX|ANCHOR|OST|CARD|SILENCE)[^)]*\)", " ", text, flags=re.I)
    text = re.sub(r"\[(?:SHOT|CLM|VO|OST|CARD|TITLE|SILENCE|beat)[^\]]*\]", " ", text, flags=re.I)
    text = re.sub(r"\[[A-Z0-9\-– ,.:]{0,40}\]", " ", text)
    return text


def script_text(rel: str | None) -> str:
    if not rel:
        return ""
    p = ROOT / rel
    if not p.exists():
        return ""
    raw = p.read_text(encoding="utf-8", errors="replace")
    # keep both: a quotation may be lifted from either form
    return norm(raw) + "\n<<<STRIPPED>>>\n" + norm(strip_apparatus(raw))


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--only")
    args = ap.parse_args()

    seen_ids: dict[str, str] = {}
    fails: list[str] = []
    warns: list[str] = []
    checked = 0

    for f in sorted(DESIGNS.glob("*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        ep = d["episode_id"]
        if args.only and ep != args.only:
            continue
        body = script_text(d.get("script"))
        existing = norm(" ".join(c for caps in d["existing_angles_do_not_repeat"].values() for c in caps))

        for s in d["shorts"]:
            if not s.get("angle"):
                continue
            checked += 1
            sid = s.get("short_id") or "<none>"
            tag = f"{ep} {sid}"

            for field in ("angle", "funnel_question_left_for_longform", "lines"):
                if not s.get(field):
                    fails.append(f"{tag}: missing {field}")

            if sid in seen_ids:
                fails.append(f"{tag}: short_id already used by {seen_ids[sid]}")
            seen_ids[sid] = tag
            m = re.match(r"short(\d+)", sid)
            if m and int(m.group(1)) in RESERVED:
                fails.append(f"{tag}: short_id is inside the reserved 60-81 slate range")

            lines = s.get("lines") or []

            # Shape rather than an exact sequence. An exact 5-element list made this check
            # meaningless the moment the spec moved to 8 lines, and an over-tight rule is how a
            # real finding ends up buried under noise. What actually matters: open hard, land soft,
            # and keep the middle building.
            deliveries = [l.get("delivery") for l in lines]
            bad = [d for d in deliveries if d not in DELIVERY_VALUES]
            if bad:
                fails.append(f"{tag}: unknown delivery value(s) {sorted(set(bad))}")
            elif deliveries:
                if deliveries[0] != "intense":
                    fails.append(f"{tag}: first line delivery is {deliveries[0]!r}, must be 'intense'")
                if deliveries[-1] != "calm":
                    fails.append(f"{tag}: last line delivery is {deliveries[-1]!r}, must be 'calm'")
                if deliveries.count("building") < 3:
                    fails.append(f"{tag}: only {deliveries.count('building')} 'building' lines, "
                                 f"the middle needs at least 3")

            # The loop line is the LAST line, whatever it is numbered. This used to select
            # id == "L5" literally, so after the 5 -> 8 line change it silently graded a middle
            # line and every real loop defect would have passed unnoticed.
            loop_line = lines[-1] if lines else None
            if loop_line and s.get("loop"):
                lid = loop_line.get("id", "?")
                txt = loop_line.get("text") or ""
                if CTA_WORDS.search(txt):
                    fails.append(f"{tag} {lid}: still contains a spoken CTA -> {txt[-60:]!r}")
                n_last = len(txt.split())
                if not (8 <= n_last <= 32):
                    fails.append(f"{tag} {lid}: {n_last} words - a loop line should be 8-32")
                if not (s.get("loop_join") or "").strip():
                    fails.append(f"{tag}: loop=true but no loop_join note explaining how {lid} "
                                 f"hands back to L1")
                first = " ".join((lines[0].get("text") or "").lower().split()[:6])
                if first and first in txt.lower():
                    fails.append(f"{tag} {lid}: repeats L1 verbatim instead of leading into it")

            if len(lines) < MIN_LINES:
                fails.append(f"{tag}: {len(lines)} lines, the spec is {MIN_LINES}")

            # The hook is the only line that has to work before the viewer decides to stay, so it
            # is the one line where length is a defect rather than a preference. Measured drift:
            # shorts 86-120, written a couple of episodes at a time, average an 18.5-word hook;
            # shorts 182-258, written 31 at once, average 22.2. Nothing else moved - fact density
            # actually rose - but the opening got a fifth longer, and a long opening lands late.
            if lines:
                n_hook = len((lines[0].get("text") or "").split())
                if n_hook > HOOK_MAX_WORDS:
                    fails.append(f"{tag} {lines[0].get('id','L1')}: hook is {n_hook} words, "
                                 f"max {HOOK_MAX_WORDS} - nobody stays for an opening that long")
                elif n_hook > HOOK_WARN_WORDS:
                    warns.append(f"{tag} {lines[0].get('id','L1')}: hook is {n_hook} words "
                                 f"(>{HOOK_WARN_WORDS}) - lands late, but not a defect")

            words = sum(len((l.get("text") or "").split()) for l in lines)
            if not (WORD_BAND[0] <= words <= WORD_BAND[1]):
                fails.append(f"{tag}: {words} spoken words, outside "
                             f"{WORD_BAND[0]}-{WORD_BAND[1]}")

            for l in lines:
                if l.get("claims"):
                    fails.append(f"{tag} {l['id']}: claim ids must be left empty until pd-verify binds them")
                for src in (l.get("source_lines") or []):
                    if not body:
                        fails.append(f"{tag} {l['id']}: no script on disk to verify against")
                        break
                    if norm(src) not in body:
                        fails.append(f"{tag} {l['id']}: source_line NOT FOUND in the script -> "
                                     f"{src[:70]!r}")

            # 4. the angle must not be a restatement of the existing Short
            if existing:
                ratio = SequenceMatcher(None, norm(s["angle"]), existing).find_longest_match(
                    0, len(norm(s["angle"])), 0, len(existing)).size
                if ratio > 45:
                    fails.append(f"{tag}: angle overlaps the existing Short by {ratio} chars verbatim")

    if warns:
        print(f"\n{len(warns)} WARNINGS (not failures):")
        for w in warns[:12]:
            print(f"  {w}")
        if len(warns) > 12:
            print(f"  ... and {len(warns)-12} more")
    print(f"checked {checked} authored shorts across {len(list(DESIGNS.glob('*.json')))} episodes")
    if fails:
        print(f"\n{len(fails)} FAILURES:")
        for x in fails:
            print("  " + x)
        return 1
    print("all checks pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
