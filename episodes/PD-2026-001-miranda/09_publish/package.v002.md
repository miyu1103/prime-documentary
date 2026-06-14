# YouTube publish package — PD-2026-001-miranda (v002, consolidated)

Episode: **PD-2026-001-miranda** · working title "Why Do Police Read You Your Rights?"
Channel: 1 (US court cases, English) · State target: `package_ready` → `publish_approved`
Owner approvals so far: script (APR-0001); **thumbnail concept A (approved 2026-06-14)**;
final thumbnail file + title/desc + publish = **pending owner approval** (gates per rule 16, §N).

English is the shipping language; Japanese notes are review-only (decisions/0002 §H), never rendered.

---

## 1. Title

- **Primary (use this):** `Why Do Police Read You Your Rights?`
  - Recognition + search demand; question format; pairs with the surprise thumbnail.
- Alternates (A/B test later):
  - `The Confession the Supreme Court Threw Out`
  - `He Won at the Supreme Court — and Still Went to Prison`

> JA: 検索される"認知"のタイトル。サムネが"驚き"なので補完ペアになる。

## 2. Thumbnail (concept A — approved)

- Text: **`WON.`** (white) / **`STILL JAILED.`** (gold), kicker `MIRANDA v. ARIZONA`,
  sub `How 4 words rewrote every U.S. arrest`.
- Background: a dark, symbolic **cell / prison-bars with cold blue light** Midjourney still
  (no real person), placed behind via `ThumbConcept` `backgroundSrc`.
- Brand colours: ink/navy + electric blue + gold; mobile-legible; one focal point.
- Render: `npx remotion still ThumbConcept out/thumb_final.png --props='{"kicker":"MIRANDA v. ARIZONA","line1":"Won.","line2":"Still jailed.","sub":"How 4 words rewrote every U.S. arrest","symbol":"bars","backgroundSrc":"thumb_bg.jpg"}'`
- Title↔thumbnail are **complementary** (no repeated words): thumbnail = the surprise, title = the recognition.

> JA: 文言は確定。あとは後ろに実画像を敷いて最終ファイルを書き出し、オーナーが実物を最終承認。

## 3. Description (概要欄 — ships in English)

```
You've heard it in a thousand movies: "You have the right to remain silent."
But those words weren't written by a screenwriter. They come from a single
confession the U.S. Supreme Court refused to allow — given by a man who won at
the highest court in the country and still ended up back in prison.

This is Miranda v. Arizona (1966): how four plain sentences quietly rewrote
every arrest in America, why the Court built them, and the twist most people
never learn about the man whose name they carry.

⏱ Chapters
00:00 The line you already know
(timestamps auto-filled from the final cut)
— A repair, not a courtesy
— Phoenix, 1963: the interrogation
— Why a confession isn't always proof
— Four cases, one question
— The ruling: June 13, 1966
— The four warnings
— The twist: he won, then went back to prison
— Why it still shapes every arrest

📚 Source
Miranda v. Arizona, 384 U.S. 436 (1966).
Full opinion: https://www.loc.gov/item/usrep384436/

ℹ️ About this video
Independent educational documentary. Narration is AI-generated. Historical
moments that were never filmed are shown as clearly labeled symbolic
reconstructions — not authentic footage. This explains how the law works and
is not legal advice.

▶ Next: who even gets a lawyer? — Gideon v. Wainwright.
👉 Subscribe for the hidden systems behind everyday life.

#MirandaRights #SupremeCourt #USLaw
```

> JA: 頭2行が"上に出る"部分＝ここで掴む。チャプター時刻は最終尺から自動で埋める。

## 4. Chapters (titles; timestamps from final cut, each ≥10s, first at 0:00)

1. `00:00` The line you already know — *(hook)*
2. A repair, not a courtesy — *(thesis)*
3. Phoenix, 1963: the interrogation
4. Why a confession isn't always proof
5. Four cases, one question
6. The ruling: June 13, 1966
7. The four warnings
8. The twist: he won, then went back to prison
9. Why it still shapes every arrest — *(close + next)*

## 5. Tags (15)

miranda rights, miranda v arizona, you have the right to remain silent, supreme court,
ernesto miranda, fifth amendment, miranda warning, police interrogation,
landmark supreme court cases, us law explained, constitutional rights, criminal justice,
history documentary, legal history, know your rights

## 6. Pinned comment (engagement)

```
Four sentences from one 1966 case — and the man whose name they carry still went to
prison. Which part surprised you most? (And: should the warning exist at all?)
```

## 7. End screen / cards

- End screen (last ~15s): **Subscribe** element + **Next video** (Gideon, when published) + best-for-viewer.
- Card mid-roll: link to the channel / playlist "Landmark Rights Cases".

## 8. Publish settings

- Visibility: **Private** now → scheduled/public **only after owner publish-approval** (§N gate).
- Audience: **Not made for kids** (COPPA).
- Language: **English (United States)**; video + audio language = English.
- Category: **Education**.
- Comments: on, hold potentially inappropriate for review.
- License: Standard YouTube.
- Monetization: on once channel is eligible.
- Playlist: "Landmark Rights Cases" (series threading, §K).

## 9. Safety / non-termination checklist (publish-gated, §N)

- [ ] AI / synthetic-content **disclosure** set + on-screen "symbolic reconstruction" labels (invariant 11).
- [ ] **Not made for kids** flag set.
- [ ] **No legal advice / no misinformation** — every on-screen claim cited (claim ledger graded).
- [ ] **Rights manifest** complete: every real asset (audio/video/stills) has `rights_basis` +
      `source` + `verified_at`; no unlicensed third-party footage; music/SFX commercial-cleared.
- [ ] **Title ⇄ thumbnail ⇄ content** match (no clickbait/misrepresentation).
- [ ] Advertiser-friendly: neutral educational tone, no gore/shock.
- [ ] Final cut hash recorded; approval targets the exact revision (rule 12).

## 10. Approval status

- ✅ Script approved (APR-0001).
- ✅ Thumbnail **concept A** approved (owner, 2026-06-14).
- ⬜ Final thumbnail **file** (with real background) — owner to approve actual image.
- ⬜ Title + description — owner sign-off.
- ⬜ First-cut review (watch `sample_v0xx.mp4`) — owner.
- ⬜ Publish (visibility change) — owner, after §9 fully passes.
