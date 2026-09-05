#!/bin/bash
# Finish EP63-65 and gate them, one job at a time. v002.
#
# Two things changed from v001, both because of a real failure at 21:31 tonight.
#
# 1. correa's render completed (out/correa.mp4, 1.83 GB) but step 7 -- the BGM bed and the
#    authoritative master VO -- never ran, because `_finish_episode.sh` died with
#    "line 124: unexpected EOF" AFTER the render. The script was not broken: an agent EDITED IT
#    WHILE BASH WAS EXECUTING IT. Bash reads a script incrementally by byte offset, so an edit
#    under a running interpreter desynchronises the offset and the rest parses as garbage. The
#    file passes `bash -n` now. correa's 08_edit master is still the 08-07 build, so an acceptance
#    run against it would have stamped a receipt for the wrong film -- exactly the "check which
#    file the inspection measured" trap. Step 7 is re-run here first.
#
# 2. Every long job now runs from an IMMUTABLE COPY of its script, taken at launch. Editing the
#    original mid-flight can no longer corrupt a job in progress.
#
# greene's acceptance is already running and is not repeated here; the idle test waits for it.
set -u
cd /c/Users/aab15/Documents/prime-documentary
export PATH="/usr/bin:/bin:$PATH"

SNAP=$(mktemp -d "${TMPDIR:-/tmp}/pdsnap.XXXXXX")
cp scripts/_finish_episode.sh "$SNAP/_finish_episode.sh"
echo "[q] running from an immutable copy: $SNAP/_finish_episode.sh"

# WMI carries the full command line; `ps -W` prints only the interpreter path, so counting script
# names there returns 0 while one is plainly running -- a guard that can never fire, which is how
# an earlier queue launched a second render on top of a live one.
idle_once() {
  local n
  n=$(powershell -NoProfile -Command \
    "@(Get-CimInstance Win32_Process | Where-Object { (\$_.CommandLine -like '*remotion*render*' -or \$_.CommandLine -like '*_finish_episode.sh*' -or \$_.CommandLine -like '*check_final_acceptance*' -or \$_.CommandLine -like '*build_case_bgm_generic*') -and \$_.CommandLine -notlike '*Win32_Process*' -and \$_.CommandLine -notlike '*shell-snapshots*' }).Count" \
    2>/dev/null | tr -d '\r ' | head -1)
  [ "${n:-1}" = "0" ]
}

wait_idle() {
  local streak=0
  for _ in $(seq 1 1400); do            # up to ~11.7 hours
    if idle_once; then
      streak=$((streak + 1))
      [ "$streak" -ge 3 ] && { echo "[q] idle x3 $(date +%H:%M)"; sleep 20; return 0; }
    else
      streak=0
    fi
    sleep 30
  done
  echo "[q] gave up waiting for an idle machine" >&2
  return 1
}

# Re-run only the tail of _finish_episode.sh for correa: the render is already on disk and good.
mux_correa() {
  local SLUG=correa EP=episodes/PD-2026-063-correa
  local OUT="$EP/08_edit/${SLUG}_final_bgm.v001.mp4"
  local EXPECT
  EXPECT=$(py -3.11 -c "import json;d=json.load(open(r'remotion/src/data/correa_film.json',encoding='utf-8'));lead=d['leadSeconds'] if d.get('leadSeconds') is not None else d['hookSeconds']+3.5;print(round(d['narrationSeconds']+lead+9.0,1))")
  echo "[q] === correa step 7 (BGM + master VO), expect ${EXPECT}s $(date +%H:%M) ==="
  [ -f out/correa.mp4 ] || { echo "[q] out/correa.mp4 missing -- cannot mux" >&2; return 1; }
  rm -f "$OUT"
  py -3.11 scripts/build_case_bgm_generic.py --slug "$SLUG" --render out/correa.mp4 --out "$OUT" \
      > out_mux_correa.log 2>&1 || { echo "[q] correa BGM build FAILED" >&2; return 1; }
  py -3.11 scripts/pd_postrender_gate.py "$OUT" --expect-sec "$EXPECT" --frames 40 \
      --out out_qc/qc_frames_correa >> out_mux_correa.log 2>&1 \
      || { echo "[q] correa post-gate FAILED -- do not show it" >&2; return 1; }
  echo "[q] correa step 7 done $(date +%H:%M) -> $OUT"
}

accept() {   # slug, episode-id, episode-number
  local slug="$1" epid="$2" num="$3"
  local master="episodes/$epid/08_edit/${slug}_final_bgm.v001.mp4"
  if [ ! -f "$master" ]; then
    echo "[q] $slug: no muxed master at $master -- refusing to gate a different file" >&2
    return 0
  fi
  echo "[q] === accept $slug $(date +%H:%M) -> $master ==="
  py -3.11 scripts/check_final_acceptance.py "$num" --render "$master" --emit-receipt \
      > "out_accept_${slug}.log" 2>&1
  echo "[q] accept $slug exit=$? $(date +%H:%M) (out_accept_${slug}.log)"
}

render() {   # slug, composition, number
  echo "[q] === render $1 $(date +%H:%M) ==="
  bash scripts/pd_run.sh --name "refinish-$1" \
      --smoke "py -3.11 scripts/check_episode_inputs.py --slug $1" \
      -- bash "$SNAP/_finish_episode.sh" "$1" "$2" "$3" --allow-video-diversity-deviation \
    || { echo "[q] $1 refused to start" >&2; return 1; }
  sleep 120
}

wait_idle && mux_correa
wait_idle && render memphis Ep64Memphis 64
wait_idle && accept correa  PD-2026-063-correa  63
wait_idle && render marmet  Ep65Marmet 65
wait_idle && accept memphis PD-2026-064-memphis 64
wait_idle && accept marmet  PD-2026-065-marmet  65

echo "[q] all jobs attempted $(date +%H:%M)"
rm -rf "$SNAP"
