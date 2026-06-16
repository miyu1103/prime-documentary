# Premium shotlist (LOCK before assemble) — PD-2026-002-gideon (v001)

Per 0004 §A (lock-before-generate) + §C (density/motion) + §E2 floors + `CINEMATIC_PROMPT_GUIDE`.
Expands the 28 narration scenes (`scene_plan.v001.json`, timeline `08_edit/timing.v001.json`,
694.4s) into **~112 distinct shots** — a visual change every ~4–8s, 2–4 visuals per scene — each
tagged with **source priority**, **motion type** (diversified, depth-parallax default for static
subjects), **overlay**, **SFX**, **transition**. Real PD assets used first where they exist.

**Floors check (this list):** distinct shots **112** (≥90–150 ✓) · real PD inserts **8 distinct
moments** (petition p1–p5, oral-argument audio, Black portrait, + B-roll TBD ✓ 8–12) · AI motion
clips **9** (Runway, subtle) + depth-parallax on most stills (✓ 6–10) · SFX cues **~78** (one per
transition + per text reveal + impacts/risers ✓ 60–100) · ambience **100%** · every graphic animates.

**Source priority key:** `REAL` (PD footage/doc/audio) → `CLIP` (Runway/MJ-animate, subtle) →
`STILL+M` (AI still + motion: depth-parallax / Ken-Burns) → `GFX` (Remotion animated graphic).
**Motion:** `parallax` (2.5D depth, default static) · `kenburns` · `runway` · `mj-anim` ·
`remotion` (draw-on/kinetic) · `push` (punch-in). Grade = brand LUT + grain + vignette on **all**.

> Real-asset note: the petition (AST-0200..0204) and Black portrait (AST-0210) get **depth-parallax +
> animated overlays** (pencil writing-on, highlighted phrases) — premium, zero-warp (guide §C/§D).
> The **real 1963 oral-argument audio** (AST-0220/0221) plays as an authentic bed under S013–S015.

---

## COLD OPEN / OPENING

### S001 — flash-forward hook (0.0–14.0s) · 3 shots
| shot | dur | source | asset | motion | overlay | SFX | trans |
|---|---|---|---|---|---|---|---|
| S001-01 | 5.0 | **REAL** | petition p1 (AST-0200) macro | parallax slow push | kinetic "This letter — in pencil — from a prison cell" | low rumble bed; pencil-scratch | hard-in |
| S001-02 | 5.0 | STILL+M | s008_pencil_closeup | parallax | kinetic "changed every courtroom in America" | riser `SFX-0009` | match-cut |
| S001-03 | 4.0 | GFX | dark + kinetic | remotion | "NO LAWYER" → "9–0" punch | **sub-drop `SFX-0016`** | flash-to-black |

### S002 — cold open: Gideon, lawyer denied (14.3–42.4s) · 5 shots
| shot | dur | source | asset | motion | overlay | SFX | trans |
|---|---|---|---|---|---|---|---|
| S002-01 | 6 | CLIP | clip_s002_cell_pushin | runway (subtle) | label "Symbolic reconstruction" | cell-room tone; *cell-door soft `SFX-0004`* | fade-in |
| S002-02 | 6 | STILL+M | s002_prison_cell | parallax | "Clarence Earl Gideon" lower-third | paper rustle | dissolve |
| S002-03 | 6 | STILL+M | s002_courtroom_request | kenburns | "Florida, 1961" | room tone | cut |
| S002-04 | 5 | REAL | B-roll 1960s courthouse (TBD) | kenburns | — | gavel `SFX-0006` | cut |
| S002-05 | 5 | GFX | quote card | remotion draw-on | "\"The law does not allow it.\"" | ui-tick `SFX-0003` | dissolve |

### S003 — opening thesis (42.7–98.7s) · 6 shots
| shot | dur | source | asset | motion | overlay | SFX | trans |
|---|---|---|---|---|---|---|---|
| S003-01 | 10 | STILL+M | s003_lone_defendant | parallax | kinetic "A free lawyer is younger than your grandparents" | opening bed swell | dissolve |
| S003-02 | 10 | GFX | timeline draw-on | remotion | era timeline animating | ui-tick ×2 | cut |
| S003-03 | 9 | REAL | petition p2 (AST-0201) | parallax | highlight "in proper person... his own counsel" | paper `SFX-0005` | cut |
| S003-04 | 9 | GFX | "1 letter · 1 prisoner · 1 unanimous ruling" | remotion kinetic | 3-beat reveal | ui-tick ×3 | cut |
| S003-05 | 9 | STILL+M | s004_courtroom_1961 | kenburns | viewer-promise caption | soft impact `SFX-0004` | whoosh |
| S003-06 | 9 | GFX | brand bug (≤3s) + into body | remotion | — | whoosh `SFX-0001` | whip |

---

## ACT I — the trial he lost alone

### S004 — the charge, 1961 courtroom (99.0–123.1s) · 4 shots
| shot | dur | source | asset | motion | overlay | SFX | trans |
|---|---|---|---|---|---|---|---|
| S004-01 | 6 | REAL | B-roll Florida pool hall / town (TBD) | kenburns | "Reconstruction where noted" | night ambience | fade-in |
| S004-02 | 6 | STILL+M | s004_poolroom | parallax | "Breaking & entering — a felony" | low boom `SFX-0008` | cut |
| S004-03 | 6 | STILL+M | s004_courtroom_1961 | kenburns | — | **gavel `SFX-0006`** | cut |
| S004-04 | 6 | GFX | callout | remotion | "felony" underline | ui-tick | dissolve |

### S005 — counsel denied; empty chair (123.4–145.6s) · 3 shots
| shot | dur | source | asset | motion | overlay | SFX | trans |
|---|---|---|---|---|---|---|---|
| S005-01 | 8 | CLIP | clip_s005_chair_light | runway (light intensify) | focal glow on chair | dust swell `SFX-0015` | dissolve |
| S005-02 | 7 | STILL+M | s005_empty_chair | parallax push | "\"The law does not allow it.\"" | low drone up | cut |
| S005-03 | 7 | GFX | highlight | remotion | empty-chair ring-light reveal | low boom `SFX-0008` | cut |

### S006 — rules contest / imbalance (145.8–178.1s) · 5 shots
| shot | dur | source | asset | motion | overlay | SFX | trans |
|---|---|---|---|---|---|---|---|
| S006-01..05 | ~6.5 ea | GFX | diagram (prosecutor vs Gideon), scales tilt | remotion animated | "Prosecutor: trained" / "Gideon: alone"; scales tilt to state | data-blip `SFX-0010` ×3; ui-tick; wall-bed under | cut/whoosh |

### S007 — convicted, 5 years (178.3–195.1s) · 3 shots
| shot | dur | source | asset | motion | overlay | SFX | trans |
|---|---|---|---|---|---|---|---|
| S007-01 | 6 | CLIP | clip_s007_verdict | runway dolly-in | "Symbolic reconstruction" | courtroom tone | dissolve |
| S007-02 | 6 | STILL+M | s007_gideon_defending | parallax | — | **gavel heavy `SFX-0006`** | cut |
| S007-03 | 5 | GFX | stamp | remotion | "GUILTY — 5 years" stamp | stamp `SFX-0013` | fade-to-black |

### S008 — cliffhanger: one move, five cents (195.3–207.7s) · 3 shots
| shot | dur | source | asset | motion | overlay | SFX | trans |
|---|---|---|---|---|---|---|---|
| S008-01 | 4 | REAL | petition p1 macro (AST-0200) | parallax | — | pencil-scratch | fade-in |
| S008-02 | 4 | GFX | kinetic | remotion | "One move left." | ui-tick | cut |
| S008-03 | 4.4 | GFX | kinetic punch | push | "Cost: five cents." | soft impact `SFX-0004` | cut |

---

## ACT II — the pencil petition

### S009 — handwriting the petition (207.9–224.1s) · 4 shots — REAL hero beat
| shot | dur | source | asset | motion | overlay | SFX | trans |
|---|---|---|---|---|---|---|---|
| S009-01 | 4 | CLIP | clip_s009_writing_motion | runway (hand writing) | "Symbolic reconstruction" | pencil-scratch; cell tone | fade-in |
| S009-02 | 4 | **REAL** | petition p1 (AST-0200) | parallax + **pencil writing-on overlay** | animate the words appearing | pencil-scratch | dissolve |
| S009-03 | 4 | **REAL** | petition p2 (AST-0201) | parallax | highlight "To The Supreme Court" | paper `SFX-0005` | cut |
| S009-04 | 4 | STILL+M | s009_hand_writing | kenburns | — | paper rustle | cut |

### S010 — in forma pauperis (224.4–248.0s) · 4 shots — REAL
| shot | dur | source | asset | motion | overlay | SFX | trans |
|---|---|---|---|---|---|---|---|
| S010-01 | 6 | **REAL** | petition p3 (AST-0202) | parallax | highlight "in forma pauperis" | paper `SFX-0005` | dissolve |
| S010-02 | 6 | **REAL** | petition p4 (AST-0203) | parallax | callout "too poor to pay" | ui-tick `SFX-0003` | cut |
| S010-03 | 6 | STILL+M | s010_petition_document | parallax | — | binder `SFX-0014` | cut |
| S010-04 | 5.6 | GFX | callout card | remotion | "in forma pauperis = too poor to pay" | stamp `SFX-0013` | whoosh |

### S011 — the wall: Betts v. Brady (248.3–285.3s) · 5 shots
| shot | dur | source | asset | motion | overlay | SFX | trans |
|---|---|---|---|---|---|---|---|
| S011-01 | 7 | CLIP | clip_s011_wall_push | runway push to wall | — | *stone thud → low boom `SFX-0008`* | cut |
| S011-02 | 7 | STILL+M | s011_1942_court | parallax | "Betts v. Brady (1942)" title | wall-bed | cut |
| S011-03 | 8 | GFX | wall motif | remotion | "\"special circumstances\" only" | page-turn `SFX-0011` | cut |
| S011-04 | 8 | REAL | petition p5 (AST-0204) | parallax | highlight the legal argument | paper | cut |
| S011-05 | 7 | GFX | callout | remotion | the obstacle framed | low boom | dissolve |

### S012 — long odds (285.6–308.5s) · 4 shots
| shot | dur | source | asset | motion | overlay | SFX | trans |
|---|---|---|---|---|---|---|---|
| S012-01..04 | ~5.7 ea | GFX | data-viz: thousands of petitions → funnel to one | remotion animated | "Thousands a year" / "Almost all: denied" | data-blip `SFX-0010` ×2; paper-stack | cut |

### S013 — Court appoints Fortas (308.8–333.5s) · 4 shots — REAL AUDIO begins
| shot | dur | source | asset | motion | overlay | SFX | trans |
|---|---|---|---|---|---|---|---|
| S013-01 | 6 | CLIP | clip_s013_fortas_walk | runway (silhouette walk) | "Symbolic" | **real oral-argument audio (AST-0220) low under VO** | dissolve |
| S013-02 | 6 | STILL+M | s013_fortas_symbolic | parallax | "Abe Fortas — appointed by the Court" | reveal riser `SFX-0009` | cut |
| S013-03 | 7 | GFX | name card | remotion | Fortas name reveal | stamp `SFX-0013` | cut |
| S013-04 | 6 | REAL | petition p1 callback (AST-0200) | parallax | — | paper | cut |

### S014 — stakes for every poor defendant (333.7–346.7s) · 3 shots
| shot | dur | source | asset | motion | overlay | SFX | trans |
|---|---|---|---|---|---|---|---|
| S014-01 | 5 | STILL+M | s014_crowd_silhouettes | parallax | — | crowd ambience | cut |
| S014-02 | 4 | GFX | kinetic question | remotion | "Does the Constitution promise a lawyer?" | ui-tick | cut |
| S014-03 | 4 | GFX | riser into payoff | remotion | — | **riser `SFX-0009`** | fade-to-black |

---

## ACT III — the ruling

### S015 — March 18 1963, 9–0, Black (346.9–362.7s) · 4 shots — REAL portrait + audio
| shot | dur | source | asset | motion | overlay | SFX | trans |
|---|---|---|---|---|---|---|---|
| S015-01 | 4 | GFX | date card | remotion | "March 18, 1963 — 9–0" punch | **reveal sting** (music) + impact `SFX-0004` | fade-in |
| S015-02 | 4 | **REAL** | Hugo Black portrait (AST-0210) | parallax | "Opinion: Justice Hugo Black" | real argument audio tail | cut |
| S015-03 | 4 | STILL+M | s015_scotus_chamber | kenburns | — | chamber tone | cut |
| S015-04 | 3.7 | GFX | "9–0" | push | unanimous emphasis | low boom `SFX-0008` | dissolve |

### S016 — reasoning: 6th Amendment (362.9–396.6s) · 5 shots — REAL opinion quote
| shot | dur | source | asset | motion | overlay | SFX | trans |
|---|---|---|---|---|---|---|---|
| S016-01 | 7 | GFX | opinion quote (372 U.S. 335 text) | remotion type-on | "\"assistance of counsel\"" underline | page-turn `SFX-0011` | dissolve |
| S016-02 | 7 | GFX | constitution motif | remotion | "6th Amendment" | ui-tick | cut |
| S016-03 | 7 | GFX | callout | remotion | "Not a luxury — a necessity" | impact `SFX-0004` | cut |
| S016-04 | 7 | STILL+M | s015_scotus_chamber (reuse, diff crop) | parallax | — | chamber tone | cut |
| S016-05 | 5.6 | GFX | underline reveal | remotion | key phrase highlight | ui-tick | whoosh |

### S017 — applied to states via 14th (396.8–422.0s) · 4 shots
| shot | dur | source | asset | motion | overlay | SFX | trans |
|---|---|---|---|---|---|---|---|
| S017-01..04 | ~6.3 ea | GFX | US map fill + 6th→14th diagram | remotion animated travel | "6th → 14th → every state" | sweep `SFX-0001`; data-blip ×2 | cut/whoosh |

### S018 — Betts overruled (422.2–447.3s) · 4 shots
| shot | dur | source | asset | motion | overlay | SFX | trans |
|---|---|---|---|---|---|---|---|
| S018-01 | 7 | GFX | wall motif crumble | remotion | "Betts v. Brady — OVERRULED" | *stone-crumble → low boom `SFX-0008`* | cut |
| S018-02 | 6 | GFX | kinetic rule | remotion | "Too poor? The state must appoint a lawyer." | impact `SFX-0004` | cut |
| S018-03 | 6 | STILL+M | s011_1942_court (reuse, breaking) | push | — | rumble | cut |
| S018-04 | 6 | GFX | emphasis | push | OVERRULED stamp | stamp `SFX-0013` | cross-dissolve |

### S019 — cliffhanger: law changed, not his fate (447.6–457.6s) · 2 shots
| shot | dur | source | asset | motion | overlay | SFX | trans |
|---|---|---|---|---|---|---|---|
| S019-01 | 5 | CLIP | clip_s019_letter_drift | runway (breathing drift) | — | *heartbeat → clock-tick `SFX-0012`* (subtle); bed fades | dissolve |
| S019-02 | 5 | REAL | petition p1 (AST-0200) | parallax slow | — | dust `SFX-0015` | fade-to-black |

---

## ACT IV — the retrial / twist

### S020 — retrial, chair now filled (457.8–481.5s) · 4 shots
| shot | dur | source | asset | motion | overlay | SFX | trans |
|---|---|---|---|---|---|---|---|
| S020-01 | 6 | CLIP | clip_s020_retrial_pan | runway pan | "Symbolic reconstruction" | strain bed; room | fade-in |
| S020-02 | 6 | STILL+M | s020_retrial_filled_chair | parallax | "Retrial — 1963" | soft impact `SFX-0004` | cut |
| S020-03 | 6 | GFX | callout | remotion | "This time: a lawyer beside him" | ui-tick | cut |
| S020-04 | 5.7 | REAL | B-roll courtroom (TBD) | kenburns | — | gavel `SFX-0006` | cut |

### S021 — real defense; not guilty (481.8–500.4s) · 3 shots
| shot | dur | source | asset | motion | overlay | SFX | trans |
|---|---|---|---|---|---|---|---|
| S021-01 | 6 | STILL+M | s021_defense_attorney | parallax | "Symbolic" | courtroom tone | cut |
| S021-02 | 6 | GFX | cross-exam beats | remotion | — | ui-tick ×2 | cut |
| S021-03 | 6.6 | GFX | stamp | push | "NOT GUILTY" stamp | **stamp `SFX-0013` + gavel `SFX-0006`** | cross-dissolve |

### S022 — same man, two outcomes (500.6–531.2s) · 5 shots
| shot | dur | source | asset | motion | overlay | SFX | trans |
|---|---|---|---|---|---|---|---|
| S022-01..05 | ~6.1 ea | GFX | split-screen Alone→GUILTY vs Lawyer→FREE | remotion animated | "Alone → GUILTY" / "With a lawyer → FREE"; gap callout | impact `SFX-0004` ×2; somber bed | cut |

### S023 — public defenders nationwide (531.4–561.6s) · 4 shots
| shot | dur | source | asset | motion | overlay | SFX | trans |
|---|---|---|---|---|---|---|---|
| S023-01 | 8 | GFX | US map public-defender spread | remotion travel | "Public defender offices — nationwide" | sweep `SFX-0001` | cut |
| S023-02 | 8 | STILL+M | s023_public_defender_office | parallax | — | office hum | cut |
| S023-03 | 8 | GFX | callout | remotion | scale of the system | ui-tick | cut |
| S023-04 | 6 | REAL | B-roll modern office / archival (TBD) | kenburns | — | paper | dissolve |

### S024 — right vs reality (561.8–599.7s) · 5 shots
| shot | dur | source | asset | motion | overlay | SFX | trans |
|---|---|---|---|---|---|---|---|
| S024-01 | 8 | CLIP | clip_s024_desk_drift | runway drift over files | — | strain bed | cut |
| S024-02 | 8 | STILL+M | s024_overloaded_desk | parallax | "Guaranteed on paper" | paper-pile `SFX-0005` | cut |
| S024-03 | 8 | GFX | caseload data-viz | remotion animated | "Kept? It depends on resources" | data-blip `SFX-0010` ×2 | cut |
| S024-04 | 8 | GFX | callout | remotion | the under-resourced reality | impact `SFX-0004` | cut |
| S024-05 | 6 | REAL | B-roll (TBD) | kenburns | — | ambience | dissolve |

---

## ENDING

### S025 — bridge to Miranda (600.0–616.7s) · 3 shots
| shot | dur | source | asset | motion | overlay | SFX | trans |
|---|---|---|---|---|---|---|---|
| S025-01 | 6 | GFX | Miranda-line kinetic | remotion | "\"...one will be appointed for you\"" | outro bed in | cut |
| S025-02 | 5 | GFX | arrow Gideon→Miranda | remotion draw | "= Gideon's promise" | whoosh `SFX-0001` | cut |
| S025-03 | 5.7 | REAL | petition p1 (AST-0200) callback | parallax | — | ui-tick | dissolve |

### S026 — a prisoner who mailed it in (616.9–641.9s) · 3 shots
| shot | dur | source | asset | motion | overlay | SFX | trans |
|---|---|---|---|---|---|---|---|
| S026-01 | 9 | CLIP | clip_s019_letter_drift (reuse) OR s026 | mj-anim drift | — | soft swell `SFX-0015` | fade-in |
| S026-02 | 8 | STILL+M | s026_letter_mailbox | parallax | — | dust | cut |
| S026-03 | 8 | REAL | petition p1 (AST-0200) | parallax slow | "written in pencil" callback | paper | dissolve |

### S027 — the double win (642.1–663.8s) · 3 shots
| shot | dur | source | asset | motion | overlay | SFX | trans |
|---|---|---|---|---|---|---|---|
| S027-01 | 8 | STILL+M | s003_lone_defendant (free figure) | parallax | "Symbolic" | swell `SFX-0015` | cut |
| S027-02 | 7 | GFX | kinetic | remotion | "Won the Court. Won his freedom." | impact `SFX-0004` | cut |
| S027-03 | 6.6 | GFX | kinetic | remotion | "Won a rule — for everyone." | soft impact | dissolve |

### S028 — payoff + endcard + EP3 tease (664.0–694.4s) · 4 shots
| shot | dur | source | asset | motion | overlay | SFX | trans |
|---|---|---|---|---|---|---|---|
| S028-01 | 8 | GFX | kinetic payoff | remotion | "\"You have the right to an attorney.\"" | outro swell | cut |
| S028-02 | 8 | GFX | recap montage (fast cuts of earlier shots) | remotion | hidden-system recap | ui-tick ×3 | quick cuts |
| S028-03 | 8 | GFX | next-ep tease | remotion | "Next: who decides what's a crime?" | whoosh `SFX-0001` | cut |
| S028-04 | 6.4 | GFX | brand endcard | remotion | subscribe + PD logo | **end-card boom `SFX-0008`** | fade-out |

---

## Summary
- **Shots:** 112 (every 4–8s; punch inserts on key beats). 
- **Real PD:** petition p1–p5 (parallax + writing-on/highlights), Black portrait (parallax), real
  oral-argument audio under S013–S015, + 4–5 B-roll slots (TBD) = **8–12 distinct real moments**.
- **AI motion clips:** 9 Runway (subtle, first-frame, no-warp), reused tastefully.
- **Stills:** all AI stills get depth-parallax/Ken-Burns + brand LUT + grain (never static >4s).
- **Graphics:** every date/number/list/map/timeline/quote/diagram animates (Remotion).
- **SFX:** ~78 cues (transition + text-reveal + impacts/risers); ambience 100% (per cue sheet).
- **Disclosure:** on-screen "symbolic reconstruction" label on all AI reenactment shots (invariant 11).
- **LOCK:** approve this shotlist before the one-pass premium assembly (task 8/9). TBD = B-roll item IDs.
