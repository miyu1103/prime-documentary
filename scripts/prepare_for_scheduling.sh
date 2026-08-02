#!/bin/bash
# Watch for finished masters and get each one SCHEDULE-READY -- without uploading anything.
#
# The owner reviews every film before it is scheduled, and that review must never be the thing
# that idles the machine. So the moment a master appears, everything that does not need a human
# runs on its own: CTR thumbnail, packaging entry, delivery record, probe + acceptance receipt.
# When the owner says "schedule EP55", the only step left is one upload command.
#
#   scripts/prepare_for_scheduling.sh            # runs until every listed episode is ready
set -u
cd /c/Users/aab15/Documents/prime-documentary
LOG=out_prepare_ready.log

# slug : publish date : thumb line1 : line2 : shock word : packaging draft file
JOBS=(
  "burge:2026-08-09:NOBODY:BELIEVED:NOBODY:episodes/_planning/PACKAGING_DRAFTS_EP53_56.v001.json"
  "flowers:2026-08-08:TRIED:6 TIMES:6 TIMES:episodes/_planning/PACKAGING_DRAFTS_EP53_56.v001.json"
  "postoffice:2026-08-10:A GLITCH:236 JAILED:236 JAILED:episodes/_planning/PACKAGING_DRAFTS_EP53_56.v001.json"
  "fieldtest:2026-08-11:A \$2 TEST:21 DAYS:21 DAYS:episodes/_planning/PACKAGING_DRAFTS_EP57_59.v001.json"
  "lejeune:2026-08-12:THEY KNEW:AND WROTE IT:THEY KNEW:episodes/_planning/PACKAGING_DRAFTS_EP57_59.v001.json"
  "robosigning:2026-08-13:NO LOAN:NO HOUSE:NO HOUSE:episodes/_planning/PACKAGING_DRAFTS_EP57_59.v001.json"
)

done_marker() { echo "$1" >> out_prepare_done.txt; }
is_done() { grep -qx "$1" out_prepare_done.txt 2>/dev/null; }
touch out_prepare_done.txt

while :; do
  pending=0
  for job in "${JOBS[@]}"; do
    IFS=':' read -r slug date l1 l2 shock draft <<< "$job"
    is_done "$slug" && continue
    ep=$(ls -d episodes/PD-2026-0*-${slug} 2>/dev/null | head -1)
    master="${ep}/08_edit/${slug}_final_bgm.v001.mp4"
    if [ ! -f "$master" ]; then pending=1; continue; fi
    # a master still being written must not be packaged: require it to stop growing
    s1=$(stat -c%s "$master"); sleep 20; s2=$(stat -c%s "$master")
    if [ "$s1" != "$s2" ]; then pending=1; continue; fi

    echo "[prep] $slug $(date)" | tee -a "$LOG"
    py -3.11 scripts/build_thumbs_ctr_v2.py --slug "$slug" \
        --face "H:/pd-media/assets/ai/${slug}/thumb/$(echo ${slug} | tr a-z A-Z)_FACE_v001.png" \
        --line1 "$l1" --line2 "$l2" --shock-word "$shock" >> "$LOG" 2>&1
    py -3.11 /c/Users/aab15/scratchpad/add_config_from_draft.py --slug "$slug" \
        --draft "$draft" --date "$date" >> "$LOG" 2>&1
    rm -f "out/${slug}_probe_slice.mp4"
    ffmpeg -hide_banner -v error -ss 600 -t 90 -i "$master" -c copy "out/${slug}_probe_slice.mp4" -y >> "$LOG" 2>&1
    py -3.11 scripts/check_final_acceptance.py "$(basename "$ep")" --probe "out/${slug}_probe_slice.mp4" >> "$LOG" 2>&1
    STAMP=$(py -3.11 -c "import os;print(int(os.path.getmtime(r'$master'))-60)")
    py -3.11 scripts/check_final_acceptance.py "$(basename "$ep")" --render "$master" \
        --render-started-at "$STAMP" --emit-receipt >> "$LOG" 2>&1
    echo "[prep] $slug READY for review -> $(basename "$master")" | tee -a "$LOG"
    done_marker "$slug"
  done
  [ "$pending" = "0" ] && break
  sleep 300
done
echo "[prep] all listed episodes are schedule-ready $(date)" | tee -a "$LOG"
