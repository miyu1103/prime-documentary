# Acceptance gate — PD-2026-002-gideon (run on the FROZEN final cut, before private upload)

Owner's quality bar (2026-06-17): "top quality, **not a slideshow (紙芝居)**, hook/opening/SFX/ending
done right, animation layered on images, captions perfectly synced & comfortable to read, use SDXL/SVD
to move the Midjourney stills where needed — and don't get BANNED, grow views / retention / subs."

This is the pass/fail rubric I (gate) run on the **committed, frozen** cut once the active edit session
finishes. Any **FAIL** blocks private upload until fixed. Maps to decisions 0004/0005/0006 + §N.

## A. No-slideshow / motion (0004 §motion) — the owner's #1 ask
- [ ] **Every shot moves** — no static-over-4s shot anywhere. (verify: frame-sample every scene)
- [ ] **Visual change every 4–8s** (≈90–150 shots over 11–12 min).
- [ ] **Layered animation on every still**: particles/haze + callouts/arrows/highlights + kinetic text +
      **2.5D depth parallax** + focal glow. Never a bare still.
- [ ] **Stills that still read static → animated** via depth-parallax (Remotion, zero-warp default) or
      **SDXL/SVD local motion** (the `svd_*` scripts) then RIFE-smoothed. Subtle, no warping.
- [ ] **Motion diversified** (depth-parallax / MJ-animate / Runway / SVD / Remotion) — not Runway-only.
- [ ] ≥6–10 motion clips; the 19 stored clips + vetted v002 stills available; vetted upgrades applied
      where they beat the in-cut still (see `05_visuals/v002_still_upgrade_map.md`).

## B. Hook / opening / structure / ending (0004 §structure)
- [ ] **Flash-forward hook 5–8s** (preview the climax, don't resolve). [a20d71c added a 5–8s hook]
- [ ] **Opening = first explanation** (thesis + promise, ≤1 min).
- [ ] **4-act body**, each ending on a mini-cliffhanger.
- [ ] **Ending**: payoff + recap + genuine next-episode tease + **end-card**. [a20d71c added end-card]

## C. Sound — four layers ALWAYS (0004 §sound)
- [ ] VO (top) + music bed (−18…−22 LUFS, ducked) + **continuous ambience (100%, never silent)** +
      **SFX on every transition & on-screen-text reveal** (60–100+; current ≈121). Master ≈ −14 LUFS.
- [ ] **Dynamic delivery (抑揚)**: calm baseline → intense at climax/twist; music swells in sync.

## D. Captions — perfect sync + comfortable display (owner's explicit ask)
- [ ] **Word-for-word** the narration.
- [ ] **Frame-accurate, forced-aligned** to TTS timestamps (NOT proportional). [a20d71c = forced-aligned;
      verify against `captions.v003.srt` + the final render; close QC-0007]
- [ ] **Comfortable display**: brand font, subtle scrim, lower safe-area, ~5–8 words, smooth fade; no drift,
      no overlap, readable at 360p on a phone.

## E. BAN-safety (§N) — hard gates, ALL must be green
- [ ] Copyright: PD/licensed only; **rights manifest per asset** (v002 = 97 assets incl. new vetted pool).
- [ ] Music cleared (library reuse, tracked).
- [ ] **AI/synthetic disclosure** in description + **on-screen "symbolic reconstruction" labels** on AI
      reenactment shots (invariant 11). [present]
- [ ] **Not-made-for-kids** set. [set]
- [ ] **No misinformation**: claims cited to 372 U.S. 335 / 316 U.S. 455 + **source live-verification**.
      ⚠️ **OPEN (QC-0008)**: live byte-hash verify is **blocked from this node** (CourtListener 202
      anti-bot; Oyez is JS-rendered). Needs the **CourtListener API adapter + COURTLISTENER_TOKEN**, or an
      owner-side fetch. Do not publish until SRC-0001..0003 carry `content_hash` + `verified_at`.
- [ ] **No legal advice** disclaimer present. [present]
- [ ] Advertiser-safe tone; **title ⇄ thumbnail ⇄ content match** (no clickbait lie — he really won 9–0).
- [ ] No defamation (parties deceased/institutional; facts accurate per claim ledger).

## F. Growth — CTR × AVD × subs (0005/0006)
- [ ] **Packaging-first A/B**: ≥2 thumbnails + 2 titles in Studio Test&Compare. Set ready in
      `youtube_meta` (Concept 2 "Pencil" + Concept 3 "ALONE"; title "He Had No Lawyer…"). **Thumbnails
      still need rendering** via ThumbConcept (backgrounds ready). Vetted `11_thumb_bg` available.
- [ ] **First 30s** obsession: hook lands, promise clear, open loop set.
- [ ] **Chapters** recomputed from the **final** TTS timeline (don't hand-time).
- [ ] End screen (subscribe + next + best-for-viewer) + playlist + **pinned comment** (question to drive
      comments). [set in youtube_meta]
- [ ] Retention: vary cut length, 0.5–1s punch inserts on key beats, transitions tied to meaning.

## Gate procedure
1. Wait for the active edit session to **commit + freeze** the final cut (working tree clean; new hash).
2. Run A–F on that exact hash; record `qc_report.v00X` (pass/fail per item) + frame/audio evidence.
3. Any FAIL → minimal targeted fix (or precise fix-list to the edit owner) → re-render → re-gate.
4. All green except owner gates → record first-cut APR (delegated) + title/thumbnail APR (delegated, after
   thumbnails render) → **private upload prep** → STOP. Public publish = owner's final GO only.
