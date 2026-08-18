# EP71 Oroville — identity and renumber record

**Written 2026-08-12. This file exists so that nobody later has to guess why the premise for
episode 71 is in files whose names begin `EP70_`.**

## What the owner decided

On the evening of 2026-08-12 the owner assigned:

| number | subject | runtime |
|---|---|---|
| **EP70** | *Martin v. United States* — the FBI raid on the wrong house | 45 min |
| **EP71** | **the Oroville Dam evacuation of 12 February 2017** | **30 min** |

The Oroville research, the re-centred premise and the rights pre-screen were all authored
**before** that assignment, under the working number 70. Their filenames say `EP70_oroville_*`
and one directory said `PD-2026-070-oroville`.

## What was moved, and what deliberately was not

**MOVED.** `episodes/PD-2026-070-oroville/` → `episodes/PD-2026-071-oroville/`. The directory
held exactly one file, `09_package/rights_prescreen.v001.json`. It moved with the directory.
One field inside it, `episode_id`, was corrected from `PD-2026-070-oroville` to
`PD-2026-071-oroville`, because leaving it would have made the file assert something false.
The correction is recorded inside that file, in the manifest and in `events.jsonl`. **No
finding, item, rejection, answer or verification record in the pre-screen was touched.**
`episodes/PD-2026-070-oroville/` no longer exists. There is no half-renamed directory.

**NOT MOVED, ON PURPOSE.** These four files keep their `EP70_` names:

```
episodes/_planning/EP70_oroville_premise.v001.json
episodes/_planning/EP70_oroville_premise.v001.scored.json
episodes/_planning/EP70_oroville_premise.v002.json
episodes/_planning/EP70_oroville_premise.v002.scored.json
episodes/_planning/EP70_oroville_protagonist_search.v001.md
```

Three reasons, in order of weight:

1. **They are scored, immutable artefacts.** `.scored.json` carries the verdict a scoring run
   produced at a stated timestamp against a stated rubric. `.claude/rules/12` makes approved
   artefacts immutable and `CLAUDE.md` invariant 6 forbids overwriting them; renaming a scored
   file is a quieter version of the same thing.
2. **Live references point at those exact paths.** `rights_prescreen.v001.json`
   `provenance.inputs` names two of them. Renaming would break a citation in a file whose whole
   value is that its citations are real.
3. **There is no filename collision to fix.** The planning convention is `EP<NN>_<slug>_*`, so
   Martin's files will be `EP70_wronghouse_*` or `EP70_martin_*` and will not touch these.

The identity that actually binds is the one **inside** the files: `"slug": "oroville"`. Every
artefact authored from 2026-08-12 onward uses `EP71_oroville_*` and `PD-2026-071-oroville`.

## Open collision — for the owner, not for this thread to resolve

`episodes/PD-2026-071-wronghouse/` exists. It was created 2026-08-11T17:35Z, state `idea`,
`target_duration_minutes: 24`, and it is the Martin / wrong-house episode — created **before**
tonight's assignment, and therefore carrying the number the owner has since given to Oroville.
It is untracked in git and another agent is working on it.

**Nothing in it was read beyond its manifest, and nothing in it was touched.** Two directories
currently carry the ordinal 071. That is recorded as a blocker on this episode's manifest so it
cannot be forgotten, and it is the other thread's or the owner's call to make, not this one's.

**And the collision is already resolvable, because the other thread wrote down why it happened.**
Its own manifest warnings say, in terms: *"Owner named this episode EP70; `PD-2026-070-oroville`
already exists, so this is created at `PD-2026-071-…`"*. So Martin's agent took 071 **only because
Oroville was sitting on 070** — it was never a disagreement about the owner's decision, it was two
threads working from the same directory at the same minute. **`PD-2026-070-*` is now free.** The
whole fix is for that thread, or the owner, to move `PD-2026-071-wronghouse` to
`PD-2026-070-wronghouse` and correct the ids inside it the same way this episode corrected its
pre-screen. Note that its planning artefacts have already begun landing under an `EP71_wronghouse_*`
prefix, so those names need the same pass.

This thread will not do it: another agent is live in that directory and the instruction was
explicit — do not touch anything Martin's agent is creating.

## Runtime and band, restated so no tool has to infer them

30 minutes, decided by the owner, recorded in `EP70_oroville_premise.v002.json` →
`runtime.decided_by`. `runtime.tier` is `PRIME_ORIGINAL`. The machine contract is
`episodes/PD-2026-071-oroville/episode_spec.v001.json`; an undeclared value is an error and
nothing is inferred (`CLAUDE.md` §4.6).

## The build decision, recorded as what it is

The premise scores **85** against `config/pd_planning_os.v002.json`, whose PRODUCTION line is
**90**. Verdict on file: `RESERVE`. **The owner chose to build it anyway, on 2026-08-12, with
the number in front of them.** That is an owner decision, not a weakened gate, and the gate is
not to be adjusted to agree with it. The one honest route to 90 was the `real_footage` +5 bonus;
it was refused because no clearance position existed on any specific clip. A rights pre-screen
now exists (`episodes/PD-2026-071-oroville/09_package/rights_prescreen.v001.json`) and its own
conclusion is still **DO NOT AWARD** — four clearable clips totalling 15 minutes, of which all
but 72 seconds are the dam, and the dam is not what this film is about. So the score stands at
85 and the build proceeds on the owner's word alone. Both facts belong in the record together.
