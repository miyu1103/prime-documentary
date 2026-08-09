#!/usr/bin/env python
"""Does the video we are about to publish actually contain anything this episode forbids?

Every other footage check in this repo reads a PLAN. This one reads the MASTER.

Three failures in two days say why that is not the same thing:

  * EP56 shipped a red London bus at 9:25 into a film whose highest constraint forbids bus
    imagery -- a sub-postmaster died under one. It was found because a human happened to open
    a frame at that timecode. No check looked.
  * EP61's finished master carried a motorbike rider on a scrambler coming toward camera.
    It was found by pulling ONE frame at 889s out of the render, after every contact sheet
    of the pool had passed. `runs/qc/weimer_clip_verdicts.v001.json` records it in the
    reviewer's own words: "Found only by extracting the rendered frame at 889s ... Neither
    the one-frame sheet nor a six-frame strip caught him."
  * EP62's i2v run established the mechanism: Wan invents subjects -- a woman's head, a hand
    holding a camera, a sheet of paper flying through frame -- and every invention appeared
    in the LAST 1-3 SECONDS of the clip. A mid-clip frame passes all of them.

And `check_spec_satisfied.py` compares `forbidden_subjects` against cut FILENAMES. The
archive's filenames are unreliable in both directions: `empty_parking_garage.mp4` is an
icicle, `open_safe_empty` is the best pool-deck aerial in EP60, and the clip that put the
motorbike on screen is called `lone_tree_in_field`. A filename check cannot see a bus.

So: walk the film's cuts, work out where each one lands in the FINISHED film, pull several
frames per cut OUT OF THE MASTER weighted toward the end of the cut, tile them into labelled
contact sheets -- and then a human, or a subagent with vision, reads the sheets and records a
verdict. The mechanical flags below (near-black, blown-out, filename keyword) are cheap and
kept, but they are not the point. THE SHEETS ARE THE CHECK.

    py -3.11 scripts/check_shipped_frames.py --slug weimer
    py -3.11 scripts/check_shipped_frames.py --slug weimer --sheets-only
    py -3.11 scripts/check_shipped_frames.py --slug weimer --render out/weimer.mp4
    py -3.11 scripts/check_shipped_frames.py --slug weimer --which-master

WHICH MASTER. `--slug` alone used to take the highest vNNN in 08_edit, and a revision number is
not a date. On willingham a `v002` rendered on 30 July beat the `v001` rendered that morning, and
three burned-in name tags belonging to the dead render were one step from being filed as
violations of the live one -- two reviewers' entire reading was invalidated. Selection now
follows the DELIVERY RECORD (09_package/final_delivery.v*.json), falls back to newest mtime, and
states which and why in its normal output; a verdict already on disk is checked with
`--which-master`.

The reviewer writes runs/qc/<slug>_shipped_frames_review.v001.json:

    {"reviewer": "...", "reviewed_at": "2026-08-05",
     "render_sha256": "<the sha this script printed>",
     "reviewed_sheets": ["runs/qc/shipped_frames/weimer/weimer_shipped_frames_08.png", ...],
     "rejected": {"889.250": "motorbike rider on a scrambler comes toward camera"}}

A rejection key is a sampled timecode in seconds (any of the sampled values, matched to 0.05s)
or a frame filename. Exit 1 when a rejection is recorded, when no sheets were produced, or when
a produced sheet was never read -- an unread sheet is NOT a pass, the same fix
write_factory_clip_qc.py needed when it stamped "reviewed" on evidence that did not exist.
Exit 0 only when every sheet exists, every sheet was read against THIS render's bytes, and no
rejection was recorded.

Read-only apart from runs/qc/. No network. No GPU. No render.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from PIL import Image

from build_footage_contact_sheet import COLS, ROWS, build_sheet
from check_episode_spec import load_and_validate
from check_spec_satisfied import _basename, _hits, _words

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "remotion" / "src" / "data"
QC = ROOT / "runs" / "qc"

# The film's own geometry, taken from remotion/src/components/Bookends.tsx. CaseFilm.tsx lays
# the body out as Sequence(from = hook + opening), so a cut's film time is hookSeconds +
# OPENING_SEC + its body start. scripts/audit_films_vs_blocklist.py does the identical walk
# (`t = hookSeconds + 3.5` then `t += dur`); this matches it rather than inventing a third.
OPENING_SEC = 3.5

TILES_PER_SHEET = COLS * ROWS      # 20, exactly what build_footage_contact_sheet tiles

# WHERE THE FRAMES COME FROM, AND WHY.
#   0.20  the shot as a contact sheet would already have shown it -- kept so the sheets remain
#         comparable with the pool sheets, and so an off-theme clip is still caught at the top
#   0.60  the middle of the second half. EP61's motorbike sat at 56% of its cut; a 20/85/95
#         scheme would have flown straight over him
#   0.85  }  EP62 measured every Wan invention -- the woman's head, the hand with the camera,
#   0.95  }  the sheet of paper -- in the LAST 1-3 SECONDS. Two samples, because one is a
#            single instant and these things enter and leave
SAMPLE_FRACTIONS = (0.20, 0.60, 0.85, 0.95)
# Under ~2s the four points are within a few frames of each other and produce near-duplicates.
SHORT_CUT_SEC = 2.0
SHORT_CUT_FRACTIONS = (0.25, 0.70, 0.92)

NEAR_BLACK_MEAN = 12.0             # a frame this dark shows the viewer nothing
BLOWN_OUT_MEAN = 240.0
BLOWN_OUT_FRAC = 0.70              # or 70% of pixels pinned at the top of the range


def _mmss(t: float) -> str:
    return f"{int(t // 60)}:{int(t % 60):02d}"


def _rel(p: Path) -> str:
    """Path as written into the receipt: repo-relative when it is inside the repo, else absolute.

    --out-dir and --render may both point outside the repo (a fixture, a scratch copy), and
    Path.relative_to raises rather than falling back.
    """
    p = Path(p)
    if not p.is_absolute():
        p = ROOT / p
    return p.relative_to(ROOT).as_posix() if p.is_relative_to(ROOT) else p.as_posix()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 22), b""):
            h.update(chunk)
    return h.hexdigest()


def probe_duration(path: Path) -> float:
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
         str(path)], capture_output=True, text=True)
    try:
        return float((r.stdout or "0").strip())
    except ValueError:
        return 0.0


def _rev_num(p: Path) -> int:
    m = re.search(r"\.v(\d+)", p.name)
    return int(m.group(1)) if m else -1


def _mtime(p: Path) -> str:
    return datetime.fromtimestamp(p.stat().st_mtime, timezone.utc).astimezone().strftime(
        "%Y-%m-%d %H:%M")


def delivered_master(epdir: Path) -> tuple[Path | None, str, str]:
    """What the episode says it actually delivered: (path, record filename, recorded sha256).

    The latest `09_package/final_delivery.v*.json` is the answer. Delivery records are immutable
    and superseded rather than edited (`.claude/rules/05-episode-artifacts.md`,
    scripts/new_delivery_revision.py), so the highest revision of THAT file really is the current
    statement of which bytes are the episode -- unlike a render filename, which is just whatever
    the person doing the re-render happened to type.
    """
    recs = sorted((epdir / "09_package").glob("final_delivery.v*.json"), key=_rev_num)
    if not recs:
        return None, "", ""
    try:
        rec = json.loads(recs[-1].read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return None, recs[-1].name, ""
    # THREE SHAPES ARE IN THIS REPO, and crashing on the old two would be worse than the defect
    # being fixed here (the survey that found them hit AttributeError on EP38):
    #   current  canonical_final: {"path": ..., "video_sha256": ...}   EP48 onward
    #   EP38     canonical_final: "<path>" + canonical_final_sha256
    #   legacy   video_file + video_sha256                             EP1-EP30
    cf = rec.get("canonical_final")
    if isinstance(cf, dict):
        raw, rec_sha = cf.get("path"), cf.get("video_sha256")
    elif isinstance(cf, str):
        raw, rec_sha = cf, rec.get("canonical_final_sha256")
    else:
        raw, rec_sha = rec.get("video_file"), rec.get("video_sha256")
    raw = str(raw or "").strip()
    rec_sha = str(rec_sha or "").split(":")[-1].strip()
    if not raw:
        return None, recs[-1].name, rec_sha
    p = Path(raw)
    if not p.is_absolute():
        p = ROOT / p
    return p, recs[-1].name, rec_sha


def select_render(slug: str, explicit: str | None) -> tuple[Path | None, dict]:
    """The finished master, chosen by WHAT WAS DELIVERED -- never by revision number.

    The rule here used to be `sorted(08_edit/<slug>_final_bgm.v*.mp4)[-1]`: the highest vNNN.
    A revision number is not a date. On willingham (2026-08-09) a stale `v002` rendered on
    30 July outranked the `v001` rendered that morning, so three burned-in name tags belonging
    to a dead render were within one step of being filed as violations of the live master, and
    two reviewers' entire reading was void. postoffice carries the identical trap right now:
    its v002 is from 08-03 and the delivered master is v001 from 08-07.

    Order:
      1. `--render`. The uploader passes the delivery path explicitly and must keep winning.
      2. the file named by the latest `09_package/final_delivery.v*.json`.
      3. newest mtime in 08_edit, when there is no usable delivery record.

    Whenever 2 and 3 disagree the selection SAYS SO -- in the normal console output and in the
    receipt. Quietly picking one is the whole defect; the caller has to be told there was a
    choice to make.
    """
    sel: dict = {"slug": slug, "basis": "", "why": "", "delivery_record": None,
                 "delivered_path": None, "delivered_sha256_recorded": "",
                 "newest_mtime_path": None, "candidates": [], "disagreement": False,
                 "warnings": []}

    epdirs = sorted((ROOT / "episodes").glob(f"PD-*-{slug}"))
    epdir = epdirs[0] if epdirs else None
    cands = sorted((epdir / "08_edit").glob(f"{slug}_final_bgm.v*.mp4")) if epdir else []
    sel["candidates"] = [{"path": _rel(c), "mtime": _mtime(c),
                          "mb": round(c.stat().st_size / 1e6)}
                         for c in sorted(cands, key=lambda x: x.stat().st_mtime, reverse=True)]
    newest = max(cands, key=lambda c: c.stat().st_mtime) if cands else None
    if newest is not None:
        sel["newest_mtime_path"] = _rel(newest)
    delivered, rec_name, rec_sha = delivered_master(epdir) if epdir else (None, "", "")
    sel["delivery_record"] = rec_name or None
    sel["delivered_sha256_recorded"] = rec_sha
    if delivered is not None:
        sel["delivered_path"] = _rel(delivered)

    # 1. explicit. Still reported against the delivery record, because the uploader can be
    #    pointed at the wrong file too and this costs nothing to check.
    if explicit:
        p = Path(explicit)
        if not p.is_absolute():
            p = ROOT / p
        sel["basis"] = "explicit"
        sel["why"] = "--render was given; the delivery record below is reported, not used"
        sel["explicit"] = _rel(p)
        if (delivered is not None and p.is_file() and delivered.is_file()
                and p.resolve() != delivered.resolve()):
            sel["disagreement"] = True
            sel["warnings"].append(
                f"--render points at {_rel(p)} but {rec_name} names {_rel(delivered)} as the "
                f"delivered master. Measuring what you asked for; make sure that is what you meant.")
        return (p if p.is_file() else None), sel

    if epdir is None:
        sel["warnings"].append(f"no episodes/PD-*-{slug} directory")
        return None, sel

    # 2. the delivery record.
    if delivered is not None and delivered.is_file():
        if newest is not None and delivered.resolve() != newest.resolve():
            sel["disagreement"] = True
            sel["warnings"].append(
                f"{rec_name} names {delivered.name} ({_mtime(delivered)}) but the newest file in "
                f"08_edit is {newest.name} ({_mtime(newest)}). MEASURING THE DELIVERED ONE. If "
                f"{newest.name} is really the master, record it with "
                f"`scripts/new_delivery_revision.py --slug {slug} --render "
                f"{_rel(newest)}`, or pass --render.")
        sel["basis"] = "final_delivery"
        sel["why"] = f"it is the file {rec_name} names as canonical_final (not the highest vNNN)"
        return delivered, sel

    if delivered is not None:
        sel["warnings"].append(
            f"{rec_name} names {_rel(delivered)}, which is not on disk -- falling back to mtime")

    # 3. mtime.
    if newest is None:
        sel["warnings"].append(f"no {slug}_final_bgm.v*.mp4 under {_rel(epdir / '08_edit')}")
        return None, sel
    sel["basis"] = "mtime"
    sel["why"] = ("newest mtime in 08_edit"
                  + ("" if rec_name else "; this episode has no final_delivery record yet")
                  + (f"; {len(cands)} revisions present and revision NUMBER was NOT used"
                     if len(cands) > 1 else ""))
    if len(cands) > 1:
        sel["warnings"].append(
            f"{len(cands)} master revisions and no usable delivery record: chose {newest.name} "
            f"by mtime. Pass --render if that is not the file you mean.")
    return newest, sel


def describe_selection(sel: dict, render_sha: str) -> None:
    """Print which master was chosen, why, and whether the delivery record agrees on the bytes."""
    rec_sha = sel.get("delivered_sha256_recorded") or ""
    if render_sha:
        sel["render_sha256"] = render_sha
        if rec_sha:
            sel["matches_delivery_sha256"] = render_sha == rec_sha
            if render_sha != rec_sha:
                sel["warnings"].append(
                    f"the bytes measured here ({render_sha[:16]}) are NOT the bytes "
                    f"{sel.get('delivery_record')} records ({rec_sha[:16]}). Either the master was "
                    f"re-rendered without a new delivery revision "
                    f"(scripts/new_delivery_revision.py), or this is the wrong file.")
    for w in sel["warnings"]:
        print(f"[shipped-frames] !! MASTER SELECTION: {w}")
    if sel.get("matches_delivery_sha256"):
        print(f"[shipped-frames] sha256 == canonical_final in {sel['delivery_record']} -- these "
              f"are the delivered bytes")


def which_master(slug: str, explicit: str | None, do_hash: bool = True) -> int:
    """`--which-master`: which file WOULD be measured, and which file the verdict on disk DID.

    Asking that by hand -- `grep '"render"' runs/qc/<slug>_shipped_frames.v001.json` -- is how
    the willingham mix-up was finally caught, after two readings had already been wasted. A
    habit that depends on remembering to grep is not a habit, so it is one command, and it is
    non-zero when the two answers disagree.
    """
    render, sel = select_render(slug, explicit)
    print(f"[which-master] {slug}: would measure {_rel(render) if render else 'NOTHING'}")
    print(f"[which-master]   basis={sel['basis'] or 'none'} -- {sel['why'] or 'no master found'}")
    if sel.get("delivery_record"):
        print(f"[which-master]   {sel['delivery_record']} names {sel['delivered_path']} "
              f"sha={sel['delivered_sha256_recorded'][:16]}")
    for c in sel["candidates"]:
        mark = "->" if render and _rel(render) == c["path"] else "  "
        print(f"[which-master]   {mark} {c['path']}  {c['mtime']}  {c['mb']}MB")
    for w in sel["warnings"]:
        print(f"[which-master]   !! {w}")
    bad = bool(sel["warnings"])

    vp = QC / f"{slug}_shipped_frames.v001.json"
    if not vp.is_file():
        print(f"[which-master]   no verdict on disk yet ({_rel(vp)})")
        return 1 if bad else 0
    v = json.loads(vp.read_text(encoding="utf-8"))
    measured = str(v.get("render") or "")
    print(f"[which-master] {vp.name}: verdict={v.get('verdict')} measured {measured or '(none)'}")
    if render and measured != _rel(render):
        print(f"[which-master]   !! THAT VERDICT IS NOT ABOUT THIS MASTER. It describes "
              f"{measured}. Do not read it as a statement about {_rel(render)}.")
        bad = True
    mp = (ROOT / measured) if measured else None
    if mp is not None and not mp.is_file():
        print(f"[which-master]   !! the file it measured is no longer there: {measured}")
        bad = True
    elif mp is not None and do_hash and v.get("render_sha256"):
        now = sha256(mp)
        ok = now == v.get("render_sha256")
        print(f"[which-master]   that file's sha256 {'==' if ok else '!='} the sha the verdict "
              f"names ({now[:16]} vs {str(v.get('render_sha256'))[:16]})")
        if not ok:
            print("[which-master]   !! the bytes changed under the verdict -- re-run the check")
            bad = True
    return 1 if bad else 0


def plan_samples(film: dict, video_seconds: float, fps: float) -> tuple[list[dict], list[str]]:
    """Every frame we intend to look at, with its time in the FINISHED film.

    Returns (samples, notes). The walk accumulates `dur` exactly as
    audit_films_vs_blocklist.py does, and cross-checks each accumulated value against the
    cut's own declared `start` -- a silent drift between the two would put every sampled
    timecode in the wrong place, which is the one way this check could lie.
    """
    notes: list[str] = []
    hook = float(film.get("hookSeconds") or 0.0)
    t = hook + OPENING_SEC
    samples: list[dict] = []
    drift = 0.0
    frame = 1.0 / fps if fps else 1.0 / 30.0
    for idx, cut in enumerate(film.get("cuts") or []):
        dur = float(cut.get("dur") or 0.0)
        if cut.get("start") is not None:
            drift = max(drift, abs((hook + OPENING_SEC + float(cut["start"])) - t))
        src = _basename(cut.get("src"))
        fracs = SHORT_CUT_FRACTIONS if dur < SHORT_CUT_SEC else SAMPLE_FRACTIONS
        for fr in fracs:
            # never let the last sample tip into the next cut
            at = min(t + dur * fr, t + max(0.0, dur - frame))
            if video_seconds and at >= video_seconds:
                continue
            samples.append({
                "cut_index": idx,
                "cut_id": cut.get("id"),
                "act": cut.get("act"),
                "src": cut.get("src"),
                "src_basename": src,
                "cut_start_s": round(t, 3),
                "cut_dur_s": round(dur, 3),
                "fraction": fr,
                "t_film_s": round(at, 3),
                "mmss": _mmss(at),
            })
        t += dur
    if drift > 0.08:
        notes.append(f"cut `start` fields and the accumulated walk disagree by up to {drift:.3f}s "
                     f"-- timecodes below follow the accumulated walk (audit_films_vs_blocklist "
                     f"arithmetic); resolve the film before trusting them")
    body_end = t
    if video_seconds and abs(body_end - video_seconds) > 60:
        notes.append(f"film body ends at {body_end:.1f}s but the render is {video_seconds:.1f}s "
                     f"long -- if that gap is not the {OPENING_SEC}s opening plus the endcard, "
                     f"the film json may not be the plan this master was rendered from")
    return samples, notes


def extract(render: Path, at: float, out: Path) -> bool:
    """One ffmpeg per frame, seeking to an explicit -ss IN THE MASTER.

    Never from the source clip: what matters is the slice that is actually on screen, after
    the in-point, the loop, the grade, the vignette and whatever is composited over it.
    -pix_fmt yuvj420p because several archive clips are full-range and mjpeg refuses them.
    """
    r = subprocess.run(
        ["ffmpeg", "-v", "error", "-ss", f"{at:.3f}", "-i", str(render),
         "-frames:v", "1", "-vf", "scale=960:-2", "-pix_fmt", "yuvj420p", "-q:v", "3",
         "-y", str(out)],
        capture_output=True, text=True)
    return r.returncode == 0 and out.is_file() and out.stat().st_size > 0


def measure(path: Path) -> dict:
    """Cheap exposure facts about one frame. Not a judgement of content -- see the docstring."""
    with Image.open(path) as im:
        g = im.convert("L")
        hist = g.histogram()
    total = sum(hist) or 1
    mean = sum(i * n for i, n in enumerate(hist)) / total
    return {
        "mean_luma": round(mean, 2),
        "frac_black": round(sum(hist[:16]) / total, 4),
        "frac_white": round(sum(hist[250:]) / total, 4),
    }


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--slug", required=True)
    ap.add_argument("--render", help="the finished master (default: the file named by the "
                                     "latest episodes/PD-*-<slug>/09_package/final_delivery.v*"
                                     ".json, else newest mtime in 08_edit -- never highest vNNN)")
    ap.add_argument("--film", help="film json override (default remotion/src/data/<slug>_film.json)")
    ap.add_argument("--sheets-only", action="store_true",
                    help="extract and tile, then stop. Records verdict=UNREVIEWED so a later "
                         "full run still fails until somebody reads the sheets.")
    ap.add_argument("--force", action="store_true", help="re-extract frames already on disk")
    ap.add_argument("--no-hash", action="store_true",
                    help="skip the render sha256 (faster; the review can then not be bound "
                         "to these exact bytes)")
    ap.add_argument("--out-dir", help="where frames and sheets go (default "
                                      "runs/qc/shipped_frames/<slug>)")
    ap.add_argument("--which-master", action="store_true",
                    help="print which master would be measured, why, and which one the verdict "
                         "already on disk actually measured -- then stop. Extracts nothing. "
                         "Exit 1 when the two disagree.")
    a = ap.parse_args()
    slug = a.slug

    if a.which_master:
        return which_master(slug, a.render, not a.no_hash)

    film_path = Path(a.film) if a.film else DATA / f"{slug}_film.json"
    if not film_path.is_absolute():
        film_path = ROOT / film_path
    if not film_path.is_file():
        print(f"[shipped-frames] {slug}: NO FILM -- {film_path}")
        return 1
    film = json.loads(film_path.read_text(encoding="utf-8"))

    render, sel = select_render(slug, a.render)
    if render is None:
        print(f"[shipped-frames] {slug}: NO RENDER -- pass --render, or build "
              f"episodes/PD-*-{slug}/08_edit/{slug}_final_bgm.v*.mp4")
        for w in sel["warnings"]:
            print(f"[shipped-frames]   {w}")
        return 1

    # The episode's own contract. Missing/invalid is not fatal here -- check_episode_spec.py
    # is the gate for that -- but the filename keyword pass needs forbidden_subjects.
    spec, spec_problems, _epdir = load_and_validate(slug)
    forbidden = [k for k in ((spec or {}).get("forbidden_subjects") or []) if str(k).strip()]

    fps = float(film.get("fps") or 30)
    seconds = probe_duration(render)
    samples, notes = plan_samples(film, seconds, fps)

    out_dir = Path(a.out_dir) if a.out_dir else QC / "shipped_frames" / slug
    if not out_dir.is_absolute():
        out_dir = ROOT / out_dir
    frames_dir = out_dir / "frames"
    frames_dir.mkdir(parents=True, exist_ok=True)

    render_sha = "" if a.no_hash else sha256(render)
    print(f"[shipped-frames] {slug}: render={_rel(render)}"
          f" {render.stat().st_size / 1e6:.0f}MB {seconds:.1f}s @{fps:g}fps")
    print(f"[shipped-frames] master chosen by {sel['basis']}: {sel['why']}")
    describe_selection(sel, render_sha)
    print(f"[shipped-frames] film={film_path.name} cuts={len(film.get('cuts') or [])} "
          f"hook={film.get('hookSeconds')}s + opening={OPENING_SEC}s -> body starts at "
          f"{float(film.get('hookSeconds') or 0) + OPENING_SEC:g}s")
    if render_sha:
        print(f"[shipped-frames] render sha256={render_sha}")
    if spec_problems:
        print(f"[shipped-frames] NOTE: no usable episode spec ({spec_problems[0]}) -- the "
              f"filename keyword pass is skipped; the sheets are unaffected")
    for n in notes:
        print(f"[shipped-frames] WARNING: {n}")

    # ---- extract -------------------------------------------------------------------------
    # Frames are cached by timecode, and a timecode means nothing across two different renders.
    # EP35 shipped with a probe receipt taken from a render that was not the file being
    # uploaded; the same mistake here would show a reviewer the OLD film's pixels and call it a
    # review of the new one. The frame cache is therefore stamped with the render it came from
    # and discarded the moment that changes.
    marker = frames_dir / "_render.sha256"
    prev = marker.read_text(encoding="utf-8").strip() if marker.is_file() else ""
    if render_sha and prev and prev != render_sha:
        gone = [f for f in frames_dir.glob("*.jpg")]
        for f in gone:
            f.unlink()
        print(f"[shipped-frames] {len(gone)} cached frame(s) came from render {prev[:12]}..., "
              f"not this one -- discarded and re-extracted")
    if render_sha:
        marker.write_text(render_sha + "\n", encoding="utf-8")
    elif prev:
        print("[shipped-frames] WARNING: --no-hash, so cached frames cannot be proved to come "
              "from THIS render. Use --force if the master was rebuilt.")

    missing = 0
    for s in samples:
        name = (f"{int(s['t_film_s'] // 60):03d}m{int(s['t_film_s'] % 60):02d}s"
                f"_{int(round((s['t_film_s'] % 1) * 1000)):03d}"
                f"__cut{s['cut_index']:04d}_p{int(s['fraction'] * 100):02d}.jpg")
        fp = frames_dir / name
        s["frame"] = _rel(fp)
        if a.force or not fp.is_file():
            if not extract(render, s["t_film_s"], fp):
                s["extract_failed"] = True
                missing += 1
                continue
        s.update(measure(fp))
    print(f"[shipped-frames] {len(samples)} frame(s) sampled from {len(film.get('cuts') or [])} "
          f"cut(s) at {'/'.join(f'{int(f * 100)}%' for f in SAMPLE_FRACTIONS)} of each cut"
          + (f"; {missing} could not be extracted" if missing else ""))

    # ---- what a machine can flag, and what it cannot -------------------------------------
    for s in samples:
        flags: list[str] = []
        if s.get("extract_failed"):
            flags.append("extract_failed")
        else:
            if s.get("mean_luma", 255) < NEAR_BLACK_MEAN:
                flags.append("near_black")
            if s.get("mean_luma", 0) > BLOWN_OUT_MEAN or s.get("frac_white", 0) > BLOWN_OUT_FRAC:
                flags.append("blown_out")
        hay = _words(s["src_basename"])
        for kw in forbidden:
            if _hits(kw, hay):
                flags.append(f"filename_keyword:{kw}")
        s["flags"] = flags

    # ---- sheets --------------------------------------------------------------------------
    sheets: list[dict] = []
    tiles = [s for s in samples if not s.get("extract_failed")]
    for n in range(0, len(tiles), TILES_PER_SHEET):
        chunk = tiles[n:n + TILES_PER_SHEET]
        idx = n // TILES_PER_SHEET + 1
        out = out_dir / f"{slug}_shipped_frames_{idx:02d}.png"
        labels: dict[str, str] = {}
        paths: list[Path] = []
        for s in chunk:
            p = ROOT / s["frame"]
            paths.append(p)
            # `off_label:` makes build_sheet draw the verdict line in warning colour.
            lead = "off_label " if s["flags"] else ""
            labels[str(p)] = f"{lead}{s['mmss']} {s['src_basename']}"
            s["sheet"] = _rel(out)
        build_sheet(paths, out,
                    f"{slug} — SHIPPED MASTER frames  (sheet {idx}, "
                    f"{chunk[0]['mmss']}–{chunk[-1]['mmss']})", labels)
        sheets.append({"sheet": _rel(out),
                       "tiles": len(chunk),
                       "from_mmss": chunk[0]["mmss"], "to_mmss": chunk[-1]["mmss"]})
    print(f"[shipped-frames] {len(sheets)} labelled contact sheet(s) in "
          f"{_rel(out_dir)}")

    # ---- the reviewer's verdict ----------------------------------------------------------
    review_path = QC / f"{slug}_shipped_frames_review.v001.json"
    review = json.loads(review_path.read_text(encoding="utf-8")) if review_path.is_file() else {}
    reviewed_sheets = [str(x).replace("\\", "/") for x in (review.get("reviewed_sheets") or [])]
    rejected_in = review.get("rejected") or {}

    rejections: list[dict] = []
    by_time = {round(s["t_film_s"], 2): s for s in samples}
    for key, why in rejected_in.items():
        hit = None
        try:
            want = round(float(key), 2)
            hit = by_time.get(want) or next(
                (s for s in samples if abs(s["t_film_s"] - want) <= 0.05), None)
        except ValueError:
            hit = next((s for s in samples
                        if Path(s.get("frame", "")).name == str(key)
                        or str(key) in s.get("frame", "")), None)
        rejections.append({
            "key": str(key),
            "reason": str(why),
            "source": "sheet_review",
            "t_film_s": hit["t_film_s"] if hit else None,
            "mmss": hit["mmss"] if hit else None,
            "cut_index": hit["cut_index"] if hit else None,
            "cut_src": hit["src"] if hit else None,
            "frame": hit.get("frame") if hit else None,
            "sheet": hit.get("sheet") if hit else None,
            "matched_a_sample": hit is not None,
        })

    # A sheet counts as read only if the reviewer named THIS file and it is on disk. Listing
    # sheets that were never opened is the exact false green write_factory_clip_qc.py carried.
    produced = {s["sheet"] for s in sheets}

    # PER-SOURCE COVERAGE: weaker than frame coverage, and it has to say so out loud.
    # A real minor, scraped footage and legible personal data are properties of the clip, so
    # seeing every clip once answers them; a card landing on a face, or content that appears
    # only between sampled points, it cannot answer. Accepted only when the claim is verified:
    # every distinct source in the film must actually appear in a listed sheet.
    per_source = str(review.get("coverage_mode", "")) == "per_source"
    per_source_gap: list[str] = []
    if per_source:
        _film_srcs = {str(c.get("src", "")).split("/")[-1] for c in film.get("cuts", [])}
        _seen = set()
        for _p in reviewed_sheets:
            _dir = (ROOT / _p).parent / "frames"
            if not _dir.is_dir():
                continue
            # Only the tiles ON THIS SHEET. Globbing the whole frames folder would count
            # evidence that exists rather than evidence someone said they read, and dropping a
            # sheet would change nothing -- which is exactly what the first version did.
            _m = re.search(r"_(\d+)\.png$", Path(_p).name)
            if not _m:
                continue
            _k = int(_m.group(1))
            _lo, _hi = (_k - 1) * TILES_PER_SHEET, _k * TILES_PER_SHEET
            for _f in _dir.glob("*.jpg"):
                _n = re.match(r"^(\d+)__", _f.name)
                if not _n or not (_lo <= int(_n.group(1)) < _hi):
                    continue
                for _s in _film_srcs:
                    if _s in _f.name:
                        _seen.add(_s)
        per_source_gap = sorted(_film_srcs - _seen)
        print(f"[shipped-frames] coverage_mode=per_source: {len(_seen)}/{len(_film_srcs)} "
              f"distinct source(s) appear in a reviewed sheet"
              + (f"; {len(per_source_gap)} NOT covered" if per_source_gap else ""))
        produced = {p for p in reviewed_sheets if (ROOT / p).is_file()}

    read = {p for p in reviewed_sheets if p in produced and (ROOT / p).is_file()}
    unread = sorted(produced - read)
    if per_source and per_source_gap:
        unread = unread + [f"<source not covered: {s}>" for s in per_source_gap[:5]]
    sha_bound = (not render_sha) or (review.get("render_sha256") == render_sha)

    # A REJECTION IS A STATEMENT ABOUT ONE SET OF BYTES, AND ONLY THOSE.
    # The first re-render proved why: fieldtest's three rejected clips were pruned and the film
    # rebuilt, but the old review still named their timecodes, so the new master came back FAIL
    # citing cut-0201 as a fingerprint card when cut-0201 is now a glass vial. Carried forward,
    # a fixed episode can never go green. The reverse -- a stale PASS reaching a new render --
    # is already handled below by sha_bound, and stays handled: dropping these does not turn an
    # unreviewed render green, it makes it UNREVIEWED, which never passes.
    if rejections and not sha_bound:
        print(f"[shipped-frames] {len(rejections)} rejection(s) in the review name "
              f"render_sha256={str(review.get('render_sha256'))[:16]!r}, not this render "
              f"({str(render_sha)[:16]!r}). They describe bytes that no longer exist here and "
              f"are NOT applied. Re-read the sheets for THESE bytes.")
        rejections = []

    verdict = "PASS"
    reasons: list[str] = []
    if not sheets:
        verdict = "FAIL"
        reasons.append("no contact sheet was produced -- there is no evidence to read")
    if rejections:
        verdict = "FAIL"
        reasons.append(f"{len(rejections)} rejection(s) recorded by the sheet review")
    # A frame nobody could extract is a frame nobody looked at. Fail closed, exactly as the
    # duplicate pre-check in upload_schedule_case_v001.py does: not knowing is not the same as
    # knowing there is nothing there.
    _unseen = [s for s in samples if s.get("extract_failed")]
    if _unseen:
        verdict = "FAIL"
        reasons.append(f"{len(_unseen)} sampled frame(s) could not be extracted from the master "
                       f"(first at {_unseen[0]['mmss']}) -- "
                       f"that part of the film has not been seen")
    if a.sheets_only:
        verdict = "UNREVIEWED" if verdict == "PASS" else verdict
        reasons.append("--sheets-only: the evidence was produced and nothing was read. "
                       "This mode never passes, by design.")
    elif sheets and unread:
        verdict = "UNREVIEWED" if verdict == "PASS" else verdict
        reasons.append(f"{len(unread)} of {len(sheets)} sheet(s) carry no record of being read "
                       f"({unread[0]} ...)" if len(unread) < len(sheets) else
                       f"none of the {len(sheets)} sheet(s) have been read")
    elif sheets and not sha_bound:
        verdict = "UNREVIEWED" if verdict == "PASS" else verdict
        reasons.append(f"the review names render_sha256={review.get('render_sha256')!r}, which is "
                       f"not this render -- re-read the sheets for THESE bytes")

    receipt = {
        "schema_version": "1.0.0",
        "slug": slug,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "render": _rel(render),
        "render_sha256": render_sha,
        "render_selection": sel,
        "render_seconds": round(seconds, 3),
        "film": _rel(film_path),
        "fps": fps,
        "hook_seconds": float(film.get("hookSeconds") or 0.0),
        "opening_seconds": OPENING_SEC,
        "body_offset_seconds": float(film.get("hookSeconds") or 0.0) + OPENING_SEC,
        "cuts": len(film.get("cuts") or []),
        "sample_fractions": list(SAMPLE_FRACTIONS),
        "short_cut_seconds": SHORT_CUT_SEC,
        "short_cut_fractions": list(SHORT_CUT_FRACTIONS),
        "forbidden_subjects": forbidden,
        "notes": notes,
        "filename_test_is_not_the_point": (
            "The keyword pass below compares forbidden_subjects against the cut's source "
            "FILENAME. It is kept because it is free, but the archive's filenames are wrong in "
            "both directions -- empty_parking_garage.mp4 is an icicle, and the clip that put a "
            "motorbike rider into EP61 is called lone_tree_in_field. THE CONTACT SHEETS ARE THE "
            "CHECK. A green line here means nobody was caught by a filename, not that the film "
            "is clean."),
        "review_file": _rel(review_path),
        "review": {
            "reviewer": review.get("reviewer"),
            "reviewed_at": review.get("reviewed_at"),
            "reviewed_sheets": sorted(read),
            "unread_sheets": unread,
            "bound_to_this_render": sha_bound,
        },
        "sheets": sheets,
        "samples": samples,
        "mechanical_flags": sorted({f for s in samples for f in s.get("flags", [])}),
        "rejections": rejections,
        "verdict": verdict,
        "verdict_reasons": reasons,
    }
    QC.mkdir(parents=True, exist_ok=True)
    verdict_path = QC / f"{slug}_shipped_frames.v001.json"
    verdict_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=1) + "\n",
                            encoding="utf-8")

    flagged = [s for s in samples if s.get("flags")]
    print(f"[shipped-frames] mechanical: {len(flagged)} flagged frame(s) "
          f"{sorted({f for s in flagged for f in s['flags']}) or '[]'}")
    for s in flagged[:12]:
        print(f"    {s['mmss']} ({s['t_film_s']:.2f}s) cut-{s['cut_index']:04d} "
              f"{s['src_basename']}  {','.join(s['flags'])}")
    if len(flagged) > 12:
        print(f"    ... and {len(flagged) - 12} more (all of them are in {verdict_path.name})")
    print("[shipped-frames] the filename keyword test above is NOT the check. It cannot see a "
          "bus. Open the sheets.")
    for r in rejections:
        where = f"{r['mmss']} ({r['t_film_s']:.2f}s)" if r["matched_a_sample"] else f"key {r['key']!r}"
        print(f"[shipped-frames] REJECTED at {where}"
              + (f" cut-{r['cut_index']:04d} {_basename(r['cut_src'])}" if r["matched_a_sample"] else "")
              + f": {r['reason']}")
    print(f"[shipped-frames] verdict -> {_rel(verdict_path)}")
    print(f"[shipped-frames] it describes {_rel(render)} AND NOTHING ELSE"
          + (f" (sha {render_sha[:16]})" if render_sha else "")
          + f". Before acting on it: py -3.11 scripts/check_shipped_frames.py --slug {slug} "
            f"--which-master")

    if verdict == "PASS":
        print(f"[shipped-frames] {slug}: PASS -- {len(sheets)} sheet(s), all read"
              + (" against this render's sha256" if render_sha else "")
              + ", no rejection recorded")
        return 0
    if verdict == "UNREVIEWED":
        print(f"[shipped-frames] {slug}: NOT A PASS -- the frames exist but nobody has said "
              f"what is in them.")
        for r in reasons:
            print(f"  - {r}")
        print(f"  Open the sheets in {_rel(out_dir)}, then write "
              f"{_rel(review_path)} with reviewed_sheets"
              + (f' and render_sha256 "{render_sha}".' if render_sha else "."))
        return 1
    print(f"[shipped-frames] {slug}: FAIL")
    for r in reasons:
        print(f"  - {r}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
