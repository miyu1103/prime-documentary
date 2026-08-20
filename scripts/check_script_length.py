#!/usr/bin/env python
"""FREE, PRE-SPEND gate: will this script actually fill the target runtime?

Closes the longest-running repeat failure on this channel. `check_runtime_band.py`
only fires on a RENDERED file -- after ElevenLabs TTS and a full Remotion render have
already been paid for. By then a short script is expensive to fix, so it kept shipping
as an owner-accepted deviation instead (EP14, EP15, EP34, EP38 at 9.40 min).

Root cause, measured 2026-07-19 over 31 episodes (real ElevenLabs clip durations on
H:\\pd-media vs the repo script text):

    MEDIAN NARRATION PACE = 178.1 wpm   (range 163.7 - 237.4)

The spec was updated to ~173 wpm but the SCRIPTS never were -- episodes 009-015 were
all written at 1,503-1,565 words, which is 150-wpm-era sizing. At 178 wpm that is
8.4-8.8 minutes of narration, not 11.5. The arithmetic never supported the target.

    words needed = target_seconds / 60 * wpm

    690s (11.5 min) @ 178 wpm = 2,048 words
    750s (12.5 min) @ 178 wpm = 2,226 words

Because pace VARIES by episode (voice settings drifted: williams 237, florence 228,
tyler/rolin/hinders 202-211 vs the 167-182 cluster), this gate reports the runtime at
the slow, median and fast ends and requires the word count to clear the band at the
MEDIAN while warning when the fast end would undershoot.

Read-only. No writes, no paid calls. Exit 0 = PASS, 1 = FAIL.

Usage:
    python scripts/check_script_length.py <script.md|script.json>
    python scripts/check_script_length.py <script.md> --lo 690 --hi 750
    python scripts/check_script_length.py <script.md> --json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")  # cp932 guard (Windows)
except Exception:
    pass

CHECK_NAME = "script_length"

# Measured 2026-07-19 across 31 shipped episodes. Do not replace these with an
# estimate -- re-measure with scripts/measure_narration_wpm.py if the voice changes.
WPM_MEDIAN = 178.1
WPM_SLOW = 163.7
WPM_FAST = 237.4

# Measured 2026-07-20 over 21 shipped episodes: finished-render duration divided by
# the sum of the narration clips. Non-speech (breathing gaps, scripted silence,
# BrandOpening 3.5s, BrandEndcard 9s) is 4-39% of runtime; the recent CaseFilm cut
# sits at 1.04-1.05. The gap budget is a production choice, so the script only has to
# carry enough speech that SOME budget in this range lands inside the band.
RATIO_MIN = 1.04   # tightest observed (cotton 1.041)
RATIO_MAX = 1.30   # generous but not the 1.388 outlier

DEFAULT_LO_SECONDS = 690.0   # 11.5 min  (VIDEO_RULES section 10)
DEFAULT_HI_SECONDS = 750.0   # 12.5 min

NARRATION_KEYS = ("text", "narration", "line", "vo")


def narration_text(path: Path) -> str:
    raw = path.read_text(encoding="utf-8", errors="ignore")
    if path.suffix.lower() == ".json":
        try:
            json.loads(raw)  # validate, then harvest narration-bearing fields
        except Exception:
            pass
        keys = "|".join(NARRATION_KEYS)
        return " ".join(re.findall(rf'"(?:{keys})"\s*:\s*"([^"]{{4,}})"', raw))
    return raw


# Everything from these headings on is production apparatus, not narration.
APPENDIX_HEADINGS = ("事実対応表", "改稿ログ", "Fact Correspondence", "Revision Log", "タイトル", "サムネ", "Title", "Thumbnail")


def count_words(text: str) -> int:
    """Spoken words only: drop headings, stage directions, markdown furniture.

    MEASURED 2026-07-20: on EP39 this over-counted by 160 words (2,127 vs the 1,967
    actually sent to TTS) because it stripped ASCII brackets but not the FULL-WIDTH
    ones the scripts use for on-screen text -- 【OST: ...】 and 〔CARD: ...〕 -- and left
    the bodies of the trailing 事実対応表 / 改稿ログ sections in. At 176 wpm that is the
    difference between a projected 725s (PASS) and 671s (below the 690s floor), i.e. the
    gate would have cleared exactly the defect it exists to catch.
    """
    # cut the appendix: its heading was removed below, but its body was being counted
    for h in APPENDIX_HEADINGS:
        idx = text.find(h)
        if idx != -1:
            text = text[:idx]
    # MEASURED 2026-08-20 (PD_ONE_PASS_PRODUCTION_SPEC.v3 6.6) and FIXED 2026-08-21 on EP76:
    # every script since EP66 carries an HTML citation comment under each factual line, and
    # they were being counted as spoken words. Inflation per script: EP69 +2,195, EP68 +1,798,
    # EP66 +1,736, EP67 +1,565, EP71 +1,256, EP70 +975, EP76 +758. On EP76 that turned a
    # 5,114-word script (the words the TTS extractor actually speaks) into 5,872 and made the
    # gate report LONG by 392 words on a script that is 29:46. Strip them first: a comment can
    # contain brackets and parentheses, so it must go before the ASCII-bracket rules below.
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.S)  # HTML citation comments
    text = re.sub(r"^#.*$", " ", text, flags=re.M)      # markdown headings
    text = re.sub(r"【[^】]*】", " ", text)               # 【OST: ...】 on-screen text
    text = re.sub(r"〔[^〕]*〕", " ", text)               # 〔CARD: ...〕 on-screen text
    text = re.sub(r"\[[^\]]*\]", " ", text)             # [B-ROLL: ...] directions
    text = re.sub(r"\([^)]*\)", " ", text)              # (beat) directions
    text = re.sub(r"^\s*[-*]\s*\w+\s*:", " ", text, flags=re.M)  # "- NARRATOR:" tags
    text = re.sub(r"[*_`>|#]", " ", text)
    return len(re.findall(r"[A-Za-z][A-Za-z'’-]*", text))


def spoken_words_from_voice_plan(epdir: Path) -> tuple[int, str] | None:
    """Authoritative count once a voice_plan exists: the text actually sent to the API.

    Prefer this over any estimate from the script -- the script is prose plus apparatus,
    the plan is the words the voice will say.
    """
    plans = sorted(epdir.glob("06_audio/voice_plan.v*.json")) + \
        sorted(epdir.glob("06_voice/voice_plan.v*.json"))
    if not plans:
        return None
    try:
        data = json.loads(plans[-1].read_text(encoding="utf-8"))
    except Exception:
        return None
    chunks = data.get("chunks") or []
    if not chunks:
        return None
    n = sum(len(re.findall(r"[A-Za-z][A-Za-z'’-]*", c.get("spoken_text", "")))
            for c in chunks)
    return (n, plans[-1].name) if n else None


def evaluate_script(path: Path, lo: float = DEFAULT_LO_SECONDS,
                    hi: float = DEFAULT_HI_SECONDS) -> dict:
    words = count_words(narration_text(path))
    # Speech seconds required so that a gap budget inside the measured range lands the
    # FINISHED film in band. Dividing by the ratio is the whole correction: the old code
    # used the band seconds directly, i.e. assumed a 100%-speech film.
    need_lo = round(lo / RATIO_MAX / 60 * WPM_MEDIAN)
    need_hi = round(hi / RATIO_MIN / 60 * WPM_MEDIAN)

    est_median = words / WPM_MEDIAN * 60
    est_slow = words / WPM_SLOW * 60      # slow voice -> LONGER runtime
    est_fast = words / WPM_FAST * 60      # fast voice -> SHORTER runtime

    ok = need_lo <= words <= need_hi
    notes = []
    if words < need_lo:
        notes.append(
            f"SHORT by {need_lo - words} words. At {WPM_MEDIAN} wpm this is "
            f"{est_median/60:.1f} min of speech; even at the loosest measured pacing "
            f"({RATIO_MAX}x) the finished film misses the {lo/60:.1f} min floor. "
            f"Do NOT pad -- add substance (a scene beat, a second case, the human "
            f"aftermath, the dissent's reasoning)."
        )
    elif words > need_hi:
        notes.append(
            f"LONG by {words - need_hi} words -> {est_median/60:.1f} min of speech, which "
            f"finishes past {hi/60:.1f} min even at the tightest measured pacing "
            f"({RATIO_MIN}x). Cut, do not speed the voice."
        )
    if est_fast < lo:
        notes.append(
            f"RISK: at the fast end of the measured pace ({WPM_FAST} wpm, seen on "
            f"williams/florence) this lands at {est_fast/60:.1f} min -- under the floor. "
            f"Either pin the voice speed or write to {round(lo/60*WPM_FAST):,} words."
        )

    return {
        "check": CHECK_NAME,
        "ok": ok,
        "script": str(path),
        "words": words,
        "words_required": [need_lo, need_hi],
        "target_seconds": [lo, hi],
        "wpm_used": {"median": WPM_MEDIAN, "slow": WPM_SLOW, "fast": WPM_FAST},
        "estimated_seconds": {
            "slow": round(est_slow, 1),
            "median": round(est_median, 1),
            "fast": round(est_fast, 1),
        },
        "finished_projection": {
            "tight": round(est_median * RATIO_MIN, 1),
            "loose": round(est_median * RATIO_MAX, 1),
        },
        "notes": notes,
    }


def _episode_band(epdir: Path) -> tuple[float, float]:
    """Resolve this episode's target band.

    MUST mirror check_runtime_band.infer_band_from_render_path -- if the pre-spend gate
    and the post-render gate disagree, one of them is lying. Order: the episode's own
    planned band, then the manifest's target_duration_minutes bucket, then the channel
    default. (Omitting the manifest step was a false-RED: it judged the 24-35 min
    long-form batch EP016-024 against the 11.5-12.5 min standard.)
    """
    plans = sorted((epdir / "04_scenes").glob("remotion_plan.v*.json"))
    if plans:
        try:
            plan = json.loads(plans[-1].read_text(encoding="utf-8"))
            band = (plan.get("motion_budget") or {}).get("runtime_band_seconds")
            if (isinstance(band, (list, tuple)) and len(band) == 2
                    and all(isinstance(x, (int, float)) for x in band) and band[0] < band[1]):
                return float(band[0]), float(band[1])
        except Exception:
            pass
    try:
        mf = json.loads((epdir / "manifest.json").read_text(encoding="utf-8"))
    except Exception:
        mf = {}
    # An explicit band beats bucket inference. The buckets are coarse by necessity --
    # EP51 willingham narrates 20.1 min and fits NO bucket (the >=20 one is 27-33) --
    # so an episode that knows its own shape may state it and be believed.
    band = mf.get("runtime_band_minutes")
    if (isinstance(band, (list, tuple)) and len(band) == 2
            and all(isinstance(x, (int, float)) for x in band) and band[0] < band[1]):
        return float(band[0]) * 60.0, float(band[1]) * 60.0
    target = mf.get("target_duration_minutes")
    if target:
        # Buckets, widest first. The table used to jump straight from >=20 to >=45,
        # so a 40-minute episode was graded against the 27-33 min band -- a false RED
        # that no amount of editing could clear. EP60 surfside (40 min) exposed it.
        if target >= 45:
            return 3300.0, 3900.0
        if target >= 36:
            return 2160.0, 2640.0      # 36-44 min -> 36:00-44:00
        if target >= 20:
            return 1620.0, 1980.0
    return DEFAULT_LO_SECONDS, DEFAULT_HI_SECONDS


def _find_script(epdir: Path) -> Path | None:
    """Newest narration-bearing script for the episode, repo-side."""
    cands: list[Path] = []
    for sub in ("03_script", "04_script", "02_script"):
        d = epdir / sub
        if d.exists():
            cands += [p for p in d.rglob("*")
                      if p.suffix.lower() in (".md", ".json") and "script" in p.name.lower()]
    slug = epdir.name.split("-")[-1]
    planning = epdir.parent / "_planning"
    if planning.exists():
        cands += [p for p in planning.glob(f"*{slug}*script*")
                  if p.suffix.lower() in (".md", ".json")]
    if not cands:
        return None
    # "The richest one wins" assumed later drafts are always longer. They are not: EP60's
    # v004 is 674 words TIGHTER than v002 because a revision pass cut padding, so the gate
    # graded a superseded draft. Prefer the highest revision number, but only among
    # candidates that are still substantial (>= 60% of the richest), so a stub named v009
    # cannot win either.
    scored = [(p, count_words(narration_text(p))) for p in cands]
    richest = max(w for _, w in scored) or 1

    def _rev(path: Path) -> int:
        m = re.findall(r"[vV](\d{1,3})", path.stem)
        return int(m[-1]) if m else -1

    substantial = [(p, w) for p, w in scored if w >= 0.60 * richest]
    if substantial and any(_rev(p) >= 0 for p, _ in substantial):
        return max(substantial, key=lambda pw: (_rev(pw[0]), pw[1]))[0]
    return max(scored, key=lambda pw: pw[1])[0]


def evaluate(epdir: Path) -> dict:
    """PREFLIGHT adapter for preflight_render_gate._run_ext_gate."""
    epdir = Path(epdir)
    script = _find_script(epdir)
    if script is None:
        return {"ok": True, "skipped": True,
                "reason": "no script artifact yet (nothing to size)"}
    lo, hi = _episode_band(epdir)
    r = evaluate_script(script, lo, hi)

    # If the episode has a voice_plan, its spoken_text is what the voice will actually
    # say -- override the script estimate with it and say so in the reason.
    vp = spoken_words_from_voice_plan(epdir)
    if vp:
        n, plan_name = vp
        r = dict(r, words=n, source=f"voice_plan ({plan_name})")
        need_lo, need_hi = r["words_required"]
        r["ok"] = need_lo <= n <= need_hi
        r["estimated_seconds"] = {
            "slow": round(n / WPM_SLOW * 60, 1),
            "median": round(n / WPM_MEDIAN * 60, 1),
            "fast": round(n / WPM_FAST * 60, 1),
        }
    if r["ok"]:
        reason = (f"{r['words']:,} words -> ~{r['estimated_seconds']['median']/60:.1f} min "
                  f"(band {lo/60:.1f}-{hi/60:.1f}) [{script.name}]")
    else:
        reason = (f"{r['words']:,} words vs required "
                  f"{r['words_required'][0]:,}-{r['words_required'][1]:,} -> narrates in "
                  f"~{r['estimated_seconds']['median']/60:.1f} min, outside the "
                  f"{lo/60:.1f}-{hi/60:.1f} min band [{script.name}]. "
                  + (" ".join(r["notes"]) if r["notes"] else ""))
    return {"ok": r["ok"], "hard": True, "skipped": False, "reason": reason, **r}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("script", type=Path)
    ap.add_argument("--lo", type=float, default=DEFAULT_LO_SECONDS)
    ap.add_argument("--hi", type=float, default=DEFAULT_HI_SECONDS)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    if not a.script.exists():
        print(f"FAIL {CHECK_NAME}: no such script {a.script}")
        return 1

    r = evaluate_script(a.script, a.lo, a.hi)
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        verdict = "PASS" if r["ok"] else "FAIL"
        print(f"{verdict} {CHECK_NAME}: {r['words']:,} words "
              f"(need {r['words_required'][0]:,}-{r['words_required'][1]:,})")
        e = r["estimated_seconds"]
        print(f"  narration estimate  slow {e['slow']/60:.1f}m | "
              f"median {e['median']/60:.1f}m | fast {e['fast']/60:.1f}m")
        print(f"  target band         {a.lo/60:.1f}-{a.hi/60:.1f} min")
        for n in r["notes"]:
            print(f"  ! {n}")
    return 0 if r["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
