"""Write the lahaina shipped-frames review, bound to the master that was actually tiled.

The previous v001 on disk described sha 436a2cb2... -- a master that no longer exists here.
This replaces it with a reading of sha 3503c1fc..., the 1866.43 s / 377-cut film in
08_edit/lahaina_final_bgm.v001.mp4.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QC = ROOT / "runs" / "qc"
SHEETS = QC / "shipped_frames" / "lahaina"

SHA = "3503c1fc07777f8ad8de5d010786557504ff288e476cdb6917a5e377c05fc132"
RENDER = "episodes/PD-2026-075-lahaina/08_edit/lahaina_final_bgm.v001.mp4"

review = {
    "schema_version": "1.0.0",
    "slug": "lahaina",
    "reviewer": (
        "Claude (Opus 5, Claude Code) -- 76 labelled contact sheets read tile by tile, "
        "1,518 frames from 377 cuts, coverage 0:00-31:06. Seven frames that the tile scale "
        "could not settle were extracted from the master at full resolution and read "
        "individually: 280s, 599s, 735s, 1005s, 177s, 1697s, 1845s."
    ),
    "reviewed_at": "2026-08-26",
    "render": RENDER,
    "render_sha256": SHA,
    "reviewed_sheets": [
        f"runs/qc/shipped_frames/lahaina/lahaina_shipped_frames_{i:02d}.png"
        for i in range(1, 77)
    ],
    "verdict": "PASS",
    "verdict_note": (
        "Ships. No frame falls in the four blocking classes of config/ship_policy.v001.json. "
        "Two real defects were found and are recorded below rather than excused: two stock "
        "aerials that are not Hawai'i, and four holds on a generated human face whose features "
        "are fully legible. Neither is a stop under owner policy -- generated people are "
        "permitted and only real-person likeness is not (pd_craft_directives, 2026-07-04), and "
        "a finished 31-minute master is not rebuilt for second-scale defects "
        "(ship_policy / 'Ship, don't polish'). Both are on the fix-before-reuse list."
    ),
    "rejected": {},
    "advisory_findings": {
        "wrong_place_footage": {
            "severity": "record and fix before these clips are reused",
            "why_not_a_rejection": (
                "10.0 s of 1,866 s, 2 cuts of 377. The narration never says the picture is "
                "Lahaina, and no claim in the film rests on it. Re-rendering 31 minutes for "
                "two B-roll shots would cost the 8/27 slot with nothing to put in it."
            ),
            "rows": [
                {
                    "cut": "cut-0205",
                    "t_film_s": 1003.081,
                    "mmss": "16:43",
                    "dur_s": 5.014,
                    "src": "pexels_v_38670817.mp4",
                    "read_at_full_resolution": "1005s",
                    "finding": (
                        "Aerial of a dense hillside town built into steep tropical forest -- "
                        "Latin America by the vegetation, roof forms and terracing. It runs "
                        "under 'Densely populated and narrow roadways hindered the movement', "
                        "a finding about Lahaina, which is a flat coastal town. This is the "
                        "worse of the two: the shot is illustrating a Lahaina-specific claim "
                        "with a picture of somewhere else."
                    ),
                },
                {
                    "cut": "cut-0036",
                    "t_film_s": 174.632,
                    "mmss": "02:54",
                    "dur_s": 4.928,
                    "src": "pexels_v_16083405.mp4",
                    "read_at_full_resolution": "177s",
                    "finding": (
                        "Aerial of a divided highway through red laterite scrub with roadside "
                        "litter -- reads as India or Africa, not Maui. Runs under 'mentioned "
                        "the possibility of Red Flag conditions'. Generic weather/landscape "
                        "line, so nothing factual rests on it."
                    ),
                },
            ],
        },
        "held_generated_faces": {
            "severity": "record; permitted by owner directive",
            "why_not_a_rejection": (
                "Owner directive 2026-07-04 (pd_craft_directives): people in generated images "
                "are fine, only real-person portraits are forbidden. None of these is a real "
                "person, none is named, none is presented as anyone in the record. They are "
                "logged because the plate review's note is boilerplate (see detector_gap) and "
                "because the itaewon standard shipped with zero held faces."
            ),
            "rows": [
                {"cut": "cut-0374", "mmss": "30:43", "dur_s": 5.01, "src": "H088.mp4",
                 "finding": "Man in a dark suit against a concrete wall, face fully legible, "
                            "held ~5 s under the closing line 'and it has been on a public "
                            "page the whole time.' Also a content mismatch: the picture has "
                            "nothing to do with the sentence."},
                {"cut": "cut-0150", "mmss": "12:13", "dur_s": 4.947, "src": "H088.mp4",
                 "finding": "Same clip, same legible face, under 'Embers are made by whatever "
                            "is burning and carried by the wind.' Content mismatch."},
                {"cut": "cut-0344", "mmss": "28:15", "dur_s": 5.053, "src": "H072.mp4",
                 "finding": "Man in a dark suit in a dim lounge, face legible. Under a line "
                            "about settlement instalments."},
                {"cut": "cut-0122", "mmss": "09:56", "dur_s": 4.984, "src": "H072.mp4",
                 "finding": "Same clip under '14:17. REPORTED OUT.' and 'the shelter at the "
                            "Lahaina Civic Center closed'. A suited man in a hotel lounge is "
                            "not what that sentence is about."},
            ],
        },
    },
    "prohibition_checks": {
        "real_person_likeness": (
            "No depiction of any real, named or recognisable person. Four holds on generated "
            "faces are listed under held_generated_faces; none resembles a public figure and "
            "none is attached to a named individual in the narration. The county administrator "
            "and the Attorney General are quoted in type cards, never depicted."
        ),
        "rights_and_licence": (
            "Every cut is either a pexels asset or an episode-scoped generated plate/i2v clip. "
            "No third-party logo, broadcaster bug, watermark or news chyron in any of the "
            "1,518 frames. Generated material carries the on-screen 'AI-assisted visualization "
            "-- symbolic reconstruction, no real likenesses' badge (seen at 30:12 and "
            "throughout)."
        ),
        "factual_support": (
            "Every numeric card resolves to a real number and matches the narration: 60 mph "
            "gusts (4:40), 102 dead, 470->518 pages, 82->84 findings, 140 recommendations, "
            "850 GB, $4.037 billion. No NaN, no blank, no placeholder in any card. The 'By the "
            "numbers' counters animate up from 0, so a low intermediate value on a tile is the "
            "animation, not a wrong figure. Quote cards attribute to FSRI findings by number."
        ),
        "fabricated_record": (
            "No generated document, judgment, licence, news page or screen resolves into "
            "legible glyphs. Paper appears blank (25:57, 28:46), notice boards are empty "
            "(23:15), monitors are dark or blank (22:20, 29:53), phones show a white screen "
            "(25:01, 29:42). Nothing on screen purports to be a real record."
        ),
    },
    "coverage": {
        "sheets": 76,
        "frames": 1518,
        "cuts": 377,
        "span": "0:00-31:06 of a 1866.43 s master",
        "widest_unsampled_gap_s": 3.60,
        "depth_maps_used_as_picture": 0,
        "nan_or_placeholder_cards": 0,
    },
    "detector_gaps": [
        "runs/qc/lahaina_plate_verdicts.v001.json marks all 135 plates 'accept' with one "
        "identical boilerplate note, including H088/H072/H032, whose faces are fully legible. "
        "The note asserts 'no identifiable real person' -- true as written, but it cannot be "
        "read as evidence anyone looked at those three, since the same sentence covers all 135.",
        "Wrong-place footage has no machine check anywhere in the ship path. Both rows above "
        "were found only by a human opening the frame; check_motion_saturation, "
        "check_spec_satisfied and the post-render gate all pass this master.",
    ],
    "next": (
        "Before pexels_v_38670817 or pexels_v_16083405 is used again, in this episode or any "
        "other, replace it -- neither is Hawai'i. If lahaina is ever re-rendered for another "
        "reason, swap cut-0205 and cut-0036 in the same pass, and re-cut cut-0150/cut-0374 "
        "(H088) and cut-0122/cut-0344 (H072) to something that matches the line."
    ),
}

out = QC / "lahaina_shipped_frames_review.v001.json"
missing = [s for s in review["reviewed_sheets"] if not (ROOT / s).is_file()]
if missing:
    raise SystemExit(f"{len(missing)} named sheet(s) are not on disk: {missing[:3]}")
out.write_text(json.dumps(review, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"wrote {out} ({len(review['reviewed_sheets'])} sheets, verdict {review['verdict']}, "
      f"sha {SHA[:16]})")
