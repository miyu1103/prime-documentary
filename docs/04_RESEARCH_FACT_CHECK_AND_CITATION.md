# 04 — Research, Fact-check and Citation

## 1. 役割分離

### Researcher

- 広く資料を集める。
- 仮説を作る。
- 重要論点を見つける。
- chronologyとentityを整理する。
- visual evidence opportunitiesを見つける。

### Fact Checker

- 主張を疑う。
- 出典を検証する。
- 数字、日付、引用を確認する。
- 反証を探す。
- 許容表現を決める。
- 使用不可の断定を止める。

同一モデルを使う場合でも、別プロンプト、別コンテキスト、別出力として実施する。

## 2. 調査成果物

- research question
- subquestions
- search plan
- source registry
- claim ledger
- contradiction map
- chronology
- entity registry
- numbers and units
- quote registry
- visual evidence opportunities
- uncertainty notes
- forbidden claims
- unanswered questions

長文メモだけで終わらせない。

## 3. Source Hierarchy

1. 法令、政府、裁判記録、原論文、公式統計、一次史料
2. 大学、研究機関、博物館、専門団体
3. 高品質報道、専門書、査読レビュー
4. 信頼できる解説
5. その他の二次資料
6. SNS・掲示板・無署名まとめ

下位資料は論点発見には使えるが、重大主張の唯一の根拠にしない。

## 4. Source Registry

- source_id
- title
- author/organization
- publication_date
- accessed_at
- URL/reference
- source_type
- authority
- directness
- independence
- recency
- bias/interest
- relevant_locations
- quotation note
- archived hash where permitted
- notes

## 5. Claim Classification

- A：一次資料で直接確認
- B：複数の高品質資料で確認
- C：単一の信頼できる二次資料
- D：推定または解釈
- E：未確認

使用原則：

- 中心命題はAまたはB。
- 数値・日付・固有名詞はA〜C。
- Dは推測表現を付ける。
- Eは台本へ入れない。
- 強い反証がある場合は隠さない。

## 6. Claim Ledger

- claim_id
- normalized_claim
- exact_wording_candidates
- importance
- sensitivity
- source_ids
- support_type
- evidence_location
- counterevidence
- confidence
- allowed_wording
- prohibited_wording
- temporal_scope
- geographic_scope
- units
- reviewer
- status

## 7. Claim Lineage

`claim_id → source_id(s) → evidence location → script_span_id → scene_id → on-screen representation → asset_id`

これにより：

- 台本修正の影響シーンを特定
- 出典削除時の関連箇所を再生成
- 公開後の訂正範囲を特定
- どの主張が視聴離脱箇所にあったか分析

## 8. Numerical Claims

必ず確認：

- numerator / denominator
- nominal / real
- annual / monthly
- calendar / fiscal year
- mean / median
- stock / flow
- percentage / percentage points
- sample size
- confidence interval
- currency and exchange date
- source revision
- unit conversion
- population definition

## 9. Quotes

保存項目：

- 原文
- 話者
- 日付
- 文脈
- 一次ソース
- 省略箇所
- 翻訳
- 使用文字数
- quotation/fair-use note

長い引用を台本の代替にしない。

## 10. Historical Reenactment

AI画像は証拠ではない。

- reconstructed / artistic visualizationとして扱う。
- 実在写真に見える場合は誤認防止を検討。
- 不明な服装・建築を断定しない。
- 複数時代の要素を混ぜない。
- 実在人物の未確認行動を画像で捏造しない。
- 顔が不明な人物を確定的に描かない。
- 不確実なら背面、手元、遠景、図解を使う。

## 11. LLMの扱い

LLMは調査助手であって出典ではない。

- LLMの記憶だけで確定しない。
- URLが存在しても本文を確認する。
- 二次資料が一次資料を正しく反映しているか確認。
- 数字の単位、期間、母集団を確認。
- current情報は取得日時を保存。
- 矛盾資料を自動除外せずcontradictionとして保存。

## 12. Research Stop Rule

停止条件：

- central claims supported
- major counterargument captured
- uncertainty bounded
- story can be written without speculation
- risk reviewer has no blocker
- marginal source adds little

## 13. Red Flags

- 「研究によると」だけで論文名なし
- 正確すぎる数字だが出典なし
- 同じ記事を転載した複数サイト
- 公式発表を独立検証と誤認
- 見出しだけを読む
- 古いcurrent情報
- 翻訳で意味が強くなる
- 相関を原因と表現
- “first ever” “largest” “never”の絶対表現
- 未来予測を事実形で書く
- 一つの利害関係者だけに依存
