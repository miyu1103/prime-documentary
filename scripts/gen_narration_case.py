#!/usr/bin/env python3
"""Generic case-episode narration runner (ElevenLabs) — `--ep <EPID>`.

Invariant 14: this GENERALIZES the proven per-episode lineage (scripts/
gen_narration_morton.py, EP52, shipped) instead of adding a 21st per-episode
copy. All canon settings are preserved from that lineage + scripts/
gen_narration.py (miranda):
  - voice PINNED: Brian nPczCjzI2devNBz1zQrb / eleven_multilingual_v2
  - per-delivery voice settings (calm/building/intense) — the EP52-shipped
    presets that the voice_plan `delivery` vocabulary drives. (gen_narration.py
    EP1 used a single flat setting; EP39+ canon is per-delivery. Recorded as a
    deliberate canon choice: voice must match the last ~15 shipped episodes.)
  - loudnorm QC -16 LUFS / -1.5 TP / LRA 11 (applied once on the master;
    narration_index offsets are measured from the exact concatenated WAVs)
  - retry w/ backoff on 429/5xx, 3 attempts
  - sha-256 idempotency: a chunk is re-generated ONLY if its mp3 is missing/
    truncated or its sidecar text_sha256 no longer matches the script text.
    Re-runs never double-spend.
  - per-chunk provenance sidecar VC-NNNN.json + events.jsonl append
    (gen_narration.py pattern) with characters + estimated cost.

Paid API. Source of truth = the LOCKED _planning script (verbatim; extraction
is strictly subtractive — narration wording is never rewritten).

Outputs (mirrors PD-2026-052-morton exactly):
  episodes/<EPID>/06_audio/voice_plan.v001.json
  episodes/<EPID>/06_audio/narration_index.v001.json  (measured, ffprobe)
  <media>/episodes/<EPID>/06_voice/draft/VC-NNNN.mp3 (+ .json provenance)
  <media>/episodes/<EPID>/06_voice/master/vc_master_v001.mp3
  episodes/<EPID>/events.jsonl (narration_generated / narration_mastered)

--dry-run   prints every chunk, NO API call, NO writes.
--plan-only writes voice_plan only, no API call.
--remaster  skips TTS; rebuilds master + index from existing (already-paid)
            mp3s at zero cost; honours --gap-beat / --gap-section.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MODEL = "eleven_multilingual_v2"
VOICE_ID = "nPczCjzI2devNBz1zQrb"   # PINNED channel voice "Brian"
SCRIPT_REVISION = "v001"
TTS = "https://api.elevenlabs.io/v1/text-to-speech/{vid}?output_format=mp3_44100_128"
SETTINGS = {
    "calm": {"stability": 0.58, "similarity_boost": 0.80, "style": 0.14, "use_speaker_boost": True},
    "building": {"stability": 0.48, "similarity_boost": 0.82, "style": 0.30, "use_speaker_boost": True},
    "intense": {"stability": 0.38, "similarity_boost": 0.84, "style": 0.44, "use_speaker_boost": True},
}
DELIVERY_BY_SECTION = {
    "HOOK": "intense", "OP": "building", "ACT_1": "building", "ACT_2": "building",
    "ACT_3": "building", "ACT_4": "building", "ACT_5": "building", "ENDING": "calm",
    # EP60 (surfside) only: THE NIGHT is its own section because it is the only part of
    # that film in a different tense -- 1:22 a.m. itself, not "what had been happening".
    # Read intense, like the cold open, not "building".
    "THE_NIGHT": "intense",
}
# Canon 4-act order (EP52-55). Episodes with a different act count declare their own
# `sections` in the registry below (EP56 is the first 5-act case film).
SECTION_ORDER = ["HOOK", "OP", "ACT_1", "ACT_2", "ACT_3", "ACT_4", "ENDING"]
SECTION_ORDER_5ACT = ["HOOK", "OP", "ACT_1", "ACT_2", "ACT_3", "ACT_4", "ACT_5", "ENDING"]
# EP60 (surfside) is the first film with a tense break. Ten script headings --
# COLD OPEN / BRAND STING / OPENING / ACT I..ACT V / THE NIGHT / ENDING -- of which
# BRAND STING is narration-free (as in EP56), so NINE sections carry speech. THE NIGHT
# sits between ACT V and ENDING and is deliberately NOT folded into either: up to ACT V
# the film says what had been happening; THE NIGHT is 1:22 a.m. itself (~2:15).
SECTION_ORDER_5ACT_NIGHT = ["HOOK", "OP", "ACT_1", "ACT_2", "ACT_3", "ACT_4", "ACT_5",
                            "THE_NIGHT", "ENDING"]
# EP52/53/54/55 headings: `## COLD OPEN ...`, `## OPENING ...`, `## ACT I — ...`
# ... `## ACT IV — ...`, `## ENDING ...` (Roman numerals). Longer numerals FIRST.
# EP56 adds `## ACT V — ...` and a narration-free `## BRAND STING ...` card heading
# (the sting is a build element; it carries no spoken line — mapped to None so any
# text that ever lands under it is caught by the section-coverage gate, not silently
# absorbed into the neighbouring act).
SECTION_HEADINGS = [
    ("HOOK", re.compile(r"^COLD\s+OPEN\b", re.IGNORECASE)),
    # EP61 (weimer) heads its cold open `## HOOK` instead of `## COLD OPEN`. Without this
    # pattern the heading maps to no section, and because `started` is still False at that
    # point the orphan guard cannot see the lines either -- the whole cold open would have
    # been dropped in silence. No other registered script has a heading beginning "HOOK",
    # so this anchored pattern cannot change any existing extraction.
    ("HOOK", re.compile(r"^HOOK\b", re.IGNORECASE)),
    # `## OPENING` -> the contract key `OP` (NOT "OPENING"): the figure beats for every
    # episode are keyed to the spec section_vocabulary, so an index emitting "OPENING"
    # would leave those beats attached to nothing.
    ("OP", re.compile(r"^OPENING\b", re.IGNORECASE)),
    ("ACT_4", re.compile(r"^ACT\s+IV\b", re.IGNORECASE)),
    ("ACT_5", re.compile(r"^ACT\s+V\b", re.IGNORECASE)),
    ("ACT_3", re.compile(r"^ACT\s+III\b", re.IGNORECASE)),
    ("ACT_2", re.compile(r"^ACT\s+II\b", re.IGNORECASE)),
    ("ACT_1", re.compile(r"^ACT\s+I\b", re.IGNORECASE)),
    # EP62 (greene) heads its sections with the CONTRACT KEYS themselves -- `## OP`,
    # `## ACT_1` ... `## ACT_5` -- because episode_spec.v001.json tells the writer to
    # spell the headings the way section_vocabulary spells them (EP61 used `## OPENING`
    # where the contract said `OP`, and the mismatch had to be handed on as a warning).
    # None of these can collide with the prose forms above: `^OP\b` cannot match
    # "OPENING" (no word boundary between P and E), and `^ACT_N\b` cannot match
    # "ACT I"/"ACT IV" (underscore is a word character, `\s+` requires whitespace).
    ("OP", re.compile(r"^OP\b", re.IGNORECASE)),
    ("ACT_1", re.compile(r"^ACT_1\b", re.IGNORECASE)),
    ("ACT_2", re.compile(r"^ACT_2\b", re.IGNORECASE)),
    ("ACT_3", re.compile(r"^ACT_3\b", re.IGNORECASE)),
    ("ACT_4", re.compile(r"^ACT_4\b", re.IGNORECASE)),
    ("ACT_5", re.compile(r"^ACT_5\b", re.IGNORECASE)),
    # THE NIGHT (EP60): no other heading in any script begins with "THE", and this
    # pattern is anchored, so it can neither swallow nor be swallowed by the acts above.
    # It stays BELOW the ACT patterns anyway, since this list is matched in order and
    # the ACT entries are deliberately longest-numeral-first (ACT IV before ACT V before
    # ACT III/II/I).
    ("THE_NIGHT", re.compile(r"^THE\s+NIGHT\b", re.IGNORECASE)),
    ("ENDING", re.compile(r"^ENDING\b", re.IGNORECASE)),
]
# post-ENDING appendix headings (EP53 `Fact Correspondence & Self-Checks`,
# EP54 `Fact Correspondence & Revision Log`, EP55 `Fact Correspondence / ...`,
# plus the EP52 RUNTIME/SELF-CHECK forms).
STOP_HEADINGS = [
    re.compile(r"^Fact\s+Correspondence", re.IGNORECASE),
    re.compile(r"^RUNTIME\b", re.IGNORECASE),
    re.compile(r"^SELF-CHECK\b", re.IGNORECASE),
    re.compile(r"^\*?\[END OF NARRATION", re.IGNORECASE),
    re.compile(r"^事実対応表"),
    re.compile(r"^改稿ログ"),
    # EP66 (openfields) closes with four post-ENDING appendices -- WHAT CHANGED FROM v002 /
    # FACTUAL CORRECTIONS AGAINST v002 / DEPARTURES FROM THE FILM BIBLE / WHAT I WANTED TO SAY
    # AND COULD NOT. None of the patterns above match them, so the extractor would map them to
    # no section and the orphan guard would abort the run before a single character was spent.
    # All four are anchored; verified against every registered script (EP53-EP65) -- zero
    # heading in any of them matches, so no existing extraction changes.
    re.compile(r"^WHAT\s+CHANGED\b", re.IGNORECASE),
    re.compile(r"^FACTUAL\s+CORRECTIONS\b", re.IGNORECASE),
    re.compile(r"^DEPARTURES\s+FROM\b", re.IGNORECASE),
    re.compile(r"^WHAT\s+I\s+WANTED\b", re.IGNORECASE),
]

# Episode registry. design_speech_seconds = DESIGN §5 narration model (@178.1
# wpm, speech only, gaps excluded); band = the finished-film 29:00-31:00 model.
EPISODES = {
    "PD-2026-053-norfolk": {
        "planning": "EP53_norfolk_script.en.v001.md",
        "design_speech_seconds": 1564.9,   # DESIGN §5: 1564.9 × 1.150 ≈ 1799.6s film
    },
    "PD-2026-054-flowers": {
        "planning": "EP54_flowers_script.en.v001.md",
        "design_speech_seconds": 1579.3,   # DESIGN §5: 4,688 w @178.1wpm
    },
    "PD-2026-055-burge": {
        "planning": "EP55_burge_script.en.v001.md",
        "design_speech_seconds": 1582.1,   # DESIGN §5: 4,696 w @178.1wpm
    },
    "PD-2026-056-postoffice": {
        "planning": "EP56_postoffice_script.en.v001.md",
        # DESIGN §5: 4,750 w @178.1wpm = 1600.2s provisional; gap budget 181.8s +
        # endcard 9s -> 1791.0s (29:51) provisional inside the 1740-1860 band.
        "design_speech_seconds": 1600.2,
        # FIRST five-act case film (ACT I..ACT V) + a narration-free `## BRAND STING`.
        "sections": SECTION_ORDER_5ACT,
    },
    # EP57-59: same five-act shape as EP56 (COLD OPEN / BRAND STING / OPENING / ACT I..V /
    # ENDING). All three scripts are R3-locked; word counts are the MEASURED ones from each
    # DESIGN §5, not estimates.
    "PD-2026-057-fieldtest": {
        "planning": "EP57_fieldtest_script.en.v001.md",
        # DESIGN §5 (R3 re-locked): 4,673 w modelled at 172.0 wpm -- deliberately NOT 178.1,
        # because EP55 and EP56 both measured ~+71s slower than the channel model.
        "design_speech_seconds": 1630.1,
        "sections": SECTION_ORDER_5ACT,
    },
    "PD-2026-058-lejeune": {
        "planning": "EP58_lejeune_script.en.v001.md",
        # DESIGN §5: 4,738 w @178.1wpm = 1596.1s; total held at 1790.0s via the gap budget.
        "design_speech_seconds": 1596.1,
        "sections": SECTION_ORDER_5ACT,
    },
    "PD-2026-059-robosigning": {
        "planning": "EP59_robosigning_script.en.v001.md",
        # DESIGN §5 (R3 re-derived): 4,670 w @178.1wpm = 1573.3s + gap 200.7 + endcard 9.
        "design_speech_seconds": 1573.3,
        "sections": SECTION_ORDER_5ACT,
    },
    "PD-2026-060-surfside": {
        # LOCKED script is v004 ("v004, もう変えません" -- owner). v003 under
        # episodes/PD-2026-060-surfside/03_script/ is stale and must not be used.
        # v005 supersedes v004: four assertions that nobody had been criminally prosecuted
        # were removed because no source held here supported them, and replaced with what the
        # Miami-Dade State Attorney actually published -- a grand jury convened July 2021 and
        # its December 2021 report, titled "Surfside Condo Collapse: Recommendations to Make
        # Buildings Safer". Absence of reporting is not evidence of absence. Do not use v004.
        "planning": "EP60_surfside_script.en.v005.md",
        # FILM BIBLE v001 (line 3): 40:00 film, narration approximately 36:00, band
        # 6,150-6,350 words at the MEASURED 173 wpm -- deliberately NOT the 178.1 channel
        # model. Extraction of the locked v004 script measures 6,302 narration words, so
        # 6302 / 173 * 60 = 2185.7s (36:26): inside the bible band and on its 36:00 target.
        "design_speech_seconds": 2185.7,
        # Ten script headings; BRAND STING carries no narration (as in EP56), so NINE
        # speech sections, with THE NIGHT standing alone between ACT V and ENDING.
        "sections": SECTION_ORDER_5ACT_NIGHT,
    },
    "PD-2026-061-weimer": {
        # LOCKED script is v003. v001 and v002 are stale and must not be used.
        # v004 supersedes v003: +72 lines of pure insertion, no deletion, 4,408 -> 5,435 words.
        # The design model assumed 173 wpm; this voice measured 194.3 on EP61 and 191.4 on EP60,
        # so a script inside the contract word band still landed 1.7 minutes under its own
        # runtime floor. ACT IV, HOOK and ENDING are byte-identical to v003.
        "planning": "EP61_weimer_script.en.v004.md",
        # ASSEMBLY_HANDOFF v001 step 2: 4,401 narration words / 25.4 min speech.
        "design_speech_seconds": 1524.0,
        # Nine script headings -- HOOK / BRAND STING / OPENING / ACT I..ACT V / ENDING --
        # of which BRAND STING carries no narration (as in EP56/EP60), so EIGHT speech
        # sections, exactly matching episode_spec.v001.json section_vocabulary
        # (HOOK, OP, ACT_1..ACT_5, ENDING) that the 99 figure beats are keyed to.
        "sections": SECTION_ORDER_5ACT,
    },
    "PD-2026-062-greene": {
        # LOCKED script is v003. v001, v002 and v004 are stale and must not be used.
        # v003 is the verified pass: 77 verbatim runs re-checked against 456 U.S. 444 with
        # zero fabrications and zero misattributions, all ten logged defects closed, and the
        # amicus attribution at line 247 corrected to scope "urged the Court to affirm" to
        # the Antioch School of Law alone (what the reporter supports).
        "planning": "EP62_greene_script.en.v003.md",
        # FINISHED-RATE model, not the raw speech rate. EP60 and EP61 measured 178.4 and
        # 178.3 words per finished minute -- that figure already carries the pipeline's own
        # inter-chunk gaps (143 s on EP60, 161 s on EP61). 5,250 narration words / 178.35
        # = 1766 s (29:26), inside the contract band [1620, 1920]. The 191-195 wpm raw
        # speech rate is NOT used here: it charges nothing for the gaps and would report
        # this script as short.
        "design_speech_seconds": 1766.0,
        # Eight headings, spelled as episode_spec.v001.json section_vocabulary spells them:
        # HOOK / OP / ACT_1..ACT_5 / ENDING. Every one carries narration (no BRAND STING).
        "sections": SECTION_ORDER_5ACT,
        # PINNED per-episode voice settings (owner instruction 2026-08-04). EP60 and EP61
        # recorded only voice_id and model_id, so pace parity across episodes is unproven
        # and check_script_length still carries a 237 wpm fast-end risk from two episodes
        # whose settings had drifted. These override the per-delivery presets' stability
        # and similarity_boost for EVERY chunk of this episode and are written into
        # voice_plan.v001.json and the narration index provenance.
        "voice_settings": {"stability": 0.35, "similarity_boost": 0.80},
    },
    "PD-2026-063-correa": {
        # LOCKED script is v002. v001 is stale and must not be used.
        "planning": "EP63_correa_script.en.v002.md",
        # FINISHED-RATE model, as EP62 -- not a raw speech rate. The script derives its own
        # section windows from 176 words per FINISHED minute (script line 9; episode_spec
        # notes 2026-08-04: EP60 191.4 wpm and EP61 194.3 wpm of raw speech become ~176 once
        # gap_beat 0.30s and gap_section 1.80s are charged). 5,278 narration words / 176 wpm
        # = 1799.3s (29:59), inside the contract band [1620, 1920].
        "design_speech_seconds": 1799.3,
        # Eight headings, spelled as episode_spec.v001.json section_vocabulary spells them:
        # HOOK / OP / ACT_1..ACT_5 / ENDING -- each carrying a parenthetical window,
        # e.g. `## ACT_1 (0:27-5:13 - 839 w)`. Every pattern in SECTION_HEADINGS is anchored
        # on the key with a word boundary, so the parenthetical changes nothing. VERIFIED
        # before spending: all eight sections extract non-empty (373 chunks / 5,315 tokens),
        # and the per-section counts reconcile with the script's declared 20/58/839/1,096/
        # 1,110/991/823/341 once the 36 standalone em-dash tokens are discounted.
        "sections": SECTION_ORDER_5ACT,
        # PINNED per-episode voice settings, identical to EP62 so the two ARE comparable.
        # EP62 measured 169.8 words per finished minute at exactly these values. EP60 and
        # EP61 recorded no settings at all, which is why neither can be compared to anything.
        "voice_settings": {"stability": 0.35, "similarity_boost": 0.80},
    },
    "PD-2026-064-memphis": {
        # LOCKED script is v002. v001 is stale and must not be used: ML-60 (the Trigg line
        # "A public utility should not be able to coerce a customer to pay a disputed claim")
        # was deleted from v002 with no record and restored on 2026-08-04, and two writer-
        # voice sentences were tightened in the same pass to stay inside the word ceiling.
        "planning": "EP64_memphis_script.en.v002.md",
        # MEASURED, not modelled. The full master WAS generated on the 5,393-word text and
        # ffprobed: 06_audio/narration_index.v001.json total_seconds = 2023.1s (33:43) against
        # a contract ceiling of 1920s -- 103s over. 5,379 index words / 2023.1s = 159.5 words
        # per FINISHED minute, so the 176 model was optimistic by 10% and the 169.1 fallback
        # by 6%. The script was cut to 5,105 narration words on 2026-08-06, which projects
        # 1915.1s (31:55) finished and 1796.1s of pure speech at that measured rate.
        # Re-ffprobe after regeneration and check total_seconds against 1920 before spending
        # anything downstream.
        "design_speech_seconds": 1796.1,
        "sections": SECTION_ORDER_5ACT,
        # PINNED, identical to EP62 and EP63 so the three ARE comparable.
        "voice_settings": {"stability": 0.35, "similarity_boost": 0.80},
    },
    "PD-2026-065-marmet": {
        # LOCKED script is v002. Repaired 2026-08-05: two sentences reattributed from
        # Brown I (2011) to Brown II (2012), L130-L144 rewritten at net zero words, and the
        # ENDING's re-report of a disposition cut from 69 words to 30.
        "planning": "EP65_marmet_script.en.v002.md",
        # FINISHED-RATE model. Script line 7 derives every window from 176 w/finished-min.
        # 5,133 narration words / 176 = 1749.9s (29:10), inside the contract band.
        # At EP62's measured 169.1 this becomes 1821s -- still inside, with the most room of
        # the four. This is the shortest script on the slate.
        "design_speech_seconds": 1749.9,
        "sections": SECTION_ORDER_5ACT,
        "voice_settings": {"stability": 0.35, "similarity_boost": 0.80},
    },
    "PD-2026-066-openfields": {
        # LOCKED script is v003. v001 and v002 are stale and must not be used: both were
        # written against a 1620 s / 4565-word floor and held it with ~590 words of restored
        # material that carried every factual error the three reads found.
        "planning": "EP66_openfields_script.en.v003.md",
        # RAW SPEECH model, measured -- not the finished-rate model EP62-65 used, because this
        # is the number the runner prints against `speech_seconds` (gaps excluded). EP65 was
        # generated at exactly these voice settings and ffprobed 5,074 index words over
        # 1767.083 s of speech = 172.3 raw wpm. This script extracts 4,262 narration words:
        # 4262 / 172.3 * 60 = 1484.4 s of pure speech. Adding this episode`s own gap budget
        # (7 section boundaries at 1.8 s, 263 beat gaps at 0.3 s, and the four designed holds
        # totalling 18.0 s) projects a 1593 s master (26:33) and a 1602 s film once
        # ENDCARD_SEC is added -- inside episode_spec runtime_seconds [1500, 1980].
        "design_speech_seconds": 1484.4,
        "sections": SECTION_ORDER_5ACT,
        # PINNED, identical to EP62-65 so all five ARE comparable.
        "voice_settings": {"stability": 0.35, "similarity_boost": 0.80},
    },
    "PD-2026-067-ramirez": {
        # LOCKED script is v002. v001 is stale and must not be generated from.
        # v001 WAS generated in full and ffprobed: 278 chunks / 4,044 index words /
        # 1354.425 s of speech / a 1448.020 s master. With ENDCARD_SEC 9.0 that is a 1457.0 s
        # film against episode_spec runtime_seconds [1560, 1895] -- 103 s UNDER the declared
        # floor. The prediction above had warned of ~45 s; the delivery was worse.
        # ROOT CAUSE, and it was not a short script: script_words [4400, 5000] was derived from
        # check_script_craft.narration_lines() returning 4,682, a count that included the
        # script's front matter (182 w), the continuation lines of every wrapped 【…】 production
        # note (217 w) and the post-ENDING appendix (282 w). The spoken text was 4,044 all
        # along. narration_lines was fixed on 2026-08-11 to delegate to extract_events in THIS
        # file, so the craft gate and the TTS runner can no longer disagree about what a
        # narration word is.
        # v002 is v001 plus 447 narration words of PURE INSERTION -- no v001 line is deleted or
        # reworded, which is what keeps the sha-256 idempotency of all 278 paid chunks intact.
        # The 24 new chunks were inserted mid-script, so the existing draft mp3s and their
        # sidecars were RENUMBERED on disk to their new positions before this run
        # (scripts/renumber_voice_chunks.py, EP66 route): $0.74 of new audio instead of $7.72
        # of re-billing.
        "planning": "EP67_ramirez_script.en.v002.md",
        # RAW SPEECH model, and now MEASURED rather than borrowed. v001's own master gives the
        # rate for this voice on this script: 4,044 index words / 1354.425 s = 179.15 raw wpm.
        # v002 extracts 4,494 index words: 4494 / 179.15 * 60 = 1505.1 s of pure speech. Its
        # gap budget is 7 section boundaries at 1.8 s plus 294 beat gaps at 0.30 s = 100.8 s
        # (there are no scripted holds), projecting a 1605.9 s master and a 1614.9 s film once
        # ENDCARD_SEC 9.0 is added -- inside [1560, 1895] with 55 s over the floor.
        # Checked at the slow edge of PD_CANON rule 25 as well: the DELIVERED end-to-end rate on
        # v001 was 4,044 / 1448.020 s = 167.6 wpm, NOT the 179.1 the runner printed (speech only,
        # 6.9% fast). At 159.5 end-to-end wpm the v002 film is 1699.9 s; at 169.7 it is 1597.6 s.
        # Both inside the band. The band is not widened, at either end.
        "design_speech_seconds": 1505.1,
        # Eight headings, spelled as episode_spec.v001.json section_vocabulary spells them:
        # HOOK / OP / ACT_1..ACT_5 / ENDING. Every one carries narration (no BRAND STING).
        "sections": SECTION_ORDER_5ACT,
        # PINNED, identical to EP62-66 so all six ARE comparable.
        "voice_settings": {"stability": 0.35, "similarity_boost": 0.80},
    },
    "PD-2026-068-pinto": {
        # LOCKED script is v002. v001 is the verified text but must not be generated from:
        # it hard-wrapped every paragraph at ~100 columns, and this extractor makes ONE TTS
        # chunk per physical prose line, so v001 yields 500 chunks (against EP66's 277 for a
        # longer script) with ~170 breaks falling mid-sentence -- three of them the fragments
        # "A", "In", "In", which assert_clean refuses outright. v002 joins the wrapped lines
        # of each paragraph and changes nothing else: the extracted narration text of the two
        # files is byte-identical, both measure 4,895 narration words under check_script_craft,
        # and every craft gate is green on both. v002 extracts 332 chunks.
        "planning": "EP68_pinto_script.en.v002.md",
        # RAW SPEECH model, as EP66/EP67 -- this is the number the runner prints against
        # `speech_seconds`, which excludes inter-chunk silence. EP66 was generated at exactly
        # these voice settings and ffprobed 4,278 index words over 1494.118 s of speech =
        # 171.8 raw wpm. This script extracts 4,902 index words: 4902 / 171.79 * 60 = 1712.1 s
        # of speech. This episode's own gap budget is 110.5 s -- 324 beat gaps at 0.30 s,
        # SIX section boundaries at 1.8 s rather than seven (the ACT_3 -> ACT_4 boundary is
        # overridden by the script's own 2.5 s hold at the TURN), and that 2.5 s hold --
        # projecting a 1822.6 s master (30:23) and a 1831.6 s film once ENDCARD_SEC 9.0 is
        # added, inside episode_spec runtime_seconds [1560, 1895]. Checked at the slow edge
        # too: at the slowest END-TO-END rate in PD_CANON rule 25 (159.5 wpm) the master is
        # 1844.0 s and the film 1853.0 s, still inside. Do NOT quote the runner's printed
        # "measured wpm" as the delivered pace -- it is speech-only and ran 7% fast on EP66
        # (printed 171.8, delivered 160.0 end-to-end).
        "design_speech_seconds": 1712.1,
        # Eight headings, spelled as episode_spec.v001.json section_vocabulary spells them:
        # HOOK / OP / ACT_1..ACT_5 / ENDING. Every one carries narration (no BRAND STING).
        "sections": SECTION_ORDER_5ACT,
        # PINNED, identical to EP62-67 so all seven ARE comparable.
        "voice_settings": {"stability": 0.35, "similarity_boost": 0.80},
    },
    # EP70/71 registered 2026-08-17. Narration needs only the script -- no images, no GPU, no
    # archive drive -- so both were started while the GPU was busy converting EP66-69 and while
    # H: (which holds the only copy of their plates) was unavailable. design_speech_seconds
    # below is PROVISIONAL until the dry run prints the real index word count; it is corrected
    # in place before any paid call, never left as a guess.
    "PD-2026-070-wronghouse": {
        "planning": "EP70_wronghouse_script.en.v001.md",
        # 45-minute flagship. episode_spec runtime_seconds [2445, 2835].
        # MEASURED by the dry run: 542 chunks / 6,958 index words / 38,658 chars.
        # Modelled at the RAW SPEECH rate 171.79 wpm -- the rate EP66 actually ffprobed at these
        # exact voice settings, not the runner's printed 178.1, which is speech-only and ran ~7%
        # fast on EP66 (PD_CANON rule 25). 6958 / 171.79 * 60 = 2430.2 s of speech.
        # Gap budget 172.8 s: 534 beat gaps at 0.30 s, seven section boundaries at 1.8 s, no
        # scripted silence in this script. Master 2603.0 s, film 2612.0 s (43:32) once ENDCARD
        # 9.0 is added -- inside [2445, 2835] with 167 s of headroom at the low edge.
        "design_speech_seconds": 2430.2,
        "sections": SECTION_ORDER_5ACT,
        "voice_settings": {"stability": 0.35, "similarity_boost": 0.80},
    },
    "PD-2026-071-oroville": {
        "planning": "EP71_oroville_script.en.v001.md",
        # 30 minutes. episode_spec runtime_seconds [1625, 1900].
        # MEASURED by the dry run: 343 chunks / 4,778 index words / 26,251 chars.
        # Same raw-speech model as EP70 above: 4778 / 171.79 * 60 = 1668.9 s of speech.
        # Gap budget 122.1 s: 335 beat gaps at 0.30 s, seven section boundaries at 1.8 s, and
        # 9.0 s of scripted silence the extractor found. Master 1791.0 s, film 1800.0 s (30:00)
        # with ENDCARD 9.0 -- inside [1625, 1900].
        "design_speech_seconds": 1668.9,
        "sections": SECTION_ORDER_5ACT,
        "voice_settings": {"stability": 0.35, "similarity_boost": 0.80},
    },
    "PD-2026-072-lacmegantic": {
        "planning": "EP72_lacmegantic_script.en.v003.md",
        # 30 minutes. episode_spec runtime_seconds [1740, 1920], script_words [4600, 4800].
        # The script measures 5,044 narration words (check_script_length, 2026-08-20). Modelled on
        # the SAME raw-speech rate this runner has measured for every episode since EP66 --
        # 171.79 raw wpm, speech only, gaps excluded: 5044 / 171.79 * 60 = 1761.6 s of speech.
        # Gap budget, using EP71's ratio of ~14 index words per chunk (343 chunks / 4,778 words):
        # about 360 chunks -> 353 beat gaps at 0.30 s = 105.9 s, plus seven section boundaries at
        # 1.8 s = 12.6 s. No scripted silence is declared in this script. Master ~1880.1 s and film
        # ~1889.1 s (31:29) once ENDCARD 9.0 is added -- inside [1740, 1920] with 31 s of headroom
        # at the high edge. Cross-checked against PD_CANON rule 25's END-TO-END band (159.5-169.7
        # wpm), which is the delivered pace rather than the runner's speech-only figure: 5,044
        # words lands between 1783 s (29:43) and 1897 s (31:37). Both edges are inside the band,
        # which is why this script was NOT padded further after check_script_length's 178.1 wpm
        # model implied 28.3 min -- that model is faster than anything this channel has delivered.
        # ★ SUPERSEDED BY MEASUREMENT, 2026-08-20. `--measure-section ACT_1` generated 39 chunks /
        # 523 words and ffprobed 164.214 s of speech: **191.1 raw wpm**, and 178.7 words per
        # FINISHED minute once the 38 beat gaps are counted. That is materially faster than the
        # 171.79 raw wpm this registry models for every episode since EP66 -- this script is short
        # declaratives with a full stop every ten words, and the voice delivers them quickly.
        # The script was then written to the measured rate rather than to the model. At the final
        # dry run it extracts 378 chunks / 5,276 index words:
        #   speech   5276 / 191.1 * 60 = 1656.4 s
        #   gaps     377 beat gaps at 0.30 s = 113.1 s, seven section boundaries at 1.8 s = 12.6 s,
        #            0.6 s of scripted silence -> 126.3 s
        #   master   1782.7 s, film 1791.7 s (29:52) once ENDCARD 9.0 is added
        # Inside episode_spec runtime_seconds [1740, 1920] with 52 s of headroom at the low edge
        # and 128 s at the high edge. Cross-check on the finished-minute figure: 5276 / 178.7 =
        # 29.52 min + 12.6 s of section gaps + 9 s endcard = 1793.1 s (29:53). The two agree to
        # within 1.4 s.
        "design_speech_seconds": 1656.4,
        "sections": SECTION_ORDER_5ACT,
        "voice_settings": {"stability": 0.35, "similarity_boost": 0.80},
    },
    "PD-2026-074-itaewon": {
        "planning": "EP74_itaewon_script.en.v005.md",
        # 30 minutes. episode_spec runtime_seconds [1740, 1920], script_words [4900, 5400].
        # The word band was set from MEASUREMENT, not from the 171.79 raw-wpm model this registry
        # carries for every episode since EP66. EP72 measured 191.1 raw wpm on its own ACT_1 and
        # then shipped 5,276 index words -> 1656.4 s speech -> a 1791.7 s film (29:52) against a
        # declared band of [4600, 4800] that its film could never have satisfied. EP74 is written
        # in the same register (short declaratives, a full stop every ten words).
        # * MEASURED 2026-08-21, and this line is no longer provisional. `--measure-section ACT_1`
        # generated 49 chunks / 734 words and ffprobed 222.025 s of speech = **198.4 raw wpm**, and
        # 186.3 words per FINISHED minute once the 48 beat gaps are counted. That is 15.5% faster
        # than the 171.79 this registry models and 3.8% faster than EP72's 191.1 -- this episode's
        # own voice at these settings. The script was then written to the measurement rather than to
        # the model, across four revisions (3,883 -> 4,669 -> 5,267 -> 5,511 words), and the word
        # band in episode_spec was re-derived from the runtime band twice as the rate sharpened,
        # ending at [5370, 5930]. At the v004 dry run it extracts 327 chunks / 5,511 index words:
        #   speech   5511 / 198.4 * 60 = 1666.6 s
        #   gaps     326 beat gaps at 0.30 s = 97.8 s, seven section boundaries at 1.8 s = 12.6 s,
        #            no scripted silence declared -> 110.4 s
        #   master   1777.0 s, film 1786.0 s (29:46) once ENDCARD 9.0 is added
        # Inside episode_spec runtime_seconds [1740, 1920] with 46 s of headroom at the low edge and
        # 134 s at the high edge. Cross-check on the finished-minute figure: 5511 / 186.3 = 29.58
        # min + 12.6 s of section gaps + 9 s endcard = 1796.5 s (29:57); the two agree to within
        # 10.5 s, both inside the band.
        "design_speech_seconds": 1727.1,
        "sections": SECTION_ORDER_5ACT,
        "voice_settings": {"stability": 0.35, "similarity_boost": 0.80},
    },
    "PD-2026-076-morandi": {
        "planning": "EP76_morandi_script.en.v001.md",
        # 30 minutes. episode_spec runtime_seconds [1740, 1920], script_words [4900, 5400].
        # PROVISIONAL, for the same stated reason as EP74 and EP75. The 171.79 raw-wpm model this
        # registry carried from EP66 to EP71 is 11% slow for this register: EP72 measured 191.1 raw
        # wpm on its own ACT_1 and shipped a 29:52 film. EP76 is written in the same register --
        # short declaratives, verbatim findings from the MIT Commissione Ispettiva read plainly.
        # Modelled here at the measured rate: 5,150 words (the midpoint of the declared band)
        # / 191.1 * 60 = 1616.9 s of speech.
        # * SUPERSEDED THE MOMENT `--measure-section ACT_1` IS RUN FOR THIS EPISODE. That
        # measurement governs over this line; rewrite design_speech_seconds from it, and from the
        # dry run's real chunk count, before any full run.
        # MEASURED 2026-08-21, not modelled. `--measure-section ACT_1` generated 46 chunks / 650
        # words at the pinned voice settings and ffprobed 211.906 s of speech = 184.0 raw wpm
        # (173.0 words per FINISHED minute once its 45 beat gaps are added). The script extracts
        # 328 chunks / 5,118 words: 5118 / 184.0 * 60 = 1669.0 s of speech. Gap budget 108.6 s
        # (320 beat gaps at 0.30 s = 96.0 s, plus seven section boundaries at 1.8 s = 12.6 s),
        # projecting a 1777.6 s master (29:38) and a 1786.6 s film (29:47) once ENDCARD_SEC 9.0
        # is added -- inside episode_spec runtime_seconds [1740, 1920], and 5,118 words is inside
        # script_words [4900, 5400].
        "design_speech_seconds": 1669.0,        "sections": SECTION_ORDER_5ACT,
        "voice_settings": {"stability": 0.35, "similarity_boost": 0.80},
    },
    "PD-2026-075-lahaina": {

        "planning": "EP75_lahaina_script.en.v001.md",
        # 30 minutes. episode_spec runtime_seconds [1740, 1920], script_words [4900, 5400].
        # PROVISIONAL, and provisional for a stated reason. The 171.79 raw-wpm model this registry
        # carried from EP66 to EP71 is 11% slow for this register: EP72 measured 191.1 raw wpm on
        # its own ACT_1 and shipped a 29:52 film against a word band its own spec could not have
        # satisfied. EP75 is written in the same register -- short declaratives, verbatim findings
        # read plainly -- so it is modelled here at the measured rate rather than at the model.
        # * SUPERSEDED BY MEASUREMENT, 2026-08-21, exactly as that line required.
        # `--measure-section ACT_1` generated 54 chunks / 808 words and ffprobed 259.133 s of
        # speech: **187.1 raw wpm**, and 176.3 words per FINISHED minute once the 53 beat gaps are
        # counted. That is 8.9% faster than the registry's 171.79 model and 2.1% slower than
        # EP72's measured 191.1 -- same register, slightly longer sentences, because this script
        # reads numbered findings verbatim. The script was then written to THIS number.
        # At the dry run it extracts 349 chunks / 5,321 index words:
        #   speech   5338 / 187.1 * 60 = 1711.9 s
        #   gaps     356 beat gaps at 0.30 s = 106.8 s, seven section boundaries at 1.8 s = 12.6 s,
        #            no scripted silence declared -> 119.4 s
        #   master   1831.3 s, film 1840.3 s (30:40) once ENDCARD 9.0 is added
        #   (5,321 words at the first dry run; 5,338 after LH-38 was upgraded to the read CBS
        #   source SRC-0014 and the paraphrase replaced with the two verbatim quotations)
        # Inside episode_spec runtime_seconds [1740, 1920] with 92 s of headroom at the low edge and
        # 88 s at the high edge -- the most centred projection of any episode in this registry.
        # Cross-check on the finished-minute figure: 5321 / 176.3 = 30.18 min + 12.6 s of section
        # gaps + 9 s endcard = 1832.5 s. The two agree to within 0.1 s.
        # DELIVERED 2026-08-21: made=311 skipped=46 failed=0. Speech total 1740.1 s against this
        # 1711.9 s model (+28.2 s, 1.6%); measured end-to-end 184.1 wpm against the 187.1 measured on
        # ACT_1 alone. Master 1857.403 s, film 1866.4 s (31:06) with ENDCARD 9.0 -- inside
        # runtime_seconds [1740, 1920] with 126 s of headroom low and 54 s high.
        "design_speech_seconds": 1740.1,
        "sections": SECTION_ORDER_5ACT,
        "voice_settings": {"stability": 0.35, "similarity_boost": 0.80},
    },
    "PD-2026-069-hyatt": {
        "planning": "EP69_hyatt_script.en.v001.md",
        # RAW SPEECH model, as EP66/EP67/EP68 -- this is the number the runner prints against
        # `speech_seconds`, which excludes inter-chunk silence. EP66 was generated at exactly
        # these voice settings and ffprobed 4,278 index words over 1494.118 s of speech =
        # 171.79 raw wpm. This script extracts 339 chunks / 4,702 index words:
        # 4702 / 171.79 * 60 = 1642.3 s of speech. Its own gap budget is 139.5 s -- 329 beat
        # gaps at 0.30 s, SIX section boundaries at 1.8 s rather than seven (the ACT_1 -> ACT_2
        # boundary is overridden by the 22.0 s H2 assembly hold), and the 30.0 s of designed
        # silence below -- projecting a 1781.8 s master (29:42) and a 1790.8 s film once
        # ENDCARD_SEC 9.0 is added, inside episode_spec runtime_seconds [1560, 1895].
        # FILM BIBLE line 144 models the same film at 1798.5 s from a 160.0 words-per-FINISHED-
        # minute rate; the two agree to within 8 s. Checked at both edges of PD_CANON rule 25
        # (159.5-169.7 end-to-end wpm): 1777.9 s and 1671.5 s of film, both inside the band.
        # Do NOT quote the runner's printed "measured wpm" as the delivered pace -- it is
        # speech-only and ran 7% fast on EP66 (printed 171.8, delivered 160.0 end-to-end).
        "design_speech_seconds": 1642.3,
        # Eight headings, spelled as episode_spec.v001.json section_vocabulary spells them:
        # HOOK / OP / ACT_1..ACT_5 / ENDING. Every one carries narration (no BRAND STING).
        "sections": SECTION_ORDER_5ACT,
        # PINNED, identical to EP62-68 so all eight ARE comparable.
        "voice_settings": {"stability": 0.35, "similarity_boost": 0.80},
        # FOUR DESIGNED SILENCES, declared here rather than parsed out of the script.
        # EP66 wrote its holds as `【4 seconds. ... Silence 1 of 4.】` and NOTE_SILENCE reads
        # them. EP69 writes every direction as a MULTI-LINE blockquoted note (`> 【... 3.0 s
        # ... Hold black 2.5 s ...】`), which the in_note tracker in extract_events correctly
        # swallows whole -- so no hold survives extraction, and a run without this table
        # produces a master with ZERO scripted silence in it. Parsing the notes generically
        # is not safe here and was rejected after measuring it: the ACT_4 opening note repeats
        # the TURN hold ("TURN at 16:28: music out, 2.5 s of silence") that line 442 also
        # states, so a scan double-counts it, and the ENDING note's "BrandEndcard runs 9.0 s"
        # would be picked up as a narration gap. The anchors below are matched as substrings
        # and every one MUST hit exactly one chunk or the run aborts before spending.
        # Budget: 22.0 + 5.5 + 2.5 = 30.0 s, exactly EP69_hyatt_FILM_BIBLE.v001.md line 144
        # (H2 22.0 / TURN 2.5 / 7:05 black 2.5 / H5 pull-through 3.0).
        "designed_silence_total_seconds": 30.0,
        "designed_silences": [
            {"after": "Nothing behind any of them if one let go.", "seconds": 22.0,
             "why": "script line 187-189, head of ACT_2: H2 runs at full length, the connection "
                    "assembling itself in one continuous move, 22 seconds, no narration over it. "
                    "Replaces the 1.8 s ACT_1 -> ACT_2 section gap."},
            {"after": "Five minutes past seven.", "seconds": 5.5,
             "why": "script line 370-373: H5 THE PULL-THROUGH 3.0 s, then cut to black and cut "
                    "the sound, hold black 2.5 s, then the 7:05 PM card. Contiguous, so the two "
                    "holds are one 5.5 s gap in the audio; the bible budgets them separately."},
            {"after": "everything in this act is read out of it.", "seconds": 2.5,
             "why": "script line 442, the TURN at FILM BIBLE 16:28: music out, 2.5 s of silence, "
                    "the H4 load bar alone on screen, then NBS Conclusion 1 read straight."},
        ],
    },
}

GAP_BEAT, GAP_SECTION = 0.30, 1.8          # EP52-shipped defaults
LOUDNORM = "loudnorm=I=-16:TP=-1.5:LRA=11"
COST_PER_1K_CHARS_USD = 0.30

CJK = re.compile(r"[　-〿぀-ゟ゠-ヿ㐀-䶿一-鿿＀-￯]")
SILENCE_LINE = re.compile(r"DESIGNED SILENCE\s+([0-9]+(?:\.[0-9]+)?)\s*s", re.IGNORECASE)
# A held beat is a production direction, never narration: `【beat ...】` (EP52 lineage) or
# EP60's `⟨HELD⟩`, which the EP60 film bible defines as the marker for "an isolated slow-read
# line". Both become a BEAT_SECONDS pause after the preceding chunk instead of spoken text.
BEAT_LINE = re.compile(r"^(?:【\s*beat\b|⟨\s*(?:HELD|BEAT)\s*⟩)", re.IGNORECASE)
BEAT_SECONDS = 0.6
# EP66 (openfields) budgets its four designed holds in prose inside the production-note
# brackets -- 【4 seconds. The empty track, still. Silence 1 of 4.】 -- rather than with the
# EP52-lineage "DESIGNED SILENCE 4s" string. Its own script section 3 fixes the budget at
# 4 + 5 + 4 + 5 = 18 s; at BEAT_SECONDS those four holds would collapse to 0.6 s each and the
# film would lose every one of them, with no way to put them back once the master exists.
# The pattern is deliberately narrow: the line must OPEN with 【, must carry the word
# silence/held/hold inside the same bracket, and the number must be followed by "second(s)".
# Measured against every script in episodes/_planning: it matches the four EP66 v003 lines
# (4, 5, 4, 5) and NOTHING in EP53-EP65, so no registered episode changes.
NOTE_SILENCE = re.compile(
    r"^【(?=[^】]*(?:[Ss]ilence|[Hh]eld|[Hh]olds?)\b)[^】]*?(\d+(?:\.\d+)?)\s*seconds?\b")
# A citation comment on its own line: EP66 v003 puts one under every factual line (175 of
# them) carrying its facts-ledger row id. Nothing in it is narration. Without this the line
# is tokenised as prose and READ ALOUD -- assert_clean cannot catch it, because "<!-- TN-13
# ✓ VERBATIM -->" contains none of the markup characters that gate looks for. Verified: zero
# occurrences of "<!--" in any registered script (EP53-EP65).
HTML_COMMENT = re.compile(r"^<!--")
# A trailing italic revision footer, e.g. EP61 v003 line 519:
#   *v001 · 2026-08-03 · facts locked to ... · hook to be rewritten last per SPEC v2 row 9.*
# It sits UNDER the ENDING heading with no appendix heading above it, so STOP_HEADINGS cannot
# reach it and it would be read aloud. Anchored on a leading `*vNNN` and a closing `*` so it
# cannot match narration.
REVISION_FOOTER = re.compile(r"^\*v\d{3}\b.*\*$")
INLINE_MARKER = re.compile(r"【[^】]*】|〔[^〕]*〕|\[[^\]]*\]")
ABBREV = re.compile(
    r"\b(?:[A-Z]|Inc|Ltd|Co|Corp|Mr|Mrs|Ms|Dr|Jr|Sr|St|No|Sen|Gov|Rep|Prof|Sgt|vs|v|al"
    r"|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sept|Sep|Oct|Nov|Dec)\.")
SENT_SPLIT = re.compile(r'(?<=[.!?])["”]?\s+(?=["“—(]?[A-Z0-9])')


# ---------------------------------------------------------------- extraction

def clean_quote(line: str) -> str:
    line = re.sub(r"^>\s?", "", line).strip()
    line = re.sub(r"\*\*|\*|`", "", line)
    return " ".join(line.split())


def section_for_heading(head: str) -> tuple[str | None, bool]:
    for sec, pat in SECTION_HEADINGS:
        if pat.match(head):
            return sec, False
    for pat in STOP_HEADINGS:
        if pat.match(head):
            return None, True
    return None, False


def extract_events(md: str, orphans: list[str] | None = None) -> list[tuple]:
    """-> ordered events: ("para", section, text) | ("silence", section, seconds).

    `orphans` (optional) collects prose lines that sit under a heading with NO section
    mapping AFTER narration has started (e.g. EP56's `## BRAND STING` card). Such lines
    would otherwise be dropped silently; build_chunks refuses to spend money on them.
    """
    out: list[tuple] = []
    section: str | None = None
    started = False
    # A production note that WRAPS ONTO THE NEXT LINE. Every rule below is line-local, and the
    # only thing that marks a note is the bracket pair, so a note opened with 【 on one line and
    # closed with 】 three lines later leaves its middle lines looking exactly like narration:
    # no 【, no CJK, no markdown. EP67 (ramirez) writes ten such notes over 16 continuation
    # lines, and the first of them ("push-in → car lot row → ... 1.9 s each ...") extracted as
    # SIX spoken chunks at the head of the HOOK -- camera directions read aloud, paid for, and
    # mastered. Measured across every script in episodes/_planning: EP53-EP66 contain ZERO
    # unbalanced 【 lines (all their notes open and close on one line), so tracking the bracket
    # across lines cannot change any registered episode; EP67 has 16 and EP69 has 31.
    # The OPENING line is deliberately NOT short-circuited here: it still falls through to the
    # rules below, so NOTE_SILENCE (a designed hold written in prose) and the CJK guard keep
    # behaving exactly as they did.
    in_note = False
    for raw in md.splitlines():
        line = raw.strip()
        # A citation comment is stripped BEFORE anything else looks at the line, so it can
        # neither be spoken nor be collected as an orphan (EP66 carries 175 of them).
        if HTML_COMMENT.match(line):
            continue
        if in_note:
            if "】" in line:
                in_note = False
            continue
        if line.count("【") > line.count("】"):
            in_note = True
        hm = re.match(r"^(#{1,6})\s+(.*)$", line)
        if hm:
            sec, is_stop = section_for_heading(hm.group(2).strip())
            if is_stop:
                break
            section = sec
            started = started or sec is not None
            continue
        if section is None or not line:
            if (orphans is not None and started and line
                    and not CJK.search(line)
                    and not line.startswith(("|", "#", ">", "- ", "* ", "---", "**["))
                    and len(re.sub(r"[^A-Za-z]", "", line)) >= 20):
                orphans.append(line)
            continue
        sm = SILENCE_LINE.search(line)
        if sm:
            out.append(("silence", section, float(sm.group(1))))
            continue
        nm = NOTE_SILENCE.match(line)
        if nm:
            # A designed hold written in prose inside a production note (EP66). It becomes
            # the silence AFTER the preceding chunk, overwriting the 0.6 s that the ⟨HELD⟩
            # marker on the line above has already set for the same chunk.
            out.append(("silence", section, float(nm.group(1))))
            continue
        if BEAT_LINE.match(line):
            out.append(("silence", section, BEAT_SECONDS))
            continue
        if line == "---":
            continue
        if line.startswith("**[") or line.startswith("*(") or REVISION_FOOTER.match(line):
            continue
        if CJK.search(line):        # 【OST: ...】 cards / JP production notes — never narration
            continue
        if line.startswith("|") or line.startswith("#"):
            continue
        if line.startswith(">"):
            text = clean_quote(line)
        elif line.startswith(("- ", "* ")):
            continue
        else:
            text = " ".join(re.sub(r"\*\*|\*|`", "", line).split())
        text = " ".join(INLINE_MARKER.sub(" ", text).split())
        if not text:
            continue
        out.append(("para", section, text))
    return out


def split_sentences(text: str) -> list[str]:
    guarded = ABBREV.sub(lambda m: m.group(0).replace(".", "\x00"), text)
    parts = [p.replace("\x00", ".").strip() for p in SENT_SPLIT.split(guarded)]
    return [" ".join(p.split()) for p in parts if p.strip()]


def sha_text(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def idempotency_key(ep: str, text: str, chunk_id: str) -> str:
    material = json.dumps({"episode_id": ep, "chunk_id": chunk_id, "model": MODEL,
                           "voice_id": VOICE_ID, "text_sha256": sha_text(text),
                           "script_revision": SCRIPT_REVISION}, sort_keys=True)
    return "sha256:" + hashlib.sha256(material.encode("utf-8")).hexdigest()


def build_chunks(ep: str, md: str) -> list[dict]:
    chunks: list[dict] = []
    orphans: list[str] = []
    n = 0
    for ev in extract_events(md, orphans):
        if ev[0] == "silence":
            if chunks:
                chunks[-1]["silence_after_seconds"] = ev[2]
            continue
        _, section, para = ev
        for sent in split_sentences(para):
            n += 1
            cid = f"VC-{n:04d}"
            chunks.append({
                "chunk_id": cid,
                "section": section,
                "delivery": DELIVERY_BY_SECTION[section],
                "spoken_text": sent,
                "text_sha256": sha_text(sent),
                "idempotency_key": idempotency_key(ep, sent, cid),
                "silence_after_seconds": None,
            })
    if orphans:
        raise SystemExit(
            "REFUSING TO GENERATE -- prose found under an unmapped heading (would be "
            "dropped silently):\n  " + "\n  ".join(o[:120] for o in orphans))
    return chunks


def apply_designed_silences(chunks: list[dict], cfg: dict) -> float:
    """Stamp the episode's registry-declared holds onto the chunks they follow.

    Returns the total scripted silence in seconds. Raises rather than guessing: an anchor
    that matches zero chunks (the script was edited) or more than one (the anchor is not
    distinctive) stops the run BEFORE any character is paid for, and the sum is checked
    against the episode's own declared budget so a mistyped number cannot pass silently.
    """
    declared = cfg.get("designed_silences") or []
    if not declared:
        return round(sum(c["silence_after_seconds"] for c in chunks
                         if c.get("silence_after_seconds") is not None), 3)
    for d in declared:
        hits = [c for c in chunks if d["after"] in c["spoken_text"]]
        if len(hits) != 1:
            raise SystemExit(
                f"REFUSING TO GENERATE -- designed_silences anchor {d['after']!r} matched "
                f"{len(hits)} chunk(s), expected exactly 1"
                + ("".join(f"\n    {c['chunk_id']} {c['section']} | {c['spoken_text'][:100]}"
                           for c in hits) if hits else ""))
        hits[0]["silence_after_seconds"] = float(d["seconds"])
    total = round(sum(float(d["seconds"]) for d in declared), 3)
    want = cfg.get("designed_silence_total_seconds")
    if want is not None and abs(total - float(want)) > 0.001:
        raise SystemExit(f"REFUSING TO GENERATE -- designed silence sums to {total}s, "
                         f"registry declares {want}s")
    return total


def assert_clean(chunks: list[dict], expected: list[str] | None = None) -> None:
    """Hard gate: refuse to spend money if any production marker leaked into TTS text."""
    bad: list[str] = []
    for c in chunks:
        t = c["spoken_text"]
        if CJK.search(t):
            bad.append(f"{c['chunk_id']}: CJK in spoken_text -> {t[:80]}")
        # ⟨⟩ added 2026-08-03: EP60 v004 marks held beats with ⟨HELD⟩, and this gate did
        # not know that bracket pair, so eight "HELD" chunks would have been read aloud.
        if re.search(r"[\[\]【】〔〕⟨⟩`#*_]", t):
            bad.append(f"{c['chunk_id']}: markup/marker in spoken_text -> {t[:80]}")
        if "OST" in t or "CARD:" in t or "SILENCE" in t or "SOUND:" in t or "VISUAL" in t:
            bad.append(f"{c['chunk_id']}: directive keyword -> {t[:80]}")
        if len(t) < 3:
            bad.append(f"{c['chunk_id']}: too short -> {t!r}")
    if bad:
        raise SystemExit("REFUSING TO GENERATE -- unclean chunks:\n  " + "\n  ".join(bad))
    order = expected or SECTION_ORDER
    got = [s for s in order if any(c["section"] == s for c in chunks)]
    unknown = sorted({c["section"] for c in chunks} - set(order))
    if got != order or unknown:
        raise SystemExit(f"REFUSING TO GENERATE -- section coverage {got}{unknown} != {order}")


# ---------------------------------------------------------------- helpers

def load_env() -> dict[str, str]:
    env: dict[str, str] = {}
    p = ROOT / ".env"
    if p.exists():
        for line in p.read_text("utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def media_root() -> Path:
    cfg = json.loads((ROOT / "config/storage.local.json").read_text("utf-8"))
    return Path(cfg["roots"]["media"]["path"])


def dur(path: Path) -> float:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    try:
        return round(float(r.stdout.strip()), 3)
    except Exception:
        return 0.0


def append_event(ep: str, event: dict) -> None:
    """gen_narration.py events.jsonl pattern (episodes/<EPID>/events.jsonl)."""
    p = ROOT / "episodes" / ep / "events.jsonl"
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")


PLAN_KEYS = ("chunk_id", "section", "delivery", "spoken_text", "text_sha256", "idempotency_key")


def resolve_settings(cfg: dict) -> dict[str, dict]:
    """Per-delivery voice settings, with the episode's own pins applied on top.

    An episode may declare `voice_settings` in the registry to pin values across every
    delivery (EP62 pins stability 0.35 / similarity_boost 0.80). Keys the episode does
    not name keep the shipped per-delivery preset. Episodes that declare nothing get
    exactly SETTINGS, unchanged.
    """
    override = cfg.get("voice_settings") or {}
    return {d: {**preset, **override} for d, preset in SETTINGS.items()}


def write_voice_plan(ep: str, chunks: list[dict], out_dir: Path, plan_path: Path,
                     settings_by_delivery: dict[str, dict] | None = None) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    settings_by_delivery = settings_by_delivery or SETTINGS
    plan_chunks = [{k: c[k] for k in PLAN_KEYS} for c in chunks]
    plan_path.write_text(json.dumps(
        {"episode_id": ep, "revision": SCRIPT_REVISION, "provider": "ElevenLabs",
         "voice_id": VOICE_ID, "model_id": MODEL,
         # The exact settings sent to the provider, per delivery. Recorded so that a
         # later episode can prove pace parity instead of assuming it.
         "voice_settings": settings_by_delivery,
         "chunks": plan_chunks},
        indent=2, ensure_ascii=False) + "\n", "utf-8")


def _silence_wav(outdir: Path, seconds: float, cache: dict[float, Path]) -> Path:
    key = round(seconds, 3)
    if key in cache:
        return cache[key]
    p = outdir / f"_silw_{key:.3f}.wav"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono",
                    "-t", f"{key}", "-c:a", "pcm_s16le", str(p)], check=True)
    cache[key] = p
    return p


def concat_master(chunks: list[dict], outdir: Path, master: Path,
                  gap_beat: float, gap_section: float) -> dict[str, dict]:
    """Concat chunk mp3s + inter-chunk silence into a loudnorm'd master.

    HOUR-LONG-SAFE (EP50 lesson): decode every chunk to uniform 44100/mono/s16le
    WAV first; all-WAV concat -> encode ONCE to the MP3 master."""
    wavdir = outdir / "_wav"
    wavdir.mkdir(parents=True, exist_ok=True)
    sil_cache: dict[float, Path] = {}
    cursor = 0.0
    lines: list[str] = []
    offsets: dict[str, dict] = {}
    for i, c in enumerate(chunks):
        src = outdir / f"{c['chunk_id']}.mp3"
        wav = wavdir / f"{c['chunk_id']}.wav"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(src), "-ar", "44100",
                        "-ac", "1", "-c:a", "pcm_s16le", str(wav)], check=True)
        d = dur(wav)
        offsets[c["chunk_id"]] = {"start": round(cursor, 3), "end": round(cursor + d, 3), "seconds": d}
        lines.append(f"file '{wav.as_posix()}'\n")
        cursor += d
        if i != len(chunks) - 1:
            override = c.get("silence_after_seconds")
            if override is not None:
                gap = float(override)
            else:
                boundary = c["section"] != chunks[i + 1]["section"]
                gap = gap_section if boundary else gap_beat
            lines.append(f"file '{_silence_wav(wavdir, gap, sil_cache).as_posix()}'\n")
            cursor += gap
    concat = outdir / "_concat.txt"
    concat.write_text("".join(lines), "utf-8")
    master.parent.mkdir(parents=True, exist_ok=True)
    raw = wavdir / "_master_raw.wav"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(concat),
                    "-c:a", "pcm_s16le", str(raw)], check=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(raw),
                    "-af", LOUDNORM, "-c:a", "libmp3lame", "-b:a", "192k", str(master)], check=True)
    return offsets


def write_index(ep: str, source_script_rel: str, chunks: list[dict], offsets: dict[str, dict],
                master: Path, index_path: Path, est_cost: float,
                gap_beat: float, gap_section: float,
                settings_by_delivery: dict[str, dict] | None = None) -> dict:
    total = round(dur(master), 3)
    speech = round(sum(o["seconds"] for o in offsets.values()), 3)
    words = sum(len(c["spoken_text"].split()) for c in chunks)
    scripted_silence = round(sum(c["silence_after_seconds"] for c in chunks
                                 if c.get("silence_after_seconds") is not None), 3)
    index = {
        "schema_version": "caniglia_narration.v1",
        "episode_id": ep,
        "revision": SCRIPT_REVISION,
        "is_stub": False,
        "provider": "elevenlabs",
        "voice_id": VOICE_ID,
        "model_id": MODEL,
        "source_script": source_script_rel,
        "master": f"artifact://episodes/{ep}/06_voice/master/vc_master_v001.mp3",
        "total_seconds": total,
        "totals": {
            "chunks": len(chunks),
            "words": words,
            "speech_seconds": speech,
            "measured_seconds": total,
            "measured_minutes": round(total / 60, 2),
            "measured_wpm": round(words / (speech / 60), 1) if speech else 0.0,
        },
        "chunks": [{
            "voice_chunk_id": c["chunk_id"],
            "id": c["chunk_id"],
            "section": c["section"],
            "text": c["spoken_text"],
            "spoken_text": c["spoken_text"],
            "word_count": len(c["spoken_text"].split()),
            "start": offsets[c["chunk_id"]]["start"],
            "end": offsets[c["chunk_id"]]["end"],
            "seconds": offsets[c["chunk_id"]]["seconds"],
            "duration": offsets[c["chunk_id"]]["seconds"],
        } for c in chunks],
        "provenance": {
            "producer": "scripts/gen_narration_case.py",
            "provider": "ElevenLabs",
            "voice_id": VOICE_ID,
            "model_id": MODEL,
            "voice_settings": settings_by_delivery or SETTINGS,
            "estimated_cost_usd": est_cost,
            "gap_beat_seconds": gap_beat,
            "gap_section_seconds": gap_section,
            "scripted_silence_seconds": scripted_silence,
            "loudnorm": LOUDNORM,
            "master_path_expected": str(master),
            "stamped_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "note": "start/end are per-chunk master offsets (inter-chunk silence excluded "
                    "from each window). Durations MEASURED with ffprobe from generated files.",
        },
    }
    index_path.write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n", "utf-8")
    return index


# ---------------------------------------------------------------- main

def main(argv: list[str]) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--ep", required=True, choices=sorted(EPISODES),
                    help="episode id (registry-gated: paid API)")
    ap.add_argument("--dry-run", action="store_true", help="no API call, no writes; print every chunk")
    ap.add_argument("--plan-only", action="store_true", help="write voice_plan only, no API call")
    ap.add_argument("--remaster", action="store_true", help="skip TTS; rebuild master + index from existing mp3s")
    ap.add_argument("--measure-section", metavar="SECTION",
                    help="generate ONLY this section (e.g. ACT_1), measure it with ffprobe, "
                         "print the words-per-finished-minute it implies, and stop before "
                         "the master and the index. Chunks land in the normal draft dir with "
                         "the normal sha-256 sidecars, so the later full run skips them.")
    ap.add_argument("--gap-beat", type=float, default=GAP_BEAT, help="inter-sentence gap seconds")
    ap.add_argument("--gap-section", type=float, default=GAP_SECTION, help="section-boundary gap seconds")
    args = ap.parse_args(argv)

    ep = args.ep
    cfg = EPISODES[ep]
    script_src = ROOT / "episodes" / "_planning" / cfg["planning"]
    source_script_rel = f"episodes/_planning/{cfg['planning']}"
    out_dir = ROOT / "episodes" / ep / "06_audio"
    voice_plan = out_dir / "voice_plan.v001.json"
    index_path = out_dir / "narration_index.v001.json"

    chunks = build_chunks(ep, script_src.read_text("utf-8"))
    scripted_silence = apply_designed_silences(chunks, cfg)
    assert_clean(chunks, cfg.get("sections"))
    chars = sum(len(c["spoken_text"]) for c in chunks)
    words = sum(len(c["spoken_text"].split()) for c in chunks)
    est = round(chars / 1000 * COST_PER_1K_CHARS_USD, 2)
    design = cfg["design_speech_seconds"]
    print(f"episode={ep} chunks={len(chunks)} words={words} chars={chars} est=${est:.2f} model={MODEL}")
    print(f"projected @178.1wpm = {words / 178.1 * 60:.0f}s speech  (DESIGN §5 model = {design}s)")
    print(f"gaps: beat={args.gap_beat}s section={args.gap_section}s "
          f"scripted_silence={scripted_silence}s")

    if args.dry_run:
        for c in chunks:
            tail = f"  <SILENCE {c['silence_after_seconds']}s>" if c.get("silence_after_seconds") else ""
            print(f"  {c['chunk_id']} {c['section']:6s} {c['delivery']:8s} | {c['spoken_text']}{tail}")
        by: dict[str, int] = {}
        for c in chunks:
            by[c["section"]] = by.get(c["section"], 0) + 1
        print(f"  section mix: {by}")
        return 0

    settings_by_delivery = resolve_settings(cfg)
    write_voice_plan(ep, chunks, out_dir, voice_plan, settings_by_delivery)
    print(f"voice_plan -> {voice_plan.relative_to(ROOT)}")
    if args.plan_only:
        return 0

    # The subset to SPEND on. `chunks` stays whole: assert_clean has already proved the
    # full script's section coverage above, and concat_master/write_index below still see
    # every chunk. Only the generation loop is narrowed.
    gen_chunks = chunks
    if args.measure_section:
        gen_chunks = [c for c in chunks if c["section"] == args.measure_section]
        if not gen_chunks:
            print(f"ERROR: no chunks in section {args.measure_section!r}; "
                  f"sections present = {sorted({c['section'] for c in chunks})}")
            return 1
        sub_chars = sum(len(c["spoken_text"]) for c in gen_chunks)
        print(f"MEASURE MODE: {args.measure_section} only -- {len(gen_chunks)} chunk(s), "
              f"{sum(len(c['spoken_text'].split()) for c in gen_chunks)} words, "
              f"{sub_chars} chars, est ${sub_chars / 1000 * COST_PER_1K_CHARS_USD:.2f}")

    outdir = media_root() / "episodes" / ep / "06_voice" / "draft"
    outdir.mkdir(parents=True, exist_ok=True)
    made = skipped = failed = 0
    made_ids: list[str] = []
    skipped_ids: list[str] = []
    failed_ids: list[str] = []
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    if not args.remaster:
        env = load_env()
        key = env.get("ELEVENLABS_API_KEY")
        if not key:
            print("ERROR: ELEVENLABS_API_KEY missing")
            return 1
        for c in gen_chunks:
            out = outdir / f"{c['chunk_id']}.mp3"
            side = out.with_suffix(".json")
            # sha-256 idempotency: existing file + matching text hash -> never re-spend.
            if out.exists() and out.stat().st_size > 2048:
                prev_sha = None
                if side.exists():
                    try:
                        prev_sha = json.loads(side.read_text("utf-8")).get("text_sha256")
                    except Exception:
                        prev_sha = None
                if prev_sha in (None, c["text_sha256"]):
                    skipped += 1
                    skipped_ids.append(c["chunk_id"])
                    continue
                print(f"  {c['chunk_id']} text changed (sha mismatch) -> regenerating")
            body = json.dumps({"text": c["spoken_text"], "model_id": MODEL,
                               "voice_settings": settings_by_delivery[c["delivery"]]}).encode("utf-8")
            req = urllib.request.Request(TTS.format(vid=VOICE_ID), data=body,
                                         headers={"xi-api-key": key, "Content-Type": "application/json",
                                                  "Accept": "audio/mpeg"}, method="POST")
            ok = False
            for attempt in range(3):
                try:
                    with urllib.request.urlopen(req, timeout=180) as r:
                        data = r.read()
                    out.write_bytes(data)
                    ok = True
                    break
                except urllib.error.HTTPError as e:
                    msg = e.read().decode(errors="replace")[:200]
                    print(f"  {c['chunk_id']} HTTP {e.code} (try {attempt + 1}): {msg}")
                    if e.code < 500 and e.code != 429:
                        break
                    time.sleep(3 * (attempt + 1))
                except Exception as e:  # noqa: BLE001
                    print(f"  {c['chunk_id']} ERR (try {attempt + 1}) {e}")
                    time.sleep(3 * (attempt + 1))
            if not ok:
                failed += 1
                failed_ids.append(c["chunk_id"])
                continue
            d = dur(out)
            side.write_text(json.dumps(
                {"episode_id": ep, "chunk_id": c["chunk_id"], "section": c["section"],
                 "delivery": c["delivery"], "text_sha256": c["text_sha256"],
                 "idempotency_key": c["idempotency_key"], "model_id": MODEL,
                 "voice_id": VOICE_ID, "characters": len(c["spoken_text"]), "seconds": d,
                 "estimated_cost_usd": round(len(c["spoken_text"]) / 1000 * COST_PER_1K_CHARS_USD, 4),
                 "provider": "ElevenLabs", "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z")},
                indent=2, ensure_ascii=False) + "\n", "utf-8")
            print(f"  {c['chunk_id']} {c['delivery']:8s} {len(c['spoken_text']):4d}ch -> "
                  f"{out.stat().st_size // 1024}KB {d:.2f}s", flush=True)
            made += 1
            made_ids.append(c["chunk_id"])
            time.sleep(0.35)

        gen_chars = sum(len(c["spoken_text"]) for c in chunks if c["chunk_id"] in set(made_ids))
        append_event(ep, {
            "event": "narration_generated",
            "episode_id": ep,
            "stage": "audio_generating",
            "revision": SCRIPT_REVISION,
            "provider": "ElevenLabs",
            "voice_id": VOICE_ID,
            "model_id": MODEL,
            "generated": len(made_ids),
            "skipped": len(skipped_ids),
            "failed": failed_ids,
            "characters_sent_this_run": gen_chars,
            "characters_total_plan": chars,
            "estimated_cost_usd_this_run": round(gen_chars / 1000 * COST_PER_1K_CHARS_USD, 2),
            "estimated_cost_usd_total_plan": est,
            "output_dir": str(outdir),
            "timestamp": now,
        })

    if failed:
        print(f"made={made} skipped={skipped} failed={failed} -> NOT building master (fix failures first)")
        return 1

    if args.measure_section:
        secs = [dur(outdir / f"{c['chunk_id']}.mp3") for c in gen_chunks]
        if not all(secs):
            print("ERROR: at least one chunk measured 0.000s -- refusing to report a rate")
            return 1
        speech = round(sum(secs), 3)
        sw = sum(len(c["spoken_text"].split()) for c in gen_chunks)
        n_gaps = len(gen_chunks) - 1
        gaps = args.gap_beat * n_gaps
        finished = speech + gaps
        print(f"MEASURED section={args.measure_section} chunks={len(gen_chunks)} words={sw}")
        print(f"  speech          {speech:.3f}s  ({speech / 60:.2f} min)  "
              f"raw {sw / (speech / 60):.1f} wpm")
        print(f"  + {n_gaps} beat gap(s) @ {args.gap_beat}s = {gaps:.1f}s")
        print(f"  finished        {finished:.3f}s  ({finished / 60:.2f} min)  "
              f"{sw / (finished / 60):.1f} words per finished minute")
        print("no master and no index written: --measure-section stops before both.")
        return 0

    master = media_root() / "episodes" / ep / "06_voice" / "master" / "vc_master_v001.mp3"
    offsets = concat_master(chunks, outdir, master, args.gap_beat, args.gap_section)
    index = write_index(ep, source_script_rel, chunks, offsets, master, index_path,
                        est, args.gap_beat, args.gap_section, settings_by_delivery)
    speech = index["totals"]["speech_seconds"]
    total = index["total_seconds"]
    append_event(ep, {
        "event": "narration_mastered",
        "episode_id": ep,
        "stage": "audio_generating",
        "revision": SCRIPT_REVISION,
        "provider": "ElevenLabs",
        "voice_id": VOICE_ID,
        "model_id": MODEL,
        "chunks": len(chunks),
        "characters_total_plan": chars,
        "estimated_cost_usd_total_plan": est,
        "speech_seconds": speech,
        "master_seconds": total,
        "audio_minutes": round(total / 60, 2),
        "design_speech_seconds": design,
        "speech_vs_design_delta_s": round(speech - design, 1),
        "gap_beat": args.gap_beat,
        "gap_section": args.gap_section,
        "master": str(master),
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    })
    print(f"made={made} skipped={skipped} failed={failed}")
    print(f"speech total = {speech:.1f}s ({speech / 60:.2f}min)  DESIGN model {design}s  "
          f"delta {speech - design:+.1f}s")
    print(f"MASTER measured narrationSeconds = {total:.3f}s ({total / 60:.2f}min)")
    print(f"measured wpm = {index['totals']['measured_wpm']}")
    print(f"master -> {master}")
    print(f"index  -> {index_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
