# EP39 (frazier) — Text-Clipping Audit vs EP40 bugs

**Date:** 2026-07-20
**Auditor:** Claude (inspection only — no EP39 files modified, no EP40/EP41 touched)
**Scope:** Check whether EP39 "frazier" carries the two text-clipping bugs found in EP40.

## VERDICT — NO CLIPPING IN FRAZIER

- **Bug 1 (Remotion emphasis scale-punch clip): NOT APPLICABLE.** frazier's 4 kinetic
  figures use `style:"maskslide"`, which never runs the emphasis code path. The
  `emphasisWords:["ROOM"]` are inert. No re-render required for this bug.
- **Bug 2 (AE card text-width mis-estimate): ABSENT.** Neither frazier AE builder uses
  `fit_size` / character-width estimation. All 20 rendered AE cards (8 hero + 12 card
  family) were frame-checked: zero clipping, zero overflow, zero font substitution.
  No re-build required.

**Affected AE cards: 0 of 20. Affected kinetic figures: 0 of 4. Re-render / re-build: NOT needed.**

---

## Bug 1 — Remotion emphasis-word clipping (KineticCaptions.tsx)

### What frazier uses
`remotion/src/data/frazier_film.json` has **4 `kind:"kinetic"` figures**, all identical
(one per act), at design times **56.306, 257.532, 458.757, 659.983 s**:

```json
{ "kind": "kinetic",
  "lines": ["THE ROOM", "CHANGES THE STORY"],
  "style": "maskslide",
  "emphasisWords": ["ROOM"] }
```

### Why the bug cannot manifest
In `remotion/src/components/motionkit/KineticCaptions.tsx`, the scale-punch that clipped
NOBODY/CITY/ADDRESS in EP40 lives in the `Word` component and is gated on
`style === 'emphasis'` (line 280: `const emphasis = style === 'emphasis' && …`).
frazier uses **`maskslide`**, which renders through the `Line` component (whole-line
vertical mask reveal, no per-word scale-punch). The `emphasisWords` array is therefore
**never consulted** — it is dead data in maskslide mode. The EP40 failure mode
structurally does not exist here.

Two further safety margins:
1. `KineticCaptions.tsx` **already contains the fix** (header comment `FIX 2026-07-20`,
   punch moved to the outer `overflow:visible` element), so even an `emphasis`-style
   figure would now be safe on re-render.
2. The only emphasis token is `"ROOM"` (4 chars) — short even in the worst case.

### Visual confirmation (rendered casefilm)
`08_edit/frazier_casefilm.v001.mp4` (dur 736.85 s; ~20 s intro prepended, so the figure
lands ≈ t76 s, not t56). At **t≈76 s** the figure renders **"THE ROOM / CHANGES THE
STORY"** with both lines fully inside frame, no left/right clipping. Crucially the word
**"ROOM" is rendered WHITE, not gold** — direct visual proof that the emphasis
scale-punch path is not active. No clipping present.

---

## Bug 2 — AE card text-width estimation (build_frazier_*_jsx.py)

### Estimation logic — NOT the EP40 mechanism
- `scripts/ae/build_frazier_hero_jsx.py`: text placed with `addText(...)` at **fixed
  font sizes** and AE-native `CENTER_JUSTIFY`. The underline is a fixed 460 px solid
  scaled by keyframe. **No `fit_size`, no character-width estimate, no width-based
  scaling/positioning.** The `one_line()` helper only trims caption *length* by whole
  clauses — it never estimates pixel width.
- `scripts/ae/build_frazier_cards_jsx.py`: same — fixed sizes + native
  CENTER/LEFT/RIGHT justification; `maskedText()` renders into fixed-width slab precomps
  (slabW 1500–1860). No width estimation anywhere. Also **throws on font-not-found**
  (line 200) so a silent font substitution is impossible.

The EP40 bug was a width *estimate* that mis-sized text against an underline/frame
("EXCLUDED" → ":XCLUDEI"). frazier has no such estimator. The only theoretical residual
risk is a fixed-size string overflowing its fixed slab → slab-edge crop; verified below
that none do.

### Frame-by-frame visual check (all outputs on H:/…/08_edit/)

**ae_hero/ (8 beats — all CLEAN, fonts correct):**

| id | strings checked | result |
|----|-----------------|--------|
| hb01 | MEASURED IQ / 70 / FUNCTIONED AT TEN | clean |
| hb02 | THE VERDICT / 1988 / DEC 16, 1988 · LIFE | clean |
| hb03 | THE RULE / 1969 / **FRAZIER v. CUPP · 394 U.S. 731** | clean (flagged long string — full, centered) |
| hb04 | PRINTS CLAIMED · PRINTS THAT EXISTED / 1 · 0 / TOLD TO BARRY LAUGHMAN | clean (split-ratio) |
| hb05 | TAKEN / 16 YEARS / IN AT 25 · OUT AT 40 | clean |
| hb06 | **257 EXONERATIONS** / **4,102 YEARS** / END TO END | clean (flagged long strings — full) |
| hb07 | NO PAROLE UNTIL / 2046 / PLEADED GUILTY 2023 | clean |
| hb08 | BY 2026 / 10 STATES / CHILDREN ONLY | clean |

**ae_cards/ (12 — all CLEAN, fonts correct):**

| id | strings checked | result |
|----|-----------------|--------|
| act1 | ACT I / AUGUST 13, 1987 | clean |
| act2 | ACT II / THE STATEMENT | clean |
| act3 | ACT III / FRAZIER v. CUPP | clean |
| act4 | ACT IV / SIXTEEN YEARS | clean |
| stamp_frazier | FRAZIER v. CUPP / 394 U.S. 731 (1969) / **ARGUED FEB 26, 1969 · DECIDED APR 22, 1969** | clean (longest string — full, wide-tracked, centered) |
| stats_ip | 257 CASES / 29% FALSE CONFESSION / 62% **MISTAKEN EYEWITNESS ID** / 205 CLEARED BY DNA / **IN AT 27, OUT AT 45** + AVERAGE EXONEREE | clean (all 5 rows, no crop) |
| doc_statement | A STATEMENT IN HIS OWN NAME (page is texture-only, no glyphs by design) | clean |
| hook_fingerprint | THE FINGERPRINT DID NOT EXIST | clean |
| iq_told | IQ 70 / TOLD: "YOUR PRINTS ARE THERE." | clean |
| exonerated | EXONERATED 2004 / DIED 2024 | clean |
| trans_sink | (no text) | n/a |
| trans_wipe | (no text) | n/a |

Every specifically-flagged long string — `FRAZIER v. CUPP · 394 U.S. 731`,
`257 EXONERATIONS`, the stats multi-line block, the act titles, and the widest one
`ARGUED FEB 26, 1969 · DECIDED APR 22, 1969` — sits fully within frame with generous
side margins. No underline/frame overrun. Anton (numerals) and Oswald (labels) both
resolve correctly; no substituted faces observed.

---

## Bottom line
frazier is **not** affected by either EP40 clipping bug. Nothing to re-render or
re-build for text clipping. (If the casefilm is ever re-rendered for unrelated reasons,
it will harmlessly pick up the already-applied KineticCaptions fix.)
