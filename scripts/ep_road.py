#!/usr/bin/env python3
"""The road from a chosen theme to a scheduled upload, driven from one seat.

WHY THIS EXISTS (owner directive, 2026-08-23)
---------------------------------------------
「テーマが決まってから予約投稿までスムーズに進む仕組みを作ってほしい」— and the diagnosis
that demanded it: PD does not lack tools. Measured this day, the pipeline's parts almost all
existed and almost none were connected — `preflight_render_gate` called from nowhere,
`write_final_delivery` run "by hand", `check_retention_cadence` never invoked, the forecast
printed and ignored. Every session re-derived the next step from 141,335 characters of prose.

This is the connection. One command answers, from artifacts on disk and never from memory:

    which stage is this episode at, what exactly is missing, and what runs next?

It DRIVES the mechanical steps (checks, repairs, paperwork) itself, prints the exact command
for the heavy or human ones, and never silently skips: every stage reports done / next / blocked
with the artifact that proves it. Stages match `docs/`'s canonical order and the EP77 standard
is enforced by the same wiring the queue uses, so this seat cannot out-run the gates.

WHAT IT WILL NOT DO
-------------------
* start a render or an upload by itself — those cost hours or touch the channel, and go through
  `pd_run.sh` / `upload_schedule_case_v001.py`, whose locks and approvals stay authoritative
* generate creative work (script prose, images) — it says what is missing and who makes it
* touch episodes below 077 unless asked by slug: the old fleet finishes on its own road

Usage:
    py -3.11 scripts/ep_road.py --slug <slug>          # where am I, what is next
    py -3.11 scripts/ep_road.py --slug <slug> --run    # also run the mechanical next steps
    py -3.11 scripts/ep_road.py --slug <slug> --json
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))


def sh(cmd: list[str]) -> tuple[int, str]:
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                       errors="replace", cwd=ROOT)
    return p.returncode, (p.stdout + p.stderr)


@dataclass
class Stage:
    name: str
    what: str                                   # one line, owner-readable
    probe: Callable[[dict], tuple[bool, str]]   # (done?, evidence)
    next_cmd: str | None = None                 # exact command when this is the frontier
    mechanical: bool = False                    # safe for --run to execute itself
    human: str | None = None                    # what only a person/Codex can supply


def ctx_for(slug: str) -> dict:
    hits = sorted(ROOT.glob(f"episodes/PD-2026-*-{slug}"))
    ep = hits[-1] if hits else None
    m = re.match(r"PD-2026-(\d+)-", ep.name) if ep else None
    return {"slug": slug, "ep": ep, "num": int(m.group(1)) if m else None,
            "pub": ROOT / "remotion" / "public" / slug,
            "film": ROOT / "remotion" / "src" / "data" / f"{slug}_film.json"}


def _exists(p: Path | None, what: str) -> tuple[bool, str]:
    return (True, f"{what}: {p.name}") if p and p.is_file() else (False, f"{what}: missing")


def _glob1(pattern: str) -> Path | None:
    hits = sorted(ROOT.glob(pattern))
    return hits[-1] if hits else None


# --------------------------------------------------------------------------- #
# probes — every one answers from bytes on disk
# --------------------------------------------------------------------------- #
def p_spec(c):    return _exists(c["ep"] / "episode_spec.v001.json" if c["ep"] else None, "spec")
def p_facts(c):   return _exists(_glob1(f"episodes/_planning/EP{c['num']}_{c['slug']}_FACTS_LEDGER.v*.md"), "facts ledger")


def p_script(c):
    s = _glob1(f"episodes/_planning/EP{c['num']}_{c['slug']}_script.en.v*.md")
    if not s:
        return False, "planning script: missing (start from _EP_SCRIPT_TEMPLATE.v001.md)"
    rc, out = sh(["py", "-3.11", str(ROOT / "scripts/check_ep77_standard.py"),
                  "--slug", c["slug"], "--stage", "inputs"])
    if rc == 0:
        return True, f"{s.name} + EP77 standard PASS"
    detail = "; ".join(l.strip()[2:] for l in out.splitlines() if l.strip().startswith("- "))
    return False, f"{s.name} but EP77 standard: {detail[:160]}"


def p_narration(c):
    ok1, _ = _exists(c["ep"] / "06_audio" / "narration_index.v001.json" if c["ep"] else None, "index")
    ok2, _ = _exists(c["pub"] / "narration.mp3", "mp3")
    return ok1 and ok2, ("narration index + master mp3" if ok1 and ok2 else
                         "narration " + ("mp3 missing" if ok1 else "index missing"))


def p_captions(c):
    s = sorted((c["ep"] / "08_edit").glob("captions.final.v*.srt")) if c["ep"] else []
    return bool(s), (s[-1].name if s else "captions.final.v*.srt: missing")


def p_images(c):
    n = len(list((c["pub"] / "img").glob("*.png"))) if (c["pub"] / "img").is_dir() else 0
    return n > 0, f"{n} hero png(s) staged"     # the spec's own count is enforced by [0/7]


def p_footage(c):
    n = len(list((c["pub"] / "factory").glob("*.mp4"))) if (c["pub"] / "factory").is_dir() else 0
    return n >= 30, f"{n} factory clip(s) staged (floor 1/45s; aim 60+, shelf holds 26k)"


def p_motion(c):
    n = len(list((c["pub"] / "motion").glob("*.mp4"))) if (c["pub"] / "motion").is_dir() else 0
    return n > 0, f"{n} i2v motion clip(s)"


def p_ae(c):
    slug = c["slug"]
    jobs = ROOT / "scripts" / "ae" / f"jobs_{slug}.json"
    if not jobs.is_file():
        return False, (f"scripts/ae/jobs_{slug}.json: missing "
                       f"(spec declares the beats; this file renders them)")
    out = ROOT / "ae-kinetic" / "out"
    n = len(list(out.glob("*.webm"))) if out.is_dir() else 0
    extra = f" ({n} rendered card(s) in ae out)" if n else ""
    return True, jobs.name + " present" + extra


def p_film(c):
    if not c["film"].is_file() or c["film"].stat().st_size < 2000:
        return False, "film json: missing or placeholder"
    rc, _ = sh(["py", "-3.11", str(ROOT / "scripts/check_ep77_standard.py"),
                "--slug", c["slug"], "--stage", "plan"])
    return rc == 0, f"{c['film'].name}" + ("" if rc == 0 else " but plan stage FAILS (紙芝居 caps)")


def p_master(c):
    rc, _ = sh(["py", "-3.11", str(ROOT / "scripts/episode_is_done.py"), c["slug"], "--quiet"])
    if rc == 0:
        return True, "accepted master on disk (receipt sha matches bytes)"
    m = sorted((c["ep"] / "08_edit").glob(f"{c['slug']}_final_bgm.v*.mp4")) if c["ep"] else []
    return False, (f"{m[-1].name} exists but not yet accepted" if m else "no master")


def p_scheduled(c):
    s = sorted((c["ep"] / "09_package").glob("*youtube_schedule_result*.json")) if c["ep"] else []
    return bool(s), (s[-1].name if s else "not scheduled")


def stages(c) -> list[Stage]:
    slug, num = c["slug"], c["num"]
    return [
        Stage("spec", "機械が読む契約 (episode_spec)", p_spec,
              human="write episode_spec.v001.json per docs/PD_EPISODE_SPEC_STANDARD.v001.md"),
        Stage("facts", "事実台帳 (一次資料つき)", p_facts,
              human="research: FACTS_LEDGER from primary sources"),
        Stage("script", "台本 (テンプレ+7分ごとの問い)", p_script,
              next_cmd=f"py -3.11 scripts/check_script_retention_plan.py --slug {slug}",
              human="write from episodes/_planning/_EP_SCRIPT_TEMPLATE.v001.md; the standard "
                    "gate at [0/7] will not open without it"),
        Stage("narration", "ElevenLabs ナレ", p_narration,
              human="run the narration generation for this episode (standing approval exists; "
                    "record cost per feedback_elevenlabs_standing_approval)"),
        Stage("captions", "字幕 (最終srt)", p_captions,
              human="generate + polish captions against the master narration"),
        Stage("images", "画像 (Codex)", p_images,
              human="Codex generates the image order; stills land in remotion/public/<slug>/img"),
        Stage("footage", "DL実写 (棚から60本目標)", p_footage,
              next_cmd=f"py -3.11 scripts/search_archive.py --shot \"...\" --kind video --sheet",
              human="stage from the shelf, then READ the contact sheets (PD_CANON §7 20c: "
                    "no machine can clear a face)"),
        Stage("motion", "i2v モーション", p_motion,
              human="run the i2v batch for staged stills (GPU; one job at a time)"),
        # ADR-0011: from EP77 the hero cards are After Effects' job. The spec now declares the
        # beats (ae_beats, enforced at [0/7] by check_episode_spec); this stage is where the
        # declared beats become rendered cards. Absent from the road, the ADR was prose again.
        Stage("ae_hero", "AEヒーローカード (ADR-0011)", p_ae,
              next_cmd=f"bash scripts/ae/render_beats.sh   # jobs: scripts/ae/jobs_{slug}.json",
              human="author scripts/ae/jobs_<slug>.json from the spec's ae_beats, then render "
                    "(AE traps: PriorSafeMode.txt / gpu_accel per reference_after_effects_automation)"),
        Stage("film", "film.json (組立+plan検査)", p_film,
              next_cmd=f"bash scripts/pd_run.sh --name finish_{slug} -- "
                       f"/usr/bin/bash scripts/_finish_episode.sh {slug} <Composition> {num}",
              mechanical=False),
        Stage("master", "レンダー+4層mux+受入", p_master,
              next_cmd=f"py -3.11 scripts/predict_acceptance.py --slug {slug}   # before spending the GPU"),
        Stage("paperwork", "納品記録ほか (自動修理)", lambda c: (
              bool(sorted((c["ep"] / "09_package").glob("final_delivery.v*.json"))) if c["ep"] else False,
              "final_delivery"),
              next_cmd=f"py -3.11 scripts/pd_autorepair.py --slug {slug}", mechanical=True),
        Stage("schedule", "予約投稿 (12:00 JST 長尺枠)", p_scheduled,
              next_cmd=f"py -3.11 scripts/upload_schedule_case_v001.py --ep {slug} --explain-policy",
              human="scheduling touches the channel: dry-run first, then the real call -- "
                    "the scheduler's own guards (sha match, policy, future publishAt) decide"),
    ]


def start(slug: str, num: int) -> int:
    """Theme decided -> everything that can be scaffolded, scaffolded; everything else, named.

    Deliberately does NOT invent content: the spec stays absent (an undeclared value is an
    error, and a scaffolded spec full of guesses would be worse than none), and the script is
    the TEMPLATE COPY, which the placeholder rule refuses until a human fills it -- so the
    scaffold cannot be mistaken for progress by any gate.
    """
    if num < 77:
        print(f"--start is the EP77 road; EP{num} belongs to the old fleet")
        return 2
    if not re.fullmatch(r"[a-z0-9]+", slug):
        print(f"slug {slug!r} must be lowercase alphanumeric (it becomes filenames and ids)")
        return 2
    ep = ROOT / "episodes" / f"PD-2026-{num:03d}-{slug}"
    if ep.exists():
        print(f"{ep.name} already exists -- showing the road instead")
        return 0
    ep.mkdir(parents=True)
    for sub in ("01_research", "03_script", "04_scenes", "06_audio", "08_edit", "09_package"):
        (ep / sub).mkdir()
    tpl = ROOT / "episodes" / "_planning" / "_EP_SCRIPT_TEMPLATE.v001.md"
    dst = ROOT / "episodes" / "_planning" / f"EP{num}_{slug}_script.en.v001.md"
    if not dst.exists():
        dst.write_text(tpl.read_text(encoding="utf-8").replace("EP{NN}", f"EP{num}"),
                       encoding="utf-8")
    print(f"=== EP road opened: {ep.name} ===")
    print(f"  scaffolded: {ep.name}/ (6 dirs), {dst.name} (template copy -- the placeholder "
          f"rule refuses it until filled, so this cannot be mistaken for a script)")
    print(f"  write next, in order:")
    print(f"    1. {ep.name}/episode_spec.v001.json  (docs/PD_EPISODE_SPEC_STANDARD.v001.md; "
          f"ae_beats is required from EP77)")
    print(f"    2. episodes/_planning/EP{num}_{slug}_FACTS_LEDGER.v001.md  (primary sources)")
    print(f"    3. fill {dst.name}  (one question per act; check with "
          f"check_script_retention_plan.py)")
    print(f"  then: py -3.11 scripts/ep_road.py --slug {slug}")
    return 0


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--run", action="store_true", help="run the mechanical next steps now")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--start", type=int, metavar="NUM",
                    help="theme decided: scaffold episodes/PD-2026-0NUM-<slug>/ and the "
                         "planning files, then show the road")
    a = ap.parse_args()

    if a.start:
        return start(a.slug, a.start)

    c = ctx_for(a.slug)
    if c["ep"] is None:
        print(f"no episode directory for {a.slug!r}.")
        print(f"  theme decided? start the road with ONE command:")
        print(f"    py -3.11 scripts/ep_road.py --slug {a.slug} --start <NUM>")
        return 2

    rows = []
    frontier = None
    for st in stages(c):
        done, evidence = st.probe(c)
        rows.append({"stage": st.name, "done": done, "evidence": evidence})
        if not done and frontier is None:
            frontier = st

    if a.json:
        print(json.dumps({"slug": a.slug, "num": c["num"], "stages": rows,
                          "frontier": frontier.name if frontier else None},
                         ensure_ascii=False, indent=1))
        return 0

    print(f"=== EP road — {a.slug} (EP{c['num']}) ===")
    for r, st in zip(rows, stages(c)):
        mark = "✓" if r["done"] else ("→" if frontier and st.name == frontier.name else "·")
        print(f"  {mark} {st.name:<10} {st.what:<28} {r['evidence']}")
    if frontier is None:
        print("\n  DONE: scheduled. Nothing on this road is left.")
        return 0

    print(f"\n  NEXT: {frontier.name}")
    if frontier.human:
        print(f"    needs a person/Codex: {frontier.human}")
    if frontier.next_cmd:
        print(f"    command: {frontier.next_cmd}")
    if a.run and frontier.mechanical and frontier.next_cmd:
        print(f"\n  --run: executing the mechanical step now")
        import shlex
        rc, out = sh(shlex.split(frontier.next_cmd))   # .split() broke on any quoted argument
        print("\n".join("    " + l for l in out.strip().splitlines()[-6:]))
        return rc
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
