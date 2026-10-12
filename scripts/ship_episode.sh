#!/usr/bin/env bash
# One seat from a finished master to a booked upload.
#
# WHY THIS EXISTS. Taking EP74 itaewon from "master on disk" to "scheduled" on 2026-08-25
# took nine separate commands and about fifteen conversation turns, every one of them the
# same nine commands in the same order. The steps were already scripted individually; what
# was missing was the order, the stop-on-failure, and the refusal to skip the one step that
# is not mechanical. Twelve episodes were queued behind it.
#
# Three phases, because exactly one of them needs a human eye:
#
#   preflight <slug>            before the GPU is spent    -- inputs + i2v clips
#   prepare   <slug>            after the render           -- extract the contact sheets
#      >>> a person reads every sheet and writes the review json <<<
#   ship      <slug> <epnum>    after the sheets are read  -- delivery, receipt, dry run
#   ship      <slug> <epnum> --book                        -- ...and actually upload
#
# WHAT IT WILL NOT DO. It will not write the review for you, it will not upload without
# --book, and it will not continue past a red step. `prepare` deliberately leaves the
# episode in a state that cannot ship: check_shipped_frames records UNREVIEWED and every
# downstream gate refuses until a real review json exists, bound to the render's sha256.
# That is the gate that caught the wrong-country footage in EP74, and no wrapper gets to
# be clever about it.
set -uo pipefail

PY="py -3.11"
MODE="${1:-}"
SLUG="${2:-}"
EPNUM="${3:-}"
BOOK="${4:-}"

die() { echo; echo "!! $*"; exit 1; }
step() { echo; echo "=== $* ==="; }
run() { echo "\$ $*"; "$@" || die "failed: $*"; }

[ -n "$MODE" ] && [ -n "$SLUG" ] || die "usage: ship_episode.sh {preflight|prepare|ship} <slug> [epnum] [--book]"

case "$MODE" in

preflight)
  step "1/2 inputs -- every missing input in one pass"
  $PY scripts/check_episode_inputs.py --slug "$SLUG" | tail -4
  step "2/2 i2v clips -- black heads and colour collapse, BEFORE the 2.5h render"
  $PY scripts/check_motion_saturation.py --slug "$SLUG" || die \
"a clip is black or grey. Do NOT render. Quarantine it out of remotion/public/$SLUG/motion
   AND out of E:/pd-media/assets/ai_video/$SLUG/motion (the archive restores what you remove),
   move its frame dir OUT of ae-demo (renaming it in place makes the assembler rebuild the
   same clip under the new name), and add it to config/footage_blocklist.v001.json 'blocked'
   with an episodes scope -- 'quality_deferred' binds nothing."
  echo
  echo "preflight clean. Render with: bash scripts/_finish_episode.sh $SLUG <Composition> <NN>"
  ;;

prepare)
  step "1/2 which master will be measured"
  OUT=$($PY scripts/check_shipped_frames.py --slug "$SLUG" --which-master 2>&1) || true
  echo "$OUT"
  MASTER=$(echo "$OUT" | sed -n 's/^\[which-master\].*would measure \(.*\)$/\1/p' | head -1)
  [ -n "$MASTER" ] || die "could not resolve the master from --which-master"
  step "2/2 extract frames and tile them (this discards sheets from a previous master)"
  run $PY scripts/check_shipped_frames.py --slug "$SLUG" --sheets-only --force
  SHA=$($PY -c "
import hashlib,sys
h=hashlib.sha256()
with open(r'$MASTER','rb') as f:
    for b in iter(lambda: f.read(8<<20), b''): h.update(b)
print(h.hexdigest())")
  echo
  echo "-------------------------------------------------------------------"
  echo "NOW READ EVERY SHEET IN runs/qc/shipped_frames/$SLUG, tile by tile."
  echo "About 55 of them, about 35 minutes. This is the step that is not mechanical."
  echo "Look for: wrong-country footage (the absence of the local language is itself a"
  echo "tell), held identifiable faces, bodies, readable documents or logos, depth maps"
  echo "used as picture, numeric cards reading NaN, and footage that contradicts the line"
  echo "it runs under."
  echo
  echo "Then write runs/qc/${SLUG}_shipped_frames_review.v001.json with:"
  echo "    render_sha256   $SHA"
  echo "    render          $MASTER"
  echo "    reviewed_sheets [every sheet path]"
  echo "    verdict         PASS   (and 'rejected' for anything that must not ship)"
  echo "-------------------------------------------------------------------"
  ;;

ship)
  [ -n "$EPNUM" ] || die "ship needs the episode number: ship_episode.sh ship $SLUG 75 [--book]"
  REVIEW="runs/qc/${SLUG}_shipped_frames_review.v001.json"
  [ -f "$REVIEW" ] || die "$REVIEW does not exist. Run 'prepare' and read the sheets first."

  step "1/6 the sheets were read, and read against THESE bytes"
  run $PY scripts/check_shipped_frames.py --slug "$SLUG"

  step "2/6 point final_delivery at the master that was just reviewed"
  OUT=$($PY scripts/check_shipped_frames.py --slug "$SLUG" --which-master 2>&1) || true
  MASTER=$(echo "$OUT" | sed -n 's/^\[which-master\].*would measure \(.*\)$/\1/p' | head -1)
  [ -n "$MASTER" ] || die "could not resolve the master"
  run $PY scripts/write_final_delivery.py --slug "$SLUG" --render "$MASTER"

  step "3/6 acceptance receipt, bound to the render sha (about 12 minutes)"
  $PY scripts/check_final_acceptance.py "$EPNUM" --emit-receipt | tail -30
  echo "(a FAIL here is expected and does not stop a ship -- only the four policy classes do)"

  step "4/6 what the ship policy decides, and why"
  $PY scripts/upload_schedule_case_v001.py --ep "$SLUG" --explain-policy \
    | grep -E '^\[policy\] (episode|decision)|UNMEASURED-BLOCKING|BLOCKING' || true
  DEC=$($PY scripts/upload_schedule_case_v001.py --ep "$SLUG" --explain-policy 2>&1 \
        | grep -oE 'decision=[a-z]+' | tail -1)
  [ "$DEC" = "decision=permit" ] || die "policy says $DEC -- read the blocking rows above"

  step "5/6 dry run"
  $PY scripts/upload_schedule_case_v001.py --ep "$SLUG" --dry-run | tail -8 \
    || die "dry run refused"

  if [ "$BOOK" != "--book" ]; then
    echo
    echo "Stopped before uploading. Read the TITLE against the film first -- a green from"
    echo "check_packaging_claims is not a substitute, and the policy says so itself."
    echo "Then: bash scripts/ship_episode.sh ship $SLUG $EPNUM --book"
    exit 0
  fi

  step "6/6 upload and schedule"
  $PY scripts/upload_schedule_case_v001.py --ep "$SLUG" | tail -6 || die "upload failed"
  echo
  step "verify on the channel -- the channel is the truth, not our manifest"
  $PY scripts/yt_video_status.py --slug "$SLUG" | head -5
  ;;

*) die "unknown mode '$MODE' -- use preflight, prepare or ship" ;;
esac
