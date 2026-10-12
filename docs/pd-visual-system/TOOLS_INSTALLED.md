# AI TOOLS — installed status (isolated venvs on D:)

> 2026-07-12 実測。全て `D:\PD_AI_Tools\<tool>\.venv`（既存 global Python310 / project .venv / ComfyUI に非干渉・各段階で無傷を検証）。

| Tool | venv torch / GPU | 状態 | 用途/Phase |
|---|---|---|---|
| PySceneDetect 0.7 + opencv 5.0.0 | (CPU) | ✅ 稼働（P03実証） | 素材カット分解 (P03) |
| OpenCLIP ViT-B/32 laion2b | 既存 global310 (torch2.0.1+cu118) 流用・重み605MB→D:\PD_AI_Models\clip | ✅ 稼働（P04実証） | 意味検索 (P04) |
| **SAM2** (2.1 hiera) | **2.5.1+cu121・CUDA=True** | ✅ GPU稼働 | 前景分離 2.5D (P08) |
| **Depth Anything V2** venv | **2.0.1+cu118・CUDA=True** | ✅ GPU（Small重みはP08取得） | 深度 2.5D (P08) |
| **WhisperX** | 依存地獄（3.8.6×torch2.8 / 3.1.1×torch2.1.2×新transformers `_pytree` 不整合） | ❌ align不能→**採用見送り** | — |
| **faster-whisper 1.2.1**（WhisperX venv同梱／global） | ctranslate2（torch非依存） | ✅ **P07で採用**（語タイムスタンプ） | 語同期 (P07) |

## 学び（機構化）
- **`pip install whisperx`（版未固定）は torch を CPU 2.8.0 で上書き＋align破綻**。→ **必ず版固定**（whisperx==3.1.1 + torch cu118）。P07_PLAN.md に反映済。
- SAM2 は torch≥2.3/cu121 が必要（既存cu118と衝突）→ 独立venvで別torch（RISK R2 の実証）。
- 機能スモーク（load_align_model / import）を**インストール直後に必ず走らせる**（importだけでは実害を見逃す＝今回 whisperx importはOKだが align で失敗）。

## 未取得（各Phaseで §10 承認のうえ取得）
- whisper large-v3 重み (P07・~3GB) / Depth-Anything-V2-Small 重み (~99MB, Apache) / SAM2 checkpoint / Wan2.2 動画モデル (P10・数十GB＝要明示承認)。
