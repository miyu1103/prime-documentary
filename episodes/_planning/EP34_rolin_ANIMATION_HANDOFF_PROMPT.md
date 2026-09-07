# EP34 rolin — アニメーション制作 引き継ぎプロンプト（別スレ用・そのまま貼る）

あなたは Prime Documentary の**プレミアム・アニメーション制作スレ**。EP34「空港で全財産を没収（Rolin/Brown・民事没収）」の**超激重（SUPER-HEAVY / L3 ceiling）アニメ素材**を制作する。台本・画像(Codex)・音・字幕は別担当。**あなたの担当は動く図(FigureBeats)とヒーロー3D/物理レンダのみ。**

## まず読む（正典・この順で）
1. `episodes/_planning/EP34_rolin_ANIMATION_ASSETS.v001.md` … **素材の正典**（27図/ヒーロー5・各図の入力データ/モーション/尺/幕時刻・深度全68枚計画・持続モーション床[p10≥9/p50≥13・走光は主運動に数えない]・ForcefulCut規律・超激重tier表）。**数値はここが確定値。**
2. `episodes/_planning/EP34_rolin_DESIGN.v001.md` … 文脈（§3）
3. `docs/PD_MOTION3D_HERO_AND_FIGURES_SPEC.md` … L1 `@remotion/three` / L2 EEVEE / **L3 Cycles ceiling** / encode row-6
4. `remotion/prototypes/motion3d/`（`blender/bpp_cycles.py`・`bpp_physics.py`・`bpp_eevee.py`・`depth/DepthScene.tsx`・`depth/depth.py`・`Opening3D.tsx`・`Figures.tsx`）… **実在雛形から拡張（二重実装禁止）**

## 作る成果物
- **ヒーロー5面（最重量級・尺≥12s・画面占有≥45%）**: CashStack(3D帯封束+DOF+rigidbody) / AirportCheckpoint(3D空港+ボリューメトリック光+群衆パーティクル) / BurdenFlipScale(物理天秤rigidbodyシム substeps20/solver20/bake) / HardshipStill・ReturnHands(`@remotion/three` dpt-large 3D dolly最大 displacementScale0.8–1.1・cam z=5.6→3.3)。
  - 設定＝マニフェスト超激重tier表（Cycles samples 200天井 / OptiX / AgX / **4K 3840×2160 / 60fps** / モーションブラー shutter0.5 / caustics OFF）。
  - USForfeitureNumber($209M/$3.2B/$68.8B)＝3D数値＋現金パーティクル飛散。
- **残り図**: `remotion/src/components/aircash/`（新規7点＝CashStack/BurdenFlipScale/SignSwapMorph/CarryOnXrayScan/CheckpointConvergeMap/ReportThresholdMeter/ReturnLedgerMotion）＋既存流用（StampReveal/TerminalType/MoneyFlow/ComparisonBars/PinDropMap 等）。`FigureBeats.tsx` に `kind` 配線・deterministic。
- **depth**: 全68枚 `_depth.png` を先行バッチ（`tools/depth/gen_depth.py`・dpt-large）。depth治療 image still尺の≥42%。

## レンダ設定・出力先・規律
- Cycles ceiling: `blender -b -P remotion/src/blender/aircash_<asset>.py -- out/hero_<asset> 3840 2160 1 <frames> 200` → `ffmpeg -framerate 60 -i out/hero_<asset>/f_%04d.png -c:v libx264 -crf 16 -pix_fmt yuv420p -colorspace bt709 -y remotion/public/rolin/hero_<asset>.mp4`（row-6）。Remotionへ `OffthreadVideo`。
- 量産例: `npx remotion render Rolin out/EP34_rolin.mp4 --props=./props/EP34_rolin.json --concurrency=4`。**CPU(libx264)固定・NVENC禁止**・1本ずつ直列・完走までkillしない。

## 制約（非交渉）
- **事実数値は一切改変しない**（~$82,000/訴追ゼロ/2020返還/$209M・$3.2B・$68.8B・各CLM）。「51%」等の厳密値は焼込まず"more likely than not / >50%"表現。in rem題号は`ILLUSTRATIVE`ラベルでTerry金額と一致させない。モーション/レンダのみ超激重化。
- **実在肖像なし**（匿名・後ろ姿・手元）・**判読テキスト/ロゴなし**・機体/空港/車は無ブランド・生成物は再現（invariant11・R2）。
- **持続モーション床（hard）**: `motion_energy` within-shot≥12 / **p10≥9 かつ p50≥13** / 12秒窓≥8。**低速depth dolly単独禁止**（必ず物体の実移動を併走）。**走光/暖光を主運動にしたビートは分子外。周回淡い光禁止。静止4s超保持禁止。尺の水増し禁止。**
- **Codex画像は触らない**（`remotion/public/rolin/img/`）。SDXL勝手起動禁止。

## 完了条件（自己申告禁止）
- `check_final_acceptance.py`（motion_energy / image_cut_luma / body_luma / footage_utilization / check_padding ほか）緑＋`check_flat_windows.py`（新規・要実装なら先に）。
- `preflight_owner_review.py --ep PD-2026-034-rolin` を実行し実数＋画像をオーナー提示してから「完成」。
- 代表窓（ベスト=#15 HardshipStill／ワースト=幕1「数える手→後ろ姿→閉じた通帳」3連続の60秒窓）を実レンダし window motion_energy 実測を添付してから量産へ。
