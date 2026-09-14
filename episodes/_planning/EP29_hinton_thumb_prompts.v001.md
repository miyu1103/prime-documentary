# EP29 `thumb_prompts.v001` — Codexサムネ背景アート＋見出し（無実の死刑囚）

**Episode:** `PD-2026-029-hinton`（rows 11–13）
**方針**：AIが作るのは**背景アートのみ（画像内に文字を入れない）**。見出しはRemotion `<Still>` で載せる（`BRAND.thumb`・1280×720）。**≥3枚＋selected**。
**共通ビジュアル（全案）**：1280×720想定・**巨大主題・超高コントラスト・黒/深ネイビー背景**・アクセントは**gold `#E5B53A` か electric `#1F6BFF` の1色だけ**・シネマティック・320pxで映える・**実在人物の顔なし・画像内テキストなし・ロゴなし**・見出し用ネガティブスペースを残す構図。
**共通ネガティブ**：`no readable text, no lettering, no logos, no watermark, no specific real person or celebrity likeness, no identifiable face, no clutter, no low-contrast, bad anatomy, no gore`。

---

## 背景アート案（1案ずつCodexへ・出力1280×720・上部か片側に文字用余白）
**T1（30 YEARS. INNOCENT.）**
> A death-row cell's heavy steel door filling the frame in deep navy shadow, a single hard shaft of **gold** light breaking across it from one side, dust in the beam. Vast dark space top-left for a headline. Oppressive, then a sliver of hope. No text, no faces.

**T2（THEY WANTED HIM DEAD）**
> The silhouette of an empty electric chair in a dark chamber, cold and ominous, one thin **electric-blue** rim light along its edge, heavy negative space above. Menacing, restrained (no gore). No text, no faces.

**T3（THE BULLETS LIED）**
> Extreme macro of a single bullet on a steel surface, a cracked/shattered "match" graphic implied by a fracture of light across it, deep black background, one **gold** glint. Clinical and cold. Room to the right for a headline. No text, no faces.

**T4（NEARLY EXECUTED FOR NOTHING）**
> A five-by-seven death-row cell seen through bars, a lone shaft of daylight on the concrete floor, an anonymous figure's shadow (no face), navy tones with a single warm accent. Claustrophobic. Headline space top. No text, no faces.

**T5（ONE EYE. ONE BULLET.）**
> A comparison microscope in hard side light against black, one eyepiece catching a cold **electric-blue** glint, a bullet beneath it out of focus. The junk-science duel, visualized. Bold, graphic. No text, no faces.

---

## 見出し候補（Remotionで載せる・UPPERCASE ≤4語・巨大・白/銀＋アクセント）
- `30 YEARS. INNOCENT.`
- `THEY WANTED HIM DEAD`
- `THE BULLETS LIED`
- `NEARLY EXECUTED`
- `ONE EYE. ONE BULLET.`

## タイトル（≤60字・フック先頭・A/B）
- **A** `Thirty Years on Death Row — For a Crime He Never Committed`
- **B** `Alabama Tried to Execute an Innocent Man for 30 Years`

## selected（初期推奨）
- **背景=T1／見出し=`30 YEARS. INNOCENT.`／タイトル=A**（"30年×無実"の一撃が最も強い）。A/Bは T1×A と T3(`THE BULLETS LIED`)×B で出し分け。
- 最終は**実物を320pxで見て派手さ・可読を確認**（row12手動）＋promise-payoff（本編が見出しを裏切らない）。※死刑・人種の主題ゆえ**扇情に振りすぎない**（尊厳を保つ）。
