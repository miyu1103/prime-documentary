# P00 ENVIRONMENT AUDIT — PD Visual System v2

- Episode: `PD-2026-009-timbs`
- Phase: `P00` (環境・リポジトリ監査)
- Audited at: 2026-07-12 (JST) by `claude-code`
- Method: read-only measurement only. No install / no upgrade / no download / no render / no write to `H:\pd-media`.
- 下記の数値は **実測値**（コマンド出力に基づく）。証拠コマンドは §7。

## 1. ハードウェア / OS

| Item | Verified value | Evidence |
|---|---|---|
| OS | Microsoft Windows 11 Pro 10.0.26200 (Build 26200, 64-bit) | `Get-CimInstance Win32_OperatingSystem` |
| CPU | 13th Gen Intel Core i9-13900KF, 24 cores / 32 logical | `Get-CimInstance Win32_Processor` |
| RAM | 127.8 GB | `Win32_ComputerSystem.TotalPhysicalMemory` |
| GPU | NVIDIA GeForce RTX 4090 | `nvidia-smi` |
| VRAM | 24564 MiB (≈24 GB) | `nvidia-smi --query-gpu=memory.total` |
| GPU driver | 591.86 | `nvidia-smi` |
| CUDA (driver max) | 13.1 | `nvidia-smi` header |
| CUDA toolkit (nvcc) | release 11.8, V11.8.89 | `nvcc --version` |

> 注意: `Win32_VideoController.AdapterRAM` は 4GB と誤報（32bit DWORD 上限の既知バグ）。実VRAM は `nvidia-smi` の 24564 MiB が正。
> 注意: ドライバが公開する CUDA は 13.1、ローカル導入済みの CUDA **Toolkit** は 11.8。将来 GPU-Python（P08/P09 等）を入れる場合はこの差を前提にする（本Phaseでは何もインストールしない）。

## 2. ドライブ / 容量

| Drive | Size | Free | Label | 役割 |
|---|---:|---:|---|---|
| C: | 1861.8 GB | 280.4 GB | (system) | OS / リポジトリ / venv |
| D: | 1863.0 GB | 1548.4 GB | — | Node.js (`D:\Tools\nodejs`) 等 |
| E: | 1863.0 GB | 1577.2 GB | — | 空き大 |
| F: | 1863.0 GB | 1548.4 GB | — | 空き大 |
| H: | 3725.9 GB | **3222.7 GB** | T7 (外付SSD) | `H:\pd-media`（メディア実体） |

- `H:\pd-media` 存在: **True**。top-level = `assets / brand / downloads / episodes / library`。
- リポジトリ本体（`C:\Users\aab15\Documents\prime-documentary`）は C: 上。C: 空きは 280 GB。将来Phaseで大容量PNG中間・長尺レンダを出す場合は出力先を H: 承認root か E:/F: に逃がす検討余地（**本Phaseでは変更しない・監視項目**）。

## 3. ツールチェーン（実測バージョン）

| Tool | Version | Path / 備考 |
|---|---|---|
| Python | 3.10.11 | `...\Programs\Python\Python310\python.exe`（INSTALLATION_REPORT のkit検証も 3.10.11） |
| Node.js | v24.16.0 | `D:\Tools\nodejs\node.exe` |
| npm | 11.13.0 | PATH |
| pnpm | 9.12.0 | 利用可（Remotionは npm 前提だが pnpm も存在） |
| Git | 2.55.0.windows.2 | — |
| FFmpeg | 8.1.1-full_build (gyan.dev) | `...\WinGet\Links\ffmpeg.exe` |
| ffprobe | 8.1.1-full_build (gyan.dev) | 同上 |
| Remotion | `remotion` / `@remotion/cli` `^4.0.0`（`@remotion/motion-blur` `^4.0.476`, `@remotion/three` `^4.0.476`, `three` `^0.185.1`, `@react-three/fiber` `^8.18`） | `remotion/package.json`（依存**宣言**。node_modules 実バージョンは非起動のため未確認＝§8リスク3） |

## 4. 追加ソフトの存在確認（存在確認のみ・起動しない）

| Software | Present | 証拠 |
|---|---|---|
| DaVinci Resolve | Yes | `C:\Program Files\Blackmagic Design\DaVinci Resolve\Resolve.exe` = True |
| Blender 5.1 | Yes | `C:\Program Files\Blender Foundation\Blender 5.1\blender.exe` = True（PATH未登録＝フルパス起動） |
| ComfyUI | Yes | `C:\Users\aab15\ComfyUI` 存在 |

> PD の編集・レンダは正典上 **Remotion + FFmpeg (CPU/libx264)**（CLAUDE.md §11, VIDEO_RULES §8）。DaVinci は存在するが常用ラインではない。

## 5. Remotion / レンダ設定（正典値・実測）

`remotion/remotion.config.ts`（実測）:
- 中間フレーム: **PNG**（ロスレス） / コーデック: **h264 (libx264 / CPU)**, `x264Preset=slow`, **CRF=16**
- pixelFormat: **yuv420p** / colorSpace: **bt709** / 音声: **AAC 320k**
- 並列: `os.cpus().length`（=32） / Chromium OpenGL: **angle**
- `Config.setOverwriteOutput(true)`（出力上書き有効。**published mp4 は再レンダしない**＝invariant 6・configコメントに明記）

`remotion/src/brand.ts`（正典）: `video = {fps: 30, width: 1920, height: 1080}`、thumb 1280×720。

> **重要な整合メモ:** ルート `C:\Users\aab15\CLAUDE.md`（動画オープニング設計ルール）は **fps60** を規定するが、これは別プロジェクト（pino-channel / 汎用OP kit）の規約。**本プロジェクト prime-documentary の長尺は fps30**（`brand.ts` + `VIDEO_RULES.md §7`）が正典。source-of-truth 階層（PD CLAUDE.md §5）に従い、PD作業では **fps30 を正**とする。矛盾ではなく適用範囲の違いとして記録。

## 6. ネットワーク / 外部依存（本Phaseで未使用）

- 外部送信・有料API・DL・アップロードは **一切実行していない**。
- `pd_safety_gate.py`（PreToolUse）＋ `guard_destructive.py` が有効。`.claude/pd-safety-policy.json` の ask/deny 正規表現がインストール・DL・push 等を承認ゲートに掛ける。

## 7. 実行した証拠コマンド（読み取りのみ）

```
git rev-parse --abbrev-ref HEAD                      # claude/vibrant-archimedes-2mmr5h
git log -1 --oneline                                 # 97dd18df EP34 rolin: schedule ...
python/node/npm/pnpm/git --version ; ffmpeg -version ; ffprobe -version
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv
nvidia-smi (CUDA header) ; nvcc --version
Get-CimInstance Win32_OperatingSystem|Win32_Processor|Win32_ComputerSystem|Win32_VideoController|Win32_LogicalDisk
Test-Path 'H:\pd-media' ; Get-ChildItem 'H:\pd-media' -Directory
Test-Path <DaVinci/Blender exe> ; Get-ChildItem C:\Users\aab15\ComfyUI
ffprobe <timbs_premium_review_v001.mp4>              # 詳細は REPOSITORY_AUDIT.md §5
```

## 8. 環境リスク（P01以降への申し送り）

1. **C: 空き 280 GB**：PNG中間＋長尺レンダで逼迫しうる。将来Phaseの大容量中間は H: 承認root / E: / F: へ。（P00未対応・監視）
2. **CUDA Toolkit 11.8 vs driver 13.1**：GPU-Python（深度・Blender bake・P08/P09）導入時に版整合が要る。本Phaseは未インストール。
3. **Remotion 実インストール版が未確認**：`node_modules` 実バージョンは Studio/render 起動で確定（本Phaseは非起動）。宣言は `^4.0.0`。P01で `npx remotion versions` 等の読み取り確認を推奨。
4. **fps 規約の二重ソース**（§5）：作業者が fps60 ルールを誤適用しないよう本書に明記済み。
5. **VRAM WMI 誤報**：自動監査が `AdapterRAM` を読むと 4GB と誤る。`nvidia-smi` を正とする。

## 9. AI ツール導入状況の監査（新ブリーフ項目15-20・実測）

### 9.1 Python 環境（重要）
| env | パス | torch | GPU AI ライブラリ | 位置づけ |
|---|---|---|---|---|
| **base Python310** | `...\Programs\Python\Python310\python.exe`（`python` 既定） | **2.0.1+cu118（CUDA=True）** | open_clip 2.30.0 / faster_whisper 1.2.1 / depth_anything_v2 / cv2 4.11.0 / onnxruntime 1.23.2 / numpy 1.26.4 | **既存のGPU AIスタック（SDXL/depth/pino系）が同居** |
| Python 3.11.9 | `...\WindowsApps\...Python.3.11...`（**Microsoft Store版**） | 未確認 | 未確認 | Store版はサンドボックス制約でMLのvenv/モデルキャッシュに難あり（§RISK） |
| project `.venv` | `prime-documentary\.venv\Scripts\python.exe` | **2.12.1+cpu**（GPU無） | open_clip/scenedetect/whisperx いずれも absent | 別用途の軽量CPU env |

> **含意**：ブリーフ§8「既存環境にAI依存を混ぜるな・独立venv」に対し、**現状は GPU AIスタックがグローバルPython310に同居済み**（＝すでに一部混在）。新ツールは触らずに **D:\PD_AI_Tools\<tool>\ の新規venvへ隔離**する（詳細=`TOOL_INSTALLATION_PLAN.md`）。既存の稼働中グローバル環境は壊さない。

### 9.2 ツール別 存在確認（実測）
| ツール | 状態 | 実測根拠 | 保存先(現/推奨) |
|---|---|---|---|
| FFmpeg / ffprobe | ✅ 8.1.1 | `-version` | WinGet Links |
| SQLite | ✅ | Python 標準 `sqlite3` | - |
| PySceneDetect | ❌ 未導入 | `import scenedetect` = absent / CLI なし | 推奨 `D:\PD_AI_Tools\PySceneDetect`(venv) |
| OpenCLIP | ✅ 2.30.0（GPU） | base Python310 | 現=global / 推奨 隔離 or 既存GPU env流用 |
| WhisperX | ❌ 未導入 | `import whisperx` = absent | 推奨 `D:\PD_AI_Tools\WhisperX`(venv) |
| faster-whisper | ✅ 1.2.1 | base Python310 | global（fallback可） |
| SAM2 | ❌ 未導入 | `import sam2` = absent | 推奨 `D:\PD_AI_Tools\SAM2`(venv・torch別) |
| Depth Anything V2 | ✅ モジュール有 | `depth_anything_v2` import 可 | global（**Small重み存在はP03で要確認**） |
| ComfyUI | ✅ フル導入 | `C:\Users\aab15\ComfyUI`（comfy/ app/ api_server 等） | 現状のまま |
| Blender | ✅ 5.1 | `...\Blender 5.1\blender.exe` | Program Files |
| DaVinci Resolve | ✅ | `Resolve.exe` | Program Files |

- `D:\PD_AI_Tools` / `D:\PD_AI_Models` は **未作成**（D:空き1.5TB＝推奨保存先として好適）。
- GPU/CUDA整合: 既存 torch **cu118** と nvcc **11.8** は一致。**SAM2 は一般に torch≥2.3/CUDA12系**を要し **cu118 と衝突**→ 独立venvで別torch（§RISK / §PLAN）。
