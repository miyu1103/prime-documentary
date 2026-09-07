# EP42 young — 設計書＆Codex A/B 共有ブリーフ（各ドラフトagentが必ず読む）

> このファイルは EP42 設計パッケージ（DESIGN / CODEX_A / CODEX_B）を書く全 agent の
> 単一の真実源。EP41 の同名ファイルを構造テンプレとして踏襲しつつ、下記の EP42 差分で数値・
> 内容を差し替える。**推測で数値を作らない。ここに無い数値は SPEC JSON から転記する。**

## 0. エピソード同定
- episode_id: `PD-2026-042-young` / slug: `young` / EP42
- 台本（確定・ロック済）: `episodes/_planning/EP42_young_script.en.v001.md`（2,140語・median 12.0分）
- SPEC（機械生成・唯一の数値源）: `episodes/_planning/EP42_young_PRODUCTION_SPEC.v001.json`
- タイトル A/B（≤60字・二人称・CTR）:
  - A: `Police Raided the Wrong House. What Does the Law Owe You?`
  - B: `They Broke Down Her Door by Mistake. The Law Shrugged.`

## 1. ★★ 最重要の新前提: 1シーン1枚・バリエーション0 ★★
- Codex の画像生成は SDXL より高精度。**同一ショットの複数バリエーション（_01/_02/_03）を作らない。**
- EP41 は「36シーン×3バリエーション=108枚」で反復回避を水増ししていた。**EP42 は禁止。**
- 代わりに **distinct still を固有プロンプトで各1枚ずつ生成**する。
  - `ai_prompts.v001.md` は **still 85本＝85行の固有プロンプト**（`generate_sdxl_4k.py` の `read_prompts()` 2行形式）。
  - `generate_sdxl_4k.py` は **`--variants 1`**（または variants 指定なし）で回す。**`--variants 3` は使わない。**
  - i2v モーション種は **16枚**（各1枚、これもバリエーション0）。
- 総生成画像 = **still 85 + motion seed 16 = 101枚（各1回）**。factory は生成でなく在庫選抜。
- この前提を CODEX_A の A-1 / §3 / §5 / 完了条件、DESIGN の素材レイヤー節に一貫反映する。

## 2. SPEC 確定値（★この値で積算・勝手に変えない。出典 SPEC JSON）
- narration 720.9s（12.0分）@ 178.1 wpm / words 2,140
- 視覚シーン（narrative）: 48（derive: S01..S48）
- 総カット **226** / 平均ショット 3.19s（cap 6.0）
- 素材内訳（distinct / cuts / per-asset上限）:
  - **still 85 distinct / 101 cuts / 1.19x（cap 2）** ← 85本を各1枚生成（バリエーション0）
  - **factory 93 distinct / 93 cuts / 1.0x（cap 1）** ← 在庫11,000本超から選抜・全点目視QC・EP39/40/41とsha256被りゼロ
  - **motion(i2v) 16 distinct / 32 cuts / 2.0x（cap 2）**
  - distinct 合計 **194 / 226 = first-use 0.8584（floor 0.70）** ✓
  - still-share **0.4469（cap 0.45）** ✓ ／ motion coverage 0.553（floor 0.45）✓
- MG（FigureBeats）ビート floor **31**（film.json 内。AEカードはmotion_densityに数えない）
- 紙芝居回避: still-cut 101 に対し video(factory 93 + i2v 32)=125 で構造的に motion>still を担保。**stillを増やしてfactoryを削るな。**

## 3. ★正確性6制約（全 agent が全出力＝プロンプト・カード文言・タイトル・図表に適用。違反はBLOCKER）
1. 和解≠責任認定。「裁判所が違憲/責任を認定」不可。使えるのは「市が290万ドル支払いに同意・市議会が48-0で承認（と報じられる）」まで。
2. no-knock令状と断定しない。令状は「search warrant（有効・判事署名）」のみ。カード/プロンプトに "no-knock" を出さない。
3. 改革は否決。Anjanette Young Ordinance は2022/11に10-4否決・不成立・現行も合法。「法が変わった/彼女が法を変えた」不可。
4. Hudsonの射程を圧縮しない。knock-and-announceは今も憲法上の "command"。否定されたのは救済としての証拠排除のみ。Scaliaの「民事訴訟で十分」論拠はPart IV=4名のみ・Kennedyは署名せず（台本ACT3に明記済）。
5. Booker T. Hudson本人を主役化しない（R3・薬物有罪の存命者）。ビジュアルは人物化せず、Detroitの戸口/敷居の象徴のみ。名は制度説明としての言及に限定。
6. Young（R2・実在私人）の着替え中/着衣なしは非グラフィック・象徴のみ（開いたドア・散らばった書類・手錠・時計・足首モニタのアイコン・空席）。顔・身体・肖像を一切描かない。
- 加えて **R1**: 実在人物の顔・肖像を生成しない。全生成ビジュアル表示中は `AI-assisted visualization`（右下）常時表示、概要欄1行AI開示。

## 4. ビジュアル方針（象徴主義・尊厳・ダーク/シネマティック）
- パレット: 夜のシカゴ西部の室内、法廷の大理石、第4修正の文言を壁に走る光、空の9席、使われないガベル。
- 反復モチーフ: **ドア**（冒頭の割れる戸口→結末の閉じた静かなドア・夜明けの光）。**時計**。**手錠**。**足首モニタ**。**マニラ封筒/黒塗り書類**（判読不能テキスト＝accuracy_lock）。**小切手＋空白の過失欄**。**市議会の投票掲示板**。
- 人物は影/後ろ姿/手元/象徴のみ。顔なし。Young も Hudson も個人として描かない。
- Act別トーン: ACT1（踏み込み・現在形・断片・速い）／ACT2（映像秘匿・テレビの光）／ACT3（判例・最も遅く荘厳・大理石と光）／ACT4（小切手・議会・否決）／ENDING（閉じたドア・夜明け）。

## 5. 技術ゴッチャ（機械精度・EP39-41の事故から）
- FigureBeats.tsx の kind は **全部小文字**: numberticker, timeline, bar, kinetic, acttitle, lowerthird, dochighlight, routemap, pindropmap, regionmap, compbars（※comparebarsは存在しない）, mechanism, quote, stat, votetally 等。大文字は無音描画。
- `read_prompts()` 形式: 「- \`S01.png\`」の次行に「<positive> ... Avoid: <negative>」。書いたら `--only S01` で拾い数を確認。
- film.json ビルダーは `scripts/build_young_film.py`（EP41 `build_thompson_film.py` を複製・young用に。ASSET_MAP/NARR/FACTORY_SEL パスを young に）。**film.json は git 未追跡＝ビルダーで再生成できる状態を保つ。**
- ゲートの入力指定は `--ep PD-2026-042-young`。**`--json <film.json>` は出力パス（上書き事故）なので入力に使わない。**
- AE: フォントは getFontsByFamilyNameAndStyleName で厳格解決（miss は throw、フォールバック禁止）。テキスト幅は sourceRectAtTime(t,false).width で実測（advance-width推定は禁止＝EP40の文字切れ原因）。OM/RS はローカライズ名（RS「最良設定」/ OM「H.264 - レンダリング設定を一致 - 15 Mbps」）。ADBE Rotate Z。per-layer motionBlur。aerender 前に .aep mtime > .jsx を assert。
- レンダ: `remotion render Ep42Young ... --public-dir=public_slim --concurrency=4`（Root.tsx に `id="Ep42Young"` を CaseFilm で登録。durationInFrames は caseFilmDurationInFrames(youngFilm, fps)）。
- 完成後: build_young_bgm.py → composite_young_hero.py（AEカード合成）→ 全ゲート＋**全編アイボール**。

## 6. AEヒーローカード（EP41同様 6-8枚。数値は台帳照合・捏造ゼロ）
- 候補ビート（台本の検証済ファクトのみ・6制約順守）:
  - `5 TO 4`（Hudson 判決・count-up は settle 値で確認）
  - `KNOCK. AND ANNOUNCE.` → `STILL A COMMAND`（射程非圧縮の視覚化・制約4）
  - `48–0`（市議会承認・「reported」枠・制約1。責任認定でない旨のサブ）
  - `10–4`（Ordinance 否決・制約3。"REJECTED"）
  - `$2.9M`（和解額。サブ「no finding of fault」・制約1）
  - `~16 MONTHS / ~100 ALLEGED`（COPA。"alleged" を必ず）
  - `3–5 SECONDS`（Hudson の進入待機・制度説明）
  - `SECTION 1983`（残る唯一の救済＝民事）
- カード文言に "no-knock"・"unconstitutional"・"she changed the law" を書かない。数値は AE ledger と一致必須。

## 7. 完了条件（設計パッケージとして）
- DESIGN: 秒数ベースのタイムライン（0.5s刻みの全区間）・各アニメの開始/終了フレーム・移動量・イージング種別・damping を数値明記（CLAUDE.md 品質ルール準拠：等速禁止・opacity単独禁止・スタッガー・motion-blur Trail・最低3背面レイヤー・overflow:hidden マスク切れ上がり・秒はfps算出で定数化）。
- CODEX_A: ai_prompts 85本（1枚ずつ・バリエーション0）＋ i2v 16 ＋ factory 93 選定＆全点目視QC手順＋境界契約 asset_manifest。
- CODEX_B: build_young_film.py 仕様・captions（実測narration）・figures（FigureBeats小文字kind・MG beats≥31）・Root.tsx登録・AEカード・レンダ・ゲート。
- A↔B の接続点は asset_manifest.v001.json ただ1ファイル（EP41同型・counts を EP42 値に）。
