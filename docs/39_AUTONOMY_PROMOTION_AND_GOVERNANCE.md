# 39 — Autonomy Promotion and Governance

## 1. Principle

Autonomy is a permission earned by evidence. Each operation has its own autonomy level.

## 2. Operation-level policy

- manual
- suggest
- auto_with_review
- auto_unless_flagged
- fully_auto
- disabled

## 3. Promotion evidence

- sample size
- acceptance rate
- false negative rate
- critical incident count
- reviewer agreement
- cost variance
- retry stability
- rollback test
- content risk class

## 4. Promotion example

Visual selection for low-risk environment shots may promote to `auto_unless_flagged` after stable results. Public scheduling remains manual even if image selection is automated.

## 5. Demotion

Automatic demotion when:
- critical incident
- provider/model change
- schema change affecting validation
- drift in acceptance
- terms/rights uncertainty
- repeated human override

## 6. Sample audit

Fully automated operations still receive random audit. Sample rate depends on risk and history.

## 7. Policy engine inputs

- operation
- content risk
- provider version
- model/prompt version
- confidence
- budget
- past acceptance
- active incident
- current autonomy level

## 8. Governance review

Monthly autonomy board, even if one person operates it:
- promotions
- demotions
- incidents
- false alarms
- cost effects
- human time saved
- quality effect

## 9. Prohibited automatic promotions

- public publish
- legal/medical high-risk assertion
- destructive delete
- rights exception
- credential scope expansion

unless separately and explicitly redesigned with stronger controls.
