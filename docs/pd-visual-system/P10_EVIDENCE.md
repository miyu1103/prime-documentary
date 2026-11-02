# P10 EVIDENCE — C2版 AI動画（Wan2.2・短B-rollのみ）

- Phase `P10` / by claude-code / 2026-07-12 (JST) / owner「全て承認」

## 用途と禁止（厳守）
- **AI動画は「実写/2.5D/Remotion/Blenderで埋められない短いB-rollの穴」だけ**（雨・煙・光・警察灯・街・通路・読める文字を含まない雰囲気カット）。
- **禁止**: 判決文・証拠書類・読める新聞・事件記録・実在人物の顔/発言再現・精密な事件再現・正確地図・重要文字。
- **timbs 80秒テスト区間はAI動画不要**（実写＋コア5＋2.5Dで充足）＝本Phaseは**枠組み＋provenance＋モデル導入**を確立し、実生成は将来の穴埋め用途で運用。

## モデル（RTX4090現実解・DL承認済）
- **Wan2.2 TI2V-5B**（720p・24fps・4090可）。`Comfy-Org/Wan_2.2_ComfyUI_Repackaged`:
  - diffusion_models/`wan2.2_ti2v_5B_fp16.safetensors`
  - text_encoders/`umt5_xxl_fp8_e4m3fn_scaled.safetensors`
  - vae/`wan2.2_vae.safetensors`
  → `C:\Users\aab15\ComfyUI\models\{diffusion_models,text_encoders,vae}`（計~20-25GB・**背景DL中**）。
- 生成は ComfyUI(8188) native Wan2.2 ワークフロー。A1111/SD3.5とVRAM競合注意（`unload-checkpoint`）。

## provenance（全生成に必須・初期 review_required）
model / model_license / weights_license / custom_node_license / prompt / negative_prompt / seed / steps / resolution / duration / 生成日時 / 生成ファイル / review_status="review_required" / 採否理由。→ `MODEL_LICENSE_RECORD.md` と生成ごとのJSONに記録。**自動採用しない・人間採否**。

## 状態（正直）
- モデルDL＝**背景実行中（~22GB）**。DL完了後に ComfyUI API で1本の雰囲気B-roll（例: 夜の雨/煙）を生成し provenance 記録＝実生成の実証。
- 枠組み・用途制約・provenance規則・モデル選定・DL は確立済。**テスト区間には不要**のため P11/P12 は先行。

## rollback / 次
- rollback: ComfyUI models配下のWan2.2ファイル削除。既存に非干渉。
- 次 P11 = C3版（音・色仕上げ）。
