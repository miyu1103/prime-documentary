#!/usr/bin/env python3
"""Decide, from an acceptance receipt, whether a finished episode may be scheduled.

WHY THIS EXISTS. Five days produced zero scheduled uploads. Of the seven reasons raised on the
night of 2026-08-11, one was a genuine risk (an identifiable real minor in frame) and six were
craft rules -- a real legislative chamber, a Turkish exit sign, a stock clock, shared footage, a
mix revision, an asset count, a 0.3-second still-frame overrun. `config/ship_policy.v001.json`
is the owner's answer: block on ban and legal risk, not on taste.

WHAT THIS DOES NOT DO. It does not change a single measurement. `check_final_acceptance.py`
still runs every check, still computes every number, and still writes every failure into the
receipt. This module reads that receipt and decides which failures hold the door shut. The
decision moved; the measurement did not. Anything that does not block is written to
`episodes/<EPID>/09_package/release_deviations.v001.json` with its number -- that record is the
whole reason this is not "ship anything".

    python scripts/pd_ship_policy.py --slug marmet                  # explain the real decision
    python scripts/pd_ship_policy.py --slug x --receipt r.json      # explain any receipt

Exit 0 = may ship. Exit 1 = refused, and the refusal names the blocking class. Read-only except
for the release record, which is written only when the caller asks for it.
"""
from __future__ import annotations

import argparse
import importlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
POLICY_PATH = ROOT / "config" / "ship_policy.v001.json"
FILM_DIR = ROOT / "remotion" / "src" / "data"

# Check id -> the sibling gate module whose evaluate(epdir) produced it.
#
# ONLY file-only gates are listed. Every one of these reads json/markdown/png and returns in
# well under a second; none of them decodes the render. The three that DO shell out to ffmpeg
# (visual_asset_qc, encoder_settings, image_cut_luma) are deliberately absent -- re-measuring
# them at schedule time would mean minutes of decode on a machine that is usually rendering,
# and their rows are written honestly as "measured value unavailable" instead.
REEVALUABLE: dict[str, str] = {
    "asset_reuse": "check_asset_reuse",
    "animation_mix": "check_animation_mix",
    "caption_breaks": "check_caption_breaks",
    "caption_coverage": "verify_caption_coverage",
    "caption_integrity": "check_caption_integrity",
    "footage_utilization": "check_footage_utilization",
    "motion_density": "check_motion_density",
    "onscreen_text_verified": "verify_onscreen_text",
    "packaging_qc": "check_packaging_qc",
    "padding": "check_padding",
    "retention_cadence": "check_retention_cadence",
    "script_craft": "check_script_craft",
    "script_length": "check_script_length",
    "script_lint": "verify_script_lint",
    "script_structure": "verify_script_structure",
    "thumb_subject_luma": "check_thumb_subject_luma",
}

# The same, for the checks check_final_acceptance implements ITSELF. Value = (function name,
# extra positional args). Only functions that read files are here; everything that ffprobes or
# decodes the render (animation_density, sound_layers, loudness, bgm_*, body_luma, motion_*)
# is absent on purpose and its rows say so.
ACC_REEVALUABLE: dict[str, tuple[str, tuple]] = {
    "voice_is_master": ("check_voice", ()),
    "captions_final": ("check_captions", (None,)),
    "caption_format": ("check_caption_format", ()),
    "caption_narration_match": ("check_caption_narration_match", ()),
    "caption_sync": ("check_caption_sync", ()),
    "structure_4part": ("check_structure", ()),
    "op_ed_bookends": ("check_bookends", ()),
    "leveled_animation": ("check_leveled_animation", ()),
    "preflight_receipt": ("check_preflight_receipt", ()),
    "probe_receipt": ("check_probe_receipt", ()),
    "thumbnail_ready": ("check_thumbnail", ()),
    "thumbnail_visibility": ("check_thumbnail_visibility", ()),
    "image_resolution": ("check_image_resolution", ()),
    "footage_diversity": ("check_footage_diversity", ()),
}

# Checks whose value COULD be recovered, but not for the price. Measured: re-running
# arc_nonrepeat on norfolk hashed 2.5 GB to answer a question the receipt already answered.
# The row is written either way; it says this instead of pretending the value does not exist.
EXPENSIVE: dict[str, str] = {
    "arc_nonrepeat": "re-running it re-fingerprints the whole prior-episode asset universe "
                     "(gigabytes of hashing) to restate a number the receipt already decided",
    "visual_asset_qc": "it shells out to ffmpeg over the staged clip pool",
    "image_cut_luma": "it decodes the render frame by frame",
    "encoder_settings": "it ffprobes the render",
}

_RESULT_KEYS = {"check", "ok", "hard", "skipped", "reason", "problems", "notes"}
_THRESHOLD_PREFIXES = ("min_", "max_", "limit", "floor", "ceiling", "required", "need",
                       "target", "threshold", "band", "allowed", "cap_")


# --------------------------------------------------------------------------- policy loading

def load_policy(path: Path | None = None) -> dict:
    """Read the owner's policy. A missing or unreadable policy is fatal, never a default."""
    p = path or POLICY_PATH
    try:
        pol = json.loads(p.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(f"cannot read ship policy {p}: {exc}") from exc
    if "machine_contract" not in pol:
        raise RuntimeError(f"{p} carries no machine_contract block; nothing can be enforced "
                           f"from prose alone")
    return pol


def _repo_path(p: Path | str | None) -> str | None:
    """Repo-relative when it can be, and never an exception on a path from elsewhere."""
    if p is None:
        return None
    try:
        return Path(p).resolve().relative_to(ROOT).as_posix()
    except Exception:  # noqa: BLE001
        return str(p)


def blocking_class_ids(policy: dict) -> list[str]:
    return [b["id"] for b in policy.get("blocking", []) if b.get("id")]


# --------------------------------------------------------------------------- re-measurement

def _scalars(d: dict) -> tuple[dict, dict]:
    """Split a gate's own result dict into what it measured and what it measured against."""
    measured, thresholds = {}, {}
    for k, v in d.items():
        if k in _RESULT_KEYS or k.startswith("_"):
            continue
        if isinstance(v, bool) or isinstance(v, (int, float)):
            pass
        elif isinstance(v, str):
            # an absolute path is provenance, not a measurement, and it is already implied by
            # the episode id -- keep the record readable
            if len(v) > 200 or "/" in v or "\\" in v:
                continue
        elif isinstance(v, list) and 0 < len(v) <= 8 and all(
                isinstance(x, (str, int, float)) for x in v):
            v = list(v)
        else:
            continue
        (thresholds if k.lower().startswith(_THRESHOLD_PREFIXES) else measured)[k] = v
    return measured, thresholds


def reevaluate(check_id: str, epdir: Path) -> dict | None:
    """Re-run a file-only gate to recover the NUMBER behind a receipt's pass/fail bit.

    The receipt records `{"padding": false}` and nothing else -- no measured value, no
    threshold. Re-running the gate's own evaluate() is the only way to put a number on the
    release record without re-running the two-hour media gate, and it uses the gate's own code,
    so there is no second implementation of any measurement here.
    """
    if str(SCRIPTS) not in sys.path:
        sys.path.insert(0, str(SCRIPTS))
    mod_name = REEVALUABLE.get(check_id)
    if mod_name:
        try:
            mod = importlib.import_module(mod_name)
            r = mod.evaluate(epdir)
            return r if isinstance(r, dict) else None
        except Exception as exc:  # noqa: BLE001
            return {"check": check_id,
                    "_error": f"{mod_name}.evaluate raised {type(exc).__name__}: {exc}"}
    if check_id in ACC_REEVALUABLE:
        fn_name, extra = ACC_REEVALUABLE[check_id]
        try:
            acc = importlib.import_module("check_final_acceptance")
            r = getattr(acc, fn_name)(epdir, *extra)
            return r if isinstance(r, dict) else None
        except Exception as exc:  # noqa: BLE001
            return {"check": check_id,
                    "_error": f"check_final_acceptance.{fn_name} raised "
                              f"{type(exc).__name__}: {exc}"}
    return None


# --------------------------------------------------------------------------- classification

def _advisory_row(check: str, mc: dict, reeval: dict | None, receipt: dict) -> dict:
    group = mc["advisory_checks"].get(check, "unclassified")
    why = mc["advisory_groups"].get(group, mc["advisory_groups"]["unclassified"])
    row = {"check": check, "class": "advisory", "advisory_group": group,
           "why_it_did_not_block": f"advisory under config/ship_policy.v001.json: {why}",
           "backlog": group not in ("process_receipt", "measurement_gap")}
    return _attach_measurement(row, check, reeval, receipt)


def _attach_measurement(row: dict, check: str, reeval: dict | None, receipt: dict) -> dict:
    """Put the number on the row, or say plainly why there is no number."""
    # 1. the receipt's own embedded detail (today: motion_energy, and only that)
    if check == "motion_energy" and isinstance(receipt.get("motion_energy"), dict):
        me = dict(receipt["motion_energy"])
        row["measured"] = {k: me[k] for k in ("body_mean", "body_p10", "body_p50") if k in me}
        row["threshold"] = {k: me[k] for k in ("min_mean", "min_p10") if k in me}
        row["measured_source"] = "receipt"
        row["measured_unavailable"] = None
        return row
    # 2. the gate's own evaluate(), re-run on files only
    if reeval is not None and not reeval.get("_error"):
        measured, thresholds = _scalars(reeval)
        row["measured"] = measured or None
        row["threshold"] = thresholds or None
        row["detail"] = str(reeval.get("reason", ""))[:600] or None
        row["measured_source"] = "reevaluated"
        row["measured_unavailable"] = None
        if reeval.get("skipped"):
            row["measured_unavailable"] = ("the gate skipped on re-run (its inputs are not in "
                                           "the repo), so the value behind the receipt's FAIL "
                                           "could not be recovered")
        elif bool(reeval.get("ok")) is True:
            row["reevaluation_disagrees"] = ("the receipt records this check as FAILED on the "
                                             "shipped bytes; re-run now it PASSES. The receipt "
                                             "is the record of the render -- this row stands.")
        return row
    # 3. nothing cheap can produce it
    row["measured"] = None
    row["threshold"] = None
    row["measured_source"] = "unavailable"
    if reeval is not None and reeval.get("_error"):
        row["measured_unavailable"] = (f"re-evaluation failed: {reeval['_error']}")
    elif check in EXPENSIVE:
        row["measured_unavailable"] = (
            f"the receipt records this check as a pass/fail bit and not its measured value, and "
            f"it is not re-run at schedule time because {EXPENSIVE[check]}. Re-run "
            f"`check_final_acceptance.py <ep> --render <mp4> --json` to see the number.")
    else:
        row["measured_unavailable"] = (
            "the acceptance receipt records this check as a pass/fail bit and not its measured "
            "value, and the gate needs the render to measure it (ffmpeg decode), which is not "
            "re-run at schedule time. Re-run "
            "`check_final_acceptance.py <ep> --render <mp4> --json` to see the number.")
    return row


def classify_hard_failure(check: str, mc: dict, epdir: Path, receipt: dict) -> dict:
    """One receipt hard-failure -> one row that either blocks or does not, with its number."""
    reeval = reevaluate(check, epdir)

    split = mc.get("split_checks", {}).get(check)
    if split:
        return _classify_split(check, split, mc, reeval, receipt)

    if check in mc.get("blocking_checks", {}):
        cls = mc["blocking_checks"][check]
        row = {"check": check, "class": cls, "blocking": True,
               "why_it_blocks": f"{check} measures {cls}, one of the four blocking classes"}
        return _attach_measurement(row, check, reeval, receipt)

    return _advisory_row(check, mc, reeval, receipt)


def _classify_split(check: str, split: dict, mc: dict, reeval: dict | None,
                    receipt: dict) -> dict:
    """A MIXED check: the id alone cannot say whether the failure was risk or taste.

    Fails closed. If the sub-condition cannot be read, the whole check blocks -- this is the one
    place where erring toward blocking is right, because a real risk hides inside an id that
    also carries craft complaints.
    """
    cls = split["class"]
    if reeval is None or reeval.get("_error"):
        row = {"check": check, "class": cls, "blocking": True,
               "why_it_blocks": (f"{check} mixes craft and {cls}; its failing sub-condition "
                                 f"could not be read at schedule time, so it blocks (fail "
                                 f"closed). {split.get('why', '')}")}
        return _attach_measurement(row, check, reeval, receipt)

    reason = str(reeval.get("reason", ""))
    blocked = False
    if "blocking_when_reason_matches" in split:
        if reeval.get("skipped") or bool(reeval.get("ok")):
            # The receipt says this FAILED on the shipped bytes; re-run, the gate no longer
            # says why. The failing sub-condition is unreadable, so it blocks.
            blocked = True
            reason = (f"the receipt records a FAIL that the gate no longer reproduces "
                      f"({'skipped' if reeval.get('skipped') else 'passes now'}), so its failing "
                      f"sub-condition cannot be read | {reason}")
        else:
            blocked = any(m.lower() in reason.lower()
                          for m in split["blocking_when_reason_matches"])
    if "blocking_when_field_false" in split:
        f = split["blocking_when_field_false"]
        if f in reeval and not reeval.get(f):
            blocked = True
        elif f not in reeval:
            blocked = True  # the deciding field is absent -> cannot clear it
            reason += f" | deciding field {f!r} absent from the gate result"

    if blocked:
        row = {"check": check, "class": cls, "blocking": True,
               "why_it_blocks": (f"{check} failed on its {cls} sub-condition, not on craft: "
                                 f"{reason[:300]}")}
        return _attach_measurement(row, check, reeval, receipt)

    row = _advisory_row(check, mc, reeval, receipt)
    row["why_it_did_not_block"] = (
        f"{check} is a mixed check; its {cls} sub-condition is clean "
        f"({split.get('blocking_when_field_false') or split.get('blocking_when_reason_matches')}), "
        f"so what failed is craft: {reason[:200]}")
    return row


# ------------------------------------------------------------------- forbidden subjects split

def _term_class(term: str, fst: dict) -> tuple[str | None, str]:
    t = " ".join(str(term).lower().split())
    if t in fst.get("blocking", {}):
        return fst["blocking"][t], f"'{t}' names a risk, not a look"
    if t in [str(x).lower() for x in fst.get("advisory", [])]:
        return None, f"'{t}' encodes taste (a look this episode chose to avoid), not a risk"
    d = fst.get("unlisted_term_default", {})
    if str(d.get("decision", "block")).lower() == "block":
        return d.get("class", "unclassified_forbidden_subject"), (
            f"'{t}' is not classified in config/ship_policy.v001.json. {d.get('why', '')} "
            f"Resolve: {d.get('resolve_by', '')}")
    return None, f"'{t}' unlisted; policy default is advisory"


def _parse_forbidden(line: str) -> list[tuple[str, int, str]]:
    """Pull (term, count, files) out of check_spec_satisfied's forbidden_subjects line.

    Its shape is `forbidden_subjects: N cut source(s) match M forbidden keyword(s) -- kw (n):
    a.mp4, b.mp4; kw2 (n): c.png`. A shape this module cannot parse is treated as a blocking
    parse failure by the caller, never waved through.
    """
    if "--" not in line:
        return []
    tail = line.split("--", 1)[1]
    out: list[tuple[str, int, str]] = []
    for part in tail.split(";"):
        part = part.strip()
        if not part or "(" not in part or "):" not in part:
            continue
        term = part.split("(", 1)[0].strip()
        try:
            n = int(part.split("(", 1)[1].split(")", 1)[0])
        except Exception:  # noqa: BLE001
            n = -1
        files = part.split("):", 1)[1].strip()
        if term:
            out.append((term, n, files[:200]))
    return out


def spec_satisfied_rows(slug: str, mc: dict, epdir: Path) -> list[dict]:
    """Run check_spec_satisfied and split its findings into risk and taste.

    mandatory_stills and distinct_video_assets are craft. forbidden_subjects is BOTH, and the
    keyword says which: a real person, a licence exposure or a fabricated record blocks; a
    gavel or a courtroom interior does not.
    """
    fst = mc["forbidden_subject_terms"]
    unev = fst.get("spec_unevaluable", {})
    spec = epdir / "episode_spec.v001.json"
    film = FILM_DIR / f"{slug}_film.json"
    rows: list[dict] = []

    if not spec.is_file():
        return [{"check": "spec_satisfied", "class": "advisory",
                 "advisory_group": "measurement_gap",
                 "measured": "no episode_spec.v001.json", "measured_source": "reevaluated",
                 "measured_unavailable": None, "threshold": None, "backlog": True,
                 "why_it_did_not_block": f"advisory: {unev.get('no_spec', '')}"}]
    if not film.is_file():
        return [{"check": "spec_satisfied.forbidden_subjects", "class": "rights_and_licence",
                 "blocking": True, "measured": f"no {film.name}", "measured_source": "reevaluated",
                 "measured_unavailable": None, "threshold": None,
                 "why_it_blocks": (f"this episode DECLARES forbidden subjects and the built film "
                                   f"is gone, so they cannot be checked against what shipped. "
                                   f"{unev.get('no_film', '')}")}]

    r = subprocess.run([sys.executable, str(SCRIPTS / "check_spec_satisfied.py"), "--slug", slug],
                       capture_output=True, text=True, cwd=str(ROOT))
    out = (r.stdout or "") + (r.stderr or "")
    if r.returncode == 0:
        return []

    lines = [ln.strip(" -") for ln in out.splitlines() if ln.strip().startswith("- ")]
    if not lines:
        return [{"check": "spec_satisfied", "class": "unclassified_forbidden_subject",
                 "blocking": True, "measured": out.strip()[-300:], "measured_source": "reevaluated",
                 "measured_unavailable": None, "threshold": None,
                 "why_it_blocks": (f"check_spec_satisfied exited {r.returncode} and this module "
                                   f"could not read its answer. {unev.get('parse_failure', '')}")}]

    for ln in lines:
        head = ln.split(":", 1)[0].strip()
        if head == "forbidden_subjects":
            hits = _parse_forbidden(ln)
            if not hits:
                rows.append({"check": "spec_satisfied.forbidden_subjects",
                             "class": "unclassified_forbidden_subject", "blocking": True,
                             "measured": ln[:300], "measured_source": "reevaluated",
                             "measured_unavailable": None, "threshold": None,
                             "why_it_blocks": unev.get("parse_failure", "unparseable")})
                continue
            for term, n, files in hits:
                cls, why = _term_class(term, fst)
                base = {"check": f"spec_satisfied.forbidden_subjects[{term}]",
                        "measured": {"term": term, "matching_cuts": n, "sources": files},
                        "threshold": 0, "measured_source": "reevaluated",
                        "measured_unavailable": None}
                if cls:
                    rows.append({**base, "class": cls, "blocking": True,
                                 "why_it_blocks": f"forbidden subject on screen: {why}"})
                else:
                    rows.append({**base, "class": "advisory", "advisory_group": "craft_footage",
                                 "backlog": True,
                                 "why_it_did_not_block": f"advisory: {why}"})
        else:
            rows.append({"check": f"spec_satisfied.{head}", "class": "advisory",
                         "advisory_group": "craft_footage", "backlog": True,
                         "measured": ln[:300], "measured_source": "reevaluated",
                         "measured_unavailable": None, "threshold": None,
                         "why_it_did_not_block": ("advisory: a missing purpose-made still or a "
                                                  "short distinct-asset count is coverage craft, "
                                                  "not a ban or legal risk")})
    return rows


# ------------------------------------------------------------------- blocking-class detectors

def blocklist_rows(slug: str) -> tuple[list[dict], dict]:
    """Rights: test the cuts that are actually IN the film against the footage blocklist.

    `config/footage_blocklist.v001.json` is the repo's hard-rights denylist (third-party
    production footage, a real identifiable minor, a real named person's identity captioned onto
    another, legible personal data). It was enforced only while STAGING and BUILDING, so a film
    built before a row was added was never re-tested -- and that film is what gets uploaded.
    This calls the existing loader (`pd_footage_blocklist.hits`); it is not a second
    implementation of the matching.
    """
    if str(SCRIPTS) not in sys.path:
        sys.path.insert(0, str(SCRIPTS))
    film = FILM_DIR / f"{slug}_film.json"
    status = {"detector": "pd_footage_blocklist.hits over the built film",
              "film": film.name, "wired_here": True}
    if not film.is_file():
        status.update(state="unmeasurable", note=f"{film.name} is not on disk")
        return [], status
    try:
        fb = importlib.import_module("pd_footage_blocklist")
        d = json.loads(film.read_text(encoding="utf-8"))
        srcs = [c.get("src") for c in (d.get("cuts") or [])] + \
               [h.get("src") for h in (d.get("hook") or [])]
        srcs = [s for s in srcs if s]
        found = fb.hits(srcs, slug)
    except Exception as exc:  # noqa: BLE001
        status.update(state="error", note=f"{type(exc).__name__}: {exc}")
        return [], status
    status.update(state="measured", cuts_tested=len(srcs), hits=len(found))
    rows = []
    for src, why in found:
        rows.append({"check": "footage_blocklist", "class": "rights_and_licence", "blocking": True,
                     "measured": {"source": str(src).split("/")[-1], "reason": str(why)[:200]},
                     "threshold": 0, "measured_source": "reevaluated", "measured_unavailable": None,
                     "why_it_blocks": "a cut in the shipped film is on the rights blocklist"})
    return rows, status


def _film_cut_stems(slug: str) -> tuple[set[str], Path]:
    """Stems of every source the built film actually places as a cut or in the hook.

    Stems, not filenames, because a plate driven to i2v leaves img/ and lands in motion/ as
    `<id>.mp4` -- the same picture in a different container. `check_spec_satisfied` and
    `check_plate_verdicts._find_as_motion` already match on the stem for that reason.
    """
    film = FILM_DIR / f"{slug}_film.json"
    if not film.is_file():
        return set(), film
    d = json.loads(film.read_text(encoding="utf-8"))
    srcs = [c.get("src") for c in (d.get("cuts") or [])] + \
           [h.get("src") for h in (d.get("hook") or [])]
    return {Path(s).stem for s in srcs if s}, film


def classify_plate_reason(note: str, cfg: dict) -> tuple[str | None, str, str]:
    """Reviewer's reason text -> (blocking class or None, why, matched phrase).

    READ THE REASON, DO NOT GUESS THE CLASS. The rules and their order live in
    `config/ship_policy.v001.json` (machine_contract.plate_reject_reasons), never here, so a new
    reason is one line of policy and not a code change. First rule whose `any_of` matches and
    whose `unless_any_of` does not, wins.

    Returns class=None for a reason the policy marks as craft. A reason NOTHING matches is NOT
    returned as None -- the caller fails it closed, which is the same rule the policy already
    applies to an unlisted forbidden_subjects term.
    """
    t = " ".join(str(note or "").lower().split())
    for rule in cfg.get("rules", []):
        if any(p in t for p in rule.get("unless_any_of", []) or []):
            continue
        hit = next((p for p in rule.get("any_of", []) or [] if p in t), None)
        if hit:
            return rule["class"], str(rule.get("why", "")), hit
    adv = cfg.get("advisory_reasons", {}) or {}
    hit = next((p for p in adv.get("any_of", []) or [] if p in t), None)
    if hit:
        return None, str(adv.get("why", "")), hit
    return "__unclassified__", "", ""


def plate_verdict_rows(slug: str, mc: dict) -> tuple[list[dict], dict]:
    """Re-ask the PLATE question after the render, over the plates that actually shipped.

    WHY THIS IS HERE (EP64 memphis, 2026-08-12). The plate gate was never missing. Measured:
    `check_plate_verdicts.py` is wired into `check_episode_inputs.py` and
    `preflight_render_gate.py` -- both INPUT stage -- and referenced 0 times in
    `check_final_acceptance.py` and 0 times in `upload_schedule_case_v001.py`. Once a film was
    rendered nothing re-asked it, so acceptance, shipped-frames and every upload guard went green
    over 16 reviewer-REJECTED plates that were cut into the shipped film.

    A rejection only reaches the door when the plate is IN THE FILM. marmet carries 9 rejects and
    correa 12; every one was regenerated or dropped before the build, none is in a cut, and
    neither episode is touched by this. That distinction is the whole gate: it fires on a
    rejection that was RECORDED AND NOT APPLIED.

    The verdict vocabulary is IMPORTED from `check_plate_verdicts` (`_norm_verdict`,
    `PLATES_KEY`), never restated, so the input gate and the ship gate can never disagree about
    what the word `flag` means.
    """
    if str(SCRIPTS) not in sys.path:
        sys.path.insert(0, str(SCRIPTS))
    cfg = mc.get("plate_reject_reasons") or {}
    vpath = ROOT / "runs" / "qc" / f"{slug}_plate_verdicts.v001.json"
    status = {"detector": "check_plate_verdicts verdicts re-read against the built film",
              "verdicts_file": _repo_path(vpath), "wired_here": True}

    if not cfg:
        status.update(state="unmeasurable",
                      note=("config/ship_policy.v001.json carries no machine_contract."
                            "plate_reject_reasons block, so no reason can be classified"))
        return [], status
    if not vpath.is_file():
        status.update(state="none", note=(
            f"no {vpath.name}: this episode's plates were never reviewed into a file a machine "
            f"can read. {cfg.get('no_verdict_file', {}).get('why', '')}"))
        return [], status

    try:
        cpv = importlib.import_module("check_plate_verdicts")
        data = json.loads(vpath.read_text(encoding="utf-8"))
        entries = data.get(cpv.PLATES_KEY) or {}
        cut_stems, film = _film_cut_stems(slug)
    except Exception as exc:  # noqa: BLE001
        status.update(state="error", note=f"{type(exc).__name__}: {exc}")
        return [], status
    if not film.is_file():
        status.update(state="unmeasurable", note=f"{film.name} is not on disk, so which plates "
                                                 f"were cut cannot be read")
        return [], status
    if not isinstance(entries, dict):
        status.update(state="error", note=f"{vpath.name} has no '{cpv.PLATES_KEY}' map")
        return [], status

    rows: list[dict] = []
    n_rej = n_unres = n_cut_rej = n_cut_unres = 0
    for pid in sorted(entries):
        e = entries[pid]
        if not isinstance(e, dict):
            continue
        v = cpv._norm_verdict(e.get("verdict"))       # the input gate's own vocabulary
        if v == "accept":
            continue
        if v == "reject":
            n_rej += 1
        else:
            n_unres += 1
        if Path(pid).stem not in cut_stems:
            continue        # recorded AND applied: regenerated or dropped before the build
        note = str(e.get("note") or "")
        base = {"measured": {"plate": pid, "verdict": str(e.get("verdict")),
                             "reviewer_reason": note[:240]},
                "threshold": "0 plates rejected or unresolved at review may be cut into the film",
                "measured_source": "reevaluated", "measured_unavailable": None}

        if v != "reject":
            n_cut_unres += 1
            d = cfg.get("unresolved_verdict_default", {})
            rows.append({**base, "check": f"plate_verdict[{pid}]",
                         "class": d.get("class", "unclassified_plate_verdict"), "blocking": True,
                         "why_it_blocks": (
                             f"this plate is CUT INTO THE SHIPPED FILM carrying an UNRESOLVED "
                             f"verdict ({str(e.get('verdict') or 'blank').strip()}). "
                             f"{d.get('why', '')}")})
            continue

        n_cut_rej += 1
        cls, why, hit = classify_plate_reason(note, cfg)
        if cls == "__unclassified__":
            d = cfg.get("unclassified_reject_default", {})
            rows.append({**base, "check": f"plate_reject[{pid}]",
                         "class": d.get("class", "unclassified_plate_reject"), "blocking": True,
                         "why_it_blocks": (
                             f"a plate REJECTED at review is cut into the shipped film and its "
                             f"reason matches no rule in the policy, so it fails closed rather "
                             f"than being guessed: {d.get('why', '')} "
                             f"Resolve: {d.get('resolve_by', '')} Reason as written: "
                             f"{note[:200]}")})
        elif cls is None:
            rows.append({**base, "check": f"plate_reject[{pid}]", "class": "advisory",
                         "advisory_group": "craft_footage", "backlog": True,
                         "why_it_did_not_block": (
                             f"a plate REJECTED at review is cut into the shipped film, and the "
                             f"reviewer's reason names craft only (matched '{hit}'): this policy "
                             f"does not stop a ship on taste. Recorded, not hidden. Reason as "
                             f"written: {note[:200]}")})
        else:
            rows.append({**base, "check": f"plate_reject[{pid}]", "class": cls, "blocking": True,
                         "why_it_blocks": (
                             f"a plate REJECTED at review for a {cls} reason is cut into the "
                             f"shipped film (matched '{hit}'). {why} Reason as written: "
                             f"{note[:200]}")})

    status.update(state="measured", plates=len(entries), cuts_tested=len(cut_stems),
                  rejected=n_rej, unresolved=n_unres,
                  rejected_in_film=n_cut_rej, unresolved_in_film=n_cut_unres,
                  blocking_rows=sum(1 for r in rows if r.get("blocking")))
    return rows, status


def packaging_claim_rows(epdir: Path) -> tuple[list[dict], dict]:
    """Factual support: read the title, thumbnail text and description against the script.

    `config/ship_policy.v001.json` puts packaging inside the BLOCKING `factual_support` class
    -- "the first claim a viewer meets" -- and on 2026-08-12 recorded that two FALSE titles
    cleared every mechanical rule the repo had, because every rule measured length, form and
    punctuation and none of them measured truth. `check_packaging_claims.py` is that missing
    measurement; this is where its verdict reaches the door.

    A claim the record does not state does not block by being suspicious -- it blocks because
    the policy says every figure, name and outcome in a title must be located in the episode's
    own script or facts ledger before it is published. Absence IS the failure.
    """
    if str(SCRIPTS) not in sys.path:
        sys.path.insert(0, str(SCRIPTS))
    status = {"detector": "check_packaging_claims.evaluate over 09_package packaging",
              "wired_here": True}
    try:
        mod = importlib.import_module("check_packaging_claims")
        r = mod.evaluate(epdir)
    except Exception as exc:  # noqa: BLE001
        status.update(state="error", note=f"{type(exc).__name__}: {exc}")
        return [], status
    if r.get("skipped"):
        status.update(state="unmeasurable", note=r.get("reason"))
        return [], status
    status.update(state="measured", claims_checked=r.get("claims_checked"),
                  unsupported=r.get("unsupported"),
                  soft_unsupported=r.get("soft_unsupported"),
                  record_sentences=r.get("record_sentences"))
    rows = []
    soft_written = 0
    for res in r.get("results", []):
        if res.get("ok"):
            continue
        hard = res.get("hard", True)
        if not hard:
            # Recorded, never hidden (the policy forbids dropping a finding silently), but
            # capped: a 4,000-character description can produce fifty paraphrase notes and
            # burying the real row is its own failure mode.
            soft_written += 1
            if soft_written > 10:
                continue
        ev = (res.get("evidence") or [{}])[0]
        rows.append({
            "check": f"packaging_claims[{res['field']}]",
            "class": "factual_support" if hard else "factual_support_advisory",
            "advisory_group": None if hard else "craft_packaging",
            "blocking": bool(hard),
            "why_it_did_not_block": None if hard else (
                "an ordinary past-tense verb or a description sentence the record does not "
                "state in these words. The gate matches words; the films paraphrase. Recorded "
                "for review, not held against the ship."),
            "measured": {"claim": res["claim"][:160], "verdict": res["verdict"],
                         "required_terms": res.get("required_terms"),
                         "record_line": ev.get("where"), "record_text": (ev.get("line") or "")[:240]},
            "threshold": "every figure, name and outcome located in the episode's own record",
            "measured_source": "reevaluated", "measured_unavailable": None,
            "why_it_blocks": (f"{res['verdict']}: the title/thumbnail/description states "
                              f"something the episode's own script and ledger do not"),
        })
    return rows, status


def detector_status(epdir: Path, slug: str, video_sha: str | None,
                    mc: dict | None = None) -> dict:
    """What actually stands behind each of the four blocking classes, FOR THIS EPISODE.

    A policy that promises to block on rights while nothing checks rights is worse than the old
    blanket rule, so this is measured per episode and written onto the release record rather
    than asserted once in prose.
    """
    st: dict[str, dict] = {}
    _plate_rows, plate_st = plate_verdict_rows(slug, mc or {})

    # 1. real person likeness -------------------------------------------------
    review = ROOT / "runs" / "qc" / f"{slug}_shipped_frames_review.v001.json"
    d = {}
    if review.is_file():
        try:
            d = json.loads(review.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            d = {}
    bound = bool(video_sha) and d.get("render_sha256") == video_sha
    st["real_person_likeness"] = {
        "detector": "check_shipped_frames.py (run by the scheduler, hard exit on failure)",
        "evidence": review.relative_to(ROOT).as_posix() if review.is_file() else None,
        "sha_bound_to_this_render": bound,
        "reviewer": str(d.get("reviewer", ""))[:160] or None,
        "plate_review": plate_st,
        "state": "partial" if review.is_file() else "none",
        "honest_limit": ("the frame sampling and the sha binding are real; the LIKENESS "
                         "judgement is free text in this file and nothing authenticates the "
                         "reviewer field. There is no face or minor detector anywhere on the "
                         "ship path. Since 2026-08-12 the PLATE verdicts are also re-read here "
                         "against the built film, so a plate a reviewer rejected for an "
                         "identifiable face can no longer reach the door by being rendered "
                         "first -- but that too is the reviewer's free text, and a plate nobody "
                         "looked at carefully passes it exactly as easily as one they did."),
    }

    # 2. rights and licence ---------------------------------------------------
    rows, bl = blocklist_rows(slug)
    rights_manifests = sorted((epdir / "09_package").glob("rights_manifest.v*.json"))
    st["rights_and_licence"] = {
        "detector": bl,
        "blocklist_hits": len(rows),
        "rights_manifest": rights_manifests[-1].name if rights_manifests else None,
        "state": "partial" if bl.get("state") == "measured" else "none",
        "honest_limit": ("the blocklist is a DENYLIST of assets already found to be bad. "
                         "Nothing on the ship path requires positive licence or provenance "
                         "clearance for the assets in the film, and this episode carries "
                         + ("a rights manifest" if rights_manifests else "NO rights manifest")
                         + "."),
    }

    # 3. factual support ------------------------------------------------------
    claims = sorted((epdir / "01_research").glob("claims.v*.json"))
    ledgers = sorted((ROOT / "episodes" / "_planning").glob(f"EP*_{slug}_FACTS_LEDGER.v*.md"))
    spec = epdir / "episode_spec.v001.json"
    n_forbidden_claims = 0
    if spec.is_file():
        try:
            n_forbidden_claims = len(json.loads(spec.read_text(encoding="utf-8"))
                                     .get("forbidden_claims") or [])
        except Exception:  # noqa: BLE001
            pass
    _pk_rows, pk_status = packaging_claim_rows(epdir)
    st["factual_support"] = {
        "detector": ("verify_onscreen_text (burned on-screen figures vs grade-A claims) + "
                     "check_script_craft (forbidden-claim pass over the script) + "
                     "check_packaging_claims (title/thumbnail/description vs this episode's "
                     "own script, captions and ledgers)"),
        "claim_ledger": claims[-1].name if claims else None,
        "facts_ledger": ledgers[-1].name if ledgers else None,
        "episode_spec_forbidden_claims": n_forbidden_claims,
        "packaging_claims": pk_status,
        "state": "partial" if (claims or ledgers or pk_status.get("state") == "measured")
                 else "none",
        "honest_limit": (
            ("verify_onscreen_text SKIPS on this episode -- there is no claims.v*.json in "
             "01_research, so it reports ok=true without measuring anything. " if not claims else
             "verify_onscreen_text covers on-screen text only. ")
            + ("check_script_craft compares the SCRIPT against the FACTS ledger by literal "
               "substring, so a paraphrase evades it. " if ledgers else
               "there is no FACTS ledger, so check_script_craft fails closed. ")
            + f"episode_spec.forbidden_claims ({n_forbidden_claims} declared) is read by no gate "
              f"that can refuse. Narration is compared against no claim ledger anywhere on the "
              f"ship path. The TITLE, THUMBNAIL TEXT and DESCRIPTION are now read against this "
              f"episode's own record by check_packaging_claims (2026-08-12, after two false "
              f"titles cleared every mechanical rule), and it blocks -- but it matches words, "
              f"stems and numbers only: it cannot judge tone or implication, it passes a title "
              f"whose words are all in a script that is itself wrong, and a paraphrase the film "
              f"states in other words reads as UNVERIFIED. A green from it is not a substitute "
              f"for reading the title against the film."),
    }

    # 4. fabricated record ----------------------------------------------------
    pq = reevaluate("packaging_qc", epdir) or {}
    st["fabricated_record"] = {
        "detector": "check_packaging_qc: the AI-disclosure line in the description that is uploaded",
        "has_ai_disclosure": pq.get("has_ai_disclosure"),
        "state": "partial" if "has_ai_disclosure" in pq else "none",
        "honest_limit": ("this is a substring test for a disclosure phrase, correctly bound to "
                         "the description the scheduler uploads. NOTHING reads truth_status / "
                         "source_type / license_decision, and nothing detects a generated "
                         "document, judgment or police file on screen -- only a human reading "
                         "the contact sheets can."),
    }

    # 5. the plate question, re-asked after the render -------------------------
    # Not a fifth blocking class: it FEEDS the four above. It is recorded separately because it
    # is the one detector whose absence caused a pulled episode, and because what it cannot do
    # is different in kind from what the others cannot do.
    _n_block = plate_st.get("blocking_rows")
    st["plate_review"] = {
        "detector": plate_st,
        "state": ("partial" if plate_st.get("state") == "measured" else "none"),
        "honest_limit": (
            (f"the plate verdicts for this episode ARE re-read against the built film "
             f"({plate_st.get('rejected_in_film')} rejected and "
             f"{plate_st.get('unresolved_in_film')} unresolved plate(s) found in cuts, "
             f"{_n_block} blocking). "
             if plate_st.get("state") == "measured" else
             f"NOT MEASURED for this episode: {str(plate_st.get('note'))[:200]}. ")
            + "IT NEVER LOOKS AT A PICTURE -- check_plate_verdicts.py says so in its own "
              "docstring, and this reads its file, not the plates. It proves a verdict exists, "
              "that it is bound to the bytes on disk, and that no plate a reviewer rejected or "
              "left unresolved was cut into the film. Whether the plates a reviewer ACCEPTED are "
              "actually right is a judgement nothing on the ship path re-checks, and a careless "
              "review passes this exactly as easily as a careful one. The class is read from the "
              "reviewer's own reason text by substring, so a reason worded in new words falls to "
              "unclassified and blocks rather than being guessed."),
    }
    return st


# -------------------------------------------------------------------- unmeasured (skipped) gates

def _blocking_class_of(check: str, mc: dict, classes: list[str]) -> str | None:
    """Which of the four blocking classes this check id belongs to, or None if it is advisory."""
    cand = mc.get("blocking_checks", {}).get(check)
    if cand in classes:
        return cand
    sp = mc.get("split_checks", {}).get(check) or {}
    if sp.get("class") in classes:
        return sp["class"]
    # policy also names sub-conditions ("script_craft.forbidden_claim"); the parent check id
    # skipping means that sub-condition was not measured either.
    for k, v in mc.get("blocking_checks", {}).items():
        if k.split(".")[0] == check and v in classes:
            return v
    # A gate that RAISED, or one that returned a dict without its own `check` key, is named in
    # the receipt by its MODULE (check_motion_density, verify_onscreen_text) rather than by its
    # check id (motion_density, onscreen_text_verified) -- _ext_gate's fallback cannot know the
    # id it never got. Without this hop a CRASHED verify_onscreen_text would be recorded as an
    # advisory absence instead of an unmeasured factual_support, which is the exact blindness
    # this whole change exists to remove. REEVALUABLE already holds the id -> module mapping.
    alias = next((cid for cid, mod in REEVALUABLE.items() if mod == check), None)
    if alias is None:
        for pfx in ("check_", "verify_"):
            if check.startswith(pfx):
                alias = check[len(pfx):]
                break
    if alias and alias != check:
        return _blocking_class_of(alias, mc, classes)
    return None


def unmeasured_rows(receipt: dict, mc: dict, classes: list[str]) -> list[dict]:
    """Checks the receipt reports as SKIPPED -- and which blocking class each one leaves blind.

    A skip is not a failure, so it never appears in `hard_failures` and nothing above this line
    ever saw it. That is precisely how `onscreen_text_verified` -- the only factual_support
    detector on the ship path -- reported green on every episode since PD-2026-037 without
    reading a single claim: no claims.v*.json, an honest skip inside the gate, and a receipt that
    wrote `true`.

    RECORD-AND-PERMIT, NOT REFUSE -- and this is a trade, not a free choice. Refusing on an
    unmeasured blocking class is the stricter and in the abstract the more correct answer: the
    policy promises to stop on factual_support, and an unmeasured factual_support is not evidence
    that the film is clean. It is rejected here for one reason that is about consequences, not
    about principle: NONE of the seven in-flight episodes carries a claim ledger, so refusing
    would stop all seven and every episode behind them on a tooling gap that no operator can
    close tonight -- and a gate that stops everything on day one gets switched off on day two,
    which would leave the project worse off than before this was found. So the absence is
    PERMITTED and recorded where it cannot be missed: as its own `unmeasured_checks` block, in
    `unmeasured_blocking_classes`, folded into `detector_gaps`, and printed as UNMEASURED. The
    cost of that choice is real and should be stated plainly: an episode can still ship with its
    factual_support class never having been measured. Turning it into a refusal is one line here
    (append these rows to `blocking` in evaluate()) once the episodes carry claim ledgers.
    """
    rows: list[dict] = []
    skipped = receipt.get("skipped_checks")

    if skipped is None:
        # A pre-1.1.0 receipt cannot answer the question at all: a skip was written as `true`.
        if receipt.get("checks"):
            rows.append({
                "check": "*", "class": "unknown", "blocking": False, "unmeasured": True,
                "skip_kind": "receipt_predates_tristate",
                "detail": (f"acceptance receipt schema_version "
                           f"{receipt.get('schema_version', 'unknown')} has no skipped_checks "
                           f"block; a gate that skipped or raised was written into `checks` as "
                           f"true, so ANY green in it may be an absence rather than a "
                           f"measurement"),
                "why_it_did_not_block": (
                    "this receipt was written before checks became tri-state, so which of its "
                    "greens were measured cannot be recovered from it. Re-run "
                    "`check_final_acceptance.py <ep> --render <mp4> --emit-receipt` to get a "
                    "receipt that can tell a skip from a pass."),
                "backlog": True})
        return rows

    for s in skipped or []:
        chk = str(s.get("check", "?"))
        cls = _blocking_class_of(chk, mc, classes)
        row = {"check": chk, "unmeasured": True, "blocking": False,
               "class": cls or "advisory",
               "skip_kind": s.get("kind"),
               "detail": str(s.get("reason", ""))[:400],
               "backlog": True}
        if cls:
            row["why_it_did_not_block"] = (
                f"UNMEASURED BLOCKING CLASS: {chk} is the {cls} detector and it DID NOT RUN "
                f"({s.get('kind')}): {str(s.get('reason', ''))[:200]}. Nothing was measured, so "
                f"nothing clears this class for this episode. It is permitted because a missing "
                f"input is a tooling gap rather than evidence about the film, and it is recorded "
                f"here so that no reader can mistake this receipt's green for a measurement.")
        else:
            row["why_it_did_not_block"] = (
                f"{chk} did not run ({s.get('kind')}): {str(s.get('reason', ''))[:160]}. It is "
                f"not in a blocking class, so the absence is recorded and does not block.")
        rows.append(row)
    return rows


# ------------------------------------------------------------------------------- the decision

def owner_approved(epdir: Path) -> dict[str, str]:
    """Deviations the owner formally accepted for THIS episode (unchanged mechanism)."""
    out: dict[str, str] = {}
    for f in sorted((epdir / "approvals").glob("*.json")):
        try:
            a = json.loads(f.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            continue
        if a.get("target_type") == "edit" and str(a.get("decision", "")).startswith("approved"):
            for dv in a.get("accepted_deviations", []) or []:
                if isinstance(dv, str):
                    out[dv] = f.name
    return out


def evaluate(epdir: Path, slug: str, receipt: dict, *, receipt_path: Path | None = None,
             video_sha: str | None = None, video_path: str | None = None,
             policy: dict | None = None, dry_run: bool = False) -> dict:
    """Apply config/ship_policy.v001.json to one acceptance receipt.

    Returns the release record. `decision` is "permit" or "refuse"; `blocking_failures` names
    the class for each refusal.
    """
    policy = policy or load_policy()
    mc = policy["machine_contract"]
    classes = blocking_class_ids(policy)

    rows: list[dict] = []
    for check in receipt.get("hard_failures", []) or []:
        rows.append(classify_hard_failure(check, mc, epdir, receipt))
    rows.extend(spec_satisfied_rows(slug, mc, epdir))
    bl_rows, _bl_status = blocklist_rows(slug)
    rows.extend(bl_rows)
    pk_rows, _pk_status = packaging_claim_rows(epdir)
    rows.extend(pk_rows)
    # The plate question, re-asked after the render. It is not in `hard_failures` and never can
    # be: check_plate_verdicts is an INPUT-stage gate and the receipt does not carry its answer.
    pv_rows, _pv_status = plate_verdict_rows(slug, mc)
    rows.extend(pv_rows)

    approved = owner_approved(epdir)
    blocking, advisory = [], []
    for r in rows:
        if not r.get("blocking"):
            advisory.append(r)
            continue
        base = r["check"].split("[")[0].split(".")[0]
        apr = approved.get(r["check"]) or approved.get(base)
        if apr:
            r = {**r, "blocking": False, "owner_approved_blocking": apr,
                 "why_it_did_not_block": (f"class {r['class']} -- BLOCKING, and shipped only "
                                          f"because the owner formally accepted it for this "
                                          f"episode in approvals/{apr}"),
                 "backlog": True}
            advisory.append(r)
        else:
            blocking.append(r)

    unclassified = [r["check"] for r in advisory if r.get("advisory_group") == "unclassified"]
    det = detector_status(epdir, slug, video_sha, mc)
    gaps = [f"{k}: {v['state']} -- {v['honest_limit']}" for k, v in det.items()
            if v.get("state") != "real"]

    # Gates that SKIPPED measured nothing, so they are neither a pass nor a failure. They are
    # not in hard_failures and were invisible here until receipt schema 1.1.0. See
    # unmeasured_rows() for why an unmeasured BLOCKING class is recorded rather than refused.
    unmeasured = unmeasured_rows(receipt, mc, classes)
    unmeasured_blocking = [r for r in unmeasured if r.get("class") in classes]
    for r in unmeasured_blocking:
        gaps.append(f"{r['class']}: UNMEASURED -- {r['check']} did not run "
                    f"({r.get('skip_kind')}): {str(r.get('detail', ''))[:220]}. This class was "
                    f"NOT cleared for this episode; the receipt's green for it is an absence.")
    for r in unmeasured:
        if r.get("skip_kind") == "receipt_predates_tristate":
            gaps.append(f"receipt: UNMEASURED-UNKNOWN -- {r['detail']}")

    return {
        "schema_version": "1.0.0",
        "artifact_type": "pd_release_deviations",
        "episode_id": epdir.name,
        "slug": slug,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "dry_run": bool(dry_run),
        "policy": {"path": POLICY_PATH.relative_to(ROOT).as_posix(),
                   "authored": policy.get("authored"),
                   "the_rule": policy.get("the_rule"),
                   "blocking_classes": classes},
        "receipt": {"path": _repo_path(receipt_path),
                    "status": receipt.get("status"),
                    "video_sha256": receipt.get("video_sha256"),
                    "hard_failures": receipt.get("hard_failures", [])},
        "video": {"path": video_path, "sha256": video_sha},
        "decision": "refuse" if blocking else "permit",
        "blocking_failures": blocking,
        "deviations": advisory,
        "unclassified_checks": unclassified,
        "unmeasured_checks": unmeasured,
        "unmeasured_blocking_classes": sorted({r["class"] for r in unmeasured_blocking}),
        "blocking_class_detectors": det,
        "detector_gaps": gaps,
        "measurement_unchanged": ("check_final_acceptance.py ran every check and computed every "
                                  "number for this render; this file records which of its "
                                  "failures were permitted and with what value. No threshold "
                                  "was lowered and no check was switched off."),
    }


def write_release_record(epdir: Path, record: dict) -> Path:
    """Write the record, never over an existing one (CLAUDE invariant 6).

    A dry run writes `release_deviations.dryrun.v{NNN}.json` so that inspecting a decision
    before booking cannot consume `release_deviations.v001.json` -- the path the policy names
    for the real release.
    """
    pkg = epdir / "09_package"
    pkg.mkdir(parents=True, exist_ok=True)
    stem = "release_deviations.dryrun" if record.get("dry_run") else "release_deviations"
    n = 1
    while (pkg / f"{stem}.v{n:03d}.json").exists():
        n += 1
    p = pkg / f"{stem}.v{n:03d}.json"
    p.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return p


def print_decision(record: dict) -> None:
    print(f"[policy] {POLICY_PATH.name}: block on ban and legal risk, not on taste "
          f"({', '.join(record['policy']['blocking_classes'])})")
    for r in record["deviations"]:
        m = r.get("measured")
        m = json.dumps(m, ensure_ascii=False) if isinstance(m, (dict, list)) else m
        if m not in (None, "", "{}"):
            tail = f" measured={m}"
        elif r.get("detail"):
            tail = f" measured={str(r['detail'])[:200]}"
        else:
            tail = f" measured=UNAVAILABLE ({str(r.get('measured_unavailable'))[:110]})"
        owner = f" [owner-approved {r['owner_approved_blocking']}]" if r.get("owner_approved_blocking") else ""
        print(f"[policy] advisory  {r['check']}{owner}:{tail}")
    for r in record["blocking_failures"]:
        print(f"[policy] BLOCKING  {r['check']}  class={r['class']}: {r.get('why_it_blocks', '')}")
    _classes = record["policy"]["blocking_classes"]
    for r in record.get("unmeasured_checks", []) or []:
        tag = "UNMEASURED-BLOCKING" if r.get("class") in _classes else "unmeasured        "
        print(f"[policy] {tag} {r['check']}  class={r['class']} "
              f"({r.get('skip_kind')}): {str(r.get('detail', ''))[:160]}")
    for g in record["detector_gaps"]:
        print(f"[policy] detector  {g}")
    if record["unclassified_checks"]:
        print(f"[policy] unclassified (treated as advisory, add them to the policy): "
              f"{record['unclassified_checks']}")
    _ub = record.get("unmeasured_blocking_classes") or []
    if _ub:
        print(f"[policy] NOT MEASURED on this episode, permitted and recorded, NOT cleared: "
              f"{_ub}")
    print(f"[policy] decision={record['decision']} "
          f"advisory={len(record['deviations'])} blocking={len(record['blocking_failures'])} "
          f"unmeasured={len(record.get('unmeasured_checks') or [])}")


# --------------------------------------------------------------------------------------- CLI

def _resolve_epdir(slug: str) -> Path:
    hits = sorted((ROOT / "episodes").glob(f"PD-*-{slug}"))
    if not hits:
        raise SystemExit(f"no episodes/PD-*-{slug}")
    return hits[-1]


def main(argv: list[str] | None = None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--slug", required=True)
    ap.add_argument("--receipt", help="explain a specific receipt (default: the latest)")
    ap.add_argument("--video-sha", help="bind the explanation to these bytes")
    ap.add_argument("--json", action="store_true", help="print the release record")
    ap.add_argument("--write", action="store_true",
                    help="write 09_package/release_deviations.v{NNN}.json (the scheduler does "
                         "this itself; here it is opt-in)")
    a = ap.parse_args(argv)

    epdir = _resolve_epdir(a.slug)
    if a.receipt:
        rp = Path(a.receipt)
    else:
        rs = sorted((epdir / "09_package").glob("acceptance_receipt.v*.json"))
        if not rs:
            raise SystemExit(f"no acceptance receipt in {epdir / '09_package'}")
        rp = rs[-1]
    receipt = json.loads(rp.read_text(encoding="utf-8"))
    rec = evaluate(epdir, a.slug, receipt, receipt_path=rp,
                   video_sha=a.video_sha or receipt.get("video_sha256"),
                   video_path=receipt.get("video_path"), dry_run=True)
    print(f"[policy] episode={epdir.name} receipt={rp.name} status={receipt.get('status')} "
          f"hard_failures={len(receipt.get('hard_failures') or [])}")
    print_decision(rec)
    if a.json:
        print(json.dumps(rec, ensure_ascii=False, indent=2))
    if a.write:
        print(f"[policy] record -> {write_release_record(epdir, rec).relative_to(ROOT)}")
    return 1 if rec["decision"] == "refuse" else 0


if __name__ == "__main__":
    raise SystemExit(main())
