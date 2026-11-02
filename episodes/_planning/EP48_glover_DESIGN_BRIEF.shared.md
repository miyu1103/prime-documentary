# EP48 glover — 設計書＆Codex A/B 共有ブリーフ（各ドラフトagentが必ず読む）

> 単一の真実源。EP46/47 の同名ファイル群を構造テンプレとして踏襲し、下記 EP48 差分で差し替える。ここに無い数値は SPEC JSON から転記。推測で数値を作らない。

## 0. エピソード同定
- episode_id: `PD-2026-048-glover` / slug: `glover` / EP48
- 台本（確定・ロック済・3チェック済）: `episodes/_planning/EP48_glover_script.en.v001.md`（2,136語・median 12.0分）
- ファクト台帳（Cornell LII一次照合）: `episodes/_planning/EP48_glover_facts.v001.json`（G01–G19）
- SPEC: `episodes/_planning/EP48_glover_PRODUCTION_SPEC.v001.json`（★数値の出典）
- タイトル（具体シーン宣言型＝最高保持）:
  - A（主）: `A Cop Ran Your Plate and Pulled You Over. He Never Saw You Break a Law.`
  - B（二人称）: `Can a Cop Stop Your Car Just Because of Who Owns It?`
  - ※「警察はどんな車でも停められる」系の過大化を禁止（制約1）。

## 1. 1シーン1枚・バリエーション0
- still distinct を固有プロンプトで各1枚。--variants 1。ai_prompts still85＝85行＋i2v種16＝shots 101。factory 92本は在庫選抜。

## 2. SPEC 確定値（★出典 EP48_glover_PRODUCTION_SPEC.v001.json）
- narration **719.6s（12.0分）**@178.1wpm / words **2,136**／ mean_shot 3.19s / max_shot 6.0s
- still **85 / 101 / 1.19x（cap2）** ／ factory **92 / 92 / 1.0x（cap1）** ／ motion(i2v) **16 / 32 / 2.0x（cap2）**
- 総カット **225** ／ still-share **0.449（cap0.45）** ／ first-use **0.858** ／ MG floor **30** ／ variety≥3 ／ density≥2.5/min

## 3. ★正確性6制約（全出力に適用・違反はBLOCKER）
1. **過大化しない。** 判示は「登録者が運転していると推認できる情報しかなく、それを打ち消す情報が officer に無い場合、その停止は合理的（reasonable suspicion）」というもの。**推認は打ち消す情報があれば消える**（例：運転者が明らかに所有者と別人＝60代の所有者なのに20代が運転）。「警察はどんな車でも停められる／プレート照合だけで誰でも停められる」と書かない。
2. **reasonable suspicion（簡易な捜査的停止＝Terry級）であって probable cause ではない。** 正確に区別。
3. 票決 **8-1**（Thomas法廷意見／**Kagan補足＝Ginsburg同調**が限界を強調[revocation≠suspension・一目で別人なら推認消滅]／**Sotomayor単独反対**）。逐語は反対/補足として中立帰属。
4. **Charles Glover は存命の私人（免許取消中の運転で有罪）**＝R2・顔/肖像なし・象徴のみ。物語は「**あなたの車・停止の合法性**」であって彼を美化しない。原被疑事実（運転免許取消）以外の犯罪性を出さない。
5. 広告適合：交通停止・4Aの物語として枠付け。完全に広告安全。
6. 数値・引用は原典一致（8-1・2020・589 U.S.・White... いや Thomas執筆）。confidence:medium（保安官の詳細・車種・手続経緯）はヘッジ／画面に断定で出さない。

## 4. ビジュアル方針（象徴主義・尊厳・ダーク/シネマティック）
- レーン色（★EP41-47 と区別）: **EP48 accent = patrol-steel `#5B8DB8`**。INK `#0A0A0C`。CODEX_B は OP props/AEカード/サムネ accent を必ず `#5B8DB8` に。
- 反復モチーフ：**パトカーのラップトップに打たれたプレート番号**・**照合ヒット画面**・**夜のハイウェイ/テールランプ**・**免許証（取消の判子）**・**登録票**・**天秤（推認 vs 個別的疑い）**・**"所有者≠運転者"の対比（60代 vs 20代のシルエット）**・**最高裁列柱/9席（8-1）**。
- 人物は影/後ろ姿/手元/象徴のみ。顔なし。
- Act別トーン：HOOK（夜・パトカー・プレート入力・ヒット・停止）／OP（"THE PLATE"系）／ACT1「その停止」（最短・プレート照合→取消判明→運転者未確認で停止）／ACT2「推認の論理」（reasonable suspicion・登録者=運転者の推認・Terry級）／ACT3「限界」判例核（8-1・打ち消す情報で推認消滅・Kagan補足・Sotomayor反対）／ENDING（あなたのプレート・推認が及ぶ範囲の余韻）。

## 5. 技術ゴッチャ（EP39-47の事故から・★全て必須）
- ★**hookSeconds=8.0**（8秒hook cold-open）＋**glover用の正しいhookLine**（caniglia/他話の流用禁止・例「A plate. A hit. A stop you never saw coming.」）。film builderに焼く（EP44/45でhookSeconds=0＋流用hookLine事故）。
- ★**asset_manifest の factory[92]/motion[16]/overlay[12] を public_path で全エントリ記載**（EP45で空→build失敗）。role=thumb/still_thumb 不使用（サムネ=also_thumb 6枚）。
- ★**film.json の figures を実 FigureBeats.tsx union で全数検証**（timeline→events[]／bar→data[]／compbars→items[]／routemap・pindropmap→pins[]／kinetic→lines[]／mechanism→{closingdoor,gears,faultsplit}／votetally→majority+dissent）。不正フィールドは render クラッシュ。dochighlight=0・stub=0。
- ★**dochighlight不使用**（黒バー＝バグに見える・3回指摘）。
- ★**quote figure は検証済逐語のみ**（EP43 R-PAYTON事故）。Sotomayor反対＝attribution "Justice Sotomayor, dissenting"／Kagan補足＝"Justice Kagan, concurring"。
- ビルダー `scripts/build_glover_film.py`（EP46 build_tlo_film.py or build_cleveland_film.py 複製・実素材のみ）。ゲート入力 `--ep PD-2026-048-glover`。`--json` は出力→入力に使わない。
- **AEカード**：ビルダー `scripts/ae/build_glover_hero_cards.py`（**cleveland修正版を複製**＝実測フィット＋引用折返し＋**repo path出力**＋**aerender二段構成**［AfterFXで.aep構築→aerender描画］）。**ACCENT は RGBタプルで #5B8DB8 = [0.357,0.553,0.722]**（hexコメントだけ変えない）。offset は hookSeconds(8.0)+3.5=11.5。beats を実発話に再アンカー。
- **BGM** `scripts/build_glover_bgm_real.py`（EP43複製・OFF=11.5）→ **composite** `scripts/composite_glover_hero.py`（film_offset適用）。
- 正確性ゲート `scripts/check_glover_facts.py`（EP45 check_cleveland_facts.py 複製・**R-NUMはasset_manifest除外＋indexキーskip・acttitle除外**を継承）。rules：R-OVERCLAIM[「stop any car」「probable cause required」を弾く]・R-STANDARD[reasonable suspicion]・R-VOTE[8-1]・R-QUOTE[Sotomayor/Kagan逐語]・R-FACE[Glover顔なし]。fact数値をALLOWED_NUMBERSに。
- Root.tsx に `id="Ep48Glover"` 登録（durationInFrames=caseFilmDurationInFrames・hookSeconds=8.0）。typecheck。
- レンダ: `remotion render Ep48Glover ... --public-dir=public_slim --concurrency=4`。★**public→public_slim staging＋全media解決0確認**。完成後**全編3回チェック**（本編・AEカード・VO同期・hookライン）。

## 6. AEヒーローカード（6-8枚・数値は台帳照合・6制約順守・accent #5B8DB8）
- 候補：`8 – 3`… いや **`8 – 1`**（VOTE_SPLIT）＋「A NARROW RULE」（制約1）／`REASONABLE SUSPICION`（CENTER・probable causeでない）／`THE OWNER IS PROBABLY DRIVING`（SPLIT_COMPARE系）＋「UNLESS THE OFFICER KNOWS OTHERWISE」（限界）／`2020 · SUPREME COURT`（DATE）／Sotomayor逐語 QUOTE（"...paved the road to finding reasonable suspicion based on nothing more than a demographic profile" attribution "Justice Sotomayor, dissenting"）／（任意）`REVOCATION, NOT SUSPENSION`（Kagan限界）。
- 「stop any car」「probable cause」を書かない。accent #5B8DB8。

## 7. 完了条件
- DESIGN（`EP48_glover_DESIGN_and_CODEX_PROMPTS.v001.md`）：0〜719.6s全区間タイムライン・各アニメ数値・48シーン絵コンテ（象徴・6制約・Glover顔なし）・FigureBeats設計（≥30・小文字kind・変種≥3・**実union準拠**・dochighlight不使用・quote検証逐語）・AEカード表（§6・#5B8DB8）・Composition（1920x1080/fps30/id=Ep48Glover/durationInFrames4項/hookSeconds8.0）。
- CODEX_A：ai_prompts 85本（全記載）＋i2v16＋factory92選定（select_glover_factory.py・--exclude-used --ep PD-2026-048-glover・EP39-47 sha256被り検証）＋asset_manifest（**factory92/motion16/overlay12を全エントリpublic_path記載**・also_thumb 6枚）。
- CODEX_B：build_glover_film.py（実素材・hookSeconds8.0・正しいhookLine・figures実union準拠・dochighlight不使用・manifest factory/motion全読込）・captions・figures・Root登録・AEカード（cleveland修正版複製・repo path・aerender二段・ACCENT RGB #5B8DB8・実測フィット）・bgm→composite（offset11.5）・public_slim staging・レンダ・全ゲート（--ep・check_glover_facts.py）・全編3回チェック。
- A↔B 接続点は asset_manifest.v001.json ただ1ファイル。
