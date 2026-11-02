# P05 EVIDENCE — Remotion コア5部品

- Phase `P05` / by claude-code / 2026-07-12 (JST) / インストール不要

## 実装
- `remotion/src/components/core5/index.tsx`：EvidenceReveal / PenaltyVsProperty / CaseJourney / QuoteUnderExamination / VerdictReversal（既存 motionkit を合成・invariant14準拠）＋ CORE5_ALIASES。
- `remotion/src/components/core5/preview.tsx`：`PDCore5` ギャラリー（demo props はここ＝部品に事件名ハードコードなし）。
- `remotion/src/Root.tsx`：`PDCore5` 構成を1件登録。

## 検証（実測）
```
npx tsc --noEmit → exit 0（クリーン。casing import bug 1件修正後）
npx remotion still PDCore5 ... --frame=45/135/210/315/435 → 6枚レンダ成功、全て目視確認
  45  PenaltyVsProperty  $10,000 vs $42,006 バー＋出典 ✅
  135 EvidenceReveal     証拠カード（ペーパークリップ/スキャン/caption）✅
  210 CaseJourney        Procedural history 経路 ✅
  315 QuoteUnderExamination 大セリフ＋THE COURT＋金下線 ✅
  435 VerdictReversal    赤 REVERSED スタンプ ✅
```
- 修正: プレビューは各部品に `dur={seg}` を明示（部品は `dur` 対応済）。

## 契約
16:9/1920×1080/30fps・duration耐性・props・seed・preview低負荷・セーフエリア・事件名非ハードコード・英語本番＋jaNote・語同期対応 = 満たす（`core5_report.md §2`）。

## rollback / 次
- rollback: `core5/` 削除＋Root.tsx 追記2箇所を戻す。既存構成に非干渉。
- 次 P06 = B1版制作（素材検索＋コア5部品で timbs 80秒 baseline を組む test-bench）。適用先本番は EP37。
