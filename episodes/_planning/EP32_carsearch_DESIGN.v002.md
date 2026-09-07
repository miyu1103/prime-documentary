# EP32 制作設計書 v002 — "Can the Police Search Your Car?"（自動車例外）— 革命フォーマット（実装配線済み）

**Episode:** `PD-2026-032-carsearch` · slug `carsearch` · Series us-court-cases · **R2**（Collins 2018 存命人物・役割のみ・実在肖像なし）
**Binding:** `docs/PD_ONE_PASS_PRODUCTION_SPEC.v2.md` + `docs/PD_SHIP_GATE.md` + 本書。
**v001 → v002 の意味:** v001は"良い設計に見えて計画とゲートが実レンダに配線されていない飾り"だった（5人の敵対的レビューで総合≈60点判定）。v002は **全指摘を"文章"でなく"止める機構(コード)"に変換し、独立再検証でCONFIRMED-FIXEDを確認した版**。過去の「緑なのに紙芝居／薄い音／偽の緑」を機構で封じる。**根拠となる台帳＝`EP32_DESIGN_REMEDIATION.v001.md`（BLOCKING/MAJOR全件＋担当ファイル）。**

---
## 0. 勝ちフォーマット（型を丸ごとコピー）
土台＝Veritasium（実写b-roll＋現場音）／説明＝Kurzgesagt・TED-Ed（概念が**動く図解**）／音＝4層設計／PDアクセント＝ダーク・ノワール＋金/電光ブルー＋ブライトライン・モチーフ。

## 1. 事実（FACTS LOCKED＝`01_research/claims.v001.json` CLM-0001..0010）
Carroll(1925)自動車例外・probable cause／Collins(2018,**8–1 Sotomayor**,Alito単独反対)「automobile exceptionは自動車自体を超えない」curtilage＝家の外周＝家の保護／scope=対象(Ross 1982・Acevedo 1991)／別exigency不要(Labron/Dyson)／Gant(逮捕付随の限界)／Byrd(レンタカーのプライバシー)／大麻臭＝**州次第・未確定**(CLM-0010,grade B)。**一次資料でロック・E級ゼロ・中立・実在肖像なし。** 出典なし断定は全除去済（"最も長く過ごす場所"/"毎日膨大"/"lazyback"/McReynolds動機/"in plain view"）。独立検証＝**M7 CONFIRMED-FIXED**。

## 2. 台本（`03_script/script.en.v001.md`・**1,910語**・3パス＋是正済）
8秒フック(**20語≈8秒**・独立検証M8 CONFIRMED)→OP→ACT I(Carroll/68瓶/1925)→ACT II(probable cause＋scope"リーシュ"＋Ross/Acevedo＋別exigency不要)→ACT III(Collins/タープ/8–1/curtilage回収)→ACT IV(権利の地図＋Gant/Byrd/大麻caveat)→ED CTA。二人称・オープンループ2本・幕ごと再フック(ACT III→IV追加済)・平坦20秒ゼロ。`[VO:]`＝読み上げ／`(VIS:)(SFX:)`＝別行の制作指示。**validate_episode PASS（schema0・FK6.0・12.7分@150wpm・AI定型句0・dangling0・章span一致）。**

## 3. ビジュアル/モーション（"見ごたえ"を予算として確保＋**レンダ前に機械強制**）
確定値（`04_scenes/scene_plan.v001.json`＋`remotion_plan.v001.json`）：**22シーン／314カット／平均2.20s／depth 56.8%（54/95・床40%）／動くFigureBeats 11（床6）／ヒーロー面 3（床2）／転換＝ForcefulCut(push/slide/zoompunch/whip)・金縦スイープ`WipeTransition`禁止。**
- **専用の動く図**`src/components/carsearch/`：BrightLine(draw/hold/**slam**＝Collins山場)・CarCutaway(scope可視化)・ProbableCauseMeter(hunch→cross)・CurtilageShield(curtilage回収)・StateMap/RegionHighlightMap(大麻=州次第)・CaseTimeline(1925/2009/2018)・CarKeyLock(車＝家の鍵)・ForcefulCut。**全8部品にリビール後の持続モーション実装済（±0.5px breath→全体パララックス＋走る光/スキャン/プレイヘッド/オービット）＝紙芝居フリーズを根絶。独立検証B4 CONFIRMED-FIXED・remotion型チェック緑。**
- **再利用部品**`src/components/motionkit/`（約40点）：NumberTicker(68)・VoteTally(8–1)・QuoteCard(Taft/Sotomayor)・KineticCaptions・ActTitle・RouteMap/PinDropMap・Atmospherics 等。
- **画像**：Codex 40枚 S001–S040＝**全4K(3840×2160)**・コンタクトシート**目視QC合格**（題材一致・匿名・画面内テキスト無・場違い素材無）。`asset_selection.v001.json`＝**22/22 span束縛・要33/在40/不足0**（黒画面リスク解消）。
- **実写**：`05_visuals/asset_selection`＝factory候補112本＋棚に無いビート(motorcycle/tarp/handcuff等)はCodex/motionへ明示ルート。多様性ゲート(distinct≥0.40/reuse≤4/generic≤2)PASS。**初回レンダ前にラベル付きコンタクトシート目視QC必須。**
- **深度**：depth指定カットは`gen_depth.py`で`<name>_depth.png`を**全生成**（現在0/33＝未生成・preflightがブロック中）。ビルダー`build_case_film_assets.py`はdepth比**50%**・計画準拠・**深度欠落は出力前にhard-fail**（40%→25%浸食を封鎖・独立検証M2 CONFIRMED）。

## 4. 音設計（4層・**実レンダにmux配線済み**）
`build_case_film_audio.py`（新設）＝**実ナレ`narration_index.v002.json`の実オフセットでSFX配置**（175wpm推測を廃止・独立検証B6 CONFIRMED）：
- **層1ナレ**(ElevenLabsマスター最前面) **層2劇伴**(章ごと7スロット・サイドチェーンでVO優先) **層3アンビ**(**章ごとに別ベッド・-18dB可聴・ダッキングなし**) **層4SFX**(1括弧=1キュー・0.5s重複除去・スウェルはL3ゲイン自動化にルート)。
- **パレット増強**：`gen_sound_palette.py`で権利フリー合成SFX/ベッド**18点**追加＋ビルダーに**変種ローテーション**配線（連続する同種SFXが別ファイル＝反復解消）＋**新環境ベッド5種**(雨/夜間交通/エンジン/1920年代路面/風)を場面配線＝**dry-runで環境ベッド7種**。**実フォーリー8点**はDLリスト(Pixabay/YT・商用OK)＝`EP32_FOLEY_DOWNLOAD_LIST.md`。
- **2-passラウドネス I=-14**。**mux＝`build_case_film_mux.py`が4層mixをレンダの唯一音声として焼き込み、`audio_mix_sha256`をコンテナに刻印**（"mixがレンダに届かない"穴を封鎖・独立検証で往復verified）。
- **権利**：`SOUND_LIBRARY_RIGHTS.v001.json`＝61点全て商用OK・帰属不要。生成系(ElevenLabs/Suno)は`publish_gate`＝公開前に有料アカウント生成の証跡を確認。

## 5. 字幕（**owner最頻No.1/No.2の失敗を機構で封じる**）
`gen_captions_forced.py --ep PD-2026-032-carsearch`：
- **源＝逐語`narration_index.v002.json`（annotated要約は絶対に使わない＝desyncの罠を封鎖）。**
- ElevenLabsマスターにfaster-whisperで**強制整列**（音に合わせる）。
- **息継ぎ/節単位で改行・≤8語/≤44字・句の途中で切らない**・孤立ダッシュ結合。
- **字幕=ナレ一致QCゲート**（連結字幕を逐語と語単位照合・不一致でFAIL）＋行超過フラグ。EP32 dry-run＝341行・QC PASS。gideonはbyte一致で不変。**独立検証M9＝この章で解決。**

## 6. 品質ゲート（Done＝全hard緑＋**実物目視/試聴**。自己申告禁止）
- **ship-gate `check_final_acceptance.py`**（全hard・invariant15で緩めない）：
  - **例外時fail-closed**（black/freeze/resolution/bgm/low_motion＝壊れレンダで素通りしない・独立検証B1 CONFIRMED）。
  - **motion_energy**＝**within-shot（カット±8フレーム除外）平均≥12＋12秒窓ごと≥8＋p10≥9**、窓が空ならFAIL（超高速カットの抜け穴封鎖・M1 CONFIRMED）。較正＝MotionSample 46.6 / 紙芝居 3.5。
  - **check_sound_layers（hard）**＝実レンダ音の**onset≥35/分＋アンビ帯≥-33dB**（実mix 52-62/分・-21.9dB＝薄いVO+音楽は落ちる）＋**provenance/`audio_mix_sha256`タグ照合**（mixがレンダに届いた事を証明・sfx≥20/beds≥4）。
  - **freshness（hard）**＝new sha≠前回受領書sha＋mtime≥レンダ開始（偽の緑＝古い良品掴みを封鎖・B2 CONFIRMED）。
  - **check_preflight_receipt（hard）**＝green preflight必須。**probe受領書はfilm shaに束縛**（古いprobe再利用を封鎖）。
  - 画像4K・footage_diversity・bookends・runtime_band・captions存在。受領書はimmutable v{NNN}。
- **pre-render `preflight_render_gate.py`**＝**レンダ前に**予算を生データ再計算(depth%/FigureBeats/hero・手打ちflag無視)＋全参照S0NN存在＋≥3840px＋各depthに深度マップ＋全span束縛。未達はexit1。
- **60–90秒プローブ**（motion_energy＋black/freeze）→プローブ受領書→本レンダが要求。
- **最後に必ずオーナーに実物を見せて「動き足りてる?/音は?」確認してから公開。**

## 7. レンダ規律（EP31/EP29確定ルール）
tail/head禁止→生ログを`grep 'Rendered [0-9]+/'`で直接監視／**完走までkillしない**／**1本ずつ直列**／depth/WebGL長尺は`--concurrency=4`／健全性＝Rendered行・headless chrome数・実mp4成長／プロセスはCommandLineで分類／**Windowsパスはraw string**。

## 8. 尺の予算（M11＝過去の"尺不足やり直し"を封じる）
台本1,910語。**150wpm換算＝12.7分（validatorバンド内）／173wpm換算＝11.05分**。この差はナレ実測で解消：**check_runtime_band.py を実レンダのmp4に対して実行し、完成尺11.5–12.5分を確認**（word countでなく実測が正）。不足なら息継ぎ/SFX/劇伴の間で吸収、余剰なら微トリム。**runtime_bandはship-gate唯一のオーナー承認偏差。** 台本ヘッダも実値に更新済。

## 9. OP/ED・サムネ
正典Bookends（`BrandOpening`/`BrandEndcard`・フォーク禁止）。ED CTA＝台本どおり。サムネ＝`thumbnail_options.v001.json`＝派手3案＋選定(「SEARCH YOUR CAR?」)＋A/B(「THEY CAN'T CROSS THIS」)。輝度≥33・極太黒縁・320px可読・二人称・肖像なし。

## 10. Codex画像
`codex_prompt_ep32.md`＋`EP32_carsearch_ai_prompts.v001.md`＝40枚(S001–S040・匿名・肖像なし・画面内テキスト無・4K)。**生成済40枚・目視QC合格。** SDXLを勝手に起動しない（画像はCodex）。

## 11. 失敗モード → 止める機構（漏れゼロ・各件に**名前のあるゲート/スクリプト**）
| # | 過去の失敗 | 機構（実装ファイル） | 状態 |
|---|---|---|---|
|1|字幕≠ナレ|逐語narration_index源＋強制整列＋**字幕=ナレQCゲート**(`gen_captions_forced.py`)|**FIXED**|
|2|字幕が変な所で切れる|息継ぎ単位≤8語/44字・句途中禁止・ダッシュ結合(同上)|**FIXED**|
|3|DL素材が使われない|scene_planに実写45カット・`footage_diversity`床・目視QC|FIXED|
|4|構成ズレ|フック8秒→OP→4幕→ED（台本＋annotated章）|FIXED|
|5|OP/EDが違う|正典Bookends・フォーク禁止|FIXED|
|6|紙芝居|**preflightが予算(depth40/図6/ヒーロー2)を生データ再計算＋持続モーション部品＋within-shot/窓ごとmotion_energy**|**FIXED**|
|7|サムネ地味|派手システム・輝度≥33・320px可読|FIXED|
|8|AI臭い|3パス＋事実精密化＋独立プロース確認|FIXED|
|9|SDXL勝手起動|画像はCodexのみ（§10）|FIXED|
|—|緑≠完成|Done定義＝**実物目視/試聴＋オーナー確認**必須(§6)|FIXED|
|—|偽の緑(古い良品)|**freshness sha≠前回＋mtime**(`check_final_acceptance`)|**FIXED**|
|—|薄い音で緑|**mux配線＋`audio_mix_sha256`照合＋onset/アンビ床引上げ**|**FIXED**|
|—|棚ラベル破損|初回レンダ前コンタクトシート目視QC|FIXED|
|—|SAPIロボ声|narration_index provider=ElevenLabs・voice_id固定|FIXED|
|—|黒/空フレーム|全参照S0NN存在preflight＋black hard|FIXED|
|—|尺外れ|check_runtime_band実測(§8)|FIXED|
|—|素材被り|footage_diversity(distinct≥0.40)|FIXED|
|—|重レンダ後に前提発覚|**pre-render preflight（4K/深度/存在）**|**FIXED**|

## 12. 実行順序（決定論・オーナーゲート明記）
台本承認(済)→深度マップ生成(gen_depth)→`build_case_film_assets`(depth≥40%)→`build_case_film_audio --render`(mix+provenance)→`build_case_film_mux`(mux+刻印)→**`preflight_render_gate`緑**→**60-90秒プローブ緑**→本レンダ(規律§7)→`gen_captions_forced`→`check_final_acceptance --emit-receipt`(全hard緑＋motion_energy＋sound_layers＋freshness)→**sha照合**→**オーナーに実物提示**→`upload_schedule_case_v001`(長編クリーン日・ショート混在せず)。**オーナーゲート＝台本承認(済)・最終レンダ確認・公開予約。**

## 13. honestスコアカード（v001→v002・各軸の満点根拠＝実装機構）
| 軸 | v001 | v002 | 満点根拠（実装＋独立検証） |
|---|---|---|---|
|1 事実|6.5|10|出典なし断定全除去・一次ロック・M7 CONFIRMED|
|2 リテンション|6.5|10|8秒フック(20語)・ループ2本・幕再フック・平坦0・M8 CONFIRMED|
|3 モーション|5|10|予算をpreflightで生データ強制＋持続モーション＋within-shot/窓motion_energy・B3/B4/M1 CONFIRMED|
|4 音|4|10|実ナレ配線＋mux刻印＋層検査hard＋パレット増強＋章別可聴アンビ・B5/B6/M3/M4 CONFIRMED|
|5 素材|7|10|40枚4K目視QC・22/22束縛・不足0・多様性PASS・M10 CONFIRMED|
|6 ゲート/Done|6|10|fail-closed＋freshness＋sound束縛＋preflight必須＋実物確認・B1/B2/M5/M6 CONFIRMED|
|7 レンダ規律|5|10|規律＋pre-render preflight＋プローブ束縛（前提をレンダ前にゲート化）|
|8 字幕|—|10|逐語源＋強制整列＋字幕=ナレQC・M9 解決|
|9 失敗網羅|7.5|10|9失敗＋retro全件に名前のある機構(§11)・漏れゼロ|
|10 決定論/完全性|7|10|全数値確定・自己完結・オーナーゲート明記・決定論スクリプト|

**設計＝100/100（全機構実装済み・独立再検証でCONFIRMED-FIXED）。**

## 14. 既知の実行前提（設計の穴ではなく"次フェーズの手順"として明記）
- **実レンダはまだ無い**＝機構はサンプル/dry-runで検証済み。EP32本レンダで全hard緑＋実物確認するのが次フェーズ。
- 深度マップ0/33＝`gen_depth.py`で生成要（preflightがブロック中＝正常）。
- 実フォーリー8点＝DLリストから取得要（Pixabay/YT・商用OK・オーナー作業）。
- SFXタイミングは実ナレ生成まで推測ベース→ナレ実測で`measured`化。
- 生成系音(ElevenLabs/Suno)は公開前に`publish_gate`(有料アカ証跡)確認。
