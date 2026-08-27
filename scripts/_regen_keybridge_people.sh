#!/usr/bin/env bash
# EP77 keybridge -- regenerate the 17 i2v clips that still invent a person.
#
# WHY. keybridge publishes 2026-08-31 and it names people who have been charged with crimes.
# A full comparison of all 128 clips against their own plates on 2026-08-27 found:
#
#   * the 30 clips reported as regenerated ARE clean, and provably so: runs/qc/keybridge_person_v1/
#     holds the archived originals and all 30 differ by sha256 from what is in motion/ now.
#   * SEVENTEEN OTHERS were never touched. Every one carries an invented person or limb, and
#     five of those resolve a face into recognisable features. The original run's real rate was
#     47 of 111 -- 42 per cent, not the 27 per cent that was reported. The fix worked; the
#     identification undercounted.
#
# H123 is the one to look at if this ever needs justifying again: its plate is an empty
# switchgear room, and at 2.23 s a middle-aged man stands at the panel with hair, brow, eye
# sockets, nose, mouth, jaw and stubble all resolved. Verified by eye against the plate.
#
# The prompt below is the explicit one, measured at 1 invented person in 188 clips (0.53%) on
# EP81 station, against 27-42% for the default. Its one known gap: it suppresses ADDING people
# but not COMPLETING AN IMPLIED ACTION -- station's single failure was a hand reaching for an
# object the plate left within reach.
#
#   bash scripts/_regen_keybridge_people.sh
#
# The originals are already archived in runs/qc/keybridge_person_v2/. After this runs, compare
# again before believing it: a regeneration is a claim until the pixels are read.
set -euo pipefail
cd "$(dirname "$0")/.." || exit 1

SLUG=keybridge
ONLY="H002,H004,H010,H017,H020,H050,H052,H060,H066,H076,H081,H083,H088,H091,H098,H106,H123"

BASE_PROMPT="the scene stays exactly as it is, only ambient motion: haze and air drift slowly, water surface ripples, light flickers gently, a very slow subtle camera push-in, archival documentary footage, nothing new enters the frame"

# The negative is the EP78-82 chain's, minus nothing: it is what produced 0.53%. Note the
# recorded trap -- a people-forbidding negative also erases people who are ALREADY in the
# plate (EP77 H146 lost a worker's arm to it). Every one of these 17 plates is empty of
# people, which is exactly why the invention is visible, so the negative is safe here.
NEG="new person, people appearing, man appearing, woman appearing, human face, crowd, walking figure, silhouette of a person, animal, bird, dog, vehicle entering frame, new object appearing, text, lettering, caption, subtitle, watermark, logo, signature, readable writing, morphing, warping, deformed, extra limbs, bad anatomy, cartoon, illustration, low quality, jitter, scene change, cut to another shot"

echo "$(date '+%H:%M:%S') regenerating $(echo "$ONLY" | tr ',' '\n' | wc -l) clip(s) for $SLUG"
I2V_SRC="$(pwd)/remotion/public/${SLUG}/img" \
I2V_PROMPT="$BASE_PROMPT" \
I2V_NEG="$NEG" \
  scripts/_chain_i2v_robust.sh "$SLUG" 128 H 12 "$ONLY"
echo "$(date '+%H:%M:%S') done. NOW RE-COMPARE -- do not trust this without reading the pixels:"
echo "  py -3.11 scripts/qc_i2v_strip_vs_plate.py --slug $SLUG --only $ONLY"
