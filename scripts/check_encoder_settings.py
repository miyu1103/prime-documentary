#!/usr/bin/env python
"""ENCODER-SETTINGS gate: the delivered master must be encoded to the spec (SPEC row 6).

WHY THIS GATE EXISTS
--------------------
`docs/PD_ONE_PASS_PRODUCTION_SPEC.v2.md` row 6 ("Not 'Max quality'") specifies the
encode exactly:

    libx264 -preset slow -crf 16 (<=17), -pix_fmt yuv420p, bt709,
    1920x1080 or better, NEVER NVENC, audio aac 320k

and names the gate as "crf/preset/pix_fmt asserted from render log". That assertion was
never implemented. Verified 2026-07-19 by reading `scripts/check_final_acceptance.py`:
the ONLY encode-related check is `check_render_resolution`, which ffprobes
`width,height,codec_name` and asserts **resolution only** -- `codec_name` is placed in
the human-readable reason string and never compared to anything. So today an
`h264_nvenc` encode, a `yuvj420p` full-range encode, a bt470bg-tagged encode, or a 128k
audio track would all pass acceptance untouched.

This is not hypothetical. Scanning all 91 mp4s under `remotion/out/` on 2026-07-19,
28 deviate from row 6 -- and the repo's OWN tooling produces them:

    ReelColdCase.mp4 / ReelCollapse.mp4 / ReelVerdict.mp4
        pix_fmt=yuvj420p, color_space=bt470bg     <- wrong range AND wrong primaries
    short33_yt_coverfirst.mp4 (and 34/35)
        color_space=unset, audio bit_rate=184k    <- under the 320k spec

Every LONG-FORM final (`PD-2026-*_film.muxed.*.mp4`) is currently compliant
(h264 / High / yuv420p / bt709 / aac ~310k), so this gate is GREEN on the real
deliverables today and acts as a regression lock on a setting the pipeline has already
been shown to get wrong elsewhere.

SCOPE -- deliberately narrow, to avoid a false-RED
--------------------------------------------------
The gate resolves THE EPISODE'S LONG-FORM FINAL RENDER and nothing else. Shorts
(1080x1920), probe slices, silent intermediates and Reels legitimately deviate from the
long-form spec and must NOT be judged by it. Resolution order:
    1. `09_package/final_delivery.v*.json` (newest) -- any of the pointer keys the
       schema has drifted through (video / final_video / render / render_actual_path).
    2. newest `remotion/out/PD-<episode-id>_film.muxed.v*.mp4`.
    3. newest `remotion/out/*<slug>*muxed*.mp4`.
If none resolves, or the file is absent, the gate SKIPs -- never fails on absence.

Audio bitrate is checked with a tolerance floor rather than an exact 320k equality: AAC
VBR/CBR muxes report ~305-316k for a 320k target, so the floor is AUDIO_MIN_BPS (256k),
which still catches the 184k Shorts-grade encode without false-flagging a real 320k mux.

CRF and preset are NOT recoverable from an mp4 (they are encoder-side parameters, not
container metadata). Rather than fake it, the gate asserts the OBSERVABLE consequences
that row 6 actually cares about -- codec family, pixel format, color tagging, resolution
and audio rate -- and reports the video bitrate for eyeballing. A CRF assertion belongs
in the render-log check, and is listed as deferred in GATE_AUDIT_v001.md.

Read-only: ffprobe only. No writes, no network, no paid calls. Exit 0 = PASS, 1 = FAIL.

Usage:
    python scripts/check_encoder_settings.py episodes/PD-2026-038-kidsforcash
    python scripts/check_encoder_settings.py --render remotion/out/x.mp4 --json
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")  # cp932 guard (Windows)
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

CHECK_NAME = "encoder_settings"

ALLOWED_VCODEC = {"h264"}            # libx264; h264_nvenc also reports "h264" in
                                     # codec_name, so the NVENC ban is enforced via the
                                     # encoder tag below when present.
BANNED_ENCODER_RE = re.compile(r"(?i)nvenc|qsv|amf|videotoolbox")
ALLOWED_PIX_FMT = {"yuv420p"}
ALLOWED_COLOR_SPACE = {"bt709"}
MIN_WIDTH, MIN_HEIGHT = 1920, 1080
ALLOWED_ACODEC = {"aac"}
AUDIO_MIN_BPS = 256_000              # 320k target; tolerance for VBR reporting

DELIVERY_KEYS = ("video", "final_video", "render", "render_actual_path",
                 "final_video_path", "master")


def _ffprobe(path: Path) -> dict:
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)],
        capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"ffprobe failed: {r.stderr.strip()[:200]}")
    return json.loads(r.stdout)


def _resolve_render(epdir: Path) -> Path | None:
    epdir = Path(epdir)
    root = epdir.parent.parent

    # 1. final_delivery pointer (newest revision)
    for fd in sorted((epdir / "09_package").glob("final_delivery.v*.json"), reverse=True):
        try:
            d = json.loads(fd.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        for k in DELIVERY_KEYS:
            v = d.get(k)
            if isinstance(v, dict):
                v = v.get("path") or v.get("file") or v.get("video")
            if not isinstance(v, str) or not v.strip():
                continue
            if v.strip().upper().startswith("TODO"):
                continue
            p = Path(v)
            if not p.is_absolute():
                p = root / v
            if p.is_file() and p.suffix.lower() == ".mp4":
                return p

    # 2. canonical long-form muxed output for this episode id
    cands = sorted((root / "remotion" / "out").glob(f"{epdir.name}_film.muxed.v*.mp4"))
    if cands:
        return cands[-1]

    # 3. slug-based fallback, long-form muxed only
    slug = epdir.name.split("-")[-1]
    cands = sorted((root / "remotion" / "out").glob(f"*{slug}*muxed*.mp4"))
    return cands[-1] if cands else None


def evaluate_render(path: Path) -> dict:
    info = _ffprobe(path)
    streams = info.get("streams") or []
    v = next((s for s in streams if s.get("codec_type") == "video"), None)
    a = next((s for s in streams if s.get("codec_type") == "audio"), None)

    problems: list[str] = []
    got: dict = {"render": str(path)}

    if v is None:
        problems.append("no video stream")
    else:
        w, h = int(v.get("width") or 0), int(v.get("height") or 0)
        enc = str((v.get("tags") or {}).get("encoder") or "")
        got.update({
            "vcodec": v.get("codec_name"), "profile": v.get("profile"),
            "pix_fmt": v.get("pix_fmt"), "color_space": v.get("color_space"),
            "color_primaries": v.get("color_primaries"),
            "color_transfer": v.get("color_transfer"),
            "width": w, "height": h,
            "video_bit_rate": int(v.get("bit_rate") or 0) or None,
            "encoder_tag": enc or None,
        })
        if v.get("codec_name") not in ALLOWED_VCODEC:
            problems.append(f"video codec {v.get('codec_name')} not in {sorted(ALLOWED_VCODEC)}")
        if enc and BANNED_ENCODER_RE.search(enc):
            problems.append(f"hardware encoder banned by spec row 6: encoder tag {enc!r}")
        if v.get("pix_fmt") not in ALLOWED_PIX_FMT:
            problems.append(f"pix_fmt {v.get('pix_fmt')} != yuv420p")
        if v.get("color_space") not in ALLOWED_COLOR_SPACE:
            problems.append(f"color_space {v.get('color_space')} != bt709")
        if w < MIN_WIDTH or h < MIN_HEIGHT:
            problems.append(f"resolution {w}x{h} < {MIN_WIDTH}x{MIN_HEIGHT}")

    if a is None:
        problems.append("no audio stream")
    else:
        br = int(a.get("bit_rate") or 0)
        got.update({"acodec": a.get("codec_name"), "audio_bit_rate": br or None,
                    "sample_rate": a.get("sample_rate")})
        if a.get("codec_name") not in ALLOWED_ACODEC:
            problems.append(f"audio codec {a.get('codec_name')} != aac")
        if br and br < AUDIO_MIN_BPS:
            problems.append(f"audio bitrate {br // 1000}k < {AUDIO_MIN_BPS // 1000}k floor "
                            f"(spec row 6: aac 320k)")

    return {"check": CHECK_NAME, "ok": not problems, "problems": problems, **got}


def evaluate(epdir: Path) -> dict:
    """PREFLIGHT adapter for preflight_render_gate._run_ext_gate."""
    epdir = Path(epdir)
    render = _resolve_render(epdir)
    if render is None:
        return {"ok": True, "hard": True, "skipped": True,
                "reason": "no long-form final render resolved yet"}
    try:
        r = evaluate_render(render)
    except (RuntimeError, json.JSONDecodeError, OSError, FileNotFoundError) as exc:
        # Fail CLOSED (EP32 B1: gates must never return green on a decode exception).
        return {"ok": False, "hard": True, "skipped": False,
                "reason": f"could not probe {render.name}: {exc}"}

    if r["ok"]:
        reason = (f"{r.get('vcodec')}/{r.get('profile')} {r.get('width')}x{r.get('height')} "
                  f"{r.get('pix_fmt')} {r.get('color_space')} + "
                  f"{r.get('acodec')} {(r.get('audio_bit_rate') or 0)//1000}k")
    else:
        reason = f"{render.name}: " + "; ".join(r["problems"])
    return {"ok": r["ok"], "hard": True, "skipped": False, "reason": reason, **r}


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("epdir", type=Path, nargs="?", help="episode dir")
    ap.add_argument("--render", type=Path, help="probe a specific mp4 instead")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    if a.render:
        if not a.render.is_file():
            print(f"FAIL {CHECK_NAME}: no such render {a.render}")
            return 1
        try:
            r = evaluate_render(a.render)
        except Exception as exc:
            print(f"FAIL {CHECK_NAME}: {exc}")
            return 1
    elif a.epdir:
        if not a.epdir.is_dir():
            print(f"FAIL {CHECK_NAME}: no such episode dir {a.epdir}")
            return 1
        r = evaluate(a.epdir)
    else:
        ap.error("give an episode dir or --render")

    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return 0 if r["ok"] else 1

    if r.get("skipped"):
        print(f"SKIP {CHECK_NAME}: {r['reason']}")
        return 0
    print(f"{'PASS' if r['ok'] else 'FAIL'} {CHECK_NAME}: {Path(r.get('render','?')).name}")
    print(f"  video : {r.get('vcodec')} {r.get('profile')} {r.get('width')}x{r.get('height')} "
          f"{r.get('pix_fmt')} cs={r.get('color_space')} "
          f"{(r.get('video_bit_rate') or 0)//1000}k")
    print(f"  audio : {r.get('acodec')} {(r.get('audio_bit_rate') or 0)//1000}k "
          f"@{r.get('sample_rate')}Hz (floor {AUDIO_MIN_BPS//1000}k)")
    for p in r.get("problems", []):
        print(f"  ! {p}")
    return 0 if r["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
