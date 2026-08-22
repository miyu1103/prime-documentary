# EP74 ITAEWON → 組み立てスレへの引き継ぎ

**日付 2026-08-22 · 作成 設計/素材スレ · 宛先 組み立て専用スレ**

これ1枚で組み立てに入れるように書いてあります。**先に「§0 3行で」と「§6 やってはいけないこと」だけ読んでください。**

---

## §0 3行で

- **EP74 は 2022年10月29日の梨泰院（イテウォン）雑踏事故。30分。R3（実在の死者159名・遺族存命・裁判継続中）。**
- **声・絵・台本・場面表は完成。実測で完成尺 31:36、宣言帯 [1740, 1920] の内側。**
- **残るは素材の選別と組み立てだけ。** 画像120枚は全数目視済み、素材は453本ダウンロード済みで未選別。

---

## §1 完成しているもと保存先

| もの | 保存先 | 実測 |
|---|---|---|
| **ナレーション音声（本番）** | `remotion/public/itaewon/narration.mp3` | **1,886.779秒**（ffprobe実測） |
| ナレーション原本 | `E:\pd-media\episodes\PD-2026-074-itaewon\06_voice\master\vc_master_v001.mp3` | 同一 |
| **ナレーション索引** | `episodes/PD-2026-074-itaewon/06_audio/narration_index.v001.json` | 343チャンク・各行の秒数と節 |
| **AI画像（板）** | `remotion/public/itaewon/img/` | **120枚・全枚 3840×2160** |
| 却下した板（保管） | `remotion/public/itaewon/img_rejected_v001/` | 6枚。**使わない**（退避済み） |
| **板の判定記録** | `runs/qc/itaewon_plate_verdicts.v001.json` | accept 120 / reject 0 / unresolved 0・sha完全一致 |
| 板のコンタクトシート | `runs/qc/plate_sheets/itaewon/` | 21枚 |
| **台本（正）** | `episodes/_planning/EP74_itaewon_script.en.v007.md` | 5,464語 |
| 台本（機械可読） | `episodes/PD-2026-074-itaewon/03_script/script.annotated.v007.json` | 221 span |
| **場面表（正・実測版）** | `episodes/_planning/EP74_itaewon_SCENE_PLAN.v003.md` | 526カット・平均3.60秒 |
| 設計書 | `EP74_itaewon_FILM_BIBLE.v001.md` ＋ `.v002.md`（v002はv001の§4/6/7/8/12.5を差し替え） | |
| **事実台帳** | `EP74_itaewon_FACTS_LEDGER.v001` 〜 `.v005.md`（**5冊すべて有効。後の版は追加のみ**） | 94行＋ABSENCE 11＋禁止17条 |
| **機械契約** | `episodes/PD-2026-074-itaewon/episode_spec.v002.json` | `check_episode_spec.py --slug itaewon` → exit 0 |
| 状態ファイル | `episodes/PD-2026-074-itaewon/manifest.json` | blockers はここに常時最新 |
| 画像発注書 | `EP74_itaewon_CODEX_BATCH_A.v001.md` ＋ `_BATCH_B.v001.md` | 済 |
| **サムネ候補** | `episodes/PD-2026-074-itaewon/10_thumbnail/` | 6案＋背景 `T01_bg.v002.png` |
| サムネ/題名の決定 | `EP74_itaewon_thumb_prompts.v002.md` | **実測で確定済み。§4参照** |
| 出荷前ファクトチェック | `episodes/PD-2026-074-itaewon/01_research/fact_recheck.v002.md` | 公開日の再確認リスト |

すべて `C:\Users\aab15\Documents\prime-documentary\` からの相対パスです。

---

## §2 まだ無いもの（＝組み立てスレの仕事）

`py -3.11 scripts/check_episode_inputs.py --slug itaewon` の実測で **3件**：

1. **`episodes/_planning/EP74_itaewon_filmconfig.v001.json`** — 未作成
2. **実写素材** `remotion/public/itaewon/factory/` が **0本**（40本以上必要／仕様上は265素材）
3. **`remotion/src/Root.tsx` に `Ep74` で始まるコンポジション** — 未登録

---

## §3 素材（実写）の現状 ← ここが唯一の山

**453本を新規ダウンロード済み。まだ1本も選別していません。**

- 実体：`D:\pd-archive\itaewon_korea_night\`（8.2GB）
- 索引：`E:\pd-archive\_ledger\*.jsonl` に登録済み（棚の検索から引ける）
- 検索語の定義：`config/episode_footage_queries.v001.json` の `episodes.itaewon`（119語）
- 取り込みのテーマ定義：`scripts/ingest_archive_sources.py` の `THEMES["itaewon_korea_night"]`

**手順（この順で）**

```
py -3.11 scripts/stage_episode_footage.py --slug itaewon --per-query 10 --dry-run
    → 候補を出し、コンタクトシートを runs/qc/prestage_frames/itaewon/ に作る
    → 何も staging しない（判定は棚の上でやる設計）

（人がシートを開いて選別）

echo '{"reviewer":"...","reject":{"<clip>.mp4":"理由"}}' > rejects.json
py -3.11 scripts/prestage_footage_review.py --slug itaewon --decide rejects.json --stage
```

**選別の下ごしらえは済んでいます**：`runs/qc/itaewon_title_triage_rejects.v001.json`
タイトルだけで落とせるもの（並木道・グリーンスクリーン・アニメ・他国・AI生成など）を規則化した除外案です。**目視の代わりではなく前段**として使ってください。

**AI生成が20本混ざっています**（ファイル名が `ai-generated`）。**これは全面禁止**です。機械で落とせます。

---

## §4 パッケージング（実測で確定済み・そのまま使えます）

すべて `check_packaging_claims.py` を通過（**claims=34 / unsupported=0 / CONTRADICTED ゼロ**）。

- **題名A**：`Officers Were Deployed To Four Of The Eleven Reports Before The Itaewon Crush`（77字）
- **題名B**：`The Court Convicted The Police Chief And Acquitted The District In Itaewon`（74字）
- **サムネ**：`3.2 METRES / 159 DIED IN THIS ALLEY`（案T01）
- **説明文**：`EP74_itaewon_thumb_prompts.v002.md` §5 に本文あり

**注意**：v001が推していた題名は**チェッカーに落とされました**（UNVERIFIED）。上の2案が実測で通ったものです。

---

## §5 組み立てが当てるべき時刻（実測・原盤から）

| 時刻 | 何 | 節 |
|---|---|---|
| 4:44 | **81,573 → 31,878**（AEビート） | ACT_1 |
| 8:14 / 8:16 | **ELEVEN / FOUR**（2秒差で一つの動作として） | ACT_2 |
| 12:13 | 十三分 | ACT_3 |
| **12:51** | **159**（5.0秒保持・映画で最長のカード） | ACT_3 |
| 15:14 | **137**（AEビート） | ACT_4 |
| 16:33 | **34 → 921**（AEビート・最も急な数字） | ACT_4 |
| 21:42 | **無罪の理由**（最大の引用カード・6.0秒保持） | ACT_5 |
| 23:06 | 第66条の11（2番目の引用カード・6.0秒保持） | ACT_5 |
| **26:35** | **STOPPED**（直前に1.5秒の designed silence） | ACT_5 |
| 29:24 | 柵（エンディングの主役画） | ENDING |

節ごとの尺・カット数・使う板の番号は `SCENE_PLAN.v003` §3 と §5 にあります。

---

## §6 やってはいけないこと（破ると出荷できません）

台帳の禁止条項17件が正本です（`FACTS_LEDGER.v001` の⛔表＋v003の⛔-15＋v004の⛔-16/17）。組み立てで特に効くのは：

1. **雑踏事故そのものを絶対に映さない。** 遺体・倒れた人・心肺蘇生・担架・血・覆われた人体、どれか1フレームでも入ったら終わりです。路地は**「空」「普通に混雑」「事後」の3状態のみ**。
2. **ACT_3 には人が写った素材を1本も入れない。** 場面表の指示です。
3. **死者は159人。160は使わない**（ナレーション・字幕・題名・サムネ・説明文すべて）。
4. **顔は可。ただし特定できてはいけない。** 板120枚はその前提で作って全数確認済みです。
5. **韓国の看板は韓国語か判読不能に。** 日本語・中国語・欧米の看板は、テキサスの映画にEUナンバープレートを出すのと同じ間違いです。
6. **木槌（ガベル）は出さない。** 韓国の裁判所は使いません。
7. **エンディングの「登録・コメント」の依頼はエンドカードのみ。ナレーションでは言わない**（`check_script_craft.SPOKEN_CTA` が hard gate。CTAを読み上げたショート46本中45本が登録転換ゼロ）。
8. **ACT_5 の李林宰（イ・イムジェ）証言のカットは、空の聴聞会室と白紙の名札に留める。** 地図や大統領府にカットを割ると、彼個人の「もしも」を映画の結論として演出したことになります。

---

## §7 踏むと1日失う罠（実測済み）

- **`check_script_length.py` を使わないでください。** HTMLコメントを台詞として数え、1話あたり1,000〜2,200語過大に出ます。語数は `gen_narration_case.py --dry-run` で測ります。
- **`--measure-section ACT_1` の外挿は過大評価になります。** 実測：ACT_1 195.5 wpm に対し全体 184.8 wpm。**ACT_1は3番目に速い節**です。初回の原盤は32:54で上限を54秒超過しました。
- **`preflight_render_gate.py` は勧告ではありません。** 32話中25話で失敗し、10話で無視され、EP70とEP71は字幕なし紙芝居を3時間かけて作る一歩手前でした。**レンダー前に必ず緑にしてください。**
- **棚の件数は当てになりません。** `alley`（10件）は**並木道**を、`train station` は**東欧のホームに顔の写った女性**を返しました。**必ずフレームを開いてください。**
- **却下した板をプールに残さない。** EP64 memphis は却下済み16枚が本編に入って取り下げになりました。EP74では退避済みですが、再生成のたびに起きます。

---

## §8 公開前に必ず再確認する1点

**`AB-11`：中断中の控訴審が再開していないか。**

ソウル高裁は2025年7月14日と8月28日に、**両方の控訴審を中断**しました（特別調査委員会の結論を待つため）。**この映画の最終幕はその事実の上に立っています。** 再開していたら最終幕を書き直す必要があります。

その他の公開日チェックは `fact_recheck.v002.md` §5 にあります。

---

## §9 検証コマンド（組み立て前に全部緑を確認）

```
py -3.11 scripts/check_episode_spec.py --slug itaewon
py -3.11 scripts/check_script_citations.py --slug itaewon
py -3.11 scripts/check_plate_verdicts.py --slug itaewon
py -3.11 scripts/check_image_order_neg.py --file episodes/_planning/EP74_itaewon_CODEX_BATCH_A.v001.md
py -3.11 scripts/verify_script_lint.py --ep PD-2026-074-itaewon
py -3.11 scripts/check_episode_inputs.py --slug itaewon
py -3.11 scripts/preflight_render_gate.py --ep PD-2026-074-itaewon   ← レンダー直前・必ず緑
```

2026-08-22 時点で、最後の2つ以外は**すべて緑**です。

---

## §10 この話が何の映画か（組み立ての判断に効くので）

**「主催者のいる催しのために書かれた規則は、主催者のいない群衆を見られない」**

- 137人の警官が梨泰院にいた。2km先の、その年に越してきた大統領府では、前年34件だった集会が5〜10月で921件になっていた。
- 3時間37分のあいだに11件の通報。**警官が向かったのは4件。**
- 裁判所は署長を有罪にし、区庁の職員を無罪にした。**理由は「主催者のいない催しに安全計画を作れと定めた規定が無かった」から。**
- その規定は今はある。2023年12月26日の改正。**事故の14か月後。**
- そして2025年夏、**両方の控訴審が止まった。**何が起きたのかを誰もまだ確定できていないから。

**カットに迷ったら、この5行に奉仕するかで決めてください。**
