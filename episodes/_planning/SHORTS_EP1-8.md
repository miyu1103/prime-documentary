# 縦型ショート 完全設計書 — 第1〜8話（Codex渡し用 / 制作可能版）

公開済み(または公開予定)の各話に1対1で対応する縦型ショート8本。**素材は先にCodexアプリで縦型生成→保存→Remotionで組む**前提。
実装=Codex。企画・構成・プロンプト・サムネ＝Claude（本書）。

## §0 仕様（全ショート共通・厳守）
- **縦 9:16 / 1080×1920 / 30fps / 35〜45秒**。字幕（テロップ）常時オン・大きめ。**最初の1秒で掴む**。末尾はループしやすく。
- 配色＝黒/紺/エレクトリックブルー/金。BGM控えめ。ナレ＝本編と同じ声（**ElevenLabsで生成OK＝課金承認待ち不要**・止まらず進める）**または字幕だけの無ナレ版**。
- **実在人物の肖像・本人映像なし（全画像で厳守）**。中立・広告安全。**第4話(FTX/SBF)・第5話(Madoff)は特に本人を描かない。**
- CTA＝「本編はこちら」で**該当の公開動画へリンク**（説明欄・固定コメント／URLはオーナーが差し込み）。公開予約は**6/24以降**・各ゲートで停止。

## §1 事前生成ワークフロー（Codexアプリ）
各ショートの「縦AI画像プロンプト」を**先にアプリで生成**し、下記に保存：
```
H:\pd-media\assets\ai\shorts\short01\  …  short08\
  ファイル名：short01_01.png 〜 short01_07.png（本編用）／ short01_thumb.png（サムネ用）
```
PNG・**縦1080×1920以上（できれば2160×3840）**。保存後、Codexがそれらを並べてRemotion縦コンポジションで組む。
**各プロンプト末尾に必ず付ける共通スタイル**（本文では省略表記）：
> 末尾共通 = 「, vertical 9:16 full-frame composition, cinematic documentary still, dramatic moody lighting, deep navy-and-black palette with electric-blue and gold accents, photorealistic, ultra-detailed, shallow depth of field. No on-screen text, no watermark, no logo, no identifiable real person.」

## §2 サムネ計画（共通）
- 各ショートに `shortNN_thumb.png`（縦・文字なしのキービジュアル）を1枚。**大きな日本語テロップはRemotionで重ねる**（画像には文字を入れない）。
- サムネ文言は各ショートに記載（短く・大きく・1〜2語＋?）。

---

## SHORT #1 →（本編 第1話 Miranda）なぜ警官は“権利”を読む？
**1つの驚き**：権利の読み上げは礼儀ではなく、取調室そのものを是正する“構造の仕組み”。
| 時間 | ナレ(VO) | テロップ | 画像 |
|---|---|---|---|
|0:00-0:03|警察が権利を読むのは、礼儀じゃない。|なぜ警官は“権利”を読む？|01|
|0:03-0:12|昔は、あなたを一人きりで何時間も尋問できた。警告もなしに。|警告なしの密室|02,03|
|0:12-0:28|追い詰められての誤った自白も。1966年、最高裁が線を引いた——拘束尋問の前に、警告せよ。|1966 最高裁が線を引く|04,05|
|0:28-0:40|これは礼儀でなく“構造の修正”。警告がなければ自白は証拠から外せる。数秒が全逮捕を変えた。|警告なし＝自白は無効|06,07|
|0:40-0:45|続きは本編で（説明欄）。フォローを。|本編はチャンネルへ|07(止め)|

**縦AI画像プロンプト**（末尾共通スタイルを付ける）
- `short01_01.png` A single bare interrogation lamp glowing over an empty metal table in a dark room
- `short01_02.png` A lone empty chair under a harsh overhead light in a bare interrogation room
- `short01_03.png` A wall clock with blurred fast-spinning hands, long hours passing
- `short01_04.png` A coerced confession document under a single light with a pen forced over it, no legible text
- `short01_05.png` An austere empty courtroom with a shaft of light falling on the floor seal
- `short01_06.png` A short rights-warning card glowing in a hand, symbolic, no legible text
- `short01_07.png` Handcuffs beside a glowing shield-of-rights symbol, balance restored
- **サムネ** `short01_thumb.png` The interrogation lamp over a metal table, ominous ／ 文言：**「なぜ“権利”を読む？」**

## SHORT #2 →（本編 第2話 Gideon）鉛筆1本で全法廷を変えた
**1つの驚き**：貧しい男が独房から鉛筆で書いた1通の手紙が、最高裁を動かした。
| 時間 | VO | テロップ | 画像 |
|---|---|---|---|
|0:00-0:03|弁護士を雇えなければ、ただで付けてもらえる？|払えなければ弁護士は付く？|01|
|0:03-0:12|ある男は起訴され、貧しく弁護士を断られ、有罪に。|弁護士を断られ有罪|02,03|
|0:12-0:26|彼は独房から、鉛筆で最高裁へ嘆願書を書いた。|独房から鉛筆で嘆願|04,05|
|0:26-0:40|1963年、9対0。払えないなら州が弁護士を付けねばならない。1通の手紙が全米の法廷を変えた。|9-0 全法廷を変えた|06,07|
|0:40-0:45|続きは本編で。フォローを。|本編はチャンネルへ|07(止め)|

- `short02_01.png` A lone empty defense table in an empty courtroom with no lawyer present, single light
- `short02_02.png` A closed courthouse door with a defendant's shadow turned away, denied, no face
- `short02_03.png` A pencil and a single sheet of prison stationery on a bare cell bunk under barred-window light
- `short02_04.png` A humble handwritten petition page lit dramatically, no legible text
- `short02_05.png` A plain envelope rising toward a distant grand institution, conceptual
- `short02_06.png` Nine empty judicial chairs unified in a row, a 9-0 result, navy and gold
- `short02_07.png` A glowing gavel over a small model courtroom, change rippling outward
- **サムネ** `short02_thumb.png` A pencil and handwritten page on a prison cell bunk ／ 文言：**「鉛筆1本で全法廷を変えた」**

## SHORT #3 →（本編 第3話 Mapp）違法な捜索の“証拠”は使える？
**1つの驚き**：警察が違法に家を捜索して見つけた物は、有罪の証拠に使えない。
| 時間 | VO | テロップ | 画像 |
|---|---|---|---|
|0:00-0:03|警察が家を違法に捜索し、何かを見つけた。それでも証拠に使える？|違法な家宅捜索の証拠は？|01|
|0:03-0:12|1957年、警察は有効な令状なしに、ある女性の家へ押し入った。|令状なしで押し入る|02,03|
|0:12-0:26|目当ての容疑者はいない。代わりに本を見つけ、別件で起訴。|目当て不在→別件で起訴|04,05|
|0:26-0:40|1961年、最高裁——違法な捜索で得た証拠は、どの州でも使えない。時に有罪者を逃がす、“巡査がしくじったから”。|証拠は排除される|06,07|
|0:40-0:45|続きは本編で。フォローを。|本編はチャンネルへ|07(止め)|

- `short03_01.png` A front door being forced open at night, splintering light through the gap
- `short03_02.png` Police silhouettes searching a modest home without a warrant, no faces
- `short03_03.png` A blank document held up where a warrant should be, a conceptual absence
- `short03_04.png` An old trunk opened to reveal a few books, an unexpected find, dramatic
- `short03_05.png` A courtroom where a minor charge is read, a single shaft of light
- `short03_06.png` Seized evidence dissolving into nothing as it is excluded, conceptual
- `short03_07.png` A glowing scale tipping toward "keep police honest" over "convict", gold rim
- **サムネ** `short03_thumb.png` A front door forced open at night ／ 文言：**「違法な捜索＝証拠は無効」**

## SHORT #4 →（本編 第4話 FTX）80億ドルはどこへ？  ※本人の顔は出さない
**1つの驚き**：顧客の数十億ドルを預かった取引所から、約80億ドルが消えた。
| 時間 | VO | テロップ | 画像 |
|---|---|---|---|
|0:00-0:03|Tシャツに短パンの30歳が、顧客の数十億ドルを預かっていた。そして約80億ドルが消えた。|80億ドルはどこへ？|01|
|0:03-0:12|FTXは巨大な暗号資産取引所。創業者は“最も信頼された顔”。|信頼の暗号資産取引所|02,03|
|0:12-0:26|だがコードに秘密の例外。私的トレード会社が、顧客の預金をほぼ無制限に引き出せた。|コードの“抜け穴”|04,05|
|0:26-0:40|皆が一斉に返金を求めた時、もう無かった。2023年、米史上最大級の詐欺で有罪。暗号資産でも、顧客の金を使えば窃盗。|2023 有罪|06,07|
|0:40-0:45|続きは本編で。フォローを。|本編はチャンネルへ|07(止め)|

- `short04_01.png` A glowing crypto-exchange neon skyline at night, impressive and hollow
- `short04_02.png` A T-shirt-and-shorts silhouette on a stage cast in a trusted golden glow, no face
- `short04_03.png` Rivers of digital coins flowing into a single bright vault icon, conceptual
- `short04_04.png` A wall of code with one glowing secret exemption gap, no legible text
- `short04_05.png` Customer deposits being quietly siphoned through a hidden channel, conceptual
- `short04_06.png` A vault door opened to reveal it is empty just as everyone arrives, dramatic
- `short04_07.png` A distant courtroom glowing, a conviction, no people
- **サムネ** `short04_thumb.png` An empty vault with the last coins vanishing ／ 文言：**「80億ドルはどこへ？」**

## SHORT #5 →（本編 第5話 Madoff）安定リターン、取引はゼロ  ※本人の顔は出さない
**1つの驚き**：何十年も安定した利益を払い続けたが、ほとんど投資していなかった。
| 時間 | VO | テロップ | 画像 |
|---|---|---|---|
|0:00-0:03|彼は何十年も安定した利益を払った。実際には、ほとんど投資していなかった。|安定リターン、取引はゼロ|01|
|0:03-0:12|ウォール街で最も信頼された名前の一つ。年々なめらかに安定した成績。|最も信頼された名前|02,03|
|0:12-0:26|だが調査で、実際の取引はほとんど無かったと判明。|取引はほぼ無し|04,05|
|0:26-0:40|“利益”は新しい投資家の金を古い投資家へ渡しただけ。2008年に崩壊、150年の刑。値動きが無さすぎることが危険信号。|崩壊→150年|06,07|
|0:40-0:45|続きは本編で。フォローを。|本編はチャンネルへ|07(止め)|

- `short05_01.png` An impossibly smooth ever-rising profit curve glowing in the dark, too perfect
- `short05_02.png` A prestigious Wall Street office at dusk, gleaming and trusted, no people
- `short05_03.png` Polished steady account statements stacked under warm light, no legible text
- `short05_04.png` An empty trading screen with no real trades, conceptual silence
- `short05_05.png` New investors' money handed straight to old investors in a closed loop, conceptual
- `short05_06.png` A tall tower of building blocks collapsing, the 2008 crash, dramatic
- `short05_07.png` A long dim corridor of receding years, a 150-year sentence, abstract
- **サムネ** `short05_thumb.png` The too-smooth rising curve glowing ／ 文言：**「安定リターン、取引はゼロ」**

## SHORT #6 →（本編 第6話 Terry）逮捕してなくても体を触れる？
**1つの驚き**：警官は逮捕も令状も無しに、“合理的な疑い”だけで止めて体を触れる。
| 時間 | VO | テロップ | 画像 |
|---|---|---|---|
|0:00-0:03|警官は、あなたを逮捕してなくても、止めて体を触れることがある。|逮捕なしで“止めて触る”|01|
|0:03-0:12|令状も、犯罪の証拠も要らない。必要なのは“合理的な疑い”——勘より少し強い根拠。|必要なのは“合理的な疑い”|02,03|
|0:12-0:28|1968年、一人の刑事が店の前を行き来する二人を見た。怪しいと感じ、服の上から触る。出てきたのは拳銃。|1968 店を下見する二人|04,05|
|0:28-0:40|最高裁はこれを認めた。逮捕より低い基準＝“stop and frisk”が路上に生まれた。今も議論が続く権力。|路上の“低い基準”が誕生|06,07|
|0:40-0:45|続きは本編で。フォローを。|本編はチャンネルへ|07(止め)|

- `short06_01.png` A police silhouette stopping a figure on a night street for a pat-down, no faces
- `short06_02.png` A blank space where a warrant should be, "none needed", conceptual
- `short06_03.png` A glowing gauge between "hunch" and "proof" landing in the middle, reasonable suspicion
- `short06_04.png` Two figures pacing back and forth before a darkened storefront, casing it, no faces
- `short06_05.png` A watchful detective's eye on the street at night, observation, no identifiable face
- `short06_06.png` A concealed handgun outline revealed under a coat, dramatic
- `short06_07.png` A lower-set boundary line drawn across a street, a weaker second standard, conceptual
- **サムネ** `short06_thumb.png` A night-street stop-and-frisk silhouette ／ 文言：**「逮捕なしで体を触れる？」**

## SHORT #7 →（本編 第7話 Riley）逮捕されてもスマホは見られない
**1つの驚き**：逮捕時に何でも調べられた2世紀の例外＝スマホは令状が要る。
| 時間 | VO | テロップ | 画像 |
|---|---|---|---|
|0:00-0:03|逮捕されても、警察はあなたのスマホを勝手には見られない。|スマホは“例外”|01|
|0:03-0:12|2世紀のあいだ、逮捕時に持っていた物は何でも調べられた。|昔は持ち物は何でも|02,03|
|0:12-0:26|だがスマホには、あなたの人生が丸ごと入っている——メッセージ、写真、居場所。|スマホ＝人生が丸ごと|04,05|
|0:26-0:40|2014年、最高裁は全員一致——スマホだけは別。“令状を取れ”。|2014 全員一致「令状を取れ」|06,07|
|0:40-0:45|続きは本編で。フォローを。|本編はチャンネルへ|07(止め)|

- `short07_01.png` A locked smartphone glowing in an evidence tray, untouchable, dramatic
- `short07_02.png` An old pocket being emptied at booking, a traditional search, no face
- `short07_03.png` A pocket and a phone shown side by side, vastly different contents, conceptual
- `short07_04.png` A single phone radiating a person's whole life — messages, photos, places, conceptual
- `short07_05.png` A phone as a glowing window into an entire life mosaic, no real faces
- `short07_06.png` Nine unified judicial chairs, a 9-0 result, navy and gold
- `short07_07.png` A warrant scroll required before a phone can be opened, conceptual
- **サムネ** `short07_thumb.png` A locked glowing phone in an evidence tray ／ 文言：**「逮捕されてもスマホは見られない」**

## SHORT #8 →（本編 第8話 Carpenter）スマホは、あなたを追跡し続ける
**1つの驚き**：スマホが残す位置の履歴も、警察は令状なしには取れない。
| 時間 | VO | テロップ | 画像 |
|---|---|---|---|
|0:00-0:03|あなたのスマホは行った場所を全部記録している。警察はそれを127日分、令状なしで欲しがった。|127日分の位置を令状なしで|01|
|0:03-0:12|スマホは数分ごとに基地局へ接続し、位置を残す。|数分ごとに位置を記録|02,03|
|0:12-0:26|警察は通信会社から数か月分の位置履歴を入手し、強盗現場の近くに被疑者を“置いた”。|数か月分を会社から入手|04,05|
|0:26-0:40|2018年、最高裁はノー——これほど詳細な位置情報には令状が要る。スマホの“デジタルの足跡”を初めて守った。|2018「位置情報も令状」|06,07|
|0:40-0:45|続きは本編で。フォローを。|本編はチャンネルへ|07(止め)|

- `short08_01.png` A glowing map dotted with a long trail of a single phone's movements, conceptual
- `short08_02.png` A phone pinging a cell tower as a location point lights up, night city
- `short08_03.png` A field of cell towers across a dark city, constant connection, conceptual
- `short08_04.png` Months of location dots accumulating into a detailed map of a life, abstract
- `short08_05.png` A carrier handing over a glowing location-history file, conceptual, no face
- `short08_06.png` A 5-4 split judicial bench, a narrow ruling, navy and gold
- `short08_07.png` A warrant scroll now required over a location map, the digital trail protected
- **サムネ** `short08_thumb.png` A glowing location-trail map of a phone ／ 文言：**「スマホは、あなたを追跡し続ける」**

---

## §3 Codex実装手順
1. 上のプロンプト（末尾共通スタイル付き）で**縦画像を事前生成** → `H:\pd-media\assets\ai\shorts\shortNN\` に指定名で保存（本編07枚＋サムネ1枚）。
2. **縦Remotionコンポジション**（1080×1920）を新規作成：各ショートの画像を時間表どおり並べ、Ken Burns/縦パンで動かす（静止しない）。テロップは時間表どおり大きく焼き込み。
3. ナレ（本編と同じ声・**ElevenLabsで生成OK＝課金承認待ち不要**）or 無ナレ字幕版。BGM控えめ。
4. サムネ＝`shortNN_thumb.png`＋大きな文言（表内の「サムネ文言」）をRemotionで重ねて書き出し。
5. 公開は**6/24以降**・各ゲートで停止。**本人の肖像なし・中立・広告安全**を最終チェック。
