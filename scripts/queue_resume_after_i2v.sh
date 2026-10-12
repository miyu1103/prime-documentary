#!/bin/bash
# Close the loop: restart the render queue, patched, once the i2v watcher is finished.
#
# WHY IT EXISTS
#   scripts/i2v_watch.sh ends by LOGGING that the render queue should be restarted and then
#   stops. That deliberate hand-brake was pulled for one reason: queue_unattended.sh had a
#   freshness bug (it re-rendered EP65 marmet on 2026-08-11 at a cost of 1h35m of GPU) and
#   restarting it was a human decision until the fix landed. The fix now exists and is proven:
#   runs/patches/queue_freshness.v001.patch, with a three-case replay in
#   runs/patches/queue_freshness_test.sh. The reason for the hand-brake is gone, so this script
#   removes it -- applies the patch and starts the queue, unattended.
#
# WHY IT IS A SEPARATE FILE AND NOT A CHANGE TO i2v_watch.sh
#   bash reads a running script by byte offset. Editing i2v_watch.sh while it runs shifts every
#   offset after the edit and corrupts the live watcher -- the failure that killed correa's
#   step 7. The watcher was running when this was written, so it was not touched.
#
# THE HAND-OFF: HOW THIS KNOWS THE WATCHER IS DONE
#   By the watcher's own EXIT, not by a log line. Two independent signals must BOTH say gone,
#   for GONE_STREAK consecutive reads:
#     1. no /tmp/pdi2v.* snapshot directory holds a live Windows pid (this is the watcher's own
#        single-instance signal, and its staleness rule -- younger than 120 s counts as live --
#        is reused verbatim);
#     2. no process in the Windows process table has i2v_watch.sh on its command line.
#   Process exit was chosen over "grep the log for ALL PLANNED i2v IS DONE" because:
#     * the watcher writes no completion marker and adding one would mean editing it mid-flight;
#     * a log grep only covers the successful exit. The watcher also exits on its disk guard (3),
#       on a refused plan (2) and on the stop switch (0), and a stuck script that never restarts
#       the queue after any of those is the same stall this removes;
#     * a log line can be true of a PREVIOUS run's log file; a dead process cannot.
#   The watcher's log is still read, for the record: its last lines and its exit context are
#   copied into this log so the reason it ended is visible without hunting.
#
# WHAT IT REFUSES TO DO.  A wrong restart costs hours of GPU. A refusal costs nothing.
#   * two queues -> refuses. The signal is the snapshot count, never the process count: one
#     queue reads as 1 or 2 processes depending on whether its child shell is between commands,
#     which is exactly why scripts/check_queue_will_stall.py counts /tmp/pdq.* instead.
#   * patch will not apply cleanly -> refuses, changes nothing.
#   * patch already applied -> does NOT apply it a second time; verifies the result and goes on.
#   * bash -n fails after patching -> restores the backup and refuses.
#   * disk below the floor -> refuses (a render needs the space the i2v png just took).
#   * a human's STOP switch present -> refuses.
#   Every refusal exits non-zero having started nothing.
#
# STOPPING
#   touch runs/i2v_plans/STOP_QUEUE_RESUME     # checked every poll; nothing is started after it
#
# USAGE
#   nohup bash scripts/queue_resume_after_i2v.sh > runs/logs/queue_resume.boot 2>&1 &
#   bash scripts/queue_resume_after_i2v.sh --status     # one-shot: every signal it reads
#   bash scripts/queue_resume_after_i2v.sh --dry-run    # full decision incl. patch dry-run, runs nothing
#
# EXIT CODES
#   0 queue started (or --status/--dry-run completed)
#   2 a STOP switch is present
#   3 free space below the floor
#   4 another instance of this script is live
#   5 the wait window expired with the watcher or the machine still busy
#   6 a queue is already running -- refused rather than start a second one
#   7 the patch does not apply cleanly, or the patched file failed verification
#   8 the queue was started but did not come up
#   9 preconditions are wrong (repo, patch file or queue script missing)
#
# ENVIRONMENT (defaults are the production values; the overrides exist so the proof harness can
# run against copies in a private TMPDIR and never touch the live machine)
#   PDR_REPO          repo root                     (/c/Users/aab15/Documents/prime-documentary)
#   PDR_SNAP_ROOT     where pdq.*/pdi2v.* live      (/tmp -- hard default, see the note below)
#   PDR_PDQ_GLOB      queue snapshot glob           (pdq.*)
#   PDR_QUEUE_SCRIPT  queue script, repo-relative   (scripts/queue_unattended.sh)
#   PDR_PATCH         patch file, repo-relative     (runs/patches/queue_freshness.v001.patch)
#   PDR_MIN_FREE_GIB  disk floor                    (25)
#   PDR_IDLE_STREAK   consecutive busy=0 reads      (6)
#   PDR_GONE_STREAK   consecutive watcher-gone reads(3)
#   PDR_POLL_SEC / PDR_HB_SEC / PDR_QUEUE_WAIT_MIN  (30 / 600 / 480)
#   PDR_FAKE_BUSY     TESTS ONLY: file whose contents replace the busy() reading
#   PDR_SKIP_SELF_SNAPSHOT  TESTS ONLY: do not re-exec from a frozen copy
set -u

REPO="${PDR_REPO:-/c/Users/aab15/Documents/prime-documentary}"
cd "$REPO" || { echo "[qr] REFUSED: cannot cd $REPO" >&2; exit 9; }
export PATH="/usr/bin:/bin:$PATH"

# Hard default /tmp, NOT ${TMPDIR:-/tmp}. TMPDIR differs between shells on this machine (one
# reports it empty, another E:/UserTemp/aab15 -- which is the same directory, but only by luck
# of the mount table). queue_unattended.sh's snapshots land in /tmp, i2v_watch.sh's land in /tmp,
# and a detector that looks anywhere else is not a detector.
SNAP_ROOT="${PDR_SNAP_ROOT:-/tmp}"
PDQ_GLOB="${PDR_PDQ_GLOB:-pdq.*}"
QUEUE_SCRIPT="${PDR_QUEUE_SCRIPT:-scripts/queue_unattended.sh}"
PATCH_FILE="${PDR_PATCH:-runs/patches/queue_freshness.v001.patch}"
MIN_FREE_GIB="${PDR_MIN_FREE_GIB:-25}"
IDLE_STREAK="${PDR_IDLE_STREAK:-6}"
GONE_STREAK="${PDR_GONE_STREAK:-3}"
POLL_SEC="${PDR_POLL_SEC:-30}"
HB_SEC="${PDR_HB_SEC:-600}"
QUEUE_WAIT_MIN="${PDR_QUEUE_WAIT_MIN:-480}"
FAKE_BUSY="${PDR_FAKE_BUSY:-}"
STOP_FILE="runs/i2v_plans/STOP_QUEUE_RESUME"
I2V_STOP="runs/i2v_plans/STOP_I2V_WATCH"

MODE=run
LOG=""
while [ $# -gt 0 ]; do
  case "$1" in
    --status)  MODE=status; shift;;
    --dry-run) MODE=dry; shift;;
    --log)     LOG="$2"; shift 2;;
    *) echo "[qr] unknown argument: $1" >&2; exit 9;;
  esac
done

# ---------------------------------------------------------------- shared primitives

# VERBATIM from scripts/queue_unattended.sh busy(), which scripts/i2v_watch.sh also copies
# verbatim. Six job classes, four exclusions, an 8-hour age cap. A second, differently-wrong
# idleness detector is what held this machine at busy=12 for 545 minutes on 2026-08-11. If that
# detector is ever changed it changes in all three files or in none.
busy() {
  if [ -n "$FAKE_BUSY" ]; then cat "$FAKE_BUSY" 2>/dev/null | tr -d '\r ' | head -1; return; fi
  powershell -NoProfile -Command \
    "@(Get-CimInstance Win32_Process | Where-Object { (\$_.CommandLine -like '*remotion*render*' -or \$_.CommandLine -like '*_finish_episode.sh*' -or \$_.CommandLine -like '*check_final_acceptance*' -or \$_.CommandLine -like '*_chain_i2v*' -or \$_.CommandLine -like '*ComfyUI*' -or \$_.CommandLine -like '*build_case_bgm*') -and \$_.CommandLine -notlike '*Win32_Process*' -and \$_.CommandLine -notlike '*shell-snapshots*' -and \$_.CommandLine -notlike '*--help*' -and \$_.CommandLine -notlike '*--version*' -and ((Get-Date) - \$_.CreationDate).TotalHours -lt 8 }).Count" \
    2>/dev/null | tr -d '\r ' | head -1
}

# pd_run.sh writes this file and tests it exactly this way. Deference to the render queue's own
# lock, not a second process scanner.
render_lock_live() {
  local p
  [ -f out_pdrun_render.lock ] || return 1
  p=$(tr -d '[:space:]' < out_pdrun_render.lock 2>/dev/null)
  [ -n "$p" ] || return 1
  tasklist //FI "PID eq $p" 2>/dev/null | grep -q "$p"
}

pid_live() { [ -n "${1:-}" ] && tasklist //FI "PID eq $1" 2>/dev/null | grep -q "$1"; }

# How many queues have been started. NOT a process count: one queue reads as 1 or 2 processes
# depending on whether its child shell is mid-command, so process counting cannot tell one queue
# from two. Each queue makes exactly one snapshot dir at startup and holds it for its whole life.
pdq_count() { ls -d "$SNAP_ROOT"/$PDQ_GLOB 2>/dev/null | wc -l | tr -d ' '; }
pdq_list()  { ls -d "$SNAP_ROOT"/$PDQ_GLOB 2>/dev/null | tr '\n' ' '; }

# Signal 1 of 2: the watcher's own single-instance marker, read with the watcher's own rules.
# Nothing is deleted here -- sweeping another process's snapshot is the watcher's job, not this
# script's, and a reader that mutates the thing it reads is how the 2026-08-12 double-watcher
# happened.
watcher_snapshot_live() {
  local d born p now; now=$(date +%s)
  for d in "$SNAP_ROOT"/pdi2v.*; do
    [ -d "$d" ] || continue
    born=$(tr -d '[:space:]' < "$d/started_at" 2>/dev/null)
    [ -n "$born" ] && [ $((now - born)) -lt 120 ] && return 0
    p=$(tr -d '[:space:]' < "$d/winpid" 2>/dev/null)
    pid_live "$p" && return 0
  done
  return 1
}

# Signal 2 of 2: the process table itself. Survives a watcher killed hard enough that its EXIT
# trap never ran, and a snapshot directory Windows refused to unlink.
watcher_process_live() {
  local n
  [ -n "$FAKE_BUSY" ] && return 1     # tests only: signal 2 is stubbed out with busy()
  n=$(powershell -NoProfile -Command \
    "@(Get-CimInstance Win32_Process | Where-Object { \$_.CommandLine -like '*i2v_watch.sh*' -and \$_.CommandLine -notlike '*Win32_Process*' -and \$_.CommandLine -notlike '*shell-snapshots*' }).Count" \
    2>/dev/null | tr -d '\r ' | head -1)
  # A detector that cannot measure must never answer "nothing is running".
  case "$n" in (''|*[!0-9]*) return 0;; esac
  [ "$n" -gt 0 ]
}

watcher_live() { watcher_snapshot_live || watcher_process_live; }

free_gib() { df -k /c 2>/dev/null | tail -1 | awk '{printf "%d", $4/1048576} END{if (NR == 0) printf "0"}'; }

crlf_bytes() { tr -dc '\r' < "$1" 2>/dev/null | wc -c | tr -d ' '; }

ts() { date '+%Y-%m-%d %H:%M:%S'; }
say() { echo "[qr $(ts)] $*"; }

# ---------------------------------------------------------------- one-shot status

if [ "$MODE" = "status" ]; then
  say "repo=$REPO snap_root=$SNAP_ROOT queue=$QUEUE_SCRIPT"
  say "busy()                 = $(busy)"
  say "render lock live       = $(render_lock_live && echo yes || echo no)"
  say "watcher snapshot live  = $(watcher_snapshot_live && echo yes || echo no)"
  say "watcher process live   = $(watcher_process_live && echo yes || echo no)"
  say "queue snapshots ($PDQ_GLOB) = $(pdq_count)  [$(pdq_list)]"
  say "free on C:             = $(free_gib)GiB (floor ${MIN_FREE_GIB})"
  say "stop switches          = $STOP_FILE:$([ -f "$STOP_FILE" ] && echo PRESENT || echo absent) $I2V_STOP:$([ -f "$I2V_STOP" ] && echo PRESENT || echo absent)"
  exit 0
fi

# ---------------------------------------------------------------- preflight

[ -f "$QUEUE_SCRIPT" ] || { echo "[qr] REFUSED: $QUEUE_SCRIPT not found" >&2; exit 9; }
[ -f "$PATCH_FILE" ]   || { echo "[qr] REFUSED: $PATCH_FILE not found" >&2; exit 9; }

if [ -f "$STOP_FILE" ]; then
  echo "[qr] REFUSING TO START: $STOP_FILE exists. Remove it first: rm $STOP_FILE" >&2; exit 2
fi

# Single instance, by the same mechanism the watcher uses: a snapshot dir carrying a Windows pid,
# swept for staleness. Named pdresume.* -- NEVER pdq.*, which check_queue_will_stall.py counts as
# a running queue.
if [ "$MODE" = "run" ] && [ -z "${PDR_SNAP:-}" ] && [ -z "${PDR_SKIP_SELF_SNAPSHOT:-}" ]; then
  now=$(date +%s)
  for d in "$SNAP_ROOT"/pdresume.*; do
    [ -d "$d" ] || continue
    born=$(tr -d '[:space:]' < "$d/started_at" 2>/dev/null)
    if [ -n "$born" ] && [ $((now - born)) -lt 120 ]; then continue; fi
    p=$(tr -d '[:space:]' < "$d/winpid" 2>/dev/null)
    if ! pid_live "$p"; then echo "[qr] sweeping stale snapshot $d (winpid ${p:-unknown} not live)"; rm -rf "$d"; fi
  done
  if [ "$(ls -d "$SNAP_ROOT"/pdresume.* 2>/dev/null | wc -l)" -gt 0 ]; then
    echo "[qr] REFUSED: another queue_resume_after_i2v is live ($(ls -d "$SNAP_ROOT"/pdresume.* 2>/dev/null | tr '\n' ' '))" >&2
    exit 4
  fi
  SNAP=$(mktemp -d "$SNAP_ROOT/pdresume.XXXXXX")
  date +%s > "$SNAP/started_at"
  # Frozen copy, for the same reason the watcher and the queue freeze theirs: this script will be
  # alive for hours and bash reads a running script by byte offset.
  cp "$0" "$SNAP/queue_resume_after_i2v.sh"
  [ -z "$LOG" ] && LOG="runs/logs/queue_resume.$(date +%Y%m%d_%H%M%S).log"
  mkdir -p runs/logs
  echo "[qr] snapshot=$SNAP log=$LOG"
  export PDR_SNAP="$SNAP" PDR_LOG="$LOG"
  exec bash "$SNAP/queue_resume_after_i2v.sh" --log "$LOG"
fi

SNAP="${PDR_SNAP:-}"
PATCH_WORK=""
cleanup() {
  [ -n "$PATCH_WORK" ] && rm -rf "$PATCH_WORK" 2>/dev/null
  # Windows will not unlink the script bash is still reading, so the rm -rf is best effort;
  # dropping winpid is what lets the next run's staleness sweep collect the directory.
  [ -n "$SNAP" ] && { rm -f "$SNAP/winpid" 2>/dev/null; rm -rf "$SNAP" 2>/dev/null; }
  return 0
}
trap cleanup EXIT

[ -n "$LOG" ] || LOG="${PDR_LOG:-}"
if [ "$MODE" = "run" ] && [ -n "$SNAP" ]; then
  [ -n "$LOG" ] && { mkdir -p "$(dirname "$LOG")"; exec >> "$LOG" 2>&1; }
  # Resolve our own Windows pid AFTER the re-exec: MSYS implements exec by spawning a new Windows
  # process while keeping the MSYS pid, so a pid recorded before the exec is already dead.
  WINPID=$(powershell -NoProfile -Command \
    "(Get-CimInstance Win32_Process | Where-Object { \$_.CommandLine -like '*$(basename "$SNAP")/queue_resume_after_i2v.sh*' -and \$_.CommandLine -notlike '*Win32_Process*' -and \$_.CommandLine -notlike '*shell-snapshots*' } | Sort-Object CreationDate | Select-Object -First 1).ProcessId" \
    2>/dev/null | tr -d '\r ' | head -1)
  case "$WINPID" in (''|*[!0-9]*) echo "[qr] cannot resolve own Windows pid after re-exec" >&2; exit 9;; esac
  echo "$WINPID" > "$SNAP/winpid"
  [ -n "$LOG" ] && echo "$WINPID" > "${LOG%.log}.pid"
fi

say "================================================================"
say "queue_resume_after_i2v start  mode=$MODE  winpid=${WINPID:-n/a}  snapshot=${SNAP:-none}"
say "repo=$REPO  snap_root=$SNAP_ROOT  queue=$QUEUE_SCRIPT  patch=$PATCH_FILE"
say "config: idle_streak=$IDLE_STREAK gone_streak=$GONE_STREAK poll=${POLL_SEC}s hb=${HB_SEC}s"
say "        queue_wait=${QUEUE_WAIT_MIN}min disk_floor=${MIN_FREE_GIB}GiB"
say "stop with: touch $STOP_FILE"
say "================================================================"

check_stop() {
  if [ -f "$STOP_FILE" ]; then say "STOP switch $STOP_FILE appeared -- exiting, nothing started"; exit 2; fi
}

# ---------------------------------------------------------------- step 1: the hand-off

WATCHER_LOG=$(ls -t runs/logs/i2v_watch.*.log 2>/dev/null | head -1)
say "step 1/5  waiting for scripts/i2v_watch.sh to exit (watcher log: ${WATCHER_LOG:-none found})"

step1_wait() {
  local streak=0 i last_hb=0 nowsec alive
  for i in $(seq 1 4320); do          # 4320 x 30 s = 36 h; planned i2v is ~11 GPU-hours
    check_stop
    # asked ONCE per poll and reused, so the heartbeat cannot report a different reading than
    # the one the streak was counted from
    if watcher_live; then alive=yes; streak=0; else alive=no; streak=$((streak + 1)); fi
    nowsec=$((i * POLL_SEC))
    if [ "$i" = "1" ] || [ $((nowsec - last_hb)) -ge "$HB_SEC" ]; then
      say "  heartbeat watcher_live=$alive gone_streak=$streak busy=$(busy) free=$(free_gib)GiB"
      last_hb=$nowsec
    fi
    [ "$streak" -ge "$GONE_STREAK" ] && return 0
    sleep "$POLL_SEC"
  done
  return 1
}

if [ "$MODE" = "run" ]; then
  step1_wait || { say "REFUSED: the watcher was still live after the whole 36 h window. Nothing started."; exit 5; }
  say "step 1/5  the watcher is gone (snapshot=no, process=no, x$GONE_STREAK reads)"
  if [ -n "$WATCHER_LOG" ]; then
    if grep -q "ALL PLANNED i2v IS DONE" "$WATCHER_LOG" 2>/dev/null; then
      say "  watcher log says: ALL PLANNED i2v IS DONE  ($WATCHER_LOG)"
    else
      say "  NOTE: '$WATCHER_LOG' does NOT contain 'ALL PLANNED i2v IS DONE'."
      say "        The watcher ended some other way (disk guard, refused plan, or the stop switch)."
      say "        That is not by itself a reason to refuse -- the disk floor below is the check"
      say "        that matters -- but it means some planned i2v may be unfinished. Last lines:"
      tail -6 "$WATCHER_LOG" 2>/dev/null | sed 's/^/          | /'
    fi
  fi
else
  # A dry run reports the reading it actually took. It must never print "the watcher is gone"
  # while the watcher is plainly alive -- a log that contradicts the machine is worse than none.
  if watcher_live; then
    say "  [dry-run] the watcher is LIVE right now -- a real run would WAIT here and go no further"
  else
    say "  [dry-run] no watcher is live -- a real run would proceed"
  fi
  [ -n "$WATCHER_LOG" ] && say "  [dry-run] latest watcher log $WATCHER_LOG: completion line $(grep -q 'ALL PLANNED i2v IS DONE' "$WATCHER_LOG" 2>/dev/null && echo present || echo absent)"
fi

# A human who pulled the i2v stop switch was intervening on purpose. Do not overrule them.
if [ -f "$I2V_STOP" ]; then
  say "REFUSED: $I2V_STOP is present -- a human stopped the i2v run deliberately."
  say "         Restarting the render queue is their call. rm that file to re-enable this."
  exit 2
fi

# ---------------------------------------------------------------- step 2: machine idle

say "step 2/5  waiting for the machine to go idle (busy=0 x$IDLE_STREAK and no render lock)"
step2_wait() {
  local streak=0 i n last_hb=0 nowsec
  for i in $(seq 1 960); do
    check_stop
    n=$(busy)
    nowsec=$((i * POLL_SEC))
    if [ "$i" = "1" ] || [ $((nowsec - last_hb)) -ge "$HB_SEC" ]; then
      say "  heartbeat busy=$n idle_streak=$streak lock=$(render_lock_live && echo live || echo none) free=$(free_gib)GiB"
      last_hb=$nowsec
    fi
    if [ "${n:-1}" = "0" ] && ! render_lock_live; then
      streak=$((streak + 1)); [ "$streak" -ge "$IDLE_STREAK" ] && return 0
    else
      streak=0
    fi
    sleep "$POLL_SEC"
  done
  return 1
}
if [ "$MODE" = "run" ]; then
  step2_wait || { say "REFUSED: still busy after the whole 8 h idle window. Nothing started."; exit 5; }
  say "step 2/5  idle: no render, no finisher, no i2v chain, no live render lock"
else
  say "  [dry-run] busy=$(busy) render_lock=$(render_lock_live && echo live || echo none) -- a real run would wait for busy=0 x$IDLE_STREAK"
fi

fg=$(free_gib)
if [ "$fg" -lt "$MIN_FREE_GIB" ]; then
  say "REFUSED: only ${fg}GiB free on C:, floor is ${MIN_FREE_GIB}GiB. A render needs that space."
  say "         Reclaim space (runs/i2v_plans/README.md names ~26GB of superseded greene frame"
  say "         dirs in C:/Users/aab15/ae-demo) and start this script again."
  exit 3
fi
say "step 2/5  disk ok: ${fg}GiB free on C: (floor ${MIN_FREE_GIB})"

# ---------------------------------------------------------------- step 3: no queue may be up

say "step 3/5  queue snapshots under $SNAP_ROOT matching '$PDQ_GLOB': $(pdq_count) [$(pdq_list)]"
if [ "$(pdq_count)" != "0" ]; then
  say "  A queue is already running. This will NOT start a second one: two queues run two"
  say "  different snapshots of _finish_episode.sh and decide the same film's contents twice"
  say "  (that happened on 2026-08-11, 37 minutes apart). It will also NOT patch"
  say "  $QUEUE_SCRIPT while bash is reading it by byte offset."
  if [ "$QUEUE_WAIT_MIN" -gt 0 ] && [ "$MODE" = "run" ]; then
    say "  Waiting up to ${QUEUE_WAIT_MIN} min for that queue to end. Stopping it is a human's"
    say "  call; the moment it is gone this applies the patch and starts a fresh one."
    deadline=$(( $(date +%s) + QUEUE_WAIT_MIN * 60 )); last_hb=0
    while [ "$(pdq_count)" != "0" ]; do
      check_stop
      [ "$(date +%s)" -ge "$deadline" ] && break
      if [ $(( $(date +%s) - last_hb )) -ge "$HB_SEC" ]; then
        say "  heartbeat a queue is still live: $(pdq_list) -- not starting a second one"
        last_hb=$(date +%s)
      fi
      sleep "$POLL_SEC"
    done
  fi
fi
if [ "$(pdq_count)" != "0" ]; then
  say "REFUSED (exit 6): a queue is running -- $(pdq_list)"
  say "  Nothing was patched and nothing was started."
  say "  To hand over to a patched queue: stop that queue, then run this script again."
  if [ "$MODE" = "dry" ]; then
    say "  [dry-run] a real run would STOP HERE with exit 6. The steps below are shown anyway,"
    say "            read-only, so the patch decision can be inspected without a live queue."
  else
    exit 6
  fi
else
  say "step 3/5  no queue is running (zero snapshots)"
fi

# ---------------------------------------------------------------- step 4: the patch

# Three states, and only one of them is a refusal.
#   unapplied -> forward dry-run succeeds        -> back up, apply
#   applied   -> reverse dry-run succeeds        -> do NOT apply again, verify and go on
#   conflict  -> neither                         -> refuse, change nothing
PATCH_WORK=$(mktemp -d "$SNAP_ROOT/pdresumepatch.XXXXXX")

patch_state() {
  if patch -p1 --binary --batch --forward --dry-run -r "$PATCH_WORK/rej" \
        -i "$PATCH_FILE" "$QUEUE_SCRIPT" > "$PATCH_WORK/fwd.txt" 2>&1; then
    echo unapplied
  elif patch -p1 --binary --batch --forward --reverse --dry-run -r "$PATCH_WORK/rej" \
        -i "$PATCH_FILE" "$QUEUE_SCRIPT" > "$PATCH_WORK/rev.txt" 2>&1; then
    echo applied
  else
    echo conflict
  fi
}

# The fix IS the placement: the same predicate, asked once when the job is picked and again the
# instant wait_idle returns. A file with the function but without the post-wait call is the bug.
verify_patched() {
  local hits w a
  bash -n "$QUEUE_SCRIPT" 2>"$PATCH_WORK/syntax.txt" || { say "  VERIFY FAIL: bash -n"; sed 's/^/    | /' "$PATCH_WORK/syntax.txt"; return 1; }
  hits=$(grep -c "already_done" "$QUEUE_SCRIPT")
  [ "$hits" = "3" ] || { say "  VERIFY FAIL: expected 3 already_done occurrences (definition + 2 calls), found $hits"; return 1; }
  w=$(grep -n "wait_idle ||" "$QUEUE_SCRIPT" | head -1 | cut -d: -f1)
  a=$(grep -n "already_done" "$QUEUE_SCRIPT" | tail -1 | cut -d: -f1)
  [ -n "$w" ] && [ -n "$a" ] || { say "  VERIFY FAIL: could not locate wait_idle / already_done lines"; return 1; }
  [ "$a" -gt "$w" ] || { say "  VERIFY FAIL: the last already_done call (line $a) is not AFTER wait_idle (line $w) -- that placement IS the fix"; return 1; }
  say "  verified: bash -n clean, already_done x3, the second call is at line $a, after wait_idle at line $w"
  return 0
}

STATE=$(patch_state)
CRLF_BEFORE=$(crlf_bytes "$QUEUE_SCRIPT")
say "step 4/5  patch state: $STATE  (md5 $(md5sum "$QUEUE_SCRIPT" | cut -d' ' -f1), CR bytes $CRLF_BEFORE)"

case "$STATE" in
  conflict)
    say "REFUSED (exit 7): $PATCH_FILE neither applies nor reverse-applies to $QUEUE_SCRIPT."
    say "  The file has drifted from what the patch was written against, or it is half applied."
    say "  Nothing was changed. Forward attempt:"
    sed 's/^/    | /' "$PATCH_WORK/fwd.txt"
    say "  Reverse attempt:"
    sed 's/^/    | /' "$PATCH_WORK/rev.txt"
    exit 7;;
  applied)
    say "  the patch is ALREADY APPLIED -- not applying it a second time"
    verify_patched || { say "REFUSED (exit 7): the file claims to carry the patch but does not verify."; exit 7; };;
  unapplied)
    if [ "$MODE" = "dry" ]; then
      say "  [dry-run] would: cp $QUEUE_SCRIPT $QUEUE_SCRIPT.bak_<stamp>"
      say "  [dry-run] would: patch -p1 --binary -i $PATCH_FILE $QUEUE_SCRIPT   (forward dry-run already succeeded)"
    else
      # Last look before touching the file: a queue that started while step 4 was thinking would
      # be reading this script by byte offset, and patching it would corrupt the live queue.
      if [ "$(pdq_count)" != "0" ] || [ "$(busy)" != "0" ]; then
        say "REFUSED (exit 6): the machine stopped being idle at the last look before patching"
        say "  (snapshots=$(pdq_count) busy=$(busy)). Nothing was changed."
        exit 6
      fi
      BAK="$QUEUE_SCRIPT.bak_$(date +%Y%m%d_%H%M%S)"
      cp "$QUEUE_SCRIPT" "$BAK"
      say "  backup: $BAK"
      if ! patch -p1 --binary --batch --forward -r "$PATCH_WORK/rej" -i "$PATCH_FILE" "$QUEUE_SCRIPT" > "$PATCH_WORK/apply.txt" 2>&1; then
        say "REFUSED (exit 7): the patch failed to apply for real after its dry-run succeeded."
        sed 's/^/    | /' "$PATCH_WORK/apply.txt"
        cp "$BAK" "$QUEUE_SCRIPT"; say "  restored from $BAK"
        exit 7
      fi
      sed 's/^/    | /' "$PATCH_WORK/apply.txt"
      CRLF_AFTER=$(crlf_bytes "$QUEUE_SCRIPT")
      say "  applied. md5 $(md5sum "$QUEUE_SCRIPT" | cut -d' ' -f1), CR bytes $CRLF_BEFORE -> $CRLF_AFTER"
      if [ "$CRLF_BEFORE" -gt 0 ] && [ "$CRLF_AFTER" = "0" ]; then
        say "REFUSED (exit 7): the file's CRLF line endings were destroyed -- --binary did not hold."
        cp "$BAK" "$QUEUE_SCRIPT"; say "  restored from $BAK"
        exit 7
      fi
      if ! verify_patched; then
        cp "$BAK" "$QUEUE_SCRIPT"
        say "REFUSED (exit 7): verification failed after patching. Restored from $BAK (md5 $(md5sum "$QUEUE_SCRIPT" | cut -d' ' -f1))."
        exit 7
      fi
    fi;;
esac

# ---------------------------------------------------------------- step 5: start the queue

QLOG="runs/logs/queue_unattended.$(date +%m%d_%H%M).log"
say "step 5/5  start command: nohup bash $QUEUE_SCRIPT > $QLOG 2>&1 &"

if [ "$MODE" = "dry" ]; then
  say "[dry-run] nothing above was applied and nothing was started."
  exit 0
fi

# Final look. Everything checked so far can have changed while step 4 ran.
if [ "$(pdq_count)" != "0" ]; then
  say "REFUSED (exit 6): a queue appeared at the final look ($(pdq_list)). Not starting a second one."
  exit 6
fi
if [ "$(busy)" != "0" ] || render_lock_live; then
  say "REFUSED (exit 6): the machine stopped being idle at the final look (busy=$(busy)). Not starting."
  exit 6
fi

mkdir -p runs/logs
nohup bash "$QUEUE_SCRIPT" > "$QLOG" 2>&1 &
QPID=$!
disown "$QPID" 2>/dev/null || true
say "  launched, msys pid $QPID, log $QLOG"

ok=0
for i in $(seq 1 12); do
  sleep 5
  if [ -s "$QLOG" ] && grep -q "immutable copy:" "$QLOG" 2>/dev/null; then ok=1; break; fi
done
QWIN=$(powershell -NoProfile -Command \
  "@(Get-CimInstance Win32_Process | Where-Object { \$_.CommandLine -like '*queue_unattended.sh*' -and \$_.CommandLine -notlike '*Win32_Process*' -and \$_.CommandLine -notlike '*shell-snapshots*' } | ForEach-Object { \$_.ProcessId }) -join ','" \
  2>/dev/null | tr -d '\r ' | head -1)

if [ "$ok" != "1" ] || ! kill -0 "$QPID" 2>/dev/null; then
  say "STARTED BUT DID NOT COME UP (exit 8): no 'immutable copy:' line within 60 s, or the process died."
  say "  log so far:"; sed 's/^/    | /' "$QLOG" 2>/dev/null | head -20
  exit 8
fi

say "================================================================"
say "QUEUE RESTARTED, PATCHED."
say "  queue log        : $QLOG"
say "  msys pid         : $QPID   (stop it with: kill $QPID)"
# Informational only, and it lists EVERY process carrying queue_unattended.sh -- including any
# that were already there. The gate above is the snapshot count, not this.
say "  windows pids with queue_unattended.sh on the command line: ${QWIN:-unresolved}"
say "  queue snapshots  : $(pdq_count) [$(pdq_list)]   (must be exactly 1)"
say "  first lines:"
head -3 "$QLOG" | sed 's/^/    | /'
say ""
say "The queue renders whatever is renderable, in deadline order. The four i2v episodes become"
say "renderable only after their film json is rebuilt, and that rebuild is downstream of a human"
say "reading the shipped-frames contact sheets. See runs/i2v_plans/WATCHER.md."
say "================================================================"
exit 0
