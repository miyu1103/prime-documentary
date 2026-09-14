# EP46 kelo — 設計書＆Codex A/B 共有ブリーフ（各ドラフトagentが必ず読む）

> 単一の真実源。EP44/45 の同名ファイル群（DESIGN/CODEX_A/CODEX_B）を構造テンプレとして踏襲し、下記 EP46 差分で数値・内容を差し替える。推測で数値を作らない。ここに無い数値は SPEC JSON から転記。

## 0. エピソード同定
- episode_id: `PD-2026-046-kelo` / slug: `kelo` / EP46
- 台本（確定・ロック済・3チェック済）: `episodes/_planning/EP46_kelo_script.en.v001.md`（2,133語・median 12.0分）
- ファクト台帳（検証済）: `episodes/_planning/EP46_kelo_facts.v001.json`（F01–F20・出典付き）
- SPEC: `episodes/_planning/EP46_kelo_PRODUCTION_SPEC.v001.json`（★数値の出典。ハンド転記でなくここから）
- タイトル（確定・アナリティクス準拠）: `Police Came for a Welfare Check.` 型ではなく**具体シーン宣言型が最高保持**（実測: "The Traffic Stop Was Over. Then the Dog Arrived." 42.5%）。EP46 主タイトル案:
  - A（主）: `The City Took Her Home and Gave It to a Developer.`（≤60字・具体シーン・広告安全）
  - B（二人称代替）: `Can the Government Take Your Home for a Private Company?`
  - ※「合法/違法」と断定的にサムネへ書かない。**"the Court said it could"** の枠。

## 1. 1シーン1枚・バリエーション0（EP42-45と同一方針）
- still は distinct を固有プロンプトで各1枚。`--variants 1`。ai_prompts は still 85本＝85行＋i2v種16本＝shots 101。factory 92本は在庫選抜。

## 2. SPEC 確定値（★この値で積算。出典 EP46_kelo_PRODUCTION_SPEC.v001.json）
- narration **718.6s（12.0分）**@178.1wpm / words **2,133** / mean_shot 3.19s / max_shot 6.0s
- still **85 / 101 / 1.19x（cap2）** ／ factory **92 / 92 / 1.0x（cap1）** ／ motion(i2v) **16 / 32 / 2.0x（cap2）**
- 総カット **101+92+32 = 225** ／ still-share **101/225 = 0.449（cap0.45）** ／ first-use **(85+92+16)/225 = 193/225 = 0.858**
- MG（FigureBeats）ビート floor **30**（AEカードは数えない）／ variety floor 3 ／ density floor 2.5/min
- 紙芝居回避: still-cut 101 に対し video(factory92+i2v32)=124 で motion>still を構造保証。

## 3. ★正確性6制約（全出力＝プロンプト・カード文言・タイトル・図表に適用。違反はBLOCKER）
1. **収用は「違法」でない。最高裁は5-4で UPHELD（合憲と判断）。** 憤りの源は「合法とされたこと」＝規範的批判＋後日談。「illegal / unconstitutional / struck down」を収用自体に使わない。枠は "the Court said the city COULD do this."
2. ドクトリン: 多数意見は Fifth Amendment の "public use" を **"public purpose"** と広く解し、公共便益(雇用・税収)を約束する経済開発型の private 転売収用も該当しうる、とした。「政府はどんな理由でも家を奪える」と過大化しない。
3. **Kennedy（第5票・補足意見）**＝pretextual／trivial／implausible な便益偽装収用は依然禁止、疑わしい事案は厳格審査の余地。この nuance を落とさない。
4. **O'Connor 反対**が情緒の核。逐語を**反対意見として**中立帰属（Court に帰属させない）: 「The specter of condemnation hangs over all property. Nothing is to prevent the State from replacing any Motel 6 with a Ritz-Carlton, any home with a shopping mall, or any farm with a factory.」＋受益/被害ライン。**Thomas 別個反対**（原意主義: public use = use by the public）。
5. Susette Kelo は**存命の私人（R2・有罪歴なし）**。顔・肖像・身体を描かない。象徴のみ（ピンクの家・水辺・空の通り・解体重機・更地・州法令集）。**捏造引用禁止**。ピンクの家は**取壊しでなく解体移築（36 Franklin St）**＝「her house was demolished」と書かない（近隣宅は取壊し）。
6. 数値・後日談は原典一致＆ヘッジ: Pfizer 約$3億拠点が触媒 → **2009離脱**表明、収用地は長年**更地**（2011ハリケーン後は瓦礫置場）、判決後**"more than forty states"**が収用改革（正確数はソース差＝**confidence:medium、">40州"表記**）。90エーカー計画・NLDC・約115物件・Institute for Justice 代理。先例 Berman(1954 blight)/Midkiff(1984 farmland) は一般記述で。

## 4. ビジュアル方針（象徴主義・尊厳・ダーク/シネマティック）
- レーン色（★EP41 gold #E5B53A / EP42 blue #3B7DD8 / EP43 amber #E0913C / EP44 teal #2FA6A0 / EP45 crimson #B23A48 と区別）: **EP46 accent = deed-green `#3F8F5F`**（土地・権利証・"greenlight"）。INK `#0A0A0C`。CODEX_B は OP props / AEカード / サムネ accent を必ず `#3F8F5F` に（他話の色を流用しない）。
- 反復モチーフ: **小さなピンクの家**（点在する更地に一軒だけ残る）・**水辺（川と入江）**・**condemnation notice をドアに貼る**・**解体重機/更地/雑草**・**企業の site plan と光る模型**・**Motel 6 と Ritz-Carlton の対比**・**空の通り**・**州法令集の背**・**家をフラットベッドに載せて移築**。
- 人物は影/後ろ姿/手元/象徴のみ。顔なし。poverty-porn 禁止・尊厳をもって。
- Act別トーン: HOOK（ピンクの家・水・更地の通り・立退き拒否）／OP（"THE LITTLE PINK HOUSE"）／ACT1「点の計画」（最短・現在形・衰退都市→Pfizer→90エーカー→収用）／ACT2「public use の意味」（判例核・5-4・Stevens多数・Kennedy留保・Berman/Midkiff）／ACT3「NOと言った4人」（最長・情緒・O'Connor逐語→Thomas）／ENDING（更地＝Nothing→2009 Pfizer離脱→>40州改革→冒頭の問いに回帰・移築されたピンクの家）。

## 5. 技術ゴッチャ（EP39-45の事故から）
- ★**dochighlight figure（黒バー/box/underline）を使わない**（バグに見える＝EP40/41/42で3回指摘・オーナー激怒）。film.json figures[] に `"kind":"dochighlight"` を入れない（grepで0を確認）。redacted が要るなら実書面に "REDACTED" を焼いた still を使う。
- FigureBeats kind は**全小文字**（numberticker/stat/votetally/timeline/quote/kinetic/lowerthird/acttitle/compbars(※comparebars非実在)/mechanism 等）。大文字は無音描画。
- ★**quote figure は検証済逐語のみ**。EP43 で未検証の Jardines 断片がゲート(R-PAYTON)に捕捉された。film.json の kind:"quote" は台本＆facts台帳にある逐語だけ。O'Connor 逐語は**反対意見**として attribution 明記（Court に帰属させない）。
- read_prompts 2行形式。`--only S01` で shots=101 確認。
- film.json ビルダー `scripts/build_kelo_film.py`（EP45 build_cleveland_film.py を複製・slug/EP/ASSET_MAP/NARR/FACTORY_SEL を kelo に）。git 未追跡＝ビルダーで再生成できる状態を保つ。**実素材のみ（stub禁止・grepでstub/placeholder/dryrun=0）**。
- ゲート入力は `--ep PD-2026-046-kelo`。`--json <film.json>` は**出力パス**→入力に使わない（EP41でthompson_film.jsonを破壊した事故）。
- asset_manifest は A↔B で counts/role enum/overlay枚数を**一字一致**。role=thumb/still_thumb を作らない（サムネは also_thumb=true の body still 6枚）。
- durationInFrames は caseFilmDurationInFrames の4項関数（hook+opening+narration+endcard）＋hookSeconds明示＋total≤750sは超える可能性（718.6s narr）ので **total≈752s を許容**（EP43=752.9sで既存）。hookSeconds は EP43同様 8.0 を基準に設計（AEカード/BGMのoffset=hook+3.5と一致必須）。
- AEカードのレイアウト名は**実装済み集合のみ**（DATE_STAMP/CENTER_STACK/MONEY_STACK/SPLIT_COMPARE/ACT_TITLE_CARD/QUOTE_CARD/VOTE_SPLIT/SEAM_TRANSITION）。DESIGNとCODEX_Bのカード表を一字一致。
- 正確性ゲート名は1つに統一（`check_kelo_facts.py`・EP43 check_caniglia_facts.py を複製し kelo 用の R-ルール＝R-DISPO[5-4 upheld と "public purpose" を誤らせない]/R-QUOTE[O'Connor/Thomas 逐語の approved 化]/R-FACE[Kelo顔なし]/R-HEDGE[">40 states" 断定化を弾く] に）。DESIGN/A/B同名。
- Root.tsx に `id="Ep46Kelo"`（CaseFilm）で登録。durationInFrames は caseFilmDurationInFrames(keloFilm, fps)。
- AE: フォント厳格解決（miss throw）・sourceRectAtTime**実測幅**（EP40クリップ事故）・ローカライズOM/RS・ADBE Rotate Z・per-layer motionBlur・aerender前に **.aep>.jsx assert**。app.newProject() を headless で呼ばない。disclosure "AI-assisted visualization" 右下常時。
- レンダ: `remotion render Ep46Kelo ... --public-dir=public_slim --concurrency=4`。完成後 `build_kelo_bgm_real.py`（EP43 build_caniglia_bgm_real.py を複製・OFF=hook+3.5）→ `composite_kelo_hero.py`（beats.json の film_offset_sec を+適用・EP43複製）→ 全ゲート＋**全編アイボール**。

## 6. AEヒーローカード（6-8枚・数値は台帳照合・捏造ゼロ・6制約順守）
- 候補ビート（検証済ファクトのみ）:
  - `5 – 4`（VOTE_SPLIT）＋サブ「THE TAKING STANDS」（制約1＝違法と読ませない・多数UPHELD）
  - `PUBLIC USE → PUBLIC PURPOSE`（SPLIT_COMPARE・ドクトリン転換）
  - O'Connor 逐語 `"...ANY MOTEL 6 WITH A RITZ-CARLTON, ANY HOME WITH A SHOPPING MALL, OR ANY FARM WITH A FACTORY"`（QUOTE_CARD・attribution "Justice O'Connor, dissenting"）
  - `NOTHING BUILT`（CENTER_STACK・更地の payoff）＋サブ「THE LAND SAT EMPTY」
  - `2005 · SUPREME COURT`（DATE_STAMP）
  - `MORE THAN 40 STATES`（CENTER_STACK・改革の規模・">40" 断定回避のヘッジ表記）＋サブ「REFORMED EMINENT DOMAIN」
  - （任意）`USE BY THE PUBLIC`（QUOTE/CENTER・Thomas 反対の原意主義・attribution "Justice Thomas, dissenting"）
  - （任意）`THE LITTLE PINK HOUSE`（ACT_TITLE系・移築のモチーフ）
- カード文言に「illegal」「the Court struck it down」「政府はどんな理由でも」を書かない。数値・引用は AE ledger と一致必須。accent `#3F8F5F`。

## 7. 完了条件（設計パッケージ）
- DESIGN（`EP46_kelo_DESIGN_and_CODEX_PROMPTS.v001.md` 相当）: 0〜718.6s全区間の秒数タイムライン・各アニメの開始/終了フレーム・移動量・イージング種別・damping・スタッガー・motion-blur Trail・最低3背面レイヤー・overflow:hiddenマスク・秒はfps算出で定数化。48シーン絵コンテ（象徴のみ・6制約・Kelo顔なし・poverty-porn禁止）。FigureBeats設計（≥30・小文字kind・変種≥3・**dochighlight不使用**・quote は検証逐語のみ）。AEカード表（§6・accent #3F8F5F）。Composition設定（1920x1080 / fps 30 / id=Ep46Kelo / durationInFrames4項 / hookSeconds=8.0）。
- CODEX_A: ai_prompts 85本（1枚ずつ・バリエーション0・**省略禁止で全85本**）＋i2v16＋factory92選定＆全点目視QC（`select_kelo_factory.py`・--exclude-used --ep PD-2026-046-kelo・EP39-45 sha256被り検証）＋境界契約 asset_manifest（EP45同型・counts を EP46 値に：still_body85/still_i2v_source16/motion16/factory92/overlay12・also_thumb 6枚指定）。
- CODEX_B: `build_kelo_film.py` 仕様（実素材・stub禁止・dochighlight不使用・quote検証逐語）・captions（実測narration・+offset）・figures（小文字kind・MG≥30）・Root.tsx登録（Ep46Kelo）・AEカード（実測幅・ledger照合・レイアウト名実装済みのみ・accent #3F8F5F）・`build_kelo_bgm_real.py`→`composite_kelo_hero.py`（film_offset適用）・レンダ・全ゲート（--ep 指定・`check_kelo_facts.py`）・完成後の全編アイボール。
- A↔B の接続点は asset_manifest.v001.json ただ1ファイル（スキーマ一字一致）。
