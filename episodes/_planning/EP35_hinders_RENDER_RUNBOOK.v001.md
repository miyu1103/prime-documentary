# EP35「hinders」レンダRUNBOOK v001 — 超激重バッチ引き渡し（別スレ/オーナーがそのまま流す）

- **Episode**: PD-2026-035-hinders（「FOLLOWING THE RULE.」／IRS structuring 民事没収）
- **binding（正典・数値の確定元）**: `episodes/_planning/EP35_hinders_ANIMATION_ASSETS.v001.md`（§2 depth計画・§SH ヒーロー・§8 完成条件）＋ `episodes/_planning/EP35_hinders_ANIMATION_HANDOFF_PROMPT.md`＋`docs/PD_MOTION3D_HERO_AND_FIGURES_SPEC.md`。
- **作業ルート（絶対）**: `C:\Users\aab15\Documents\prime-documentary`。以下のコマンドはこのルートを CWD として実行する。
- **前提ノード**: Windows / RTX 4090（24GB・実測 2026-07-08 空きVRAM ~21GB）。Blender **5.1**＝`C:\Program Files\Blender Foundation\Blender 5.1\blender.exe`。深度＝ComfyUI venv python `C:\Users\aab15\ComfyUI\venv\Scripts\python.exe`（torch 2.5.1+cu121 / transformers 5.13.0 / CUDA可）。
- **不変ルール（reference_remotion_render_ops）**: 1本ずつ**直列**・完走まで**killしない**・進捗を**tailで隠さない**・健全性はheadless chrome数とCPU/GPUで見る。CPU(libx264)固定・**NVENC禁止**。SSD(H:)/`runs/`はコミットしない。

> **⚠ 事実数値は一切改変しない（超激重化してもモーション/レンダ品質のみ）**:
> `$32,820.56`（押収 CLM-0002）／`$107,702.66`／`301`入金／`~$2M`累計／`278`サンプル／`91%`（件数比）／`231`件 `$17.1M`（CLM-0014）。
> 公聴会は本人証言を出さない（grade B）。判読テキスト/実通貨/実ロゴ/実在肖像なし（invariant11）。3レーン分離＝Iowa暖アンバー/Federal冷スチール/NC冷緑。

> **⚠ fps 表記の正典衝突（報告事項・CLAUDE §5）**: `ANIMATION_ASSETS.v001.md §SH.0`（＝「数値の確定元」正典）は **row-6 encode を `-framerate 30`／ヒーロー連番 fps=30** と明記。一方 `ANIMATION_HANDOFF_PROMPT.md` の1箇所は「60fps／`ffmpeg -framerate 60`」と食い違う。**本RUNBOOKは正典(ASSETS §SH.0)に従い fps=30 を採用**。60fpsで焼く場合はオーナー承認の上、全ヒーローで統一しBlenderのシーンfpsも30→60へ揃えること（片方だけ変えるとシム/モーションの実時間がずれる）。

---

## 0. 事前フライト（毎回・順に）

```bash
cd /c/Users/aab15/Documents/prime-documentary

# 1) GPU が空いているか（A1111:7860 / ComfyUI:8188 がフルロード中ならVRAM競合。unload-checkpoint で解放）
nvidia-smi --query-gpu=memory.free,utilization.gpu --format=csv

# 2) 深度 venv 健全性
"C:/Users/aab15/ComfyUI/venv/Scripts/python.exe" -c "import torch,transformers;print(torch.__version__,transformers.__version__,torch.cuda.is_available())"

# 3) Blender 5.1 実在
ls "C:/Program Files/Blender Foundation/Blender 5.1/blender.exe"

# 4) 元画像プールの現数（depth前提。設計要件 >=136 unique）
ls remotion/public/hinders/img/*.png | grep -v _depth | wc -l
```

---

## 1. 深度バッチ（DepthImageV / dpt-large・239カット計画）

### 1.1 depth 適用カバレッジ計画（§2 区間表・**verbatim 転記**）

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

- 「depth処理カット」＝ **DepthImageV(dpt-large深度マップ)を適用する単独画像カットのみ**。図 F1–F21（204カット）は depth✔だが L3 near/mid/far 層パララックスで**別機構**＝239に非算入。
- 数値注記: 区間行の単純四捨五入和は 240、正典 §2 の確定「計」は **239**（丸め差・確定値=239を採る）。
- **depthパララックス数値（§3.1）**: near 24–28px / mid 14–18px / far 6–8px、`Easing.out(cubic)`、L3全体 scale 1.03→1.08。ヒーロー隣接カットは §SH.4 で最大 ±64px まで拡張（subdivided plane の segments を上げジャギ回避）。
- **各 depth 画像カットは構造モーション必須**: 前景プレーン実移動 / 走行光 / 図オーバレイの1つ以上で ROI≥25%画素が≥4.0%/幅・秒(≈77px/s)。**ken-burns 単独＝FAIL**。
- **連続 depth 画像の上限＝≤12s**（超える前に図/実写差替静止画/キネティック字幕を差込む）。

### 1.2 実行コマンド（元画像フォルダを一括処理・`<name>_depth.png` を隣に生成）

```bash
cd /c/Users/aab15/Documents/prime-documentary
"C:/Users/aab15/ComfyUI/venv/Scripts/python.exe" tools/depth/gen_depth.py remotion/public/hinders/img
```

- 冪等: 既存 `_depth.png` は自動 skip、`_depth` を含む名前は入力から除外。**元画像(Codex担当)は上書きしない**（`_depth` のみ追加）。生成物は `remotion/public/hinders/img/` が `.gitignore` 済み＝**コミットされない**（確認済み）。
- 仕様（`tools/depth/gen_depth.py`）: `Intel/dpt-large`（safetensors・torch<2.6でも可）／near=白／0-255正規化／`GaussianBlur(2)`／出力 mode **L**・元画像と同一サイズ。
- device: `torch.cuda.is_available()` が真なら GPU(0)。**A1111/ComfyUI が動いていない前提で単発実行**（VRAM競合時は他を落とすか `unload-checkpoint`）。
- 実測基準（2026-07-08・13枚）: GPU device 0・**13枚を約90秒**（≈6.9s/枚、初回モデルロード込み）。136枚見積り ≈ 12–16分（初回ロード後は ~5s/枚）。

### 1.3 ★ブロッカー（239カバレッジ未達・要 Codex 対応）

- **設計要件**: 元画像プール **≥136 unique**（単独露出の生成静止画）。239 depthカットは 324 単独画像placement のうち 239（=74%）で「image-cut depth必須カバレッジ ≥70%」を満たす同一集合。
- **現状（2026-07-08 実測）**: `remotion/public/hinders/img/` に **13枚**（`PD-2026-035-S001-IMG-001` 〜 `S013-IMG-013`・Codex 生成継続中）。
- **判定**: **136 未満では 45%＝239 の depth カバレッジは物理的に未達**。13枚に depth を打っても 13枚分しか埋まらない。
- **担当**: 元画像の拡張は **ai_prompts v002（S001–S068＝62枚 → ≥136 へ拡張）＝Codex 担当**（本アニメスレの範囲外）。画像が ≥136 unique に到達し次第、上の 1.2 を**再実行**すれば増分だけ depth が付く（既存 skip・冪等）。
- **ゲート合流**: `footage_utilization` は 136生成 unique 資産の各々が最終mp4に ≥1回出現を強制（§7-6・黒画面ゼロ）。画像不足のままの最終レンダは受領ゲートで落ちる。

---

## 2. Blender ヒーロー本番連番レンダ（F2 / F5 / F20 ＝ Cycles ceiling 3面）

**引数規約**（`hinders_bsa_flow.py` で確認済み）: `blender -b -P <script.py> -- <OUT> <RX> <RY> <FS> <FE> <SAMPLES>`。`FS==FE`→**テスト静止画**（シム進まず静的geoで1枚）、`FS<FE`→**PNG連番** `<OUT>/f_0001.png…`（bake_all→render animation）。**Blender 5.x は動画出力削除＝必ずPNG連番→別途encode**。

- **降格禁止**: §SH.3 により F2/F5/F20 の Cycles ceiling 3面は **EEVEE へ降格しない**（最上級の掴み）。時間都合で降格する場合は silent cap 禁止＝**必ずログに残す**。
- **負荷（§SH.5 実務見積り）**: 各 ~8s/frame@1080p（`bpp_cycles.py` 実測）× 4K supersample(3840→1080=約4倍画素)＝**実効 ~30s/frame 級**。100f/カット→**約50分/カット**。**GPU占有・1本ずつ直列・完走までkillしない・tailで隠さない**。
- **frames（`<FE>`）は「目安」**（設計は図ごとの尺を個別明記していない）。主要モーション frame ＋ freeze整合の終端継続分を含めて **ROI連続40f(0.67s)静止を出さない** 長さにする。`<FE> = round(カット秒 × 30)`。

### 2.1 テスト静止画（本番前に必ず1枚・構図/ライト/マテリアル確認）

```bash
cd /c/Users/aab15/Documents/prime-documentary
# F2（既存スクリプト）を FS==FE=1 で静止テスト
& "C:/Program Files/Blender Foundation/Blender 5.1/blender.exe" -b -P remotion/src/blender/hinders_bsa_flow.py -- out/hero_bsa_flow_test 1920 1080 1 1 64
```
（PowerShell 実行。Bash から呼ぶ場合は `"C:/Program Files/Blender Foundation/Blender 5.1/blender.exe" -b -P ...` と `&` を外す。）

### 2.2 本番連番（3840×2160 → 後段で 1080p supersample・Cycles 200 samples）

```powershell
# ==== F2 BSAOriginFlow ★（Mantaflow FLIP 流体シム）— 主要:流下0-48f + 滴下余韻 ====
#   スクリプト: remotion/src/blender/hinders_bsa_flow.py（実在）
& "C:\Program Files\Blender Foundation\Blender 5.1\blender.exe" -b -P remotion/src/blender/hinders_bsa_flow.py -- out/hero_bsa_flow 3840 2160 1 120 200

# ==== F5 FrozenAccount ★（rigid-body 氷破断シム・WIND field 95->0 f1-18）— 主要:亀裂0-40f + push8f ====
#   スクリプト: remotion/src/blender/hinders_frozen_account.py 【要実装（別スレ制作・bpp_physics.py 拡張）】
& "C:\Program Files\Blender Foundation\Blender 5.1\blender.exe" -b -P remotion/src/blender/hinders_frozen_account.py -- out/hero_frozen_account 3840 2160 1 110 200

# ==== F20 CaroleAfterCard ★（Cycles ceiling 店内3D dolly）— 主要:奥→手前ドリー0-72f + "SOLD"札 ====
#   スクリプト: remotion/src/blender/hinders_carole_after.py 【要実装（別スレ制作・bpp_cycles.py 拡張）】
& "C:\Program Files\Blender Foundation\Blender 5.1\blender.exe" -b -P remotion/src/blender/hinders_carole_after.py -- out/hero_carole_after 3840 2160 1 140 200
```

- **`<FE>` 目安根拠**: F2=主要48f＋滴下余韻→**120**／F5=主要40f＋push8f＋氷片沈降余韻→**110**／F20=主要72f＋札着地＋店内ドリー継続→**140**。カット実尺が確定したら `round(秒×30)` で置換（freeze整合を割らない下限＝主要モーション frame）。
- **物理シム（F2 流体 / F5 氷破断）**: `bake_all(bake=True)` → `render(animation=True)`。**静止画レンダはシムが進まない**（`FS==FE` テストは静的geoフォールバック）。rigid-body world = substeps20/solver20・friction0.35/restitution0.05。bake は render とは別に時間がかかる。
- **Cycles GPU**: `OPTIX→CUDA→HIP→ONEAPI` 順で試行、無ければ CPU。`use_denoising=True`・`view_transform='AgX'`・**caustics OFF固定**（bloomで代替）。氷/ガラス＝Transmission1.0/Roughness0.02/IOR1.85＋Bevel0.025×3seg。motion blur steps=16・shutter0.5。
- **直列**: F2 完走 → F5 → F20 の順。同時起動禁止（VRAM/GPU競合）。

---

## 3. encode（row-6 verbatim・PNG連番 → mp4）

各ヒーローの PNG 連番を row-6 の**確定コマンド**で焼く（**bt709 / libx264 / crf16 / yuv420p / fps30**）。出力は本編 public 配下へ。

```bash
cd /c/Users/aab15/Documents/prime-documentary

# F2 → hero_bsa_flow.mp4
npx remotion ffmpeg -framerate 30 -i out/hero_bsa_flow/f_%04d.png -c:v libx264 -crf 16 -pix_fmt yuv420p -y remotion/public/hinders/hero_bsa_flow.mp4

# F5 → hero_frozen_account.mp4
npx remotion ffmpeg -framerate 30 -i out/hero_frozen_account/f_%04d.png -c:v libx264 -crf 16 -pix_fmt yuv420p -y remotion/public/hinders/hero_frozen_account.mp4

# F20 → hero_carole_after.mp4
npx remotion ffmpeg -framerate 30 -i out/hero_carole_after/f_%04d.png -c:v libx264 -crf 16 -pix_fmt yuv420p -y remotion/public/hinders/hero_carole_after.mp4
```

- **出力先（確定）**: `remotion/public/hinders/hero_bsa_flow.mp4` / `hero_frozen_account.mp4` / `hero_carole_after.mp4`。
- 3840×2160 連番でレンダした場合、この encode で 1080p へ落とすなら `-vf scale=1920:1080:flags=lanczos` を `-c:v` の前に追加（supersample 縮小＝L3"さらに上"のエイリアス除去）。素の row-6 は解像度を変えない＝連番解像度のまま焼く。
- bt709 を明示したい場合は `-colorspace bt709 -color_primaries bt709 -color_trc bt709` を付す（HANDOFF 版準拠）。素の row-6 verbatim は色フラグ無し。
- 本編取込は §4 の `OffthreadVideo`。音声は本編mux時に aac 320k。

---

## 4. @remotion/three ヒーロー（F3 / F11 / F14 / F14b / F15）＋本編合成

これら5面は WebGL 実3D（~real-time）。**本編合成は `--concurrency=4`・CPU(libx264)固定・NVENC禁止**（GPU競合回避・instanced 301/278 で負荷高）。

- 依存: `@remotion/three@4.0.484 three @react-three/fiber@8 @types/three`＋`@remotion/motion-blur`＋`DepthImageV`。
- 決定論: すべて `useCurrentFrame()`/keyframe 駆動（r3f `useFrame` 禁止＝非決定論でCodex再現性を壊す）。seeded `mulberry32`（`Math.random` 禁止）。等速線形禁止（`spring{damping,mass}` か `Easing.out(Easing.cubic)`）。opacity単独リビール禁止（translateY/scale併用）。
- 本編 Composition id = `Ep35Hinders`（1920×1080 / fps60）。

```bash
cd /c/Users/aab15/Documents/prime-documentary

# 代表窓（ヒーロー面を含む区間）を先に実レンダして window motion_energy を実測 → その後に全編量産
npx remotion render Ep35Hinders out/ep35_hero_sample.mp4 --concurrency=4 --frames=<start>-<end>

# 全編（本番・CPU libx264・NVENC禁止）
npx remotion render Ep35Hinders out/ep35_hinders_full.mp4 --concurrency=4
```

- F3 ThresholdMeter / F11 PolicyReversalTimeline / F14 McLellanParallel / F14b McLellanLedger(301 instanced) / F15 TIGTA-Dots(278 点群)。Blender連番ヒーロー(F2/F5/F20)は `OffthreadVideo` で `remotion/public/hinders/hero_*.mp4` を取込。
- コンポーネント実装先: `remotion/src/components/hinders/`（現状 `theme.tsx` のみ。図コンポーネントは MOTIONKIT プリセット＋data props差分で **要実装**・新規フルスクラッチ禁止＝invariant14）。

---

## 5. 完成ゲート（§8・自己申告禁止・実レンダのバイト列を測る）

**手順**: `check_final_acceptance.py` → 受領書 → `preflight_owner_review.py` → オーナー提示。緩めて通すの禁止（invariant13/15・rule 19）。

```bash
cd /c/Users/aab15/Documents/prime-documentary

# 5.1 最終受領（motion_energy / image_cut_luma / body_luma / footage_utilization / check_padding 等を内包）
#     受領書 = episodes/PD-2026-035-hinders/09_package/acceptance_receipt.v001.json（video_sha256 がファイルと一致必須）
python scripts/check_final_acceptance.py PD-2026-035-hinders --render out/ep35_hinders_full.mp4 --emit-receipt

# 5.2 オーナーレビュー束（実数＋代表フレーム画像を生成。これを提示してから「完成」と言う）
python scripts/preflight_owner_review.py --ep PD-2026-035-hinders --render out/ep35_hinders_full.mp4

# 5.3 尺バンド（唯一のオーナー承認偏差になり得るハード。19.5–20.5分＝1,170–1,230s）
python scripts/check_runtime_band.py PD-2026-035-hinders
```

**実在スクリプト（確認済み・そのまま実行可）**:
- `scripts/check_final_acceptance.py` ✅（内部で motion_energy〔`scripts/measure_motion_energy.py`✅ を呼ぶ〕/ image_cut_luma / body_luma / footage_utilization / check_padding / caption_sync / bgm 等を判定・`--emit-receipt` で受領書発行）
- `scripts/preflight_owner_review.py` ✅（`--ep` 必須・`--render`・`--frames`〔既定16〕）
- `scripts/check_runtime_band.py` ✅ / `scripts/check_padding.py` ✅ / `scripts/measure_motion_energy.py` ✅
- 補助で単体実行可: `scripts/check_footage_utilization.py` ✅ / `scripts/check_image_cut_luma.py` ✅ / `scripts/check_motion_bbox_flow.py` ✅

**要実装（設計が参照するが scripts/ に不在＝別途作成が必要。無い間は手動レビュー項目）**:
- `scripts/check_flat_windows.py` ❌（平坦20秒ゼロの機械化。当面は `check_padding`＋`measure_motion_energy` の全12s窓≥8で代替）
- `scripts/check_figure_flow.py` ❌（図ROI≥30%画素≥3.5%/幅秒の機械化）
- `scripts/check_freeze_frames.py` ❌（連続40f静止=FAIL の機械化。当面 `check_final_acceptance` 内の freeze/motion 判定で代替）
- `scripts/check_image_pan_flow.py` ❌ / `scripts/check_figure_cadence.py` ❌（隣接ペア≤90s の cadence 検証）

**代表窓の実レンダ motion_energy 添付（§8・必須）**: §4 の代表窓レンダ（`out/ep35_hero_sample.mp4`）に対し `python scripts/measure_motion_energy.py out/ep35_hero_sample.mp4` を実行し、within-shot 平均≥16 / p10≥11 / 全12s窓≥8 の実測値をオーナー提示に添付してから量産へ。

**super-heavy tier 固有ゲート（§8・未コード＝手動レビュー）**:
- `hero_present`: hookウィンドウにヒーロープレート実在・`OffthreadVideo`（実レンダ・静止画でない）・1920×1080・crf≤17/yuv420p。
- 8面ヒーロー各の §SH.1 数値（手法/サンプル/解像度/カメラ/物理/ボリューメトリック/dpt振幅/パーティクル/motion blur/encode）を満たさない＝rework。
- silent cap 禁止（時間都合の skip/降格は必ずログ）。

---

## 6. 超激重負荷サマリ（§SH.5）＋ EEVEE フォールバック規律（§SH.3）

| 要素 | 手法 | 負荷 | 直列/並列 |
|---|---|---|---|
| F2 / F5 / F20 | Blender Cycles ceiling（3840→1080 supersample・200 samples） | 実効 **~30s/frame 級**・100f→**~50分/カット** | GPU占有・**1本ずつ直列** |
| F5 氷破断 / F2 流体 | 物理シム（substeps20/solver20） | **bake は render と別枠**で追加時間 | bake→render animation |
| F3 / F11 / F14 / F14b / F15 | @remotion/three 実3D | ~real-time（301/278 instanced で高負荷） | **`--concurrency=4` 厳守** |
| encode | row-6 libx264 crf16 yuv420p bt709 fps30 | 軽量 | 逐次 |

**EEVEE(L2 fast)フォールバック規律（§SH.3）**:
- Cycles ceiling が時間で間に合わない場合**のみ**、章トランジション/2番手ヒーローを EEVEE fast（`bpp_eevee.py`・taa_render_samples 96–192・use_raytracing/ssr/gtao・~1.8s/frame・aperture_fstop2.2・Glare Bloom）へ降格。
- **F2 / F5 / F20 の ceiling 3面は降格しない**（最上級の掴み）。
- **降格は silent cap 禁止＝必ずログに残す**（no silent cap）。
- 再レンダ後は `audio_mix_sha256`＋freshness 照合（偽の緑を出さない）。

---

## 7. 事実数値の不改変（再掲・非交渉）

超激重化で改変してよいのは**モーション/レンダ品質仕様のみ**。以下は**一切改変しない**:

- `$32,820.56`（押収・CLM-0002／対物訴訟名 *United States v. $32,820.56*）
- `$107,702.66`
- `301` 入金 ／ `~$2M` 累計（McLellan・CLM-0012・3年）
- `278` TIGTAサンプル ／ `91%`（件数比・合法原資・CLM-0014）
- `231` 件 `$17.1M`（合法原資没収総額・CLM-0014）
- 各 CLM ID（CLM-0002/0007/0011/0012/0014/0016/0020 ほか）
- 公聴会は本人証言を出さない（CLM-0020 grade B）。NYT一面見出しは可読ブランド書体を出さない（CLM-0007）。

---

## 付録A. 実行順チートシート

```text
0. 事前フライト（§0）: nvidia-smi / venv / blender.exe / 画像数
1. depth（§1.2）: gen_depth.py（画像 >=136 になってから本番。現状13枚=ブロッカー）
2. Blender ヒーロー静止テスト（§2.1）→ 本番連番 F2→F5→F20 直列（§2.2）
3. encode row-6（§3）→ remotion/public/hinders/hero_*.mp4
4. @remotion/three 代表窓レンダ（§4）→ motion_energy 実測（§5）
5. 全編レンダ --concurrency=4（§4）
6. check_final_acceptance --emit-receipt（§5.1）→ preflight_owner_review（§5.2）→ オーナー提示
7. 受領書 video_sha256 一致・許容ハード不合格が runtime_band のみ → 予約(upload_schedule_case_v001.py)
```

## 付録B. 既知の制約 / ブロッカー一覧

1. **元画像 ≥136 unique が未達（最大ブロッカー）**: 現状 13枚（Codex 生成継続中）。ai_prompts v002 拡張＝Codex 担当。136未満では 239 depth カバレッジ未達・`footage_utilization` ゲートも落ちる。
2. **Blender ヒーロースクリプト 2本が未実装**: `hinders_frozen_account.py`（F5）・`hinders_carole_after.py`（F20）＝別アニメスレで `bpp_physics.py`/`bpp_cycles.py` を拡張して作成。`hinders_bsa_flow.py`（F2）は実在。
3. **図コンポーネント未実装**: `remotion/src/components/hinders/` は `theme.tsx` のみ。27図は MOTIONKIT プリセット＋data props差分で要実装（新規フルスクラッチ禁止）。
4. **機械ゲート 5本が未実装（要実装）**: `check_flat_windows.py` / `check_figure_flow.py` / `check_freeze_frames.py` / `check_image_pan_flow.py` / `check_figure_cadence.py`。無い間は手動レビュー＋既存ゲートで代替。
5. **fps 正典衝突**: ASSETS §SH.0=30 / HANDOFF=60。本RUNBOOKは 30 採用。オーナー裁定が要る場合あり。
```
