# Retired one-off scripts

66 scripts named after a single episode, moved here 2026-08-23. Every one was referenced by
nothing: not by another script, not by a doc, not by a config. Two independent scans agreed --
one over 16,712 files in the whole repository, one restricted to the source tree -- and both
returned the same 79 unreferenced one-offs. 13 of those 79 belong to episodes still in flight
(EP70-76) and were deliberately left in `scripts/`.

**Why they are here and not deleted.** They are the record of how those episodes were made, and
`git mv` keeps their history. Nothing about them was edited.

**Why they were moved at all.** Measured the same day: 813 scripts, 268 named after one episode,
one question ("is this episode already built?") implemented in four separate places and wrong in
all four. A defect in a decision copied N times has to be found N times, and the person fixing
it cannot know what N is. Fewer copies is the only structural fix.

**If you need one back:** `git mv scripts/_attic/oneoffs/<name> scripts/<name>`. But first ask
whether the generic path already does it -- `build_case_film_generic.py`, `write_sound_plan.py`,
`upload_schedule_case_v001.py` and `episode_is_done.py` all exist because a one-off was
generalised instead of copied again.
