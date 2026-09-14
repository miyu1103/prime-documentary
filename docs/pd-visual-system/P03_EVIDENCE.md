# P03 EVIDENCE — 素材インデックス最小実証 (PySceneDetect)

- Phase `P03` / by claude-code / 2026-07-12 (JST)

## 実インストール（隔離）
```
py -3.10 -m venv D:\PD_AI_Tools\PySceneDetect\.venv        # Python 3.10.11
.venv\Scripts\python -m pip install "scenedetect[opencv]"  # scenedetect 0.7 / opencv 5.0.0 / numpy 2.2.6
```
既存 global Python310 / project .venv / ComfyUI env は不変。

## PoC 実行と結果（実測ログ）
```
scene_index_poc.py --limit 150 → done=135 skip=15 err=0 total_cuts=287 wall=375.2s
（skip=15 は先行スモークの重複＝再開動作）
resume再実行 --limit 150      → done=0 skip=150 err=0 wall=0.0s   （再開/差分更新 実証）
error-continue test           → broken.mp4=status:error / good.mp4=done（クラッシュせず）
最終DB集計                    → assets_done=150 error=0 cuts=287 avg 1.91/max26 avg_proc 2.68s DB256KB
サムネ                        → 861枚 / 12.4MB @ H:\pd-media\previews\pd-visual-system\scene_index
VFR保持                       → DBに r/avg frame rate, time_base, start_pts, nb_frames, is_vfr（実確認）
```

## 受入基準
100-500限定/VFR(PTS/time_base)保持/25-50-75%3フレーム/中断再開/差分更新/エラー継続/素材非破壊 = **全PASS**（`asset_index_report.md §3`）。

## 保護・rollback
- 原本 read-only。移動/削除/上書き/再エンコードなし。git操作なし。
- rollback: `D:\PD_AI_Tools\PySceneDetect\.venv` 削除＋`data/pd_vs_scene_index.sqlite`＋`H:\pd-media\previews\pd-visual-system\scene_index`削除。

## 未確認 / 次
- VFR素材でのシーク精度は P04前に要検証。全15,757点処理は約11.7h/1.3GB＝**§10承認対象**（PoC範囲外）。
- 次 P04 = OpenCLIP 意味検索（本DBの代表フレームを埋め込み）。
