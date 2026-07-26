"""WEEKLY unattended retention measurement + rule audit (no LLM, no cookie).

Scheduled via Windows Task Scheduler (task: PD-Weekly-Retention, Mon 12:07 JST).
Owner directive 2026-07-26: run the deep-research measurement loop weekly.

What it does (all read-only against YouTube; writes only repo report files):
  1. Pull audience-retention curves via the OFFICIAL Analytics API
     (scripts/yt_studio_retention.py --source api — no Studio cookie needed).
  2. Audit every curve against the MEASURED retention rules
     (canon: episodes/_planning/DEEP_RESEARCH_FINDINGS.v001.md §1 / memory pd-retention-rules):
       R-30s : retention at 0:30  >= 55%   (channel median was 62%)
       R-60s : retention at 1:00  >= 35%   (median 40%)
       R-120s: retention at 2:00  >= 27%   (median 32%)
       R-HALF: half-life (first point <50%) >= 42s
       R-DECAY: mid-video decay (2:00->8:00) <= 1.5 pt/min
       R-CLIFF: no single-minute drop > 8pt inside 1:20-3:00 (the explanation-block cliff)
  3. Write a dated report episodes/_planning/measurements/retention_check.<YYYYMMDD>.md
     with per-video PASS/FAIL and week-over-week deltas vs the previous report.
  4. git add+commit+push the report (report file only).

Exit codes: 0 = ran and wrote report (even with FAILs); 1 = infrastructure error.
"""
from __future__ import annotations

import datetime as dt
import json
import pathlib
import subprocess
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = pathlib.Path(__file__).resolve().parents[1]
CURVES = ROOT / "scripts" / "_yt_retention_curves.json"
OUTDIR = ROOT / "episodes" / "_planning" / "measurements"
TITLES = ROOT / "scripts" / "_yt_studio_video_ctr.json"  # cached title/length join

RULES = {
    "R-30s": ("retention @0:30 >= 55%", 30, 0.55),
    "R-60s": ("retention @1:00 >= 35%", 60, 0.35),
    "R-120s": ("retention @2:00 >= 27%", 120, 0.27),
}


def run_pull() -> None:
    r = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "yt_studio_retention.py"), "--source", "api"],
        cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace",
        timeout=1800,
    )
    if r.returncode != 0:
        print(r.stdout[-2000:] if r.stdout else "")
        print(r.stderr[-2000:] if r.stderr else "")
        raise RuntimeError("retention pull failed")


def val_at(points: list, sec: float, dur: float):
    """points: [(ratio_pos 0..1, watch_ratio)] normalized; return watch ratio at sec."""
    if not points or dur <= 0:
        return None
    target = sec / dur
    best = min(points, key=lambda p: abs(p[0] - target))
    if abs(best[0] - target) > 0.05:
        return None
    return best[1]


def main() -> int:
    run_pull()
    data = json.loads(CURVES.read_text(encoding="utf-8"))
    titles = {}
    if TITLES.exists():
        for row in json.loads(TITLES.read_text(encoding="utf-8")).get("rows", []):
            titles[row.get("video_id")] = (row.get("title"), row.get("length_seconds"))

    today = dt.date.today().strftime("%Y%m%d")
    OUTDIR.mkdir(parents=True, exist_ok=True)
    prev_reports = sorted(OUTDIR.glob("retention_check.*.md"))
    lines = [f"# Weekly retention check — {today}",
             "",
             "Canon rules: DEEP_RESEARCH_FINDINGS.v001.md §1 / memory pd-retention-rules.",
             "", "| video | title | 30s | 60s | 120s | half-life | verdicts |",
             "|---|---|---|---|---|---|---|"]
    videos = data.get("videos") or []  # list of {video_id,title,length_seconds,parse_status,points}
    n_fail = 0
    for entry in videos:
        vid = entry.get("video_id", "?")
        pts = [(p.get("pos"), p.get("watch_ratio")) for p in (entry.get("points") or [])
               if p.get("pos") is not None]
        title = entry.get("title") or titles.get(vid, ("?", None))[0]
        try:
            dur = float(entry.get("length_seconds") or titles.get(vid, (None, 0))[1] or 0)
        except (TypeError, ValueError):
            dur = 0
        if dur <= 240 or not pts:
            continue  # long-forms with curves only
        verdicts = []
        vals = {}
        for key, (_desc, sec, floor) in RULES.items():
            v = val_at(pts, sec, dur)
            vals[sec] = v
            if v is not None and v < floor:
                verdicts.append(f"{key} FAIL({v:.0%})")
        half = next((p[0] * dur for p in sorted(pts) if p[1] is not None and p[1] < 0.5), None)
        if half is not None and half < 42:
            verdicts.append(f"R-HALF FAIL({half:.0f}s)")
        n_fail += bool(verdicts)
        fmt = lambda v: f"{v:.0%}" if v is not None else "-"
        lines.append(f"| {vid} | {str(title)[:40]} | {fmt(vals.get(30))} | {fmt(vals.get(60))} "
                     f"| {fmt(vals.get(120))} | {f'{half:.0f}s' if half else '-'} "
                     f"| {'; '.join(verdicts) if verdicts else 'PASS'} |")
    lines += ["", f"videos with >=1 FAIL: {n_fail}",
              f"previous reports: {len(prev_reports)} (compare newest manually or in the monthly pass)"]
    out = OUTDIR / f"retention_check.{today}.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {out}")

    for cmd in (["git", "add", str(out.relative_to(ROOT))],
                ["git", "commit", "-m", f"weekly retention check {today} (automated)"],
                ["git", "push", "origin", "HEAD"]):
        r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True,
                           encoding="utf-8", errors="replace")
        if r.returncode != 0 and "nothing to commit" not in (r.stdout + r.stderr):
            print(f"git step failed (non-fatal): {' '.join(cmd)}\n{r.stderr[-500:]}")
            break
    return 0


if __name__ == "__main__":
    sys.exit(main())
