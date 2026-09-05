#!/usr/bin/env python3
"""Claude Code PreToolUse hook: block destructive Bash commands, and refuse anything that
would compete with a long-running job that is ACTUALLY in flight.

Reads hook JSON from stdin. Exit code 2 blocks a tool call.

    python scripts/guard_destructive.py --selftest      # prove both directions, cheaply

Why this file was rewritten on 2026-08-12
-----------------------------------------
PD_CANON section 4 forbids heavy work beside a live render. On 2026-08-11 an agent ran
`build_case_film_generic.py` while marmet was rendering and nothing refused it. Four separate
defects were measured, not guessed:

1. `render_in_flight()` looked ONLY for a live `remotion render`. The queue's own busy detector
   (`scripts/queue_unattended.sh`, function `busy()`) counts six job classes, including
   `_finish_episode.sh`. The build that slipped through ran at 13:48-13:51Z; marmet's finisher
   had started 13:45:43Z but the `remotion render` process did not exist until 13:59:06Z. A
   second, narrower definition of "busy" is exactly how it got through. There is now ONE
   definition, copied from the queue and drift-checked by --selftest.
2. Any exception in the detector returned None, i.e. ALLOW. A guard that cannot measure must
   refuse, not guess -- EP52 and EP62 died with no error line at all.
3. A second `remotion render`, a second `queue_unattended.sh` and a second `_finish_episode.sh`
   were not in any list, so the guard would happily start a job on top of a live one.
4. The hook was wired for the `Bash` tool only; a `PowerShell` tool call never reached it.

The `--help`/`--version`/8-hour exclusions are NOT decoration either: on 2026-08-11 a hung
`remotion render --help` held the queue's busy count at 12 for 545 minutes. Without those
exclusions this guard would have refused every heavy command for nine hours.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AUDIT = ROOT / "runs" / "logs" / "guard_destructive.audit.log"

# The detector must return well inside the hook timeout in .claude/settings.json, or Claude Code
# kills the hook and the refusal never happens -- which is indistinguishable from allowing.
DETECT_TIMEOUT_S = 6

BLOCK_PATTERNS = [
    (re.compile(r"(^|[;&|]\s*)rm\s+-[^\n]*r[^\n]*f\s+/(?:\s|$)"), "recursive deletion of filesystem root"),
    (re.compile(r"\brm\s+-rf\s+\.(?:\s|$)"), "recursive deletion of current directory"),
    (re.compile(r"\bgit\s+reset\s+--hard\b"), "destructive git reset"),
    (re.compile(r"\bgit\s+clean\s+-[^\n]*f"), "destructive git clean"),
    (re.compile(r"\bgit\s+push\s+[^\n]*--force(?:-with-lease)?\b"), "force push"),
    (re.compile(r"\bDROP\s+(?:DATABASE|SCHEMA|TABLE)\b", re.I), "destructive SQL"),
    (re.compile(r"\bTRUNCATE\s+TABLE\b", re.I), "destructive SQL"),
    (re.compile(r"\b(public|publish)\b[^\n]*(youtube|video)", re.I), "public publishing requires explicit approval"),
]


# Commands that put a heavy, sustained load on the same disk a render is streaming frames to.
# A long-form render holds the disk for two hours; anything here run beside it can kill it, and
# the render dies with no error line, so the cause is not obvious from the log afterwards.
DISK_HEAVY = [
    (re.compile(r"\bdu\s+-\w*[sh]"), "du over a large tree"),
    (re.compile(r"\bfind\s+\S+\s+-(newermt|type|name|size)\b"), "find over a large tree"),
    (re.compile(r"\bbuild_asset_manifest\w*\.py"), "asset manifest rebuild (ffprobe over the pool)"),
    (re.compile(r"\bbuild_case_film\w*\.py"), "film.json build (ffprobe over every staged clip)"),
    (re.compile(r"\bbuild_\w*thumbnails?\w*\.py"), "thumbnail compositing (reads 4K plates)"),
    (re.compile(r"\bcheck_final_acceptance\.py"), "acceptance scan of a full-length master"),
    (re.compile(r"\bcheck_shipped_frames\.py"), "frame extraction from a full-length master"),
    (re.compile(r"\bpd_postrender_gate\.py"), "post-render gate frame extraction"),
    (re.compile(r"\bffmpeg\b(?![^\n]*-t\s+[0-9])"), "unbounded ffmpeg pass"),
    (re.compile(r"\bbuild_motion_from_plates\.py|\bcomfy_wan\.py|\bsd35_gen\.py"), "GPU generation"),
]

# Jobs that must never run a SECOND time beside a live one. Not about disk: the GPU takes exactly
# one job, and two queues racing means two different snapshots of _finish_episode.sh decide what
# the same film contains (that happened on 2026-08-11, 37 minutes apart).
RENDER_EXCLUSIVE = [
    (re.compile(r"\bremotion\s+render\b"), "starting a second `remotion render`"),
    (re.compile(r"\bqueue_unattended\.sh\b"), "starting a second unattended queue"),
    (re.compile(r"\b_finish_episode\.sh\b"), "starting a second episode finisher"),
    (re.compile(r"\bpd_render_guarded\.sh\b"), "starting a second guarded render"),
]

# Reading ABOUT a job is not running it. Without this, `grep -n queue_unattended.sh scripts/`
# would be refused, and the guard would become the wall it is meant not to be. This exemption is
# applied ONLY to RENDER_EXCLUSIVE; DISK_HEAVY matching is left byte-identical to before, because
# a `grep -r` over the media tree really is disk-heavy.
READ_ONLY_LEAD = re.compile(
    r"\s*(?:sudo\s+)?(?:grep|rg|egrep|fgrep|cat|bat|less|more|head|tail|wc|ls|stat|file|diff|"
    r"git|echo|printf|awk|sed|sort|uniq|nl|cut|tr|od|xxd|basename|dirname|realpath|test|\[)\b",
    re.I)

_SPLIT = re.compile(r"\|\||&&|[;\n|&]")

# ---------------------------------------------------------------------------------------------
# ONE definition of "the machine is busy", copied verbatim in meaning from busy() in
# scripts/queue_unattended.sh. --selftest fails if the two drift apart. Do not edit one alone.
# (queue_unattended.sh itself must never be edited while a queue is running: bash reads a running
# script by byte offset. Reading it, as --selftest does, is safe.)
BUSY_INCLUDE = ("*remotion*render*", "*_finish_episode.sh*", "*check_final_acceptance*",
                "*_chain_i2v*", "*ComfyUI*", "*build_case_bgm*")
BUSY_EXCLUDE = ("*Win32_Process*", "*shell-snapshots*", "*--help*", "*--version*")
BUSY_MAX_AGE_H = 8


class DetectorFailed(RuntimeError):
    """The process table could not be read. Never means 'nothing is running'."""


def _ps_probe() -> list[str]:
    """Command lines of every live PD job, per queue_unattended.sh busy(). Raises DetectorFailed."""
    inc = " -or ".join(f"$_.CommandLine -like '{p}'" for p in BUSY_INCLUDE)
    exc = " ".join(f"-and $_.CommandLine -notlike '{p}'" for p in BUSY_EXCLUDE)
    query = (f"Get-CimInstance Win32_Process | Where-Object {{ ({inc}) {exc} "
             f"-and ((Get-Date) - $_.CreationDate).TotalHours -lt {BUSY_MAX_AGE_H} }} | "
             f"ForEach-Object {{ $_.CommandLine }}")
    try:
        r = subprocess.run(["powershell", "-NoProfile", "-Command", query], capture_output=True,
                           text=True, encoding="utf-8", errors="replace", timeout=DETECT_TIMEOUT_S)
    except Exception as exc_:  # noqa: BLE001 - timeout, missing powershell, anything
        raise DetectorFailed(f"could not read the process table: {exc_}") from exc_
    if r.returncode != 0:
        raise DetectorFailed(f"powershell exited {r.returncode}: {(r.stderr or '').strip()[:160]}")
    return [ln.strip() for ln in (r.stdout or "").splitlines() if ln.strip()]


def _label(line: str) -> str:
    low = line.lower()
    if "remotion" in low and "render" in low:
        m = re.search(r"render\s+([A-Za-z0-9_.\-]+)", line)
        return f"`remotion render {m.group(1)}`" if m else "a `remotion render`"
    for key, name in (("_finish_episode", "the episode finisher (_finish_episode.sh)"),
                      ("_chain_i2v", "an i2v chain"),
                      ("check_final_acceptance", "the acceptance gate"),
                      ("comfyui", "ComfyUI"),
                      ("build_case_bgm", "the BGM build")):
        if key in low:
            return name
    return "a long-running PD job"


def busy_job(probe=None) -> str | None:
    """Name of the live job, or None when the machine is idle. Raises DetectorFailed."""
    lines = (probe or _ps_probe)()
    labels = [_label(ln) for ln in lines]
    for lb in labels:                       # name the render first; it is the expensive one
        if "remotion render" in lb:
            return lb
    return labels[0] if labels else None


def _segments(command: str) -> list[str]:
    return [s for s in _SPLIT.split(command) if s.strip()]


def _first(patterns, command: str, exempt_read_only: bool) -> str | None:
    parts = _segments(command) if exempt_read_only else [command]
    for seg in parts:
        if exempt_read_only and READ_ONLY_LEAD.match(seg):
            continue
        for pattern, reason in patterns:
            if pattern.search(seg):
                return reason
    return None


def _audit(tool: str, command: str, verdict: str, reason: str) -> None:
    """Record every decision. 'Did the hook even fire?' must be answerable by measurement --
    on 2026-08-11 it cost an investigation to establish that it had not."""
    try:
        AUDIT.parent.mkdir(parents=True, exist_ok=True)
        with AUDIT.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps({"ts": datetime.now().astimezone().isoformat(timespec="seconds"),
                                 "tool": tool, "verdict": verdict, "reason": reason,
                                 "command": command[:300]}, ensure_ascii=False) + "\n")
    except Exception:  # noqa: BLE001 - auditing must never wedge a tool call
        pass


def decide(command: str, tool: str = "", probe=None) -> int:
    """0 = allow, 2 = block. `probe` is injectable so both directions can be demonstrated."""
    for pattern, reason in BLOCK_PATTERNS:
        if pattern.search(command):
            print(f"Blocked: {reason}. Use an approved, scoped alternative.", file=sys.stderr)
            _audit(tool, command, "BLOCK", reason)
            return 2

    reason = _first(DISK_HEAVY, command, exempt_read_only=False)
    if reason is None:
        reason = _first(RENDER_EXCLUSIVE, command, exempt_read_only=True)
    if reason is None:
        _audit(tool, command, "allow", "")
        return 0

    try:
        job = busy_job(probe)
    except DetectorFailed as exc:
        print(f"Blocked: {reason} -- and the guard could NOT determine whether a render is in "
              f"flight ({exc}).\n"
              f"PD_CANON section 4 forbids this beside a live render, and a guard that cannot "
              f"measure must refuse rather than guess: EP52 morton and EP62 greene both died with "
              f"no error line at all.\n"
              f"Measure first: `py -3.11 scripts/handover_snapshot.py --print`. If the machine is "
              f"genuinely idle, the process table is broken and that is the thing to fix.",
              file=sys.stderr)
        _audit(tool, command, "BLOCK-FAILCLOSED", f"{reason}; detector failed: {exc}")
        return 2

    if job:
        print(f"Blocked: {reason} while {job} is running.\n"
              f"EP62 greene died twice this way on 2026-08-09 -- no error line, two hours lost -- "
              f"and EP52 morton before it. Wait for the render, or use a bounded read (a single "
              f"ffprobe, `ls` on one directory, a log tail).",
              file=sys.stderr)
        _audit(tool, command, "BLOCK-BUSY", f"{reason}; live: {job}")
        return 2

    _audit(tool, command, "allow-idle", reason)
    return 0


# ---------------------------------------------------------------------------------------------
def _drift() -> tuple[bool, str]:
    """The queue owns the definition of 'busy'. Fail loudly if this file has drifted from it."""
    src = ROOT / "scripts" / "queue_unattended.sh"
    try:
        text = src.read_text(encoding="utf-8", errors="replace")
    except Exception as exc:  # noqa: BLE001
        return False, f"could not read {src}: {exc}"
    m = re.search(r"^busy\(\)\s*\{(.*?)^\}", text, re.S | re.M)
    if not m:
        return False, "could not find busy() in queue_unattended.sh"
    body = m.group(1)
    inc = set(re.findall(r"-like\s+'([^']+)'", body))
    exc = set(re.findall(r"-notlike\s+'([^']+)'", body))
    if inc != set(BUSY_INCLUDE) or exc != set(BUSY_EXCLUDE):
        return False, (f"drift from queue_unattended.sh busy():\n"
                       f"    include here {sorted(BUSY_INCLUDE)}\n    include there {sorted(inc)}\n"
                       f"    exclude here {sorted(BUSY_EXCLUDE)}\n    exclude there {sorted(exc)}")
    return True, f"include={len(inc)} exclude={len(exc)} clauses identical to queue_unattended.sh"


def selftest() -> int:
    BUILD = "py -3.11 scripts/build_case_film_generic.py --config episodes/_planning/EP67.json"
    LIVE = lambda: ["node remotion-cli.js render Ep65Marmet ../out/marmet.mp4"]  # noqa: E731
    IDLE = lambda: []                                                            # noqa: E731
    def BOOM():
        raise DetectorFailed("simulated: powershell timed out after 6s")

    cases = [
        ("render live  -> build_case_film_generic REFUSED", BUILD, LIVE, 2),
        ("render live  -> second remotion render REFUSED", "cd remotion && npx remotion render Ep62Greene o.mp4", LIVE, 2),
        ("render live  -> second queue REFUSED", "bash scripts/queue_unattended.sh", LIVE, 2),
        ("render live  -> second finisher REFUSED", "bash scripts/_finish_episode.sh greene Ep62Greene 62", LIVE, 2),
        ("render live  -> git status ALLOWED", "git status --porcelain", LIVE, 0),
        ("render live  -> check_queue_will_stall ALLOWED", "py -3.11 scripts/check_queue_will_stall.py", LIVE, 0),
        ("render live  -> log tail ALLOWED", "tail -5 out_render_marmet.mp4.log", LIVE, 0),
        ("render live  -> single ffprobe ALLOWED", "ffprobe -v error -show_format out/marmet.mp4", LIVE, 0),
        ("render live  -> grep ABOUT the queue ALLOWED", 'grep -n "queue_unattended.sh" scripts/*.py', LIVE, 0),
        ("machine IDLE -> build_case_film_generic ALLOWED", BUILD, IDLE, 0),
        ("machine IDLE -> second remotion render ALLOWED", "npx remotion render Ep62Greene o.mp4", IDLE, 0),
        ("detector RAISES -> build_case_film_generic REFUSED", BUILD, BOOM, 2),
        ("detector RAISES -> git status still ALLOWED", "git status", BOOM, 0),
        ("always -> rm -rf / REFUSED", "rm -rf / ", IDLE, 2),
        ("always -> git reset --hard REFUSED", "git reset --hard origin/main", IDLE, 2),
    ]
    bad = 0
    print(f"{'expect':>7}  {'got':>4}  case")
    print("-" * 78)
    for name, cmd, probe, expect in cases:
        import io, contextlib
        with contextlib.redirect_stderr(io.StringIO()):
            got = decide(cmd, "selftest", probe)
        ok = got == expect
        bad += 0 if ok else 1
        print(f"{expect:>7}  {got:>4}  {'ok ' if ok else 'FAIL'} {name}")
    ok, msg = _drift()
    bad += 0 if ok else 1
    print("-" * 78)
    print(f"{'drift':>7}  {'ok ' if ok else 'FAIL'}  {msg}")
    print(f"\n{len(cases) + 1 - bad}/{len(cases) + 1} checks pass")
    return 1 if bad else 0


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if "--selftest" in argv:
        return selftest()
    try:
        payload = json.load(sys.stdin)
    except Exception:  # noqa: BLE001
        _audit("", "", "allow-unparseable-payload", "stdin was not hook JSON")
        return 0
    tool_input = payload.get("tool_input", {})
    command = tool_input.get("command", "") if isinstance(tool_input, dict) else ""
    return decide(command, str(payload.get("tool_name", "")))


if __name__ == "__main__":
    raise SystemExit(main())
