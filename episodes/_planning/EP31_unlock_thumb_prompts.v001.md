# EP31 `thumb_prompts.v001` — Codexサムネ背景アート＋見出し（スマホ強制解除）

**Episode:** `PD-2026-031-unlock`（rows 11–13）
**方針**：AIが作るのは**背景アートのみ（画像内に文字を入れない）**。見出し文字はRemotion `<Still>` で載せる（`BRAND.thumb`・1280×720）。**≥3枚＋selected**。
**CTR目標**：現状 **2.31%（実測）→ 6%**（`docs/PD_WINNING_PATTERN.md`）。二人称の脅威1アイデア・320pxで可読を最優先。
**共通ビジュアル（全案）**：1280×720想定・**巨大主題・超高コントラスト・黒/深ネイビー背景**・アクセントは**gold `#E5B53A` か electric `#1F6BFF` の1色だけ**・シネマティック・320pxで映える・**実在人物の顔なし・実機ロゴ/OS UIなし・画像内テキストなし・ロゴなし**・見出しを載せる**ネガティブスペースを残す**構図。
**共通ネガティブ**：`no readable text, no lettering, no numbers, no brand logos, no phone OS interface, no watermark, no real person or celebrity or judge likeness, no identifiable face, no clutter, no low-contrast, bad anatomy`。

---

## 背景アート案（1案ずつCodexへ・出力1280×720・上部か片側に文字用余白）
**T1（THEY CAN FORCE YOUR THUMB）**
> Extreme close-up: an anonymous hand with a metal handcuff at the wrist, its thumb pressed hard onto a blank glowing phone sensor, cold **electric blue** unlock-glow exploding from the screen against a near-black background. Huge, high-contrast, menacing. Empty dark space top-left for a headline. No text, no faces, no logos.

**T2（FACE ID = NO RIGHTS?）**
> A cold **electric blue** face-scan grid of light raking across an anonymous profile emerging from deep black shadow, only cheekbone and one eye lit, biometric and unsettling. Vast negative space on the right for a headline. No text, no faces recognizable, no logos.

**T3（YOUR PASSCODE > FACE ID）**
> Split composition on black: left, an anonymous face half-lit by cold blue scan light; right, a closed antique safe dial catching a single **gold** rim-light; a bold gold "greater-than" wedge of light implied in the dark gutter between them. High contrast, headline space across the top. No text, no logos.

**T4（YOUR PHONE. THEIR RULES.）**
> A single featureless smartphone glowing cold blue, gripped by an anonymous hand, with a hard **gold** police-style light raking in from one side and red-and-blue bleed in the deep background. Huge and central, lots of dark space to the right for a headline. No text, no logos.

**T5（THE MIND IS THE LAST LOCK）**
> A heavy antique safe combination dial in deep shadow, one dramatic **gold** rim-light on the dial, a faint cold-blue glow behind like a screen, forced perspective making it loom. Vast black negative space above for a headline. Minimal, cinematic. No text, no faces.

---

## 見出し候補（Remotionで載せる・UPPERCASE ≤4語・巨大・白/銀＋アクセント）
- `THEY CAN FORCE YOUR THUMB`
- `FACE ID = NO RIGHTS?`
- `YOUR PASSCODE > FACE ID`
- `YOUR PHONE. THEIR RULES.`
- `CAN THEY FORCE IT OPEN?`

## タイトル（≤60字・フック先頭・A/B）
- **A** `Police Can Force Your Thumb — But Maybe Not Your Mind`
- **B** `Can the Police Force You to Unlock Your Phone?`

## selected（初期推奨）
- **背景=T1／見出し=`THEY CAN FORCE YOUR THUMB`／タイトル=A**（手錠＋強制解除の一撃が最も"自分事の脅威"）。A/Bは **T1×A** と **T3×`YOUR PASSCODE > FACE ID`×B**（逆説の学び系）で出し分け。
- 最終は**実物を320pxで見て派手さ・可読を確認**（row12手動）＋promise-payoff（本編が見出しを裏切らない＝"force your thumb"は Payne(9th) に基づく事実）を担保。**「顔=無権利」は断定でなく "?" 付きに留める**（fact_recheck の MYTHS 準拠）。
