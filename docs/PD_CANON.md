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
| TikTok | 3本（カバー付き）／119本 上げ直し残 | Studio の一覧（公開グリッドは遅れる） |
| TikTok 用レンダー | 122本＋EP62-65の12本（8/10レンダー中） | `ls remotion/out/short*_tt.mp4` |
| 長尺エピソード | 65（EP62-65 は仕上げ中） | `ls -d episodes/PD-2026-0*` |

### 長尺の在庫が尽きている

12:00 JST の長尺枠は **8/15 まで埋まり、8/16 以降が空き**。
`yt_schedule_audit.py` のサマリ行は**全時間帯の最終予約**を基準に「次の空きは 8/19」と保守的に出す。
**12:00 の実データを見ること**（8/16-8/18 に出るのは 06/09/18/21 のショート）。

### ショートは3本か4本か（未決）

EP53-56 は 1話4本、EP57-59 と EP62-65 の設計書は 1話3本。
`SHORTS_VERTICAL_PLATE_SPEC.v001.md` は両論併記のまま決めていない。
**195本計画は「1話3本」前提。**決めたらここに書く。

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

### 契約（`episodes/<EPID>/episode_spec.v001.json`）

**ツールが数字を読む唯一の場所。**設計書の散文は残すが、機械はこれしか読まない。
未宣言はエラー。既定値で補完してはならない。

### 予約の条件（rule 19・機械が強制）

`upload_schedule_case_v001.py` は次を全部満たさないと上げない。

1. `acceptance_receipt.v*.json` の `video_sha256` が**そのファイルの実 sha と一致**
2. ハード不合格が `runtime_band`、**または**そのエピソードの
   `approvals/*.json`（`target_type:"edit"` かつ `decision:"approved*"`）の
   `accepted_deviations[]` に載っているものだけ
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

### 制作・素材

21. **却下した素材が film.json に残る。** correa 46 / memphis 52 / marmet 45本。
    原因は再ビルド工程が `2>&1 | grep` でエラーを飲み、終了コードも見なかったこと。
    **機構化済み**: `build_case_film_generic.py` が却下クリップを含む film.json の書き出しを拒否
22. **factory 棚のラベルが壊れている**（`evidence_bag` がカートゥーン）。出荷前に必ずコンタクトシートで目視
23. **マスターをリビジョン番号で選ぶな。** willingham で7/30の古い v002 が当日の v001 に勝った。
    **機構化済み**: `check_shipped_frames.py` は納品記録 → mtime の順で選び、食い違いを大声で出す
24. **ファイル名の頭文字から意味を推測するツール**が3回できた（`check_episode_inputs` /
    `build_asset_manifest_motionfirst` / `check_final_acceptance` の OPENING）
25. **176語/分は楽観的。**実測 159.5-169.7。尺は実測VOで設計する
26. **英語台本に日本語を混ぜない**（ナレ欠落バグ）

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
   `PD_ONE_PASS_PRODUCTION_SPEC.v2.md` → ship-gate → `check_final_acceptance` を読んでから触る
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

- **自己申告のQCは禁止。**実ファイルを独立に測って合否を出す
- 完了報告は実数で短く。「たぶん」「はず」を使わない
- 他エージェントの「検証しました」は、**誰が取得したか**まで問う（URLごと捏造した実例あり）

---

## 9. どこに何があるか

| 目的 | ファイル |
|---|---|
| 憲法・不変条件 | `CLAUDE.md` |
| 拘束ルール | `.claude/rules/`（特に `19-ship-gate.md`） |
| 1発完璧の仕様 | `docs/PD_ONE_PASS_PRODUCTION_SPEC.v2.md`（EP19以降を拘束） |
| 出荷ゲート詳細 | `docs/PD_SHIP_GATE.md` |
| 契約の書き方 | `docs/PD_EPISODE_SPEC_STANDARD.v001.md` |
| 勝ち筋・数値目標 | `docs/PD_WINNING_PATTERN.md` |
| 視聴データの実測 | `docs/DEEP_RESEARCH_FINDINGS.v001.md` |
| 失敗全集 | `docs/PD_RETRO_20260805_UNPAUSE.v001.md` / `docs/PD_RETRO_20260810_TIKTOK_AND_CALENDAR.v001.md` |
| TikTok・カレンダー | `episodes/_planning/HANDOFF_20260810_TIKTOK_AND_CALENDAR.v001.md` |
| 再利用部品40種 | `remotion/src/motionkit/CATALOG.md`（新演出はまず此処。二重実装禁止） |
| 素材棚 | `docs/FACTORY_INVENTORY.md`（**ラベルは壊れている。目視必須**） |

---

## 10. この文書の育て方

- **新しい罠を踏んだら §7 に1行足す。**別の場所に新しい申し送りを作らない
- **状態が変わったら §1 を更新する。**数字だけでなく**測り直すコマンド**も一緒に
- **機構で塞いだら「機構化済み」と書き、どのファイルかを書く。**
  意志で防ぐと書いてあるものは、いずれ必ず破られる
- 詳細は各文書に置き、ここには**現在地・禁止・入口**だけを置く。
  この文書が長くなりすぎたら、読まれなくなって元の木阿弥になる
