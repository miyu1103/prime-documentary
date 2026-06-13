# Contract — Topic screening

## Input

- Artifact type: `topic-candidate`
- Exact immutable revisions required

## Preconditions

- channel strategy
- demand signals

## Output

- Artifact type: `topic-evaluation`
- score breakdown
- uncertainty
- risk
- kill condition


## Common execution envelope

```json
{
  "contract_version": "1.0.0",
  "episode_id": "PD-2026-001-example",
  "stage": "stage.name",
  "input_revisions": [],
  "config_revision": "cfg-v001",
  "idempotency_key": "sha256:...",
  "requested_by": "orchestrator",
  "dry_run": false,
  "budget_reservation_id": null
}
```

## Required result envelope

```json
{
  "status": "succeeded",
  "output_revisions": [],
  "validation": {
    "schema": "pass",
    "quality_gate": "pass"
  },
  "warnings": [],
  "cost": {},
  "provenance": {},
  "retry": {
    "classification": "none"
  }
}
```

## Idempotency

Same stage, same exact input revisions, same config revision, and same provider profile must resolve to the same idempotency key. A prior successful result is reused unless an explicit force-rerun reason is recorded.

## Failures

Failures use the canonical error taxonomy. Retryable failure must not mutate approved artifacts. Terminal failure must create a blocker with actionable evidence.

## Staleness

Any change to an input revision marks this output stale. Stale artifacts remain immutable and auditable but cannot satisfy downstream gates.

## Approval

The stage may request approval according to operation-level autonomy policy. Approval always targets an exact output revision.
