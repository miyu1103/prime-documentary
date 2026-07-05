#!/usr/bin/env python3
r"""Bind the 4-layer sound mix to the case-film video render (the MISSING WIRE).

WHY THIS FILE EXISTS
--------------------
``scripts/build_case_film_audio.py`` builds the REAL narration-timed 4-layer mix
(a WAV) and an ``audio_provenance.v*.json`` that records the mix ``sha256`` plus a
``mux.command_template``. But nothing ever executed that template: an independent
review flagged that the rich mix is *never actually muxed into the shipped file*
-- the acceptance gate's ``check_sound_layers`` could still pass on a lone music
bed while the built 4-layer WAV sat orphaned on the SSD.

This tool closes the loop between the two ends:

    build_case_film_audio  (mix WAV + provenance sha)
        -> build_case_film_mux  (mux the WAV as SOLE audio + STAMP the sha)   <-- THIS FILE
            -> check_final_acceptance  (reads provenance + the stamped tag)

WHAT IT DOES
------------
1. RESOLVE the built mix WAV from the episode's ``audio_provenance`` (its
   ``mix.render_audio_copy`` / ``mix.wav_path_expected``) or from ``--audio``.
   If the WAV does not exist it FAILS with the exact command to build it first --
   it never silently ships a video-only (music-thin / orphaned-mix) deliverable.

2. MUX that WAV as the render's SOLE audio track (only ``1:a:0`` is mapped, so the
   video's own audio, if any, is dropped):

       ffmpeg -y -i <video> -i <mix.wav> -map 0:v:0 -map 1:a:0 \
           -c:v copy -c:a aac -b:a 320k -ar 48000 -ac 2 \
           -metadata audio_mix_sha256=<sha> -metadata comment=<...> \
           -movflags +faststart+use_metadata_tags -shortest <out.mp4>

   Audio settings (aac / 320k / 48000 / faststart) match the project's canonical
   final builders (e.g. ``scripts/build_ep29_hinton_final.py``) and the
   provenance ``mux.command_template``.

3. STAMP the mix ``sha256`` into the OUTPUT container as the format-level metadata
   tag ``audio_mix_sha256`` (plus a human ``comment``). The sha is taken from the
   provenance ``mix.sha256`` (authoritative); if provenance has not recorded it
   yet it falls back to hashing the resolved WAV. The ship gate can then read
   ``format_tags.audio_mix_sha256`` off the render and confirm it equals the mix
   sha in ``audio_provenance`` -- i.e. THIS mix reached THIS render.

4. EMIT an immutable, versioned mux receipt
   (``episodes/<ep>/06_audio/mux_receipt.v{NNN}.json``) recording the input video
   sha, mix sha, output sha, the exact ffmpeg command, and the stamped tag. The
   output is written next to the render as ``<slug>_film.muxed.v{NNN}.mp4``.
   Nothing approved is overwritten (CLAUDE invariant 6): a fresh version is
   allocated. Content carries NO wall-clock so the receipt is deterministic.

IDEMPOTENCY / SAFETY
--------------------
No network, no paid API, no GPU. If a prior receipt already muxed the SAME input
video sha + mix sha and its output still exists, this tool SHORT-CIRCUITS and
reports that output instead of re-encoding. ``--dry-run`` prints the resolved
paths + ffmpeg command and writes NOTHING (used now because the EP32 video render
does not exist yet). Atomic writes (temp + rename). Windows paths via pathlib.

SELF-TEST (dry-run on EP32):
    ./.venv/Scripts/python.exe scripts/build_case_film_mux.py \
        --ep PD-2026-032-carsearch --video H:\pd-media\episodes\PD-2026-032-carsearch\08_edit\case_film.v001.mp4 --dry-run
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parents[1]

SCHEMA_VERSION = "1.0.0"
GENERATOR = "scripts/build_case_film_mux.py"
MIX_SHA_TAG = "audio_mix_sha256"

# canonical audio settings (match build_ep29_hinton_final.py + provenance mux.command_template)
AAC_BITRATE = "320k"
SAMPLE_RATE = "48000"
CHANNELS = "2"


# ============================================================================
# helpers
# ============================================================================
def sha256_file(path: Path) -> Optional[str]:
    """Streaming SHA-256 of a file, or None if it does not exist."""
    if not path.exists():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def rel(path: Path) -> str:
    """Repo-relative POSIX-ish string when inside ROOT, else the absolute path.

    Logical/repo-relative for in-repo artifacts (rule 14); SSD media stays absolute.
    """
    try:
        if path.is_relative_to(ROOT):
            return str(path.relative_to(ROOT))
    except (ValueError, OSError):
        pass
    return str(path)


def quote_arg(a: str) -> str:
    """Shell-ish display quoting for the emitted command (display only, never exec)."""
    if a == "" or re.search(r"[\s\\]", a):
        return '"' + a.replace('"', r"\"") + '"'
    return a


def find_provenance(ep_dir: Path, override: Optional[str]) -> Path:
    if override:
        return Path(override)
    audio_dir = ep_dir / "06_audio"
    cands = sorted(audio_dir.glob("audio_provenance.v*.json"))
    if not cands:
        raise SystemExit(
            f"ERROR: no audio_provenance.v*.json under {audio_dir}. "
            f"Build the mix first: ./.venv/Scripts/python.exe scripts/build_case_film_audio.py "
            f"--ep {ep_dir.name} --render")
    return cands[-1]


def next_version(ep_audio_dir: Path, video_dir: Path, slug: str) -> int:
    """Lowest v{NNN} free for BOTH the receipt and the muxed output (no overwrite)."""
    used = {0}
    for p in ep_audio_dir.glob("mux_receipt.v*.json"):
        m = re.search(r"\.v(\d+)\.json$", p.name)
        if m:
            used.add(int(m.group(1)))
    for p in video_dir.glob(f"{slug}_film.muxed.v*.mp4"):
        m = re.search(r"\.muxed\.v(\d+)\.mp4$", p.name)
        if m:
            used.add(int(m.group(1)))
    return max(used) + 1


def probe_format_tag(path: Path, tag: str) -> Optional[str]:
    """Read one format-level metadata tag off a container, or None."""
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", f"format_tags={tag}",
             "-of", "json", str(path)],
            capture_output=True, text=True, check=False)
        data = json.loads(out.stdout or "{}")
        return (data.get("format", {}) or {}).get("tags", {}).get(tag)
    except Exception:
        return None


def find_prior_mux(ep_audio_dir: Path, video_sha: Optional[str], mix_sha: Optional[str]) -> Optional[dict]:
    """Idempotency: a prior receipt that muxed the SAME video sha + mix sha AND whose
    output file still exists. Returns that receipt dict, else None."""
    if not video_sha or not mix_sha:
        return None
    for p in sorted(ep_audio_dir.glob("mux_receipt.v*.json"), reverse=True):
        try:
            rec = json.loads(p.read_text("utf-8"))
        except Exception:
            continue
        same = (rec.get("input_video", {}).get("sha256") == video_sha
                and rec.get("mix_audio", {}).get("sha256_stamped") == mix_sha)
        out_path = rec.get("output", {}).get("path")
        if same and out_path and Path(out_path).exists():
            return rec
    return None


# ============================================================================
# main
# ============================================================================
def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    ap = argparse.ArgumentParser(
        description="Mux the 4-layer audio mix onto the case-film render as its SOLE audio, "
                    "stamp the mix sha, and emit an immutable mux receipt.")
    ap.add_argument("--ep", required=True, help="episode slug, e.g. PD-2026-032-carsearch")
    ap.add_argument("--video", required=True, help="the case-film video render (.mp4)")
    ap.add_argument("--audio", help="mix WAV (default: resolved from audio_provenance)")
    ap.add_argument("--provenance", help="audio_provenance JSON (default: latest audio_provenance.v*.json)")
    ap.add_argument("--dry-run", action="store_true",
                    help="print resolved paths + ffmpeg command; write nothing, run no ffmpeg")
    args = ap.parse_args()

    ep = args.ep
    ep_dir = ROOT / "episodes" / ep
    if not ep_dir.is_dir():
        print(f"ERROR: episode dir not found: {ep_dir}", file=sys.stderr)
        return 2

    prov_path = find_provenance(ep_dir, args.provenance)
    if not prov_path.exists():
        print(f"ERROR: provenance not found: {prov_path}", file=sys.stderr)
        return 2
    provenance = json.loads(prov_path.read_text("utf-8"))
    prov_sha = sha256_text(prov_path.read_text("utf-8"))
    mix_block = provenance.get("mix", {}) or {}

    # ---- resolve the mix WAV -------------------------------------------------
    #   --audio > provenance render_audio_copy > provenance wav_path_expected
    if args.audio:
        audio_path = Path(args.audio)
        audio_source = "--audio"
    elif mix_block.get("render_audio_copy"):
        audio_path = Path(mix_block["render_audio_copy"])
        audio_source = "provenance.mix.render_audio_copy"
    elif mix_block.get("wav_path_expected"):
        audio_path = Path(mix_block["wav_path_expected"])
        audio_source = "provenance.mix.wav_path_expected"
    else:
        print("ERROR: provenance has no mix.render_audio_copy / mix.wav_path_expected "
              "and no --audio was given.", file=sys.stderr)
        return 2
    audio_exists = audio_path.exists()

    # ---- the sha we STAMP: provenance mix.sha256 (authoritative), else the WAV --
    prov_mix_sha = mix_block.get("sha256")
    file_mix_sha = sha256_file(audio_path) if audio_exists else None
    stamp_sha = prov_mix_sha or file_mix_sha

    # integrity: if both known, they MUST match (the WAV on disk == what provenance describes)
    if prov_mix_sha and file_mix_sha and prov_mix_sha != file_mix_sha:
        print("ERROR: mix WAV sha does not match provenance mix.sha256 --\n"
              f"       provenance: {prov_mix_sha}\n"
              f"       on disk   : {file_mix_sha}\n"
              f"       ({audio_path})\n"
              "       The WAV is not the mix this provenance describes. Rebuild the mix.",
              file=sys.stderr)
        return 2

    video_path = Path(args.video)
    video_exists = video_path.exists()
    video_dir = video_path.parent
    slug = ep

    # ---- allocate an immutable version + output path -------------------------
    ep_audio_dir = ep_dir / "06_audio"
    version = next_version(ep_audio_dir, video_dir, slug)
    out_name = f"{slug}_film.muxed.v{version:03d}.mp4"
    out_path = video_dir / out_name
    receipt_path = ep_audio_dir / f"mux_receipt.v{version:03d}.json"

    # ---- assemble the ffmpeg mux command -------------------------------------
    comment = (f"PD case film final mux; sole audio = built 4-layer mix; "
               f"{MIX_SHA_TAG}={stamp_sha or 'UNKNOWN'}; generator={GENERATOR}")
    argv = [
        "ffmpeg", "-y",
        "-i", str(video_path),
        "-i", str(audio_path),
        "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", AAC_BITRATE, "-ar", SAMPLE_RATE, "-ac", CHANNELS,
        "-metadata", f"{MIX_SHA_TAG}={stamp_sha or ''}",
        "-metadata", f"comment={comment}",
        # +use_metadata_tags: the MP4/MOV muxer silently DROPS arbitrary metadata
        # keys unless this flag is set (only 'comment' etc. survive otherwise). With
        # it, the custom audio_mix_sha256 atom is written and reads back via
        # ffprobe format_tags. The sha is ALSO embedded in 'comment' as a fallback.
        "-movflags", "+faststart+use_metadata_tags",
        "-shortest",
        str(out_path),
    ]
    command_str = " ".join(quote_arg(a) for a in argv)

    # ---- console: resolved plan ---------------------------------------------
    print(f"episode        : {ep}")
    print(f"provenance     : {rel(prov_path)}")
    print(f"video          : {video_path}  ({'exists' if video_exists else 'MISSING'})")
    print(f"mix wav        : {audio_path}  ({'exists' if audio_exists else 'MISSING'})  [{audio_source}]")
    print(f"stamp {MIX_SHA_TAG} = {stamp_sha}  (source: "
          f"{'provenance.mix.sha256' if prov_mix_sha else ('hashed WAV' if file_mix_sha else 'UNKNOWN')})")
    print(f"output (v{version:03d}) : {out_path}")
    print(f"receipt        : {rel(receipt_path)}")
    print("ffmpeg command :")
    print("  " + command_str)

    # ---- DRY-RUN: emit nothing ----------------------------------------------
    if args.dry_run:
        if not audio_exists:
            print("\n[dry-run] mix WAV does not exist yet -- build it first with:")
            print(f"  ./.venv/Scripts/python.exe scripts/build_case_film_audio.py --ep {ep} --render")
        if not video_exists:
            print("[dry-run] video render does not exist yet (expected for EP32) -- no file written.")
        print("\n[dry-run] no ffmpeg executed, no receipt written.")
        return 0

    # ---- REAL RUN guards -----------------------------------------------------
    if not video_exists:
        print(f"ERROR: video render not found: {video_path}", file=sys.stderr)
        return 2
    if not audio_exists:
        print("ERROR: the built mix WAV does not exist -- refusing to ship video-only audio.\n"
              f"       expected: {audio_path}\n"
              "       Build the 4-layer mix first:\n"
              f"       ./.venv/Scripts/python.exe scripts/build_case_film_audio.py --ep {ep} --render",
              file=sys.stderr)
        return 2
    if not stamp_sha:
        print("ERROR: could not determine the mix sha to stamp (provenance mix.sha256 is null "
              "and the WAV could not be hashed).", file=sys.stderr)
        return 2

    # ---- idempotency: same video + same mix already muxed? -------------------
    video_sha = sha256_file(video_path)
    prior = find_prior_mux(ep_audio_dir, video_sha, stamp_sha)
    if prior:
        print(f"\n[idempotent] this video sha + mix sha were already muxed -> "
              f"{prior['output']['path']} (receipt {prior.get('receipt_version')}). Nothing to do.")
        return 0

    # ---- execute the mux (atomic temp + rename) ------------------------------
    out_path.parent.mkdir(parents=True, exist_ok=True)
    # temp keeps a .mp4 extension so ffmpeg infers the container (a .part suffix would not)
    tmp_out = out_path.with_suffix(".part.mp4")
    argv_run = [*argv[:-1], str(tmp_out)]
    print("\nrunning ffmpeg mux ...")
    result = subprocess.run(argv_run)
    if result.returncode != 0:
        if tmp_out.exists():
            tmp_out.unlink()
        print(f"ERROR: ffmpeg exited {result.returncode}", file=sys.stderr)
        return 1
    tmp_out.replace(out_path)

    out_sha = sha256_file(out_path)
    stamped_readback = probe_format_tag(out_path, MIX_SHA_TAG)
    stamp_ok = stamped_readback == stamp_sha
    print(f"WROTE {out_path}")
    print(f"output sha256  : {out_sha}")
    print(f"stamped tag readback: {MIX_SHA_TAG}={stamped_readback} "
          f"({'OK' if stamp_ok else 'MISMATCH'})")

    # ---- receipt (deterministic; no wall-clock in content) -------------------
    receipt = {
        "schema_version": SCHEMA_VERSION,
        "kind": "case_film_mux_receipt",
        "episode_id": ep,
        "receipt_version": f"v{version:03d}",
        "generator": GENERATOR,
        "provenance_ref": {
            "path": rel(prov_path),
            "sha256": prov_sha,
            "mix_sha256": prov_mix_sha,
        },
        "input_video": {
            "path": str(video_path),
            "sha256": video_sha,
        },
        "mix_audio": {
            "path": str(audio_path),
            "source": audio_source,
            "sha256_provenance": prov_mix_sha,
            "sha256_on_disk": file_mix_sha,
            "sha256_stamped": stamp_sha,
        },
        "output": {
            "path": str(out_path),
            "sha256": out_sha,
            "audio_codec": "aac",
            "audio_bitrate": AAC_BITRATE,
            "sample_rate": int(SAMPLE_RATE),
            "channels": int(CHANNELS),
            "sole_audio_track": True,
        },
        "stamp": {
            "tag": MIX_SHA_TAG,
            "value": stamp_sha,
            "readback": stamped_readback,
            "verified": stamp_ok,
            "comment": comment,
            "note": (f"check_final_acceptance can read format_tags.{MIX_SHA_TAG} off the render "
                     f"and confirm it equals audio_provenance.mix.sha256 -> this mix reached this render."),
        },
        "ffmpeg": {
            "command": command_str,
            "mux_map": "-map 0:v:0 -map 1:a:0 (mix WAV is the SOLE audio; video's own audio dropped)",
        },
        "deterministic": True,
        "side_effects": {
            "external_cost_usd": 0,
            "external_calls": [],
            "wrote_files": [rel(receipt_path), str(out_path)],
            "ran_ffmpeg": True,
        },
    }

    # atomic write (temp + rename)
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(receipt, indent=2, ensure_ascii=False) + "\n"
    tmp_receipt = receipt_path.with_suffix(receipt_path.suffix + ".tmp")
    tmp_receipt.write_text(payload, encoding="utf-8")
    tmp_receipt.replace(receipt_path)
    print(f"receipt -> {receipt_path}")

    if not stamp_ok:
        print("WARNING: stamped tag did not read back equal to the mix sha; the ship gate "
              "verification would fail. Investigate before scheduling.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
