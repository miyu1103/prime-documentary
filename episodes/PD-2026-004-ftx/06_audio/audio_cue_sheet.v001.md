# PD-2026-004-ftx — Audio Cue Sheet (v001): Music + SFX + Ambience

Owner directive: **"効果音・背景音・環境音はしっかり入れて"** — rich, deliberate sound design.
Source script: `03_script/script.en.v002.md`. Music = Suno reuse library; SFX/ambience = rights-clear
(owner-owned / licensed library). 4-layer mix like ep3: **narration + music + ambience + SFX**.

## Global mix targets
- **Loudness:** master ≈ **-14 LUFS** (YouTube), true peak ≤ -1 dBTP. (ep3 ran -17; bring up to -14.)
- **Narration always on top:** duck music/ambience **-8 to -12 dB** under VO (sidechain). VO clean,
  de-essed, gentle compression, high-pass ~80Hz.
- **Dynamics for retention:** quiet→loud contrast at act turns; a real **silence beat** before big reveals.
- Stereo width on music/ambience; keep VO centered/mono-safe (mobile speakers).
- No copyrighted tracks; no real news-broadcast audio. Everything rights-clear.

## Music regions (Suno library — emotional arc)
| # | Time | Beat | Music intent |
|---|---|---|---|
| M1 | 0:00–0:45 | Hook + cold open | sparse dark pulse, single sub-bass hit, ticking unease |
| M2 | 0:45–1:35 | Opening | low cinematic bed, rising curiosity, soft pulse |
| M3 | 1:35–3:55 | Act I (trust/image) | warmer, "too good to be true" sheen with a faint minor undertone |
| M4 | 3:55–6:35 | Act II (the code) | cold, precise, mechanical ticking + growing dread as the tap opens |
| M5 | 6:35–8:55 | Act III (the run) | accelerating tension, percussion building, then a hollow drop at "the crater" |
| M6 | 8:55–10:55 | Act IV (verdict) | weighty, courtroom gravity; sparse, then a single resolving low chord on "Guilty" |
| M7 | 10:55–12:00 | Ending | reflective, clean, hopeful-but-sober; lifts slightly on subscribe/tease |
- Music **drops out almost entirely** for ~1s before: "It isn't 'crypto.' It's theft." and before "Guilty."

## Ambience beds (continuous, low, sets place)
- **AMB-1 night bedroom / room tone** under hook (faint fridge hum, distant traffic, 3am stillness).
- **AMB-2 server room** hum/HVAC under Act II code beats.
- **AMB-3 office/trading floor** murmur, keyboards, phones under Act I & Alameda beats.
- **AMB-4 crowd / lobby** rumble under the run (Act III).
- **AMB-5 courtroom** room tone — large, reverberant, cough/paper rustle, under Act IV.
- **AMB-6 quiet room tone** under ending. Keep all beds -20 to -26 dB, ducked under VO.

## SFX hits (spot effects — punchy, sparing, meaningful)
| Cue | Time/beat | SFX |
|---|---|---|
| S1 | hook | phone unlock tap, soft UI tap on "withdraw", loading spinner whir → **dead silence** |
| S2 | cold open | deep sub "whoomp" as vault door motif appears; coin-stream shimmer |
| S3 | $8,000,000,000 | particle "dissolve/sizzle" as the number disintegrates |
| S4 | Act I money pours in | rising "cash whoosh" / coin cascade; camera-shutter clicks (Super Bowl/press) |
| S5 | wall + secret door | low concrete rumble; thin "creak" + acid-green electrical buzz as the door leaks |
| S6 | **code reveal** | mechanical keyboard typing; a single sharp "click/beep" as `allow_negative` highlights |
| S7 | the tap opens | liquid "siphon/gurgle" + coins draining through a gate |
| S8 | victim beat | warm UI chime → it sours into a hollow, detuned tone as the balance fades |
| S9 | "It's theft." | music cut; a single hard low **impact** under the word, then silence |
| S10 | the run | rising crowd murmur → roar; rapid app-error buzzes; alarms swelling |
| S11 | $16B→0 | fast descending "counter" ticks; a final flatline tone |
| S12 | the crater | wind/hollow void tone; a few lonely coin "tinks" at the rim |
| S13 | courthouse | heavy door boom; distant city; flag rope clink |
| S14 | **verdict** | silence → single hard **gavel strike** with deep reverb tail |
| S15 | 7 counts | seven escalating stamp/impact hits, one per count |
| S16 | prison door / 25y | heavy steel door slam + lock clunk; magazine-page flutter dissolving |
| S17 | arena name removed | metal unbolting / scraping |
| S18 | ending "keys/coins" | soft protective hand-close + warm coin tap |
| S19 | comment card | subtle notification "pop" |
| S20 | tease | quill scratch on paper; candle flicker; old clock tick |

## Notes
- Keep SFX **purposeful**, not constant — they should hit emotional/structural moments, not clutter.
- Every animated (Tier R) shot gets a matched SFX; moving stills get ambience + occasional accents.
- Final pass: forced-align captions to the tempo-adjusted narration master (APR-0002), then mix the
  4 layers, then grade loudness to -14 LUFS. QC gate: no-slideshow + 4-layer audio present (like ep3).
