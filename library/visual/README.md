# library/visual — 再利用ビジュアル・モチーフ・ライブラリ（decisions/0002 §B）

汎用モチーフ（gavel/法廷/書類・天秤/旗/格子/地図テクスチャ/抽象「制度」絵/余白カット 等）を
**一度だけ生成して全話で再利用**する。episode 固有の絵は各 episode の `05_visuals` で別管理。

- `visual_registry.v001.json` … motif records の配列。各要素は `schemas/visual-motif.schema.json` 準拠。
- 画像実体（png）は**SSD側**、`asset_uri`（論理URI）で参照（rule14）。レジストリ JSON は brain＝リポ。
- 自動選択は `src/pd_factory/library/selection.py:select_motif`（motif 一致＋orientation/mood＋直近被り回避、決定論的）。
- ブランド統一のため全モチーフは Midjourney `--sref`（共通シード）で生成（decisions/0002 §B/§G）。

## 生成手順（owner 一度きり）
1. `prompts/12_visual_motif_library_prompts.md` の各プロンプトを Midjourney で生成（Claude が4枚から最適1枚を視認推薦）。
2. 採用画像を SSD に保存し、`visual_registry.v001.json` に record を追記（`motif_id`=`MOT-NNNN`、`sref`、`content_hash`、`rights_basis`、`verified_at`）。
