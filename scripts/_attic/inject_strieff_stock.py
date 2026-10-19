#!/usr/bin/env python3
"""EP49 strieff: weave REAL graded stock cutaways into the CaseFilm cutlist.

Owner 2026-07-24: "せっかくたくさんダウンロードしたんだから意味のある所に使ってほしい" +
"動画に関しては無料素材でまかなえるならそれも使ってほしい" (stock-first for motion, incl.
human/action beats). This runs AFTER build_strieff_film.py (the audited producer) and rewrites
selected cuts in-place to point at color-graded stock clips (remotion/public/strieff/stock/*.mp4,
graded to the noir look — NO haze/scanlines). Content is matched to the narration beat under it.

It NEVER touches the clean i2v 'motion' clips (M*_rife) and NEVER touches the reserved doorway
person slot (body ~5-9s) — that is a HUMAN/MOTION GAP left for the SDXL->Wan i2v follow-up.

Each replaced cut becomes kind=footage, treatment=footage, startFrom=0 (CaseFilm honors a per-cut
startFrom so short stock clips start at their first frame). Cut count / timing are unchanged, so
all timeline math (BGM, AE offsets) stays valid. Idempotent: re-run after a fresh producer build.

Usage: py -3.11 scripts/inject_strieff_stock.py [--dry-run]
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(r"C:\Users\aab15\Documents\prime-documentary")
FILM = ROOT / "remotion" / "src" / "data" / "strieff_film.json"
PUB_FILM = ROOT / "remotion" / "public" / "strieff" / "film_data.v001.json"
STOCK_DIR = ROOT / "remotion" / "public" / "strieff" / "stock"

# (body_time_sec, stock_basename, narration beat note). Times are body/narration-relative
# (same clock as cuts[].start). The covering cut at each time is retitled to the stock clip;
# if that cut is a 'motion' i2v (kept clean) or already stocked, the nearest img/factory cut is used.
PLACEMENTS = [
    # ---- HOOK (0-62): tip -> stakeout -> stop -> ID/radio -> warrant -> arrest -> meth ----
    (16.0, "st_cctv_watch", "a detective has been watching that house"),
    (27.0, "st_police_night", "he walks over and tells him to stop"),
    (34.0, "st_celltower", "reads his ID to a dispatcher over the radio"),
    (40.0, "st_records_server", "a name comes back with an outstanding warrant"),
    # 46.5s "the man is arrested" -> HUMAN/MOTION GAP (SDXL): no stock arrest clip fits
    # (only a pink-neon money composite + a green-screen silhouette). Left for the i2v follow-up.
    (49.5, "st_drugs_evidence", "the search turns up evidence (forensic)"),
    (56.0, "st_phone_records", "runs your name / used against you in court"),
    # ---- OP (64-121): the exclusionary rule, Strieff 2016, attenuation ----
    (68.0, "st_lawbooks", "a rule in American law"),
    (72.5, "st_scales", "search you illegally, evidence is normally thrown out"),
    (83.0, "st_document", "the exclusionary rule"),
    (96.0, "st_jail", "the man was convicted"),
    (106.5, "st_courthouse", "the case is Utah v. Strieff, decided in 2016"),
    (111.0, "st_capitol", "the attenuation doctrine"),
    # ---- ACT_1 (123-249): the facts, the illegal stop ----
    (130.0, "st_cctv_watch", "Detective Fackrell got an anonymous tip"),
    (136.0, "st_house_night", "watched the place, on and off, for about a week"),
    (141.0, "st_feet_walking", "a steady stream of people making short visits"),
    (154.0, "st_feet_walking", "Strieff walked out and headed across a parking lot"),
    (160.0, "st_police_night", "he stopped him and asked what he was doing"),
    (172.0, "st_document", "we keep to what the record says"),
    (205.0, "st_tension_abstract", "no reasonable suspicion — the stop was not legal"),
    (235.0, "st_courthouse", "the Terry-stop rule"),
    # ---- ACT_2 (251-379): exclusionary rule, attenuation, Brown factors ----
    (268.0, "st_scales", "fruit of the poisonous tree"),
    (300.0, "st_lawbooks", "the attenuation exception"),
    (330.0, "st_document", "the Brown v. Illinois factors"),
    (355.0, "st_judge_gavel", "did the warrant break the chain?"),
    (375.0, "st_night_street", "the warrant intervenes"),
    # ---- ACT_3 (381-570): the ruling, 5-3, the dissents ----
    (398.0, "st_courthouse", "the ruling"),
    (432.0, "st_judge_gavel", "5-3, decided 2016"),
    (458.0, "st_capitol", "an 8-justice court, Scalia's seat empty"),
    (485.0, "st_tension_abstract", "Sotomayor, dissenting — a carceral state"),
    (518.0, "st_jail", "Kagan, dissenting — the incentive increases"),
    (548.0, "st_courthouse", "the evidence stayed in"),
    # ---- ENDING (572-687): outstanding warrants, the stop becomes almost free ----
    (588.0, "st_records_server", "outstanding warrants exist across the country"),
    (612.0, "st_night_street", "an illegal stop becomes almost free"),
    (640.0, "st_cctv_watch", "a door held open"),
    (666.0, "st_house_night", "closing"),
]


def covering_index(cuts, t):
    for i, c in enumerate(cuts):
        if c["start"] <= t < c["start"] + c["dur"]:
            return i
    # clamp to nearest
    return min(range(len(cuts)), key=lambda i: abs(cuts[i]["start"] - t))


def pick_target(cuts, t, stocked):
    """Return an index to replace: the covering cut, unless it is a kept i2v 'motion' clip or
    already stocked — then the nearest img/factory cut not yet stocked (search outward)."""
    base = covering_index(cuts, t)

    def ok(i):
        c = cuts[i]
        src = c["src"].replace("\\", "/")
        if i in stocked:
            return False
        if "/motion/" in src:          # keep the clean i2v clips
            return False
        return True

    if ok(base):
        return base
    for d in range(1, 8):
        for i in (base - d, base + d):
            if 0 <= i < len(cuts) and ok(i):
                return i
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    film = json.loads(FILM.read_text(encoding="utf-8"))
    cuts = film["cuts"]

    missing = [b for _, b, _ in PLACEMENTS if not (STOCK_DIR / f"{b}.mp4").exists()]
    if missing:
        print(f"WARN {len(set(missing))} graded stock clips not staged yet: "
              f"{sorted(set(missing))}", file=sys.stderr)

    stocked: set[int] = set()
    applied = []
    skipped = []
    for t, base, note in PLACEMENTS:
        idx = pick_target(cuts, t, stocked)
        if idx is None:
            skipped.append((t, base, note))
            continue
        c = cuts[idx]
        old = c["src"]
        c["src"] = f"strieff/stock/{base}.mp4"
        c["kind"] = "footage"
        c["treatment"] = "footage"
        c["startFrom"] = 0
        c["stock_note"] = note
        stocked.add(idx)
        applied.append((idx, round(c["start"], 1), base, old.split("/")[-1], note))

    # recount
    def kindof(c):
        s = c["src"].replace("\\", "/")
        if "/stock/" in s:
            return "stock"
        if "/motion/" in s:
            return "motion"
        if "/factory/" in s:
            return "factory"
        return "still" if c["kind"] == "img" else "footage"
    from collections import Counter
    counts = Counter(kindof(c) for c in cuts)
    stock_time = sum(c["dur"] for c in cuts if "/stock/" in c["src"].replace("\\", "/"))
    motion_time = sum(c["dur"] for c in cuts if c["kind"] != "img")
    total = film["narrationSeconds"]

    print(f"[inject] applied {len(applied)} stock cutaways, skipped {len(skipped)}")
    print(f"[inject] cut mix: {dict(counts)}  (total {len(cuts)})")
    print(f"[inject] stock time {stock_time:.0f}s = {stock_time/total*100:.1f}% of body; "
          f"moving time {motion_time/total*100:.1f}%")
    for idx, st, base, old, note in applied:
        print(f"   cut-{idx:03d} @{st:>6.1f}s  {base:<20} <- {old:<34} | {note}")
    if skipped:
        print("  SKIPPED (no free cut near time):")
        for t, base, note in skipped:
            print(f"   @{t:.1f}s {base} | {note}")

    if args.dry_run:
        print("[inject] --dry-run: not writing")
        return 0
    payload = json.dumps(film, ensure_ascii=False, indent=2)
    FILM.write_text(payload, encoding="utf-8")
    PUB_FILM.write_text(payload, encoding="utf-8")
    print(f"[inject] wrote {FILM}")
    print(f"[inject] wrote {PUB_FILM}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
