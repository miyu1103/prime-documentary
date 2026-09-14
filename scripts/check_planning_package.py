"""FREE, PRE-SPEND gate: audit an EP planning package (script/design/CODEX_A) against
the channel's known repeat-failure modes BEFORE anything is spent on TTS/GPU/build.

Owner directive 2026-07-26: "同じ失敗を繰り返さない". Per the meta-rule
(lessons-must-be-gates), every enforceable lesson becomes a blocking check:

  F1  runtime shortfall            -> check_script_length.py band PASS (EP14/15/34/38)
  F2  Japanese mixed into EN script-> narration dropped silently at TTS (EP38)
  F3  hook->OP->acts->ED structure -> missing on EP21-24 ("いつもの構成でない")
  F4  self-declared QC             -> this tool IS the independent measurement
  F5  dochighlight figure          -> reads as a rendering bug; owner flagged 3x (EP40/41/42)
  F6  DATE_STAMP overlay           -> banned since EP50
  F7  kamishibai / motion poverty  -> DESIGN must carry the perceptual-motion budget
                                      (figure beats >= 82 on 30-min, AE hero program)
  F8  variant-spam images          -> CODEX_A must carry 1-scene-1-image / no variants
  F9  real-person likeness         -> CODEX_A must carry the likeness ban block
  F10 review theater               -> review log must contain real R1/R2 (and R3 when done)

Usage:
    python scripts/check_planning_package.py <EPNN> <slug> [--lo 1740] [--hi 1860] [--require-r3]
e.g.
    python scripts/check_planning_package.py 53 norfolk --require-r3
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "episodes" / "_planning"

CJK = re.compile(r"[぀-ヿ㐀-鿿！-｠]")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("ep", help="episode number, e.g. 53")
    ap.add_argument("slug", help="episode slug, e.g. norfolk")
    ap.add_argument("--lo", type=int, default=1740, help="runtime band floor seconds")
    ap.add_argument("--hi", type=int, default=1860, help="runtime band ceiling seconds")
    ap.add_argument("--require-r3", action="store_true",
                    help="fail unless the review log contains a substantive R3 section")
    args = ap.parse_args()

    ep, slug = args.ep, args.slug
    base = f"EP{ep}_{slug}"
    files = {
        "ledger": PLAN / f"{base}_FACTS_LEDGER.v001.md",
        "script": PLAN / f"{base}_script.en.v001.md",
        "review": PLAN / f"{base}_review_log.v001.md",
        "design": PLAN / f"{base}_DESIGN_ARCHITECTURE.v001.md",
        "codex_a": PLAN / f"{base}_CODEX_A_ASSETS.v001.md",
    }

    failures: list[str] = []
    warnings: list[str] = []

    # F-existence -----------------------------------------------------------
    for key, p in files.items():
        if not p.exists():
            failures.append(f"MISSING {key}: {p.name}")
    if failures:
        for f in failures:
            print(f"FAIL {f}")
        print(f"\nRESULT: FAIL ({len(failures)} blocking)")
        return 1

    script_text = files["script"].read_text(encoding="utf-8")
    review_text = files["review"].read_text(encoding="utf-8")
    design_text = files["design"].read_text(encoding="utf-8")
    codex_text = files["codex_a"].read_text(encoding="utf-8")

    # F1 runtime band via the canonical gate ---------------------------------
    r = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "check_script_length.py"),
         "--lo", str(args.lo), "--hi", str(args.hi), str(files["script"])],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    gate_out = (r.stdout or "") + (r.stderr or "")
    if "PASS" in gate_out and "FAIL" not in gate_out:
        print(f"ok   F1 script_length gate PASS ({args.lo}-{args.hi}s)")
    else:
        failures.append(f"F1 script_length gate did not PASS:\n{gate_out.strip()}")

    # F2 CJK in narration body ----------------------------------------------
    bad_lines = []
    for i, line in enumerate(script_text.splitlines(), 1):
        s = line.strip()
        if not s or s.startswith("#") or s.startswith(">") or s.startswith("【") or "【OST" in s:
            continue
        if CJK.search(s):
            bad_lines.append(f"  line {i}: {s[:60]}")
    if bad_lines:
        failures.append("F2 CJK characters inside narration body (TTS will drop/garble):\n"
                        + "\n".join(bad_lines[:10]))
    else:
        print("ok   F2 narration body is CJK-free")

    # F3 canonical structure --------------------------------------------------
    for marker in ("COLD OPEN", "OPENING", "ACT"):
        if marker not in script_text:
            failures.append(f"F3 script missing structural marker: {marker}")
    if all(m in script_text for m in ("COLD OPEN", "OPENING", "ACT")):
        print("ok   F3 hook->OP->acts structure markers present")

    # F5/F6 bans ---------------------------------------------------------------
    for ban, code in (("dochighlight", "F5"), ("DATE_STAMP", "F6")):
        prohib = (r"禁止|ban|banned|do not|使わない|作らない|書かない|言及しない|描かない|なし|ゼロ|zero"
                  r"|absent|不可|FAIL|reject|grep|0件|R-[A-Z]"
                  # a hit inside a machine-gate ban-regex block IS a prohibition
                  r"|re\.(compile|IGNORECASE)")
        hits = []
        for n, t in (("design", design_text), ("codex_a", codex_text)):
            # every occurrence must sit in a prohibitive context; one permissive use = fail
            for m in re.finditer(ban, t, re.I):
                ctx = t[max(0, m.start() - 300):m.end() + 200]
                if not re.search(prohib, ctx, re.I):
                    hits.append(f"{n} (…{t[max(0, m.start() - 60):m.end() + 120].strip()}…)")
                    break
        if hits:
            failures.append(f"{code} banned element '{ban}' referenced non-prohibitively in: {', '.join(hits)}")
        else:
            print(f"ok   {code} '{ban}' absent or explicitly banned")

    # F7 motion budget in DESIGN ----------------------------------------------
    if re.search(r"(figure[- ]?beat|FigureBeat)", design_text, re.I) and re.search(r"8[2-9]|9\d|1\d\d", design_text):
        print("ok   F7 DESIGN carries figure-beat density budget")
    else:
        failures.append("F7 DESIGN missing figure-beat (>=82) motion budget")
    if not re.search(r"AE|hero", design_text, re.I):
        failures.append("F7 DESIGN missing AE hero program section")

    # F8 one-scene-one-image rule in CODEX_A -----------------------------------
    if re.search(r"1シーン1枚|バリエーション0|variants?\s*(指定なし|0)|--variants 3.{0,20}(使わない|禁止)", codex_text):
        print("ok   F8 CODEX_A carries 1-scene-1-image / no-variants rule")
    else:
        failures.append("F8 CODEX_A missing the 1-scene-1-image / no-variants rule")

    # F9 likeness ban in CODEX_A ------------------------------------------------
    if re.search(r"likeness|肖像", codex_text, re.I):
        print("ok   F9 CODEX_A carries the real-person likeness ban")
    else:
        failures.append("F9 CODEX_A missing the real-person likeness ban block")

    # F10 review rounds -----------------------------------------------------------
    has_r1 = re.search(r"R1|Round\s*1|ラウンド1", review_text, re.I)
    has_r2 = re.search(r"R2|Round\s*2|ラウンド2", review_text, re.I)
    r3_match = re.search(r"(?:^|\n)#+[^\n]*(?:R3|Round\s*3)[^\n]*\n(.{200,})", review_text, re.I | re.S)
    if not (has_r1 and has_r2):
        failures.append("F10 review log missing substantive R1/R2 sections")
    else:
        print("ok   F10 review log has R1+R2")
    if args.require_r3:
        # substantive = long enough to hold real audit evidence AND not self-labeled placeholder
        r3_body = r3_match.group(1) if r3_match else ""
        if (len(r3_body) >= 1500
                and "placeholder" not in r3_body.lower()
                and "プレースホルダ" not in r3_body):
            print("ok   F10 review log has substantive R3")
        else:
            failures.append("F10 --require-r3: R3 section absent, too thin (<1500 chars), or placeholder-labeled")

    # thumbnail faces present in CODEX_A (EP21-24 F7 'サムネ地味' upstream fix) ----
    if re.search(r"T0?1.{0,40}face|emotive", codex_text, re.I):
        print("ok   thumb: CODEX_A includes emotive-face thumbnail stills")
    else:
        warnings.append("CODEX_A has no emotive-face thumbnail section (CTR driver #1)")

    # word count report ------------------------------------------------------------
    words = len(re.findall(r"[A-Za-z']+", script_text))
    print(f"info word-ish count (latin tokens): {words}")

    for w in warnings:
        print(f"WARN {w}")
    if failures:
        print()
        for f in failures:
            print(f"FAIL {f}")
        print(f"\nRESULT: FAIL ({len(failures)} blocking, {len(warnings)} warn)")
        return 1
    print(f"\nRESULT: PASS ({len(warnings)} warn)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
