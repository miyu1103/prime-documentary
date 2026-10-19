# EP35「hinders」動画素材マニフェスト（別スレ制作用・アニメ素材のみ・**超激重 L3 ceiling tier**）

- **Episode**: EP35
- **slug**: hinders（PD-2026-035-hinders / 「FOLLOWING THE RULE.」）
- **制作**: 別スレ（本文全体を読まずにこの素材だけで制作可能な自己完結版）
- **binding**: `EP35_hinders_DESIGN.v001.md`（§3.0〜§3.7・§9.1 が正典）＋ `docs/PD_MOTION3D_HERO_AND_FIGURES_SPEC.md`（超激重tierの正典）
- **prototype参照**: `remotion/prototypes/motion3d/`（`Opening3D.tsx`／`Figures.tsx`／`blender/bpp_cycles.py`・`bpp_eevee.py`・`bpp_physics.py`／`depth/depth.py`・`DepthScene.tsx`／`map/MapScene.tsx`／`audio/AudioReactive.tsx`）
- **解像度/fps**: 1920×1080 / fps=60（本編Remotion）。Blenderヒーロー連番は fps=30 でレンダ→row-6でencode。Composition id=Ep35Hinders。
- **依存**: `@remotion/motion-blur`＋`DepthImageV`＋（超激重）`@remotion/three@4.0.484 three @react-three/fiber@8 @types/three`。WebGL長尺は `--concurrency=4`。Blender **5.1**（`C:\Program Files\Blender Foundation\Blender 5.1\blender.exe`）。dpt-large 深度: `tools/depth/gen_depth.py`（ComfyUI venv python・`Intel/dpt-large`）。

> **オーナー指示「超激重にして」を反映**: ヒーロー面8つ＋主要図を **最上位プレミアム重量級（SUPER-HEAVY / L3 ceiling）** へ格上げした（§SH）。2D板合成（L0=紙芝居の主因）を捨て、**L1 実3D深度（@remotion/three）／L2 Blender EEVEE fast hero／L3 Blender Cycles ceiling hero／物理シム（Mantaflow流体・rigid-body破断・パーティクル点群）** へ写像。**事実数値（金額・件数・claim）は一切改変しない。改変したのはモーション/レンダ品質仕様のみ**。

> 注記（捏造防止）: 設計書は各図に「リビール時刻(目安)」と「持続モーション」を与えるが、**図ごとの秒数(尺)は個別に明記していない**（ヒーロー8図のみ主要モーションのフレーム数が数値化）。持続は「主要モーション完了後もカット終端まで別種構造モーションを継続（freeze整合）」が全図共通。**シーン番号 S0NN は設計が図↔シーンID一対一を列挙していない**ため、配置は「幕＋リビール時刻」で示す（設計の粒度に忠実）。

---

## 1. 専用Remotion図コンポーネント（bespoke FigureBeats 全27図・ヒーロー8） — §3.6

各図は**新規フルスクラッチ禁止**。MOTIONKIT CATALOG.md の既存部品/プリセットへ写像し data-driven props 差分で作る（CLAUDE invariant14・二重実装禁止）。全図に L3 near/mid/far 層パララックス（＝DepthImageVとは別機構）が付く（depth✔）。各図は**描画後 optical-flow 実測で独立運動要素≥6**が必須。**★=ヒーロー（超激重tier対象・§SH）**。

| # | 図ID(コンポーネント名) | 機能（何を見せる図か） | 入力データ（数値・claim） | モーション（リビール＋持続） | 尺 | 配置(幕・リビール) | ★hero |
|---|---|---|---|---|---|---|---|
| F1 | Register38Years | 38年営業のレジ/売上 | 38 years・現金売上 | 数字ホイール減速回転＋near札/far厨房パララックス（終端までドリフト） | カット尺 | Act1 0:35 | |
| F2 | **BSAOriginFlow** | 1970 BSAの資金トラッキング由来が小店へ滴下 | 1970 BSA(CLM-0015)・組織犯罪資金 | 流体連続流下＋細枝が小店へ滴下トラベル | 0–48f流下+滴下λ0.9 Trail | Act1 1:20 | ★ |
| F2b | **StructuringExplainer**(新設) | 「$10k線下に小さく保つ＝罪」の説明 | $10,000線・structuring(§5324) | 入金列を$10k線下で反復→「小さく保つ＝罪」ラベル充填走行 | カット尺 | Act1 2:10 | |
| F3 | **ThresholdMeter** | $10k報告閾値ゲージ | $10,000閾値 | 入金ブロック継続積上げ＋完了後ゲージ微光走行 | 積上げ0–60f stagger6f | Act1 3:05 | ★ |
| F4 | ThresholdBreach | 閾値線の破断 | $10k線 | 亀裂が線沿い継続伝播＋0.5s以内push遷移 | カット尺 | Act1 4:00 | |
| F5 | **FrozenAccount** | 口座凍結 | $32,820.56押収(CLM-0002) | 氷亀裂継続伝播＋near通帳パララックス | 亀裂0–40f λ0.75 Trail | Act2 4:25 | ★ |
| F5b | **BurdenShiftScale**(新設) | 立証責任の逆転 | 民事没収・"PROVE IT INNOCENT" | 天秤が政府側→市民側へ実回転＋"PROVE IT INNOCENT"充填 | カット尺 | Act2 5:15 | |
| F6 | CaseCaptionNameplate | 対物訴訟名 | *United States v. $32,820.56*(CLM-0002) | 訴訟名一語ずつzoompunch＋空被告席midパララックス連続ドリー | カット尺 | Act2 6:00 | |
| F7 | WalkAwayTally | 争わず諦める所有者の列 | 「歩き去るowner」 | 所有者列が逐次グレーアウト走行 | カット尺 | Act2 7:10 | |
| F8 | CivilForfeitureInvert | 民事没収の逆転構造 | 有罪推定の反転 | バー継続回転＋下線帯左→右描画継続 | カット尺 | Act2 7:20 | |
| F9 | CoinFlip | 運任せの結末 | — | 着地後ぐらつき→平落ち→0.5s以内whip遷移 | カット尺 | Act2 8:05 | |
| F10 | HeadlineKinetic | NYT一面見出し | NYT 2014-10-25一面(CLM-0007・直接引用可) | 見出し一語ずつzoompunch＋紙面奥へ連続後退トラベル | カット尺 | Act3 8:35 | |
| F11 | **PolicyReversalTimeline** | 方針転換タイムライン＋"WITHOUT PREJUDICE"常時ノード | 2014方針転換・without prejudice(L2) | プレイヘッド常時右滑走(サブROI局所flow≥5%/幅秒)＋"WITHOUT PREJUDICE"をAct4通し表示 | 走査完了≤カット尺 | Act3 9:30→12:40→18:15 | ★ |
| F12 | SeizureVsReturn | 押収と返還の対比 | 押収→返還 | 両側slide-in中央衝突→両束が実押込±10px継続 | カット尺 | Act3 10:20 | |
| F13 | DismissedStamp | without prejudice却下印 | "DISMISSED WITHOUT PREJUDICE" | 二語zoompunch着弾→下線帯左→右描画トラベル継続 | カット尺 | Act3 11:30 | |
| F14 | **McLellanParallel** | Iowa/NC 二事例の並置 | Carole vs McLellan・同一法 | 左Iowa/右NC横開き＋両景パララックス＋F11遠景赤マーカー右進行 | 横開き0–24f | Act4 12:20 | ★ |
| F14b | **McLellanLedger** | McLellan 入金台帳 | 301入金・~$2M・3年(CLM-0012) | 301入金逐次点灯＋累計~$2Mカウントアップ走行＋年ラベル横スクロール | 点灯stagger4f/カウント0–90f | Act4 12:55 | ★ |
| F14c | **McLellanStore**(新設) | 田舎コンビニ＝小額取引の店 | 給油/煙草/宝くじ・小額 | 店内奥→手前ドリー＋レジ小額連続点灯 | カット尺 | Act4 13:45 | |
| F15 | **TIGTA-Dots** | TIGTAサンプルの合法原資比 | 278サンプル・91%(件数比)(CLM-0014) | 278ドット組成→91%が緑へ波状逐次反転トラベル→完了後スローパララックス | 組成0–40f/波反転40–90f stagger2f | Act4 14:30 | ★ |
| F15b | LegalSourceBars | 合法原資没収の総額 | 231件・$17.1M(CLM-0014) | 231件$17.1M横棒実伸長→到達後カウンタ微走行＋0.5s以内push | カット尺 | Act4 15:05 | |
| F16 | FeeDeniedCard | 弁護士費用否認 | 2016 8th Cir. fee否認(CLM-0011) | 宙吊りカード着地→半緑/半グレー境界線左→右描画継続 | カット尺 | Act5 15:55 | |
| F17 | ThreatReframeCard | 「まだ法は生きている」脅威再フック | "STILL ON THE BOOKS" | パネル＋二人称脅威＋背景制度スパイン奥スロードリフト | カット尺 | Act5 16:10 | |
| F17b | FeeContrastCard | McLellan/Carole 費用対比（L5回収） | McLellan"FEES PAID"／Carole"FEES DENIED" | 対比二段＋両段充填バー左→右伸長 | カット尺 | Act5 17:20 | |
| F18 | CongressHearingCard | 公聴会（逐語引用出さない） | 2015公聴会(CLM-0020 grade B・本人証言禁止) | 公聴会室・証人席・無人シルエット＋書類実捲れトラベル継続 | カット尺 | Act5 17:40 | |
| F19 | RESPECTActNode | RESPECT Act最終ノード（射程限定） | 2019 RESPECT Act(CLM-0016)・金点灯 | Timeline最終ノード金点灯＋スパイン左→右確定走査＋金グロー=1回減衰パルスのみ | 走査（サブROI） | Act5 18:15 | |
| F20 | **CaroleAfterCard** | 店の売却後（L4回収） | Mrs.Lady's売却・"SOLD"札 | 空店内奥→手前ドリー＋"SOLD"札着地＋店内ドリートラベル継続 | ドリー0–72f/札λ0.75 Trail | Act5 18:50 | ★ |
| F21 | InfoDensitySpine | ED橋渡し（次回ループへ） | 次回オープンループ | プレイヘッド走査トラベル→end-card | カット尺 | ED 19:40 | |

**内部整合（設計確定値）**: 図数=**27**、ヒーロー=**8**。幕別新規図: Act1=5 / Act2=6 / Act3=4 / Act4=5 / Act5=6（全幕≥3）。新規hero幕別: Act1=F2,F3 / Act2=F5 / Act3=F11 / Act4=F14,F14b,F15 / Act5=F20（全幕≥1）。**全隣接ペアのリビール間隔≤90s**（F2b/F5b/F14c 新設で解消済）。✔は手計算でなく `check_figure_cadence` 実出力を貼る。

---

## 2. 深度マップ（DepthImageV / dpt-large）が必要な画像 — §3.0 / §3.7 / §10

設計は**個別 S0NN 画像ID→depth の一覧を列挙していない**（捏造しない）。深度計画は「集合＋カット数＋分類ルール」で定義される。

- **depth適用対象の定義**: 「depth処理カット」＝ **DepthImageV(dpt-large深度マップ)を適用する単独画像カットのみ**。
- **総数=239カット（＝全528カットの45%）**。内訳（§3.7 Act別加重の総和）:

| 区間 | カット | depth% | depthカット数 |
|---|---|---|---|
| HOOK | 4 | 25% | 1 |
| OP | 4 | 25% | 1 |
| Act1 | 100 | 46% | 46 |
| Act2 | 116 | 48% | 56 |
| Act3 | 88 | 50% | 44 |
| Act4 | 100 | 45% | 45 |
| Act5 | 106 | 42% | 45 |
| ED | 10 | 20% | 2 |
| **計** | **528** | **45%** | **239** |

- **元画像プール**: 単独露出の生成静止画 **136 unique**（現行 ai_prompts v001 は S001–S068＝62枚 → **v002で≥136へ拡張要件**）。239 depthカットは 324 単独画像placement のうち 239（=74%）＝「image-cut の depth必須カバレッジ≥70%」を満たす同一集合。
- **深度生成手順**: 各画像の隣に `<name>_depth.png` を `tools/depth/gen_depth.py`（`Intel/dpt-large`・near=bright・0-255正規化・GaussianBlur(2)）で生成。Remotion側は subdivided plane を深度マップで変位→camera dolly-in で**実パララックス**。
- **重要な区別**: **図 F1–F21（204カット）は depth✔だが DepthImageV適用ではなく L3 near/mid/far 層パララックスで別機構**。239には非算入。
- **depthパララックス数値（239カット・§3.1）**: near 24–28px / mid 14–18px / far 6–8px、Easing.out(cubic)、L3全体 scale 1.03→1.08。
- **連続depth画像の上限**: depth画像カットのみ**連続≤12s**（超える前に図/実写差替静止画/キネティック字幕を差込む）。
- **各depth画像カットは追加の構造モーション必須**: 前景プレーンの実移動 / 走行光 / 図オーバレイのいずれか1つ以上で被覆率床（ROI≥25%画素が≥4.0%/幅・秒≈77px/s）を満たす。ken-burns単独では未達＝FAIL。

---

## 3. ヒーロー面（大きく動く見せ場）8つ — §3.0 / §3.6

| # | ヒーロー図 | 幕 | 主要モーション（設計§3.6数値） | 超激重写像(§SH) |
|---|---|---|---|---|
| 1 | **F2 BSAOriginFlow** | Act1 1:20 | 流下0–48f Easing.out(cubic)＋滴下 λ0.9 Trail＋far 8px/s | Blender **Mantaflow 3D流体シム**（新規） |
| 2 | **F3 ThresholdMeter** | Act1 3:05 | 積上げ0–60f stagger6f＋針Easing.inOut(quad)＋微光5%/幅秒 | **@remotion/three 実3Dゲージ**（新規） |
| 3 | **F5 FrozenAccount** | Act2 4:25 | 氷亀裂0–40f λ0.75 Trail＋near24/mid16/far6pxパララックス＋終端push8f | Blender **物理氷破断シム(rigid-body fracture)**（新規） |
| 4 | **F11 PolicyReversalTimeline** | Act3(9:30通し) | プレイヘッド局所flow≥5%/幅秒＋zoompunch λ0.9/10・走査完了≤カット尺 | **@remotion/three 3D空間タイムライン**（新規） |
| 5 | **F14 McLellanParallel** | Act4 12:20 | 横開き0–24f Easing.out(cubic)＋両景パララックス＋赤マーカーspring | **@remotion/three 3D並置**＋dpt-large二枚（新規） |
| 6 | **F14b McLellanLedger** | Act4 12:55 | 301入金stagger4f＋~$2Mカウント0–90f＋年ラベル局所5%/幅秒スクロール | **@remotion/three 3D台帳＋301点灯パーティクル**（新規） |
| 7 | **F15 TIGTA-Dots** | Act4 14:30 | 278ドット組成0–40f＋91%波反転40–90f stagger2f＋パララックス4%/幅秒 | Blender/three **278点群パーティクルシム**（新規） |
| 8 | **F20 CaroleAfterCard** | Act5 18:50 | 奥→手前ドリー0–72f Easing.out(cubic)＋"SOLD"札 λ0.75 Trail | Blender **Cycles ceiling 店内3D dolly**（新規） |

各ヒーロー図は**独立運動要素≥6を実体列挙**（設計§3.6実装決定論表に座標/値まで数値化済み）。超激重の数値負荷は§SHで確定。

---

## 4. 再利用MOTIONKIT部品（新規フルスクラッチ禁止・二重実装禁止） — §3.6実装決定論表

hero8図は下記の既存部品＋プリセットへ写像。残19図も**最寄りプリセット＋data props差分**で構成（CATALOG.md参照が前提）。超激重tierでは**この2D部品層の上に3D/Blenderヒーロー版を重ね**、2D版はフォールバック/合成レイヤーとして保持（extend, do not fork＝invariant14）。

| 図 | MOTIONKIT部品/プリセット | 超激重で追加する実3D/Blender層 |
|---|---|---|
| F2 | `FluidStreamFlow` ＋ `BranchDripV` | Blender Mantaflow液体シム連番（新規アセット） |
| F3 | `StackMeterV` ＋ `GaugeSweep` | @remotion/three 実3Dゲージ（新規） |
| F5 | `IceCrackPropagate` ＋ `DepthPlanes` | Blender rigid-body 氷破断シム（新規） |
| F11 | `PlayheadTrackV` ＋ `NodeLatch` | @remotion/three 3D空間タイムライン fly-through（新規） |
| F14 | `SplitCompareV` ＋ `DepthPlanes` | @remotion/three 3D並置＋dpt-large二面（新規） |
| F14b | `LedgerCountUp` ＋ `ScrollAxisV` | @remotion/three 301点灯パーティクル（新規） |
| F15 | `DotMatrixReveal` ＋ `WaveFlip` | Blender/three 278点群シム（新規） |
| F20 | `RoomDollyV` ＋ `SignLatch` | Blender Cycles ceiling 店内3D（新規） |
| depth全般 | `DepthImageV`（dpt-large深度マップ流用・実在slice1=`CaseFilm.tsx` DepthStill） | dpt-large 最大振幅化（§SH.4） |

MOTIONKITに完全一致部品が無い図は**最寄りプリセット＋data props差分**で作り、新規フルスクラッチを避ける。**Blenderヒーローアセット（fluid/ice-fracture/point-cloud/room-dolly）は既存部品に存在しない＝新規Blenderアセット（別スレ制作）**として§SHに明示。

---

## 5. トランジション規律（ForcefulCut 4種のみ） — §3.2

| 種別 | 尺 | 用途 | パラメータ | Trail |
|---|---|---|---|---|
| push | 8f | 幕・シーン移動 | 旧画面進行方向100%押出＋新押込・Easing.out(cubic) | λ0.75/8 |
| slide | 7f | 書類→書類 | 横100%・Easing.inOut(quad) | λ0.6 |
| zoompunch | 5f | 統計/見出し/図リビール | scale1.0→1.12→1.0＋縦ブラー | 必須 λ0.9/10 |
| whip | 4f | レーン切替 | 横ブラーwipe | 必須 λ1.0 |

**禁止事項（明示）**: 金縦スイープ / 周回淡光 / lissajous / 定位置グロー呼吸 / 明滅 — **すべて禁止**。
**§3.1装飾ループ撤去**: L0 SceneBed の±3%正弦呼吸→撤去（リビール駆動一方向スロードリフト or 静的）。L1テクスチャ6–10px/s往復ループ→撤去（イベント駆動一方向ドリフト・残す場合±1%以下）。L2グローはリビール時の1回減衰パルスのみ（呼吸ループ/明滅=禁止）。
**freeze整合**: 図の主要モーション完了後は (a)別種構造モーションをカット終端まで継続、または (b)完了から0.67s以内に必ずForcefulCut遷移。ROI連続40f(0.67s)静止を発生させない。「固定/静止一定」表記は全撤回。**超激重ヒーローの3D/物理シムはカット全長を実運動で埋めるため freeze発生の物理的余地なし。**

---

## 6. 数値予算サマリ — §3.0 / §3.7

| 指標 | 確定値 |
|---|---|
| 完成尺 | **20分**（19.5–20.5分＝1,170–1,230s・唯一のship-gate=`check_runtime_band.py`実TTS実測） |
| シーン数 | **38** |
| カット総数 | **528**（平均2.32s／カット） |
| depth処理カット比率 | **45%＝239カット**（DepthImageV適用の単独画像カットのみ） |
| 動くFigureBeats | **27図**（幕別新規≥3・新規hero全幕≥1） |
| ヒーロー面 | **8面**（F2/F3/F5/F11/F14/F14b/F15/F20・全て超激重tier対象） |
| 3レーン分離 | Iowa(暖アンバー)／Federal(冷スチール)／NC(冷緑)・EP33/34と素材/色/音を分離 |
| motion_energy(ROI) | within-shot平均≥16（≈0.83%/幅・秒）／p10≥11（≈0.57%/幅・秒）／全12s窓≥8・主役ROI限定測定 |
| 図ROIフロー | ROI内≥30%画素が≥3.5%/幅・秒（≈67px/s）以上 |
| depth画像フロー | depth ROI≥25%画素が≥4.0%/幅・秒（≈77px/s）以上 |
| 要素密度 | 各図 独立運動要素**≥6**（描画後 optical-flow クラスタ数＋実描画サブ要素数で実測・自己申告不可） |

---

## 7. 持続モーションの必須ルール（紙芝居フリーズ根絶） — §3.0 / §3.1 / §3.2 / §3.7

1. **motion_energy床（凍結禁止）**: 主役ROI/前景プレーン限定で within-shot≥16px/s・p10≥11px/s・全12s窓≥8。全カット12s窓で床を割らない。
2. **ROI連続フリーズ禁止**: 任意の図/主役ROIでフロー閾値未満が**連続40f(0.67s)超＝FAIL**。主要モーション完了後も別種構造モーション（パララックス継続 / プレイヘッド走行 / 下線帯左→右描画 / スローケンバーンズ）をカット終端まで継続。
3. **depth画像は必ず構造モーションを重畳**: 全depth画像カットに前景プレーン実移動 / 走行光 / 図オーバレイのいずれか1つ以上を必須（ken-burns単独＝未達FAIL）。連続depth画像は**≤12s**。
4. **平坦20秒ゼロ**: 全windowに構造モーション/実移動を敷設。主柱＝`check_padding`＋`check_motion_energy`、補助＝`check_image_pan_flow`／`check_freeze_frames`／`check_figure_flow`。
5. **周回光・呼吸ループ禁止**: SceneBed正弦呼吸・テクスチャ往復ループ・定位置グロー呼吸・明滅はすべて撤去/禁止。動きは**リビール駆動の一方向**か**イベント駆動**のみ。
6. **黒画面ゼロ**: `footage_utilization` で 136生成unique資産の各々が最終mp4に≥1回出現を強制。
7. **OP/EDも動かす（§9.1）**: OP(0:07–0:19)＝食堂ネオン点灯→連邦紋章にじみ→Title 3モーションビート（ロゴ静止禁止・motion窓≥8）。ED(19:45–20:24)＝暗い食堂ネオンが暖かく灯り直しend-card（連続グロー・F21走査）。**超激重ではOP背景を@remotion/three 実3D背景プレート＋Blenderヒーロー`OffthreadVideo`をhook冒頭（gold BrandOpening着地前）に配置**（§SH.6・row-9/10/14順序不変・invariant11=抽象生成・実在肖像なし）。

---

# §SH. 超激重（SUPER-HEAVY / L3 ceiling）制作tier — `PD_MOTION3D_HERO_AND_FIGURES_SPEC.md`準拠

> **品質ラダー（同spec §0・本Windows/RTXノード実測 2026-07-05）**: L0=2D板(避ける)／**L1 depth=@remotion/three(実奥行き・~real-time)**／**L2 hero fast=Blender EEVEE(~1.8s/frame)**／**L3 hero ceiling=Blender Cycles OptiX(~8s/frame @1080p)**。超激重は**ヒーロー8面をL3 ceiling or L1実3D or 物理シムへ全振り**、L3の"さらに上"（HDRI環境／ボリューメトリック／8K→1080p supersample）を許容範囲まで積む。**すべてのモーションは `useCurrentFrame()`/keyframe駆動＝決定論**（r3f `useFrame`禁止・非決定論でCodex再現性を壊す）。等速線形禁止（`spring{damping,mass}` or `Easing.out(Easing.cubic)`）。opacity単独リビール禁止（translateY/scale併用）。

## §SH.0 共通レンダ規律（超激重の負荷）
- **Blender 5.1 headless**: `blender -b -P <script.py> -- <OUT> <RX> <RY> <FS> <FE> <SAMPLES>`。`FS==FE`→テスト静止画、else→PNG連番 `<OUT>/f_0001.png…`（Blender5.xは動画出力削除＝**必ずPNG連番→別途encode**）。
- **Cycles GPU**: `OPTIX`→`CUDA`→`HIP`→`ONEAPI`の順で試行し全非CPUデバイス有効化、無ければCPU。`use_denoising=True`。`view_transform='AgX'`（映画的トーンマップ）。**caustics OFF固定**（ガラス＋causticsで一部フレームがレンダ時間爆発＝bloomで代替）。
- **物理シム**: rigid-body world `substeps_per_frame=20` / `solver_iterations=20`、friction0.35/restitution0.05、`ptcache.bake_all(bake=True)`後に `render(animation=True)`（**静止画レンダはシムが進まない＝必ずアニメレンダ**）。
- **encode（row-6 verbatim）**: `npx remotion ffmpeg -framerate 30 -i <OUT>/f_%04d.png -c:v libx264 -crf 16 -pix_fmt yuv420p -y hero.mp4`（bt709・音声はaac320kで本編mux時）。ヒーロー連番は**fps=30**。
- **本編統合**: `OffthreadVideo`でRemotionに取込。WebGL(@remotion/three)長尺は **`--concurrency=4`**（GPU競合回避）。CPU(libx264)固定・**NVENC切替禁止**。SSD(H:)/`runs/`はコミットしない。
- **決定論乱数**: seeded `mulberry32`（`Math.random`禁止）。フィルムグレイン=`feTurbulence`(seed=frame%N)・`mixBlendMode:overlay`・opacity0.05–0.09。ビネット=radial-gradient。

## §SH.1 ヒーロー超激重仕様（8面・数値負荷明記）

各ヒーローに［3D手法／サンプル数／解像度／カメラムーブ／物理シム／ボリューメトリック光／dpt-large最大振幅／パーティクル／モーションブラーサンプル／encode］を明記。**基準ソース = `bpp_cycles.py`（Cycles/OptiX/AgX/glass Transmission1.0・Roughness0.02・IOR1.85・Bevel0.025×3seg・softbox1.4/1.1/0.8・DOF f2.2・~8s/frame）／`bpp_physics.py`（rigid-body substeps20/solver20・WIND field strength95→0 frame1-18）／`bpp_eevee.py`（EEVEE taa96–192・~1.8s/frame）／`depth/depth.py`（dpt-large）**。

### F2 BSAOriginFlow ★ — 3D流体シム（**新規Blenderアセット**）
- **3D手法**: Blender **Mantaflow liquid(FLIP)** 流体シミュレーション。domain解像度 res=192（super-heavy・upres factor×2で有効384相当）、adaptive domain。汚れた資金が上流ドメインから小店ROIへ流下・分岐・滴下。**bpp_physics.pyのシム実行規律を流用**（bake_all→render animation）。
- **サンプル数**: Cycles ceiling **200 samples**＋denoise（`bpp_cycles.py`の160–200上限）。
- **解像度**: 3840×2160レンダ→1080pへ**supersample縮小**（L3"さらに上"・エイリアス除去）。
- **カメラムーブ**: 上流→小店へ 0–48f dolly＋わずかな見下ろしtilt（`bpp_cycles.py` cam location keyframe方式・Easing bezier default）。
- **物理シム**: FLIP液体＋viscosity低・spray/foam/bubbleセカンダリパーティクル有効。
- **ボリューメトリック光**: world volume薄霧＋key/rim area lightで流体に体積ゴッドレイ（softbox1.4/1.1/0.8）。
- **dpt-large最大振幅**: 背景プレートdepth変位 **最大±64px（near28→super-heavy拡張）**。
- **パーティクル**: spray/foam 最大~20k、滴下核 emissive。
- **モーションブラーサンプル**: `render.use_motion_blur=True`・shutter0.5・**motion blur steps=16**。
- **encode**: PNG連番→row-6（libx264 crf16 yuv420p・fps30）。

### F3 ThresholdMeter ★ — 実3Dゲージ（**@remotion/three 新規**）
- **3D手法**: `@remotion/three` `ThreeCanvas`。$10kゲージ＋入金ブロックを実3Dメッシュ化・camera実移動でパララックス自動。
- **サンプル数**: WebGL MSAA×8＋SSAO＋実時間DOF（L1・~real-time）。
- **解像度**: 1920×1080実レンダ（`--concurrency=4`）。
- **カメラムーブ**: ゲージ正面→斜め俯瞰 0–60f dolly（useCurrentFrame駆動・`Easing.out(cubic)`）。
- **物理シム**: 入金ブロック積上げに軽量擬似重力keyframe（stagger6f）。
- **ボリューメトリック光**: 3点ライト＋emissiveゲージ針のグローbloom（post feTurbulence grain）。
- **dpt-large最大振幅**: near札プレート±28px（層パララックス）。
- **パーティクル**: ゲージ完了時の微光スパーク~200。
- **モーションブラーサンプル**: `@remotion/motion-blur` Trail λ0.9（速い針動作のみ）。
- **encode**: Remotion本編に直接合成（本編fps60）。

### F5 FrozenAccount ★ — 物理氷破断シム（**新規Blenderアセット**）
- **3D手法**: Blender **rigid-body fracture（cell fracture）**。通帳/口座パネルを氷結晶化→亀裂連鎖伝播で破断。**`bpp_physics.py`の rigid-body world規律（substeps20/solver20/friction0.35/restitution0.05・WINDトリガ or falling core）を流用**。
- **サンプル数**: Cycles ceiling **200 samples**＋denoise。氷=glass（Transmission1.0/Roughness0.02/IOR1.85＋Bevel0.025×3seg＝エッジが光を拾う）。
- **解像度**: 3840×2160→1080p supersample。
- **カメラムーブ**: 通帳へ push-in 0–40f＋終端push8f遷移（cam location keyframe）。
- **物理シム**: cell fracture破片~120＋亀裂伝播。bake_all→render animation必須。
- **ボリューメトリック光**: 冷色rim＋softbox反射で氷内部散乱。AgX。
- **dpt-large最大振幅**: near通帳プレート±48px。
- **パーティクル**: 氷片飛散＋frost結晶パーティクル~5k。
- **モーションブラーサンプル**: motion blur steps=16・shutter0.5。
- **encode**: PNG連番→row-6→`OffthreadVideo`。

### F11 PolicyReversalTimeline ★ — 3D空間タイムライン（**@remotion/three 新規**）
- **3D手法**: `@remotion/three` 3D空間にタイムラインスパインを敷設・camera fly-throughでノード間を実移動。"WITHOUT PREJUDICE"を3Dパネルで常時ノード表示（Act4通し）。
- **サンプル数**: WebGL MSAA×8＋SSAO＋bloom。
- **解像度**: 1920×1080（`--concurrency=4`）。
- **カメラムーブ**: プレイヘッドに追従fly-through（局所flow≥5%/幅秒・走査完了≤カット尺・useCurrentFrame駆動）。
- **物理シム**: なし（decorativeパーティクルのみ）。
- **ボリューメトリック光**: スパイン奥ドリフト＋ノード点灯bloom（zoompunch λ0.9/10）。
- **dpt-large最大振幅**: 背景制度スパインプレート±32px。
- **パーティクル**: ノード点灯スパーク＋データフロー粒子~1k。
- **モーションブラーサンプル**: Trail λ0.9（マーカー右進行）。
- **encode**: 本編直接合成 or `OffthreadVideo`。

### F14 McLellanParallel ★ — 3D並置＋dpt-large二面（**@remotion/three 新規**）
- **3D手法**: `@remotion/three` `SplitCompareV`の3D版。左Iowa/右NCを2枚のdpt-large変位プレーンとして3D空間に配置・横開き＋両景独立パララックス。
- **サンプル数**: WebGL MSAA×8＋DOF。
- **解像度**: 1920×1080（`--concurrency=4`）。
- **カメラムーブ**: 横開き 0–24f `Easing.out(cubic)`＋中央境界線描画。
- **物理シム**: なし。
- **ボリューメトリック光**: F11遠景赤マーカー右進行のグロー（**等速線形禁止・spring駆動**）。
- **dpt-large最大振幅**: 左右プレート各±48px（二面同時変位）。
- **パーティクル**: 境界線走査スパーク~300。
- **モーションブラーサンプル**: Trail λ0.9（見出しzoompunch）。
- **encode**: 本編直接合成。

### F14b McLellanLedger ★ — 3D台帳＋301点灯パーティクル（**@remotion/three 新規**）
- **3D手法**: `@remotion/three` 3D台帳グリッド。**301入金を301個の実インスタンスメッシュ**として逐次点灯（大量点灯パーティクル）・累計~$2Mカウントアップ・年ラベル横スクロール（サブROI局所5%/幅秒）。
- **サンプル数**: WebGL MSAA×8＋instanced mesh（301描画・GPU負荷高）。
- **解像度**: 1920×1080（`--concurrency=4`）。
- **カメラムーブ**: 台帳俯瞰→スクロール追従 0–90f。
- **物理シム**: 点灯時の軽量パーティクルバースト。
- **ボリューメトリック光**: 各点灯セルのemissive bloom。
- **dpt-large最大振幅**: near伝票プレート±16px。
- **パーティクル**: **301点灯＋各点灯スパーク（計~9k粒子）**。
- **モーションブラーサンプル**: Trail λ0.6（スクロール）。
- **encode**: 本編直接合成 or `OffthreadVideo`。

### F15 TIGTA-Dots ★ — 278点群パーティクルシム（**新規Blender/three アセット**）
- **3D手法**: **278個の実3D点群**（Blenderパーティクル or `@remotion/three` instanced 278メッシュ）。組成→91%（253個）が緑へ波状逐次反転・残9%（25個）赤保持。**数値は設計§1.2の 278/91%/231件$17.1M を厳守（改変禁止）**。
- **サンプル数**: Blender版=Cycles 200 samples／three版=MSAA×8＋SSAO。
- **解像度**: 3840×2160→1080p（Blender版）／1920×1080（three版・`--concurrency=4`）。
- **カメラムーブ**: 点群正面→スローパララックス俯瞰（完了後・4%/幅秒）。
- **物理シム**: 点群組成に軽量attractorシム（波状反転 stagger2f）。
- **ボリューメトリック光**: 緑反転波のemissive伝播bloom。
- **dpt-large最大振幅**: 背景プレート±32px。
- **パーティクル**: **278主点＋波反転トレイル（計~3k）**。
- **モーションブラーサンプル**: motion blur steps=12（Blender版）／Trail λ0.9（three版）。
- **encode**: PNG連番→row-6 or 本編直接合成。

### F20 CaroleAfterCard ★ — Cycles ceiling 店内3D dolly（**新規Blenderアセット**）
- **3D手法**: Blender **Cycles ceiling** 空Mrs.Lady's店内を3D化・奥→手前 dolly＋"SOLD"札着地（L4回収）。**最上級の掴み1カット**（`bpp_cycles.py`のglass/softbox/DOF/AgX/bloom規律を店内マテリアルへ適用）。
- **サンプル数**: Cycles ceiling **200 samples**＋denoise（さらに上=HDRI環境光追加）。
- **解像度**: 3840×2160→1080p supersample。
- **カメラムーブ**: 奥→手前 dolly 0–72f `Easing.out(cubic)`（`bpp_cycles.py` cam keyframe方式）。
- **物理シム**: "SOLD"札落下＋埃/光条パーティクルドリフト。
- **ボリューメトリック光**: 窓からの体積ゴッドレイ＋softbox反射・AgX。
- **dpt-large最大振幅**: near椅子±24/mid窓±16/far通り±6px（層＋実3D併用）。
- **パーティクル**: 埃/光条スロードリフト~2k＋"SOLD"札 Trail λ0.75。
- **モーションブラーサンプル**: motion blur steps=16・shutter0.5。
- **encode**: PNG連番→row-6→`OffthreadVideo`。

## §SH.2 主要（非ヒーロー）図の格上げ方針
- F1/F6/F10/F14c/F17b/F18/F20系の**空間/店内/公聴会カード**は L1 `@remotion/three` 実3D深度（dpt-large変位プレーン＋camera dolly）へ格上げ（~real-time・`--concurrency=4`）。
- F4/F8/F12/F13/F16/F19の**印章/バー/下線帯**はMOTIONKIT 2D＋Trailモーションブラー維持（3D不要・ただしfreeze整合厳守）。
- 統計系F15b（231件$17.1M横棒）はF15点群と同レーンで3D棒グラフ化可（instanced mesh）。

## §SH.3 EEVEE(L2 fast)フォールバック
Cycles ceilingがレンダ時間で間に合わない場合のみ、章トランジション/2番手ヒーローを **EEVEE fast（`bpp_eevee.py`・taa_render_samples 96–192・use_raytracing/ssr/gtao・~1.8s/frame・aperture_fstop2.2・Glare Bloom）** へ降格（no silent cap＝降格は必ずログ）。**F2/F5/F20のceiling 3面は降格しない（最上級の掴み）。**

## §SH.4 dpt-large 深度 最大振幅化
- 全depth画像(239)の変位振幅を super-heavy 化: 標準near28px→**ヒーロー隣接カットで最大±64px**（`depth/depth.py`の0-255正規化マップ＋GaussianBlur(2)を subdivided plane に適用・camera dolly-inで実パララックス）。
- subdivided plane解像度を上げ（segments増）変位のジャギ回避。連続depth≤12s規律は不変。

## §SH.5 超激重レンダ負荷サマリ（実務見積り）
- **Cycles ceiling 3面(F2/F5/F20)**: 各~8s/frame@1080p（`bpp_cycles.py`実測）×supersample(3840→1080=約4倍画素)で**実効~30s/frame級**。100f/カット→約50分/カット×3＝**要GPU占有・1本ずつ直列**。
- **物理シム(F5氷破断/F2流体)**: bake（substeps20/solver20）＋render animation。bakeは別途時間。
- **@remotion/three 実3D(F3/F11/F14/F14b/F15)**: ~real-timeだが**`--concurrency=4`厳守**（GPU競合・instanced 301/278で負荷高）。
- **encode**: 全ヒーロー row-6（libx264 crf16 yuv420p bt709・fps30）→`OffthreadVideo`本編mux。
- **規律**: tailで隠さない・完走まで殺さない・1本ずつ直列（reference_remotion_render_ops）。再レンダ後 `audio_mix_sha256`＋freshness照合。

## §SH.6 OP/ED 超激重（§9.1＋spec §1）
- **OP(0:07–0:19)**: `@remotion/three` 実3D背景プレート（食堂ネオン3D点灯→連邦紋章にじみ）＋その前に**Blenderヒーロー`OffthreadVideo`をhook冒頭（gold BrandOpening着地前）**に配置（row-9/10/14順序不変）。Title=`overflow:hidden`+translateY マスク・1文字スタッガー≈0.045s・motion窓≥8・ロゴ静止禁止。Bookendsはタイトル層のまま（3Dは背景のみ＝invariant14）。
- **ED(19:45–20:24)**: 暗い食堂ネオンが暖かく灯り直しend-card（連続グロー・F21走査）。roar禁止・"That is next."語尾から1.8sフェード。**抽象生成3D＝実在肖像なし（invariant11）**。

---

## 8. 完成条件（超激重tierゲート・spec §4）
- `hero_present`（tier採用時必須）: hookウィンドウにヒーロープレート実在・`OffthreadVideo`（実レンダ・静止画でない）・1920×1080・crf≤17/yuv420p（row-6）。
- `figure_density`: explainer spanは主要claimブロック毎に≥1アニメ図・静止図holdは>2s禁止（row8 motion auditに合流）。
- 8面ヒーロー各の§SH.1数値（手法/サンプル/解像度/カメラ/物理/ボリューメトリック/dpt振幅/パーティクル/motion blur/encode）を満たさない＝rework。
- **未コードゲートは手動レビュー項目**（silent cap禁止＝ヒーロー時間都合skip時は必ずログ）。
- **事実数値（$32,820.56／$107,702.66／301／~$2M／278／91%／231件$17.1M／各CLM ID）は超激重化しても一切改変しない。**
