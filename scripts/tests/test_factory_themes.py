# -*- coding: utf-8 -*-
"""Regression test for the factory taxonomy's word-boundary matching.

FACTORY_LABEL_AUDIT.v001 §5: `factory_themes.theme_of()` used to match its rule
keywords as bare substrings, so a keyword hidden inside a longer word won and
misfiled 1,968 files before any provider ever returned anything:

    tree   inside s-tree-t        682 street photos  -> nature_landscape
    house  inside light/ware-house 740 files         -> property_home
    phone  inside micro-phone      310 files         -> surveillance_tech
    atm    inside atm-osphere      236 files         -> finance_money

This locks the fix (word boundaries + plural + >=MIN_PREFIX prefix) AND locks the
legitimate compounds the naive "exact token only" fix would have broken.

Run:  python scripts/tests/test_factory_themes.py     (no pytest needed)
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from factory_themes import RULES, rule_hits, theme_of, tokenize  # noqa: E402

# (subtype, expected theme, why) -- the four measured bug classes plus telephone.
HIDDEN_KEYWORD_CASES = [
    ("snowy_street_night", "urban_night", "tree must not match street"),
    ("rain_street_reflection_night", "atmosphere_symbolic", "specific rain_street beats generic street"),
    ("homeless_person_on_street_night", "urban_night", "tree must not match street"),
    ("lighthouse_in_storm", "nature_landscape", "house must not match lighthouse"),
    ("warehouse_interior_dark", "urban_night", "house must not match warehouse"),
    ("warehouse_loading_dock", "urban_night", "house must not match warehouse"),
    ("moody_atmosphere_fog", "atmosphere_symbolic", "atm must not match atmosphere"),
    ("vintage_radio_microphone", "documents_paper", "phone must not match microphone"),
    ("red_rotary_telephone", "atmosphere_symbolic", "phone must not match telephone"),
]

# Compounds/plurals that MUST keep matching -- the strict-token fix broke these.
COMPOUND_CASES = [
    ("courthouse_steps", "legal_court", "court is a prefix of courthouse"),
    ("courtroom_interior", "legal_court", "court is a prefix of courtroom"),
    ("courtroom_empty_wide", "legal_court", "court is a prefix of courtroom"),
    ("documents_on_desk", "documents_paper", "document + plural"),
    ("stacked_legal_documents", "documents_paper", "document + plural"),
    ("gold_bars_stacked", "finance_money", "multi-token rule gold_bar + plural"),
    ("security_monitors_wall", "surveillance_tech", "security_monitor + plural"),
    ("stormy_sky_time_lapse", "nature_landscape", "storm is a prefix of stormy"),
    ("candlelit_room_dark", "atmosphere_symbolic", "candle is a prefix of candlelit"),
    ("handshake_business", "atmosphere_symbolic", "hands is a prefix of handshake"),
    ("test_tubes_rack_lab", "medical_lab", "multi-token rule test_tube + plural"),
    ("laboratory_glassware", "medical_lab", "laboratory spelled out (lab is 3 chars)"),
    ("atm_machine_at_night", "finance_money", "atm still matches as an exact token"),
    ("dna_helix_blue", "forensics_dna", "dna still matches as an exact token"),
    ("wall_street_sign", "finance_money", "wall_street stays ahead of generic street"),
    ("small_town_main_street", "property_home", "main_street stays ahead of generic street"),
    ("rain_on_city_street_neon", "urban_night", "city stays ahead of generic street"),
    ("white_house_exterior", "legal_court", "explicit white_house rule still wins"),
    ("suburban_house_exterior_night", "property_home", "house as a real token"),
    ("smartphone_in_dark", "surveillance_tech", "explicit smartphone rule"),
]

# Direct matcher assertions: the failure class must be impossible, not just unlikely.
NEGATIVE_HITS = [
    ("snowy_street_night", "tree"),
    ("street_lamp", "tree"),
    ("lighthouse_in_storm", "house"),
    ("warehouse_loading_dock", "house"),
    ("vintage_radio_microphone", "phone"),
    ("moody_atmosphere_fog", "atm"),
    ("hemisphere_view", "phone"),
]
POSITIVE_HITS = [
    ("lone_tree_in_field", "tree"),
    ("front_door_house", "house"),
    ("mobile_phone_map_location", "phone"),
    ("atm_machine_at_night", "atm"),
    ("courthouse_steps", "court"),
    ("gold_bars_stacked", "gold_bar"),
]


def main() -> int:
    failures: list[str] = []

    for subtype, expected, why in HIDDEN_KEYWORD_CASES + COMPOUND_CASES:
        got = theme_of(subtype, "backgrounds")
        if got != expected:
            failures.append(f"theme_of({subtype!r}) = {got!r}, want {expected!r}  ({why})")

    for text, kw in NEGATIVE_HITS:
        if rule_hits(text, kw):
            failures.append(f"rule_hits({text!r}, {kw!r}) matched inside a longer word")
    for text, kw in POSITIVE_HITS:
        if not rule_hits(text, kw):
            failures.append(f"rule_hits({text!r}, {kw!r}) failed to match a legitimate token")

    # fx categories keep bypassing the rules entirely
    if theme_of("anything_at_all", "light_assets") != "light":
        failures.append("fx category bucket regressed")
    if theme_of("nothing_here_matches_xyzzy", "backgrounds") != "misc_background":
        failures.append("unmatched background must fall back to misc_background")
    if tokenize("Courthouse-Steps_02") != ["courthouse", "steps", "02"]:
        failures.append("tokenize() regressed")

    # every rule keyword must still be able to match itself
    for kw, _theme in RULES:
        if not rule_hits(kw.strip("_"), kw):
            failures.append(f"rule {kw!r} cannot match its own keyword")

    if failures:
        print("FAIL factory_themes:")
        for f in failures:
            print("  -", f)
        return 1
    n = len(HIDDEN_KEYWORD_CASES) + len(COMPOUND_CASES) + len(NEGATIVE_HITS) + len(POSITIVE_HITS)
    print(f"PASS factory_themes: {n} cases "
          f"(street/lighthouse/warehouse/atmosphere/microphone/telephone + {len(RULES)} rule self-matches)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
