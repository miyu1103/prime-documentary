# v002 still-upgrade map — PD-2026-002-gideon

Vision comparison of the **in-cut stills** (`remotion/public/mj/…`, used by `GideonPremium`
`GIDEON_SCENE_IMG`) vs the **vision-selected vetted picks** (`05_visuals/selected/…`).
Recommendations for a **v002 polish pass** — **NOT yet applied** (the v001 cut is rendered and
pending owner approval; a parallel process is mid-edit). Apply as one clean pass: copy the chosen
pick into `remotion/public/mj/` as a new file, update `GIDEON_SCENE_IMG`, re-render, re-QC, and bump
`manifest.active_revisions.rights_manifest -> v002`. Rights for these picks are already registered in
`rights_manifest.v002.json` (AST-0222..AST-0251).

## Direct comparisons (reviewed)
| scene(s) | in-cut still | vetted pick | verdict | note |
|---|---|---|---|---|
| S015 (S012 SCOTUS) | `mj/s015_scotus_chamber.png` | `selected/05_supreme_court.png` | **SWAP** | 列柱の奥行き・電光青・厳粛さで明確に上。A はグレア過多 |
| S003, S027 (lone defendant) | `mj/s003_lone_defendant.png` | `selected/04_defense_table.png` | **SWAP** | 被告が完全シルエット（顔不可視◎）、弱者vs法廷の対比が圧倒的 |
| S002 (cold-open cell) | `mj/s002_prison_cell.png` | `selected/03_cell_writing.png` | **SWAP** | 「書く」動作でシンボリック拡張可、ランプ暖色×格子電光青◎。※S002の語りが"独房で書く"文脈か要確認 |
| S004 (arrest locale) | `mj/s004_courtroom_1961.png` / `s004_poolroom.png` | `selected/07_pool_hall.png` | **SWAP（要確認）** | ネオン即時認識で逮捕地として最強。※S004が現状"法廷"静止画なので、07は実際の"プールホール/逮捕"ビートに割当てること。※"POOL HALL"可読ネオン= invariant11の軽微注意（後処理ぼかし検討可） |
| S024 (document pile) | `mj/s024_overloaded_desk.png` | `selected/09_law_books.png` | KEEP + alt | 現行は孤立感が良い。09は配色/精度・スマホ映えで勝るので**v002代替候補**として保持 |

## Additive picks (no direct in-cut equivalent — optional v002 inserts)
- `selected/01_style_anchor.png` — ブランド establishing（ColdOpen の青光＋舞う塵の基準）に追加可
- `selected/02_pencil_letter.png` — S008 は **実在 petition 優先（real-first）** のため、02 は alt 挿入のみ
- `selected/06_light_through_bars.png` — S002 冒頭の"鉄格子から差す光"トランジション素材として追加可
- `selected/08_handcuffs.png` — 逮捕モチーフ挿入（S004/S006）。4090 深度パララックスで動かす
- `selected/10_corridor.png` — 監房廊下の挿入/トランジション素材
- `selected/11_thumb_bg.png` — サムネ背景（packaging）。title/thumbnail 承認ゲートで使用（暗部=左）

## Apply-checklist (when coordinating the v002 render)
1. ツリーがクリーンな状態で実施（並行編集の着地後）。
2. 採用 pick を `remotion/public/mj/<stem>_v2.png` としてコピー（既存 v001 ファイルは上書きしない）。
3. `GIDEON_SCENE_IMG` の該当 scene を新ファイルへ。S004 は実シーンのビートを scene_plan で確認してから割当。
4. 再レンダリング → `assemble_gideon_premium` → 再QC（`qc_report.v002`）。
5. `manifest.active_revisions`：`rights_manifest->v002`, `qc_report->v002`, `edit->v002`、events 追記。
6. 新カットの hash で **新しい first-cut APR** を再発行（旧 APR-0002 は再レンダで失効＝rule 12）。
