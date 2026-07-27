# SHORTS_SLATE EP53–56 v001 — 13 new Shorts built from assets that already exist

**Created:** 2026-07-28 · **Status:** PLAN ONLY. Nothing rendered, nothing scheduled, no GPU used, no API written.
**Scope:** `short60`–`short72` (13 new Shorts) across EP53 Norfolk Four / EP54 Curtis Flowers / EP55 Jon Burge / EP56 Post Office Horizon.
**Governing method (do NOT invent a new pipeline):** `episodes/_planning/SHORTS_METHOD.v001.md` (the 12 rules) + `SHORTS_REMOTION_SPEC.md` (Short.tsx data contract, safe areas) + `SHORTS_CONVERSION_v001.md` §4 (end CTA) + memory `pd-shorts-pipeline` (English-only, 1/day 12:00 JST, coverfirst, thumb traps).
**Why:** `DEEP_RESEARCH_FINDINGS.v001.md` §Distribution — Shorts are **65.3% of views at 0.16 min/view**; Suggested is **44.5% of watch time at 3.91 min/view**. Shorts buy reach; long-form buys watch-time and subscribers. Historic Shorts converted **0 subscribers** because there was no funnel. Every short below exists to move one person to the long-form.

---

## 0. State of play (measured on disk / on the live channel, 2026-07-28)

### 0.1 What already exists per episode

| Episode | Slug | AI stills on disk | i2v clips | Long-form VO master | Long-form captions | Existing short |
|---|---|---|---|---|---|---|
| EP53 | `PD-2026-053-norfolk` | **250** (S001–S205, M01–M42_src, T01–T03_face) | **none** | ✅ `vc_master_v001.mp3` 1,673.9 s / 304 chunks | ✅ 820 cues | **short57** (scheduled 8/19) |
| EP54 | `PD-2026-054-flowers` | **257** (S001–S210, M01–M44_src, T01–T03_face) | **✅ 44** `M01_rife.mp4`–`M44_rife.mp4`, 1920×1080 @48 fps, ~3.42 s each | ✅ 1,708.6 s / 300 chunks | ✅ 826 cues | **short58** (scheduled 8/20) |
| EP55 | `PD-2026-055-burge` | **267** (S001–S210, M01–M42_src, F001–F012, T01–T03) — **100 % complete** | **none** | ✅ 1,748.0 s / 296 chunks | ✅ 816 cues | **short59** (scheduled 8/21) |
| EP56 | `PD-2026-056-postoffice` | **67 of 267** — only `S001`–`S067` | none (dir empty) | ❌ **not generated** | ❌ | none |

Paths: stills `H:\pd-media\assets\ai\<slug>\`, i2v `H:\pd-media\assets\ai_video\flowers\`, VO `H:\pd-media\episodes\<EPID>\06_voice\master\vc_master_v001.mp3`, index `episodes/<EPID>/06_audio/narration_index.v001.json`, captions `episodes/<EPID>/08_edit/captions.final.v001.srt`.

### 0.2 Format facts that constrain every build

- **All stills are 3840×2160, 16:9.** Nothing vertical was generated. This is fine and is exactly what `short57`–`short59` did: they reuse episode S-stills at 4K and Short.tsx crops/moves them (`MovingImage` + `<stem>_depth.png` parallax). Verified: `short57_01.png` is a byte copy of `norfolk/S009.png`, `_02`=`S016`, `_03`=`S022`, `_04`=`S036`, `_05`=`S005`, `_06`=`S029`, `_07`=`S001`, `_09`=`S011`.
- **Pick crop-survivors.** `[STYLE]` is telephoto/centred/shallow-DOF, so macro and single-subject plates survive a 9:16 centre crop. Wide harbor / vast-marble / gallery-from-high-rear plates do **not**. Every asset list below is already filtered for this.
- **EP53 has no face-forward stills.** Its `F001`–`F012` emotive-face set is specified in `EP53_norfolk_CODEX_A_ASSETS.v001.md` §5.13 but **was never generated** (0 files on disk). EP53 shorts therefore satisfy METHOD rule 7 (faces + emotion) via `T01`–`T03_face` (3 files, face pushed to a horizontal third — usable for the ShortThumb cover, weak for a centre crop) plus motion. See §6 gap G1.
- **EP55 is the only episode with a full emotive-face lane** (`F001`–`F012` on disk) — its shorts should carry a face in the hook and payoff.

### 0.3 Live schedule audit (read-only, `scripts/yt_schedule_audit.py`, run 2026-07-28)

27 uploads carry a future `publishAt`. Last reservation **2026-08-21 12:00 JST**. Shorts already booked: 7/31, 8/01, 8/02, 8/03, then one per day 8/04 → 8/13, then **8/16 → 8/21**. Long-form occupies 7/28 → 8/03 (double-stacked with a short on 7/31–8/03, which is allowed — the rule is one *short* per day).

> **Collision-free short slots: 2026-08-14 (Fri), 2026-08-15 (Sat), and 2026-08-22 onward.** 8/14 and 8/15 are a genuine two-day hole in the daily cadence (nothing sits between 8/13 and 8/16) and should be filled first.

---

## 1. Rules applied to every short in this slate

Each of the 13 shorts below is built to these, and the per-short build checklist (§5) verifies them:

1. **1-second hook** — frame 0 is mid-action; first spoken line names a person and an irreversible event. No logo, no "in this video", no brand card at the head.
2. **No brand intro.** The gold `BrandOpening` is a long-form device. Shorts open on the image.
3. **Open loop → payoff.** The hook withholds; the last 3 s answer the first 2 s.
4. **Length 40–58 s.** English legal material with the accuracy locks intact does not fit 20–40 s (measured on shorts #19–#24: GAP 2.7 s overshot, GAP 1.2 s landed 51–59 s). Target **GAP = 0.72 s** (the `gen_newshort_narration.py` default) and tighten with `--gap 0.45` if a short exceeds 58 s.
5. **Loop tail.** The final beat repeats the hook image + hook telop so the last frame cuts cleanly to the first (the pattern `short57` already uses: `{line:'L5', id:'loop', src:img('01'), fast:true, telop:<hook telop>}`).
6. **Muted-first.** Big speech-synced captions (`build_short_mix.py` splits at breath units, ~7 words max, 56–68 px, y 1280–1560). **Pattern interrupt every 1–2 s:** no beat longer than 2.0 s without a cut, punch-zoom or new image. Beat counts below are sized for this.
7. **Faces + motion in hook and payoff** — EP54 uses `M##_rife.mp4` i2v clips; EP55 uses `F0##` emotive faces; EP53/EP56 use `pushin`/`parallax` on depth-mapped stills plus the `ShortArt` code layers.
8. **Franchise format.** Every short in this slate fits one of three named repeatable formats so the series is recognisable:
   - **F-A "The machine that manufactures agreement"** — interrogation/confession mechanics (EP53).
   - **F-B "The number that convicted him"** — arithmetic as the villain (EP54, EP56).
   - **F-C "They knew, and nothing happened"** — a written warning that was buried (EP55, EP56).
9. **Sub-conversion.** Spoken + on-screen CTA, funnel line, pinned comment, Related-video. `SUBSCRIBE` never appears — the long-form end-card is live in `Short.tsx` since 2026-07-28 and every short must set its props (§7 step 7b; gap G2 closed).
10. **Persona.** Same channel voice `nPczCjzI2devNBz1zQrb`, `eleven_multilingual_v2`, same kinetic-caption style, same spoken close: *"Follow for the cases they don't teach you."*
11. **Cross-platform.** `-yt` and `-tt` exports per short (TikTok never says "YouTube"/"link"). Reels export reuses the `-tt` cut (`short52`/`short53` already produced `_reels.mp4`).
12. **Retention iteration.** Log each short's swipe-away point post-publish; the biggest drop is the next short's target.

**Vertical-format constraints (from `SHORTS_REMOTION_SPEC.md` §4):** 1080×1920 @30 fps. Telop zone y 180–560. Caption zone y 1280–1560. Never place anything important at x>960 or y>1620 (platform UI). Citations go top-left via `CitationTopLeft` — **and never on the same beat as a top telop** (the short19 defect: the telop covered the middle of a legal disclaimer and inverted its meaning).

---

## 2. EP53 — The Norfolk Four (`PD-2026-053-norfolk`) — 3 new shorts

Format lane **F-A**. Accuracy locks carried from `EP53_norfolk_FACTS_LEDGER.v001`: all four are LIVING with ABSOLUTE PARDONS — innocence is stated as fact; Det. Ford was **never charged for this case** (his 12½-year federal sentence was for extortion + lying to the FBI in unrelated matters) and no short may imply otherwise; Michelle Moore-Bosko is named with dignity and never depicted; no identifiable person anywhere.

---

### short60 — "His confession didn't match the murder. So they fixed the confession."

- **Slot:** 2026-08-14 (Fri) 12:00 JST · **Format:** F-A · **Target 46–52 s**
- **Hook line (first 1 s, re-recorded):** *"American police are allowed to lie to you about the evidence — and in this room they used it like a crowbar."* — 20 w. Frame 0 = `S055` (polygraph needle mid-swing).
- **Open loop:** what does eleven hours in that room actually manufacture? **Payoff (last 3 s):** the crime was used to repair the confession.

**Script excerpt (verbatim, from `EP53_norfolk_script.en.v001.md` ACT I):**
> "They gave him a polygraph in the middle of the night and then told him he had failed it — which was false, and, you should know, perfectly legal; American police are allowed to lie to you about the evidence, and in this room they used that permission like a crowbar."
> "And here is the detail that should have ended the case on the spot: he got it wrong. His account of how Michelle died didn't match how Michelle died. The method was wrong. The details were wrong. So the statement was taken again, and corrected, and taken again, until it finally agreed with the crime scene."
> "The confession did not describe the crime; the crime was used to repair the confession."

**Audio source**

| Line | Source | Master timecode | Dur | Words |
|---|---|---|---|---|
| L1 hook | **RE-RECORD** | — | ~6.5 s | **20** |
| L2 | CUT `vc_master_v001.mp3` VC-0059 | 268.95 → 283.95 | 15.00 s | 51 |
| L3 | CUT VC-0076 → VC-0079 | 363.96 → 375.63 | 11.67 s | 37 |
| L4 | CUT VC-0080 + VC-0082 (drop VC-0081 "Read that back slowly") | 375.93 → 382.67 **and** 384.85 → 389.81 | 11.70 s | 34 |
| L5 CTA | **RE-RECORD** | — | ~7 s | **26** |

L5 text (re-record): *"Four sailors confessed. Every DNA test said no. The full case is on the channel — follow for the cases they don't teach you."* (26 w)
**Re-record total: 46 words.** Cut total ≈ 38.4 s; with GAP 0.72 s ×4 ≈ **~52 s finished**.

**Assets (all exist, `H:\pd-media\assets\ai\norfolk\`)**

| Beat | File | What it is | Motion |
|---|---|---|---|
| hook | `S055.png` | Polygraph needle mid-swing, jagged line | `pushin`, `fast` |
| b1 | `S054.png` | Examiner's hands on polygraph dials | `parallax` |
| b1b | `S005.png` | Bare bulb over empty steel table, two chairs | `kenburns` |
| b2 | `S052.png` | Detective from behind leaning across the table | `pushin` |
| b2b | `S051.png` | Exhausted young man, head bowed into hands | `parallax` |
| b3 | `S056.png` | Torn polygraph chart curling on steel | `pushin` |
| b3b | `S057.png` | Trembling hand signing a blurred typed page | `parallax` |
| b4 | `S058.png` | Smeared signed statement squared on steel table | `kenburns` |
| c1 | `S059.png` | Single fresh chalk stroke, dust still falling | `pushin` |
| cta | `S060.png` | Wide interrogation room, bulb, empty chair | `kenburns` |
| loop | `S055.png` | (repeat of hook) | `pushin`, `fast` |

**Caption plan:** `build_short_mix.py` auto-splits at breath units. Telops (upper zone, ≤2 lines, all-caps): `POLICE MAY\nLIE TO YOU` · `ELEVEN HOURS\nOVERNIGHT` · `HE GOT IT\nWRONG` · `SO THEY FIXED\nTHE CONFESSION` · `CONFESSION\nNUMBER ONE`. No citation art on any telop beat.
**CTA:** on-screen `▶ FULL CASE` pill + long-form title line; spoken as L5. TikTok cut swaps to *"…the full case is on our profile."*
**Cover frame / ShortThumb:** background `norfolk/T01_face.png` (illustrative sailor, hollow dread) — headline `THEY FIXED\nTHE CONFESSION`, badge `INNOCENT`. Baked over the first 1.5 s by `scripts/coverfirst.sh`.

---

### short61 — "The Navy proved he was on a ship. He confessed anyway."

- **Slot:** 2026-08-23 (Sun) 12:00 JST · **Format:** F-A · **Target 44–50 s**
- **Hook (re-record):** *"The United States Navy had him on a ship when she was killed. He confessed anyway."* — 16 w. Frame 0 = `S078` (destroyer's white wake across black night water).
- **Payoff:** the confession grew roots — he testified to it against other innocent men.

**Script excerpt (ACT II, verbatim):**
> "Navy duty records placed him aboard his ship when Michelle was killed — an alibi most defendants would kill for, stamped and filed by the United States military. It did not matter. Nobody in that room wanted it to matter. After hours of Ford's method, Joseph Dick confessed to a crime his own service records said he could not have committed."
> "The story he had been handed grew roots in him. He repeated it to prosecutors, repeated it to himself, and would eventually stand up in court and testify to it — against other innocent men, in words that had been written for him in that room."

**Audio source**

| Line | Source | Master timecode | Dur | Words |
|---|---|---|---|---|
| L1 hook | **RE-RECORD** | — | ~5.5 s | **16** |
| L2 | CUT VC-0104 → VC-0107 | 502.01 → 515.61 | 13.60 s | 40 |
| L3 | CUT VC-0108 | 515.91 → 522.13 | 6.22 s | 21 |
| L4 | CUT VC-0110 → VC-0111 | 531.74 → 546.21 | 14.47 s | 46 |
| L5 CTA | **RE-RECORD** | — | ~7 s | **25** |

L5 text: *"Every DNA test excluded him. He stayed convicted for eleven years. The full case is on the channel — follow for the cases they don't teach you."* (25 w)
**Re-record total: 41 words.** Cut ≈ 34.3 s → **~48 s finished**.

**Assets** — `S078` (destroyer wake) · `S077` (two barracks bunks, one stripped) · `S006` (eight Navy berthing lockers, one ajar) · `S073` (slight young man from behind in the chair) · `S075` (young man from behind, hands flat on table) · `S098` (hands fanning time cards and bank slips) · `S079` (witness-stand microphone, single hard shaft) · `S083` (second chalk stroke added) · `S050` (empty jail visiting booth) · loop `S078`.
**Telops:** `ON A SHIP\nTHAT NIGHT` · `THE NAVY\nSAID SO` · `HE CONFESSED\nANYWAY` · `THEN HE\nKEPT CONFESSING` · `CONFESSION\nNUMBER TWO`.
**Cover:** background `S077`, headline `THE NAVY SAID\nHE WASN'T THERE`, badge `CONFESSED`.

---

### short62 — "They took a guilty plea six weeks after they found the real killer."

- **Slot:** 2026-08-26 (Wed) 12:00 JST · **Format:** F-A · **Target 46–54 s**
- **Hook (re-record):** *"In March 1999 the DNA found the real killer. In April, the state took another innocent man's guilty plea."* — 19 w. Frame 0 = `S126` (DNA gel, one lane bright, four empty).
- **Payoff:** Ballard pleaded guilty and swore he acted alone — while four other men stayed in prison for doing it with him.

**Script excerpt (ACT III, verbatim):**
> "And the cruelest bookkeeping of all is in the dates, so look at them with me… But Joseph Dick pleaded guilty in April 1999. April. After the letter. After the match. The Commonwealth accepted a guilty plea for life in prison from a DNA-excluded man a month and a half after its own laboratory identified the real killer."
> "The State of Virginia accepted a guilty plea from Omar Ballard, who swore under oath that he had done this alone — while keeping four other men in prison for doing it with him."

**Audio source**

| Line | Source | Master timecode | Dur | Words |
|---|---|---|---|---|
| L1 hook | **RE-RECORD** | — | ~6.5 s | **19** |
| L2 | CUT VC-0203 → VC-0206 | 1013.37 → 1020.45 | 7.08 s | 15 |
| L3 | CUT VC-0207 | 1020.75 → 1028.87 | 8.12 s | 27 |
| L4 | CUT VC-0213 | 1074.84 → 1084.45 | 9.61 s | 34 |
| L5 CTA | **RE-RECORD** | — | ~7 s | **24** |

L5 text: *"A federal judge later ruled all four actually innocent. The full case is on the channel — follow for the cases they don't teach you."* (24 w)
**Re-record total: 43 words.** Cut ≈ 24.8 s → **~46 s finished**.

**Assets** — `S126` (gel: one lane aligns bright, four empty) · `S121` (folded cream letter alone in a warm shaft) · `S134` (clerk's hand pressing a date stamp) · `S136` (young defendant, chin dropped) · `S139` (young man standing to face the bench) · `S143` (four identical steel cell doors) · `S170` (gel igniting, one lane blazes) · `S184` (open handcuffs on a federal courtroom table) · loop `S126`.
**Telops:** `MARCH 1999:\nDNA MATCH` · `APRIL 1999:\nGUILTY PLEA` · `SIX WEEKS\nAFTER` · `HE SAID HE\nACTED ALONE` · `FOUR STAYED\nIN PRISON`.
**Cover:** background `S170`, headline `SIX WEEKS\nAFTER THE MATCH`, badge `DNA CLEARED`.

---

## 3. EP54 — Curtis Flowers (`PD-2026-054-flowers`) — 3 new shorts

Format lane **F-B**. Locks from `EP54_flowers_FACTS_LEDGER.v001`: Flowers is LIVING and FULLY CLEARED; Doug Evans is LIVING and was **never criminally charged or disciplined** — every characterisation must trace verbatim to SCOTUS, the Mississippi Supreme Court, or on-record reporting; Odell Hallmon is a convicted triple murderer (safe per record); the murders remain **unsolved** and no alternative suspect may be named or hinted; victim dignity for Bertha Tardy, Carmen Rigby, Robert Golden and Derrick "Bobo" Stewart.

**EP54 is the only episode with real motion:** 44 Wan-i2v clips at `H:\pd-media\assets\ai_video\flowers\M##_rife.mp4`, 1920×1080 @48 fps, ~3.42 s each. Use them as `kind:'video'` beats in the hook and payoff — this is the cheapest available fix for METHOD rule 7 and for the standing "animation feels thin" complaint.

---

### short63 — "He voted not guilty. They handcuffed him in the jury box."

- **Slot:** 2026-08-22 (Sat) 12:00 JST · **Format:** F-B · **Target 44–50 s**
- **Hook (re-record):** *"A juror in Mississippi refused to convict. He was handcuffed in open court."* — 13 w. Frame 0 = **`M23_rife.mp4`** (juror chair in a cold spotlight, a deputy's long shadow entering) — motion from frame 0.
- **Payoff:** the attorney general took the case away and dropped the charge — but the message had already been broadcast.

**Script excerpt (ACT III, verbatim):**
> "When the mistrial was declared, James Bibbs — a juror, a citizen doing the duty the state had summoned him to do — was handcuffed in open court and charged with perjury. The prosecution pursuing him: Doug Evans."
> "The state attorney general's office eventually stepped in, took the case away, and dropped the charge entirely. But the message had been broadcast, in handcuffs, in a public courtroom — and it did not need repeating."

**Audio source**

| Line | Source | Master timecode | Dur | Words |
|---|---|---|---|---|
| L1 hook | **RE-RECORD** | — | ~4.5 s | **13** |
| L2 | **RE-RECORD** bridge (sets the 2008 hung jury; the master's version leans on the running trial count) | ~9 s | **27** |
| L3 | CUT `vc_master_v001.mp3` VC-0172 → VC-0173 | 918.01 → 930.58 | 12.57 s | 38 |
| L4 | CUT VC-0175 → VC-0176 | 943.67 → 956.23 | 12.56 s | 36 |
| L5 CTA | **RE-RECORD** | — | ~7 s | **25** |

L2 text: *"Trial five, 2008. The jury hung on a single holdout — one Black juror, James Bibbs, who was not persuaded a thin case had become a certain one."* (27 w)
L5 text: *"He was tried six times for the same four murders. The full case is on the channel — follow for the cases they don't teach you."* (25 w)
**Re-record total: 65 words.** Cut ≈ 25.1 s → **~48 s finished**.

**Assets** — hook `M23_rife.mp4` (video) · `S123` (juror chair pulled into a hard cold spotlight) · `S124` (deliberation-room door ajar, cold blade of light) · `S148` (deputy's silhouette in the doorway, keys) · `M21_rife.mp4` (jurors' backs, two clusters leaning apart) · `S126` (chair returned to the box but left out of line) · `S079` (heavy pencil line mid-stroke across a name card) · `S154` (**F07** — illustrative lone holdout juror, frightened but resolute; the one face-forward plate this short needs) · loop `M23_rife.mp4`.
**Telops:** `HE VOTED\nNOT GUILTY` · `MISTRIAL` · `HANDCUFFED\nIN COURT` · `CHARGED WITH\nPERJURY` · `CHARGE\nDROPPED`.
> **Legal-lock telop, mandatory:** the final beat carries `CHARGE DROPPED · NEVER CONVICTED` so the short cannot be read as saying Bibbs was punished. Do **not** put a `citation` ShortArt on the same beat (short19 defect).

**Cover:** background `S123`, headline `HE VOTED\nNOT GUILTY`, badge `HANDCUFFED`.

---

### short64 — "The state asked five jurors 145 questions. It asked eleven others twelve."

- **Slot:** 2026-08-25 (Tue) 12:00 JST · **Format:** F-B · **Target 48–56 s**
- **Hook (re-record):** *"The Supreme Court counted. Forty-one of forty-two Black jurors — struck."* — 11 w. Frame 0 = **`M34_rife.mp4`** (wall of struck juror cards, first corner catching gold fire).
- **Payoff:** *"The numbers speak loudly," Kavanaugh wrote* — 7–2, conviction gone.

**Script excerpt (ACT IV, verbatim):**
> "In the six trials combined, the Court wrote, the state used its strikes against '41 of the 42 black prospective jurors that it could have struck.' In the first four trials, thirty-six Black prospective jurors came up — 'The State tried to strike all 36.'"
> "In trial six, the state struck five of the six Black citizens in the pool, and the Court noticed how: it had asked those five Black prospective jurors a hundred and forty-five questions — hunting for any excuse — while asking the eleven seated white jurors a total of twelve. 'The numbers speak loudly,' Kavanaugh wrote."

**Audio source**

| Line | Source | Master timecode | Dur | Words |
|---|---|---|---|---|
| L1 hook | **RE-RECORD** | — | ~4 s | **11** |
| L2 | CUT VC-0251 → VC-0252 | 1336.10 → 1352.56 | 16.46 s | 45 |
| L3 | CUT VC-0253 | 1352.86 → 1369.57 | 16.71 s | 50 |
| L4 | CUT VC-0254 + VC-0258 | 1369.87 → 1372.47 **and** 1414.08 → 1419.51 | 8.03 s | 24 |
| L5 CTA | **RE-RECORD** | — | ~7 s | **23** |

L5 text: *"Six trials, four death sentences, twenty-three years — and the murders are still unsolved. The full case is on the channel. Follow for more."* (23 w)
**Re-record total: 34 words.** Cut ≈ 41.2 s → **~55 s finished** (if it lands >58 s, re-run `gen_newshort_narration.py --gap 0.45`).

**Assets** — hook `M34_rife.mp4` (video) · `S168` (microfilm reader alone in a dark records room) · `S073` (twelve jury chairs lit flat) · `S074` (twelve chairs, exactly one fallen into shadow) · `S169` (close on the one unstruck card among struck ones) · `S170` (wall of struck cards igniting) · `M33_rife.mp4` (two light bars, the tall gold one still climbing) · `S166` (empty elevated court bench, nine chairs) · `S180` (hands opening a slim bound opinion, one line lit) · loop `M34_rife.mp4`.
**Telops:** `41 OF 42` · `STRUCK` · `145 QUESTIONS` · `VS 12` · `"THE NUMBERS\nSPEAK LOUDLY"` · `7–2`.
**Cover:** background `S170`, headline `41 OF 42\nSTRUCK`, badge `7–2 SCOTUS`.

---

### short65 — "The only witness who said he confessed later said, on tape: that was a lie."

- **Slot:** 2026-08-28 (Fri) 12:00 JST · **Format:** F-B · **Target 46–54 s**
- **Hook (re-record):** *"Four juries were told he confessed in jail. The man who said so was lying."* — 14 w. Frame 0 = `S131` (dark human silhouette behind ribbed prison visitation glass).
- **Payoff:** the tape. *"That was a lie."*

**Script excerpt (ACT III, verbatim):**
> "And then, in 2016, the state's star witness showed the world exactly who he was. Odell Hallmon took a gun and murdered three people — his ex-girlfriend, Marquita Hill; her mother, Carolyn Ann Sanders; and a man named Kenneth Loggins — and wounded a fourth. He pleaded guilty about two weeks later. Three murders. Life in prison."
> "And on tape, the state's star witness said this: 'As far as him telling me he killed some people, hell, naw, he ain't never told me that. That was a lie.'"
> "Four trials. Four juries told about a confession that, by the teller's own recorded words, never happened. The only direct evidence in six prosecutions — gone, in one sentence."

**Audio source**

| Line | Source | Master timecode | Dur | Words |
|---|---|---|---|---|
| L1 hook | **RE-RECORD** | — | ~5 s | **14** |
| L2 | **RE-RECORD** bridge (introduces Hallmon; the master's introduction runs three long paragraphs) | ~9 s | **28** |
| L3 | CUT VC-0212 → VC-0215 | 1113.64 → 1130.10 | 16.46 s | 42 |
| L4 | CUT VC-0219 → VC-0221 | 1156.74 → 1167.75 | 11.01 s | 35 |
| L5 | CUT VC-0223 → VC-0224 | 1169.46 → 1179.28 | 9.82 s | 27 |
| L6 CTA | **RE-RECORD** | — | ~6 s | **21** |

> L6 requires `gen_newshort_narration.py`'s `DELIVERY` map to accept a sixth line — pass explicit deliveries via `--text-json` (`L6: "calm"`). If you would rather not touch the map, fold L5+L6 into one line.

L2 text: *"His name was Odell Hallmon. A career criminal from the same county, who swore Curtis Flowers had confessed to him in jail — and told that story in four of the six trials."* (31 w — trim to 28 at record time)
L6 text: *"The charges were dropped for good in 2020. The full case is on the channel — follow for the cases they don't teach you."* (23 w)
**Re-record total: 65 words.** Cut ≈ 37.3 s → **~57 s finished**.

**Assets** — `S131` (ribbed-glass silhouette) · `S135` (silhouette closer, leaning toward the glass) · `M27_rife.mp4` (silhouette leaning a degree closer — video) · `S136`/`S137`/`S138` (three warm points of light in a dark field → guttering → three fading trails: the three murders, handled with zero depiction) · `S139` (cassette recorder and phone handset on a bare table) · `M30_rife.mp4` (hands holding a recorder toward the glass, reels starting — video) · `S140` (abstract waveform with one violent spike) · `S134` (open ledger of tallies, one column absurdly long) · loop `S131`.
**Telops:** `THE ONLY\nDIRECT EVIDENCE` · `4 OF 6 TRIALS` · `2016: HE KILLED\nTHREE PEOPLE` · `THEN, ON TAPE` · `"THAT WAS\nA LIE."`
> **Legal-lock:** the murders remain unsolved and Doug Evans was never charged — neither fact is asserted otherwise anywhere in this short. Hallmon's triple murder is stated only as the record has it (pleaded guilty, life).

**Cover:** background `S140`, headline `"THAT WAS\nA LIE."`, badge `ON TAPE`.

---

## 4. EP55 — Jon Burge (`PD-2026-055-burge`) — 3 new shorts

Format lane **F-C**. Locks from `EP55_burge_FACTS_LEDGER.v001`: Burge is dead and stands convicted of **perjury + obstruction only** — he was **never charged with torture**, and no short may blur that; Andrew Wilson was guilty of the two officers' murders and the film says so; the four 2003 pardonees are innocent of record; all other claimants get the official torture *finding*, not blanket innocence; torture is described clinically, never staged.

EP55 has the complete `F001`–`F012` emotive-face lane on disk — use it.

---

### short66 — "A jail doctor put police torture in writing in 1982. The letter was buried."

- **Slot:** 2026-08-15 (Sat) 12:00 JST · **Format:** F-C · **Target 46–52 s**
- **Hook:** **CUT, no re-record needed** — the long-form cold open already opens on a person + an irreversible event inside 5 s. Frame 0 = `S003` (doctor's white coat on an infirmary door hook at night).
- **Open loop:** who buried it, and what happened to the page? **Payoff:** in 2010 that same page was carried into a federal courtroom as an exhibit.

**Script excerpt (COLD OPEN, verbatim):**
> "In February of 1982, a doctor at the Cook County Jail examined a new prisoner and found injuries he could not explain away… So the doctor did what doctors are supposed to do. He wrote a letter to the superintendent of the Chicago Police Department, describing the injuries, demanding — his words — a thorough investigation. That letter went up the chain of command, landed on the desk of one of the most powerful men in Illinois, and died there. No answer. No investigation. Nothing."

**Audio source**

| Line | Source | Master timecode | Dur | Words |
|---|---|---|---|---|
| L1 hook | CUT `vc_master_v001.mp3` VC-0001 | 0.00 → 7.62 | 7.62 s | 23 |
| L2 | CUT VC-0003 → VC-0005 | 14.21 → 35.84 | 21.63 s | 61 |
| L3 | CUT VC-0006 → VC-0009 | 36.15 → 46.80 | 10.65 s | 29 |
| L4 | CUT VC-0223 → VC-0227 (the 2010 trial: "For five weeks, a federal courtroom heard everything the statute of limitations had buried… The letter.") | 1309.82 → 1327.65 | 17.83 s | 46 |
| L5 CTA | **RE-RECORD** | — | ~7 s | **26** |

L5 text: *"He was never charged with torture — only with lying about it. The full case is on the channel. Follow for the cases they don't teach you."* (26 w)
**Re-record total: 26 words.** Cut ≈ 57.7 s — **too long**; trim L2 to VC-0004 → VC-0005 only (24.07 → 35.84, 11.77 s, 33 w). Revised cut ≈ 47.9 s → **~57 s finished**; if over 58 s, drop VC-0001 and open on VC-0002 instead.

**Assets** — `S003` (doctor's coat on the infirmary door hook) · `F003` (**emotive face** — illustrative jail doctor, brow furrowed in troubled resolve) · `S071` (typed sheet still rolled in the typewriter platen) · `S072` (sealed envelope on the infirmary desk, stethoscope) · `S074` (manila routing envelope in a wire out-tray) · `S075` (letter atop a paperwork stack in an executive in-tray) · `S010` (black rotary telephone silent on a vast executive desk) · `S008` (file drawer sliding shut over a typed page) · `S159` (**the payoff plate** — the 1982 letter sealed in a clear exhibit sleeve, 2010) · `S196` (drawer sliding open, the letter catching morning light) · loop `S003`.
**Telops:** `FEBRUARY 1982` · `BURNS. CLIP\nWOUNDS.` · `HE WROTE IT\nDOWN` · `NO ANSWER` · `2010: EXHIBIT` · `NEVER CHARGED\nWITH TORTURE`.
**Cover:** background `S159`, headline `THEY BURIED\nTHE LETTER`, badge `1982`.

---

### short67 — "Prosecutors proved he tortured people. They couldn't charge him with anything."

- **Slot:** 2026-08-24 (Mon) 12:00 JST · **Format:** F-C · **Target 48–56 s**
- **Hook (re-record):** *"Illinois gave prosecutors three years to charge a torturer. The city took twenty-four."* — 13 w. Frame 0 = `S127` (institutional wall clock, second hand caught mid-sweep).
- **Open loop:** how does a proven crime become uncharged? **Payoff:** charges filed — none.

**Script excerpt (ACT III, verbatim):**
> "Anthony Holmes, 1973: the clock died in 1976. Andrew Wilson, February 1982: the clock died in February 1985 — while the letter about him sat unanswered in a prosecutor's filing system. Every victim of the eighties: expired by the early nineties, before the Goldston report ever saw daylight."
> "They examined one hundred and forty-eight claims of torture… They believed torture had occurred in roughly half the cases they examined. In three of them — Andrew Wilson's among them — they found proof beyond a reasonable doubt: enough evidence, right now, to convict Jon Burge and his men in any courtroom in America."
> "And then came the conclusion… charges filed — none. Every provable crime was decades past its three-year clock."

**Audio source**

| Line | Source | Master timecode | Dur | Words |
|---|---|---|---|---|
| L1 hook | **RE-RECORD** | — | ~4.5 s | **13** |
| L2 | CUT VC-0160 → VC-0162 | 904.06 → 925.93 | 21.87 s | 48 |
| L3 | CUT VC-0172 + VC-0174 → VC-0175 | 971.71 → 974.77 **and** 984.29 → 999.54 | 18.31 s | 54 |
| L4 | CUT VC-0177 → VC-0178 | 1001.39 → 1013.82 | 12.43 s | 34 |
| L5 CTA | **RE-RECORD** | — | ~7 s | **25** |

L5 text: *"He was finally jailed for lying about it under oath. Four and a half years. The full case is on the channel — follow for more."* (25 w)
**Re-record total: 38 words.** Cut ≈ 52.6 s — trim L2 to VC-0160 → VC-0161 (904.06 → 919.32, 15.26 s, 31 w). Revised cut ≈ 46 s → **~55 s finished**.

**Assets** — `S127` (wall clock, second hand mid-sweep) · `S128` (large wall clock in near-black, hands unreadable — an `also_thumb` plate) · `S113` (banker's boxes on steel shelving, labels smeared) · `S115` (microfilm reader alone in a dark records annex) · `F009` (**emotive face** — untouchable-commander archetype, contempt) · `S119` (thick final report banded shut, chair pushed in) · `S118` (single blank legal form centred on an empty desk — the charge that was never filed) · `S143` (death-row corridor, every cell door standing open) · loop `S127`.
**Telops:** `3-YEAR CLOCK` · `1973 → EXPIRED 1976` · `1982 → EXPIRED 1985` · `148 CLAIMS` · `PROOF BEYOND\nREASONABLE DOUBT` · `CHARGES FILED: 0`.
**Cover:** background `S128`, headline `PROVEN.\nUNCHARGEABLE.`, badge `0 CHARGES`.

---

### short68 — "He was in federal prison. The city kept paying his police pension."

- **Slot:** 2026-08-27 (Thu) 12:00 JST · **Format:** F-C · **Target 42–50 s**
- **Hook (re-record):** *"He went to federal prison for lying about police torture — and kept his police pension."* — 15 w. Frame 0 = `S175` (boardroom table split by a hard blade of cold light).
- **Payoff:** four to four. A tie meant Burge won. The cheque arrived every month until he died.

**Script excerpt (ACT IV, verbatim):**
> "Days after the sentencing, the police pension board met to decide whether a man imprisoned for lying about torture should keep collecting his police pension. Four civilian members voted to strip it. Four police members voted to let him keep it. Four to four — a tie — and under the rules, a tie meant Burge won. The state's attorney general fought it all the way to the Illinois Supreme Court and lost."
> "Every month, from his cell and then from his Florida living room, the pension arrived: the city paying the man its own report had named, roughly three thousand dollars at a time, until the day he died."

**Audio source**

| Line | Source | Master timecode | Dur | Words |
|---|---|---|---|---|
| L1 hook | **RE-RECORD** | — | ~5 s | **15** |
| L2 | CUT VC-0244 | 1443.14 → 1451.73 | 8.59 s | 25 |
| L3 | CUT VC-0245 → VC-0247 | 1452.03 → 1462.24 | 10.21 s | 32 |
| L4 | CUT VC-0248 → VC-0249 | 1462.54 → 1479.51 | 16.97 s | 53 |
| L5 CTA | **RE-RECORD** | — | ~7 s | **27** |

L5 text: *"Chicago answered with America's first reparations for police violence — and put the story in its schools. The full case is on the channel. Follow for more."* (27 w)
**Re-record total: 42 words.** Cut ≈ 35.8 s → **~50 s finished**.

**Assets** — `S175` (boardroom table split by cold light) · `S101` (police star badge face-up on a cleared desk, empty chair) · `S173` (empty defence table after sentencing) · `S176` (macro of plain envelopes accumulating on a Florida sideboard) · `S144` (Florida driveway mailbox, red flag raised, heat shimmer) · `S106` (white cabin cruiser at a Florida dock, golden dusk) · `F011` (**emotive face** — older Black woman and man in the council gallery, tears) · `S195` (empty Florida dock at dusk, no boat, slack ropes) · loop `S175`.
**Telops:** `4½ YEARS\nFEDERAL PRISON` · `PENSION BOARD` · `4 TO 4` · `A TIE MEANT\nHE KEPT IT` · `~$3,000/MONTH\nUNTIL HE DIED`.
> **Legal-lock telop on the payoff beat:** `CONVICTED OF PERJURY — NEVER CHARGED WITH TORTURE`.

**Cover:** background `S176`, headline `IN PRISON.\nSTILL PAID.`, badge `4–4 TIE`.

---

## 5. EP56 — Post Office Horizon (`PD-2026-056-postoffice`) — 4 new shorts ⚠ BLOCKED

Format lanes **F-B** and **F-C**. Locks from `EP56_postoffice_FACTS_LEDGER.v001`: the convicted sub-postmasters are INNOCENT (Court of Appeal 2021 + the 2024 Act) — innocence is stated as fact; the villain is the institution, held to adjudicated findings only; nearly all principals are LIVING; **nobody has been criminally convicted for the scandal** (date-stamped) — state it plainly, never predict it away; Martin Griffiths' death gets one passage at the Inquiry's own wording, no depiction, and is **not used in any short**.

> **⚠ EP56 is not buildable yet.** (a) Stills stop at `S067` — 200 of 267 missing, including **all** faces (`F001`–`F012`, `T01`–`T03`) and **all** motion seeds (`M01`–`M42`). (b) There is **no VO master and no narration index** — TTS was gated to the 2026-07-28 18:08 quota reset. So **every EP56 line is a re-record**, and the asset lists below are restricted to `S001`–`S067`, which exist.

---

### short69 — "The computer invented a debt. Her employer prosecuted her for it."

- **Slot:** 2026-08-29 (Sat) 12:00 JST · **Format:** F-B · **Target 44–50 s**
- **Hook:** *"In 2003 a village shopkeeper watched her computer invent a two-thousand-pound debt in front of her."* — 16 w. Frame 0 = `S025` (cold green screen at dawn, one impossible glowing total).
- **Payoff:** the money never existed, and the people who owned the computer knew.

**Script excerpt (COLD OPEN, verbatim — usable as-is):**
> "In 2003, in a Hampshire village shop, sub-postmistress Jo Hamilton watched her computer invent a debt in front of her. The screen said two thousand pounds was missing from her post-office till — money she had never seen. She phoned the helpline and followed its instructions — and while she was on the line, the missing two thousand became four. She remortgaged her house to pay it. Her employer prosecuted her anyway — for theft, in front of her whole village. But the money never existed. The computer was lying."

**Audio:** **ALL RE-RECORD — 5 lines, ~112 words** (L1 16 · L2 32 · L3 24 · L4 17 · L5 CTA 23). The long-form master does not exist.
L5: *"Her conviction was quashed in 2021. Nobody has been convicted for doing this to her. The full case is on the channel. Follow for more."* (24 w)

**Assets (all on disk)** — `S025` (impossible total on a cold green screen) · `S011` (macro of the green cursor block on curved glass) · `S024` (green terminal on a warm counter at closing) · `S026` (counted cash rows beside the glowing screen) · `S027` (1990s handset off the cradle, green glow) · `S043` (macro of a hand gripping the receiver, whitened knuckles) · `S031` (house keys on remortgage papers) · `S055` (manila prosecution file tied with red legal tape) · `S054` (macro of a charge-sheet heading, two smeared counts) · `S057` (red post-office sign at night in hard rain — `also_thumb`) · loop `S025`.
**Telops:** `£2,000 MISSING` · `SHE NEVER\nSAW IT` · `ON THE PHONE\nIT BECAME £4,000` · `SHE REMORTGAGED\nHER HOUSE` · `PROSECUTED\nANYWAY` · `THE MONEY NEVER\nEXISTED`.
**Cover:** background `S057`, headline `THE COMPUTER\nINVENTED A DEBT`, badge `INNOCENT`.

---

### short70 — "Her employer was also her prosecutor. About one a week, for fifteen years."

- **Slot:** 2026-08-30 (Sun) 12:00 JST · **Format:** F-C · **Target 44–52 s**
- **Hook:** *"The Post Office investigated the crime, decided the charge, and prosecuted the case. The police were never called."* — 18 w. Frame 0 = `S051` (dark saloon car parked outside a village shop at dawn).
- **Payoff:** the running number of Post Office or Fujitsu employees convicted of anything — it never changes.

**Script excerpt (ACT II, verbatim):**
> "In England and Wales, any company may bring a private prosecution — and the Post Office did, on an industrial scale. When a shortfall appeared, the Post Office investigated the crime, and the Post Office decided the charge, and the Post Office prosecuted the case. Victim, detective, and prosecutor, in one body. The police were not called, because the police were not needed. Between 1999 and 2015, roughly seven hundred sub-postmasters were prosecuted by the Post Office itself — on average, about one a week, for a decade and a half."
> "Theft was the hammer — it meant prison, headlines, ruin. And then, quietly, an offer: plead guilty to false accounting, pay back the shortfall, and the theft charge goes away."

**Audio:** **ALL RE-RECORD — 5 lines, ~118 words** (L1 18 · L2 34 · L3 26 · L4 17 · L5 CTA 23).
L5: *"Roughly a thousand people were convicted. The number of Post Office employees convicted is still zero. The full case is on the channel."* (22 w)

**Assets** — `S051` (saloon car outside the shop at dawn) · `S052` (official briefcase open on the counter, forms fanned) · `S053` (typed notice taped inside the shop door glass) · `S054` (charge-sheet heading, two counts) · `S055` (prosecution file, red tape) · `S056` (fountain pen poised above a plea-form signature line) · `S058` (empty British courtroom, canopied bench) · `S059` (barrister's wig on a ribboned brief) · `S057` (red sign in hard rain) · loop `S051`.
**Telops:** `VICTIM` · `DETECTIVE` · `PROSECUTOR` · `ONE BODY` · `~700 PROSECUTED\n1999–2015` · `ONE A WEEK` · `EMPLOYEES\nCONVICTED: 0`.
> **Legal-lock:** never call this a "unique power" — private prosecution is an ordinary right in England and Wales, and the ledger says so explicitly.

**Cover:** background `S058`, headline `HER EMPLOYER\nWAS THE PROSECUTOR`, badge `~700 CASES`.

---

### short71 — "He refused to sign. So they fired him — and he spent twenty years proving it."

- **Slot:** 2026-08-31 (Mon) 12:00 JST · **Format:** F-C · **Target 42–50 s**
- **Hook:** *"He put sixty-five thousand pounds into a village post office. He kept every receipt."* — 14 w. Frame 0 = `S012` (shoebox packed with receipts on a kitchen table, lamplight).
- **Payoff:** the Post Office had just fired the one man in Britain who would never let it go.

**Script excerpt (ACT I, verbatim):**
> "In May 1998, a man named Alan Bates and his partner Suzanne Sercombe put sixty-five thousand pounds of their own money into a small post office in Craig-y-Don, on the North Wales coast. He was a careful man — the kind who kept receipts, filed paperwork, backed up his backups. That detail will matter more than anything else in this film."
> "Alan Bates refused to press it. He refused to sign for phantom losses at all, and he sent the Post Office letter after letter saying precisely why. In November 2003, the Post Office terminated his contract without giving a reason — its own files, disclosed years later, called him unmanageable. He lost the shop and the sixty-five thousand pounds. What the Post Office did not know was that it had just fired the one man in Britain who would never, ever let it go."

**Audio:** **ALL RE-RECORD — 5 lines, ~120 words** (L1 14 · L2 33 · L3 30 · L4 21 · L5 CTA 22).
L5: *"He beat them in the High Court in 2019. The full case is on the channel — follow for the cases they don't teach you."* (23 w)

**Assets** — `S012` (shoebox of receipts, lamplight) · `S013` (grey Welsh headland, flat silver sea) · `S019` (grey North Wales seafront promenade) · `S020` (small Welsh corner shop, slate hills) · `S023` (handwritten paper ledger retired into an archive box) · `S034` (wall of labelled box files, one pulled proud) · `S046` (man's back filing papers by lamplight) · `S047` (man's back carrying two heavy box files into daylight) · `S048` (couple's backs before their own shuttered shopfront) · loop `S012`.
**Telops:** `£65,000` · `HE KEPT\nEVERY RECEIPT` · `HE REFUSED\nTO SIGN` · `"UNMANAGEABLE"` · `FIRED, NOV 2003` · `WRONG MAN\nTO FIRE`.
**Cover:** background `S012`, headline `HE KEPT\nEVERY RECEIPT`, badge `20 YEARS`.

---

### short72 — "The helpline told every one of them: you are the only one."

- **Slot:** 2026-09-01 (Tue) 12:00 JST · **Format:** F-B · **Target 44–52 s**
- **Hook:** *"Hundreds of shopkeepers phoned the same helpline. Every one was told the same sentence."* — 14 w. Frame 0 = `S033` (midnight village street, only the post office still lit).
- **Payoff:** there turned out to be ten thousand of them.

**Script excerpt (ACT I + ENDING, verbatim):**
> "The helpline had an answer, and the answer never changed. No one else is having this problem. You are the only one. The inquiry that finally examined this scandal heard that sentence described by sub-postmaster after sub-postmaster — the same reassurance, delivered up and down the country, to hundreds of people at once, each of them alone in a dark shop with a number that could not be true. It was not a small lie. It was the load-bearing lie. If you are the only one, the machine is fine — and the problem is you."
> "For years, a helpline told frightened people, one call at a time, that they were the only one. There turned out to be ten thousand of them."

**Audio:** **ALL RE-RECORD — 5 lines, ~124 words** (L1 14 · L2 31 · L3 30 · L4 26 · L5 CTA 23).
L5: *"They found each other in a village hall in 2009. The full case is on the channel — follow for more."* (20 w)

**Assets** — `S033` (midnight village street, only the post office lit) · `S027` (handset off the cradle, cord hanging, green glow) · `S042` (woman's back on the telephone against the green screen glow) · `S043` (hand gripping the receiver, whitened knuckles) · `S039` (woman's back at a midnight counter, terminal glow) · `S040` (husband and wife's backs, receipts sorted at the kitchen table) · `S036` (far-wide elderly customers queueing outside a village shop — **stand-in** for the Fenny Compton payoff) · `S049` (neighbours' backs under umbrellas across the village street) · `S014` (English village skyline under grey night cloud) · loop `S033`.
> **⚠ Asset substitution:** the true payoff plate for this short is the Fenny Compton village-hall beat, which lives in **ACT 4 (`S129`–`S166`) — not generated**. `S036`+`S049` are the best in-hand substitutes and read as "a crowd of only-ones". Regenerate the ACT 4 hall plate before build if possible.

**Telops:** `"YOU ARE THE\nONLY ONE"` · `SAID TO HUNDREDS` · `THE LOAD-BEARING\nLIE` · `10,000 OF THEM` · `ONE VILLAGE HALL`.
**Cover:** background `S033`, headline `"YOU ARE THE\nONLY ONE"`, badge `10,000 WERE`.

---

## 6. Schedule (one short per day, 12:00 JST, collision-free)

Audited live against the channel on 2026-07-28 with `python scripts/yt_schedule_audit.py` (read-only). **Do not re-derive this from local manifests** — the channel API is the source of truth.

| Date (JST) | Day | Short | Episode | Working title | Build status |
|---|---|---|---|---|---|
| 2026-08-14 | Fri | `short60` | EP53 | They fixed the confession | ✅ ready |
| 2026-08-15 | Sat | `short66` | EP55 | They buried the letter | ✅ ready |
| *8/16 – 8/21* | | *occupied* | | *(existing shorts incl. short56/57/58/59)* | — |
| 2026-08-22 | Sat | `short63` | EP54 | He voted not guilty | ✅ ready |
| 2026-08-23 | Sun | `short61` | EP53 | The Navy said he wasn't there | ✅ ready |
| 2026-08-24 | Mon | `short67` | EP55 | Proven. Uncharged. | ✅ ready |
| 2026-08-25 | Tue | `short64` | EP54 | 41 of 42 | ✅ ready |
| 2026-08-26 | Wed | `short62` | EP53 | Six weeks after the match | ✅ ready |
| 2026-08-27 | Thu | `short68` | EP55 | In prison. Still paid. | ✅ ready |
| 2026-08-28 | Fri | `short65` | EP54 | "That was a lie." | ✅ ready |
| 2026-08-29 | Sat | `short69` | EP56 | The computer invented a debt | ⚠ needs VO |
| 2026-08-30 | Sun | `short70` | EP56 | Her employer was the prosecutor | ⚠ needs VO |
| 2026-08-31 | Mon | `short71` | EP56 | He kept every receipt | ⚠ needs VO |
| 2026-09-01 | Tue | `short72` | EP56 | "You are the only one" | ⚠ needs VO + asset sub |

Episodes are interleaved (53 → 55 → 54 → 53 → 55 → 54 …) so no case runs three days straight, which also spreads the footage load across three separate still libraries (`footage_diversity` intent).

> **⛔ Funnel dependency — read before scheduling anything.** The long-forms for EP53, EP54, EP55 and EP56 are **not built and not scheduled** (the last scheduled long-form is 2026-08-03). A short whose pinned comment points at a private or non-existent long-form is a dead link — exactly the failure `SHORTS_CONVERSION_v001.md` STEP 0 exists to prevent. Therefore: **schedule the short, but do not post the pinned comment or set the Related-video until the matching long-form is public.** Same caveat already applies to the scheduled `short57`/`short58`/`short59`.

---

## 7. Build checklist (per short, using the existing pipeline — no new tooling)

Run from repo root unless noted. `NN` = short number, `EP` = episode slug.

**A. Audio (hybrid: cut from the long-form master + re-record only the hook/CTA)**

1. Cut the body lines from the long-form master with the timecodes in §2–§4. Pad each segment −0.12 s / +0.18 s so breaths survive:
   ```bash
   ffmpeg -y -ss <start-0.12> -to <end+0.18> \
     -i "H:/pd-media/episodes/<EP>/06_voice/master/vc_master_v001.mp3" \
     -c:a libmp3lame -b:a 128k \
     "H:/pd-media/episodes/<EP>/06_voice/draft/short<NN>/en_us/short<NN>_L2.mp3"
   ```
   Two-segment lines (short60 L4, short64 L4, short67 L3): cut both, then `ffmpeg -f concat`.
   > ⚠ **Naming trap (memory `pd-shorts-pipeline`):** shorts drafts MUST live in `06_voice/draft/short<NN>/en_us/` with `short<NN>_L?.mp3` names. Writing into `06_voice/draft/` directly collides with the episode's `VC-####.mp3` and silently splices long-form audio into the short.
2. Write `episodes/<EP>/09_package/short<NN>_lines.v001.json` = `[{id,delivery,text}, …]` with the **verbatim** text of every line (cut lines included — the index needs the text even though the mp3 already exists).
3. Synthesize only the missing lines. `gen_newshort_narration.py` skips any draft chunk that already exists (>2048 bytes), so the pre-placed cuts are preserved:
   ```bash
   python scripts/gen_newshort_narration.py --short NN --ep <EP> \
     --text-json episodes/<EP>/09_package/short<NN>_lines.v001.json --dry-run   # verify chars/$ first
   python scripts/gen_newshort_narration.py --short NN --ep <EP> \
     --text-json episodes/<EP>/09_package/short<NN>_lines.v001.json
   ```
   Voice `nPczCjzI2devNBz1zQrb` / `eleven_multilingual_v2`; delivery arc L1 intense → L5 calm. ElevenLabs is standing-approved; still record chars + cost.
4. Build the 4-layer mix and the caption timing:
   ```bash
   python scripts/build_short_mix.py --short NN --ep <EP>
   ```
   Writes `remotion/src/data/short<NN>_timing.ts` (`SHORT<NN>_TOTAL_SEC`, `LINE_WINDOWS`, `SHORT<NN>_CAPTIONS`) and the −14 LUFS mix into `remotion/public/shorts/short<NN>/audio/`. **Check `SHORT<NN>_TOTAL_SEC` ≤ 58**; if over, re-run step 3 with `--gap 0.45`.
   > Volume: `build_short_mix.py` already carries the speechnorm + glue-compressor + 2-pass static −14 chain added at short17 — do not bypass it.

**B. Visuals**

5. Copy the chosen stills and rename sequentially:
   ```bash
   cp H:/pd-media/assets/ai/<slug>/S055.png remotion/public/shorts/short<NN>/short<NN>_01.png   # etc.
   ```
   (This is exactly how `short57_01.png` = `norfolk/S009.png`.) EP54 i2v clips copy as-is from `H:/pd-media/assets/ai_video/flowers/M##_rife.mp4`.
6. Generate the depth maps required by the parallax treatment (**GPU step — not part of this planning task**):
   ```bash
   python scripts/gen_depth_maps.py --dir remotion/public/shorts/short<NN>
   ```
   Every `short<NN>_XX.png` needs a `short<NN>_XX_depth.png` beside it or the render crashes.
7. Write `remotion/src/data/short<NN>.ts` on the `short57.ts` pattern: a doc-comment carrying the sensitivity frame and the accuracy locks, `const ACCENT`, `const img`, and a `CUTS: Cut[]` array with `{line,id,src,kind,motion,telop,fast,art}` — including the trailing `{line:'L5', id:'loop', …}` beat that repeats the hook image and hook telop (METHOD rule 5).

7b. **Set the long-form funnel end-CTA props — MANDATORY for all 13 shorts in this slate.** Implemented in
   `Short.tsx` on 2026-07-28 (`SHORTS_CONVERSION_v001.md` §4, gap G2 closed). Three optional fields on the
   `SHORT<NN>: ShortData` object; supplying **any one** of them replaces the bare `SUBSCRIBE` end-card with
   the long-form card. Omit all three and the Short renders exactly as it did before — so `short57`/`58`/`59`
   are unaffected until someone adds them.

   | prop | required here | rule |
   |---|---|---|
   | `ctaLongThumbSrc` | ✅ | matching long-form's thumbnail, path under `remotion/public`, **16:9 (1280×720)**. Convention: `shorts/short<NN>/short<NN>_ctathumb.png` |
   | `ctaLongTitle` | ✅ | shortened long-form title, **one line, ≤ 36 ASCII chars** (auto-shrinks to a 34 px floor if longer) |
   | `ctaHeadline` | optional | defaults to `'FULL CASE'`. UPPERCASE, ≤ 2 words, ≤ 12 chars |

   ```ts
   export const SHORT60: ShortData = {
     shortId: 'short60',
     // …existing fields unchanged…
     ctaLongThumbSrc: 'shorts/short60/short60_ctathumb.png',
     ctaLongTitle: 'They Fixed the Confession',
     ctaHeadline: 'FULL CASE',
     beats: buildBeats(),
   };
   ```

   Notes: the component drops any caption cue that falls inside the `cta` beat (the card occupies the caption
   band), so no `short<NN>_timing.ts` surgery is needed; the loop-tail cue survives. The `-tt` cut swaps the
   pill to `▶ ON OUR PROFILE` automatically. The CTA beat length still comes from `LINE_WINDOWS` — the spec's
   fixed `CTA_SEC = 3.0` was **not** implemented (it would desync the narration); shape the CTA line's length
   in step 3 instead. `ctaTextYT` / `ctaTextTT` stay in the data file but are unused once these props are set.
8. Register three compositions in `remotion/src/Root.tsx` next to the `short59` block: `Short-short<NN>-yt`, `Short-short<NN>-tt`, and `Still ShortThumb-short<NN>` (1080×1920) with `headline` / `badge` / `backgroundSrc` from the cover concept.

**C. Render / package**

9. `cd remotion && npm run typecheck` — must be clean before any render.
10. `npx remotion still ShortThumb-short<NN> out/short<NN>_thumb.png`
11. `npx remotion render Short-short<NN>-yt out/short<NN>_yt.mp4 --crf=16`
    `npx remotion render Short-short<NN>-tt out/short<NN>_tt.mp4 --crf=16`
    > `remotion/public` is ~18 GB and is copied on every render. Build a minimal `--public-dir` containing only `shorts/short<NN>` for the still/thumb pass.
12. `bash scripts/coverfirst.sh <NN>` → `out/short<NN>_yt_coverfirst.mp4` (bakes the cover over the first 1.5 s so the Shorts feed's auto-picked cover frame is the bold one — the API cannot set a Shorts feed cover).
13. If the mix was regenerated after the render, re-mux rather than re-render: `ffmpeg -map 0:v -map 1:a` (Remotion sometimes serves a stale bundled `public` copy).

**D. Acceptance (before scheduling — self-report is not acceptance)**

14. Verify by measurement, not by claim: 1080×1920 / 30 fps / runtime ≤ 58 s (`ffprobe`); no static hold > 2.0 s; captions never enter the telop zone; every legal-lock telop present and unobstructed by `citation` art; no `SUBSCRIBE` string in frame; TikTok cut contains no external platform name.
15. **Eyes-on QC of every still at phone size** before scheduling — the factory-shelf mislabel incident and the SDXL fake-text/fake-seal trap both slipped past machine gates. Any plate showing readable typography or an official-looking seal is rejected and replaced.

**E. Publish**

16. `python scripts/schedule_short_youtube.py --short NN --publish-at <UTC>` (12:00 JST = 03:00 UTC), after adding the short's metadata to that script's `CONFIG` dict. Privacy `private` + future `publishAt`.
17. **Hold** the pinned comment (`scripts/post_short_pinned_comments.py`, dry-run first) and the Studio Related-video link until the matching long-form is public (§6).

---

## 8. Gaps that would block a build

| # | Gap | Impact | Fix |
|---|---|---|---|
| **G1** | **EP53 `F001`–`F012` emotive faces were never generated** (specified in `EP53_norfolk_CODEX_A_ASSETS.v001.md` §5.13; 0 files on disk). | METHOD rule 7 (faces + emotion in hook and payoff) is only partly met for `short60`/`short61`/`short62`. EP54 has 15 face plates, EP55 has 15; EP53 has 3 (thumb-only, face pushed to a horizontal third, poor 9:16 centre crop). | Codex-generate the 12 `F###.png` from the existing prompt block. Not a hard blocker — the three EP53 shorts are buildable without them. |
| **G2** | ~~**`Short.tsx` still renders `SUBSCRIBE`** and `ShortData` has no `ctaLongThumbSrc` / `ctaLongTitle` / `ctaHeadline`.~~ **✅ CLOSED 2026-07-28.** | — | **Implemented** in `remotion/src/compositions/Short.tsx`: §4-2 props + §4-3 timeline + §4-4 layout, `SUBSCRIBE` gone from the new path, backward-compatible (byte-identical stills when the props are absent, `tsc` 0 errors). Deviations recorded in `SHORTS_CONVERSION_v001.md` §4 "✅ IMPLEMENTED". **All 13 shorts must now set the props per §7 step 7b** — the component does not funnel by itself. |
| **G3** | **EP56 has no VO master and no narration index.** TTS was gated to the 2026-07-28 18:08 quota reset. | All four EP56 shorts are 100 % re-record (~474 words). No line can be cut from a master that does not exist. | Run the EP56 long-form TTS, or accept the four shorts as standalone recordings (~474 w ≈ 2,700 chars ≈ $0.81 — trivial, and it unblocks 8/29–9/01 without waiting for the episode). |
| **G4** | **EP56 stills stop at `S067`** — 200 of 267 missing, including all 12 `F###` faces, all 3 `T##_face` thumb plates and all 42 `M##_src` motion seeds. | `short72`'s true payoff plate (Fenny Compton village hall, ACT 4 `S129`–`S166`) does not exist — substituted. No face-forward plate exists for any EP56 short or its cover. | Resume the Codex generation run. `short69`/`short70`/`short71` are buildable from `S001`–`S067` as listed; only `short72` carries a substitution. |
| **G5** | **`build_shorts_hero_cards.py` and `composite_shorts_hero.py` — referenced in `SHORTS_METHOD.v001.md` §BUILD INTEGRATION — do not exist in `scripts/`.** | The method document points at AE hero-beat tooling that was never committed. Following it literally will fail. | The working path is the `short57`–`short59` one documented in §7 (`gen_newshort_narration.py` → `build_short_mix.py` → `short<NN>.ts` → Root.tsx → render → `coverfirst.sh`). Correct `SHORTS_METHOD.v001.md` §BUILD INTEGRATION to match. |
| **G6** | **No i2v motion clips for EP53, EP55 or EP56** (`H:\pd-media\assets\ai_video\` has `flowers` with 44 clips; `postoffice` exists but is **empty**; `norfolk` and `burge` do not exist). | Only the three EP54 shorts can meet the "real motion, not Ken Burns" bar with actual video. EP53/EP55/EP56 rely on depth-parallax + fast cutting on stills — the owner has previously rejected zoom-on-still as 紙芝居. | Either run Wan i2v on the existing `M##_src.png` seeds (EP53: 42, EP55: 42 — both already on disk) or accept a higher cut rate (beat length ≤ 1.6 s) plus `ShortArt` code layers on those nine shorts. |
| **G7** | **No long-form for EP53–56 is built or scheduled.** | The short→long funnel — the entire reason this slate exists — has no destination. | Do not post pinned comments / Related-video links until each long-form is public. Shorts can still be scheduled; they simply run as reach-only until the destination exists. |

---

## 9. Totals

- **13 new shorts** — EP53 ×3 (`short60`–`short62`), EP54 ×3 (`short63`–`short65`), EP55 ×3 (`short66`–`short68`), EP56 ×4 (`short69`–`short72`). With the already-built `short57`/`short58`/`short59`, that is **4 shorts per episode** for EP53–55 and 4 for EP56.
- **Audio cut from existing masters:** **27 of the 46 lines** across the 9 EP53–55 shorts — **5 minutes 31 seconds** of already-paid-for ElevenLabs narration reused at zero cost.
- **Re-recorded audio:** **874 words total** — **400 w** across the nine EP53–55 shorts (hooks, CTAs and three bridges only: 46 / 41 / 43 / 65 / 34 / 65 / 26 / 38 / 42), plus **474 w** for the four EP56 shorts (full VO — no master exists). ≈ 5,000 characters ≈ **$1.50** at the pipeline's $0.30/1k-char estimate.
- **Schedule:** 2026-08-14 → 2026-09-01, one per day at 12:00 JST, zero collisions with the 27 reservations already on the channel.
