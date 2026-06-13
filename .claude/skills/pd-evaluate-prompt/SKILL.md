---
name: pd-evaluate-prompt
description: Evaluate a prompt or model change against a frozen dataset
---

# Procedure


1. Identify task, current prompt/model, candidate and evaluation set.
2. Freeze inputs and randomize comparison order where relevant.
3. Run schema and deterministic validators.
4. Run independent rubric review.
5. Compare critical error, acceptance, repair rate, latency, cost and human review time.
6. Inspect failure clusters.
7. Recommend promote/hold/reject with rollback version.
8. Update prompt registry only after acceptance.


# Required report

- exact scope and revisions
- inputs inspected
- actions or proposed actions
- verification
- side effects and cost
- blockers
- rollback or disable path
