# 02 — End-to-End Pipeline

## 1. Pipeline Contract

各stageは共通構造を返す。

```json
{
  "stage": "script.verify",
  "episode_id": "PD-2026-001-example",
  "input_revision": "v003",
  "status": "succeeded",
  "output_refs": [],
  "validation": {},
  "confidence": 0.92,
  "warnings": [],
  "cost": {},
  "retry": {},
  "provenance": {}
}
```

## 2. 全工程一覧

| No. | 工程 | 主目的 | 主出力 | 自動化 |
|---|---|---|---|---|
| 00 | Demand sensing | 視聴者需要を収集 | demand signals | 全自動 |
| 01 | Idea generation | 題材と切り口を生成 | topic candidates | 全自動 |
| 02 | Portfolio scoring | 期待値とリスクを採点 | ranked shortlist | 全自動 |
| 03 | Batch approval | 週次候補を承認 | approved queue | 人間→将来自動 |
| 04 | Pre-research | 根拠と映像化可能性確認 | feasibility brief | 全自動 |
| 05 | Research plan | 問いと検索計画 | research plan | 全自動 |
| 06 | Deep research | 資料収集 | source library | 全自動 |
| 07 | Claim ledger | 主張・根拠・確度 | claims.json | 全自動 |
| 08 | Thesis design | 中心命題 | thesis | 自動＋承認 |
| 09 | Outline | 章構造 | outline | 全自動 |
| 10 | Script draft | 英語台本 | draft | 全自動 |
| 11 | Script verification | 事実・論理・英語監査 | verified script | 自動＋承認 |
| 12 | Scene decomposition | 意味単位のシーン化 | scene plan | 全自動 |
| 13 | Visual strategy | 視覚形式割当 | visual plan | 全自動 |
| 14 | Prompt compilation | SDXL生成条件 | generation jobs | 全自動 |
| 15 | Image generation | 画像候補生成 | raw assets | 全自動 |
| 16 | Visual QC | 破綻・連続性検査 | approved assets | 全自動＋例外 |
| 17 | Motion plan | 動き・尺設計 | motion instructions | 全自動 |
| 18 | Narration chunks | 音声単位分割 | voice jobs | 全自動 |
| 19 | Voice generation | ナレーション生成 | voice takes | 全自動 |
| 20 | Voice QC | 発音・欠落検査 | approved narration | 全自動＋例外 |
| 21 | Music selection | BGM選定 | cue sheet | 全自動 |
| 22 | SFX/ambience | 環境音・効果音 | sound cue sheet | 全自動 |
| 23 | Timeline assembly | 仮編集 | rough cut | 全自動 |
| 24 | Edit QC | 同期・テンポ・音量検査 | review cut | 自動＋承認 |
| 25 | Render | レビュー・最終書出し | render files | 全自動 |
| 26 | Thumbnail ideation | サムネ案 | variants | 全自動 |
| 27 | Metadata | タイトル・説明・章 | publish package | 全自動 |
| 28 | Package approval | 最終確認 | approval | 人間→将来自動 |
| 29 | Upload/schedule | アップロード・予約 | scheduled video | 承認後自動 |
| 30 | Monitoring | CTR・維持率等 | snapshots | 全自動 |
| 31 | Learning loop | 勝敗要因更新 | playbook | 全自動＋月次監査 |

## 3. Stage 00：Demand Sensing

入力：

- YouTube分析
- 検索候補
- 競合動画
- コメント
- チャンネル内検索語
- 過去のtopic performance
- 外部トレンド
- evergreen catalog

処理：

- keyword/entity clustering
- question extraction
- audience pain/curiosity extraction
- saturation estimate
- freshness vs evergreen
- demand evidence
- channel fit

禁止：

- 再生数だけで需要を判断
- 一時ニュースを長期需要と混同
- 競合タイトルのコピー
- 一つの外部指標に依存

## 4. Stage 01：Idea Generation

一つのsubjectから複数angleを作る。

- chronology
- hidden system
- myth correction
- rise/fall
- causal chain
- comparison
- forgotten actor
- unintended consequence
- engineering explanation
- human story
- economic incentive
- psychological mechanism

出力はsubjectではなく`topic-angle pair`。

## 5. Stage 02：Scoring

スコアだけでなく理由を返す。

- positive evidence
- negative evidence
- uncertainty
- expected performance band
- production complexity
- risk
- recommended format
- title hypotheses
- falsification condition

## 6. Stage 03：Batch Approval

比較画面に表示：

- one-line premise
- why now
- why PD
- expected viewer
- competing videos
- score breakdown
- research feasibility
- visual feasibility
- risk
- estimated cost
- estimated human review
- series value

## 7. Stage 04〜07：Research

無秩序に検索せず、research planを先に作る。

終了条件：

- central questionへ暫定回答
- central claimsに必要な根拠
- major counterargument
- chronology
- key entities
- missing evidence
- visual opportunities
- risk notes

## 8. Stage 08〜11：Story and Script

順序：

1. thesis
2. audience promise
3. narrative tension
4. chapter functions
5. claim allocation
6. first draft
7. fact audit
8. logic audit
9. English edit
10. narration edit
11. approval

ファクト修正と文体修正を一度に行わない。変更理由が追えなくなる。

## 9. Stage 12〜17：Visuals

- scene planは台本確定後に作る。
- 企画初期に映像化可能性だけは確認する。
- 重要度によって候補数を変える。
- QC failure taxonomyに応じて限定再生成する。

Priority：

- Tier A：冒頭、サムネ候補、転換点、結論
- Tier B：主要説明
- Tier C：補助・移行

## 10. Stage 18〜22：Audio

- master voiceは台本承認後。
- 低品質draft voiceで尺確認してよい。
- musicは毎回新規生成せずlibrary selectionを優先。
- 発音ミスはチャンクだけ再生成。

## 11. Stage 23〜25：Edit and Render

粗編集を自動生成し、問題箇所へmarkerを付ける。

人間レビューへ渡す情報：

- high-risk timestamps
- low-confidence visual matches
- repeated visual clusters
- pacing anomalies
- claim-sensitive scenes
- audio anomalies
- missing citations
- suggested fixes

## 12. Stage 26〜29：Package and Publish

- 本編完成前に仮タイトルを作ってよい。
- 最終版は本編との約束一致を検査。
- upload既定はprivateまたはunlisted。
- 公開承認後にschedule。

## 13. Stage 30〜31：Analytics and Learning

学びは感想で終わらせず、以下で登録。

- observation
- hypothesis
- evidence
- confidence
- affected rule
- proposed experiment
- expiration/review date

## 14. Partial Rerun

- titleだけ変更：metadata以降
- 一主張削除：script span → scenes → assets → voice chunks → affected timeline range
- 一画像破綻：asset generation → visual QC → timeline relink → render
- 発音ミス：voice chunk → audio QC → timeline relink → render
- BGM権利問題：music cue → timeline audio → render → package
- 事実誤り：claim → linked script spans/scenes/assets/on-screen text/metadata

## 15. WIP Limits

初期推奨：

- researching：最大3本
- scripting：最大2本
- assets_generating：最大2本
- edit_assembly：最大1本
- edit_review：最大2本
- package_ready：最大3本

上流を無制限に流すと、編集待ちの未使用素材へ費用が発生する。
