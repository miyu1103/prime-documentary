EP71 OROVILLE — CODEX PASTE SET (batch A)
episode PD-2026-071-oroville · slug oroville

WHAT THIS IS
  12 files, batch_01.txt … batch_12.txt, carrying all 118 commissioned plates
  O001–O118. Each file is one paste into one Codex session. Paste the whole file.
  Source of every word in here: episodes/_planning/EP71_oroville_CODEX_BATCH_A.v001.md.
  These files are a SPLIT of that document. No prompt was written, reworded or improved here.

BATCH SIZE, AND WHY IT IS 10 AND NOT 20
  EP70's batches ran 20 plates at ~22 KB. EP71's canonical [STYLE] (750 chars) and [NEG]
  (1,408 chars) are more than four times EP70's, so 20 plates would be ~48 KB — twice a
  pasteable batch. Batch size here is set by BYTES, not by plate count: 10 plates per file,
  24–25 KB each, which is what EP70's 22 KB actually bought.

PLATE COUNT
  118 commissioned plates, ids O001–O118, contiguous, no duplicates, reconciled against
  episode_spec.v001.json mandatory_stills (118) — exact match, both directions.
  20 of them are people plates and match episode_spec people_plates exactly.
  Plates run in DOCUMENT order, not numeric order: O115–O118 are the four plates added to
  the shelter block and they sit inside ACT_3 between O065 and O066, exactly where the order
  document and the scene plan put them. batch_07 therefore ends ACT_3 and opens ACT_4.

FILE NAMES AND DELIVERY
  Deliver to:  episodes/PD-2026-071-oroville/05_visuals/approved/
  Convention:  O001.png and O001b.png — the plate id, lower-case 'b' on the second camera
               position, .png, nothing else in the name. No spaces, no descriptive words.
               (A descriptive filename is not free: check_spec_satisfied.py matches
               forbidden_subjects against the FILE NAME as whole words. See GAPS.md §3.)
  Two images per prompt = 236 files for 118 declared stills. The 118 named ids are the
  contract; the b-variants are headroom against reject-and-flag, per EP70.

RESOLUTION
  Long edge 3840 px or greater on every plate, 16:9. Production spec v2 row 5.
  public/img is the render truth.

WHAT IS BARRED, ON EVERY PLATE
  The [NEG] block is repeated in full under every single prompt. That is deliberate: a Codex
  session drops context between pastes, and an un-repeated negative is a negative that will
  not apply. Do not strip it, do not shorten it, do not state it once at the top.
  Above all: nothing flooded, breached, collapsed, rescued or mourned — the dam did not
  fail and no town flooded; no children; no document facsimile (card, not scan); and no
  likeness of a real identifiable individual.

BEFORE COMMISSIONING
  py -3.11 scripts/check_image_order_neg.py --file episodes/_planning/EP71_oroville_CODEX_BATCH_A.v001.md
  py -3.11 scripts/check_prompt_diversity.py
  And read GAPS.md in this directory first. Nothing was left out of the paste set, but two
  findings affect delivery: the forbidden term `manila` collides with this film's own
  document ground (§3), and O107 is declared a people plate whose prompt has no person in
  it (§4).
