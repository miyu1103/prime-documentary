#!/usr/bin/env python3
"""Fix what can be fixed, record what was changed, and only then call a human.

WHY THIS EXISTS
---------------
The owner's complaint, 2026-08-23, and it is the right one:

    「毎回いろんなブレーキがかかるのがとても嫌で困ってる」

Measured the same day, that is exactly what the pipeline does. Of 34 finished episodes, **27
shipped with `preflight_receipt` red** -- and the reason is not that anything is wrong with
those films. It is that `preflight_render_gate.py` is **called from nowhere**: it appears zero
times in `scripts/_finish_episode.sh`. The receipt it wants has never been written, so the gate
that reads it goes red, every episode, forever, and a person has to look at that red and decide
to ignore it. Same story for `write_final_delivery.py`: zero calls, and `docs/HANDOVER.md` tells
the operator to run it "by hand".

That is a brake with nothing behind it. There is no decision to make and no defect to fix; a
step simply was never wired. This module wires them, and does it as a repair rather than as
another gate, because another gate is the last thing this repository needs.

THE SHAPE
---------
    detect -> repair what is repairable -> record exactly what changed -> continue
                                        -> stop and call a human ONLY for the rest

**Never auto-repaired**, under any circumstance: the four classes that can end the channel --
`real_person_likeness`, `rights_and_licence`, `factual_support`, `fabricated_record`
(`config/ship_policy.v001.json`). A machine must not quietly resolve a ban risk. Those stop.

WHAT IS DELIBERATELY NOT HERE YET
---------------------------------
The owner approved repairing the FILM ITSELF, not only the paperwork. Three obvious candidates
were measured and rejected for this first pass, rather than shipped as plausible guesses:

  * `padding` reads `06_audio/narration_index.v001.json`, not the film json. The dead air is
    between narration chunks, so "trim the gaps" would mean re-timing rendered audio.
  * `animation_mix` (紙芝居) is fixable by shortening long hero holds, but every cut is timed
    against the narration; shortening one requires redistributing the rest, and getting that
    wrong desynchronises the whole film.
  * `arc_nonrepeat` (素材被り) is a straight src swap that changes no timing at all -- except
    that hyatt is at 100% footage utilisation (232/232), so there is nothing to swap TO. It
    needs a spare-material step in front of it.

Each is a real repair and each needs its own evidence. Adding a rule is `Rule(...)` plus a
function; see `RULES`.

Usage:
    py -3.11 scripts/pd_autorepair.py --slug <slug>            # repair, then report
    py -3.11 scripts/pd_autorepair.py --slug <slug> --dry-run  # say what it would do
    py -3.11 scripts/pd_autorepair.py --list

Exit codes: 0 nothing left that needs a person, 2 a human is needed, 3 the episode is unknown.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

# The four classes a machine may never resolve on its own (config/ship_policy.v001.json).
NEVER_AUTO = {"visual_asset_qc", "onscreen_text_verified", "packaging_qc", "check_packaging_qc"}


@dataclass
class Repair:
    check: str
    done: bool
    what: str
    command: str | None = None


@dataclass
class Rule:
    check: str
    kind: str                      # "wiring" = runs a step nobody wired; "content" = edits the film
    why: str                       # what the red actually means, in one line
    run: Callable[[str, Path, bool], Repair]


def _run(cmd: list[str], dry: bool) -> tuple[bool, str]:
    if dry:
        return True, "(dry-run) " + " ".join(cmd)
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                       errors="replace", cwd=ROOT)
    tail = (p.stdout + p.stderr).strip().splitlines()
    return p.returncode == 0, (tail[-1] if tail else f"exit {p.returncode}")[:160]


def _epdir(slug: str) -> Path | None:
    hits = sorted(ROOT.glob(f"episodes/PD-2026-*-{slug}"))
    return hits[-1] if hits else None


# --------------------------------------------------------------------------- #
# rules
# --------------------------------------------------------------------------- #
def _repair_preflight_receipt(slug: str, epdir: Path, dry: bool) -> Repair:
    """Run the gate that writes 04_scenes/preflight_receipt.v*.json. Nobody ever wired it.

    27 of 34 finished episodes are red on this and not one of them has the receipt on disk.
    """
    cmd = ["py", "-3.11", str(ROOT / "scripts/preflight_render_gate.py"), "--ep", epdir.name]
    ok, msg = _run(cmd, dry)
    made = sorted((epdir / "04_scenes").glob("preflight_receipt.v*.json"))
    if dry:
        return Repair("preflight_receipt", done=False, what="WOULD RUN: " + " ".join(cmd),
                      command=" ".join(cmd))
    return Repair("preflight_receipt", done=bool(made),
                  what=(f"wrote {made[-1].name}" if made else f"ran but wrote no receipt: {msg}"),
                  command=" ".join(cmd))


def _repair_final_delivery(slug: str, epdir: Path, dry: bool) -> Repair:
    """Write 09_package/final_delivery.v*.json. HANDOVER says to do this by hand."""
    cmd = ["py", "-3.11", str(ROOT / "scripts/write_final_delivery.py"), "--slug", slug]
    ok, msg = _run(cmd, dry)
    made = sorted((epdir / "09_package").glob("final_delivery.v*.json"))
    if dry:
        return Repair("final_delivery", done=False, what="WOULD RUN: " + " ".join(cmd),
                      command=" ".join(cmd))
    return Repair("final_delivery", done=bool(made),
                  what=(f"wrote {made[-1].name}" if made else msg), command=" ".join(cmd))


RULES: list[Rule] = [
    Rule("preflight_receipt", "wiring",
         "the receipt is missing because preflight_render_gate.py is called from nowhere",
         _repair_preflight_receipt),
    Rule("final_delivery", "wiring",
         "HANDOVER tells a person to run write_final_delivery.py by hand",
         _repair_final_delivery),
]
BY_CHECK = {r.check: r for r in RULES}


# --------------------------------------------------------------------------- #
def failing_checks(slug: str) -> tuple[list[str], str]:
    """What the pre-render forecast says will fail. No GPU, no network."""
    try:
        from predict_acceptance import forecast
    except Exception as exc:                       # noqa: BLE001
        return [], f"forecast unavailable ({type(exc).__name__}: {exc})"
    try:
        f = forecast(slug)
    except Exception as exc:                       # noqa: BLE001
        return [], f"forecast failed ({type(exc).__name__}: {exc})"
    return [c["check"] for c in f["checks"] if c["verdict"] == "WILL FAIL"], ""


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--list", action="store_true", help="what can be repaired automatically")
    a = ap.parse_args()

    if a.list:
        for r in RULES:
            print(f"{r.check:<22} [{r.kind}] {r.why}")
        print(f"\nnever repaired automatically (ban risk): {', '.join(sorted(NEVER_AUTO))}")
        return 0
    if not a.slug:
        ap.error("--slug is required unless --list")

    epdir = _epdir(a.slug)
    if epdir is None:
        print(f"no episode directory for slug {a.slug!r}", file=sys.stderr)
        return 3

    failing, err = failing_checks(a.slug)
    if err:
        print(f"[autorepair] {a.slug}: {err}", file=sys.stderr)
        return 2

    # A missing receipt does not always reach the forecast as a WILL FAIL; a wiring rule whose
    # artifact is simply absent is repairable regardless of what the forecast says about it.
    targets = list(failing)
    for r in RULES:
        if r.kind == "wiring" and r.check not in targets:
            if r.check == "preflight_receipt" and not sorted((epdir / "04_scenes").glob("preflight_receipt.v*.json")):
                targets.append(r.check)
            if r.check == "final_delivery" and not sorted((epdir / "09_package").glob("final_delivery.v*.json")):
                targets.append(r.check)

    repairs: list[Repair] = []
    needs_human: list[str] = []
    for check in targets:
        if check in NEVER_AUTO:
            needs_human.append(f"{check} (ban-risk class -- a machine must not resolve this)")
            continue
        rule = BY_CHECK.get(check)
        if rule is None:
            needs_human.append(f"{check} (no repair rule yet)")
            continue
        repairs.append(rule.run(a.slug, epdir, a.dry_run))

    print(f"=== autorepair {a.slug} ===")
    for r in repairs:
        tag = "WOULD " if a.dry_run else ("FIXED " if r.done else "FAILED")
        print(f"  {tag} {r.check:<20} {r.what}")
    for n in needs_human:
        print(f"  CALL   {n}")
    if not repairs and not needs_human:
        print("  nothing to repair")

    record = {
        "schema_version": "1.0.0", "tool": "pd_autorepair.py", "slug": a.slug,
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "dry_run": a.dry_run,
        "forecast_will_fail": failing,
        "repaired": [{"check": r.check, "done": r.done, "what": r.what, "command": r.command}
                     for r in repairs],
        "needs_human": needs_human,
    }
    if not a.dry_run:
        out = epdir / "09_package" / "autorepair.v001.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(record, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"\n  recorded -> {out.relative_to(ROOT)}")

    if needs_human:
        print(f"\n  {len(needs_human)} item(s) a machine cannot fix. This is the stop that is "
              f"worth stopping for.")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
