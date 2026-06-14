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

## Open (decide next)

- Pino's **personality** (curious / witty / calm-wise / deadpan).
- **Channel name + handle.**
- Pino's **voice id** (ElevenLabs) and speaking style.
- First episode topic + a Shorts batch.
