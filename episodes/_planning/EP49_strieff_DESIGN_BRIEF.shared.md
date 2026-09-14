# EP49 strieff — 設計書＆Codex A/B 共有ブリーフ（各ドラフトagentが必ず読む）

> 単一の真実源。EP46/47/48 の同名ファイル群を構造テンプレとして踏襲し、下記 EP49 差分で差し替える。ここに無い数値は SPEC JSON から転記。推測で数値を作らない。

## 0. エピソード同定
- episode_id: `PD-2026-049-strieff` / slug: `strieff` / EP49
- 台本（確定・ロック済・3チェック済）: `episodes/_planning/EP49_strieff_script.en.v001.md`（2,139語・median 12.0分）
- ファクト台帳（Cornell LII一次照合）: `episodes/_planning/EP49_strieff_facts.v001.json`（S00–S19）
- SPEC: `episodes/_planning/EP49_strieff_PRODUCTION_SPEC.v001.json`（★数値の出典）
- タイトル（具体シーン宣言型）:
  - A（主）: `The Stop Was Illegal. They Searched You Anyway. The Court Said It Counts.`
  - B（二人称）: `A Cop Stops You for No Reason, Then Finds a Warrant. Now What?`
  - ※「停止は合法だった」「排除法則は廃止された」と書かない（制約1）。

## 1. 1シーン1枚・バリエーション0
- still distinct を固有プロンプトで各1枚。--variants 1。ai_prompts still85＝85行＋i2v種16＝shots 101。factory 93本は在庫選抜。

## 2. SPEC 確定値（★出典 EP49_strieff_PRODUCTION_SPEC.v001.json）
- narration **720.6s（12.0分）**@178.1wpm / words **2,139**／ mean_shot 3.19s / max_shot 6.0s
- still **85 / 101 / 1.19x（cap2）** ／ factory **93 / 93 / 1.0x（cap1）** ／ motion(i2v) **16 / 32 / 2.0x（cap2）**
- 総カット **226** ／ still-share **≤0.45** ／ first-use **~0.858** ／ MG floor **31** ／ variety≥3 ／ density≥2.5/min

## 3. ★正確性6制約（全出力に適用・違反はBLOCKER）
1. **停止は違法だった（州が譲歩・最高裁も認定）。「停止は合法」と書かない。** 証拠が使えるのは**先在する令状が違法な停止と発見の因果を"attenuate"（希釈/遮断）したから**という一点のみ。排除法則は**廃止でなく"狭められた"**（「abolished」と書かない）。
2. **attenuation 3要素**（Brown v. Illinois）：①時間的近接（数分＝抑制寄り）②**介在事情＝先在する有効な令状**（多数の決め手・鎖を断つ）③**警察の違法の目的/悪質性（flagrancy）**（最高裁は「せいぜい過失、悪質でない」と評価＝州寄り）。②③が①を上回った。正確に。
3. 票決 **5-3**（Thomas法廷意見＝Roberts・Kennedy・Breyer・Alito／**Sotomayor反対**[Ginsburgが I-III同調・Part IV "carceral state" は Sotomayor単独]／**Kagan反対**[Ginsburg同調]）。**Scalia死去で空席＝8名**。逐語は反対として中立帰属。
4. **Edward Strieff は存命の私人（本件後に薬物所持で有罪）**＝R2・顔/肖像なし・象徴のみ。薬物は臨床的最小限。物語は**排除法則＋違法な停止が生む結果**であって彼を美化しない。
5. 広告適合：4A/排除法則の物語として枠付け。metham... は臨床的に最小限。完全に広告安全。
6. 数値・引用は原典一致。**Sotomayor "carceral state" 逐語**（"...you are not a citizen of a democracy but the subject of a carceral state, just waiting to be cataloged."）＋"anyone's dignity can be violated in this manner"＋Kagan逐語（違法停止のインセンティブ）。★**"we are all harmed" は逐語でない＝使わない**（agentが確認済）。confidence:medium（Fackrell名・監視期間・2006年・手続経緯）はヘッジ／画面に断定で出さない。

## 4. ビジュアル方針（象徴主義・尊厳・ダーク/シネマティック）
- レーン色（★EP41-48 と区別）: **EP49 accent = somber-plum `#9C6BAA`**。INK `#0A0A0C`。CODEX_B は OP props/AEカード/サムネ accent を必ず `#9C6BAA` に。
- 反復モチーフ：**夜の家から出てくる人影（後ろ姿）**・**理由なき停止（パトカーのライト）**・**IDの照会**・**令状ヒットの画面**・**手錠**・**"断ち切られた鎖"（因果の遮断＝attenuation の視覚）**・**空席（Scalia＝8席）**・**天秤（3要素）**・**最高裁列柱**・**カタログ化される市民（Sotomayorの比喩＝ファイル/記録の壁）**。
- 人物は影/後ろ姿/手元/象徴のみ。顔なし。
- Act別トーン：HOOK（夜・家から出る人影・理由なき停止・ID照会・令状ヒット）／OP（"THE ILLEGAL STOP"系）／ACT1「その停止」（最短・違法な停止→令状→逮捕→捜索→発見）／ACT2「排除法則と例外」（本来は抑制／attenuation の例外・3要素）／ACT3「5-3と反対」判例核（Scalia空席・多数の論理・**Sotomayor "carceral state"**・Kaganのインセンティブ）／ENDING（あなたが理由なく停められたら・排除法則が狭まった余韻）。

## 5. 技術ゴッチャ（EP39-48の事故から・★全て必須）
- ★**hookSeconds=8.0**＋**strieff用の正しいhookLine**（流用禁止・例「A stop with no reason. A warrant. A search the law now allows.」）。film builderに焼く。
- ★**asset_manifest の factory[93]/motion[16]/overlay[12] を public_path で全エントリ記載**。role=thumb/still_thumb 不使用（サムネ=also_thumb 6枚）。
- ★**film.json の figures を実 FigureBeats.tsx union で全数検証**（timeline→events[]／bar→data[]／compbars→items[]／routemap・pindropmap→pins[]／kinetic→lines[]／mechanism→{closingdoor,gears,faultsplit}／votetally→majority+dissent）。dochighlight=0・stub=0。
- ★**dochighlight不使用**。★**quote figure は検証済逐語のみ**。Sotomayor反対＝attribution "Justice Sotomayor, dissenting"／Kagan反対＝"Justice Kagan, dissenting"。
- ビルダー `scripts/build_strieff_film.py`（EP48 build_glover_film.py or build_cleveland_film.py 複製・実素材のみ）。ゲート入力 `--ep PD-2026-049-strieff`。
- **AEカード** `scripts/ae/build_strieff_hero_cards.py`（**cleveland修正版を複製**＝実測フィット＋引用折返し＋**repo path出力**＋**aerender二段構成**）。**ACCENT RGBタプルで #9C6BAA = [0.612,0.420,0.667]**。offset=hookSeconds(8.0)+3.5=11.5。beatsを実発話に再アンカー。
- **BGM** `scripts/build_strieff_bgm_real.py`（EP43複製・OFF=11.5）→ **composite** `scripts/composite_strieff_hero.py`。
- 正確性ゲート `scripts/check_strieff_facts.py`（EP45複製・**R-NUM asset_manifest除外＋indexキーskip・acttitle除外**継承）。rules：R-LEGAL[「stop was legal」「exclusionary rule abolished」を弾く]・R-ATTEN[attenuation/3要素の枠]・R-VOTE[5-3・Scalia空席]・R-QUOTE[Sotomayor/Kagan逐語・"we are all harmed"禁止]・R-FACE[Strieff顔なし・薬物非扇情]。fact数値をALLOWED_NUMBERSに。
- Root.tsx `id="Ep49Strieff"` 登録・hookSeconds=8.0・typecheck。
- レンダ: `remotion render Ep49Strieff ... --public-dir=public_slim --concurrency=4`。★public→public_slim staging＋media解決0。完成後**全編3回チェック**。

## 6. AEヒーローカード（6-8枚・値は台帳照合・6制約順守・accent #9C6BAA）
- 候補：`5 – 3`（VOTE_SPLIT）＋「AN 8-JUSTICE COURT · SCALIA'S SEAT EMPTY」（Scalia空席）／`THE STOP WAS ILLEGAL`（CENTER）＋「BUT THE EVIDENCE STAYED」（制約1）／`ATTENUATION`（SPLIT/CENTER）＋「THE WARRANT BROKE THE CHAIN」（3要素の②）／Sotomayor逐語 QUOTE（"...THE SUBJECT OF A CARCERAL STATE, JUST WAITING TO BE CATALOGED" attribution "Justice Sotomayor, dissenting"）／`2016 · SUPREME COURT`（DATE）／（任意）Kagan「THE INCENTIVE TO VIOLATE」逐語。
- 「the stop was legal」「exclusionary rule abolished」「we are all harmed」を書かない。accent #9C6BAA。

## 7. 完了条件
- DESIGN（`EP49_strieff_DESIGN_and_CODEX_PROMPTS.v001.md`）：0〜720.6s全区間タイムライン・各アニメ数値・48シーン絵コンテ（象徴・6制約・Strieff顔なし・薬物非扇情）・FigureBeats設計（≥31・小文字kind・変種≥3・**実union準拠**・dochighlight不使用・quote検証逐語）・AEカード表（§6・#9C6BAA）・Composition（id=Ep49Strieff/durationInFrames4項/hookSeconds8.0）。
- CODEX_A：ai_prompts 85本（全記載）＋i2v16＋factory93選定（select_strieff_factory.py・--exclude-used --ep PD-2026-049-strieff・EP39-48 sha256被り検証）＋asset_manifest（**factory93/motion16/overlay12を全エントリpublic_path記載**・also_thumb 6枚）。
- CODEX_B：build_strieff_film.py（実素材・hookSeconds8.0・正しいhookLine・figures実union準拠・manifest全読込）・captions・figures・Root登録・AEカード（cleveland修正版複製・repo path・aerender二段・ACCENT RGB #9C6BAA・実測フィット）・bgm→composite（offset11.5）・public_slim staging・レンダ・全ゲート（--ep・check_strieff_facts.py）・全編3回チェック。
- A↔B 接続点は asset_manifest.v001.json ただ1ファイル。
