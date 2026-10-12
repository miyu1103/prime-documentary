# PD-2026-017-onecoin — "Nothing" (mid-feature, ~30 min)

OneCoin / Ruja Ignatova "The Missing Cryptoqueen": a cryptocurrency with **no blockchain at all** that took in billions through belief and the fear of missing out — and a founder who vanished in 2017 and remains on the FBI Most Wanted list. Not a crypto explainer: a study of why a lie that gives people hope outsells a truth that offers them nothing.

- **State:** `approved` (topic gate) · **Risk:** R3 · **Tier:** A · **Lang:** EN narration · **Profile:** mid ~30 min (ADR-0008)
- **Thesis:** A lie that gives people hope will always outsell a truth that offers them nothing; the crowd defended the con because of what believing it made them feel.
- **Moral center / dignity guardrail:** the victims (ordinary people who lost savings). No schadenfreude; living fugitive/associates via the indictment/records only ("alleged/charged"); no real-person likeness.
- **Ambition:** a 30-min auteur short film whose FORM enacts the con (seduce → believe → nothing); gold→white→black; second-person complicity; the "empty ledger" motif; an unresolved ending.

## Done so far (Claude, left process)
- `00_topic/topic.v001.json` (R3, score 90) · `04_scenes/design_bible.v001.md` (auteur treatment + acceptance contract §7) · `manifest.json`.
- Infra: `decisions/0008-mid-duration-profile.md` (validator mid band) · binds to `docs/PD_ONE_PASS_PRODUCTION_SPEC.v1.md`.

## Next (Claude, left process)
research (`pd-research`, primary: DOJ indictment / FBI Most Wanted / national-regulator actions / technologist account that no real blockchain existed / BBC reporting) → claims/sources → script.en (5 movements, ~4.0–4.5k words) → annotated → `validate_episode.py 17` (mid) → script_verified → shotlist + ai_prompts + thumb_prompts → **fact_recheck packet (R3, legal-review-ready)** → Codex handoff.

## Definition of done (binding)
`./.venv/Scripts/python.exe scripts/check_final_acceptance.py 17` → exit 0 (+ manual rows 5/7/12/13 of the spec). Validator PASS is NOT "done."

## Remaining human gates
final script · first cut · title/thumbnail (manual upload) · **pre-publish legal + fact re-check (R3)** · public scheduling. ElevenLabs master narration = cost gate (owner GO).
