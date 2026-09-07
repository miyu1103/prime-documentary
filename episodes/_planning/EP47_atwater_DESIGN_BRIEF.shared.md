# EP47 atwater — 設計書＆Codex A/B 共有ブリーフ（各ドラフトagentが必ず読む）

> 単一の真実源。EP44/45/46 の同名ファイル群を構造テンプレとして踏襲し、下記 EP47 差分で差し替える。ここに無い数値は SPEC JSON から転記。推測で数値を作らない。

## 0. エピソード同定
- episode_id: `PD-2026-047-atwater` / slug: `atwater` / EP47
- 台本（確定・ロック済・3チェック済）: `episodes/_planning/EP47_atwater_script.en.v001.md`（2,135語・median 12.0分）
- ファクト台帳（Cornell LII一次照合）: `episodes/_planning/EP47_atwater_facts.v001.json`
- SPEC: `episodes/_planning/EP47_atwater_PRODUCTION_SPEC.v001.json`（★数値の出典）
- タイトル（具体シーン宣言型）:
  - A（主）: `Arrested Over a Seatbelt. The Supreme Court Said Police Could.`（≤60字近似・広告安全）
  - B（二人称）: `Police Can Arrest You for a Ticket-Only Offense. Legally.`
  - ※「違法だった」と断定しない（制約1＝合憲とされた）。

## 1. 1シーン1枚・バリエーション0
- still distinct を固有プロンプトで各1枚。--variants 1。ai_prompts still85＝85行＋i2v種16＝shots 101。factory 92本は在庫選抜。

## 2. SPEC 確定値（★出典 EP47_atwater_PRODUCTION_SPEC.v001.json）
- narration **719.3s(12.0分)**@178.1wpm / words **2,135** / mean_shot 3.19s / max_shot 6.0s
- still **85 / 101 / 1.19x(cap2)** ／ factory **92 / 92 / 1.0x(cap1)** ／ motion(i2v) **16 / 32 / 2.0x(cap2)**
- 総カット **225** ／ still-share **0.4489(cap0.45)** ／ first-use **0.8578**
- MG(FigureBeats)ビート floor **30**／ variety floor 3 ／ density floor 2.5/min

## 3. ★正確性6制約（全出力に適用・違反はBLOCKER）
1. **逮捕は合憲＝UPHELD（5-4）。** 罰金刑のみの軽罪でも令状なし現行犯逮捕は第4修正に反しない、と最高裁は判断。「illegal / unconstitutional / struck down」を逮捕自体に使わない。枠は "the Court said police COULD do this."
2. **Souter法廷意見**は逮捕を「pointless indignity（無意味な屈辱）」と認めつつ、4Aを事案ごとの利益衡量に曲げず、救済は立法に委ねた。この nuance を落とさない。逐語 "Atwater's claim to live free of pointless indignity..." は**多数意見**として帰属。
3. **O'Connor 反対**が対抗軸。逐語 "The Court neglects the Fourth Amendment's express command in the name of administrative ease. In so doing, it cloaks the pointless indignity that Gail Atwater suffered with the mantle of reasonableness." を**反対意見**として中立帰属（Courtに帰属させない）。
4. 票決 **5-4**（Souter多数＝Rehnquist・Scalia・Kennedy・Thomas／O'Connor反対＝Stevens・Ginsburg・Breyer）。
5. **Gail Atwater は存命の私人（R2・有罪歴なし＝罰金のみ）**。顔・肖像・身体を描かない・象徴のみ。**同乗の子ども2人を扇情化しない**（年齢を強調しない・"two young children" のみ）。捏造引用禁止。
6. 数値: **罰金上限 $50**（テキサス法 $25-$50・no contest で$50）confidence high。判決日 2001-04-24。Officer Turek。confidence:medium（逮捕年1997・子の年齢）はヘッジ／画面に出さない。

## 4. ビジュアル方針（象徴主義・尊厳・ダーク/シネマティック）
- レーン色（★EP41 gold / EP42 blue / EP43 amber / EP44 teal / EP45 crimson / EP46 green #3F8F5F と区別）: **EP47 accent = civil-violet `#7A5CD0`**。INK `#0A0A0C`。CODEX_B は OP props/AEカード/サムネ accent を必ず `#7A5CD0` に。
- 反復モチーフ: **テキサスの片側二車線の道**・**ピックアップtrックの車内（空のチャイルドシート2つ＝子は象徴のみ）**・**外れたシートベルトのバックル**・**手錠**・**留置のブッキング台/指紋**・**$50の罰金票**・**天秤（罰金のみ↔全逮捕）**・**最高裁列柱/9席**・**"開いた扉と閉じた扉"（救済は立法へ）**。
- 人物は影/後ろ姿/手元/象徴のみ。顔なし。**子どもを扇情化しない**（空のチャイルドシート等の象徴）。
- Act別トーン: HOOK（土＝テキサスの道・シートベルト・手錠・現在形）／OP（"A TRAFFIC STOP"系）／ACT1「その停止」（最短・シートベルト違反→手錠→ブッキング→$50）／ACT2「§1983の問い」（罰金のみの逮捕は不合理な押収か・歴史と実務）／ACT3「合憲」判例核（5-4・Souter "pointless indignity" but permitted・救済は立法・O'Connor反対）／ENDING（あなたの車・"they may, not must" の余韻・立法に委ねられた不満）。

## 5. 技術ゴッチャ（EP39-46の事故から）
- ★**dochighlight figure を使わない**（バグに見える）。figures[] に "kind":"dochighlight" を入れない（grepで0）。
- FigureBeats kind 全小文字。read_prompts 2行形式。`--only S01` で shots=101 確認。
- ★**quote figure は検証済逐語のみ**。Souter逐語＝"Justice Souter, for the Court"、O'Connor逐語＝"Justice O'Connor, dissenting"。attribution厳格。
- film.json ビルダー `scripts/build_atwater_film.py`(EP46 build_tlo_film.py 複製・slug/EP/paths を atwater に・**実素材のみstub禁止**)。★**asset_manifest は stills85＋factory92＋motion16＋overlay12 を全エントリ記載**（public_path必須。EP45事故回避）。
- ゲート入力 `--ep PD-2026-047-atwater`。`--json` は出力→入力に使わない。
- asset_manifest は A↔B で counts/role enum/overlay枚数**一字一致**・role=thumb/still_thumb 不使用(サムネ=also_thumb 6枚)。counts: still_body85/still_i2v_source16/motion16/factory92/overlay12。
- durationInFrames 4項関数＋hookSeconds=8.0明示・composition id `Ep47Atwater`・Root.tsx登録。
- 正確性ゲート `check_atwater_facts.py`(EP46 check_tlo_facts.py 複製・R-ルール：R-DISPO[5-4 UPHELD＝illegal禁止]・R-QUOTE[Souter/O'Connor逐語approved・帰属厳格]・R-FACE[Atwater顔なし・子ども非扇情]・R-HEDGE[$50/2001以外の推定値を断定化しない])。★**R-NUM等の構造ルールは narrative figure のみ対象**（asset_manifest構造カウント・acttitle index 除外＝EP45修正済）。
- AE: フォント厳格解決・sourceRectAtTime**実測**・ローカライズOM/RS・.aep>.jsx assert・per-layer motionBlur・disclosure右下常時。
- レンダ: `remotion render Ep47Atwater ... --public-dir=public_slim --concurrency=4`。★**public→public_slim へ全メディア(img/factory/motion/audio)コピー staging**(EP45事故回避)。完成後 `build_atwater_bgm_real.py`(EP43複製・OFF=11.5)→`composite_atwater_hero.py`(EP43複製・film_offset適用)→全ゲート＋**全編アイボール**。

## 6. AEヒーローカード（6-8枚・値は台帳照合・6制約順守）
- 候補:
  - `5 – 4`（VOTE_SPLIT）＋サブ「THE ARREST STANDS」（制約1＝違法と読ませない）
  - `FINE-ONLY OFFENSE → FULL ARREST`（SPLIT_COMPARE・罰金のみ→全逮捕）
  - O'Connor 逐語 `"...IT CLOAKS THE POINTLESS INDIGNITY ... WITH THE MANTLE OF REASONABLENESS"`（QUOTE_CARD・attribution "Justice O'Connor, dissenting"）
  - Souter 概念 `"POINTLESS INDIGNITY"`（QUOTE/CENTER・attribution "Justice Souter, for the Court"・多数が認めつつ許容）
  - `$50 MAX FINE`（numberticker/stat・no-jail の罰金上限）
  - `2001 · SUPREME COURT`（DATE_STAMP）
  - （任意）`NO JAIL OFFENSE`（CENTER・投獄不能の軽罪でも逮捕可）
  - （任意）`LEFT TO LEGISLATURES`（救済は立法へ）
- カード文言に「illegal / the Court struck it down」を書かない。数値・引用は AE ledger 一致必須。accent `#7A5CD0`。

## 7. 完了条件
- DESIGN: 0〜719.3s全区間タイムライン・各アニメ数値明記・48シーン絵コンテ(象徴・6制約・子ども非扇情)・FigureBeats設計(≥30・小文字kind・変種≥3・dochighlight不使用・quote検証逐語)・AEカード表(§6・accent #7A5CD0)・Composition設定(1920x1080/fps30/id=Ep47Atwater/durationInFrames4項/hookSeconds8.0)。
- CODEX_A: ai_prompts 85本(1枚ずつ・**省略禁止で全85本**)＋i2v16＋factory92選定＆全点目視QC(`select_atwater_factory.py`・--exclude-used --ep PD-2026-047-atwater・EP39-46 sha256被り検証)＋asset_manifest(**stills85＋factory92＋motion16＋overlay12を全エントリ記載**・also_thumb 6枚)。
- CODEX_B: `build_atwater_film.py`(実素材・dochighlight不使用・quote検証逐語・manifest factory/motion全読込)・captions・figures(小文字kind・MG≥30)・Root.tsx登録(Ep47Atwater)・AEカード(実測幅・ledger照合・accent #7A5CD0)・bgm→composite(film_offset適用)・public_slim staging・レンダ・全ゲート(--ep・check_atwater_facts.py)・全編アイボール。
- A↔B 接続点は asset_manifest.v001.json ただ1ファイル(スキーマ一字一致)。
