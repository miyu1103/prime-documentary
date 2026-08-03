# RISK REGISTER — PD Visual System v2 (P00)

- Episode `PD-2026-009-timbs` / 2026-07-12 (JST) / by claude-code
- 目的: 新ツール導入で既存Prime Documentary環境・Python依存・素材・Gitを壊さないためのリスク台帳。
- 重大度: H=高 / M=中 / L=低。

| # | リスク | 重大 | 実測根拠/背景 | 予防・緩和 | rollback |
|---|---|---|---|---|---|
| R1 | **AI依存の混在で既存GPUスタック破壊** | **H** | torch2.0.1+cu118・open_clip等が**グローバルPython310に同居**(ENV§9)。ここへ新pip installすると既存SDXL/depth/pino系が壊れる | 新ツールは`D:\PD_AI_Tools\<tool>`の**独立venvのみ**。global/.venv/ComfyUI env は不変。導入後に既存パイプのsmokeで無傷確認 | venv削除で完全復旧 |
| R2 | **SAM2 の torch/CUDA 衝突** | **H** | SAM2は概ねtorch≥2.3/CUDA12要求、既存はcu118 | SAM2専用venvで別torch(cu121/124)。globalは触らない | venv削除 |
| R3 | **Python 3.11 が Store版** | M | 3.11.9=Microsoft Store(qbz5n…)。AppData仮想化・symlink制約でML venv/モデルキャッシュ不具合 | ツール用は**python.org 3.10/3.11をProgramsへ**（導入は§10承認）。Store版でvenvを作らない | 別Python使用に切替 |
| R4 | **モデル重みの大容量DL/課金外部** | **H** | Wan2.2/large-v3/SAM2/CLIP重み=数GB〜 | DL前に容量・展開後・保存先・ライセンスを提示し**承認**(§10)。5GB超/10GB超消費/数時間バッチは必ず事前提示 | 重み削除（`D:\PD_AI_Models`隔離） |
| R5 | **85,000点一括処理の暴走** | **H** | 素材85k点・H:\pd-media | **PoCは100〜500点**で速度/ディスク/エラー/再開性を先に計測。一括は別承認 | PoC DB削除 |
| R6 | **H:\pd-media 原本破壊/移動** | **H** | 素材ルート=読み取り専用(safety protected_paths) | 派生は`generated/previews/indexes`等の承認write rootのみ。原本read-only | 派生削除（原本不変） |
| R7 | **AI生成物を証拠として誤用** | **H** | invariant11・media-truth rule | 判決文/証拠/新聞/記録/実在人物顔・発言/正確地図/重要文字は**AI生成禁止**。全生成`review_status:review_required`＋provenance | 生成物不採用・隔離 |
| R8 | **ASR結果で台本を上書き** | M | WhisperX導入時 | **台本が正本**・ASRは整列専用・差分レポート。金額/年号/条文/事件番号/人名/地名/裁判所名はreview_required | 台本原本から再生成 |
| R9 | **紙芝居ゲートの偽の緑** | M | [[feedback_animation_still_too_little]]。P01実測でSPN-0006 motion_yavg0.87(主役が近静止) | 動きの大きさ(optical-flow/YAVG)の**正の下限**・near-still率上限・語同期を機構ゲート化 | ゲート再測定 |
| R10 | **2.5Dの穴/歪み** | M | SAM2/Depth不正確 | 背景105-110%拡大・横移動小・scale差中心・mask feather・**歪み/穴は不採用**。box対象を明示管理 | 該当カット不採用 |
| R11 | **Blender毎回新セット/カメラ合成ズレ** | M | Blender 5.x fcurves廃止・座標合成 | セット1つを再利用。四隅座標出力→Remotion変形。3f連番検証 | .blend破棄・再利用版へ |
| R12 | **既存Remotion/Node/FFmpeg破壊** | M | node_modules実版未確認(非起動) | Remotion実版はP05前に読み取り確認。npm依存追加は原則せず必要時ask。FFmpeg/Node/Blender更新は§10承認 | package変更をbackupから復旧 |
| R13 | **Git事故（push/reset/clean等）** | **H** | 未コミット 修正75/未追跡928 | commit/push/merge/rebase/reset --hard/clean は**禁止**。選択的addのみ(承認時) | backup `.pd-visual-system-backup_*`／未コミット保持 |
| R14 | **schema同名衝突未解決** | M | scene-plan/qc-report 3件(INSTALLATION_REPORT §9)。validate_kit exit1 | schemas触る前(P03+)にowner namespace解決。P00/P01/PoCには非ブロッキング | 変更せず据え置き |
| R15 | **参照チャンネル固有要素の複製** | M | P02(保留)。ブリーフ§9 | ロゴ/固有配色/セット/素材/ショット順を複製しない。**機能原理のみ**翻訳。COPY_BOUNDARYで分離 | 該当実装破棄 |
| R16 | **ディスク逼迫(C:280GB)** | L | C:空き280GB | AIツール/モデル/中間は**D:(1.5TB)・H:(3.2TB)**へ。C:に大容量を置かない | 中間削除 |

## 事前承認が必要な操作（再掲・ブリーフ§10）
5GB超DL / モデル重み取得 / 管理者権限 / 環境変数変更 / CUDA・GPUドライバ変更 / Python本体追加更新 / Node更新 / FFmpeg更新 / Blender更新 / DaVinci設定変更 / 既存ファイル上書き / 構成大幅変更 / 10GB超消費 / 数時間バッチ。提示内容=何を/なぜ/DL容量/展開後/保存先/既存影響/リスク/rollback/代替案。
