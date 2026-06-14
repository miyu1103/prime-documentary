# remotion — Prime Documentary render pipeline

編集エンジン（decisions/0002 §A）。図解・テロップ・章カード・キネティックタイポ・パララックス・
オープニング・サムネを**コードで描画**し、FFmpeg で書き出す。DaVinci GUI 手仕上げは行わない。

## セットアップ
```bash
cd remotion
npm install
npm run studio        # プレビュー（http://localhost:3000）
npm run typecheck     # 型チェック
```

## レンダー例
```bash
# オープニング動画
npx remotion render Opening out/opening.mp4
# サムネ静止画（A/B は --props で variant/title/background を差し替え）
npx remotion still ThumbnailFrame out/thumb.png --props='{"title":"...","variant":"center"}'
```

## 現状の composition
- `Opening` … ロゴリビール＋地平線（§G ブランド）。
- `ThumbnailFrame` … 黒地＋ゴールド地平線＋白大文字＋PDマーク（§D/§G）。背景は Midjourney still 差し込み可。

## ブランド
全色・フォントは `src/brand.ts`（唯一の真実源）。`assets/brand/` の PNG が来たら `PdLogoImage` で合成。

## 今後（設計済み・未実装）
12分テンプレ composition、下部テロップ(出典・claim_id連動)、章カード、図解(関係図/年表/地図)、
キネティックタイポ、オープンキャプション、トランジション、A/B サムネ量産スクリプト。
入力は `edit_plan`（pd_factory 側）から渡す。
