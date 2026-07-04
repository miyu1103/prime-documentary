# ショート画像 品質ディレクティブ（商用OK・最高品質）

Owner directive (2026-07-05)。**この文書はショート（縦9:16）制作スレッド向け**。
長尺エピソードの画像方針は変更しない（長尺は従来どおり Codex のみ / rule 19）。

## 結論（何を使うか）

ショートのAI画像は、**商用利用OKなモデルだけ**を使い、下記のチューニング済みパイプラインで生成する。
「生成できた」ではなく「品質ゲート通過」が使用可否（CLAUDE invariant 13）。

### 1) 現時点で使う正典パイプライン（ready・商用OK）

RTX4090ノードのローカルSDXLを、以下の**チューニング済みラッパー**経由で叩く。素の txt2img を直接呼ばない。

```
C:\Users\aab15\stable-diffusion-webui\gen_max.ps1
```

固定で効く設定（微妙画像の主因を全部潰してある）:
- clip_skip=1（SDXLの正。2は誤設定）
- SDXL専用VAE `sdxl_vae_fp16fix.safetensors`
- ADetailer 顔+目 2パス自動（人物の破綻を防ぐ決定打）
- Hires.fix R-ESRGAN 4x+ 2x / DPM++ 2M SDE / Karras / steps32 / CFG5

縦ショート生成コマンド例（9:16）:
```powershell
& "C:\Users\aab15\stable-diffusion-webui\gen_max.ps1" `
  -Prompt "<英語プロンプト>" -Orient short -Out "<出力先>.png"
# 人物なしの図なら -NoADetailer / さらに高精細なら -Premium(DAT x4)
# モデルは -Model juggernaut(既定) / realvis どちらも商用OK
```
起動前提: A1111 API(7860)が稼働していること。停止中なら
`& ".\venv\Scripts\python.exe" launch.py --api --no-half-vae --xformers`（venv直起動。batは不可）。

商用OKモデル（このノードに導入済み）: JuggernautXL Ragnarok / RealVisXL V5.0 フル版。

### 2) 近日昇格：SD3.5 Large（商用OK・SDXL超え・準備中）

`C:\Users\aab15\ComfyUI` に SD3.5 Large を導入中（Stabilityコミュニティライセンス＝年商$1M未満は商用可）。
**検証で緑になり次第、ショートの第一選択をSD3.5 Largeに昇格する**。それまでは上記(1)を使う。
（本文書は準備が整った時点で更新する。現時点で「SD3.5が使える」と仮定しない。）

## 禁止（重要）

- ❌ **FLUX.1-dev は使用禁止**。高品質だが**非商用ライセンス**。収益化チャンネルの動画に出力を使うと規約違反。
  ローカルに `ComfyUI\models\diffusion_models\flux1-dev-fp8.safetensors` があっても、**参考・比較検証専用**。ショート／長尺いずれの成果物にも入れない。
- ❌ 素のSDXLを既定設定（clip_skip2・VAEなし・ADetailerなし・Hiresなし）で回して貼らない。必ず gen_max.ps1 を通す。

## 不変条件（既存ルールの再掲）

- 実在人物の肖像は不可（invariant 11）。AI画像は開示・権利追跡・ブランド整合。
- 素材の被り禁止（footage_diversity）。ショート内・話またぎとも。
- 商用可否が不明なモデル／LoRAは、ライセンス確認前に使わない。
