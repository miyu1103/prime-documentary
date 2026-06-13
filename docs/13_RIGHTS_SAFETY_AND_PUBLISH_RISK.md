# 13 — Rights, Safety and Publish Risk

## 1. リスク分類

### R0：低リスク

一般的な科学、技術、自然、歴史的構造等。通常の自動処理が可能。

### R1：軽度注意

商標、建築物、歴史再現、一般人物画像等。自動QC＋サンプリング。

### R2：中リスク

実在人物、企業、具体的事件、評価を伴う主張。fact/right review。

### R3：高リスク

犯罪、政治、戦争、医療、金融、宗教、未成年、死傷、係争。専用レビュー。

### R4：原則停止

重大な名誉毀損、個人情報、進行中の係争で未確認断定、扇動、露骨な暴力、違法取得資料等。専門確認なしに進めない。

## 2. Rights Manifest

各assetに保存：

- origin
- creator/provider
- generated/acquired
- creation date
- plan/license
- commercial use status
- attribution
- restrictions
- evidence URI
- transformation
- expiry
- territory
- notes
- last_verified_at

## 3. AI Visual Disclosure

全AI画像へ常に大きなラベルを載せるとは限らないが、次の場合は誤認防止を強める。

- 実在の歴史的場面の再現
- 実在人物の行動
- 証拠写真のように見える
- ニュース性の高い現在事件
- 画像自体が主張の根拠に見える
- 本物の記録映像と混在する

表示候補：

- AI-assisted visualization
- Artistic reconstruction
- Illustrative reenactment
- Visualization based on historical descriptions

## 4. Defamation and Privacy

- 事実と意見を分ける。
- 未確定の疑惑を断定しない。
- 反論・否定情報を無視しない。
- private personを扱う必要性を検討。
- 住所、連絡先、家族等の個人情報を出さない。
- 被害者を刺激的な素材にしない。
- sensational thumbnailを避ける。
- “fraud”, “criminal”, “lied”等の強い語は根拠を厳格化。

## 5. Voice Cloning

- 本人の明確な同意
- consent evidence
- allowed use
- duration
- revocation
- disclosure
- provider policy
- storage policy

既定ではPD固有の許諾済みナレーター音声を使用する。公人の声真似を既定で禁止。

## 6. Music Rights

- 生成時の契約プラン
- 生成日
- 商用利用条件
- ダウンロード原本
- prompt
- track ID
- account evidence
- attribution
- territory
- dispute status

後からプランを変更しても、過去曲の権利が自動的に変わると仮定しない。

## 7. Third-party Materials

- 必要性
- 使用量
- 変形性
- 出典表示
- 市場代替性
- 地域法
- プラットフォームポリシー

を検討する。長い映像・音楽・文章のコピーを避ける。

## 8. Provider Terms Registry

各provider adapter：

- provider name
- service
- terms URL/reference
- commercial use summary
- automation/API rules
- storage rules
- model training/data use
- rate limits
- last_verified_at
- verifier
- affected asset query

規約変更時に影響episodeを検索可能にする。

## 9. YouTube Publish Risk

- copyright claim
- strike risk
- advertiser suitability
- age restriction
- reused content perception
- synthetic content disclosure
- misleading metadata
- spam-like mass publishing
- duplicate videos
- child-directed classification

## 10. Reused/Low-value Content Risk Mitigation

- 独自台本
- 独自調査
- 独自構成
- 独自ナレーション
- 説明目的に合った編集
- 画像の意味ある選定
- 図解と出典
- 同一テンプレートの過剰反復を避ける
- 動画ごとの中心命題

## 11. Publish Risk Review Output

```json
{
  "risk_class": "R2",
  "blockers": [],
  "required_disclosures": [],
  "required_human_review": true,
  "claims_requiring_review": [],
  "assets_requiring_review": [],
  "rights_status": "conditional",
  "recommendation": "proceed_with_conditions"
}
```
