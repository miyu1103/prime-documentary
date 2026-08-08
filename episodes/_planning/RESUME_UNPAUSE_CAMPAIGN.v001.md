# 再開手順 — 非公開になった長尺を公開へ戻す作業 v001

**2026-08-07 · 前セッションから** · このセッションはサブエージェント上限（200体）を使い切って止まった。
**新しいチャットで再開すること。**このスレを continue しても上限は戻らない。
**レンダーは会話と独立したバックグラウンドプロセスなので、チャットを閉じても走り続ける。**

## 2026-08-09 実測チェックポイント（最新・ここから読むこと）

**残る非公開の長尺は willingham / norfolk / morton の3本だけ。**

- **flowers `PfdEpNQyaQQ` と postoffice `4FlCaOVpln0` は既に public**（API実測）。
  旧 `0iDUT0gzBiQ` / `0sjw_1OxCVk` は private・予約なしのまま残る（永久に公開されない）。
- **予約中の長尺は4本**: 8/9 burge `Iw-EPUD2nHg` / 8/11 fieldtest `KPYLtYYODLE` /
  8/12 lejeune `J97Rh1qOTPA` / 8/16 weimer `SpXTxT6nd24`。
- **`audit_films_vs_blocklist.py`: 40本中0本** がブロック素材を参照（Codexのfilm変更後も維持）。

### ⛔ いま作業を止めているもの：ディスク

```
C: 1.9TB中 空き31GB（99%使用）
TEMP 101.9GB — うち Adobe 77.3GB（最終更新 8/4、After Effects の一時領域）
RAM 90.9GB空き / GPU 21.7GB空き ← こちらは問題なし
```

willingham のレンダーが2回失敗。エラーは
`Error: Timed out after 30000ms while setting up the headless browser` —
**真因はブラウザの一時領域が作れないこと。** concurrency=4 の再試行も同じ理由で失敗。

**After Effects が起動中だったため、前セッションでは Adobe の一時領域に触っていない。**
選択肢は (a) AEを閉じてから8/4以降更新のないものを測って削除、
(b) 一時領域を別ドライブ（H:）へ逃がす。**どちらもオーナー承認が要る。**
ディスクが空くまで willingham / norfolk / morton は焼けない。

### Codex が並行で入れた変更（12コミット）

`git log --oneline -12` で確認できる。本作業に関係するもの:

- **`willingham_film.json` `norfolk_film.json` `morton_film.json` を変更している。**
  ブロックリスト監査は通っているが、レンダー前に `check_spec_satisfied` を再確認すること。
- **「ショートは長尺へのトラフィックをゼロしか送っていない」**（`7f7ef0b3`）。
  実測。対処は `docs/PD_SHORTS_RELATED_VIDEO_LINKING.v001.md` と
  `episodes/_planning/SHORTS_RELATED_LINK_WORKLIST.v001.md`。Studioでしか設定できない。
- **330本の全数目視で歩留まり15〜36%**（`74e9ae8d`）＋ `check_motion_integrity.py` 是正。
  「ゲートは中間を見られなかった」という指摘は本作業が踏んだのと同じ構造。

### このスレの失敗を全部記録した

**`docs/PD_RETRO_20260805_UNPAUSE.v001.md`** — 15件のミスと、それぞれの再発防止。
**再開前に §5「前セッションが踏んだ罠」より先にこれを読むこと**（より詳しく、実例つき）。
とくに:
- `film.json` の figure `start` は**ナレーション基準**。画面時刻は `+ hookSeconds + 3.5`。
  これを知らずに、きれいなエピソードを1時間止めた。
- 完了判定はログの `DONE` ではなく**成果物のタイムスタンプ**で行う（6日前のログを読んで誤報した）。
- 公開状況は**必ずAPI**。ローカルの `youtube_schedule_result` は更新されない。

---

## 2026-08-07 16:18 JST 実測チェックポイント

- **flowers**: 新マスター `flowers_final_bgm.v001.mp4`、1,945,066,444 bytes、
  SHA-256 `4c2913fd589fbee40dcd7233d3a122454c83786aee57c8c3f71a933382dacfd2`。
  完成品1436フレーム／325素材をper-source 17枚へ再構成し、独立読者B+Cが全17枚を原寸読了。
  4類型0件、shipped-frame PASS。新video `PfdEpNQyaQQ` を **8/10 12:00 JST** に予約済み。
  API上はprocessed 28:52、private + `publishAt=2026-08-10T03:00:00Z`。旧 `0iDUT0gzBiQ` はprivate・予約なしのまま。
- **postoffice**: 新video `4FlCaOVpln0` を **8/13 12:00 JST** に予約済み、processed 29:47。
  旧 `0sjw_1OxCVk` はprivate・予約なしのまま。
- **willingham**: blocklist後のmanifestは people=29 / motion=59。P01/P03/P26はimg・motionとも不在。
  film 231 cuts / distinct video 179、`check_spec_satisfied` PASS。新レンダーは未完了。
- **norfolk**: factory 230本を12枚にし、独立読者B+Cが全230タイルを原寸読了、4類型0件。
  `factory_clip_qc.v001.json` は230 accept、input preflight READY。新レンダーは未完了。
- **morton**: 現filmは動画264 cuts / distinct 221。Baku・Kashmir・Rebel・y2mate系は0。
  `episode_spec.v001.json` を実測221へ更新し、理由を `episode_spec_revision.v001.md` に記録。
  `check_spec_satisfied` PASS。新レンダーは未完了。
- **単一レンダーキュー**: PID 28220
  `render_queue.sh willingham:Ep51Willingham:51 norfolk:Ep53Norfolk:53 morton:Ep52Morton:52`。
  先に起動されていた別系統のEP62-65 review queue（lock PID 32296）の後ろで待機中。
  そのscript内には「owner asked」と記録されているが、本依頼の「判断待ち」と矛盾するため、
  本作業からは停止も変更もしていない。
  **別のrender_queueを起動しないこと。EP62-65をこの作業から停止しないこと。**
- 耐久修正: `pd_run.sh` はWindows PIDを記録し `/usr/bin:/bin` をPATHへ固定。
  `render_queue.sh` は `/usr/bin/bash` 固定。`_finish_episode.sh` はi2vコピー直後に
  img＋motion両poolのblocklist pruneを必ず再実行する。

残作業は willingham / norfolk / morton の新マスター完成後、各マスターでシートを再生成し、
**同一シートを2人の独立読者が全枚読む**こと。読了前にreviewed_sheetsへ書かない。

---

## 2026-08-09 04:15 JST 実測チェックポイント

- **インシデント**: 4類型違反の旧5本（willingham/morton/norfolk/flowers/postoffice旧）が
  public に戻っていた → 全5本 private へ復帰済み。詳細と残存リスクは
  `INCIDENT_20260809_OLD_UPLOADS_REPUBLISHED.v001.md`。**Codexの毎時ループが生きている間は再発しうる。**
- **flowers新 `PfdEpNQyaQQ` / postoffice新 `4FlCaOVpln0` は既に public**（予約日8/10・8/13を
  待たず公開されていた。両方とも審査PASS済みのため public のまま残置）。→ この2話は完了扱い。
- **willingham 8/8 00:10 の失敗の真因**: Remotion headless browser セットアップ30秒タイムアウト×2回。
  `pd_render_guarded.sh` の既定タイムアウトを120秒へ変更済み。
- **render_queue.sh の30時間デッドロックの真因**: 62行目の後段待機ループに死活チェックがなく、
  死んだPID 45388のロックを待ち続けた。stale-lock検出を後段ループにも追加済み。
- **現在のレンダー**: norfolk 仕上げジョブ（Codex系統、8/9 03:56起動）が進行中。
  その後ろに新キュー `render_queue.sh willingham:Ep51Willingham:51 morton:Ep52Morton:52` が待機。
  norfolk はこのキューから除外済み（二重レンダー回避）。
- **予約済み長尺（API実測）**: 8/9 burge / 8/11 fieldtest / 8/12 lejeune / 8/16 weimer。
  空き12:00枠 = 8/10・8/13・8/14・8/15。残り3話の目安: norfolk→8/13、willingham→8/14、morton→8/15。
- **flowers の verdict=UNREVIEWED は `--sheets-only` 再実行の副作用**。レビュー済みsha
  `4c2913fd…` は現マスターと一致（実測）。台帳復旧には非 sheets-only で再実行が必要（未実施）。
- **memphis (EP64)**: Codexが8/8にレンダー、マスター生成済みだがポストゲートFAILで停止中。
  本キャンペーン対象外。

---

## 0. まず状況を実データで確認する（推測しない）

```bash
cd /c/Users/aab15/Documents/prime-documentary
tail -3 out_render_queue.log            # レンダー待ち行列の現在地
py -3.11 scripts/audit_films_vs_blocklist.py | tail -1
for s in willingham norfolk morton flowers postoffice; do
  f=$(ls episodes/PD-2026-0*-$s/08_edit/${s}_final_bgm.v001.mp4 2>/dev/null)
  [ -n "$f" ] && echo "$s: $(stat -c %y "$f" | cut -c1-16)"
done
```

**マスターは必ずタイムスタンプで確認する。** 前セッションは `[finish:norfolk] DONE` というログを読んで
「完了」と判断したが、それは6日前の実行分だった。日付を見ずに古いマスターを審査しかけた。

公開状況は**ローカルのファイルではなくチャンネルAPI**を正とすること。前セッションはローカルの
古い日付を読んで「8/14と8/15は埋まっている」と誤報告した（実際は既に公開済みの別動画だった）。

---

## 1. いま何が起きているか

**2026-08-05、初めて完成品のフレームを実測する検査 `check_shipped_frames.py` を作った。**
1カットにつき4フレーム（20/60/85/95%）を完成品から抜く。従来は1クリップ1フレームだった。

**初回実行で11話中10話が不合格。** 実際に入っていたもの:

- 実在の子どもの顔（willingham 18:37、flowers 18:30-18:38）
- 他社作品の映像（morton — y2mate 由来と Rebel News。**著作権ストライク＝BAN 経路**）
- 実在人物の名札を別人に（burge「JON BURGE」を無関係の女性に、ほか5話）
- 実在の女子生徒2名（norfolk 3:21）
- 霊安室、ロンドンのバス、東京の警視庁 など

10本を予約から外した（**削除はしていない。日付を消しただけ**）。

**オーナーの判断（2026-08-06）**: 「妥協して予約してもいい」「進めてください」
「今非公開になってる動画は早急に公開できるようにしてほしい。全部。」

→ **画質面はすべて妥協して出す。** ただし**4類型だけは下げない**（オーナーの「BANされない」が根拠）:

1. 他社作品・スクレイプ映像（chyron / watermark / 他社字幕 / ripper由来のファイル名）
2. 実在の未成年が画面に映っている（**書類に子どもが描かれているのは該当しない**）
3. 実在人物の名札が、別の実在人物の上に乗っている
4. 実在の私人の個人情報が読める（氏名＋SSN、弁護士番号、住所）

---

## 2. 完了済み

| 日付 | 話 | 状態 |
|---|---|---|
| 8/7 | EP59 robosigning | ✅ 元マスターのまま復帰（全71シート読了・HARDゼロ） |
| 8/8 | EP60 surfside | ✅ 元マスターのまま復帰（全93シート読了・HARDゼロ） |
| 8/9 | EP55 burge | ✅ **修正版を再アップ** `Iw-EPUD2nHg`（旧 `Ew5bZNOk17E` は非公開のまま） |
| 8/11 | EP57 fieldtest | ✅ **修正版を再アップ** `KPYLtYYODLE`（旧 `FOdVK1qQE6w` は非公開のまま） |
| 8/12 | EP58 lejeune | ✅ 元から合格（唯一初回で通った話） |
| 8/16 | EP61 weimer | ✅ 元マスターのまま復帰。**R3の法務レビューは実施していない**（オーナーが続行を承認、APRに明記） |

**空いている日: 8/10・8/13・8/14・8/15**（8/4〜8/6 は過ぎたので埋められない）

---

## 3. 残り5本と、それぞれの状態

| 話 | マスター | 残作業 |
|---|---|---|
| **flowers** (EP54) | ✅ 8/7 04:00 新 | 目視 **17枚中5枚しか読めていない**（読了: 1,3,5,6,10）→ 残り12枚 |
| **postoffice** (EP56) | ✅ 8/7 06:11 新 | 目視ゼロ |
| **willingham** (EP51) | レンダー中 | 完了後に目視 |
| **norfolk** (EP53) | 待機列 | 〃 |
| **morton** (EP52) | 待機列 | 〃。**素材点数 221 / 宣言223 で2本不足**（バクー庁舎とカシミール新聞を除外したため）。`episode_spec` の宣言値を実測の221へ直し、理由を書く |

---

## 4. 1本を出すための手順（burge と fieldtest で2回通した確立手順）

```bash
# ① 目視用シートを作る（71枚→16枚に圧縮。全素材を1枚ずつカバー）
py -3.11 scripts/check_shipped_frames.py --slug <slug> --sheets-only
py -3.11 scripts/build_per_source_sheet.py --slug <slug>
#    → runs/qc/shipped_frames/<slug>_per_source/ に 16-19 枚

# ② 全部読む。判定は上の4類型だけ。読んだシートだけを reviewed_sheets に書く
#    runs/qc/<slug>_shipped_frames_review.v001.json
#      "coverage_mode": "per_source"   ← これを書くと素材単位カバーとして検証される
#      "render_sha256": <①が表示したsha>
#      "reviewed_sheets": [実際に開いたものだけ]
#      "rejected": {}
py -3.11 scripts/check_shipped_frames.py --slug <slug>     # PASS が出るまで

# ③ 納品記録を新しい版で作る（実測。前の版から写さない）
py -3.11 scripts/new_delivery_revision.py --slug <slug> --reason "..."

# ④ 受入ゲート
py -3.11 scripts/check_final_acceptance.py <EPID> --render <master> --emit-receipt

# ⑤ ④の hard_failures のうち既存APRが覆っていないものだけを APR-000N.json に書く
#    burge の APR-0002/0003、fieldtest の APR-0002 が文例。免除の前に必ず実測する

# ⑥ アップロード（旧動画を明示して差し替え）
py -3.11 scripts/upload_schedule_case_v001.py --ep <slug> --replaces <旧videoId> --dry-run
py -3.11 scripts/upload_schedule_case_v001.py --ep <slug> --replaces <旧videoId>
```

`--replaces` は「ガードを無視する」ではない。**指定した動画が非公開かつ予約解除済みでなければ拒否**する。
旧アップロードの記録（v001）は上書きせず、新しい版（v002）として書く。

**旧videoId**: willingham `dueMY2lSu8w` / morton `Gx_i5aMJWLM` / norfolk `6VL_mA6OiS0` /
flowers `0iDUT0gzBiQ` / postoffice `0sjw_1OxCVk`

---

## 5. 前セッションが踏んだ罠（同じ穴に落ちないこと）

- **`kill -0` は死んだWindowsプロセスを「生きている」と返す。** これでキューが50分空転した。
  `render_queue.sh` は `tasklist` に修正済み。他の場所で生存確認を書くときも同じ。
- **プロセス検索が自分自身に一致する。** `CommandLine -match 'comfy'` が自分のコマンドラインに当たり、
  「ComfyUIが復活し続ける」と誤診断した。**ポート（8188）や nvidia-smi で判定すること。**
- **却下したプレートは `img` と `motion` の両方にいる。** `P01.png` を外しても `P01.mp4` が残り、
  willingham の film ビルドが2回失敗した。`prune_pool_by_blocklist.py` は `--pool img`
  `--pool motion` も明示して回す。
- **キューを多重起動するとレンダーが並行して全部遅くなる。** ロックはそのためにある。
  再起動前に必ず `pkill -9 -f render_queue.sh`。
- **プールから消してもマニフェストは古いまま。** 必ず
  `build_asset_manifest_motionfirst.py` → `build_case_film_generic.py` の順で作り直す。
- **GPUの取り合い。** Remotion のレンダーは 4090 を要る。ComfyUI(i2v) が動いていると
  レンダーがゲートで abort する。i2v の再開手順は `EP62_greene_I2V_RESUME.v001.md`。
  監視プロセスが ComfyUI を再起動するので、**止めるときは監視を先に落とす。**

---

## 6. 未解決（オーナー判断待ち）

- **旧アップロード2本**（`Ew5bZNOk17E` burge旧、`FOdVK1qQE6w` fieldtest旧）が画面に非公開で残る。
  永久に公開されないが、消したければ削除できる。**取り消せない操作なので承認が要る。**
- **EP62 greene** — i2v変換 122/228 で停止中。再開手順は上記ファイル。
  完了後も**224本の全数目視が必須**（自動化は試して失敗した。理由もそのファイルに書いてある）。
- **EP63 correa** — 券の縁の矛盾（発注文「四辺直線」vs 正典 `C136`「三辺ギザギザ」）と、
  尺が上限32:00を約30秒超過。詳細は `EP63_correa_PLATE_QC_FINDINGS.v001.md`。
- **ショートが1日2本**予約されている（8/7〜8/20）。取り決めは1日1本。オーナーは「ショートはそのままでいい」
  と述べたので現状維持。

---

## 7. 最初にやること

1. §0 のコマンドで現在地を測る
2. **flowers の残り12枚を読む**（`runs/qc/shipped_frames/flowers_per_source/` の 2,4,7,8,9,11-17）
   → §4 の手順で **8/10** に入れる
3. postoffice を §4 の手順で **8/13** に
4. willingham・norfolk・morton をレンダー完了順に **8/14・8/15・8/17** へ

**目視は並列化すること。** 1枚のシートを2人の独立した読み手に読ませる体制が、今回の実害を
全部見つけている。単独で読むと枚数の壁で止まる（このセッションがそうなった）。
