#!/usr/bin/env bash
# Finish every missing TikTok Short variant without overlapping an active render.
set -uo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
LOG="$REPO/out_tiktok_render_queue.log"
cd "$REPO" || exit 1

log() { echo "[tt-queue $(date '+%H:%M:%S')] $*" | tee -a "$LOG"; }

active_tiktok_renders() {
  powershell.exe -NoProfile -Command \
    '$n = @(Get-CimInstance Win32_Process | Where-Object { $_.Name -eq "node.exe" -and $_.CommandLine -match "Short-short[0-9]+-tt" }).Count; Write-Output $n' \
    2>/dev/null | tr -d '\r[:space:]'
}

missing_numbers() {
  py -3.11 -c 'import pathlib,re; p=pathlib.Path("remotion/out"); yt={int(m.group(1)) for f in p.glob("short*_yt_coverfirst.mp4") if (m:=re.fullmatch(r"short(\d+)_yt_coverfirst",f.stem))}; tt={int(m.group(1)) for f in p.glob("short*_tt.mp4") if (m:=re.fullmatch(r"short(\d+)_tt",f.stem))}; print(" ".join(map(str,sorted(yt-tt))))'
}

log "queue starting; waiting for the inherited Claude render to finish"
while true; do
  active="$(active_tiktok_renders)"
  [ "${active:-0}" = "0" ] && break
  log "existing TikTok render still active ($active node process(es)); waiting 30s"
  sleep 30
done

while true; do
  missing="$(missing_numbers)"
  [ -n "$missing" ] || break
  batch="$(echo "$missing" | tr ' ' '\n' | head -20 | tr '\n' ' ')"
  log "rendering batch: $batch"
  if ! bash scripts/render_shorts_tiktok.sh $batch >> "$LOG" 2>&1; then
    log "STOPPED: batch failed; no automatic retry. Inspect the log before resuming."
    exit 1
  fi
done

py -3.11 scripts/build_tiktok_schedule_queue.py >> "$LOG" 2>&1
count="$(find remotion/out -maxdepth 1 -type f -name 'short*_tt.mp4' | wc -l | tr -d ' ')"
log "QUEUE COMPLETE: $count TikTok renders on disk"
