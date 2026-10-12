# EP34 動画素材マニフェスト（別スレ制作用）— 超激重（SUPER-HEAVY / L3 ceiling）tier

- **Episode**: EP34
- **slug**: rolin（PD-2026-034-rolin）
- **制作**: 別スレ（本マニフェストだけで自己完結・本文全文の再読不要）
- **binding**: `episodes/_planning/EP34_rolin_DESIGN.v001.md`（数値・機構の最終正典。矛盾時は設計書§番号を確認）
- **tier binding**: `docs/PD_MOTION3D_HERO_AND_FIGURES_SPEC.md`（L1 @remotion/three 実3D深度 / L2 Blender EEVEE fast hero / L3 Blender Cycles ceiling hero / encode row-6）＋prototype実装 `remotion/prototypes/motion3d/`（`Opening3D.tsx`・`Figures.tsx`・`blender/bpp_cycles.py`・`blender/bpp_eevee.py`・`blender/bpp_physics.py`・`depth/DepthScene.tsx`・`depth/depth.py`・`map/MapScene.tsx`・`audio/AudioReactive.tsx`）
- **オーナー指示（2026-07-08）**: 「超激重にして」。本マニフェストは**最上位のプレミアム重量級（SUPER-HEAVY / L3 ceiling）tier**。ヒーロー面5つ＋主要図を最重量級（Blender Cycles ceiling render または `@remotion/three` 実3D）へ写像する。
- **合成fps**: 60fps 単一 / durationInFrames=72,000（=1,200s）/ 全時刻は「秒」規定（frame=秒×60）
- **実装分担**: TSX部品・図データ・ゲート・**Blenderアセット/シーンスクリプトは Claude が実装**。Codex は画像68枚のみ（SDXL勝手起動禁止）。
- **図データファイル**: `remotion/src/data/rolin_film.json`（cuts治療/画像/footage・figures・per-shot予測flowタグ＋併走モーション種別＋ロワーサード/テロップbbox・秒表記）。deterministic（`useCurrentFrame`）・BRANDトークンのみ。
- **注記**: 設計書は図の位置を「幕/秒」で管理し、個別S0NNのIDは割当てていない。本表は設計書どおり「幕/時刻(秒)」で参照する（S0NNは捏造しない）。事実数値は捏造しない。モーション/レンダ仕様は超激重化してよい。

---

## 0. 超激重（SUPER-HEAVY / L3 ceiling）制作tier — 総則

**モーション品質ラダー（`PD_MOTION3D_HERO_AND_FIGURES_SPEC.md` §0・本ノード RTX 実測）**:

| tier | エンジン | 見え | レンダコスト(1080p) | 本話での用途 |
|---|---|---|---|---|
| L0 | Remotion 2D板 | 紙芝居の主因 | 即時 | **禁止** |
| L1 depth | `@remotion/three`（WebGL）実3D | 本物の奥行き・パララックス・DOF風 | ほぼリアルタイム | depth再現スチルの3D dolly・タイトル奥行き |
| L2 hero(fast) | Blender **EEVEE** | 発光/ブルーム/反射床/DOF | ~1.8 s/frame | 章トランジション・補助ヒーロー |
| **L3 hero(ceiling)** | Blender **Cycles**(OptiX GPU) | 本物のガラス屈折・ベベル・GI | **~8 s/frame** | **最上級の掴み（本tierのヒーロー主砲）** |

**本tierの写像方針**:
- **ヒーロー面5つ**（#1 CashStack / #2 AirportCheckpoint / #8 BurdenFlipScale / #15 HardshipStill / #19 ReturnHands）＝**L3 Cycles ceiling render** または **L1 `@remotion/three` 実3D** の最重量級で制作。数だけの水増しでなく、§3の占有≥45%・尺≥12sを実測で満たす。
- **主要図**（#12-14 USForfeitureNumber・#4 CheckpointConvergeMap・#11 PinDropMap・#23 DHSAirportRecur）＝3D数値/3Dマップ＋パーティクルへ格上げ。
- **CLAUDE invariant 14（二重実装禁止）**: 本tierは既存 `CaseFilm.tsx` の `depth` treatment・`FigureBeats.tsx`・`ForcefulCut.tsx`・Bookends を**置換せず、その上に天井を足す**。L3 Blenderヒーローは `hero.mp4` を PNG連番→encode→`OffthreadVideo` として既存合成へ差し込む（生成ビジュアル＝invariant 11満たす・実在肖像なし・記録として提示しない）。

**共通レンダ規約（row-6 準拠・超激重）**:
- Blender 5.1 headless: `blender -b -P <script.py> -- <OUT> <RX> <RY> <FS> <FE> <SAMPLES>`。`FS==FE`→単一テストstill、`FS<FE`→PNG連番 `f_0001.png…`（Blender 5.xはアプリ内動画出力廃止＝**必ずPNG連番→別encode**）。
- **超激重の解像度アップリフト**: ヒーローは**3840×2160（4K）でレンダ**（本話は4K納品）。frame時間は1080p比 約4×（L3で ~30 s/frame級）。品質⇔時間は本tierで時間側を許容。
- **超激重のfpsアップリフト**: 60fps合成に対しジャダー回避のためヒーローPNG連番も**60fpsでレンダ**（spec既定30fpsからフレーム数2倍・レンダ時間2倍）。encode時 `-framerate 60`。
- Cycles: `cycles.samples` 本tierは **200（天井・spec範囲160-200の上端）**、`use_denoising=True`、`view_transform='AgX'`、GPU=OptiX→CUDA→HIP→ONEAPI→CPU、**caustics OFF維持**（ガラスでframe爆発を防ぐ・prototype注記）。
- **モーションブラー**: Cyclesは `render.use_motion_blur=True`・shutter 0.5・rolling shutter off。L1(@remotion/three)側の速い動きは `@remotion/motion-blur` `Trail`（AbsoluteFillをラップ・inline flex rowを直接ラップ禁止＝glyph崩れ）。ブラーサンプルはCyclesのサンプル数(200)に内包。
- **encode（row-6 verbatim）**: `npx remotion ffmpeg -framerate 60 -i <OUT>/f_%04d.png -c:v libx264 -crf 16 -pix_fmt yuv420p -y hero.mp4`（bt709 / 音声 aac 320k は本編mux時）。
- **レンダ負荷/規律**: WebGL depth（L1）併用のため長尺本編は `--concurrency=4`。Blenderヒーロー（L2/L3）は**本編とは別プロセス・別スレで先行連番レンダ**（GPU占有・OptiX）。1本ずつ直列・tailで進捗を隠さない・完走まで殺さない。健全性=headless chrome数とCPU/GPU。CPU（libx264）・クオリティ最優先（NVENC切替えない）。
- **決定論**: 全モーションは `useCurrentFrame()`（r3f `useFrame` 禁止）／Blenderは frame keyframe＋bake。乱数は seeded `mulberry32`（`Math.random` 禁止）。

**新規Blenderアセット（別スレ制作・prototype無しは明示）**: 下表「3D手法」列で `【新規Blenderアセット】` と明記した図は、`bpp_cycles.py`/`bpp_eevee.py`/`bpp_physics.py` を土台に**新規シーンスクリプト**を書き起こす（gem showcaseの流用でなく題材固有のジオメトリ）。prototype流用可のものは `【prototype流用】` と明記。

---

## 0-bis. 超激重ヒーロー写像テーブル（数値明記）

| ヒーロー/図 | 3D手法 | サンプル | 解像度 | カメラムーブ | 物理シム | ボリューメトリック光 | dpt-large深度最大振幅 | パーティクル | モーションブラー | encode |
|---|---|---|---|---|---|---|---|---|---|---|
| **#1 CashStack** | 【新規Blenderアセット】L3 Cycles（3D帯封束＋被写界深度） | 200 | 3840×2160 | dolly-in（cam 55mm・DOF `aperture_fstop 2.2`・fs束→着地でフォーカス送り） | rigidbody（束が積上・軽い接触沈み込み・substeps 20/solver 20・restitution 0.05） | softbox 3枚(1.4/1.1/0.8)＋Glare Bloom(Strength1.0/Size0.8) | — | 舞う塵 seeded 30粒（additive） | Cycles shutter0.5（sample200内） | row-6 60fps |
| **#2 AirportCheckpoint** | 【新規Blenderアセット】L3 Cycles（3D空港セット＋ボリューメトリック＋群衆パーティクル） | 200 | 3840×2160 | truck+dolly（コンコースを抜ける・AgX） | — | **ボリューメトリック（Principled Volume world/spotの光条・空港天窓の光柱）**＋softbox | — | **群衆パーティクル（匿名シルエット・instanced・横流動）** | Cycles shutter0.5 | row-6 60fps |
| **#8 BurdenFlipScale** | 【新規Blenderアセット】L3 Cycles（**物理天秤シム**） | 200 | 3840×2160 | 寄り＋皿を追うDOF | **rigidbody天秤：皿へ質量投下→spring減衰振動で市民側→政府側へ傾く（substeps_per_frame 20・solver_iterations 20・point cache bake_all）** | softbox＋Glare Bloom | — | 落下する象徴質量（帯封束プロキシ） | Cycles shutter0.5 | row-6 60fps |
| **#15 HardshipStill** | L1 `@remotion/three`（**dpt-large 3D dolly 最大**）＋QuoteCard | — (WebGL) | 3840×2160合成 | DepthCam dolly-in **z=5.6→3.3**（`Easing.out(cubic)`・横スウェイ±0.22最小） | — | grade＋vignette＋accent影（DepthScene流用） | **displacementScale 最大 ≈0.9-1.1**（planeGeometry 6×4×360×240・overscan1.16） | DustField seeded 30粒 | `Trail`（AbsoluteFill） | 本編内直接 |
| **#19 ReturnHands** | L1 `@remotion/three`（dpt-large 3D dolly）＋束が手に戻る実移動 | — (WebGL) | 3840×2160合成 | dolly-in z=5.6→3.3（暖光は補助・主運動=束移動） | — | 暖色grade＋vignette | **displacementScale 高 ≈0.8-1.0** | DustField 30粒 | `Trail` | 本編内直接 |
| **#12-14 USForfeitureNumber×3** | 【新規Blenderアセット】L3 Cycles（3D押出数値＋パーティクル）または `@remotion/three` 3Dテキスト | 200 | 3840×2160 | 桁走行に合わせスロー寄り | — | Glare Bloom＋softbox | 間の人間ビートは L1 depth dolly併走 | **桁着地で現金パーティクル飛散（$209M/$3.2B/$68.8B）** | Cycles shutter0.5 | row-6 60fps |
| **#4 CheckpointConvergeMap** | 【新規Blenderアセット】L2 EEVEE 3Dマップ有向フロー | 96-192(taa) | 3840×2160 | 俯瞰スロー旋回 | — | EEVEE bloom(Glare) | — | **有向パーティクル（TSA→州警官→DEAが検問へ実移動）** | EEVEE TAA | row-6 60fps |
| **#11 PinDropMap 15空港** | 【prototype流用】`map/MapScene.tsx`（3D地図）＋L2 EEVEE補助 | 96-192(taa) | 3840×2160合成 | 緩慢パン→Pittsburgh寄り | — | glow | — | **流量ライン持続流動＋時差点灯パルス** | `Trail` | 本編内直接 |
| **#23 DHSAirportRecur** | L1 `@remotion/three`（Texas $800K再現depth）＋別トレイ移動 | — (WebGL) | 3840×2160合成 | dolly-in z=5.6→3.3 | — | grade＋vignette | **displacementScale 中 ≈0.6-0.8** | DustField 30粒 | `Trail` | 本編内直接 |

**L3 Cyclesヒーロー基準マテリアル/ライティング（`bpp_cycles.py` 準拠・題材へ差替）**: world 暗青グラデ(0.012,0.02,0.04)・reflective metallic floor(Metallic0.9/Roughness0.22)・3点area light(key1600/fill800/rim1300)＋off-camera softbox 3枚(1.4/1.1/0.8)・Glare(Bloom, Quality High, Highlights Threshold0.8, Strength1.0, Size0.8)。ガラス題材は Principled `Transmission Weight=1.0 / Roughness=0.02 / IOR=1.85` ＋ Bevel(width0.025/3segments)。**帯封束/天秤/数値は題材固有ジオメトリで新規作成**（gem流用禁止＝説明性優先）。

**輝度整合（超激重でも§4輝度床を割らない）**: AgX/Bloomは暗く沈みやすい。L3/L1ヒーローも合成後 **median YAVG≥48・per-cut≥48** を `image_cut_luma`（実装済SOLID）で実測。AgXトーンでmedian割れは softbox strength／emission／key energy を上げて是正（暗いまま出さない）。

---

## 1. 専用Remotion図コンポーネント（bespoke FigureBeats）全数

**FigureBeat定義**: 連続して動く実尺（1ビート≤25s）。微ドリフト/微振動/微パララックスは持続モーションに数えない。持続の定量下限＝リビール後も画面高≥2.5%/秒の実移動、または前景オブジェクトの明確な運動。**キネティック度床＝主要要素が画面高≥2.5%/秒で動く秒数がビート尺の≥60%**。走光/暖光を主運動にしたビートは分子外（主運動は必ず物体の実移動）。

**実キネティック分子＝23本**（#1-15, 17-23, 27）。**補助図（分子外）＝#16, #24-26**。「格上げ」列＝本超激重tierでの3D写像。

| # | コンポーネント名 | 機能（何を見せる図か） | 入力データ（数値・claim） | モーション（リビール＋持続） | 尺(s) | 幕/時刻 | ★hero | 超激重格上げ |
|---|---|---|---|---|---|---|---|---|
| 1 | **CashStack＋NumberTicker** | 帯封束の山＋確認済み金額の着地 | 「約82,000ドル」（丸め・確認済み値のみ着地／精密$82,373は焼込まない） | 束が下から積上→額着地後、束が画面高3%/秒でパララックス移動（走光は補助）。着地は0:20-0:28（0-30s窓内） | **12** | OP/13-25s | ★ | L3 Cycles 3D帯封束＋DOF＋rigidbody |
| 2 | **AirportCheckpoint**（Codex再現depth） | 空港検問の再現 | Pittsburgh空港・押収現場 | depth dolly＋空港群衆パララックス層が横流動（物体移動が主） | 16 | 幕1/~18s | ★ | L3 Cycles 3D空港＋ボリューメトリック＋群衆パーティクル |
| 3 | CarryOnXrayScan（新規） | X線内の現金塊発見 | TSA X線で密な塊を検知 | X線内の現金塊が実移動して発見される | ~10 | 幕1 | | L2 EEVEE（X線発光レイヤー） |
| 4 | CheckpointConvergeMap（新規） | 検問へ人員が集まる有向フロー | TSA→州警官→DEAが検問へ集結 | 3主体が検問へ集まる有向フロー（点が実移動） | ~12 | 幕1 | | L2 EEVEE 3Dマップ＋有向パーティクル |
| 5 | ReportThresholdMeter（新規） | 現金申告義務の閾値メーター | CLM-0024＝国内線は上限/申告義務なし・国際$10,000超のみ | 可動メーター針が走る＋国内=無制限バー伸長 | ~9 | 幕1 | | L1 三面奥行きメーター |
| 6 | NoChargeStamp（StampReveal） | 無起訴スタンプ | 麻薬なし・逮捕なし・無起訴 | whip着弾後、スタンプ影が画面高3%/秒で沈む | ~3.5 | 幕1 | | 既存＋深度影 |
| 7 | InRemCaption（TerminalType＋DocHighlight・ILLUSTRATIVE） | in rem（物への訴訟）題号 | 「合衆国 対 現金の山」。**別事件フォーマット＋`ILLUSTRATIVE EXAMPLE/例`ラベル・Terry金額と一致させない** | 現金束が被告席へ実移動＋プレイヘッド走行 | ~8 | 幕2 | | L1 奥行き法廷 |
| 8 | **BurdenFlipScale**（幕2のみ1回・汎用象徴カウンタ対象） | 立証責任の反転（CAFRA） | **">50% — more likely than not"（illustrativeチップ付／「51%」の厳密数値は焼込み禁止）** | 皿が市民→政府へspring減衰振動＋">50%"着地 | **12** | 幕2/~12s | ★ | L3 Cycles **物理天秤rigidbodyシム** |
| 9 | ProfitIncentiveFlow（MoneyFlow有向） | 押収益が機関へ流れる構造 | equitable sharing（1984法）＝押収機関が収益保持。OL⑤ | 矢印/現金が機関へ流動（段ごとForcefulCut刻み）。幕2に第2インスタンスをスペア配置 | ~7 | 幕2 | | L1 有向3Dフロー |
| 10 | ForfeitureRevenueBar（ComparisonBars） | 没収収益の棒 | 没収収益 | 棒せり上がり＋数値ロールアップ | ~6 | 幕2末 | | 3D押出バー |
| 11 | PinDropMap 15空港＋流量ライン | 15空港の押収分布 | 15空港・Pittsburgh寄り | 時差点灯→Pittsburgh寄り＋流量ライン持続流動 | ~8 | 幕3 | | `map/MapScene.tsx`＋L2 EEVEE |
| 12-14 | USForfeitureNumber×3（別cut分割） | 3大総額を人間ビートで分断 | $209M（5,000人超・15空港・2006-2015）／$3.2B（約65,000件・無起訴・OIG 2017）／$68.8B（IJ・2000年以降・下限推計） | 各カウント桁走行、間の人間ビートはdepth dolly＋動く実写footage併走 | 各≤25 | 幕3 | | L3/L1 3D数値＋現金パーティクル飛散 |
| 15 | **HardshipStill**（Codex再現depth＋QuoteCard） | 返還遅延の人的被害 | 歯科治療の先送り・トラック修理不能（Rebecca公開声明） | depth dolly＋閉じた通帳/帯封束の実移動＋引用スライドイン | 18 | 幕3/~20s | ★ | L1 dpt-large 3D dolly 最大振幅 |
| 16 | CaseHeader（LowerThird 2段組） | 事件ヘッダ | Brown v. TSA（W.D.Pa.・2020/1提訴） | 下線走行＋書類パララックス（着地後は走光のみ＝床未達） | ~5 | 幕4 | 補助(分子外) | 据置 |
| 17 | ThreeClaims（KineticCaptions maskslide） | 訴状3主張 | ①TSA権限逸脱②第4修正（合理的疑いなき拘束）③DEAが$5,000以上を相当理由なく押収 | translateYマスク切上り×3スタッガー | ~12 | 幕4 | | 奥行きスタッガー |
| 18 | ReturnTimeline（casetimeline_c） | 返還までの時系列 | CAFRA請求期限・返還2020初頭 | プレイヘッド走行＋各ノード到達パルス。幕4に第2インスタンスをスペア配置 | ~10 | 幕4 | | 3D奥行きタイムライン |
| 19 | **ReturnHands**（返還・depth再現） | 貯金が手に戻る | 全額返還（2020初頭・理由提示なし） | 束が手に戻る実移動（暖光は補助） | **14** | 幕4/~14s | ★ | L1 dpt-large 3D dolly＋束移動 |
| 27 | **ReturnLedgerMotion**（新規） | 返還書類/現金束の実移動（幕4の60秒窓固有figure補填） | 返還書類群＋帯封束が原告へ | 返還の書類群と帯封束がテーブル上を実移動して原告へ渡る（物体移動主） | ~10 | 幕4 | | L1 3D卓上移動 |
| 20 | Program Scorecard（ComparisonBars） | 空港プログラムの費用対効果 | **"$22M vs 57"（約3年で約2,200万ドル押収／逮捕57件）・「TIP」名は不使用** | 逮捕棒が虚しく小＋比率ロールアップ | ~10 | 幕5 | | 3D押出比較バー |
| 21 | SignSwapMorph（新規） | 押収主体が別機関へ交代 | 「AIRPORT CASH PROGRAM」→「DHS/HSI/CBP」。**「TIP」正式名は一次確認まで焼込み禁止・総称ラベル** | 看板モーフ＋押収継続カウンタ | ~12 | 幕5 | | L2 EEVEE 3D看板モーフ |
| 22 | SplitBar 51/49（天秤再登場でなく分割バー） | 係争中の未決 | 合憲性未決（">50%"・51-49の数値は焼込まない） | バー境界が揺れ「未決」＋DocHighlight redact | ~6 | 幕5 | | 奥行きバー |
| 23 | DHSAirportRecur（新規） | 別機関による現金押収の継続 | Texas空港$800K再現（マリファナ臭主張・押収・無起訴） | Texas $800K再現depth＋現金束が別トレイへ移動。幕5に第2インスタンスをスペア配置 | ~10 | 幕5/17:50 | | L1 dpt-large 3D dolly＋束移動 |
| 24-26 | 幕頭タイトルビート（幕2/3/4頭） | 幕頭タイトル | 各幕タイトル | マスク切上り＋走光（着地後走光のみ＝床未達→降格） | 各幕頭 | 幕2/3/4頭 | 補助(分子外) | 据置（L1奥行き背景可） |

**新規部品＝7点**（実装はClaude・`aircash/`配下）: `CashStack.tsx`／`BurdenFlipScale.tsx`／`SignSwapMorph.tsx`／`CarryOnXrayScan.tsx`／`CheckpointConvergeMap.tsx`／`ReportThresholdMeter.tsx`／`ReturnLedgerMotion.tsx`。実装条件＝`FigureBeats.tsx`に`kind`配線・deterministic（`useCurrentFrame`）・BRANDトークンのみ・still-render smoke通過。**超激重ヒーローのBlender連番（#1/#2/#8/#12-14/#4/#21）は別スレで新規シーンスクリプトを作成し `hero.mp4` を `OffthreadVideo` として当該figure cutへ差し込む。**

---

## 2. 深度マップ（_depth.png）が必要な画像ID一覧

- **全68枚のCodex画像に`_depth.png`を先行バッチ生成する**（`tools/depth/gen_depth.py`・prototype `depth/depth.py`・`Intel/dpt-large` safetensors・ComfyUI venv python）。レンダ前に全画像分をバッチ完了させる。
- depth **治療（cut.kind=`depth`）を実際に当てる比率＝画像スチル尺の≥42%**（`check_flat_windows.py`のfで機械検査）。
- **超激重のdepth振幅アップリフト**: L1 `DepthScene`/`CaseFilm.tsx` depth treatment の `displacementScale` を**ヒーロー depth再現で最大 ≈0.9-1.1**（planeGeometry 6×4×360×240・overscan1.16・camera dolly z=5.6→3.3）まで上げ、奥行きを最大化（端が溶けないよう横スウェイ±0.22最小・DustField 30粒併走）。
- **depth再現を明示指定された主要スチル**（必ずdepth＋能動モーション併走。低速depth dolly単独は禁止＝flow7-10<床）:
  - AirportCheckpoint（#2・幕1）※超激重ではL3 Cyclesへ格上げ、depthは背景プレート/フォールバック
  - HardshipStill（#15・幕3・displacementScale最大）
  - ReturnHands（#19・幕4・displacementScale高）
  - DHSAirportRecur = Texas $800K再現（#23・幕5・displacementScale中）
  - USForfeitureNumber間の人間ビート（#12-14・幕3・depth dolly＋動く実写footage併走）
- 治療種別（depth/parallax/duotone/bleed）は `EP34_rolin_ai_prompts.v001.md` で68枚を image-span ID 単位に1枚ずつ確定（§10.1）。
- **レンダ制約**: WebGL depth使用のため長尺本編は `--concurrency=4`（`_depth.png` 全画像バッチ完了後にレンダ）。

---

## 3. ヒーロー面（大きく動く見せ場）一覧

**5面**。全て **尺≥12s・画面占有面積≥45%** を `hero`印ゲートで面積%・尺実測（数だけの水増しを排除）。**本超激重tierでは全ヒーローがL3 Cycles ceiling または L1実3Dで制作**。

| ヒーロー | figure# | 幕 | 尺(s) | 画面占有 | 超激重手法 |
|---|---|---|---|---|---|
| CashStack（＋NumberTicker） | #1 | OP | 12 | ~55% | L3 Cycles 3D帯封束＋DOF＋rigidbody |
| AirportCheckpoint | #2 | 幕1 | 16 | ~60% | L3 Cycles 3D空港＋ボリューメトリック＋群衆パーティクル |
| BurdenFlipScale | #8 | 幕2 | 12 | ~50% | L3 Cycles 物理天秤rigidbodyシム |
| HardshipStill | #15 | 幕3 | 18 | ~48% | L1 dpt-large 3D dolly 最大振幅 |
| ReturnHands | #19 | 幕4 | 14 | ~52% | L1 dpt-large 3D dolly＋束移動 |

（幕5・EDにヒーロー面なし。#1は8s→12sに延伸してhero床≥12sを満たす＝自己免除撤回済。）

---

## 4. 再利用MOTIONKIT／既存部品（二重実装禁止）

新規7点（§1）と超激重Blenderアセット以外は**既存部品を再利用**。新演出を作る前に必ず `motionkit/CATALOG.md` を先確認（二重実装禁止・CLAUDE invariant 14）。

- **基盤**: `CaseFilm.tsx`（cut.kind=depth/parallax/duotone/bleed・`DepthStill`）／`FigureBeats.tsx`（`kind`配線）／`ForcefulCut.tsx`（シーン境界トランジション）
- **超激重tier prototype**（`remotion/prototypes/motion3d/`・本番へポートして使用）: `Opening3D.tsx`（`OpeningDoc3D`/`OpeningPhoto3D`・L1背景/タイトル奥行き）／`Figures.tsx`（`StatCounter`/`Timeline`/`BarChart`/`NetworkDiagram`＝`DiagramFlow`へvariant統合）／`depth/DepthScene.tsx`（L1 dpt-large 2.5D）／`map/MapScene.tsx`（3D地図＝#11）／`audio/AudioReactive.tsx`（音反応オーバーレイ）／`blender/bpp_cycles.py`（L3ヒーロー土台）／`blender/bpp_eevee.py`（L2土台）／`blender/bpp_physics.py`（rigidbody土台＝#8/#1）
- **carsearch/**（EP32譲りの部品群）・**motionkit/**（プレミアム再利用部品40種＋プリセット群）
- **図で流用する既存パーツ**: `StampReveal`（#6）／`TerminalType`＋`DocHighlight`（#7・#22）／`MoneyFlow`（#9）／`ComparisonBars`（#10・#20）／`PinDropMap`（#11）／`NumberTicker`（#1）／`LowerThird`（#16）／`KineticCaptions`（#17）／`casetimeline_c`（#18）／`QuoteCard`（#15）

---

## 5. トランジション規律（§3.2）

**シーン境界（`ForcefulCut.tsx`）** mode: `push`／`slide`／`zoompunch`／`whip`。
- パラメータ: **spring(damping15, mass0.7, stiffness200, 0.20s)＋減衰ブラー16→0px**（モーションブラー必須）。
- 幕別頭トランジション: HOOK=zoompunch／OP=push／幕1=push／幕2-5=zoompunch／ED=push。

**幕内質感トランジション**: `IrisTransition`／`GlitchCut`／`FocusPull`（各≤0.17s）。

**禁止事項（恒久）**:
- 金縦スイープ（左右スイープ線）
- クロスフェード主体
- 黄ウォッシュ（yellow wash）
- 単ズームのみ
- **周回・lissajous淡い光ループ**

**カデンス（AND定義・平坦20秒ゼロ）**:
1. 各12秒窓に within-shot（境界ForcefulCut除外）で持続する figure/depth/parallax 由来の motion_energy ≥8 必須。
2. 静止スチルのみの12秒窓＝0（各窓に最低1つの持続モーション実体）。
3. 各60秒窓のキネティック被覆秒数 ≥窓の40%（≈24s）。
4. cut配列に per-shot予測flowタグ＋併走モーション種別フィールドを必須化（ビルダーが出力前に落とす）。
→ `check_flat_windows.py`（hard）が機械検査。

---

## 6. 数値予算サマリ（§3.0）

| 項目 | 本話値 |
|---|---|
| 完成尺 | 1,170-1,230s（20分・`check_runtime_band.py`が唯一の承認偏差） |
| シーン数 | **39** |
| カット数 | **392**（＝画像160＋footage188＋figure44） |
| 平均カット長（image+footageのみ・figure除く） | 2.30-2.60s（902s÷348＝2.59s／静止4s超保持禁止） |
| figure beat尺 | ≈302s÷44＝6.9s/beat（≤25s/beat） |
| depth比率 | 画像スチル尺の ≥42% |
| キネティック被覆 | 各60秒窓 ≥40%（≈24s/60s）かつ 真アニメート図/動く実写の合計screen-time ≥全体40% |
| 動くFigureBeats（実キネティック） | **23本**（#1-15, 17-23, 27。#16・#24-26は補助＝分子外） |
| ヒーロー面 | **5面**（尺≥12s・占有≥45%・全て超激重L3/L1） |
| motion_energy | within-shot平均≥12・p10≥9・p50≥13・12秒窓≥8 |
| 本編輝度 | median YAVG≥48・暗frame率≤15%・per-image-cut≥48・12秒窓median≥44・連続暗≤1.5s |
| footage多様性 | distinct≥0.40（固有clip実採用≥76種が支配床）・再利用≤4・footage screen-time≥35%（≥420s） |
| 画像 | 68枚・全4K（3840×2160）・Codex生成 |

幕別カット/figure割付（§3.4）:

| 幕 | 尺(s) | シーン | 総カット | 画像cut(尺) | footage cut(尺) | figure cut(尺) |
|---|---|---|---|---|---|---|
| HOOK | 8 | 1 | 3 | 2(5s) | 1(3s) | 0 |
| OP | 17 | 1 | 5 | 2(3s) | 2(2s) | 1(12s) |
| 幕1 | 244 | 8 | 93 | 42(100s) | 43(92s) | 8(52s) |
| 幕2 | 221 | 7 | 72 | 30(80s) | 34(85s) | 8(56s) |
| 幕3 | 223 | 8 | 72 | 30(78s) | 33(82s) | 9(63s) |
| 幕4 | 242 | 7 | 77 | 30(92s) | 38(92s) | 9(58s) |
| 幕5 | 213 | 6 | 64 | 20(63s) | 36(90s) | 8(60s) |
| ED | 36 | 1 | 6 | 4(18s) | 1(12s) | 1(6s) |
| **計** | **≈1,204** | **39** | **392** | **160(≈441s)** | **188(≈461s)** | **44(≈302s)** |

（figure cut44 ＝ 固有figure27本＋reuse/スペア17インスタンス。各figure≥1カットを物理的に満たす。）

---

## 7. 持続モーションの必須ルール（紙芝居フリーズ根絶）

- **motion_energy床**: within-shot（境界カット除外）平均≥12・**p10≥9 かつ p50≥13**・12秒窓≥8。走光/低速depthだけでは超えられない床。境界ForcefulCutのスパイクは床に算入しない。
- **走光/暖光を主キネティック要素にしたビートは分子から除外**＝主運動は必ず**物体の実移動**。（超激重L3/L1ヒーローも Bloom/暖光は補助・主運動は3D物体移動）
- **低速depth dolly単独禁止**（flow7-10 < p10床9・p50床13）。必ず能動モーション（物体の実移動）を併走させる。
- **キネティック度床**＝主要要素が画面高≥2.5%/秒で動く秒数がビート尺の≥60%。未達（タイトル切上り＋走光のみ等）は補助図に降格し分子に数えない。
- **各60秒窓のキネティック被覆 ≥40%**。全60秒窓に固有figure≥1（幕2/4/5は境界部分窓に第2インスタンスをスペア配置して被覆）。
- **静止スチル4s超保持禁止**。静止スチルのみの12秒窓＝0。
- **周回・lissajous淡い光ループ禁止**（単調等速のfreeze床は不可）。テンションは物体運動・カット刻みで作る。
- 治療別予測optical-flowレンジ: 低速depth dolly≈7-10／dual-layer parallax≈9-13／playhead走行・有向パーティクル・被写体内オブジェクト移動≈14-20／L3物理シム・群衆パーティクル≈14-24。p10≥9・p50≥13を単独で満たせない治療は必ず能動モーション併走。
- cut配列に **per-shot予測flowタグ＋併走モーション種別を必須フィールド化**（併走レイヤー無しカットはビルダーが出力前に落とす）。
- 検証ゲート: `check_flat_windows.py`（hard・新規）＋`motion_energy`（実装済SOLID・p50≥13は加算改修）。量産前に代表窓（ベスト=#15 HardshipStill／ワースト=幕1「数える手→後ろ姿→閉じた通帳」3カット連続の60秒窓）を実レンダし window motion_energy 実測を添付してから量産に進む。

---

## 8. 超激重レンダ規律・実行前提（別スレ制作の運用）

- **環境**: Windows RTX ノード・Blender 5.1（`C:\Program Files\Blender Foundation\Blender 5.1\blender.exe`）・OptiX GPU・Python 3.11・SSD H:（`H:\pd-media`）・Node・`@remotion/three@4.0.484`+three+`@react-three/fiber@8`。
- **ヒーロー先行連番→encode→差込**: L3/L2 Blenderヒーローは**別プロセス・別スレで先行レンダ**（PNG連番 `f_%04d.png`）→ row-6 encode（`-framerate 60 -c:v libx264 -crf 16 -pix_fmt yuv420p`）→ `hero.mp4` を `OffthreadVideo` として該当 figure/hero cut へ差し込む。Bookends（gold BrandOpening）は据置・3Dは背後プレート（invariant 14）。
- **レンダコスト目安（超激重・4K/60fps）**: L3 Cycles ~30 s/frame級（1080p ~8s×4Kアップリフト約4×）。12s×60fps=720frame → 単ヒーローで約6時間級。**GPU占有・1本ずつ直列・完走まで殺さない・tailで進捗を隠さない**。健全性=GPU利用率とframe進捗。CPU（libx264）encode・クオリティ最優先（NVENC切替えない）。
- **本編（L1 depth WebGL含む）**: `_depth.png` 全画像バッチ完了後に `--concurrency=4` でレンダ。
- **決定論/偽の緑遮断**: 全モーション `useCurrentFrame`／Blenderは keyframe＋bake（rigidbodyは `point_cache` bake_all）。再レンダ後は必ずsha照合（`freshness` sha≠前回＋mtime）＋mux `audio_mix_sha256` 刻印。必須ゲート・レジストリ（fail-closed＋負のフィクスチャ）＋全hard緑（新規ゲートはビルド後計上）で初めて完成。
- **量産例**: `npx remotion render Rolin out/EP34_rolin.mp4 --props=./props/EP34_rolin.json --concurrency=4`。ヒーロー: `blender -b -P remotion/src/blender/aircash_cashstack.py -- out/hero_cashstack 3840 2160 1 720 200` → `npx remotion ffmpeg -framerate 60 -i out/hero_cashstack/f_%04d.png -c:v libx264 -crf 16 -pix_fmt yuv420p -y public/EP34/hero_cashstack.mp4`。
- **権利/分業**: Codex=画像68枚のみ。Blenderアセット/TSX/ゲートはClaude。生成3D/深度ビジュアルは説明/再現（invariant 11・実在肖像なし・匿名/後ろ姿/シルエット/手のみ・R2）。SDXL勝手起動禁止。
- **輝度**: 超激重ヒーロー（AgX/Bloom）も合成後 median YAVG≥48・per-cut≥48 を `image_cut_luma`（実装済SOLID）で実測。割れは softbox/emission/key energy で是正。
