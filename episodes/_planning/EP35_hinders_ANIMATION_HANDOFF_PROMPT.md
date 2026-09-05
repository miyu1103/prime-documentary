# EP35 hinders — アニメーション制作 引き継ぎプロンプト（別スレ用・そのまま貼る）

あなたは Prime Documentary の**プレミアム・アニメーション制作スレ**。EP35「銀行のルール通りにしたら全財産を奪われた（Hinders・IRS structuring）」の**超激重（SUPER-HEAVY / L3 ceiling）アニメ素材**を制作する。台本・画像(Codex)・音・字幕は別担当。**あなたの担当は動く図(FigureBeats)とヒーロー3D/物理レンダのみ。**

## まず読む（正典・この順で）
1. `episodes/_planning/EP35_hinders_ANIMATION_ASSETS.v001.md` … **素材の正典**（27図/ヒーロー8・各図の入力データ/モーション/尺/幕時刻・depth239カット計画[連続≤12s]・持続モーション床[within-shot≥16/p10≥11・要素≥6]・ForcefulCut 4種規律・OP/ED・超激重tier §SH表）。**数値はここが確定値。**
2. `episodes/_planning/EP35_hinders_DESIGN.v001.md` … 文脈（§3.0〜§3.7・§9.1）
3. `docs/PD_MOTION3D_HERO_AND_FIGURES_SPEC.md` … L1 `@remotion/three` / L2 EEVEE / **L3 Cycles ceiling** / encode row-6
4. `remotion/prototypes/motion3d/`（`blender/bpp_cycles.py`・`bpp_physics.py`・`bpp_eevee.py`・`depth/DepthScene.tsx`・`depth/depth.py`・`Figures.tsx`）… **実在雛形から拡張（二重実装禁止）**

## 作る成果物
- **ヒーロー8面（最重量級）**: BSAOriginFlow(Blender Mantaflow 3D流体シム) / ThresholdMeter(`@remotion/three` 実3Dゲージ) / FrozenAccount(Blender rigid-body 氷破断シム WIND field95→0 f1-18) / PolicyReversalTimeline(3D空間タイムライン fly-through) / McLellanParallel(3D並置+dpt-large二面) / McLellanLedger(3D台帳+301点灯パーティクル) / TIGTA-Dots(278点群パーティクルシム) / CaroleAfterCard(Cycles ceiling 店内3D dolly)。
  - 設定＝マニフェスト§SH表（Cycles samples 160–200 / OptiX / AgX / glass Transmission1.0/IOR1.85/Bevel0.025×3seg / softbox 1.4/1.1/0.8 / DOF f2.2 / **4K supersample / 60fps** / ~30s/frame級）。
- **残り19図**: `remotion/src/components/hinders/`（新設=StructuringExplainer/BurdenShiftScale/McLellanStore ほか）＋最寄りMOTIONKITプリセット+data props差分（`FluidStreamFlow`/`IceCrackPropagate`/`PlayheadTrackV`/`SplitCompareV`/`LedgerCountUp`/`DotMatrixReveal`/`RoomDollyV` 等・§4写像表どおり）。全図 optical-flow実測で**独立運動要素≥6**必須。
- **depth**: 239カット（=全528の45%・Act別加重）を `DepthImageV`(dpt-large)。連続depth画像≤12s。元画像プール **≥136 unique**（ai_prompts v002で拡張）。

## レンダ設定・出力先・規律
- Cycles ceiling: `blender -b -P remotion/src/blender/hinders_<asset>.py -- out/hero_<asset> 3840 2160 1 <frames> 200` → `ffmpeg -framerate 60 -i out/hero_<asset>/f_%04d.png -c:v libx264 -crf 16 -pix_fmt yuv420p -colorspace bt709 -y remotion/public/hinders/hero_<asset>.mp4`（row-6）。Remotionへ `OffthreadVideo`。
- Cycles ceiling 3面はsupersampleで実効~30s/frame級・GPU占有1本ずつ直列。`@remotion/three`系は **`--concurrency=4`**。**CPU(libx264)固定・NVENC禁止**・完走までkillしない。

## 制約（非交渉）
- **事実数値は一切改変しない**（$32,820.56/$107,702.66/301/~$2M/278/91%/231件$17.1M/各CLM）。公聴会は本人証言を出さない(grade B)。NYT一面見出しは可読ブランド書体を出さない。モーション/レンダのみ超激重化。
- **実在肖像なし**（匿名・手元・後ろ姿・シルエット）・**判読テキスト/実通貨/実ロゴなし**・生成物は再現（invariant11・R2）。3レーン分離（Iowa暖アンバー/Federal冷スチール/NC冷緑）でEP33/34と素材被り禁止。
- **持続モーション床（hard）**: ROI within-shot≥16/p10≥11/12秒窓≥8、任意ROIで**連続40f(0.67s)静止=FAIL**、depth画像は構造モーション重畳必須（ken-burns単独=FAIL）。**SceneBed正弦呼吸/往復ループ/定位置グロー呼吸/明滅=全撤去。周回淡い光禁止。尺の水増し禁止。**
- **Codex画像は触らない**（`remotion/public/hinders/img/`）。SDXL勝手起動禁止。

## 完了条件（自己申告禁止）
- `check_final_acceptance.py`（motion_energy / image_cut_luma / body_luma / footage_utilization / check_padding ほか）緑＋（要実装なら先に）`check_flat_windows.py`/`check_figure_flow`。
- `preflight_owner_review.py --ep PD-2026-035-hinders` を実行し実数＋画像をオーナー提示してから「完成」。
- 代表窓を実レンダし window motion_energy 実測を添付してから量産へ。
