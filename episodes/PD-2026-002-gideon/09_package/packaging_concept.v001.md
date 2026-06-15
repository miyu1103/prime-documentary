# Packaging concept — PD-2026-002-gideon (v001)

Packaging-first (decisions/0005, 0006 §B): title + thumbnail designed **before** heavy production.
Goal = maximize CTR × AVD without clickbait lies. **Owner gate: title + thumbnail approval (APR).**
A/B plan: ship 2–3 thumbnails + 2 titles via YouTube Studio "Test & Compare"; keep the winner.

Reuses the existing brand thumbnail component (same props as EP1: `kicker / line1 / line2 / sub /
symbol / backgroundSrc`) — no rebuild. Only the background image + words change per concept.

---

## Thesis (what the package must promise and the video must pay off)
A penniless prisoner with no lawyer handwrote a letter to the Supreme Court — and won, 9–0, creating
the right to an appointed lawyer for every poor defendant in America. The hidden room: the right was
guaranteed, but the system that keeps it (public defenders) is chronically under-resourced.

---

## Titles (curiosity gap · front-load keywords · ~40–60 chars · no clickbait)

**Primary A (browse / curiosity):**
`He Had No Lawyer — So He Beat the Supreme Court` (46)

**Primary B (search / how-it-works):**
`Why You Get a Lawyer If You Can't Afford One` (44)

Alternates (for A/B and repackaging losers):
- `A Prisoner, a Pencil, and the Supreme Court` (43)
- `The Letter That Gave America Public Defenders` (45)
- `The Case That Put a Lawyer in Every Courtroom` (46)

Rule check: each complements (does not repeat) its paired thumbnail words; no fake claim — he really
did win 9–0 and was acquitted on retrial. Keyword front-loading: "lawyer", "Supreme Court".

---

## Thumbnail concepts (one focal point · fewest, biggest words · readable at tiny size · high contrast)

> Backgrounds are owner-generated in **Midjourney** (commercial plan), brand `--sref`. Symbolic only,
> never presented as authentic historical footage (invariant 11). Prompts are drafts to refine on the gate.

### Concept 1 — "The Empty Chair"  (recommended lead)
- **Focal point:** a single empty wooden chair at a defense table in a dark, dramatic courtroom, one
  hard light on it; a lone silhouetted figure standing apart with no one beside him.
- **Brand props:** `kicker: "GIDEON v. WAINWRIGHT"`, `line1: "No lawyer."`, `line2: "He won anyway."`,
  `sub: "How one prisoner changed every U.S. trial"`, `symbol: "scales"`.
- **Pairs with title:** Primary B or "A Prisoner, a Pencil…" (so words don't repeat the thumbnail).
- **MJ background brief:** `empty wooden defendant's chair alone at a table in a vast shadowy 1960s
  American courtroom, single dramatic shaft of cold light, deep blacks, cinematic, volumetric haze,
  no text, no people in focus --ar 16:9`

### Concept 2 — "The Pencil vs. the Court"
- **Focal point:** an extreme close-up of a worn pencil and a hand-printed letter on prison paper,
  the marble Supreme Court facade looming, out of focus, behind it. Scale contrast = the hook.
- **Brand props:** `kicker: "1963"`, `line1: "A pencil."`, `line2: "vs. the Supreme Court."`,
  `sub: "The letter that rewrote the rules"`, `symbol: "none"`.
- **Pairs with title:** Primary A ("He Had No Lawyer — So He Beat the Supreme Court").
- **MJ background brief:** `extreme close-up of an old yellow pencil resting on a handwritten letter
  on lined paper, the white marble U.S. Supreme Court building blurred in the background, dramatic
  cold light, shallow depth of field, cinematic, no readable text --ar 16:9`

### Concept 3 — "ALONE"
- **Focal point:** a single small figure dwarfed by an enormous courtroom / columns; overwhelming
  scale = one person against the state.
- **Brand props:** `kicker: "GIDEON v. WAINWRIGHT"`, `line1: "ALONE"`, `line2: "against the state"`,
  `sub: "Then he mailed the Court a letter"`, `symbol: "scales"`.
- **Pairs with title:** "The Case That Put a Lawyer in Every Courtroom".
- **MJ background brief:** `one tiny lone man standing in an immense empty neoclassical courthouse
  with towering columns, dramatic god-rays, sense of overwhelming scale and isolation, cinematic,
  cold palette, no text --ar 16:9`

**A/B launch set:** Concept 1 + Concept 2 (+ Concept 3 as third slot) with Primary A and Primary B.

---

## Description (draft — first 2 lines = hook + keywords; chapters finalized after timing)

```
He couldn't afford a lawyer, so a Florida court made him defend himself — and convicted him. Then,
from a prison cell, Clarence Earl Gideon mailed the U.S. Supreme Court a handwritten letter.

This is Gideon v. Wainwright (1963): how one pauper's petition forced a unanimous Supreme Court to
guarantee an appointed lawyer for every poor defendant in America — the promise behind "if you
cannot afford a lawyer, one will be appointed for you" — and the underfunded system it left behind.

⏱ Chapters
0:00 The prisoner who beat the Court
0:38 The right that's younger than you think
1:35 The empty chair: on trial with no lawyer
3:35 The letter — and the wall called Betts v. Brady
6:05 Nine to nothing
8:05 The right vs. the reality (public defenders)
10:35 Who actually gets a lawyer

📚 Sources
Gideon v. Wainwright, 372 U.S. 335 (1963).
Betts v. Brady, 316 U.S. 455 (1942).
Full opinion: https://www.courtlistener.com/opinion/106456/gideon-v-wainwright/

ℹ️ About this video
Independent educational documentary. Narration is AI-generated. Historical moments that were never
filmed are shown as clearly labeled symbolic reconstructions — not authentic footage. This explains
how the law works and is not legal advice.

▶ Previous: why police read you your rights — Miranda v. Arizona.
▶ Next: who decides what counts as a crime?
👉 Subscribe for the hidden systems behind everyday life.

#Gideon #RightToCounsel #SupremeCourt
```

> Chapter timestamps above are placeholders; recompute from the final TTS timeline before publish
> (EP1 lesson: don't hand-time chapters). Keep first chapter at 0:00.

---

## Tags (draft)
`gideon v wainwright, right to counsel, public defender, supreme court, sixth amendment, clarence
earl gideon, betts v brady, appointed lawyer, landmark supreme court cases, us law explained,
constitutional rights, criminal justice, legal history, know your rights, gideons trumpet`

## Package gate checklist (must be true before APR title/thumbnail)
- [ ] Owner picks ≥2 thumbnail concepts + 2 titles for the A/B set.
- [ ] Midjourney backgrounds generated (owner) for the chosen concepts.
- [ ] Thumbnails rendered via the brand component; readable at 120px wide.
- [ ] Title ⇄ thumbnail ⇄ content match verified (no clickbait lie).
