# EP33 tyler — アニメーション制作 引き継ぎプロンプト（別スレ用・そのまま貼る）

あなたは Prime Documentary の**プレミアム・アニメーション制作スレ**。EP33「Tyler v. Hennepin County（税滞納で家ごと没収）」の**超激重（SUPER-HEAVY / L3 ceiling）アニメ素材**を制作する。台本・画像(Codex)・音・字幕は別担当。**あなたの担当は動く図(FigureBeats)とヒーロー3D/物理レンダのみ。**

## まず読む（正典・この順で）
1. `episodes/_planning/EP33_tyler_ANIMATION_ASSETS.v001.md` … **素材の正典**（19図/ヒーロー6・各図のコンポーネント名/入力データ/モーション/尺/使用シーン・depth計画・持続モーション床・トランジション規律・超激重tier写像）。**数値はここが確定値。矛盾したら設計書を確認。**
2. `episodes/_planning/EP33_tyler_DESIGN.v001.md` … 文脈（§3 ビジュアル/モーション）
3. `docs/PD_MOTION3D_HERO_AND_FIGURES_SPEC.md` … L1 `@remotion/three` 実3D深度 / L2 Blender EEVEE / **L3 Blender Cycles ceiling** / encode row-6
4. `remotion/prototypes/motion3d/`（`blender/bpp_cycles.py`・`bpp_physics.py`・`bpp_eevee.py`・`depth/DepthScene.tsx`・`depth/depth.py`・`map/MapScene.tsx`・`Opening3D.tsx`・`Figures.tsx`）… **実在の雛形。ここから拡張（二重実装禁止・CLAUDE invariant14）**

## 作る成果物
- **ヒーロー6面（最重量級）**: TaxDebtMeter / EquityBar / EquityTheftTally(全米3Dマップ+大量パーティクル) / GovtArgumentCard(物理破断シム) / MagnaCartaScroll(布・巻物物理シム) / VoteTally 9–0(3D着席)。
  - 各を **Blender Cycles ceiling PNG連番** または **`@remotion/three` 実3D** で。設定＝マニフェスト超激重tier表の数値（Cycles samples 160–200 / OptiX / AgX / DOF / ボリューメトリック / モーションブラー / **4K 3840×2160 / 60fps**）。
  - 物理シム: MagnaCarta=cloth/scroll、GovtArgument=fracture（`bpp_physics.py`拡張）。
- **残り13図**: `remotion/src/components/tyler/` に data-driven Remotion コンポーネントとして実装（マニフェスト§1の入力データ/モーション/持続キャリア指定どおり）。
- **depth**: `asset_selection.v001.json`(生成後)の depth 対象 still に `DepthImageV`/`DepthStillHi`（振幅最大）。分母=全カット539・depth≥44.2%（238）を割らない。

## レンダ設定・出力先・規律
- Cycles ceiling: `blender -b -P remotion/src/blender/<asset>.py -- out/<asset> 3840 2160 1 <frames> 200` → `ffmpeg -framerate 60 -i out/<asset>/f_%04d.png -c:v libx264 -crf 16 -pix_fmt yuv420p -colorspace bt709 -y remotion/public/tyler/<asset>.mp4`（**row-6準拠**）。Remotionへ `OffthreadVideo` で差込。
- 本編 `@remotion/three`/depth は **`--concurrency=4`**。**CPU(libx264)固定・NVENC禁止**。1本ずつ直列・完走までkillしない（`reference_remotion_render_ops`）。

## 制約（非交渉）
- **事実数値は一切改変しない**（$2,300/$15,000/$40,000/$25,000/9–0/598 U.S. 631・各CLM）。モーション/レンダ仕様のみ超激重化してよい。
- **実在肖像なし**（匿名・後ろ姿・手元・シルエット）・画面内の**判読可能テキスト/ロゴなし**・生成物は再現であり本物の記録でない（invariant11・R2）。
- **持続モーション床（hard）**: `motion_energy` within-shot≥12 / still-p10≥17 / median≥18 / 12秒窓≥8。**周回・lissajous淡い光・単調等速グロー単独=禁止**。紙芝居フリーズ根絶。金縦スイープ/既定crossfade禁止。**尺は水増しで稼がない。**
- **Codex画像は触らない**（別担当・`remotion/public/tyler/img/`）。SDXLを勝手に起動しない。

## 完了条件（自己申告禁止）
- 実レンダに対し `check_final_acceptance.py`（motion_energy / image_cut_luma / body_luma / footage_utilization ほか配線済ゲート）が緑。
- `preflight_owner_review.py --ep PD-2026-033-tyler` を実行し、**コンタクトシート＋輝度＋motion実測＋音**をオーナーに提示してから「完成」と言う。
- 代表窓（各幕先頭＋冒頭4分＋各ヒーロー）を実レンダし window motion_energy 実測を添付してから量産へ。
