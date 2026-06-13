# 21 — Production Economics and Capacity

## 1. 経営上の単位

- cost per episode
- cost per published minute
- human minutes per episode
- GPU hours per episode
- edit workstation hours
- provider cost
- asset acceptance cost
- cost per 1,000 watch hours
- payback period
- library reuse value

## 2. Hidden Costs

- 調査のやり直し
- 人間レビュー待ち
- 低品質候補の確認
- ファイル探索
- 再レンダー
- provider障害
- 権利確認
- 公開後修正
- unused assets
- tool switching

API料金だけをコストとみなさない。

## 3. Bottleneck Theory

スループットは最も遅い制約で決まる。

想定ボトルネック：

1. 人間承認
2. 編集assembly
3. creative finish
4. 画像QC
5. GPU生成
6. 調査

上流の生成速度だけを上げても、編集在庫が増えるだけ。

## 4. Capacity Model

各工程：

- average duration
- p95 duration
- concurrency
- acceptance rate
- retry rate
- human touch time
- wait time

月間能力はcritical pathで計算する。

## 5. Quality Tiers

### Tier A：Flagship

- 高い調査密度
- hero visual多い
- 人間レビュー厚い
- 長期資産候補

### Tier B：Standard

- 標準工程
- L3の中心
- 量産と品質の均衡

### Tier C：Experiment

- 低コスト
- 新テーマ検証
- 成功時に拡張

品質tierを「雑さ」ではなく投資量の違いとして定義。

## 6. Make-or-Reuse

新規生成前に確認：

- existing visual library
- location/background
- map template
- diagram template
- music library
- ambience
- motion template
- title style

再利用で視聴者価値が落ちないものは再利用。

## 7. Early Kill Economics

テーマは上流で捨てるほど安い。

- topic stageで棄却：ほぼゼロ
- research後：小損
- script後：中損
- assets後：大損
- edit後：非常に大きい

したがって、企画・予備調査のgateを厳密にする。

## 8. Cost Allocation

episodeだけでなくlibrary investmentを分ける。

- episode direct cost
- reusable library cost
- platform/tool fixed cost
- R&D
- failed experiment
- maintenance

## 9. Automation ROI

自動化候補の優先度：

`frequency × human minutes × error cost × standardizability ÷ implementation cost`

最優先になりやすい：

- naming
- manifest update
- file transfer
- timeline assembly
- subtitle
- QC checks
- status report
- repeated prompts
- selective rerun

## 10. Human Review ROI

人間レビューを削る対象：

- 低重要度で自動精度が高い
- 差分表示可能
- ロールバック可能
- 損害が限定的

残す対象：

- ブランド
- 高リスク事実
- 権利
- public publish
- 大きな予算
- 新しいコンテンツ形式
