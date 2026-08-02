#!/bin/bash
# Finish one episode: i2v output -> manifest -> film.json -> slim public dir -> guarded
# render -> BGM/master-VO remux -> post-render gate. Every stage is checked; the first
# failure stops the chain so nothing downstream is built on a bad input.
#
#   scripts/_finish_episode.sh <slug> <CompId> <publicNN>
#   scripts/_finish_episode.sh flowers Ep54Flowers 54
#
# Assumes i2v for this episode is COMPLETE and the GPU is free -- a render and an i2v job
# must never overlap on the single 4090. Run it after the i2v chain has exited.
#
# The final mp4 still has to be WATCHED end to end before it is shown to anyone; a green
# post-render gate means "no black, no freeze, right duration", not "good".
set -u
cd /c/Users/aab15/Documents/prime-documentary

SLUG="${1:?usage: _finish_episode.sh <slug> <CompId> <publicNN>}"
COMP="${2:?composition id required}"
NUM="${3:?public dir number required}"
LOG="out_finish_${SLUG}.log"
: > "$LOG"

say(){ echo "[finish:$SLUG] $*" | tee -a "$LOG"; }
die(){ say "STOPPED -- $*"; exit 1; }

say "START $(date)"

say "[0/7] input pre-flight (fails in seconds, not hours)"
py -3.11 scripts/check_episode_inputs.py --slug "$SLUG" >> "$LOG" 2>&1 || {
  grep -E "^\[inputs\]|^  - " "$LOG" | tail -12 | sed "s/^/[finish:$SLUG]   /"
  die "inputs missing -- fix the list above; nothing was rendered"
}
grep -E "^\[inputs\] .*READY" "$LOG" | tail -1 | sed "s/^/[finish:$SLUG]   /"

say "[1/7] assemble i2v frames -> mp4"
py -3.11 scripts/assemble_episode_i2v.py --slug "$SLUG" >> "$LOG" 2>&1 || die "assemble failed"

say "[2/7] copy i2v motion into the render-visible public dir"
mkdir -p "remotion/public/${SLUG}/motion"
cp -n "H:/pd-media/assets/ai_video/${SLUG}/motion/"*.mp4 "remotion/public/${SLUG}/motion/" 2>/dev/null
say "  motion clips visible: $(ls remotion/public/${SLUG}/motion/*.mp4 2>/dev/null | wc -l)"

say "[3/7] rebuild asset manifest v003 (filesystem scan + per-asset content check)"
py -3.11 scripts/build_asset_manifest_motionfirst.py --slug "$SLUG" >> "$LOG" 2>&1
# a non-zero exit here means the scan found PROBLEMS, which are printed in the log
grep -E "^\[${SLUG}\]|PROBLEM" "$LOG" | tail -4 | sed "s/^/[finish:$SLUG]   /"

say "[4/7] build film.json"
CFG=$(ls episodes/_planning/EP5*_${SLUG}_filmconfig.v001.json 2>/dev/null | head -1)
[ -n "$CFG" ] || die "no filmconfig for $SLUG"
py -3.11 scripts/build_case_film_generic.py --config "$CFG" >> "$LOG" 2>&1 || die "film build failed"

# EP50's acceptance run measured what the size-based caption splitter does to a finished film:
# 54 orphan cues, 185 mid-phrase splits, 613 over-long lines -- the owner's 「字幕が変な所で
# 途切れる」. The polish re-segments cues on phrase boundaries and writes the SAME cues into
# film.json, so the burned-in captions and the sidecar .srt break identically. It runs BEFORE
# the render, because burned captions cannot be fixed afterwards.
EPDIR=$(ls -d episodes/PD-2026-0*-${SLUG} | head -1)
SRT="${EPDIR}/08_edit/captions.final.v001.srt"
if [ -f "$SRT" ]; then
  say "[4b] polish captions (no orphans / no dangling ends / <=84 chars per cue)"
  py -3.11 scripts/polish_captions_srt.py --srt "$SRT" --lead 0.25 \
       --film "remotion/src/data/${SLUG}_film.json" >> "$LOG" 2>&1 || die "caption polish failed"
  py -3.11 scripts/check_caption_breaks.py "$SRT" >> "$LOG" 2>&1 || die "caption breaks still bad"
  grep -E "^(PASS|FAIL) caption_breaks|cues .* orphans" "$LOG" | tail -2 | sed "s/^/[finish:$SLUG]   /"
fi

say "[4c] retire staged clips the film does not reference (footage_utilization)"
py -3.11 scripts/retire_unused_pool_clips.py --slug "$SLUG" >> "$LOG" 2>&1 || true
grep -E "^\[retire\]" "$LOG" | tail -1 | sed "s/^/[finish:$SLUG]   /"

say "[5/7] rebuild slim public dir (hardlinks, never junctions)"
rm -rf "remotion/public_ep${NUM}"
py -3.11 scripts/build_render_public_dir.py --slug "$SLUG" >> "$LOG" 2>&1 || die "public dir not render-ready"

EXPECT=$(py -3.11 -c "import json;d=json.load(open(r'remotion/src/data/${SLUG}_film.json',encoding='utf-8'));print(round(d['narrationSeconds']+d['hookSeconds']+3.5+9.0,1))")
say "[5b] 60-second probe render BEFORE committing to the full film"
bash scripts/probe_before_render.sh "$COMP" "remotion/src/data/${SLUG}_film.json" "remotion/public_ep${NUM}" "$SLUG" >> "$LOG" 2>&1 || {
  grep -E "^\[probe\]" "$LOG" | tail -4 | sed "s/^/[finish:$SLUG]   /"
  die "the 60s probe already shows black/frozen frames -- fixed cheaply now, not after 2 hours"
}
grep -E "^\[probe\]" "$LOG" | tail -2 | sed "s/^/[finish:$SLUG]   /"

say "[6/7] guarded render -> out/${SLUG}.mp4 (expect ${EXPECT}s)"
rm -f "out/${SLUG}.mp4"
bash scripts/pd_render_guarded.sh "$COMP" "remotion/src/data/${SLUG}_film.json" \
     "remotion/public_ep${NUM}" "out/${SLUG}.mp4" "$EXPECT" >> "$LOG" 2>&1 \
     || die "render or its gates failed (see $LOG and out_render_${SLUG}.mp4.log)"

say "[7/7] BGM bed + authoritative master VO, then re-gate the muxed result"
EP=$(ls -d episodes/PD-2026-0*-${SLUG} | head -1)
OUT="${EP}/08_edit/${SLUG}_final_bgm.v001.mp4"
mkdir -p "${EP}/08_edit"
rm -f "$OUT"
py -3.11 scripts/build_case_bgm_generic.py --slug "$SLUG" --render "out/${SLUG}.mp4" --out "$OUT" >> "$LOG" 2>&1 \
     || die "BGM build failed"
py -3.11 scripts/pd_postrender_gate.py "$OUT" --expect-sec "$EXPECT" --frames 40 \
     --out "out_qc/qc_frames_${SLUG}" >> "$LOG" 2>&1 \
     || die "post-gate FAILED on the BGM master -- do not show it"

say "DONE $(date) -> $OUT"
say "NEXT: WATCH IT END TO END. A green gate is not an opinion about quality."
