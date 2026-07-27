# -*- coding: utf-8 -*-
"""Measure and correct FACTORY SHELF MISLABELING using recovered source metadata.

The incident: `H:\\pd-media\\assets\\factory\\` was filled by running ~300 curated
queries against Pexels/Pixabay and naming every downloaded file after the QUERY
("AF-BG-40537__voting_booth_curtain.jpg"), not after what actually came back. The
theme a builder reads off that filename (`factory_themes.theme_of(subtype)`) is
therefore a claim about the query, not about the pixels. Documented casualty:
theme folder `evidence_bag` containing cartoons.

Since 2026-07-27 the retrofit recovered the REAL provider title for 88,740 of those
files (Pexels/Pixabay canonical URL slug) into
`H:\\pd-media\\assets\\archive\\_ledger\\factory.jsonl`. That makes the mislabel
measurable for the first time: compare the recovered title against (a) the local
filename slug and (b) the theme's keyword set.

Scoring reuses the ingest framework's relevance engine verbatim — this module
imports `relevance` / `term_hits` / `sense_ok` / `WEAK_TERMS` / `GLOBAL_NEG` from
`scripts/ingest_archive_sources.py` and merely REGISTERS the factory taxonomy's
themes into it (term cache + STRONG_EXTRA), so both shelves are judged by one
vocabulary and one set of sense guards. Nothing is re-implemented.

Verdicts (per ledger row):
  match          local theme's vocabulary is supported by the recovered title and no
                 other theme fits clearly better
  contradiction  cross_theme : another theme beats the local one by >= MARGIN
                 off_label   : local theme scores ZERO and the title shares no
                               content token with the filename slug (the
                               christmas-market-in-civic_voting case)
  weak           title neither supports nor refutes the label (generic slug, or the
                 label is `misc_background`, which claims nothing)
  no_metadata    no recovered title to judge with

Outputs (additive only — originals are never moved, renamed or deleted):
  1. factory.jsonl gains `theme_local`, `theme_recovered`, `label_verdict`,
     `label_verdict_kind`, `label_scores` on every row.
  2. D:\\pd-media-browse\\factory_browse\\<theme_recovered>\\  rebuilt from the
     corrected themes, plus `_mislabeled\\` holding every contradiction as a symlink
     (`<local>__to__<recovered>` for re-homed, `<local>__unsupported` for flagged
     in place) so they can be eyeballed as a group.
  3. H:\\pd-media\\assets\\archive\\_qc\\factory_label_audit\\  labeled contact
     sheets for eyeball verification + audit JSON/CSV.

Usage:
  python scripts/audit_factory_labels.py measure [--dry-run] [--limit N]
  python scripts/audit_factory_labels.py report
  python scripts/audit_factory_labels.py sheet   [--sample 40] [--seed 7]
  python scripts/audit_factory_labels.py link    [--dry-run]
  python scripts/audit_factory_labels.py selftest          # matcher equivalence proof

Measured result v001 (2026-07-28, 88,740 rows): 40.0% of claim-bearing labels
contradicted, 17.5% confidently mislabeled and re-homed. Eyeball on 40 items: raw
shelf label visually correct 52.5%, corrected view 70.0%. See
episodes/_planning/measurements/FACTORY_LABEL_AUDIT.v001.md
"""
from __future__ import annotations

import argparse
import collections
import csv
import datetime as dt
import json
import os
import random
import re
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "scripts"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import ingest_archive_sources as ing  # noqa: E402  (relevance engine — reused, not copied)
from factory_themes import RULES  # noqa: E402  (factory taxonomy — single source)

ASSETS_ROOT = r"H:\pd-media\assets"
LEDGER = os.path.join(ASSETS_ROOT, "archive", "_ledger", "factory.jsonl")
QC_DIR = os.path.join(ASSETS_ROOT, "archive", "_qc", "factory_label_audit")
BROWSE = r"D:\pd-media-browse\factory_browse"
STATE = os.path.join(ASSETS_ROOT, "archive", "_ledger", "factory_browse_state.json")
MISLABEL_DIR = "_mislabeled"

MARGIN = 25          # a rival theme must beat the local one by this much
THRESHOLD = 30       # ingest's DEFAULT_THRESHOLD: >=1 strong term or a full phrase

# ---------------------------------------------------------------- taxonomy ----
# Factory subject themes. `misc_background` is the taxonomy's "no rule matched"
# bucket: it makes no claim, so it can be neither confirmed nor contradicted.
SUBJECT_THEMES = ["legal_court", "civic_voting", "crime_police", "forensics_dna",
                  "medical_lab", "finance_money", "property_home", "school_youth",
                  "surveillance_tech", "documents_paper", "urban_night",
                  "nature_landscape", "atmosphere_symbolic"]
# Format buckets: derived from the shelf CATEGORY (light_assets/ vfx_overlays/ ...),
# not from a subject query. They claim a visual FORM, so they are scored against
# form vocabulary and are never re-linked into a subject theme.
FORMAT_THEMES = ["light", "vfx", "particle", "texture", "abstract", "abstract_loop"]
UNCLAIMED = "misc_background"

# Factory theme -> ingest THEMES whose curated query vocabulary applies (recall,
# inherited at WEAK weight unless also listed in STRONG below).
INGEST_MAP: dict[str, list[str]] = {
    "legal_court": ["courtroom_justice", "government_buildings"],
    "crime_police": ["police_modern", "police_period", "prison_jail"],
    "forensics_dna": ["laboratory_forensics"],
    "medical_lab": ["laboratory_forensics"],
    "finance_money": ["money_banking"],
    "property_home": ["small_town"],
    "surveillance_tech": ["science_tech", "period_telephone_tech"],
    "documents_paper": ["newspapers_printing"],
    "urban_night": ["world_cities", "chicago_city"],
    "nature_landscape": ["ocean_nature", "landscapes_timelapse", "weather_disasters",
                         "wildlife_animals"],
    "abstract": ["textures_backgrounds"],
    "texture": ["textures_backgrounds"],
}

# Unambiguous SINGLE-WORD domain terms per factory theme (weight 30 — one clears
# THRESHOLD). Grounded in the shelf's own subtype vocabulary (the ~300 queries that
# actually built the shelf). Multi-word subject matter lives in PHRASES below, never
# here: splitting "witness stand" into "witness"+"stand" would make "stand" a
# weight-30 legal term and admit food stands and stands of trees.
STRONG: dict[str, str] = {
    "legal_court": """courtroom court courthouse gavel judge judges judicial judiciary
        jury juror justice lawyer lawyers attorney barrister legal law laws lawsuit
        litigation verdict trial tribunal defendant prosecutor plaintiff testimony
        witness constitution constitutional statute legislation legislature senate
        congress capitol parliament notary oath""",
    "civic_voting": """vote votes voting voter voters ballot ballots election elections
        electoral referendum democracy democratic campaign rally protest protests
        protester protesters demonstration demonstrator activist activism picket
        placard suffrage civic citizenship flag flags patriotic parade""",
    "crime_police": """police policeman policewoman officer officers cop cops patrol
        siren sirens handcuff handcuffs arrest arrested detention prison prisons
        prisoner inmate jail jails cellblock penitentiary crime criminal detective
        sheriff interrogation ambulance swat suspect custody""",
    "forensics_dna": """dna helix genome genomic genetic genetics chromosome molecular
        molecule biotech biotechnology fingerprint fingerprints vial vials specimen
        swab forensic forensics microscopy""",
    "medical_lab": """donation donations donor donors plasma transfusion
        medical medicine hospital clinic clinical doctor doctors nurse
        nurses patient patients surgery surgeon surgical pill pills capsule pharmacy
        pharmaceutical syringe injection vaccine stethoscope ekg ecg laboratory
        microscope centrifuge beaker flask glassware chemistry chemical healthcare
        scientist""",
    "finance_money": """money cash currency banknote banknotes bank banking banker
        dollar dollars euro sterling coin coins gold bullion ingot vault finance
        financial investment investor trading trader ticker bitcoin cryptocurrency
        crypto blockchain atm wealth profit economy economic accounting audit tax
        taxes invoice wallet purse savings mortgage""",
    "property_home": """house houses home homes household apartment apartments
        residence residential dwelling cottage bungalow farmhouse villa mansion
        suburb suburbs suburban neighborhood neighbourhood realtor landlord tenant
        eviction property porch driveway backyard doorway""",
    "school_youth": """school schools schoolyard schoolhouse classroom teacher teachers
        student students pupil pupils education educational graduation graduate
        diploma campus university college kindergarten preschool textbook backpack
        chalkboard blackboard playground""",
    "surveillance_tech": """surveillance cctv camera cameras lens monitor monitors
        computer computers laptop keyboard server servers datacenter network
        networking internet online digital binary coding software hardware circuit
        motherboard processor microchip semiconductor satellite antenna radar
        transmitter smartphone phone telephone mobile handset hacker hacking cyber
        cybersecurity encryption password firewall technology robot robotic drone
        gps biometric hologram holographic algorithm switchboard telegraph globe""",
    "documents_paper": """book books bookstore
        document documents documentation paperwork contract contracts
        agreement letter letters envelope envelopes postage newspaper newspapers
        newsprint headline tabloid printing typewriter typing typewritten quill
        inkwell signature signing parchment manuscript scroll receipt invoice
        certificate dossier memo shredder shredded notebook notepad ledger archive
        archives archival library bookshelf bookcase folder folders""",
    "urban_night": """station stations concourse
        city cities cityscape skyline skyscraper skyscrapers downtown
        urban metropolis street streets avenue boulevard sidewalk traffic road roads
        highway motorway freeway underpass overpass bridge tunnel subway metro train
        trains railway railroad platform tram trolley airport terminal runway hangar
        parking garage rooftop office offices boardroom cubicle elevator escalator
        lobby stadium arena alley alleyway neon crosswalk pedestrian taxi""",
    "nature_landscape": """mountain mountains peak summit hill hills valley canyon
        cliff cliffs forest forests woodland woods tree trees pine jungle ocean sea
        seascape beach coast coastal shore shoreline lake lakes pond river stream
        creek waterfall cascade desert dune dunes glacier frozen fog foggy mist misty
        cloud clouds sky skies sunset sunrise dawn dusk twilight storm stormy
        lightning thunder rain rainy field fields meadow grass grassland prairie
        island islands wave waves wildlife bird birds deer flower flowers blossom
        autumn winter landscape landscapes nature scenery countryside harbor harbour
        lighthouse cemetery graveyard churchyard church chapel aurora horizon farm
        farmland""",
    "atmosphere_symbolic": """crowd crowds firewood bonfire
        silhouette silhouettes shadow shadows backlit mirror
        reflection reflections shattered chair chairs stool clock clocks hourglass
        wristwatch candle candles candlelight padlock lock locks chain chains key
        keys keyhole handshake fingers palm chess chessboard fireplace ember embers
        spotlight umbrella raincoat lantern moody lonely alone loneliness grief
        solitude praying prayer wheelchair elderly crying figure""",
    # ---- format buckets (claim a visual FORM, not a subject) ----
    "light": """sun sunny sunshine sunlit sunrise sunset daylight daybreak
        light lights lighting sunlight sunbeam sunbeams flare glow glowing
        glare bokeh neon lamp lamps lantern candle candlelight flame flames firelight
        headlight headlights spotlight floodlight searchlight moonlight moonlit aurora
        firework fireworks beam beams illuminated illumination luminous shine shining
        bright brightness backlit streetlight torch flashlight projector caustics
        luminescence""",
    "vfx": """burning burnt bonfire
        smoke smoky fog mist steam vapor vapour ink explosion explode fireball
        fire flame flames spark sparks lightning splash molten lava magma shockwave
        geyser sandstorm powder plume swirl frost eruption blast splatter""",
    "particle": """snowfall snowy flurry
        particle particles dust motes speck specks snow snowflake snowflakes
        blizzard ash ashes ember embers spark sparks glitter confetti bubble bubbles
        pollen seed seeds dandelion firefly fireflies foam spray sand leaf leaves
        petal petals droplet droplets floating drifting swirling plankton
        bioluminescence scraps""",
    "texture": """wall walls paint painted film noise brushed
        texture textures textured grain grainy leather rust rusted rusty
        metal metallic fabric cloth textile weave woven canvas parchment cardboard
        stone rock brick marble granite wood wooden timber plank concrete cement
        cracked crack peeling scratched scratch grunge grungy blueprint surface
        pattern patterned aged worn weathered distressed steel linen burlap paper""",
    "abstract": """abstract abstraction gradient gradients blur blurred defocused
        minimal minimalist geometric geometry shape shapes wallpaper backdrop bokeh
        cinematic moody colorful colourful marbling acrylic""",
    "abstract_loop": """loop looping looped seamless animation animated motion graphics
        gradient node nodes network rotation rotating spinning kaleidoscope""",
}


def _flatten(spec: str) -> list[str]:
    """Whitespace-separated single-word domain terms -> sorted unique list."""
    return sorted({t for t in re.split(r"\s+", spec.strip()) if len(t) > 2})


# Curated multi-word phrases (matched as phrases by ing.term_hits across space/hyphen).
PHRASES: dict[str, list[str]] = {
    "legal_court": ["supreme court", "law library", "law books", "scales of justice",
                    "lady justice", "balance scale", "white house", "government building",
                    "federal building", "city hall", "jury box", "witness stand",
                    "courthouse steps", "gavel block", "court room", "law book"],
    "civic_voting": ["ballot box", "polling station", "polling booth", "voting booth",
                     "american flag", "stars and stripes", "union jack", "protest sign"],
    "crime_police": ["police car", "squad car", "police station", "crime scene",
                     "barbed wire", "razor wire", "cell block", "law enforcement",
                     "one way mirror", "guard tower", "police officer", "prison cell",
                     "jail cell", "evidence bag", "police badge", "police tape"],
    "forensics_dna": ["double helix", "blood sample", "blood test", "petri dish",
                      "test vial", "dna helix"],
    "medical_lab": ["operating room", "emergency room", "heart monitor", "test tube",
                    "test tubes", "hospital corridor", "medical laboratory", "x ray"],
    "finance_money": ["stock market", "stock exchange", "trading floor", "wall street",
                      "bank vault", "safe deposit", "credit card", "debit card",
                      "cash register", "gold bar", "gold bars", "dollar bill",
                      "dollar bills", "piggy bank"],
    "property_home": ["real estate", "for sale", "picket fence", "front door",
                      "moving truck", "moving boxes", "main street", "small town",
                      "rural road", "loading dock", "suburban house"],
    "school_youth": ["school bus", "school hallway", "class room", "lecture hall",
                     "swing set", "graduation cap"],
    "surveillance_tech": ["security camera", "surveillance camera", "circuit board",
                          "data center", "cell tower", "radio tower", "fiber optic",
                          "world map", "face recognition", "artificial intelligence",
                          "neural network", "server room", "computer screen",
                          "mobile phone", "rotary phone", "control room"],
    "documents_paper": ["printing press", "wax seal", "fountain pen", "filing cabinet",
                        "magnifying glass", "ledger book", "front page", "ink pot",
                        "stack of papers", "old book", "old books"],
    "urban_night": ["city skyline", "city street", "city lights", "parking garage",
                    "train station", "subway station", "long exposure", "light trails",
                    "office building", "high rise", "aerial view of city"],
    "nature_landscape": ["northern lights", "mountain range", "sand dunes",
                         "forest path", "ocean waves", "storm clouds", "milky way",
                         "sunset over", "aerial view of the sea"],
    "atmosphere_symbolic": ["pocket watch", "chess board", "chess piece",
                            "broken glass", "concrete wall", "brick wall",
                            "empty chair", "desk lamp", "rotary phone",
                            "person standing", "man standing", "woman standing"],
    "light": ["lens flare", "god rays", "golden hour", "light leak", "bokeh lights",
              "sun rays", "light beam", "light beams", "neon light", "neon lights"],
    "vfx": ["ink in water", "black background", "water splash", "smoke cloud",
            "dust cloud", "dry ice", "tear gas", "slow motion"],
    "particle": ["dust motes", "slow motion", "black background", "snow falling",
                 "floating particles"],
    "texture": ["film grain", "close up", "stone wall", "brick wall", "wood grain",
                "paper texture", "rusty metal", "peeling paint"],
    "abstract": ["dark background", "abstract background", "color splash"],
    "abstract_loop": ["motion graphics", "data stream", "seamless loop"],
}

_STOP = ing.STOPWORDS | {"close", "up", "shot", "view", "photo", "photography", "image",
                         "video", "background", "backgrounds", "free", "stock", "person",
                         "people", "man", "woman", "black", "white", "blue", "red",
                         "green", "yellow", "grey", "gray", "brown", "orange", "purple",
                         "pink", "beige", "dark", "light", "closeup", "macro", "top",
                         "front", "side", "near", "over", "under", "into", "during",
                         "while", "wearing", "holding", "standing", "sitting", "his",
                         "her", "their", "its", "this", "that", "there", "some", "other"}


_PAT: dict[str, "re.Pattern[str]"] = {}
SUBJECT_VOCAB: set[str] = set()


def _fast_term_hits(term: str, text: str) -> bool:
    """Memoized drop-in for ing.term_hits — IDENTICAL pattern, identical semantics.

    ing.term_hits builds its regex per call; `re` caches only 512 compiled patterns,
    and this audit scores ~2,700 distinct terms x 19 themes x 88,740 rows, so the
    cache thrashes and every call recompiles. Here the pattern is compiled once per
    term and guarded by a substring pre-filter that is a strict necessary condition
    of the regex (the term's first word must appear literally, since the pattern is
    an escaped literal with optional plural suffix). Equivalence is asserted against
    the original in `selftest`.
    """
    if not term:
        return False
    head = re.split(r"[-\s]+", term, maxsplit=1)[0]
    if head and head not in text:
        return False
    pat = _PAT.get(term)
    if pat is None:
        core = r"[-\s]+".join(re.escape(p) for p in re.split(r"[-\s]+", term) if p)
        pat = re.compile(rf"\b{core}(?:s|es|'s|s')?\b")
        _PAT[term] = pat
    return pat.search(text) is not None


def register_factory_themes() -> None:
    """Teach the ingest relevance engine the factory taxonomy.

    Populates ing._theme_pos_cache (positive terms + phrases) and ing.STRONG_EXTRA
    (weight-30 domain terms) so `ing.relevance(factory_theme, title)` works with the
    engine's own boundary matching, sense guards, weak-only cap and negative list.
    """
    for theme in SUBJECT_THEMES + FORMAT_THEMES:
        strong = _flatten(STRONG[theme])
        phrases = [p.lower() for p in PHRASES.get(theme, [])]
        terms: set[str] = set(strong) | set(phrases)
        # factory taxonomy's own routing keywords (the rules a builder's filename hits)
        terms |= {kw.strip("_").replace("_", " ") for kw, th in RULES if th == theme}
        curated = set(terms)
        # inherited recall from the ingest shelf's curated queries. These are DEMOTED
        # to weak weight (see below): ing.term_weight() gives any term not in
        # WEAK_TERMS a full 30, and inherited query words like "floor" (from
        # money_banking's "stock exchange trading floor") or "glass" (from
        # laboratory_forensics' "glass beaker clink") were single-handedly winning
        # best-fit for titles like "brown wooden armchair on brown wooden floor".
        inherited: set[str] = set()
        for src in INGEST_MAP.get(theme, []):
            t, ph = ing.theme_terms(src)
            inherited |= t
            phrases = phrases + [p for p in ph if p not in phrases]
        terms = {t for t in (terms | inherited) if len(t) > 2}
        ing._theme_pos_cache[theme] = (terms, phrases)
        ing.STRONG_EXTRA[theme] = strong + phrases + [
            kw.strip("_").replace("_", " ") for kw, th in RULES if th == theme]
        # term_weight() checks STRONG_EXTRA[theme] FIRST, so a curated term stays
        # weight-30 for its own theme while counting only 15 anywhere else.
        ing.WEAK_TERMS |= {t for t in inherited if t not in curated}
    # extra sense guards for shelf-specific ambiguity
    ing.SENSE_GUARDS.setdefault("stock", []).extend(
        [r"stock photo", r"stock image", r"stock footage", r"livestock", r"rolling stock"])
    ing.SENSE_GUARDS.setdefault("light", []).extend(
        [r"light (?:blue|green|brown|grey|gray|pink|colored)", r"traffic light"])
    ing.SENSE_GUARDS.setdefault("data", []).extend([r"data protection notice"])
    ing.term_hits = _fast_term_hits  # memoized; semantics asserted in `selftest`
    # Vocabulary of words that NAME A SUBJECT somewhere in the taxonomy. Used to
    # decide whether a filename/title token overlap is meaningful: three misses found
    # by eyeballing v000 ("police_station_at_night" -> a railway station,
    # "antique_brass_scales" -> a Ford Model T, "static_noise_particles" -> a river)
    # all survived as `weak` purely because ONE generic modifier ("station",
    # "antique", "noise") appeared in both the query and the title.
    SUBJECT_VOCAB.clear()
    for th in SUBJECT_THEMES + FORMAT_THEMES:
        SUBJECT_VOCAB.update(_flatten(STRONG[th]))
    SUBJECT_VOCAB.update(w for kw, _t in RULES for w in kw.strip("_").split("_") if len(w) > 2)


def cmd_selftest() -> None:
    """Prove the memoized matcher is equivalent to the engine's own term_hits."""
    original = ing.term_hits
    register_factory_themes()          # this swaps in _fast_term_hits
    terms = sorted({t for th in SUBJECT_THEMES + FORMAT_THEMES
                    for t in ing._theme_pos_cache[th][0]})
    texts = []
    for i, rec in enumerate(read_rows(LEDGER)):
        texts.append((rec.get("title") or "").lower())
        if i > 4000:
            break
    bad = 0
    for text in texts[:1500]:
        for t in terms:
            if original(t, text) != _fast_term_hits(t, text):
                bad += 1
                if bad < 6:
                    print(f"MISMATCH term={t!r} text={text!r}")
    print(f"selftest: {len(terms)} terms x {len(texts[:1500])} titles, mismatches={bad}")
    return


def content_tokens(text: str | None) -> set[str]:
    return {t for t in re.split(r"[^a-z0-9]+", (text or "").lower())
            if len(t) > 2 and t not in _STOP}


# ------------------------------------------------------------- classification --

def classify(rec: dict) -> dict:
    """Returns the audit fields for one ledger row."""
    title = (rec.get("title") or "").strip()
    prov = rec.get("title_provenance") or "none"
    local = rec.get("original_dir_theme") or rec.get("theme") or UNCLAIMED
    out = {"theme_local": local, "theme_recovered": local,
           "label_verdict": "weak", "label_verdict_kind": "", "label_scores": {}}

    if not title or title == "untitled" or prov in ("none", "gone_from_provider"):
        out["label_verdict"] = "no_metadata"
        return out

    scored = {t: ing.relevance(t, title)[0] for t in SUBJECT_THEMES + FORMAT_THEMES}
    local_score = scored.get(local, 0)
    # a format-bucket item is only ever re-themed inside the format buckets, and a
    # subject item only inside the subject themes: a "smoke on black" vfx overlay is
    # not a nature photo, and a courthouse photo is not a texture.
    pool = FORMAT_THEMES if local in FORMAT_THEMES else SUBJECT_THEMES
    best_theme, best_score = max(((t, scored[t]) for t in pool),
                                 key=lambda kv: (kv[1], kv[0] == local))
    top3 = sorted(scored.items(), key=lambda kv: -kv[1])[:3]
    out["label_scores"] = {t: s for t, s in top3 if s > 0}
    out["label_scores"][local] = local_score

    # only a SUBJECT-BEARING shared word counts as the filename corroborating the
    # title; shared modifiers like "station"/"antique"/"noise" do not (see
    # register_factory_themes).
    overlap = content_tokens(rec.get("subtype")) & content_tokens(title) & SUBJECT_VOCAB

    if local == UNCLAIMED:
        # the label claims nothing -> cannot contradict; still recover a real theme
        out["label_verdict"] = "weak"
        out["label_verdict_kind"] = "unclaimed_label"
        if best_score >= THRESHOLD and best_theme != UNCLAIMED:
            out["theme_recovered"] = best_theme
        return out

    # A label is only CONTRADICTED when the recovered title fails to support it AND
    # clearly supports a different theme. If the title supports the local theme, the
    # item is at worst dual-subject ("colorful abstract light streaks explosion" in
    # the light bucket) — not a mislabel. Conservative by design: this audit accuses
    # the shelf, so its false-accusation rate must be low.
    if (best_theme != local and local_score < THRESHOLD
            and best_score >= THRESHOLD and best_score - local_score >= MARGIN):
        out["label_verdict"] = "contradiction"
        out["label_verdict_kind"] = "cross_theme"
        out["theme_recovered"] = best_theme
        return out

    if local_score >= THRESHOLD:
        out["label_verdict"] = "match"
        out["theme_recovered"] = local
        if best_theme != local and best_score - local_score >= MARGIN:
            out["label_verdict_kind"] = "dual_subject"
        return out

    if local_score == 0 and not overlap and len(content_tokens(title)) >= 2:
        # Zero vocabulary support for the label AND no word in common with the query
        # the file is named after. No rival theme fits either (a rival scoring >=
        # THRESHOLD would have been caught above), so there is nowhere better to put
        # it: it STAYS in place and is flagged for eyeball review instead of being
        # evicted into a junk bucket where genuine assets would be lost.
        out["label_verdict"] = "contradiction"
        out["label_verdict_kind"] = "off_label"
        out["theme_recovered"] = local
        return out

    out["label_verdict"] = "weak"
    out["label_verdict_kind"] = "filename_only" if overlap else "generic_title"
    return out


# ------------------------------------------------------------------ commands --

def read_rows(path: str, limit: int = 0):
    with open(path, encoding="utf-8") as f:
        for i, line in enumerate(f):
            line = line.strip()
            if not line:
                continue
            if limit and i >= limit:
                return
            yield json.loads(line)


def cmd_measure(dry_run: bool = False, limit: int = 0) -> None:
    register_factory_themes()
    os.makedirs(QC_DIR, exist_ok=True)
    rows, verd = [], collections.Counter()
    per_theme: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    flow = collections.Counter()
    for rec in read_rows(LEDGER, limit):
        a = classify(rec)
        rec.update(a)
        # keep the ledger's canonical `theme` in step with the corrected assignment so
        # search_archive.py --theme and BOTH link tools agree on one tree. The pre-audit
        # label is never lost: it stays in `original_dir_theme` / `theme_local`.
        if rec.get("theme") != a["theme_recovered"]:
            rec["theme"] = a["theme_recovered"]
            rec["theme_source"] = "label_audit_v001"
        rows.append(rec)
        v = a["label_verdict"]
        key = v if not a["label_verdict_kind"] else f"{v}:{a['label_verdict_kind']}"
        verd[key] += 1
        per_theme[a["theme_local"]][v] += 1
        if v == "contradiction":
            flow[(a["theme_local"], a["theme_recovered"])] += 1
    print(f"rows classified: {len(rows)}")
    for k, c in verd.most_common():
        print(f"  {k:34} {c:7} ({100*c/len(rows):5.2f}%)")

    summary = {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "ledger": LEDGER, "rows": len(rows), "margin": MARGIN, "threshold": THRESHOLD,
        "verdicts": dict(verd),
        "per_theme": {t: dict(c) for t, c in sorted(per_theme.items())},
        "top_flows": [{"from": a, "to": b, "n": n} for (a, b), n in flow.most_common(40)],
    }
    if dry_run:
        print("(dry-run: ledger not written)")
    else:
        tmp = LEDGER + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        os.replace(tmp, LEDGER)
        print(f"ledger rewritten with audit fields: {LEDGER}")
    with open(os.path.join(QC_DIR, "audit_summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=1, ensure_ascii=False)
    with open(os.path.join(QC_DIR, "contradictions.csv"), "w", encoding="utf-8",
              newline="") as f:
        w = csv.writer(f)
        w.writerow(["manifest_id", "kind", "theme_local", "theme_recovered", "subtype",
                    "recovered_title", "file_path"])
        for r in rows:
            if r["label_verdict"] == "contradiction":
                w.writerow([r.get("manifest_id"), r["label_verdict_kind"], r["theme_local"],
                            r["theme_recovered"], r.get("subtype"), r.get("title"),
                            r.get("file_path")])
    print(f"qc artifacts -> {QC_DIR}")


def cmd_report() -> None:
    p = os.path.join(QC_DIR, "audit_summary.json")
    s = json.load(open(p, encoding="utf-8"))
    tot = s["rows"]
    print(f"rows {tot}")
    rows = []
    for t, c in s["per_theme"].items():
        n = sum(c.values())
        contra = c.get("contradiction", 0)
        rows.append((contra / n if n else 0, t, n, c.get("match", 0), contra,
                     c.get("weak", 0), c.get("no_metadata", 0)))
    print(f"{'theme':22} {'n':>7} {'match':>7} {'contra':>7} {'weak':>7} {'rate':>7}")
    for rate, t, n, m, ct, w, nm in sorted(rows, reverse=True):
        print(f"{t:22} {n:7} {m:7} {ct:7} {w:7} {100*rate:6.1f}%")
    print("\ntop mislabel flows:")
    for f in s["top_flows"][:20]:
        print(f"  {f['from']:22} -> {f['to']:22} {f['n']}")


# ------------------------------------------------------------- contact sheets --

FONT = "C\\:/Windows/Fonts/consola.ttf"  # ffmpeg filter syntax: escaped drive colon


def _label(text: str, width: int) -> str:
    return text.replace(":", "\\:").replace("'", "").replace("%", "")[:width]


def cmd_sheet(sample: int = 40, seed: int = 7, contra: int = 25) -> None:
    """Sample across verdict classes and render labeled contact sheets for eyeballing."""
    rng = random.Random(seed)
    buckets: dict[str, list] = collections.defaultdict(list)
    for rec in read_rows(LEDGER):
        v = rec.get("label_verdict")
        if not v:
            continue
        k = v if v != "contradiction" else f"contradiction:{rec.get('label_verdict_kind')}"
        if rec.get("kind") != "image":
            continue
        buckets[k].append(rec)
    plan = {"contradiction:cross_theme": contra // 2 + contra % 2,
            "contradiction:off_label": contra // 2,
            "match": (sample - contra) // 2,
            "weak": (sample - contra) - (sample - contra) // 2}
    picks = []
    for k, n in plan.items():
        pool = buckets.get(k, [])
        picks += [(k, r) for r in rng.sample(pool, min(n, len(pool)))]
    os.makedirs(QC_DIR, exist_ok=True)
    manifest = []
    tiles = []
    for i, (k, r) in enumerate(picks, 1):
        fp = r["file_path"]
        if not os.path.isfile(fp):
            continue
        kind = r.get("label_verdict_kind") or r["label_verdict"]
        line1 = f"#{i:02d} [{kind}] LOCAL={r['theme_local']} -> REC={r['theme_recovered']}"
        line2 = f"file={r.get('subtype')} | title={(r.get('title') or '')[:52]}"
        tiles.append((fp, line1, line2))
        manifest.append({"n": i, "bucket": k, "manifest_id": r.get("manifest_id"),
                         "theme_local": r["theme_local"],
                         "theme_recovered": r["theme_recovered"],
                         "subtype": r.get("subtype"), "title": r.get("title"),
                         "file_path": fp, "scores": r.get("label_scores")})
    with open(os.path.join(QC_DIR, "eyeball_sample.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=1, ensure_ascii=False)
    # render in pages of 8 (4x2) so labels stay legible
    per_page = 8
    pages = [tiles[i:i + per_page] for i in range(0, len(tiles), per_page)]
    for pi, page in enumerate(pages, 1):
        out = os.path.join(QC_DIR, f"contact_sheet_p{pi:02d}.jpg")
        cmd = ["ffmpeg", "-y", "-loglevel", "error"]
        for fp, _l1, _l2 in page:
            cmd += ["-i", fp]
        filt = []
        cap2 = [l2 for _f, _l1, l2 in page]
        for i, (fp, cap, _l2) in enumerate(page):
            filt.append(
                f"[{i}:v]scale=480:270:force_original_aspect_ratio=decrease,"
                f"pad=480:270:(ow-iw)/2:(oh-ih)/2:color=black,"
                f"pad=480:310:0:40:color=0x101010,"
                f"drawtext=fontfile='{FONT}':text='{_label(cap, 74)}':fontcolor=white:"
                f"fontsize=12:x=5:y=6,"
                f"drawtext=fontfile='{FONT}':text='{_label(cap2[i], 74)}':fontcolor=0xffd479:"
                f"fontsize=12:x=5:y=22[v{i}]")
        for i in range(len(page), per_page):
            filt.append(f"color=c=0x101010:s=480x310:d=1[v{i}]")
        filt.append("".join(f"[v{i}]" for i in range(per_page))
                    + f"xstack=inputs={per_page}:layout="
                      "0_0|w0_0|w0+w1_0|w0+w1+w2_0|0_h0|w0_h0|w0+w1_h0|w0+w1+w2_h0[out]")
        cmd += ["-filter_complex", ";".join(filt), "-map", "[out]",
                "-frames:v", "1", "-q:v", "3", out]
        r = subprocess.run(cmd, capture_output=True, text=True)
        print(f"sheet {out} rc={r.returncode} {r.stderr[:300]}")
    print(f"{len(tiles)} tiles, {len(pages)} sheets -> {QC_DIR}")


# ----------------------------------------------------------------- browse link -

def slugify(text: str, max_len: int = 70) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")
    if len(s) > max_len:
        s = s[:max_len].rsplit("-", 1)[0] or s[:max_len]
    return s or "untitled"


def cmd_link(dry_run: bool = False, limit: int = 0) -> None:
    """Rebuild the browse view on theme_recovered + a _mislabeled/ review folder."""
    state = json.load(open(STATE, encoding="utf-8")) if os.path.isfile(STATE) else {}
    created = kept = moved = missing = errors = 0
    n = 0
    for rec in read_rows(LEDGER, limit):
        n += 1
        src = rec["file_path"]
        key = rec.get("manifest_id") or f"{rec['source']}:{rec['id']}"
        if not os.path.isfile(src):
            missing += 1
            continue
        theme = rec.get("theme_recovered") or rec.get("theme")
        base = f"{rec['source']}__{rec['id']}__{slugify(rec.get('title'))}" \
               f"{os.path.splitext(src)[1].lower()}"
        tdir = os.path.join(BROWSE, theme)
        desired = os.path.join(tdir, base)
        old = state.get(key)
        if old and os.path.normcase(old) != os.path.normcase(desired):
            if not dry_run:
                try:
                    if os.path.lexists(old):
                        os.unlink(old)
                        moved += 1
                except OSError:
                    pass
            else:
                moved += 1
        final = None
        if not dry_run:
            os.makedirs(tdir, exist_ok=True)
            stem, ext = os.path.splitext(desired)
            for k in range(1, 30):
                cand = desired if k == 1 else f"{stem}-{k}{ext}"
                if os.path.lexists(cand):
                    try:
                        if os.path.samefile(cand, src):
                            final = cand
                            kept += 1
                            break
                    except OSError:
                        pass
                    continue
                try:
                    os.symlink(src, cand)
                    final = cand
                    created += 1
                except OSError as e:
                    print(f"link ERROR {src} -> {cand}: {e}")
                    errors += 1
                break
            if final:
                state[key] = final
        # contradictions also get a review link under _mislabeled/
        if rec.get("label_verdict") == "contradiction" and not dry_run:
            kind = rec.get("label_verdict_kind")
            sub = (f"{rec['theme_local']}__to__{rec['theme_recovered']}"
                   if kind == "cross_theme" else f"{rec['theme_local']}__unsupported")
            rdir = os.path.join(BROWSE, MISLABEL_DIR, sub)
            os.makedirs(rdir, exist_ok=True)
            rp = os.path.join(rdir, base)
            if not os.path.lexists(rp):
                try:
                    os.symlink(src, rp)
                except OSError:
                    errors += 1
        if n % 5000 == 0:
            print(f"link {n}: created {created} kept {kept} re-linked {moved}", flush=True)
            if not dry_run:
                tmp = STATE + ".tmp"
                with open(tmp, "w", encoding="utf-8") as f:
                    json.dump(state, f)
                os.replace(tmp, STATE)
    if not dry_run:
        tmp = STATE + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(state, f)
        os.replace(tmp, STATE)
    print(f"link DONE rows={n} created={created} kept={kept} re-linked={moved} "
          f"missing={missing} errors={errors} dry_run={dry_run}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("measure")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--limit", type=int, default=0)
    sub.add_parser("report")
    sub.add_parser("selftest")
    p = sub.add_parser("sheet")
    p.add_argument("--sample", type=int, default=40)
    p.add_argument("--contra", type=int, default=25)
    p.add_argument("--seed", type=int, default=7)
    p = sub.add_parser("link")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()
    if a.cmd == "measure":
        cmd_measure(a.dry_run, a.limit)
    elif a.cmd == "report":
        cmd_report()
    elif a.cmd == "selftest":
        cmd_selftest()
    elif a.cmd == "sheet":
        register_factory_themes()
        cmd_sheet(a.sample, a.seed, a.contra)
    elif a.cmd == "link":
        cmd_link(a.dry_run, a.limit)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
