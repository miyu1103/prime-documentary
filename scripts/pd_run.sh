#!/bin/bash
# Start a long job only after the same code path has survived a tiny run, hold a lock so two
# of them can never overlap, and surface the first error immediately instead of hours later.
#
# The three failures this covers, all from 2026-08-01:
#   * an episode rebuild died on a syntax error inside the launched command and sat dead for
#     three hours, because nothing looked at the log after starting it;
#   * a second render started on top of a running one and both slowed to a crawl;
#   * a two-hour render was spent on inputs that a thirty-second check would have rejected.
#
#   scripts/pd_run.sh --name ep55 --smoke "py -3.11 scripts/check_episode_inputs.py --slug burge" \
#       -- bash scripts/_finish_episode.sh burge Ep55Burge 55
#
# --smoke is the cheap proof. Everything after -- is the real job. The job runs in the
# background; this returns once it has survived its first 60 seconds.
set -u
cd /c/Users/aab15/Documents/prime-documentary
export PATH="/usr/bin:/bin:$PATH"

NAME=""; SMOKE=""; LOCK_CLASS="render"
while [ $# -gt 0 ]; do
  case "$1" in
    --name) NAME="$2"; shift 2;;
    --smoke) SMOKE="$2"; shift 2;;
    --class) LOCK_CLASS="$2"; shift 2;;
    --) shift; break;;
    *) echo "unknown option $1" >&2; exit 2;;
  esac
done
[ -n "$NAME" ] || { echo "--name is required" >&2; exit 2; }
[ $# -gt 0 ] || { echo "no command given after --" >&2; exit 2; }

LOCK="out_pdrun_${LOCK_CLASS}.lock"
if [ -f "$LOCK" ]; then
  lock_pid=$(tr -d '[:space:]' < "$LOCK" 2>/dev/null)
  if [ -n "$lock_pid" ] && tasklist //FI "PID eq $lock_pid" 2>/dev/null | grep -q "$lock_pid"; then
    echo "[run] REFUSED: a '$LOCK_CLASS' job is already running (Windows pid $lock_pid). Two of these"
    echo "      must never overlap -- wait for it, or stop it deliberately."
    exit 1
  fi
  echo "[run] clearing stale '$LOCK_CLASS' lock (Windows pid ${lock_pid:-unknown} is not live)"
  rm -f "$LOCK"
fi

if [ -n "$SMOKE" ]; then
  echo "[run] smoke: $SMOKE"
  if ! eval "$SMOKE"; then
    echo "[run] REFUSED: the cheap check failed. Nothing expensive was started." >&2
    exit 1
  fi
fi

LOG="out_pdrun_${NAME}.log"
: > "$LOG"
nohup "$@" >> "$LOG" 2>&1 &
JOB=$!
# MSYS $! is not a Windows PID. tasklist cannot see it, so translate via ps -W.
WINJOB=$(ps -W | awk -v p="$JOB" '$1 == p { print $4; exit }')
case "$WINJOB" in (''|*[!0-9]*) echo "[run] cannot resolve Windows pid for MSYS pid $JOB" >&2; kill "$JOB" 2>/dev/null; exit 1;; esac
echo "$WINJOB" > "$LOCK"
trap 'rm -f "$LOCK"' EXIT

echo "[run] started $NAME (pid $JOB) -> $LOG"
sleep 60
if ! kill -0 "$JOB" 2>/dev/null; then
  wait "$JOB"; rc=$?
  echo "[run] DIED within 60s (exit $rc). First lines:" >&2
  head -25 "$LOG" >&2
  rm -f "$LOCK"
  exit 1
fi
if grep -qiE "traceback|syntaxerror|command not found|no such file|error:" "$LOG"; then
  echo "[run] WARNING: the log already shows an error 60s in:" >&2
  grep -iE "traceback|syntaxerror|command not found|no such file|error:" "$LOG" | head -5 >&2
fi
echo "[run] alive after 60s -- $(wc -l < "$LOG") log line(s) so far"
# the lock belongs to the job, not to this shell
trap - EXIT
