# Lottie Download List（LottieFilesで手動DLする分）

> **ステータス: 設計／前提・仮定**

## 0. 前提・仮定

- 本書は `docs/lottie-asset-workflow.md` の**実行用DLリスト**。LottieFiles で**手動検索→商用ライセンス確認→手動DL**するローカル JSON だけを対象にする、そのまま使える調達リスト。
- **整合チェック済み**: `docs/lottie-asset-workflow.md`（命名 `LT-NNNN__<slug>.json`・配置 `remotion/public/assets/lottie/`・ライセンス記録必須・ブランド着色方針）、`docs/asset-factory.md`（`lottie_assets` カテゴリ・manifest）、`docs/asset-priority-list.md` グループ G（数量）、`episodes/_planning/VIDEO_RULES.md` §5（商用OKのみ）、`remotion/src/brand.ts`（配色）。
- **禁止（厳守）**: LottieFiles の **API キー・クラウド連携・有料プラン・有料素材購入は使わない／前提にしない**（`docs/lottie-asset-workflow.md` §7）。**手動DLのローカル JSON / dotLottie のみ**。
- 命名・配置:
  - ID = `LT-NNNN`（`LT-0001` から連番。manifest の `id` と一致）。
  - 保存名 = `LT-NNNN__<slug>.json`（dotLottie は `.lottie`、プレビューは `LT-NNNN__<slug>.preview.png`）。
  - 配置 = `remotion/public/assets/lottie/`（軽量JSONは public 直置き可。実体退避先 `H:\pd-media\assets\factory\lottie_assets\` にも保存）。
- **ライセンス（商用可）を必ず確認・記録**: 各 DL で `name / commercial(=true のみ採用) / attributionRequired / attribution / author / sourceUrl / acquiredAt` を manifest に残す。1つでも欠ける・商用不可・ライセンス記載なしは**採用しない**（`docs/lottie-asset-workflow.md` §3）。**外部素材は推奨前に商用ライセンス確認**（メモ rights check before download）。
- **ブランド着色方針**: できれば**単色・モノクロ寄り**の素材を選び、`LottieMotion` の `tint`（Phase4・Lottie 色キー差し替え or CSSフィルタ）で**ブランド色へ着色**する。線/矢印=electric blue `#1F6BFF`、強調=gold `#E5B53A`、地=ink `#0A0A0C`/navy `#0B1A2B`。多色の派手な素材・テキスト入りは避ける（画面文字なし）。
- **選定基準（全項目共通）**: ①軽量（ベクター・少パス）②単色化しやすい（塗り分けが単純）③商用ライセンス明示 ④テキストなし ⑤ループ可否が用途に合う。

---

## 1. 用途別 DL リスト

> 各項目: 候補ID / LottieFiles 検索キーワード / 選定基準（軽量・単色化しやすい・商用可）/ 保存名 / 用途 sceneType。**各 ID はDL候補の暫定採番**（実採番は manifest と一致させる）。各用途 2〜3 個を目安に**最も軽量・単色なものを選抜**。

### A. arrow（矢印）

| 候補ID | 検索キーワード | 選定基準 | 保存名 | 用途 sceneType |
|---|---|---|---|---|
| LT-0001 | `arrow draw`, `arrow line`, `pointer` | 単線・1色・描画(draw on)アニメ・軽量 | `LT-0001__arrow_draw.json` | timeline, solution_reveal |
| LT-0002 | `arrow animation`, `directional arrow` | ループ不要・出現のみ・単色化容易 | `LT-0002__arrow_appear.json` | comparison, solution_reveal |
| LT-0003 | `curved arrow`, `flow arrow` | 曲線1本・関係/流れ表現・軽量 | `LT-0003__arrow_curved.json` | evidence_board, timeline |

### B. line draw（線が描かれる）

| 候補ID | 検索キーワード | 選定基準 | 保存名 | 用途 sceneType |
|---|---|---|---|---|
| LT-0004 | `line draw`, `underline`, `stroke` | 単線ストローク・下線強調・1色 | `LT-0004__line_draw.json` | timeline, evidence_board |
| LT-0005 | `divider line`, `drawing line` | 横一線の描画・章/区切り・軽量 | `LT-0005__line_divider.json` | chapter_title, explanation |

### C. check（チェック完了）

| 候補ID | 検索キーワード | 選定基準 | 保存名 | 用途 sceneType |
|---|---|---|---|---|
| LT-0006 | `check`, `success check`, `tick` | アウトライン・単色・短い完了アニメ | `LT-0006__check.json` | comparison, solution_reveal |
| LT-0007 | `checkmark circle`, `success` | 円+チェック・単色化容易・gold/electric着色前提 | `LT-0007__check_circle.json` | solution_reveal, summary |

### D. warning（警告）

| 候補ID | 検索キーワード | 選定基準 | 保存名 | 用途 sceneType |
|---|---|---|---|---|
| LT-0008 | `warning`, `alert`, `caution` | 三角+!・アウトライン・単色・テキストなし | `LT-0008__warning.json` | problem_statement |
| LT-0009 | `error alert`, `attention` | 短い注意喚起・単色化容易・控えめ | `LT-0009__alert.json` | problem_statement, evidence_board |

### E. map pin（地図ピン）

| 候補ID | 検索キーワード | 選定基準 | 保存名 | 用途 sceneType |
|---|---|---|---|---|
| LT-0010 | `map pin`, `location pin`, `marker drop` | ピン落下/出現・単色・軽量 | `LT-0010__map_pin_drop.json` | place_intro, timeline |
| LT-0011 | `location marker`, `pin pulse` | パルス付きピン・単色化容易・ループ可 | `LT-0011__map_pin_pulse.json` | place_intro |

### F. chart（グラフ描画）

| 候補ID | 検索キーワード | 選定基準 | 保存名 | 用途 sceneType |
|---|---|---|---|---|
| LT-0012 | `bar chart`, `graph animation` | 棒が伸びる・データなし枠のみ・単色化容易 | `LT-0012__bar_chart.json` | data_reveal, comparison |
| LT-0013 | `line chart`, `growth graph` | 折れ線描画・単線・テキストなし | `LT-0013__line_chart.json` | data_reveal, comparison |
| LT-0014 | `pie chart`, `donut chart` | 円グラフ展開・単色階調化可・軽量 | `LT-0014__pie_chart.json` | data_reveal |

### G. loading（読み込み）

| 候補ID | 検索キーワード | 選定基準 | 保存名 | 用途 sceneType |
|---|---|---|---|---|
| LT-0015 | `loading`, `spinner`, `progress` | 単色スピナー・ループ可・最軽量 | `LT-0015__loading_spinner.json` | reenactment, data_reveal |
| LT-0016 | `progress bar`, `loading bar` | バー進行・単色化容易・UI演出 | `LT-0016__progress_bar.json` | reenactment, data_reveal |

### H. business icon（ビジネス系アイコン）

| 候補ID | 検索キーワード | 選定基準 | 保存名 | 用途 sceneType |
|---|---|---|---|---|
| LT-0017 | `business icon`, `finance icon` | line icon・単色アウトライン・テキストなし | `LT-0017__business_icon.json` | company_profile, explanation |
| LT-0018 | `growth`, `chart up icon` | 成長/上昇・単色化容易・控えめ | `LT-0018__growth_icon.json` | company_profile, data_reveal |
| LT-0019 | `document icon`, `report line icon` | 書類アイコン・単色・evidence系に汎用 | `LT-0019__document_icon.json` | evidence_board, explanation |

### I. UI accent（UI装飾・スキャン/フォーカス）

| 候補ID | 検索キーワード | 選定基準 | 保存名 | 用途 sceneType |
|---|---|---|---|---|
| LT-0020 | `scan`, `focus`, `ui motion` | スキャンライン/フォーカス枠・単色・調査演出 | `LT-0020__scan_focus.json` | evidence_board, data_reveal |
| LT-0021 | `cursor`, `toggle`, `ui accent` | カーソル/トグル・単色・軽量UI風 | `LT-0021__ui_cursor.json` | reenactment, data_reveal |

### J. chapter decoration（章装飾アニメ）

| 候補ID | 検索キーワード | 選定基準 | 保存名 | 用途 sceneType |
|---|---|---|---|---|
| LT-0022 | `divider`, `flourish`, `ornament` | 装飾区切り・単色・テキストなし | `LT-0022__chapter_flourish.json` | chapter_title |
| LT-0023 | `title reveal`, `frame reveal` | 枠出現アニメ・単色化容易・章扉用 | `LT-0023__title_frame_reveal.json` | chapter_title, opening_hook |

---

## 2. 合計の目安数

| 用途 | 個数 |
|---|---|
| A. arrow | 3 |
| B. line draw | 2 |
| C. check | 2 |
| D. warning | 2 |
| E. map pin | 2 |
| F. chart | 3 |
| G. loading | 2 |
| H. business icon | 3 |
| I. UI accent | 2 |
| J. chapter decoration | 2 |
| **合計** | **23 個** |

> **目安: 各用途 2〜3 個 → 合計 ~23 個（~25 個規模）**。priority-list グループ G（MVP 14 個）を満たし、将来拡充（~25）まで見込んだDL候補。
> 図解の主力は **SVG/Remotion 描画（priority-list グループ B）** とし、Lottie は**軽量演出パーツの補助**に留める（`docs/lottie-asset-workflow.md` §0）。まず P1（arrow / line draw / check / map pin / chart / business icon）を優先DL、P2（loading / warning / UI accent / chapter decoration）は後追い。

---

## 3. DL ごとの手順（再掲・必須）

1. LottieFiles で検索キーワードから探す → **商用利用可・帰属要否を確認**（不明・有料のみは不採用）。
2. **単色・軽量・テキストなし**を満たす最良の1つを選ぶ。
3. **手動DL**（JSON / dotLottie）。API・クラウド同期は使わない。
4. `LT-NNNN__<slug>.json` にリネームし `remotion/public/assets/lottie/`（＋H: の `lottie_assets/`）へ保存。
5. manifest に1エントリ登録: `id` / `type="lottie_assets"` / `sourceTool="lottie"` / `license{name,commercial=true,attributionRequired,attribution,author,sourceUrl,acquiredAt}` / `mood` / `intensity` / `useCases` / `compatibleSceneTypes`（20語彙）/ `colorTone`（ブランド配色語彙）/ `tags`。
6. ブランド着色: `tint` で line=electric blue、強調=gold へ寄せる（Phase4 で実装）。
7. `LottieMotion` 経由 `staticFile('assets/lottie/LT-NNNN__<slug>.json')` で参照（`@remotion/lottie` は Phase4 で導入）。

## 4. 注意（ライセンス・商用可の確認と記録）

- **商用利用可（`commercial=true`）以外は棚に入れない**（VIDEO_RULES §5 / asset-factory §4.1）。
- 帰属表記が必要な素材は `attribution` 文字列を必ず記録し、出典テロップ運用に乗せる。
- **権利不明・ライセンス未記載は採用しない**。1点ずつ出典URL・作者・取得日を残す（監査可能に）。
- LottieFiles の「Free / Simple License」表記でも、**作品ページごとに商用可否を個別確認**する（作者設定で異なる場合がある）。

## 参照

- `docs/lottie-asset-workflow.md` — Lottie 運用フロー・命名・ライセンス記録・着色・禁止事項。
- `docs/asset-factory.md` — `lottie_assets` カテゴリ・manifest・importer 接続。
- `docs/asset-priority-list.md` グループ G — 数量・優先度。
- `episodes/_planning/VIDEO_RULES.md` §5 — 権利（商用OKのみ）。
- `remotion/src/brand.ts` — ブランド配色。
