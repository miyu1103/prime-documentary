# AE jobs file — format v001 (EP77+)

`scripts/ae/jobs_{slug}.json` is the render-ready form of the `ae_beats` an episode's
`episode_spec.v001.json` declares (ADR-0011). One file per episode, a **flat JSON array** so
`render_beats.sh` can read it unchanged. Validate with
`py -3.11 scripts/ae/check_ae_jobs.py --slug <slug>` — it refuses a file that drops a declared
beat, retypes a number as a string, or breaks the ≥12 / ≥90 s floors.

## Fields per job

| field | type | meaning |
|---|---|---|
| `id` | str | `{slug}_{beat id lower}` — globally unique because AE writes `{id}.avi/webm` into one shared out dir |
| `beat` | str | the spec's beat id (`AE001`) — traceability back to the contract |
| `act` / `kind` / `source` | str | passthrough from the spec, unedited |
| `seconds` | number | equals the spec's `duration_sec` |
| `headline` | str | the display string the spec declares |
| `style` | str? | present ONLY where today's `kinetic_beat.jsx` renders the kind correctly (`number`, `punch`). Absent = needs the ADR-0011 generic builder; **do not feed style-less jobs to `render_beats.sh`** |
| `big` / `bigSize` / `label` / `words` | | the fields `kinetic_beat.jsx` consumes, when `style` is set |
| `value` / `prefix` / `suffix` | number / str / str | the typed number behind a numeric card. **`value` is a JSON number, never a string** — a string arrives on screen as NaN (EP76 morandi, 2026-08-24). Currency goes in `prefix`, unit in `suffix`. Timestamps/dates are display strings, not values |
| `value_a` / `value_b` | number | the two sides of a `comparison`, same typing rule |
| `lines` | list | body copy for `list_build` / `system_map` / `timeline` / `comparison`. Every line that states a fact carries its ledger row id in `cite` |
| `quote` / `attribution` | str | `quote_card` only — the quote verbatim from the ledger row, never paraphrased |
| `forbid` | str | the R3 guardrail bound to this card (from the spec notes / ledger). The renderer and the reviewer both read it |

## Rules

1. Every beat in the spec appears exactly once; ids, acts, kinds, seconds match the spec byte
   for byte. The jobs file adds render detail; it never edits the contract.
2. Display copy beyond the declared headline must trace to a ledger row (`cite`), same as
   narration. No invented numbers, no verdict vocabulary where the ledger says charges.
3. `document_blowup` never renders readable document text (fabricated_record class).
4. AE runs through `pd_run.sh` with its own lock class, `gpuAccelType SOFTWARE`, and the
   `PriorSafeMode.txt` crash-trap cleanup (ADR-0011).
