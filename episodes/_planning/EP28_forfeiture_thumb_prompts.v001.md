# EP28 `thumb_prompts.v001` — Codexサムネ背景アート＋見出し（民事没収）

**Episode:** `PD-2026-028-forfeiture`（rows 11–13）
**方針**：AIが作るのは**背景アートのみ（画像内に文字を入れない）**。見出し文字はRemotion `<Still>` で載せる（`BRAND.thumb`・1280×720）。**≥3枚＋selected**。
**共通ビジュアル（全案）**：1280×720想定・**巨大主題・超高コントラスト・黒/深ネイビー背景**・アクセントは**gold `#E5B53A` か electric `#1F6BFF` の1色だけ**・シネマティック・320pxで映える・**実在人物の顔なし・画像内テキストなし・ロゴなし**・見出しを載せる**ネガティブスペースを残す**構図。
**共通ネガティブ**：`no readable text, no lettering, no logos, no watermark, no real person or celebrity likeness, no identifiable face, no clutter, no low-contrast, bad anatomy`。

---

## 背景アート案（1案ずつCodexへ・出力1280×720・上部か片側に文字用余白）
**T1（THEY TOOK THE HOUSE）**
> A modest brick row house at night dominating the frame, drenched in deep navy shadow, a hard **gold** police-style glow raking across it from one side, a single ominous seal/mark on the front door. Huge, high-contrast, cinematic, empty sky area top-left for a headline. No text, no faces.

**T2（$40 → YOUR HOME）**
> Split composition: on the left, two twenty-dollar bills tiny in a dark hand; on the right, a locked front door of a home looming huge; deep black gutter between them for an implied arrow. Navy base, one **electric blue** accent line. High contrast, negative space top for headline. No text, no faces.

**T3（NO CRIME. NO HOUSE.）**
> A cold empty courtroom bench in heavy shadow with a single house key resting on it under a hard spotlight, **gold** rim light, vast dark negative space above for a headline. Dramatic, minimal, high contrast. No text, no faces.

**T4（THE CITY TOOK IT）**
> A heavy padlock and chain across an ordinary family front door, shot huge and close, cold navy tones with a single **gold** glint on the lock, menacing, lots of dark space to the right for a headline. No text, no faces.

**T5（LEGAL ROBBERY）**
> A judge's gavel looming in the foreground casting a long hard shadow over a tiny lone house behind it, forced perspective, deep black background, one **electric blue** edge light, bold and graphic. Headline space across the top. No text, no faces.

---

## 見出し候補（Remotionで載せる・UPPERCASE ≤4語・巨大・白/銀＋アクセント）
- `THEY TOOK THE HOUSE`
- `$40 → YOUR HOME`
- `NO CRIME. NO HOUSE.`
- `LEGAL ROBBERY`
- `THE CITY TOOK IT`

## タイトル（≤60字・フック先頭・A/B）
- **A** `They Took Their House Over $40 — And Never Charged Anyone`
- **B** `The City Tried to Seize a Family's Home for a $40 Crime`

## selected（初期推奨）
- **背景=T1／見出し=`THEY TOOK THE HOUSE`／タイトル=A**（"家を奪う"の一撃が最も強い）。A/Bは T1×A と T3×`NO CRIME. NO HOUSE.`×B で出し分け。
- 最終は**実物を320pxで見て派手さ・可読を確認**（row12手動）＋promise-payoff（本編が見出しを裏切らない）を担保。
