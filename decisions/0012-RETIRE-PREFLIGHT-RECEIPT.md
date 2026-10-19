# ADR-0012 — `preflight_receipt` is retired: it measured a pipeline that no longer exists

**Status:** Accepted (2026-08-23, under the owner's rebuild directive of the same day)
**Review by:** 2026-10-05
**Revoke if:** any episode from EP77 on ships with a defect that `preflight_render_gate.py`'s
four checks (motion budget / assets exist / coverage / film crosscheck) would have caught and
that no surviving pre-render gate did catch — measured against the shipped master with
`check_final_acceptance.py`. One such episode reinstates the check the same day.
**Scope:** the acceptance check `preflight_receipt` in `check_final_acceptance.py`, and nothing
else. The tool `preflight_render_gate.py` itself stays on disk, unmodified.

## What was measured (2026-08-23)

| fact | number |
|---|---|
| finished episodes red on `preflight_receipt` at ship time | **27 of 34** |
| calls to `preflight_render_gate.py` from any pipeline script | **0** |
| recent 10 episodes having `remotion_plan.v*.json`, which it requires | **0 of 10** |
| … `asset_selection.v*.json` | **0 of 10** |
| … `scene_plan.v*.json` | 1 of 10 |
| … `script.annotated.v*.json` | 2 of 10 |

The experiment that settled it: the gate was actually run on EP69 hyatt — a finished,
receipted, scheduled film — and wrote a receipt whose verdict is **BLOCK**, because the four
planning artifacts it validates are ones the channel stopped producing around EP67. Wiring it
in (the obvious "fix") would therefore have put a permanent, unfixable red on every future
episode. The red on 27 episodes was never information about the films; it was the calendar of
when the pipeline changed shape.

## What replaces the protection it was for

The intent — "validate the plan before the heavy render" — is not abandoned; it is carried by
gates that read the artifacts the pipeline produces **now**:

- `check_spec_satisfied.py` (wired, `[4/7]`): mandatory stills in cuts, forbidden subjects
- `probe_before_render.sh` (wired, pre-render): renders a real 60 s slice, measures black /
  freeze / motion, writes its own receipt
- `check_ep77_standard.py --stage plan` (wired, `[4d]`, EP77+): still-hold caps before the GPU
- `check_gates_still_bite.py` (wired, queue start): proves the surviving gates still reject
  bad input

## The rule this writes down

A gate whose required inputs the pipeline no longer produces does not degrade into "extra
safety". It degrades into a permanent red that trains everyone to ignore red — which is how
three real defects hid inside the noise for months (CLAUDE.md §4.6). Retire it, on the record,
with a revoke condition.
