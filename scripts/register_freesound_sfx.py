#!/usr/bin/env python3
"""Register the CC0 freesound SFX shelf into the sound-rights manifest.

WHY THIS EXISTS
---------------
`E:\\pd-media\\assets\\archive\\_ledger\\freesound.jsonl` holds 125 CC0 audio
files (all `license_decision == "cc0"`, all `usage_tag == "sfx"`, all
`theme == "sfx_environment"`).  CC0 is not the gate: **the publish gate is
inclusion in `episodes/_planning/SOUND_LIBRARY_RIGHTS.v001.json`**, and none of
these rows are in it.  Until they are registered, no shipped mix may use them
(see any EP bgm_plan: "候補トラックは全て rights registry 収載の内部ライブラリのみ").

There is a SECOND blocker that registration alone does not clear: the files live
at `D:\\pd-archive\\sfx_environment\\`, outside the library root
(`E:\\pd-media\\library`).  `scripts/build_case_film_audio.py` resolves one-shot
SFX as `lib / "sfx" / filename`, so a clip must also be STAGED into
`E:\\pd-media\\library\\sfx\\` before the builder can see it.

  UNLOCK = (1) --apply  [rights registry entry]  AND  (2) --stage  [library copy]

Both steps are recorded in the manifest: an entry is only `build_visible` once
its staged copy exists.

USAGE
-----
  python scripts/register_freesound_sfx.py                     # generate pending entries (default, writes nothing canonical)
  python scripts/register_freesound_sfx.py --verify-sha 8      # spot-check 8 files' sha256 against the ledger
  python scripts/register_freesound_sfx.py --verify-sha 0      # verify ALL files (slow)
  python scripts/register_freesound_sfx.py --apply             # merge entries into SOUND_LIBRARY_RIGHTS.v001.json (.bak first)
  python scripts/register_freesound_sfx.py --stage FSX-0004,FSX-0005   # copy those clips into the library sfx dir
  python scripts/register_freesound_sfx.py --list rain         # search the shelf by title/keyword

Exit code 0 = OK, 1 = a hard check failed (non-CC0 row, missing file, sha
mismatch).  Nothing here touches YouTube or any published artifact.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
LEDGER = Path(r"E:\pd-archive\_ledger\freesound.jsonl")
REGISTRY = REPO / "episodes" / "_planning" / "SOUND_LIBRARY_RIGHTS.v001.json"
PENDING = REPO / "episodes" / "_planning" / "SOUND_LIBRARY_RIGHTS.freesound_pending.v001.json"
LIBRARY_SFX = Path(r"E:\pd-media\library\sfx")

ID_PREFIX = "FSX"  # distinct from SFX- (ElevenLabs), MUS- (Suno), SYN- (ffmpeg)

CC0_LICENSE = (
    "Creative Commons Zero 1.0 Universal (CC0) — public domain dedication; "
    "commercial use permitted, no attribution required"
)
CC0_URL = "https://creativecommons.org/publicdomain/zero/1.0/"

# The amb_light_wind precedent: broadband wind roar reads as an aeroplane under
# narration (owner 2026-07-06 / 2026-07-10).  Flag, do not silently ship.
WIND_FLAG_KEYWORDS = {"wind", "waves", "surf", "ocean"}


def load_ledger() -> list[dict]:
    if not LEDGER.exists():
        sys.exit(f"FAIL: ledger not found: {LEDGER}")
    rows = []
    with LEDGER.open(encoding="utf-8") as fh:
        for line_no, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                sys.exit(f"FAIL: {LEDGER}:{line_no} is not valid JSON ({exc})")
    return rows


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def build_entries(rows: list[dict]) -> tuple[list[dict], list[str]]:
    """Return (entries, problems).  One entry per CC0 row.

    IDs are `FSX-<freesound id>` — derived from the source id, NOT a running
    sequence, so they stay stable as the ingest keeps appending rows (the ledger
    grew 125 -> 132 during EP56 packaging).  Re-running after new rows land only
    ever ADDS ids; it never renumbers an already-registered clip.
    """
    entries: list[dict] = []
    problems: list[str] = []
    seen: set[str] = set()

    for row in sorted(rows, key=lambda r: str(r.get("id", ""))):
        lic = str(row.get("license_decision", "")).lower()
        if lic != "cc0":
            problems.append(f"non-CC0 row skipped: id={row.get('id')} license_decision={lic!r}")
            continue

        src_path = Path(str(row.get("file_path", "")))
        filename = src_path.name
        if not filename:
            problems.append(f"row id={row.get('id')} has no file_path")
            continue

        asset_id = f"{ID_PREFIX}-{row.get('id')}"
        if asset_id in seen:
            problems.append(f"duplicate source id in ledger: {asset_id}")
            continue
        seen.add(asset_id)

        keywords = sorted({str(k).lower() for k in row.get("matched_keywords", [])})
        usage_tags = sorted({str(row.get("usage_tag") or "sfx"), str(row.get("theme") or "")} - {""})
        wind_flagged = bool(WIND_FLAG_KEYWORDS & set(keywords))

        staged = LIBRARY_SFX / filename
        entries.append(
            {
                "id": asset_id,
                "filename": filename,
                # These live OUTSIDE library_root until staged; both paths recorded.
                "path_relative": None,
                "path_absolute": str(src_path),
                "path_relative_when_staged": f"library/sfx/{filename}",
                "staged": staged.exists(),
                "build_visible": staged.exists(),
                "category": "sfx",
                "function": "environment_texture",
                "provenance_method": "downloaded-cc0",
                "owned": False,
                "license": CC0_LICENSE,
                "license_url": CC0_URL,
                "license_field_raw": row.get("license_field_raw"),
                "commercial_ok": True,
                "attribution_required": False,
                "provenance_status": "recorded_license",
                "publish_gate": (
                    "CC0 needs no clearance, but this asset may only enter a shipped mix once it is "
                    "(1) present in this manifest and (2) staged into E:\\pd-media\\library\\sfx\\ so "
                    "build_case_film_audio.py can resolve it; L4 one-shot / thin texture use ONLY — it "
                    "must never replace an L3 canonical AMBIENCE_BEDS bed"
                ),
                "file_sha256_recorded": row.get("sha256"),
                "bytes": row.get("bytes"),
                "source": row.get("source"),
                "source_url": row.get("source_url"),
                "source_id": row.get("id"),
                "fetched_at": row.get("fetched_at"),
                "title": row.get("title"),
                "usage_tags": usage_tags,
                "matched_keywords": keywords,
                "pd_layer": "L4_sfx_only",
                "pd_use_note": (
                    "WIND/WAVE-HEAVY — audition under narration before use; the amb_light_wind "
                    "precedent (broadband roar reads as an aeroplane) applies"
                    if wind_flagged
                    else "environment texture; audition under narration at the -30..-34 dB glue range"
                ),
            }
        )
    return entries, problems


def verify_sha(entries: list[dict], sample: int) -> list[str]:
    """sample>0 -> random spot-check of that many; sample==0 -> all."""
    targets = entries if sample == 0 else random.sample(entries, min(sample, len(entries)))
    problems: list[str] = []
    for e in targets:
        p = Path(e["path_absolute"])
        if not p.exists():
            problems.append(f"MISSING FILE {e['id']}: {p}")
            continue
        actual = sha256_of(p)
        if actual != e["file_sha256_recorded"]:
            problems.append(f"SHA MISMATCH {e['id']}: ledger={e['file_sha256_recorded']} actual={actual}")
        else:
            print(f"  ok  {e['id']}  {e['filename'][:64]}")
    return problems


def write_pending(entries: list[dict], problems: list[str]) -> None:
    doc = {
        "schema_version": "1.0.0",
        "kind": "sound_library_rights_manifest_pending_merge",
        "revision": "v001",
        "generated_by": "scripts/register_freesound_sfx.py",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "merges_into": str(REGISTRY.relative_to(REPO)).replace("\\", "/"),
        "source_ledger": str(LEDGER),
        "archive_root": r"D:\pd-archive\sfx_environment",
        "library_sfx_dir": str(LIBRARY_SFX),
        "unlock_steps": [
            "1. python scripts/register_freesound_sfx.py --apply   (writes the entries into SOUND_LIBRARY_RIGHTS.v001.json, .bak kept)",
            "2. python scripts/register_freesound_sfx.py --stage <IDS>   (copies just the clips a build needs into E:\\pd-media\\library\\sfx\\)",
            "L4 one-shot / thin texture use only — never as an L3 AMBIENCE_BEDS replacement",
        ],
        "summary": {
            "entries": len(entries),
            "all_cc0": True,
            "all_commercial_ok": True,
            "any_attribution_required": False,
            "staged_now": sum(1 for e in entries if e["staged"]),
            "wind_flagged": sum(1 for e in entries if e["pd_use_note"].startswith("WIND")),
        },
        "problems": problems,
        "assets": entries,
    }
    PENDING.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {PENDING}  ({PENDING.stat().st_size:,} bytes, {len(entries)} entries)")


def apply_merge(entries: list[dict]) -> None:
    reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
    existing = {a["id"] for a in reg["assets"]}
    new = [e for e in entries if e["id"] not in existing]

    # Refresh staged/build_visible on already-registered rows: --stage runs after
    # --apply, so these flags go stale unless re-synced from the filesystem.
    fresh = {e["id"]: e for e in entries}
    refreshed = 0
    for a in reg["assets"]:
        f = fresh.get(a["id"])
        if f and (a.get("staged") != f["staged"] or a.get("build_visible") != f["build_visible"]):
            a["staged"], a["build_visible"] = f["staged"], f["build_visible"]
            refreshed += 1

    if not new and not refreshed:
        print("nothing to merge - all entries already present and staging flags current")
        return

    backup = REGISTRY.with_suffix(REGISTRY.suffix + ".bak")
    shutil.copy2(REGISTRY, backup)
    if refreshed:
        print(f"refreshed staging flags on {refreshed} existing entries")

    reg["assets"].extend(new)
    s = reg["summary"]
    s["total_assets"] = len(reg["assets"])
    s["licensed_commercial_ok"] = s.get("licensed_commercial_ok", 0) + len(new)
    s.setdefault("by_method", {})
    s["by_method"]["downloaded-cc0"] = s["by_method"].get("downloaded-cc0", 0) + len(new)
    s["all_commercial_ok"] = all(a.get("commercial_ok") for a in reg["assets"])
    s["any_attribution_required"] = any(a.get("attribution_required") for a in reg["assets"])
    reg["generated_by"] = reg.get("generated_by", "") + " + scripts/register_freesound_sfx.py (CC0 shelf)"

    REGISTRY.write_text(json.dumps(reg, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"merged {len(new)} entries into {REGISTRY}  (backup: {backup.name})")


def stage(entries: list[dict], ids: list[str]) -> list[str]:
    by_id = {e["id"]: e for e in entries}
    problems = []
    LIBRARY_SFX.mkdir(parents=True, exist_ok=True)
    for i in ids:
        e = by_id.get(i)
        if not e:
            problems.append(f"unknown id {i}")
            continue
        src, dst = Path(e["path_absolute"]), LIBRARY_SFX / e["filename"]
        if not src.exists():
            problems.append(f"MISSING FILE {i}: {src}")
            continue
        if dst.exists():
            print(f"  already staged  {i}  {dst.name}")
            continue
        shutil.copy2(src, dst)
        print(f"  staged  {i} -> {dst}")
    return problems


def main() -> int:
    # Windows consoles default to cp932 here; ledger titles are arbitrary unicode.
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--verify-sha", type=int, metavar="N", help="verify N random files (0 = all) against the ledger sha256")
    ap.add_argument("--apply", action="store_true", help="merge entries into SOUND_LIBRARY_RIGHTS.v001.json")
    ap.add_argument("--stage", metavar="IDS", help="comma-separated FSX ids to copy into the library sfx dir")
    ap.add_argument("--list", metavar="TERM", help="search the shelf by title/keyword and print matches")
    args = ap.parse_args()

    rows = load_ledger()
    entries, problems = build_entries(rows)
    print(f"ledger rows={len(rows)}  cc0 entries={len(entries)}  problems={len(problems)}")
    for p in problems:
        print(f"  ! {p}")

    if args.list:
        term = args.list.lower()
        for e in entries:
            hay = f"{e['title']} {' '.join(e['matched_keywords'])}".lower()
            if term in hay:
                mark = "staged" if e["staged"] else "     "
                print(f"  {e['id']}  {mark}  {e['title'][:72]}")
        return 0

    if args.verify_sha is not None:
        problems += verify_sha(entries, args.verify_sha)

    if args.stage:
        problems += stage(entries, [i.strip() for i in args.stage.split(",") if i.strip()])
        entries, _ = build_entries(rows)  # refresh staged/build_visible flags

    write_pending(entries, problems)

    if args.apply:
        if any(p.startswith(("SHA MISMATCH", "MISSING FILE")) for p in problems):
            print("REFUSING --apply: integrity problems above must be resolved first")
            return 1
        apply_merge(entries)

    hard = [p for p in problems if p.startswith(("SHA MISMATCH", "MISSING FILE", "FAIL"))]
    return 1 if hard else 0


if __name__ == "__main__":
    sys.exit(main())
