#!/usr/bin/env python3
"""Feed every gate an input it MUST reject, and fail if it does not.

WHY THIS EXISTS
---------------
On 2026-08-23 a gate did not break. It stopped applying.

`check_final_acceptance.check_freshness` carries the only signal that can see a master built
before the render it claims to contain -- the failure that would stamp a green receipt on a
different film. It was gated on the literal name `<slug>_final_bgm.v001.mp4`. Seven shipped
episodes were graded on v002, and on every one of them the signal did not run, did not fail,
and did not warn. Nothing was red. Nothing was missing. The check was simply absent, and no
test noticed, because every test asked "does the good input pass?" and none asked
"does the bad input still fail?"

That is the shape of this whole class of defect, and it is why `docs/HANDOVER.md` permanent
rule 5 says a check that has never been shown to fail is decoration. This file turns that rule
into something that runs.

WHAT IT IS NOT
--------------
Not a test of whether the films are good. Not a replacement for the gates. It asks one question
of each gate -- "can you still bite?" -- and it costs no GPU, no network and no quota, so it can
run before every render and inside the ordinary test suite.

HOW TO ADD ONE
--------------
Write a `Probe`: build a deliberately bad input, run the real gate on it, and say what a
correct rejection looks like. If your probe passes on the FIRST run, you have not made the
input bad enough -- check that before trusting it.

Usage:
    py -3.11 scripts/check_gates_still_bite.py            # all probes
    py -3.11 scripts/check_gates_still_bite.py --list
    py -3.11 scripts/check_gates_still_bite.py --only freshness_mux_order

Exit codes: 0 every gate still bites, 1 at least one has stopped biting.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))


@dataclass
class Result:
    bit: bool          # did the gate reject the bad input?
    detail: str        # what it actually said


@dataclass
class Probe:
    name: str
    guards: str        # the real failure this gate exists to catch
    run: Callable[[], Result]


def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


# --------------------------------------------------------------------------- #
# probes
# --------------------------------------------------------------------------- #
def _probe_freshness_mux_order() -> Result:
    """A master OLDER than the render it should contain, named v002.

    The real event: correa finished its render, then `_finish_episode.sh` died before step 7,
    so the 08_edit master was a build from three days earlier. Every other freshness signal
    passes on it. Named v002 deliberately: that is the version the check used to ignore.
    """
    import check_final_acceptance as cfa
    tmp = Path(tempfile.mkdtemp())
    old_root = cfa.ROOT
    try:
        cfa.ROOT = tmp
        (tmp / "out").mkdir()
        ep = tmp / "episodes" / "PD-2026-099-probe"
        (ep / "08_edit").mkdir(parents=True)
        (ep / "09_package").mkdir(parents=True)
        master = ep / "08_edit" / "probe_final_bgm.v002.mp4"
        master.write_bytes(b"a master that predates its own render")
        os.utime(master, (900_000, 900_000))
        raw = tmp / "out" / "probe.mp4"
        raw.write_bytes(b"the render")
        os.utime(raw, (1_000_000, 1_000_000))
        r = cfa.check_freshness(ep, master, "a" * 64, None)
        return Result(bit=not r["ok"], detail=str(r.get("reason", ""))[:150])
    finally:
        cfa.ROOT = old_root
        shutil.rmtree(tmp, ignore_errors=True)


def _probe_episode_is_done() -> Result:
    """A master on disk that is NOT the film the receipt accepted.

    mtime says done. Filename says done. Only the bytes say otherwise.
    """
    import episode_is_done as eid
    tmp = Path(tempfile.mkdtemp())
    old_root = eid.ROOT
    try:
        eid.ROOT = tmp
        ep = tmp / "episodes" / "PD-2026-099-probe"
        (ep / "08_edit").mkdir(parents=True)
        (ep / "09_package").mkdir(parents=True)
        (ep / "08_edit" / "probe_final_bgm.v002.mp4").write_bytes(b"some other film")
        (ep / "09_package" / "acceptance_receipt.v001.json").write_text(
            json.dumps({"video_sha256": f"sha256:{_sha(b'the accepted film')}"}), encoding="utf-8")
        rc, why = eid.verdict("probe")
        return Result(bit=rc != eid.DONE, detail=why[:150])
    finally:
        eid.ROOT = old_root
        shutil.rmtree(tmp, ignore_errors=True)


def _probe_decision_expiry() -> Result:
    """A decision that outlived its own review date and is still marked Accepted."""
    import check_decisions as cd
    tmp = Path(tempfile.mkdtemp())
    old_dir = cd.DECISIONS
    try:
        cd.DECISIONS = tmp
        (tmp / "0099.md").write_text(
            "# ADR-0099\n\n**Status:** Accepted (2026-01-01)\n"
            "**Review by:** 2026-01-02\n**Revoke if:** CTR stays under 2.0%\n", encoding="utf-8")
        states = [r["state"] for r in cd.scan()]
        return Result(bit="EXPIRED" in states, detail=f"states={states}")
    finally:
        cd.DECISIONS = old_dir
        shutil.rmtree(tmp, ignore_errors=True)


def _probe_experiment_lock() -> Result:
    """A retitle aimed at a control video of a live experiment.

    The real event: on 2026-08-12 a proposed batch would have retitled 6 of the 13 controls.
    Skipped, not failed, once every experiment has been read -- there is nothing left to guard.
    """
    import pd_experiments as px
    locked = px.locks("title")
    if not locked:
        return Result(bit=True, detail="no experiment is running; nothing to guard (not a failure)")
    victim = sorted(locked)[0]
    try:
        px.assert_unlocked([victim], "title")
        return Result(bit=False, detail=f"{victim} is listed as locked but the guard let it pass")
    except SystemExit as exc:
        return Result(bit=True, detail=str(exc).splitlines()[0][:150])


def _probe_doc_contradictions() -> Result:
    """The binding documents disagreeing with each other. That checker ships its own --demo."""
    # PYTHONIOENCODING is not optional here. Without it the child prints its report through
    # the Windows cp932 console codec, dies on a "<=" it wrote itself, and this probe reports
    # ASLEEP for a gate that is perfectly healthy. Measured 2026-08-23: the first run of this
    # file raised a false alarm exactly that way. A probe that lies is worse than no probe.
    env = {**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1"}
    r = subprocess.run(["py", "-3.11", str(ROOT / "scripts/check_doc_contradictions.py"), "--demo"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace",
                       cwd=ROOT, env=env)
    out = (r.stdout + r.stderr).strip().splitlines()
    return Result(bit=r.returncode == 0, detail=(out[-1] if out else "")[:150])


def _probe_pd_edit_reverts() -> Result:
    """An edit that breaks the file must be put back, not left half-applied.

    Every long failure in the EP50-59 run had one shape: exit 0, nothing changed. pd_edit is
    the answer to it, so it has to keep working.
    """
    tmp = Path(tempfile.mkdtemp())
    try:
        f = tmp / "probe.py"
        original = "x = 1\ny = 2\n"
        f.write_text(original, encoding="utf-8")
        subprocess.run(["py", "-3.11", str(ROOT / "scripts/pd_edit.py"),
                        "--file", str(f), "--old", "y = 2", "--new", "y = ("],
                       capture_output=True, text=True, cwd=ROOT)
        back = f.read_text(encoding="utf-8")
        return Result(bit=back == original,
                      detail="file restored" if back == original else f"LEFT BROKEN: {back!r}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# --------------------------------------------------------------------------- #
# vacuous passes
# --------------------------------------------------------------------------- #
# A gate handed an EMPTY episode should not answer "ok". Ten of them currently do, each with a
# reason of the form "nothing here to check". Measured 2026-08-23 against all 161 acceptance
# receipts on disk: not one of those branches has ever fired on a real episode, so nothing has
# shipped through them and NO VERDICT IS BEING CHANGED HERE -- changing ten gates from pass to
# fail could stop the line over a path rename, which is a worse defect than the one it fixes.
#
# What is guarded is GROWTH. Today's bug was a gate that quietly stopped applying; a gate that
# passes because its input moved is the same failure with a different cause. This baseline
# freezes the ten that already do it. An eleventh makes the probe fire, and whoever added it has
# to say so out loud instead of it becoming normal.
VACUOUS_BASELINE = {
    "check_bookends",                 # no composition matching slug
    "check_caption_format",           # no final .srt to format-check
    "check_caption_narration_match",  # no narration spoken_text and/or final .srt
    "check_caption_sync",             # SRT not found
    "check_footage_diversity",        # no film-data cutlist
    "check_hook",                     # shotlist totals missing
    "check_image_resolution",         # no hero PNGs staged
    "check_leveled_animation",        # no composition matching slug
    "check_structure",                # no narration sections
    "check_thumbnail_visibility",     # no selected thumbnail to measure
}


def vacuous_passes() -> set[str]:
    """Gate functions that return ok=True when handed an episode directory with nothing in it."""
    import inspect
    import check_final_acceptance as cfa
    tmp = Path(tempfile.mkdtemp())
    try:
        ep = tmp / "episodes" / "PD-2026-099-probe"
        (ep / "09_package").mkdir(parents=True)
        (ep / "08_edit").mkdir(parents=True)
        out = set()
        for name, fn in sorted(vars(cfa).items()):
            if not (name.startswith("check_") and inspect.isfunction(fn)):
                continue
            sig = inspect.signature(fn)
            params = list(sig.parameters)
            if params[:1] != ["epdir"]:
                continue                       # needs a real mp4; not probeable this cheaply
            kwargs, usable = {}, True
            for p in params[1:]:
                if sig.parameters[p].default is inspect.Parameter.empty:
                    if "dur" in p:
                        kwargs[p] = 700.0
                    else:
                        usable = False
                        break
            if not usable:
                continue
            try:
                if fn(ep, **kwargs).get("ok"):
                    out.add(name)
            except Exception:
                pass                            # raising on an empty episode is a rejection
        return out
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def _probe_no_new_vacuous_passes() -> Result:
    now = vacuous_passes()
    added = sorted(now - VACUOUS_BASELINE)
    healed = sorted(VACUOUS_BASELINE - now)
    if added:
        return Result(bit=False, detail="now passes an EMPTY episode: " + ", ".join(added))
    if healed:
        return Result(bit=True, detail="fixed since the baseline (remove from it): "
                                       + ", ".join(healed))
    return Result(bit=True, detail=f"{len(now)} known, none added")


PROBES = [
    Probe("no_new_vacuous_passes",
          "a gate passing because its input moved, exactly as today’s gate stopped applying",
          _probe_no_new_vacuous_passes),
    Probe("freshness_mux_order", "a receipt stamped green on a film the master does not contain",
          _probe_freshness_mux_order),
    Probe("episode_is_done", "rebuilding a finished film, or silently skipping an unfinished one",
          _probe_episode_is_done),
    Probe("decision_expiry", "a decision binding forever after its own review date passed",
          _probe_decision_expiry),
    Probe("experiment_lock", "a retitle destroying the control arm of a running experiment",
          _probe_experiment_lock),
    Probe("doc_contradictions", "two binding documents answering the same question differently",
          _probe_doc_contradictions),
    Probe("pd_edit_reverts", "an edit that exits 0 having left the file broken or unchanged",
          _probe_pd_edit_reverts),
]


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="run one probe by name")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()

    if a.list:
        for p in PROBES:
            print(f"{p.name:<22} guards against: {p.guards}")
        return 0

    probes = [p for p in PROBES if not a.only or p.name == a.only]
    if not probes:
        print(f"no probe named {a.only!r}", file=sys.stderr)
        return 1

    print(f"=== gates still bite? — {dt.datetime.now():%Y-%m-%d %H:%M} ===")
    print("Each gate is handed an input it MUST reject.\n")
    dead = []
    for p in probes:
        try:
            r = p.run()
        except Exception as exc:                       # a probe that crashes is a failure
            r = Result(bit=False, detail=f"probe raised {type(exc).__name__}: {exc}")
        print(f"{'BITES ' if r.bit else 'ASLEEP'}  {p.name:<22} {r.detail}")
        if not r.bit:
            dead.append(p)

    print()
    if dead:
        print(f"{len(dead)} gate(s) have STOPPED BITING. Each one now lets through:")
        for p in dead:
            print(f"  {p.name}: {p.guards}")
        print("\nThis is not a style problem. Do not render or ship until it is understood.")
        return 1
    print(f"all {len(probes)} gate(s) still reject the input they exist to reject")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
