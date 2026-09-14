"""Build the EP82 Valdez raw Codex image receipt without modifying any plate."""

from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[3]
DEST = Path(r"E:\pd-media\05_visuals\valdez\img")
REJECTED = DEST / "_rejected_initial"
CACHE = Path(
    r"C:\Users\aab15\.codex\generated_images"
    r"\01a0344d-e427-79d0-8dd6-2fbeabc1127c"
)
ORDER = ROOT / "episodes/_planning/EP82_valdez_CODEX_BATCH_A.v001.md"
PASTE_ALL = ROOT / "episodes/_planning/EP82_valdez_CODEX_PASTE_ALL.txt"
PLATES = ROOT / "episodes/_planning/EP82_valdez_CODEX_PASTE/plates.v001.jsonl"
REPORT = ROOT / "episodes/PD-2026-082-valdez/05_visuals/codex_image_batch.v001.json"

VISUAL_REJECTS = {
    "V007": "generated bridge instruments contain text-like glyphs and numerals",
    "V022": "semantic mismatch: desk and bench generated instead of the requested empty bunk",
    "V023": "visible clock numerals conflict with the shared no-numerals constraint",
    "V116": "quantity mismatch: ten chairs generated instead of the specified nine",
    "V153": "a left-edge gallery figure shows a partial facial profile",
}

OWNER_REVIEW = {
    "V051": "bridge styling appears older than the episode's 1989 tanker setting",
    "V081": "wheel and bridge styling may read older than the episode's 1989 setting",
    "V092": "continuity with the preceding bunk plate is weak",
    "V133": "ending bunk callback should be checked against the opening composition",
    "V134": "the requested same-bunk continuity is weak",
    "V137": "bridge styling should be checked for 1989 tanker plausibility",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    rows = [
        json.loads(line)
        for line in PLATES.read_text(encoding="utf-8").splitlines()
        if line
    ]
    expected = {f"V{i:03d}.png" for i in range(1, 185)}
    root_files = sorted(DEST.glob("V*.png"))
    rejected_files = sorted(REJECTED.glob("V*.png"))
    all_files = root_files + rejected_files
    delivered_names = {path.name for path in all_files}

    cache_by_hash: dict[str, list[Path]] = defaultdict(list)
    for path in sorted(CACHE.glob("*.png")):
        cache_by_hash[sha256(path)].append(path)

    assets: list[dict[str, object]] = []
    corrupt: list[dict[str, str]] = []
    delivery_by_hash: dict[str, list[str]] = defaultdict(list)
    for row in rows:
        root_path = DEST / row["file"]
        rejected_path = REJECTED / row["file"]
        candidates = [path for path in (root_path, rejected_path) if path.is_file()]
        if len(candidates) != 1:
            continue
        path = candidates[0]
        digest = sha256(path)
        delivery_by_hash[digest].append(path.name)
        try:
            with Image.open(path) as image:
                image.load()
                metadata = {
                    "width": image.width,
                    "height": image.height,
                    "format": image.format,
                    "mode": image.mode,
                }
        except Exception as exc:  # diagnostic path
            corrupt.append({"file": path.name, "error": str(exc)})
            continue
        matches = cache_by_hash.get(digest, [])
        canonical_prompt = "\n".join(
            (row["style"], row["prompt"], row["neg"])
        ).encode("utf-8")
        disposition = "reject_recommended" if row["id"] in VISUAL_REJECTS else (
            "owner_review" if row["id"] in OWNER_REVIEW else "accepted_raw_candidate"
        )
        assets.append(
            {
                "id": row["id"],
                "file": row["file"],
                "section": row["section"],
                "people_flag": "P" in row.get("flags", []),
                "disposition": disposition,
                "visual_qc_reason": VISUAL_REJECTS.get(row["id"], OWNER_REVIEW.get(row["id"])),
                "path": str(path).replace("\\", "/"),
                "sha256": digest,
                "canonical_prompt_sha256": hashlib.sha256(canonical_prompt).hexdigest(),
                "bytes": path.stat().st_size,
                **metadata,
                "cache_file": str(matches[0]).replace("\\", "/") if len(matches) == 1 else None,
            }
        )

    dimensions = Counter(f"{a['width']}x{a['height']}" for a in assets)
    modes = Counter(str(a["mode"]) for a in assets)
    formats = Counter(str(a["format"]) for a in assets)
    wrong_ratio = [
        str(a["id"])
        for a in assets
        if abs(int(a["width"]) / int(a["height"]) - 16 / 9) > 0.003
    ]
    exact_duplicates = [names for names in delivery_by_hash.values() if len(names) > 1]
    cache_mismatches = [str(a["id"]) for a in assets if a["cache_file"] is None]
    inventory = "\n".join(
        f"{a['id']}|{a['sha256']}|{a['bytes']}|{a['width']}x{a['height']}|{a['mode']}|{a['format']}|{a['disposition']}"
        for a in assets
    )
    accepted = [
        row["id"]
        for row in rows
        if row["id"] not in VISUAL_REJECTS and row["id"] not in OWNER_REVIEW
    ]
    technical_pass = (
        len(rows) == 184
        and len(assets) == 184
        and delivered_names == expected
        and not corrupt
        and dimensions == {"1672x941": 184}
        and modes == {"RGB": 184}
        and formats == {"PNG": 184}
        and not wrong_ratio
        and not exact_duplicates
        and not cache_mismatches
    )

    report = {
        "schema_version": "1.0",
        "episode_id": "PD-2026-082-valdez",
        "recorded_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "status": "raw_generation_complete_visual_exceptions_pending_owner",
        "scope": "EP82 Valdez V001-V184 built-in image generation, exact-ID raw delivery, technical QC, cache provenance verification, and preliminary visual QC only",
        "source_contract": {
            "order_file": "episodes/_planning/EP82_valdez_CODEX_BATCH_A.v001.md",
            "order_file_sha256": sha256(ORDER),
            "instruction_file": "episodes/_planning/EP82_valdez_CODEX_PASTE_ALL.txt",
            "instruction_file_sha256": sha256(PASTE_ALL),
            "plates_file": "episodes/_planning/EP82_valdez_CODEX_PASTE/plates.v001.jsonl",
            "plates_file_sha256": sha256(PLATES),
            "batch_files": 23,
            "requested_ids": "V001-V184",
            "requested_count": 184,
            "people_flags": sum("P" in row.get("flags", []) for row in rows),
            "one_prompt_one_image": True,
            "required_aspect_ratio": "16:9",
            "raw_dimensions": "1672x941",
        },
        "source_preflight": {
            "shared_negative_constraints": "pass",
            "prompt_coverage": "184/184",
            "prompt_diversity": "pass_after_six_minimal_composition_edits",
            "ids_edited_for_diversity": ["V113", "V133", "V136", "V137", "V141", "V152"],
        },
        "generation": {
            "provider": "Codex built-in image generation",
            "use_case": "historical-scene",
            "calls": 184,
            "outputs": 184,
            "automatic_retries": 0,
            "variants": 0,
            "overwrites": 0,
            "model_profile": "built-in provider metadata not exposed",
            "seed": "not exposed",
            "provider_cost": "not exposed by built-in tool",
            "raw_directory": str(DEST).replace("\\", "/"),
            "rejected_directory": str(REJECTED).replace("\\", "/"),
            "cache_root": str(CACHE).replace("\\", "/"),
        },
        "technical_qc": {
            "status": "pass" if technical_pass else "fail",
            "files": len(assets),
            "root_candidates": len(root_files),
            "rejected_candidates": len(rejected_files),
            "missing_ids_across_root_and_rejected": sorted(expected - delivered_names),
            "unexpected_ids_across_root_and_rejected": sorted(delivered_names - expected),
            "corrupt": corrupt,
            "dimensions": dict(dimensions),
            "image_mode": dict(modes),
            "format": dict(formats),
            "wrong_aspect_ids": wrong_ratio,
            "exact_duplicate_groups": exact_duplicates,
            "cache_sha_matches": len(assets) - len(cache_mismatches),
            "cache_sha_mismatches": cache_mismatches,
            "total_bytes": sum(int(a["bytes"]) for a in assets),
            "inventory_sha256": hashlib.sha256(inventory.encode("utf-8")).hexdigest(),
        },
        "visual_qc": {
            "status": "exceptions_pending_owner",
            "method": "All labelled delivery contact sheets and the rejected contact sheet were reviewed; suspected text, numeral, face, quantity, continuity, and anachronism failures were inspected at original resolution when needed.",
            "contact_sheet_directory": "runs/qc/plate_sheets/valdez",
            "contact_sheets": 12,
            "rejected_contact_sheet_directory": "runs/qc/plate_sheets/valdez-rejected",
            "rejected_contact_sheets": 1,
            "accepted_without_flag": accepted,
            "reject_recommended": VISUAL_REJECTS,
            "owner_review": OWNER_REVIEW,
            "automatic_regeneration_performed": False,
            "staged_for_edit": False,
            "approved_for_use": False,
        },
        "downstream_gates": {
            "root_require_all": "blocked_by_five_visual_rejects",
            "native_4k_or_upscale": "pending_for_all_179_root_candidates",
            "owner_visual_approval": "pending",
            "remotion_staging": "not_started",
        },
        "assets": assets,
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "report": str(REPORT),
                "technical_status": report["technical_qc"]["status"],
                "files": len(assets),
                "root_candidates": len(root_files),
                "reject_recommended": len(VISUAL_REJECTS),
                "owner_review": len(OWNER_REVIEW),
                "cache_sha_matches": report["technical_qc"]["cache_sha_matches"],
                "accepted_without_flag": len(accepted),
            },
            ensure_ascii=False,
        )
    )
    return 0 if technical_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
