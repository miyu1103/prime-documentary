# SHORTS_METHOD v001 — Prime Documentary Shorts production spec
**Purpose:** the RULES every Short must follow to be a growth/subscriber engine (not just "more posts"). Evidence-based (Law By Mike 93M, in-lane top shorts, CTR research). Owner-approved 2026-07-23. This governs all Shorts from the next one on. Refined continuously by the TOP-1% GROWTH REFERENCE + our own per-short retention data.
**Role in strategy:** Shorts = REACH + SUBSCRIBER engine (top of funnel). Long-form = revenue + retention. Shorts RPM is low — grow with Shorts, monetize with long-form. See [[pd-monetization-strategy]].

---

## THE 12 RULES (each is a hard build requirement + how to verify)

1. **1-SECOND HOOK.** No intro, no logo, no "in this video." Open MID-action on the single most shocking line/image. The first spoken line + first frame must state or tease the payoff. Verify: watch frame 0-30 (1s) muted AND with sound — is the hook already landing?
2. **PACKAGING-FIRST.** Write the cover frame + the first line + the title BEFORE building. The cover (first ~1.5s coverfirst) and the opening line ARE the packaging. Verify: cover + first line exist and carry a curiosity gap before any footage is chosen.
3. **OPEN-LOOP → PAYOFF.** State a shocking premise/question up front, WITHHOLD the answer, deliver it at the very end. The whole short exists to make them watch to the payoff. Verify: the last 3s answer the first 2s.
4. **LENGTH 20–40s target** (test per short; completion% > length). Only go to ~60s if the payoff needs it. Never pad. Verify: runtime ≤ 60s; prefer 20–40s unless justified.
5. **LOOP DESIGN.** End connects seamlessly back to the start (visual + audio) so it can loop; reward a 2nd watch with one detail. Goal: >100% "viewed." Verify: last frame → first frame is a clean visual/audio match.
6. **MUTED-FIRST.** Big, bold, speech-synced captions always (most watch muted). A visual PATTERN-INTERRUPT every 1–2s (cut / punch-zoom / new image / AE beat) so no swipe window opens. Verify: no static hold > ~2s; captions legible at phone size.
7. **FACES + EMOTION + MOTION.** A dramatized (illustrative, non-real) emotive face and/or motion in the key beats — never a static slideshow. (Same likeness firewall as thumbnails: AI-generated non-real characters, never photoreal likeness of the real people.) Verify: at least the hook + payoff carry a face/emotion or strong motion.
8. **FRANCHISE THE WINNING FORMAT.** When a hook/format hits, REPEAT it with a new case (Law By Mike's move: same template, swap the scenario). Build shorts as a recognizable series, not one-offs. Verify: the short fits a named repeatable format (e.g. "Police can legally do THIS", "They were innocent — and the law said ___").
9. **SUB-CONVERSION MECHANICS** (our shorts historically converted 0 subs — this is the fix): (a) a spoken + on-screen CTA ("follow for the cases they don't teach you"); (b) a consistent recognizable persona/brand so viewers crave more; (c) a short→long FUNNEL ("full case on the channel" cliffhanger); (d) pinned comment + endcard. Verify: CTA present, funnel line present, branding consistent.
10. **ANONYMOUS PERSONA (② "within means").** One consistent narrator identity across all shorts — the "Brian" voice + a fixed illustrative narrator character/mark + fixed kinetic-caption style — for parasocial recognizability without a real host. Verify: persona voice + visual signature present and identical to prior shorts.
11. **CROSS-PLATFORM (⑥).** Export every short as YouTube Shorts + TikTok + Reels (1080×1920, ≤60s, safe margins for each platform's UI). Test hooks on TikTok (fastest new-account reach); port winners. Verify: 3 platform exports produced; captions clear of each UI's overlay zones.
12. **RETENTION-GRAPH ITERATION (⑦ breakout-hunting).** After publish, read each short's retention/swipe-away graph; fix the exact moment people leave on the next short. Optimize for variance (one breakout = 10x), not average. Verify: per-short retention logged; the biggest drop-off is the next iteration's target.

---

## BUILD INTEGRATION (our actual pipeline)
- Base: Remotion vertical 1080×1920 @30fps (the short50/51 pipeline) + AE hero-beats (`build_shorts_hero_cards.py`, vertical) + coverfirst (`composite_shorts_hero.py`) + Brian TTS + `build_short_mix.py` (-14 LUFS).
- **Changes to bake in going forward:** (a) a HOOK block = first 1s designed as the cover + first line (packaging-first); (b) enforce a pattern-interrupt cadence (cut/zoom/AE ≤2s) in the timing file; (c) a LOOP tail that matches the head; (d) a standard CTA + funnel outro card + persona mark; (e) three platform exports (yt/tt/reels) with UI-safe caption zones; (f) length target 20–40s (tighten scripts).
- **Trend-jack (④) fast track:** a stripped rapid-response variant of this spec for same-day breaking-case shorts (trend radar surfaces the topic → this template turns it around fast).

## AD-SAFETY & LIKENESS
Illustrative non-real faces only (no photoreal likeness of real defendants/victims, esp. living). No gore/nudity. Accurate to the case. AI-disclosure per channel standard.

## VERIFICATION (before scheduling any short)
Run the 12-rule checklist above + the standing checks: runtime ≤60s, captions legible at phone size, VO synced, cover-first baked, no static >2s, CTA+funnel present, 3 platform exports, persona consistent. Then per-short retention is logged post-publish to drive the next iteration.
