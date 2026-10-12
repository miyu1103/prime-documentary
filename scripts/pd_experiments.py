#!/usr/bin/env python3
"""The running-experiment register: read it, and refuse writes that would destroy one.

WHY THIS EXISTS
---------------
On 2026-08-12 a repackaging instruction was written that would have retitled 6 of the 13
control videos of a live experiment. Nothing mechanical could have stopped it -- the control
list existed only inside the prose of a receipt. One agent happened to read that receipt.

`schemas/experiment.schema.json` had existed since before that night with no data behind it.
A schema with no instance is decoration. `config/pd_experiments.v001.json` is the instance,
and this module is the only code that reads it, so there is one definition of "locked".

WHAT IT GUARANTEES, AND WHAT IT DOES NOT
----------------------------------------
It can prove: this video id is inside an arm of an experiment whose read date has not passed,
for this kind of mutation. That is all. It does not know whether a change is a good idea, and
it cannot see a mutation made by hand in the Studio UI.

Usage:
    py -3.11 scripts/pd_experiments.py                        # what is running, what is due
    py -3.11 scripts/pd_experiments.py --locks title          # every id locked against retitling
    py -3.11 scripts/pd_experiments.py --check ID [ID ...] --kind title
    py -3.11 scripts/pd_experiments.py --validate             # every entry against the schema

Exit codes: 0 clear, 2 at least one id is locked (or an entry is invalid under --validate).
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTER = ROOT / "config" / "pd_experiments.v001.json"
SCHEMA = ROOT / "schemas" / "experiment.schema.json"
JST = dt.timezone(dt.timedelta(hours=9))
KINDS = ("title", "thumbnail", "description")


def load() -> dict:
    return json.loads(REGISTER.read_text(encoding="utf-8"))


def today() -> dt.date:
    return dt.datetime.now(JST).date()


def _arm_ids(exp: dict, arm: str) -> set[str]:
    """Ids of one arm. An arm either lists them or names the file they were written from.

    Deliberately not duplicated into the register: TITLE_APPLY_39.applied.v001.json is the
    record the write actually produced, so it cannot drift from what was written.
    """
    spec = (exp.get("arms") or {}).get(arm) or {}
    if spec.get("video_ids"):
        return set(spec["video_ids"])
    src = spec.get("derived_from")
    if not src:
        return set()
    p = ROOT / src
    if not p.exists():
        print(f"WARN {exp['experiment_id']}: arm {arm} derives from {src}, which is missing",
              file=sys.stderr)
        return set()
    d = json.loads(p.read_text(encoding="utf-8"))
    rows = d["videos"] if isinstance(d, dict) and "videos" in d else d
    return {r["video_id"] for r in rows if isinstance(r, dict) and r.get("video_id")}


def locks(kind: str, on: dt.date | None = None) -> dict[str, list[str]]:
    """video_id -> the reasons it may not be mutated in this way today."""
    on = on or today()
    out: dict[str, list[str]] = {}
    for exp in load()["experiments"]:
        if exp.get("status") not in ("active", "planned"):
            continue
        rule = (exp.get("locked_video_ids") or {}).get(kind)
        if not rule:
            continue
        until = rule.get("until")
        if until and dt.date.fromisoformat(until) <= on:
            continue                      # the lock has expired; the experiment can be read
        ids: set[str] = set(rule.get("video_ids") or [])
        for arm in rule.get("ids_from_arm") or []:
            ids |= _arm_ids(exp, arm)
        for vid in ids:
            out.setdefault(vid, []).append(
                f"{exp['experiment_id']} ({rule.get('reason', 'locked')}) until {until or 'read'}")
    return out


def assert_unlocked(video_ids, kind: str) -> None:
    """Raise before the first write. Callers should invoke this, not re-implement it."""
    lk = locks(kind)
    hit = {v: lk[v] for v in video_ids if v in lk}
    if hit:
        lines = "\n".join(f"  {v}: {'; '.join(r)}" for v, r in sorted(hit.items()))
        raise SystemExit(
            f"REFUSING: {len(hit)} target(s) are locked by a running experiment ({kind}).\n"
            f"{lines}\n"
            f"Register: {REGISTER.relative_to(ROOT)}. Changing these destroys the comparison.")


def due(on: dt.date | None = None) -> list[dict]:
    on = on or today()
    out = []
    for exp in load()["experiments"]:
        r = exp.get("read_on")
        if exp.get("status") in ("completed", "cancelled") or not r:
            continue
        try:
            if dt.date.fromisoformat(r) <= on:
                out.append(exp)
        except ValueError:
            pass                          # e.g. "publish_of_fifth + 28 days" -- not a date yet
    return out


def validate() -> int:
    try:
        import jsonschema                 # noqa: F401
    except ImportError:
        print("jsonschema not installed -- structural check only")
        bad = 0
        req = ("experiment_id", "hypothesis", "change", "primary_metric",
               "start_condition", "stop_condition", "status")
        for exp in load()["experiments"]:
            miss = [k for k in req if k not in exp]
            if miss:
                bad += 1
                print(f"FAIL {exp.get('experiment_id', '?')}: missing {miss}")
        print("OK" if not bad else f"{bad} invalid")
        return 2 if bad else 0
    import jsonschema
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    bad = 0
    for exp in load()["experiments"]:
        try:
            jsonschema.validate(exp, schema)
            print(f"OK   {exp['experiment_id']}")
        except jsonschema.ValidationError as e:
            bad += 1
            print(f"FAIL {exp.get('experiment_id', '?')}: {e.message}")
    return 2 if bad else 0


def report() -> int:
    d = load()
    now = today()
    print(f"=== experiments — {now} (register {REGISTER.relative_to(ROOT)} v{d['version']}) ===\n")
    for exp in d["experiments"]:
        r = exp.get("read_on", "-")
        try:
            days = (dt.date.fromisoformat(r) - now).days
            when = f"{r} (in {days} d)" if days >= 0 else f"{r} (DUE {-days} d ago)"
        except ValueError:
            when = r
        print(f"[{exp['status']:<9}] {exp['experiment_id']}")
        print(f"            {exp.get('owner_visible_name', '')}")
        print(f"            read: {when}")
        for v in exp.get("verdicts", []):
            print(f"              {v['verdict']:<9} if {v['when']}")
        print()
    for kind in KINDS:
        lk = locks(kind)
        if lk:
            print(f"LOCKED against {kind} change: {len(lk)} video id(s)")
    print("\n  py -3.11 scripts/pd_experiments.py --locks title    # list them")
    dues = due()
    if dues:
        print("\n!! DUE NOW: " + ", ".join(e["experiment_id"] for e in dues))
    for s in d.get("stopped", []):
        print(f"\nSTOPPED {s['what']} ({s['decided_at']}): {s['measurement'][:90]}")
    return 0


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--locks", choices=KINDS, help="list every id locked against this mutation")
    ap.add_argument("--check", nargs="+", metavar="ID", help="exit 2 if any id is locked")
    ap.add_argument("--kind", choices=KINDS, default="title")
    ap.add_argument("--validate", action="store_true")
    a = ap.parse_args()

    if a.validate:
        return validate()
    if a.locks:
        lk = locks(a.locks)
        for vid, reasons in sorted(lk.items()):
            print(f"{vid}  {'; '.join(reasons)}")
        print(f"\n{len(lk)} locked against {a.locks} change")
        return 0
    if a.check:
        try:
            assert_unlocked(a.check, a.kind)
        except SystemExit as e:
            print(e, file=sys.stderr)
            return 2
        print(f"clear: none of {len(a.check)} id(s) is locked against {a.kind} change")
        return 0
    return report()


if __name__ == "__main__":
    raise SystemExit(main())
