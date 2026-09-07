# ショート画像 品質ディレクティブ（商用OK・最高品質）

Owner directive (2026-07-05)。**基本はショート（縦9:16）向けの標準**。
長尺エピソードの画像は原則これまで通り **Codex** で作る（rule 19）。ただしオーナー明示許可(2026-07-05)により、下記の商用OK高品質ローカルは**長尺でも例外的に使用可**：(a) Codexが作った画像の修正・手直し、(b) 不足画像の緊急追加。詳細は末尾「長尺での例外的使用」。

## 結論（何を使うか）

ショートのAI画像は、**商用利用OKなモデルだけ**を使い、下記のチューニング済みパイプラインで生成する。
「生成できた」ではなく「品質ゲート通過」が使用可否（CLAUDE invariant 13）。
**第一選択＝SD3.5 Large（1）／フォールバック＝SDXL gen_max.ps1（2）。** どちらも商用OK。

### 1) 第一選択：SD3.5 Large（商用OK・SDXL超え・2026-07-05 検証済み昇格）

`C:\Users\aab15\ComfyUI` の SD3.5 Large（fp8・全部入り14GB）を第一選択とする。
ライセンス＝Stabilityコミュニティライセンス（年商$1M未満は商用可）。RTX4090で1枚~45秒。

生成（プロンプト差し替えで量産・縦ショートはW768 H1344）:
```powershell
cd C:\Users\aab15\ComfyUI
.\venv\Scripts\python.exe sd35_gen.py "<英語プロンプト>" "<出力先>.png" <seed> 768 1344 32 4.5
```
起動前提: ComfyUI API(8188)稼働。停止中なら
`cd C:\Users\aab15\ComfyUI; .\venv\Scripts\python.exe main.py --port 8188`（venv直起動）。

**⚠️VRAM競合（必読）**: ComfyUI(SD3.5)とA1111(7860)は同じ4090・24GBを取り合う。両方フルロードするとサンプリングが0%で停止する。SD3.5で作るなら、A1111側のVRAMを先に解放してから回す:
`Invoke-RestMethod -Method Post http://127.0.0.1:7860/sdapi/v1/unload-checkpoint`（A1111プロセスは維持・次回自動再ロード）。逆にA1111(gen_max)を使う番なら、ComfyUIを起動しっぱなしにしない。

### 2) フォールバック：SDXL gen_max.ps1（商用OK・ready）

SD3.5が使えない時（ComfyUI未起動・A1111が別用途でVRAM占有中など）は、チューニング済みSDXLを使う。素の txt2img は直接呼ばない。
```powershell
& "C:\Users\aab15\stable-diffusion-webui\gen_max.ps1" -Prompt "<英語プロンプト>" -Orient short -Out "<出力先>.png"
# -NoADetailer(人物なし) / -Premium(DAT x4高精細) / -Model juggernaut|realvis(どちらも商用OK)
```
固定設定: clip_skip1 / SDXL-VAE / ADetailer顔+目2パス / Hires R-ESRGAN 4x+ / DPM++ 2M SDE Karras / steps32 CFG5。
起動: A1111 API(7860)。停止中なら `& ".\venv\Scripts\python.exe" launch.py --api --no-half-vae --xformers`（venv直・batは不可）。
商用OKモデル: JuggernautXL Ragnarok / RealVisXL V5.0 フル版。

## 長尺での例外的使用（2026-07-05 オーナー許可）

長尺の本編画像は**原則 Codex**（rule 19）。ただし次の2ケースに限り、商用OK高品質ローカル（SD3.5 `sd35_gen.py` 第一 / SDXL `gen_max.ps1` フォールバック）を使ってよい：
- **(a) Codex画像の修正・手直し**（顔の破綻直し・部分描き直し・高精細化など。img2img/ADetailer/Hiresで整える）
- **(b) 不足画像の緊急追加**（Codexの生成が間に合わない/欠けたコマを埋める）

制約（長尺の不変条件はすべて適用）:
- 素のSDXLは不可（必ず gen_max.ps1 か sd35_gen.py 経由）。**FLUX-devは長尺でも不可**。
- 実在人物の肖像は不可（invariant 11）。AI画像は開示・権利manifest・provenance・ブランド整合を長尺の既存フローに載せる。
- 「原則Codex」は維持。上記(a)(b)以外で長尺画像をローカル生成に置き換えない。

## 禁止（重要）

- ❌ **FLUX.1-dev は使用禁止**。高品質だが**非商用ライセンス**。収益化チャンネルの動画に出力を使うと規約違反。
  ローカルに `ComfyUI\models\diffusion_models\flux1-dev-fp8.safetensors` があっても、**参考・比較検証専用**。ショート／長尺いずれの成果物にも入れない。
- ❌ 素のSDXLを既定設定（clip_skip2・VAEなし・ADetailerなし・Hiresなし）で回して貼らない。必ず gen_max.ps1 を通す。

## 不変条件（既存ルールの再掲）

- 実在人物の肖像は不可（invariant 11）。AI画像は開示・権利追跡・ブランド整合。
- 素材の被り禁止（footage_diversity）。ショート内・話またぎとも。
- 商用可否が不明なモデル／LoRAは、ライセンス確認前に使わない。
