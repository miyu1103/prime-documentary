---
name: pd-autonomy-review
description: Evaluate whether an operation can be promoted or must be demoted
---

# Procedure


1. Select one operation, not the whole pipeline.
2. Gather sample size, acceptance, false negatives, critical incidents, reviewer agreement, cost variance and rollback evidence.
3. Segment by risk class, provider and model/prompt version.
4. Compare saved human time against added risk and rework.
5. Recommend promote/hold/demote.
6. Create or update the exact autonomy policy revision.
7. Define random audit rate and automatic demotion triggers.
8. Public publishing and destructive operations remain manual unless explicitly redesigned.


# Required report

- exact scope and revisions
- inputs inspected
- actions or proposed actions
- verification
- side effects and cost
- blockers
- rollback or disable path
