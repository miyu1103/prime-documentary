# EP46 tlo — 設計書＆Codex A/B 共有ブリーフ（各ドラフトagentが必ず読む）

> 単一の真実源。EP44/45 の同名ファイル群（DESIGN/CODEX_A/CODEX_B）を構造テンプレとして踏襲し、下記 EP46 差分で数値・内容を差し替える。ここに無い数値は SPEC JSON から転記。推測で数値を作らない。

## 0. エピソード同定
- episode_id: `PD-2026-046-tlo` / slug: `tlo` / EP46
- 台本（確定・ロック済・3チェック済）: `episodes/_planning/EP46_tlo_script.en.v001.md`（2,125語・median 11.9分）
- ファクト台帳（Cornell LII一次照合）: `episodes/_planning/EP46_tlo_facts.v001.json`
- SPEC: `episodes/_planning/EP46_tlo_PRODUCTION_SPEC.v001.json`（★数値の出典）
- タイトル（具体シーン宣言型＝最高保持）:
  - A（主）: `A Teacher Searched Her Purse. The Supreme Court Said It Was Fine.`（≤60字近似・具体シーン・広告安全）
  - B（二人称）: `Can Your School Search Your Bag Without a Warrant?`
  - ※「生徒に権利はない/学校は何でも捜索できる」系の過大化を禁止（制約1）。

## 1. 1シーン1枚・バリエーション0（EP44/45と同一）
- still distinct を固有プロンプトで各1枚。`--variants 1`。ai_prompts は still 84本＝84行＋i2v種16本＝shots 100。factory 92本は在庫選抜。

## 2. SPEC 確定値（★出典 EP46_tlo_PRODUCTION_SPEC.v001.json）
- narration **715.9s（11.9分）**@178.1wpm / words **2,125** / mean_shot 3.19s / max_shot 6.0s
- still **84 / 100 / 1.19x（cap2）** ／ factory **92 / 92 / 1.0x（cap1）** ／ motion(i2v) **16 / 32 / 2.0x（cap2）**
- 総カット **224** ／ still-share **0.4464（cap0.45）** ／ first-use **0.8571**
- MG（FigureBeats）ビート floor **30**（AEカードは数えない）／ variety floor 3 ／ density floor 2.5/min

## 3. ★正確性6制約（全出力＝プロンプト・カード文言・タイトル・図表に適用。違反はBLOCKER）
1. **生徒は無権利ではない。** 最高裁は「公立学校職員による捜索にも第4修正は適用される」と明言。ただし基準を**令状不要・相当な理由(probable cause)不要＝合理的疑い(reasonable suspicion)へ引き下げた**（消滅でなく引き下げ）。「学校は令状なしで何でも/いつでも捜索できる」と過大化しない。
2. **二段テスト**が判例核: ①開始時に正当（生徒が校則or法に違反した証拠が出ると疑う合理的根拠）、②範囲が相当（年齢・性別・違反の性質に照らし過度に侵襲的でない）。逐語準拠（台帳）。
3. **公立学校職員**の捜索基準であり、**警察が関与/主導する場合はより高い基準**があり得る（本判決 footnote 7 で留保）。この区別を明記。
4. 票決 **6-3**（White法廷意見／Brennan・Marshall・Stevens が理由付け＝合理性の引下げに反対）。多数/反対を中立帰属。
5. **T.L.O.は当時未成年（14歳）**＝R2・象徴のみ・顔/肖像なし。原事案に薬物（所持・売買の証拠）が含まれるが**4A＝生徒の権利の物語**として枠付け＝薬物を扇情化/美化しない・臨床的最小限に。原被疑事実の性質でサムネ/タイトルを煽らない。
6. 数値・引用は原典一致: 469 U.S. 325 (1985)・二段テスト逐語・"reasonable grounds"・White執筆。confidence:medium（校名Piscataway・副校長名Choplick）はヘッジ／画面に出さない。

## 4. ビジュアル方針（象徴主義・尊厳・ダーク/シネマティック）
- レーン色（★EP41 gold #E5B53A / EP42 blue #3B7DD8 / EP43 amber #E0913C / EP44 teal #2FA6A0 / EP45 crimson #B23A48 と区別）: **EP46 accent = schoolhouse-green `#3F8F5F`**。INK `#0A0A0C`。CODEX_B は OP props / AEカード / サムネ accent を必ず `#3F8F5F` に。
- 反復モチーフ: **机の上のハンドバッグ**・**校舎の廊下/ロッカー**・**空の教室/トイレのドア**・**天秤（probable cause↔reasonable suspicion）**・**校門/校旗**・**最高裁列柱**・**"二段の階段"（inception→scope）**・**警官のバッジ（footnote 7 の境界＝警察関与）**。
- 人物は影/後ろ姿/手元/象徴のみ。**未成年は絶対に肖像化しない**。薬物は臨床的・非扇情（押収物を並べた机など・美化しない）。
- Act別トーン: HOOK（トイレ・教師・14歳・机の上のバッグ・現在形）／OP（"THE SEARCH"系）／ACT1「その捜索」（最短・バッグ→タバコ→更なる押収）／ACT2「校門(schoolhouse)の権利」（4Aは適用される・Tinkerの系譜・probable cause vs 学校）／ACT3「合理性」判例核（6-3・二段テスト・reasonable suspicion・footnote 7 警察留保）／ENDING（あなたのロッカー・権利は残るが基準は下がる余韻）。

## 5. 技術ゴッチャ（EP39-45の事故から）
- ★**dochighlight figure（黒バー/box/underline）を使わない**（バグに見える＝3回指摘）。figures[] に `"kind":"dochighlight"` を入れない（grepで0）。
- FigureBeats kind は**全小文字**（numberticker/stat/votetally/timeline/quote/kinetic/lowerthird/acttitle/compbars(※comparebars非実在)/mechanism 等）。大文字は無音描画。
- ★**quote figure は検証済逐語のみ**（EP43 R-PAYTON 事故）。White法廷意見の逐語は台帳一致・attribution "Justice White, for the Court"。
- read_prompts 2行形式。`--only S01` で shots=100 確認。
- film.json ビルダー `scripts/build_tlo_film.py`（EP45 build_cleveland_film.py を複製・slug/EP/paths を tlo に・**実素材のみstub禁止**・grepでstub/placeholder/dryrun=0）。★**asset_manifest は still だけでなく factory 92・motion 16 も全エントリ記載**（public_path 必須。EP45で factory/motion 空欠落→build失敗の事故）。
- ゲート入力 `--ep PD-2026-046-tlo`。`--json <film.json>` は出力→入力に使わない。
- asset_manifest は A↔B で counts/role enum/overlay枚数**一字一致**・role=thumb/still_thumb 不使用（サムネ=also_thumb 6枚）。counts: still_body84/still_i2v_source16/motion16/factory92/overlay12。
- durationInFrames 4項関数（hook8.0+opening3.5+narration+endcard9）＋hookSeconds=8.0明示・composition id `Ep46Tlo`・Root.tsx登録。
- 正確性ゲート `check_tlo_facts.py`（EP45 check_cleveland_facts.py 複製・R-ルールを tlo 用に：R-OVERCLAIM[「no rights/search anything」系を弾く]・R-STANDARD[probable cause を要求と誤らせない＝reasonable suspicion]・R-VOTE[6-3・attribution]・R-QUOTE[White逐語approved]・R-MINOR[T.L.O.顔なし・薬物非扇情]）。★**R-NUM/構造ルールは narrative figure のみ対象**（asset_manifest の構造カウント・acttitle index は除外＝EP45で誤検出修正済）。
- AE: フォント厳格解決・sourceRectAtTime**実測**・ローカライズOM/RS・.aep>.jsx assert・per-layer motionBlur・disclosure右下常時。
- レンダ: `remotion render Ep46Tlo ... --public-dir=public_slim --concurrency=4`。★**public→public_slim へ全メディア（img/factory/motion/audio）をコピー staging**（EP45で public_slim 未staging→render不能の事故）。完成後 `build_tlo_bgm_real.py`(EP43複製・OFF=11.5)→`composite_tlo_hero.py`(EP43複製・film_offset適用)→全ゲート＋**全編アイボール**。

## 6. AEヒーローカード（6-8枚・数値は台帳照合・捏造ゼロ・6制約順守）
- 候補（検証済ファクトのみ）:
  - `6 – 3`（VOTE_SPLIT）＋サブ「THE 4TH APPLIES IN SCHOOL」（制約1＝無権利と読ませない）
  - `PROBABLE CAUSE → REASONABLE SUSPICION`（SPLIT_COMPARE・引き下げた基準）
  - `TWO-PART TEST`（CENTER_STACK）＋サブ「JUSTIFIED AT INCEPTION · REASONABLE IN SCOPE」
  - White 逐語 `"REASONABLE GROUNDS FOR SUSPECTING THE SEARCH WILL TURN UP EVIDENCE..."`（QUOTE_CARD・attribution "Justice White, for the Court"）
  - `NO WARRANT · NO PROBABLE CAUSE`（CENTER_STACK・ただし4Aは適用の枠）
  - `1985 · SUPREME COURT`（DATE_STAMP）
  - （任意）`WHEN POLICE STEP IN`（footnote 7 の留保・警察関与でより高い基準）
- カード文言に「no rights / search anything / probable cause required」を書かない。数値・引用は AE ledger 一致必須。accent `#3F8F5F`。

## 7. 完了条件（設計パッケージ）
- DESIGN（`EP46_tlo_DESIGN_and_CODEX_PROMPTS.v001.md`）: 0〜715.9s全区間タイムライン・各アニメの開始/終了フレーム・移動量・イージング種別・damping・スタッガー・motion-blur Trail・最低3背面レイヤー・overflow:hiddenマスク・秒はfps算出で定数化。48シーン絵コンテ（象徴・6制約・**未成年の肖像化禁止**・薬物非扇情）。FigureBeats設計（≥30・小文字kind・変種≥3・**dochighlight不使用**・quote検証逐語）。AEカード表（§6・accent #3F8F5F）。Composition設定（1920x1080/fps30/id=Ep46Tlo/durationInFrames4項/hookSeconds8.0）。
- CODEX_A: ai_prompts 84本（1枚ずつ・**省略禁止で全84本**）＋i2v16＋factory92選定＆全点目視QC（`select_tlo_factory.py`・--exclude-used --ep PD-2026-046-tlo・EP39-45 sha256被り検証）＋asset_manifest（**stills84＋factory92＋motion16＋overlay12を全エントリ記載**・also_thumb 6枚）。
- CODEX_B: `build_tlo_film.py`（実素材・dochighlight不使用・quote検証逐語・manifestの factory/motion 全読込）・captions（実測narration・+offset）・figures（小文字kind・MG≥30）・Root.tsx登録（Ep46Tlo）・AEカード（実測幅・ledger照合・accent #3F8F5F）・bgm→composite（film_offset適用）・public_slim staging・レンダ・全ゲート（--ep・check_tlo_facts.py）・全編アイボール。
- A↔B 接続点は asset_manifest.v001.json ただ1ファイル（スキーマ一字一致）。
