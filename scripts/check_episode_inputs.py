#!/usr/bin/env python
"""Fail an episode build in SECONDS when an input is missing, instead of hours into a render.

Every EP55-59 failure on 2026-08-01 was a missing or misnamed INPUT, not a defect in the work:
a filmconfig named EP057_ instead of EP57_, no narration.mp3 in the public dir, and no P###
people stills for the builder to find. Each one surfaced only after the manifest, the film
json, the caption pass and (for one) a two-hour render had already run.

This runs first and prints EVERYTHING that is missing at once, so one fix-up round clears the
whole list rather than discovering the next gap after the next long build.

    python scripts/check_episode_inputs.py --slug lejeune

The episode spec is the first gate. check_episode_spec.py runs before anything else here, and
when the spec is missing or invalid this stops there instead of measuring the episode against
the constants in this file: an undeclared value is an error, never an inferred default. That
is the failure that produced EP50-59, where the acceptance gate fell back to a 690-750s band
and every 29-minute episode failed a band it was never built to. Every number below that the
spec declares -- beats per act, people plates, the mandatory stills, the distinct-video floor
-- is read from the spec rather than from a constant.

Exit 0 = ready to build. Exit 1 = listed inputs are missing. Read-only.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

from check_episode_spec import load_and_validate

ROOT = Path(__file__).resolve().parents[1]
# These two are absolute floors, not targets. The spec's own numbers raise them; nothing
# lowers them. Every other number this file used to hard-code now comes from the spec.
MIN_FACTORY = 40
MIN_STILLS = 40


def _face_share(path: Path) -> float | None:
    """Largest detected face as a share of the frame; None when no detector is available.

    None and 0.0 are DIFFERENT answers and the difference is the whole point: "I looked and
    there is no face" is a measurement, "I could not look" is not. Conflating them is what let
    seven object stills pass as people plates.
    """
    try:
        import cv2
    except ImportError:
        return None
    img = cv2.imread(str(path))
    if img is None:
        return 0.0
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    found = cascade.detectMultiScale(gray, scaleFactor=1.08, minNeighbors=6,
                                     minSize=(int(img.shape[0] * 0.05),) * 2)
    if len(found) == 0:
        return 0.0
    x, y, w, h = max(found, key=lambda f: f[2] * f[3])
    return (w * h) / float(img.shape[0] * img.shape[1])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument(
        "--allow-video-diversity-deviation",
        action="store_true",
        help=("permit a review-cut build when the only pool shortfall is distinct footage/motion; "
              "the deviation remains printed and check_spec_satisfied still reports it"),
    )
    ap.add_argument(
        "--no-forecast",
        action="store_true",
        help=("skip the pre-render acceptance forecast (scripts/predict_acceptance.py). It costs "
              "about half a minute and never changes this command exit code"),
    )
    a = ap.parse_args()
    slug = a.slug

    # THE SPEC RUNS FIRST. If it is missing or invalid this stops here: the numbers below are
    # the episode's own declared numbers, and measuring an episode against constants it never
    # agreed to is exactly how nine consecutive receipts came back red and stopped being read.
    spec, spec_problems, ep = load_and_validate(slug)
    if spec_problems:
        print(f"[inputs] {slug}: NOT READY -- the episode spec is missing or invalid, so no "
              f"input can be checked ({len(spec_problems)} problem(s)):")
        for p in spec_problems:
            print(f"  - {p}")
        print(f"[inputs] {slug}: nothing was measured against a default. Write "
              f"episodes/PD-*-{slug}/episode_spec.v001.json, then run this again.")
        return 1
    assert spec is not None and ep is not None

    problems: list[str] = []
    notes: list[str] = []

    # THE EP77 ROAD (owner directive 2026-08-23: 「77話以降は今までのやり方で進まないようにして
    # ほしい」). For episode 077+ the script/pool standard is checked HERE, at the choke point
    # both the queue and the finisher refuse on -- so the old route is closed by wiring, not by
    # policy prose. Episodes below 077 return PASS instantly inside the tool; EP70-76 finish
    # exactly as they are. Details and the measured numbers: scripts/check_ep77_standard.py.
    r77 = subprocess.run(
        ["py", "-3.11", str(ROOT / "scripts/check_ep77_standard.py"),
         "--slug", slug, "--stage", "inputs"],
        capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=ROOT)
    if r77.returncode == 1:
        for ln in r77.stdout.splitlines():
            if ln.strip().startswith("- "):
                problems.append("EP77 standard: " + ln.strip()[2:])
    elif r77.returncode not in (0, 1):
        problems.append(f"EP77 standard could not be evaluated (exit {r77.returncode}) -- "
                        f"fail closed rather than silently skipping")
    num = ep.name.split("-")[2].lstrip("0")

    # SORTED: an unsorted glob returned v001 while the design owner had already delivered
    # v003. EP60 would have been measured on a 2-4 beat placeholder config instead of the real
    # 13-20 one -- reported as kamishibai when it was fine, or worse, passed on the wrong file.
    cfgs = sorted((ROOT / "episodes" / "_planning").glob(f"EP*{slug}_filmconfig.v*.json"))
    if not cfgs:
        problems.append(f"no filmconfig: expected episodes/_planning/EP{num}_{slug}_filmconfig.v001.json")
    else:
        wanted = f"EP{num}_{slug}_filmconfig"
        if not any(c.name.startswith(wanted) for c in cfgs):
            problems.append(f"filmconfig misnamed: found {cfgs[0].name}, the builder looks for "
                            f"{wanted}.v001.json")
        else:
            cfg = None
            try:
                # LATEST revision, not the first. Sorting the glob was only half the fix --
                # this still read cfgs[0], so EP60 was measured against the v001 placeholder
                # (2-4 beats per act) while the design owner had already delivered v003 with
                # 13-20. It would have reported kamishibai on a config nobody was using.
                cfg = json.loads(cfgs[-1].read_text(encoding="utf-8"))
            except Exception as exc:  # noqa: BLE001
                problems.append(f"filmconfig is not valid JSON ({exc})")
            if isinstance(cfg, dict):
                # EP57 shipped 10 figure beats in total against 78-91 on its siblings, and the
                # gate called it kamishibai only after the render. The floor is the episode's
                # own figure_beats_per_act, not a constant in this file.
                beats_lo = int(spec["figure_beats_per_act"][0])
                thin = {k: len(v) for k, v in (cfg.get("figures_by_section") or {}).items()
                        if str(k).upper().startswith("ACT") and isinstance(v, list)
                        and len(v) < beats_lo}
                if thin:
                    problems.append(
                        f"figure beats below the spec floor of {beats_lo} per act: "
                        + ", ".join(f"{k}={n}" for k, n in sorted(thin.items()))
                        + f" (declared in {ep.name}/episode_spec.v001.json)")

    narr = ep / "06_audio" / "narration_index.v001.json"
    if not narr.is_file():
        problems.append(f"no narration index: {narr.relative_to(ROOT)}")
    else:
        chunks = json.loads(narr.read_text(encoding="utf-8")).get("chunks") or []
        spoken = [c for c in chunks if str(c.get("text") or "").strip()]
        if len(spoken) < 20:
            problems.append(f"narration index has only {len(spoken)} spoken chunk(s)")
        else:
            notes.append(f"narration {len(spoken)} chunks, "
                         f"{chunks[-1]['end'] / 60:.1f} min")

    pub = ROOT / "remotion" / "public" / slug
    if not (pub / "narration.mp3").is_file():
        problems.append(f"no narration audio: remotion/public/{slug}/narration.mp3")
    stills = list((pub / "img").glob("*.png")) if (pub / "img").is_dir() else []
    # A FILENAME IS NOT A FACE.
    # This counted anything beginning with "P" and never looked at the picture. EP59 passed
    # with seven "people plates" that are a hand holding an envelope, a wall calendar, mail
    # sacks, a printer, a man from behind, a truck at night and a hand on a phone -- haarcascade
    # false positives on object art. The floor would have gone green on an envelope.
    # AUTHORED-AS-A-PERSON beats FACE-DETECTED, because the two disagree for good reasons.
    # EP57 and EP60 require every person to be ANONYMISED -- turned away, in profile lost to
    # shadow, back-lit to silhouette, cropped below the eyes -- so a frontal-face detector sees
    # nothing and reported 3 of 14 and 5 of 14. Those plates are correct; the detector was
    # measuring the wrong thing. EP59 is the opposite case: seven plates that a haarcascade
    # false-positived out of object art (an envelope, a wall calendar, mail sacks, a printer)
    # with no person in any of them, and no people brief behind them.
    # So a plate counts when it was AUTHORED as a person -- named in this episode\x27s people
    # prompt file -- or when a face is actually detected.
    authored = set()
    for pat in ("04_scenes/ai_prompts_people*.md", "04_scenes/*PEOPLE*.md"):
        for f in ep.glob(pat):
            authored |= set(re.findall(r"\bP\d{2,3}\b", f.read_text(encoding="utf-8")))
    for f in (ROOT / "episodes" / "_planning").glob(f"EP*{slug.upper()}*PEOPLE*.md"):
        authored |= set(re.findall(r"\bP\d{2,3}\b", f.read_text(encoding="utf-8")))
    # An episode may DECLARE which plates are its people plates. EP62-65 name theirs with
    # the episode prefix (G210-G219, C211-C220, M198-M207, R207-R216), all ordered in the
    # batch and all generated, and this counted 0 of 10 on every one of them because it
    # only ever looked at names beginning with "P". A filename is not a face, and it is
    # not a people plate either.
    declared = {s.upper() for s in spec.get("people_plates", [])}
    declared |= {Path(s).stem.upper() for s in spec.get("people_plates", [])}
    faces = []
    unverified = []
    for p in stills:
        if p.name.upper() in declared or p.stem.upper() in declared:
            faces.append(p)               # declared by the spec
            continue
        if not p.name.upper().startswith("P"):
            continue
        if p.stem.upper() in authored:
            faces.append(p)               # written as a person, by brief
            continue
        share = _face_share(p)
        if share is None:
            unverified.append(p)          # detector unavailable: say so, do not assume
        elif share > 0:
            faces.append(p)
    # A PEOPLE PLATE CONVERTED TO MOTION IS STILL A PEOPLE PLATE. i2v moves a converted still
    # out of img/ into img_unused/ and the film uses motion/<stem>.mp4 instead -- the person is
    # IN the film, animated, which is the whole point of converting people first. Measured
    # 2026-08-17 on ramirez: 16 of its 24 people plates had been converted, this count only ever
    # looked at img/, and the episode was refused for having too FEW people at the exact moment
    # its people became motion. Count a retired still when its motion clip exists, under the
    # same qualification rules as the live ones.
    unused_dir = ROOT / "remotion" / "public" / slug / "img_unused"
    motion_dir = ROOT / "remotion" / "public" / slug / "motion"
    if unused_dir.is_dir() and motion_dir.is_dir():
        for p in sorted(unused_dir.glob("*.png")):
            mp4 = motion_dir / f"{p.stem}.mp4"
            if not (mp4.is_file() and mp4.stat().st_size > 100_000):
                continue
            if (p.name.upper() in declared or p.stem.upper() in declared
                    or (p.name.upper().startswith("P") and p.stem.upper() in authored)):
                faces.append(p)
                continue
            if p.name.upper().startswith("P"):
                share = _face_share(p)
                if share is None:
                    unverified.append(p)
                elif share > 0:
                    faces.append(p)
    if unverified:
        notes.append(f"{len(unverified)} people plate(s) could not be verified -- no face "
                     f"detector in this interpreter; re-run with py -3.11")
    if len(stills) < MIN_STILLS:
        problems.append(f"only {len(stills)} still(s) in remotion/public/{slug}/img (need >= {MIN_STILLS})")
    plates_min = int(spec["people_plates_min"])
    if len(faces) < plates_min:
        problems.append(f"only {len(faces)} P### people still(s) in remotion/public/{slug}/img, "
                        f"against the {plates_min} this episode declares -- EP57 carried 2 in a "
                        f"film about one person and EP60 carried 0 "
                        f"(run scripts/register_face_stills.py --slug {slug})")
    # Stills generated FOR this episode to cover a gap the archive cannot fill. EP54's fourteen
    # courtroom plates went missing between here and the render; they are named now, so their
    # absence is a listed problem instead of a discovery.
    mandatory = list(spec.get("mandatory_stills") or [])
    # MATCH ON THE STEM, THE SAME RULE check_spec_satisfied.py ALREADY USES.
    # A commissioned plate can reach the film as img/W001.png or, once it has been given
    # motion (i2v), as motion/W001.mp4 -- the same picture in a different container. EP61
    # weimer converts 64 of its 150 plates precisely because a 43-clip footage pool cannot
    # otherwise carry a 30-minute film above the 68% video floor. Demanding the PNG here while
    # the post-build gate accepts either one made the two checks disagree about the same film,
    # and the pre-flight was the one that was wrong. This does NOT weaken anything: a plate
    # that exists in NO form is still listed.
    def _staged(name: str) -> bool:
        stem = name.rsplit(".", 1)[0]
        if (pub / "img" / name).is_file():
            return True
        return any((pub / "motion" / f"{stem}{ext}").is_file()
                   for ext in (".mp4", ".mov", ".webm"))

    absent = [s for s in mandatory if not _staged(s)]
    if absent:
        problems.append(f"{len(absent)} of {len(mandatory)} mandatory_stills are not in "
                        f"remotion/public/{slug}/img: {', '.join(absent)}")
    factory = list((pub / "factory").glob("*.mp4")) if (pub / "factory").is_dir() else []
    if len(factory) < MIN_FACTORY:
        message = f"only {len(factory)} factory clip(s) (need >= {MIN_FACTORY})"
        if a.allow_video_diversity_deviation:
            notes.append(f"REVIEW-CUT DEVIATION accepted: {message}")
        else:
            problems.append(message)
    motion = list((pub / "motion").glob("*.mp4")) if (pub / "motion").is_dir() else []

    qc = list((ep / "05_visuals").glob("factory_clip_qc.v*.json"))
    if factory and not qc:
        problems.append(f"no factory_clip_qc manifest (run scripts/write_factory_clip_qc.py --slug {slug})")
    elif qc:
        # THE FOOTAGE IS LOOKED AT BEFORE THE RENDER, NOT AFTER.
        # The shelf filenames lie, so "on theme" is not machine-decidable -- but "has anyone
        # actually opened the contact sheet" is, and that is the part that kept slipping.
        # EP54 measured 115 rejects out of 204 once someone looked: nine modern ambulances,
        # eight law-firm adverts, a Guy Fawkes hacker and an Indian tractor, inside a 1996
        # Mississippi story. All of it was visible on a contact sheet in minutes.
        try:
            rows = json.loads(qc[-1].read_text(encoding="utf-8")).get("clips", [])
        except Exception as exc:  # noqa: BLE001
            rows = []
            problems.append(f"factory_clip_qc is not valid JSON ({exc})")
        unreviewed = [r for r in rows if r.get("verdict") == "unreviewed"]
        accepted = [r for r in rows if r.get("verdict") == "accept"]
        if unreviewed:
            problems.append(
                f"{len(unreviewed)} of {len(rows)} staged clip(s) have never been looked at. "
                f"Build sheets with scripts/build_footage_contact_sheet.py --dir "
                f"remotion/public/{slug}/factory --media video --out-dir runs/qc/{slug}_factory, "
                f"read them, record verdicts in runs/qc/{slug}_clip_verdicts.v001.json, "
                f"then re-run scripts/write_factory_clip_qc.py --slug {slug}")
        else:
            # A flat floor of 40 is meaningless for a 30-minute film. Size the requirement to
            # the narration: ~4.5s per cut, roughly two thirds of cuts are footage, and
            # footage_diversity caps reuse at 2 -- so the pool has to be about that big or the
            # builder is forced into repeats and the diversity gate fails AFTER the render.
            # EP54 came out of visual QC with 89 accepted clips for a 28-minute film; the
            # subagent that reviewed it flagged the same arithmetic by hand.
            secs = 0.0
            if narr.is_file():
                try:
                    secs = float(json.loads(narr.read_text(encoding="utf-8"))
                                 .get("total_seconds") or 0)
                except Exception:  # noqa: BLE001
                    secs = 0.0
            # Two numbers, because the builder and the gate disagree by design: the builder
            # may reuse a video asset twice (MAX_VIDEO_REUSE = 2), while the acceptance gate\x27s
            # asset_reuse cap is 1. `need` is the blocking floor (a pool below it cannot even be
            # built); `no_reuse` is what it would take to satisfy the gate outright. EP54 shipped
            # 253 footage cuts from 188 distinct assets -- 65 doubled -- and the pre-flight said
            # READY because it only checked the lower number. Both are printed now.
            # The episode's declared number is the contract. The measured narration can
            # only raise it -- never lower it, because a film whose narration runs longer than
            # the low edge of its own runtime band needs more footage, not less.
            declared = int(spec["distinct_video_assets"])
            no_reuse = max(declared, int(secs / 4.5 * 0.65)) if secs else declared
            # Ask the planner, do not re-derive. `no_reuse // 2` encoded "the builder may
            # reuse a factory clip twice", which stopped being true when solve_totals was changed
            # to plan with check_asset_reuse's asymmetric caps (factory 1, motion 2). That stale
            # halving demanded 132 clips of EP62 greene while the corrected plan uses 63 of its 74.
            # Three copies of one sum is how the builder and the gate drifted apart in the first
            # place; this leaves one.
            need = max(MIN_FACTORY, no_reuse // 2)
            try:
                from build_case_film_generic import solve_totals as _solve, _CAP_FACTORY as _capf
                _f, _m, _s = _solve(secs or 1800.0, len(accepted), len(motion), len(stills))
                if _f <= len(accepted) * _capf:
                    # The pool CAN produce a legal plan -- but MIN_FACTORY still binds. Without
                    # the outer max(), a three-clip pool would satisfy a three-clip plan and the
                    # absolute floor would be gone: that is weakening the gate, not correcting it.
                    need = max(MIN_FACTORY, min(need, len(accepted)))
            except Exception:                          # planner unavailable: keep the old floor
                pass
            motion_n = len(motion)
            if no_reuse and len(accepted) + motion_n < no_reuse:
                notes.append(
                    f"asset_reuse will FAIL: {len(accepted)}+{motion_n} distinct video assets vs "
                    f"~{no_reuse} footage cuts, so ~{no_reuse - len(accepted) - motion_n} clip(s) "
                    f"must repeat. Stage more to avoid it, or accept the deviation knowingly")
            if len(accepted) < need:
                message = (
                    f"only {len(accepted)} clip(s) survived visual QC, but a {secs / 60:.0f}-minute "
                    f"film needs about {need} at the reuse cap ({len(rows) - len(accepted)} were "
                    f"rejected). Stage replacements with scripts/stage_episode_footage.py "
                    f"--slug {slug} before building -- a thin pool comes back as a "
                    f"footage_diversity failure after the render, not before it.")
                if a.allow_video_diversity_deviation:
                    notes.append(f"REVIEW-CUT DEVIATION accepted: {message}")
                else:
                    problems.append(message)

    # A clip that a person opened and rejected must not reach the render. The machine gates
    # measure motion, luma and diversity; a rejected clip passes all three, so nothing downstream
    # sees it. Measured 2026-08-09: correa 46, memphis 52, marmet 45 rejected clips sitting in
    # film.json files written before the rejections were applied, with the rebuild that should
    # have replaced them having failed silently. Deliberately not waivable by
    # --allow-video-diversity-deviation: that deviation accepts a thin pool, never the rejects.
    verdicts = ROOT / "runs" / "qc" / f"{slug}_clip_verdicts.v001.json"
    if verdicts.is_file():
        try:
            rejected = set(json.loads(verdicts.read_text(encoding="utf-8")).get("rejected") or {})
        except Exception as exc:  # noqa: BLE001
            rejected = set()
            problems.append(f"{verdicts.name} is unreadable ({exc}) -- cannot prove the film is "
                            f"free of clips that were rejected by eye")
        if rejected:
            # Judge the POOL, not the film.json. The film.json on disk at this point is about
            # to be rebuilt at [4/7] from whatever the pool holds, so failing on its contents
            # stops builds that would have come out clean. If the pool is free of rejects, no
            # rebuild can put one in the film; if it is not, the render is contaminated whatever
            # the current film.json says.
            pool = ROOT / "remotion" / "public" / slug / "factory"
            present = sorted(p.name for p in pool.glob("*.mp4") if p.name in rejected)
            if present:
                shown = ", ".join(present[:3])
                problems.append(
                    f"{len(present)} clip(s) rejected in visual QC are still staged in "
                    f"remotion/public/{slug}/factory (e.g. {shown}). The build draws from this "
                    f"directory, so remove them before rendering -- "
                    f"runs/qc/{slug}_clip_verdicts.v001.json records why each was rejected.")

    # Wired 2026-08-10. The owner asked FOUR TIMES whether the opening design document followed
    # their manual (C:/Users/aab15/CLAUDE.md). I answered "yes" twice; on the fourth asking I
    # finally checked mechanically and found a missing required section. Nobody should have to ask
    # a fourth time, so the check now runs on its own, at the stage where fixing it is free.
    _pkg = sorted((ROOT / "episodes" / "_planning").glob(f"EP*_{slug}_PACKAGING.v*.md"))
    if _pkg:
        _r = subprocess.run([sys.executable, str(ROOT / "scripts" / "check_opening_spec.py"),
                             "--slug", slug], capture_output=True, text=True, encoding="utf-8")
        if _r.returncode != 0:
            _bad = [l for l in (_r.stdout or "").splitlines()
                    if l.startswith("欠落") or l.startswith("禁止事項")]
            problems.append(f"{_pkg[-1].name} does not satisfy the opening design-doc manual: "
                            + (" / ".join(_bad) if _bad else "see check_opening_spec.py --slug "
                                                             + slug))

    # THE POOL IS LOOKED AT ACROSS EACH CLIP, NOT ONCE AT t=1s.
    # EP62 greene passed pre-flight, the 60s probe, the post-render gate, forty acceptance
    # checks and the pool QC, and still shipped a modern US election ballot (filed
    # `person_holding_papers`) and a 2011 Range Rover Evoque on an EU plate (filed
    # `playground`) into a film about 1975 Louisville. Re-measured 2026-08-11: BOTH defects
    # are visible in the single t=1s frame the old pool sheet already took. They survived
    # because the verdict was recorded PER SHEET -- "somebody opened sheet 03" cleared twenty
    # clips -- and because nothing bound that review to the pool it was made against.
    # check_pool_frames.py requires a verdict for EVERY clip, bound by a hash of the pool id
    # list. pool_state() reads a directory listing and one json -- no ffmpeg, no decode.
    try:
        from check_pool_frames import pool_state
        _ps = pool_state(pub / "factory", verdicts, spec)
        if not _ps["ok"]:
            problems.extend(_ps["problems"])
        else:
            notes.append(_ps["reason"])
    except Exception as exc:  # noqa: BLE001
        # Fail closed. "The check could not run" is not "the pool was reviewed" -- that
        # conflation is what let seven object stills pass as people plates above.
        problems.append(f"the pool-frame review could not be checked ({type(exc).__name__}: "
                        f"{exc}) -- run scripts/check_pool_frames.py --slug {slug} --state")

    # AND THE SAME QUESTION, ASKED OF THE GENERATED PLATES.
    # Measured 2026-08-11: check_pool_frames blocks a build on unreviewed ARCHIVE FOOTAGE, and
    # nothing whatever blocked one on unreviewed GENERATED PLATES -- check_pool_faces and
    # qc_delivered_plates are wired into nothing at all. Every EP66 plate defect came through
    # that hole: a round pole where the callback needed a squared post (L170), a manufacturer
    # wordmark that survived two [NEG] bans (L146), fused fingers on a hand that had already
    # been re-ordered once to fix them (L236). Each was found because somebody was asked to
    # look, never because a gate refused. check_plate_verdicts.py requires a resolved verdict
    # for EVERY plate in the set, bound BOTH by a hash of the id list and by each file own
    # sha256 -- a plate is regenerated under its own id, so the id list alone would carry the
    # old verdict onto a new picture. Directory listing, one json, cached digests; no decode.
    try:
        from check_plate_verdicts import plate_state
        _pv = plate_state(slug, spec)
        if not _pv["ok"]:
            problems.extend(_pv["problems"])
        else:
            notes.append(_pv["reason"])
    except Exception as exc:  # noqa: BLE001
        # Fail closed, for the same reason as above: "the check could not run" is not "the
        # plates were reviewed".
        problems.append(f"the plate review could not be checked ({type(exc).__name__}: "
                        f"{exc}) -- run scripts/check_plate_verdicts.py --slug {slug}")

    # AND THE DOCUMENTS A HUMAN BUILDS FROM MUST STATE THE NUMBERS THE MACHINE READS.
    # CLAUDE.md s4.6 makes episode_spec the only place a TOOL reads a number from; it does not
    # stop the prose from stating a different one, and the prose is what a person works to.
    # Measured 2026-08-11: EP66 openfields carries eleven statements of target_cut_sec 3.5,
    # people_plates_min 10 and mandatory_stills 65 across four documents against a spec that
    # says 3.1, 20 and 185, and EP67 ramirez states mandatory_stills 96 against 122. The
    # comparison lives in check_design_doc.py, which reads both; it is CALLED here because this
    # file is on the path that blocks a build and that one is not.
    try:
        from check_design_doc import spec_document_drift
        _drift = spec_document_drift(slug)
        if _drift:
            problems.extend(_drift)
        else:
            notes.append("design documents state no number that contradicts episode_spec")
    except Exception as exc:  # noqa: BLE001
        problems.append(f"the design-document / spec comparison could not run "
                        f"({type(exc).__name__}: {exc}) -- run "
                        f"scripts/check_design_doc.py --slug {slug}")

    comp = ROOT / "remotion" / "src" / "Root.tsx"
    if comp.is_file():
        want = f"Ep{num}"
        if not re.search(rf'id="{want}\w*"', comp.read_text(encoding="utf-8")):
            problems.append(f"no Remotion composition id starting with {want} in Root.tsx")

    # AND WHAT THE POST-RENDER GATE WILL SAY, PRINTED WHERE SOMEBODY IS ALREADY LOOKING.
    # This file lists missing INPUTS. It has never said anything about the ~40 acceptance checks
    # that run AFTER the render, and on 2026-08-11 three episodes each surfaced acceptance
    # failures after a 1.6-hour render that were computable from artifacts already on disk --
    # a preflight receipt that was not green, a padding measurement over the narration index, a
    # mux stage that does not stamp the tag sound_layers requires. scripts/predict_acceptance.py
    # runs every acceptance check that can be decided without the mp4 and says CANNOT PREDICT for
    # the rest. It is a FORECAST: it costs about half a minute, it never changes the exit code of
    # this file, and a failure inside it is printed and ignored. --no-forecast skips it.
    if not a.no_forecast:
        try:
            from predict_acceptance import forecast, one_line
            print(one_line(forecast(slug)))
        except Exception as exc:  # noqa: BLE001
            print(f"[forecast] {slug}: unavailable ({type(exc).__name__}: {exc})")

    print(f"[inputs] {slug}: stills={len(stills)} (faces {len(faces)}) factory={len(factory)} "
          f"motion={len(motion)}" + (f" | {'; '.join(notes)}" if notes else ""))
    if problems:
        print(f"[inputs] {slug}: NOT READY -- {len(problems)} problem(s):")
        for p in problems:
            print(f"  - {p}")
        return 1
    print(f"[inputs] {slug}: READY to build")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
