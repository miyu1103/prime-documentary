# 月次ディープパス（毎月1日リマインダー）— Claude Codeに貼るプロンプト

```
Prime Documentaryの月次ディープパスを実行して。

1. episodes/_planning/measurements/ の週次レポート全部を読み、月間トレンド
   （ルール違反の増減・新規公開動画のカーブがpd-retention-rulesを守れたか）を判定
2. DEEP_RESEARCH_FINDINGS.v001.md §8 の実験のうち、データが溜まったものに判定を出す
   （判定ルールは各実験に書いてある）
3. SHOULDルールのうち新データで昇格/棄却できるものを更新
   （FINDINGS v002として改訂・メモリも同期）
4. 外部研究の追加パス：T2/T3/T7のサンプルを拡張（各+20本目標）し、
   ルールに反する新証拠がないか敵対的に確認
5. 結果を episodes/_planning/measurements/monthly_review.<YYYYMM>.md に書いてコミット

GPU不使用・予約/公開なし・EP build中のファイルには触れない。
```
