# PD-2026-004-ftx — Motion / Asset Policy (owner-directed, updated 2026-06-18)

Owner directives (2026-06-18):
1. **"Runway も使うけど全部はやりすぎ。要所で。"** — paid Runway only at key beats.
2. **"今まで画像の枚数が少なかった"** — far MORE images than past episodes.
3. **"ミッドジャーニーで最高のものを出したらSDXLで増産してもいい"** — MJ = hero/best images;
   then mass-produce coverage with SDXL.
4. **"アニメーションの割合も10パーセント以内でいい"** — true animation ≤ 10% of shots.
5. **"SDXLは使うなら最高品質で"** — if SDXL, max quality.
6. **"絶対に動画にしたい。静止画が多いと白けてちゃっちく感じる"** — it MUST feel like video; a
   static-heavy slideshow feels cheap. (No-slideshow is also the ep QC gate.)

## How we reconcile "≤10% animation" with "must feel like a video"
The bulk are STILLS, but **every still is treated as a moving shot** — so nothing is static, yet
"real animation" stays ≤10%. The slideshow feel comes from frozen frames, not from using stills.

## Shot budget (12:00 episode)
- **High cut rate:** average shot ~3–5s → **target ~160–200 shots** (vs ep3's ~87). Many images.
- **Tier R — true animation, HARD CAP ≤10% (~16–20 shots), key beats only:**
  cold-open number dissolving; Act II the door opening + coins flowing through the glowing
  `allow_negative` line; Act III the run/draining balances; the verdict beat. Runway for the few
  hero motion shots; local SVD (free, 4090) for the rest of this 10%.
- **Tier M — moving stills, the default ~90%:** MJ/SDXL still + **always** one of: slow push-in/
  pull-out (Ken Burns), pan/tilt, **2.5D parallax** (depth-split foreground/background), drifting
  light/particles/dust, plus film grain + subtle handheld micro-jitter. Cinematic, never frozen.
- **Tier K — graphics in motion:** timelines, animated numbers/balance-sheet, maps, code reveal.

## Image production pipeline (quality-first)
- **Midjourney = hero images:** the key, must-look-perfect frames (hook, door reveal, verdict,
  thumbnail). Brand --sref for consistent look. Owner generates these manually.
- **SDXL = volume/coverage at MAX quality:** expand each scene with more angles/inserts/B-roll so we
  hit the high shot count without 200 manual MJ jobs. Use the photoreal stack from
  [[feedback_video_natural_style]]: **RealVisXL** (photoreal; Lightning steps 7–8 / cfg 2 / DPM++ SDE
  Karras for speed, or full RealVisXL at high steps for hero-grade), JuggernautXL as alt. Negative:
  cgi/3d/oversaturated/hdr/fantasy/cartoon. Then **R-ESRGAN upscale → 1080p supersample**, restrained
  grade + film grain. Launch SDXL via venv python (API :7860) per [[reference_sdxl_launch]].
- **Consistency:** SDXL coverage shots must match the MJ hero look (same palette, era, grain, lens
  feel) so the mix is seamless — no obvious "AI filler" look ([[feedback_video_natural_style]]).

## Rules
- All people = anonymous silhouettes (R2 / no real likeness); no real face in any MJ/SDXL/Runway shot.
- Natural, restrained grade; no oversaturated AI look. Symbolic reconstruction only — never presented
  as real footage (invariant 11).
- Per-shot the shotlist tags: source (MJ-hero / SDXL), tier (R/M/K), and motion treatment. The ≤10%
  animation cap is enforced when the shotlist is built.
