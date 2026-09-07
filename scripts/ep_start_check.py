#!/usr/bin/env python
"""Run the gates BEFORE the work, on the empty form, so the target is known on day zero.

WHY THIS EXISTS. The owner's observation on 2026-08-24, after a day of them:
"something always breaks half way through -- I think the beginning is what matters."

Every defect that day was decided at the start of a step and only surfaced later:

  * a handoff carried a title the source contradicts -- decided when the title was written,
    found four hours later while reading the NTSB preliminary report
  * two scripts were marked green by the road at 3,062 and 2,784 words against a declared
    4,640-5,120 band -- decided when the road was wired with one gate instead of three
  * 29 thumbnail plates came back nearly black and unsaturated -- decided by one phrase,
    "deep black palette, vast empty dark negative space", in the order that produced them
  * a 121-row image order could not be parsed by the exporter it was written for -- decided
    the moment the table was given two columns instead of the canonical four

None of those needed a smarter person. Each needed the check that would eventually judge the
work to be run at the start, on nothing, so its rules were visible before the hours went in.

    py -3.11 scripts/ep_start_check.py --slug <slug> --step script
    py -3.11 scripts/ep_start_check.py --slug <slug> --step order
    py -3.11 scripts/ep_start_check.py --slug <slug> --step thumbs

It prints the numbers the work must hit, then proves the graders run, on a stub. It writes
nothing into the episode.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

# Windows consoles here are cp932. Without this the tool dies on its own em dash
# before printing a single target, which is the opposite of its whole purpose.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def sh(cmd: list[str]) -> tuple[int, str]:
    p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, errors="ignore")
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def spec_for(slug: str):
    from check_episode_spec import load_and_validate
    spec, problems, _ = load_and_validate(slug)
    return spec, problems


def step_script(slug: str) -> int:
    spec, problems = spec_for(slug)
    if not spec:
        print("The contract is not valid yet, so the script has no target. Fix this first:")
        for p in problems:
            print("   -", p)
        return 1

    lo_s, hi_s = (int(v) for v in spec["runtime_seconds"])
    lo_w, hi_w = (int(v) for v in spec["script_words"])
    acts = spec["section_vocabulary"]

    print("WRITE TO THESE NUMBERS. They come from this episode's own contract.\n")
    print(f"  runtime          {lo_s}-{hi_s} s  ({lo_s/60:.0f}-{hi_s/60:.0f} min)")
    print(f"  spoken words     {lo_w}-{hi_w}")
    print(f"  sections         {len(acts)}: {' / '.join(acts)}")
    print(f"  questions        one per act, and no gap over 7 minutes at 160 wpm")
    print(f"  short sentences  20-35 % of all sentences, six words or fewer")
    print(f"  emotion commands 0.  'imagine', 'shockingly', 'sit with' all count")
    print(f"  hard facts       5-12 per minute")
    print(f"  you / your       under 8 per 1,000 words")
    print(f"  questions        under 2 per 1,000 words")
    print("\nAND THE PART NO GATE MEASURES (PD_SCREENPLAY_STANDARD, binding):")
    print("  * the controlling idea is ONE sentence and is NEVER spoken in the film")
    print("  * ONE motif: a thing shown in changing states, never explained, looping at the end")
    print("  * silences are written, not directed: place them after the recognition,")
    print("    after the limit, and before the final image")
    print("  * no villain. state the system's own rationale before showing its failure")
    print("  * the ENDING adds no new fact. it re-frames what is already there")

    print("\nNow proving the graders actually run, on the template as it stands:\n")
    rc_any = 0
    s = list((ROOT / "episodes/_planning").glob(f"EP*_{slug}_script.en.v*.md"))
    if not s:
        print("  no script file yet -- run ep_road.py --slug %s --start NN first" % slug)
        return 1
    script = s[0]

    for label, cmd in (
        ("ep77_standard", ["py", "-3.11", "scripts/check_ep77_standard.py",
                           "--slug", slug, "--stage", "inputs"]),
        ("script_length", ["py", "-3.11", "scripts/check_script_length.py",
                           "--lo", str(lo_s), "--hi", str(hi_s), str(script)]),
        ("script_craft", ["py", "-3.11", "scripts/check_script_craft.py", str(script),
                          "--words", str(lo_w), str(hi_w)]),
    ):
        rc, out = sh(cmd)
        head = next((l.strip() for l in out.splitlines()
                     if l.strip().startswith(("FAIL", "PASS", "["))), out.strip()[:100])
        print(f"  {label:14s} exit {rc}  {head[:110]}")
        rc_any |= rc
    print("\nAll three run. A tick on the road now means all three, not one of them.")
    return 0


def step_order(slug: str) -> int:
    """Prove the order's SHAPE before 121 rows are written into the wrong one."""
    print("The exporter reads exactly one table shape. Prove it on two rows, not on 121.\n")
    stub = ("# STUB\n\n"
            "**`[STYLE]`** — prepend to every plate:\n\n"
            "> cinematic documentary reconstruction, one practical light source visible in the "
            "frame, high contrast, photorealistic, 16:9,\n\n"
            "**`[NEG]`** — append to every plate:\n\n"
            "> Avoid: text, lettering, handwriting, cursive, signature, numerals, numbers, "
            "seals, emblems, logos, badge, insignia, human face, facial features, portrait, "
            "identifiable person, low-resolution.\n\n"
            "### HOOK\n\n"
            "| id | beat | prompt | flags |\n|---|---|---|---|\n"
            "| H001 | H001 | A wall-mounted operations clock in a dim room under one desk lamp | |\n"
            "| H002 | H002 | Two anonymous workers seen from behind on a deck at night | P |\n")
    tmp = Path(tempfile.mkdtemp()) / f"EP00_{slug}_CODEX_BATCH_A.v001.md"
    tmp.write_text(stub, encoding="utf-8")

    rc1, out1 = sh(["py", "-3.11", "scripts/check_image_order_neg.py", "--file", str(tmp)])
    print(f"  check_image_order_neg  exit {rc1}  {out1.strip().splitlines()[-1][:110] if out1.strip() else ''}")
    rc2, out2 = sh(["py", "-3.11", "scripts/export_codex_batch_paste.py",
                    "--order", str(tmp), "--dry-run"])
    print(f"  export_codex_batch     exit {rc2}  {out2.strip().splitlines()[0][:110] if out2.strip() else ''}")
    print("\nRules the shape enforces, learned the hard way on 2026-08-24:")
    print("  * FOUR columns: id | beat | prompt | flags. Two columns parse as zero plates")
    print("  * sections are '### NAME'. '## 5. NAME' is invisible to the parser")
    print("  * [STYLE] is PREPENDED, [NEG] appended. Writing 'paste after' inverts one of them")
    print("  * the people flag is the single letter P. 'PEOPLE' counts as zero people plates")
    print("  * [NEG] must be a BLOCKQUOTE and must carry all five token families, including")
    print("    handwriting -- a fenced code block is not read at all")
    return rc1 | rc2


def step_thumbs(slug: str) -> int:
    print("Thumbnail plates are judged against the two this channel actually converted with.\n")
    rc, out = sh(["py", "-3.11", "scripts/check_thumb_punch.py", "--demo"])
    for line in out.strip().splitlines()[-4:]:
        print("  " + line[:110])
    print("\n  bands: brightness 42-78 | contrast 60-95 | lit 3-16 % | dark 35-72 % | saturation 30-85")
    print("\nTwo phrases are banned in a thumbnail order because they produced 29 failing plates:")
    print("  'deep black palette'   and   'vast empty dark negative space'")
    print("Every plate needs a coloured practical light IN the frame and a subject at 40-60 %.")
    print("\nAnd shape is not meaning. After delivery run:")
    print("  py -3.11 scripts/thumb_feed_sheet.py <dir>   and look at 168x94.")
    return rc


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--step", required=True, choices=["script", "order", "thumbs"])
    a = ap.parse_args()
    print(f"=== start check — {a.slug} — {a.step} ===\n")
    return {"script": step_script, "order": step_order, "thumbs": step_thumbs}[a.step](a.slug)


if __name__ == "__main__":
    sys.exit(main())
