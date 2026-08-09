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
            need = max(MIN_FACTORY, no_reuse // 2)
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

    comp = ROOT / "remotion" / "src" / "Root.tsx"
    if comp.is_file():
        want = f"Ep{num}"
        if not re.search(rf'id="{want}\w*"', comp.read_text(encoding="utf-8")):
            problems.append(f"no Remotion composition id starting with {want} in Root.tsx")

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
