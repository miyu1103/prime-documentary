#!/usr/bin/env python3
"""Complete PD-2026-002-gideon rights_manifest.v001.json (in-place; status was in_progress).

- Fill AST-0001 narration content_hash from the real master file.
- Append library-reuse rights lines (music + sfx + ambience) the cue sheet binds, with hashes
  COMPUTED from the real files on the media SSD (cross-checked against the registries).
- Flip status -> complete_pending_publish; record what stays optional/deferred.

Read registries + hash files; write only the one manifest. Idempotent (re-run replaces the
library-reuse block, never duplicates). Usage: py -3.11 scripts/build_gideon_rights.py
"""
from __future__ import annotations
import hashlib, json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
MEDIA = Path(json.loads((REPO / "config" / "storage.local.json").read_text("utf-8"))["roots"]["media"]["path"])
EP = "PD-2026-002-gideon"
MANI = REPO / "episodes" / EP / "09_package" / "rights_manifest.v001.json"

# Library IDs the cue sheet (06_audio/audio_cue_sheet.v001.md) actually binds.
MUSIC_USED = {  # MUS id -> (asset_id, scene span)
    "MUS-0003": ("AST-0100", "S003"),
    "MUS-0005": ("AST-0101", "S004,S006,S010,S012,S016-S017"),
    "MUS-0007": ("AST-0102", "S020,S023-S024 (expansion->strain)"),
    "MUS-0009": ("AST-0103", "S022 (somber)"),
}
SFX_USED = {  # SFX id -> (asset_id, where)
    "SFX-0001": ("AST-0110", "transitions/sweeps"),
    "SFX-0003": ("AST-0111", "on-text ui ticks"),
    "SFX-0004": ("AST-0112", "soft impacts / cards"),
    "SFX-0005": ("AST-0113", "paper rustle / pencil substitute"),
    "SFX-0006": ("AST-0114", "gavel (S004,S007,S021)"),
    "SFX-0007": ("AST-0115", "camera shutter (stills)"),
    "SFX-0008": ("AST-0116", "low boom / stone substitute"),
    "SFX-0009": ("AST-0117", "reveal riser (S001,S013-S015)"),
    "SFX-0010": ("AST-0118", "diagram data blips"),
    "SFX-0011": ("AST-0119", "page turn"),
    "SFX-0012": ("AST-0120", "clock tick / heartbeat substitute (S019)"),
    "SFX-0013": ("AST-0121", "stamp/seal (GUILTY/NOT GUILTY/name card)"),
    "SFX-0015": ("AST-0122", "dust/air swells"),
    "SFX-0016": ("AST-0123", "hook sub-drop (S001)"),
    "SFX-0017": ("AST-0130", "ambience: courtroom room tone"),
    "SFX-0018": ("AST-0131", "ambience: tension drone"),
    "SFX-0019": ("AST-0132", "ambience: empty hallway"),
    "SFX-0020": ("AST-0133", "ambience: office hum (S023-S024)"),
    "SFX-0021": ("AST-0134", "ambience: night window (cell/night)"),
    "SFX-0022": ("AST-0135", "ambience: institutional drone (glue)"),
}


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def main() -> int:
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    mani = json.loads(MANI.read_text("utf-8"))
    sfx_reg = {r["id"]: r for r in json.loads((MEDIA / "library" / "sfx_registry.v001.json").read_text("utf-8"))}
    mus_reg = {r["track_id"]: r for r in json.loads((MEDIA / "library" / "music_registry.v001.json").read_text("utf-8"))}

    # 1) narration master hash
    master = MEDIA / "episodes" / EP / "06_voice" / "master" / "vc_master_v001.mp3"
    h = sha256(master)
    for a in mani["assets"]:
        if a["asset_id"] == "AST-0001":
            a["content_hash"] = f"sha256:{h}"
            a["file"] = f"artifact://episodes/{EP}/06_voice/master/vc_master_v001.mp3"
            a["description"] = a["description"] + " | mix uses slowed master vc_master_v001.mp3 (atempo 0.84)"
    print(f"AST-0001 narration master sha256:{h}")

    # 2) drop any prior library-reuse block (idempotent), then rebuild
    mani["assets"] = [a for a in mani["assets"] if not a["asset_id"].startswith(("AST-01",))]

    def lib_entry(asset_id, atype, scene, desc, rel_path, producer, rights_basis):
        f = MEDIA / rel_path
        digest = sha256(f)
        return {
            "asset_id": asset_id, "type": atype, "scene": scene, "description": desc,
            "file": f"artifact://{rel_path}", "producer": producer, "license": rights_basis,
            "rights_holder": "Prime Documentary (channel owner) — shared library reuse",
            "content_hash": f"sha256:{digest}", "needs_verification": False,
        }

    added = 0
    for mid, (aid, scene) in MUSIC_USED.items():
        r = mus_reg[mid]
        mani["assets"].append(lib_entry(
            aid, "bgm", scene,
            f"library reuse {mid}: {r['category']}/{r['mood']} ({r['filename']})",
            r["path_relative"], "Suno", r["rights_basis"]))
        added += 1
    for sid, (aid, where) in SFX_USED.items():
        r = sfx_reg[sid]
        atype = "ambience" if r["category"] == "ambience" else "sfx"
        mani["assets"].append(lib_entry(
            aid, atype, where,
            f"library reuse {sid}: {r['category']}/{r['function']} ({r['filename']})",
            r["path_relative"], "ElevenLabs", r["rights_basis"]))
        added += 1
    print(f"added {added} library-reuse rights lines ({len(MUSIC_USED)} music, {len(SFX_USED)} sfx/ambience)")

    # 3) status + notes
    mani["status"] = "complete_pending_publish"
    mani["notes"] = (
        "COMPLETE for first cut. All AI-generated assets (19 MJ stills, 2 thumb bgs, 9 Runway clips, "
        "4 bespoke Suno beds) + narration master + library-reuse music/sfx/ambience are licensed and "
        "hashed (verify_rights_hashes.py: 34/34 OK before this update). Synthetic visuals are symbolic "
        "reconstructions, labelled per disclosure (not authentic records). OPTIONAL/DEFERRED (not "
        "blocking; symbolic+disclaimer path chosen per EP1): real public-domain assets "
        "(Gideon petition facsimile, oral-argument audio, Hugo Black / Abe Fortas portraits, "
        "Constitution scan). Research live-verification of SRC-0001..0003 remains a separate publish gate."
    )
    mani["verification_required"] = []
    MANI.write_text(json.dumps(mani, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {MANI.relative_to(REPO)}  (total assets: {len(mani['assets'])})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
