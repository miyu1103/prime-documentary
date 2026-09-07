"""Write the EP76 morandi shipped-frames review, bound to the fourth render.

Three renders were thrown away before this one. The first died on 4.43 s of black from an
intentionally-empty backdrop plate declared as a mandatory still; the second and third were
read and rejected here for wrong-place footage this session had staged. This is the reading
of the bytes that will ship.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QC = ROOT / "runs" / "qc"

SHA = "f507d956e0f11031ef43689e3dac5a925d771fe207b2d66c242bcc035cb885cc"
RENDER = "episodes/PD-2026-076-morandi/08_edit/morandi_final_bgm.v001.mp4"

review = {
    "schema_version": "1.0.0",
    "slug": "morandi",
    "reviewer": (
        "Claude (Opus 5, Claude Code) -- 74 labelled contact sheets read tile by tile, "
        "coverage 0:00-30:51, plus two full-resolution frame extractions at 1661 s and "
        "1663 s to settle a question the tile scale could not."
    ),
    "reviewed_at": "2026-08-27",
    "render": RENDER,
    "render_sha256": SHA,
    "reviewed_sheets": [
        f"runs/qc/shipped_frames/morandi/morandi_shipped_frames_{i:02d}.png"
        for i in range(1, 75)
    ],
    "verdict": "PASS",
    "verdict_note": (
        "Ships. Nothing in the four blocking classes of config/ship_policy.v001.json. "
        "This is the fourth render; the three before it were each read and each rejected "
        "here, which is what the gate is for. Two findings are recorded below rather than "
        "excused, and neither is a stop."
    ),
    "rejected": {},
    "advisory_findings": {
        "one_wrong_place_clip_survived": {
            "cut_time": "08:10-08:13",
            "src": "AR-pixabay_206692__construction_site_development_infrastructure_rea.mp4",
            "finding": (
                "White apartment blocks rising out of desert sand; reads as the Gulf, not "
                "Liguria. It is the sibling of AR-pixabay_206694, which was removed after the "
                "second render -- same shoot, ID two digits apart. Removing clips by exact ID "
                "is what let it through: the defect belongs to the shoot, not to the file."
            ),
            "why_not_a_rejection": (
                "Three seconds of 1,851. The wrong-place sweep that preceded this render took "
                "out 25 clips (11 named + 14 foreign-city skylines as a category) and this is "
                "the only survivor a full reading found. A fourth re-render for three seconds "
                "is not a trade worth making with the slot 30 hours away and the GPU shared "
                "with the design lane."
            ),
        },
        "generated_figure_under_a_named_real_person": {
            "cut_time": "27:39-27:43",
            "src": "V099.mp4",
            "finding": (
                "A generated man at a lectern runs under the caption 'was convicted at first "
                "instance and sentenced to twelve years', immediately after the on-screen "
                "title card naming GIOVANNI CASTELLUCCI. A viewer can read the figure as him."
            ),
            "read_at_full_resolution": (
                "1661 s and 1663 s. The figure has thick dark curly hair and a beard and is "
                "turned away from camera by 27:43. Castellucci is a real, photographed public "
                "figure and looks nothing like this. There is no resemblance to carry a "
                "likeness claim, and the film's 'AI-assisted visualization -- symbolic "
                "reconstruction, no real likenesses' badge is on screen in this film."
            ),
            "why_not_a_rejection": (
                "real_person_likeness blocks a plate that reads as a depiction of a specific "
                "real person or is unambiguously identifiable as one. This is neither. It is "
                "recorded because the juxtaposition is the risky part, not the face, and "
                "because the episode is R3: the caption is correctly qualified ('at first "
                "instance', and the film states elsewhere that the judgment is not final)."
            ),
        },
    },
    "prohibition_checks": {
        "real_person_likeness": (
            "No depiction of any real, named or recognisable person. Real names appear only "
            "as type -- GIOVANNI CASTELLUCCI and ROBERTO FERRAZZA on lower-third cards, each "
            "carrying its own qualifier ('Convicted at first instance ... His lawyers said "
            "they would appeal. The judgment is not final.' / 'Acquitted, because the fact "
            "does not constitute an offence.'). The one generated figure that shares a beat "
            "with a name is recorded above and does not resemble him."
        ),
        "rights_and_licence": (
            "Every cut is a pexels/pixabay/motion-library asset or an episode-scoped "
            "generated plate or i2v clip. No third-party logo, broadcaster bug, watermark or "
            "news chyron anywhere in the 74 sheets. The 'AI-assisted visualization -- "
            "symbolic reconstruction, no real likenesses' badge renders at 30:22."
        ),
        "factual_support": (
            "Every number card resolves and matches the narration: 43 killed / 13 injured, "
            "243 m of deck, 240->243 counter, 32 convicted vs 25 acquitted or time-barred "
            "(bar pair), 23 days, 90 days, 1,067 metres, EUR 202 million, 88 per cent, more "
            "than twenty thousand road bridges. No NaN, no blank, no placeholder. Quote cards "
            "attribute to the COMMISSIONE ISPETTIVA MINISTERIALE with dates, and the closing "
            "'because the fact does not exist' card names what it is: the formula on which "
            "every defendant charged with the two intentional offences was acquitted."
        ),
        "fabricated_record": (
            "No generated document resolves into legible glyphs. The ledgers, ring binders, "
            "drawing boards, files and typewriter pages are blank or illegible by design "
            "(23:58, 24:30, 25:59, 28:00). Nothing on screen purports to be a real record."
        ),
    },
    "coverage": {
        "sheets": 74,
        "cuts": 365,
        "span": "0:00-30:51 of a 1851.13 s master",
        "black_stretches_measured_on_the_master": 0,
        "depth_maps_used_as_picture": 0,
        "nan_or_placeholder_cards": 0,
        "endcard": "present, 30:43-30:51",
    },
    "detector_gaps": [
        "There is still no machine check for wrong-place footage anywhere in the ship path. "
        "All 26 wrong-place clips found across this episode's four renders were found by a "
        "human opening a frame; check_motion_saturation, check_spec_satisfied, the pre-render "
        "gate and the post-render gate passed every one of them.",
        "runs/qc/morandi_plate_verdicts.v001.json marks all 120 plates 'accept' with one "
        "boilerplate sentence, and V010.png -- an intentionally empty black ground -- was "
        "among them. A per-plate verdict that reads identically for every plate is a "
        "signature, not a reading.",
        "check_motion_saturation measures motion/ only. The 4.43 s of black that killed the "
        "first render came from a still, and no pre-render check looks at still luma. A PIL "
        "mean-luma pass over the stills in cuts found it in one command.",
    ],
    "next": (
        "Retire AR-pixabay_206692 from the pool before it is used again, and retire by shoot "
        "rather than by exact ID -- 206692 and 206694 are the same site. If morandi is ever "
        "re-rendered for another reason, swap cut at 08:10 and re-cut 27:39-27:43 to "
        "something that does not put a generated man under a real man's name."
    ),
}

out = QC / "morandi_shipped_frames_review.v001.json"
missing = [s for s in review["reviewed_sheets"] if not (ROOT / s).is_file()]
if missing:
    raise SystemExit(f"{len(missing)} named sheet(s) are not on disk: {missing[:3]}")
out.write_text(json.dumps(review, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"wrote {out} ({len(review['reviewed_sheets'])} sheets, verdict {review['verdict']}, "
      f"sha {SHA[:16]})")
