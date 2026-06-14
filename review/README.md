# review/ — local Animatic review (P0, $0, local-only)

オーナーが第1話 Miranda のアニマティックをローカルで安全に視聴し、タイムコード付きの
マーカー＋日本語コメントを構造化記録するための最小環境（CLAUDE.md §13 / P0 仕様）。
有料API・公開・アップロード・秘密・破壊操作は一切行いません。

## 起動（ワンコマンド）
```bash
py -3.11 review/serve.py          # http://127.0.0.1:7332 を自動で開く
py -3.11 review/serve.py --port 8080 --no-open
```
前提：アニマティックがレンダー済みであること（`remotion/out/miranda-animatic.mp4`、無ければ
`animatic_miranda.mp4` を使用）。未レンダーなら remotion で先に出力してください。

## 操作
- 再生/停止＝Space、5秒移動＝←/→、速度＝0.5/1/2x。
- **1回目**：B 退屈 / U 分かりにくい / A 違和感 / X 公開不可（現在位置にマーカー）。
- **2回目**：M で位置取得 → カテゴリ/重要度を選びコメント入力 → Ctrl+Enter で確定。
- 重要度ショートカット：1 軽微 / 2 要修正 / 3 公開不可。手動保存＝S。
- マーカー/コメント一覧のタイムコードをクリックでその位置へジャンプ。

## 保存（JSONが正本）
- 確定レビュー：`episodes/PD-2026-001-miranda/08_qc/reviews/animatic_review.v001.json`
- 自動保存の下書き：`.../animatic_review.draft.v001.json`
- 上書き前バックアップ：`.../reviews/backups/`（原子的書込み temp+rename）
- スキーマ：`schemas/animatic-review.schema.json`（保存時に検証）

draft とバックアップは git 無視。確定レビュー JSON はコミット対象（Claude が後で読み修正計画化）。

## スモークテスト
```bash
py -3.11 review/serve.py --no-open --port 7333 &   # 起動
curl http://127.0.0.1:7333/api/meta                # fps/尺
curl http://127.0.0.1:7333/api/review              # 初期レビュー
# ブラウザで http://127.0.0.1:7333/ を開き、再生→マーカー→コメント→再読込で再開を確認
```

## テスト
`PYTHONPATH=src pytest tests/test_review.py`（スキーマ・原子的保存・バックアップ・state履歴）。

## ロールバック
`review/` 削除＋`schemas/animatic-review.schema.json`／Makefile／.gitignore を git revert。
レビューJSONは新規ファイルのみで既存成果物は不変。
