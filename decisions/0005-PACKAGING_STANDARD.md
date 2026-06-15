# 0005 — Packaging standard: thumbnail + title + description (both channels)

Status: **accepted** (owner delegated 2026-06-14). Applies to **both** channel 1 (court cases) and
channel 2 (Money with Pino). Extends `decisions/0002 §D/§G` (ch1 brand look). The package is the
single biggest **discovery** lever; the title↔thumbnail approval gate (rule 16) is unchanged.

Core principle: **thumbnail and title are complementary** — the **thumbnail carries the surprise**,
the **title carries the recognition/search**. They never repeat the same words.

## A. Thumbnail system — "same frame, different punch"

**Keep consistent (brand → recognition, repeat clicks):**
- Palette (ink/navy + electric blue + gold), display font, layout structure, logo placement.
- The `ThumbConcept` skeleton (ch1) / a Pino skeleton (ch2).

**Vary per video (→ click-worthy):**
- Background image / subject, the bold words, the emotional/curiosity hook.

**Rules:**
- **Objective = maximize CTR.** Every thumbnail choice serves the click: a curiosity/emotion trigger,
  strong contrast, one unmistakable focal point, the fewest possible words at the biggest size, and a
  clear read at phone-thumbnail scale. Validate by shrinking it tiny — if it still hits, it works.
- **3–5 huge words**, one focal point, **mobile-legible**, high contrast.
- **Channel 2: Pino appears in every thumbnail** — a recurring character face is a top CTR + brand
  device.
- Not identical episode-to-episode (identical = blurs together in the feed).
- **A/B test — MANDATORY on every video, in YouTube Studio → "Test & Compare".** Submit **2–3
  thumbnail variants** (and titles where the feature allows); YouTube rotates them and picks the
  winner by watch-time share. Keep the winner; feed results into the learning loop (§D) to refine the
  skeleton. So produce ≥2 thumbnail variants + ≥2 candidate titles per episode by default.

## B. Title system

**Rules:**
- **Curiosity gap — don't reveal the answer** ("Why…", "The reason…", "What nobody tells you…").
- **Front-load keywords** (first 3–5 words; mobile/search truncates ~40 chars).
- **Specific / numbers** beat vague ("4 words" > "some words").
- **~40–60 characters**; land the hook early.
- **Complement the thumbnail** (no repeated words).
- **No clickbait lies** — title must match content (BAN/CTR-decay risk, §N).

**Power formats:**
- Question — `Why Do Police Read You Your Rights?`
- Paradox/contradiction — `He Won at the Supreme Court — and Still Went to Prison`
- Hidden reason — `The Hidden Reason …` / `What Nobody Tells You About …`
- Mechanism — `How [X] Actually Works`

Mix **search-optimized** (keyword-heavy) and **browse-optimized** (curiosity-heavy) titles across
the channel. **A/B test** by swapping and watching CTR.

## C. Description template (SEO + discovery + retention)

Lower direct-CTR impact, but drives search, suggested-video matching, and retention. Templated:

```
[1–2 line hook + keywords]            ← most important (shown above "...more")
⏱ Chapters (timestamps)               ← retention + search "key moments"
📚 Source(s)                          ← credibility (links)
▶ Next: [next episode tease]  /  👉 Subscribe …
[fixed footer: channel links · disclaimers (AI/synthetic + "not advice") · #3 hashtags]
```

**Rules:**
- First **2 lines** carry the hook + main keywords (rest is collapsed).
- Chapters required (UX + search + retention).
- Keywords **natural**, not stuffed.
- Disclosures live here (AI/synthetic; "not legal advice" ch1 / "not financial advice" ch2) — §N.
- 3 relevant hashtags (render above the title).

## D. Learning loop

`analytics-strategist` reads CTR / impressions / search vs browse traffic and feeds
`package-strategist`: double down on the title/thumbnail patterns that win, retire what doesn't,
and refine the per-channel skeleton over time (the measurable advantage, CLAUDE.md §1).

## E. Binds

`package-strategist` (build the package to this standard), `analytics-strategist` (test + learn),
`documentary-writer` (title options), `visual-director` (thumbnail image). Title↔thumbnail pair
still requires owner approval for the exact revision (rule 16).
