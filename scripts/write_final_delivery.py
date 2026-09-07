#!/usr/bin/env python3
"""Write 09_package/final_delivery.v*.json for a finished episode.

The uploader refuses to schedule without this record, and until now every episode that had one got
it from a bespoke per-episode script (build_ep19_varsityblues_final.py, build_ep20_gardner_final.py,
and so on). EP62-65 had none, so the first scheduling attempt died on `missing final_delivery`.

The record names which file was delivered. That matters beyond the uploader: check_shipped_frames
reads it to decide which master to measure, after an older revision with a higher version number
beat the live one on willingham and three burned-in name tags from a dead render were nearly
reported against the current film.

Everything here is measured from the file, not copied from anywhere:

    py -3.11 scripts/write_final_delivery.py --slug marmet
    py -3.11 scripts/write_final_delivery.py --slug marmet --render path/to.mp4

Integrated loudness is read from the episode's newest acceptance receipt when one exists (the gate
already measured it over the whole film); it is omitted rather than guessed when it does not.
"""
from __future__ import annotations

import argparse
import glob
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:  # noqa: BLE001
    pass

ROOT = Path(__file__).resolve().parents[1]


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def probe(p: Path) -> dict:
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_format", "-show_streams", "-of", "json", str(p)],
        capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"ffprobe failed on {p}: {r.stderr.strip()[:200]}")
    return json.loads(r.stdout)


def resolve_episode(slug: str) -> Path:
    hits = [Path(p) for p in glob.glob(str(ROOT / "episodes" / f"PD-*-{slug}")) if Path(p).is_dir()]
    if len(hits) != 1:
        raise SystemExit(f"could not resolve episode for slug {slug!r}: {[h.name for h in hits]}")
    return hits[0]


def loudness_from_receipt(epdir: Path) -> str | None:
    """The integrated LUFS the acceptance gate already measured, or None.

    Measuring it again here would mean a second full pass over a half-hour file for a number the
    gate has already produced; inventing a plausible one would be worse than leaving it out.
    """
    recs = sorted((epdir / "09_package").glob("acceptance_receipt.v*.json"))
    for rec in reversed(recs):
        try:
            d = json.loads(rec.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            continue
        results = d.get("results") or d.get("checks") or []
        if isinstance(results, dict):
            results = [{"check": k, **(v if isinstance(v, dict) else {})}
                       for k, v in results.items()]
        for c in results:
            if isinstance(c, dict) and c.get("check") == "loudness":
                m = re.search(r"(-?\d+\.\d+)\s*LUFS", str(c.get("reason", "")))
                if m:
                    return f"{m.group(1)} LUFS integrated (measured by check_final_acceptance)"
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--render", help="explicit master; default is the newest <slug>_final_bgm.v*.mp4")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    epdir = resolve_episode(a.slug)
    if a.render:
        master = Path(a.render).resolve()
    else:
        # newest by mtime, NOT by revision number: on willingham a v002 from four days earlier
        # outranked the live v001 and the wrong file was measured.
        cands = sorted((epdir / "08_edit").glob(f"{a.slug}_final_bgm.v*.mp4"),
                       key=lambda p: p.stat().st_mtime)
        if not cands:
            raise SystemExit(f"no {a.slug}_final_bgm.v*.mp4 in {epdir / '08_edit'}")
        master = cands[-1]
        if len(cands) > 1:
            print(f"!! {len(cands)} master revisions present; taking the NEWEST by mtime:")
            for c in cands:
                print(f"     {c.name}  {c.stat().st_mtime:.0f}"
                      + ("   <- chosen" if c == master else ""))
    if not master.is_file():
        raise SystemExit(f"master not found: {master}")

    info = probe(master)
    v = next((s for s in info["streams"] if s.get("codec_type") == "video"), {})
    aud = next((s for s in info["streams"] if s.get("codec_type") == "audio"), {})
    fmt = info.get("format", {})

    def fps(s: dict) -> str:
        rate = s.get("avg_frame_rate") or "0/1"
        try:
            n, d = (int(x) for x in rate.split("/"))
            return f"{n / d:g}fps" if d else "?fps"
        except Exception:  # noqa: BLE001
            return "?fps"

    caps = sorted((epdir / "08_edit").glob("captions.final.v*.srt"))
    thumbs = sorted((epdir / "09_package").glob("thumbnail.selected.v*.png"))
    rec = {
        "schema_version": "1.0.0",
        "episode_id": epdir.name,
        "revision": "v001",
        "canonical_final": {
            "path": master.relative_to(ROOT).as_posix(),
            "video_sha256": sha256(master),
            "duration_seconds": round(float(fmt.get("duration", 0.0)), 1),
            "bytes": int(fmt.get("size", master.stat().st_size)),
            "container": (fmt.get("format_name") or "").split(",")[0],
            "video": (f"{v.get('codec_name', '?')} {v.get('width', '?')}x{v.get('height', '?')} "
                      f"{fps(v)} ({int(v.get('bit_rate', 0)):,} bps)" if v.get("bit_rate")
                      else f"{v.get('codec_name', '?')} {v.get('width', '?')}x{v.get('height', '?')} {fps(v)}"),
            "audio": (f"{aud.get('codec_name', '?')} {aud.get('sample_rate', '?')}Hz "
                      f"{aud.get('channel_layout', '?')}"),
        },
        "captions": caps[-1].relative_to(ROOT).as_posix() if caps else None,
        "thumbnail": thumbs[-1].relative_to(ROOT).as_posix() if thumbs else None,
    }
    lo = loudness_from_receipt(epdir)
    if lo:
        rec["canonical_final"]["loudness"] = lo

    pkg = epdir / "09_package"
    n = 1
    while (pkg / f"final_delivery.v{n:03d}.json").exists():
        n += 1
    rec["revision"] = f"v{n:03d}"
    out = pkg / f"final_delivery.v{n:03d}.json"

    if a.dry_run:
        print(json.dumps(rec, ensure_ascii=False, indent=1))
        print(f"DRY_RUN would write {out.relative_to(ROOT)}")
        return 0
    pkg.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(rec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)}")
    print(f"  {rec['canonical_final']['path']}")
    print(f"  {rec['canonical_final']['duration_seconds']}s  "
          f"{rec['canonical_final']['bytes'] / 1e6:.0f}MB  "
          f"{rec['canonical_final']['video_sha256'][:23]}..")
    if not caps:
        print("  !! no captions.final.v*.srt found")
    if not thumbs:
        print("  !! no thumbnail.selected.v*.png found")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
