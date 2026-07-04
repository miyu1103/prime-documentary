# EP29 制作設計書 — "Thirty Years in the Dark"（無実の死刑囚）

**Episode ID:** `PD-2026-029-hinton`  ·  **slug:** `hinton`
**Series arc:** *They Did Nothing Wrong*（普通の人 vs システムの暴走）2/3
**Duration profile:** standard — target **12:00 (720s)**, band **690–750s** · **AS-BUILT (2026-07-05): 696.8s = 11.6min（band内）**
**R-rating:** **R2**（実在・存命人物＋死刑・人種。fact_recheck と公開前法務ゲート必須）
**Binding spec:** `docs/PD_ONE_PASS_PRODUCTION_SPEC.v2.md`（rows 1–16 のインスタンス）

---

## 0. ログライン / なぜ勝てるか

> 30年間、アラバマ州は彼を殺す準備をしていた——彼がやっていない2件の殺人のために。

- **データ勝ち筋との一致**：「これは他人事じゃない × 権力(司法・州)の暴走 × 正義」。**人種 × 死刑 × 30年 × 逆転**＝US最強の拡散燃料（怒り＋涙）。政府/州が悪役＝名誉毀損リスク低め。
- **感情設計**：理不尽（無実で死刑房）→ 尊厳（房の中で人間性を失わない男）→ 逆転（全員一致の最高裁・釈放）。
- **入口ショート（別制作）**：`30 Years on Death Row for a Crime He Didn't Commit #Shorts`

> **オーナー厳命(2026-07-04)：見ごたえ最優先。「普通の情報提供」は禁止。** 事実の羅列にしない。一流のドキュメンタリー作家の**物語**として、緊張・謎・人物・転換・ペイオフで引く。**台本は最低3回レビュー（§10a）。**

---

## ✅ 制作ステータス（AS-BUILT 2026-07-05）

左工程＋ナレ音声＋字幕まで完成・機械ゲート緑。**残るは画像→組立のみ**。
- **事実**: `fact_recheck.v001`（多出典・GUARDRAILS）で確定。
- **台本**: `script.annotated.v001.json`（正典スキーマ）＝確定ナレ源・**2,058語**（3パス済）。
- **ナレ音声**: ElevenLabs master **676.3s**（`voice_is_master` PASS・$約4）。
- **字幕**: 強制アライン `captions.final.v001.srt`（一致100%／format／カバー **全PASS**）。
- **尺**: 総尺 **696.8s = 11.6分**（band 690–750 内）。式＝hook8＋opening3.5＋ナレ＋endcard9。
- **カット割**: `shotlist.v001.json`（**251カット**・平均2.8s・treatmentローテ・密度≥23）。
- **残**: 画像40枚(Codex・`ai_prompts.v001`)→`remotion/public/hinton`ステージ→`data/hinton_film.json`→Remotion組立→`check_final_acceptance` exit0→MotionSample目視。

---

## 1. 事実の骨子（**FACTS LOCKED**: `fact_recheck.v001` で多出典確定・GUARDRAILS拘束）

実話ベース：**Anthony Ray Hinton**（アラバマ／無実の死刑囚）。

- ★ 1985年、ファストフード店長を狙った連続強盗殺人（2件）でアラバマの黒人男性 Hinton を逮捕。犯行時、彼は**施錠された倉庫で夜勤中**というアリバイ。
- ★ 有罪の柱は**信用性の低い弾道（ballistics）鑑定**——母親の古いリボルバーと現場の弾が「一致」とされた。
- **弁護が機能不全（訂正・最重要）**：弁護人は鑑定費を**上限$1,000と誤認**（実際は上限規定なし）→その額しか請求せず、雇えた"専門家"は**片目しか見えず比較顕微鏡を操作できない**土木技師。※この**"誤認"が最高裁のineffective assistance判断の核心**（"予算上限"ではない）。
- 逮捕1985/7/31・**有罪1986/9/17**（評決約1時間）→ **nearly 30 years** 死刑房（2015/4/3釈放＝死刑冤罪152人目）。※尺表現は"約30年/almost three decades"、断定年数は避ける。
- ★ **Equal Justice Initiative / Bryan Stevenson** が受任。新しい弾道専門家が「弾は銃と一致しない」と証明。
- ★ 2014年、**連邦最高裁が全員一致**で「弁護は違憲的に不十分」（*Hinton v. Alabama*）。
- ★ 2015年4月、州が再鑑定で結び付けられず**釈放**。回顧録 *The Sun Does Shine*（★2018）。

> **不変項1/10/13：** ★は全て公開記録（EJI／連邦最高裁／全国報道／本人回顧録）から**逐語ロック**するまで本文に書かない。ドラマは事実の上に立てる。人種・死刑という重い主題を扇情でなく**尊厳**で描く。存命本人の肖像は作らない（§5）。

---

## 2. 4部構成 — 秒割タイムライン（**AS-BUILT: fps=30（CaseFilm／BRAND.video.fps）／全長 696.8s** ／ 数値は定数）

> **AS-BUILT SYNC (2026-07-05)** — 真実源＝`episodes/PD-2026-029-hinton/03_script/script.annotated.v001.json`（この .md は当初ドラフト）。実測: ナレ **676.3s**・**2,058語**・**28 on_screen_text**・字幕全PASS・`shotlist.v001` 251カット・総尺 **696.8s**（hook8+OP3.5+676.3+ED9・band内）。CaseFilmは **30fps**（旧記載 fps=60 は誤り＝オープニング実演用で長尺エンジン非適用）。組立=`CaseFilm-hinton`（プレミアム＋別スレAmbientMotion/派手Bookends/3Dヒーローで統一）→ ship-gate 受領書緑まで（`docs/PD_SHIP_GATE.md`）。

| Part | 区間(s) | 尺 | 役割 | ナレ語数(≈173wpm) |
|---|---|---|---|---|
| **HOOK** | 0.0–8.0 | 8.0s | フラッシュフォワード：死刑房の鉄扉／「30年」「無実」のタイポ。**最後に書く** | ~23w |
| **BrandOpening** | 8.0–11.5 | 3.5s | 金 `BrandOpening`（フックの後） | 0 |
| **ACT I 逮捕** | 11.5–~175 | ~2.7min | 夜勤のアリバイ／逮捕／"一致した"弾＝ジャンク科学の芽 | ~470w |
| **ACT II 崩れた裁判** | ~175–~350 | ~2.9min | 貧困の弁護・不適格鑑定・人種の偏り。有罪へ | ~500w |
| **ACT III 30年** | ~350–~560 | ~3.5min | 死刑房の時間／房で人間性を保つ男／EJIの闘い（再フックの山） | ~605w |
| **ACT IV 光** | ~560–711 | ~2.5min | 全員一致の最高裁／釈放／**フック回収**／稼いだLikeへのCTA | ~430w |
| **BrandEndcard** | 711–720 | 9.0s | `BrandEndcard`（CTA/cadence） | 0 |

**ナレ合計 ＝ 2,058語（AS-BUILT）**＝ElevenLabs実音声 **676.3s** → 総尺 **696.8s＝11.6分（band内）**。※当初~1,750語で band 下限割れが判明し、出典内で **+約300語**して補正済（2026-07-05）。
**リテンション（row16）**：フックの謎（彼は殺されるのか？）をラストまで保持。オープンループ「だが弾は、嘘をついていた…」をACT II末。**再フック~2:30ごと**（アリバイ→鑑定→30年→最高裁）。20秒超の平坦禁止。

---

## 3. HOOK（0:00–0:08）— 最後に書く・ペイオフ検証（row 9）

- **画**：4カット×~2.0s。1) 死刑房の鉄扉が閉まる（フッテージ暗め+ネイビー）2) 現場の弾丸マクロ→「MATCH?」が砕ける（モーショングラフィックス）3) 房内で天を仰ぐ**匿名の男**（実在に似せない）4) 「30 YEARS / INNOCENT」の巨大タイポ。
- **フック文（★暫定）**：`For thirty years, Alabama planned to execute him — for two murders he did not commit.`
- **ペイオフ**：ACT IV で「全員一致の最高裁→釈放」を必ず提示（promise-payoff = true）。

---

## 4. FILM BIBLE（Academy級・row15/16）

- **コールドオープンの問い**：無実の男を、州はなぜ30年も殺そうとし続けたのか。
- **三幕の上げ**：個の冤罪（I）→ 制度の欠陥＝ジャンク科学＋貧困の弁護＋人種（II）→ 時間との闘いと尊厳（III）→ 逆転と代償（IV）。
- **人間の縦糸**：房の中でも笑いと想像力を手放さない男（回顧録の核）。
- **モチーフ**：**光と闇**（*The Sun Does Shine*）。時間（刻まれる年月）。一致しない弾（真実 vs 見せかけの科学）。
- **テーマ**：「確実そうに見える証拠ほど、確かめよ。」
- **禁止**：扇情・平板な事件解説。**普通の情報提供は不合格。**

---

## 5. ビジュアル/アニメ・システム（row8・`MotionSample.tsx` 準拠＝紙芝居禁止）

**土台＝`remotion/src/compositions/CaseFilm.tsx`（プレミアム・エンジン, `data/hinton_film.json` 駆動, fps=30）。** 実装記録＝`docs/PD_ONE_PASS_PRODUCTION_SPEC.v2.md §C2`。承認済み `MotionSample` の質感を全編維持。**統一アニメ**＝別スレの `components/AmbientMotion.tsx`（各ビートに重ねる手続き型モーショングラフィックス）＋派手 `Bookends`（OP/ED）と合体（コミット後に重ねる。二重実装せず彼らのを使う＝不変項14）。**数値は決定論＝値で書く。**

### 5.1 カット遷移（"かくっ"禁止・全カットに設計トランジション）
- 平均カット長 **2.5–3.0s**。**裸のハードカット禁止。**
- **クロスディゾルブ**：隣接カットの Sequence を **0.35s オーバーラップ**で溶かす（1F黒/ジャンプなし）。**カット越しに動きの向き・速度を継続**（velocity resetしない＝"かくっ"根絶）。
- **入りの設計モーション**：`spring{damping:18,stiffness:90,mass:0.9}` で index%3 ローテ＝プッシュイン(scale 1.14→1.0)/せり上がり(translateY 64→0px)/スライド(translateX ±60→0px)。
- **モーションブラー**：入り 0–9F 減衰 `blur(14→0px)`。速い要素は `@remotion/motion-blur` **Trail(layers 6–7, trailOpacity 0.5–0.55)**。

### 5.2 静止画（Codex生成）を動かす（同一手法連続禁止でローテ）
- `bleed`＝2.5Dパララックス(fgS 1.05→1.14)／`scan`＝走査光+微グリッド／`duotone`＝ネイビー基調／`focus`＝ラックフォーカス(blur 16→0)。斜め2.5D `card` は**稀に**。
- 各カット常時：**Particles＋Vignette＋Grain(0.11)**。統一後は **AmbientMotion** を上に重ね「静止フレームゼロ」。

### 5.3 キネティック・タイポグラフィ（`on_screen_text` を必ず実装＝**28ビート**）
- `script.annotated` の**全 `on_screen_text`**（`30 YEARS`／`INNOCENT`／`9–0`(全員一致)／`MATCH?`(砕ける)／`ALIBI`／年）を上部1/5に大型キネティックタイポ（下部字幕と別レイヤー・span↔chunk 1:1）。
- **マスク切り上がり**：`overflow:hidden` 枠内で translateY 118%→0（`spring{damping:18,stiffness:110}`）、行ごと **7F stagger**。line0=白/以降=gold。short=92px・long=54px。
- **金キッカーチップ**＋**金アニメ下線**（scaleX spring）＋入りに **Trail** 残像。
- 数値/年表（`30 YEARS`のcount-up、`9–0`、弾道"一致しない"可視化）は count-up / draw-on で動的に。

### 5.4 フッテージ（factory棚＝主役）
- 強め暗く＋**ネイビー multiply 0.14＋ビネット**で統一。**featureless（素の霧/空/抽象）は除外**。各クリップにゆっくり push（translateX ±14, scale 1.04→1.1）。

### 5.5 Runway／禁止
- **Runway**：フック or 釈放の決定的 **1–2カットのみ** img2vid。使いすぎない。
- **禁止**：金の縦スイープ（`WipeTransition`）／黄・金の全画面ウォッシュ・フラッシュ／ただのズーム・左右パンだけ（`CameraRig`）。`StyleTest`は手本にしない。

### 5.6 情報ビジュアル＝Figures tier（別スレ `DiagramFlow` 拡張を取り込む・row16）
データ系は平文でなく**アニメ図**（`PD_MOTION3D_HERO_AND_FIGURES_SPEC §3`・単一アクセント・暗いサーフェス・`useCurrentFrame()` 駆動）：
- **StatCounter**：`30 YEARS`／獄中年数を **0→値 count-up**（`Easing.out(Easing.cubic)`）＋accent下線。
- **Timeline**：1985逮捕 → 死刑判決 → 2014最高裁(9–0) → 2015釈放。baseline を L→R spring、event dot 0.18s スタッガー、year+captionマスク上げ。
- **BarChart / 対比**：弾道"一致"の主張 vs 再鑑定＝一致しない、を対比バーで（0.12s スタッガー・direct label）。
- **NetworkDiagram**：EJI/Stevenson → 新鑑定 → 最高裁 の関係図（edgeを `strokeDashoffset` spring で描く）。

### 5.7 プレミアム3Dヒーロー階層（`PD_MOTION3D_HERO_AND_FIGURES_SPEC` L1–L3・elective・**owner-gated**）
- **掴みヒーロープレート**：コールドオープン（金 `BrandOpening` 着地の前）に **Blender L2 EEVEE**（発光ジェム＋Glare Bloom＋反射床＋DOF f2.2, ~1.8s/f）を PNGseq→`libx264 crf16 yuv420p`→`OffthreadVideo` で敷く。最上級1カットのみ **L3 Cycles**（ガラス屈折 IOR1.85＋Bevel, AgX, ~8s/f）。抽象生成物＝不変項11 OK。EP29モチーフ＝**光と闇**（*The Sun Does Shine*）＝闇に差す一条の光/鉄扉を3Dで。
- **OP背景奥行き**：`@remotion/three`(L1) で `BrandOpening` 背景に実奥行き＋前景ボケ＋スロー・ドリー（Bookendsはタイトル層＝不変項14）。deps `@remotion/three@4.0.484 three @react-three/fiber@8`、参照 `remotion/prototypes/motion3d/`。**本番移植はオーナー承認後**。
- 決定論：全モーション `useCurrentFrame()` 駆動（r3f `useFrame` 禁止）、encode row6 値。

### 5.8 アニメ最新強化（別スレ実装・レベルアップ反映 2026-07-05）
> **coordination（不変項14）**：下記は別スレの実装（プロトタイプ＝`remotion/prototypes/`／pino-channel workbench）。本番は各コンポーネントの**コミット後に彼らのものを使う**（私は二重実装しない）。全て `useCurrentFrame()` 駆動・決定論。

- **① 任意画像の"実"3D深度パララックス（challenge#1・実装済）**：全ヒーロー静止画に **DPT深度マップ（Intel DPT / ComfyUI venv）** を生成→`@remotion/three` で**細分割プレーンを変位**→カメラ移動で**単一の静止画から"本物"のパララックス**。＝2.5Dカードの擬似深度でなく**実深度**で、**「紙芝居問題」を全静止画で根絶**。移植先＝`MovingImage` バリアント（`depth/depth.py`＋`depth/DepthScene.tsx`）。**EP29の40枚全部**に効く＝death-row/鉄扉/夜勤/法廷が生きる。
- **② dolly-in＋dust 改良（fix・実装済）**：弱い横オービットは廃止（メッシュ伸びを隠す＝wow無し）。**カメラが写真の中へ入る"確信のdolly-in"（head-on＝ラバーシート融解回避）**＋強めの変位＋**前景の3D dust motes がプレーンに対して視差**＝実奥行きを売る。EP29は房内/鉄扉/夜勤カットで特に効かせる。
- **③ 音声リアクティブ・ビジュアル（challenge#2・実装済）**：`@remotion/media-utils` が完成mix音声から **脈打つコア＋円形スペクトラム＋波形＋エネルギーグロー** を駆動＝**画がナレの息に合わせて呼吸**（retention row16）。使いどころ＝コールドオープン／`reveal`（**9–0の瞬間**）／感情の山（54処刑・釈放）。**全編化しない**（点で効かせる）。
- **④ アニメーション地図（challenge#3・実装済）**：`MapScene.tsx`（`us-atlas`＝US Census 由来・パブリックドメイン、d3 `geoAlbersUsa` 投影）＝**死刑存置/廃止で州を2色に割る**・**Alabama（Hinton の州）を発光**・冤罪確定数を州ピンで。地理を"正確に"見せる（row16）。参照＝`remotion/prototypes/motion3d/map/`（`convert_map.mjs`→`us_map.json`／実行時d3不要）。
- **⑤ 剛体崩壊シミュ（challenge#4・Blender・実装中）**：**証言/物証が崩れる**（弾道一致の虚構が砕ける）決めカット1つを Blender剛体（EEVEE・Bloom・DOF→`OffthreadVideo`）で。owner-gated・点で。参照＝`blender/bpp_physics.py`。
- **統合**：①②は静止画技法（§5.2の`bleed`）を**実深度パララックスへ格上げ**、③は感情の山、④は"死刑の地理"、⑤は証拠崩壊の決めカットに重ねる。`AmbientMotion`（各ビートの手続き型MG）＋派手`Bookends`と合体（コミット後）。**本番移植・3Dヒーロー(§5.7)・地図/物理はオーナー承認後**。

> **不変項11＋オーナー指示(2026-07-04)**：**人物の姿は描いてよい**（匿名の代表的人物）。**禁じるのは実在・特定本人の肖像だけ**（Hinton本人・実在の関係者の顔の再現）。Codex画像は「房の中の匿名の男」「看守」「法廷の匿名の人々」「夜勤の労働者」等で描く（実在の誰かに似せない）。実写の本人アーカイブは権利未クリアで不使用（factory棚＝権利クリア汎用のみ）。

---

## 6. 素材プラン（row7・集めて未使用ゼロ）

- **多様性ゲート `footage_diversity`（機械・ハード）**：distinct/total **≥ 0.40**・単一クリップ再利用 **≤ 4回**・天秤/ガベル等の汎用象徴 **≤ 2回**・空スパン 0。ビルダーは上限3/汎用1で更に厳しく散らす。**画像:フッテージ ≒ 4:6**、no-repeat(MIN_GAP~22)。
- **factory抽出テーマ**（`select_factory_assets.py --theme`・**組立前に90本前後を分散ステージ**＝distinct_frac≥0.55確保）：`crime_police`(現場/警察)・`legal_court`(法廷/ガベル/書類/独房・刑務所)・`forensics_dna`(弾道・鑑定・実験)・`documents_paper`・`urban_night`(夜の街)・時計/カレンダー。cf. `[[reference_factory_shelf]]`。EP28と同一クリップの再利用を避け**別テーマ束から引く**（[[feedback_footage_diversity]]）。
- **Codex ヒーロー静止画**（`ai_prompts.v001`・**計40枚**・1画像1プロンプト・長辺≥3840・**匿名人物OK/実在本人なし**・使い回し単調回避）：房内で座る匿名の男／鉄扉／弾丸マクロ／古いリボルバー（証拠）／法廷の匿名の陪審／夜勤の倉庫／窓から差す一条の光。negative に `specific real person / celebrity likeness, on-image text, bad anatomy`。人物は自然な実写調・特定実在に似せない。

---

## 7. OP/ED（row14・正典Bookends・作り直さない）

- `components/Bookends.tsx` の `BrandOpening{seriesLabel,title,subtitle}` / `BrandEndcard{...}`（`OPENING_SEC=3.5`/`ENDCARD_SEC=9` 固定）を import。フォーク禁止（不変項14）。金OPはフックの後、EDは末尾。
- `seriesLabel="Prime Documentary"`。**ED CTA（稼いだLike）**：`If a State can do this to an innocent man — hit like, so it's harder to look away.`

### 7a. 音声エンディング（オーナー指示2026-07-04・row1関連）
- EDのBGMは**切りのいい所（musicalな終止）で終わる**。末尾9秒 `BrandEndcard`＝**アウトロ専用枠**。
- **エンディング用キュー**を **align-to-end 配置**（"曲の終わり"を動画終端に一致・途中でブツ切りしない）＋拍/終止に合わせ**1.5–2sクリーンフェードで無音着地**。
- **ナレ長・間は一切変えない**（尺は台本が主）。ゲート＝**`bgm_ending`**（全音量チョップでない）。musicalな収まりは最終**耳チェック（末尾10秒）**で確認。

---

## 8. サムネ（rows11–13・派手・肖像なし）3案

全案：1280×720・UPPERCASE ≤4語・巨大主題・超高コントラスト・黒/ネイビー＋**gold `#E5B53A`/electric `#1F6BFF`**・白/銀文字・320pxで可読・Codex背景生成・`selected`1つ。

1. **`30 YEARS. INNOCENT.`** — 死刑房の鉄扉＋差し込む一条の光（gold）。
2. **`THEY WANTED HIM DEAD`** — 空の電気椅子/独房の影、白文字＋gold下線。
3. **`THE BULLETS LIED`** — 弾丸マクロ＋割れた"MATCH"、electric accent。

タイトル（≤60・フック先頭・A/B）：
- A `Thirty Years on Death Row — For a Crime He Never Committed`
- B `Alabama Tried to Execute an Innocent Man for 30 Years`

---

## 9. 通過必須ゲート（Done・§D）

`./.venv/Scripts/python.exe scripts/check_final_acceptance.py 29 --json` **exit 0**（ハードゲート＝実ファイル測定）：
`runtime_band`690–750s／`render_resolution`≥1920×1080／`images_present`／`motion_present`＋**`animation_density`**(near-still≤10%・単一ホールド≤3s＝紙芝居/スローKB検出)／`bgm_present`(無音>25sなし)＋**`bgm_ending`**(終端が切りよく解決)／`voice_is_master`(ElevenLabs)／`captions_final`(≥90%)／`caption_format`／`caption_narration_match`(字幕↔ナレ≥90%)・`structure_4part`(HOOK→OPENING→body→ENDING＋`hinton_film.json`実フック)・`op_ed_bookends`(正典Bookends)／`thumbnail_ready`＋**`thumbnail_visibility`**(輝度mean≥33＋コントラスト＝暗い/しょぼいサムネ阻止)／`image_resolution`(≥3840)／`factory_used`＋**`footage_diversity`**(distinct/total≥0.40・再利用≤4・天秤等汎用象徴≤2＝素材使い回し阻止)。
**Ship-gate（`docs/PD_SHIP_GATE.md`）**：`check_final_acceptance.py 29 --render <mp4> --emit-receipt` で**動画sha256紐づけ受領書**発行 → `upload_schedule_case_v001.py --ep hinton` は**緑の受領書（sha一致・許容不合格はruntime_bandのみ）が無ければ物理的に投稿不可**。自己申告Done不可。
**手動実測（飛ばさない・未コード）**：row5画質/sharpness・row13タイトル≤60/A-B・row15クラフト・**目視で失敗1〜9消滅**（MotionSampleと並べ／on_screen_text全実装）。

---

## 10. Codex前にClaudeがロックする成果物（§B・左工程ゲート）

1. `EP29_FILM_BIBLE.v001` + `script.annotated.v001.json`（Academy級・フック最後・4部ロール・173wpm band・`on_screen_text`/`visual_intent`）
   - **§10a 台本レビュー＝最低3パス（全パス通過まで handoff しない）**：
     - **Pass1 事実/因果(R2/R3)**：全★を出典で逐語ロック・causation lock・死刑/人種/存命人物の扱いを法務チェック・捏造ゼロ。
     - **Pass2 ドラマ/クラフト(row15)**：問い→三幕→ペイオフ。**「普通の情報提供」化を1文ずつ潰す**。
     - **Pass3 リテンション/字幕(row16)**：再フック~2:30ごと・平坦20秒なし・オープンループ回収・語数band・息継ぎ字幕。
2. `shotlist.v001.json`（全スパン asset_type+motion+transition+`search_keywords`・平均≤6s・0.35sディゾルブ）
3. `ai_prompts.v001`（1画像1プロンプト・匿名人物OK/実在本人なし・≥3840）
4. `thumb_prompts.v001` + 見出し/キッカー
5. **`fact_recheck.v001`(R2)**：★の固有名詞/年/鑑定/最高裁判旨を逐語ロック＋法務
6. `manifest.target_duration_minutes = 12`

> **順序**：fact_recheck(R2) → FILM_BIBLE/script（3パス）→ shotlist/prompts → Codex画像 → Remotion組立(Claude) → acceptance exit0 → **目視で失敗1〜9消滅** → オーナー各ゲート → `package_ready`。**1本ずつ。**
