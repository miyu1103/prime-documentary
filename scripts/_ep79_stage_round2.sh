#!/usr/bin/env bash
# EP79 alaska261 -- second footage round. Object nouns only, two words, MEASURED FIRST.
#
# WHY THIS EXISTS. Round 1 delivered 51 clips; 31 survived review. A reviewer who read all 31 at
# full frame found: 18 open ocean and sunsets, 4 welding, 3 American flags, 2 defocused baggage
# claim, 1 plastics moulding machine. Not one jackscrew, acme nut, dial indicator, maintenance
# hangar, work card, MD-80 on jacks or hearing room -- the six things the episode is about.
# Those queries were written from mood words (ocean, dusk, industry, america). Mood words select
# mood footage, and this film contains none of that.
#
# So round 2 is written from the SHOTLIST, and the nouns come out of the script itself:
#   "a single steel screw standing vertically inside the fin" / "a nut travels along it"
#   "two threads run in a spiral" / "the grease, which slows the wear down"
#   "you measure that movement with a dial indicator ... the gauge with the one needle"
#   "you are up a stand, inside the tail of an aeroplane" / "you clamp a fixture on"
#   "a hangar where one job produces dust and another job requires a clean surface"
#   "a card with a maximum interval of eight months" / "and whatever it says, it goes in the file"
#   "a Boeing engineer put it plainly at the public hearing"
#
# TRAP 7, recorded on EP80 and paid for twice: ask for the NAME OF A THING, in two words.
# Concept words fail badly -- "wind / cliff / escalator / bubbles" returned the Grand Canyon, a
# wind farm, a subway and a goat. Two-word object nouns are the only band that has ever hit here.
#
# TRAP 8, found while writing THIS file: the right noun is not enough, because the shelf has to
# contain the word. A first draft of this script shipped 158 correct-sounding object nouns
# ("dial indicator", "acme nut", "torque wrench", "maintenance hangar", "hearing room") and 145
# of them returned ZERO clips -- 21 candidates in total, worse than round 1. The shelf's 21,300
# titles available to this episode contain: screw 0, bolt 0, wrench 0, grease 0, caliper 0,
# micrometer 0, hangar 0, mechanic 0, hearing 0, courtroom 0, lectern 0, rivet 0, vise 0.
# What it does contain: clock 110, typewriter 79, paper 149, card 82, library 131, office 129,
# lamp 55, machine 107, factory 100, tower 95, laboratory 101, needle 10, pointer 7.
# So every query below was counted against the actual available title set before it was written,
# and none of them is here on a hunch. The film's objects are reached through the nearest thing
# the shelf really holds: a clock face for the dial indicator's needle, a machine shop for where
# a screw and an in-house fixture get made, a typewriter and a file for the work card.
#
# WHAT IS DELIBERATELY NOT ASKED FOR:
#   - no "ocean", "sunset", "sunrise", "sea horizon", "golden hour". The pool already holds 18.
#     Coast survives here as four queries, for rock and a boat, and nothing else.
#     "sea cliff" alone would have matched 41 titles; it is left out on purpose.
#   - no "welding", "sparks", "flag". The pool already holds 4 and 3.
#   - no "airport terminal", "baggage claim", "departure board": modern glass, an era violation
#     against a January 2000 setting, and the pool already holds 2 of them.
#   - no "circuit board" (58 matches) and no "test tube" / "science laboratory" (48 + 24). Each
#     would have flooded the list with high-count off-topic filler, which is how round 1 became
#     18 clips of the same sea.
#   - no airline names, no liveries, no tail markings. The plate review just rejected two plates
#     for carrying the Alaska Airlines Eskimo emblem; a real livery in stock footage is exactly
#     the same rights problem, so nothing here asks for an aeroplane's exterior paint.
#   - nothing from episode_spec forbidden_subjects: no wreckage, impact, debris field, salvage,
#     bodies, crash site, child, mugshot, readable document -- and none of the banned countries.
#     stage_footage_by_title.py refuses a query that asks for one and screens titles too; 2,404
#     shelf titles were dropped by that screen on this run.
#
# --per-query 12, not 40: at 40 the three biggest queries ("library books" 53, "factory worker"
# 41, "vintage typewriter" 36) take a third of the list on their own. 12 costs 109 title matches
# out of 545 and buys the spread across all eleven subjects instead.
set -euo pipefail
Q=(); add() { Q+=(--query "$1"); }

# 1. THE MECHANISM: one screw, one nut, two threads, thirty-two turns of steel. The shelf has no
#    screw and no thread, so the mechanism is reached through the only geared machinery it holds
#    -- clock and watch movements, which are also the right scale and the right era.
for q in "clock mechanism" "watch mechanism" "clock gears" "gear mechanism" "metal gears" \
         "gear wheel" "watch gears" "metal chain" "machine parts"; do add "$q"; done

# 2. THE MACHINE SHOP. Where a jackscrew is cut, and where the in-house restraining fixture that
#    "was not even close to Boeing's engineering drawing requirements" was made.
for q in "industrial machine" "factory machine" "factory floor" "metal workshop" \
         "foundry workshop" "metal casting" "metal grinder" "metal turning" "turning machine" \
         "conveyor belt" "printing press" "factory worker" "worker machine"; do add "$q"; done

# 3. THE GAUGE WITH ONE NEEDLE -- the controlling image of the whole episode: a needle at rest,
#    being read, reading nothing anyone wrote down, at rest again. "It is about the size of a
#    pocket watch, it costs less than a good pair of boots, and it has one needle."
for q in "analog clock" "clock face" "clock hands" "minute hand" "pocket watch" "watch face" \
         "watch hands" "old clock" "antique clock" "alarm clock" "clock ticking" "wall clock" \
         "balance scale" "weighing scale" "scale weight" "laboratory scale"; do add "$q"; done

# 4. THE AEROPLANE, from outside the paint. Thin on this shelf and asked for thinly.
for q in "aircraft maintenance" "airport tarmac" "airport runway" "propeller plane" \
         "airplane wing" "airport night"; do add "$q"; done

# 5. THE BENCH. Boeing's bench measurements of 214 overhauled assemblies; the laboratory that
#    identified pink garnet grains in Hawaiian's grease.
for q in "laboratory tools" "laboratory microscope" "microscope lens" "lab technician" \
         "gloved hands" "typing hands"; do add "$q"; done

# 6. THE INSPECTION LIGHT. Incandescent and fluorescent shop lighting, which is what 2000 looks
#    like; an LED panel is an era violation and gets rejected at the strip.
for q in "light bulb" "lamp light" "old lamp" "ceiling light" "fluorescent light" \
         "desk lamp"; do add "$q"; done

# 7. THE PAPERWORK -- the largest group, because the film is carried by it. The eight-month card,
#    the file, the in-limits reading that "went nowhere", AD 2000-15-15 putting it back in.
#    Asked for as objects and furniture, never as text: a readable document is forbidden.
for q in "vintage typewriter" "typewriter typing" "typewriter paper" "typewriter desk" \
         "old typewriter" "signing document" "reading document" "document hands" \
         "flipping pages" "file folder" "folder pages" "office file" "old files" \
         "paper stack" "writing paper" "hand writing" "signing paper" "paper documents" \
         "desk paper" "office desk" "old office" "office room" "book pages" "old book" \
         "book shelf" "library shelf" "library shelves" "library books" "card catalog" \
         "ink pen" "fountain pen" "pen paper" "writing notebook" "notebook pages" \
         "cardboard boxes" "printer paper" "paper roll" "blank paper" "book stack"; do add "$q"; done

# 8. THE HEARING. "A Boeing engineer put it plainly at the public hearing." Rooms, benches and a
#    microphone -- no faces to hold, no seal to read.
for q in "conference room" "meeting room" "empty room" "wooden bench" "wooden chairs" \
         "empty chairs" "government building" "capitol building" "court building" "city hall" \
         "lecture hall" "studio microphone" "vintage microphone" "microphone close"; do add "$q"; done

# 9. THE CONTROL POSITION. The controller who offered them a lower altitude; analogue and CRT.
for q in "radio tower" "radio antenna" "antenna tower" "control panel" "radio station" \
         "clock tower"; do add "$q"; done

# 10. THE BUILDING AROUND THE WORK -- corridor and steel stair, the hangar's own architecture.
for q in "empty corridor" "metal stairs"; do add "$q"; done

# 11. WATER AND COAST, kept to four queries on purpose. Rock and a boat; no open horizon.
for q in "rocky coast" "coastal rocks" "patrol boat" "harbor water"; do add "$q"; done

echo "queries: $(( ${#Q[@]} / 2 ))"
py -3.11 -X utf8 scripts/stage_footage_by_title.py --slug alaska261 "${Q[@]}" \
  --per-query 12 --emit-candidates runs/qc/alaska261_candidates_r2.json
