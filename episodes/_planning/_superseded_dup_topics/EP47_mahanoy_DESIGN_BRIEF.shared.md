# EP47 mahanoy — 設計書＆Codex A/B 共有ブリーフ（各ドラフトagentが必ず読む）

> 単一の真実源。EP44/45/46 の同名ファイル群を構造テンプレとして踏襲し、下記 EP47 差分で数値・内容を差し替える。ここに無い数値は SPEC JSON から転記。推測で数値を作らない。

## 0. エピソード同定
- episode_id: `PD-2026-047-mahanoy` / slug: `mahanoy` / EP47
- 台本（確定・ロック済・3チェック済）: `episodes/_planning/EP47_mahanoy_script.en.v001.md`（2,131語・median 11.96分）
- ファクト台帳（検証済・slip opinion PDF 一次照合）: `episodes/_planning/EP47_mahanoy_facts.v001.json`（F01–F20・出典付き）
- SPEC: `episodes/_planning/EP47_mahanoy_PRODUCTION_SPEC.v001.json`（★数値の出典）
- タイトル（確定・具体シーン宣言型＝最高保持）:
  - A（主）: `Her Weekend Snapchat Cost Her a Season. Then the Court Stepped In.`※≤60超なら → `A Weekend Snap Got Her Benched. The Supreme Court Stepped In.`（≤60・具体シーン・広告安全）
  - B（二人称代替）: `Can Your School Punish You for a Post You Made Off Campus?`
  - ※「学校は校外投稿を一切罰せない」系の過大化を禁止（制約1）。罵倒語をタイトル/サムネに出さない。

## 1. 1シーン1枚・バリエーション0
- still distinct を固有プロンプトで各1枚。--variants 1。ai_prompts still 85＝85行＋i2v種16＝shots 101。factory 92本は在庫選抜。

## 2. SPEC 確定値（出典 EP47_mahanoy_PRODUCTION_SPEC.v001.json）
- narration **717.9s(11.96分)**@178.1wpm / words **2,131** / mean_shot 3.19s / max_shot 6.0s
- still **85 / 101 / 1.19x(cap2)** ／ factory **92 / 92 / 1.0x(cap1)** ／ motion(i2v) **16 / 32 / 2.0x(cap2)**
- 総カット **225** ／ still-share **101/225 = 0.449(cap0.45)** ／ first-use **193/225 = 0.858**
- MG(FigureBeats)ビート floor **30**（AEカードは数えない）／ variety floor 3 ／ density floor 2.5/min
- 紙芝居回避: still-cut 101 に対し video(factory92+i2v32)=124 で motion>still を構造保証。

## 3. ★正確性6制約（全出力に適用・違反はBLOCKER）
1. **過大化しない。** 最高裁は「学校は校外言論を一切罰せない」とは言っていない。本件の処分を違憲としつつ、**規制余地を明示的に残した**（serious bullying/harassment・threats・cheating やレッスン/論文/PC規則違反・school security の突破）。bright-line を意図的に設定せず。この留保を必ず明記。
2. **Tinker(1969)** がアンカー: 生徒は校門で言論の自由を「脱ぎ捨てない（do not shed ... at the schoolhouse gate）」が、実質的混乱は規制可。校外では学校の Tinker 利益が **diminished（消滅でなく減退）**。正確に。
3. 票決 **8-1**。Breyer 法廷意見／**Thomas 単独反対**／Alito 補足(Gorsuch 同調)。多数/反対/補足を中立帰属。
4. **B.L.（Brandi Levy）は当時未成年**＝最大限配慮。R2: 顔・肖像・身体を描かない・象徴のみ。**罵倒語を一切再現しない**＝投稿は常に "an angry post / a frustrated Snap" と言い換え。distress 扇情化しない。
5. 広告適合: 生徒の言論の自由の物語として枠付け。未成年の苦痛を煽らない・slur を出さない。完全に広告安全。
6. 数値・引用は原典一致: 8-1・JV cheer・varsity 落選・Cocoa Hut・約250人 story・1年出場停止・Third Circuit が「Tinker は校外に及ばず」と広く判断・混乱は「Algebra で数分＋数名の動揺」程度。逐語（Tinker "schoolhouse gate"／Breyer "nurseries of democracy"／4類型）は台帳一致。

## 4. ビジュアル方針（象徴主義・尊厳・現代/シネマティック）
- レーン色（★EP41 gold / EP42 blue / EP43 amber / EP44 teal / EP45 crimson / EP46 green #3F8F5F と区別）: **EP47 accent = digital-violet `#7A5CD0`**（SNS・若年・デジタル）。INK `#0A0A0C`。CODEX_B は OP props/AEカード/サムネ accent を必ず `#7A5CD0` に。
- 反復モチーフ: **スマホ画面（Snap の送信ボタンに親指・24時間カウントダウン）**・**コンビニ駐車場（土曜）**・**フックに掛かった空のチア制服**・**空の観客席/体育館**・**校門/校舎の廊下**・**1969の黒い腕章のシルエット（Tinker）**・**裁判所の長い廊下**・**"nurseries of democracy" ＝苗床/若木の象徴**・**校内 vs 校外の対比**。
- 人物は影/後ろ姿/手元/象徴のみ。**未成年は絶対に肖像化しない**。罵倒語を画面に焼かない（投稿はぼかし/象徴）。
- Act別トーン: HOOK（土曜・駐車場・親指と送信ボタン・24hカウントダウン・顔なし）／OP（"THE WEEKEND SNAP"）／ACT1「土曜・スマホ・部活」（最短・現在形・落選→週末投稿→1年停止）／ACT2「校門(the schoolhouse gate)」（Tinker 1969・下級審の広い線・そのリスク）／ACT3「Diminished, not gone」（判例核・8-1・3特徴・nurseries of democracy・4類型・Alito補足・Thomas反対）／ENDING（駐車場に回帰・"the gate follows you"・冒頭の問いに慎重な答え）。

## 5. 技術ゴッチャ（EP39-46の事故から）
- ★**dochighlight figure（黒バー/box/underline）を使わない**（バグに見える＝3回指摘）。figures[] に "kind":"dochighlight" を入れない(grepで0)。
- FigureBeats kind 全小文字。read_prompts 2行形式。`--only S01` で shots=101 確認。
- ★**quote figure は検証済逐語のみ**（EP43 R-PAYTON 事故）。Tinker "schoolhouse gate"／Breyer "nurseries of democracy" は台帳一致・attribution 明記（Tinker は "Tinker v. Des Moines, 1969"、Breyer は "Justice Breyer, for the Court"）。**罵倒語を quote に入れない**。
- film.json ビルダー `scripts/build_mahanoy_film.py`(EP46 build_kelo_film.py を複製・slug/EP/paths を mahanoy に・**実素材のみstub禁止**・grepでstub/placeholder/dryrun=0)。
- ゲート入力 `--ep PD-2026-047-mahanoy`。`--json` は出力→入力に使わない。
- asset_manifest は A↔B で counts/role enum/overlay枚数**一字一致**・role=thumb/still_thumb 不使用(サムネ=also_thumb 6枚)。counts: still_body85/still_i2v_source16/motion16/factory92/overlay12。
- durationInFrames 4項関数＋hookSeconds=8.0明示＋total≈752s（narr717.9）。AEレイアウト名は**実装済み集合のみ**(DATE_STAMP/CENTER_STACK/MONEY_STACK/SPLIT_COMPARE/ACT_TITLE_CARD/QUOTE_CARD/VOTE_SPLIT/SEAM_TRANSITION)・DESIGN↔CODEX_B一字一致。正確性ゲート名 `check_mahanoy_facts.py` に統一（R-OVERCLAIM[「never punish off-campus」系を弾く]/R-VOTE[8-1・attribution]/R-QUOTE[Tinker/Breyer逐語のapproved化]/R-MINOR[B.L.顔なし・slur非再現]）。composition id `Ep47Mahanoy`。
- AE: フォント厳格解決・sourceRectAtTime**実測**・ローカライズOM/RS・.aep>.jsx assert・per-layer motionBlur・disclosure右下常時。
- レンダ: `remotion render Ep47Mahanoy ... --public-dir=public_slim --concurrency=4`。完成後 `build_mahanoy_bgm_real.py`(EP43 複製・OFF=hook+3.5)→`composite_mahanoy_hero.py`(EP43 複製・film_offset適用)→全ゲート＋**全編アイボール**。

## 6. AEヒーローカード（6-8枚・値は台帳照合・6制約順守）
- 候補:
  - `8 – 1`（VOTE_SPLIT）＋サブ「DIMINISHED, NOT GONE」（制約1＝校外を治外法権と読ませない）
  - `ON CAMPUS  /  OFF CAMPUS`（SPLIT_COMPARE・学校の利益の強弱）
  - Tinker 逐語 `"STUDENTS DO NOT SHED THEIR RIGHTS ... AT THE SCHOOLHOUSE GATE"`（QUOTE_CARD・attribution "Tinker v. Des Moines, 1969"）
  - Breyer 逐語 `"THE NURSERIES OF DEMOCRACY"`（QUOTE_CARD・attribution "Justice Breyer, for the Court"）
  - `STILL REGULABLE`（CENTER_STACK）＋サブ「THREATS · HARASSMENT · CHEATING · SECURITY」（制約1＝残された4類型）
  - `2021 · SUPREME COURT`（DATE_STAMP）
  - （任意）`A WEEKEND SNAP`（ACT_TITLE系・24hで消える投稿のモチーフ）
  - （任意）Alito 補足の「A SLICE OF PARENTAL AUTHORITY」系（CENTER・attribution "Justice Alito, concurring"）
- カード文言に「schools can never punish」「slur/罵倒語」を書かない。数値・引用は AE ledger 一致必須。accent `#7A5CD0`。

## 7. 完了条件
- DESIGN: 0〜717.9s全区間タイムライン・各アニメ数値明記・48シーン絵コンテ(象徴・6制約・**未成年の肖像化禁止**・slur非表示)・FigureBeats設計(≥30・小文字kind・変種≥3・dochighlight不使用・quote検証逐語)・AEカード表(§6・accent #7A5CD0)・Composition設定(1920x1080/fps 30/id=Ep47Mahanoy/durationInFrames4項/hookSeconds=8.0)。
- CODEX_A: ai_prompts 85本(1枚ずつ・**省略禁止で全85本**)＋i2v16＋factory92選定＆全点目視QC(`select_mahanoy_factory.py`・--exclude-used --ep PD-2026-047-mahanoy・EP39-46 sha256被り検証)＋asset_manifest(EP46同型・counts を EP47 値に・also_thumb 6枚)。
- CODEX_B: `build_mahanoy_film.py`(実素材・dochighlight不使用・quote検証逐語)・captions(実測narration・+offset)・figures(小文字kind・MG≥30)・Root.tsx登録(Ep47Mahanoy)・AEカード(実測幅・ledger照合・accent #7A5CD0)・bgm→composite(film_offset適用)・レンダ・全ゲート(--ep・`check_mahanoy_facts.py`)・全編アイボール。
- A↔B 接続点は asset_manifest.v001.json ただ1ファイル(スキーマ一字一致)。
