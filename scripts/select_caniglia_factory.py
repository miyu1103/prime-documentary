#!/usr/bin/env python
"""Select EP42 (young) real factory footage from the Asset Factory shelf.

Models scripts/build_thompson_film.py's FACTORY_SEL flow: pick real .mp4 clips from
H:/pd-media/assets/factory/backgrounds that fit EP42's DARK / CINEMATIC / LEGAL tone
(courthouse, marble, night interiors, documents, doors), with:
  - sha256 NO-OVERLAP against EP39 (frazier) / EP40 (lech) / EP41 (thompson) staged factory,
  - per-subtype caps for visual variety,
  - act allocation matching the CODEX_B factory column (HOOK+OP 5 / ACT_1 14 / ACT_2 12 /
    ACT_3 28 / ACT_4 16 / ENDING 18 = 93),
  - labeled contact sheets so a HUMAN eyeballs every clip before it ships (the shelf's
    labels are unreliable -- machine cannot tell a cartoon/face/off-theme clip apart).

Two phases:
  --phase candidates : build an over-selected, sha-clean candidate pool + contact sheets +
                       runs/qc/caniglia_factory_candidates.v001.json   (for eyeball QC)
  --phase finalize   : read an eyeballed keep/cull decision file and write exactly 93 to
                       runs/qc/caniglia_factory_selected.v001.json with eyeballed_content.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHELF = Path("H:/pd-media/assets/factory/backgrounds")
# Prior episodes to avoid by sha256: EP39/EP40/EP41 are staged on disk; EP42 (young) is NOT
# staged yet, so its selection is read from its selected JSON instead.
PRIOR_FACTORY = [ROOT / "remotion" / "public" / s / "factory"
                 for s in ("frazier", "lech", "thompson")]   # EP39 / EP40 / EP41
PRIOR_SELECTED_JSONS = [ROOT / "runs" / "qc" / "young_factory_selected.v001.json"]  # EP42
QC = ROOT / "runs" / "qc"
CANDIDATES_JSON = QC / "caniglia_factory_candidates.v001.json"
SELECTED_JSON = QC / "caniglia_factory_selected.v001.json"
TARGET = 93

# Act allocation (sums to 93) -- CODEX_B §5.3 factory column (EP43: HOOK_OP 7 / ACT_1 10 /
# ACT_2 19 / ACT_3 38 / ENDING 19). EP43 BODY has 3 acts (no ACT_4).
ACT_QUOTA = {"HOOK_OP": 7, "ACT_1": 10, "ACT_2": 19, "ACT_3": 38, "ENDING": 19}

# On-theme subtype keywords -> act affinity. A shelf clip is on-theme iff its subtype
# contains an ALLOW key and no DENY key. First matching ALLOW sets the act suggestion.
# EP43 tone: closed/open front door, porch, night residential, hotel, phone, police/
# ambulance lights, a car on a highway in custody (Cady), marble courthouse/SCOTUS,
# documents/evidence, dawn. NO real-person faces / readable text / cartoons.
ALLOW: dict[str, str] = {
    # HOOK/OP -- the private home, the door, the keys, the question
    "front_door_house": "HOOK_OP", "suburban_house_exterior_night": "HOOK_OP",
    "white_picket_fence": "HOOK_OP", "key_turning_in_lock": "HOOK_OP",
    "old_keys_on_table": "HOOK_OP",
    # ACT_1 -- the night: the argument, the window, the hotel
    "two_people_arguing_silhouette": "ACT_1", "rain_on_window_night": "ACT_1",
    "window_blinds_shadow_stripes": "ACT_1", "motel_neon_sign_night": "ACT_1",
    "wooden_desk_lamp_night": "ACT_1", "candlelit_room_dark": "ACT_1",
    "snowy_street_night": "ACT_1",
    # ACT_2 -- the welfare check: phone -> porch -> police/ambulance lights -> seizure
    "red_rotary_telephone": "ACT_2", "rotary_phone_close_up": "ACT_2",
    "smartphone_in_dark": "ACT_2", "mobile_phone_map_location": "ACT_2",
    "police_car_lights_night": "ACT_2", "ambulance_lights_at_night": "ACT_2",
    "police_badge_close_up": "ACT_2", "police_station_at_night": "ACT_2",
    "evidence_bag": "ACT_2", "evidence_locker_shelves": "ACT_2",
    "person_at_window_silhouette_night": "ACT_2",
    # ACT_3 -- doctrine: Cady (a car, a highway, custody) + marble courthouse + documents
    "city_traffic_night_long_exposure": "ACT_3", "highway_night_long_exposure": "ACT_3",
    "empty_parking_garage": "ACT_3", "courthouse_steps": "ACT_3",
    "supreme_court_building": "ACT_3", "courtroom_interior": "ACT_3",
    "courtroom_empty_wide": "ACT_3", "courtroom_gavel_block_macro": "ACT_3",
    "judge_gavel_wooden": "ACT_3", "federal_building_columns_night": "ACT_3",
    "bank_building_columns": "ACT_3", "capitol_dome_dusk": "ACT_3",
    "law_library_books": "ACT_3", "law_books_spines_macro": "ACT_3",
    "balance_scale_brass": "ACT_3", "antique_brass_scales": "ACT_3",
    "documents_on_desk": "ACT_3", "case_files_stack_desk": "ACT_3",
    "stacked_legal_documents": "ACT_3", "wax_seal_on_document": "ACT_3",
    # ENDING -- payoff: the open door at dawn, mood, quiet
    "open_door_bright_light": "ENDING", "moody_atmosphere_fog": "ENDING",
    "foggy_harbor_dawn": "ENDING", "cemetery_fog": "ENDING",
    "abstract_dark_background": "ENDING", "dark_cinematic_background": "ENDING",
    "concrete_wall_texture_dark": "ENDING", "candle_in_dark": "ENDING",
    "city_skyline_dusk": "ENDING", "lone_person_silhouette_walking": "ENDING",
}
# Belt-and-suspenders: off-theme / face-risk / readable-text substrings to hard-exclude.
DENY = ("graduation", "flag_waving", "american_flag", "ocean", "mountain", "frozen_lake",
        "aurora", "canyon", "medical", "doctor", "robot", "solar_panel", "wind_turbine",
        "bitcoin", "satellite", "milky_way", "vinyl_record", "dog_tags", "airport",
        "shipping_container", "hydro_dam", "rural_road", "moving_truck", "film_camera",
        "world_map", "technology_abstract", "forest", "tree_in_field", "storm", "cloud",
        "vista", "earth_at_night", "turbine", "empty_road_sunset", "misty", "newspaper",
        "us_constitution", "us_constitution_document", "charging_bull", "wall_street",
        "stock_market", "credit_card", "dna", "circuit_board", "binary_code", "hacker",
        "fingerprint", "school_bus", "homeless", "doctor_consulting", "elderly_person",
        "child_looking", "person_crying", "wheelchair", "graduation_cap", "sdxl")
SUBTYPE_CAP = 4       # variety: at most N clips of the same subtype
SILHOUETTE_CAP = 8    # total silhouette/person clips allowed (no identifiable faces)


def subtype_of(name: str) -> str:
    stem = name.rsplit(".", 1)[0]
    return stem.split("__", 1)[1] if "__" in stem else stem


def theme_match(sub: str) -> str | None:
    if any(d in sub for d in DENY):
        return None
    for key, act in ALLOW.items():
        if key in sub:
            return act
    return None


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for blk in iter(lambda: f.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


def probe_dur(p: Path) -> float:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(p)], capture_output=True, text=True)
    try:
        return round(float(r.stdout.strip()), 3)
    except Exception:
        return 0.0


def prior_sha_universe() -> set[str]:
    shas: set[str] = set()
    for d in PRIOR_FACTORY:                       # EP39/40/41 staged clips on disk
        if not d.is_dir():
            continue
        for p in d.iterdir():
            if p.is_file() and p.suffix.lower() in (".mp4", ".mov", ".webm"):
                shas.add(sha256_file(p))
    for jp in PRIOR_SELECTED_JSONS:               # EP42 (young) not staged -> read its JSON
        if jp.exists():
            for rec in json.loads(jp.read_text("utf-8")):
                s = rec.get("sha256")
                if s:
                    shas.add(s)
    return shas


# ---------------------------------------------------------------- candidates

def build_candidates(pool_per_act_extra: float = 1.4) -> list[dict]:
    print(f"[sha] hashing prior EP39/40/41 factory ...", flush=True)
    prior = prior_sha_universe()
    print(f"[sha] {len(prior)} prior factory fingerprints to avoid", flush=True)

    # group shelf mp4 by subtype, on-theme only
    by_sub: dict[str, list[str]] = {}
    for name in sorted(p.name for p in SHELF.iterdir() if p.suffix.lower() == ".mp4"):
        sub = subtype_of(name)
        if theme_match(sub) is None:
            continue
        by_sub.setdefault(sub, []).append(name)

    quota = {a: int(round(n * pool_per_act_extra)) for a, n in ACT_QUOTA.items()}
    picked: list[dict] = []
    per_act: dict[str, int] = {a: 0 for a in ACT_QUOTA}
    per_sub: dict[str, int] = {}
    sil_count = 0
    skipped_sha = 0

    # round-robin over subtypes so the pool is varied, not front-loaded
    subs = sorted(by_sub)
    idx = {s: 0 for s in subs}
    active = True
    while active and len(picked) < sum(quota.values()):
        active = False
        for sub in subs:
            act = theme_match(sub)
            if per_act[act] >= quota[act]:
                continue
            if per_sub.get(sub, 0) >= SUBTYPE_CAP:
                continue
            is_sil = "silhouette" in sub or "crowd" in sub
            if is_sil and sil_count >= SILHOUETTE_CAP:
                continue
            names = by_sub[sub]
            while idx[sub] < len(names):
                name = names[idx[sub]]
                idx[sub] += 1
                p = SHELF / name
                sha = sha256_file(p)
                if sha in prior:
                    skipped_sha += 1
                    continue
                d = probe_dur(p)
                if d < 3.0:            # too short to cover a ~3.2s cut cleanly
                    continue
                picked.append({
                    "asset_id": f"AF-{name.split('__')[0].replace('AF-', '')}",
                    "basename": name,
                    "subtype": sub,
                    "act_suggestion": act,
                    "duration_sec": d,
                    "sha256": sha,
                    "public_path": f"caniglia/factory/{name}",
                    "shelf_path": str(p),
                    "eyeballed_content": "",   # filled after human contact-sheet review
                })
                per_act[act] += 1
                per_sub[sub] = per_sub.get(sub, 0) + 1
                if is_sil:
                    sil_count += 1
                active = True
                break
    print(f"[candidates] {len(picked)} picked  (sha-skipped {skipped_sha})  acts={per_act}")
    return picked


def load_frame(p: Path):
    from PIL import Image
    proc = subprocess.run(["ffmpeg", "-v", "error", "-ss", "1", "-i", str(p),
                           "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return Image.open(io.BytesIO(proc.stdout)).convert("RGB")


def contact_sheets(cands: list[dict], tag: str) -> list[Path]:
    from PIL import Image, ImageDraw, ImageFont
    COLS, ROWS, THUMB_W, LABEL_H, PAD = 5, 4, 360, 30, 6
    thumb_h = int(THUMB_W * 9 / 16)
    cell_w, cell_h, head = THUMB_W + PAD, thumb_h + LABEL_H + PAD, 34

    def font(sz):
        for n in ("arial.ttf", "DejaVuSans.ttf"):
            try:
                return ImageFont.truetype(n, sz)
            except Exception:
                continue
        return ImageFont.load_default()

    per = COLS * ROWS
    sheets = [cands[i:i + per] for i in range(0, len(cands), per)]
    written: list[Path] = []
    for si, chunk in enumerate(sheets, 1):
        W = COLS * cell_w + PAD
        H = head + ROWS * cell_h + PAD
        canvas = Image.new("RGB", (W, H), (18, 18, 22))
        draw = ImageDraw.Draw(canvas)
        draw.text((PAD, 8), f"caniglia factory candidates — sheet {si}/{len(sheets)} ({len(cands)} total)",
                  fill=(235, 235, 240), font=font(20))
        f_lbl = font(12)
        for i, cand in enumerate(chunk):
            gi = (si - 1) * per + i
            r, c = divmod(i, COLS)
            x, y = PAD + c * cell_w, head + r * cell_h
            try:
                im = load_frame(Path(cand["shelf_path"]))
                im.thumbnail((THUMB_W, thumb_h))
                tile = Image.new("RGB", (THUMB_W, thumb_h), (0, 0, 0))
                tile.paste(im, ((THUMB_W - im.width) // 2, (thumb_h - im.height) // 2))
                canvas.paste(tile, (x, y))
            except Exception:
                draw.rectangle([x, y, x + THUMB_W, y + thumb_h], fill=(60, 20, 20))
                draw.text((x + 6, y + 6), "UNREADABLE", fill=(255, 180, 180), font=f_lbl)
            lbl = f"[{gi}] {cand['subtype'][:34]} {cand['act_suggestion']}"
            draw.rectangle([x, y + thumb_h, x + THUMB_W, y + thumb_h + LABEL_H], fill=(30, 30, 36))
            draw.text((x + 4, y + thumb_h + 4), lbl, fill=(210, 210, 220), font=f_lbl)
        out = QC / f"caniglia_factory_candidates_{si:02d}.png"
        out.parent.mkdir(parents=True, exist_ok=True)
        canvas.save(out)
        written.append(out)
        print(f"  wrote {out} ({len(chunk)} tiles)")
    return written


# Subtypes proven clean & on-theme on the first eyeball pass -- draw top-up clips only from
# these (deep pools on the shelf), excluding basenames already reviewed.
STRONG_SUBS = [
    "courtroom_interior", "courtroom_empty_wide", "courtroom_gavel_block_macro",
    "documents_on_desk", "case_files_stack_desk", "stacked_legal_documents",
    "front_door_house", "suburban_house_exterior_night", "open_door_bright_light",
    "bank_building_columns", "federal_building_columns_night", "supreme_court_building",
    "courthouse_steps", "law_library_books", "candle_in_dark",
    "city_traffic_night_long_exposure", "highway_night_long_exposure",
    "snowy_street_night", "rain_on_window_night", "police_car_lights_night",
    "ambulance_lights_at_night", "abstract_dark_background", "dark_cinematic_background",
    "concrete_wall_texture_dark",
]


def build_topup(seen: set[str], want: int = 34, cap_per_sub: int = 3) -> list[dict]:
    prior = prior_sha_universe()
    by_sub: dict[str, list[str]] = {}
    for name in sorted(p.name for p in SHELF.iterdir() if p.suffix.lower() == ".mp4"):
        sub = subtype_of(name)
        if sub in STRONG_SUBS and name not in seen:
            by_sub.setdefault(sub, []).append(name)
    picked: list[dict] = []
    per_sub: dict[str, int] = {}
    subs = [s for s in STRONG_SUBS if s in by_sub]
    idx = {s: 0 for s in subs}
    active = True
    while active and len(picked) < want:
        active = False
        for sub in subs:
            if per_sub.get(sub, 0) >= cap_per_sub:
                continue
            names = by_sub[sub]
            while idx[sub] < len(names):
                name = names[idx[sub]]
                idx[sub] += 1
                p = SHELF / name
                sha = sha256_file(p)
                if sha in prior:
                    continue
                d = probe_dur(p)
                if d < 3.0:
                    continue
                picked.append({
                    "asset_id": f"AF-{name.split('__')[0].replace('AF-', '')}",
                    "basename": name, "subtype": sub, "act_suggestion": theme_match(sub),
                    "duration_sec": d, "sha256": sha,
                    "public_path": f"caniglia/factory/{name}", "shelf_path": str(p),
                    "eyeballed_content": "",
                })
                per_sub[sub] = per_sub.get(sub, 0) + 1
                active = True
                break
            if len(picked) >= want:
                break
    return picked


def contact_sheets_range(merged: list[dict], start: int, end: int, tag: str) -> list[Path]:
    """Render tiles for merged[start:end], labeling each with its GLOBAL index."""
    from PIL import Image, ImageDraw, ImageFont
    COLS, ROWS, THUMB_W, LABEL_H, PAD = 5, 4, 360, 30, 6
    thumb_h = int(THUMB_W * 9 / 16)
    cell_w, cell_h, head = THUMB_W + PAD, thumb_h + LABEL_H + PAD, 34

    def font(sz):
        for n in ("arial.ttf", "DejaVuSans.ttf"):
            try:
                return ImageFont.truetype(n, sz)
            except Exception:
                continue
        return ImageFont.load_default()

    items = list(range(start, end))
    per = COLS * ROWS
    pages = [items[i:i + per] for i in range(0, len(items), per)]
    written: list[Path] = []
    for si, page in enumerate(pages, 1):
        W, H = COLS * cell_w + PAD, head + ROWS * cell_h + PAD
        canvas = Image.new("RGB", (W, H), (18, 18, 22))
        draw = ImageDraw.Draw(canvas)
        draw.text((PAD, 8), f"caniglia factory {tag} — sheet {si}/{len(pages)} (global idx {start}..{end-1})",
                  fill=(235, 235, 240), font=font(20))
        f_lbl = font(12)
        for i, gi in enumerate(page):
            cand = merged[gi]
            r, c = divmod(i, COLS)
            x, y = PAD + c * cell_w, head + r * cell_h
            try:
                im = load_frame(Path(cand["shelf_path"]))
                im.thumbnail((THUMB_W, thumb_h))
                tile = Image.new("RGB", (THUMB_W, thumb_h), (0, 0, 0))
                tile.paste(im, ((THUMB_W - im.width) // 2, (thumb_h - im.height) // 2))
                canvas.paste(tile, (x, y))
            except Exception:
                draw.rectangle([x, y, x + THUMB_W, y + thumb_h], fill=(60, 20, 20))
                draw.text((x + 6, y + 6), "UNREADABLE", fill=(255, 180, 180), font=f_lbl)
            lbl = f"[{gi}] {cand['subtype'][:34]} {cand['act_suggestion']}"
            draw.rectangle([x, y + thumb_h, x + THUMB_W, y + thumb_h + LABEL_H], fill=(30, 30, 36))
            draw.text((x + 4, y + thumb_h + 4), lbl, fill=(210, 210, 220), font=f_lbl)
        out = QC / f"caniglia_factory_{tag}_{si:02d}.png"
        canvas.save(out)
        written.append(out)
        print(f"  wrote {out} ({len(page)} tiles)")
    return written


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", choices=("candidates", "topup", "finalize"), required=True)
    ap.add_argument("--decision", type=Path, help="finalize: JSON {index: eyeballed_content} of KEEPERS")
    a = ap.parse_args()

    if a.phase == "topup":
        cands = json.loads(CANDIDATES_JSON.read_text("utf-8"))
        seen = {c["basename"] for c in cands}
        extra = build_topup(seen)
        outp = QC / "caniglia_factory_topup.v001.json"
        outp.write_text(json.dumps(extra, ensure_ascii=False, indent=2), "utf-8")
        print(f"[topup] {len(extra)} fresh candidates -> {outp}")
        # contact-sheet the top-up with global indices offset by len(cands)
        merged = cands + extra
        sheets = contact_sheets_range(merged, len(cands), len(merged), "topup")
        return 0

    if a.phase == "candidates":
        cands = build_candidates()
        CANDIDATES_JSON.parent.mkdir(parents=True, exist_ok=True)
        CANDIDATES_JSON.write_text(json.dumps(cands, ensure_ascii=False, indent=2), "utf-8")
        print(f"wrote {CANDIDATES_JSON} ({len(cands)} candidates)")
        contact_sheets(cands, "caniglia")
        return 0

    # finalize: keep only eyeballed indices, attach eyeballed_content, cap at 93.
    # Global indices span the merged [candidates ++ topup] list (topup starts at len(candidates)).
    cands = json.loads(CANDIDATES_JSON.read_text("utf-8"))
    topup_path = QC / "caniglia_factory_topup.v001.json"
    if topup_path.exists():
        cands = cands + json.loads(topup_path.read_text("utf-8"))
    decision = json.loads(a.decision.read_text("utf-8"))
    keepers: list[dict] = []
    for idx_s, content in decision.items():
        idx = int(idx_s)
        c = dict(cands[idx])
        c["eyeballed_content"] = content
        c["qc"] = {"reviewed": True, "on_theme": True, "no_watermark": True,
                   "no_recognizable_person": True, "no_cartoon": True,
                   "label_matches_content": True, "has_readable_text": False, "notes": ""}
        keepers.append(c)
    if len(keepers) != TARGET:
        print(f"WARNING: {len(keepers)} keepers != target {TARGET}")
    # verify sha uniqueness within selection AND zero overlap with EP39/40/41
    shas = [k["sha256"] for k in keepers]
    assert len(shas) == len(set(shas)), "duplicate sha in selection"
    print("[sha] hashing prior EP39/40/41 factory for overlap audit ...", flush=True)
    prior = prior_sha_universe()
    overlap = sorted(set(shas) & prior)
    assert not overlap, f"SHA OVERLAP with prior episodes: {overlap}"
    for k in keepers:
        assert k["eyeballed_content"].strip(), f"empty eyeballed_content for {k['basename']}"
    SELECTED_JSON.write_text(json.dumps(keepers, ensure_ascii=False, indent=2), "utf-8")
    print(f"wrote {SELECTED_JSON} ({len(keepers)} clips) sha-unique={len(set(shas))} "
          f"prior_overlap={len(overlap)} (prior universe {len(prior)})")
    import collections
    print("acts:", dict(collections.Counter(k["act_suggestion"] for k in keepers)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
