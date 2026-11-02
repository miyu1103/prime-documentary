# EP77 引き継ぎ — 新しい道の1本目（設計スレへ）

**2026-08-23、再構築スレより。** EP77 はこのチャンネルで初めて「EP77の道」を走る話であり、
この話自体が再構築の受入検査でもある。以下の「---- ここから ----」以降を、
**設計を担当する新しいセッションにそのまま貼る。**

貼る側への注意：途中のセッションに足さない（文脈が大きいほど請求が増える・rule 20）。

---- ここから ----

あなたは Prime Documentary **EP77 の設計（左工程：spec → 事実台帳 → 台本）**を担当する。
リポジトリは `C:\Users\aab15\Documents\prime-documentary`。

## 0. 何が新しいか（1分で）

EP77 から制作の道が変わった（2026-08-23 オーナー指示・再構築完了・69テスト緑）。

- **入口は1コマンド**: `py -3.11 scripts/ep_road.py --slug keybridge --start 77`
  が骨組みを作り、以後いつでも `--slug keybridge` で「いまどこ・次に何・そのコマンド」が出る。
- **旧ルートは配線で封鎖済み**。関所2つ（[0/7] と [4d]）を通らないとレンダーに到達できない。
  頑張って回避する必要も、回避する方法も無い。**関所が要求する形で書けば、そのまま通る。**
- 検査は「レンダー後に赤を出す」から「**書いた時点で満たす**」に変わった。あなたが書く台本は、
  テンプレの型に沿っていれば、チャンネルで最も落ちてきた2つのゲート
  （retention 18/34話・structure 14/34話）を**構造的に**通る。

## 1. 題材（決定済み・変えない）

**EP77 = `keybridge` — ボルチモア Key Bridge 崩落（2024年3月）。**

- 根拠と拘束: `episodes/_planning/TOPIC_POOL_500.v001.md` **§2b「THE SIX — FINAL」**
  （2026-08-23 第3次・最終。§2 と §B は撤回済み、読み違えない）
- 需要実測: 中央値 307,441 / ≥10万再生 5ch / 20分超の最高 1,426,780
- 法的中心: 連邦裁判所の責任制限訴訟 ＋ 合衆国の船主・管理会社への請求。**係争中 = R3。**
- タイトル草案: 「The Ship Lost Power Four Times Before It Left the Berth. Baltimore Never Knew.」
  （§2c にサムネ案もある。ただしどちらも**一次資料で検証してから**使う——草案は仮説であって事実ではない）
- 着手前に **同ファイル §E「Before any of these is built」** を必ず読む（このスレの前提条件が書いてある）

## 2. 最初に打つコマンド（この順）

```bash
cd /c/Users/aab15/Documents/prime-documentary
git pull
py -3.11 scripts/ep_road.py --slug keybridge --start 77   # 骨組み生成（既にあれば現在地表示）
py -3.11 scripts/ep_road.py --slug keybridge              # 道の全景。以後これが羅針盤
```

`pd_brief.py` はセッション開始時に自動で出る（触ってはいけない実験中の動画52本などが載る）。

## 3. あなたの担当範囲（道の最初の3工程）

### 工程1: `episode_spec.v001.json`（機械が読む唯一の契約）

書き方: `docs/PD_EPISODE_SPEC_STANDARD.v001.md`。未宣言はエラー、既定値で埋まらない。
**EP77 からの新要件**: `ae_beats` が必須（decisions/0011・schema が強制）。

- `min_count` ≥ 12 / `per_act_min` ≥ 1 / `screen_seconds_min` ≥ 90
- `jobs_file`: `scripts/ae/jobs_keybridge.json`（実レンダーは後工程。宣言だけする）
- 各 beat: `id`(AE001形式) / `act`(section_vocabulary の語) / `kind`(hero_number,
  document_blowup, comparison, timeline, system_map, quote_card, map_move, list_build,
  title_card のいずれか) / `headline` / `source`（**事実台帳の行ID**）
- 検算: `py -3.11 scripts/check_episode_spec.py --slug keybridge`（げんこつは出ない。
  不備は名指しの問題行で返る）

### 工程2: `episodes/_planning/EP77_keybridge_FACTS_LEDGER.v001.md`

一次資料のみ（NTSB・裁判記録・公式発表）。係争中なので R3：
`forbidden_claims` に「裁判所がまだ認定していないこと」を明記し、台本は一切それを断定しない。
数字・日付・固有名は**全行に出典**。捏造検証の実例があるチャンネルなので、URLは自分で開いて確かめる。

### 工程3: 台本 — `episodes/_planning/EP77_keybridge_script.en.v001.md`

`--start` が**テンプレのコピー**を置いてある。それを**埋める**（別ファイルを作らない）。

- `{PLACEHOLDER}` が1つでも残ると関所が拒否する（未記入のコピーは台本と見なされない）
- **幕ごとに問いを1つ**。数ではなく間隔（ramirez は10問で落ち、greene は8問で通った。
  ゲートの実体は「160wpmで7分ごとに literal な `?`」）
- 見出し（`## HOOK` / `## ACT_1..` / `## ENDING`）は消さない——そのまま構成ゲートの節になる
- 語数は spec の宣言帯域から。**160 wpm で割る**（176 は楽観値・使うと1分50秒短い台本になる）
- 英語のみ（日本語が混ざるとナレ欠落バグ）。事実行には台帳の行IDをHTMLコメントで
- 自己検算（いつでも・何度でも・タダ）:
  ```bash
  py -3.11 scripts/check_script_retention_plan.py --slug keybridge
  py -3.11 scripts/check_ep77_standard.py --slug keybridge --stage inputs
  ```
- 台本は**3回パス**（R3）。ゲートは下限しか見ない。質はレビューでしか出ない

**完了条件**: `ep_road.py --slug keybridge` で `spec` `facts` `script` の3つに ✓ が付き、
`script` の行に「EP77 standard PASS」と出ること。そこまで行ったら HANDOVER を更新して切る。
以降（ナレ・画像・素材・組立）は別レーン。

## 4. やってはいけないこと

1. **配信カレンダーに触らない**（1スレ専有・PD_CANON §3。台帳が30本ずれた実績）
2. **レンダー・アップロードを始めない**（担当外。道の後工程）
3. **実験中の動画52本のタイトル/サムネに触らない**（9/07まで。pd_brief に一覧）
4. ゲートを通すために**しきい値・schema・宣言値を緩めない**（invariant 15）。
   通らないなら数字を添えて報告し、オーナー判断にする
5. `_finish_episode.sh` 等の実行中スクリプトを編集しない（編集前に実行中でないことを確認）
6. 生成済みの `03_script/script.en.v001.md` を直接編集しない（企画台本を直して再生成。
   EP62-66 はこれを怠って台帳と食い違った）

## 5. 規律（このリポジトリの流儀）

- 数字には必ず出所。書けないものは「測っていません」と書く
- 「たぶん・はず」禁止。確信が低いなら【未検証】
- 検査結果を使う前に「それは何を数えたか」を確認（計測器が嘘をついた実例が §7 に10件超）
- 詰まったら、それが再構築の最初の実地バグ。**回避せず記録して報告**（直すのは価値ある仕事）

## 6. 参照（必要になった時だけ開く）

| 何 | どこ |
|---|---|
| 題材の拘束・前提 | `episodes/_planning/TOPIC_POOL_500.v001.md` §2b・§2c・§E |
| spec の書き方 | `docs/PD_EPISODE_SPEC_STANDARD.v001.md` |
| 台本テンプレ原本 | `episodes/_planning/_EP_SCRIPT_TEMPLATE.v001.md` |
| 罠の全一覧 | `docs/PD_CANON.md` §7 |
| 再構築の全記録 | `docs/handover/2026-08-23-rebuild.md` |
| AE の決定 | `decisions/0011-AE-FROM-EP77.md` |

---- ここまで ----
