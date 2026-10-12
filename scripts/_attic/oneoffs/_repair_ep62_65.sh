#!/bin/bash
# Reconcile the four review masters after the primary queue.  A concurrent edit can make a shell
# that is already reading _finish_episode.sh stop after the raw guarded render; in that case the
# expensive, already-gated picture render is preserved and only the BGM/master-VO mux is resumed.
set -euo pipefail
cd /c/Users/aab15/Documents/prime-documentary

JOBS=(
  "greene:Ep62Greene:62"
  "correa:Ep63Correa:63"
  "memphis:Ep64Memphis:64"
  "marmet:Ep65Marmet:65"
)

for job in "${JOBS[@]}"; do
  slug="${job%%:*}"
  rest="${job#*:}"
  comp="${rest%%:*}"
  num="${rest##*:}"
  ep=$(ls -d episodes/PD-2026-0*-${slug} | head -1)
  final="${ep}/08_edit/${slug}_final_bgm.v001.mp4"

  if [ -s "$final" ] && ffprobe -v error -select_streams v:0 -show_entries stream=index \
      -of csv=p=0 "$final" >/dev/null 2>&1; then
    echo "[repair-62-65] $slug final already present"
    continue
  fi

  if [ -s "out/${slug}.mp4" ] && grep -q \
      "GUARDED RENDER COMPLETE: out/${slug}.mp4 PASSED both gates" \
      "out_finish_${slug}.log" 2>/dev/null; then
    echo "[repair-62-65] $slug raw render is gated; resuming BGM/master-VO mux only"
    expect=$(py -3.11 -c "import json;d=json.load(open(r'remotion/src/data/${slug}_film.json',encoding='utf-8'));print(round(d['narrationSeconds']+d['hookSeconds']+3.5+9.0,1))")
    mkdir -p "${ep}/08_edit"
    rm -f "$final"
    py -3.11 scripts/build_case_bgm_generic.py --slug "$slug" \
      --render "out/${slug}.mp4" --out "$final"
    py -3.11 scripts/pd_postrender_gate.py "$final" --expect-sec "$expect" --frames 40 \
      --out "out_qc/qc_frames_${slug}"
  else
    echo "[repair-62-65] $slug has no reusable gated raw render; rerunning its guarded build"
    bash scripts/_finish_episode.sh "$slug" "$comp" "$num" \
      --allow-video-diversity-deviation
  fi

  [ -s "$final" ] || { echo "[repair-62-65] $slug final is still missing"; exit 1; }
done

echo "[repair-62-65] all four review masters present"
