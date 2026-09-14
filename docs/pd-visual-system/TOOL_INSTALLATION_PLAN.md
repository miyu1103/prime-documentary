# TOOL INSTALLATION PLAN — PD Visual System v2

- Episode: `PD-2026-009-timbs` / Phase `P00`（計画のみ・**本Phaseでインストールしない**）
- 原則（ブリーフ§8/§9/§10 と CLAUDE.md rule 18・19 準拠）:
  - **一度に全部入れない。Phase順で導入→検証**。
  - **既存の稼働環境（グローバルPython310のGPUスタック・Remotion・ComfyUI）を壊さない。**
  - 新ツールは **`D:\PD_AI_Tools\<tool>\` の独立venv**、モデル重みは **`D:\PD_AI_Models\<kind>\`**。
  - 5GB超DL / モデル重み取得 / 10GB超消費 / 数時間バッチ は **事前承認**（§10）。
- 実測状況の要点（`ENVIRONMENT_AUDIT.md §9`）: torch 2.0.1+cu118(GPU可) / open_clip・faster_whisper・depth_anything_v2 は**導入済**、scenedetect・whisperx・sam2 は**未導入**。ComfyUI/Blender/DaVinci/FFmpeg 導入済。Python 3.11.9(Store版) と 3.10 併存。

## 0. 導入順（Phaseと1:1）
P03=PySceneDetect / P04=OpenCLIP / (P07)=WhisperX / (P08)=SAM2+DepthAnythingV2 / (P09)=Blender(既存) / (P10)=ComfyUI+動画モデル。**各Phaseは前Phaseのowner承認後にのみ着手。**

## 1. 事前確認チェックリスト（各ツール共通・ブリーフ§8）
必要Python版 / PyTorch版 / CUDA互換 / VRAM / RAM / ディスク / ライセンス / Windows対応 / CLI・API可否 / rollback / 既存衝突。各ツール節に記載。

## 2. ツール別プラン

### 2.1 PySceneDetect（P03・素材カット分解PoC）
- 状態: **未導入**。目的: 動画をカット単位に分解→開始/終了/サムネ/メタをSQLiteへ。25/50/75%代表フレーム抽出。
- 版: `scenedetect[opencv]`（最新）。Python 3.10 or 3.11。依存: 既存FFmpeg・OpenCV(cv2 4.11 導入済)。CUDA不要（CPU）。
- 保存先: `D:\PD_AI_Tools\PySceneDetect\`（venv）。DBは repo `data/*.sqlite`（gitignore済）。
- VRAM: 不要 / RAM: 小 / ディスク: venv〜0.5GB＋サムネ。DL<0.2GB（承認不要）。
- ライセンス: BSD-3（PySceneDetect）/ FFmpeg(LGPL/GPL) 既存。CLI: `scenedetect` 可。
- **PoC規模: 100〜500点のみ**（速度/精度/ディスク/エラー率/再開可否/実用性を計測）。85,000点一括は禁止。
- rollback: venv削除＋PoC DB削除。既存無影響。

### 2.2 OpenCLIP（P04・意味検索PoC）
- 状態: **導入済 2.30.0（GPU）**。目的: 代表フレームを埋め込み→英語検索文で候補抽出。
- 判断: 既にグローバルGPU env で稼働。ブリーフ§8の「隔離」に厳密に従うなら `D:\PD_AI_Tools\OpenCLIP\` に専用venvを新設し重みは `D:\PD_AI_Models\clip\`。ただし**既存で動くため、まずは既存GPU envでPoC→隔離は後日**でも可（owner選択）。
- モデル: ViT-B/32 or ViT-L/14（laion2b）。重みDL 0.3〜1.7GB（**承認要**：重み取得）。VRAM 2〜6GB。
- ライセンス: OpenCLIP=MIT / LAION重み=研究用途注意（商用可否をLICENSE_REGISTERに記録）。
- rollback: index(SQLite/npy)削除。モデルキャッシュ保持可。

### 2.3 WhisperX / faster-whisper（P07・音声同期）
- 状態: whisperx **未導入** / faster-whisper **導入済 1.2.1**。目的: 英語ナレの単語タイムスタンプ。**台本が正本・ASRで上書きしない・差分レポート**。金額/年号/条文/事件番号/人名/地名/裁判所名は **review_required**。
- 版: whisperx（align用）。torch+cu必要。**whisperx は依存ピンが厳しくグローバルと衝突しやすい**→ `D:\PD_AI_Tools\WhisperX\` 独立venv必須。代替: faster-whisper単体（導入済）で語整列を自前実装。
- モデル: large-v3 等（DL 1.5〜3GB・**承認要**）。VRAM 5〜10GB。
- ライセンス: WhisperX=BSD-4? / Whisper重み=MIT。
- rollback: venv削除。既存faster-whisperは温存。

### 2.4 SAM2 + Depth Anything V2（P08・2.5D）
- 状態: SAM2 **未導入** / DepthAnythingV2 **モジュール導入済（Small重みはP08で確認）**。目的: 人物/物体/背景分離＋Depth→前景/中景/背景を別速度で2.5D。
- **重大衝突**: SAM2 は一般に **torch≥2.3 / CUDA12** 要求。既存GPU env は torch2.0.1+cu118。→ **SAM2専用venv（別torch cu121/cu124）で隔離必須**。Depth Anything V2 は **Small のみ**（Base/Large/Giantは無条件採用しない）。
- 対象指定は丸投げ禁止。`{target_label, prompt_type:"box", box_xyxy, review_required:true}` で明示管理。初期2.5Dは背景105-110%拡大・横移動小・scale差中心・mask feather・歪み/穴は不採用。
- モデル: SAM2(sam2_hiera_*) 0.2〜0.9GB / DepthV2-Small 〜0.1GB（**承認要**）。VRAM 6〜12GB。
- ライセンス: SAM2=Apache-2.0（重みは要確認）/ DepthAnythingV2=Apache-2.0（Small）。**各重み・custom nodeを個別にLICENSE_REGISTERへ**。
- rollback: venv＋派生png削除。原本不変。

### 2.5 Blender（P09・PD Evidence Room）
- 状態: **導入済 5.1**。目的: 再利用可能な「PD Evidence Room」1セットを作り**繰り返し使う**（毎回新セット禁止）。カメラ8種、暗い青/黒/銀照明。
- Remotion合成: カメラ移動中はCSS固定座標で無理に貼らず、**Blenderからフレーム毎スクリーン四隅座標を出力→Remotionで変形**。
- 版注意: Blender 5.x は `Action.fcurves` 廃止（`_act_fcurves`ヘルパー）・単フレームsmoke検証は連番バグを見逃す（3f連番で検証）。4K/200≈44s/frame。
- ライセンス: Blender=GPL（成果物は自作アセット）。DL不要（導入済）。
- rollback: .blend/連番は outputs/renders へ隔離出力。既存無影響。

### 2.6 ComfyUI + 動画モデル（P10・AI B-roll のみ）
- 状態: ComfyUI **導入済**。目的: 既存/2.5D/Remotion/Blenderで**不足する短いB-rollだけ**（雨/煙/光/警察灯/街/通路等・**読める文字なし**）。
- モデル: Wan2.2系のRTX4090現実解（量子化/オフロード）。**重みDL大（承認要・5GB超想定）**。VRAM 12〜24GB。
- **AI動画で作らない**: 判決文/証拠/読める新聞/事件記録/実在人物発言・顔/精密な事件再現/正確地図/重要文字。全生成に model/licenses(重み・custom node)/prompt/neg/seed/steps/res/duration/日時/file/review理由 を保存、初期 `review_status:"review_required"`。
- A1111/ComfyUIのVRAM競合注意（同時フルロード禁止・`unload-checkpoint`）。
- rollback: 生成物は H:\pd-media\generated（承認write root）へ・不採用は隔離。

## 3. Remotion コア5部品（P05・コード側＝インストール不要）
`EvidenceReveal / PenaltyVsProperty / CaseJourney / QuoteUnderExamination / VerdictReversal` のみ。別名はalias（DocumentReveal→EvidenceReveal 等・`config/pd-visual-system/component-registry.json`）。16:9/1920×1080/30fps/duration耐性/props(内容・速度・位置・強度)/seed固定/セーフエリア/事件名ハードコード禁止/英語本番＋日本語確認別データ/preview低負荷/語タイムスタンプ連携。**新規npm依存は原則不要**（既存 remotion/@remotion/motion-blur/three で足りる。追加時はrule準拠でask）。

## 4. インストール時の共通ガード
- venv作成→`pip install`（**ask対象**＝安全ゲートで承認）→ 版固定を requirements に記録。
- モデルDL は保存先・容量・ライセンスを提示して**承認後**（§10）。
- 既存グローバルPython310・.venv・ComfyUI env は**変更しない**（新venvのみ）。
- 各導入後に「動く最小PoC」で検証してからPhase成果に進む。

## 5. 未確定・要owner決定
1. OpenCLIP を既存GPU envで使うか完全隔離するか。
2. Python 3.11 は Store版でなく python.org 版を `D:\PD_AI_Tools` 用に入れるか（Store版はML venv非推奨・§RISK）。
3. WhisperX を正式採用か faster-whisper 自前整列で足すか。
4. 各モデル重みの商用ライセンス可否（LICENSE_REGISTER 記録）。
