# 25 — Cross-machine Windows / Mac Workflow

## 1. 目的

RTX 4090生成機とMac編集機を、共有フォルダで雑につなぐのではなく、一つの分散制作システムとして扱う。

## 2. Node roles

### Windows Generation Node
- local SDXL/ComfyUI execution
- visual candidate generation
- image QC requiring GPU
- embeddings/duplicate detection
- optional transcription or local models
- asset proxy generation

### Mac Edit Node
- DaVinci Resolve project/timeline
- review render
- creative finishing
- final audio/video QC
- upload control

### Control Plane
初期はどちらか一台または軽量サーバーでよい。
- metadata DB
- job queue
- event log
- approval state
- artifact registry
- budget

## 3. Path abstraction

DBへOS絶対パスを保存しない。

保存：
`artifact://episodes/PD-2026-001/visual/S001/asset.v001.png`

各nodeがlogical URIをローカルパスへ解決する。

## 4. Artifact transfer

優先順位：
1. NAS/object storage
2. managed sync with checksum
3. shared network volume
4. manual transfer only as emergency fallback

同期完了条件：
- size match
- checksum match
- metadata sidecar present
- atomic rename complete
- artifact registry updated

書き込み途中のファイルを編集機が読むことを防ぐため、`.partial`からatomic renameする。

## 5. Cache policy

Windows：
- model cache
- raw candidates
- approved masters
- temporary previews

Mac：
- edit proxies
- selected masters
- audio
- render cache

source of truthはartifact store。local cacheを正本とみなさない。

## 6. Job handoff

例：
1. scene plan approved
2. orchestrator creates image jobs
3. Windows worker leases jobs
4. outputs upload and validate
5. asset registry marks approved candidates
6. edit plan becomes runnable
7. Mac worker imports selected assets
8. timeline result and project backup register

## 7. Clock and identifiers

- UTC timestamp in storage
- display timezone configurable
- ULID/UUID generated centrally or collision-safe
- node_id recorded
- no filename-only coordination

## 8. Offline behavior

Mac停止中：
- research/script/image/audio can progress until edit WIP limit
- edit jobs remain queued

Windows停止中：
- planning and audio can progress
- image jobs remain queued
- existing approved assets may allow edit

## 9. DaVinci project safety

- project template version
- project backup before automation
- timeline revision name
- import log
- media relink report
- render preset version
- no destructive overwrite of approved timeline

## 10. Bandwidth and proxy strategy

raw image assets may be high resolution. Generate:
- master
- edit proxy
- contact sheet thumbnail

Mac initially downloads proxies; approved final render relinks masters where needed.

## 11. Failure cases

- duplicate sync
- partial transfer
- filename collision
- stale proxy
- local edit not registered
- project database unavailable
- NAS offline
- different color profiles
- missing fonts
- different plugin versions

Each has a preflight check before timeline assembly or final render.

## 12. Machine readiness manifest

Each node publishes:
- OS
- app versions
- Python version
- GPU/VRAM
- free disk
- mounted stores
- installed fonts
- DaVinci availability
- model inventory
- worker version
- last heartbeat

Jobs specify capabilities rather than machine names.
