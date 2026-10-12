#!/usr/bin/env python
"""The binding documents must not disagree with each other. This is the check that says so.

WHY. On 2026-08-23 a scan of the documents that call themselves binding found ten places where
two of them answered the same question differently. The worst pair were the two files every new
session is told to read first: `docs/PD_CANON.md` stated the pre-2026-08-12 shipping rule under
the heading "rule 19 enforces this", while `.claude/rules/19-ship-gate.md` said that rule had
been abolished -- and the code (`upload_schedule_case_v001.py:26`) had already moved on. Others:
the production spec split across v1/v2/v3 with **zero** binding documents pointing at the
version EP72-76 were actually built to; the title length stated as both "<=60" and "59-100";
the hook written "FIRST" and "last" in the same file; three different answers for runtime; and
`animation_density` described as mandatory and advisory on adjacent lines.

None of that was carelessness. Each was a correct decision written in a new place while the old
place kept its old sentence. The volume makes it invisible: twenty documents call themselves
binding and a session is asked to read about 27,000 words before starting.

So this is not a style checker. Every rule below is a contradiction that actually existed, and
the check exists so the SAME one cannot come back silently. When a new one is found, add a rule
here rather than a paragraph to docs/ -- docs/ already holds 135,000 words and is not read at
run time (`.claude/rules/20`).

    py -3.11 scripts/check_doc_contradictions.py            # exit 1 if anything disagrees
    py -3.11 scripts/check_doc_contradictions.py --demo     # prove it still catches things

A check that has never been shown to fail is decoration (docs/HANDOVER.md, permanent rule 5).
`--demo` writes a deliberately contradictory file to a temp directory, runs the rules over it,
and asserts they fire.
"""
from __future__ import annotations

import argparse
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Documents that bind execution. Per-episode planning notes and dated handovers are records of
# what was true on a day and are deliberately NOT included: a record is allowed to be old.
def binding_files() -> list[Path]:
    out = [ROOT / "CLAUDE.md", ROOT / "AGENTS.md"]
    out += sorted((ROOT / ".claude" / "rules").glob("*.md"))
    out += sorted((ROOT / ".claude" / "skills").rglob("SKILL.md"))
    out += sorted((ROOT / ".claude" / "agents").glob("*.md"))
    out += [ROOT / "docs" / n for n in (
        "HANDOVER.md", "PD_CANON.md", "PD_SHIP_GATE.md", "PD_WINNING_PATTERN.md",
        "PD_EPISODE_SPEC_STANDARD.v001.md", "PD_EPISODE_DESIGN_MANUAL.v001.md",
        "PD_EDITORIAL_DIRECTION.v002.md", "PD_SCREENPLAY_STANDARD.v001.md",
        "PD_ONE_PASS_PRODUCTION_SPEC.v3.md")]
    return [p for p in out if p.is_file()]


# A line is exempt when it says, in the line itself, that it is quoting history. That is how a
# document records "this used to say X" without tripping the rule that forbids X.
EXEMPT = re.compile(
    r"廃止|訂正|SUPERSEDED|superseded|supersedes|記録|the record|corrected|旧ルール|それまで|"
    r"予定|以前|was still|used to|contradicts itself|2026-08-23|"
    # A line that FORBIDS the retired tool is the opposite of an instruction to use it.
    r"do not implement|do not use|never use|使わない|禁止|retired", re.I)

RULES: list[tuple[str, str, str]] = [
    # (id, regex, what is wrong with a line that matches)
    ("spec_version",
     r"PD_ONE_PASS_PRODUCTION_SPEC\.v[12]\b",
     "points at production spec v1/v2. v3 binds from EP72; v1/v2 are records. Say which."),
    ("title_length",
     r"タイトル\s*(?:≤|<=)\s*60|title\s*(?:≤|<=)\s*60\s*chars",
     "states the <=60 character title cap. v3 measured it at 1.38% CTR and replaced it "
     "with 59-100 characters."),
    ("hook_order",
     r"hook[^.\n]{0,40}written\s+last|フック[^。\n]{0,10}最後に書",
     "says the hook is written last. Owner decision 2026-08-10, binding from EP66: FIRST."),
    ("runtime_default",
     r"(?:標準|standard)[^\n]{0,12}11\.5|11\.5\s*分[^\n]{0,6}(?:標準|既定)",
     "presents 11.5 minutes as the standard runtime. The only source of truth is "
     "episode_spec.runtime_seconds; 690-750s is a fallback for episodes that declare nothing."),
    ("ship_rule",
     r"ハード不合格が\s*`?runtime_band`?、?\s*\*?\*?または",
     "states the shipping rule abolished on 2026-08-12. Only four classes block now "
     "(config/ship_policy.v001.json)."),
    ("retired_tool",
     r"DaVinci|Midjourney|Runway",
     "names a tool retired by CLAUDE.md section 11 on 2026-06-20. In a live skill or agent "
     "description this is what the model is told to use."),
    ("animation_both_ways",
     r"animation_density[^\n]{0,40}(?:必須|mandatory)",
     "calls animation_density mandatory. It is a production requirement and an advisory "
     "gate: it never blocks a ship."),
]

# retired_tool only matters where a model reads it as an instruction, not in prose history.
LIVE_MENU_ONLY = {"retired_tool"}


def scan() -> list[tuple[str, Path, int, str, str]]:
    hits = []
    for f in binding_files():
        live_menu = ".claude" in str(f)
        try:
            lines = f.read_text(encoding="utf-8", errors="ignore").splitlines()
        except Exception:
            continue
        for i, ln in enumerate(lines, 1):
            if EXEMPT.search(ln):
                continue
            for rid, pat, why in RULES:
                if rid in LIVE_MENU_ONLY and not live_menu:
                    continue
                if re.search(pat, ln, re.I):
                    hits.append((rid, f, i, ln.strip()[:120], why))
    return hits


def broken_links() -> list[tuple[Path, int, str]]:
    """A pointer to a file that is not there. PD_CANON carried two for weeks."""
    out = []
    rx = re.compile(r"`((?:docs|config|schemas|scripts)/[A-Za-z0-9_./-]+\.(?:md|json|py|sh))`")
    for f in binding_files():
        try:
            lines = f.read_text(encoding="utf-8", errors="ignore").splitlines()
        except Exception:
            continue
        for i, ln in enumerate(lines, 1):
            for m in rx.finditer(ln):
                target = m.group(1)
                # `docs/handover/YYYY-MM-DD.md` is a template telling the reader what to name
                # a file, not a link to one. Three binding documents carry it on purpose.
                if re.search(r"YYYY|MM-DD|NNN|<[a-z_]+>|\bvNNN\b|\*", target):
                    continue
                if not (ROOT / target).exists():
                    out.append((f, i, target))
    return out


def report(hits, links) -> int:
    for rid, f, i, ln, why in hits:
        print(f"[{rid}] {f.relative_to(ROOT).as_posix()}:{i}\n    {ln}\n    -> {why}")
    for f, i, target in links:
        print(f"[broken_link] {f.relative_to(ROOT).as_posix()}:{i}\n    {target} does not exist")
    n = len(hits) + len(links)
    print(f"\n{n} contradiction(s) in {len(binding_files())} binding document(s)")
    if n == 0:
        print("The binding documents agree with each other.")
    return 1 if n else 0


def demo() -> int:
    """Prove the rules still bite, on text written to fail."""
    bad = "\n".join([
        "read `docs/PD_ONE_PASS_PRODUCTION_SPEC.v2.md` before touching anything",
        "- [ ] タイトル ≤60字・二人称",
        "the hook (~8 s) written last + promise-payoff verified",
        "標準は11.5分",
        "2. ハード不合格が `runtime_band`、**または**そのエピソードの",
        "animation_density は必須",
        "see `docs/THIS_FILE_DOES_NOT_EXIST.md`",
    ])
    tmp = Path(tempfile.mkdtemp()) / "bad.md"
    tmp.write_text(bad, encoding="utf-8")
    fired = set()
    for i, ln in enumerate(bad.splitlines(), 1):
        if EXEMPT.search(ln):
            continue
        for rid, pat, _ in RULES:
            if rid in LIVE_MENU_ONLY:
                continue
            if re.search(pat, ln, re.I):
                fired.add(rid)
                print(f"  caught [{rid}] line {i}: {ln[:70]}")
    expect = {"spec_version", "title_length", "hook_order", "runtime_default",
              "ship_rule", "animation_both_ways"}
    missing = expect - fired
    print(f"\nfired {len(fired)} of {len(expect)} rules")
    if missing:
        print(f"NOT CAUGHT: {sorted(missing)} -- these rules are decoration, fix them")
        return 1
    # and the exemption must work, or every corrected line becomes a permanent false alarm
    ok_line = "※ 2026-08-23 訂正：ここは長く「タイトル ≤60字」と書かれていた"
    if not EXEMPT.search(ok_line):
        print("NOT EXEMPT: a line that declares itself a correction still trips the rule")
        return 1
    print("every rule fires on bad input, and a line marked as a correction does not")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--demo", action="store_true",
                    help="run the rules against deliberately contradictory text")
    a = ap.parse_args()
    if a.demo:
        return demo()
    return report(scan(), broken_links())


if __name__ == "__main__":
    sys.exit(main())
