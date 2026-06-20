# PRIME DOCUMENTARY — EPISODE PLAN HANDOFF (EP6–EP8)

Status: READY FOR CODEX. Author: planning/structure pass (Claude). Owner gates still apply.
Do NOT publish, run paid APIs, or generate paid assets from this file. This is a plan, not an approval.

## 0. GLOBAL DECISIONS
- Channel: Prime Documentary (English, US court cases). Continues episodes 1–5.
- Slate (LOCKED; EP7 owner-override note in §5):
    - EP6 = Terry v. Ohio (1968)            — being stopped & frisked on the street
    - EP7 = Riley v. California (2014)       — searching the phone in your pocket
    - EP8 = Carpenter v. United States (2018) — tracking your phone's location
- Macro thesis of the trilogy: "How much can the state see of you — your body, your phone, your
  movements — and where is the line today?"
- FRAMING RULE (non-negotiable): every episode OPENS in the present tense, with the viewer's own
  body/phone/street. The court case is the ORIGIN STORY, never "a history lesson." Past tense is
  for the case events only.
- Why this slate (goal alignment): all three map onto live US anxieties (police stops / "know your
  rights", phone search, location tracking & data privacy); all recognizable, evergreen,
  advertiser-safe, non-partisan, low ban-risk. Avoids news-cycle decay.
- Format spec (match EP1 Miranda / EP2 Gideon):
    - ~12:00 runtime, ~1,650–1,850 narration words @ ~150 wpm, grade 7–8 readability.
    - Structure: HOOK (promise + payoff seeds) → OPENING (promise of the episode) → 4 ACTS →
      ENDING (next-episode tease).
    - Mark narration with [VO:]. Tag every load-bearing fact to a claim ID [CLM-xxxx]. Keep
      production notes OUT of narration text.
    - Obey docs/05 (style/anti-AI-filler), rules/09 (claims), docs/13 (rights/safety).
- Series threading: EP5 (Madoff) closes the fraud cluster; EP6 opens the "state vs. you" cluster.
  EP6→7→8 each end on a genuine tease into the next (street → phone contents → phone location).

## 0A. TOOLCHAIN & ASSET SOURCES (owner-approved 2026-06-20; authoritative for EP6–8)
- Research: CourtListener API (token required) + primary/strong secondary sources → claim ledger.
- Script: pd-script (LLM), schema-validated, claim-linked.
- IMAGES: **Codex image generation = PRIMARY.** Midjourney is DROPPED (no quality gain; manual).
  Local SDXL / SVD / AnimateDiff allowed for free local bulk + variants only. ALL images, whatever
  the source, MUST: (1) be disclosed as AI-generated; (2) be registered in the rights manifest
  (origin / creator / license / verified_at); (3) contain NO real-person likeness or deepfake
  (invariant 11); (4) match PD brand (palette/spec in remotion/src/brand.ts).
- Motion / on-screen graphics: Remotion (parallax, data, typography); Runway optional for AI motion.
- Narration: ElevenLabs (master). PAID → owner approval + idempotency + budget check.
- Music / SFX: Suno reuse library (rights-tracked); no new paid generation assumed.
- Edit & render: **Remotion + FFmpeg** (owner-confirmed 2026-06-20). NOT DaVinci. Render CPU/libx264,
  quality-first.
- Thumbnail: Remotion.
- Publish: YouTube, private upload first; public scheduling = gate.
- Heavy media (images/video/audio/renders) → H:\pd-media (git-ignored). Repo holds the "brain" only.
- RECONCILED: CLAUDE.md §11 updated 2026-06-20 (edit = Remotion+FFmpeg, images = Codex), explicitly
  superseding earlier DaVinci/Midjourney references in docs/ and decisions/. (decisions/0002 & 0007
  prose not yet rewritten, but are overridden by CLAUDE.md §11 — the top source-of-truth.)

## 1. DIVISION OF LABOR (Claude ↔ Codex)
Strength-based split (owner-set):
- **CLAUDE owns the LEFT side**: topic, research + claim ledger, thesis, outline, and the FINISHED
  SCRIPT. Codex must NOT write or rewrite scripts.
- **CODEX owns the RIGHT side**: scenes → visual assets (image generation) → narration audio →
  music → motion → edit → render.

### 1A. CLAUDE — script status (this is Claude's deliverable, not Codex's)
- EP6–8 scripts: written, fact-checked (§7), owner content-approved (§8). Claude finishes the
  formal grounding (CLM placeholders → cited claim ledger) + final polish → script.en.v001.md.
- Codex consumes these as the authoritative, locked input. Do not regenerate them.

### 1B. CODEX — START HERE (per episode, EP6 first), using Claude's finished script
1. pd-new-episode → workspace/manifest/IDs PD-2026-006/007/008 (if not already created).
2. pd-scenes → convert the finished script into scene / shot / visual / on-screen-text plans
   (continuity + generation specs). Use the ACT STRUCTURE + visual notes below.
3. pd-generate-assets → generate images: **Codex (primary)**, SDXL/SVD for bulk variants. Every
   image: AI-disclosed, rights-manifest registered, brand-consistent, NO real-person likeness.
4. audio = ElevenLabs narration (PAID → owner approval + budget) ; music = Suno reuse library ;
   motion/graphics = Remotion.
5. pd-build-edit → assemble & render in **Remotion + FFmpeg** (CPU/libx264, quality-first); QC.
6. STOP at the first-cut gate and the title/thumbnail gate (owner approval). No publish without
   approval (CLAUDE.md §3, rules/16).
- Constraints: respect guard_destructive / check_secrets hooks; commit each step; no paid ops or
  publish without approval; real people by role, neutral; all synthetic visuals disclosed.

## 2. EP6 — Terry v. Ohio (1968)  [risk_class: R2]
- Logline: A cop can stop you on the street and pat you down with no warrant and no proof of a
  crime — the 1968 case that drew the line between a hunch and proof.
- Working titles (test 3–5): "A Cop Can Search You Without a Warrant — Here's the Catch" /
  "When Can the Police Actually Stop You?" / "The Hunch That Rewrote Street Policing"
- Thesis: Most people assume police need real evidence to stop and search you. Understanding Terry
  reveals they only need "reasonable suspicion" — a lower, blurrier standard that governs millions
  of street stops today.
- Why now: "know your rights" / police-encounter content is one of the largest live genres; this is
  the legal floor under all of it.
- HOOK promise→payoff (body MUST pay off):
    (a) "stopped & frisked, no warrant, no crime seen" → Act III (the ruling allows it).
    (b) "it began with one detective watching two men pace a sidewalk" → Act I (McFadden).
    (c) "the line between a hunch and proof" → Act III ("reasonable suspicion") + Act IV (cost).
- ACT STRUCTURE (function | target | key claims to verify):
    - ACT I  The street  | 1:15–3:30 | Cleveland Oct 1963; Det. McFadden (veteran); two men
      repeatedly cased a store window; pat-down of outer clothing; pistols recovered.
    - ACT II The problem | 3:30–6:15 | 4th Amdt "unreasonable searches & seizures"; usual standard
      = probable cause/warrant; McFadden had neither; officer-safety vs warrant-rule tension;
      links to EP3 (exclusionary rule).
    - ACT III The ruling | 6:15–9:00 | 1968, 8–1, Chief Justice Earl Warren; new standard
      "reasonable suspicion" (< probable cause); frisk limited to weapons, outer clothing;
      stop=seizure, frisk=search but reasonable; Justice Douglas sole dissent.
    - ACT IV The cost  | 9:00–10:45 | "Terry stop" ubiquitous; reasonable suspicion depends on
      judgment → bias risk; later stop-and-frisk controversy (NEUTRAL; documented debate, not
      accusation; no city/era stated as fact unless grounded).
- ENDING tease (10:45–12:00): all of this depended on being out in the open. What about something
  you try to keep private even in public — words in a closed phone booth, or the phone in your
  pocket? → EP7.
- Packaging/thumbnail: present-tense POV of a street stop (symbolic reconstruction, AI-disclosed);
  bold question text; PD brand palette (black/navy/electric-blue/gold).
- Safety: neutral educational tone; neither anti- nor pro-police framing.

## 3. EP7 — Riley v. California (2014)  [risk_class: R2]
- Logline: When police arrest you, can they go through your phone? In 2014 the Supreme Court said
  no — not without a warrant.
- Working titles: "Can the Police Search Your Phone?" / "The Phone in Your Pocket Has Rights" /
  "Arrested — Can They Read Your Texts?"
- Thesis: People assume that once you're arrested, everything on you is fair game. Riley reveals the
  Court treats a modern smartphone as different in kind — a window into your whole life that needs
  its own warrant.
- Why now: the most relatable privacy question — everyone carries a phone; "can a cop go through
  it?" is constant. Unanimous ruling = clean, advertiser-safe.
- Weave-in (replaces a standalone Katz episode): one chapter on the older principle "the 4th
  Amendment protects people, not places" (Katz v. US, 1967, phone booth; "reasonable expectation of
  privacy") as the intellectual root that makes Riley possible.
- HOOK promise→payoff:
    (a) "arrested — they reach for your phone" → Act III (warrant required).
    (b) "the Court called the phone different from anything in your pockets" → Act III.
- ACT STRUCTURE (function | claims to verify):
    - ACT I  The arrest & the phone | everyday stakes; search-incident-to-arrest doctrine.
    - ACT II The old rule vs the device | search-incident-to-arrest justifications (officer safety,
      evidence preservation); why a phone breaks them (data ≠ a cigarette pack).
    - ACT III The ruling | 2014, 9–0, Chief Justice Roberts; phones hold "the privacies of life";
      "get a warrant"; the Katz "people, not places" lineage (Stewart majority; Harlan concurrence
      = reasonable-expectation test).
    - ACT IV What it means | encryption, cloud, everything-on-one-device; limits (exigent
      circumstances exception).
- ENDING tease: Riley protects what's INSIDE the phone. But the phone also quietly records
  something you never typed — everywhere you've been. Who owns that trail? → EP8 Carpenter.
- CLAIMS TO LOCK: Riley v. California 2014, unanimous; consolidated with US v. Wurie; holding =
  warrant generally required to search a cell phone seized incident to arrest; Roberts opinion;
  Katz 1967 (Stewart majority; Harlan concurrence).
- Safety: R2; neutral; real defendants by role.

## 4. EP8 — Carpenter v. United States (2018)  [risk_class: R2]
- Logline: Your phone logs where you are every few minutes and hands it to your carrier. In 2018 the
  Court decided the police generally need a warrant to get that map.
- Working titles: "Your Phone Is Tracking You — and the Police Wanted the Map" / "127 Days of Your
  Location, Without a Warrant" / "The Case That Brought Privacy Into the Smartphone Age"
- Thesis: We assume anything we 'share' with a company loses its privacy. Carpenter reveals that a
  record you can't avoid creating — your constant location — is too revealing to lose that
  protection automatically.
- Why now: peak relevance — data brokers, location selling, surveillance, AI. Strongest "this is
  you, right now" payoff and the trilogy's climax.
- HOOK promise→payoff:
    (a) "127 days of location records, no warrant" → Act I/III.
    (b) "who does that trail belong to?" → Act III (warrant generally required).
- ACT STRUCTURE (function | claims to verify):
    - ACT I  The trail | Detroit-area robberies 2010–11; co-suspect gave numbers; FBI obtained
      Carpenter's cell-site location info (CSLI), ~127 days / ~12,900 points; placed near
      robberies; convicted, 100+ yr sentence; obtained WITHOUT a warrant via the Stored
      Communications Act (lower standard).
    - ACT II The third-party doctrine | 1970s cases (Smith v. Maryland — dialed numbers; US v.
      Miller — bank records): share with a third party → lose reasonable expectation of privacy;
      why CSLI differs in kind (continuous, involuntary, comprehensive).
    - ACT III The line | 2018, 5–4, Chief Justice Roberts; accessing historical CSLI = a search;
      warrant generally required; did NOT overturn the third-party doctrine, refused to EXTEND it;
      dissents (Kennedy, Thomas, Alito, Gorsuch) warn the line is vague / a job for legislatures.
    - ACT IV What it means for you | location is one of many trails (searches, purchases, messages);
      Carpenter cracked the doctrine for location only; open questions remain.
- ENDING (series capstone): three episodes, one question — body (Terry), phone contents (Riley),
  phone location (Carpenter). The Constitution is improvising against machines its authors never
  imagined; the line runs through the device in your hand.
- Safety: R2; Carpenter is a convicted person on public record — describe neutrally, factual; no
  editorializing on guilt beyond the record.

## 5. OPEN DECISION FOR OWNER
- EP7: Riley (2014, LOCKED — max current relevance) vs Katz (1967, more elegant legal lineage but
  dated framing). If owner switches to Katz: move the Katz chapter out of EP7, make it the
  standalone EP7, keep Carpenter as EP8.

## 6. REFERENCE (all committed to Git — Codex can read these directly)
- Seed narration drafts (structural reference only; [CLM-xxxx] are placeholders — re-ground every
  fact via pd-research before any becomes script.en.v001.md):
    - episodes/_planning/seeds/EP6_terry.seed.en.md
    - episodes/_planning/seeds/EP7_riley.seed.en.md
    - episodes/_planning/seeds/EP8_carpenter.seed.en.md
- House format examples: episodes/PD-2026-001-miranda/03_script/script.en.v001.md ;
  episodes/PD-2026-002-gideon/03_script/script.en.v001.md

## 7. FACT VERIFICATION LOG (checked 2026-06-20 vs primary/authoritative web sources)
Load-bearing facts of all three cases were fact-checked BEFORE handoff; corrections already applied
to the seed drafts. pd-research must still register these into the claim ledger (claims.vNNN.json)
and assign real CLM ids — but the facts below are confirmed.
- EP6 Terry v. Ohio — 392 U.S. 1, decided 1968-06-10; 8–1; Warren; sole dissent Douglas. Cleveland,
  1963-10-31; Det. McFadden (39 yrs on force / 35 as detective). CORRECTION applied: the two men
  cased the window "about a dozen trips total (~5–6 each)", not "more than a dozen." Holding
  (reasonable suspicion + weapons frisk) verified.
  Sources: https://www.law.cornell.edu/supremecourt/text/392/1 ; https://api.oyez.org/cases/1967/67
- EP7 Riley v. California — 573 U.S. 373, decided 2014-06-25; 9–0 in the RESULT (Roberts; Alito
  concurred in part & in the judgment — not unanimous in reasoning); companion United States v.
  Wurie; "get a warrant"; Chimel rationales; exigency exception preserved. CORRECTION applied:
  "every justice agreed" → "not one justice dissented" (precise).
  Sources: https://www.law.cornell.edu/supremecourt/text/13-132 ; https://supreme.justia.com/cases/federal/us/573/373
- EP8 Carpenter v. United States — 585 U.S. 296 / 138 S.Ct. 2206, decided 2018-06-22; 5–4; Roberts;
  dissents Kennedy/Thomas/Alito/Gorsuch. Detroit-area RadioShack/T-Mobile robberies 2010–11; SCA
  §2703(d) "specific and articulable facts" (< probable cause); 127 days / ~12,898 CSLI points;
  sentenced 116 years. Third-party doctrine = Smith v. Maryland (1979) + United States v. Miller
  (1976); NOT overruled, NOT extended. CORRECTIONS applied: "~12,898 points", "116 years".
  Sources: https://www.lawfaremedia.org/article/summary-supreme-court-rules-carpenter-v-united-states ; https://en.wikipedia.org/wiki/Carpenter_v._United_States ; https://www.justice.gov/usao-edmi/pr/cell-phone-store-robber-sentenced-116-years
- WARNING for Codex: a Cornell LII AI-summary misreports Carpenter as "6–3" — IGNORE; the vote is
  5–4 per all primary sources.

## 8. OWNER APPROVAL — content / direction sign-off (2026-06-20)
- The owner approved the EP6–EP8 seed scripts (Terry / Riley / Carpenter) — slate, thesis,
  structure, and narrative content — as fact-verified in §7. Recorded against the seed drafts at the
  commit that adds this line.
- SCOPE: this authorizes Codex to proceed through the pipeline (pd-new-episode → pd-research →
  pd-script) WITHOUT re-confirming topic or direction.
- BINDING GATE (unchanged, per rules/16 + invariant 1): the formal final-script approval still
  targets the exact produced revision episodes/PD-2026-00X/03_script/script.en.v001.md, once the
  [CLM-xxxx] placeholders are entered into the claim ledger as graded, cited claims and script_qc
  passes. This content sign-off carries forward to that revision provided no fact or claim changes
  from the verified seed; any factual change re-opens the gate.
