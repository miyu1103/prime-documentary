# P05 CORE-5 COMPONENTS REPORT — Remotion

- Phase `P05`（Remotionコア5部品の実装）/ 2026-07-12 (JST) / by claude-code
- インストール不要（コードのみ）。既存 remotion 環境で実装・検証。

## 1. 実装（既存motionkitを合成・二重実装なし）
`remotion/src/components/core5/index.tsx` に **5部品のみ**を実装。各々は既存 `motionkit` プリミティブの薄いラッパ（invariant 14 準拠）:
| コア部品 | verb | 合成元(motionkit) |
|---|---|---|
| **EvidenceReveal** | Reveal | EvidenceCard / Img＋Spotlight＋HighlightRing＋LowerThird |
| **PenaltyVsProperty** | Compare | ComparisonBars＋NumberTicker(ratio)＋LowerThird |
| **CaseJourney** | Trace | RouteMap / ProcessSteps / YearSweep＋LowerThird |
| **QuoteUnderExamination** | Isolate | QuoteCard＋Spotlight(examine)＋LowerThird |
| **VerdictReversal** | Overturn | VoteTally→StampReveal＋LowerThird |

alias（DocumentReveal→EvidenceReveal 等）は `CORE5_ALIASES`＋`config/pd-visual-system/component-registry.json`。

## 2. 契約充足（registry / ブリーフ§4）
- 16:9・1920×1080・30fps（`useVideoConfig`・ハードコードなし）
- **duration耐性**（全内部タイミングが `dur ?? durationInFrames` 基準）
- props で内容/位置/強度、`seed` で変化固定、`preview` で低負荷（atmosphere bed省略）
- テキストはセーフエリア（motionkit準拠）、**事件名ハードコードなし**（demoは preview.tsx 側）
- 英語本番＋`jaNote`（日本語確認・非描画）
- 語タイムスタンプ連携：`<Sequence from={wordFrame}>` に載せれば内部ビートが `dur` に追従

## 3. 検証（自己申告でなく実測）
- **typecheck**: `npx tsc --noEmit` → **exit 0（クリーン）**（casing import bug 1件を修正後）。
- **実レンダ目視**（`outputs/pd-visual-system/core5_check/*.png`・PDCore5構成）:
  - PenaltyVsProperty＝$10,000(青) vs $42,006(金)バー＋出典 ✅
  - EvidenceReveal＝証拠カード（ペーパークリップ/設計図スキャン/caption）✅
  - CaseJourney＝Procedural history 経路（ノード＋描画線）✅
  - QuoteUnderExamination＝大セリフ＋"— THE COURT"＋金下線 ✅
  - VerdictReversal＝赤"REVERSED"スタンプ ✅
- 発見・修正: プレビューで各部品に `dur` 未指定だと comp 全長基準で動く→preview.tsx で `dur={seg}` 明示（部品自体は正しく `dur` 対応）。

## 4. 成果物 / 変更ファイル
- 新規: `remotion/src/components/core5/index.tsx`（5部品＋alias）/ `remotion/src/components/core5/preview.tsx`（PDCore5ギャラリー）
- 変更: `remotion/src/Root.tsx`（`PDCore5` 構成を1件登録＋import）
- 生成(検証用): `outputs/pd-visual-system/core5_check/frame_*.png`（6枚）
- 文書: 本 `core5_report.md`

## 5. プレビュー方法
```
cd remotion && npm run studio    # Studio で "PDCore5" を選択
# or 単フレーム: npx remotion still PDCore5 out.png --frame=45
```

## 6. リスク / 限界 / 次
- 各部品の全 test（5/8/12秒・長文・欠損・比率精度）は preset 網羅で今後拡充（今回は代表 dur=3s で描画確認）。
- EvidenceReveal は asset 指定時の focusRegions ステップを実素材で要確認（今回は card モードを描画）。
- **適用先=EP37**（DEC-20260712-002）。timbs baseline は P06 で B1 版の test-bench に使用。
- rollback: `core5/` 削除＋Root.tsx の PDCore5 追記2箇所を戻す（既存構成に非干渉）。
