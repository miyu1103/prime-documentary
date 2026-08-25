#!/bin/bash
# Finish one episode: i2v output -> manifest -> film.json -> slim public dir -> guarded
# render -> BGM/master-VO remux -> post-render gate. Every stage is checked; the first
# failure stops the chain so nothing downstream is built on a bad input.
#
#   scripts/_finish_episode.sh <slug> <CompId> <publicNN> [--allow-video-diversity-deviation]
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
ALLOW_DIVERSITY="${4:-}"
LOG="out_finish_${SLUG}.log"
: > "$LOG"

say(){ echo "[finish:$SLUG] $*" | tee -a "$LOG"; }
die(){ say "STOPPED -- $*"; exit 1; }

say "START $(date)"

# RESTORE WHAT [5/7] SET ASIDE, BEFORE MEASURING ANYTHING (2026-08-23).
# [5/7] builds the slim render dir and moves every unreferenced asset into <pool>_unused/.
# That is correct for the render and wrong for the NEXT run: re-entering this chain then sees
# a pool that has already been trimmed to one film's cuts and refuses on "inputs missing".
# EP71 oroville hit it -- stills 118 -> 13, factory 63 -> 45 -- and it costs a full restart
# every time. Nothing is deleted by that step, so putting it back is safe and idempotent.
for _p in img motion factory; do
  _u="remotion/public/${SLUG}/${_p}_unused"
  if [ -d "$_u" ] && [ -n "$(ls -A "$_u" 2>/dev/null)" ]; then
    _n=$(ls -A "$_u" | wc -l)
    mv -n "$_u"/* "remotion/public/${SLUG}/${_p}/" 2>/dev/null
    say "[0/7] restored ${_n} asset(s) from ${_p}_unused (set aside by a previous [5/7])"
  fi
done

say "[0/7] input pre-flight (fails in seconds, not hours)"
INPUT_ARGS=(--slug "$SLUG")
if [ "$ALLOW_DIVERSITY" = "--allow-video-diversity-deviation" ]; then
  INPUT_ARGS+=(--allow-video-diversity-deviation)
  say "  REVIEW-CUT DEVIATION: strict distinct-video floor may remain red; publish is blocked"
fi
py -3.11 scripts/check_episode_inputs.py "${INPUT_ARGS[@]}" >> "$LOG" 2>&1 || {
  grep -E "^\[inputs\]|^  - " "$LOG" | tail -12 | sed "s/^/[finish:$SLUG]   /"
  die "inputs missing -- fix the list above; nothing was rendered"
}
grep -E "^\[inputs\] .*READY" "$LOG" | tail -1 | sed "s/^/[finish:$SLUG]   /"

say "[1/7] assemble i2v frames -> mp4"
py -3.11 scripts/assemble_episode_i2v.py --slug "$SLUG" >> "$LOG" 2>&1 || die "assemble failed"

say "[2/7] copy i2v motion into the render-visible public dir"
mkdir -p "remotion/public/${SLUG}/motion"
# A *_depth.mp4 IS A RENDERER INPUT, NEVER A PICTURE (2026-08-25, EP75). The archive still
# holds the 63 depth-map clips an earlier i2v run made by globbing H* over the depth
# companions. This copy is unconditional, so every finisher run put them back into the
# render-visible pool -- lahaina went from 91 real clips to 155 sixty seconds after the
# quarantine, and would have shipped depth maps as picture for the second time.
for _m in "E:/pd-media/assets/ai_video/${SLUG}/motion/"*.mp4; do
  [ -e "$_m" ] || continue
  case "$(basename "$_m")" in *_depth.mp4) continue;; esac
  cp -n "$_m" "remotion/public/${SLUG}/motion/" 2>/dev/null
done
say "  motion clips visible: $(ls remotion/public/${SLUG}/motion/*.mp4 2>/dev/null | wc -l)"

say "[2b/7] enforce episode blocklist after source copy (img + motion)"
# The source archive is intentionally immutable, so a rejected i2v can reappear every time the
# render-visible pool is refreshed. Pruning only before this copy is not durable: Willingham's
# blocked P01/P03/P26 motion plates were copied back and reached the film builder again. Check
# both pools after every copy; prune_pool_by_blocklist moves matches recoverably and is a no-op
# when the episode has no scoped rejection.
py -3.11 scripts/prune_pool_by_blocklist.py --slug "$SLUG" --pool img >> "$LOG" 2>&1 \
  || die "img blocklist prune failed"
py -3.11 scripts/prune_pool_by_blocklist.py --slug "$SLUG" --pool motion >> "$LOG" 2>&1 \
  || die "motion blocklist prune failed"

say "[3/7] rebuild asset manifest v003 (filesystem scan + per-asset content check)"
py -3.11 scripts/build_asset_manifest_motionfirst.py --slug "$SLUG" >> "$LOG" 2>&1
# a non-zero exit here means the scan found PROBLEMS, which are printed in the log
grep -E "^\[${SLUG}\]|PROBLEM" "$LOG" | tail -4 | sed "s/^/[finish:$SLUG]   /"

say "[4/7] build film.json"
# EP5* excluded EP60 entirely, and .v001 pinned the FIRST revision -- so surfside stopped
# dead at "no filmconfig", and any episode whose designer shipped a v002/v003 would have been
# built from the stale first draft. Match any episode number, take the LATEST revision.
CFG=$(ls episodes/_planning/EP*_${SLUG}_filmconfig.v*.json 2>/dev/null | sort | tail -1)
[ -n "$CFG" ] || die "no filmconfig for $SLUG"
py -3.11 scripts/build_case_film_generic.py --config "$CFG" >> "$LOG" 2>&1 || die "film build failed"
say "  built from $(basename "$CFG")"

# [4a] THE FILM IS CHECKED AGAINST ITS OWN CONTRACT, BEFORE THE RENDER.
# The pre-flight at [0/7] only sees inputs. This sees the PLAN: whether the stills that were
# generated for this episode actually reached a cut, whether anything the episode forbids is
# in it, and whether the distinct-asset floor is met. Every one of those has already shipped
# a defect: EP54 lost fourteen purpose-made courtroom stills to a surplus-trimming rule and
# EP58/EP59 carried the same loss unnoticed; EP56 rendered a red London bus into a film whose
# highest constraint forbids bus imagery because a sub-postmaster died under one.
# THE GUARD BELOW USED TO BE UNABLE TO FIRE. It searched `grep "^\[satisfied\]" | tail -4`,
# but check_spec_satisfied prints its failures as detail lines beginning with two spaces and a
# dash -- "  - mandatory_stills: 98 of 185 declared still(s) are in no cut". The inner grep
# threw those away and kept only the two summary lines, which never contain the words being
# searched for. Measured on EP66 openfields, whose film is missing 96 of 185 purpose-made
# plates: the guard did not die. Every episode since this was written rendered unprotected by
# the very check whose comment above lists three defects it exists to catch.
# Fixed by capturing the check's own output instead of re-reading the shared log.
py -3.11 scripts/check_spec_satisfied.py --slug "$SLUG" > "${LOG}.satisfied" 2>&1
_sat=$?
cat "${LOG}.satisfied" >> "$LOG"
sed "s/^/[finish:$SLUG]   /" "${LOG}.satisfied" | head -8
if [ $_sat -ne 0 ] && grep -qE "mandatory_stills|forbidden_subjects" "${LOG}.satisfied"; then
  die "the film violates its own spec (mandatory stills missing, or forbidden subject present)"
fi

# EP50's acceptance run measured what the size-based caption splitter does to a finished film:
# 54 orphan cues, 185 mid-phrase splits, 613 over-long lines -- the owner's 「字幕が変な所で
# 途切れる」. The polish re-segments cues on phrase boundaries and writes the SAME cues into
# film.json, so the burned-in captions and the sidecar .srt break identically. It runs BEFORE
# the render, because burned captions cannot be fixed afterwards.
EPDIR=$(ls -d episodes/PD-2026-0*-${SLUG} | head -1)
# THE FILENAME WAS HARDCODED WHILE [4/7] WRITES WHEREVER THE FILMCONFIG SAYS. On EP67
  # ramirez those are two different files: tonight's script extension moved the master from
  # 1448.020s to 1600.809s and the captions were re-cut as captions.final.v002.srt with the
  # filmconfig repointed, while v001 -- 448 words short, ending 152.8s early -- stayed on disk
  # for audit. This line would have polished v001 and written THOSE cues into the film json,
  # burning captions 152.8 seconds out of sync into the render. Read the declared value.
  SRT=$(py -3.11 -c "import json,sys;print(json.load(open(sys.argv[1],encoding='utf-8')).get('captions') or '')" "$CFG" 2>/dev/null)
  [ -n "$SRT" ] && [ -f "$SRT" ] || SRT="${EPDIR}/08_edit/captions.final.v001.srt"
if [ -f "$SRT" ]; then
  # THE LEAD THIS STEP APPLIES IS THE EPISODE'S, NOT A CONSTANT. 0.25 s stays the house default
  # and is exactly what every episode up to EP65 gets, because no filmconfig before EP66
  # declares the key. EP66's captions were aligned with the house 0.60 s lead when they were
  # written (out_ep66_captions.log: "applied caption lead -0.60s"), so the hard-coded 0.25 here
  # would have re-polished them to 0.85 s -- an episode's declared value silently overwritten by
  # its own pipeline, several steps after it was declared. A filmconfig may now declare
  # captionLeadSeconds; when it does not, this resolves to 0.25 and nothing changes.
  CAP_LEAD=$(py -3.11 -c "import json,sys;v=json.load(open(sys.argv[1],encoding='utf-8')).get('captionLeadSeconds');print(0.25 if v is None else float(v))" "$CFG")
  say "[4b] polish captions (lead ${CAP_LEAD}s from $(basename "$CFG"); no orphans / no dangling ends / <=84 chars per cue)"
  py -3.11 scripts/polish_captions_srt.py --srt "$SRT" --lead "$CAP_LEAD" \
       --film "remotion/src/data/${SLUG}_film.json" >> "$LOG" 2>&1 || die "caption polish failed"
  py -3.11 scripts/check_caption_breaks.py "$SRT" >> "$LOG" 2>&1 || die "caption breaks still bad"
  grep -E "^(PASS|FAIL) caption_breaks|cues .* orphans" "$LOG" | tail -2 | sed "s/^/[finish:$SLUG]   /"
fi

# THE EP77 ROAD, plan stage (owner directive 2026-08-23). The film json exists, the render
# has not started: this is the last moment a 紙芝居 plan (still holds over the cap -- red on
# 8/34 shipped episodes, always discovered three hours too late) can be fixed for the cost of
# an i2v pass instead of a re-render. Episodes below 077 pass instantly inside the tool.
say "[4d] EP77 standard, plan stage (still-hold caps before any GPU is spent)"
py -3.11 scripts/check_ep77_standard.py --slug "$SLUG" --stage plan >> "$LOG" 2>&1 \
  || die "the film plan fails the EP77 standard -- fix the plan; the render has not started, so this costs minutes"
grep "\[ep77-standard\]" "$LOG" | tail -1 | sed "s/^/[finish:$SLUG]   /"

say "[4c] retire staged clips the film does not reference (footage_utilization)"
py -3.11 scripts/retire_unused_pool_clips.py --slug "$SLUG" >> "$LOG" 2>&1 || true
grep -E "^\[retire\]" "$LOG" | tail -1 | sed "s/^/[finish:$SLUG]   /"

# [4d] THE AUDIO IS PROVED BUILDABLE BEFORE THE RENDER, NOT AFTER IT.
# Step 7 now depends on build_case_film_audio.py, whose density gate rejects an episode with
# too few SFX cues or too few distinct ambience beds (it returns 1). Discovering that after a
# four-hour render would throw the render away. The dry-run exits non-zero on exactly the same
# conditions and takes seconds. Its provenance goes to a SCRATCH path on purpose: written into
# 06_audio it would become the highest revision and the mux would then bind to a mix that was
# never rendered.
say "[4d] dry-run the 4-layer mix (a failing density gate costs seconds here, a render later)"
mkdir -p out_qc
py -3.11 scripts/build_case_film_audio.py --ep "$(basename "$(ls -d episodes/PD-2026-0*-${SLUG} | head -1)")" \
     --out "out_qc/_${SLUG}_audio_dryrun.json" --dry-run >> "$LOG" 2>&1 \
  || die "the 4-layer mix would fail its density gate -- fix the sound plan BEFORE rendering"
grep -E "^density:" "$LOG" | tail -1 | sed "s/^/[finish:$SLUG]   /"

say "[5/7] rebuild slim public dir (hardlinks, never junctions)"
rm -rf "remotion/public_ep${NUM}"
py -3.11 scripts/build_render_public_dir.py --slug "$SLUG" >> "$LOG" 2>&1 || die "public dir not render-ready"

EXPECT=$(py -3.11 -c "import json;d=json.load(open(r'remotion/src/data/${SLUG}_film.json',encoding='utf-8'));lead=d['leadSeconds'] if d.get('leadSeconds') is not None else d['hookSeconds']+3.5;print(round(d['narrationSeconds']+lead+9.0,1))")
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

say "[7/7] 4-layer mix (VO + music + ambience + SFX) -> mux with the mix-sha stamp, then re-gate"
EP=$(ls -d episodes/PD-2026-0*-${SLUG} | head -1)
EPID=$(basename "$EP")
OUT="${EP}/08_edit/${SLUG}_final_bgm.v001.mp4"
mkdir -p "${EP}/08_edit"
rm -f "$OUT"
# WHY THIS IS NO LONGER build_case_bgm_generic.py (2026-08-11).
# That tool builds narration + music and NOTHING else: its ambience beds are multiplied by
# `volume=0.0` (measured: -91.0 dB, i.e. digital silence) and it contains no SFX layer at all
# -- `grep -i sfx scripts/build_case_bgm_generic.py` returns nothing. So every episode from
# EP38 on shipped a TWO-layer bed while build_case_film_audio.py's real FOUR-layer mix sat
# unused on the SSD: precisely the "orphaned sound plan" that check_sound_layers was written
# to catch. It duly failed on 83 of 108 acceptance receipts and needed an owner waiver each
# time. The tag the gate wants (audio_mix_sha256) could NOT honestly be stamped on the BGM
# output, because that output is not the mix the tag names -- stamping it would have been a
# false attestation. The fix is to deliver the mix the spec actually asks for. EP32-EP36
# shipped exactly this way and passed sound_layers 25 times.
# The mix is written to the next FREE provenance revision: build_case_film_audio defaults to
# v001 and would otherwise overwrite an existing provenance (CLAUDE invariant 6).
AREV=$(py -3.11 -c "
import glob, sys
ns = []
for p in glob.glob(sys.argv[1] + '/06_audio/audio_provenance.v*.json'):
    tail = p.split('audio_provenance.v')[-1].split('.json')[0]
    if tail.isdigit():
        ns.append(int(tail))
print('v%03d' % ((max(ns) + 1) if ns else 1))
" "$EP")
say "  building the 4-layer mix as ${AREV}"
py -3.11 scripts/build_case_film_audio.py --ep "$EPID" --revision "$AREV" --render >> "$LOG" 2>&1 \
     || die "4-layer mix build failed -- see $LOG"
grep -E "^ambience:|^SFX cues:|^density:" "$LOG" | tail -3 | sed "s/^/[finish:$SLUG]   /"
# The mux makes that WAV the SOLE audio, stamps audio_mix_sha256, and REFUSES a mix whose
# duration disagrees with the render -- a stale mix would slide the VO off the burned-in
# captions while the ship gate went green. All four EP62-65 mixes on disk were stale by
# 15.9-115.0 s when this was written, so the guard is not theoretical.
py -3.11 scripts/build_case_film_mux.py --ep "$EPID" --video "out/${SLUG}.mp4" --out "$OUT" >> "$LOG" 2>&1 \
     || die "mux failed (stale mix, or the stamp did not read back) -- see $LOG"
grep -E "^freshness|^stamped tag readback" "$LOG" | tail -2 | sed "s/^/[finish:$SLUG]   /"
# Snapshot the film json BESIDE the master, before anything can rebuild it. Without this
# the cheap repair path is lost the moment the pool changes: scripts/pd_splice_cuts.py can
# replace a handful of cuts in a finished master in ~30 min instead of a 4-hour re-render, but
# only if it has the json the master was actually rendered from. EP62 greene lost exactly that --
# its json was rebuilt nine hours after its render, 278 of 389 cuts moved, and the splice aborted
# on its own provenance probe. Cheap insurance: a few hundred KB per episode.
cp "remotion/src/data/${SLUG}_film.json" "${EP}/08_edit/${SLUG}_film.rendered.json" 2>/dev/null \
  && say "[7/7] snapshotted the film json beside the master (splice-repair provenance)"
py -3.11 scripts/pd_postrender_gate.py "$OUT" --expect-sec "$EXPECT" --frames 40 \
     --out "out_qc/qc_frames_${SLUG}" >> "$LOG" 2>&1 \
     || die "post-gate FAILED on the BGM master -- do not show it"

say "DONE $(date) -> $OUT"
say "NEXT: WATCH IT END TO END. A green gate is not an opinion about quality."
