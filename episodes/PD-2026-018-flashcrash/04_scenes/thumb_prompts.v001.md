# EP18 flashcrash — Thumbnail prompts + Title candidates (CTR) v001

> 正典 ONE-PASS row11-13 準拠。**1280×720・16:9**。**UPPERCASE 見出し≤3〜4語・焦点1つ・高コントラスト（黒/紺背景＋金 `#E5B53A` または電気青 `#1F6BFF` ＋白/銀文字）・モバイル親指サイズ(320px)で判読可・誇張しすぎない（本編が約束を果たす honesty）。** **R3：実在人物（Sarao）の顔/肖像/実写・実ロゴ・実取引所は不可＝象徴のみ。** A/B/Cの3案以上を `09_package/EVIDENCE/thumbs/` にレンダー（Remotion `<Still>`）。

## サムネ・コンセプト（3案＋予備）

### THUMB-A 「家 vs 崩落」（推奨・好奇心ギャップ）
- 構図：左に郊外の小さな一軒家（一つだけ灯った窓）、右に**崩れ落ちる赤い市場グラフ**。中央に細い対比線。
- 見出し（UPPERCASE 大）：**"$1 TRILLION"**（金 `#E5B53A`）／サブ小さく **"36 MINUTES"**（白）。
- 背景：黒〜濃紺。家の窓だけ暖色。グラフは赤の崩落。
- 心理：「小さな家」と「一兆ドル」の落差＝一目で“なぜ？”。本人を出さず象徴で派手。
- SDXLプレート例：`A tiny lone suburban house with one lit window on the left, a violent red crashing market graph on the right, black background, dramatic high contrast, cinematic, no people, no text. Avoid: real person, face, logo, watermark, words, blurry, cartoon`

### THUMB-B 「幻の壁」（仕組みの謎）
- 構図：巨大な**半透明の光る注文の壁**が小さな市場を見下ろす。手前に小さな人影シルエット（顔なし・後ろ姿）。
- 見出し：**"THE GHOST"**（電気青 `#1F6BFF`）／サブ **"THAT MOVED WALL ST."**（白・小）。
- 心理：「幽霊が市場を動かした？」＝知的好奇心。
- SDXLプレート例：`A towering translucent glowing wall of orders looming over a tiny market, a small faceless silhouette from behind, dark, electric blue glow, high contrast, cinematic, no readable text. Avoid: real person face, logo, watermark, words, blurry`

### THUMB-C 「寝室 vs ウォール街」（David vs システム）
- 構図：暗い寝室の複数モニター（空席・顔なし）を手前に、奥に崩れる巨大な金融街の光。
- 見出し：**"FROM HIS BEDROOM"**（金）／緊張の赤いグラフを背景に。
- 心理：「寝室から？」の意外性。
- SDXLプレート例：`A dark bedroom with several glowing monitors and an empty chair in foreground, a collapsing skyline of financial light behind, high contrast, cinematic, no people. Avoid: real person face, logo, watermark, readable text, blurry`

### THUMB-D（予備）「ペニー」
- 巨大な **"$0.01"**（金）＋崩落グラフ。"A GIANT COMPANY, ONE PENNY"（小）。

## タイトル候補（CTR・≤60字英・好奇心ギャップ・honest）

> 本編が約束を果たすこと（CLM-0013＝単独原因と断定しない）と矛盾しない範囲で“疑問形/数字”を使う。**「one man caused the crash」と断定する釣りはしない。**

1. **Did One Man Really Break the Stock Market?**  — 疑問形＝議論/コメント誘発・断定回避でR3安全（48字）★A
2. **The Man Who Shook Wall Street From His Bedroom**  — 意外性＋人物（47字）★B
3. **$1 Trillion Gone in 36 Minutes: The Flash Crash**  — 数字×時間の衝撃（48字）★C
4. **How a Bedroom Trader Rattled Wall Street**  — David vs system（41字）予備
5. **The Ghost Order That Moved a Trillion Dollars**  — 仕組みの謎（46字）予備

**A/B実験ペア（doc27）**：①(疑問形A × THUMB-A) vs ②(人物B × THUMB-C)。クリック後の満足＝本編が「単独犯ではない」を誠実に解くこと＝高評価/低離脱。

## サムネ品質ゲート（row12）チェック
- [ ] UPPERCASE 見出し ≤4語・焦点1つ
- [ ] 高コントラスト（黒/紺＋金#E5B53A or 青#1F6BFF＋白文字）
- [ ] 320px幅で判読可
- [ ] 実在人物の顔/肖像・実ロゴなし（R3）
- [ ] 内容と一致（誇張しすぎない）
- [ ] ≥3案を EVIDENCE/thumbs に出力＋selected選定
