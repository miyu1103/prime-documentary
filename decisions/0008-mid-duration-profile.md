# ADR-0008 — Mid-length duration profile (~30 min)

**Status:** Accepted (2026-06-27)
**Context:** EP17 (`PD-2026-017-onecoin`) is a **~30-minute mid-feature** — longer than the standard explainer (11.5–12.5 min) but shorter than the 60-min flagship feature (ADR-0003). `validate_episode.py` had only two bands: standard (10.0–12.8 narration-min) and a single `tdm>=20` "feature" band (0.50–1.05× runtime). A 30-min episode where **narration ≈ runtime** (little designed silence, unlike Titan) was being checked against a band whose lower bound (0.50×=15 min) was far too loose.

**Decision:** Split the long-form handling into two explicit, documented profiles keyed off `manifest.target_duration_minutes` (no silent weakening of the standard gate — invariant 15):

| Profile | target_duration_minutes | Narration band (of runtime) | Rationale |
|---|---|---|---|
| standard | unset / < 20 | fixed **10.0–12.8 min** | unchanged |
| **mid** | **20 ≤ tdm < 45** | **0.80–1.08 × tdm** | narration ≈ runtime; modest holds only |
| feature | tdm ≥ 45 | 0.50–0.85 × tdm | heavy designed silence/visual (ADR-0003) |

For EP17 (`tdm=30`): narration band **24.0–32.4 min** (≈ 3,600–4,860 words @150 wpm). FK ≤ 9.5 and the AI-filler ban are unchanged.

**Companion (finished-runtime, not narration):** `scripts/check_final_acceptance.py` measures the **rendered runtime** band from the same field — mid = **27–33 min** (1620–1980 s) — independent of this narration-minutes gate.

**Consequences:** EP16 (feature, tdm=58) is unaffected (narration 41.8 min stays within 29.0–49.3). A new 30-min class is now first-class and verifiable. Any future band change is an ADR, never an inline edit (source-of-truth hierarchy).
