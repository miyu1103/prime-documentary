# MODEL LICENSE RECORD — PD Visual System

各埋め込み/生成モデルの重み・取得元・ハッシュ・ライセンスを記録（media-truth-license rule・P04受入基準）。

## OpenCLIP ViT-B/32 (laion2b_s34b_b79k) — P04 意味検索
| 項目 | 値 |
|---|---|
| 用途 | 素材フレームとテキストの意味検索（画像/テキスト埋め込み） |
| コード | OpenCLIP（`open_clip` 2.30.0）— **MIT** |
| モデル | ViT-B-32 / pretrained `laion2b_s34b_b79k` |
| 取得元 | Hugging Face `laion/CLIP-ViT-B-32-laion2B-s34B-b79K`（snapshot 1a25a446…） |
| 重みファイル | `D:\PD_AI_Models\clip\models--laion--CLIP-ViT-B-32-laion2B-s34B-b79K\snapshots\1a25a446712ba5ee05982a381eed697ef9b435cf\open_clip_model.safetensors` |
| 重みサイズ | 605,143,316 bytes |
| 重み sha256 | `ac4f8c4b88af6d963118cbf40ad93176d092abbedfcb752601ae1866352656e6` |
| モデルカード ライセンス | MIT（重み） |
| 学習データ | LAION-2B（研究目的データセット由来） |
| **商用利用判断** | **`review_required`** — コード/重みはMITだが学習データがLAION-2B。**本モデルは"素材の候補探索(内部ツール)"に限定使用**し、生成物として配信しない。最終採否は人間。falseやapprovedへ推測変換しない（media-truth rule） |
| 取得日時 | 2026-07-12 (JST) |
| review_status | review_required |

> 注: 本モデルは**検索インデックス生成のみ**に使う。動画に映る素材そのものではない。素材（factory stock）のライセンスは別途 stock_ledger / LICENSE_REGISTER で管理。
