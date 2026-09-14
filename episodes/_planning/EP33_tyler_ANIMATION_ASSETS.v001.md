# EP33 動画素材マニフェスト（別スレ制作用・アニメ/モーション抽出）＋超激重(SUPER-HEAVY / L3 ceiling)制作tier

- **Episode:** EP33
- **slug:** tyler（PD-2026-033-tyler）
- **制作:** 別スレ（本設計書全体を読まずに、この重いアニメ素材だけを制作する担当向け）
- **binding:** `episodes/_planning/EP33_tyler_DESIGN.v001.md`
- **tier binding:** `docs/PD_MOTION3D_HERO_AND_FIGURES_SPEC.md`（L1 @remotion/three 実3D深度 / L2 Blender EEVEE fast hero / L3 Blender Cycles ceiling hero / encode row-6 / figures tier）
- **参照実在部品:** `remotion/prototypes/motion3d/`（`Opening3D.tsx`・`Figures.tsx`・`depth/DepthScene.tsx`＋`depth/depth.py`・`map/MapScene.tsx`＋`map/us_map.json`・`blender/bpp_cycles.py`・`blender/bpp_eevee.py`・`blender/bpp_physics.py`＋`PHYSICS_NOTES.md`）
- **基盤:** `fps=30 / 1920×1080`（`remotion/src/brand.ts`）／基盤コンポ=`CaseFilm.tsx`（`treatment:"depth"`=`DepthStill`実装済）／専用図=`remotion/src/components/tyler/`／再利用=`motionkit/`
- **オーナー指示(2026-07-08):** 「超激重にして」＝本マニフェストを最上位プレミアム重量級(L3 ceiling)へ格上げ。ヒーロー面6＋主要図を最重量級パイプライン（Blender Cycles ceiling render / @remotion/three 実3D）へ写像。
- **担当分担（pd-division-of-labor）:** 画像生成のみCodex。Remotionコンポーネント/Blenderアセット/校正はClaude。実在ツールキットに無いものは捏造せず「**新規Blenderアセット（別スレ制作）**」と明示する。
- **不変条件:** invariant11=生成3D映像は実在肖像なし・記録として提示しない。invariant14=`prototypes/motion3d/`を`remotion/src/components/`へ**拡張ポート**（fork禁止・owner-gated）。
- **注:** 本設計書はFigureBeatの「個別秒数」を独立列で持たない。配置はシーン帯（§3.4）とtcアンカー（§3.2/§5.4）で確定。**事実数値（CLM）は超激重化で変えない。モーション/レンダ仕様のみ超激重化する。**

---

## 1. 専用Remotion図コンポーネント（bespoke FigureBeats）全19種

**distinct実数=18種**（#19 郵便受けカウンタは#1 TaxDebtメーターの早期seedで同一コンポーネント。FigureBeat床は#19を#1へ畳んだ18種で充足）。★=ヒーロー面。カウント対象は「方向性の実運動を持つ図」＝リビール後ホールドのみのカードは除外。

### ★ヒーロー面6（Trail=@remotion/motion-blur, lag0.35, layers6）

| # | コンポーネント名 | 機能（何を見せる図か） | 入力データ（数値・claim） | モーション（リビール＋持続） | 尺/配置 | 使用シーン | ★hero |
|---|---|---|---|---|---|---|---|
| 1 | `tax_debt_meter`（TaxDebtメーター） | 未払税が債務総額へ膨張する様 | `$2,300`→`$15,000`（中間実額出さず・T5・CLM-0004） | リング枠→桁マウント→桁ロール、**1:50 slam**。持続=針オービット8–12px＋桁ロール継続 | T5 1:20登場/1:50 slam・Act1帯0:24–3:40 | S003–S009 | ★ |
| 2 | `EquityBar` | 債務/売却/余剰の三段対比 | `DEBT $15,000`→`SALE $40,000`→`SURPLUS $25,000`（T7・CLM-0004/0005） | 三連: 灰DEBT→緑SALEslam→赤SURPLUSslam＋Trail。**余剰$25,000は4:50初出し**。持続=減衰オシレーション8–10px | T7 4:50・Act2帯3:40–6:35 | S010–S016 | ★ |
| 3 | `EquityTheftTally`（全米ヒーローマップ・新規） | 全米home equity theftの規模＋集積 | `$780,000,000+`＋`Est. — Pacific Legal Foundation`（T11・CLM-0017） | 走行カウンタ＋全米ドット集積アニメ＋Trail。中盤7.5分のヒーロー空白解消。持続=ドット連続集積＋カウンタ加算 | T11 9:00・Act3帯6:35–10:20 | S017–S024 | ★ |
| 4 | `GovtArgumentCard`（崩壊・新規） | 郡の最強論が崩れる感情ペイオフ | 郡の余剰保持正当化論（OL4・CLM-0006関連） | 積層カード→**13:20に構造破断＋Trail＋zoompunch崩壊**。持続=崩壊粒子ドリフト＋残響振動 | 13:20・Act4帯10:20–14:20 | S025–S031 | ★ |
| 5 | `MagnaCartaScroll` | 余剰返還原則の800年の源流 | `…AND THE RESIDUE SHALL BE LEFT TO THE EXECUTORS…`（T15・Magna Carta 1215 ch.26・CLM-0014A逐語） | 巻物unfurl＋ラテン字stroke-trace→訳文TerminalType。**1215アイコン限定（Overplusは別チップ）**。持続=連続パララックス8–12px＋インクtrace進行 | T15 14:40・Act5帯14:20–19:00 | S032–S038 | ★ |
| 6 | `VoteTally`（9–0） | 全員一致判決の着弾 | `9–0`＋`598 U.S. 631`（T18・CLM-0010） | **~18:15初オンスクリーン化**。弁論進行で席が方向性充填→9席同時発火＋単一hard impact | T18 ~18:15・Act5帯 | S032–S038 | ★ |

### 動く図（残り13・各持続 bbox中央値≥8px実運動・カードは恒常キャリア指定）

| # | コンポーネント名 | 機能 | 入力データ（数値・claim） | モーション（リビール＋持続） | 配置tc | 使用シーン | ★ |
|---|---|---|---|---|---|---|---|
| 7 | `HomeSeizedIcon`／SEIZED札 | 家が差押えられる象徴 | `SEIZED`（T1） | zoompunch。赤札着弾 | T1 0:00・Act1 | S001・S003–S009 | — |
| 8 | `SurplusSplitDonut` | 余剰の分配先（元所有者ゼロ） | `COUNTY`／`TOWN`／`SCHOOL DISTRICT`（T8・CLM-0006）・**元所有者ウェッジ欠落** | DonutReveal。分配点灯 | T8 5:40・Act2 | S010–S016 | — |
| 9 | `StateMap`（保持側点灯／緑化） | 保持許容州→要求州への転回 | 保持側点灯=**PLF列挙12州**`Est.—PLF`／緑化側=required-return（T9 `AT LEAST A DOZEN STATES STILL ALLOWED IT`点灯12・T21 `36 states + federal…`or`A large majority…`） | seed点灯→18:40緑化ペイオフ | 9:00 seed／T9 11:20／T21 18:40 | S017–S024・S032–S038 | — |
| 10 | `FeltComparison` 92/8 | 債務が物件価値のごく一部だった体感 | `92% PAID`／`8% DEBT`＋`Est. — PLF`（T12・CLM-0018） | 恒常キャリア=加算カウンタ＋背景パララックス | T12 9:20・Act3 | S017–S024 | — |
| 11 | `CaseTimeline`（短/長） | 先例と本件の時系列 | `1215`·`1884`·`1980`·`2023`（T17・CLM-0015） | 恒常キャリア=呼吸プレイヘッド走行 | Act2短／T17 16:00 Act5長 | S010–S016・S032–S038 | — |
| 12 | `PropertyRedefine` | 財産権の定義書換 | `PROPERTY`→赤ペン取消（T13） | キネティック取消線 | T13 10:00 | S017–S024 | — |
| 13 | `QuoteCard` | Roberts/Gorsuch名言 | T19 `"…render unto Caesar what is Caesar's, but no more."`（CLM-0013）／T3' `"fines by any other name"`（CLM-0012） | 恒常キャリア=緩push＋背景パララックス | T19 18:30／T3' 18:50 | S032–S038 | — |
| 14 | `AuctionGavel` | 競売の象徴 | （画面テキストなし） | graphic-symbol ledgerで**別カウント**（汎用象徴 種類≤2・登場回数≤3・src命名にgavel等禁止） | Act2 | S010–S016 | — |
| 15 | `DoorPlacardStrip` | 二人称メッセージの札 | `NOT HER WINDOW — YOURS.`（T22） | 札着脱/リリース | T22 19:20・Act5/ED | S032–S040 | — |
| 16 | `OralArgQuestionTally`（新規） | 口頭弁論の質問往復 | 弁論の質問数（CLM-0009関連） | 恒常キャリア=席方向性充填 | 16:40・Act4 | S025–S031 | — |
| 17 | `SplitLadder`（新規） | 三審の上昇 | District→8th Cir→SCOTUS（CLM-0008） | 恒常キャリア=段上昇プレイヘッド。**11:15再フック** | 11:15・Act4 | S025–S031 | — |
| 18 | `HallEquityLadder`（新規） | Hall事件の収奪の段 | Hall宅`$1`移転→約`$308,000`転売→債務約`$22,600`（CLM-0021・**★裏取り後のみ金額焼込／未裏取りは金額を出さず匿名象徴の段のみ**） | 恒常キャリア=段展開＋数値ロール | Act3 | S017–S024 | — |
| 19 | 郵便受け物理カウンタ | Act1早期seed（=#1と同一コンポ） | `tax_debt_meter`のseed表示 | 物理カウンタ（#1へ畳む・distinct非算入） | Act1 | S003–S009 | — |

> **HallEquityLadder（#18）の金額グリフ焼込は`verify_onscreen_text`のグリフ照合対象**。CLM-0021がgrade-A化されるまで `$1`／`$308k`／`$22,600` の焼込をblock（T10ソースチップと同caveat）。

### 幕別アクティブFigureBeat床（各幕≥4・カード除外規則適用後）
Act1=5・Act2=4・Act3=4・Act4=4・Act5=5。カウント対象は方向性の実運動を持つ図のみ。リビール後ホールドのカードは非対象。時間分布床=各60秒窓にアクティブFigureBeat≥1、図間の最大無図区間≤60秒、リフレインstill連続露出≤25秒。冒頭4分（0:24–3:40）はmotion-reel必須収録区間。

---

## 2. 超激重（SUPER-HEAVY / L3 ceiling）制作tier ★本改稿の主眼★

### 2.0 品質ラダーと本話の格上げ方針
`PD_MOTION3D_HERO_AND_FIGURES_SPEC.md §0` の実測ラダー（本Windows/RTXノード, 2026-07-05）:

| Tier | Engine | フレーム時間(1080p) | 用途 |
|---|---|---|---|
| L0 baseline | Remotion 2D板 | 即時 | **避ける（紙芝居の主因）** |
| L1 depth | `@remotion/three`(WebGL) | ~実時間 | 実奥行き・パララックス・DOF風 |
| L2 hero(fast) | Blender **EEVEE** | **~1.8 s/frame** | 掴みヒーロー・章トランジション |
| L3 hero(ceiling) | Blender **Cycles**(OptiX GPU) | **~8 s/frame**（100f≈13分） | 最上級の掴み1カット |

**本話=超激重：ヒーロー面6は全て L3 Cycles ceiling（またはL1実3Dの重量版）へ格上げ。** L3の"さらに上"（4K→1080p supersample縮小 / HDRI環境 / ボリューメトリック / 高モーションブラーサンプル）を採る＝フレーム時間が延びる（下記は品質⇔時間のトレードオフをオーナー承認済み前提で最上位を選ぶ）。**主要支援図（CaseTimeline/StateMap/SplitLadder/HallEquityLadder/SurplusSplitDonut）は L2 EEVEE fast hero もしくは L1 @remotion/three 実3Dへ格上げ。** 残り図は L1 `DepthStillHi`（実3D displaced mesh）を既定にし、板の合成(L0)を使わない。

### 2.1 共通・超激重レンダ規格（全ヒーロー）
- **Blender 5.1 headless:** `blender -b -P <script.py> -- <OUT> <RX> <RY> <FS> <FE> <SAMPLES>`。`FS==FE`は`<OUT>_test.png`単発、以外はPNG連番`<OUT>/f_0001.png…`（Blender5.xはアプリ内FFMPEG動画出力を廃止→**必ずPNG連番→別工程エンコード**）。
- **超激重の基準解像度:** レンダ`RX×RY = 3840×2160`（4K）→ **1920×1080へ縮小＝スーパーサンプル（アンチエイリアス/微細反射の底上げ）**。1080p直レンダより重い＝超激重の中核。
- **Cycles device:** `OPTIX`→`CUDA`→`HIP`→`ONEAPI`の順で試行、非CPUデバイス全有効化、無ければCPU（`bpp_cycles.py`実装どおり）。`view_transform='AgX'`（映画的トーンマップ）。`use_denoising=True`。
- **caustics厳禁（locked）:** ガラス材質でcaustics ONにすると一部フレームがレンダ時間爆発（`bpp_cycles.py`注記）。`caustics_reflective=False / caustics_refractive=False`のまま。グロー供給はGlare(Bloom)。
- **モーションブラー:** `scene.render.use_motion_blur=True`、`motion_blur_shutter=0.5`（超激重ではモーションブラーサンプルをCyclesレンダサンプル数に相乗り＝サンプル192–256で滑らかな高速動作ブラー）。速い動き（slam/崩壊/着席）に必須。
- **ボリューメトリック光:** 逆光god-ray/薄靄は Principled Volume（`density≈0.015–0.03`）または World Volume で付与＝**プロトタイプに無い→新規Blenderアセット（別スレ制作）**。
- **Bloom:** Blender5.x compositor node group＋socket API（`Type='Bloom'`, `Quality='High'`, `Highlights Threshold=0.75–0.8`, `Strength=1.0`, `Size=0.8`）。`bpp_cycles.py`の`setup_bloom`を流用。
- **物理シム:** rigid-body/cloth/particleは**必ず`render(animation=True)`でアニメ全区間レンダ**（単発stillはシム未実行でフレーム1初期位置になる＝`PHYSICS_NOTES.md`の既知罠）。`rigidbody_world.substeps_per_frame=20 / solver_iterations=20`、`friction=0.35 / restitution=0.05`、ベイク`ptcache.bake_all`。
- **エンコード（row-6 verbatim）:** `npx remotion ffmpeg -framerate 30 -i <OUT>/f_%04d.png -c:v libx264 -crf 16 -pix_fmt yuv420p -y hero.mp4`（RemotionバンドルffmpegでOK・外部不要）。最終mux時 `bt709`／音声は本編側 `aac 320k`。hero clipは`fps=30`。
- **エピソード統合:** `hero.mp4`を`OffthreadVideo`として`BrandOpening`の裏（フック/コールドオープンのヒーロープレート、金色BrandOpening着地前）に配置。抽象生成映像＝invariant11充足。

### 2.2 ヒーロー面6 → 最重量級パイプライン写像

| # | ヒーロー | 3D手法(Engine) | サンプル数 | 解像度 | カメラムーブ | 物理シム | ボリューメトリック光 | dpt-large深度 | パーティクル | モーションブラー | encode |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **TaxDebtメーター** `tax_debt_meter` | **L3 Cycles**（3D押し出し数字＋被写界深度） | Cycles 192 | 3840×2160→1080p | slow dolly-in＋8°オービット。DOF `aperture_fstop=2.2`（メーター面フォーカス）／1:50 slamでレンズ微punch | なし | 薄靄god-ray（Volume density 0.02）＝**新規** | native 3D（深度マップ不要） | slam着弾スパーク少数＝**新規** | shutter0.5・サンプル相乗り | row-6 crf16/yuv420p |
| 2 | **EquityBar** | **L3 Cycles**（3D押し出しバー三連＋DOF rack focus） | Cycles 192 | 3840×2160→1080p | 三本のバー間をrack-focus dollyで移動。SURPLUS赤バー4:50着弾でレンズpunch | 任意: 余剰バーのsettleを軽rigid-body落下 | 冷色god-ray薄靄＝**新規** | native 3D | 赤SURPLUS slamで粉塵バースト＝**新規** | shutter0.5 | row-6 |
| 3 | **EquityTheftTally 全米マップ** | **L3 Cycles**（3D地形＋大量パーティクル集積）※基盤は`map/MapScene.tsx`(SVG・L1)を土台に3D化 | Cycles **200**（最重・粒子最多） | 3840×2160→1080p | 高空からの俯瞰スイープ降下（州が起伏で見える角度） | パーティクルシステム（rigid-bodyでない） | 地形上の大気靄＋光柱＝**新規** | native 3D（`map/us_map.json`公有地図ジオメトリを押し出し） | **家喪失1件=発光インスタンス1粒の集積・8,000+粒**（走行カウンタと同期・数はPLF `Est.`規模の視覚表現で事実断定しない）＝**新規** | shutter0.5 | row-6 |
| 4 | **GovtArgumentCard崩壊** | **L3 Cycles**（物理破断シム）※基盤`blender/bpp_physics.py`（rigid-body崩落＋WINDフォースフィールド） | Cycles 160（物理多フレーム→時間制御） | 3840×2160→1080p | ワイド固定＋微push。13:20構造破断で寄り | **rigid-body**: 積層カードスラブをWIND(strength 95→0, frame1–18)で突き倒す。substeps20/solver20・friction0.35/restitution0.05・`bake_all`＋`render(animation=True)`。多片破断はCell Fracture＝**新規** | 崩落の粉塵ボリューム＝**新規** | native 3D | 破片デブリ＋粉塵パーティクル＝**新規** | **shutter0.5必須**（高速崩壊のブレ） | row-6 |
| 5 | **MagnaCartaScroll** | **L3 Cycles**（物理布/巻物シム）＝**プロトタイプ無し→新規Blenderアセット（別スレ制作）** | Cycles 192 | 3840×2160→1080p | 展開する巻物に沿うslow dolly＋インクtrace進行 | **cloth sim**: 平面にpin group＋gravity＋弱wind で巻物unfurl。羊皮紙材質（半透過/SSS） | 暖色の埃立つ光柱（god ray）＝**新規** | native 3D | 舞う埃モート＝**新規** | shutter0.5 | row-6 |
| 6 | **VoteTally 9–0** | **L3 Cycles**（3D着席）＝**プロトタイプ無し→新規Blenderアセット（別スレ制作）** | Cycles 192 | 3840×2160→1080p | 法廷ベンチを横切るdolly reveal→9席方向性充填→~18:15で9席同時発火＋単一hard impactでスナップ寄り | 任意: 着弾リップル軽シム | 法廷の斜光柱（god ray）＝**新規** | native 3D | 同時発火フラッシュのスパーク＝**新規** | shutter0.5 | row-6 |

**フォールバック規律:** GPU/時間制約でL3が不可なら **L2 EEVEE fast hero**（`bpp_eevee.py`・taa 96–192・~1.8s/frame）へ一段降格し、降格を**silent capにしない＝ログ必須**（spec §4 rule17）。L0板合成へは落とさない。

### 2.3 主要支援図の格上げ（L2 EEVEE / L1 実3D）
- **`EquityTheftTally`以外の地図系（`StateMap`）:** `map/MapScene.tsx`の実3D/アニメ地図（州スタッガー描画・都市ピン波紋・資金ルート弧＋走行光点）を土台に L1 @remotion/three＋Trail。公有`us_map.json`。
- **`CaseTimeline`・`SplitLadder`・`HallEquityLadder`・`SurplusSplitDonut`:** L2 EEVEE fast hero（発光ジェム/押し出し＋Bloom＋反射床＋DOF）か、`Figures.tsx`（`StatCounter/Timeline/BarChart/NetworkDiagram`）の実装を`DiagramFlow.tsx`へ拡張ポート（invariant14・並行実装禁止）。
- **深度stills（238カット）:** L1 `DepthStillHi`＝`depth/DepthScene.tsx`の`@remotion/three`実displaced mesh（`<name>_depth.png`変位）。板の擬似bleedは使わない。

### 2.4 超激重レンダ負荷とレンダ規律（追加分）
- **フレーム時間の見積り接地（spec §0実測）:** L3 Cycles=~8s/frame @1080p（100f≈13分）。**超激重の4K→1080p supersample＋ボリューメトリック＋モーションブラーサンプル増は、この8s/frameを数倍に押し上げる**（正確な総時間は捏造しない。ヒーロー6本×各~100–200fを、この係数で見積り直してから着手）。物理シム(#4崩壊)はベイク＋全区間アニメレンダで更に重い。
- **Blenderレンダは1本ずつ直列・GPU OptiX・完走までkillしない**（`tail`で進捗を隠さない・健全性はGPU使用率とフレーム進行）。PNG連番は必ず別工程エンコード。
- **Remotion側の実3D/深度（L1 @remotion/three・`DepthStillHi`・`MapScene`3D）は`--concurrency=4`**（長尺WebGL/depthの既定）。CPU libx264・NVENC不使用（quality-first）。
- **決定論:** 全モーションは`useCurrentFrame()`駆動（r3f`useFrame`禁止＝非決定・Codex再現性破壊）。乱数は`mulberry32`シード（`Math.random`禁止）。Blenderのfcurve補間はデフォルトbezier（等速線形禁止に自動適合）。
- **motion-reel（§6.3）は超激重でも必須:** 全19図＋各ヒーローの実尺レンダ動画＋非hero無作為抽出をオーナー提示。静止コンタクトシートだけで「紙芝居でない」宣言は禁止。
- **新規Blenderアセット（別スレ制作の要作成物）:** #3 3D地形+8,000+粒子集積／#4 Cell Fracture多片破断+粉塵／#5 巻物cloth sim（羊皮紙）／#6 法廷ベンチ9席着席／全ヒーローのボリューメトリック光柱・god ray。これらは`prototypes/motion3d/`に**未実在**＝新規作成物として明示追跡（EP33出荷の別ワークストリーム）。既存流用は #1/#2（`bpp_cycles.py`押し出し＋DOF）・#4基盤（`bpp_physics.py`）・#3基盤（`MapScene.tsx`）・深度（`DepthScene.tsx`+`depth.py`）。

---

## 3. 深度マップが必要な画像ID一覧（§3.5 depth計画）

**設計書はper-imageのdepth対象を`image_id`単位で列挙していない**（68行のper-image台帳=`asset_selection.v001.json`が正典で、生成前に別途作成・validate）。捏造せず、depth付与の「対象範囲と規則」を示す。

- **分母=全カット539／閾値=≥40%／本話=238/539=44.2%（余裕4.2pt）。**
- **depth付与対象=再現/静止stills 252カットのうち238カット（still比94.4%）。** これらstillsは**Codex画像68枚**から引く（平均~3.7 cut/image）。
- **depth対象外（深度を付けない）:** グラフィック図222カット（合成2Dデータ図・dpt-large深度なし）／実写footage 65カット（深度なし）。graphicsへのdpt-large自動付与フォールバックは撤回（平坦合成に単眼深度はno-op/アーティファクト・分母ロジック矛盾）。奥行きが要るならレイヤ・パララックスとして明示定義し深度分母に算入しない。
- **残14 still（=252−238）:** Ken Burns/フラット扱い（depthなし）。POST-renderでdepthカットがフラット化し40%接近時は、この未depth slack stills（14枚）をdpt-large深度付与へ昇格して40%を割らせない（マージンはstills由来のみで再計算）。
- **深度パイプライン:** `tools/depth/gen_depth.py`（ComfyUI venv python, `Intel/dpt-large`）が`remotion/public/<ep>/`の各画像脇に`<name>_depth.png`を書く（near=bright・正規化→GaussianBlur）。
- **超激重の深度振幅（格上げ）:** 標準`DepthStill`=前後レイヤ差±(50–80)px・zoom1.0→1.06。**超激重`DepthStillHi`=最大振幅±(90–120)px・zoom1.0→1.10・高分割displaced mesh・カメラdolly-inで実パララックス最大化**（`depth/DepthScene.tsx`の`@remotion/three`実装）。板の擬似bleedは既定にしない。
- **レンダ制約:** 長尺WebGL/depthは`--concurrency=4`。
- **整合ゲート:** `build_case_film_assets.py`が計画JSONの`depth:true`実数を数え、内訳合計(238)と一致しない計画を出力前exit1。

> depth対象の具体`image_id`は`asset_selection.v001.json`（68行台帳・`image_id → scene/cut・subject・composition・act・再利用数`）で確定。主なdepth候補stills: 1999年風コンド外観・匿名高齢女性の窓辺（朝の光リフレイン複数）・空き部屋の郵便受け・senior community・Hennepin郡庁舎/競売・匿名弁護士(PLF長机)・Hall事件の匿名フィギュア・Southfield風の家と$1移転/$308k転売象徴・Runnymedeの草原・マグナカルタ巻物(1215)・後代英制定法象徴(Overplus・1215と別ビジュアル)・大理石法廷・全米各地の匿名の家々のドア(SEIZED札着脱)・StateMap下地。

---

## 4. ヒーロー面（大きく動く見せ場）一覧＝6面

時間分布床あり（≥1ヒーロー/≤6分・全幕ゼロ禁止・Act3/Act4にも配置）。全ヒーローTrail=@remotion/motion-blur, lag0.35, layers6。**超激重tierでは各ヒーローを§2.2の最重量級パイプラインで制作。**

1. **TaxDebtメーター（`tax_debt_meter`）** — Act1・1:50 slam。針オービット8–12px＋桁ロール。→ L3 Cycles 3D押し出し＋DOF。
2. **EquityBar** — Act2・4:50 余剰$25,000初出し。三連slam＋Trail、減衰オシレーション8–10px。→ L3 Cycles 3D押し出しバー＋rack focus。
3. **EquityTheftTally 全米ヒーローマップ** — Act3（hero昇格・中盤谷解消）。走行カウンタ＋ドット集積＋Trail。→ L3 Cycles 3D地形＋8,000+粒子集積。
4. **GovtArgumentCard崩壊** — Act4（heroTrail昇格）。13:20 構造破断＋zoompunch＋崩壊粒子ドリフト。→ L3 Cycles rigid-body破断シム。
5. **MagnaCartaScroll** — Act5。巻物unfurl＋stroke-trace、連続パララックス8–12px。→ L3 Cycles cloth sim巻物。
6. **VoteTally 9–0** — Act5・~18:15。9席同時発火＋単一hard impact。→ L3 Cycles 3D着席。

---

## 5. 再利用MOTIONKIT部品（二重実装禁止・§3.3）

**`motionkit/`から流用（新規実装しない）:**
`VoteTally`・`NumberTicker`・`DonutReveal`・`StackedProportion`・`RegionHighlightMap`/`StateMap`・`QuoteCard`・`KineticCaptions`・`TerminalType`・`ActTitle`・`LowerThird`/`CitationLowerThird`・`Atmospherics`・`DepthParticles`／`LightRays`／`AuroraField`／`GridWarp`。

**新規（`components/tyler/`に実装・上記に無いもののみ）:**
`OralArgQuestionTally`・`SplitLadder`・`GovtArgumentCard`・`HallEquityLadder`・`EquityTheftTally`（hero版）。

**プロトタイプ拡張ポート（invariant14・fork禁止・owner-gated）:**
`prototypes/motion3d/Figures.tsx`（`StatCounter/Timeline/BarChart/NetworkDiagram`）→`remotion/src/components/DiagramFlow.tsx`の新variantとしてマージ。`Opening3D.tsx`／`depth/DepthScene.tsx`／`map/MapScene.tsx`→`remotion/src/components/`へポート。Blender`bpp_cycles.py`／`bpp_eevee.py`／`bpp_physics.py`はhero連番生成に流用し、新規アセット（§2.4）を追加。

---

## 6. トランジション規律（§3.8・超激重でも不変）

- **全40シーン境界＝`ForcefulCut`（push / slide / zoompunch / whip）。** 図内slamはzoompunch。
- **禁止事項:**
  - `WipeTransition`（**金縦スイープ**）禁止。
  - 既定crossfade禁止。
  - **周回/lissajous淡い光・単調等速グローを単独モーション源にすること禁止。**
  - 下部暗化スクリム（黒グラデ帯/半透明黒板）禁止（可読性はアウトライン＋ドロップシャドウ＋発光グローのみ）。
- `AuroraField`／`LightRays`はL0/L1ベッド限定（blend=screen/additive固定）。単独モーション源にしない。
- 各シーンに正の方向性モーション（パララックス/プレイヘッド/カウンタ加算/バーセトリング）を**1つ以上**。
- 遷移SFXは転換種別ごと≥4系統×各2ピッチ=8ファイル以上に分割し境界ごとローテーション（連続同一≤2回・単一使用≤全SFXイベントの15%）。

---

## 7. 数値予算サマリ（§3.0/§3.4/§8）

| 指標 | 本話確定値 | 床（binding） |
|---|---|---|
| 完成尺 | 1,200s（20:00） | 1,170–1,230s（19.5–20.5分・`check_runtime_band`実測が唯一合否） |
| シーン数 | 40 | 34–40 |
| 総カット | 539 | ≥450 |
| 平均カット長 | 2.23s | ≈2.3s（2.0–2.6s） |
| depth処理率 | 44.2%（238/539・分母=全カット） | ≥40%（余裕4.2pt） |
| 動くFigureBeats | 19種（distinct 18） | ≥10・各幕アクティブ≥4 |
| ヒーロー面 | 6（超激重: 全て L3 Cycles ceiling / 実3D） | ≥3・時間分布床（≥1/≤6分・全幕ゼロ禁止） |
| カット構成 | stills 252（depth 238）／graphics 222／footage 65 | フラット2D Ken Burnsのみ≤8%（≤43） |
| Codex画像 | 68枚（±4・全4K 3840×2160） | 幕別 Act1~13/Act2~10/Act3~16/Act4~9/Act5~15/Hook+OP+ED~5 |
| 字幕枚数 | 460–500枚 | — |
| 転換 | ForcefulCut（push/slide/zoompunch/whip） | 金縦スイープ・既定crossfade禁止 |
| 単一フレーム完全ホールド | ゼロ | — |
| **超激重hero render解像度** | **4K(3840×2160)→1080p supersample** | L0板合成禁止 |
| **超激重hero engine** | **Blender Cycles OptiX / @remotion/three** | フォールバック=L2 EEVEE（ログ必須・silent cap禁止） |

---

## 8. 持続モーションの必須ルール（紙芝居フリーズ根絶・§3.2/§3.8/§6.3）

- **サブピクセル呼吸は撤回。** 各図に方向性の実運動（パララックス／プレイヘッド走行／カウンタ加算／バーセトリング）を持たせる。
- **持続px床（advisory目標）:** 全図の持続実運動 **≥8px/frame**、ヒーロー図は8–12px。
- **motion_energy床（hard・配線済SOLIDゲートの引上げ再校正）:**
  - **still-p10 ≥ 17**（=⌈0.35×46.6⌉・基準アンカー MotionSample≈46.6[良]/紙芝居≈3.5[悪]）。DepthStillが17未達なら`DepthStillHi`で17達成まで振幅/zoom引上げ（**床を下げてstillsを認証しない**）。
  - **全体分布 median ≥ 18**、**12秒窓ごとの実フロー中央値 ≥ 8**。
  - within-shot=カット±8フレーム除外（切替スパイクの誤合格封鎖）。
  - 台帳の実床は within-shot≥12／p10≥9。本話はその引上げ再校正。
- **motion-variety（motion_energyの補助指標）:** ショット内フローの方向ヒストグラム・エントロピー≥1.5bit かつ 時間軸フロー大きさのCV≥0.25。
- **時間分布床:** 各60秒窓にアクティブFigureBeat≥1、無図区間≤60秒、リフレインstill連続露出≤25秒（間に必ず方向性モーションのある図/実写を挟む）。冒頭4分（0:24–3:40）はmotion-reel必須収録。
- **周回淡い光禁止・単調等速グロー単独禁止**（AuroraField/LightRaysはL0/L1ベッド限定・screen）。VoteTally薄暗ホールドは撤廃。
- **リビール後ホールドのみのカードはアクティブFigureBeat床のカウント対象から除外。** カードは恒常キャリア（緩push＋背景パララックス／プレイヘッド走行等）を必ず指定。
- **超激重tierの持続保証:** ヒーローはBlender/実3Dの実カメラムーブ＋物理シム＋パーティクル走行＝構造的に等速線形にならない（Blender fcurveデフォルトbezier / spring駆動）。motion_energyの見ごたえ目標を余裕で満たすが、**hard保証の所在は不変**＝`motion_energy`（上記校正）＋§6.3 motion-reel人間承認。per-figure bbox-localフローはadvisory参考のみ（旧`check_motion_bbox_flow`はドロップ済・引用禁止）。
