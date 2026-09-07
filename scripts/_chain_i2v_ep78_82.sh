#!/bin/bash
# EP78-EP82 i2v queue -- five episodes, one GPU, strictly serial.
#
#   scripts/_chain_i2v_ep78_82.sh
#
# Order is the one the design lane asked for in docs/handover/EP78_82_TO_I2V.md:
#   80 concordia -> 81 station -> 82 valdez -> 78 colgan -> 79 alaska261
# 80/81/82 have ZERO live footage, so i2v is their only video source; they go first.
#
# This wraps scripts/_chain_i2v_robust.sh; it does not reimplement it. What it adds:
#   1. It WAITS for the GPU. _chain_i2v_robust.sh refuses (exit 0) when another slug holds
#      out_gpu_comfy.lock, so calling it blind would look like success and silently skip an
#      episode. EP77 keybridge is on the card when this is launched.
#   2. Per-episode motion prompt and negative prompt. The batch's built-in SCENE_PROMPT asks
#      for an "atmospheric living environment" and comfy_wan negates "static, motionless";
#      together they invite Wan to POPULATE the frame (measured: a man in a suit on a blank
#      concrete wall, a woman's face at a kerbside). Every episode here forbids 125-155
#      subject classes, so what may move is stated explicitly and what may not is negated.
#   3. Progress is counted from the delivered mp4s in remotion/public/<slug>/motion/, never
#      from a tool's exit code.
#   4. Between episodes -- and only when no chain holds the GPU -- spent frame dirs are
#      reclaimed, because 920 clips x 57 MB would not fit on the 134 GB free at launch.
#   5. check_motion_saturation.py runs per slug and its exit code is recorded.
#
# Never touches remotion/public/<slug>/img or factory/. motion/ only.
set -u
cd /c/Users/aab15/Documents/prime-documentary

LOG=out_i2v_ep78_82.log
STATUS=out_i2v_ep78_82.status
GPU_LOCK=out_gpu_comfy.lock

say(){ echo "[queue] $(date '+%m-%d %H:%M:%S') $*" | tee -a "$LOG"; }

# What may move, in every one of the five. Nothing new enters the frame.
BASE_PROMPT="the scene stays exactly as it is, only ambient motion: haze and air drift slowly, water surface ripples, light flickers gently, a very slow subtle camera push-in, archival documentary footage, nothing new enters the frame"
BASE_NEG="new person, people appearing, man appearing, woman appearing, human face, crowd, walking figure, silhouette of a person, animal, bird, dog, vehicle entering frame, new object appearing, text, lettering, caption, subtitle, watermark, logo, signature, readable writing, morphing, warping, deformed, extra limbs, bad anatomy, cartoon, illustration, low quality, jitter, scene change, cut to another shot"

# Episode-specific bans, taken from episodes/<EPID>/episode_spec.v001.json forbidden_subjects.
# The event itself is forbidden in all five: the film never shows the accident happening.
neg_for(){
  case "$1" in
    concordia) echo "$BASE_NEG, capsized ship, listing ship, ship on its side, ship rolling over, collision, sinking ship, wreck, salvage, rescue boat, lifeboat launching, person in the water, body" ;;
    station)   echo "$BASE_NEG, fire, flames, open flame, burning building, smoke, sparks, pyrotechnics, band on stage, concert crowd, panic, trampled, charred ruins, rubble, firefighter" ;;
    valdez)    echo "$BASE_NEG, oil spill, spreading oil slick, oil pouring, oiled bird, oiled animal, dead animal, ship aground, ship on a reef, hull breach, tanker breaking, ship name painted on hull, company logo, funnel markings" ;;
    colgan)    echo "$BASE_NEG, crash, impact, explosion, fire, burning house, burning wreckage, falling airplane, crash site" ;;
    alaska261) echo "$BASE_NEG, crash, impact, explosion, debris field, wreckage, airplane inverted, airplane diving, falling airplane, splash on the water, crash site" ;;
    # Added 2026-08-30 with the queue. Each of these three episodes has a signature FALSE
    # image that i2v reaches for unprompted, and each is named in its own forbidden_subjects.
    max737)    echo "$BASE_NEG, crash site, wreckage, debris field, impact crater, burning aircraft, aircraft on fire, fireball, explosion, aircraft breaking up, aircraft falling, nose dive, cockpit alarm light, airline livery, tail registration, manufacturer marking" ;;
    threemile) echo "$BASE_NEG, explosion, fireball, mushroom cloud, burning reactor, reactor on fire, melting floor, green glow, glowing rods, glowing water, radioactive slime, mutation, black smoke from a cooling tower, smoke from a cooling tower, flat screen monitor, laptop, mobile phone, LED lighting, modern car" ;;
    katrina)   echo "$BASE_NEG, drowning, person in water, person on a roof, rooftop rescue, person being rescued, person wading, identifiable face, family photograph, portrait, child, school bus, buses in floodwater, abandoned bus, helicopter rescue basket, superdome crowd" ;;
    *)         echo "$BASE_NEG" ;;
  esac
}

# slug:kind:target -- target is the plate count measured on disk (depth excluded).
#
# REWRITTEN 2026-08-30. The old queue was
#   "concordia:N:185 station:S:188 valdez:V:183 colgan:C:166 alaska261:K:198"
# and it was wrong twice over. It STOPPED AT alaska261, so max737, threemile and katrina --
# the 9/6, 9/7 and 9/8 slots -- would have sat at zero i2v while 54 hours of GPU ran on the
# five episodes above them, and nobody would have noticed until their render day. And every
# target was the pre-review plate count: 49 plates were rejected across these episodes on
# 08-27 (an Alaska Airlines emblem, Chernobyl's sarcophagus, the Twin Towers, three generator
# watermarks, empty grounds), so a chain aiming at the old numbers hunts plates that are no
# longer on disk.
#
# Counts below are `ls img/*.png | grep -v _depth | wc -l` on 2026-08-30 17:xx.
# concordia and station are done (182/185 and 183/184) and are left in so the chain's own
# resume logic confirms it rather than taking my word; each costs one pass of the pending
# check and no GPU.
QUEUE="concordia:N:185 station:S:184 valdez:V:179 colgan:C:156 alaska261:K:190 max737:X:184 threemile:T:181 katrina:W:173"

delivered(){ ls "remotion/public/$1/motion/"*.mp4 2>/dev/null | grep -v '_depth' | wc -l | tr -d ' '; }

# Frame dirs that already carry a finished clip's worth of pngs. This is the SAME thing the
# inner chain's count_done() measures, and it is why the inner loop has to be given a target it
# can actually reach. MEASURED 2026-08-30: concordia took 34 minutes to make its last TWO clips.
# count_done() counts /c/Users/aab15/ae-demo/wan_frames_<slug>_*, but THIS script runs
# reclaim_i2v_frames.py --apply, which deletes the frame dir of every clip whose mp4 is already
# on disk. So after a reclaim count_done reported 2 against a TARGET of 185, never converged, and
# ran all 60 attempts -- restarting ComfyUI on each one -- before giving up. Roughly 20-28 wasted
# minutes per episode, about three hours across the eight, and ~45 needless ComfyUI restarts.
# The inner chain is invoked with --only, so the most it can ever reach is
# (frames already present) + (plates we asked for). Give it that.
frames_present(){
  local n=0 d
  for d in /c/Users/aab15/ae-demo/wan_frames_$1_*; do
    [ -d "$d" ] || continue
    if [ "$(ls "$d"/*.png 2>/dev/null | wc -l)" -ge 40 ]; then n=$((n + 1)); fi
  done
  echo "$n"
}

# POISON PLATES. Measured 2026-08-26 on concordia N093: ComfyUI accepted the prompt, wrote
# ZERO files to output/wanout, and comfy_wan polled a job that never produced anything until
# i2v_episode_batch's 600 s clip timeout fired and exited the chunk. Because is_done() is false
# for it, N093 is first in the todo list of the NEXT chunk too -- so every chunk burns 600 s on
# the same plate and delivers nothing. Two rounds went that way before it was caught.
# A stem that times out twice is quarantined, the rest of the episode proceeds, and the
# quarantined stems are reported at the end for a deliberate re-roll (different --seed-base).
quarantine_file(){ echo "runs/qc/i2v_quarantine_$1.txt"; }

is_quarantined(){ [ -f "$(quarantine_file "$1")" ] && grep -qx "$2" "$(quarantine_file "$1")"; }

# Every plate that has no mp4 yet and is not quarantined, as a comma list for the chain's
# 5th positional argument (--only). Without this the batch would re-attempt the poison plate.
pending_only(){
  local slug="$1" kind="$2" out="" stem
  for p in "remotion/public/$slug/img/$kind"*.png; do
    [ -f "$p" ] || continue
    stem=$(basename "$p" .png)
    case "$stem" in *_depth) continue ;; esac
    [ -f "remotion/public/$slug/motion/$stem.mp4" ] && continue
    is_quarantined "$slug" "$stem" && continue
    out="${out:+$out,}$stem"
  done
  echo "$out"
}

# Read the chain's own log back and quarantine anything that timed out twice.
harvest_timeouts(){
  # Two statements, not one: under `set -u` a later assignment in the SAME `local` cannot
  # read an earlier one, and `log="out_i2v_${slug}.log"` killed the queue at 20:15 on 2026-08-26.
  local slug="$1" kind="$2" qf stem n
  local log="out_i2v_${slug}.log"
  [ -f "$log" ] || return 0
  qf=$(quarantine_file "$slug")
  grep -oE "\] ${kind}[0-9]+ TIMEOUT" "$log" 2>/dev/null | awk '{print $2}' | sort | uniq -c \
  | while read -r n stem; do
      if [ "$n" -ge 2 ] && ! is_quarantined "$slug" "$stem"; then
        echo "$stem" >> "$qf"
        say "$slug: QUARANTINE $stem -- timed out ${n}x, produced no frames"
      fi
    done
}

gpu_held_by_other(){
  local me="$1"
  [ -f "$GPU_LOCK" ] || return 1
  local pid slug
  pid=$(cut -d' ' -f1 "$GPU_LOCK" 2>/dev/null)
  slug=$(cut -d' ' -f2 "$GPU_LOCK" 2>/dev/null)
  [ -n "$pid" ] || return 1
  kill -0 "$pid" 2>/dev/null || return 1     # stale lock: the holder is gone
  [ "$slug" = "$me" ] && return 1            # our own chain
  return 0
}

wait_for_gpu(){
  local me="$1" waited=0
  while gpu_held_by_other "$me"; do
    if [ $((waited % 600)) -eq 0 ]; then
      say "waiting for GPU: '$(cut -d' ' -f2 "$GPU_LOCK")' is on the card (${waited}s)"
    fi
    sleep 60
    waited=$((waited + 60))
  done
}

# --selftest exercises every helper against the real repo under the real `set -u`, and prints
# numbers a human can check, without touching the GPU. It exists because this script died
# silently TWICE on 2026-08-26 -- once to an external SIGTERM, once to `slug: unbound variable`
# on line 85 -- and both times the only symptom was a log that stopped advancing.
if [ "${1:-}" = "--selftest" ]; then
  for item in $QUEUE; do
    s="${item%%:*}"; r="${item#*:}"; k="${r%%:*}"; t="${r##*:}"
    harvest_timeouts "$s" "$k"
    o="$(pending_only "$s" "$k")"
    n=0; [ -n "$o" ] && n=$(echo "$o" | tr ',' '\n' | wc -l)
    q=0; [ -f "$(quarantine_file "$s")" ] && q=$(wc -l < "$(quarantine_file "$s")")
    echo "selftest $s: plates=$t delivered=$(delivered "$s") quarantined=$q pending=$n first=$(echo "$o" | cut -d, -f1)"
    [ $((n + $(delivered "$s") + q)) -eq "$t" ] || echo "  !! pending+delivered+quarantined != plates"
  done
  gpu_held_by_other "__selftest__" && echo "selftest gpu: HELD by $(cut -d' ' -f2 "$GPU_LOCK")" \
                                   || echo "selftest gpu: free"
  exit 0
fi

say "START queue=$QUEUE"
echo "queue started $(date)" > "$STATUS"

for item in $QUEUE; do
  SLUG="${item%%:*}"; rest="${item#*:}"; KIND="${rest%%:*}"; TARGET="${rest##*:}"
  SRC="/c/Users/aab15/Documents/prime-documentary/remotion/public/$SLUG/img"

  if [ ! -d "$SRC" ]; then say "$SLUG: SKIP -- no source dir $SRC"; continue; fi

  say "$SLUG: begin kind=$KIND target=$TARGET delivered=$(delivered "$SLUG")"

  # Reclaim spent frames while the card is idle. Only dirs whose mp4 is already on disk.
  if ! gpu_held_by_other "$SLUG"; then
    py -3.11 scripts/reclaim_i2v_frames.py --apply >> "$LOG" 2>&1
  fi

  harvest_timeouts "$SLUG" "$KIND"   # carry over poison plates from an earlier, killed run

  round=0
  while [ $round -lt 30 ]; do
    ONLY="$(pending_only "$SLUG" "$KIND")"
    if [ -z "$ONLY" ]; then
      say "$SLUG: nothing pending (delivered=$(delivered "$SLUG")/$TARGET)"
      break
    fi
    round=$((round + 1))
    wait_for_gpu "$SLUG"
    say "$SLUG: round $round -- $(echo "$ONLY" | tr ',' '\n' | wc -l) plate(s) pending (delivered=$(delivered "$SLUG")/$TARGET)"
    # Not "$TARGET": see frames_present() above. The inner loop runs until count_done
    # reaches the number it is given, and with --only it can never reach the episode's full
    # plate count once reclaim has deleted the finished frame dirs.
    N_ONLY=$(echo "$ONLY" | tr ',' '\n' | wc -l | tr -d ' ')
    INNER_TARGET=$(( $(frames_present "$SLUG") + N_ONLY ))
    I2V_SRC="$SRC" \
    I2V_PROMPT="$BASE_PROMPT" \
    I2V_NEG="$(neg_for "$SLUG")" \
      scripts/_chain_i2v_robust.sh "$SLUG" "$INNER_TARGET" "$KIND" 12 "$ONLY" >> "$LOG" 2>&1
    harvest_timeouts "$SLUG" "$KIND"
    after=$(delivered "$SLUG")
    say "$SLUG: round $round end delivered=$after/$TARGET"
    # A round that delivered nothing AND quarantined nothing means the chain is being killed
    # from outside or the card is gone -- keep looping, but slowly, so a dead card does not
    # spin 30 rounds in a minute and declare the episode finished.
    sleep 30
  done
  QN=0; [ -f "$(quarantine_file "$SLUG")" ] && QN=$(wc -l < "$(quarantine_file "$SLUG")")

  # A depth matte has shipped as picture twice. Prove it did not happen again.
  DEPTH=$(ls "remotion/public/$SLUG/motion/" 2>/dev/null | grep -c '_depth' || true)
  N=$(delivered "$SLUG")
  py -3.11 scripts/check_motion_saturation.py --slug "$SLUG" \
      --json "runs/qc/${SLUG}_motion_saturation.v001.json" >> "$LOG" 2>&1
  SAT=$?
  say "$SLUG: DONE motion=$N/$TARGET depth_in_motion=$DEPTH saturation_exit=$SAT quarantined=$QN"
  echo "$SLUG motion=$N/$TARGET depth=$DEPTH saturation_exit=$SAT quarantined=$QN $(date)" >> "$STATUS"
done

say "QUEUE COMPLETE"
echo "queue complete $(date)" >> "$STATUS"
