#!/usr/bin/env python3
r"""Record EP76 morandi's pool-frame review: what survived a full-resolution look and what did not.

WHAT THIS RECORDS, AND WHY IT DISAGREES WITH THE EARLIER RECORD. 61 clips were staged into
`remotion/public/morandi/factory` and logged in `runs/qc/morandi_footage_reviewed.v001.json` as
"looked at on a labelled contact sheet". They had been -- but on the ARCHIVE sheets, whose tiles are
about 400px, and where a clip is represented by a single frame. `check_pool_frames.py` re-sampled
every staged clip across its own duration and wrote 21 sheets at a size where the frame can actually
be read. All 21 were read. 32 of the 61 do not survive.

Most of the 32 are clips THIS reviewer accepted on the earlier sheets. That is the finding, not an
aside: MO-33068304 turns out to have three lines of legible GERMAN prose typed on the page, in a film
whose entire argument is about what documents said; MO-32244801 has foreign lettering on a worker's
vest; MO-34964490/501 have a Shell forecourt; MO-29927991 has EVERGREEN and CMA CGM readable on the
cranes; MO-29089174 is an American freeway with a conventional-cab tractor, and the spec bars the
American register outright. None of that is visible at 400px. It is the same lesson EP76's plate
review already recorded in two places -- a thumbnail is not evidence -- arriving a second time.

THE BAR APPLIED. episode_spec.v001.json declares era_setting Genoa/Liguria 1962-2026 and bars the
American, British and Asian registers as well as holiday-Italy. A clip is rejected when the frame
reveals WHERE or WHEN it is and the answer is not Genoa; when a brand, a language or a number plate
is readable; when a face is identifiable and the person has no business in this record; or when the
clip serves no beat in the film and would be atmosphere poured over narration
(`feedback_visual_narration_meaning_match`).

Usage:
    py -3.11 scripts/write_morandi_clip_verdicts.py [--dry-run]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FACTORY = ROOT / "remotion" / "public" / "morandi" / "factory"
OUT = ROOT / "runs" / "qc" / "morandi_clip_verdicts.v001.json"
REVIEWED_AT = "2026-08-22"
REVIEWER = "claude (EP76 asset lane), pool-frame review of all 21 sheets"

ACCEPT: dict[str, str] = {
    "15161525": "raindrops on dark glass at night; abstract, cold, no place cue",
    "16922448": "a typewriter on a table by a shuttered window, dim; period-plausible, no readable text",
    "19217896": "a dim corridor under two strip lights; anonymous, serves the rooms register",
    "19791475": "a typewriter in warm shallow focus; no readable text (grade cooler in the cut)",
    "20413417": "hands working a mechanical adding machine -- a machine that produces a number, "
                "which is the film's controlling idea, not decoration",
    "27732551": "rusted chain and hasp in close-up; rust is the film's core material",
    "27732553": "rusted iron gate, chain and lock; same register",
    "28110696": "raindrops on a window at night, very dark; abstract",
    "28924398": "night motorway drive, headlights streaking; no signage, no place cue",
    "29269079": "a distant road at night reduced to a line of light; place unreadable",
    "29900465": "rain and a single street light; abstract",
    "29904000": "top-down aerial of a container berth; NO legible branding in any sample, unlike its "
                "sibling 29927991. Genoa's valley is a working port, so this is on-subject",
    "30117908": "anonymous hands turning old paper in a dim room, text out of focus -- the film's "
                "own register, and the reason the paperwork beats have anything to cut to",
    "30117913": "a person writing at a desk stacked with paper, dim, face not visible",
    "30281179": "aerial container terminal under OVERCAST light; matches the palette",
    "30728494": "wet road ahead through a windscreen with a lorry in front, flat grey -- 'the "
                "ordinary drive'. No signage or plate readable in any sample",
    "30911562": "close on a coarse concrete surface; the film's central material",
    "31033366": "a vintage typewriter being struck, close; carriage text not resolvable",
    "31042229": "city lights thrown out of focus behind a rain-covered window",
    "31940806": "night drive in rain, windscreen; signage present but illegible in every sample",
    "32086252": "water beading on a pale cold surface; abstract texture",
    "33938640": "raindrops on a window pane, dark interior edge",
    "33938711": "raindrops on glass, cold blue",
    "33938713": "raindrops on glass, moody blue",
    "34576517": "one anonymous figure walking away down a wet covered footbridge; cold, symmetrical, "
                "face never visible. Reads as crossing, not as a named person",
    "35039489": "night roadworks beside a barrier: excavation, plant, no brand, no face",
    "37137791": "a lamp and its reflection on still water in fog at a quiet dock",
    "37596049": "white overalls sweeping a dim workshop floor, legs only, no face, no brand",
    "37751603": "a large concrete interior in monochrome, symmetrical and brutalist; strong for the "
                "structure beats (it IS monochrome -- use deliberately or grade)",
}

REJECT: dict[str, str] = {
    "15622734": "a modern dotted bullet-journal notebook and a green gel pen; the era is wrong and "
                "the cursive is close to readable",
    "16393893": "labelled 'construction worker on a roof'; it is an AERIAL of a TROPICAL site -- "
                "palms are in frame 5. Wrong region entirely",
    "19810376": "golden-hour underpass with joggers, cyclists and a dog walker; a lifestyle clip in "
                "a film whose light is overcast Genoa, and it serves no beat",
    "27860328": "hands wearing two large gold rings filling in a ruled docket beside a red plastic "
                "crate; reads as a market ledger, and the jewellery makes the person specific",
    "28692145": "modern glass towers and a tower crane under a bright blue sky",
    "29014199": "modern high-rise construction, blue sky, sunny; wrong era and wrong light",
    "29089174": "an AMERICAN freeway -- a conventional-cab tractor unit and US pickups across five "
                "lanes. episode_spec bars the American register outright",
    "29927991": "EVERGREEN and CMA CGM are readable on the cranes and sheds; corporate branding on "
                "screen in a film about corporate responsibility",
    "30331619": "a red hoist on a modern residential tower against blue sky",
    "30339959": "a sodium-orange foggy alley; pure mood, attached to no beat",
    "30814424": "rain on a wooden cafe table; the film's rain falls on concrete, and a cafe reads "
                "as leisure",
    "30850349": "Indian city traffic -- flyover, vehicle mix and number plates are unmistakable",
    "31352807": "a forklift operator whose face is lit and identifiable; no beat needs him, and "
                "this film assigns blame",
    "32062391": "a teal-and-green umbrella on bright grass; the palette is the opposite of the film's",
    "32228166": "modern hi-vis scaffolding work, faces visible, wrong region",
    "32243439": "a modern factory in blue light, blue helmets, modern PPE",
    "32244795": "a modern East Asian site walk-round in hi-vis",
    "32244801": "foreign lettering readable on the worker's vest; modern East Asian site",
    "32244802": "modern East Asian rebar work, hi-vis, bright",
    "33068304": "THE WORST OF THE SET: three lines of GERMAN prose are legibly typed on the page "
                "('...die wahren Ereignisse...'). Readable invented text on a document, in a film "
                "whose evidence is documents",
    "33855578": "a South Asian steel works; the smoke and scale are good and the region is not",
    "34724032": "an elevated highway timelapse over East Asian tower blocks",
    "34842426": "saturated green and yellow windows at night; belongs to another film",
    "34959549": "another East Asian highway timelapse, orange",
    "34964490": "a Shell forecourt, logo clearly legible",
    "34964501": "the same Shell forecourt from the junction",
    "35140392": "a silhouette in a shuttered arcade that reads East Asian",
    "35140407": "the silhouette resolves into a lit, identifiable face, with red shop signs behind",
    "35186847": "silhouettes in a tunnel mouth; the street beyond is unmistakably East Asian",
    "35379333": "a night concrete plant; the worker's clothing and footwear read South-East Asian",
    "36331848": "a chair on a rural road below non-European hills; no beat, and the place shows",
    "37957757": "a yellow taxi behind the subject; reads American",
}


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    by_id: dict[str, str] = {}
    for p in sorted(FACTORY.glob("*.mp4")):
        vid = p.name.split("__")[0].removeprefix("MO-")
        by_id[vid] = p.name
    staged = sorted(by_id.values())

    missing = [k for k in list(ACCEPT) + list(REJECT) if k not in by_id]
    unjudged = [v for k, v in by_id.items() if k not in ACCEPT and k not in REJECT]
    if missing or unjudged:
        print(f"ids in this file not on disk: {missing or 'none'}")
        print(f"clips on disk with NO verdict: {unjudged or 'none'}")
        if unjudged:
            print("refusing to write a review that silently skips a staged clip")
            return 1

    accepted = sorted(by_id[k] for k in ACCEPT)
    rejected = {by_id[k]: why for k, why in sorted(REJECT.items())}
    pool_id = hashlib.sha256("\n".join(staged).encode("utf-8")).hexdigest()

    doc = {
        "schema_version": "1.0.0",
        "slug": "morandi",
        "reviewed_at": REVIEWED_AT,
        "reviewer": REVIEWER,
        "review_method": (
            "All 21 sheets in runs/qc/pool_frames/morandi were read. Each clip is sampled across "
            "its own duration, so a clip that only goes wrong late is caught. Where a tile was "
            "ambiguous the full-resolution frame under frames/ was opened."),
        "pool_size": len(staged),
        "accepted_count": len(accepted),
        "rejected_count": len(rejected),
        "rejected": rejected,
        "pool_frame_review": {
            "reviewer": REVIEWER,
            "reviewed_at": REVIEWED_AT,
            "pool_id_sha256": pool_id,
            "reviewed_clips": staged,
            "accepted": accepted,
            "method": (
                "Sheets 1-21 of runs/qc/pool_frames/morandi, read in order, every tile looked at."),
            "era_reference": (
                "episode_spec.v001.json declares era_setting Genoa/Liguria 1962-2026 and bars the "
                "American, British and Asian registers and holiday-Italy. A clip is rejected when "
                "the frame reveals WHERE or WHEN it is and the answer is not Genoa; when a brand, "
                "a language or a plate is readable; when a face is identifiable and no beat needs "
                "that person; or when it is atmosphere attached to no beat."),
            "counts": {"staged": len(staged), "accepted": len(accepted), "rejected": len(rejected)},
            "supersedes": (
                "runs/qc/morandi_footage_reviewed.v001.json, which recorded these 61 as reviewed. "
                "They were -- on 400px archive tiles showing one frame each. 32 do not survive a "
                "look at a size where the frame can be read, and most of those 32 were accepted by "
                "this same reviewer on those tiles. A thumbnail is not evidence."),
            "note": (
                "The surviving pool is heavily weighted to water on glass (7 of 29). "
                "footage_diversity will see that. The assembly should spread them or drop some; "
                "they are kept here because each is individually clean, not because the film needs "
                "seven."),
        },
    }

    print(f"staged {len(staged)} | accepted {len(accepted)} | rejected {len(rejected)} "
          f"({100*len(rejected)/len(staged):.0f}%)")
    if a.dry_run:
        print("--dry-run: nothing written")
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
