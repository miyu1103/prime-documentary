# PD 正典 — ここだけ読めば動ける

**これは何か。** Prime Documentary の制作・出荷・運用について、いま何が真実で、何を踏んではいけないかを
1ファイルにまとめたもの。**新しいスレッドは着手前にこれを読む。**

**なぜ作ったか。** 情報が `CLAUDE.md` / `.claude/rules/` / `docs/`（81ファイル）/ `episodes/_planning/` の
申し送り / 各スレの記憶に散り、どれが現在地か分からなくなった。同じ失敗が別のスレで繰り返され、
2つのセッションが同時にカレンダーを書き換えて台帳が30本ずれた。

**この文書の設計。** 状態を表す数字には**必ずそれを測り直すコマンドを併記する**。
数字は必ず古くなる。古くなったことに気づけない文書は、無いより悪い。
**数字を信じるな。コマンドを走らせろ。**

**この文書が上書きしないもの。** `CLAUDE.md`（憲法）と `.claude/rules/`（拘束）が上位。
矛盾を見つけたら黙って推測せず、矛盾として報告する。

---

## 0. 最初の5分でやること

**チャンネルの現在地は自動で出る。**`SessionStart` フックが `scripts/pd_brief.py` を走らせるので、
「いま何が決まっていて、何を測っていて、何を触ってはいけないか」は**何も打たなくても**セッション頭に出る。
出典と理由まで見たいときだけ `--full`。**あとは `py -3.11 scripts/daily_status.py` を叩く。**
数字の唯一の置き場所は `config/pd_experiments.v001.json` で、**散文がそれと食い違ったら実測側が勝つ**。
走っている実験の対象動画を改題・サムネ差し替えすると比較が消える（`apply_title_batch.py` は拒否するが、
Studio の画面から手で変えたものは誰にも見えない）。 いまの実測値（両プラットフォームの在庫・
予約・クォータ）と、**次に打つコマンドが引数まで入った形**で出る。ここに書いた数字は古くなるが、
あれは毎回測り直すので古くならない。

```bash
cd /c/Users/aab15/Documents/prime-documentary
git pull                                          # 他スレの成果を取り込む
py -3.11 scripts/yt_channel_index.py              # 実チャンネルを列挙（唯一の正）
py -3.11 scripts/yt_schedule_audit.py | head -45  # 予約の現在地
```

そのうえで **§1 を測り直してから** 着手する。ローカルの manifest や
`youtube_schedule_result` は**最大11日古かった実績がある**。公開状況は必ず API。

---

## 1. いま何が真実か

> 下の数字は **2026-08-10 時点**。**必ず測り直すこと。**

| 対象 | 実測 | 測り直すコマンド |
|---|---|---|
| チャンネル総本数 | 150 | `py -3.11 scripts/yt_channel_index.py` |
| 公開中の長尺 | 55 | 同上（出力2行目） |
| 予約済み | 40（8/18まで） | `py -3.11 scripts/yt_schedule_audit.py` |
| ショート 制作済 | 186 / 計画195 | 不足9本 = EP038 / EP050 / EP060 / EP061 |
| ショート 未投稿 | 83（1日4本＝約21日分） | `bash scripts/daily_shorts_push.sh`（dry） |
| ショート 関連リンク | 対象81本すべて設定済（8/7＋8/10） | `node scripts/studio/related_link_batch.js --verify-only` |
| 関連リンク 行き先未確定 | 8本 | `runs/_cache/related_link_worklist.v002.json` の `unresolved` |
| TikTok | **アカウント作り直し中（2026-08-16 オーナー決定）**。v1 `@prime.documentary8` は152本すべて0再生で放棄。着手前に `docs/PD_TIKTOK_ACCOUNT_V2.v001.md` を読むこと | 同ファイル §0 の実測 |
| TikTok 用レンダー | 122本＋EP62-65の12本（8/10レンダー中） | `ls remotion/out/short*_tt.mp4` |
| 長尺エピソード | 65（EP62-65 は仕上げ中） | `ls -d episodes/PD-2026-0*` |

### 長尺の在庫が尽きている

12:00 JST の長尺枠は **8/15 まで埋まり、8/16 以降が空き**。
`yt_schedule_audit.py` のサマリ行は**全時間帯の最終予約**を基準に「次の空きは 8/19」と保守的に出す。
**12:00 の実データを見ること**（8/16-8/18 に出るのは 06/09/18/21 のショート）。

### ショートは1話3本（2026-08-10 オーナー決定・確定）

**1話3本で固定。**195本計画がこの前提で組まれており、EP53-56 の4本は例外として扱う。
両論併記だった `SHORTS_VERTICAL_PLATE_SPEC.v001.md` はこの決定に従う。

**同日決定：新規ショートの制作は止め、未投稿83本を1日4本ずつ流すだけにする。**
理由は実測——ショートは全再生の79%を稼ぐが**長尺への送客は0**、登録転換は長尺の1/3（1.16 対 3.95/千再生）。
83本は約21日分あるので、制作に使っていた時間はサムネ・タイトル・冒頭20秒に回す。

---

## 2. 絶対にやらないこと

1. **4類型が入ったまま公開しない** — 他社映像／実在未成年／名札転用／私人の個人情報
2. **予約済み動画の日付・公開状態を不要に触らない** — **過去日付の `publishAt` は即時公開になる**
3. **ゲートを通すために宣言値・しきい値を緩めない**（CLAUDE invariant 15）
4. **検査結果を使う前に、その検査がどのファイルを測ったか確認する**
5. **目視QCで却下した素材を使わない** — 却下クリップは機械ゲートを全部通る
6. **削除対象を日付で選ばない** — これで13本のつもりが137本消えた
7. **AI生成の判決文・新聞・警察文書・証拠を作らない**（invariant 11）
8. **実在人物の肖像を出さない**（人物像そのものは可）

---

## 3. 1スレだけが触るもの

| 対象 | 理由 |
|---|---|
| **配信カレンダー**（アップロード・予約・再配置） | 8/9 に2セッションが同時に書き換え、台帳が30本ずれた |
| **`remotion/src/data/<slug>_film.json`** | 同時書き込みで壊れた実績あり |
| **`episodes/<EPID>/manifest.json`** | 越境更新の事故あり |

着手前に他スレが動いていないか確認する。

---

## 4. レンダー中は重い処理を走らせない

**これは最も高くついた失敗。** 2026-08-09、長尺3本のレンダーが**エラーを1行も残さず**死んだ。
OSのイベントログにも痕跡なし、メモリは128GB中82GB空き。原因は**同じディスクを叩く並行作業**だった。

- EP52 morton: 61分の受入ゲートが同じディスクを叩き `Failed to fetch` で死亡
- EP62 greene: 93% まで進んで死亡、リトライも66%で死亡（マニフェスト再ビルド・4Kプレート読み込み・`du`・`find` と同時）

**機構化済み**: `scripts/guard_destructive.py`（Bash の PreToolUse フック）が
`remotion render` 実行中は `du` / `find` / マニフェスト再ビルド / film.json 生成 /
サムネ合成 / 全尺スキャン / 無制限 ffmpeg を**拒否する**。
ログの tail・単発 ffprobe・`ls`・git は通る。

---

## 5. 日々の運用

```bash
bash scripts/daily_shorts_push.sh      # ショート投入（索引削除→実取得→台帳同期→上げる→再取得して衝突報告）
```

- **12:00 JST は長尺専用。** ショートは **06:00 / 09:00 / 18:00 / 21:00 の1日4本**
- 自己申告で終わらせない。上のスクリプトは再取得して衝突まで報告する

---

## 6. 長尺の作り方

### EP77以降の入口は1つ（2026-08-23 オーナー指示・機械が強制）

```bash
py -3.11 scripts/ep_road.py --slug <slug>     # いまどの工程で、次に何をするかを実測で出す
```

**旧ルートは配線で塞いである。** EP77以降は `check_ep77_standard.py` を通らないと
[0/7]（台本テンプレ・7分ごとの問い・素材の他話被り）と [4d]（紙芝居の上限）で止まる。
台本は `episodes/_planning/_EP_SCRIPT_TEMPLATE.v001.md` から書く（型を満たせばゲートは構造的に緑）。
`preflight_receipt` は**退役**（`decisions/0012`・直近10話で要求成果物が0件だった）。
EP76以前は何も変わらない。

### 工程

```
題材 → 事実台帳 → 台本(3周) → scene_plan → 画像(Codex) → i2v モーション → 目視QC
  → 音(ElevenLabs + 4層ミックス) → 字幕 → film.json → probe → レンダー → mux → 受入 → 予約
```

### ゲートの鎖（この順に走る）

| ゲート | いつ | 何を見る |
|---|---|---|
| `check_episode_spec.py` | 最初 | 契約が揃っているか。**未宣言の値はエラー、既定値で埋めない** |
| `check_episode_inputs.py` | [0/7] | 入力（プール・音声・composition）。数秒で落ちる |
| `preflight_render_gate.py` | 組立後 | 計画そのもの。`preflight_receipt.v*.json` |
| `check_spec_satisfied.py` | film.json 後 | 必須スチルが実際にカットに入ったか／禁止主題が無いか |
| `probe_before_render.sh` | レンダー前 | 60秒スライスを描いて黒・凍結・動きを測り、**受領書を書く** |
| `pd_postrender_gate.py` | レンダー後 | 黒・凍結・尺 |
| `check_final_acceptance.py` | 最後 | 全項目。`--emit-receipt` で受領書 |

### 長尺に必ず入れるもの（2026-08-10 オーナー指示・それまでどの文書にも無かった）

**この2つは、承認済みなのに設計に入らず、記憶ファイルにしか残っていなかった。**
EP65 は実写7本で出荷し、AE は一度も使わなかった。文書に無いものは使われない。

- **アーカイブ実写をガッツリ使う。** `factory_used` の下限は45秒に1本（26分なら約35本）だが、
  **これは床であって目標ではない。60本以上を狙う。**
  EP65 が7本だったのは棚が薄いからではなく**検索語が悪かったから**（§10 参照：
  `police interview room`→0件 / `interrogation room detective`→12件）。
  0件は棚の事実ではなく**言葉の事実**。`--weak-ok --sheet` で必ず目視してから結論を出す。
- **AE キネティック文字を中盤に1〜2回。** 2026-08-04 にオーナー承認済み（short118 で実証）。
  置く場所は**数字と転換**。ジョブ定義は `scripts/ae/jobs_<slug>.json`、
  書き出しは `scripts/ae/render_beats.sh`。EP66 は 78日 / 15–22回 / ONE DOLLAR。

### 契約（`episodes/<EPID>/episode_spec.v001.json`）

**ツールが数字を読む唯一の場所。**設計書の散文は残すが、機械はこれしか読まない。
未宣言はエラー。既定値で補完してはならない。

### 予約の条件（rule 19・機械が強制）

`upload_schedule_case_v001.py` は次を全部満たさないと上げない。

1. `acceptance_receipt.v*.json` の `video_sha256` が**そのファイルの実 sha と一致**
2. **止めてよい失敗は4クラスだけ**（`real_person_likeness` / `rights_and_licence` /
   `factual_support` / `fabricated_record`）。それ以外は記録して出荷する。
   判断は `scripts/pd_ship_policy.py` が `config/ship_policy.v001.json` を読んで下す
   （`upload_schedule_case_v001.py:26` が import しているのを実測・2026-08-23）。
   **旧ルール（runtime_band ＋ accepted_deviations の部分集合の時だけ投稿）は
   2026-08-12 に廃止**。5日間ゼロ投稿の直接原因だった。詳細は `.claude/rules/19-ship-gate.md`
3. `sched_utc` が未来（過去なら dry-run でも拒否）

**APR は形が決まっている。** `check`/`decision:"accepted"` だけの JSON は**効かない**。

---

## 7. 踏み抜いた罠（全スレ横断）

### 計測器そのものが嘘をつく

1. **自分に一致する検索** — `ps | grep build_motion` が 0 を返す（`ps` は引数を出さない）。
   プロセス確認は PowerShell `Win32_Process` の `CommandLine` で。
   ただし**その検索コマンド自身がヒットする**ので除外すること
2. **`ls out/*.mp4 | tail`** — アルファベット順で先頭4本を見落とし「0本」と報告した
3. **`ls A | tail -1 || echo NONE`** — パイプがあると `||` は発火しない（終了コードは `tail` のもの）
4. **PowerShell の `-match` を配列に当てる** — `$Matches` が埋まらず、60件残っているのに「残0」と読んだ
5. **キャッシュ** — `yt_channel_index` のキャッシュが直前のアップロードを隠す。
   「流入ゼロ」の数字は**対策を打つ90分前**のキャッシュだった
6. **`kill -0` / 存在を数えるカバー率** — 生存確認は PID＋CPU増分で
7. **台帳を自前で数える** — `_ledger\*.jsonl` を glob して集計すると、素材が別台帳
   （`factory.jsonl` 等）にある分を丸ごと見落とす。「Pexels は未取得」と報告した直後、
   `shelf_rows` で数えたら 34,905 点あった。**数えるときは必ず `from shelf import shelf_rows`**
8. **行にそのフィールドが無いだけ** — `kind` で数えて「記録映像は0本」と報告した。
   gov レーンが `kind` を書いていなかっただけで、実際は ia 1,422／nara 814 本ある
   （2026-08-10 に全台帳へ遡って付与済み・両方の数え方が一致することを確認）
9. **代理指標で判定する** — 音声QCがピーク値だけで「音割れ」と判定し、法廷録音30本を
   `unusable` にした。実際は mp3 復号のオーバーシュートで `flat factor` は 0＝無傷。
   直接証拠が既に計測されていて、判定側が読んでいなかった
10. **音楽用のしきい値を話し声に当てる** — 128kbps 下限／44.1kHz 下限は音楽・効果音の基準。
   最高裁は自らの弁論を **48kbps モノラル 22kHz** で配布しており、この基準では全滅する。
   `SPEECH_SOURCES` に登録すること（新しい音声ソースを足すたびに再発する）

### YouTube

7. **過去日付の `publishAt` は即時公開**（norfolk が16:01に一瞬 public になった）。
   `upload_schedule_case_v001.py` の日付は手書き。dry-run の `OK schedule local=` を目視する
8. **`videos.update` 直後の GET は `publishAt=None` を返すことがある**（実測8秒）。1回で断定しない
9. **supersede 受領書はアップロード**前**に書かれる**。完了判定に使うと早発火する。
   `WATCH https://` 行など、上がった後にしか出ない印を使う
10. **一度 public になった動画に `publishAt` をすぐ付けられないことがある**。
    private 化 → 数秒待って再 PUT
11. **クォータ 日次10,000ユニット・リセット 16:00 JST。**アップロード1本 ≒ 1,650-2,050
12. **uploads playlist は9本取りこぼす。**列挙口は `yt_channel_index.py` の和集合だけ
13. **関連動画リンクは Studio UI にしかない。**Data API に機能が無い

### TikTok

14. **投稿後にカバーは変更できない**（編集ボタンが全部無効）。付け直すには削除して再アップロード
15. **カバーはアップロード完了後に設定。**57%時点で入れると上書きされる
16. **「cover set」のログは何も保証しない。**画像URLを前後で読み比べる
17. **権威あるデータは Studio の一覧。**公開グリッドは反映が遅れる
18. **著作権チェックが緑になるまで送信しない。**早いとチェックが止まる
19. **1日の投稿上限がある。**回避しない
20. **3本ごとに Chrome を taskkill してから起動。**同じプロファイルでは既存プロセスに合流するだけ
20b. **TikTok 版の Composition は別途登録が要る。** `Short-short<N>-tt` が Root.tsx に無いと
    `render_shorts_tiktok.sh` は12本とも「RENDER DID NOT PRODUCE A FRESH FILE」で失敗する。
    先に `py -3.11 scripts/register_tiktok_compositions.py --apply`
21. **TikTok は「中身」ではなく「振る舞い」で配信を止められる。** v1 は一晩で100本超アップ→
    137本一括削除→また大量アップで、152本すべて0再生になった（公開自体はされている）。
    大量投稿・一括削除・上限の回避を絶対にやらない。ランプは
    `docs/PD_TIKTOK_ACCOUNT_V2.v001.md` §3
22. **アカウントの状態は Web から読めない。** 自動操作のChromeでは `/search`・`/setting`・
    プロフィールが Akamai `Access Denied`（Studio 管理画面だけ通る）。制限の有無はスマホアプリでのみ確認可

### 制作・素材

20a. **i2v は元プレートに無い人物を生成する。既定プロンプトだと 27%。**（2026-08-27 実測）
    EP77 keybridge は組み込みの `SCENE_PROMPT`（"atmospheric living environment"）＋既定 neg で
    **112本中30本**に人が湧いた。無人の会議室にスーツの男、無人の法廷ベンチに2人、
    コンクリート橋桁だけの絵に男、設計図のホワイトボードに女性。
    EP80 concordia は下のプロンプトで **182本中0本**。母数が違うので断定はできないが、
    定義は `scripts/_chain_i2v_ep78_82.sh` の `BASE_PROMPT` / `neg_for()` にあり、
    `I2V_PROMPT` / `I2V_NEG` にそのまま渡せる。**新規の話数はこれを使うこと。**

    - prompt: `the scene stays exactly as it is, only ambient motion: haze and air drift slowly,
      water surface ripples, light flickers gently, a very slow subtle camera push-in,
      archival documentary footage, nothing new enters the frame`
    - neg: `new person, people appearing, man appearing, woman appearing, human face, crowd,
      walking figure, silhouette of a person, animal, bird, vehicle entering frame,
      new object appearing, text, lettering, watermark, logo, morphing, warping, deformed,
      extra limbs, cartoon, low quality, jitter, scene change, cut to another shot,`
      ＋その話数の `forbidden_subjects`

    **`check_motion_saturation` はこれを一切検出しない**（色しか測らない。ツール自身が
    「クリップが何を映しているかについては何も言わない」と出力する）。**検出は目視だけ。**
    手順は `scripts/qc_i2v_tail_vs_plate.py`＝終端フレームを元プレートの真下に貼って全数対照。

20b. **人物禁止ネガは、元から写っている人まで消す。**（2026-08-27 実測）
    EP77 の H146 で、元プレートにいた作業員の腕（黄色い上着＋黒手袋）が i2v 後に消えた。
    H135 / H137 / H145 では保持されたので常にではない。
    **プレートに人が写っている絵には人物禁止ネガを使わない。** 無人のプレートにだけ使う。
    正しい言い方は「すでに写っている人はそのまま、新しい人だけ入れない」。

20c. **アーカイブ実写の「顔」はファイル名では絶対に分からない。** EP65 marmet の
    `AR-10159563__woman_sitting_on_a_chair_while_reading_a_magazine.mp4` は、
    **無地の壁の前に一人で座り、顔がはっきり写り、カメラに笑いかける実在の人物**だった。
    年齢は映像から断定できない＝**未成年でないと証明できない**＝カテゴリ2で失格。
    **3つの検査が通していた**：①ファイル名キーワード判定（"woman" と書いてある）
    ②プールQC（コンタクトシートを見て**承認していた**）③全機械ゲート（実在の顔は動き・輝度・
    多様性・尺の全部を通る）。**完成した出荷バイト列のフレームを読んで初めて見つかった。**
    → 出荷前に `check_shipped_frames` のシートを**必ず全部読む**。判定基準は
    「アーカイブ実写に識別可能な実在の顔 → 年齢不明でも却下」。
20d. **顔の自動検出（Haar）は使えない。** 4話35本すべてを赤にした（雨の窓に387個の「顔」）。
    誤検知を減らすと今度は**本物のカテゴリ2素材を0件と報告する**。
    `scripts/check_pool_faces.py` は**失敗した試みとして残してあるだけ**で、緑を信用してはいけない。
    有効なのは目で読むことだけ。
21. **却下した素材が film.json に残る。** correa 46 / memphis 52 / marmet 45本。
    原因は再ビルド工程が `2>&1 | grep` でエラーを飲み、終了コードも見なかったこと。
    **機構化済み**: `build_case_film_generic.py` が却下クリップを含む film.json の書き出しを拒否
22. **factory 棚のラベルが壊れている**（`evidence_bag` がカートゥーン）。出荷前に必ずコンタクトシートで目視
23. **マスターをリビジョン番号で選ぶな。** willingham で7/30の古い v002 が当日の v001 に勝った。
    **機構化済み**: `check_shipped_frames.py` は納品記録 → mtime の順で選び、食い違いを大声で出す
24. **ファイル名の頭文字から意味を推測するツール**が3回できた（`check_episode_inputs` /
    `build_asset_manifest_motionfirst` / `check_final_acceptance` の OPENING）
25. **176語/分は楽観的。**実測 159.5-169.7。尺は実測VOで設計する。
    **ナレ生成ログの `measured wpm` を信用しないこと。**それは合成した発話だけの速度で、
    チャンクの間に入る無音を数えていない。EP66 openfields はログが `171.8` と出したが、
    納品されたマスターは 4,278語 / 1604.211 s = **160.0 wpm**（7%の乖離・無音は約110秒）。
    ※数値は2026-08-10のフック延長後に再実測（延長前は 4,262語 / 1598.038 s、同じく160.0 wpm）。
    171.8 で語数を引くと尺が1分50秒足りない台本になる。**必ず母数を自分で割る**:
    `ffprobe -v error -show_entries format=duration -of csv=p=0 <master.mp3>` と
    `06_audio/narration_index.v001.json` の語数で、自分で除算してから使う。
26. **英語台本に日本語を混ぜない**（ナレ欠落バグ）
26b. **EP62-66 の `03_script/script.en.v001.md` は古い。** ファイル自身が「編集するな・
    企画台本から再生成しろ」と言っているのに、誰も再生成しなかった。greene は台本5問に対し
    実際に喋ったのは9問（memphis 0対7・marmet 1対7）。**読むと別の映画の台本が出てくる。**
    正は `06_audio/narration_index.v001.json`。EP67以降は一致している。
27. **実行中のシェルスクリプトを絶対に編集しない。** bash はスクリプトを
    **バイトオフセットで逐次読む**ので、走っている最中に本体を書き換えるとオフセットがずれ、
    残りがゴミとして解析される。2026-08-10、`_finish_episode.sh` を別作業が編集した結果、
    correa は **[6/7] のレンダーを完走した直後に
    `line 124: unexpected EOF while looking for matching` で落ち、[7/7] のBGM＋ナレ合成が
    走らなかった**。ファイル自体は健全（`bash -n` は通る）。
    危険なのはここ: **08_edit のマスターは古いままなので、受入検査はそれを測って
    「別の映画の受領書」を出す。**（ゲートは緑になりうる）
    **機構**: 長時間ジョブは起動時にスクリプトを複製して複製側を実行する
    （`scripts/queue_finish_62_65.v002.sh` の `SNAP` を参照）。
    **検査**: レンダー後は必ず `08_edit/<slug>_final_bgm.v001.mp4` の mtime が
    `out/<slug>.mp4` より新しいことを確認してから受入検査に入る。

### チャンネル標準の既知偏差（出荷済み全話が抱えている）

`sound_layers` / `preflight_receipt` / `asset_reuse` / `padding` / `caption_format` は
norfolk〜weimer（8/10-8/15 予約済み）が**全部 FAIL のまま出荷している**。
新しい話でこれらが赤でも「新規の欠陥」ではない。**本当に新規かは受領書を横並びで比べて判断する**：

```bash
# 直近の受領書を横並びにして、その項目が自分だけ赤なのかを見る
py .venv/Scripts/python.exe scripts/... # → docs 参照。無ければ receipts を読んで比較する
```

---

## 8. 作業のやり方

### 着手前

1. **正典パイプラインから始める。**独自 ffmpeg 組み立て禁止。
   `PD_ONE_PASS_PRODUCTION_SPEC.v3.md`（**EP72以降**。EP62-71 は v2）→ ship-gate →
   `check_final_acceptance` を読んでから触る
2. **全 fail を先に把握してから1バッチで直す。**1つ直して回すと連動ゲートの副作用で沼る
   （EP35 で v003→v04 の1回を無駄にした）
3. **オーナー基準で自分で1周見てから出す** — 字幕サイズ／OP-ED／8秒フック／非静止／
   素材被り／切りの良い終わり

### 作業中に自分へ問う4つ

1. **このログは「やったこと」か「変わったこと」か。**副作用を主張するなら読み返す
2. **この検出器を、失敗するはずの入力で試したか。**
   ユーザー名判定はありえない文字列でも「使用中」を返した
3. **証拠が食い違うとき、権威あるのはどちらか。決めてから理論を作ったか。**
   片方だけ見て2時間無駄にした
4. **破壊的操作の対象を、定義的な属性で選んだか。件数を突き合わせたか**

### 編集と実行

- **編集は必ず `scripts/pd_edit.py` を通す**（適用→存在確認→構文チェック→失敗なら巻き戻し）
- **長時間ジョブは `scripts/pd_run.sh` から**（安いスモーク→ロック→60秒後にログを読む）
- **失敗したらツールに検査を足す。**`docs/` に段落を足さない（既に73,000語あり実行時に読まれない）
- **一度も落ちたことのない検査は飾り。**追加したら、わざと悪い入力で落ちることを実演してから頼る

### 報告

- **数字には必ず出所を添える。オーナーに聞かせない。**
  「150本」ではなく「150本（`yt_channel_index.py`）」と書く。出所を書けないなら
  **「まだ測っていません」と書く**。2026-08-10、一日で5回、確かめずに断言して外した——
  「動画0本」（実は4本）「孤児50個」（実は34個）「0秒から喋っている」（実は11.5秒無音）
  「CTRは取得不可」（取得できた）「設計書はマニュアル通り」（1項目欠落）。
  5回とも、その場で打ったコマンドの出力を読まずに報告したもの。
  オーナーに「それはどのコマンドで測った？」と聞かせるのは負担の転嫁であって、機構ではない。
- **自己申告のQCは禁止。**実ファイルを独立に測って合否を出す
- 完了報告は実数で短く。「たぶん」「はず」を使わない
- 他エージェントの「検証しました」は、**誰が取得したか**まで問う（URLごと捏造した実例あり）

---

## 9. どこに何があるか

| 目的 | ファイル |
|---|---|
| 毎日の現在地と次の一手 | `py -3.11 scripts/daily_status.py`（**新しいスレはまず此処**） |
| 憲法・不変条件 | `CLAUDE.md` |
| 拘束ルール | `.claude/rules/`（特に `19-ship-gate.md`） |
| **「設計書を作って」と言われたら** | **下の2つのどちらかを必ず開く。自己流で書かない** |
| ├ 動画オープニングの設計書 | `C:/Users/aab15/CLAUDE.md`（37行）。**Codex が単体で読んで実装する前提**なので、品質ルール・イージング・レイヤー数・秒数を**本文に数値で書ききる**。抽象語で済ませない。正典実装は `Documents/pino-channel/remotion/src/Opening.tsx` |
| └ PDエピソードの設計書 | `docs/PD_EPISODE_SPEC_STANDARD.v001.md`（契約JSONの書き方）＋ `docs/PD_ONE_PASS_PRODUCTION_SPEC.v3.md`（一発完璧の仕様・EP72以降）＋ `docs/PD_EPISODE_DESIGN_MANUAL.v001.md`（決める順番。**EP77以降はAEの宣言が必須**） |
| 1発完璧の仕様 | `docs/PD_ONE_PASS_PRODUCTION_SPEC.v3.md`（**EP72以降を拘束**）。EP62-71 は `v2`、EP17-18 は `v1`。**古い版は記録として残す**（受領書が読めなくなるため消さない） |
| 出荷ゲート詳細 | `docs/PD_SHIP_GATE.md` |
| 契約の書き方 | `docs/PD_EPISODE_SPEC_STANDARD.v001.md` |
| 勝ち筋・数値目標 | `docs/PD_WINNING_PATTERN.md` |
| 視聴データの実測 | `episodes/_planning/DEEP_RESEARCH_FINDINGS.v001.md`（**docs/ には無い**。2026-08-23 に実パスへ訂正） |
| 失敗全集 | `docs/PD_RETRO_20260805_UNPAUSE.v001.md` / `docs/PD_RETRO_20260810_TIKTOK_AND_CALENDAR.v001.md` |
| TikTok・カレンダー | `episodes/_planning/HANDOFF_20260810_TIKTOK_AND_CALENDAR.v001.md` |
| 再利用部品40種 | `remotion/src/motionkit/CATALOG.md`（新演出はまず此処。二重実装禁止） |
| 素材棚 | `docs/PD_ARCHIVE_SHELF_WORKLOG.v001.md`（**使い方・判定・罠の全部。下の §10 が要約**） |
| 素材棚（旧・factory） | `episodes/_planning/FACTORY_INVENTORY.md`（**docs/ には無い**。2026-08-23 に実パスへ訂正。ラベルは壊れている。目視必須） |

---

## 10. 素材棚（2026-08-10 全面点検済み）

詳細と根拠は `docs/PD_ARCHIVE_SHELF_WORKLOG.v001.md`。ここは他スレが踏まないための最小限。

### 探すとき

```bash
py -3.11 scripts/search_archive.py --shot "courthouse building exterior" --kind video --md --sheet
```

1. **ショットは「監督の言葉」でなく「素材提供者が付ける題名の語彙」で書く。**
   `police interview room`→0件 / `interrogation room detective`→12件。
   `handcuffs on wrists`→0件 / `person in handcuffs`→16件。
   カバレッジが 85/50/90% から **100/90/100%** に上がったのは、棚が増えたからではなく書き方を直したから
2. **0件が返ったら `--weak-ok --sheet` を付けて必ず目で見る。**
   弱一致は大半が語の衝突（`branch`＝木の枝／`card`＝基板）だが、本命が埋まっていた率が 12/13
3. **`[640x480] SD` の表示を読む。** 動画31,107本すべて解像度既知。SDを選ぶのは判断であって事故ではない

### 数えるとき

**`from shelf import shelf_rows` を使う。自前で `glob("*.jsonl")` しない。**
3つのツールが各自の定義を持ち、3つとも違う壊れ方をしていた
（`purged.jsonl` 64,640行を在庫に加算して 197,712点と報告／`ukna_candidates` の
22,348行を「未レビュー在庫」と誤報。全部 `file_path: null` で1本もDLしていない）。

### 触らないもの

- **台帳の行を消さない。** 47%は削除の記録。消すと取り込みが同じものを取り直す
  （住所録46,707枚が実際に戻ってきた）。削除は `absent_index.json` が別管理する
- **取り込みの技術基準を上げない。** 記録系の480p未満は削除でなく隔離する設計。
  代替不能な記録映像に削除経路を作ると、過去にニュルンベルクのリールを7本破壊した

### 組み立て側が知るべきこと

- **出荷ゲートは素材の解像度を見ていない。** `check_final_acceptance` は完成尺だけを
  `>=1920x1080` で測る。**640x480を1080pに引き伸ばした作品は通る。**
  索引 `_ledger/video_resolution.json` を `(source:id)` で引ける
- 危ないのは100%SDのテーマではなく、**2割だけ混ざるテーマ**
  （`courtroom_justice` 17% / `prison_jail` 19%。nara 89% ia 73%、ストック系はほぼ0%）
- **判定 `unusable` の theme×source を使わない。** `search_archive` 経由なら自動で外れる。
  台帳を直接舐めるコードは危ない

---

## 11. この文書の育て方

- **新しい罠を踏んだら §7 に1行足す。**別の場所に新しい申し送りを作らない
- **文書どうしが食い違ったら、直したうえで `scripts/check_doc_contradictions.py` に規則を1行足す。**
  2026-08-23、拘束文書98本で10件の食い違いが見つかった（出荷条件・仕様の版・タイトル長・
  フックの順番・尺・アニメ・退役ツール・リンク切れ）。どれも不注意ではなく、
  **新しい決定が新しい場所に書かれ、古い場所が古い文のまま残った**もの。
  意志では防げないので機械に持たせた。`--demo` が「わざと悪い入力で落ちること」を毎回実演する
- **状態が変わったら §1 を更新する。**数字だけでなく**測り直すコマンド**も一緒に
- **機構で塞いだら「機構化済み」と書き、どのファイルかを書く。**
  意志で防ぐと書いてあるものは、いずれ必ず破られる
- 詳細は各文書に置き、ここには**現在地・禁止・入口**だけを置く。
  この文書が長くなりすぎたら、読まれなくなって元の木阿弥になる
