# PD-2026-004-ftx — Midjourney Prompts + SDXL Coverage Plan (v001)

Source script: `03_script/script.en.v002.md`. Policy: `04_scenes/motion_policy.v001.md`.
Goal (owner): **many images** (target ~160–200 final shots), **MJ = hero / best frames**, then
**SDXL mass-produces coverage at max quality**, **true animation ≤10%**, but **every still moves**
(no slideshow). All people = **anonymous silhouettes, no real likeness** (R2).

---

## GLOBAL STYLE (paste into every MJ prompt)

**Look:** photoreal cinematic documentary, modern fintech noir. Restrained and natural — NOT glossy
AI fantasy (see [[feedback_video_natural_style]]). Moody, low-key lighting, real-camera feel, subtle
film grain, shallow depth of field, volumetric haze.

**Palette:** near-black / deep charcoal base, cold teal shadows, one hot accent — **acid green** (the
"code/money" color) or **gold** (wealth) — used sparingly.

**MJ suffix (append to each prompt):**
`--ar 16:9 --style raw --v 6.1 --sref [BRAND_SREF] --no text, watermark, logo, cartoon, 3d render, cgi, oversaturated, hdr, fantasy aurora, deformed, recognizable face, real person likeness`

**Brand consistency:** owner sets one `[BRAND_SREF]` from the best hero render, then reuses it on all
prompts so MJ + SDXL coverage match. Hero shots get extra MJ iterations; coverage goes to SDXL.

**SDXL coverage (after MJ heroes approved):** RealVisXL (photoreal) or JuggernautXL, MAX quality
(hero-grade high steps; Lightning steps 7–8/cfg2/DPM++ SDE Karras for bulk), negative:
`cgi, 3d, cartoon, oversaturated, hdr, fantasy, text, watermark, extra fingers, deformed face`, then
**R-ESRGAN upscale → 1080p+ supersample**, restrained grade + grain. Match the hero palette/lens.

**Tiers:** **R** = true animation (Runway/SVD, key beats, ≤10% total). **M** = moving still
(Ken Burns / 2.5D parallax / drifting light — the default). **K** = motion graphics (numbers, timeline, code, maps).

---

## SHOT MAP (by script beat)

> Each block = one beat. "Heroes" are MJ must-be-perfect frames; "SDXL coverage" lists extra angles/
> inserts to generate for volume. Target counts add up to ~170 shots.

### 00 — FLASH-FORWARD HOOK (0:00–0:10) — "3 a.m., the app, withdraw"  | target ~8 shots
- **H1 [R]** Extreme close-up of a phone screen in the dark, a single large glowing balance number reflected in a tired eye; bedroom black around it. *Prompt:* `extreme close-up of a smartphone screen glowing in a pitch-black bedroom at 3am, a large bank-balance number reflected in a person's tired eye, cold blue screen light, cinematic, shallow focus, film grain` + suffix. *Motion: Runway — finger taps "withdraw", spinner spins, freezes.*
- **H2 [R]** The word/spinner "Processing…" then frozen. *Prompt:* `macro shot of a mobile app loading spinner frozen mid-spin, "withdraw" button greyed out, ultra dark UI, ominous` + suffix.
- **SDXL coverage [M]:** silhouette of a person sitting on a bed edge lit only by phone; close-up of thumb hovering over a button; wide dark bedroom; clock reading 3:00. (~4 inserts)

### 01 — COLD OPEN (0:10–0:45) — "not hacked; the money was already spent" | target ~10
- **H3 [R]** A glowing line of code dissolving into streaming coins flowing OUT of a vault door. *Prompt:* `a single glowing line of green code stretching across darkness, dissolving into a stream of golden coins flowing out through a heavy vault door, symbolic, cinematic, volumetric light` + suffix. *Motion: Runway — coins flow out, vault empties.*
- **H4 [K]** Huge number `$8,000,000,000` half-dissolving into particles. *Motion graphics.*
- **SDXL coverage [M]:** a million tiny silhouettes/crowd dots forming a map of the US; an anonymous hoodie silhouette at a glowing desk (no face); FTX-style abstract brand glow on a stadium (generic, no real logo). (~6)

### 02 — OPENING (0:45–1:35) — "the promise; $26B → 25 years; what's coming" | target ~12
- **H5 [M]** A balance scale: stacks of coins on one side, an empty vault on the other. *Prompt:* `symbolic brass scale in moody light, gold coins piled on one pan, an empty open safe on the other, dark teal background, cinematic` + suffix.
- **K1 [K]** Mini timeline preview: "$26B fortune → Super Bowl → 25 years" as animated chips.
- **SDXL coverage [M]:** vault interior with neat stacks; a phone showing "your funds are safe"; an arena exterior glowing at night (generic); a courtroom door. (~9)

### ACT I — THE MOST TRUSTED MAN (1:35–3:55) — image, two companies | target ~26
- **H6 [M]** Anonymous figure (silhouette/back-of-head only) in rumpled t-shirt & shorts on a beanbag amid suits. *Prompt:* `silhouette of a young man in a wrinkled t-shirt and shorts slouched on a beanbag chair, surrounded by sharply dressed executives in a glass boardroom, faceless, backlit, cinematic documentary` + suffix.
- **H7 [M]** Same figure's hands on a game controller / glowing game screen during a meeting. *Prompt:* `close-up of hands holding a game controller under a boardroom table, a video game glowing on a laptop during a serious meeting, faceless, moody` + suffix.
- **H8 [R]** Money "pouring in" — rivers of light/coins flowing toward a glowing building. *Motion: Runway.*
- **H9 [M]** Two glass towers labeled by motif (exchange vs hedge-fund), a WALL between them. *Prompt:* `two modern glass office towers at night separated by a tall solid wall, one calm and orderly, one full of frantic glowing screens, symbolic split, cinematic` + suffix.
- **H10 [M]** A doorway cut into that wall, faint light leaking through. *Prompt:* `a secret door cut into a thick concrete wall between two buildings, thin acid-green light leaking from its edges, ominous, photoreal` + suffix.
- **SDXL coverage [M/K]:** Super Bowl TV glowing in a living room; arena with generic brand glow; athletes' silhouettes endorsing; crowd of customer silhouettes; trading desks full of screens; beanbag office; "world-saving / charity" symbolic imagery (globe, donation); stacks of cash; a magazine cover mockup with a faceless figure (no real face/text). (~17)

### ACT II — THE LINE OF CODE (3:55–6:35) — the backdoor, "it's theft", the victim | target ~30
- **H11 [K]** The literal code reveal: dark IDE, one line highlighted `allow_negative = true`, acid-green glow. *Motion graphics — line types in / highlights.*
- **H12 [M]** Normal customer blocked: a glowing wall/barrier stops a coin at "zero". *Prompt:* `a glowing red barrier stopping a single coin at a line marked zero, dark fintech interface, symbolic, cinematic` + suffix.
- **H13 [R]** The exception: ONE channel where coins keep flowing past zero into a private vault. *Motion: Runway — coins stream through the open gate.*
- **H14 [M]** A "secret tap/pipe" running from a customer-deposit pool into a hedge-fund room. *Prompt:* `a hidden pipe siphoning glowing liquid gold from a large reservoir labeled with crowd silhouettes into a private gambling room, symbolic, dark, cinematic` + suffix.
- **H15 [M] — VICTIM BEAT (illustrative).** A nurse/teenager silhouette looking at a phone balance = "down payment". *Prompt:* `silhouette of an ordinary person in scrubs looking hopefully at a phone showing a savings balance, warm small apartment, intimate, faceless, cinematic` + suffix. *Then the balance turns to a faint ghost number.* *Motion: M (push-in) → tiny R flicker as number fades.*
- **H16 [K] — QUOTE CARD.** Stark text moment for "It isn't 'crypto.' It's theft." (typographic, on black, restrained). *Motion graphics.*
- **SDXL coverage [M/K]:** rows of server racks; a single blinking server; coins as a flowing river; "house down payment" imagery (keys, small house); empty wallet; ghostly fading numbers; gambling/poker-chips-as-bets motif; a dark control room. (~14)

### ACT III — THE WEEK IT CAME DUE (6:35–8:55) — the run, $16B→0, the crater | target ~28
- **H17 [R] — THE RUN (key beat).** A surging crowd of silhouettes rushing a glowing bank/exchange gate. *Prompt:* `a huge crowd of faceless silhouettes surging toward the glowing doors of a modern bank at night, panic, dramatic backlight, cinematic` + suffix. *Motion: Runway — crowd surges.*
- **H18 [R] — BALANCES DRAINING.** A wall of account numbers all ticking down to zero. *Motion: Runway/graphics — numbers cascade to 0.*
- **H19 [K] — $16B → $0 in a day.** A net-worth line graph crashing vertically; ticking counter. *Motion graphics.*
- **H20 [M] — THE CRATER.** A literal crater/hole where stacks of money used to be. *Prompt:* `an enormous dark crater in the ground where stacks of gold once stood, a few coins glinting at the rim, somber, cinematic wide shot` + suffix.
- **SDXL coverage [M/K]:** "bankruptcy" filing papers; news chyrons (generic, no real text); empty trading floor; rival pulling support (two logos-as-shapes turning away); the $8B / $1.7B / $1.3B figures as motion chips; clawback/recovery imagery (coins slowly returning) for the honesty beat; an arena with the name being removed/scrubbed. (~20)

### ACT IV — THE VERDICT (8:55–10:55) — trial, insiders, guilty x7, sentence | target ~24
- **H21 [M]** Federal courthouse exterior, cold dawn, columns, flag. *Prompt:* `imposing federal courthouse exterior at cold dawn, stone columns, long shadows, a single flag, somber documentary, cinematic` + suffix.
- **H22 [M]** Empty witness chair under a hard light (the inner circle testifies). *Prompt:* `an empty wooden witness stand under a single hard overhead light in a dim courtroom, dust in the beam, tense, photoreal` + suffix.
- **H23 [R] — VERDICT.** A gavel coming down / "GUILTY" weight; jury box silhouettes. *Motion: Runway — gavel strike, hold.*
- **H24 [K] — 7 COUNTS.** Seven count-labels stamping "GUILTY" one by one. *Motion graphics.*
- **H25 [M]** A prison door / number replacing a magazine cover; "25 years". *Prompt:* `a heavy steel prison door slowly closing, a faded magazine cover of a faceless figure dissolving into it, symbolic fall from grace, cinematic` + suffix.
- **SDXL coverage [M/K]:** courtroom benches; scales of justice; "115 years max" vs "25 years" chips; $11B forfeiture stamp; the arena name being unbolted; gavel close-ups; judge's bench (empty, no person). (~16)

### ENDING — LESSON / QUESTION / TEASE (10:55–12:00) | target ~16
- **H26 [M]** "Not your keys, not your coins" — a key and a coin, one hand closing. *Prompt:* `a single brass key and a gold coin resting on dark velvet, one hand reaching to close over them protectively, intimate, cinematic` + suffix.
- **H27 [K] — COMMENT DRIVER.** "25 years — too much, too little, just right?" poll-style card. *Motion graphics.*
- **H28 [M] — TEASE.** A pre-computer-age fraud motif (old ledger, candlelight, ink). *Prompt:* `an antique accounting ledger and quill by candlelight on a dark wood desk, a hidden false entry, 19th-century fraud, warm cinematic` + suffix.
- **End card / disclaimer plate [K]:** branded end-card + AI-disclosure + "not financial/legal advice" lower-third; subscribe motif.
- **SDXL coverage [M/K]:** recap montage stills (reuse motifs: door, code, crater, gavel); subscribe button motif; channel branding. (~12)

---

## TIER TALLY (enforces ≤10% animation)
- **Tier R (true animation):** H1, H2, H3, H8, H13, H15(flicker), H17, H18, H23 + ~3 SVD = **~13–15 shots**.
- Total target ~170 → animation ≈ **8–9%** ✅ within the 10% cap.
- Everything else = **Tier M (moving still)** or **Tier K (motion graphics)** — all in motion, no slideshow.

## PRODUCTION ORDER
1. Owner generates **MJ heroes (H1–H28)**, picks the best, locks `[BRAND_SREF]`.
2. **SDXL** mass-produces the coverage lists at max quality, matched to the hero look → R-ESRGAN → 1080p.
3. Promote only the tagged **Tier R** shots to Runway/SVD; everything else gets Ken Burns / 2.5D parallax.
4. Assemble to the locked 12:00 narration; force-align captions (APR-0002).
