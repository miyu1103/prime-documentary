#!/usr/bin/env python
"""Replace a handful of cuts in a FINISHED master without re-rendering the film.

WHY THIS EXISTS
---------------
EP62 greene shipped with six cuts that the blocklist forbids: two uses each of
AR-8847832 (a modern US election ballot), AR-28450296 (a modern European park) and
AR-8035620 (legible Breaking Bad shot-list cards). Six cuts is about 29 seconds of
picture in a 31-minute film -- 73 seconds once each is widened to its enclosing GOPs,
which is 3.93% of the 55,846 frames. The reflex was to prune the pool, re-run
scripts/build_case_film_generic.py and re-render the whole thing -- four hours, and the
rebuild reshuffles all 389 cuts so nothing about the master survives. (It already
happened once: greene_film.json was rebuilt on 2026-08-11 after the 2026-08-10 render,
and 278 of its 389 cuts now name a different clip than the shipped master does. That is
what --verify exists to catch, and it does: 26.1 dB and 31.3 dB against a 36 dB bar.)

The owner's question was the right one: replace the broken cuts, leave the rest alone.
This tool does exactly that.

    old master ──┬── keep [0 .. a-1]          (stream copy, byte-identical)
                 ├── RE-RENDER [a .. b]       (Remotion, only these frames)
                 └── keep [b+1 .. end]        (stream copy, byte-identical)
                     + the ORIGINAL audio stream, copied, never re-encoded

HOW IT KEEPS THE REST OF THE FILM INTACT
----------------------------------------
* The film json is edited IN PLACE for the named cuts only -- `src` (and the
  `srcSeconds` / `loopSource` that follow from it). `start`, `dur`, `id`, `seed`,
  `act`, `kind`, `treatment` and every other cut are left byte-for-byte alone, and
  that is checked structurally after the write. The builder is never re-run.
* Cut i's picture depends on cut i's own fields and on its index (CaseFilm passes
  `index` into CutView and derives `startFrom` from it), so leaving the array order and
  every other cut untouched leaves every other cut's pixels untouched.
* Splice boundaries are snapped OUTWARD to the master's own keyframes, so the kept head
  and tail are copied without being decoded, and the re-rendered middle always begins on
  an IDR. Nothing is cut mid-GOP.
* Segments are joined as MPEG-TS (each carries its own in-band SPS/PPS) and then remuxed
  to mp4. Concatenating mp4s directly would keep only the first segment's `avcC`, which
  silently mis-decodes the others if the two encodes disagree by even one VUI field.
* The middle is encoded by Remotion itself, reading the repo's remotion.config.ts, so
  the encoder settings are the originals by construction rather than by transcription.
  They are then read back off both files with ffprobe and compared anyway.

WHAT IT REFUSES TO DO
---------------------
The whole method rests on one precondition: the film json on disk must be the json the
master was rendered from. If it is not, every frame number here points at the wrong
picture. `--verify` renders a couple of frames from cuts that are NOT being replaced and
PSNRs them against the same timecodes in the master; below the threshold the run aborts
before anything is written. Run it. It costs two frames.

USAGE
-----
    py -3.11 scripts/pd_splice_cuts.py \
        --slug greene --comp Ep62Greene \
        --master episodes/PD-2026-062-greene/08_edit/greene_final_bgm.v001.mp4 \
        --out    episodes/PD-2026-062-greene/08_edit/greene_final_bgm.v002.mp4 \
        --public-dir remotion/public_slim \
        --replace cut-0011=greene/factory/AR-xxxx.mp4 \
        --replace cut-0098=greene/factory/AR-yyyy.mp4 \
        --verify 2

    # see the plan and the frame budget, touch nothing:
    ... --dry-run

LIMITS -- read these before reaching for it
-------------------------------------------
* It changes cut CONTENT, never cut TIMING. `start` and `dur` are invariants.
* Anything that moves the timeline -- a new hook, a script change, a caption re-sync, a
  different narration -- shifts every later frame and needs a full render.
* Whole-file gates (loudness, animation_density, motion_energy, footage_diversity) must
  be re-run on the spliced master. That is a scan, not a render, but it is not free.
* The acceptance receipt binds to `video_sha256`; a spliced master is a new file and
  needs re-grading.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REMOTION = ROOT / "remotion"
BOOKENDS = REMOTION / "src" / "components" / "Bookends.tsx"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


# --------------------------------------------------------------------------- shell


def run(cmd: list[str], cwd: Path | None = None, quiet: bool = True) -> subprocess.CompletedProcess:
    r = subprocess.run(
        cmd, cwd=str(cwd) if cwd else None, capture_output=True, text=True, encoding="utf-8",
        errors="replace",
    )
    if r.returncode != 0 and not quiet:
        print(r.stdout[-4000:])
        print(r.stderr[-4000:], file=sys.stderr)
    return r


def must(cmd: list[str], what: str, cwd: Path | None = None) -> subprocess.CompletedProcess:
    r = run(cmd, cwd=cwd)
    if r.returncode != 0:
        print(f"[splice] FAILED: {what}", file=sys.stderr)
        print("  cmd: " + " ".join(cmd), file=sys.stderr)
        print((r.stderr or r.stdout)[-4000:], file=sys.stderr)
        raise SystemExit(2)
    return r


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 22), b""):
            h.update(chunk)
    return h.hexdigest()


# --------------------------------------------------------------------------- probe


def probe_streams(path: Path) -> dict:
    r = must(
        ["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)],
        f"ffprobe {path.name}",
    )
    return json.loads(r.stdout)


def video_stream(info: dict) -> dict:
    for s in info["streams"]:
        if s.get("codec_type") == "video":
            return s
    raise SystemExit(f"[splice] no video stream")


def audio_stream(info: dict) -> dict | None:
    for s in info["streams"]:
        if s.get("codec_type") == "audio":
            return s
    return None


ENCODER_KEYS = (
    "codec_name", "profile", "level", "pix_fmt", "width", "height",
    "color_range", "color_space", "color_transfer", "color_primaries",
    "chroma_location", "field_order", "r_frame_rate",
)


def encoder_fingerprint(info: dict) -> dict:
    v = video_stream(info)
    return {k: v.get(k) for k in ENCODER_KEYS}


def video_packet_count(path: Path) -> int:
    r = must(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_packets",
         "-show_entries", "stream=nb_read_packets", "-of", "csv=p=0", str(path)],
        f"count packets {path.name}",
    )
    return int(r.stdout.strip().splitlines()[0])


def keyframe_frames(path: Path, fps: float) -> list[int]:
    """Frame indices of every video keyframe. Reads the packet index; decodes nothing."""
    r = must(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "packet=pts_time,flags", "-of", "csv=p=0", str(path)],
        f"keyframe scan {path.name}",
    )
    out: list[int] = []
    for line in r.stdout.splitlines():
        parts = line.strip().split(",")
        if len(parts) < 2 or "K" not in parts[1]:
            continue
        try:
            out.append(int(round(float(parts[0]) * fps)))
        except ValueError:
            continue
    return sorted(set(out))


def audio_stream_md5(path: Path) -> str:
    """md5 of the AUDIO ELEMENTARY STREAM (copied packets), not the container."""
    r = must(
        ["ffmpeg", "-v", "error", "-i", str(path), "-map", "0:a:0", "-c", "copy", "-f", "md5", "-"],
        f"audio md5 {path.name}",
    )
    return r.stdout.strip().split("=")[-1]


def framemd5_window(path: Path, start_frame: int, count: int, fps: float) -> str:
    """md5 of `count` DECODED frames starting at `start_frame`. Input seek is
    frame-accurate in ffmpeg (it lands on the previous keyframe and decodes forward)."""
    r = must(
        ["ffmpeg", "-v", "error", "-ss", f"{start_frame / fps:.6f}", "-i", str(path),
         "-frames:v", str(count), "-map", "0:v:0", "-f", "framemd5", "-"],
        f"framemd5 {path.name}@{start_frame}",
    )
    body = [ln for ln in r.stdout.splitlines() if ln and not ln.startswith("#")]
    return hashlib.md5(("\n".join(ln.split(",")[-1].strip() for ln in body)).encode()).hexdigest(), len(body)


def psnr_window(a: Path, b: Path, start_frame: int, count: int, fps: float,
                seek_b: bool = True) -> float:
    """Mean PSNR (dB) of `count` frames of b against a.

    `a` is always seeked to `start_frame`. ffmpeg input seek is frame-accurate -- it lands on
    the previous keyframe and decodes forward -- verified against `select=eq(n\,59)`, which
    produced an identical PNG. `seek_b=False` is for a probe file that IS the single frame:
    seeking a one-frame file to 2 s yields nothing, the psnr filter then prints no summary at
    all, and this read back NaN the first time it ran.

    Calibration on the fixture, one freshly rendered frame against the master:
        the same frame           43.5 dB
        the neighbouring frame   28.4 dB   (same cut, one frame off)
        a frame of another cut   15.2 dB
    so the 36 dB default separates "this json made this master" from "it did not"."""
    ss = f"{start_frame / fps:.6f}"
    cmd = ["ffmpeg", "-v", "info", "-ss", ss, "-i", str(a)]
    if seek_b:
        cmd += ["-ss", ss]
    # Both legs are trimmed explicitly. `-frames:v N` bounds only the OUTPUT, and framesync
    # repeats the shorter leg's last frame, so an unbounded graph silently compares frame 59
    # of one file against frames 59,60,61 of the other -- that is where the first 34 dB
    # reading came from against a true 43.5 dB.
    graph = (f"[0:v]trim=end_frame={count},setpts=PTS-STARTPTS[x];"
             f"[1:v]trim=end_frame={count},setpts=PTS-STARTPTS[y];[x][y]psnr")
    cmd += ["-i", str(b), "-an", "-lavfi", graph, "-f", "null", "-"]
    r = must(cmd, f"psnr {a.name} vs {b.name}@{start_frame}")
    m = re.search(r"average:([0-9.]+|inf)", r.stderr)
    if not m:
        return float("nan")
    return float("inf") if m.group(1) == "inf" else float(m.group(1))


def media_duration(path: Path) -> float:
    info = probe_streams(path)
    return float(info["format"]["duration"])


# --------------------------------------------------------------------------- film


def opening_sec() -> float:
    """OPENING_SEC out of Bookends.tsx -- the number lives there once."""
    if not BOOKENDS.is_file():
        return 3.5
    m = re.search(r"OPENING_SEC\s*=\s*([0-9.]+)", BOOKENDS.read_text(encoding="utf-8"))
    return float(m.group(1)) if m else 3.5


def lead_frames(film: dict, fps: float) -> int:
    """Exactly CaseFilm.caseFilmLeadFrames -- the offset the body sits at."""
    if film.get("leadSeconds") is not None:
        return round(film["leadSeconds"] * fps)
    return round((film.get("hookSeconds") or 0) * fps) + round(opening_sec() * fps)


def cut_frame_span(film: dict, cut: dict, fps: float) -> tuple[int, int]:
    """[first, last] absolute frame of a cut -- CaseFilm's own <Sequence> arithmetic."""
    lead = lead_frames(film, fps)
    a = lead + round(cut["start"] * fps)
    n = max(1, round(cut["dur"] * fps))
    return a, a + n - 1


def find_cut(film: dict, key: str) -> tuple[int, dict]:
    for i, c in enumerate(film["cuts"]):
        if c.get("id") == key:
            return i, c
    if key.isdigit():
        i = int(key)
        if 0 <= i < len(film["cuts"]):
            return i, film["cuts"][i]
    raise SystemExit(f"[splice] no cut {key!r} in the film json")


def source_seconds(public_dir: Path, src: str) -> float | None:
    p = public_dir / src
    if not p.is_file() or p.suffix.lower() not in (".mp4", ".mov", ".webm", ".mkv"):
        return None
    r = run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)])
    try:
        return round(float(r.stdout.strip()), 3)
    except ValueError:
        return None


# --------------------------------------------------------------------------- ranges


@dataclass
class Replacement:
    cut_index: int
    cut_id: str
    old_src: str
    new_src: str
    start_s: float
    dur_s: float
    frame_a: int
    frame_b: int


@dataclass
class Range:
    a: int          # first frame to re-render (a keyframe of the master)
    b: int          # last frame to re-render (the frame before the next keyframe)
    cuts: list[str] = field(default_factory=list)
    wanted: list[tuple[int, int]] = field(default_factory=list)  # the cut spans inside

    @property
    def n(self) -> int:
        return self.b - self.a + 1


def snap_to_gop(a: int, b: int, kfs: list[int], total: int) -> tuple[int, int]:
    """Widen [a,b] to the enclosing GOPs of the master."""
    before = [k for k in kfs if k <= a]
    sa = before[-1] if before else 0
    after = [k for k in kfs if k > b]
    sb = (after[0] - 1) if after else (total - 1)
    return sa, sb


def merge_ranges(rs: list[Range]) -> list[Range]:
    rs = sorted(rs, key=lambda r: r.a)
    out: list[Range] = []
    for r in rs:
        if out and r.a <= out[-1].b + 1:
            prev = out[-1]
            prev.b = max(prev.b, r.b)
            prev.cuts += r.cuts
            prev.wanted += r.wanted
        else:
            out.append(r)
    return out


# --------------------------------------------------------------------------- render


def remotion_render(comp: str, out: Path, public_dir: Path, frames: tuple[int, int] | None,
                    entry: str | None, concurrency: int | None, log: Path) -> None:
    # Windows: npx is npx.cmd and CreateProcess will not find bare "npx".
    npx = shutil.which("npx") or "npx"
    cmd = [npx, "remotion", "render"]
    if entry:
        cmd.append(entry)
    # The default work dir can land on another drive (TEMP is on E: here), and relpath
    # raises across mounts on Windows. Relative when it can be, absolute otherwise.
    def rel(p: Path) -> str:
        try:
            return os.path.relpath(p, REMOTION)
        except ValueError:
            return str(p)
    cmd += [comp, rel(out)]
    cmd.append(f"--public-dir={rel(public_dir)}")
    if frames:
        cmd.append(f"--frames={frames[0]}-{frames[1]}")
    if concurrency:
        cmd.append(f"--concurrency={concurrency}")
    t0 = time.time()
    r = run(cmd, cwd=REMOTION)
    log.write_text((r.stdout or "") + "\n--- stderr ---\n" + (r.stderr or ""), encoding="utf-8")
    if r.returncode != 0 or not out.is_file():
        print(f"[splice] remotion render failed (rc={r.returncode}); log: {log}", file=sys.stderr)
        print((r.stderr or r.stdout)[-3000:], file=sys.stderr)
        raise SystemExit(2)
    print(f"[splice]   rendered {out.name} in {time.time() - t0:.0f}s")


# --------------------------------------------------------------------------- verify


def verify_film_matches_master(film: dict, film_path: Path, master: Path, comp: str,
                               public_dir: Path, entry: str | None, fps: float,
                               samples: int, skip_cuts: set[int], work: Path,
                               min_psnr: float) -> list[dict]:
    """Render single frames from cuts that are NOT being replaced and compare them to the
    master at the same timecode. A rebuilt/edited film json fails this immediately."""
    cuts = film["cuts"]
    candidates = [i for i in range(len(cuts)) if i not in skip_cuts]
    if not candidates:
        return []
    picks = [candidates[int(round(k * (len(candidates) - 1) / max(1, samples - 1)))]
             for k in range(samples)] if samples > 1 else [candidates[len(candidates) // 2]]
    picks = sorted(set(picks))
    results = []
    for i in picks:
        a, b = cut_frame_span(film, cuts[i], fps)
        mid = a + (b - a) // 2
        probe = work / f"probe_{mid}.mp4"
        remotion_render(comp, probe, public_dir, (mid, mid), entry, None, work / f"probe_{mid}.log")
        db = psnr_window(master, probe, mid, 1, fps, seek_b=False)
        results.append({
            "cut_index": i, "cut_id": cuts[i].get("id"), "frame": mid,
            "src": cuts[i].get("src"), "psnr_db": None if math.isnan(db) else db,
            "pass": bool(db >= min_psnr),
        })
        state = "OK" if db >= min_psnr else "MISMATCH"
        print(f"[splice]   provenance frame {mid} ({cuts[i].get('id')}): PSNR {db:.2f} dB  {state}")
    return results


# --------------------------------------------------------------------------- main


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--slug", required=True, help="episode slug; picks remotion/src/data/<slug>_film.json")
    ap.add_argument("--film", help="override the film json path")
    ap.add_argument("--comp", required=True, help="Remotion composition id (e.g. Ep62Greene)")
    ap.add_argument("--entry", help="Remotion entry point (default: the repo root entry)")
    ap.add_argument("--master", required=True, help="the finished mp4 to repair")
    ap.add_argument("--out", required=True, help="where to write the repaired mp4")
    ap.add_argument("--public-dir", required=True, help="the public dir the master was rendered with")
    ap.add_argument("--replace", action="append", default=[], metavar="CUT=SRC",
                    help="cut id (or index) = new src, relative to the public dir. Repeatable.")
    ap.add_argument("--verify-only", action="store_true",
                    help="run the provenance probe and stop. Answers 'does this film json still "
                         "describe this master?' before anyone plans a repair.")
    ap.add_argument("--verify", type=int, default=2, metavar="N",
                    help="provenance probe frames from UNREPLACED cuts (0 disables; don't)")
    ap.add_argument("--min-psnr", type=float, default=36.0,
                    help="dB a provenance probe must reach against the master")
    ap.add_argument("--sample-untouched", type=int, default=4, metavar="N",
                    help="untouched windows to frame-hash old vs new after the splice")
    ap.add_argument("--window", type=int, default=12, help="frames per verification window")
    ap.add_argument("--concurrency", type=int, default=None)
    ap.add_argument("--receipt", help="receipt json path (default: runs/qc/<slug>_splice_receipt.json)")
    ap.add_argument("--work", help="scratch dir (default: a temp dir, deleted on success)")
    ap.add_argument("--keep-work", action="store_true")
    ap.add_argument("--allow-missing-src", action="store_true",
                    help="do not require the new src to exist under the public dir (fixtures only)")
    ap.add_argument("--dry-run", action="store_true", help="plan and frame budget only; write nothing")
    a = ap.parse_args()

    film_path = Path(a.film) if a.film else (REMOTION / "src" / "data" / f"{a.slug}_film.json")
    if not film_path.is_absolute():
        film_path = ROOT / film_path
    master = Path(a.master)
    master = master if master.is_absolute() else ROOT / master
    out = Path(a.out)
    out = out if out.is_absolute() else ROOT / out
    public_dir = Path(a.public_dir)
    public_dir = public_dir if public_dir.is_absolute() else ROOT / public_dir
    for p, what in ((film_path, "film json"), (master, "master"), (public_dir, "public dir")):
        if not p.exists():
            print(f"[splice] no such {what}: {p}", file=sys.stderr)
            return 1
    if not a.replace:
        print("[splice] nothing to do: pass at least one --replace CUT=SRC", file=sys.stderr)
        return 1

    original_bytes = film_path.read_bytes()
    film = json.loads(original_bytes.decode("utf-8"))
    fps = float(film.get("fps") or 30)

    minfo = probe_streams(master)
    mv = video_stream(minfo)
    m_fps = eval_fps(mv.get("r_frame_rate", "30/1"))
    if abs(m_fps - fps) > 1e-6:
        print(f"[splice] fps mismatch: film json {fps}, master {m_fps}", file=sys.stderr)
        return 1
    total = video_packet_count(master)
    print(f"[splice] master   {master.name}: {total} frames @ {fps:g} fps "
          f"({total / fps:.3f}s), {mv.get('codec_name')}/{mv.get('profile')}/L{mv.get('level')} "
          f"{mv.get('pix_fmt')} {mv.get('color_primaries')}/{mv.get('color_transfer')}/{mv.get('color_space')}")

    # ---- resolve the replacements -------------------------------------------------
    reps: list[Replacement] = []
    for spec in a.replace:
        if "=" not in spec:
            print(f"[splice] bad --replace {spec!r}; want CUT=SRC", file=sys.stderr)
            return 1
        key, new_src = spec.split("=", 1)
        idx, cut = find_cut(film, key.strip())
        new_src = new_src.strip().replace("\\", "/")
        if not (public_dir / new_src).is_file() and not a.allow_missing_src:
            print(f"[splice] replacement missing on disk: {public_dir / new_src}", file=sys.stderr)
            return 1
        fa, fb = cut_frame_span(film, cut, fps)
        if fb >= total:
            print(f"[splice] cut {cut.get('id')} ends at frame {fb}, past the master's {total}",
                  file=sys.stderr)
            return 1
        reps.append(Replacement(idx, cut.get("id", str(idx)), cut.get("src", ""), new_src,
                                cut["start"], cut["dur"], fa, fb))

    kfs = keyframe_frames(master, fps)
    print(f"[splice] keyframes {len(kfs)} (max GOP {max((y - x) for x, y in zip(kfs, kfs[1:])) if len(kfs) > 1 else total} frames)")

    ranges = []
    for r in reps:
        sa, sb = snap_to_gop(r.frame_a, r.frame_b, kfs, total)
        ranges.append(Range(sa, sb, [r.cut_id], [(r.frame_a, r.frame_b)]))
    ranges = merge_ranges(ranges)
    budget = sum(r.n for r in ranges)
    print(f"[splice] {len(reps)} cut(s) -> {len(ranges)} re-render range(s), "
          f"{budget} frames ({budget / fps:.1f}s) of {total} ({total / fps:.1f}s) = "
          f"{100 * budget / total:.1f}% of a full render")
    for r in ranges:
        want = ", ".join(f"{x}-{y}" for x, y in r.wanted)
        print(f"[splice]   frames {r.a}-{r.b} ({r.n}f, {r.a / fps:.2f}s-{(r.b + 1) / fps:.2f}s) "
              f"covering {', '.join(r.cuts)} [cut spans {want}]")
    for r in reps:
        print(f"[splice]   {r.cut_id} @ {r.start_s:.3f}s +{r.dur_s:.3f}s: "
              f"{Path(r.old_src).name} -> {Path(r.new_src).name}")

    if a.dry_run:
        print("[splice] --dry-run: nothing written")
        return 0

    work = Path(a.work) if a.work else Path(tempfile.mkdtemp(prefix=f"splice_{a.slug}_"))
    work.mkdir(parents=True, exist_ok=True)
    print(f"[splice] work dir {work}")

    receipt: dict = {
        "schema_version": "1.0.0",
        "tool": "scripts/pd_splice_cuts.py",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "slug": a.slug, "composition": a.comp,
        "film": str(film_path.relative_to(ROOT)),
        "master_in": str(master.relative_to(ROOT)) if master.is_relative_to(ROOT) else str(master),
        "master_out": str(out.relative_to(ROOT)) if out.is_relative_to(ROOT) else str(out),
        "fps": fps, "frames_total": total,
        "frames_rerendered": budget,
        "fraction_of_full_render": round(budget / total, 6),
        "replacements": [], "ranges": [], "verification": {},
    }

    film_backup = film_path.with_suffix(film_path.suffix + f".pre_splice_{time.strftime('%Y%m%d_%H%M%S')}.bak")

    try:
        # ---- provenance: does this json actually describe this master? -------------
        if a.verify > 0:
            print("[splice] provenance probe (unreplaced cuts, rendered fresh vs the master)")
            probes = verify_film_matches_master(
                film, film_path, master, a.comp, public_dir, a.entry, fps, a.verify,
                {r.cut_index for r in reps}, work, a.min_psnr)
            receipt["verification"]["provenance_probes"] = probes
            if a.verify_only:
                ok = bool(probes) and all(p["pass"] for p in probes)
                print(f"[splice] provenance {'OK -- this json reproduces this master' if ok else 'MISMATCH -- this json does NOT reproduce this master'}")
                return 0 if ok else 3
            if not probes or not all(p["pass"] for p in probes):
                print("[splice] ABORT: the film json does not reproduce this master. Nothing was "
                      "written. The json has been rebuilt or edited since the render; splice "
                      "against the json the master came from, or re-render.", file=sys.stderr)
                return 3
        else:
            receipt["verification"]["provenance_probes"] = "skipped (--verify 0)"

        # ---- edit the film json, those cuts only -----------------------------------
        before = json.loads(original_bytes.decode("utf-8"))
        film_backup.write_bytes(original_bytes)
        for r in reps:
            c = film["cuts"][r.cut_index]
            c["src"] = r.new_src
            secs = source_seconds(public_dir, r.new_src)
            if secs is not None:
                c["srcSeconds"] = secs
                if c["dur"] > secs + 0.05:
                    c["loopSource"] = True
                else:
                    c.pop("loopSource", None)
            receipt["replacements"].append({
                "cut_index": r.cut_index, "cut_id": r.cut_id,
                "start_s": r.start_s, "dur_s": r.dur_s,
                "frames": [r.frame_a, r.frame_b],
                "old_src": r.old_src, "new_src": r.new_src,
                "new_src_seconds": secs, "loop_source": bool(c.get("loopSource")),
            })
        drift = structural_diff(before, film, {r.cut_index for r in reps})
        if drift:
            print("[splice] ABORT: the edit touched more than the named cuts:", file=sys.stderr)
            for d in drift[:20]:
                print("   " + d, file=sys.stderr)
            return 4
        film_path.write_text(json.dumps(film, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        json.loads(film_path.read_text(encoding="utf-8"))  # it must still parse
        for r in reps:
            chk = run([sys.executable, str(ROOT / "scripts" / "pd_edit.py"),
                       "--file", str(film_path), "--show", f'"src": "{r.new_src}"'])
            if chk.returncode != 0:
                print(f"[splice] ABORT: {r.new_src} not present after the write", file=sys.stderr)
                film_path.write_bytes(original_bytes)
                return 4
        print(f"[splice] film json edited in place ({len(reps)} cut(s)); backup {film_backup.name}")

        # ---- re-render only the affected ranges ------------------------------------
        seg_new: dict[int, Path] = {}
        for i, r in enumerate(ranges):
            mp4 = work / f"new_{i:02d}.mp4"
            print(f"[splice] rendering frames {r.a}-{r.b} ({r.n}f)")
            remotion_render(a.comp, mp4, public_dir, (r.a, r.b), a.entry, a.concurrency,
                            work / f"new_{i:02d}.log")
            got = video_packet_count(mp4)
            if got != r.n:
                print(f"[splice] ABORT: range {r.a}-{r.b} rendered {got} frames, expected {r.n}",
                      file=sys.stderr)
                return 5
            fp_new, fp_old = encoder_fingerprint(probe_streams(mp4)), encoder_fingerprint(minfo)
            diffs = {k: (fp_old[k], fp_new[k]) for k in fp_old if fp_old[k] != fp_new[k]}
            if diffs:
                print(f"[splice] ABORT: encoder settings differ from the master: {diffs}",
                      file=sys.stderr)
                return 5
            seg_new[i] = mp4
        receipt["ranges"] = [{"a": r.a, "b": r.b, "frames": r.n, "cuts": r.cuts,
                              "seconds": [round(r.a / fps, 3), round((r.b + 1) / fps, 3)]}
                             for r in ranges]

        # ---- cut the keep-segments out of the master, no decode --------------------
        splits = sorted(({r.a for r in ranges} | {r.b + 1 for r in ranges}) - {0, total})
        splits = [s for s in splits if 0 < s < total]
        seg_dir = work / "seg"
        seg_dir.mkdir(exist_ok=True)
        must(["ffmpeg", "-v", "error", "-y", "-i", str(master), "-map", "0:v:0", "-c", "copy",
              "-bsf:v", "h264_mp4toannexb", "-f", "segment", "-segment_format", "mpegts",
              "-segment_frames", ",".join(str(s) for s in splits), "-reset_timestamps", "1",
              str(seg_dir / "keep_%03d.ts")], "segment the master at its keyframes")
        segs = sorted(seg_dir.glob("keep_*.ts"))
        bounds = [0] + splits + [total]
        expect = [bounds[i + 1] - bounds[i] for i in range(len(bounds) - 1)]
        if len(segs) != len(expect):
            print(f"[splice] ABORT: segmenter produced {len(segs)} pieces, expected {len(expect)}",
                  file=sys.stderr)
            return 6
        counts = [video_packet_count(s) for s in segs]
        if counts != expect:
            print(f"[splice] ABORT: segment frame counts {counts} != expected {expect}",
                  file=sys.stderr)
            return 6
        print(f"[splice] master split into {len(segs)} piece(s): {counts} frames (sum {sum(counts)})")

        # ---- swap in the fresh ranges, join as TS ----------------------------------
        replaced_seg_index = {}
        for i, r in enumerate(ranges):
            replaced_seg_index[bounds.index(r.a)] = i
        pieces: list[Path] = []
        for si, seg in enumerate(segs):
            if si in replaced_seg_index:
                src_mp4 = seg_new[replaced_seg_index[si]]
                ts = work / f"new_{replaced_seg_index[si]:02d}.ts"
                must(["ffmpeg", "-v", "error", "-y", "-i", str(src_mp4), "-map", "0:v:0",
                      "-c", "copy", "-bsf:v", "h264_mp4toannexb", "-f", "mpegts", str(ts)],
                     "annexb the re-rendered range")
                pieces.append(ts)
            else:
                pieces.append(seg)
        joined = work / "joined.mp4"
        must(["ffmpeg", "-v", "error", "-y", "-fflags", "+genpts",
              "-i", "concat:" + "|".join(str(p) for p in pieces),
              "-map", "0:v:0", "-c", "copy", "-r", f"{fps:g}",
              "-video_track_timescale", str(int(mv.get("time_base", "1/90000").split("/")[1])),
              "-muxpreload", "0", "-muxdelay", "0", str(joined)], "join the pieces")

        # ---- reattach the ORIGINAL audio, copied ------------------------------------
        out.parent.mkdir(parents=True, exist_ok=True)
        # The mpegts round trip drops the mp4 `colr` box (the H.264 VUI keeps the matrix but
        # ffprobe reads primaries/transfer from the container), so the master's colour tags are
        # read off the master and written back explicitly. Checked by the encoder comparison
        # below, which is what caught this.
        colour = []
        for opt, key in (("-color_primaries", "color_primaries"), ("-color_trc", "color_transfer"),
                         ("-colorspace", "color_space"), ("-color_range", "color_range")):
            if mv.get(key):
                colour += [opt, mv[key]]
        must(["ffmpeg", "-v", "error", "-y", "-i", str(joined), "-i", str(master),
              "-map", "0:v:0", "-map", "1:a:0", "-c", "copy", *colour,
              "-movflags", "+faststart", str(out)], "mux with the original audio")

        # ---- prove it ---------------------------------------------------------------
        print("[splice] verifying")
        v: dict = {}
        oinfo = probe_streams(out)
        n_out = video_packet_count(out)
        v["frames"] = {"master": total, "spliced": n_out, "equal": n_out == total}
        d_old, d_new = float(minfo["format"]["duration"]), float(oinfo["format"]["duration"])
        v["duration_s"] = {"master": d_old, "spliced": d_new,
                           "delta_s": round(d_new - d_old, 6),
                           "within_one_frame": abs(d_new - d_old) < 1.0 / fps}
        am_old, am_new = audio_stream_md5(master), audio_stream_md5(out)
        v["audio_stream_md5"] = {"master": am_old, "spliced": am_new, "identical": am_old == am_new}
        fp_old, fp_new = encoder_fingerprint(minfo), encoder_fingerprint(oinfo)
        v["encoder"] = {"master": fp_old, "spliced": fp_new, "identical": fp_old == fp_new}

        # constant frame delta -> nothing dropped or duplicated at a seam
        # Packets come out in DECODE order and this file has B-frames, so raw deltas run
        # -2,-1,+3,+5 in a perfectly good stream; the first version of this check failed on
        # that. Sort into presentation order first, then every gap must be exactly one frame.
        def pts_list(p: Path) -> list[float]:
            rr = must(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                       "packet=pts_time", "-of", "csv=p=0", str(p)], "pts scan")
            return sorted(float(x) for x in rr.stdout.split() if x)
        pts_new, pts_old = pts_list(out), pts_list(master)
        deltas = {round((y - x) * fps, 3) for x, y in zip(pts_new, pts_new[1:])}
        v["pts_continuity"] = {
            "distinct_frame_deltas": sorted(deltas),
            "uniform": deltas == {1.0},
            "presentation_times_match_master": pts_new == pts_old,
        }

        touched = [(rr.a, rr.b) for rr in ranges]

        def untouched(f0: int, f1: int) -> bool:
            return all(f1 < x or f0 > y for x, y in touched)

        # Both sides of every seam are mandatory: a dropped or duplicated frame at a splice
        # point shows up there and nowhere else. The rest are spread over the file.
        seams = []
        for rr in ranges:
            if rr.a - a.window >= 0 and untouched(rr.a - a.window, rr.a - 1):
                seams.append(rr.a - a.window)
            if rr.b + a.window < total and untouched(rr.b + 1, rr.b + a.window):
                seams.append(rr.b + 1)
        spread = []
        for j in range(1, a.sample_untouched + 1):
            k = min(total - a.window - 1, max(0, (j * total) // (a.sample_untouched + 1)))
            if untouched(k, k + a.window - 1) and k not in seams:
                spread.append(k)
        windows = sorted(set(seams + spread))
        same = []
        for w in windows:
            h_old, n1 = framemd5_window(master, w, a.window, fps)
            h_new, n2 = framemd5_window(out, w, a.window, fps)
            same.append({"start_frame": w, "frames": a.window, "master_md5": h_old,
                         "spliced_md5": h_new, "identical": h_old == h_new and n1 == n2})
            print(f"[splice]   untouched frames {w}-{w + a.window - 1}: "
                  f"{'IDENTICAL' if h_old == h_new else 'DIFFERENT'} ({h_old[:12]})")
        v["untouched_decoded_frames"] = same

        # the GOP padding: re-encoded, so not bit-identical -- report how close
        pads = []
        for rr in ranges:
            for f0, f1 in ((rr.a, min(rr.wanted, key=lambda t: t[0])[0] - 1),
                           (max(rr.wanted, key=lambda t: t[1])[1] + 1, rr.b)):
                if f1 - f0 + 1 >= 2:
                    n = min(a.window, f1 - f0 + 1)
                    pads.append({"frames": [f0, f1], "sampled": n,
                                 "psnr_db": psnr_window(master, out, f0, n, fps)})
        v["gop_padding_psnr"] = pads
        for p in pads:
            print(f"[splice]   GOP padding {p['frames'][0]}-{p['frames'][1]}: "
                  f"PSNR {p['psnr_db']:.2f} dB vs the master (re-encoded, same picture)")

        v["replaced_regions_differ"] = []
        for rr in ranges:
            for f0, f1 in rr.wanted:
                n = min(a.window, f1 - f0 + 1)
                h_old, _ = framemd5_window(master, f0, n, fps)
                h_new, _ = framemd5_window(out, f0, n, fps)
                v["replaced_regions_differ"].append(
                    {"frames": [f0, f1], "master_md5": h_old, "spliced_md5": h_new,
                     "changed": h_old != h_new})

        receipt["verification"].update(v)
        receipt["sha256"] = {"master_in": sha256_of(master), "master_out": sha256_of(out)}
        receipt["film_json_backup"] = str(film_backup.relative_to(ROOT))

        hard = [
            ("frame count unchanged", v["frames"]["equal"]),
            ("duration unchanged", v["duration_s"]["within_one_frame"]),
            ("audio stream bit-identical", v["audio_stream_md5"]["identical"]),
            ("encoder settings match", v["encoder"]["identical"]),
            ("no dropped/duplicated frames", v["pts_continuity"]["uniform"]
             and v["pts_continuity"]["presentation_times_match_master"]),
            ("untouched regions identical", all(s["identical"] for s in same) and bool(same)),
            ("replaced regions changed", all(x["changed"] for x in v["replaced_regions_differ"])),
        ]
        receipt["verdict"] = "PASS" if all(ok for _, ok in hard) else "FAIL"
        receipt["checks"] = [{"check": n, "pass": bool(ok)} for n, ok in hard]

        rp = Path(a.receipt) if a.receipt else (ROOT / "runs" / "qc" / f"{a.slug}_splice_receipt.json")
        rp = rp if rp.is_absolute() else ROOT / rp
        rp.parent.mkdir(parents=True, exist_ok=True)
        rp.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        print()
        for n, ok in hard:
            print(f"  [{'PASS' if ok else 'FAIL'}] {n}")
        print(f"\n[splice] {receipt['verdict']}  {out}")
        print(f"[splice] sha256 in  {receipt['sha256']['master_in']}")
        print(f"[splice] sha256 out {receipt['sha256']['master_out']}")
        print(f"[splice] receipt {rp}")
        print("[splice] whole-file gates (loudness, animation_density, motion_energy, "
              "footage_diversity) and the acceptance receipt still bind to the new sha -- re-run them.")
        return 0 if receipt["verdict"] == "PASS" else 7
    finally:
        if not a.keep_work and not a.work and work.exists():
            shutil.rmtree(work, ignore_errors=True)


def eval_fps(rate: str) -> float:
    if "/" in rate:
        n, d = rate.split("/")
        return float(n) / float(d)
    return float(rate)


def structural_diff(before: dict, after: dict, allowed_cut_indexes: set[int]) -> list[str]:
    """Everything except the named cuts' src/srcSeconds/loopSource must be untouched."""
    out: list[str] = []
    keys = set(before) | set(after)
    for k in sorted(keys - {"cuts"}):
        if before.get(k) != after.get(k):
            out.append(f"top-level key {k!r} changed")
    bc, ac = before.get("cuts", []), after.get("cuts", [])
    if len(bc) != len(ac):
        out.append(f"cut count {len(bc)} -> {len(ac)}")
        return out
    mutable = {"src", "srcSeconds", "loopSource"}
    for i, (b, c) in enumerate(zip(bc, ac)):
        for k in sorted(set(b) | set(c)):
            if b.get(k) == c.get(k):
                continue
            if i in allowed_cut_indexes and k in mutable:
                continue
            out.append(f"cut[{i}] ({b.get('id')}) field {k!r}: {b.get(k)!r} -> {c.get(k)!r}")
    return out


if __name__ == "__main__":
    raise SystemExit(main())
