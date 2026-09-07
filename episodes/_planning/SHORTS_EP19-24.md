# 縦型ショート 完全設計書 — 第19〜24話（別スレッド制作用・自己完結版）

第19〜24話に1対1で対応する縦型ショート6本。**この設計書だけで別スレッドの Claude Code が単体で完成まで作れるよう、仕様・数値・言い回しロックをすべて本文に書ききる。** 元の話スレッドや口頭指示に依存しない。

> **重要（2026-07-03 オーナー指示）**
> - ショートは**別スレッドの Claude Code** が制作する。この設計書が唯一の指示書。
> - **Codex 画像生成は必須ではない。** 縦画像は「①`H:\pd-media\assets\factory\` の商用OK**動画フッテージ**（縦クロップ）②既存エピソード素材の流用 ③必要な所だけローカルSDXL(7860)で縦生成」で賄ってよい。下の各`image`プロンプトは**SDXLで作る場合の指定**であり、フッテージで代替できるものはフッテージ優先（動く素材＝紙芝居回避）。
> - チャンネルは**US英語**。VO・テロップ・サムネ文言は下表の英語をそのまま使う。翻訳工程なし。
> - 動きの基準は本編と同じ新テンプレ思想（フッテージ主役＋2.5D＋モーショングラフィックス、ただの左右パン/ズーム禁止、金の縦スイープ禁止、黄色ウォッシュ禁止）。

## §0 共通仕様（`SHORTS_EP1-8.md` §0〜§2 と同一。ここに要点を再掲）

- **画面**: 縦 9:16 / 1080×1920 / 尺 35〜45秒 / 字幕（テロップ）常時 / モバイル前提の大きな文字。
- **本人肖像なし**（実在人物の顔・似顔・声真似は禁止・invariant 11）。**画像内に可読な実在テキスト/ロゴ/数字を描かない**（テロップは Remotion で焼く）。
- **ナレ音声**: 本編と同じ声 `ElevenLabs VOICE_ID nPczCjzI2devNBz1zQrb / eleven_multilingual_v2 / stability0.35 / similarity0.80`。英語生成（ElevenLabsは事前承認済・追加確認不要）。
- **音**: 4層ミックス（BGM／緊張／環境／SFX）＋ダッキング＋**2パス静的 -14 LUFS**。中盤で音量が痩せないよう `speechnorm+グルー圧縮`（`build_short_mix.py` の short17〜設定を踏襲）。GAP≈2.70s。
- **コンポジション**: 縦Remotion `Short.tsx`（1080×1920）。時間表どおり並べ、**上品に動かす**（フッテージはそのまま／静止画は2.5D・浮遊カード）。**カットは結構スピーディー**・ナレの無音は最大0.6秒。
- **サムネ**: `shortNN_thumb.png`（<2MB）＋大文言を `ShortThumb` で重ねて書き出し。Shorts公開時は**先頭0.7sにカバーフレーム焼き込み**（libx264 crf18）。
- **VO末尾CTA（共通）**: "Watch the full story on the channel. Follow for more."（**#23 Swartzのみ 988 併記の別文**＝§SHORT #23参照）。
- **画像プロンプト末尾に共通スタイルを付す**（`SHORTS_EP1-8.md` §1）: *"museum-grade cinematic symbolic documentary still, black / deep navy base, electric-blue signal, silver highlights, restrained muted-gold accent, film grain, no faces, no readable text/logos, symbolic reconstruction (not authentic footage)."*
- **保存先**: `H:\pd-media\assets\ai\shorts\short19\` 〜 `short24\`（使う画像＋`shortNN_thumb.png`）。フッテージ流用時はそのパスを `image` 欄に併記。

## §1 公開ゲート（全話共通）

- **1日1本ちょうど・12:00 JST 予約**（`publishAt`）。新規予約前に全 `publishAt` を監査し空き日へ。衝突は `--replace` で日付修正。
- 各本オーナーが一度OK。**R2/R3 は法務目線レビュー必須**（下の各RISK参照）。**#23 Swartz は最高リスク**＝安全ハンドリング・レビュー必須。
- 最終チェック: 本人肖像なし・中立・広告安全・**言い回しロック（pleaded/convicted/alleged/attributed 等）**・字幕がナレに一致・切れ目が自然。
- 本編台本（`PD-2026-0NN-*/03_script/script.en.*`）が更新されたら整合を取り直す。

---

## SHORT #19 →（本編 第19話 Varsity Blues）Wealthy parents paid for a secret "side door" into elite colleges — and the schools were treated as the victims.
**The one surprise**: The rich weren't just making big legal donations (the "back door"); a counselor sold a criminal "side door" — faking athletes and test scores — and almost every famous defendant pleaded guilty rather than fighting at trial.

| time | VO (English) | telop (English, short) | image |
|---|---|---|---|
|0:00-0:03|Wealthy parents paid to sneak their kids into top colleges — through a secret "side door."|The "side door"|01|
|0:03-0:12|In March 2019, prosecutors unsealed "Operation Varsity Blues" and arrested 50 people. The mastermind, Rick Singer, ran a counseling business and a foundation prosecutors called a sham charity.|March 2019: 50 arrested|02,03|
|0:12-0:26|Parents paid about $25 million to buy fake athletic recruiting spots — children labeled as recruits for sports they never played, with staged photos. Others paid to have a man secretly take the SAT or fix the answers.|$25M for fake "athletes"|04,05|
|0:26-0:40|Actress Felicity Huffman paid $15,000 to fix her daughter's test and pleaded guilty — 14 days. Lori Loughlin and her husband paid $500,000 for fake crew spots and pleaded guilty to fraud conspiracy. The schools were treated as victims, not suspects. In all, 55 were charged and 53 convicted — almost all by guilty plea.|Pleaded guilty · schools = victims|06,07|
|0:40-0:45|Watch the full story on the channel. Follow for more.|(CTA endcard)|07(hold)|

- `short19_01.png` A grand university gate at dusk with three doors implied — one bright front entrance, and a small shadowed side door glowing faint gold, symbolic "side door" motif, no readable signage
- `short19_02.png` A faceless well-dressed parent's hands sliding a thick envelope of cash across a polished desk in low key, no faces, no logos, cold institutional light
- `short19_03.png` An empty ornate charity gala hall, one spotlight on a lectern, gold and navy, the hollow "foundation," no people
- `short19_04.png` A blank sports jersey and a running shoe resting under a hard light beside a stack of cash, the "bought athlete," no team marks, no numbers, symbolic
- `short19_05.png` A standardized-test answer sheet with rows of empty bubbles under a desk lamp, a single pencil, no readable text, tense stillness (**footage alt**: `factory` exam-hall or paper-scanning clip, vertical crop)
- `short19_06.png` A dignified empty courtroom bench in a shaft of cold light, neutral and severe, no people, no seals
- `short19_07.png` A single empty chair on a bare stage under one gold spotlight, the displaced honest applicant, quiet and resonant, negative space for text
- **thumbnail** `short19_thumb.png` A university gate with one glowing hidden "side door," cash on the step ／ headline: **"THE SIDE DOOR"** ／ badge: "$25M"

> **FACT-CHECK** — "side door" (Singer's term, DOJ-adopted)=CLM-0003; March 2019 unsealed / 50 arrested=CLM-0001; Singer's business "The Key" + sham-charity foundation=CLM-0002; ~$25M athletic bribes / fake recruits / staged photos=CLM-0004 + CLM-0007; secret test-taking/answer-fixing=CLM-0005 + CLM-0006; Huffman $15,000 / pleaded guilty / 14 days=CLM-0009; Loughlin+Giannulli $500,000 / crew / pleaded guilty to **fraud conspiracy**=CLM-0010; schools = victims not suspects=CLM-0011; 55 charged / 53 convicted / almost all by plea=CLM-0014.
> **RISK (R3 — living people, pleaded guilty)** — LOCKS: **"pleaded guilty," never "convicted at trial."** Loughlin/Giannulli **money-laundering & bribery counts were DISMISSED** — say only "pleaded guilty to fraud conspiracy," never "convicted of money laundering/bribery." Singer was **charged with 3, pleaded to 4** (don't say "convicted"). Date-qualify counts: **50 initial vs 55 charged / 53 convicted.** Schools = victims (never "the universities committed fraud"). Do **not** impute knowledge to any child. No real-person likeness of Singer/Huffman/Loughlin/Giannulli. Pre-publish legal review.

---

## SHORT #20 →（本編 第20話 Gardner Heist）The biggest art heist in history is still unsolved — and the empty frames still hang on the wall.
**The one surprise**: The FBI says it believes it knows who did it, but never named them and says they're now dead — and the clock to charge the theft has already run out, so recovery, not punishment, is all that's left.

| time | VO (English) | telop (English, short) | image |
|---|---|---|---|
|0:00-0:03|The biggest art heist in history — and the empty frames still hang on the wall.|Still unsolved|01|
|0:03-0:12|March 18, 1990, Boston. Two men dressed as police talked their way into the Isabella Stewart Gardner Museum, handcuffed the guards in the basement, and were inside about 81 minutes.|1990: fake cops, 81 minutes|02,03|
|0:12-0:26|They took 13 works — cutting a Rembrandt and a Vermeer right out of their frames. The haul is estimated around half a billion dollars, though the art is unsellable. Not one of the 13 has ever been found.|13 works · ~$500M · none found|04,05|
|0:26-0:40|The FBI says it believes it knows who did it — but never named them, and says they are now dead. The clock to charge the theft has run out; there's a standing $10 million reward. And the empty frames still hang exactly where the paintings were.|Empty frames still hang|06,07|
|0:40-0:45|Watch the full story on the channel. Follow for more.|(CTA endcard)|07(hold)|

- `short20_01.png` An ornate empty gilded picture frame hanging on a dim museum wall, nothing but shadow inside it, one shaft of gold light, haunting and iconic, no readable text
- `short20_02.png` A grand museum gallery at night, cold moonlight through tall windows, empty and silent, no people (**footage alt**: `factory` museum/gallery interior clip, vertical crop)
- `short20_03.png` Two faceless silhouettes in police-style caps and coats at a heavy door, seen from behind in low key, no visible faces, no badges/logos, tense
- `short20_04.png` A close-up of an empty canvas stretcher where a painting was cut from its frame, frayed edge, cold navy shadow, symbolic of the loss
- `short20_05.png` A cluster of empty ornate frames leaning in storage light, a Vermeer-shaped void (symbolic, NOT a reproduction of the real work), melancholic
- `short20_06.png` A single spotlight on one empty frame on a gallery wall, a small reward-notice card as an unreadable blur beside it, reverent, no legible text
- `short20_07.png` The empty frames on the wall at dusk, a doorway of gold light beyond, hope-of-return mood, negative space for text
- **thumbnail** `short20_thumb.png` One empty gilded frame glowing on a dark museum wall ／ headline: **"STILL MISSING"** ／ badge: "$500M"

> **FACT-CHECK** — largest art heist / largest property crime (attributed to museum/FBI)=CLM-0007; March 18 1990 / fake police / guards handcuffed in basement / ~81 minutes=CLM-0001 + CLM-0002; 13 works / cut from frames=CLM-0003 + CLM-0004; ~$500M **estimate**, works unsellable=CLM-0006; none recovered / still unsolved=CLM-0008; FBI believes it identified the thieves, never named them, says deceased / no one charged=CLM-0012; statute of limitations on the theft expired=CLM-0011; $10M reward=CLM-0010; empty frames still displayed=CLM-0009.
> **RISK (R2 — unsolved, third parties)** — LOCKS: **never name or imply the guilt of any person**; the FBI **never publicly named** the thieves; people sometimes called the likely thieves were named by **journalists, not the FBI** (CLM-0014); **$500M is an ESTIMATE** (never "sold for/worth exactly $500M"); "largest" is an **attributed** characterization; the guard who buzzed them in must **not** be portrayed as complicit; no real-person likeness. Confirm living/deceased status of any named person before use. Pre-publish legal review.

---

## SHORT #21 →（本編 第21話 D.B. Cooper）He jumped out of a plane with $200,000 — and vanished forever.
**The one surprise**: It is the only unsolved hijacking in the history of U.S. commercial aviation; the single clue ever found was $5,800 of decaying cash by a river — and in 2016 the FBI *suspended* the case, never *solved* it.

| time | VO (English) | telop (English, short) | image |
|---|---|---|---|
|0:00-0:03|He jumped out of a plane with two hundred thousand dollars — and vanished forever.|Never found|01|
|0:03-0:12|November 24, 1971. A calm man in a dark suit, ticketed as "Dan Cooper," hijacked a flight from Portland to Seattle with a note claiming he had a bomb.|1971: "Dan Cooper"|02,03|
|0:12-0:26|He demanded $200,000 and four parachutes, let the passengers go, then ordered the crew to fly low toward Mexico City. A little after 8 p.m., he lowered the plane's rear stairs and parachuted into a freezing night over Washington.|$200K · 4 parachutes · jumped|04,05|
|0:26-0:40|The FBI chased it for 45 years — the only unsolved hijacking in U.S. aviation history. In 1980 a boy found about $5,800 of the cash by a river; the serial numbers matched. It's the only money ever found. In 2016 the FBI suspended the case — suspended, not solved.|Suspended · not solved|06,07|
|0:40-0:45|Watch the full story on the channel. Follow for more.|(CTA endcard)|07(hold)|

- `short21_01.png` A lone parachute silhouette falling into a vast black rainy night sky, tiny against the dark, cold and final, no face, wide negative space
- `short21_02.png` A 1971 airliner cabin aisle in warm dim light, an anonymous seated silhouette from behind in a dark suit, no face, period-neutral (**footage alt**: vintage-style aircraft interior clip)
- `short21_03.png` A briefcase opened just enough to show ambiguous wires and red shapes in shadow, a folded note beside it, menace implied not shown, no readable text
- `short21_04.png` A banded stack of twenty-dollar bills under a hard light on a cold surface, generic currency, no legible serial detail, tense
- `short21_05.png` The lowered aft airstair of a jet at night, rain and dark forest below, a void of black air, dramatic scale, no figure
- `short21_06.png` A child's hand uncovering decaying banded bills in wet riverbank sand, cold blue dawn, the only clue, no faces
- `short21_07.png` A closed FBI-style case folder in a shaft of light, edges worn, "suspended not solved" mood, no legible text
- **thumbnail** `short21_thumb.png` A parachute vanishing into a black night sky over forest ／ headline: **"HE VANISHED"** ／ badge: "$200K"

> **FACT-CHECK** — Nov 24 1971 / alias "Dan Cooper" / Portland→Seattle / "D.B." a press error=CLM-0001; note claiming a bomb + briefcase=CLM-0002; $200,000 + four parachutes=CLM-0003; passengers released, flew toward Mexico City low/slow=CLM-0005 + CLM-0006; a little after 8 p.m. lowered aft stairs, parachuted over SW Washington, never seen again=CLM-0007; freezing rainy night=CLM-0008; 45-year FBI hunt / only unsolved U.S. hijacking=CLM-0009; 1980 boy found ~$5,800, serial numbers matched, only cash recovered=CLM-0011; 2016 FBI **suspended, not solved**=CLM-0010; calm man in dark suit description=CLM-0014.
> **RISK (R2 — unsolved)** — LOCKS: **UNSOLVED**; never assert anyone "was D.B. Cooper"; the FBI **never confirmed any suspect**; suspects were **proposed by third parties, not the FBI**; never accuse any living person. Keep jump time ("a little after 8 p.m.") and place ("southwestern Washington") broad; "about 36" passengers; bomb was a **claim**, not a confirmed device. Symbolic visuals only, **no face**. Pre-publish legal review.

---

## SHORT #22 →（本編 第22話 Michael Milken）He was charged with 98 counts — and pleaded guilty to six.
**The one surprise**: The man who built the junk-bond market was indicted on 98 counts including RICO racketeering, but the case never went to trial — he pleaded to six felonies, was never convicted of insider trading or racketeering, and was pardoned decades later without erasing the plea.

| time | VO (English) | telop (English, short) | image |
|---|---|---|---|
|0:00-0:03|He was charged with ninety-eight counts — and pleaded guilty to six.|98 charged → 6 pleaded|01|
|0:03-0:12|Michael Milken built the high-yield, or "junk," bond market, financing companies the big banks had shut out. In 1987, his pay was reported at around $550 million — called the largest single-year pay in America.|Built the "junk" bond market|02,03|
|0:12-0:26|After a cooperating witness pointed investigators his way, a 1989 indictment charged him with 98 counts, including RICO racketeering. But those were accusations — the case never went to trial.|98 counts · never went to trial|04,05|
|0:26-0:40|In 1990 he pleaded guilty to six felony counts; the RICO charge and the other 92 were dropped. He paid about $600 million and was barred from the industry for life. In 2020 he received a full presidential pardon — which forgives the punishment, but does not erase the guilty plea, and did not lift that lifetime ban.|Pardon ≠ innocence|06,07|
|0:40-0:45|Watch the full story on the channel. Follow for more.|(CTA endcard)|07(hold)|

- `short22_01.png` A towering stack of legal document folders in shadow beside a single thin folder lit gold, the "98 vs 6" imbalance shown as paper volume only, no readable text or numbers
- `short22_02.png` An X-shaped trading desk silhouette in an empty 1980s Beverly Hills office at dawn, banks of dark monitors, no faces, cold navy and gold
- `short22_03.png` Abstract high-yield bond certificates fanned in gold light dissolving into a rising skyline of leveraged towers, symbolic finance, no legible text
- `short22_04.png` A federal indictment folder under a hard courtroom light, thick and heavy, no readable words, cold institutional dread
- `short22_05.png` An empty jury box in a shaft of light — the trial that never happened — dignified, no people, no seals
- `short22_06.png` A presidential pardon document with an ornate seal rendered as an unreadable gold emboss (no legible text), resting in cold light, ambiguous mercy
- `short22_07.png` A balance scale in low key, a small gold "genius" laurel on one pan and a cold blue mask of "greed" on the other, unresolved, no faces
- **thumbnail** `short22_thumb.png` A huge stack of case files beside one thin folder, gold vs navy ／ headline: **"98 CHARGES, 6 PLEAS"** ／ badge: "PARDONED"

> **FACT-CHECK** — built high-yield/junk-bond market=CLM-0001; Beverly Hills X-desk + ~$550M 1987 pay (record)=CLM-0002; Boesky cooperated, pointed toward Milken=CLM-0004; 1989 **98-count** indictment incl. **RICO** (charges, not findings; never tried)=CLM-0005; 1990 **pleaded guilty to six**, RICO + 92 counts dropped=CLM-0006; ~$600M (=$200M fine + $400M restitution), **SEC lifetime bar**=CLM-0007; 10-yr sentence reduced, ~2 served (optional, omit for time)=CLM-0008; Feb 18 2020 full pardon = clemency not innocence, plea stands, ban not lifted=CLM-0009.
> **RISK (R3 — living, pardoned)** — LOCKS: **"pleaded guilty to six," NEVER "convicted"**, never "convicted of insider trading," never "convicted of racketeering/RICO," never "convicted at trial." Keep **CHARGED (98, incl. RICO)** distinct from **PLEADED (6)**. **~$600M = $200M fine + $400M restitution** (the fund is not a "fine"). **Pardon = clemency, NOT innocence/exoneration**; the guilty plea **stands**; the SEC lifetime ban was **NOT lifted**. Genius-vs-greed is **attributed, never resolved** ("defenders argue / critics argue"). **Re-confirm he is still alive before publish.** No real-person likeness. Pre-publish legal review.

---

## SHORT #23 →（本編 第23話 Aaron Swartz）The website he took from didn't even want him charged.
**The one surprise**: JSTOR, the party whose articles he downloaded, settled and said it did not want him prosecuted — yet federal prosecutors pursued a 13-count case anyway.

> **⚠ 最高リスク・OPTIONAL。** これは**自死を扱うR3・very_high**。オーナーが「Swartzショートを公開するか否か」をまず判断する。作る場合は**安全ハンドリング・レビュー必須**、下記ロックを一字も外さないこと。若いチャンネルではBAN/デモネタイズ回避を最優先に、迷ったら作らない選択も可。

| time | VO (English) | telop (English, short) | image |
|---|---|---|---|
|0:00-0:03|The website he took from didn't even want him charged.|The victim said no|01|
|0:03-0:12|Aaron Swartz was a programming prodigy — as a teenager he co-authored the RSS 1.0 specification and helped build the technical layer of Creative Commons. He believed knowledge paid for by the public should belong to the public.|Prodigy · open knowledge|02,03|
|0:12-0:26|Over MIT's open network, he downloaded about 4.8 million scholarly articles — most of the JSTOR archive. JSTOR settled with him and said plainly it did not want him prosecuted. MIT stayed neutral. Federal prosecutors charged him anyway — four counts, then thirteen.|JSTOR didn't want charges|04,05|
|0:26-0:40|On paper the charges stacked to a theoretical maximum of 35 years; prosecutors signaled a plea of about six months, and legal scholars said the 35-year headline wildly overstated what he really faced. Aaron Swartz died by suicide on January 11, 2013, at age 26. His family said the prosecution's overreach contributed to his death.|A crime with no victim|06,07|
|0:40-0:45|If you're struggling, call or text 988 — the Suicide & Crisis Lifeline. Watch the full story on the channel.|988 Lifeline · (CTA endcard)|07(hold)|

- `short23_01.png` A vast dark digital library of glowing document icons behind a locked gate of light, one small key nearby, "knowledge behind a paywall," no faces, no readable text
- `short23_02.png` A single open laptop glowing on a desk in a quiet dark room, lines of soft blue light, the young coder implied by an empty chair, no face (**footage alt**: server-room / data-stream clip, vertical crop)
- `short23_03.png` An abstract web of glowing nodes linking documents into an open network, electric blue, the idea of shared knowledge, no text
- `short23_04.png` A calm university archive corridor at night, endless shelves receding, one cold shaft of light, no people, dignified
- `short23_05.png` A civil-settlement style document beside a dropped set of handcuffs left unused, symbolic "the victim said no / charges anyway," no readable text
- `short23_06.png` A balance scale tilted under a vast stack of statute books versus one small figure of light, disproportion made visual, no faces, restrained
- `short23_07.png` A single quiet candle-soft point of warm light in deep navy darkness, a respectful memorial mood — NO depiction of death, NO method, NO location — pure gentle light, generous space for the 988 endcard
- **thumbnail** `short23_thumb.png` A locked gate of glowing documents with one small key ／ headline: **"THE VICTIM SAID NO"** ／ badge: "13 CHARGES"

> **FACT-CHECK** — co-authored RSS 1.0 as a teen=CLM-0001; helped build Creative Commons' technical layer=CLM-0003; open-access belief / manifesto (context, not confession)=CLM-0005; ~4.8M articles / most of JSTOR / MIT open network / not affiliated=CLM-0007; **JSTOR settled and did not want prosecution; MIT neutral**=CLM-0008; charged under CFAA + wire fraud, 4 counts → 13=CLM-0009; theoretical stacked max ~35 years + ~6-month plea signal (Peters) + scholars (Kerr) said it overstated exposure=CLM-0011; **death by suicide Jan 11 2013, age 26**=CLM-0013; family said prosecution's overreach contributed / "a crime with no victims"=CLM-0014.
> **RISK (R3 — very_high, death by suicide) — SAFE-HANDLING LOCKS (do not deviate):**
> 1. **Death stated ONCE, exactly: "Aaron Swartz died by suicide on January 11, 2013, at age 26."** NEVER "committed suicide," "took his own life," any **method, location, note, scene, or reenactment**. It appears only in the 0:26-0:40 line — nowhere in title, telop, thumbnail, or metadata.
> 2. **"35 years" NEVER unqualified** — always the **theoretical stacked statutory maximum**, paired with the **~6-month plea signal** and the **scholarly critique**. Never "he was facing 35 years."
> 3. **Causation is ALWAYS attributed to the family**, never asserted by the narrator ("His family said…"). No "the prosecution caused his death," no "MIT killed him."
> 4. He was **charged, never tried or convicted**. JSTOR = the party, said it didn't want charges.
> 5. **988 Suicide & Crisis Lifeline** shown on-screen (0:40-0:45) and in the description; CTA quiet/respectful. No real-person likeness. **Mandatory safe-handling + legal review before any publish.**

---

## SHORT #24 →（本編 第24話 Raj Rajaratnam）To catch a billionaire trader, the FBI used the mob's favorite tool: wiretaps.
**The one surprise**: It was the first big insider-trading case built on court-authorized wiretaps — and at trial, prosecutors played the jury his own phone calls, the alleged scheme in his own voice.

| time | VO (English) | telop (English, short) | image |
|---|---|---|---|
|0:00-0:03|To catch a billionaire trader, the FBI used the same tool it used on the mob: wiretaps.|Wiretaps on Wall Street|01|
|0:03-0:12|Raj Rajaratnam ran the Galleon Group, a hedge fund that at its peak managed about seven billion dollars. His sources sat inside the companies themselves — an Intel executive, a McKinsey partner, an IBM executive — each charged separately.|$7B fund · insiders|02,03|
|0:12-0:26|It was the first big insider-trading case built on court-authorized wiretaps. Prosecutors played the jury his own phone calls — the alleged scheme in his own voice. On May 11, 2011, a jury convicted him on all fourteen counts.|Convicted on all 14 counts|04,05|
|0:26-0:40|He was sentenced to eleven years — at the time, prosecutors called it the longest insider-trading sentence in American history — and ordered to forfeit nearly fifty-four million dollars. In 2013 the appeals court upheld the wiretaps as lawful. A separate trial even convicted a Goldman Sachs director of feeding him boardroom secrets.|11 years · wiretaps upheld|06,07|
|0:40-0:45|Watch the full story on the channel. Follow for more.|(CTA endcard)|07(hold)|

- `short24_01.png` A vintage reel-to-reel wiretap recorder turning in shadow, a single red record glow, headphones nearby, surveillance noir, no faces, no text
- `short24_02.png` A cold glass hedge-fund tower at dusk with a faint "$7B" implied only as scale of light in windows (no legible number), power and money, no logos (**footage alt**: financial-district skyline clip, vertical crop)
- `short24_03.png` Three faceless corporate silhouettes in different office settings passing a glowing sliver of paper hand to hand, "insiders," no faces, no company marks
- `short24_04.png` A telephone handset with a visible glowing sound-wave leaking from it, the "crime in his own voice," electric blue on black, no text
- `short24_05.png` A solemn jury box seen from the bench side in a shaft of cold light, the moment of the verdict, no people, dignified
- `short24_06.png` A gavel resting on a dark bench with a cold blue shaft of light, weight of an eleven-year sentence, no readable text
- `short24_07.png` A single empty boardroom chair at the head of a long dark table under one light, "the secrets came from the very top," no faces, no logos
- **thumbnail** `short24_thumb.png` A wiretap recorder turning with a red glow over a night skyline ／ headline: **"HIS OWN VOICE"** ／ badge: "11 YEARS"

> **FACT-CHECK** — Galleon ~$7B peak / billionaire=CLM-0001; tippers inside Intel/McKinsey/IBM (Chiesi), each charged separately=CLM-0010; first major insider case built on court-authorized wiretaps (mob/drug tool)=CLM-0008; wiretapped calls played for the jury=CLM-0018; May 11 2011 jury **convicted on all 14 counts**=CLM-0002; 11-year sentence=CLM-0003; "longest insider-trading sentence" (attributed, 2011)=CLM-0004; forfeit $53.8M (~$54M)=CLM-0005; 2013 Second Circuit upheld wiretaps + affirmed conviction=CLM-0009; Rajat Gupta (Goldman director) separately convicted for tipping=CLM-0011.
> **RISK (R2 — convicted at trial)** — LOCKS: **convicted at a jury trial = stateable as fact** (he did **NOT** plead guilty — he fought it and lost; do not say "admitted guilt"). The "longest sentence" superlative is **attributed to prosecutors/press and time-bound to 2011** (never flat/undated). **Profit hedged** → anchor to the **~$54M forfeiture** (don't state a single flat profit number). **Gupta is a SEPARATE case** — never merge his penalties/verdict with Rajaratnam's; tippers **charged separately** (each disposition distinct). **No verbatim wiretap dialogue** unless verified against the public trial record. No real-person likeness. Pre-publish legal review.

---

## §2 制作・公開手順（別スレッド Claude Code 用チェックリスト）

1. **素材**: 各話 `image` を用意 — フッテージ優先（`H:\pd-media\assets\factory\` の縦クロップ、または本編 `05_visuals` 流用）、足りない所だけ SDXL(7860) で縦生成し `H:\pd-media\assets\ai\shorts\shortNN\` へ。**本人肖像なし・ロゴなし・可読な実在テキストなし**。**Codex生成は不要**。
2. **ナレ**: §0の声で英語生成（承認済）。GAP≈2.70s、35〜45s。
3. **組み立て**: `Short.tsx`（1080×1920）で時間表どおり。フッテージはそのまま／静止画は2.5D・浮遊カード。テロップは上表の英語を大きく焼き込み（下部セーフ・重い黒箱を避ける）。カットはスピーディー・無音は最大0.6秒。
4. **音**: 4層＋ダッキング＋2パス静的 -14 LUFS（`build_short_mix.py`）。中盤で痩せないこと。
5. **サムネ**: `shortNN_thumb.png`（<2MB）＋大文言を `ShortThumb` で。公開時は先頭0.7sカバーフレーム焼き込み（crf18）。
6. **公開**: **1日1本・12:00 JST 予約**。予約前に全 `publishAt` 監査→空き日。**R2/R3 は法務レビュー、#23 Swartz は安全ハンドリング・レビュー必須**（作るか否かはオーナー判断）。最終チェック＝本人肖像なし・中立・広告安全・言い回しロック・字幕がナレに一致。
7. **命名衝突に注意**: 既存 `short01`〜`short18` と衝突させない。新規は `short19`〜`short24`。`Root.tsx` へ `Short-shortNN-yt/-tt` と `ShortThumb-shortNN` を登録。
8. **整合**: 本編台本（`PD-2026-0NN-*/03_script/`）更新時は VO/FACT-CHECK を取り直す。durable source content_hash は公開前に確定。
