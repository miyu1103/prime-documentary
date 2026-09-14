#!/usr/bin/env python
"""PD EPISODE PREFLIGHT -- one command that answers "can this episode be built, and what is missing".

This is the single entry point that consolidates every scattered lesson in
episodes/_planning/PD_FAILURE_REGISTRY.v001.md into ONE mechanical check, run BEFORE any
expensive step (i2v, render, AE). It measures the filesystem, never a manifest's claims.

  py -3.11 scripts/pd_preflight.py --slug flowers
  py -3.11 scripts/pd_preflight.py --all [--json out.json] [--fast]

Exit 0 = every checked episode is BUILD-READY. Exit 1 = at least one blocker.
`--fast` skips frame decoding (size checks only) -- quicker, but it CANNOT catch the
black-video failure that hit EP52 morton, so never use it as the final word before a render.

Checks, in the order a build actually depends on them:
  A. NARRATION  index present, not a stub, real chunk timings, master audio on disk,
                narration.mp3 staged where the render will look for it.
  B. ASSETS     v003 manifest present, content-checked, and every referenced public_path
                exists / is not a stub / is not near-black.
  C. POOLS      enough real video to sustain motion-first (>=0.62 video share) for the FULL
                measured runtime at reuse<=2, plus a non-empty people/face pool.
  D. CONFIG     filmconfig present, valid figure kinds, no banned kinds, sections match the
                narration's real section names.
  E. FILM       film.json present and consistent; if so, defer the final word to
                pd_prerender_gate.py, which is the blocking gate on the render path.
"""
from __future__ import annotations

import argparse
import io
import json
import subprocess
import sys
from pathlib import Path


def _pd_media_root() -> Path:
    """The media root, resolved -- never assumed.

    FIXED 2026-08-22. This file hardcoded H:/pd-media. That drive stopped being enumerated by
    Windows around the 2026-08-16 reboot and config/storage.local.json was repointed to E:\pd-media
    on 2026-08-17. Rule 14: no OS-absolute path is a source of truth. The literal below is kept only
    as a last-resort fallback so an unconfigured checkout behaves as it used to instead of crashing.
    """
    import json as _json
    _cfg = Path(__file__).resolve().parents[1] / "config" / "storage.local.json"
    try:
        return Path(_json.loads(_cfg.read_text(encoding="utf-8"))["roots"]["media"]["path"])
    except Exception:
        return Path("H:/pd-media")


PD_MEDIA = _pd_media_root()


ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "remotion" / "public"
MEDIA = PD_MEDIA
MIN_OK_BYTES = 50_000
MIN_LUMA = 8.0
MIN_VIDEO_SHARE = 0.62
TARGET_CUT_SEC = 4.6
MAX_VIDEO_REUSE = 2
CAPTION_MAX_CHARS = 84
# 2026-08-22: this set had 17 entries and FigureBeats.tsx draws 38. The gate was refusing
# kinds that are ALREADY IN PUBLISHED FILMS -- casetimeline_c appears 28 times across shipped
# episodes, hinders 28, brightline 7, probablecause 5 -- and it BLOCKED EP71 oroville on
# `casetimeline_c` while hyatt/marmet/greene/correa shipped with it. The config was right and
# the gate\x27s vocabulary was stale. Measured, not guessed: the list below is every kind
# FigureBeats.tsx actually renders, minus BANNED_FIGURE_KINDS.
#
# This is NOT a weakened threshold. The gate still refuses anything FigureBeats cannot draw,
# which is the property that matters; it simply stopped refusing things it can.
VALID_KINDS = {"numberticker", "stat", "votetally", "timeline", "quote", "kinetic",
               "lowerthird", "acttitle", "compbars", "bar", "mechanism", "regionmap",
               "pindropmap", "routemap", "arrow", "highlightring", "spotlight",
               # drawn by FigureBeats.tsx and present in shipped films, previously refused:
               "brightline", "burdenflip", "carcutaway", "carkeylock", "casetimeline_c",
               "cashstack", "convergemap", "curtilage", "equitytheft", "govtargument",
               "hallladder", "hinders", "oralargtally", "probablecause", "returnledger",
               "signswap", "splitladder", "statemap", "thresholdmeter", "xrayscan"}
BANNED_FIGURE_KINDS = {"dochighlight"}

EPISODES = {p.name.split("-", 3)[-1]: p.name for p in sorted((ROOT / "episodes").glob("PD-*"))}


def jload(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def mean_luma(path: Path, at: float | None = None) -> float:
    try:
        from PIL import Image
    except ImportError:
        return -1.0
    try:
        if at is None:
            img = Image.open(path)
        else:
            r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{at}", "-i", str(path),
                                "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"],
                               capture_output=True, timeout=60)
            if not r.stdout:
                return -1.0
            img = Image.open(io.BytesIO(r.stdout))
        b = img.convert("L").resize((64, 36)).tobytes()
        return sum(b) / len(b)
    except Exception:
        return -1.0


class Report:
    def __init__(self, slug: str, ep: str):
        self.slug, self.ep = slug, ep
        self.blockers: list[str] = []
        self.warnings: list[str] = []
        self.facts: dict = {}

    def block(self, msg: str):
        self.blockers.append(msg)

    def warn(self, msg: str):
        self.warnings.append(msg)

    @property
    def ready(self) -> bool:
        return not self.blockers


def check_narration(r: Report, ep_dir: Path) -> float:
    idx = ep_dir / "06_audio" / "narration_index.v001.json"
    if not idx.exists():
        r.block("A/NARRATION: narration_index.v001.json missing")
        return 0.0
    d = jload(idx)
    if d.get("is_stub") is True:
        r.block("A/NARRATION: narration_index is a STUB (estimated timings, not measured TTS)")
    chunks = d.get("chunks") or []
    if not chunks:
        r.block("A/NARRATION: narration_index has no chunks")
        return 0.0
    total = float(d.get("total_seconds") or max(float(c["end"]) for c in chunks))
    r.facts["narration_seconds"] = round(total, 1)
    r.facts["narration_minutes"] = round(total / 60, 1)
    r.facts["chunks"] = len(chunks)

    master = MEDIA / "episodes" / r.ep / "06_voice" / "master" / "vc_master_v001.mp3"
    if not master.exists():
        r.block(f"A/NARRATION: master audio missing at {master}")
    else:
        r.facts["master_mb"] = round(master.stat().st_size / 1e6, 1)
    staged = PUBLIC / r.slug / "narration.mp3"
    if not staged.exists():
        r.block(f"A/NARRATION: narration.mp3 not staged at {staged} (the render will find no audio)")

    over = [c for c in chunks
            if len(str(c.get("text") or c.get("spoken_text") or "")) > CAPTION_MAX_CHARS]
    if over:
        r.facts["chunks_needing_caption_split"] = len(over)
    return total


def check_assets(r: Report, ep_dir: Path, total_sec: float, fast: bool) -> None:
    man_p = ep_dir / "05_visuals" / "asset_manifest.v003.json"
    if not man_p.exists():
        r.block("B/ASSETS: asset_manifest.v003.json missing "
                "(run scripts/build_asset_manifest_motionfirst.py --slug " + r.slug + ")")
        return
    man = jload(man_p)
    if man.get("is_stub") is True:
        r.block("B/ASSETS: asset manifest is a stub")
    if man.get("content_checked") is False:
        r.warn("B/ASSETS: manifest was built with --no-content-check (black video can slip through)")

    pools = {k: [x.get("public_path") for x in (man.get(k) or []) if x.get("public_path")]
             for k in ("stills", "people", "motion", "factory", "overlay")}
    body = [x.get("public_path") for x in (man.get("stills") or [])
            if x.get("public_path") and x.get("role") == "body"]
    r.facts["pools"] = {k: len(v) for k, v in pools.items()}
    r.facts["pools"]["stills_body"] = len(body)

    # existence / integrity of everything the film could reference
    missing, stub, dark = [], [], []
    every = sorted({p for v in pools.values() for p in v})
    for rel in every:
        fp = PUBLIC / rel
        if not fp.exists():
            missing.append(rel)
            continue
        if fp.stat().st_size < MIN_OK_BYTES:
            stub.append(rel)
            continue
        if fast:
            continue
        is_vid = fp.suffix.lower() in (".mp4", ".mov", ".webm")
        if is_vid and rel.startswith(f"{r.slug}/overlay/"):
            continue                      # overlays are legitimately dark (screen blend)
        lum = mean_luma(fp, at=0.5 if is_vid else None)
        if 0 <= lum < MIN_LUMA:
            dark.append(f"{rel}(luma{lum:.1f})")
    if missing:
        r.block(f"B/ASSETS: {len(missing)} manifest paths DO NOT EXIST e.g. {missing[:3]}")
    if stub:
        r.block(f"B/ASSETS: {len(stub)} files under {MIN_OK_BYTES}B e.g. {stub[:3]}")
    if dark:
        # "cut assets" was wrong and cost a diagnosis: this scans the whole POOL from the asset
        # manifest, not the film's cuts. On 2026-08-23 it blocked itaewon, lahaina and morandi on
        # clips that are in no cut at all, while pd_prerender_gate -- which does read the cuts --
        # passed all three. Say which set is being measured.
        r.block(f"B/ASSETS: {len(dark)} near-black asset(s) STAGED IN THE POOL (not necessarily "
                f"in any cut -- pd_prerender_gate measures the cuts) e.g. {dark[:3]}")

    # C. pool capacity for motion-first across the FULL runtime
    n_video = len(pools["motion"]) + len(pools["factory"])
    want_cuts = max(60, int(round(total_sec / TARGET_CUT_SEC)))
    need_video = int(want_cuts * MIN_VIDEO_SHARE)
    have_video = n_video * MAX_VIDEO_REUSE
    r.facts["cuts_wanted"] = want_cuts
    r.facts["video_cuts_needed"] = need_video
    r.facts["video_cuts_available"] = have_video
    if have_video < need_video:
        short_min = (need_video - have_video) / MAX_VIDEO_REUSE
        r.block(f"C/POOLS: motion-first impossible -- need {need_video} video cuts for "
                f"{total_sec/60:.1f} min, pools supply {have_video} at reuse<=2 "
                f"(short by ~{short_min:.0f} more real clips)")
    if not pools["people"]:
        r.block("C/POOLS: people/face pool EMPTY -- P## faces would never reach the film")
    if len(body) < 40:
        r.warn(f"C/POOLS: only {len(body)} body stills")


def check_config(r: Report, sections: list[str]) -> None:
    n = r.ep.split("-")[2].lstrip("0")
    cfg_p = ROOT / "episodes" / "_planning" / f"EP{n}_{r.slug}_filmconfig.v001.json"
    if not cfg_p.exists():
        r.block(f"D/CONFIG: {cfg_p.name} missing")
        return
    try:
        cfg = jload(cfg_p)
    except json.JSONDecodeError as e:
        r.block(f"D/CONFIG: invalid JSON ({e})")
        return
    for key in ("slug", "episode_id", "hookLine", "figures_by_section"):
        if not cfg.get(key):
            r.block(f"D/CONFIG: missing required key {key!r}")
    figs = cfg.get("figures_by_section") or {}
    unknown = [s for s in figs if s not in sections]
    if unknown:
        r.block(f"D/CONFIG: figure sections not in the narration: {unknown} "
                f"(their figures would be silently dropped; real sections are {sections})")
    kinds, bad, banned = set(), [], []
    total_figs = 0
    for sec, items in figs.items():
        for f in items or []:
            total_figs += 1
            k = f.get("kind")
            kinds.add(k)
            if k in BANNED_FIGURE_KINDS:
                banned.append(k)
            elif k not in VALID_KINDS:
                bad.append(k)
    if bad:
        r.block(f"D/CONFIG: invalid figure kinds {sorted(set(bad))}")
    if banned:
        r.block(f"D/CONFIG: BANNED figure kinds {sorted(set(banned))}")

    # A CORRECTLY SPELLED KIND WITH THE WRONG PROPS RENDERS NOTHING, and until 2026-08-22 this gate
    # could not see it. EP72 and EP73 both returned READY carrying six figures between them whose
    # props no component reads -- `timeline` given `items` instead of `events`, `bar` given
    # `series`, `routemap` given `from`/`to`, `mechanism` given `steps`. Six blank full-screen
    # figures in films the gate had cleared for render. figure_spec parses the FigureSpec union out
    # of FigureBeats.tsx, so it cannot drift the way the hand-written VALID_KINDS list did.
    try:
        sys.path.insert(0, str(ROOT / "scripts"))
        from figure_spec import check_figure, spec as figure_spec_table  # noqa: PLC0415
        table = figure_spec_table()
        shape_problems = []
        for sec, items in figs.items():
            for i, f in enumerate(items or []):
                for msg in check_figure(f, table):
                    shape_problems.append(f"{sec}[{i}] {f.get('kind')}: {msg}")
        if shape_problems:
            head = "; ".join(shape_problems[:3])
            r.block(f"D/CONFIG: {len(shape_problems)} figure(s) carry props the renderer does not "
                    f"read -- they would draw BLANK: {head}"
                    f"{' ...' if len(shape_problems) > 3 else ''} "
                    f"(full list: py -3.11 scripts/figure_spec.py --config <this file>)")
    except Exception as e:  # noqa: BLE001
        r.warn(f"D/CONFIG: figure prop-shape check did not run ({type(e).__name__}: {e}). "
               f"A blank figure would not be caught here.")
    if len(kinds) < 6:
        r.warn(f"D/CONFIG: only {len(kinds)} distinct figure kinds (<6 = monotony)")
    hook = str(cfg.get("hookLine") or "")
    if hook.rstrip().endswith("?"):
        r.block("D/CONFIG: hookLine is a QUESTION (0 of 26 winning openings open with one)")
    r.facts["figures"] = total_figs
    r.facts["figure_kinds"] = len(kinds)


def check_film(r: Report) -> None:
    film = ROOT / "remotion" / "src" / "data" / f"{r.slug}_film.json"
    if not film.exists():
        r.warn("E/FILM: film.json not built yet (scripts/build_case_film_generic.py)")
        return
    d = jload(film)
    cuts = d.get("cuts") or []
    vid = sum(1 for c in cuts if str(c.get("src", "")).lower().endswith((".mp4", ".mov", ".webm"))
              or c.get("kind") == "footage")
    r.facts["film_cuts"] = len(cuts)
    r.facts["film_video_share"] = round(vid / len(cuts), 4) if cuts else 0
    comp = ROOT / "remotion" / "src" / "compositions"
    wrapper = list(comp.glob(f"{r.slug.capitalize()}Film.tsx")) + list(comp.glob(f"{r.slug}*.tsx"))
    if not wrapper:
        r.block(f"E/FILM: no Remotion composition wrapper for {r.slug} in {comp}")
    root = (ROOT / "remotion" / "src" / "Root.tsx").read_text(encoding="utf-8")
    if r.slug.lower() not in root.lower():
        r.block(f"E/FILM: {r.slug} is not registered in Root.tsx (nothing to render)")


def preflight(slug: str, fast: bool) -> Report:
    ep = EPISODES.get(slug)
    if not ep:
        raise SystemExit(f"unknown slug {slug}")
    r = Report(slug, ep)
    ep_dir = ROOT / "episodes" / ep
    total = check_narration(r, ep_dir)
    sections: list[str] = []
    idx = ep_dir / "06_audio" / "narration_index.v001.json"
    if idx.exists():
        seen = set()
        for c in jload(idx).get("chunks") or []:
            if c["section"] not in seen:
                seen.add(c["section"])
                sections.append(c["section"])
    r.facts["sections"] = sections
    if total > 0:
        check_assets(r, ep_dir, total, fast)
    check_config(r, sections)
    check_film(r)
    return r


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", action="append", help="repeatable; omit with --all")
    ap.add_argument("--all", action="store_true", help="every EP51+ episode")
    ap.add_argument("--fast", action="store_true", help="skip frame decoding (cannot catch black video)")
    ap.add_argument("--json", type=Path, default=None)
    a = ap.parse_args()

    slugs = a.slug or ([s for s in EPISODES if EPISODES[s] >= "PD-2026-051"] if a.all else None)
    if not slugs:
        raise SystemExit("give --slug <slug> (repeatable) or --all")

    results = []
    for slug in slugs:
        r = preflight(slug, a.fast)
        results.append(r)
        print("=" * 74)
        print(f"PD PREFLIGHT  {slug}  ({r.ep})   {'READY' if r.ready else 'BLOCKED'}")
        print(f"  {json.dumps(r.facts, ensure_ascii=False)}")
        for w in r.warnings:
            print(f"  [warn]  {w}")
        for b in r.blockers:
            print(f"  [BLOCK] {b}")
    print("=" * 74)
    ready = [r.slug for r in results if r.ready]
    blocked = [r.slug for r in results if not r.ready]
    print(f"READY  ({len(ready)}): {', '.join(ready) or '-'}")
    print(f"BLOCKED({len(blocked)}): {', '.join(blocked) or '-'}")
    if a.json:
        a.json.write_text(json.dumps(
            [{"slug": r.slug, "episode_id": r.ep, "ready": r.ready, "facts": r.facts,
              "blockers": r.blockers, "warnings": r.warnings} for r in results],
            ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"wrote {a.json}")
    return 0 if not blocked else 1


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    try:
        raise SystemExit(main())
    except SystemExit:
        raise
    except Exception as e:                       # fail closed
        print(f"PREFLIGHT CRASHED ({type(e).__name__}: {e}) -- treat as BLOCKED")
        sys.exit(1)
