# EP44 tekoh — 設計書＆Codex A/B 共有ブリーフ（各ドラフトagentが必ず読む）

> 単一の真実源。EP43 の同名ファイル群（DESIGN/CODEX_A/CODEX_B）を構造テンプレとして踏襲し、下記 EP44 差分で数値・内容を差し替える。推測で数値を作らない。ここに無い数値は SPEC JSON から転記。

## 0. エピソード同定
- episode_id: `PD-2026-044-tekoh` / slug: `tekoh` / EP44
- 台本（確定・ロック済）: `episodes/_planning/EP44_tekoh_script.en.v001.md`（2,139語・median 12.0分）
- SPEC: `episodes/_planning/EP44_tekoh_PRODUCTION_SPEC.v001.json`
- タイトルA/B（≤60字・二人称・CTR・★射程を過大化しない・原被疑事実を出さない）:
  - A: `If Police Skip Your Rights, Can You Sue the Officer? The Court Said No.`
  - B: `They Used the Statement You Wrote With No Warning. You Can't Sue.`
  - ※「ミランダ廃止/黙秘権消滅/警察は権利を読まなくてよくなった」系は禁止（制約1）。

## 1. 1シーン1枚・バリエーション0（EP42/43と同一方針）
- still は distinct を固有プロンプトで各1枚。`--variants 1`。ai_prompts は still 85本＝85行＋i2v種16本＝shots 101。factory 93本は在庫選抜。

## 2. SPEC 確定値（★この値で積算。出典 SPEC JSON）
- narration 720.6s（12.0分）@ 178.1wpm / words 2,139 / 視覚シーン48 / 総カット**226** / 平均3.19s
- still **85 / 101 / 1.19x（cap2）** ／ factory **93 / 93 / 1.0x（cap1）** ／ motion(i2v) **16 / 32 / 2.0x（cap2）**
- distinct **194 / 226 = first-use 0.8584** ／ still-share **0.4469（cap0.45）** ／ motion coverage 0.553
- MG（FigureBeats）ビート floor **31**（AEカードは数えない）
- 紙芝居回避: still-cut 101 に対し video(factory93+i2v32)=125 で motion>still を構造保証。

## 3. ★正確性6制約（全出力＝プロンプト・カード文言・タイトル・図表に適用。違反はBLOCKER）
1. 射程を過大化しない。否定されたのは「ミランダ違反“単体”を理由に §1983 で警官を民事で訴える」道だけ。ミランダ自体は刑事公判で有効（未告知供述は排除されうる）。「Miranda is dead / no right to remain silent / police need not read rights」を出力に一切書かない（EP14 Lange型事故）。
2. 6-3（Alito法廷意見／Kagan反対＋Breyer・Sotomayor）。9-0でない。多数/反対を中立帰属。
3. Miranda(1966)/Dickerson(2000) と Vega を混同しない。Vega はミランダを覆していない＝§1983救済のみ否定。
4. §1983 の意味（州の役人を憲法違反で民事提訴する連邦法）を正確に。「刑事免責」と混同しない。§1983一般論で「no immunity」と断定しない（qualified immunityがある）。
5. ★広告適合性（最重要級）: Tekoh の原被疑事実（疑われた罪の性質・刑事裁判で無罪）を**一切名指しせず・描写も表示もしない**。タイトル/サムネ/カード/プロンプト/概要欄のどこにも罪状の性質(語)を出さない。原告は「疑われ、無罪となった私人」として尊厳をもって。
6. Tekoh も Vega も存命の私人（R2）。顔・肖像・身体を描かない。象徴のみ（病院の廊下[夜]・机の上のペンと書面・署名欄・空の取調台・空の陪審席・最高裁列柱・録取書）。
- R1: 実在人物の顔・肖像を生成しない。全生成ビジュアル表示中 `AI-assisted visualization`（右下）常時表示、概要欄1行AI開示。

## 4. ビジュアル方針（象徴主義・尊厳・ダーク/シネマティック）
- レーン色（★EP41 gold #E5B53A / EP42 blue #3B7DD8 / EP43 amber #E0913C と区別）: **EP44 accent = interrogation-teal `#2FA6A0`**。INK `#0A0A0C`。CODEX_B は OP props / AEカード / サムネ accent を必ず `#2FA6A0` に（他話の色を流用しない）。
- 反復モチーフ: **ペン＋署名欄**（警告なしに書かれた書面）。**空の取調台**。**病院の廊下（夜）**。**空の陪審席**（無罪）。**最高裁列柱／9席**。**"守りの柵"の視覚**（prophylactic＝深い権利を囲う柵、柵は権利そのものではない）。**閉じたドア/開いたドア**（救済の扉）。
- 人物は影/後ろ姿/手元/象徴のみ。顔なし。原被疑事実を示唆する画像を作らない（制約5）。
- Act別トーン: HOOK（ペン・署名欄・警告なし）／ACT1「その夜」（最短・現在形・病院廊下・録取）／ACT2「転機」（無罪→民事提訴→§1983→二度の敗訴→第9巡回区）／ACT3「命令」判例核（6-3・prophylactic柵・Kagan反対・最も遅い）／ENDING（あなたの椅子・救済なしの余韻）。

## 5. 技術ゴッチャ（EP39-43の事故から）
- ★**dochighlight figure（黒バー/box/underline）を使わない**（バグに見える＝EP40/41/42で3回指摘）。film.json figures[] に `"kind": "dochighlight"` を入れない（grepで0を確認）。redacted文書が要るなら実書面に "REDACTED" を焼いた still を使う。
- FigureBeats kind は全小文字（numberticker/stat/votetally/timeline/quote/kinetic/lowerthird/acttitle/compbars(※comparebars非実在)/mechanism 等）。大文字は無音描画。
- read_prompts 2行形式。--only S01 で shots=101 確認。
- film.json ビルダー `scripts/build_tekoh_film.py`（EP43 build_caniglia_film.py を複製・slug/EP/ASSET_MAP/NARR/FACTORY_SEL を tekoh に）。git 未追跡＝ビルダーで再生成できる状態を保つ。実素材のみ（stub禁止）。
- ゲート入力は `--ep PD-2026-044-tekoh`。`--json <film.json>` は出力パス→入力に使わない。
- asset_manifest は A↔B で counts/role enum/overlay枚数を一字一致。role=thumb/still_thumb を作らない（サムネは also_thumb=true の body still 6枚）。
- durationInFrames は caseFilmDurationInFrames の4項関数＋hookSeconds明示＋total≤750s assert。
- AEカードのレイアウト名は実装済み集合のみ（DATE_STAMP/CENTER_STACK/MONEY_STACK/SPLIT_COMPARE/ACT_TITLE_CARD/QUOTE_CARD/VOTE_SPLIT/SEAM_TRANSITION）。DESIGNとCODEX_Bのカード表を一字一致。
- 6制約の正確性ゲート名は1つに統一（check_tekoh_facts.py）。DESIGN/A/B同名。
- Root.tsx に `id="Ep44Tekoh"`（CaseFilm）で登録。durationInFrames は caseFilmDurationInFrames(tekohFilm, fps)。
- AE: フォント厳格解決（miss throw）・sourceRectAtTime実測幅・ローカライズOM/RS・ADBE Rotate Z・per-layer motionBlur・aerender前に .aep>.jsx assert。
- レンダ: `remotion render Ep44Tekoh ... --public-dir=public_slim --concurrency=4`。完成後 build_tekoh_bgm.py（実装・EP42 build_young_bgm_real.py を複製）→ composite_tekoh_hero.py（beats.jsonの film_offset_sec を+適用・EP42 composite_young_hero.py を複製）→ 全ゲート＋全編アイボール。

## 6. AEヒーローカード（6-8枚・数値は台帳照合・捏造ゼロ・6制約順守）
- 候補ビート（検証済ファクトのみ）:
  - `6–3` ＋ サブ「ONE DOOR CLOSED」（制約1/2＝ミランダ廃止と読ませない）
  - `MIRANDA STANDS / DICKERSON STANDS`（制約1/3）
  - `A FENCE, NOT THE GROUND`（prophylactic＝柵と深い権利・quote/center）
  - `SECTION 1983`（民事救済の連邦法）
  - `ACQUITTED`（無罪＝12人の陪審が有罪にせず）
  - `2 TRIALS`（民事で二度敗訴）
  - `"...strips … the ability to seek a remedy…"`（Kagan反対の逐語・quote card・中立帰属）
  - `2022 · SUPREME COURT`（date/context）
- カード文言に「Miranda is dead」「no immunity」「原被疑事実」を書かない。数値・引用は AE ledger と一致必須。

## 7. 完了条件（設計パッケージ）
- DESIGN: 0〜720.6s全区間の秒数タイムライン・各アニメの開始/終了フレーム・移動量・イージング種別・damping・スタッガー・motion-blur Trail・最低3背面レイヤー・overflow:hiddenマスク・秒はfps算出で定数化。48シーン絵コンテ（象徴のみ・6制約・原被疑事実の画像禁止）。FigureBeats設計（≥31・小文字kind・変種≥3・**dochighlight不使用**）。AEカード表（§6・accent #2FA6A0）。Composition設定（1920x1080 / fps EP43同値 / id=Ep44Tekoh / durationInFrames4項）。
- CODEX_A: ai_prompts 85本（1枚ずつ・バリエーション0）＋i2v16＋factory93選定＆全点目視QC（select_tekoh_factory.py・--exclude-used --ep PD-2026-044-tekoh・EP39/40/41/42/43 sha256被り検証）＋境界契約 asset_manifest（EP43同型・counts を EP44 値に）。★85本は必ず全部書く（省略禁止）。
- CODEX_B: build_tekoh_film.py 仕様（実素材・stub禁止・dochighlight不使用）・captions（実測narration）・figures（小文字kind・MG≥31）・Root.tsx登録・AEカード（実測幅・ledger照合・レイアウト名実装済みのみ・accent #2FA6A0）・build_tekoh_bgm→composite_tekoh_hero（film_offset適用）・レンダ・全ゲート（--ep 指定・check_tekoh_facts.py）・完成後の全編アイボール。
- A↔B の接続点は asset_manifest.v001.json ただ1ファイル（スキーマ一字一致）。
