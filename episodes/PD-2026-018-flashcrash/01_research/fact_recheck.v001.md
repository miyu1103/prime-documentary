# EP18 flashcrash — Fact re-check & R3 lock packet v001

> R2/R3手順：公開前に**load-bearingな事実/数値/引用を一次（DOJ/CFTC/SEC/裁判記録）に突き合わせ**、各 source の durable `content_hash` を算出（現在 `sha256:pending`）。**因果ロック**を全工程で維持。下表の「確定」は記録一致、「要再確認」は公開前に再検証。

## A. 数値・事実ロック（claims紐付け）
| 項目 | 値（脚本で使用） | 出典 | 状態 |
|---|---|---|---|
| 暴落日時 | 2010-05-06, ~14:32 EDT 開始, ~36分 | SRC-0001/0007 (CLM-0001) | 確定 |
| 下落幅 | ダウ ~998.5pt (~9%), 一時 ~$1T 消失→大半回復 | SRC-0001/0007 | 確定 |
| 大口売り | 75,000 E-mini S&P 契約 (~$4.1B), 価格非依存アルゴ | SRC-0001 (CLM-0007) | 確定（運用会社は**名指し非難しない**） |
| HFT評価 | 「原因ではないが寄与」 | SRC-0002 (CLM-0007) | 確定 |
| 手口/期間 | spoofing, E-mini/CME, 改変市販ソフト, 2009-2014 | SRC-0003/0005 (CLM-0004) | 確定 |
| 利得 | **自認 ≥$12.8M**／CFTC主張 **>$40M** | SRC-0003/0005 (CLM-0005) | 確定（自認と主張を区別） |
| 起訴 | 2015 DOJ (wire fraud/commodities fraud/spoofing), London逮捕, 引渡し争い | SRC-0004/0005 (CLM-0008) | 確定 |
| 有罪答弁 | **2016, wire fraud 1件＋spoofing 1件**, 没収 ~$12.9M | SRC-0003/0004 (CLM-0009) | 確定（**“暴落を引き起こした罪”ではない**） |
| 喪失 | 稼ぎの大半を投資詐欺/ポンジで喪失 | SRC-0006/0008 (CLM-0010) | 要再確認（£40m等の正確額） |
| 量刑 | **2020, 実刑なし＝在宅拘禁1年**（最大~8年に直面） | SRC-0006/0004 (CLM-0012) | 要再確認（裁判記録で正確な文言） |
| 自閉 | 重度アスペルガー; 専門家鑑定（金に無関心・ハイスコア） | SRC-0006 (CLM-0011) | 要再確認（鑑定の正確な引用・帰属） |

## B. ★因果ロック（不可侵・全工程＝ナレ/テロップ/サムネ/タイトル）
- **許可**：contributed to / exacerbated / significantly responsible for the order imbalance / helped tip / part of.
- **禁止（事実としての断定）**：caused the crash / single-handedly / one man broke the market / triggered the crash by himself.
- **帰属**：因果評価は当局/報告書/裁判に帰属。ナレーターは断定しない。常に他要因（大口売り・HFT引き上げ・ギリシャ不安）と併置。
- **有罪答弁は事実**として可。ただし「spoofing/wire fraudに有罪答弁」であって「暴落に有罪」ではない。

## C. 公開前の必須作業
1. 各 source の `content_hash` を算出し sources.v001 を更新（現 pending）。
2. 量刑・喪失額・自閉鑑定引用を一次（裁判記録/判決）で確定。
3. 現在事実（その後の市場・規制）に触れる場合は publish-time 再確認。
4. **専用 法務/権利レビュー**（R3）を exact revision/hash で実施・記録 → なしに publish 不可。
