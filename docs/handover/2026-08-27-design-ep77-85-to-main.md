# 2026-08-27 — 設計レーン（EP77–85）→ メインスレ 引き継ぎ

このスレでやったことは全部ディスクとコミットに落ちています。チャットにしか無い情報はありません。
最新コミット `5c4a4db4`。ブランチ `claude/vibrant-archimedes-2mmr5h`。

---

## 0. 着手前の3コマンド

```
py -3.11 scripts/handover_snapshot.py
py -3.11 scripts/report_plate_delivery.py
py -3.11 scripts/check_episode_inputs.py --slug <slug>
```

3つ目が **READY to build** を出したら、その話数は組み立てに進めます。

---

## 1. いまの現在地（2026-08-27 実測）

| 話 | プレート | 実写 | i2v | 状態 |
|---|---|---|---|---|
| **77 keybridge** | 128 | 42 | 128 | **READY to build。組み立てスレへ引き渡し済み**（`docs/handover/EP77_KEYBRIDGE_TO_BUILD.md`） |
| **80 concordia** | 185 | 16 | 181 | **残り Root.tsx だけ**（下記2章） |
| 81 station | 188 | 0 | 156→188 生成中 | プレート判定・filmconfig・meta が未 |
| 82 valdez | 183 | 0 | 待機 | 同上 |
| 78 colgan | 166 | 66 | 待機 | 同上＋実写66本の全画面再判定 |
| 79 alaska261 | 198 | 51 | 待機 | 同上＋実写51本の全画面再判定 |
| 84 threemile | 186 | 0 | 未 | 全工程。**実写は集めない**（オーナー決定） |
| 83 max737 | 188 | 0 | 未 | 同上 |
| 85 katrina | 186 | 0 | 未 | 同上 |

**画像は9話とも4K＋深度が完成しています。Codex への追加発注はゼロです。**

---

## 2. EP80 concordia — あと1手で READY

```
$ py -3.11 scripts/check_episode_inputs.py --slug concordia
NOT READY -- 3 problem(s):
  - only 16 factory clip(s) (need >= 40)          ← オーナー決定で16本確定。下記5章
  - only 16 clip(s) survived visual QC ...        ← 同上（同じ事実の別表現）
  - no Remotion composition id starting with Ep80 in Root.tsx
```

**実写16本はオーナー決定（2026-08-27）で確定です。宣言値は下げません。**
`release_deviations.v001.json` に「16 vs 床40」として記録してください。理由は5章。

やること:

```
py -3.11 scripts/build_case_film_generic.py --config episodes/_planning/EP80_concordia_filmconfig.v001.json
# → remotion/src/data/concordia_film.json
# その後 Root.tsx に Ep80Concordia を登録（LahainaFilm.tsx と同じ形）
```

**Root.tsx はこちらで登録していません。** film.json が無い状態で登録するとバンドル全体が壊れます。

済んでいるもの: プレート185枚（全数 verdict・sha256 bind・binding=exact）／
filmconfig 70カード（`figure_spec` PASS）／youtube_meta（`check_packaging_claims` hard fail **0**）／
i2v 181本（マスターとバイト一致・depth混入0・saturation exit 0）。

未納は **N093 の1本**だけ。i2v レーンが 8/28 夜に seed を変えて振り直します。

---

## 3. 1話を仕上げる手順（EP81 以降はこれの繰り返し）

EP77 と EP80 で2回通した手順です。**この順でしか通りません。**

```
# ① プレートを全数見る（機械は絵を一度も見ない。ここだけは省略不可）
py -3.11 scripts/check_plate_verdicts.py --slug <slug> --scaffold --reviewer "<name>"
py -3.11 scripts/build_plate_contact_sheet.py --slug <slug> --per-sheet 4 --cols 2 --cell 776x437
#   → runs/qc/plate_sheets/<slug>/ を全部開いて読む
#   → 判定を runs/qc/<slug>_plate_decision.v001.json に {reject:{id:why}, note:{id:text}} で書く
py -3.11 scripts/apply_plate_decision.py --slug <slug> --decision runs/qc/<slug>_plate_decision.v001.json
#   → reject したものは img/rejected/ へ深度マップごと手で移す

# ② 実写プール（83/84/85 は不要。オーナー決定）
py -3.11 scripts/prestage_footage_review.py --slug <slug>
py -3.11 scripts/build_fullframe_strips.py --slug <slug> \
    --from-frames runs/qc/prestage_frames/<slug>/frames \
    --limit-to runs/qc/<slug>_prestage.v001.json --frames 3 --width 960 --stack
#   → runs/qc/fullframe/<slug>_candidates/ を1本ずつ読む
#   → runs/qc/<slug>_candidate_reasons.v001.json に {accept:{}, reject:{}} を書く
py -3.11 scripts/expand_candidate_reasons.py --slug <slug> --reasons <上のファイル>
py -3.11 scripts/prestage_footage_review.py --slug <slug> --decide runs/qc/<slug>_rejects.json --stage
py -3.11 scripts/write_factory_clip_qc.py --slug <slug>

# ③ filmconfig
#   episodes/_planning/EP80_concordia_filmconfig.v001.json を写して数値を差し替える
py -3.11 scripts/figure_spec.py --config episodes/_planning/EP<NN>_<slug>_filmconfig.v001.json

# ④ youtube_meta
#   episodes/PD-2026-080-concordia/09_package/youtube_meta.v001.json を写す
py -3.11 scripts/check_packaging_claims.py --slug <slug> --package     # hard fail 0 まで直す

# ⑤ 素材台帳 → 判定
py -3.11 scripts/build_asset_manifest_motionfirst.py --slug <slug>
py -3.11 scripts/check_episode_inputs.py --slug <slug>
```

---

## 4. このスレで作った道具（全部コミット済み）

| | |
|---|---|
| `build_fullframe_strips.py --from-frames --stack --limit-to` | prestage がキャッシュしたフレームから **1クリップ＝1枚の縦積み**を作る。コピー前に判定できる。**横並びだと読み手側の縮小で1枚520pxまで落ち、国が読めない**。縦積みなら約929px |
| `expand_candidate_reasons.py` | クリップID→ファイル名。両側が食い違ったら書かずに落ちる |
| `write_pool_frame_review.py` | reject を先に退避 → **退避後のプールの hash** で `pool_frame_review` を書く。途中で死んでも再実行できる |
| `apply_plate_decision.py` | scaffold の全行に judgement を流し込む。sha256 には触らない |
| `report_plate_delivery.py` | 発注 vs 納品 vs 4K化を毎回ディスクから数え直す |
| `scripts/ae/kinetic_card.jsx` ＋ `render_cards.sh` | **長尺用AEカード（1920×1080・透過）**。下記6章 |

---

## 5. EP80 の実写が16本しかない理由（同じ判断が他話でも要る）

候補80本を出し、36本を全画面で開いた結果です。**近い数字ではなく構造的に無理でした。**

**棚にある客船の映像は、全部に会社名が読めます** — Star Cruises（香港）/ VIKING（コトル）/
SILJA（ストックホルム）/ P&O（サウサンプトン）/ Holland America Line（シドニー）。
**実在の船を題材にした番組が、その船を棚から取れません。**
生き残ったのは「場所が写らない水」と「イタリアの海岸」で、それが16本です。

EP77 の歩留まりは **候補181本→採用32本＝18%**。EP80 は 80本→16本＝20%。
**この棚から40本を集めるには約200〜600本を全画面で読む必要があり、それが1話あたり半日の正体です。**

→ **オーナー決定（2026-08-27）: 83・84・85 は実写を最初から集めない。**
　プレート186〜188枚を i2v で動かせば映像比は満たせます。EP80 が実証しました。

---

## 6. AEカード — 部品を作りました。ただし4種類だけです

`scripts/ae/kinetic_card.jsx`（新規）が **1920×1080・透過webm** を吐きます。
`kinetic_beat.jsx`（ショート用・1080×1920）は**触っていません**。あれは動いているので。

**描けるのは4種類**: `hero_number` / `title_card` / `quote_card` / `list_build`。
EP77 の14枚中6枚がこれで、**書き出して `remotion/public/keybridge/ae/` に設置済み**です。

**残り5種類（`comparison` `timeline` `system_map` `map_move` `document_blowup`）は部品がありません。**
`render_cards.sh` はそれを**黙って空で通さず、名指しで拒否**します。
同じ内容は Remotion 側のカード（filmconfig の70枚）でカバーされています。

```
bash scripts/ae/render_cards.sh scripts/ae/jobs_<slug>.json          # 全部
bash scripts/ae/render_cards.sh scripts/ae/jobs_<slug>.json <id>     # 1枚だけ焼き直し
```

**AEの罠**: 強制終了するとクラッシュ修復ダイアログが出て**以後すべての起動を止めます**。
走っている間は触らないこと。`render_cards.sh` はビルドログが汚れていたらレンダーを拒否します
（AEはスクリプト失敗を終了コードに出さず、前回の .aep をそのまま焼き直すため）。

---

## 7. i2v レーンから（そちらが引き継ぎます）

キューは**独立プロセス（pid 37556）で生きています**。チャットとは無関係に動き続けます。
**このスレに張ってあった監視はセッションと一緒に消えるので、以後は自分で見に行く必要があります。**

```
tail -2 out_i2v_ep78_82.log
ls remotion/public/station/motion/*.mp4 | wc -l
nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader
```

見込み（実測 3.08分/本）: station 8/27 17:15 → valdez 8/28 02:40 → colgan 8/28 11:10 →
alaska261 8/28 21:20。詳細は `docs/handover/2026-08-27-i2v-ep78-82.md`。

**手作業が4つ残ります**（i2v レーンの3節）:
話数ごとの全数プレート対照QC / 設計レーンの reject 退避 / N093 の振り直し / 納品連絡。

> **このうちQCだけは省略しないでください。**
> 機械ゲートは「何が写っているか」を一度も見ません。EP77 はそれで **27%の人物混入**を素通りさせています。

**GPU を使う前に i2v レーンに宣言してください。** キューは `out_gpu_comfy.lock` を見て待つので
事故にはなりませんが、待った時間はそのまま遅れになります（EP77 と取り合って通算10時間後退）。
**ロックを消しての割り込みだけは絶対に避けてください。両方の作業が壊れます。**

---

## 8. 踏んだ罠（正典 `docs/PD_CANON.md` の 20a / 20b に追記済み）

1. **i2v は元プレートに無い人物を生成する。既定プロンプトで 27%**（EP77: 112本中30本）。
   明示プロンプト（`_chain_i2v_ep78_82.sh` の `BASE_PROMPT`）なら 0/182。
   **`check_motion_saturation` はこれを一切検出しない**（色しか測らない）。**検出は目視だけ。**
2. **人物禁止ネガは、元から写っている人まで消す**（EP77 H146 の作業員の腕）。
   無人のプレートにだけ使う。「すでに写っている人はそのまま、新しい人だけ入れない」。
3. **プレートの差し替えID**: 本編に既に入っている板は**新ID**（EP77 は H132–H147）。
   まだ何もビルドしていなくて `mandatory_stills` に載っている板は**同ID**（EP80 は N001/N104/N141）。
   逆にすると仕様と食い違うか、生きている板を上書きします。
4. **`check_pool_frames.pool_id_hash()` はファイル名のリストを取る。** `Path` を渡すと `TypeError`。
5. **reject を移動してから hash を計算しないと、verdict が存在しないプールに bind されます。**
6. **`stat` figure に `group` は無い**（`figure_spec.py` が拾う）。`value` は必ず数値。文字列だと
   100ピクセルの「NaN」として出荷されます。範囲は `stat` でなく `kinetic` の `lines` で書くこと。
7. **クエリは概念語でなく物の名前を引く。** EP80 で "wind / cliff / escalator / bubbles" を入れたら、
   棚はグランドキャニオン・風力発電所・地下鉄・ヤギ・アルカトラズを返しました。
8. **`git add remotion/public/<slug>` は動画と画像を巻き込む。** 一度 2.35GB をコミットして
   push が落ちました（リポジトリは既に 7.57GB）。**JSON と設計書だけをコミットすること。**
9. **納品ディレクトリはサブフォルダを見る。** EP82 の V079 は `img_raw_codex_batch_b_v001/` に
   届いていたのに、集計ツールがルートしか見ておらず1日「未納」と読んでいました。

---

## 9. 境界

- **EP77 と EP80 の所有権は組み立て側にあります。** `img/` `factory/` `motion/` を触らないこと。
  判定台帳はいまのファイルのハッシュに bind されています
- **1つの話数を2スレで同時に触らない**
- **予約・投稿は公開レーンだけ**。過去日付を指定すると即時公開されます

---

## 10. 次の一手（優先順）

1. **EP80 の film.json → Root.tsx**（15分。これで2本目が組み立てに乗る）
2. **EP81 station** — i2v が 17:15 に終わる。プレート188枚の判定から
3. EP82 → EP78 → EP79（i2v の完了順）
4. EP84 → EP83 → EP85（**実写なし**なので1話あたり半日）
