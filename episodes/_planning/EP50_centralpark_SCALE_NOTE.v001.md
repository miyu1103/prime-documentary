# EP50 — PRODUCTION-SCALE REALITY CHECK (v001) — read this before committing spend

> Blunt one-pager. EP50 is the channel's first 60-min long-form. It is **~5x a 12-min episode** across every axis. Baseline = EP49 strieff (2,139 words, 720.6s narration, 226 cuts). Do not start the build assuming "a bit longer." It is a different-size machine.

## THE 5x ARITHMETIC (EP49 12-min → EP50 hour-long)

| Axis | EP49 (12-min) | EP50 (target) | Multiple | Source of EP50 number |
|------|--------------:|--------------:|:--------:|-----------------------|
| Script words | 2,139 | **~9,970** | 4.7x | 56.0 min × 178.1 wpm |
| Narration runtime | 720.6 s (12.0 min) | **3,360 s (56.0 min)** | 4.7x | narration target |
| Finished runtime | ~12.4 min | **~56:20** | 4.5x | 8.0 + 3.5 + 3360 + 9 = 3380.5 s |
| Total cuts | 226 | **1,080** | 4.8x | asset split ÷ mean_shot 3.11s |
| Distinct SDXL stills | 85 | **400** | 4.7x | still lane |
| Factory/stock clips | 93 | **450** | 4.8x | factory lane |
| i2v / motion clips | 16 | **80** | 5.0x | motion lane |
| In-film MG beats (floor) | 31 | **140** | 4.5x | ceil(56.0 × 2.5/min) |
| AE hero-cards | ~6–8 | **~22** | ~3x | punctuation, not saturation |
| TTS narration minutes | 12.0 | **56.0** | 4.7x | same voice/pipeline, 5x length |
| Render frames @30fps | ~22,320 | **101,415** | 4.5x | durationInFrames |

## THE THINGS THAT HURT AT 5x (not linear — they bite harder)
- **Render time & frames.** ~101k frames vs ~22k. At the channel's measured throughput this is a multi-hour render, not a coffee-break render. **Check machine state before kicking it off** (MEMORY: heavy-job preflight) and stage `public → public_slim` FIRST — a 5x asset tree copied naively is the EP38 50GB-copy trap all over again, at hour-long scale.
- **public_slim disk.** ~930 distinct assets (400 stills + 450 factory + 80 motion) + overlays + AE renders. Budget disk as **~4–5x** a 12-min ep's slim tree before you start, not when it fails at frame 60k.
- **Asset QC surface.** 1,080 cuts to eyeball. The "declare it done from one frame" failure (MEMORY: EP39–41) is 5x more likely to hide a defect here. **Watch the WHOLE ~56 min** before calling it shipped; measured > estimated.
- **Fact surface.** 35 ledger entries vs ~20; more dates, names, dollar figures, and 8+ hedge-on-screen items (interrogation hours, taped-vs-oral split, Reyes prior-crime specifics, per-person years, per-person $ split, Trump ad cost). The facts gate (`check_centralpark_facts.py`) must carry every one; a wrong number in an hour is still a wrong number.
- **Codex build reliability.** Codex's build phase is systematically buggy at 1x (MEMORY: no narration, empty manifests, bad figure schemas, wrong-case AE deck). At 5x the blast radius is 5x. **Audit + gate every piece before render; never run AE blind.**

## THE RETENTION RISK (the honest part)
Channel analytics (2026-07): **long-form under-retains**; subs come from long-form but **27–36 min videos were killed for weak retention**, and the winning format has been the **12-min second-person 4A**. Going to 56 min is a **bet against our own data.** It only pays off if the *saga* carries it — this is the one topic on the slate with a true multi-year reversal (children convicted on coerced confessions → real attacker's DNA → exoneration → $41M). The hour is earned by STORY, not by stretching a 12-min structure to 5x length. If the script reads like a padded 12-min ep, kill the length, not the retention.

## RECOMMENDED DE-RISK (do all four)
1. **Chaptered YouTube timestamps** — publish the 7 acts as chapters so the audience can navigate an hour; chapters measurably help long-form retention and session time.
2. **Hard per-act hook + open loop** — every act ends on the loop written in `STRUCTURE.v001.md`. No act may end on a resolved beat.
3. **Front-load the engine** — put **Act 2 (The Interrogations)** — the moral gut-punch — early and make it the longest (11 min). Do not save the emotional core for minute 40; the 30-second and 3-minute retention cliffs are where we bleed.
4. **Ship a 12-min cut-down as a companion Short/mid-form** — hedge the bet: a tight 4A version of the same story feeds the format that actually converts subs, and funnels to the hour-long. One script, two runtimes.

**Bottom line:** the assets, render, and disk are a straightforward ~5x and manageable with the standard gates. The *real* cost is retention risk. Green-light the hour only because this specific saga can hold it — and de-risk with chapters, per-act hooks, a front-loaded Act 2, and a companion short.
