# P03 ASSET INDEX PoC REPORT — PySceneDetect

- Phase `P03`（素材インデックス最小実証） / 2026-07-12 (JST) / by claude-code
- 目的: 100〜500素材に限定し、ffprobe＋PySceneDetect＋3点サンプリング＋SQLite＋再開可能処理を検証。

## 1. 導入（実インストール・隔離）
- **PySceneDetect 0.7 + opencv-python 5.0.0 + numpy 2.2.6** を **独立venv `D:\PD_AI_Tools\PySceneDetect\.venv`（Python 3.10.11）** に導入。
- **既存環境は無傷**：グローバルPython310（torch cu118스택）・プロジェクト`.venv`・ComfyUI env を一切変更していない。
- CUDA不要（CPU）。DL≒57MB（opencv wheel等）＝5GB未満・承認不要枠。

## 2. PoC 実行結果（実測）
| 指標 | 値 |
|---|---|
| 対象 | `H:\pd-media\assets`（動画総数 **15,757**）から**決定論サンプル 150点** |
| 完了 / エラー | **150 / 0** |
| 総カット数 | **287**（平均 **1.91** カット/点・最大26） |
| 平均処理時間 | **2.68 s/点**（150点 wall≈375s） |
| VFR検出 | 0（factory stockはCFR中心。VFR判定ロジックは実装・保持済） |
| DB サイズ | 256 KB（`data/pd_vs_scene_index.sqlite`・gitignore） |
| サムネ | **861枚 / 12.4 MB**（avg 14.8 KB）＠`H:\pd-media\previews\pd-visual-system\scene_index\` |

## 3. 受入基準の充足（すべてPASS）
| 基準 | 結果 | 根拠 |
|---|---|---|
| 100〜500点に限定 | ✅ | 150点。`--limit>500` はスクリプトが拒否 |
| VFR情報をPTS/time_base込みで保持 | ✅ | DBに `r_frame_rate/avg_frame_rate/time_base/start_pts/nb_frames/duration_sec/is_vfr` を保存（実DB確認済） |
| 各カット25/50/75%の3フレーム | ✅ | 各cutに `cutNNN_25/50/75.jpg` 実生成（ディスク確認済） |
| 中断再開 | ✅ | 再実行で **done=0 / skip=150 / 0.0s**（mtime+size一致でスキップ） |
| 差分更新 | ✅ | mtime/size 変化時のみ再処理する分岐 |
| エラー継続 | ✅ | 壊れmp4混在テスト＝broken→`status=error`記録・good→`done`・**クラッシュせず継続** |
| 素材非破壊 | ✅ | 原本は読み取りのみ。移動/削除/上書き/再エンコードなし |

## 4. 成果物 / 変更ファイル
- 新規: `scripts/pd-visual-system/scene_index_poc.py`（再実行可能CLI・読み取り専用・再開/エラー継続）
- 生成: `data/pd_vs_scene_index.sqlite`（試験DB）/ `H:\pd-media\previews\pd-visual-system\scene_index\**`（サムネ）
- 導入: `D:\PD_AI_Tools\PySceneDetect\.venv`（隔離venv）/ `D:\PD_AI_Models`（空・将来用）
- 文書: 本 `asset_index_report.md`

## 5. 再実行方法（CLI）
```
D:\PD_AI_Tools\PySceneDetect\.venv\Scripts\python.exe ^
  scripts\pd-visual-system\scene_index_poc.py --limit 150 ^
  --media-root "H:\pd-media\assets" ^
  --db "data\pd_vs_scene_index.sqlite" ^
  --thumbs-dir "H:\pd-media\previews\pd-visual-system\scene_index"
```
`--limit`(≤500) / `--threshold`(既定27.0) / `--media-root` を変更可。同DBに再実行で差分のみ処理。

## 6. スケール見積り（全15,757点＝将来・要承認）
- 時間: 2.68s×15,757 ≈ **約11.7時間（単スレッド）** → 並列化必要。**数時間バッチ＝§10で事前承認対象**。
- ディスク: サムネ ≈ 1.3 GB / DB ≈ 27 MB（H:・D:で吸収可）。
- ＝**全件処理は別途承認**。本PoCは規模・実用性の確認まで。

## 7. リスク / 限界 / 次の前提
- opencv `CAP_PROP_POS_FRAMES` シークはVFRで誤差の可能性 → 次段(P04)前にVFR素材で精度検証。
- 意味検索（OpenCLIP）は **P04**。本DBの代表フレームを埋め込み対象にする。
- schemas は未変更（scene-plan衝突は無関係）。
- rollback: venv削除＋`data/pd_vs_scene_index.sqlite`＋`H:\pd-media\previews\pd-visual-system\scene_index`削除で完全復旧（原本不変）。
