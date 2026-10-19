# EP78 · {TITLE} — SCRIPT v001

<!--
THE TEMPLATE THAT MAKES THE GATES GREEN BY CONSTRUCTION (EP77+, binding via
scripts/check_ep77_standard.py — an episode 077+ cannot reach the render without this shape).

Why each rule exists, with the number behind it (all measured 2026-08-23, 34 finished episodes):

  * ONE QUESTION PER ACT. retention_cadence was red on 18/34. It is NOT the number of
    questions — ramirez asked 10 and failed because they clustered in the first six minutes;
    greene asked 8, spread them, and passed. One literal "?" per act guarantees no 7-minute
    question-free gap at ~160 wpm, which is the exact thing the gate measures.
  * THE HEADINGS BELOW, EXACTLY. structure_4part was red on 14/34. The post-render gate reads
    the narration section labels; these headings become those labels.
  * LENGTH: the spec's word band is the law (episode_spec.v001.json). At the measured 160 wpm
    (PD_CANON §7 25 — do NOT use 176), 30 min ≈ 4,800 spoken words. Check with:
        py -3.11 scripts/check_script_retention_plan.py --script <this file>
  * NO JAPANESE in narration lines (narration-dropout bug, PD_CANON §7 26).
  * Every factual sentence carries its ledger row id as an HTML comment — they are stripped
    before speech and check_script_length no longer counts them.

Replace every {PLACEHOLDER}. Delete this comment block when done. Keep the headings.
-->

## HOOK
<!-- 8 seconds of film ≈ 20-25 words. Open on the scene, not the system. -->
{The concrete moment. A person, a place, a time.}
{The impossible outcome, stated plainly.}
{One question the viewer now owns: ...?}

## OP
<!-- canonical bookend — not narrated, do not write copy here -->

## ACT_1 — {WHAT HAPPENED}
{An ordinary person, an ordinary day, contact with the system.}
{...}
{Act question: ...?}

## ACT_2 — {WHY THAT SHOULD BE IMPOSSIBLE}
{...}
{Act question: ...?}

## ACT_3 — {ANATOMY OF THE HIDDEN SYSTEM}
<!-- state the system's own rationale before showing its failure (editorial direction v002 §9) -->
{...}
{Act question: ...?}

## ACT_4 — {THE OUTCOME}
{...}
{Act question: ...?}

## ENDING
<!-- fear lands on preparedness: "the world is frightening" -> "now I can see it" -->
{The hidden rule, named in one sentence.}
{And this concerns you, because ...}
