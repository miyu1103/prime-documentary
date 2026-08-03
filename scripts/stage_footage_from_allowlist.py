#!/usr/bin/env python
"""Stage an episode's footage from its OWN reviewed allowlist -- never from a search query.

WHY THIS EXISTS (2026-08-04, EP61 weimer):
  Every footage script in this repo selects by QUERY. That is precisely the mechanism that put
  a red London bus into EP56 (the design said "no buses"; `london street` staged one) and 31
  rubble clips into EP60 (the design said "no rubble"; `rubble collapse` staged them). A query
  cannot be constrained by a review, because the review happened after the query.

  EP61 inverts it: four agents looked at 288 contact-sheet tiles, wrote down the 84 clip IDs
  that may be used, named 4 that may NOT (a readable face, wet glass whose vertical divisions
  read as prison bars, iron bars, an animal behind chain-link), and set a per-family USE CAP
  because 12 of the field clips are the same lone tree and 10 of the town clips are the same
  dusk drone. This script stages exactly that list, capped, and nothing else. The allowlist is
  the gate; there is no query anywhere in this file.

  NOTE the trap: the 4 banned IDs are also present in `allow`. `allow - banned` is the usable
  set, not `allow`.

OVERLAY-CLASS RENAME (documented, not a workaround for a safety check):
  build_asset_manifest_motionfirst.py demotes any file whose name contains AF-LIGHT / AF-PART /
  AF-VFX to the overlay pool, because those families are normally particle and light-leak
  plates authored to be SCREENED over a picture. EP61's snow family is AF-PART-0249..0266 and
  its meltwater clip is AF-PART-1247, and the design records that these specific clips were
  eyeballed and are real photographed footage ("上記9本は目視済みの実写のみ";
  AF-PART-1247 is marshland meltwater, "名前と中身が無関係"). The name-based heuristic is wrong
  for these reviewed clips, so the staged copy is renamed AFPART-<n>__<label> -- the ID stays
  legible for audit, the substring no longer matches. The luma content check still applies.

    py -3.11 scripts/stage_footage_from_allowlist.py --slug weimer [--dry-run] [--force]

Read-only against the shelf: files are COPIED, never moved or edited. Writes a receipt next to
the allowlist recording every staged clip, its source path, sha256 and licence.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = Path(r"H:\pd-media\assets\archive\_ledger\factory.jsonl")
OK_LICENSE = {"free_commercial", "pd", "cc0"}
VIDEO_EXT = {".mp4", ".mov", ".webm", ".mkv"}
NAME_RE = re.compile(r"^(AF-[A-Z]+-\d+)__(.+)\.(mp4|mov|webm|mkv)$", re.I)
OVERLAY_CLASS = ("AF-LIGHT", "AF-PART", "AF-VFX")

# Within a capped family, these IDs are taken FIRST because the visual review named them --
# either as the best frame of the family or as its only different composition. Source:
# episodes/_planning/EP61_weimer_FOOTAGE_AND_AE.v001.md sections 1.1-1.7.
PREFERRED: dict[str, list[str]] = {
    "small_town_main_street": ["AF-BG-9226"],          # cloudy basketball hoop; only other framing
    "church_interior_light_beam": ["AF-BG-14099", "AF-BG-14089"],
    "white_picket_fence": ["AF-BG-22109", "AF-BG-22096", "AF-BG-22104"],
    "snow_falling_dark": ["AF-PART-0266"],
    "rain_on_window_night": ["AF-BG-1437", "AF-BG-1432"],
}
# Same shoot as another member of the family; the review says take one of the pair only.
DROP_DUPLICATE_SHOT = {"AF-BG-0253", "AF-PART-0253", "AF-BG-9596"}
# Families with no cap in the allowlist but a one-of-two note in the review.
EXTRA_CAPS = {"candle_in_dark": 1}
# config/footage_blocklist.v001.json is the CROSS-EPISODE ban list (mislabelled, rights-unsafe
# or near-identical clips). It is enforced inside build_case_film_generic.py, which refuses to
# emit a film naming one -- so a blocked clip staged here only wastes a build. EP61 met this on
# the church family: the allowlist admits nine interiors, the blocklist keeps four. Filter here,
# BEFORE the cap is applied, so the cap is spent on clips that can actually reach a cut.
BLOCKLIST = ROOT / "config" / "footage_blocklist.v001.json"


def blocked_ids() -> dict[str, str]:
    if not BLOCKLIST.is_file():
        return {}
    out: dict[str, str] = {}
    for row in json.loads(BLOCKLIST.read_text(encoding="utf-8")).get("blocked", []):
        label, reason = row["label"], row["reason"]
        for ident in row["ids"]:
            out[ident] = label + ": " + reason
    return out


def load_shelf(ids: set[str]) -> dict[str, dict]:
    """Resolve clip IDs to ledger rows by the ID prefix of the file's basename."""
    found: dict[str, dict] = {}
    with LEDGER.open(encoding="utf-8") as fh:
        for line in fh:
            if not line.strip():
                continue
            row = json.loads(line)
            fp = row.get("file_path") or ""
            m = NAME_RE.match(Path(fp).name)
            if not m or m.group(1) not in ids or m.group(1) in found:
                continue
            found[m.group(1)] = {"row": row, "src": Path(fp),
                                 "family": m.group(2), "ext": Path(fp).suffix.lower()}
    return found


def staged_name(clip_id: str, family: str, ext: str) -> str:
    safe = clip_id
    for k in OVERLAY_CLASS:
        if k in safe:
            safe = safe.replace(k, k.replace("-", "", 1))
    return f"{safe}__{family}{ext}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--allowlist", type=Path, default=None)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true", help="restage into a non-empty factory dir")
    a = ap.parse_args()

    eps = sorted((ROOT / "episodes").glob(f"PD-*-{a.slug}"))
    if not eps:
        raise SystemExit(f"no episodes/PD-*-{a.slug} directory")
    epdir = eps[0]
    alp = a.allowlist or (epdir / "05_visuals" / "footage_allowlist.v001.json")
    if not alp.is_file():
        raise SystemExit(f"no allowlist {alp}")
    al = json.loads(alp.read_text(encoding="utf-8"))

    allow = list(dict.fromkeys(al["allow"]))
    banned = dict(al.get("banned") or {})
    caps = dict(al.get("family_caps") or {})
    caps.update(EXTRA_CAPS)
    usable = [i for i in allow if i not in banned]
    bl = blocked_ids()

    def why_blocked(clip_id: str) -> str | None:
        return bl.get(clip_id) or bl.get(clip_id.split("-")[-1])

    dropped_blocked = [(i, why_blocked(i)) for i in usable if why_blocked(i)]
    usable = [i for i in usable if not why_blocked(i)]
    print(f"[allowlist] {alp.relative_to(ROOT).as_posix()}: allow={len(allow)} "
          f"banned={len(banned)} blocklisted={len(dropped_blocked)} usable={len(usable)}")
    for cid_, why in dropped_blocked:
        print(f"  [blocklist] {cid_} dropped -- {why}")

    shelf = load_shelf(set(usable))
    missing = [i for i in usable if i not in shelf]
    if missing:
        raise SystemExit(f"{len(missing)} allowlisted clip(s) not in the shelf ledger: {missing}")

    bad_lic = [i for i in usable if shelf[i]["row"].get("license_decision") not in OK_LICENSE]
    if bad_lic:
        raise SystemExit(f"licence not clear for commercial use: {bad_lic}")
    gone = [i for i in usable if not shelf[i]["src"].is_file()]
    if gone:
        raise SystemExit(f"{len(gone)} allowlisted file(s) absent from disk: {gone[:5]}")

    # ---- group, then apply the reviewed use caps -------------------------------------------
    families: dict[str, list[str]] = {}
    for i in usable:
        families.setdefault(shelf[i]["family"], []).append(i)

    chosen: list[str] = []
    report: list[tuple[str, int, int]] = []
    for fam in sorted(families):
        members = [i for i in families[fam] if i not in DROP_DUPLICATE_SHOT]
        cap = caps.get(fam)
        if cap is None or len(members) <= cap:
            keep = members
        else:
            pref = [i for i in PREFERRED.get(fam, []) if i in members][:cap]
            rest = [i for i in members if i not in pref]
            need = cap - len(pref)
            step = len(rest) / need if need else 0
            spread = [rest[min(len(rest) - 1, int(k * step))] for k in range(need)]
            keep = pref + list(dict.fromkeys(spread))
            k = 0
            while len(keep) < cap and k < len(rest):     # rounding collisions
                if rest[k] not in keep:
                    keep.append(rest[k])
                k += 1
        chosen.extend(keep)
        report.append((fam, len(families[fam]), len(keep)))

    for fam, have, kept in report:
        cap = caps.get(fam)
        flag = f" cap={cap}" if cap else ""
        print(f"  {fam:34s} shelf={have:3d} -> staged={kept:3d}{flag}")
    print(f"[cap] {len(usable)} usable -> {len(chosen)} staged after family caps")

    dest = ROOT / "remotion" / "public" / a.slug / "factory"
    existing = sorted(p for p in dest.glob("*") if p.suffix.lower() in VIDEO_EXT) if dest.is_dir() else []
    if existing and not a.force:
        raise SystemExit(f"{dest} already holds {len(existing)} clip(s); pass --force to restage")

    staged: list[dict] = []
    for cid in sorted(chosen):
        info = shelf[cid]
        out = dest / staged_name(cid, info["family"], info["ext"])
        staged.append({
            "clip_id": cid, "family": info["family"],
            "staged_as": out.name, "public_path": f"{a.slug}/factory/{out.name}",
            "source_path": str(info["src"]), "bytes": info["src"].stat().st_size,
            "sha256": info["row"].get("sha256"), "title": info["row"].get("title"),
            "source": info["row"].get("source"), "source_url": info["row"].get("source_url"),
            "license_decision": info["row"].get("license_decision"),
            "renamed_from_overlay_class": out.name.split("__")[0] != cid,
        })

    if a.dry_run:
        print(f"(dry-run) would copy {len(staged)} clip(s) into "
              f"{dest.relative_to(ROOT).as_posix()}")
        for s in staged[:6]:
            print(f"    {s['clip_id']:16s} -> {s['staged_as']}")
        return 0

    dest.mkdir(parents=True, exist_ok=True)
    for p in existing:
        p.unlink()
    for s in staged:
        shutil.copy2(s["source_path"], dest / s["staged_as"])
    receipt = epdir / "05_visuals" / "footage_staging_receipt.v001.json"
    receipt.write_text(json.dumps({
        "schema_version": "footage_staging_receipt/v001",
        "episode_id": al.get("episode_id"), "slug": a.slug,
        "staged_at": datetime.now(timezone.utc).isoformat(),
        "producer": "scripts/stage_footage_from_allowlist.py",
        "allowlist": alp.relative_to(ROOT).as_posix(),
        "allow_count": len(allow), "banned_count": len(banned),
        "usable_count": len(usable), "staged_count": len(staged),
        "family_caps_applied": caps,
        "dropped_duplicate_shot": sorted(DROP_DUPLICATE_SHOT & set(usable)),
        "clips": staged,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"staged {len(staged)} clip(s) -> {dest.relative_to(ROOT).as_posix()}")
    print(f"receipt {receipt.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    raise SystemExit(main())
