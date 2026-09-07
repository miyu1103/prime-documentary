# EP43 caniglia — 設計書＆Codex A/B 共有ブリーフ（各ドラフトagentが必ず読む）

> 単一の真実源。EP42 の同名ファイル群（DESIGN/CODEX_A/CODEX_B）を構造テンプレとして踏襲し、
> 下記 EP43 差分で数値・内容を差し替える。**推測で数値を作らない。ここに無い数値は SPEC JSON から転記。**

## 0. エピソード同定
- episode_id: `PD-2026-043-caniglia` / slug: `caniglia` / EP43
- 台本（確定・ロック済）: `episodes/_planning/EP43_caniglia_script.en.v001.md`（2,141語・median 12.0分）
- SPEC（唯一の数値源）: `episodes/_planning/EP43_caniglia_PRODUCTION_SPEC.v001.json`
- タイトル A/B（≤60字・二人称・CTR・★射程を過大化しない）:
  - A: `Police Came for a Welfare Check. They Left With His Guns.`
  - B: `Can Police Enter Your Home to "Help" — and Take What They Find?`
  - ※「警察は令状なしに家に入れないと最高裁が決めた」系は**禁止**（制約1）。

## 1. ★★ 前提: 1シーン1枚・バリエーション0 ★★（EP42と同一方針）
- Codexは高精度。同一ショットの複数バリエーション（_01/_02/_03）を作らない。`--variants 1`。
- still は distinct を固有プロンプトで各1枚。`ai_prompts.v001.md` は still 85本＝85行＋i2v種16本。総生成画像 = 85 + 16 = 101枚（各1回）。factory 93本は在庫選抜。

## 2. SPEC 確定値（★この値で積算。出典 SPEC JSON）
- narration 721.3s（12.0分）@ 178.1 wpm / words 2,141
- 視覚シーン 48（derive: S01..S48）/ 総カット **226** / 平均ショット 3.19s（cap 6.0）
- still **85 distinct / 101 cuts / 1.19x（cap 2）** ／ factory **93 / 93 / 1.0x（cap 1）** ／ motion(i2v) **16 / 32 / 2.0x（cap 2）**
- distinct 合計 **194 / 226 = first-use 0.8584（floor 0.70）** ／ still-share **0.4469（cap 0.45）** ／ motion coverage 0.553
- MG（FigureBeats）ビート floor **31**（film.json 内。AEカードは数えない）
- 紙芝居回避: still-cut 101 に対し video(factory 93 + i2v 32)=125 で motion>still を構造保証。stillを増やしてfactoryを削るな。

## 3. ★正確性6制約（全出力＝プロンプト・カード文言・タイトル・図表に適用。違反はBLOCKER）
1. 射程を過大化しない。判決が否定したのは「community caretaking の“住居”拡張」だけ。exigent circumstances / emergency aid の例外は温存（Roberts+Breyer / Kavanaugh / Alito の補足意見）。タイトル/サムネ/カードに「警察は令状なしに家に入れない」と断定する文言を出さない。
2. 9-0は「破棄・差戻し(vacate & remand)」。Caniglia の全面勝訴/事件終結と断定しない。カードで "9-0" を出すなら "ONE EXCUSE, CLOSED" 等、限定を併記。
3. Cady v. Dombrowski の対象は「警察管理下の自動車」。住居と混同しない。Cadyカード/プロンプトは車・レッカー・トランクの象徴で、家と分ける。
4. Edward Caniglia は R2（存命私人）。顔・肖像・身体を描かない。象徴のみ（食卓の拳銃・空のポーチ・救急車の赤色灯・玄関・電話・証拠タグ）。
5. メンタルヘルス/自殺念慮は非グラフィック・非扇情。手段の描写や内面の憶測をしない。「もう撃ってくれ」は記録事実として1回のみ、演出で誇張しない。概要欄に988 Suicide & Crisis Lifeline を記載。
6. Payton（住居＝第4修正の中心・令状なし立ち入りは presumptively unreasonable）と温存例外を正確に。「家は絶対に守られる」と誇張しない。
- 加えて R1: 実在人物の顔・肖像を生成しない。全生成ビジュアル表示中 `AI-assisted visualization`（右下）常時表示、概要欄1行AI開示。

## 4. ビジュアル方針（象徴主義・尊厳・ダーク/シネマティック）
- レーン色（★EP41 gold #E5B53A / EP42 warrant-blue #3B7DD8 と区別）: **EP43 accent = porch-amber `#E0913C`**（誰かのために点けた玄関灯の暖色＝"助けに来た"の皮肉）。INK `#0A0A0C`。CODEX_B は OP props / AEカード / サムネ accent を必ず `#E0913C` にする（EP42色の流用禁止）。
- 反復モチーフ: **玄関ドア**（閉じた戸→夜明けの開いた戸）。**食卓の拳銃**。**空のポーチ**。**救急車の赤色灯**。**電話**（非緊急ライン）。**証拠タグ／布の上の2丁**。**車＋レッカー**（Cady専用・家と分離）。**9席の最高裁／大理石**。
- 人物は影/後ろ姿/手元/象徴のみ。顔なし。Caniglia を個人として描かない。危機の一瞬は抑制。
- Act別トーン: HOOK（象徴モンタージュ・食卓の銃・閉じた戸）／ACT1「その夜」（最短・現在形・抑制・ホテルのキーカード）／ACT2「安否確認」（電話→ポーチ→救急車→押収）／ACT3「命令」判例核（Cady=車、9-0、"headlineは罠"、補足意見、vacate&remand・最も遅い）／ENDING（開いた戸・夜明け・988）。

## 5. 技術ゴッチャ（EP39-42の事故から）
- FigureBeats kind は全部小文字（numberticker/timeline/bar/kinetic/acttitle/lowerthird/dochighlight/routemap/pindropmap/regionmap/compbars(※comparebars非実在)/mechanism/quote/stat/votetally 等）。大文字は無音描画。
- read_prompts 形式: 「- \`S01.png\`」の次行に「<positive> ... Avoid: <negative>」。--only S01 で拾い数（101）を確認。
- film.json ビルダー `scripts/build_caniglia_film.py`（EP42 build_young_film.py を複製・ASSET_MAP/NARR/FACTORY_SEL/SLUG/EP を caniglia に）。film.json は git 未追跡＝ビルダーで再生成できる状態を保つ。
- ゲート入力は `--ep PD-2026-043-caniglia`。**`--json <film.json>` は出力パス（上書き事故）→入力に使わない**。
- asset_manifest は **A↔B で同一スキーマ**（EP42の教訓）。counts/role enum を A(producer)とB(consumer/validator)で一字一致。サムネは also_thumb=true の body still 6枚から（role=thumb/still_thumb は作らない）。
- durationInFrames は caseFilmDurationInFrames の4項関数で表記（round(hookSeconds*fps)+round(OPENING_SEC*fps)+ceil(narrationSeconds*fps)+round(ENDCARD_SEC*fps)）。hookSeconds を明示（0なら round(30×narr)）。total ≤ 750s を assert。
- AEカードのレイアウト名は実装済みのみ（DATE_STAMP/CENTER_STACK/MONEY_STACK/SPLIT_COMPARE/ACT_TITLE_CARD/QUOTE_CARD/VOTE_SPLIT/SEAM_TRANSITION）。DESIGNとCODEX_Bのb01..の表を一字一致。
- 6制約の正確性ゲート名は1つに統一（例 `check_caniglia_facts.py`）。DESIGN/A/B で同名。
- AE: フォントは getFontsByFamilyNameAndStyleName で厳格解決（miss は throw）。テキスト幅は sourceRectAtTime 実測（advance-width推定禁止＝文字切れ原因）。OM/RS ローカライズ名。ADBE Rotate Z。per-layer motionBlur。aerender 前に .aep mtime > .jsx を assert。
- Root.tsx に `id="Ep43Caniglia"`（誤記 Ep43Canig 等に注意）で CaseFilm 登録。durationInFrames は caseFilmDurationInFrames(canigliaFilm, fps)。
- レンダ: `remotion render Ep43Caniglia ... --public-dir=public_slim --concurrency=4`。完成後 build_caniglia_bgm.py → composite_caniglia_hero.py → 全ゲート＋**全編アイボール**。

## 6. AEヒーローカード（6-8枚・数値は台帳照合・捏造ゼロ・6制約順守）
- 候補ビート（検証済ファクトのみ）:
  - `9–0` ＋ サブ「ONE EXCUSE, CLOSED」（制約1/2＝全面勝訴と読ませない）
  - `NO WARRANT`（押収の事実）
  - `A CAR, NOT A HOME`（Cady限定・制約3）※車の象徴
  - `"vehicles ≠ homes"`（Thomas逐語・quote card）
  - `STILL OPEN` ＋「WARRANT · CONSENT · EMERGENCY」（温存例外・制約1の核）
  - `VACATE & REMAND`（制約2）
  - `2015 · CRANSTON, RI`（date stamp）
  - `988`（endcard/概要欄と連動・制約5）
- カード文言に「令状なしで家に入れない」「全面勝訴」を書かない。数値・引用は AE ledger と一致必須。

## 7. 完了条件（設計パッケージ）
- DESIGN: 秒数ベースのタイムライン（0〜721.3s 全区間・各Act）・各アニメの開始/終了フレーム・移動量・イージング種別（spring or Easing.out(Easing.cubic)・等速禁止）・damping・スタッガー・motion-blur Trail・最低3背面レイヤー・overflow:hidden マスク切れ上がり・秒はfps算出で定数化。48シーン絵コンテ（象徴のみ・6制約）。FigureBeats設計（≥31・小文字kind・変種≥3）。AEカード表（§6）。冒頭に Composition 設定（1920x1080 / fps は EP42 と同じ値 / id=Ep43Caniglia / durationInFrames は4項関数）と依存(@remotion/motion-blur)。
- CODEX_A: ai_prompts 85本（1枚ずつ・バリエーション0）＋ i2v 16 ＋ factory 93 選定＆全点目視QC（select_caniglia_factory.py・--exclude-used で EP39/40/41/42 sha256 除外）＋境界契約 asset_manifest（EP42同型・counts を EP43 値に）。
- CODEX_B: build_caniglia_film.py 仕様・captions（実測narration）・figures（小文字kind・MG≥31）・Root.tsx登録・AEカード（実測幅・ledger照合・.aep>.jsx assert・レイアウト名は実装済みのみ・accent #E0913C）・build_caniglia_bgm→composite_caniglia_hero・レンダ・全ゲート（--ep 指定）・完成後の全編アイボール。
- A↔B の接続点は asset_manifest.v001.json ただ1ファイル（スキーマ一字一致）。
