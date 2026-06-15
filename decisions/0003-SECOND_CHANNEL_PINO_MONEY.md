# 0003 — Second channel: Pino, mass-market everyday-money explainer

Status: **accepted** (owner direction 2026-06-14)
Relates to: `decisions/0002` (channel 1, court cases) — shared "hidden systems" brand DNA, reuses
the same PD pipeline, Remotion infra, and all safety gates.

## Context

A second YouTube channel built around an original mascot character, **Pino** (a round, fluffy,
glowing creature; expression set already generated in Midjourney). Goal: a scalable character-IP
channel. Owner priority is explicit and ordered: **make money first; target the highest ad rates;
never get the channel banned.**

## Decision

- **Subject: mass-market, everyday MONEY** — the money and economics of ordinary life, explained
  simply. *Not* specialized/expert finance, *not* jargon. e.g. "why things cost what they do,"
  consumer scams, hidden fees, how businesses actually make money, the economics of everyday things.
- **Pino is the host and speaks** in a **clear, friendly, adult-intelligible voice** (deliberately
  **not** baby-cute — that would risk a "made-for-kids" classification; see Safety).
- **Audience: general adults**, advertiser-friendly.
- **Format: both** — **Shorts** (discovery + subscriber growth) and **long-form 8–12 min**
  (monetization). A Short hook can graduate into a long-form deep-dive on the same system.
- **Objective: maximize CPM/RPM and revenue** (CLAUDE.md §2). Money is the first priority.
- **Episode formula:** a familiar money question everyone has wondered → reveal the hidden system
  behind it → "now you know" → tease the next (reuses 0002 §K threading, §M topic selection).
- **Readability:** mass-market, even simpler/punchier than channel 1 — US grade ~6–7, short
  sentences, concrete, no finance jargon (extends 0002 §J).
- **CPM lean (within mass-market):** favor topics that touch real money decisions — banking, credit,
  insurance, fees, big purchases, subscriptions, scams — framed accessibly. These attract
  finance/insurance advertisers (top CPM) without being "expert."

## Safety — must not get banned (highest constraint)

All of `decisions/0002 §N` (channel-survival / non-termination) applies as hard publish gates.
Money-channel specifics:

- **Set "not made for kids"** at the channel/video level; keep Pino's voice/tone adult-readable so
  YouTube does not auto-classify as kids content (COPPA → near-zero ad revenue).
- **No financial / investment advice, no "get rich quick," no guaranteed-returns or earnings
  claims.** This is YMYL ("your money your life") — explain *how money works*, never tell viewers
  what to do with theirs. Avoids advice liability, scam-policy strikes, and demonetization.
- **Facts cited** (claim ledger + fact-checker); numbers sourced and dated; no misleading
  thumbnails/titles.
- Advertiser-friendly, neutral-but-fun tone; no sensational "they're stealing your money" rage-bait.

## Production (reuse PD infra)

- Visuals: Pino expression set (Midjourney) → Remotion 2.5D rig (blink / mouth-flap / gestures, $0)
  + optional LivePortrait lip-sync on the 4090 (free) → composited with kinetic money graphics.
- Audio: ElevenLabs narration as Pino's voice (pick a distinct, clear, friendly voice id — separate
  from channel 1's "Brian"); reuse the music/SFX/ambience library.
- Same manifest / revision / approval / QC / publish-preflight machinery as channel 1.

## Binds

`topic-strategist`, `documentary-writer`, `visual-director`, `package-strategist`, `rights-editor`,
`audio-director`.

## Identity (owner decisions 2026-06-14)

- **Channel name: "Money with Pino"** (handle TBD; verify availability).
- **Personality: sharp & skeptical — "don't get fooled."** A savvy consumer-advocate who shows you
  how money tricks work so you see them coming.
- **Voice: bright & upbeat**, clear and adult-intelligible (ElevenLabs voice id TBD — distinct from
  channel 1's Brian; not baby-cute → avoids kids classification).
- **Combination = "cheerful but street-smart":** upbeat delivery over savvy, protective content.

> Tone guardrail (ties to Safety + 0002 §N): the "don't get fooled" angle is **empowering and
> educational, never conspiratorial rage-bait.** Frame as "here's how this works, so it can't work
> on you," not "THEY are stealing from you." Keeps it advertiser-safe and trustworthy.

## Open (decide next)

- Pino's **ElevenLabs voice id** (pick a bright, clear, upbeat adult voice).
- Channel **handle** + availability check.
- First long-form topic + an opening **Shorts batch**.

## Content formats & launch (owner-designed 2026-06-14)

**Episode formula (all formats):** a familiar money question everyone has wondered → reveal the
hidden system/trick behind it → "now you know" → tease the next. Empowering, never rage-bait (§Safety).

**Repeatable formats (each a reusable template):**
1. **Why is X so expensive?** — hidden margin/structure (popcorn, ink, concert tickets). Short/long.
2. **The trick behind X** — one seller tactic ($9.99 charm pricing, "limited time", drip fees). Short.
3. **How does X actually make money?** — business model reveal (free apps, Costco, casinos, IKEA). Long.
4. **Don't get fooled: X** — scam/trap awareness (subscription traps, fake discounts, warranties). Short/long.
5. **A vs B — which is the rip-off?** — comparison (brand vs generic, lease vs buy, cash vs card). Short.
6. **The hidden cost of X** — what you don't see (free shipping, buy-now-pay-later, airline fees). Short.
7. **How they make you spend more** — psychology/design (store layout, menus, dark patterns). Long.

**Launch rotation (3 pillars):** signature Short **"Pino's trick reveal"** (format 2) · signature
Short **"Don't get fooled"** (format 4, save/share-worthy) · flagship long-form **"How X makes
money"** (format 3, monetization). Shorts → discovery/subs; long-form → revenue. Name the recurring
series for brand recognition.

**Opening Shorts batch (first 5):** (1) why movie popcorn is $8 · (2) why prices end in $9.99 ·
(3) why "free" apps make billions · (4) why the gym wants your January signup · (5) why cards make
you spend more than cash. **First long-form:** "Supermarkets are designed to make you spend more."

**Sample Short script — "Why is movie popcorn so expensive?" (~50s, Pino, upbeat + savvy):**
> "Eight bucks for popcorn? Yeah — that's on purpose. Theaters barely make money on your ticket —
> most of it goes to the studio. So how do they survive? You. At the snack counter. Popcorn costs
> them pennies and sells for eight dollars. That's not an accident — that IS the business. The movie
> gets you in the door; the popcorn pays the rent. So next time you see that giant bucket, now you
> know what it's really for. Follow for more tricks they hope you never notice."

Readability grade ~6–7; structure = surprise → mechanism → number → "don't get fooled" → follow CTA.
Production reuses the PD pipeline + Pino expression set + Remotion rig (0003 §Production).
