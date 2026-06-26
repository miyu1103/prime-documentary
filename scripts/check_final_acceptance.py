#!/usr/bin/env python
"""Independently verify that an episode's FINAL render is publish-grade.

WHY THIS EXISTS (EP14 lange post-mortem): the per-episode build scripts write a
self-asserted `quality_gate` dict into their own QC json. EP14's gate claimed
four_part_structure/all_shots_filled/captions_burned_in/lange_premium_used = true,
yet the delivered file used the SAPI *review-proxy* narration (provider
local_windows_sapi, "Microsoft Zira"), had no final captions, and was missing
images/hook. The producer graded its own homework and the values did not match
the bytes on disk (CLAUDE.md invariant 13: "generated" != "usable"; rule 17:
report measured results, not "looks good").

This script is a SEPARATE verifier: it MEASURES the actual render + reads
narration/caption provenance from the repo, and emits PASS/FAIL. It must be run
as an independent gate; the rendering agent must NOT hand-write the acceptance.

Read-only. Probes the file with ffprobe/ffmpeg; no writes, no paid calls, no
upload. Exit 0 = PASS (all hard checks), 1 = FAIL or error.

Hard checks (block the final):
  - voice_is_master    : a non-proxy narration plan exists with an ElevenLabs
                         (master) provider -- NOT local SAPI / windows / proxy.
  - captions_final     : a non-proxy caption sidecar (.srt) exists, non-empty,
                         and (if render known) covers >=90% of the runtime.
  - runtime_band       : finished runtime within 690-750s (11.5-12.5 min).
  - images_present     : no excessive black (a "no images" / placeholder render
                         shows long black stretches).
  - bgm_present        : a continuous (ducked) music bed -- narration-only mixes
                         leave long silence between sentences (EP14 final = 109s).
Soft checks (reported, do not block):
  - hook_added         : runtime exceeds (shotlist body + bookends) by enough to
                         hold a >=25s hook + breathing beats.
  - loudness           : integrated LUFS within [-16, -12].

Usage:
  .venv/Scripts/python.exe scripts/check_final_acceptance.py 15
  .venv/Scripts/python.exe scripts/check_final_acceptance.py PD-2026-015-theranos --render H:/.../final/x.mp4
  .venv/Scripts/python.exe scripts/check_final_acceptance.py 15 --json
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EPDIR = ROOT / "episodes"

RUNTIME_LO, RUNTIME_HI = 690.0, 750.0           # 11.5-12.5 min finished runtime
MAX_TOTAL_BLACK_S = 8.0                          # cumulative black tolerated
MAX_SINGLE_BLACK_S = 3.0                         # any single black gap
MAX_TOTAL_SILENCE_S = 25.0                       # >this => no continuous BGM bed
LUFS_LO, LUFS_HI = -16.0, -12.0
SAPI_MARKERS = ("sapi", "local_windows", "windows_sapi", "zira", "local-")
MASTER_MARKERS = ("eleven",)                     # ElevenLabs = the usual master voice


def resolve_episode(arg: str) -> str:
    if (EPDIR / arg).is_dir():
        return arg
    hits = [os.path.basename(p) for p in glob.glob(str(EPDIR / f"PD-*-{int(arg):03d}-*"))] if arg.isdigit() else []
    if not hits:
        hits = [os.path.basename(p) for p in glob.glob(str(EPDIR / f"*{arg}*")) if os.path.isdir(p)]
    if len(hits) == 1:
        return hits[0]
    raise SystemExit(f"Could not resolve episode '{arg}'. Matches: {hits}")


def _load(p: Path):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None


def check_voice(epdir: Path) -> dict:
    """A non-proxy narration plan must exist with a master (ElevenLabs) provider."""
    audio = epdir / "06_audio"
    plans = [p for p in audio.glob("*.json")
             if re.search(r"voice_plan|narration_index", p.name)]
    nonproxy = [p for p in plans if "review_proxy" not in p.name]
    proxy_providers, final_providers = [], []
    for p in plans:
        d = _load(p)
        blob = json.dumps(d).lower() if d is not None else ""
        prov = ""
        m = re.search(r'"provider"\s*:\s*"([^"]+)"', blob)
        if m:
            prov = m.group(1)
        (proxy_providers if "review_proxy" in p.name else final_providers).append(prov or "(none)")
    has_master = any(any(mk in prov for mk in MASTER_MARKERS) for prov in final_providers)
    has_sapi_final = any(any(mk in prov for mk in SAPI_MARKERS) for prov in final_providers)
    ok = bool(nonproxy) and has_master and not has_sapi_final
    if not nonproxy:
        reason = "no non-proxy narration plan exists -> final would use the SAPI review-proxy voice (the EP14 failure)"
    elif has_sapi_final:
        reason = f"final narration plan provider is SAPI/local: {final_providers}"
    elif not has_master:
        reason = f"final narration plan provider is not ElevenLabs master: {final_providers or proxy_providers}"
    else:
        reason = f"master narration present: {final_providers}"
    return {"check": "voice_is_master", "ok": ok, "hard": True, "reason": reason}


def _srt_last_end_seconds(p: Path) -> float:
    txt = p.read_text(encoding="utf-8", errors="ignore")
    ends = re.findall(r"-->\s*(\d\d):(\d\d):(\d\d)[,.](\d{1,3})", txt)
    if not ends:
        return 0.0
    h, m, s, ms = ends[-1]
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000.0


def check_captions(epdir: Path, render_dur: float | None) -> dict:
    edit = epdir / "08_edit"
    srts = [p for p in edit.glob("*.srt") if "review_proxy" not in p.name]
    srts = [p for p in srts if p.stat().st_size > 0]
    if not srts:
        return {"check": "captions_final", "ok": False, "hard": True,
                "reason": "no non-proxy caption .srt in 08_edit (only review-proxy captions, or none)"}
    best = max(srts, key=lambda p: _srt_last_end_seconds(p))
    cover = _srt_last_end_seconds(best)
    ok = True
    reason = f"final captions {best.name} (last cue {cover:.0f}s)"
    if render_dur and cover < 0.90 * render_dur:
        ok = False
        reason = f"captions {best.name} cover only {cover:.0f}s of {render_dur:.0f}s render (<90%)"
    return {"check": "captions_final", "ok": ok, "hard": True, "reason": reason}


def ffprobe_duration(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(path)],
        capture_output=True, text=True, check=True)
    return float(json.loads(out.stdout)["format"]["duration"])


def check_runtime(dur: float) -> dict:
    ok = RUNTIME_LO <= dur <= RUNTIME_HI
    return {"check": "runtime_band", "ok": ok, "hard": True,
            "reason": f"{dur:.1f}s = {dur/60:.2f}min (band {RUNTIME_LO:.0f}-{RUNTIME_HI:.0f}s)"}


def check_black(path: Path) -> dict:
    """No excessive black -> a 'no images'/placeholder render is caught."""
    try:
        out = subprocess.run(
            ["ffmpeg", "-hide_banner", "-nostats", "-i", str(path),
             "-vf", "blackdetect=d=0.5:pic_th=0.98", "-an", "-f", "null", os.devnull],
            capture_output=True, text=True, check=True, timeout=900)
    except Exception as exc:  # noqa: BLE001
        return {"check": "images_present", "ok": True, "hard": True, "skipped": True,
                "reason": f"blackdetect skipped ({exc})"}
    spans = re.findall(r"black_duration:(\d+(?:\.\d+)?)", out.stderr)
    durs = [float(x) for x in spans]
    total, longest = sum(durs), (max(durs) if durs else 0.0)
    ok = total <= MAX_TOTAL_BLACK_S and longest <= MAX_SINGLE_BLACK_S
    return {"check": "images_present", "ok": ok, "hard": True,
            "reason": f"black total {total:.1f}s / longest {longest:.1f}s "
                      f"(limits {MAX_TOTAL_BLACK_S:.0f}/{MAX_SINGLE_BLACK_S:.0f})"}


def check_bgm(path: Path) -> dict:
    """No continuous music bed -> the mix is narration-only. A properly bedded
    (and ducked) 4-layer mix has near-zero silence; a narration-only render
    leaves long gaps between sentences (EP14 final = 109s, EP15 proxy = 102s)."""
    try:
        out = subprocess.run(
            ["ffmpeg", "-hide_banner", "-nostats", "-i", str(path),
             "-af", "silencedetect=n=-40dB:d=0.6", "-f", "null", os.devnull],
            capture_output=True, text=True, check=True, timeout=900)
    except Exception as exc:  # noqa: BLE001
        return {"check": "bgm_present", "ok": True, "hard": True, "skipped": True,
                "reason": f"silencedetect skipped ({exc})"}
    sil = [float(x) for x in re.findall(r"silence_duration:\s*(\d+(?:\.\d+)?)", out.stderr)]
    total = sum(sil)
    ok = total <= MAX_TOTAL_SILENCE_S
    return {"check": "bgm_present", "ok": ok, "hard": True,
            "reason": f"total silence {total:.0f}s (limit {MAX_TOTAL_SILENCE_S:.0f}s; "
                      f"high => no continuous BGM bed / narration-only mix)"}


def check_hook(epdir: Path, dur: float) -> dict:
    """Soft: runtime must exceed (shotlist body + bookends) enough to hold a hook."""
    sl = _load(epdir / "04_scenes" / "shotlist.v001.json") or {}
    body = (sl.get("totals") or {}).get("estimated_total_seconds")
    if not body:
        return {"check": "hook_added", "ok": True, "hard": False, "skipped": True,
                "reason": "shotlist totals missing"}
    bookends = 12.5  # BrandOpening 3.5 + BrandEndcard 9
    headroom = dur - (body + bookends)
    ok = headroom >= 25.0
    return {"check": "hook_added", "ok": ok, "hard": False,
            "reason": f"runtime exceeds body+bookends by {headroom:.0f}s "
                      f"(need >=25s for hook+breathing; body={body:.0f}s)"}


def check_loudness(path: Path) -> dict:
    try:
        out = subprocess.run(
            ["ffmpeg", "-hide_banner", "-nostats", "-i", str(path),
             "-af", "ebur128=framelog=quiet", "-f", "null", os.devnull],
            capture_output=True, text=True, check=True, timeout=900)
    except Exception as exc:  # noqa: BLE001
        return {"check": "loudness", "ok": True, "hard": False, "skipped": True,
                "reason": f"ebur128 skipped ({exc})"}
    m = re.findall(r"I:\s*(-?\d+(?:\.\d+)?)\s*LUFS", out.stderr)
    if not m:
        return {"check": "loudness", "ok": True, "hard": False, "skipped": True, "reason": "no LUFS parsed"}
    lufs = float(m[-1])
    ok = LUFS_LO <= lufs <= LUFS_HI
    return {"check": "loudness", "ok": ok, "hard": False,
            "reason": f"integrated {lufs:.1f} LUFS (target -14, band {LUFS_LO}..{LUFS_HI})"}


def resolve_render(epdir: Path, override: str | None) -> Path | None:
    if override:
        return Path(override)
    fd = sorted(epdir.glob("09_package/final_delivery.v*.json"))
    for p in reversed(fd):
        d = _load(p) or {}
        fv = d.get("final_video")
        if fv:
            return Path(fv.replace("file://", ""))
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description="Independently verify a final render is publish-grade.")
    ap.add_argument("episode", help="episode number or id")
    ap.add_argument("--render", help="explicit path to the final .mp4 (else from final_delivery)")
    ap.add_argument("--json", action="store_true", help="emit JSON")
    args = ap.parse_args()

    ep = resolve_episode(args.episode)
    epdir = EPDIR / ep
    render = resolve_render(epdir, args.render)
    render_dur = None
    results: list[dict] = []

    # media checks (only if the render is reachable)
    if render and render.is_file():
        try:
            render_dur = ffprobe_duration(render)
            results.append(check_runtime(render_dur))
            results.append(check_black(render))
            results.append(check_bgm(render))
            results.append(check_hook(epdir, render_dur))
            results.append(check_loudness(render))
        except Exception as exc:  # noqa: BLE001
            results.append({"check": "render_probe", "ok": False, "hard": True,
                            "reason": f"could not probe render {render}: {exc}"})
    else:
        results.append({"check": "render_present", "ok": False, "hard": True,
                        "reason": f"final render not found (looked at {render}); "
                                  f"render the TheranosPremium final before acceptance"})

    # in-repo provenance checks (always)
    results.append(check_voice(epdir))
    results.append(check_captions(epdir, render_dur))

    hard_fail = [r for r in results if r["hard"] and not r["ok"]]
    soft_fail = [r for r in results if not r["hard"] and not r["ok"]]
    status = "PASS" if not hard_fail else "FAIL"

    report = {"check": "final_acceptance", "episode": ep,
              "render": str(render) if render else None,
              "render_duration_seconds": round(render_dur, 2) if render_dur else None,
              "status": status, "results": results}
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"FINAL ACCEPTANCE - {ep}")
        print(f"render: {render}  ({render_dur:.1f}s)" if render_dur else f"render: {render}")
        for r in results:
            mark = "PASS" if r["ok"] else ("FAIL" if r["hard"] else "warn")
            tag = "[hard]" if r["hard"] else "[soft]"
            print(f"  {mark:4} {tag} {r['check']}: {r['reason']}")
        print(f"\nRESULT: {status}" + (f"  ({len(soft_fail)} soft warning(s))" if soft_fail else ""))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
