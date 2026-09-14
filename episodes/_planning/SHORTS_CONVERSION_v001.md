# SHORTS_CONVERSION v001 — 公開済みショート22本を「登録につながる導線」に変える実行パッケージ

**作成:** 2026-07-19
**根拠データ:** `scripts/_yt_analytics.json`（YouTube Analytics 2026-05-01 .. 2026-07-18 / 47本）
**上位方針:** `episodes/_planning/PACKAGING_FIX_v001.md` §4 の結論を実装可能な形に落としたもの
**性質:** **下書きのみ。YouTube への書き込みは一切行っていない**（コメント投稿・ピン留め・メタ更新・再アップロード・公開設定変更、すべて未実施）。実行はオーナー承認後。

---

## 実行手順（この順に、この担当で）

> 前提: **既存22本の動画ファイルは絶対に触らない。** 再アップロードすると views / 維持率 / 公開日がリセットされ、
> 本書の測定基盤そのものが消える。既存22本に対して行う変更は **固定コメント1件の追加だけ**。

### STEP 0 ─ 事前検証（担当: Claude / 所要 10分）※ 投稿前に必ず実施
1. **video_id と公開状態の再確認。** `videos.list(part=status,snippet)` で §2 の44本（ショート22＋長尺22）の
   `privacyStatus` を取得する。
   **理由:** 本書の公開状態の根拠 `scripts/_yt_deep.json` は **2026-06-28 取得＝3週間前**で、しかも当時 `publishAt` 待ちの
   スケジュール投稿は一律 `private` と記録されている（例: `2XWqZWx916c` は private 記録なのに149 viewsある＝記録が古い）。
   **`private` の長尺にリンクした固定コメントは、視聴者から見ると死んだリンクになる。**
2. `privacyStatus != "public"` の長尺が1本でもあれば、**そのショートは STEP 2 の対象から外す**（保留リストへ）。
   現時点で最も疑わしいのは EP015 Theranos 長尺 `LXFjJqE6vKU`（§2 表の注記参照）。
3. `scripts/_yt_analytics.json` の再取得は不要（本書は 2026-07-19 13:30 取得のものに固定）。

### STEP 1 ─ 投稿スクリプトの作成とドライラン（担当: Claude / 所要 30分）
- 新規作成: **`scripts/post_short_pinned_comments.py`**
- 既存の認証系をそのまま流用する（新しい認証は不要）:
  - `src/pd_factory/providers/youtube.py` の `_access_token(env)`
  - `scripts/youtube_auth.py` の SCOPES に **`https://www.googleapis.com/auth/youtube.force-ssl` が既に含まれている**
    ＝ `commentThreads.insert` に必要な権限は取得済み。**再認証不要。**
- 使用API: `POST https://www.googleapis.com/youtube/v3/commentThreads?part=snippet`
  body: `{"snippet":{"videoId":"<short_id>","topLevelComment":{"snippet":{"textOriginal":"<§3の文面>"}}}}`
- 文面は **スクリプトに直書きせず `episodes/_planning/shorts_pinned_comments.v001.json` を読む**
  （`[{"short_id":..., "episode":..., "long_id":..., "text":...}]`）。本書 §3 がそのまま元データ。
- 必須フラグ: `--dry-run`（既定ON）/ `--only <short_id>` / `--limit N`。
  ドライランは **1文字もPOSTせず**、解決した video_id・URL・文字数・重複文チェック結果を表に出すだけ。
- ドライランの合格条件: 22本すべてで(a) URL が `https://youtu.be/<11文字>` (b) 文面が全22本ユニーク
  (c) 文中に "subscribe" / "登録" の語が無い (d) 280文字以内。

### STEP 2 ─ パイロット3本を投稿（担当: オーナー承認 → Claude が実行）
- **最初は3本だけ。** 対象は再生数上位かつ長尺の存在が確実な3本:
  1. `L8iKnBSVXKg`（EP007 Riley / 199 views）
  2. `dedDocuyCUM`（EP006 Terry / 188 views）
  3. `2XWqZWx916c`（EP014 Lange / 149 views）
- 実行: `python scripts/post_short_pinned_comments.py --only L8iKnBSVXKg,dedDocuyCUM,2XWqZWx916c --no-dry-run`
- 投稿結果（comment id）を `episodes/_planning/shorts_pinned_comments_result.v001.json` に保存。

### STEP 3 ─ ピン留め（担当: **オーナー手作業**。API では不可能）
> **重要な技術的制約:** YouTube Data API v3 に **コメントをピン留めするエンドポイントは存在しない。**
> `commentThreads.insert` で投稿はできるが、ピン留めは **YouTube Studio または YouTube モバイルアプリ**からの手動操作のみ。
> したがって本施策は「API で投稿 → 人間がピン留め」の2段構えになる。ここを自動化しようとしないこと。

手順（1本あたり約20秒）:
1. 該当ショートを YouTube アプリまたは Studio で開く
2. コメント欄で自分（チャンネル）の投稿を長押し / ⋮
3. 「固定」→ 確定

**補足: 本チャンネルはコメント総数0**（`_yt_analytics.json` 全47本で `comments=0`）。
つまり **ピン留めしなくても自分のコメントが唯一のコメントとして最上部に出る。**
ピン留めは「新規コメントが付いたときに沈まない保険」であり、STEP 3 が遅れても STEP 2 の効果は出る。

### STEP 4 ─ 72時間の観察（担当: Claude）
- パイロット3本の対応長尺（`XWYWAgkExH4` / `bYcqabvvxak` / `Sz8zPUoBANM`）の views 増分を確認。
- **判定基準:** 3本合計で長尺側 views が +10 以上なら継続。0 のままなら §5 の仮説が外れているので、
  文面ではなく「導線そのものが機能しない」と結論し、残り19本の投稿は行わずに再設計する。

### STEP 5 ─ 残り19本を投稿（担当: Claude / STEP 4 合格後）
- `python scripts/post_short_pinned_comments.py --no-dry-run`（--only なしで残り全部）
- 投稿後、オーナーが19本を順次ピン留め（STEP 3 と同じ操作 / 合計約7分）。

### STEP 6 ─ 14日後の効果測定（担当: Claude / 2026-08-02 目安）
- 測定するのは **登録者数ではなく、まず長尺側のトラフィックソース内訳**。
  Studio > 各長尺 > リーチ > トラフィックソース に **「Shorts フィード」または「関連動画」** が立つかどうか。
- ここが0のままなら、原因はショートではなく長尺の入口（サムネ／タイトル）側。
  → `PACKAGING_FIX_v001.md` §5 のタイトル・サムネ改修に予算を移す。

### STEP 7 ─ 新規ショートへの末尾CTA実装（担当: Codex / STEP 2 と並行可）
- §4 の仕様に沿って `remotion/src/compositions/Short.tsx` の `CtaLayer` を差し替える。
- **既存22本には適用しない**（再レンダー＝再アップロード＝数字リセットのため）。次に作るショートから適用。

---

## 1. なぜこれをやるのか（実測3行）

| 事実 | 数値 | 出典 |
|---|---|---|
| ショートは全再生の大半を稼いでいる | ショート22本 = **1,340 views** / 全47本 = 2,093 views ＝ **64.0%** | `_yt_analytics.json` per_video |
| なのに登録は増えていない | ショート由来の `subscribersGained` = **0**（22本すべて0）。チャンネル全体の +2 のうち1件は長尺 Madoff `sphERPA4gAc` 由来 | 同上 |
| 離脱が原因ではない | 上位5本の維持率 = 69.6% / 50.8% / 46.2% / **92.1%** / (計測異常) ＝ **最後まで見られている** | 同上 |

**したがって原因は「離脱」ではなく「最後まで見た人に何も要求していない」。**
変えるべきは1点だけ ＝ **視聴後の行き先を作る**（`PACKAGING_FIX_v001.md` §4 の結論）。

### ⚠️ 指示前提との差分（正直に記載）
- 指示では「ショートは全再生の66%（1,392回）」「総視聴時間214分」とあったが、
  **本書が突き合わせた `_yt_analytics.json`（2026-07-19 13:30取得）での実測値は 1,340 views（64.0%）/ 197分。**
  `PACKAGING_FIX_v001.md` §0 も 1,340 と記載しており、そちらと一致する。
  **本書は 1,340 / 197分 を採用する。** 差分は集計期間かショート判定の1〜2本のずれと推定されるが、
  どちらの数字でも結論（ショートが再生の6割超・登録0）は変わらない。
- レーン別の内訳（権利12本=1,068 views・平均70.7% / 犯罪10本=272 views・平均41.1%）は
  **指示の数値と完全一致した**。§5 の判断はこれに基づく。

---

## 2. 公開済みショート22本 一覧（video_id / タイトル / 再生数 / 維持率 / 対応長尺）

**突き合わせ方法:** `scripts/_yt_analytics.json` の `per_video`（47行）から、
各話 `09_package/shortNN_youtube_schedule_result.v001.json`（＋ short06/07/08 は
`shortNN_youtube_publish_result.*.json`）の `video_id` に一致する22行を抽出。
長尺は各話 `09_package/youtube_schedule_result.*.json` / `youtube_meta.*.json` / `manifest.json` の
**最新リビジョンの `video_id`** を採用（EP007/EP014 は再アップロード履歴があるため最新版のみ有効）。

### 2-1. 権利・警察レーン（n=12 / 1,068 views / 平均維持率 70.7%）

| # | ショート video_id | ショートタイトル | 再生 | 維持率 | 対応長尺 video_id | 長尺タイトル |
|---|---|---|---|---|---|---|
| S07 | `L8iKnBSVXKg` | Police Need a Warrant to Search Your Phone #Shorts | **199** | 69.6% | `XWYWAgkExH4` | The Supreme Court Case That Put a Warrant on Your Phone |
| S06 | `dedDocuyCUM` | Police Can Stop & Frisk You Without an Arrest #Shorts | **188** | 50.8% | `bYcqabvvxak` | A Cop Can Search You Without a Warrant - Here's the Catch |
| S14 | `2XWqZWx916c` | Can Police Chase You Into Your Own Home? #Shorts | **149** | 46.2% | `Sz8zPUoBANM` | Can a Police Officer Follow You Into Your Own Home? |
| S13 | `Lux3a25vBSw` | Arrested? Police Can Take Your DNA — and Keep It #Shorts | **145** | **92.1%** | `g5yFmDt48oU` | The Supreme Court Said Police Can Swab Your DNA at Arrest |
| S08 | `m33s6uFmXao` | Police Tracked His Phone for 127 Days — No Warrant? #Shorts | **125** | ⚠️275.6% | `zE3nCUlUmLY` | Your Phone Is Tracking You — and the Police Wanted the Map |
| S12 | `bFGZ_6BTI9I` | Did You Sign Away Your Right to Sue? #Shorts | 65 | 39.8% | `1pox44KsaV8` | The Fine Print That Quietly Took Your Right to Sue |
| S10 | `6rUWUk3x9Xs` | Can the Government Take Your Home for a Private Company? #Shorts | 60 | 35.6% | `89SQoRgAD7U` | Your Home for a Developer? The Kelo Supreme Court Case |
| S01 | `ypDjfK9o5Bg` | Why Do Police Read You Your Rights? #Shorts | 54 | 65.3% | `cQFql7tT1fE` | Read Rights or It's Out \| Miranda v. Arizona |
| S03 | `PF4ZJjy_KCs` | Police Searched Illegally — Can They Still Use It? #Shorts | 38 | 37.9% | `An0to4U0hJQ` | The Police Broke In — So the Court Let Her Go |
| S02 | `uL9q1GM_1Vw` | Can't Afford a Lawyer? A Pencil Letter Changed Everything #Shorts | 29 | 52.1% | `ch2hQ5jhDmQ` | He Had No Lawyer — So He Beat the Supreme Court |
| S09 | `mrPV1Tv_6gE` | Can Police Take Your Property Without a Conviction? #Shorts | 13 | 82.9% | `m-uWzgWHGPg` | Police Took His $42,000 Car. The Supreme Court Drew a Line. |
| S11 | `sxk0gbFBnMU` | Can Your School Punish You for a Post Made at Home? #Shorts | 3 | ⚠️0.0% | `cSfe3iGnBBM` | Can Your School Punish You for a Post You Made Off Campus? |

### 2-2. 犯罪・詐欺レーン（n=10 / 272 views / 平均維持率 41.1%）

| # | ショート video_id | ショートタイトル | 再生 | 維持率 | 対応長尺 video_id | 長尺タイトル |
|---|---|---|---|---|---|---|
| S15 | `2Smc35dUF5c` | When Does a Bold Promise Become a Crime? #Shorts | 87 | ⚠️0.0% | `LXFjJqE6vKU` ⚠️ | When Does a Bold Promise Become a Crime? The Rise and Fall of Theranos |
| S16 | `_TcVNCh2PlA` | The World Counted Down 4 Days. They Were Already Gone. #Shorts | 77 | 37.4% | `marQjsCagh0` | They Were Warned — The Last Dive of the Titan |
| S04 | `AMZXUw3Arn0` | $8 Billion Vanished From a Crypto Exchange — Where Did It Go? #Shorts | 56 | 62.2% | `waA4XJ9bYcE` | The Hidden Code Door Behind the $8 Billion FTX Fraud |
| S18 | `NLvlce3XCaw` | $1 Trillion Vanished in 36 Minutes — Then Came Back #Shorts | 16 | 39.4% | `5Jap-0h43A4` | The Day $1 Trillion Vanished in 36 Minutes |
| S20 | `vLs3VaidXkI` | The Biggest Art Heist in History Is Still Unsolved #Shorts | 11 | 43.7% | `1h267U6PY0I` | $500M Gone: The Gardner Heist |
| S05 | `O0mK6cK1iTs` | Steady Returns for Decades — and Almost Zero Real Trades #Shorts | 11 | 11.9% | `sphERPA4gAc` | Madoff's Perfect Chart: The $65B Lie Wall Street Believed |
| S17 | `TxGQKxxzjfs` | She Sold a Crypto That Prosecutors Say Never Existed #Shorts | 6 | 80.3% | `vikfOBHullI` | There Was No Coin: $4 Billion in Empty Promises |
| S19 | `jD5nQ2ARL-M` | How Did Wealthy Parents Sneak Their Kids Into Elite Colleges? #Shorts | 3 | ⚠️103.5% | `j8U8c4BB_GQ` | The Side Door: Operation Varsity Blues |
| S21 | `rV-56tT8cMg` | He Jumped From a Plane With $200,000 and Vanished #Shorts | 3 | 9.7% | `tt7U1XgjCU4` | (EP021 D.B. Cooper 長尺) |
| S22 | `PpiUNN5QWQQ` | Charged With 98 Counts, He Pleaded Guilty to Just 6 #Shorts | 2 | 23.4% | `mj9qEKPRatE` | (EP022 Milken 長尺) |

### 2-3. 対応する長尺の有無

- **対応長尺が存在するショート: 22本（22本中 22本 = 100%）。**
  22本すべてが「長尺エピソードのショート版」として作られており、孤児ショートは1本も無い。
- **対応長尺が存在しないショート: 0本。**
- **ただし「存在する ≠ そのURLを今すぐ貼ってよい」。以下2件は STEP 0 で公開状態を検証してから。**

| 要検証 | ショート | 長尺 | 懸念 |
|---|---|---|---|
| ⚠️ 高 | S15 `2Smc35dUF5c`（87 views） | `LXFjJqE6vKU` | `_yt_deep.json`(2026-06-28) で `private`。**かつ 2026-05-01〜07-18 の analytics 47行に長尺として現れない＝この期間の再生0**。非公開のままの可能性が最も高い。**公開が確認できるまで投稿対象外**にすること |
| ⚠️ 中 | S13 `Lux3a25vBSw`（145 views・維持率92.1%） | `g5yFmDt48oU` | `_yt_deep.json` では `public`。ただし analytics 47行に無い＝この期間の再生0。URL自体は生きている見込みだが STEP 0 で確認 |

### 2-4. データ品質の注記（⚠️印の行について）

`averageViewPercentage` に信用できない値が4件ある。**平均を語るときは必ず併記すること。**

| video_id | 記録値 | 解釈 |
|---|---|---|
| `m33s6uFmXao` | 275.57% | ループ再生が加算された値。「1人が平均2.8周見た」＝実質は極めて強い、が数値としては使えない |
| `jD5nQ2ARL-M` | 103.47% | 同上（3 views と母数が小さい） |
| `2Smc35dUF5c` | 0.0% | `estimatedMinutesWatched=1` / `averageViewDuration=0` ＝計測失敗。87 views に対して視聴時間が付いていない |
| `sxk0gbFBnMU` | 0.0% | 同上（3 views） |

**この4件を除いた「クリーン平均」:**
- 権利レーン（n=10）: **57.2%**
- 犯罪レーン（n=8）: **38.5%**
- 倍率は 4.0倍 → **1.49倍**に縮む。ただし **views の差（89.0/本 vs 27.2/本 = 3.27倍）は異常値の影響を受けない。** §5 の判断はこの views 差を主根拠にする。

---

## 3. 固定コメント文面（22本 / 英語 / 全文異なる）

**設計ルール（全22本共通）**
- 1〜2文。英語。
- **そのショートが出した問いの「答えの続き」が長尺にある**という繋ぎ方。
- **"subscribe" / "登録して" は書かない。** "check out" / "don't miss" のような販促動詞も使わない。
- 末尾に `https://youtu.be/<long_id>` を1本だけ置く。URLは1コメントに1つまで。
- **テンプレの使い回し禁止。** 導入句・接続の仕方・締めのラベル（"The full case:" / "Told in full here:" / "How that worked:" …）は22本すべて別。

> 実行時はこの表を `episodes/_planning/shorts_pinned_comments.v001.json` に写し、
> スクリプトはそのJSONだけを読む（本Markdownをパースさせない）。

### 3-1. 権利・警察レーン

**S07 — `L8iKnBSVXKg` → `XWYWAgkExH4`**
> That warrant requirement is only about a decade old, and the argument that produced it is worth the full version. Here it is: https://youtu.be/XWYWAgkExH4

**S06 — `dedDocuyCUM` → `bYcqabvvxak`**
> The catch is what counts as "reasonable suspicion" — a standard set in 1968 by a detective watching three men pace a storefront. The full case: https://youtu.be/bYcqabvvxak

**S14 — `2XWqZWx916c` → `Sz8zPUoBANM`**
> Not automatically, no — and the honking-horn misdemeanor that settled it is stranger than the rule it produced. We walk through it here: https://youtu.be/Sz8zPUoBANM

**S13 — `Lux3a25vBSw` → `g5yFmDt48oU`**
> The swab is legal at arrest; the 5-4 split over *why* is where this gets genuinely uncomfortable. Both sides laid out: https://youtu.be/g5yFmDt48oU

**S08 — `m33s6uFmXao` → `zE3nCUlUmLY`**
> Those 127 days came from the phone company, not the phone — and that distinction is what the whole case turned on. Unpacked here: https://youtu.be/zE3nCUlUmLY

**S12 — `bFGZ_6BTI9I` → `1pox44KsaV8`**
> Almost certainly you did. The clause is usually a few lines long, and knowing where it sits changes what you can still do. Explained in full: https://youtu.be/1pox44KsaV8

**S10 — `6rUWUk3x9Xs` → `89SQoRgAD7U`**
> It happened in New London, Connecticut, and what stood on that land afterward is the part most people never hear. Full story: https://youtu.be/89SQoRgAD7U

**S01 — `ypDjfK9o5Bg` → `cQFql7tT1fE`**
> The warning exists because of one 1966 case, and what happens when police skip it is the part that didn't fit in a minute. Full case: https://youtu.be/cQFql7tT1fE

**S03 — `PF4ZJjy_KCs` → `An0to4U0hJQ`**
> Whether that evidence can still be used has a specific answer, and it came out of a raid on one woman's house in Cleveland. Told in full here: https://youtu.be/An0to4U0hJQ

**S02 — `uL9q1GM_1Vw` → `ch2hQ5jhDmQ`**
> The pencil letter is where this begins, not where it ends — the Court's answer arrived a year later and changed every state courtroom. The whole story: https://youtu.be/ch2hQ5jhDmQ

**S09 — `mrPV1Tv_6gE` → `m-uWzgWHGPg`**
> They can. The limit the Supreme Court finally drew involves a $42,000 car and a maximum fine of $10,000. Full case here: https://youtu.be/m-uWzgWHGPg

**S11 — `sxk0gbFBnMU` → `cSfe3iGnBBM`**
> A cheerleader's weekend post got her suspended, and the answer drew a line right at the school gate. How it went: https://youtu.be/cSfe3iGnBBM

### 3-2. 犯罪・詐欺レーン

> このレーンは §5 の方針により **新規制作を止める**。ただし既に公開済みの10本は 272 views を持っているので、
> 固定コメントは **10本すべてに入れる**（コストゼロ・数字リセットなし）。
> ※ S15 のみ STEP 0 で長尺の公開状態を確認するまで保留。

**S15 — `2Smc35dUF5c` → `LXFjJqE6vKU`** ⚠️*STEP 0 で長尺が public と確認できるまで投稿しない*
> The line between a bold promise and a crime came down to what the machines actually did in the room. The whole rise and fall: https://youtu.be/LXFjJqE6vKU

**S16 — `_TcVNCh2PlA` → `marQjsCagh0`**
> The four-day search was over before it started, and the warnings that came years earlier are the harder half of this story. Told in full: https://youtu.be/marQjsCagh0

**S04 — `AMZXUw3Arn0` → `waA4XJ9bYcE`**
> Where the money went is traceable — it runs through a single change in the code that let one account borrow without limit. Traced step by step: https://youtu.be/waA4XJ9bYcE

**S18 — `NLvlce3XCaw` → `5Jap-0h43A4`**
> The trillion came back in minutes; the explanation took years and ended at a bedroom in West London. Full account: https://youtu.be/5Jap-0h43A4

**S20 — `vLs3VaidXkI` → `1h267U6PY0I`**
> Thirteen works are still missing, and the empty frames left hanging on the museum wall are there for a reason. The whole case: https://youtu.be/1h267U6PY0I

**S05 — `O0mK6cK1iTs` → `sphERPA4gAc`**
> Those impossibly smooth returns plot onto a chart that should have ended it decades earlier. Why nobody stopped it: https://youtu.be/sphERPA4gAc

**S17 — `TxGQKxxzjfs` → `vikfOBHullI`**
> There was no blockchain behind it — just a database and a sales force — and billions moved anyway. How that worked: https://youtu.be/vikfOBHullI

**S19 — `jD5nQ2ARL-M` → `j8U8c4BB_GQ`**
> The route had a name, the "side door," and it ran through coaching staff rather than admissions offices. Laid out here: https://youtu.be/j8U8c4BB_GQ

**S21 — `rV-56tT8cMg` → `tt7U1XgjCU4`**
> Some of the money did surface years later, on a riverbank — and that find raised more questions than it closed. The full story: https://youtu.be/tt7U1XgjCU4

**S22 — `PpiUNN5QWQQ` → `mj9qEKPRatE`**
> Ninety-eight down to six wasn't a mistake, it was a negotiation — and what he actually pleaded to is narrower than most people assume. The whole story: https://youtu.be/mj9qEKPRatE

### 3-3. 投稿前セルフチェック（スクリプトの `--dry-run` で機械判定する）

| # | 条件 | 判定方法 |
|---|---|---|
| C1 | 22本すべて文面がユニーク | 文字列 set のサイズ == 22 |
| C2 | "subscribe" / "Subscribe" / "登録" を含まない | 部分一致検索でヒット0 |
| C3 | URL がちょうど1つ、形式は `https://youtu.be/` + 11文字 | 正規表現 `https://youtu\.be/[\w-]{11}` の出現回数 == 1 |
| C4 | 文数が1〜2 | `.` `?` `!` の後の空白で分割して ≤2 |
| C5 | 280文字以内 | `len(text) <= 280` |
| C6 | long_id が §2 表の値と一致 | JSON と本書の突合 |

---

## 4. 新規ショート用 末尾3秒CTA仕様

> ## ✅ IMPLEMENTED 2026-07-28
>
> **実装ファイル:** `remotion/src/compositions/Short.tsx`（コンポーネント1点のみ。データファイル・Root.tsx・既存ショートは無変更）
>
> ### 追加された props（`ShortData` の3フィールド・**すべて optional**）
>
> | prop | 型 | 既定 | 規格 |
> |---|---|---|---|
> | `ctaLongThumbSrc` | `string?` | なし（省略時カードを描画しない） | 対応長尺のサムネ。`remotion/public` からの相対パス。16:9（1280x720） |
> | `ctaLongTitle` | `string?` | なし（省略時タイトル行を描画しない） | 長尺タイトルの短縮版。**1行・半角36文字以内** |
> | `ctaHeadline` | `string?` | `'FULL CASE'` | UPPERCASE・2語以内・半角12文字以内 |
>
> ### 渡し方（`remotion/src/data/short<NN>.ts` の `SHORT<NN>` オブジェクトに3行足すだけ）
>
> ```ts
> export const SHORT60: ShortData = {
>   shortId: 'short60',
>   // …既存フィールドはそのまま…
>   ctaTextYT: '…',            // 据え置き（レガシーCTA用。新CTAでは使われない）
>   ctaTextTT: '…',            // 据え置き
>   ctaLongThumbSrc: 'shorts/short60/short60_ctathumb.png',  // 16:9
>   ctaLongTitle: 'They Fixed the Confession',               // 1行・36字以内
>   ctaHeadline: 'FULL CASE',                                // 省略可
>   beats: buildBeats(),
> };
> ```
>
> **切り替え条件:** 3つのうち**1つでも指定があれば**新CTA（長尺カード）を描画し、`SUBSCRIBE` は一切出さない。
> **3つとも省略すれば従来の `CtaLayer`（`SUBSCRIBE`）が動く。**
> `ctaLongThumbSrc` だけ無い場合はカードを省いて見出し＋タイトル＋ピルを出す（壊れた画像を出さない）。
>
> ### 後方互換の実証（自己申告ではなく実測）
>
> 変更前のコンポーネントと変更後のコンポーネントで `short57`（props未指定）の同一フレームを静止画書き出しし、**SHA-256 が3フレームとも完全一致**:
>
> | frame | 内容 | sha256（変更前＝変更後） |
> |---|---|---|
> | 1529 | CTAビート中（`SUBSCRIBE` カード） | `43c84491…4d9c0c40` |
> | 700 | 本編中（telop＋字幕） | `04d7a371…ec433c24` |
> | 1700 | loop tail | `20a70b47…3262bafbb` |
>
> ＝ **予約済みの short57/58/59 および過去公開分の再レンダーは1ピクセルも動かない。** `npx tsc --noEmit` は変更前後とも **0 errors**。
>
> ### 仕様どおり実装した項目
>
> §4-2 の3 props / §4-3 のタイムライン（全て秒指定→`Math.round(s * fps)`。フレーム直書きなし）/ スタッガー（カード0.13s → 見出し0.20s → タイトル0.40s → ピル0.67s → ブランド0.87s）/ 見出し・タイトルの `overflow:hidden` ＋ `translateY` マスク切り上がり / カード入りのみ `Trail layers=4 lagInFrames=1.0 trailOpacity=0.35` / 背景3レイヤー（暗幕・放射グロー・`AmbientMotion`）/ `sin(frame/22)*3px` の常時フロート（静止フレーム無し）/ opacity単独フェード無し / §4-4 のレイアウト数値と安全域 `x 80–1000` `y 300–1400` / `SUBSCRIBE` 文字列の完全排除。
>
> **字幕は仕様書より一歩進めた:** 「CTA区間に cue を置かない」を**データ側の手作業ではなくコンポーネントが機械的に保証**する。
> `ctaBeat` の窓に入る cue を `Short` が自動で落とすため、`short<NN>_timing.ts` 側の細工は不要。
> loop tail（CTAビートの後ろ）の cue は残る＝話し言葉のCTAは字幕としても出る。
>
> ### 実装できなかった / 意図的に変えた3点
>
> 1. **`CTA_SEC = 3.0` のビート長固定は実装していない（コンポーネントの守備範囲外）。**
>    short57–59 の実働経路ではビート尺は `build_short_mix.py` が出す `LINE_WINDOWS`（＝実ナレーション長）から算出される。
>    コンポーネント側で3秒に固定すると音声とズレる。**仕様書と実働経路が衝突しているので実働経路を採った。**
>    CTAアニメのタイミングは全て秒指定なので、ビート長が3秒でも5秒でも入りの動きは同一（余りはホールドに回る）。
>    3.00秒固定が必要なら**データ側（L5 の窓）で行うこと**。
> 2. **「最終フレームでカードが見えている状態で終わる」も不採用。** `SHORTS_METHOD` rule 5 の loop tail
>    （最終ビートでフック画に戻す）と衝突するため。CTAカードは `id === 'cta'` のビートにのみ出る。
>    ループの頭に戻ったときの残像はフック画で作る、という既存の設計を優先した。
> 3. **TikTok版のピルは `▶ FULL CASE` ではなく `▶ ON OUR PROFILE`。** 実際に描画すると
>    既定見出し `FULL CASE` と文字列が丸かぶりして間抜けだったため。§4-5 のナレーション差し替え
>    （"…is on our profile."）と揃い、外部プラットフォーム名も出していないのでルール上の問題はない。
>    戻したければ `Short.tsx` の1文字列。

**適用範囲:** 次に作るショート（short38〜）から。**既存22本には適用しない**（再レンダー＝再アップロード＝views/維持率リセット）。
**実装対象ファイル:** `remotion/src/compositions/Short.tsx` の `CtaLayer`（現行 356〜419行）を差し替える。
**環境:** 1080 x 1920 / **fps 30**（`remotion/src/brand.ts` の `BRAND.video.fps = 30`）。秒数はすべて fps から算出し、フレーム直書きはしない。

### 4-1. 現行の問題（コードを読んだうえでの指摘）

現行 `CtaLayer` は最終ビート（`beat.id === 'cta'`）に以下を出している:
- `PRIME DOCUMENTARY`（gold / 44px / letterSpacing 4）
- `ctaTextYT`（既定文言 `'Watch the full story on the channel'` / 78px）
- gold の丸ピル **`▶ SUBSCRIBE`**（40px）

問題は3点:
1. **`SUBSCRIBE` を出している。** §1 の実測では、ショート単体の視聴者は登録の意思決定をしない（22本で登録0）。
   1段飛ばしのCTAで、実際に0件だった。**この文字列を廃止する。**
2. **行き先が「the channel」＝抽象。** どの動画を見ればいいのか画面に無い。
3. **CTAビートの尺が可変。** short27 の CTA ビート（L5）は `59.182 → 62.34` ＝ **3.158秒**と、たまたま3秒前後になっているだけで、
   仕様として固定されていない。**3.00秒 = 90フレームに固定する。**

### 4-2. 型の追加（`ShortData` に3フィールド）

`remotion/src/compositions/Short.tsx` の `ShortData` に追加:

```ts
ctaLongThumbSrc?: string;   // 対応長尺のサムネ（staticFile相対 / 1280x720 の16:9）
ctaLongTitle?: string;      // 対応長尺のタイトル短縮版。半角36文字以内・1行。
ctaHeadline?: string;       // 既定 'FULL CASE'。UPPERCASE・2語以内・半角12文字以内。
```

`ctaTextYT` / `ctaTextTT` は**据え置き**（TikTok書き出しは従来どおり外部プラットフォーム名を出さない）。
**画面にURLは出さない**（ショート再生画面のURL文字列は押せず、覚えられない。行き先の受け皿は固定コメントと「関連動画」設定）。

### 4-3. タイムライン（CTAビート = 3.00秒 = 90f / 全区間記述）

`const CTA_SEC = 3.0;` `const F = (s: number) => Math.round(s * fps);`

| 区間 | フレーム | 何が起きるか |
|---|---|---|
| 0.00–0.13s | f0–f4 | 直前ビートの絵がそのまま残り、上に `ink` の暗幕が `opacity 0 → 0.72` で入る。**同時に scale 1.00 → 1.04**（opacity単独禁止のため） |
| 0.13–0.60s | f4–f18 | **長尺サムネカード**が入る。`spring({damping: 18, stiffness: 130, mass: 0.8})` で `scale 0.86 → 1.00` かつ `translateY +52px → 0` |
| 0.20–0.67s | f6–f20 | **見出し `FULL CASE`** が下からマスク切れ上がり。`overflow:hidden` + `translateY 110% → 0%`、`spring({damping: 20, stiffness: 130, mass: 0.7})` |
| 0.40–0.90s | f12–f27 | **長尺タイトル1行**がマスク切れ上がり。見出しと同じspring、**ディレイ 6f のスタッガー** |
| 0.67–1.10s | f20–f33 | **`▶ ON THE CHANNEL` ピル**が `translateY +24px → 0` ＋ `scale 0.9 → 1.0`、`spring({damping: 16, stiffness: 120})` |
| 1.10–3.00s | f33–f90 | 全要素ホールド。カード全体が `translateY = sin(frame / 22) * 3px` で微小フロート（静止フレームを作らない）。背景は `scale 1.04 → 1.08` の `Easing.out(Easing.cubic)` でゆっくり寄り続ける |
| 2.85–3.00s | f85–f90 | 何もフェードアウトさせない。**最終フレームでカード・見出し・タイトルが完全に見えている状態で終わる**（ループ再生の頭に戻ったとき残像が効く） |

**モーションブラー:** サムネカードの入り（f4–f18）のみ `@remotion/motion-blur` の `<Trail layers={4} lagInFrames={1.0} trailOpacity={0.35}>` で包む。
それ以外にはかけない（テキストにかけると可読性が落ちる）。

### 4-4. レイアウト（1080 x 1920 / 数値は px）

**セーフエリア:** YouTube Shorts の UI は **右端 x>840** と **下端 y>1500** を覆う。CTA要素はすべて `x 80–1000` / `y 300–1400` に収める。

| レイヤー | 要素 | 位置・サイズ | 書式 |
|---|---|---|---|
| L1（最背面） | 直前ビートの絵 ＋ `ink` 暗幕 opacity 0.72 | 全画面 | — |
| L2 | 放射グラデのグロー | `radial-gradient(70% 44% at 50% 41%, navy 0%, transparent 72%)` | — |
| L3 | 見出し `FULL CASE` | 中央揃え / top **430** / 高さ 110 | display font **88px** / letterSpacing **6** / gold `#E5B53A` / UPPERCASE・**12文字以内** |
| L4 | **長尺サムネカード** | 幅 **720** × 高さ **405**（16:9）/ left **180** / top **570** | 角丸 **18** / 枠 **6px solid gold** / `boxShadow 0 24px 64px ink` |
| L5 | 長尺タイトル1行 | 幅 840 / left 120 / top **1030** / 中央揃え | body font **46px** / weight 700 / white / **半角36文字以内・1行厳守**（2行になる長さは data 側で短縮する） |
| L6 | ピル `▶ ON THE CHANNEL` | 中央 / top **1130** / 高さ 76 / 横 padding 30 | 背景 gold / 文字 ink / display font **40px** / letterSpacing 2 |
| L7 | ブランド | `PRIME DOCUMENTARY` / 中央 / top **1250** | body font **36px** / letterSpacing 4 / gold 透明度 0.7 |

**`SUBSCRIBE` の文字列は全レイヤーから削除する。**
**字幕（`CaptionLayer`）は CTA 区間に cue を置かない**（`shortNN_timing.ts` の最終 LineWindow に caption を出力しない）。L4〜L6 が隠れるため。

### 4-5. ナレーション（末尾3秒に載せる音声）

| 項目 | 数値・規則 |
|---|---|
| 秒数 | **2.2〜2.6秒**。3.00秒のうち **末尾0.4〜0.8秒は無音**（カードだけが残る "間" を作る） |
| 語数 | **10〜16語** |
| 文字数 | **50〜85文字**（半角） |
| 構成 | **必ず2部構成。** ①そのショートが冒頭で出した問いを、答えの形で言い直す（1文） → ②`The full case is on the channel.` で閉じる |
| 禁止 | `subscribe` / `like` / `follow` / `hit the bell` / `link in bio`。**販促語は入れない** |
| 声・トーン | 本編ナレーションと同一ボイス・同一トーン。CTAだけ明るくしない（ドキュメンタリーの語り口を切らない） |

**書き方の例（short27 Rodriguez を使った場合）:**
> "The stop was over — and seven extra minutes made it unconstitutional. The full case is on the channel."
> （17語 / 101文字 → **やや長い。次のように削る**）
> "Seven extra minutes made that stop unconstitutional. The full case is on the channel."
> （14語 / 84文字 / 約2.4秒 ＝ 規格内）

**TikTok版（`platform === 'tiktok'`）:** ②を `The full case is on our profile.` に差し替え、**L6 のピルを `▶ FULL CASE` に変更**（外部プラットフォーム名を出さない現行ルールを維持）。L4 のサムネカードはそのまま使う。

### 4-6. 長尺への実際の接続（画面外の設定 / 公開時にオーナーが行う）

画面内のCTAだけでは遷移しない。**新規ショートは公開時に必ず以下2つを設定する。**

1. **固定コメント**（§3 と同じ書式で、そのショート専用に1本書き下ろす）。投稿は `scripts/post_short_pinned_comments.py`、ピン留めは手動（§実行手順 STEP 3 の制約と同じ）。
2. **「関連動画」設定** — YouTube Studio > 該当ショート > 詳細 > **関連動画** に対応長尺を指定する。
   ショート再生画面から長尺へ直接飛べる公式の導線で、**API不要・数字リセットなし**。
   ※ これは**新規ショートだけでなく既存22本にも今すぐ設定できる**（動画ファイルを触らないため）。
   STEP 3 のピン留め作業と同じタイミングでまとめてやると効率が良い。

### 4-7. 実装チェックリスト（Codex 向け・全項目コードで満たすこと）

- [ ] `CtaLayer` から `SUBSCRIBE` の文字列を削除した
- [ ] CTAビート長を `CTA_SEC = 3.0` に固定し、`framesFor(CTA_SEC, fps)` で算出している（フレーム直書きなし）
- [ ] すべての動きが `spring` または `Easing.out/inOut(Easing.cubic)`。等速線形が1つも無い
- [ ] opacity単独のフェードインが1つも無い（すべて translateY か scale と併用）
- [ ] 見出し／タイトル／ピルが 6f ずつのスタッガーで入る
- [ ] サムネカードの入りに `Trail`（layers 4 / lagInFrames 1.0 / trailOpacity 0.35）がかかっている
- [ ] 背景に最低3レイヤー（暗幕・放射グロー・`AmbientMotion`）が重なっている
- [ ] 見出しとタイトルが `overflow:hidden` + `translateY` のマスク切れ上がりで出る
- [ ] f33以降も `sin` フロートで静止フレームが無い
- [ ] 全要素が `x 80–1000` / `y 300–1400` に収まっている（Shorts UI と重ならない）
- [ ] CTA区間に caption cue が無い
- [ ] `platform === 'tiktok'` でピルが `▶ FULL CASE`、ナレーション末尾が `on our profile` になる

**確認方法:**
- プレビュー: `npm run studio`（`remotion/` で実行）→ composition `Short-short38-yt` の最後の90フレームを再生
- 単体書き出し: `npx remotion render Short-short38-yt out/short38_yt.mp4`
- TikTok版: `npx remotion render Short-short38-tt out/short38_tt.mp4`

---

## 5. 今後のショートのレーン方針

### 判定: **権利・警察レーン専業にする。犯罪・詐欺系ショートは新規制作を停止する。**

### 5-1. 根拠（すべて `_yt_analytics.json` 実測 / 2026-05-01〜07-18）

| 指標 | 権利・警察（n=12） | 犯罪・詐欺（n=10） | 差 |
|---|---|---|---|
| 合計再生数 | **1,068** | 272 | **3.93倍** |
| 1本あたり再生数 | **89.0** | 27.2 | **3.27倍** |
| 平均維持率（生値） | **70.7%** | 41.1% | 1.72倍 |
| 平均維持率（異常値4件を除外） | **57.2%**（n=10） | 38.5%（n=8） | 1.49倍 |
| 合計視聴時間 | **188分** | 9分 | **20.9倍** |
| 100再生超えの本数 | **5本**（199/188/149/145/125） | **0本**（最高87） | — |
| 10再生未満の本数 | **1本**（3） | **4本**（6/3/3/2） | — |

**最も強い証拠は「合計視聴時間 188分 vs 9分」＝ 20.9倍。**
再生数の差（3.9倍）だけでなく、**1再生あたりの深さも違う**。犯罪・詐欺系は「再生されても、ほとんど見られていない」。
権利レーンの上位3本（199 / 188 / 149 views）は**犯罪レーン10本の合計（272）を、3本で上回る**。

### 5-2. なぜ犯罪・詐欺系を「タイトルの書き直し」で救わないのか

`PACKAGING_FIX_v001.md` §2 が長尺で下したのと同じ判断を、ショートにも適用する。

- 犯罪レーンの最上位 S15 Theranos は **87 views**。これは権利レーンの**8位（54 views）と9位（38 views）の間**でしかない。
  **レーンの天井が、他方の中位に届いていない。**
- しかも S15 のタイトル `When Does a Bold Promise Become a Crime?` は疑問形＋抽象で、既に「良いフック」の形をしている。
  それで87に留まった＝**表現の問題ではなく需要の問題**。
- 逆に権利レーンの S09 `Can Police Take Your Property Without a Conviction?` は **13 views しか無いのに維持率82.9%**。
  ＝ **需要はあるが露出が回らなかっただけ**。こちらは打ち直す価値がある。

**結論: 表現を直せば伸びるのは権利レーン。犯罪レーンは表現を直しても土台が無い。**

### 5-3. 具体的な運用ルール（次のショートから）

| # | ルール | 数値根拠 |
|---|---|---|
| L1 | **新規ショートは権利・警察・行政による個人への強制力の話に限定する。** 詐欺・金融犯罪・未解決事件・企業不正はショート化しない | 1本あたり 89.0 vs 27.2 views |
| L2 | **主語は「あなた」または「ひとりの人物」。制度・組織・企業を主語にしない** | 上位5本すべてが `Police can / Can police …` の形。最上位の犯罪系 S15 だけが例外だが 87 で頭打ち |
| L3 | **タイトルは疑問形か「Police can 〜」の断定形。判例名は入れない** | 長尺 Kelo（判例名入り）維持率 1.55% ＝チャンネル最低（`PACKAGING_FIX_v001.md` §2） |
| L4 | **既に公開済みの犯罪・詐欺系10本は消さない・非公開にしない。** 固定コメントだけ入れて放置する | 272 views は既存資産。触ると数字がリセットされるが、コメント追加はリセットを起こさない |
| L5 | **長尺の犯罪・詐欺系は先にショートで需要を測ってから作る**（無料のA/Bテスト） | `PACKAGING_FIX_v001.md` §6-6 と同じ原則 |
| L6 | **例外の唯一の形:** 「予見された警告を無視した組織 vs 個人」の構造に落とせるものは可（例: Titan `_TcVNCh2PlA` 77 views・37.4%＝犯罪レーン2位）。この構造は L1 の「権力 vs 個人」と同型 | 犯罪レーン内で Titan だけが権利レーン下位と同水準 |

### 5-4. 次に作るべきショート（既存の長尺で、まだショートが無いもの）

§2 の突き合わせで、**EP025 以降の長尺には既にショートが用意されているが、2026-07-18 時点の analytics 47行に現れていない**
（＝公開直後または未公開）。以下は権利レーンかつ既に素材がある候補で、L1〜L3 に合致する:

| 候補 | ショート素材 | 長尺 | L1適合 |
|---|---|---|---|
| EP027 Rodriguez | `Ri1hlCBOjhc` | `tpAKfHKuwqY`（長尺で維持率 **42.5% ＝チャンネル最高**） | ◎ 交通停止＝二人称・警察 |
| EP028 Forfeiture | `8YxBH6zKals` | `YhEJHK279f8` | ◎ $40 で家を取られる |
| EP031 Unlock | `k26eTD3alnA` | `YQIhk2dKZHU` | ◎ 指紋 vs パスコード |
| EP032 Car search | `NMqzv7KcHdM` | `bXATF9ZnKLE` | ◎ 車内捜索 |
| EP033 Tyler | `gR6IpnynBzM` | `rU2vk9XL4vY` | ◎ 税滞納で家を没収 |
| EP034 Rolin | `smfqeisWRUo` | `6ozsIfwqrP0` | ◎ 空港での現金押収 |
| EP035 Hinders | `3rW-jeKH8Z0` | `Xc_PxdC_75c` | ◎ IRS の口座差押 |

**これら7本はすべて §4 の末尾3秒CTA仕様の適用対象になる**（まだ公開していない＝再アップロードのリスクが無いものは、
公開前にCTAを差し替えられる）。**STEP 0 で各本の公開状態を確認し、未公開のものは §4 を適用してから公開すること。**

---

## 付記 ─ 本書で行っていないこと

- YouTube API への書き込み: **なし**（コメント投稿・ピン留め・メタ更新・サムネ・公開設定、すべて未実施）
- 既存22本の再レンダー／再アップロード: **なし**
- ~~`remotion/src/compositions/Short.tsx` の変更: **なし**（§4 は仕様書であって、コードは未変更）~~
  → **2026-07-28 実装済み**（§4 冒頭の「✅ IMPLEMENTED」参照）。コード変更のみで、レンダー・アップロード・予約変更は一切していない。
- `scripts/post_short_pinned_comments.py` の作成: **なし**（STEP 1 でオーナー承認後に作成）

すべてオーナー承認後に実施。実施は **STEP 2 のパイロット3本 → 72時間観察 → 残り19本** の順を厳守すること。
