# 0004 — Episode quality standard v2 (raise the bar from PD-2026-002)

Status: **accepted** (owner direction 2026-06-14)
Applies from **PD-2026-002 onward** (channel 1). The Pino channel (0003) adopts a Shorts/long
variant of the same layers. **PD-2026-001 (Miranda) stays as-is** (immutable; already approved).

Goal: every episode after #1 is **several times higher quality** than the first — in content *and*
production — by locking structure and assets up front and enforcing density/motion/sound minimums.

## A. Lock-before-generate (process)

Decide and approve the **structure + shot list + asset list BEFORE generating** heavy media:
`thesis → outline → script → storyboard/shotlist → asset plan → (animatic) → generate → assemble`.
This prevents rework and is the "固めてから進める" the owner asked for. Owner gate at script and at
first-cut (rule 16) unchanged.

## B. Structure (12-min target; same for Pino long-form)

- **Hook / cold open — ~0:00–0:08 (5–8s).** **Flash-forward:** pull the single most dramatic
  moment from *later* in the episode — the climax/twist visual + a punchy line — and show it as a
  cold-open teaser, then rewind to start the story. Land the grab in the first 5 seconds. **Tease,
  don't resolve** (keep the open loop). Reuses footage already in the cut = no extra asset cost.
  Never open on a static text-only card; it moves from frame one.
- **Opening — ~0:08–1:00.** The **first explanation**: thesis + the context the viewer needs +
  viewer promise ("what you'll learn") + ≤3s brand. Into the body inside the first minute.
- **Body — ~9–10 min, 4 acts.** Chronological/causal. Each act: setup → detail → insight, ending on
  a **mini-cliffhanger / open loop** that pulls to the next.
- **Ending — last ~1 min.** Payoff (the hidden system) → tight recap → CTA + **genuine next-episode
  tease** (0002 §K).

> Flow the owner wants: **a 5–8s hook, then the opening carries the first explanation**, then body,
> then ending. Length locked at **12 min**. (PD-2026-001's longer 20s cold open stays as-is.)

## C. Visual density & motion (the core upgrade)

- **No static slides. Every shot moves** — real B-roll, an AI motion clip, strong Ken-Burns/parallax
  on a *detailed* still, or an animated Remotion graphic. A still that only sits = defect.
- **A visual change every ~4–8s** (new shot or major motion) → ≈ 90–150 shots for 12 min.
- **More images:** target **2–4 distinct visuals per scene** (not one card per paragraph).
- **Source priority per shot:** real PD footage (where it exists) → AI **motion clip** for hero beats
  (Runway / Midjourney-animate) → AI still **with** motion → Remotion graphic (data/typography).
- **Several hero motion clips per episode** for the biggest beats.
- Maps, diagrams, timelines **animate** (draw-on, travel, pulse) — never static.

**Rhythm & transitions:**
- Vary cut length: mostly 4–8s, but **punctuate key beats with a 0.5–1s full-frame "punch" insert**
  (a number, a name, a reveal image) + an SFX hit — for emphasis and rhythm. Don't keep a uniform
  pace; variation holds attention.
- Use a **small, consistent set of transitions tied to meaning**: whoosh/whip + SFX on a topic
  change, ink-dip on an act break, match-cut to connect ideas, quick punch-in for emphasis.
- **Restraint = premium.** No random fancy effects; overused/decorative transitions read amateur.

## D. Real-asset-first inserts (decision §L)

Insert **real public-domain audio and video** wherever it exists (oral-argument audio, newsreels,
documents, portraits) — it raises credibility and is genuine evidence. AI symbolic reconstruction
only for what was never recorded, always labelled (invariant 11). Every real asset rights-gated (§N).

## E. Sound — four layers, always on

1. **Narration (VO)** — top, always intelligible.
2. **Music bed** — per the audio cue sheet, ducked ~3–4 dB under VO.
3. **Ambience / room tone** — **continuous; the episode is never silent.** Tenser drone in tension
   scenes.
4. **SFX** — on **every transition** and **every on-screen-text reveal**, plus impacts/risers on
   beats. Mix: VO 0 ref · music −18…−22 LUFS · ambience ≈ −30 · master ≈ −14 LUFS.

## E2. Abundance floors (owner: use these heavily — "バンバン")

Minimums per 12-min episode. These are floors, not targets; richer is better. QC flags shortfalls.

- **Real PD inserts:** ≥ **8–12** distinct real footage/audio moments **where real material exists**
  (newsreel B-roll, oral-argument audio, documents, portraits). Use them liberally; AI only fills
  what was never recorded.
- **AI motion clips (hero shots):** ≥ **6–10** (Runway / Midjourney-animate) on the biggest beats.
- **Animated graphics:** every data / number / list / map / timeline / quote is animated, not static.
- **SFX cues:** ≥ **one per transition + one per on-screen-text reveal** → realistically **60–100+**
  cues across the episode; plus impacts/risers on key beats.
- **Ambience:** **100% coverage** — a bed under every second; never a silent frame.
- **Distinct shots:** ≥ **90–150** (a visual change every 4–8s, per §C).

## F. Content bar

- Deeper research, more sources, **one sharp thesis**, several **surprising but verified** facts.
- Readability: channel 1 grade 7–8, Pino grade 6–7; short sentences, concrete, jargon explained
  inline (§J).
- Retention structure: open loops, act cliffhangers, payoff at the end; honest next-episode thread.

## G. Quality gates (QC enforces C–F; flagged issues block first-cut pass)

- **Motion coverage:** flag any shot static beyond ~4s with no camera/parallax/animation.
- **Visual density:** shots-per-minute ≥ threshold; flag scenes with a single static visual.
- **Audio layers present:** VO + music + ambience + SFX all on the timeline; no silent gaps.
- **Real-asset usage:** real PD inserts used where available (not all-AI when real exists).
- **Citations:** every on-screen/spoken claim backed by a graded, cited claim (§N).
- BAN-avoidance checklist (§N) + rights manifest complete before publish.

## H. Binds

`documentary-writer` (structure, hooks, readability), `visual-director` (density, motion, source
priority, storyboard), `edit-engineer` (assembly, motion, four-layer mix), `audio-director` (VO,
music, ambience, SFX, mix), `research-director`/`rights-editor` (real PD assets + rights), `pd-qc`
(gates §G). Speed comes from reusing the libraries built in episode 1, not from lowering this bar.
