# EP71 OROVILLE — CODEX PASTE: GAPS AND FINDINGS

Written while splitting `EP71_oroville_CODEX_BATCH_A.v001.md` into
`EP71_oroville_CODEX_PASTE/batch_01.txt … batch_12.txt`. Formatting pass only; no prompt
was authored, reworded or dropped.

## 1. Plates omitted from the paste set: **none**

All 118 plates carried an id, a beat and a full prompt, so none had to be held back.

| check | result |
|---|---|
| plates parsed from the order document | 118 |
| `mandatory_stills` declared in `episode_spec.v001.json` | 118 |
| declared but absent from the document | none |
| present in the document but not declared | none |
| duplicate ids | none |
| holes in the run O001–O118 | none |
| plates missing a prompt or a beat | none |

**118 = 118, contiguous, no duplicates.** The count reconciles in both directions.

## 2. The one structural difference from EP70, stated plainly

EP70's order document carries a **`script anchor`** column, and its own header says every
anchor "is checked by the builder to be a real substring of a spoken line". So EP70's paste
files can honestly say `for the line: "Five o'clock in the morning"` — that is narration.

**EP71's order document has no such column.** Its per-plate column is `beat`, described in the
document as "the script span it serves", and its contents are short labels — `she walks in`,
`the trolley`, `the concrete` — not narration. Verbatim narration is attached at SECTION
level only (`### HOOK — O001–O006 · script span: "On the afternoon of Sunday…" → …`), and
`EP71_oroville_script.en.v001.md` likewise anchors plates in ranges per section, never one by
one.

**Therefore the paste files say `for the beat:` and not `for the line:`, and the value is the
document's own beat label, unchanged.** Writing a narration line into that slot would have
meant choosing a sentence for each of 118 plates, which is authoring, not formatting. If a
per-plate verbatim anchor is wanted, it has to be added to the order document by whoever owns
the script — not inferred here.

## 3. Forbidden-subject sweep — **4 hits, all the same word, and it is a collision**

Method: `_words()` + `_hits()` imported from `scripts/check_spec_satisfied.py`, i.e. the exact
whole-word matcher the build gate uses, run over all 131 `forbidden_subjects` against every
plate's prompt and beat.

| plate | forbidden term matched |
|---|---|
| O007 | `manila` |
| O094 | `manila` |
| O112 | `manila` |
| O113 | `manila` |

The term is **`manila`**, and in `forbidden_subjects` it sits at index 123 between
`jakarta` and `european street`, among `istanbul, cairo, sydney, toronto, mexico city,
jakarta` — it is barred as **the capital of the Philippines**, part of the foreign-place net
this episode declared after EP62/EP63 shipped foreign streets through green gates.

What the four plates actually order is **manila card** — the film's document ground. O007 is
literally "the paperwork ground". The subject is not a city.

**It is also in the global `[STYLE]` block** ("… orchard bark, dry grass, manila card …"), which
is prepended to all 118 prompts, so the word ships on every plate in the set.

Consequence, and it is real: `check_spec_satisfied.py` matches `forbidden_subjects` against
the **basename of each cut's asset**. Delivering these plates as `O007.png` is safe. Delivering
any of them as, say, `O007_manila_card.png` fails the gate on a filename. Hence the naming rule
in README.txt. **No prompt was edited to remove the word** — the [STYLE] block is canonical and
byte-identical across every tier of the order, and quietly rewording it here would be exactly
the drift that generator refuses to allow. Whoever owns the spec should decide between
narrowing the term to `manila philippines` and leaving it; that is a spec edit, not a paste edit.

Nothing else hit. No plate in this episode names a flood, a breach, a collapse, a rescue, a
casualty, a child, a courtroom fitting or a foreign place. The `[NEG]` block itself matches
54 forbidden terms, which is correct and expected — it is a list of things to suppress.

## 4. People plates — 20 declared, 20 flagged, **one of them has no person in it**

`episode_spec.people_plates` and the `**P**` flags in the order document agree exactly
(mismatch: none). Each row below shows the wording in the plate's own prompt that keeps
the figure from becoming an identifiable individual.

| plate | flagged **P** in doc | non-identifiability wording in the prompt |
|---|---|---|
| O004 | yes | back three-quarters to camera, hand, out of focus, out of frame, unidentifiable |
| O009 | yes | at distance, from behind, unidentifiable |
| O016 | yes | from behind, hand, silhouette, unidentifiable |
| O023 | yes | all that is in frame, hands |
| O028 | yes | from behind, unidentifiable |
| O035 | yes | at distance, back to camera, small in frame |
| O041 | yes | unidentifiable |
| O047 | yes | at distance, unidentifiable |
| O053 | yes | edge of frame, nothing above |
| O058 | yes | edge of frame, hand |
| O064 | yes | close on a hand, hand |
| O070 | yes | unidentifiable |
| O076 | yes | from behind, unidentifiable |
| O081 | yes | hands, nothing above |
| O087 | yes | back to camera, unidentifiable |
| O092 | yes | hand, out of frame |
| O097 | yes | from behind, unidentifiable |
| O102 | yes | at distance, back to camera, unidentifiable |
| O107 | yes | **none** |
| O111 | yes | at distance, from behind, unidentifiable |

**O107 is the finding.** It is declared a people plate in the spec and flagged `**P**` in the
order, but its prompt is *"an empty chair with a coat left over the back of it in a plain room,
nobody there"* — there is no figure to make unidentifiable. As written it cannot satisfy
`people_plates_min: 20`; as ordered it is correct for the beat ("the coat on the chair"). The
prompt was **not** altered to add a person. Someone has to choose: amend the prompt in the
order document, or move the people flag to another plate. Flagging it here is the whole point
of the rule — the alternative was a silently invented figure in a room ordered empty.

The other nineteen are all explicitly from behind, at distance, out of focus, in silhouette, or
cropped to hands and lower legs, and the `[NEG]` under every prompt carries `recognisable
person, identifiable person, likeness of a real individual, portrait of a named person,
celebrity, public figure, deepfake`.

**Note what the `[NEG]` deliberately does not contain: `human face`, `facial features`, `eyes`.**
That is the order document's own decision (§1) — those three tokens would suppress the people
lane entirely, and what is suppressed instead is identifiability. It means a face can appear.
This episode names real plaintiffs — Denise Johnson, Francis Bechtel, Nicoli Nicholas — and
**none of them may ever be depicted**. If a delivered plate reads as a specific individual it is
rejected and regenerated; that is the only acceptance test on this lane, and it needs a human
looking at a contact sheet, because no gate in this repository measures it.
