# Ship Gate (binding on every thread)

長尺エピソードは、独立ゲートが実レンダのバイト列を測定して緑の受領書を出すまで予約・投稿しない。自己申告の「完了」は禁止（CLAUDE invariant 13/15）。

- 手順: `check_final_acceptance.py <ep> --render <mp4> --emit-receipt` → `09_package/acceptance_receipt.v001.json`。
- 予約は `upload_schedule_case_v001.py --ep <slug>` のみ。受領書の `video_sha256` がファイルと一致しなければ投稿しない。
- チェックやしきい値を通すために緩めない。詳細は `docs/PD_SHIP_GATE.md`。

## 出荷判断は `config/ship_policy.v001.json`（オーナー指示 2026-08-12）

**測定は変えない。判断だけを変える。** `check_final_acceptance.py` は今までどおり全チェックを実行し、
全数値を計算し、全 hard failure を受領書に書く。変わったのは「どの failure が扉を閉めるか」で、
その判断は `scripts/pd_ship_policy.py` が policy を読んで下し、`upload_schedule_case_v001.py` が実行する。

- **止めてよいのは4クラスだけ**: `real_person_likeness` / `rights_and_licence` / `factual_support` /
  `fabricated_record`。ban・法務リスクで止める。**taste（作り込みの好み）では止めない。**
- 旧ルール（hard failure が `runtime_band` ＋ episode の `accepted_deviations` の部分集合の時だけ投稿）は
  **廃止**。5日間ゼロ投稿の直接原因で、2026-08-11 に挙がった7件のうち本物のリスクは1件だけだった。
- それ以外の failure は **出荷してよい。ただし必ず記録する**:
  `episodes/<EPID>/09_package/release_deviations.v001.json`
  （check id / 実測値 / しきい値 / なぜ止めなかったか / backlog）。
  実測値が取れないチェックは「取れない理由」を書く。**黙って落とすのは禁止。**
- `forbidden_subjects` は用語ごとに分ける。人物・権利・偽造記録を指す語（child, mugshot, watermark,
  readable document …）は BLOCKING。見た目の語（gavel, clock, courtroom …）は advisory。
  **未分類の語がヒットしたら止める**（`duc nguyen` のような実名が隠れるのはここ）。policy に1行足して解決する。
- blocking を通せる唯一の道は、**その話数の** `approvals/*.json`（target_type=edit / decision=approved* /
  `accepted_deviations` に check id）。advisory に承認は要らない（`decision_rights`）。
- 判断の説明だけが欲しい時（quota も回線も使わない）:
  `upload_schedule_case_v001.py --ep <slug> --explain-policy` / `pd_ship_policy.py --slug <slug>`。

**変えていない保護**（taste ではなく correctness。これらは緩めない）:
受領書の sha 一致 / `check_shipped_frames` のレビュー verdict / 重複タイトル・重複 RESULT の拒否 /
過去日 `publishAt` の拒否 / final_delivery の canonical sha 一致 / channel allowlist / quota 事前確認。

**今の検出力（2026-08-12 実測、正直に）**: 4クラスとも `partial`。likeness は接触シートを人が読む前提で
reviewer 欄は認証されない。rights は denylist のみで積極的なライセンス確認はゼロ。factual は
claims.v*.json が無い話数で `verify_onscreen_text` が skip → 受領書には `true` と載る。fabricated は
説明文の AI 開示文の substring テストだけ。`release_deviations` の `detector_gaps` に毎回書き出される。

### 生成プレート（板）の verdict → 出荷時にもう一度問う（2026-08-12 追加・BLOCKING）

**ゲートは欠けていなかった。誰も二度目を訊かなかった。** EP64 memphis は、レビュアーが REJECT した
プレート16枚が本編に切り込まれたまま予約され、数時間後に取り下げられた。実測した配線:
`scripts/check_plate_verdicts.py` は `check_episode_inputs.py` と `preflight_render_gate.py` の
**入力段**にのみ配線され、`check_final_acceptance.py` に**0回**、`upload_schedule_case_v001.py` にも
**0回**しか現れない。レンダーが終わった瞬間にプレートの問いは消え、受領書も shipped-frames も
アップロードの各ガードも緑になった。

`pd_ship_policy.plate_verdict_rows` がその問いを**出荷時に**戻す。

- **効くのは「REJECT され、かつ本編に切り込まれている」板だけ。** marmet は reject 9枚、correa は
  12枚あるが、全部ビルド前に再生成/除外されカットに1枚も無い＝この判定は両話に一切触れない。
  「記録されたが適用されていない却下」だけを捕まえる。判定は `cuts`＋`hook` の src を**stem**で
  照合する（i2v にかけた板は `<id>.mp4` として motion/ に移るため）。
- **クラスはレビュアーの理由テキストから読む。IDや勘で決めない。** ルールと順序は
  `config/ship_policy.v001.json` の `machine_contract.plate_reject_reasons`（コード側に定数を置かない）。
  memphis 実測: M049/M117=`real_person_likeness`（「reads as a depiction of」「unambiguously
  identifiable」）/ M159=`rights_and_licence`（generator watermark）/ M013/M202=`factual_support`
  （「states a fact the record does not」「the opinion does not record」）/ M079=`fabricated_record`
  （「glyphs resolve」＝読める生成文書）。
- **否定の手がかりを優先する**（`unless_any_of`）。M070「silhouetted, **not identifiable**」と
  M202「Faces are **not** visible, so R3 is clean; the failure is factual」は likeness に入れない。
  「child」という語だけで likeness に飛ばすのは誤り＝M202 は顔が写っておらず、欠陥は事実関係。
- **craft だけの理由は advisory**（continuity/framing/サムネ構図。memphis で10枚）。taste では止めない。
- **分類できない理由は fail closed** して `unclassified_plate_reject` で止める。`forbidden_subjects` の
  未分類語と同じ規則で、同じ理由（実名 `duc nguyen` が隠れていたのはそこ）。policy に1行足して解決する。
- **本編に入った `unresolved`（flag/pending/blank）は pass ではない**＝`unclassified_plate_verdict` で
  止める。理由テキストが無い以上どのクラスも晴れない。memphis は49枚がこれ。
- **verdict ファイルが無い話数は止めない・記録する。** 実測: ビルド済み film 45本中、
  `runs/qc/<slug>_plate_verdicts.v001.json` を持つのは8本のみ。無い37本で止めれば初日に全停止し、
  翌日にゲートごと切られる。`detector_gaps` に UNMEASURED として書き出す（`unmeasured_rows()` と同じ取引・
  同じ代償）。**代償は本物**: プレートを一度も見ていない話数は今でも出荷できる。
- **実測（2026-08-12）**: memphis=BLOCKING 55件（reject 6＋unresolved 49）・advisory 10件で `refuse`。
  verdict ファイルを持つ他の7本（marmet/greene/correa/hyatt/openfields/pinto/ramirez）は
  **この判定の blocking 0件・advisory 0件**。greene は `permit`。marmet と correa の blocking 1件は
  本判定ではなく既存の `packaging_claims[title]`。

**できないこと（正直に）**: **一度も画像を見ない。** `check_plate_verdicts.py` は自分の docstring で
そう明言しており、こちらはその**ファイルを読むだけ**でプレートは読まない。証明できるのは
「全板に verdict がある」「その verdict がディスク上のバイト列に bind されている」「reject/unresolved が
カットに入っていない」の3点だけ。**レビュアーが accept した板が実際に正しいかは、出荷経路上のどこも
再確認しない — 雑なレビューは丁寧なレビューと全く同じように通る。** クラス判定は理由文の部分一致なので、
新しい言い回しの理由は unclassified に落ちて（推測されず）止まる。

### タイトル/サムネ/説明文 → `scripts/check_packaging_claims.py`（2026-08-12 追加・BLOCKING）

「主張を台本と突き合わせる機械チェックは存在しない」は**もう正しくない**。同日、機械ルール（文字数・
疑問形・二人称・引用形式・記号）を**全部通過した虚偽タイトルが2本**出た（Central Park「Five Boys
Confessed on Camera」＝台本は Salaam が videotaped confession を与えていないと述べる／Norfolk
「Seven Sailors Signed Confessions」＝自白は4件、7人は**起訴**）。人が台本を読んで初めて気づいた。
その穴を埋めるのが本チェックで、`pd_ship_policy.py`（`factual_support` クラス）と
`apply_title_batch.py`（ライブ改題の直前）の両方に配線済み。

- **やること**: タイトル/サムネ文字/説明文から、数量・金額・期間・年月日・固有名・断定的な結末動詞を
  過剰に抽出し、その話数自身の記録（`03_script/script.en.v*.md` / captions / `01_research/claims.v*.json`
  / `*_facts.v*.json` / `_planning/EP*_<slug>_FACTS_LEDGER.v*.md`）と**文単位**で突き合わせる。
- **判定**: `SUPPORTED` 以外は全部 fail。`CONTRADICTED`（記録が否定）/ `NUMBER_MISMATCH`（同じ主語に
  別の数）/ `QUALIFIED_ONLY`（記録は「理論上の最大」等の留保付きでしか言っていない＝swartz の
  「35 YEARS FOR PAPERS.」）/ `FORBIDDEN_AS_FACT`（その話数の DO_NOT_STATE_AS_FACT）/
  `SUPPORTED_LEDGER_ONLY`（調査台帳にはあるがナレーションは一度も言っていない）/ `UNVERIFIED`。
  **UNVERIFIED は pass ではない** — これが「five」を「four と書かれた台本」で捕まえる仕組みそのもの。
- **出力**: 主張・判定・根拠行を `file:line` 付きで印字する。レビュアーが一目で検算できること。
- **HARD / SOFT**: 全 claim を抽出・検証・印字するが、扉を閉めるのは HARD のみ＝数値・金額・期間・
  日付・固有名・投票比、および outcome 語彙（confess/acquit/seize/die/land…）。一般の過去形
  （became / closed / chose）と説明文の UNVERIFIED は `note`（記録するが止めない）。説明文は
  4,000字の散文で言い換えが常態、そこで UNVERIFIED を55件出すと本命が埋まるため。`--strict` で両方 block。
- **実測（2026-08-12）**: 虚偽2本は両方 reject（Norfolk は script.en.v001.md:57 の
  "None of the three ever confessed" を引用／Central Park は :109 の
  "And Yusef Salaam gave no videotaped confession at all"）。同じ話数の**真**のタイトル
  「Seven Sailors Were Charged With One Murder.」は :59 を引用して pass。
  既知good 13本（ライブ通過12＋真タイトル）は claim 45件で hard fail 0・soft note 8。
  兄弟エージェントが見つけた4件（swartz サムネ / dbcooper "HE NEVER LANDED." / madoff "in 2000" /
  gardner "Emptied a Boston Museum"）は全て捕捉。ライブ57本＝claim 281件中 SUPPORTED 143、
  blocking 84（UNVERIFIED 71・CONTRADICTED 11・QUALIFIED_ONLY 2）、全通過は15本。
- **誤検知の主因は UNVERIFIED**（ライブ blocking の85%）。手検証したサンプルでは、台本が別の語で
  同じ事実を述べている例が多数（例: hinders は "seized" と "IRS" が別文／king の 2003 は台本にある）。
  **sharp な判定（CONTRADICTED / NUMBER_MISMATCH / QUALIFIED_ONLY）の方が精度が高い。**
  新規パッケージングでは「本編の文からタイトルを書く」だけで簡単に緑になる。
- **回帰テスト**: `tests/test_packaging_claims.py`（虚偽2本が通ったら / 真2本が落ちたら失敗する）。
- **できないこと（docstring にも明記）**: トーン・含意・「台本自体が間違っている主張」は判定できない。
  語幹と数の照合なので、記録が別の語で言い換えている真の主張は UNVERIFIED（誤検知）になり、
  正しい語が誤った関係で並ぶ文は SUPPORTED（見逃し）になる。**穴は縮んだだけで塞がっていない。
  緑を見た人間は、それでもタイトルを本編と突き合わせて読むこと。**

## 制作要件（変更なし）

- **アニメは制作要件として必須。ただし出荷は止めない。**（2026-08-23 に1文へ統合。
  直前まで「必須要件」と「advisory」が隣り合う2行に分かれて書かれており、
  どちらなのか読めなかった）
  - 作るとき: `CaseFilm` は設計トランジション＋モーションブラー(Trail)＋マスク切り上がり文字。
    紙芝居・左右スイープ線・黄ウォッシュ・ただのズームは不可。
  - 測るとき: `animation_density` が機械フロア。**下回っても出荷は止めず、
    `release_deviations.v001.json` に実測値を記録して backlog に積む**（4クラス以外は止めない）。
- 素材の被り: `footage_diversity`（distinct≥0.40／再利用≤4／天秤等の汎用象徴≤2）。advisory。
- 長尺の画像は原則 Codex（SDXLを勝手に起動しない）。例外(オーナー許可2026-07-05)=商用OK高品質ローカル(SD3.5 sd35_gen.py / SDXL gen_max.ps1)を「Codex画像の修正」「不足画像の緊急追加」に限り使用可。素のSDXL・FLUX-devは不可。実在肖像禁止/権利/provenanceは不変。詳細 `docs/SHORTS_IMAGE_QUALITY_DIRECTIVE.md`。
