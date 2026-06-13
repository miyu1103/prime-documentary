# 09 — Packaging, Publishing and Analytics

## 1. Publish Package

```text
publish/
├─ final_video.*
├─ thumbnail/
├─ title_candidates.json
├─ selected_title.txt
├─ description.md
├─ chapters.txt
├─ subtitles/
├─ tags.json
├─ playlist.json
├─ pinned_comment.md
├─ rights_manifest.json
├─ source_notes.md
├─ qc_report.json
└─ approval.json
```

## 2. Packaging Philosophy

動画の価値が高くてもクリックされなければ届かない。一方で、誇張してクリックを取ると維持率と信頼を失う。

パッケージ条件：

- 何の動画か理解できる。
- 知識ギャップがある。
- 感情または意外性がある。
- 競合一覧で識別できる。
- 本編が約束を回収する。
- 小画面で読める。
- 英語圏で自然。
- 過度な文字量がない。

## 3. Title Evaluation

- clarity
- curiosity
- specificity
- emotional pull
- novelty
- search language
- mobile truncation
- promise accuracy
- cultural naturalness
- channel-history similarity
- competitor similarity
- policy risk

## 4. Title Pattern Library

- The Hidden System Behind X
- Why X Was Never Really About Y
- The Rise and Collapse of X
- How X Quietly Changed Y
- The Forgotten Reason X Happened
- Inside the Machine That Built X
- What Everyone Gets Wrong About X
- The Decision That Transformed X
- Why X Could Never Last
- The Real Cost of X

型を機械的に当てず、中心命題に合わせる。

## 5. Thumbnail Evaluation

- focal clarity at small size
- contrast
- visual novelty
- face/object readability
- text readability
- title complementarity
- promise accuracy
- generated-artifact defects
- sensitive content
- brand fit
- title information duplication

## 6. Thumbnail Rules

- 一つの中心対象。
- 強い対比。
- 明確な感情または異常。
- 文字は原則2〜4語、または文字なし。
- タイトルと同じ情報を重複させない。
- 誤認させる架空の証拠画像を避ける。
- 実在人物の表情・行動を捏造して断定しない。
- モバイルサイズで検査。

## 7. Variant Management

- concept variants：3
- execution variants per concept：2〜3
- final shortlist：2〜3

差が小さい量産は意味がない。

## 8. Description

- concise value statement
- accurate summary
- chapters
- source/reading note where appropriate
- disclosure where needed
- channel positioning
- related video links after data exists
- no keyword stuffing
- no false claims

## 9. Publishing Safeguards

- default privacy private
- expected channel ID allowlist
- duplicate video hash check
- title/thumbnail approval revision match
- scheduled timezone explicit
- made-for-kids setting explicit
- language explicit
- subtitles verified
- monetization/ad suitability workflow
- upload resume
- post-upload processing status
- final URL saved

## 10. Publish Gate

すべてpass：

- script_verified
- critical claims supported
- rights_clear
- assets_complete
- voice_qc_pass
- edit_qc_pass
- thumbnail_qc_pass
- metadata_qc_pass
- render_technical_pass
- budget_within_limit
- approval valid for current revisions

## 11. Automated Upload Scope

承認後に自動化：

- upload
- title
- description
- tags
- language
- thumbnail
- subtitles
- chapters
- playlist
- schedule
- URL取得
- manifest更新
- analytics jobs登録

初期はprivate/unlistedを既定とする。

## 12. Analytics Windows

- 1h：技術事故、公開状態
- 24h：初期CTR、初期維持率、流入
- 72h：パッケージ適合、初動
- 7d：テーマと視聴者適合
- 28d：長尾、検索・関連流入
- 90d：エバーグリーン性
- 180d+：資産価値

## 13. Analytics Fields

- impressions
- CTR
- views
- watch time
- average view duration
- average percentage viewed
- retention curve
- traffic sources
- browse/suggested/search
- geography
- device
- subscribers gained
- comments
- likes
- revenue metrics where available
- end screen
- returning viewers

## 14. Scene-level Mapping

Retention timestampをscene rangesへjoin。

- relative retention change at scene start
- drop slope
- recovery
- repeated visual indicator
- narration pace
- visual mode
- claim complexity
- chapter position
- music transition
- cut frequency

相関を因果と断定せず、仮説生成に使う。

## 15. Learning Record

- observation
- hypothesis
- evidence
- confidence
- affected rule
- proposed experiment
- review date
- sample size
- confounders

## 16. Alerts

- upload failed
- processing stuck
- copyright claim
- policy restriction
- thumbnail missing
- severe early retention cliff
- wrong subtitle/language
- unintended public state
- unusual negative comments
- analytics data gap

公開後のtitle/thumbnail変更は時刻と前後データ窓を保存する。
