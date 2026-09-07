# P04 EVIDENCE — 意味検索の最小実証 (OpenCLIP)

- Phase `P04` / by claude-code / 2026-07-12 (JST)

## 構成・実行
```
model: OpenCLIP ViT-B/32 laion2b_s34b_b79k  (weight 605MB, sha256 ac4f8c4b...656e6, -> D:\PD_AI_Models\clip)
env  : global Python310 (torch 2.0.1+cu118, CUDA) — 新venv不要・追加DLは重みのみ
build: 287カット代表フレームをCUDAで1.97s埋め込み -> data/pd_vs_clip_index.npz (512d)
eval : 20クエリ Top-10 -> data/pd_vs_clip_eval.json
```

## 目視確認（画素ベース）
- police car night ✅ / lawyer courthouse steps ✅ / office dark ✅ / spinning globe ❌(金属球)。
- 20件 top-1 暫定: 明確関連≈9-10 / 部分≈7 / 失敗3(prison・handcuffs=素材不在, globe=取りこぼし)。厳密≈45-50%・実用≈80%。

## 受入基準
Top-10人間評価記録 / モデル・重み・取得元・ハッシュ・ライセンス保存(MODEL_LICENSE_RECORD.md) / 失敗例保存 = **全PASS**（`semantic_search_report.md`）。

## 保護・rollback・限界
- 素材read-only。license不明重みの自動採用なし（laion2b=商用review_required・内部検索限定）。全素材一括埋め込みは未実施（287カットのみ）。
- rollback: data/生成物＋`D:\PD_AI_Models\clip`削除。既存環境不変。
- 次: P05 Remotionコア5部品（インストール不要・コード実装）。素材検索(P03/P04)はEP37制作で活用。
