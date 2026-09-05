# Lottie Asset Workflow — Prime Documentary

> **ステータス: 設計／前提・仮定**
> このドキュメントは Lottie 軽量演出パーツの運用ルールを定める。実装(Phase4)前の設計フェーズ。

## 0. 前提・仮定

- LottieFiles は**無料登録のみ**を使う。
- **APIキー・クラウド連携・有料プラン・有料素材購入は使わない／前提にしない。**
- 使うのは**手動でダウンロードしたローカルの Lottie JSON / dotLottie** のみ。Claude Code / Codex がそれを Remotion 内で操作する。
- Lottie は**メイン映像の生成手段ではない**。矢印・線・アイコン・図解パーツ・地図ピン・UI風モーション・章タイトル装飾などの**軽量演出パーツ**に限定する。
- 配置先（仮定として明記）: ユーザ表記 `public/assets/lottie/` は本 repo では **`remotion/public/assets/lottie/`** に対応する。本 repo の Remotion public ルートは `remotion/public/`。
- Lottie JSON は小さいため `public` 配下に置いてよい。重い元データを H: ドライブに退避する必要はない。
- 依存 `@remotion/lottie` は**未導入**。現状の `LottieMotion.tsx` は外部パッケージを import しない**非破壊プレースホルダ**。差し替えは Phase4 で Codex が行う。

## 1. 運用フロー（手動DL → 使用）

```
LottieFiles で検索 → ライセンス(商用可)確認 → 手動DL(JSON/dotLottie)
  → remotion/public/assets/lottie/ にリネーム保存
  → manifest に1エントリ登録(出典/作者/ライセンス/取得日)
  → LottieMotion(MotionDemo)で参照 → ラフカット/本編で使用
```

各ステップの責務:

1. **検索**: 用途に合う最小・軽量のモーションを LottieFiles で探す（検索語は §5）。
2. **ライセンス確認**: 商用利用可・帰属要否を必ず確認（§4）。不明なものは採用しない。
3. **手動ダウンロード**: JSON もしくは dotLottie をローカルに保存。API/クラウド同期は使わない。
4. **リネーム保存**: 命名規則（§2）に従い `remotion/public/assets/lottie/` に置く。
5. **manifest 登録**: `manifest.example.json` のフォーマットで1エントリ追加（§3, §6）。
6. **使用**: `LottieMotion` 経由で `staticFile('assets/lottie/<file>')` を参照。

## 2. 命名規則

```
LT-NNNN__<slug>.json          例: LT-0001__arrow_draw.json
LT-NNNN__<slug>.lottie        dotLottie の場合
LT-NNNN__<slug>.preview.png   任意のプレビュー静止画
```

- `LT-NNNN`: Lottie 連番ID（`LT-0001` から）。manifest の `id` と一致させる。
- `<slug>`: 小文字・英数・アンダースコア。用途が一目で分かる短い語（`arrow_draw`, `map_pin`, `check`）。
- 大文字・スペース・日本語をファイル名に使わない（クロスプラットフォーム安全、`.claude/rules/14`）。

## 3. ライセンス記録（必須）

各 Lottie について manifest の `license` に以下を残す。1つでも欠ける場合は**採用しない**。

- `name`: ライセンス種別（例 `LottieFiles Free / Simple License`, `CC0`, `CC-BY-4.0`）。
- `commercial`: 商用利用可否（`true` のみ採用）。
- `attributionRequired`: 帰属表記要否。
- `attribution`: 表記が必要な場合の文字列。
- `author`: 作者名。
- `sourceUrl`: 取得元 URL（LottieFiles の作品ページ）。
- `acquiredAt`: 取得日（`YYYY-MM-DD`）。

> 権利不明・商用不可・ライセンス記載なしの素材は使わない（CLAUDE.md 不変条件、`.claude/rules/13`）。
> 外部素材を推奨する前に商用ライセンスを確認する（メモ: rights check before download）。

## 4. サイズ・カラー方針（ブランド配色）

- **配色はブランドに合わせる**。基準パレットは `remotion/src/brand.ts` の `BRAND.color`:
  - ink `#0A0A0C` / navy `#0B1A2B` / electric `#1F6BFF`(主) / silver `#C8CDD6` / gold `#E5B53A`(アクセント) / white `#F5F7FA`。
- **着色方針**:
  - できれば**単色・モノクロ系の Lottie** を選び、`LottieMotion` の `tint`（Phase4 で Lottie の色キー差し替え or CSS フィルタ）でブランド色へ寄せる。
  - 多色の派手な素材は документ調と合わないため避ける。
  - 線/矢印は electric blue、強調は gold を基本とする。
- **サイズ**: 1920×1080 の演出パーツとして使う前提。元 JSON の `w`/`h` は小さくてよい（ベクターなのでスケール自由）。manifest に `width`/`height` を記録。

## 5. 用途別の探し方（検索語）

| 用途 | LottieFiles 検索語の例 |
| --- | --- |
| 矢印（描画/出現） | `arrow draw`, `arrow line`, `pointer` |
| 線・下線・アンダーライン | `line draw`, `underline`, `stroke` |
| アイコン | `icon outline`, `line icon`, `minimal icon` |
| 図解パーツ | `diagram`, `connector`, `flow`, `node` |
| 地図ピン | `map pin`, `location pin`, `marker drop` |
| UI風モーション | `loading`, `progress`, `toggle`, `cursor` |
| 章タイトル装飾 | `divider`, `flourish`, `title reveal`, `ornament` |
| チェック/成否 | `check`, `success`, `tick`, `cross` |

選定基準: 軽量・単色寄り・ループ可否が用途に合うこと・商用可。

## 6. Asset Factory / Asset Manifest との接続

- Lottie は Asset Factory の **`lottie_assets` カテゴリ**として扱う（SDXL 画像・stock とは別カテゴリの軽量モーション素材）。
- manifest の `type` は固定値 **`"lottie_assets"`**、`sourceTool` は **`"lottie"`**。
- Asset Manifest 側の共通フィールド（`mood`, `intensity`, `useCases`, `compatibleSceneTypes`, `colorTone`, `tags`）を埋め、シーンプランナーが用途・シーン種別から選べるようにする。
- 連番 `id`（`LT-NNNN`）でファイル名・manifest・参照を一貫させる。
- 既存の episode 別 manifest（`episodes/.../manifest.json`）とは独立した**横断ライブラリ**として `remotion/public/assets/lottie/manifest.json` に集約する（`manifest.example.json` がテンプレート）。

## 7. 禁止事項

- LottieFiles **API キー・クラウド連携・有料プラン・有料素材購入**の利用。
- **権利不明・商用不可・ライセンス未記録**の素材の使用。
- Lottie をメイン映像生成手段として使うこと（演出パーツに限定）。
- ファイル名・manifest・参照 ID の不一致。
- `@remotion/lottie` を Phase4 前に import してビルドを壊すこと。

## 8. Phase4 への引き継ぎ（Codex）

- `npm i @remotion/lottie lottie-web`（`remotion/` 配下）。
- `LottieMotion.tsx` のプレースホルダ描画を `<Lottie animationData={...} loop speed />` に差し替え（手順はファイル先頭コメント参照）。
- `tint` のブランド着色を Lottie 色キー差し替え or CSS フィルタで実装。
- Root.tsx / 既存コンポーネントは触らず、`MotionDemo` でのみ使用する。
