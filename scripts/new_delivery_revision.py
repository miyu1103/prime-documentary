#!/usr/bin/env python
"""Point final_delivery at a re-rendered master, as a NEW revision.

`upload_schedule_case_v001.py` refuses when the video's sha256 does not match the canonical
sha in `09_package/final_delivery.v*.json`. After a re-render it never does, and the fix is not
to edit v001: that file records which bytes went up the first time, and it is the only evidence
of what the public would have seen. `.claude/rules/05-episode-artifacts.md` -- approved
artefacts are immutable, a semantic change makes a new revision.

    py -3.11 scripts/new_delivery_revision.py --slug fieldtest

Every field is MEASURED off the new file (sha256, duration, bytes, codecs, fps) rather than
copied forward, so an error in the previous revision cannot propagate. Only `captions` and
`thumbnail` carry over, because those really are the same artefacts.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 22), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--render", help="explicit master path; avoids lexicographic revision selection")
    ap.add_argument("--reason", default="")
    a = ap.parse_args()

    eps = sorted((ROOT / "episodes").glob(f"PD-*-{a.slug}"))
    if not eps:
        raise SystemExit(f"no episode directory for {a.slug}")
    ep = eps[0]
    pkg = ep / "09_package"

    if a.render:
        master = Path(a.render)
        if not master.is_absolute():
            master = ROOT / master
        master = master.resolve()
        edit_dir = (ep / "08_edit").resolve()
        if master.parent != edit_dir or not master.is_file():
            raise SystemExit(f"--render must be an existing master directly under {edit_dir}: {master}")
    else:
        masters = sorted((ep / "08_edit").glob(f"{a.slug}_final_bgm.v*.mp4"))
        if not masters:
            raise SystemExit(f"no master under {ep / '08_edit'}")
        master = masters[-1]

    prev = sorted(pkg.glob("final_delivery.v*.json"))
    if not prev:
        raise SystemExit(f"no existing final_delivery under {pkg} -- nothing to supersede")
    old = json.loads(prev[-1].read_text(encoding="utf-8"))
    old_sha = str(old.get("canonical_final", {}).get("video_sha256", ""))

    sha = sha256(master)
    if old_sha.endswith(sha):
        print(f"[delivery] {prev[-1].name} already names this master ({sha[:16]}) -- nothing to do")
        return 0

    probe = json.loads(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries",
         "format=duration,size:stream=codec_name,width,height,r_frame_rate,sample_rate,channels",
         "-of", "json", str(master)], capture_output=True, text=True, check=True).stdout)
    fmt = probe["format"]
    v = next(s for s in probe["streams"] if s.get("width"))
    aud = next(s for s in probe["streams"] if s.get("sample_rate"))
    num, den = (int(x) for x in v["r_frame_rate"].split("/"))
    fps = num / den
    fps_s = str(int(fps)) if float(fps).is_integer() else str(round(fps, 3))

    n = 2
    while (pkg / f"final_delivery.v{n:03d}.json").exists():
        n += 1
    out_path = pkg / f"final_delivery.v{n:03d}.json"

    out = {
        "schema_version": "1.0.0",
        "episode_id": ep.name,
        "revision": f"v{n:03d}",
        "supersedes": prev[-1].name,
        "supersedes_reason": a.reason or (
            f"{prev[-1].name} names a render that is no longer the master. This revision names "
            f"the current one; the previous file is kept as the record of what those bytes were."),
        "canonical_final": {
            "path": master.relative_to(ROOT).as_posix(),
            "video_sha256": f"sha256:{sha}",
            "duration_seconds": round(float(fmt["duration"]), 3),
            "bytes": int(fmt["size"]),
            "container": "mp4",
            "video": f"{v['codec_name']} {v['width']}x{v['height']} {fps_s}fps",
            "audio": f"{aud['codec_name']} 320k {int(aud['sample_rate']) // 1000}kHz "
                     f"{'stereo' if aud['channels'] == 2 else str(aud['channels']) + 'ch'}, "
                     f"-14 LUFS",
        },
        "captions": old.get("captions"),
        "thumbnail": old.get("thumbnail"),
    }
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    json.loads(out_path.read_text(encoding="utf-8"))

    print(f"[delivery] wrote {out_path.name}")
    print(f"  sha   {sha[:16]}   (previous named {old_sha[7:23]})")
    print(f"  dur   {out['canonical_final']['duration_seconds']}s   "
          f"bytes {out['canonical_final']['bytes']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
