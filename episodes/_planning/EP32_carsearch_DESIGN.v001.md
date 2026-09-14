# EP32 制作設計書 — "Can the Police Search Your Car?"（自動車例外）— 革命フォーマット第1号

**Episode ID:** `PD-2026-032-carsearch` · **slug:** `carsearch` · **Series:** us-court-cases
**Duration:** standard — **~11分**（band 690–750s）· **R-rating:** R2（Collins 2018＝存命人物。役割のみ・実在肖像なし）
**Binding:** `docs/PD_ONE_PASS_PRODUCTION_SPEC.v2.md` + `docs/PD_SHIP_GATE.md` + 本書（革命フォーマットの追加拘束）。
**なぜ革命第1号か:** 実測(pd-analytics-findings)の勝ち筋「警察 vs あなたの権利・第4修正・二人称・自分事」ど真ん中。北極星（CTR6%/APV45%/30秒残存70%）を初めて取りに行く実証台。**"今までと同じ(CaseFilmにストック静止画＋文字を貼る)"を一切やめ、成功チャンネルの型を丸ごと真似る。**

---

## 0. 勝ちフォーマット（型を丸ごとコピー＝オリジナル不要）
- **土台＝Veritasium型**：実写b-rollと現場の音をふんだんに。
- **説明＝Kurzgesagt/TED-Ed型**：概念そのものが**動く図解**で説明される（ストック＋文字でない）。
- **音＝4層設計**（欠落の最大要因を埋める）。
- **PDの小アクセント**：ダーク・ノワールのグレード、金/電光ブルーのブランド、ブライトライン・モチーフ。

## 1. 事実（FACTS LOCKED — `01_research/claims.v001.json` CLM-0001..0010）
Carroll v. US (1925) 自動車例外誕生・probable cause／Collins v. Virginia (2018, **8–1 Sotomayor**, Alito単独反対)「automobile exceptionは自動車自体を超えて及ばない」curtilage＝家の外周は家の保護／scope=対象(Ross・Acevedo)／別exigency不要(Labron・Dyson)／Gant(逮捕付随の限界)／Byrd(レンタカーのプライバシー)／大麻臭＝**州次第・未確定**とフラグ。一次資料（判例本文・最高裁PDF・LII・SCOTUSblog）で逐語ロック。**LLMを出典にしない・E級を本文に入れない・実在肖像なし・中立。**

## 2. 台本（`03_script/script.en.v001.md`・~2,000語・約11分・3パス済）
8秒フック（100年前から令状なしで車を捜索できる／だが一箇所だけ踏み込めない）→ OP → **ACT I** Carroll/1925 → **ACT II** probable causeの真意＋捜索の"リーシュ" → **ACT III** Collins/タープのバイク（回収） → **ACT IV** 権利の地図＋実用的心構え → curtilageで回収 → ED CTA。二人称・オープンループ2本・幕ごと再フック・平坦20秒ゼロ。**全ビートに動く図＋音キューを台本に埋込済（VIS:/SFX:）。**

## 3. ビジュアル/アニメ（革命の核＝"見ごたえ"を予算として先に確保）
**土台＝`CaseFilm.tsx`（プレミアム版・data駆動, fps30）。** ただし**"また少ない"を根治するため、レンダ前にビルダーで知覚的モーション予算を強制**（ゲート最適化でなく目に最適化）：
- **① depthカット ≥ 40%**（画像カットの4割以上を実深度パララックス`DepthStill`。深度マップは`gen_depth.py`で全画像に事前生成）。
- **② 動くFigureBeats ≥ 6**（数値/年表/概念を平文でなくアニメ図に。下記の専用部品）。
- **③ ヒーロー・モーション面 ≥ 2**（Blender EEVEE掴みプレート or 専用の力あるモーション面。フック冒頭＋Collins山場）。
- **④ カット刻み平均 ~2.2s**（速い）／**⑤ 転換多様化**＝`ForcefulCut`（push/slide/zoompunch/whip・**金縦スイープ`WipeTransition`は禁止**）／**⑥ パララックス振幅UP**。

### 3a. EP32専用の"動く図解"部品（`src/components/carsearch/`・実装済・型チェック緑）
各ACTに最低1つ配置：
- `BrightLine`（draw/hold/slam）＝全編モチーフ。**slam＝Collins「NO」の山場**（最大の衝撃・Trailブラー＋フラッシュ）。
- `CarCutaway`（all/big/small）＝ACT II「捜索可能ゾーン」を車の断面で分解（scope=対象の可視化）。
- `ProbableCauseMeter`（stall/cross）＝ACT II「 hunchは足りない／probable causeで越える」。
- `CurtilageShield`＝ACT III「家の保護が外周に広がる」＝curtilage回収。
- `StateMap`＝ACT IV「大麻臭＝州次第」を非一様な色で。
- `CaseTimeline`＝ACT I/III/IV「1925 Carroll→2009 Gant→2018 Collins」年表。
- `CarKeyLock`＝ACT III「最も露出した車が最も守られた家の鍵になる」。
- `KineticType`（既存）＝キネティック字幕（モーションブラーで滑込/弾け）。`Figures`/`FigureBeats`＝汎用アニメ図。
- **ヒーロー面**：フック冒頭に`BrightLine slam`級 or Blender L2プレート、Collins山場に`CarKeyLock`+`BrightLine slam`。

### 3b. フッテージ（factory棚＝主役級・Veritasium型）
実写b-roll ~100本以上を**初回レンダ前にコンタクトシート目視QC**（ラベル破損対策）でステージ。夜の交通停止・パトランプ・住宅街・車内・法廷・高速など。強め暗く＋ネイビー＋ビネットで統一。featureless除外。

## 4. 音設計（4層・欠落の最大要因を埋める＝PD Gideon実績110+キューの現代化）
`build_case_sound_design.py`（新設）で台本のSFXキュー＋カット境界から自動生成：
- **層1 ナレ**（ElevenLabsマスター・最前面）
- **層2 劇伴**（幕/ビートで上下・reveal/tension/somber/outro）
- **層3 連続アンビエンス**（場面ごと：夜窓/法廷/オフィス/緊張ドローン。低音量ベッド）
- **層4 SFX**（カット境界にwhoosh・リビールにboom/impact・盛上げにriser・図にui-tick/data-blip・stamp/gavel/page-turn・sub-drop）。台本の`(SFX:)`を逐次配置。
- ミックス＝サイドチェーン（VO優先）＋loudnorm -14。**音密度ゲート**（SFX/アンビエンス存在を機械検出）追加。

## 5. 品質ゲート（Done＝ゲート緑＋実物目視/試聴。自己申告禁止）
- 既存 ship-gate（`check_final_acceptance.py --emit-receipt`＋受領書sha）＝全hardチェック。
- **新規 optical-flowゲート `motion_energy`**：`measure_motion_energy.py`（tblend差分＋signalstats YAVG）＝**実際の動きの量**。較正＝MotionSample(動的)46.6 / v004(紙芝居)3.5 →**本編mean ≥ 12**（＋sustained-low p10フロア）。＝"凍ってない%"を超えて"ちゃんと動く"を機械化。
- **知覚的モーション予算(§3の①②③)をビルダーで先に検証** → 満たしてからレンダ。
- **偽の緑対策**：再レンダ後「実ファイル存在＋sha≠前回sha」を確認してからmux/受領書。
- **本レンダ前に60–90秒スライスでプローブ**（動きエネルギー＋目視）。

## 6. レンダ規律（EP31/EP29振り返りの確定ルール）
- **`tail`/`head`を通さない**。生ログへ→`grep 'Rendered [0-9]+/'`で直接監視。**完走まで絶対killしない**（見えない≠止まってる）。
- **1本ずつ直列**（並列はバンドル/RAMを食い合う。別スレと交通整理）。**depth/WebGL長尺は`--concurrency=4` or セグメント分割**。
- 健全性＝Rendered X/Y行・headless chrome数(>0)・実mp4成長。CPUは補助。プロセスはCommandLineで分類。
- **画像は必ず4K化**（gen前に解像度チェック。1672のまま重レンダしない）。**Windowsパスはraw string**。

## 7. OP/ED・サムネ
正典Bookends（`BrandOpening`/`BrandEndcard`・フォーク禁止）。ED CTA＝台本のとおり。サムネ＝派手版システム（v003方式：明るいヒーロー＋赤バースト＋特大黒縁＋"$40"級のフック語）。二人称。3案＋selected。輝度mean≥33。

## 8. Codex画像（`EP32_carsearch_ai_prompts.v001.md`・**40枚**）
S001–S040：再現の要所＋別アングル/寄りの派生（速いカットで被らない）。匿名人物のみ・実在肖像なし・on-image text無し・4K化。並行生成可。

## 9. 実行チェックリスト（この設計書の結晶）
- [ ] factory初回レンダ前にコンタクトシート目視QC
- [ ] 知覚的モーション予算：depth≥40%／動くFigureBeats≥6／ヒーロー面≥2 を確保
- [ ] カット~2.2s・転換多様化・パララックス振幅UP
- [ ] 4層音設計（SFX/アンビエンス/劇伴）
- [ ] 60–90秒プローブ（動きエネルギー＋目視）→ 本レンダ（tail無し・1本ずつ・concurrency4・killしない）
- [ ] sha照合（再レンダ後 実ファイル存在＋sha≠前回）→ mux → 受領書
- [ ] `motion_energy`本編mean≥12 ＋ 全hardゲート緑 ＋ **オーナーに実物を1回見せて"動き足りてる?"確認**
- [ ] 予約：ドライラン→metadata提示→GO→本番（長編クリーン日・ショート混在せず）

## 10. 分担・順序
Claude＝左工程（企画/リサーチ/台本）＋Remotion組立＋音設計＋レンダ＋最終チェック。Codex＝40枚生成。**オーナーゲート**＝台本最終承認・公開予約。順序＝台本承認→画像→4K/深度→組立(予算確保)→プローブ→レンダ→目視＋motion_energy→受領書→**実物提示**→予約。
