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
"""
from __future__ import annotations

# Ordered (substring, theme). First match wins -> specific before general.
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
    ("rain_on", "atmosphere_symbolic"), ("rain_street", "atmosphere_symbolic"),
    ("umbrella", "atmosphere_symbolic"), ("desk_lamp", "atmosphere_symbolic"), ("concrete_wall", "atmosphere_symbolic"),
    ("moody", "atmosphere_symbolic"),
    ("dark_cinematic", "abstract"), ("abstract", "abstract"),
    ("loop", "abstract_loop"),
]

_FX_BUCKET = {
    "light_assets": "light", "vfx_overlays": "vfx", "particle_assets": "particle",
    "texture_assets": "texture", "loops": "abstract_loop",
}


def theme_of(subtype: str | None, category: str | None = None) -> str:
    """Derive the theme for an asset from its subtype (and category for fx buckets)."""
    if category in _FX_BUCKET:
        return _FX_BUCKET[category]
    s = (subtype or "").lower()
    for kw, theme in RULES:
        if kw in s:
            return theme
    return "misc_background" if category == "backgrounds" else "misc"
