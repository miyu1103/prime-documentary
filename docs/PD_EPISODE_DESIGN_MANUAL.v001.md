# PD エピソード設計マニュアル v001（2026-08-03）

新しい話（EP61以降）を設計するときの手順書。**散文の設計書の書き方は変えない。**
変えるのは「決める順番」と「機械が読める形で何を渡すか」。

対象：設計を担当するスレ。組み立て側は `docs/PD_EP60_ASSET_PIPELINE_POSTMORTEM.v001.md` の A章も併読。

---

## 0. 目的（これを外すと全部ずれる）

**毎日1本を12:00 JSTに出し続けて稼ぐこと。**

- 再生されない・登録者が増えないのは**失敗ではない**（運）
- **防げたミスをするのが失敗**
- BANされるのは論外

だから設計書の役目は「良い作品の説明」ではなく、**組み立てが止まらず・間違えずに走りきるための契約**。

---

## 1. たった一つの原則

> **宣言されていない値は、推測せずエラーにする。**

2026-08-02、受入ゲート30項目のうち **6項目が9話すべてで不合格**だった。作品が悪かったのではない。
どの話も自分の尺・語数・構成・必要素材数を宣言しておらず、ゲートが黙って
「11.5〜12.5分の番組」という既定値に落ちていた。

赤が常時6件出ていると**赤が普通の状態**になる。その中に本物の欠陥3件
（見ずに合格印を押す素材QC・一度も実行されていない二重投稿ガード・別レンダーの検査記録）が
何ヶ月も隠れていた。

---

## 2. 決める順番（この順でないと手戻りする）

### ① テーマ候補を出す → **素材の在庫を先に測る**

**設計を書く前に測る。** EP60は40分の設計を完成させてから素材を探し、
**検索語38個のうち37個が空振り**した。「コンクリートのひび」「駐車場の柱」「配筋の腐食」——
この話の核心の画がアーカイブに一本も無かった。先に測っていれば題材選びが変わっていた。

```
scripts/check_cross_episode_reuse.py --check-query <語>   # 話またぎの被り率。20%超は捨てる
scripts/search_archive.py --sheet <語>                     # ヒットしたファイル群の種類数を見る
scripts/scan_video_shape.py                                # 縦動画・HD未満の除外（棚の約3割）
```

判断基準（EP60実測より）：

- **検索のゼロは「棚に無い」ではなく「その言葉では届かない」。** `concrete` は 0/24 だったが、
  `bridge` 215本・`abandoned` 153本・`underpass` 49本で在庫があった。**物の名前でなく場所の名前で引く。**
- **1語がファイル群1〜2種類にしか届かないなら、その語は使えない。** 実測：`concrete` 24/24、
  `column` 24/24、`boxes` 24/24 が全部同じ群。検索は概念ではなくラベルを引いている。
- **ファイル名は中身と無関係。** `empty_parking_garage.mp4` がつらら、`evidence_locker_shelves` が皿、
  `courtroom_gavel_block_macro` の19本が硬貨と食べ物。逆に `open_safe_empty` がEP60最良のプールデッキ空撮だった。
  **ファイル名による自動選定を設計に入れない。**

### ② 尺を決める → **数字で宣言する**

**尺の正は `episodes/<EPID>/episode_spec.v*.json` の `runtime_seconds` ただ1つ。**
（2026-08-23 訂正：それまで「11.5分」「30分」「三段（8-11/15-22/18-30分）」の3つの答えが
別々の文書に書かれていた）

- `check_final_acceptance.py:284` は **まず spec の `runtime_seconds` を読む。** 宣言があれば
  それが band になる。実測で確認済み。
- **宣言が無い話数だけ** `manifest.target_duration_minutes` に落ち、それも無ければ
  **690〜750秒（11.5〜12.5分）** の既定で測られる。EP50-59 が全滅したのはこれ。
- `PD_EDITORIAL_DIRECTION.v002.md` の三段（Daily 8-11 / Investigates 15-22 /
  Prime Original 18-30）は**企画を選ぶときの目安**であって、ゲートが読む値ではない。
- 実績としては30分が多い（実測1656〜1786秒）。ただしそれは**慣習であって既定値ではない。
  話ごとに必ず宣言する。**

### ③ 「映してはいけないもの」を書く ← **最重要**

散文に書いても機械は読まない。**必ず `forbidden_subjects` / `forbidden_claims` に列挙する。**

実際に起きたこと：

- **EP56**：Martin Griffiths はバスで亡くなった。設計書は「バス・バス停・道路・ロープ・薬・遺書を
  全編で禁止」と明記していたが、組み立て側が `london street` で検索し、**赤いバスが9:25に4.8秒入った。**
- **EP60**：「崩落・瓦礫・救助・遺体を描かない」と決まっていたが、組み立て側の検索語に
  `rubble collapse` `search and rescue` が入り、**31本が集まった。** 人物素材4枚も抵触し、
  film から108箇所参照されていた。

どちらも散文には書いてあった。**機械が読めなかっただけ。**

### ④ 台本を書く（語数を測って宣言）

ナレーション実測 4,673〜4,750語（30分）。**ト書きや前書きを含めた語数ではなく、読み上げる語だけ**を数える。

### ⑤ 演出データ（figure beats）を作る

**1幕13〜17個。** EP57は10個、EP58/59は8個で、ゲートが「紙芝居」と判定した
（0.37 beats/min、必要2.5）。EP52〜56は78〜91個。

`scripts/set_figure_beats.py --config <filmconfig> --beats <json> --dry-run` が
Remotionの型定義を読んで検証する。**書き込み前に必ず通す。**

### ⑤b After Effects のビートを置く（**EP77以降は必須**）

決定は `decisions/0011-AE-FROM-EP77.md`（2026-08-23）。オーナー指示は
「**77話以降は設計段階から AE をガッツリ使う**」。まず設計で効かせる。

**どれだけ置くか（下限。目標ではない）**

| 項目 | 下限 | 根拠（2026-08-23 実測・spec を持つ26話） |
|---|---|---|
| ビート数 | **12** | 中央値は8幕×13〜17＝図版104〜136個。AEはその約1割 |
| 1幕あたり | **1** | 12個を1幕に固めたら別の映画になる |
| 画面に出る合計秒数 | **90秒** | 12個 × 7.5秒（ヒーローカードが読める長さ） |

旧基準は PD_CANON §6 の「中盤に1〜2回」で、これは全図版の1〜2%。**そこから6〜12倍にする。**

**何をAEに任せるか（9種類から選ぶ）**

`hero_number`（数字1つを大きく） / `document_blowup`（書類の一点を拡大） /
`comparison`（AとBを並べる） / `timeline` / `system_map` / `quote_card` /
`map_move` / `list_build` / `title_card`。

カット・字幕・OP/ED・モーションブラー・38種の図版は **Remotion のまま**。
同じものを二重に作らない（不変条件14）。

**書き方**

`episode_spec` に `ae_beats` を書く（テンプレートは §4）。1ビートごとに
`id` / `act` / `kind` / `headline`（60字以内）/ `source` が要る。

**`source` は必須で、逃げ道が無い。** AEカードは画面で事実を主張するので、
タイトルと同じ `factual_support` の対象（rule 19）。台帳の行番号か台本の行を必ず書く。

**検証（設計段階で走る。AEもGPUも要らない）**

```
py -3.11 scripts/check_episode_spec.py --slug <slug>
py -3.11 -m pytest tests/test_ae_beats_design_gate.py -q
```

**この検査が保証しないこと。** 「AEカードが実際に描けたか」は見ていない。
EP76で図版8個が真っ白になりかけた件と同じで、**画素を読む検証は組み立て段階**に別途要る
（`decisions/0011`）。設計が通っても、描けた証拠にはならない。

### ⑥ 画像を発注する → **足りない分だけ**

**「たぶん足りない」で発注しない。** 順番は：

```
被り率を測る → ファイル群の種類数を見る → コンタクトシート → 目視 → 残った本数を数える → 不足分だけ発注
```

EP60は34モチーフを見て「実写75本」と確定させてから、バッチE=100枚を決めた。

### ⑦ 契約ファイルを書く（これが無いと組み立てが始まらない）

`episodes/<EPID>/episode_spec.v001.json`。テンプレートは §4。

---

## 3. 複数スレで1話を作るときの事故（実際に起きた）

**納品済み ≠ レンダーが読める。**
EP60のバッチC・Dの64枚は `H:` にあったが `remotion/public/surfside/img` に1枚も無く、
そのままレンダーすれば**1コマも映らなかった**。
**納品の検証先は必ず `remotion/public/<slug>/img`。**

**同じ役割の素材が違うルールで2組できる。**
EP60は顔素材が2系列でき、片方の4枚が絶対禁止に抵触していた。
**系列ごとに、どのブリーフで作られたかを記録する。**

**余った素材は黙って捨てられる（修正済みだが、原理は覚えておく）。**
EP54は静止画134枚に対し画像カット119個で、余った15枚が**アルファベット順の末尾**から切られた。
その末尾が、法廷映像が棚に無いから作らせた14枚だった。
いまは新着素材が先頭に固定され、捨てた分は毎回出力される。

---

## 4. 契約ファイルのテンプレート

```json
{
  "schema_version": "1.0.0",
  "episode_id": "PD-2026-061-<slug>",
  "slug": "<slug>",
  "runtime_seconds": [1620, 1920],
  "script_words": [4400, 4900],
  "section_vocabulary": ["HOOK","OP","ACT_1","ACT_2","ACT_3","ACT_4","ACT_5","ENDING"],
  "figure_beats_per_act": [13, 17],
  "distinct_video_assets": 234,
  "people_plates_min": 8,
  "mandatory_stills": [],
  "thumbnail_candidates_min": 3,
  "footage_review_required": true,
  "audio_layers": 2,
  "forbidden_subjects": [],
  "forbidden_claims": [],
  "ae_beats": {
    "min_count": 12,
    "per_act_min": 1,
    "screen_seconds_min": 90,
    "jobs_file": "scripts/ae/jobs_<slug>.json",
    "gpu_accel": "SOFTWARE",
    "beats": [
      {"id": "AE001", "act": "HOOK",  "kind": "hero_number",
       "headline": "$86,900", "source": "FACTS_LEDGER row 12", "duration_sec": 8},
      {"id": "AE002", "act": "ACT_1", "kind": "document_blowup",
       "headline": "NO CHARGES FILED", "source": "script.en.v001.md:57", "duration_sec": 9}
    ]
  },
  "notes": ""
}
```

- `ae_beats` は **EP77以降は必須**（`decisions/0011`）。EP76以前は書かなくてよく、
  書いても検査は通る。下限と考え方は §2 の ⑤b。
- `beats` は12個以上・全幕に1個以上・合計90秒以上。**この3つは同時に満たす必要がある。**
- `gpu_accel` は既定 `SOFTWARE`。このPCではAEのGPU支援が不安定（`decisions/0011`）。

- `distinct_video_assets` = `runtime_seconds[0] × 0.65 ÷ 4.5`。**「上限2回まで使える」前提で半分にしない。**
  EP54はそれで188本しか用意せず、253カットに対し**65回の使い回し**になった。
- `mandatory_stills` = **この話のために作らせた画像は全部書く。** 書けば組み立て後に照合される。
- `section_vocabulary` = 台本の見出しをそのまま。EP60は `THE_NIGHT` を含む10区分。

検証：

```
scripts/check_episode_spec.py --slug <slug>        # 宣言の不足を着手前に弾く
scripts/check_spec_satisfied.py --slug <slug>      # film.json生成後・レンダー前に照合
```

---

## 5. 組み立て側への引き継ぎチェックリスト

- [ ] `episode_spec.v001.json` が `check_episode_spec.py` を通る
- [ ] 台本の確定版のファイル名を明示（古い稿がどこにあるかも書く）
- [ ] `forbidden_subjects` / `forbidden_claims` を記入済み
- [ ] `figures_by_section` が1幕13個以上（`set_figure_beats.py --dry-run` 通過）
- [ ] 画像は `remotion/public/<slug>/img` に置いたか、置く担当を明示
- [ ] 素材の在庫を測った結果（何本足りず、何枚をAI画像で埋めるか）
- [ ] 尺が30分でない場合、`manifest.json` に `target_duration_minutes`

---

## 6. 覚えておくこと

**一度も落ちたことのない検査は飾り。**
新しい検査を足したら、わざと壊した入力で拒否されることを実演してから使う。

そして仕組みで防げないものが2つある：

1. **意味の一致** ——「法廷」という名の素材が、その一文に合っているかは機械に判定できない。目で見るしかない。
2. **面白いかどうか** —— これは運の領域。ここで失敗しても失敗ではない。

参照：`CLAUDE.md` §4.6 ／ `docs/PD_EPISODE_SPEC_STANDARD.v001.md` ／
`docs/PD_EP60_ASSET_PIPELINE_POSTMORTEM.v001.md`
