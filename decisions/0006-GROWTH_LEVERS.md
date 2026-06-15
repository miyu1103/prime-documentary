# 0006 — Growth levers: every controllable input, as executable rules

Status: **accepted** (owner direction 2026-06-14, "cover everything we can control").
Applies to **both channels**. Consolidates the success levers into rules the pipeline/agents must
follow. Builds on `0002 §K/§M` (topic + threading), `0003` (Pino), `0004` (quality), `0005`
(packaging).

**Control boundary (state it plainly):** we control **inputs** — topic, packaging, retention
structure, quality, sound, launch ops, iteration speed, volume. We do **not** control outcomes — the
algorithm's decisions, virality, taste, competitors, policy shifts. Strategy = **maximize every
controllable input; treat output as probabilistic; never bet the channel on one video.**

## A. Topic & demand — `topic-strategist`
- **Outlier-driven selection:** systematically find videos that **overperformed their channel size**
  and produce a **sharper, higher-quality version**. Prefer proven demand over novel obscurity.
- **Suggested-adjacency:** when a big video is currently winning a topic, make adjacent content to
  ride the *suggested* feed (the main growth engine), not just search.
- **Topical authority:** cluster episodes so YouTube reads the channel as **the entity** for the
  niche ("US rights cases", "everyday money tricks") → recurring suggested placement.
- Weight: recognition + evergreen + advertiser-safety + high-CPM + series-thread fit (0002 §M).

## B. Packaging-first — `package-strategist`
- **Design title + thumbnail BEFORE production.** If a compelling package can't be made, **don't
  make the video.** Reverse the workflow.
- Build to 0005 (same frame / different punch; complementary title↔thumbnail).
- **North-star metric = CTR × average-view-duration** (not raw views). Optimize the product.
- **A/B test** packages (Test & Compare); **repackage underperformers** before retiring them.

## C. Retention engineering — `documentary-writer` + `edit-engineer` + `retention-engineer`
- **Obsess the first 30 seconds** (the intro retention cliff); the **flash-forward 5–8s hook** (0004).
- **Open loops + act cliffhangers**; delayed payoff.
- **Self-relevant framing** — make it about the viewer ("your rights", "your money"), not a bystander.
- **Pattern interrupts** + varied pacing + 0.5–1s punch inserts (0004 rhythm).

## D. Engagement design — `documentary-writer` + `package-strategist`
- **One comment-driving question** per video (a safe, debatable prompt) — pinned.
- **Shareable / saveable value** — a concrete takeaway people forward or save (esp. Pino "don't get
  fooled"); saves + shares are strong signals.
- Clear single CTA (subscribe / next).

## E. Session time & funnel — `package-strategist` + `edit-engineer`
- **End screens → next video**; **playlists/series** engineered for binge (session watch-time is a
  top ranking signal).
- **Shorts → long-form funnel:** Shorts for discovery + subscribers; long-form for retention +
  monetization. Engineer the handoff (Short teases the long deep-dive).
- **Cross-channel promo:** ch1 ↔ ch2 share "hidden systems" DNA; cross-link where genuine.

## F. Launch & operations — `production-controller` + `pd-publish`
- **48-hour launch protocol:** publish at a strong slot, notify subscribers, watch early
  CTR/retention (the algorithm's initial test window decides reach). No fake engagement.
- **Buffer of finished videos** so the best can ship on the best schedule and cadence never breaks.
- **Fast iteration:** ship → measure → adjust in **days, not months**. Fastest learner wins.
- **Volume / swings:** many at-bats × high quality; **one outlier can carry a channel** — maximize
  quality swings, don't perfectionist-stall a single video.

## G. Quality & differentiation — per `0004`
- Production quality, **premium sound + distinct voice**, abundance floors (0004 §E2) — the moat in a
  low-effort-AI sea.
- **Character IP (Pino)** — a copy-proof asset (recognition, future expansion).

## H. Monetization — `package-strategist` + `topic-strategist`
- **High-CPM lean** (finance/insurance/legal-adjacent topics, mass-market framing).
- **≥ 8-min** long-form for mid-roll inventory, balanced against retention.
- **US/English**, **not-made-for-kids**, advertiser-safe (0003 §Safety, 0002 §N).

## I. Learning loop — `analytics-strategist` (the compounding edge, CLAUDE.md §1)
- Track per video: **CTR, impressions, AVD, retention-graph dips, traffic source (search vs browse
  vs suggested), saves/shares/comments.**
- Feed `package-strategist` + `topic-strategist`: **double down on winning patterns, retire losers,
  fix the exact retention dips** next time. Turn each episode's data into a recorded learning rule.

## J. Binds & enforcement
Each lever is owned by the agent above and checked at its stage; `pd-qc` and the package/publish
gates verify B–H are satisfied before a video ships. The learning loop (I) updates the standards
over time. None of this lowers the safety/rights/BAN gates (0002 §N).
