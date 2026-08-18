#!/bin/bash
# Unattended i2v runner -- keeps the GPU working after the render queue runs out of renderable
# episodes. Modelled directly on scripts/queue_unattended.sh; every guard below exists because
# something on this machine already failed without it.
#
# WHY IT EXISTS
#   queue_unattended.sh renders marmet, greene and correa and then reaches openfields, ramirez,
#   pinto and hyatt. All four have ZERO motion clips, so _finish_episode.sh [4a] kills each of
#   them in seconds and the queue settles into a 10-minute retry loop that can never succeed.
#   The ~8 GPU-hours of planned i2v in runs/i2v_plans/ is what unblocks them, and nothing starts
#   it. This does.
#
# HOW IT COEXISTS WITH THE RENDER QUEUE  (do not "fix" this -- it is deliberate and symmetric)
#   * This runner uses queue_unattended.sh's busy() detector VERBATIM: same six job-class
#     patterns, same four exclusions (--help / --version / Win32_Process / shell-snapshots),
#     same 8-hour age cap. A second, differently-wrong detector is what let a hung
#     `remotion render --help` hold this machine at busy=12 for 545 minutes on 2026-08-11.
#     If that detector is ever changed, change it in BOTH files or in neither.
#   * The queue's busy() already counts `*_chain_i2v*` and `*ComfyUI*`. So the moment this
#     runner launches a chain, the render queue sees the machine as busy and waits. That is
#     correct: one 4090, one heavy GPU job.
#   * Renders outrank i2v. Two things enforce that:
#       - this runner needs SIX consecutive idle readings (3 min) where the queue needs three
#         (1.5 min), so in a simultaneous race the queue wins;
#       - it re-reads busy() one last time immediately before launching and backs off if the
#         answer changed, and it defers to a live out_pdrun_render.lock (the same file, read the
#         same way, that pd_run.sh itself writes -- not a new process scanner).
#   * This runner never takes pd_run.sh's "render" lock class. Taking it would make the queue
#     print "refused -- next" and skip real renders.
#   * The watcher's own command line matches none of the busy() patterns, so sitting here
#     waiting never blocks a render. Only an actual chain does.
#
# WHAT IT RUNS
#   The plans in runs/i2v_plans/*.json, in the order declared in runs/i2v_plans/README.md
#   (hyatt -> ramirez -> openfields, smallest need first; pinto last, only if its plan exists).
#   Phases run strictly in the order the plan declares them, because that ordering IS the plan's
#   priority tiering -- hands and faces first -- so an interrupted run has already produced the
#   plates that matter most. Plan files are never edited and no declared conversion count is
#   ever lowered.
#
# RESUME
#   Progress is the frame dirs on disk, counted by the same rule _chain_i2v_robust.sh uses
#   (a wan_frames_<slug>_<plate> dir holding >= 40 png). A phase whose cumulative target is
#   already met is skipped; anything else is handed to the chain, which does its own on-disk
#   resume and is the authority. Nothing here keeps a counter of its own.
#
# THE ASSEMBLER FPS CORRECTION
#   _chain_i2v_robust.sh assembles after every chunk at the assembler's default --fps-in 24,
#   which makes a 121-frame clip play 5.04 s. ramirez's mean cut is 5.30 s and hyatt's is 5.81 s,
#   so at 24 every motion cut in those two would carry loopSource and rewind mid-shot (the EP62
#   greene defect). The plans therefore declare assemble_fps_in 20 and 18. assemble_episode_i2v.py
#   skips an output that already exists, so after each phase this moves any master whose measured
#   duration is the wrong one into ai_video/<slug>/_superseded_fps24/ (moved, never deleted) and
#   re-assembles at the declared rate. openfields declares 24 and is untouched.
#
# STOPPING
#   touch runs/i2v_plans/STOP_I2V_WATCH   -- no new phase starts; a running chain finishes first.
#
# USAGE
#   bash scripts/i2v_watch.sh                 # run (blocks; launch it with nohup ... &)
#   bash scripts/i2v_watch.sh --dry-run       # full preflight + exact command sequence, runs nothing
#   bash scripts/i2v_watch.sh --busy          # print the shared busy() reading and exit
#   bash scripts/i2v_watch.sh --count <slug>  # print on-disk finished-clip count for a slug
#   env: I2V_MIN_FREE_GIB (default 25), I2V_IDLE_STREAK (6), I2V_POLL_SEC (30), I2V_HB_SEC (600),
#        I2V_FRAMES_ROOT (test only -- where wan_frames_* dirs are counted from)
set -u
cd /c/Users/aab15/Documents/prime-documentary
export PATH="/usr/bin:/bin:$PATH"

MIN_FREE_GIB="${I2V_MIN_FREE_GIB:-25}"
IDLE_STREAK="${I2V_IDLE_STREAK:-6}"
POLL_SEC="${I2V_POLL_SEC:-30}"
HB_SEC="${I2V_HB_SEC:-600}"
FRAMES_ROOT="${I2V_FRAMES_ROOT:-/c/Users/aab15/ae-demo}"
PLAN_DIR="runs/i2v_plans"
STOP_FILE="runs/i2v_plans/STOP_I2V_WATCH"   # fixed, so --plan-dir cannot move the stop switch
# Hard-coded, NOT ${TMPDIR:-/tmp}: TMPDIR differs between shells on this machine (one shell
# reports it empty, another E:/UserTemp/aab15), and a single-instance guard that looks in a
# different directory than the running instance wrote to is no guard at all. /tmp is where
# queue_unattended.sh's snapshots actually land, so both live in one place.
SNAP_ROOT="/tmp"

# slug:planfile:required|optional -- run order is README.md's: smallest need first.
EPISODES="hyatt:ep69_hyatt_i2v_batch.v001.json:required
ramirez:ep67_ramirez_i2v_batch.v001.json:required
openfields:ep66_openfields_i2v_batch.v001.json:required
pinto:ep68_pinto_i2v_batch.v001.json:optional"

DRY=0
LOG=""
while [ $# -gt 0 ]; do
  case "$1" in
    --dry-run) DRY=1; shift;;
    --log) LOG="$2"; shift 2;;
    --min-free-gib) MIN_FREE_GIB="$2"; shift 2;;
    --plan-dir) PLAN_DIR="$2"; shift 2;;   # tests only; the stop switch stays where it is
    *) break;;   # --busy / --count are handled below, once busy()/count_done() exist
  esac
done

# ---------------------------------------------------------------- shared primitives

# VERBATIM from scripts/queue_unattended.sh. Idleness is asked of WMI because it carries the
# full command line; `ps -W` prints only the interpreter path and would answer 0 with a render
# plainly running.
busy() {
  powershell -NoProfile -Command \
    "@(Get-CimInstance Win32_Process | Where-Object { (\$_.CommandLine -like '*remotion*render*' -or \$_.CommandLine -like '*_finish_episode.sh*' -or \$_.CommandLine -like '*check_final_acceptance*' -or \$_.CommandLine -like '*_chain_i2v*' -or \$_.CommandLine -like '*ComfyUI*' -or \$_.CommandLine -like '*build_case_bgm*') -and \$_.CommandLine -notlike '*Win32_Process*' -and \$_.CommandLine -notlike '*shell-snapshots*' -and \$_.CommandLine -notlike '*--help*' -and \$_.CommandLine -notlike '*--version*' -and ((Get-Date) - \$_.CreationDate).TotalHours -lt 8 }).Count" \
    2>/dev/null | tr -d '\r ' | head -1
}

# Same rule as _chain_i2v_robust.sh count_done(): a frame dir with >= 40 png is one finished clip.
count_done() {
  local slug="$1" n=0 d
  for d in "$FRAMES_ROOT"/wan_frames_"${slug}"_*; do
    [ -d "$d" ] || continue
    if [ "$(ls "$d"/*.png 2>/dev/null | wc -l)" -ge 40 ]; then n=$((n + 1)); fi
  done
  echo "$n"
}

# Any failure to measure reports 0, which trips the disk guard rather than hiding it.
free_gib() { df -k /c 2>/dev/null | tail -1 | awk '{printf "%d", $4/1048576} END{if (NR == 0) printf "0"}'; }

# Self-identification, not job detection: which Windows process is running THIS snapshot's copy
# of the script. The snapshot basename is unique, so the answer is unambiguous.
#
# It has to be asked this way. `ps -W | awk '$1==$$'` answers correctly BEFORE the re-exec and
# wrongly after it: MSYS implements exec by spawning a fresh Windows process while keeping the
# MSYS pid, so the pre-exec Windows pid is dead the moment stage 2 starts. Recording that number
# made the staleness sweep declare a live watcher stale and let a second instance start -- caught
# on 2026-08-12 with both instances running and heartbeating into different logs.
own_winpid() {
  powershell -NoProfile -Command \
    "(Get-CimInstance Win32_Process | Where-Object { \$_.CommandLine -like '*$1/i2v_watch.sh*' -and \$_.CommandLine -notlike '*Win32_Process*' -and \$_.CommandLine -notlike '*shell-snapshots*' } | Sort-Object CreationDate | Select-Object -First 1).ProcessId" \
    2>/dev/null | tr -d '\r ' | head -1
}

# pd_run.sh writes this file and checks it exactly this way. Reading it is deference to the
# render queue's own lock, not a second process detector.
render_lock_live() {
  local p
  [ -f out_pdrun_render.lock ] || return 1
  p=$(tr -d '[:space:]' < out_pdrun_render.lock 2>/dev/null)
  [ -n "$p" ] || return 1
  tasklist //FI "PID eq $p" 2>/dev/null | grep -q "$p"
}

case "${1:-}" in
  --busy)  busy; exit 0;;
  --count) echo "$(count_done "${2:?slug required}")"; exit 0;;
esac

# ---------------------------------------------------------------- preflight / guards

if [ -f "$STOP_FILE" ]; then
  echo "[i2v] REFUSING TO START: $STOP_FILE exists. Remove it first: rm $STOP_FILE" >&2
  exit 4
fi

# Second-instance guard. Counting our own process is unreliable -- one bash job shows as 1 or 2
# in WMI depending on the launcher -- so the signal is a snapshot directory carrying a Windows
# pid, swept for staleness the way pd_run.sh sweeps its lock.
if [ "$DRY" = "0" ] && [ -z "${I2V_WATCH_SNAP:-}" ]; then
  now=$(date +%s)
  for d in "$SNAP_ROOT"/pdi2v.*; do
    [ -d "$d" ] || continue
    born=$(cat "$d/started_at" 2>/dev/null | tr -d '[:space:]')
    # A watcher that is still resolving its own Windows pid must not be swept out from under
    # itself, so anything younger than two minutes counts as live regardless of the pid file.
    if [ -n "$born" ] && [ $((now - born)) -lt 120 ]; then continue; fi
    p=$(cat "$d/winpid" 2>/dev/null | tr -d '[:space:]')
    if [ -z "$p" ] || ! tasklist //FI "PID eq $p" 2>/dev/null | grep -q "$p"; then
      echo "[i2v] sweeping stale snapshot $d (winpid ${p:-unknown} not live)"
      rm -rf "$d"
    fi
  done
  live=$(ls -d "$SNAP_ROOT"/pdi2v.* 2>/dev/null | wc -l)
  if [ "$live" -gt 0 ]; then
    echo "[i2v] REFUSED: another i2v_watch is live ($(ls -d "$SNAP_ROOT"/pdi2v.* 2>/dev/null | tr '\n' ' '))" >&2
    exit 5
  fi

  SNAP=$(mktemp -d "$SNAP_ROOT/pdi2v.XXXXXX")
  date +%s > "$SNAP/started_at"
  # Renders run from a snapshot of _finish_episode.sh because editing a script mid-flight
  # desynchronises bash's byte offset and killed correa's step 7. The same applies to this file
  # and to the chain driver, so both are frozen and the frozen copies are what run.
  cp scripts/i2v_watch.sh "$SNAP/i2v_watch.sh"
  cp scripts/_chain_i2v_robust.sh "$SNAP/_chain_i2v_robust.sh"
  [ -z "$LOG" ] && LOG="runs/logs/i2v_watch.$(date +%Y%m%d_%H%M%S).log"
  mkdir -p runs/logs
  echo "[i2v] snapshot=$SNAP log=$LOG"
  export I2V_WATCH_SNAP="$SNAP" I2V_WATCH_LOG="$LOG"
  exec bash "$SNAP/i2v_watch.sh" --log "$LOG"
fi

SNAP="${I2V_WATCH_SNAP:-}"
[ -n "$LOG" ] || LOG="${I2V_WATCH_LOG:-runs/logs/i2v_watch.$(date +%Y%m%d_%H%M%S).log}"
if [ "$DRY" = "0" ]; then
  # Windows will not unlink the script bash is still reading, so this is best effort; dropping
  # winpid is what actually lets the next run's staleness sweep collect the directory.
  trap 'rm -f "$SNAP/winpid" 2>/dev/null; rm -rf "$SNAP" 2>/dev/null' EXIT
  exec >> "$LOG" 2>&1
  WORK="$SNAP"
  CHAIN="$SNAP/_chain_i2v_robust.sh"
else
  WORK=$(mktemp -d "$SNAP_ROOT/pdi2vdry.XXXXXX")
  trap 'rm -rf "$WORK"' EXIT
  CHAIN="scripts/_chain_i2v_robust.sh"
fi

say() { echo "[i2v] $*"; }

if [ "$DRY" = "0" ]; then
  WINPID=$(own_winpid "$(basename "$SNAP")")
  case "$WINPID" in (''|*[!0-9]*) echo "[i2v] cannot resolve own Windows pid after re-exec" >&2; exit 6;; esac
  echo "$WINPID" > "$SNAP/winpid"
  echo "$WINPID" > "${LOG%.log}.pid"
fi

say "=== i2v_watch start $(date) dry_run=$DRY ==="
[ "$DRY" = "0" ] && say "winpid=$WINPID snapshot=$SNAP  (stop with: touch $STOP_FILE)"
say "config: min_free=${MIN_FREE_GIB}GiB idle_streak=$IDLE_STREAK poll=${POLL_SEC}s heartbeat=${HB_SEC}s"
say "frames root: $FRAMES_ROOT   chain: $CHAIN"

# ---------------------------------------------------------------- expand the plans

# The plan files carry the exact chain invocation, but with $P_PEOPLE / $N_PEOPLE placeholders
# that only make sense next to prompt_regimes. Rather than eval a string out of a JSON file,
# every argument is parsed with a strict regex, cross-checked against the plan's own structured
# fields, and re-emitted as a tab-separated runbook; the long prompts go to files so nothing has
# to survive a second round of shell quoting. A plan that does not agree with itself is refused.
expand_plans() {
  py -3.11 - "$WORK" "$PLAN_DIR" <<'PYEOF' 2>&1
import json, os, re, sys
work, plan_dir = sys.argv[1], sys.argv[2]
EPISODES = [("hyatt", "ep69_hyatt_i2v_batch.v001.json", True),
            ("ramirez", "ep67_ramirez_i2v_batch.v001.json", True),
            ("openfields", "ep66_openfields_i2v_batch.v001.json", True),
            ("pinto", "ep68_pinto_i2v_batch.v001.json", False)]
CMD = re.compile(r'bash\s+scripts/_chain_i2v_robust\.sh\s+(\S+)\s+(\d+)\s+([A-Za-z]{1,3})\s+(\d+)\s+"([^"]*)"\s+(\d+)\s*$')
rows, fatal = [], []
for slug, fname, required in EPISODES:
    path = os.path.join(plan_dir, fname)
    if not os.path.isfile(path):
        if required:
            fatal.append(f"MISSING REQUIRED PLAN {path}")
        else:
            print(f"note: optional plan {fname} is absent -- {slug} will be skipped", file=sys.stderr)
        continue
    try:
        d = json.load(open(path, encoding="utf-8"))
    except Exception as e:
        fatal.append(f"{fname}: unreadable ({e})"); continue
    if d.get("slug") != slug:
        fatal.append(f"{fname}: slug is {d.get('slug')!r}, expected {slug!r}"); continue
    fps_in = int(d["clip_length"]["assemble_fps_in"])
    length_declared = int(d["clip_length"]["length_frames"])
    regimes = d["prompt_regimes"]
    prev = 0
    for ph in d["phases"]:
        n = int(ph["phase"])
        m = CMD.search(ph["command"])
        if not m:
            fatal.append(f"{fname} phase {n}: command does not match the canonical chain form"); break
        c_slug, target, kinds, chunk, only, length = m.group(1), int(m.group(2)), m.group(3), int(m.group(4)), m.group(5), int(m.group(6))
        seed = re.search(r"I2V_SEED_BASE=(\d+)", ph["command"])
        problems = []
        if c_slug != slug: problems.append(f"command slug {c_slug}")
        if target != int(ph["cumulative_target"]): problems.append(f"target {target} != cumulative_target {ph['cumulative_target']}")
        if target <= prev: problems.append(f"target {target} not greater than previous phase {prev}")
        if length != length_declared: problems.append(f"length {length} != clip_length.length_frames {length_declared}")
        if not re.fullmatch(r"[A-Za-z0-9_,\-]+", only): problems.append("only-list has unexpected characters")
        if not (1 <= chunk <= 64): problems.append(f"chunk {chunk}")
        if seed is None: problems.append("no I2V_SEED_BASE")
        expected = ph.get("plates_full") or (list(ph["plates"]) + list(ph.get("extra_non_people_in_this_phase", [])))
        if set(x.strip() for x in only.split(",")) != set(expected):
            problems.append("only-list does not match the phase's declared plates")
        if ph["regime"] not in regimes: problems.append(f"unknown regime {ph['regime']}")
        if problems:
            fatal.append(f"{fname} phase {n}: " + "; ".join(problems)); break
        reg = regimes[ph["regime"]]
        pf = f"{work}/{slug}.{n}.prompt".replace("\\", "/")
        nf = f"{work}/{slug}.{n}.neg".replace("\\", "/")
        open(pf, "w", encoding="utf-8").write(reg["I2V_PROMPT"])
        open(nf, "w", encoding="utf-8").write(reg["I2V_NEG"])
        rows.append("\t".join(str(x) for x in
                    [slug, n, target, kinds, chunk, only, length, seed.group(1), fps_in, pf, nf, ph["regime"]]))
        prev = target
    else:
        k = d.get("arithmetic", {}).get("conversions_needed")
        if k is not None and int(k) != prev:
            fatal.append(f"{fname}: final cumulative target {prev} != declared conversions_needed {k}")
        print(f"plan ok: {slug} K={prev} phases={len(d['phases'])} fps_in={fps_in} length={length_declared}", file=sys.stderr)
rows = [r for r in rows if r]
if fatal:
    for f in fatal: print("PLAN REFUSED: " + f, file=sys.stderr)
    sys.exit(2)
open(os.path.join(work, "runbook.tsv"), "w", encoding="utf-8").write("\n".join(rows) + "\n")
print(f"runbook: {len(rows)} phase(s)", file=sys.stderr)
PYEOF
}

if ! expand_plans; then
  say "STOPPING: a required plan is missing or does not agree with itself. Nothing was run."
  exit 2
fi
RUNBOOK="$WORK/runbook.tsv"

# ---------------------------------------------------------------- per-phase helpers

# Refuse to hand the chain a phase it cannot finish: MAX_ATTEMPTS=60 means a target that can
# never be reached costs 60 ComfyUI boots and hours of nothing.
plates_available() {
  local slug="$1" only="$2" n=0 p
  for p in $(echo "$only" | tr ',' ' '); do
    ls "H:/pd-media/assets/ai/$slug/"*"$p"*.png >/dev/null 2>&1 && n=$((n + 1))
  done
  echo "$n"
}

# assemble_episode_i2v.py skips an existing output, so a master built at the chain's default
# 24 fps-in would survive forever. Measure, move the wrong ones aside (never delete), re-assemble.
fix_fps() {
  local slug="$1" fps="$2" len="$3"
  local master="H:/pd-media/assets/ai_video/$slug/motion"
  local super="H:/pd-media/assets/ai_video/$slug/_superseded_fps24"
  if [ "$fps" != "24" ] && [ -d "$master" ]; then
    local want moved f dur
    want=$(awk -v l="$len" -v f="$fps" 'BEGIN{printf "%.3f", l/f}')
    moved=0
    for f in "$master"/*.mp4; do
      [ -f "$f" ] || continue
      dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f" 2>/dev/null)
      [ -n "$dur" ] || continue
      if [ "$(awk -v a="$dur" -v b="$want" 'BEGIN{print ((a-b)<-0.30 || (a-b)>0.30) ? 1 : 0}')" = "1" ]; then
        mkdir -p "$super"; mv "$f" "$super/"; moved=$((moved + 1))
      fi
    done
    [ "$moved" -gt 0 ] && say "  fps fix: moved $moved clip(s) built at the wrong rate to $super"
  fi
  py -3.11 scripts/assemble_episode_i2v.py --slug "$slug" --fps-in "$fps"
}

wait_idle() {
  local streak=0 n i
  for i in $(seq 1 2880); do
    [ -f "$STOP_FILE" ] && { say "STOP file present -- exiting cleanly"; exit 0; }
    n=$(busy)
    if [ "$i" = "1" ] || [ $(( i * POLL_SEC % HB_SEC )) -lt "$POLL_SEC" ]; then
      say "heartbeat $(date +%H:%M) busy=$n streak=$streak free=$(free_gib)GiB waiting-for-idle"
    fi
    if [ "${n:-1}" = "0" ] && ! render_lock_live; then
      streak=$((streak + 1))
      if [ "$streak" -ge "$IDLE_STREAK" ]; then
        say "idle x$IDLE_STREAK $(date +%H:%M)"
        sleep 20
        # last look: the queue's own wait_idle needs only three reads, so it can have started
        # something in the time this one was counting to six.
        n=$(busy)
        if [ "${n:-1}" != "0" ] || render_lock_live; then
          say "  stood down at the last check (busy=$n) -- a render got there first"
          streak=0
        else
          return 0
        fi
      fi
    else
      streak=0
    fi
    sleep "$POLL_SEC"
  done
  return 1
}

hb_start() {
  local slug="$1" phase="$2" target="$3"
  ( while :; do
      sleep "$HB_SEC"
      say "heartbeat $(date +%H:%M) chain=$slug phase=$phase done=$(count_done "$slug")/$target free=$(free_gib)GiB"
      [ "$(free_gib)" -lt "$MIN_FREE_GIB" ] && say "  WARNING free space below ${MIN_FREE_GIB}GiB while a chain is running"
    done ) &
  HB_PID=$!
}
hb_stop() { [ -n "${HB_PID:-}" ] && kill "$HB_PID" 2>/dev/null; HB_PID=""; }

# ---------------------------------------------------------------- dry run

if [ "$DRY" = "1" ]; then
  say "--- dry run: preflight ---"
  say "busy() right now = $(busy)   render lock live = $(render_lock_live && echo yes || echo no)"
  fg=$(free_gib)
  say "free on C: = ${fg}GiB (floor ${MIN_FREE_GIB}GiB)"
  if [ "$fg" -lt "$MIN_FREE_GIB" ]; then
    say "DISK GUARD WOULD TRIP: ${fg}GiB < ${MIN_FREE_GIB}GiB -- nothing would be started"
  fi
  say "--- dry run: command sequence ---"
  last=""
  while IFS=$'\t' read -r slug phase target kinds chunk only length seed fps pf nf regime <&3; do
    [ -n "$slug" ] || continue
    if [ "$slug" != "$last" ]; then
      say ""
      say "EPISODE $slug   on-disk finished clips = $(count_done "$slug")   assemble --fps-in $fps"
      last="$slug"
    fi
    avail=$(plates_available "$slug" "$only")
    done_now=$(count_done "$slug")
    if [ "$done_now" -ge "$target" ]; then verdict="SKIP (done=$done_now >= target=$target)"; else verdict="RUN"; fi
    say "  phase $phase [$regime] target=$target plates=$(echo "$only" | tr ',' ' ' | wc -w) available=$avail -> $verdict"
    say "    I2V_PROMPT=\$(cat $pf) I2V_NEG=\$(cat $nf) I2V_SEED_BASE=$seed \\"
    say "      bash $CHAIN $slug $target $kinds $chunk \"$only\" $length"
    say "    then: py -3.11 scripts/assemble_episode_i2v.py --slug $slug --fps-in $fps"
  done 3< "$RUNBOOK"
  say ""
  say "--- dry run: nothing above was executed ---"
  exit 0
fi

# ---------------------------------------------------------------- main loop

say "busy() at start = $(busy) -- a non-zero reading means a render is live and this waits."

last_slug=""
skip_ep=""
# fd 3, so nothing the chain or a python step reads can swallow the runbook.
while IFS=$'\t' read -r slug phase target kinds chunk only length seed fps pf nf regime <&3; do
  [ -n "$slug" ] || continue
  [ "$slug" = "$skip_ep" ] && continue
  [ -f "$STOP_FILE" ] && { say "STOP file present -- exiting cleanly before $slug phase $phase"; exit 0; }

  if [ "$slug" != "$last_slug" ]; then
    say ""
    say "=== EPISODE $slug (fps_in=$fps) $(date +%H:%M) ==="
    last_slug="$slug"
  fi

  done_now=$(count_done "$slug")
  if [ "$done_now" -ge "$target" ]; then
    say "$slug phase $phase: already satisfied on disk (done=$done_now >= target=$target) -- skipping"
    continue
  fi

  fg=$(free_gib)
  if [ "$fg" -lt "$MIN_FREE_GIB" ]; then
    say "!!! DISK GUARD: only ${fg}GiB free on C:, floor is ${MIN_FREE_GIB}GiB."
    say "!!! i2v leaves ~136MB of png per clip. STOPPING before $slug phase $phase. Free space, then restart this watcher."
    exit 3
  fi

  need=$((target - done_now))
  avail=$(plates_available "$slug" "$only")
  if [ "$avail" -lt "$need" ]; then
    say "$slug phase $phase: only $avail of the planned plates exist on H: but $need more clips are needed."
    say "  the chain would boot ComfyUI 60 times and never reach the target -- skipping this EPISODE."
    say "  Do NOT lower the plan's target to make this pass; stage the missing plates."
    skip_ep="$slug"
    continue
  fi

  wait_idle || { say "$slug phase $phase: still busy after the whole wait window -- moving on, NOT exiting"; continue; }

  say "--- $slug phase $phase [$regime] target=$target need=$need $(date +%H:%M) ---"
  hb_start "$slug" "$phase" "$target"
  I2V_PROMPT="$(cat "$pf")" I2V_NEG="$(cat "$nf")" I2V_SEED_BASE="$seed" \
    bash "$CHAIN" "$slug" "$target" "$kinds" "$chunk" "$only" "$length"
  rc=$?
  hb_stop
  say "$slug phase $phase: chain exit=$rc done=$(count_done "$slug")/$target $(date +%H:%M)"
  fix_fps "$slug" "$fps" "$length"
done 3< "$RUNBOOK"

say ""
say "================================================================"
say "ALL PLANNED i2v IS DONE $(date)"
for job in $EPISODES; do
  s="${job%%:*}"
  say "  $s: $(count_done "$s") frame dirs, $(ls "remotion/public/$s/motion/"*.mp4 2>/dev/null | wc -l) motion mp4"
done
say ""
say "NEXT, BY HAND -- this watcher deliberately does none of it:"
say "  1. per episode: py -3.11 scripts/check_motion_clip_stillness.py --slug <slug>"
say "     eyeball the flagged plates, then"
say "     py -3.11 scripts/build_asset_manifest_motionfirst.py --slug <slug>"
say "     py -3.11 scripts/build_case_film_generic.py --config episodes/_planning/<EPnn>_<slug>_filmconfig.v001.json"
say "     py -3.11 scripts/check_spec_satisfied.py --slug <slug>"
say "  2. THEN RESTART THE RENDER QUEUE: bash scripts/queue_unattended.sh"
say "     It is NOT restarted here. The queue has a known freshness bug -- tonight it"
say "     re-rendered marmet redundantly and cost 1h35m -- and a patch is being prepared."
say "     Restarting it is a human decision until that patch lands."
say "================================================================"
