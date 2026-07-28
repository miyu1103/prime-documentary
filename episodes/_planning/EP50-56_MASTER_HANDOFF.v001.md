# EP50–56 MASTER HANDOFF (v001, 2026-07-29 03:00) — 新スレ再開用

このスレ（複数日・エージェント枠200使い切り）を閉じ、**新セッションで大量並列＋クリーン文脈**で再開するための完全引継ぎ。目的は **時短ではなく最高品質＋失敗ゼロ＋CTR/維持率/登録者/再生数の最大化**（オーナー 2026-07-29）。Repo `C:\Users\aab15\Documents\prime-documentary`、Media `H:\pd-media`、branch `claude/vibrant-archimedes-2mmr5h`、channel `UCuQPtAz1rca9eJ4xhvX0yKA`。

## 0. 最初に必ず読む
- 記憶 `C:\Users\aab15\.claude\projects\C--Users-aab15-OneDrive-Desktop\memory\MEMORY.md`（特に **feedback-no-render-churn / feedback-lessons-must-be-gates / feedback-verify-dont-assume / feedback-top-1-percent-not-average / pd-retention-rules / pd-opening-formula / pd-craft-checklist / feedback-work-without-stopping / feedback-codex-one-shot-images**）
- `episodes/_planning/PD_IRONCLAD_GATES.v001.md`（鉄壁ゲート）、`BUILD_RESUME_HANDOFF.v001.md`、`EP51-56_FACES_CODEX_SPEC.v001.md`

## 1. EP50 は完成（触らない）
- **`episodes/PD-2026-050-centralpark/08_edit/EP50_FINAL.mp4` = v006**（肌クリーン・BGM・pre/postゲート通過・視覚QC済み）。61分/3663.8s。
- 経緯：肌の傷/シミ再作業→人物76枚肌クリーン再生成→**73/76 i2v**（最後3人はクラッシュ多発で打ち切り＝完成品に影響なし）→motion-first film.json（v003マニフェスト）→レンダー→BGM(v006)。
- **未解決（任意・品質up）**：AE合成版 `centralpark_final_bgm.v006_ae.mp4` が **黒6秒（video 131.5–138.5s）** を含みFAIL。原因ビート＝**B8（layout=HERO_TIMELINE, start=120, cp=CP03）**。AEビート素材 `08_edit/ae_hero/render/B1..B12.mp4` は生成済み・beats.json は `08_edit/ae_hero/beats.json`（36ビート）。B8合成が黒を入れている→ここだけ直せばAE版が復活。**やるなら品質重視で直す；不要ならv006で確定でよい。**
- 旧AE版 v005_ae（傷あり顔）は retired。

## 2. EP51–56 の素材状況（実測・2026-07-29）
共有stock動画 74本 `H:/pd-media/assets/stock/video`（全話再利用可）。**顔はCodex生成済み（P##）**。
| EP | slug | 尺 | 静止画S | i2v元M_src | 顔P(+T) | **i2v動画(実)** | asset_manifest |
|----|------|----|--------|-----------|---------|----------------|----------------|
| 51 | willingham | 20分 | 150 | 30 | **32** | **0** | なし |
| 52 | morton | 30分 | 215 | 43 | 16(+3) | **71** ◎最良 | v001のみ |
| 53 | norfolk | 30分 | 205 | 42 | 16(+3) | **0** | なし |
| 54 | flowers | ~ | 210 | 44 | 16(+3) | **44**(RIFE) ○ | v001のみ |
| 55 | burge | 30分 | 210 | 42 | 16(+3) | **0** | なし |
| 56 | postoffice | ~ | ~ | ~ | 16(+3) | **0** | v001のみ | UK設定 |
- 黒スタブ0・真っ黒ほぼ0（EP53 S155だけ暗め）。純画像素材はOK。
- **最も組み立てに近い＝EP52 morton（i2v71）＋EP54 flowers（i2v44）。まずこの2本を出せる。**

## 3. 各話ビルドに必要な"足場"（現状ほぼ未整備＝新スレの主タスク）
build スクリプトは `scripts/build_centralpark_film.py` が**テンプレ**。必要入力（EP50実績）：
1. `06_audio/narration_index.v001.json` — 生成には `03_script/script.annotated.v001.json` が要る（**全話 未整備**）。annotated 生成は `scripts/build_kidsforcash_annotated.py` がテンプレ（script.en + facts.json → annotated）。VCチャンク `06_voice/draft/VC-*.json` は section+seconds は持つが **text は持たない**（キャプション文は script.en から）。
2. `04_scenes/<slug>_beatsheet.v001.json` + `<slug>_build_manifest.v001.json` — EP50の `centralpark_beatsheet.v001.json`/`centralpark_build_manifest.v001.json` が構造テンプレ。
3. `05_visuals/asset_manifest.v003.json` — motion-first。`scripts/build_centralpark_manifest_motionfirst.py` がテンプレ。**P##顔を people/motion プールに必ず入れる**。morton/flowers/postoffice は `scripts/build_<slug>_asset_manifest.py` が既存。
4. `scripts/build_<slug>_film.py` — centralpark をクローンし全パス差し替え。**必ず保持**：`treatments=["bleed","duotone","focus"]`（depth/scan/card禁止＝ワープ/走査線）、`_split_caption_text`（字幕2行）、`SECTION_TARGETS` を尺に合わせスケール、`repeated()` motion-first、`DEFAULT_ASSETS=asset_manifest.v003.json`（v001ではない！）、P##globを people プールへ。
5. `08_edit/ae_hero/beats.json` — 台本の山場からAEヒーローカードを作成。
→ 生成後：`build_<slug>_film.py` → `remotion/src/data/<slug>_film.json` → **プリゲート**。

## 4. GPU工程（1枚4090・直列。長時間は必ず background）
- i2v が要るのは **EP51/53/55/56（0本）**。M_src + 顔P## を Wan i2v。ドライバ `C:/Users/aab15/ae-demo/comfy_wan.py`（ComfyUI :8188）、バッチ `scripts/i2v_centralpark_batch.py`（**skip判定は `ae-demo/wan_frames_cp_<n>/` を見る＝修正済み**、`I2V_MAX` でチャンク実行可）、堅牢チェーン `scripts/_chain_ep50_rei2v_robust.sh`（**単一インスタンスlock＋I2V_MAX時はチャンク毎に新ComfyUI**）。**必ず** `pd_gpu_lock.py i2v`（webUI VRAM解放）→ i2v。監視 `pd_watchdog.py`。
- レンダーは **`scripts/pd_render_guarded.sh <compId> <film.json> remotion/public_slim <out.mp4> <expect_sec>`** のみ（pre-gate→GPU確認→render→post-gate、不合格でブロック）。
- BGM `scripts/build_<slug>_bgm_real.py`（centralparkテンプレ）→ AE合成 `scripts/ae/composite_<slug>_hero.py`（centralparkテンプレ、**合成後は必ず別途post-gate**＝黒/フリーズ混入注意）。

## 5. 絶対に繰り返さない失敗（このスレで踏んだ11個＋メタ）
記憶 **feedback-no-render-churn** に全記載。要点：
1. **90秒超のジョブは必ず background**（フォアグラウンドは2分でkillされ部分ファイル量産）。
2. **カウント/スキップは実際の出力パスを検証してから信用**。
3. **versioned成果物を作り直したら読み手を全部grep**（v001/v003取り違え）。
4. **見積もりは最大の未着手工程基準・控えめに**（3hレンダー未着手で「4h」は誤り）。
5. **AE合成後は別途ゲート**（黒/フリーズ混入）。
6. **長時間i2vは最初からチャンク+新comfy+lock+watchdog**（GPU連続劣化でクラッシュ）。
7. **ship-then-inspect 禁止＝レンダー前に全ゲート、見せる前にpost-gate+全編視聴、欠陥は一括修正して1回のレンダー**（EP50は6回再レンダーで2日溶かした）。
メタ：**注意点は150〜200把握・でも全部ではない→①検証で未知を炙り出す②新規=即ゲート化。記憶頼みにせず機械ゲートで強制。**

## 6. 新スレでやること（並列エージェント前提）
1. **失敗レジストリ統合＋プリフライト**（散在ルールを1本の網羅チェックへ）。
2. **EP51–56 を1話1エージェント＋各話内並列**で：足場構築（§3）→ i2v（§4, 必要な4話）→ pre-gate → guarded render → BGM → AE合成 → post-gate → **全編視聴QC**。全ゲート（motion-first≥62%・ワープ禁止・字幕2行・肌クリーン・維持率/CTR/craft/opening formula）適用。
3. まず **morton→flowers**（i2vあり＝最速で出せる）、並行で残り4話の i2v をチャンクバッチ。
4. **スケジュール/公開はしない**（オーナーが最終確認）。
5. 時短より品質。ただし churn（無意味なやり直し）はしない＝検証しながら。

## 7. 開いている判断（オーナー確認待ち・急がない）
- EP50 の AE黒（B8）を直してAE版に差し替えるか、v006（AE無し）で確定か。
- i2v無し4話：フル i2v で最高品質か、stock多用で i2v 削減か（品質/時間トレードオフ）。デフォルトは**品質優先＝i2v生成**。
