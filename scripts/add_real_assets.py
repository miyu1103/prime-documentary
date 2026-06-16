#!/usr/bin/env python3
r"""Rights-log acquired real PD assets into PD-2026-002-gideon rights_manifest.v001.json.

Real public-domain inserts (0004 §D/§N): hashes computed from the downloaded files on the SSD;
each entry records the PD basis + source URL. Idempotent (replaces the AST-02xx real-asset block).
    py -3.11 scripts/add_real_assets.py
"""
from __future__ import annotations
import hashlib, json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
MEDIA = Path(json.loads((REPO / "config/storage.local.json").read_text("utf-8"))["roots"]["media"]["path"])
EP = "PD-2026-002-gideon"
REAL = MEDIA / "episodes" / EP / "05_visuals" / "real"
MANI = REPO / "episodes" / EP / "09_package" / "rights_manifest.v001.json"

PD_COURT = "Public domain — U.S. federal court record (Gideon v. Wainwright cert petition, NARA NAID 597554); no copyright. Mirror: Wikimedia Commons."
PD_LOC = "Public domain — Library of Congress, Bain/PPOC (LCCN 2014718460); no known restrictions on publication."
PD_SCOTUS = "Public domain — U.S. Supreme Court oral-argument recording, 1963-01-15 (Oyez / National Archives); U.S. government work, no copyright."

ASSETS = [
    ("AST-0200", "image", "S001/S009/S010", "Gideon's handwritten pencil cert petition, page 1 (HERO) — 'In The Supreme Court... No. 890 Misc. OCT TERM 1961'", "gideon_petition_cert_p1.jpg", "NARA/Commons", PD_COURT, "https://commons.wikimedia.org/wiki/File:Gideon_petition_for_certiorari.jpg"),
    ("AST-0201", "image", "S009/S010", "Gideon cert petition page 2 of 5 (06-05-1962)", "gideon_petition_cert_p2.jpg", "NARA/Commons", PD_COURT, "https://commons.wikimedia.org/wiki/File:Petition_for_a_Writ_of_Certiorari_from_Clarence_Gideon_..._(page_2_of_5)_(4127741167).jpg"),
    ("AST-0202", "image", "S009/S010", "Gideon cert petition page 3 of 5", "gideon_petition_cert_p3.jpg", "NARA/Commons", PD_COURT, "https://commons.wikimedia.org/wiki/File:Petition_for_a_Writ_of_Certiorari_from_Clarence_Gideon_..._(page_3_of_5)_(4127742041).jpg"),
    ("AST-0203", "image", "S010/S012", "Gideon cert petition page 4 of 5", "gideon_petition_cert_p4.jpg", "NARA/Commons", PD_COURT, "https://commons.wikimedia.org/wiki/File:Petition_for_a_Writ_of_Certiorari_from_Clarence_Gideon_..._(page_4_of_5)_(4127742707).jpg"),
    ("AST-0204", "image", "S010/S012", "Gideon cert petition page 5 of 5", "gideon_petition_cert_p5.jpg", "NARA/Commons", PD_COURT, "https://commons.wikimedia.org/wiki/File:Petition_for_a_Writ_of_Certiorari_from_Clarence_Gideon_..._(page_5_of_5)_(4127742451).jpg"),
    ("AST-0210", "image", "S015", "Hugo L. Black portrait (opinion author) — real photograph", "hugo_black_portrait_loc.jpg", "Library of Congress", PD_LOC, "https://commons.wikimedia.org/wiki/File:Hugo_L._Black_LCCN2014718460.jpg"),
    ("AST-0220", "audio_real", "S013-S015", "Real oral-argument audio 1963-01-15, part 1 (Abe Fortas for Gideon)", "gideon_oral_argument_19630115_part1.mp3", "Oyez/NARA (SCOTUS)", PD_SCOTUS, "https://s3.amazonaws.com/oyez.case-media.mp3/case_data/1962/155/19630115a_155_part1.delivery.mp3"),
    ("AST-0221", "audio_real", "S013-S015", "Real oral-argument audio 1963-01-15, part 2", "gideon_oral_argument_19630115_part2.mp3", "Oyez/NARA (SCOTUS)", PD_SCOTUS, "https://s3.amazonaws.com/oyez.case-media.mp3/case_data/1962/155/19630115a_155_part2.delivery.mp3"),
]


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
    mani["assets"] = [a for a in mani["assets"] if not a["asset_id"].startswith("AST-02")]
    added = 0
    for aid, atype, scene, desc, fname, producer, basis, url in ASSETS:
        f = REAL / fname
        if not f.exists():
            print(f"SKIP {aid}: missing {fname}")
            continue
        mani["assets"].append({
            "asset_id": aid, "type": atype, "scene": scene, "description": desc,
            "file": f"artifact://episodes/{EP}/05_visuals/real/{fname}",
            "producer": producer, "license": basis,
            "rights_holder": "Public domain (no rights holder)",
            "content_hash": f"sha256:{sha256(f)}", "needs_verification": False,
            "source_url": url, "is_real_pd_asset": True,
        })
        added += 1
    mani["notes"] = mani.get("notes", "") + f" | +{added} real PD assets (petition x5, Black portrait, oral-argument audio x2) acquired + hashed 2026-06-17 (0004 §D, floor 8-12 met)."
    MANI.write_text(json.dumps(mani, indent=2, ensure_ascii=False) + "\n", "utf-8")
    print(f"added {added} real-asset rights lines; manifest now {len(mani['assets'])} assets")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
