# -*- coding: utf-8 -*-
"""Single source of the factory subtype -> theme taxonomy.

The factory builder owns asset_manifest.v001.json and rewrites it with FLAT paths
and no `theme` field. So theme is NOT stored; it is DERIVED from `subtype` at query
time via theme_of(). This keeps the theme taxonomy usable no matter how often the
builder rewrites the manifest, and needs no physical file moves.

Themes (backgrounds): legal_court, civic_voting, crime_police, forensics_dna,
medical_lab, finance_money, property_home, school_youth, surveillance_tech,
documents_paper, urban_night, nature_landscape, atmosphere_symbolic, abstract.
fx categories map to their own bucket (light/vfx/particle/texture/abstract_loop).

MATCHING (fixed 2026-07-28, FACTORY_LABEL_AUDIT.v001 §5): rules match on WORD
BOUNDARIES, not bare substrings. The old bare-substring match let a keyword hidden
inside a longer word win -- `tree` inside s-tree-t (682 street photos filed as
nature_landscape), `house` inside light/ware-house (740), `phone` inside
micro-phone (310), `atm` inside atm-osphere (236): 1,968 files misfiled before any
provider ever returned anything. A rule token now matches a subtype token only if
it is the same token, its regular plural, or a prefix of it with >= MIN_PREFIX
characters (so court->courthouse/courtroom, document->documents, snow->snowy still
work, while tree !-> street and atm !-> atmosphere). Suffix and infix hits, the
entire failure class, are gone. See scripts/tests/test_factory_themes.py.

This derived label is NOT trustworthy on its own regardless: it describes the
download QUERY, not the pixels (40% of claim-bearing labels are contradicted by
the file's own recovered provider title). Build-path theme selection must go
through scripts/factory_ledger_themes.py, which reads the audited ledger.
"""
from __future__ import annotations

import re

# A rule token may match a longer subtype token only as a prefix of at least this
# many characters. 3-letter rules (atm, dna, ekg, law) therefore require an exact
# token -- which is precisely what stops `atm` from claiming `atmosphere`.
MIN_PREFIX = 4

# Ordered (keyword, theme). First match wins -> specific before general.
# Keywords are `_`-joined token patterns matched on word boundaries (see above),
# NOT substrings; `law_` is kept in its historical spelling and normalized.
RULES: list[tuple[str, str]] = [
    ("court", "legal_court"), ("gavel", "legal_court"), ("jury", "legal_court"),
    ("justice", "legal_court"), ("judge", "legal_court"), ("law_", "legal_court"),
    ("constitution", "legal_court"), ("witness", "legal_court"), ("scales", "legal_court"),
    ("balance_scale", "legal_court"), ("capitol", "legal_court"), ("supreme_court", "legal_court"),
    ("federal_building", "legal_court"), ("white_house", "legal_court"),
    ("bank_building_columns", "legal_court"), ("government_building", "legal_court"),
    ("ballot", "civic_voting"), ("voting", "civic_voting"), ("protest", "civic_voting"),
    ("flag", "civic_voting"),
    ("police", "crime_police"), ("prison", "crime_police"), ("jail", "crime_police"),
    ("evidence", "crime_police"), ("crime_scene", "crime_police"), ("interrogation", "crime_police"),
    ("handcuff", "crime_police"), ("badge", "crime_police"), ("barbed_wire", "crime_police"),
    ("one_way_mirror", "crime_police"), ("case_files", "crime_police"), ("ambulance", "crime_police"),
    ("dna", "forensics_dna"), ("fingerprint", "forensics_dna"), ("blood", "forensics_dna"),
    ("medical", "medical_lab"), ("hospital", "medical_lab"), ("lab", "medical_lab"),
    ("laboratory", "medical_lab"),  # `lab` is 3 chars -> exact token only; spell it out
    ("test_tube", "medical_lab"), ("centrifuge", "medical_lab"), ("operating", "medical_lab"),
    ("pills", "medical_lab"), ("ekg", "medical_lab"), ("microscope", "medical_lab"),
    ("glassware", "medical_lab"),
    ("money", "finance_money"), ("cash", "finance_money"), ("dollar", "finance_money"),
    ("gold_bar", "finance_money"), ("vault", "finance_money"), ("safe", "finance_money"),
    ("stock", "finance_money"), ("trading", "finance_money"), ("wall_street", "finance_money"),
    ("bull", "finance_money"), ("bitcoin", "finance_money"), ("credit_card", "finance_money"),
    ("briefcase", "finance_money"), ("atm", "finance_money"),
    ("house", "property_home"), ("picket_fence", "property_home"), ("for_sale", "property_home"),
    ("suburb", "property_home"), ("moving_truck", "property_home"), ("moving_boxes", "property_home"),
    ("demolition", "property_home"), ("main_street", "property_home"), ("rural_road", "property_home"),
    ("school", "school_youth"), ("graduation", "school_youth"), ("playground", "school_youth"),
    ("surveillance", "surveillance_tech"), ("cctv", "surveillance_tech"), ("camera", "surveillance_tech"),
    ("cell_tower", "surveillance_tech"), ("smartphone", "surveillance_tech"), ("phone", "surveillance_tech"),
    ("binary", "surveillance_tech"), ("circuit", "surveillance_tech"), ("server", "surveillance_tech"),
    ("data_center", "surveillance_tech"), ("data_flow", "surveillance_tech"), ("fiber_optic", "surveillance_tech"),
    ("satellite", "surveillance_tech"), ("world_map", "surveillance_tech"), ("globe", "surveillance_tech"),
    ("hacker", "surveillance_tech"), ("radio_tower", "surveillance_tech"), ("security_monitor", "surveillance_tech"),
    ("technology_abstract", "surveillance_tech"), ("tv_static", "surveillance_tech"),
    ("document", "documents_paper"), ("contract", "documents_paper"), ("paperwork", "documents_paper"),
    ("newspaper", "documents_paper"), ("typewriter", "documents_paper"), ("quill", "documents_paper"),
    ("wax_seal", "documents_paper"), ("magnifying_glass", "documents_paper"), ("shredded", "documents_paper"),
    ("burning_paper", "documents_paper"), ("library", "documents_paper"),
    ("microphone", "documents_paper"),  # was stolen by `phone` via the substring bug
    # `rain_street` is the specific case and MUST stay ahead of the generic `street`
    # rule below (moved up from the atmosphere block when `street` was introduced).
    ("rain_street", "atmosphere_symbolic"),
    ("street", "urban_night"),  # 682 street files used to land in nature via `tree`
    ("city", "urban_night"), ("skyline", "urban_night"), ("drone", "urban_night"),
    ("traffic", "urban_night"), ("subway", "urban_night"), ("train", "urban_night"),
    ("airport", "urban_night"), ("parking_garage", "urban_night"), ("bridge", "urban_night"),
    ("highway", "urban_night"), ("rooftop", "urban_night"), ("office", "urban_night"),
    ("boardroom", "urban_night"), ("warehouse", "urban_night"), ("elevator", "urban_night"),
    ("stadium", "urban_night"), ("abandoned_factory", "urban_night"),
    ("mountain", "nature_landscape"), ("forest", "nature_landscape"), ("ocean", "nature_landscape"),
    ("tree", "nature_landscape"), ("desert", "nature_landscape"), ("snow", "nature_landscape"),
    ("storm", "nature_landscape"), ("harbor", "nature_landscape"), ("lighthouse", "nature_landscape"),
    ("cemetery", "nature_landscape"), ("church", "nature_landscape"), ("empty_road", "nature_landscape"),
    ("shadow", "atmosphere_symbolic"), ("silhouette", "atmosphere_symbolic"), ("mirror", "atmosphere_symbolic"),
    ("broken_window", "atmosphere_symbolic"), ("chair", "atmosphere_symbolic"), ("clock", "atmosphere_symbolic"),
    ("candle", "atmosphere_symbolic"), ("padlock", "atmosphere_symbolic"), ("chains", "atmosphere_symbolic"),
    ("keys", "atmosphere_symbolic"), ("hands", "atmosphere_symbolic"), ("chess", "atmosphere_symbolic"),
    ("fireplace", "atmosphere_symbolic"), ("spotlight", "atmosphere_symbolic"), ("rotary_phone", "atmosphere_symbolic"),
    ("telephone", "atmosphere_symbolic"),  # `phone` no longer matches inside `telephone`
    ("rain_on", "atmosphere_symbolic"),
    ("umbrella", "atmosphere_symbolic"), ("desk_lamp", "atmosphere_symbolic"), ("concrete_wall", "atmosphere_symbolic"),
    ("moody", "atmosphere_symbolic"),
    ("dark_cinematic", "abstract"), ("abstract", "abstract"),
    ("loop", "abstract_loop"),
]

_FX_BUCKET = {
    "light_assets": "light", "vfx_overlays": "vfx", "particle_assets": "particle",
    "texture_assets": "texture", "loops": "abstract_loop",
}


_SPLIT = re.compile(r"[^a-z0-9]+")


def tokenize(text: str | None) -> list[str]:
    """Lowercase `text` and split it into word tokens (`courthouse_steps` -> [courthouse, steps])."""
    return [t for t in _SPLIT.split((text or "").lower()) if t]


def _token_matches(token: str, rule_token: str) -> bool:
    """True if a subtype token satisfies a rule token on a WORD boundary.

    Exact token, regular plural (`gold_bar` -> `gold_bars`, `box` -> `boxes`), or a
    prefix of at least MIN_PREFIX characters (`court` -> `courthouse`/`courtroom`,
    `snow` -> `snowy`, `document` -> `documents`, `monitor` -> `monitors`).
    Never a suffix and never an infix: that is the whole bug class (`street` must
    not satisfy `tree`, `microphone` must not satisfy `phone`, `atmosphere` must
    not satisfy `atm`, `lighthouse`/`warehouse` must not satisfy `house`).
    """
    if token == rule_token:
        return True
    if token in (rule_token + "s", rule_token + "es"):
        return True
    return len(rule_token) >= MIN_PREFIX and token.startswith(rule_token)


def rule_hits(text: str | None, keyword: str) -> bool:
    """True if `keyword` (a `_`-joined token pattern) occurs in `text` on word boundaries."""
    toks = tokenize(text)
    kws = tokenize(keyword)
    if not kws or len(kws) > len(toks):
        return False
    last = len(kws) - 1
    for i in range(len(toks) - last):
        window = toks[i:i + len(kws)]
        if window[:last] == kws[:last] and _token_matches(window[last], kws[last]):
            return True
    return False


def theme_of(subtype: str | None, category: str | None = None) -> str:
    """Derive the theme for an asset from its subtype (and category for fx buckets).

    WARNING: this is a claim about the download QUERY, not about the pixels. It is
    40% wrong on the current shelf (FACTORY_LABEL_AUDIT.v001). Build-path selection
    must use scripts/factory_ledger_themes.py; this stays for legacy/offline callers
    and for files that have no ledger row yet.
    """
    if category in _FX_BUCKET:
        return _FX_BUCKET[category]
    for kw, theme in RULES:
        if rule_hits(subtype, kw):
            return theme
    return "misc_background" if category == "backgrounds" else "misc"
