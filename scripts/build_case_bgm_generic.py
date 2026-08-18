#!/usr/bin/env python3
"""Generic PD BGM/ambience bed + master-VO remux (one implementation for every episode).

Generalised from build_centralpark_bgm_real.py, which hard-coded EP50's nine sections and
its music choices. Here the section list comes from the episode's real narration_index and
the score is assigned by each section's ROLE, so a 6-section 20-minute film and an
8-section 30-minute film both get a coherent chapter score with no per-episode edits.

Score shape (pd-structure-template: the primary reveal lands 65-85% of runtime):
  HOOK    near-silent restraint -- a low bed, never digital silence
  OP      measured arpeggio, slightly forward
  ACT_*   alternating tension_build / somber so no two neighbours share a cue
  reveal  the SINGLE raise, on whichever act contains the 70% mark (the reveal hinge)
  final   act opens warm (the reversal) -- unless the raise already owns it
  ENDING  outro

Audio contract, unchanged from EP50: VO is the authoritative master (the baked narration in
the render is replaced), beds loop to fill their window and are ducked under the VO by
sidechain compression, two-pass loudnorm to -14 LUFS / TP <= -1.0 dBTP, AAC 320k.
The input render is never overwritten.

Usage:
  py -3.11 scripts/build_case_bgm_generic.py --slug flowers --render out/flowers.mp4 \
      --out episodes/PD-2026-054-flowers/08_edit/flowers_final_bgm.v001.mp4 [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEDIA = Path("H:/pd-media")
LIB = MEDIA / "library"
MUS, AMB = LIB / "music", LIB / "ambience"
FFMPEG = r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe"
FFPROBE = r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffprobe.exe"
OPENING_SEC = 3.5

EPISODES = {p.name.split("-", 3)[-1]: p.name for p in sorted((ROOT / "episodes").glob("PD-*"))}

HOOK_BED = MUS / "hook/mus_20260614_hook_glass_air_bed_v1.mp3"
OPEN_BED = MUS / "opening/mus_20260614_opening_measured_arpeggio_v1.mp3"
TENSION = [MUS / "tension_build/mus_20260614_tension_build_courtroom_horizon_v1.mp3",
           MUS / "tension_build/mus_20260614_tension_build_courtroom_horizon_v2.mp3"]
SOMBER = [MUS / "somber/mus_20260614_somber_ledger_of_ash_v1.mp3",
          MUS / "somber/mus_20260614_somber_ledger_of_ash_v2.mp3"]
REVEAL = MUS / "reveal/mus_20260614_reveal_verdict_at_dawn_v1.mp3"
REVEAL_WARM = MUS / "reveal/mus_20260614_reveal_verdict_at_dawn_v2.mp3"
OUTRO = MUS / "outro/mus_20260614_outro_last_frame_v1.mp3"
OUTRO_TAIL = MUS / "outro/mus_20260614_outro_last_frame_v2.mp3"

AMB_CYCLE = [AMB / "amb_night_window.mp3", AMB / "amb_institutional_drone.mp3",
             AMB / "amb_courtroom_room_tone.mp3", AMB / "amb_office_hum.mp3",
             AMB / "amb_tension_drone.mp3"]
AMB_WARM = AMB / "amb_light_wind.mp3"


def probe(f: Path) -> float:
    r = subprocess.run([FFPROBE, "-v", "quiet", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(f)], capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return -1.0


def score_for(sections: list[str], starts: dict[str, float], vo_total: float,
              hook_vol: float = 0.30
              ) -> tuple[dict[str, tuple[Path, float]], dict[str, Path]]:
    """Assign a cue + volume per section by role, with exactly one raise at the reveal.
    hook_vol carries the cold-open level so the opening is audible (see --hook-vol).

    The raise goes to the act CONTAINING the 70% mark of the narration, not to a fixed
    act index: pd-structure-template puts the primary reveal at 65-85% of runtime, and on a
    3-act film `acts[-2]` would land it under halfway (EP51 willingham, measured 24-47%).
    When that act is also the last one, it keeps the raise and no separate warm act is set --
    the ENDING carries the warmth instead.
    """
    acts = [s for s in sections if s.startswith("ACT")]
    reveal_act = None
    if acts:
        mark = 0.70 * vo_total
        for i, s in enumerate(acts):
            hi = starts[acts[i + 1]] if i + 1 < len(acts) else vo_total
            if starts[s] <= mark < hi:
                reveal_act = s
                break
        reveal_act = reveal_act or acts[-1]
    final_act = acts[-1] if acts else None
    if final_act == reveal_act:
        final_act = None                 # the raise owns the last act; ENDING closes warm
    music: dict[str, tuple[Path, float]] = {}
    ambience: dict[str, Path] = {}
    ai = 0
    for sec in sections:
        if sec == "HOOK":
            music[sec] = (HOOK_BED, hook_vol)
            ambience[sec] = AMB / "amb_night_window.mp3"
        elif sec == "OP":
            music[sec] = (OPEN_BED, 0.20)
            ambience[sec] = AMB / "amb_institutional_drone.mp3"
        elif sec.startswith("ENDING") or sec.startswith("OUTRO"):
            music[sec] = (OUTRO, 0.20)
            ambience[sec] = AMB_WARM
        elif sec == reveal_act:
            music[sec] = (REVEAL, 0.24)          # the single raise
            ambience[sec] = AMB / "amb_tension_drone.mp3"
        elif sec == final_act:
            music[sec] = (REVEAL_WARM, 0.22)     # opens warm on the reversal
            ambience[sec] = AMB_WARM
        else:
            idx = acts.index(sec) if sec in acts else 0
            pool = TENSION if idx % 2 == 0 else SOMBER
            music[sec] = (pool[(idx // 2) % len(pool)], 0.18 if pool is TENSION else 0.16)
            ambience[sec] = AMB_CYCLE[ai % len(AMB_CYCLE)]
            ai += 1
    return music, ambience


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--render", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--hook-sec", type=float, default=8.0)
    # Owner, on EP50 and again on EP51: 「最初BGMないね」. The CODEX score called the hook
    # "near-silent restraint" and scored it at 0.14 with a 1.5s fade -- under a cold open that
    # carries no narration either, that measures -33 dB and simply reads as a dead opening.
    # Measured reference: the accepted EP48/EP49 openings sit at -14..-20 dB.
    ap.add_argument("--hook-vol", type=float, default=0.30,
                    help="music level over the cold open and the HOOK section")
    ap.add_argument("--hook-fade-in", type=float, default=0.8)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    ep = EPISODES.get(a.slug)
    if not ep:
        raise SystemExit(f"unknown slug {a.slug}")
    idx_p = ROOT / "episodes" / ep / "06_audio" / "narration_index.v001.json"
    vo = MEDIA / "episodes" / ep / "06_voice" / "master" / "vc_master_v001.mp3"
    # SPEC v2 row 9 (binds from EP66): where the authoritative narration master sits on the
    # video timeline. The composition reads `leadSeconds` from <slug>_film.json (see
    # caseFilmLeadFrames in remotion/src/compositions/CaseFilm.tsx) and this remux MUST agree
    # with it, or the master VO lands somewhere other than the burned captions. Absent -- which
    # is every episode up to and including EP65 -- `off` stays `--hook-sec + OPENING_SEC`, the
    # 11.5 s this script has always used, so their remuxes are unchanged. Tested with `is not
    # None`, never truthiness: EP66 declares 0.0 and a falsy test would discard it.
    off = a.hook_sec + OPENING_SEC
    _film_data = ROOT / "remotion" / "src" / "data" / f"{a.slug}_film.json"
    if _film_data.exists():
        _lead = json.loads(_film_data.read_text(encoding="utf-8")).get("leadSeconds")
        if _lead is not None:
            off = float(_lead)

    if not a.render.exists():
        print(f"MISSING render {a.render}", file=sys.stderr)
        return 2
    if not vo.exists():
        print(f"MISSING VO master {vo}", file=sys.stderr)
        return 2
    if a.out.resolve() == a.render.resolve() or (a.out.exists() and not a.dry_run):
        print("REFUSING to overwrite input/existing output", file=sys.stderr)
        return 2

    total = probe(a.render)
    d = json.loads(idx_p.read_text(encoding="utf-8"))
    starts: dict[str, float] = {}
    order: list[str] = []
    for c in d["chunks"]:
        if c["section"] not in starts:
            starts[c["section"]] = float(c["start"])
            order.append(c["section"])
    vo_end = float(d["chunks"][-1]["end"]) + off
    music, ambience = score_for(order, starts, float(d["chunks"][-1]["end"]), a.hook_vol)

    def win(sec: str) -> tuple[float, float]:
        i = order.index(sec)
        lo = starts[sec] + off
        hi = (starts[order[i + 1]] + off) if i + 1 < len(order) else vo_end
        return lo, hi

    bgm = [(music[s][0], *win(s), music[s][1]) for s in order]
    bgm.insert(0, (HOOK_BED, 0.0, starts[order[0]] + off, a.hook_vol))
    bgm.append((OUTRO_TAIL, vo_end, total, 0.22))
    amb = [(ambience[s], *win(s)) for s in order]
    amb.insert(0, (AMB / "amb_night_window.mp3", 0.0, starts[order[0]] + off))
    amb.append((AMB_WARM, vo_end, total))

    for grp in (bgm, amb):
        for row in grp:
            if not Path(row[0]).exists():
                print(f"MISSING {row[0]}", file=sys.stderr)
                return 2

    print(f"[{a.slug}] render={total:.1f}s VO={probe(vo):.1f}s OFF={off} sections={order}")
    for s in order:
        lo, hi = win(s)
        print(f"    {s:<8} {lo:7.1f}-{hi:7.1f}s  {Path(music[s][0]).stem[:44]:<46} vol={music[s][1]}")
    if a.dry_run:
        print("(dry-run) nothing written")
        return 0

    inputs = ["-i", str(vo)]
    parts = [f"[0:a]aformat=sample_rates=48000:channel_layouts=stereo,"
             f"adelay={int(off*1000)}|{int(off*1000)},apad,atrim=0:{total:.3f},asplit=2[vo][vokey]"]
    i = 1
    mlab = []
    for k, (p, s, e, v) in enumerate(bgm):
        dur = max(0.1, e - s)
        inputs += ["-i", str(p)]
        parts.append(f"[{i}:a]aformat=sample_rates=48000:channel_layouts=stereo,"
                     f"aloop=loop=-1:size=2000000000,atrim=0:{dur:.3f},"
                     f"afade=t=in:st=0:d={(a.hook_fade_in if k == 0 else 1.5):.2f},"
                     f"afade=t=out:st={max(0, dur-2):.3f}:d=2.0,"
                     f"volume={v:.3f},adelay={int(s*1000)}|{int(s*1000)}[m{k}]")
        mlab.append(f"[m{k}]")
        i += 1
    parts.append("".join(mlab) + f"amix=inputs={len(mlab)}:normalize=0:dropout_transition=0[music_raw]")
    parts.append("[music_raw][vokey]sidechaincompress=threshold=0.03:ratio=6:attack=120:"
                 "release=450:makeup=1[music]")
    alab = []
    for k, (p, s, e) in enumerate(amb):
        dur = max(0.1, e - s)
        inputs += ["-i", str(p)]
        parts.append(f"[{i}:a]aformat=sample_rates=48000:channel_layouts=stereo,"
                     f"aloop=loop=-1:size=2000000000,atrim=0:{dur:.3f},"
                     f"afade=t=in:st=0:d=1.0,afade=t=out:st={max(0, dur-1.5):.3f}:d=1.5,"
                     f"volume=0.0,adelay={int(s*1000)}|{int(s*1000)}[a{k}]")
        alab.append(f"[a{k}]")
        i += 1
    parts.append("".join(alab) + f"amix=inputs={len(alab)}:normalize=0:dropout_transition=0[amb]")
    parts.append(f"[vo][music][amb]amix=inputs=3:normalize=0:weights=1.0 0.9 0.8:"
                 f"dropout_transition=0,atrim=0:{total:.3f}[pre]")

    work = a.out.parent / f"_{a.slug}_bgm_pre.wav"
    a.out.parent.mkdir(parents=True, exist_ok=True)
    print("[mix] building bed ...", flush=True)
    r = subprocess.run([FFMPEG, "-y", "-hide_banner", *inputs, "-filter_complex", ";".join(parts),
                        "-map", "[pre]", "-ar", "48000", "-ac", "2", str(work)],
                       capture_output=True, text=True)
    if r.returncode:
        print(r.stderr[-3000:], file=sys.stderr)
        return 3
    print("[loudnorm] pass1 ...", flush=True)
    m = subprocess.run([FFMPEG, "-hide_banner", "-i", str(work), "-af",
                        "loudnorm=I=-14:TP=-1.0:LRA=11:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    js = json.loads(m[m.rfind("{"):m.rfind("}") + 1])
    ln = (f"loudnorm=I=-14:TP=-1.0:LRA=11:measured_I={js['input_i']}:measured_TP={js['input_tp']}"
          f":measured_LRA={js['input_lra']}:measured_thresh={js['input_thresh']}"
          f":offset={js['target_offset']}:linear=true")
    print("[mux] pass2 + mux ...", flush=True)
    r2 = subprocess.run([FFMPEG, "-y", "-hide_banner", "-i", str(a.render), "-i", str(work),
                         "-af", ln, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                         "-c:a", "aac", "-b:a", "320k", "-ar", "48000", "-shortest", str(a.out)],
                        capture_output=True, text=True)
    work.unlink(missing_ok=True)
    if r2.returncode:
        print(r2.stderr[-3000:], file=sys.stderr)
        return 4
    print(f"WROTE {a.out} ({probe(a.out):.1f}s, master VO + BGM @ -14 LUFS, OFF={off})")
    print(f"NEXT: py -3.11 scripts/pd_postrender_gate.py {a.out} --expect-sec {total:.0f} "
          f"--frames 40 --out out_qc/qc_frames_{a.slug}")
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    raise SystemExit(main())
