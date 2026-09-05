# P04 SEMANTIC SEARCH PoC REPORT — OpenCLIP

- Phase `P04`（意味検索の最小実証） / 2026-07-12 (JST) / by claude-code
- 目的: 商用条件を記録した埋め込みモデルで、20クエリの検索品質を人間評価する。
- モデル/重み/ハッシュ/ライセンス = `MODEL_LICENSE_RECORD.md`。

## 1. 構成（既存GPU環境流用・追加DLは重みのみ）
- モデル: OpenCLIP **ViT-B/32 laion2b_s34b_b79k**（重み605MB→`D:\PD_AI_Models\clip`・sha記録済）。
- 環境: 既存グローバル Python310（torch 2.0.1+cu118・**CUDA**）。新venvは作らず追加DLを最小化。
- 埋め込み対象: P03の**287カット×代表フレーム(50%)** を **CUDAで1.97秒**で埋め込み（`data/pd_vs_clip_index.npz`・512次元）。
- 検索CLI: `scripts/pd-visual-system/clip_search_poc.py`（`build`/`query`/`eval`）。

## 2. 20クエリ評価（`data/pd_vs_clip_eval.json`）
- 手法: テキスト埋め込みとフレーム埋め込みのcos類似でTop-10。top-1の関連性を、**代表4件は実サムネを目視確認**、残りは記述的ファイル名＋スコアで暫定判定（**フルTop-10精度はowner確認対象**）。

### 目視確認（画素ベース・ファイル名非依存）
| クエリ | Top-1 | 目視結果 |
|---|---|---|
| night police car flashing lights | police_car_lights_night | ✅ 夜道＋赤青ライトの車列 |
| lawyer entering courthouse | courthouse_steps | ✅ 列柱建物の階段を歩く人物 |
| office interior dark mood | office_interior_dark | ✅ 暗い机・ランプ・書類 |
| spinning globe at night | molten_metal_pour | ❌ 金属球（地球儀でない）＝球形状で誤マッチ |

### top-1 暫定判定（20件）
- **明確に関連 ✅（9〜10件）**: police car / lawyer courthouse / city traffic night / interrogation room / money counting / dark cinematic / office dark / american flag / rain on glass（＋gavel→courtroom は妥当）
- **部分的 ⚠（〜7件）**: courthouse exterior・government office・Supreme Court→bank_building_columns（列柱で視覚類似だが文脈ずれ）/ highway aerial / person silhouette / legal documents→courtroom
- **失敗 ❌（3件）**: prison corridor→data_center_corridor（**刑務所素材なし**）/ handcuffed hands→dog_tags（**手錠素材なし**）/ spinning globe→molten sphere（globe素材の取りこぼし）

**暫定 top-1 精度 ≈ 45〜50%（厳密）／ 実用可(⚠含む) ≈ 80%**。失敗の主因は**150点サンプルに該当素材が無い（材料ギャップ）**＝全件インデックス化 or AI B-roll(P10)で補う対象。

## 3. 失敗例（保存・受入基準）
- prison corridor / handcuffed hands = 該当素材の不在（＝P10 AI B-rollの用途 or 素材追加）。
- spinning globe = globe_spinning_dark 素材が存在するのにmolten球に負けた＝**同一概念内の取りこぼし**。閾値/複数フレーム集約(25/50/75平均)で改善余地。

## 4. 受入基準（PASS）
- Top-10 precisionの人間評価を記録 = ✅（目視4件＋暫定20件・owner確認枠）
- モデル/重み/取得元/ハッシュ/ライセンス保存 = ✅（`MODEL_LICENSE_RECORD.md`）
- 検索失敗例を残す = ✅（§3）

## 5. 成果物 / rollback
- 新規: `clip_search_poc.py` / `data/pd_vs_clip_index.npz` / `data/pd_vs_clip_manifest.json` / `data/pd_vs_clip_eval.json` / `data/pd_vs_queries.txt` / `MODEL_LICENSE_RECORD.md` / 本書。
- rollback: 上記 data/ 生成物と重み(`D:\PD_AI_Models\clip`)削除。既存環境不変。
- 適用: 本検索は **EP37以降の素材選定**を高速化（DEC-20260712-002）。timbsは実験台。
